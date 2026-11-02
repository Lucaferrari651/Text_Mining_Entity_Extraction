"""Why do the systems disagree with the gold annotation? Mismatch analysis from saved predictions (no model, no network).

  python3 analyze_mismatches.py ner_data --system "RoBERTa=u_fewnerd_roberta" --system "GLiNER 0.8=g_zero_t08" \
      --datasets fewnerd,wnut17,tweetner7 --out mismatches.md

Per dataset (test split, full-set prediction files preds_<dataset>.json) and per target type (COMP, PROD):
  A. gold profile: how many mentions, how many distinct strings, share lowercase-initial / multi-word / Twitter handle markup
     ({@name@}) / strings never seen in the training split;
  B. annotation consistency in the training split: strings that carry more than one type (company AND product, or a target type
     AND "other"), i.e. how much of the label is decided by context or by guidelines rather than by the string;
  C. what each system did with the gold mentions of each kind (found with the right type / same span other type / overlapping /
     missed), split by seen-in-training vs unseen and by handle vs plain;
  D. the most frequent gold strings that were confused or missed and the most frequent false positives;
  E. random examples (fixed seed): the sentence with the gold entity in bold, its gold type and what each system did.
"""
import argparse, collections, json, random
from pathlib import Path
from ldred import ner_datasets as D
from compare_ner import sample_indices

TYPES = ("COMP", "PROD")


def text(doc, a, b):
    return " ".join(doc["sents"][0][a:b])


def mentions(doc, only=None):
    return [(m["pos"][0], m["pos"][1], e["type"]) for e in doc["entities"] for m in e["mentions"]
            if only is None or e["type"] in only]


def string_labels(docs):
    """lowercased mention string -> Counter of unified types, over a split."""
    by = collections.defaultdict(collections.Counter)
    for d in docs:
        for a, b, t in mentions(d):
            by[text(d, a, b).lower()][t] += 1
    return by


def classify(pred, a, b, t):
    """Outcome for one gold mention given the system's set of (sent, start, end, type) for that sentence."""
    here = {p[3] for p in pred if p[1] == a and p[2] == b}
    if t in here:
        return "found"
    if here:
        return "same span, other type: " + "/".join(sorted(here))
    if any(p[1] < b and p[2] > a for p in pred):
        return "overlapping, other boundaries"
    return "missed"


