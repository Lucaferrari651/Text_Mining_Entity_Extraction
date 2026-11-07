"""Does detection get worse when the sentence has few entities? Recall and false positives by entity density (no model, no network).

  python3 analyze_density.py ner_data --system "RoBERTa=u_fewnerd_roberta" --system "GLiNER 0.8=g_zero_t08" \
      --datasets fewnerd,wnut17,tweetner7 --out density.md [--sample-from l_llama8b/metrics.json]

Idea from the information-density paper (arXiv 2604.18944): density of a sentence = gold entity tokens (all entity types) / all tokens.
It is computed from the gold annotation, so it is an analysis variable, not something a system can use at test time.
Sentences are split into: 'no target entity' (no gold person / company / product; only false positives can happen there), and three
equal-sized groups by density (low / middle / high) among the sentences that have at least one target mention.
Per system and group: recall of gold PER / COMP / PROD mentions (exact span and type) and false positives per 100 sentences
(predicted PER / COMP / PROD span that is not a gold mention of that type).
"""
import argparse, json
from pathlib import Path
from ldred import ner_datasets as D
from compare_ner import sample_indices

TARGET = ("PER", "COMP", "PROD")


def density(doc):
    """Gold entity tokens (all types) divided by sentence length."""
    n = len(doc["sents"][0])
    return sum(b - a for e in doc["entities"] for m in e["mentions"] for a, b in [m["pos"]]) / n if n else 0.0


def has_target(doc):
    return any(e["type"] in TARGET for e in doc["entities"])


def thresholds(docs):
    """Density cut points that split the sentences with a target mention into three equal-sized groups."""
    ds = sorted(density(d) for d in docs if has_target(d))
    return ds[len(ds) // 3 - 1], ds[2 * len(ds) // 3 - 1]


def group(doc, cuts):
    if not has_target(doc):
        return "no target entity"
    d = density(doc)
    return "low density" if d <= cuts[0] else "middle density" if d <= cuts[1] else "high density"


GROUPS = ["no target entity", "low density", "middle density", "high density"]


def score(docs, preds, cuts):
    """{group: {'sent', 'gold': Counter by type, 'found': Counter, 'fp'}} for one system."""
    out = {g: {"sent": 0, "len": 0, "gold": dict.fromkeys(TARGET, 0), "found": dict.fromkeys(TARGET, 0), "fp": 0} for g in GROUPS}
    for doc, pred in zip(docs, preds):
        r = out[group(doc, cuts)]
        r["sent"] += 1; r["len"] += len(doc["sents"][0])
        gold = {(m["pos"][0], m["pos"][1], e["type"]) for e in doc["entities"] for m in e["mentions"] if e["type"] in TARGET}
        for _, _, t in gold:
            r["gold"][t] += 1
        mine = {(s[1], s[2], s[3]) for s in pred if s[3] in TARGET}
        for g in gold & mine:
            r["found"][g[2]] += 1
        r["fp"] += len(mine - gold)
    return out


def pct(x, n):
    return f"{x / n:.0%}" if n else "-"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("data_dir")
    ap.add_argument("--system", action="append", required=True)
    ap.add_argument("--datasets", default="fewnerd,wnut17,tweetner7"); ap.add_argument("--out")
    ap.add_argument("--sample-from", help="metrics.json of an LLM run: restrict every system to the sentences it saw")
    a = ap.parse_args()
    systems = [s.split("=", 1) for s in a.system]
    md = []
    for name in a.datasets.split(","):
        docs = D.load(name, a.data_dir, "test")
        idx = None
        if a.sample_from:
            meta = json.load(open(a.sample_from))["args"]
            idx = sample_indices(len(docs), meta["eval_limit"], meta["seed"])
        preds = {}
        for label, folder in systems:
            p = Path(folder) / f"preds_{name}.json"
            if p.exists():
                x = [{tuple(s) for s in doc} for doc in json.load(open(p))]
                if idx is not None and len(x) == len(docs):
                    x = [x[i] for i in idx]
                elif len(x) != len(docs if idx is None else idx):
                    continue
                preds[label] = x
        if idx is not None:
            docs = [docs[i] for i in idx]
        if not preds:
            continue
        cuts = thresholds(docs)
        sc = {label: score(docs, P, cuts) for label, P in preds.items()}
        first = next(iter(sc.values()))
        md.append(f"# {name} ({len(docs)} sentences)\n")
        md.append(f"Density cut points (gold entity tokens / tokens): low <= {cuts[0]:.3f} < middle <= {cuts[1]:.3f} < high.\n")
        md.append("| Group | sentences | mean length | gold PER / COMP / PROD | System | recall PER | recall COMP | recall PROD | recall all | false positives per 100 sentences |")
        md.append("|---|---|---|---|---|---|---|---|---|---|")
        for g in GROUPS:
            n, ln = first[g]["sent"], first[g]["len"]
            gold = first[g]["gold"]
            for label, s in sc.items():
                r = s[g]
                tot_g, tot_f = sum(r["gold"].values()), sum(r["found"].values())
                md.append(f"| {g} | {n} | {ln / n:.1f} | {gold['PER']} / {gold['COMP']} / {gold['PROD']} | {label} | "
                          f"{pct(r['found']['PER'], r['gold']['PER'])} | {pct(r['found']['COMP'], r['gold']['COMP'])} | "
                          f"{pct(r['found']['PROD'], r['gold']['PROD'])} | {pct(tot_f, tot_g)} | {100 * r['fp'] / n:.1f} |")
        md.append("")
    out = "\n".join(md)
    print(out)
    if a.out:
        Path(a.out).write_text(out, encoding="utf-8")


if __name__ == "__main__":
    main()
