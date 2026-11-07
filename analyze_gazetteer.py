"""How far does a company dictionary (e.g. DBpedia) go? Coverage, dictionary-only baseline, and a model + dictionary hybrid.

  python3 analyze_gazetteer.py ner_data --names dbpedia_companies.txt --datasets fewnerd,wnut17,tweetner7 --out gaz.md \
      [--system "RoBERTa=u_fewnerd_roberta" --system "GLiNER 0.8=g_zero_t08"] [--sample-from l_llama8b/metrics.json]

Per dataset (test split):
  A. Coverage: share of gold mentions of each unified type whose exact string is a dictionary entry. COMP split into strings
     seen / not seen in training and handle ({@name@}) / plain. Gold PRODUCT strings found in the company list show how often the
     dictionary alone would call a product a company.
  B. Dictionary-only baseline for COMP (--stoplist drops one-token matches of common non-entity words): precision / recall / F1 with every match accepted ('any') and with single-word matches
     restricted to capitalised tokens ('capitalised'); most frequent false matches with their gold label.
  C. Hybrid (needs --system with full-test prediction files): model alone, + dictionary matches where the model predicted nothing
     ('add'), + relabelling model spans that are exactly a dictionary entry to COMP ('relabel'). COMP F1 and the PER+COMP+PROD micro F1.
Note: Few-NERD is built from Wikipedia, so DBpedia coverage there is optimistic; the tweet datasets are the fair test.
"""
import argparse, collections, json
from pathlib import Path
from ldred import gazetteer as G
from ldred import metrics as M
from ldred import ner_datasets as D
from compare_ner import sample_indices


def text(doc, a, b):
    return " ".join(doc["sents"][0][a:b])


def gold_mentions(docs):
    return [(i, m["pos"][0], m["pos"][1], e["type"]) for i, d in enumerate(docs) for e in d["entities"] for m in e["mentions"]]


def pct(x, n):
    return f"{x / n:.0%}" if n else "-"


def load_preds(folder, name, n_docs, idx):
    p = Path(folder) / f"preds_{name}.json"
    if not p.exists():
        return None
    x = [{tuple(s) for s in doc} for doc in json.load(open(p))]
    if idx is not None and len(x) == n_docs:
        return [x[i] for i in idx]
    return x if len(x) == (n_docs if idx is None else len(idx)) else None


def prf_row(label, r, key="COMP"):
    p, rc, f = r.get(key, (0, 0, 0))
    return f"| {label} | {p:.3f} | {rc:.3f} | **{f:.3f}** |"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("data_dir"); ap.add_argument("--names", required=True)
    ap.add_argument("--datasets", default="fewnerd,wnut17,tweetner7"); ap.add_argument("--out")
    ap.add_argument("--system", action="append", default=[]); ap.add_argument("--sample-from")
    ap.add_argument("--no-legal-variants", action="store_true")
    ap.add_argument("--stoplist", action="store_true", help="never accept one-token matches of words that are almost never "
                    "entities in the training split (the, good, who, ...)")
    a = ap.parse_args()
    gaz = G.Gazetteer.from_file(a.names, add_legal_variants=not a.no_legal_variants)
    systems = [s.split("=", 1) for s in a.system]
    md = [f"Dictionary: {len(gaz)} normalised entries from `{Path(a.names).name}`.\n"]
    for name in a.datasets.split(","):
        test, train = D.load(name, a.data_dir, "test"), D.load(name, a.data_dir, "train")
        idx = None
        if a.sample_from:
            meta = json.load(open(a.sample_from))["args"]
            idx = sample_indices(len(test), meta["eval_limit"], meta["seed"])
            test_full, test = test, [test[i] for i in idx]
        train_comp = {text(d, a_, b_).lower() for d in train for a_, b_, t in
                      [(m["pos"][0], m["pos"][1], e["type"]) for e in d["entities"] for m in e["mentions"]] if t == "COMP"}
        stop = G.common_words(train) if a.stoplist else frozenset()
        gold = gold_mentions(test)
        md.append(f"# {name}\n\n## A. Coverage of gold mention strings by the dictionary\n")
        md.append("| Gold type | n | in dictionary |\n|---|---|---|")
        for T in D.UNIFIED:
            ms = [g for g in gold if g[3] == T]
            hit = sum(test[i]["sents"][0][a_:b_] in gaz for i, a_, b_, _ in ms)
            md.append(f"| {T} | {len(ms)} | {pct(hit, len(ms))} |")
        comp = [g for g in gold if g[3] == "COMP"]
        groups = {"seen in training": lambda s: s.lower() in train_comp, "not seen in training": lambda s: s.lower() not in train_comp,
                  "handle markup": lambda s: s.startswith("{@"), "plain text": lambda s: not s.startswith("{@")}
        md.append("\nGold COMP by kind:\n\n| Kind | n | in dictionary |\n|---|---|---|")
        for g, f in groups.items():
            ms = [x for x in comp if f(text(test[x[0]], x[1], x[2]))]
            md.append(f"| {g} | {len(ms)} | {pct(sum(test[i]['sents'][0][a_:b_] in gaz for i, a_, b_, _ in ms), len(ms))} |")
        md.append("\n## B. Dictionary-only baseline for COMP\n")
        md.append("| Variant | P | R | F1 |\n|---|---|---|---|")
        for sw in ("any", "capitalised"):
            preds = G.predict_docs(gaz, test, sw, stop=stop)
            md.append(prf_row(f"single-word matches: {sw}", M.ner_f1(test, preds, ("COMP",))))
        preds = G.predict_docs(gaz, test, "capitalised", stop=stop)
        fp = collections.Counter()
        for d, p in zip(test, preds):
            at = {(m["pos"][0], m["pos"][1]): e["type"] for e in d["entities"] for m in e["mentions"]}
            for _, a_, b_, _t in p:
                if at.get((a_, b_)) != "COMP":
                    fp[f"{text(d, a_, b_)} [gold: {at.get((a_, b_), 'none')}]"] += 1
        md.append("\nMost frequent false matches (capitalised variant): " + ", ".join(f"{s} ({c})" for s, c in fp.most_common(10)) + "\n")
        base = {}
        for label, folder in systems:
            P = load_preds(folder, name, len(test_full) if idx is not None else len(test), idx)
            if P is not None:
                base[label] = P
        if base:
            md.append("## C. Model + dictionary\n")
            md.append("| System | COMP P | COMP R | COMP F1 | PER+COMP+PROD F1 |\n|---|---|---|---|---|")
            for label, P in base.items():
                for variant, preds in [("model", P), ("+ add", G.hybrid(P, gaz, test, "add", stop=stop)),
                                       ("+ add + relabel", G.hybrid(P, gaz, test, "relabel", stop=stop))]:
                    r = M.ner_f1(test, preds, D.TARGET)
                    md.append(f"| {label} {variant} | {r['COMP'][0]:.3f} | {r['COMP'][1]:.3f} | **{r['COMP'][2]:.3f}** | {r['ALL'][2]:.3f} |")
        md.append("")
    out = "\n".join(md)
    print(out)
    if a.out:
        Path(a.out).write_text(out, encoding="utf-8")


if __name__ == "__main__":
    main()