def pct(x, n):
    return f"{x / n:.0%}" if n else "-"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("data_dir")
    ap.add_argument("--system", action="append", required=True, help='"label=folder" with full-test preds_<dataset>.json')
    ap.add_argument("--datasets", default="fewnerd,wnut17,tweetner7"); ap.add_argument("--out")
    ap.add_argument("--sample-from", help="metrics.json of the LLM run: restrict every system to the sentences the LLM saw")
    ap.add_argument("--examples", type=int, default=4); ap.add_argument("--seed", type=int, default=13)
    a = ap.parse_args()
    systems = [s.split("=", 1) for s in a.system]
    rng, md = random.Random(a.seed), []
    for name in a.datasets.split(","):
        test, train = D.load(name, a.data_dir, "test"), D.load(name, a.data_dir, "train")
        seen = string_labels(train)
        idx = None
        if a.sample_from:
            meta = json.load(open(a.sample_from))["args"]
            idx = sample_indices(len(test), meta["eval_limit"], meta["seed"])
        preds = {}
        for label, folder in systems:
            p = Path(folder) / f"preds_{name}.json"
            if p.exists():
                x = [{tuple(s) for s in doc} for doc in json.load(open(p))]
                if idx is not None and len(x) == len(test):
                    x = [x[i] for i in idx]
                elif len(x) != len(test if idx is None else idx):
                    continue
                preds[label] = x
        if idx is not None:
            test = [test[i] for i in idx]
        md.append(f"# {name}")
        for T in TYPES:
            gold = [(i, a_, b_) for i, d in enumerate(test) for a_, b_, t in mentions(d) if t == T]
            if not gold:
                continue
            strs = [text(test[i], a_, b_) for i, a_, b_ in gold]
            handle = [s.startswith("{@") for s in strs]
            unseen = [s.lower() not in seen for s in strs]
            md.append(f"\n## {name}: gold {T}\n")
            md.append(f"**A. Profile.** {len(gold)} mentions, {len(set(strs))} distinct strings; lowercase-initial "
                      f"{pct(sum(s[:1].islower() for s in strs), len(gold))}, multi-word {pct(sum(' ' in s for s in strs), len(gold))}, "
                      f"`{{@handle@}}` markup {pct(sum(handle), len(gold))}, string never seen in training "
                      f"{pct(sum(unseen), len(gold))}.")
            multi = {s: c for s, c in seen.items() if sum(c.values()) >= 3 and sum(1 for t in c if c[t]) > 1}
            both = sum(c["COMP"] + c["PROD"] for s, c in seen.items() if c["COMP"] and c["PROD"])
            oth = sum(c["COMP"] + c["PROD"] for s, c in seen.items() if (c["COMP"] or c["PROD"]) and c["OTHER"])
            allm = sum(c["COMP"] + c["PROD"] for c in seen.values())
            top = sorted(((s, c) for s, c in seen.items() if c["COMP"] and c["PROD"]), key=lambda x: -sum(x[1].values()))[:5]
            md.append(f"\n**B. Annotation consistency (training split).** Strings labelled both company and product cover "
                      f"{pct(both, allm)} of all COMP+PROD mentions; strings labelled COMP/PROD in some places and OTHER in others "
                      f"cover {pct(oth, allm)}. Examples (string: counts): "
                      + "; ".join(f"{s}: {dict((k, v) for k, v in c.items() if v)}" for s, c in top))
            md.append("\n**C. Outcome per system** (found = right span and type)\n")
            md.append("| System | group | n | found | other type | other boundaries | missed |\n|---|---|---|---|---|---|---|")
            cases = collections.defaultdict(list)
            for label, P in preds.items():
                groups = {"all": [True] * len(gold), "seen in training": [not u for u in unseen], "unseen": unseen}
                if any(handle):
                    groups.update({"handle markup": handle, "plain text": [not h for h in handle]})
                for g, flags in groups.items():
                    idx = [k for k, f in enumerate(flags) if f]
                    outs = collections.Counter()
                    for k in idx:
                        i, a_, b_ = gold[k]
                        o = classify(P[i], a_, b_, T)
                        outs[o.split(":")[0]] += 1
                        if g == "all":
                            cases[(label, o.split(":")[0])].append((i, a_, b_, o))
                    n = len(idx)
                    md.append(f"| {label} | {g} | {n} | {pct(outs['found'], n)} | {pct(outs['same span, other type'], n)} | "
                              f"{pct(outs['overlapping, other boundaries'], n)} | {pct(outs['missed'], n)} |")
            md.append("\n**D. Frequent strings**\n")
            for label, P in preds.items():
                miss = collections.Counter(strs[k] for k, (i, a_, b_) in enumerate(gold) if classify(P[i], a_, b_, T) != "found")
                conf = collections.Counter(f"{strs[k]} -> {classify(P[i], a_, b_, T).split(': ')[-1]}"
                                           for k, (i, a_, b_) in enumerate(gold)
                                           if classify(P[i], a_, b_, T).startswith("same span"))
                fp = collections.Counter()
                for i, pr in enumerate(P):
                    gold_at = {(a_, b_): t for a_, b_, t in mentions(test[i])}
                    for sid, a_, b_, t in pr:
                        if t == T and gold_at.get((a_, b_)) != T:
                            fp[f"{text(test[i], a_, b_)} [gold: {gold_at.get((a_, b_), 'none')}]"] += 1
                md.append(f"- {label}, gold {T} most often not found: " + ", ".join(f"{s} ({c})" for s, c in miss.most_common(8)))
                md.append(f"- {label}, gold {T} given another type: " + (", ".join(f"{s} ({c})" for s, c in conf.most_common(6)) or "-"))
                md.append(f"- {label}, false positives (predicted {T}, gold at that span in brackets): "
                          + (", ".join(f"{s} ({c})" for s, c in fp.most_common(8)) or "-"))
            md.append("\n**E. Examples for slides** (random gold mentions that at least one system got wrong; the gold entity is in bold)\n")
            wrong = [k for k, (i, a_, b_) in enumerate(gold)
                     if any(classify(P[i], a_, b_, T) != "found" for P in preds.values())]
            for k in rng.sample(wrong, min(a.examples, len(wrong))):
                i, a_, b_ = gold[k]
                toks = list(test[i]["sents"][0]); toks[a_] = "**" + toks[a_]; toks[b_ - 1] += "**"
                what = " | ".join(f"{label}: {classify(P[i], a_, b_, T)}" for label, P in preds.items())
                md.append(f"> {' '.join(toks)}\n>\n> Gold: **{T}** | {what}\n")
        md.append("")
    out = "\n".join(md)
    print(out)
    if a.out:
        Path(a.out).write_text(out, encoding="utf-8")


if __name__ == "__main__":
    main()
