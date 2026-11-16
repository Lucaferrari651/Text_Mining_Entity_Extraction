"""Rule-based boundary repair on saved predictions (no GPU): does cutting "Inc." and "'s" off predicted spans help?

Rules (applied to predicted PER/COMP/PROD spans, the span must keep at least one token):
  possessive   drop a final token "'s", "’s" or "'"
  suffix       drop a final legal-form token (Inc, Inc., Ltd, Corp, Co, LLC, plc, ...) and a comma/full stop left behind (COMP only)
  article      drop a leading "the"
  ext_suffix   the opposite: add a following legal-form token (Inc, Ltd...) to a predicted COMP span
  ext_possessive  add a following "'s" to a predicted span
For each rule, run and dataset: micro-F1 before and after, how many predictions the rule changed, how many of those changed
predictions were exact before (harm) and became exact (gain). Also how often the GOLD spans themselves end in such a token:
the rule is only right where the dataset's annotators left these tokens out.

  python boundary_rules.py --data-dir ner_data --run s_all_rl --run m_raw --out results/ner/boundary_rules.json
"""
import argparse, json, random
from ldred import ner_datasets as D
from ldred.markup import strip_handles

POSS = {"'s", "’s", "'", "’"}
LEGAL = {"inc", "inc.", "ltd", "ltd.", "corp", "corp.", "co", "co.", "llc", "plc", "corporation", "incorporated", "limited", "company", "gmbh", "ag", "s.a.", "sa"}
T = set(D.TARGET)


def trim(span, toks, rule):
    sid, s, e, t = span
    w = toks[sid]
    if rule == "possessive":
        while e - s > 1 and w[e - 1] in POSS: e -= 1
    elif rule == "suffix" and t == "COMP":
        while e - s > 1 and (w[e - 1].lower() in LEGAL or w[e - 1] in {",", "."}):
            e -= 1
    elif rule == "article":
        if e - s > 1 and w[s].lower() == "the": s += 1
    elif rule == "ext_suffix" and t == "COMP":
        if e < len(w) and w[e].lower() in LEGAL: e += 1
    elif rule == "ext_possessive":
        if e < len(w) and w[e] in POSS: e += 1
    return (sid, s, e, t)


def f1(g, p):
    return round(2 * len(g & p) / (len(g) + len(p)), 3) if g or p else 0.0


def evaluate(docs, preds, rules):
    toks = [d["sents"] for d in docs]
    gold = {(i,) + (m["sent_id"], m["pos"][0], m["pos"][1], e["type"]) for i, d in enumerate(docs) for e in d["entities"] for m in e["mentions"] if e["type"] in T}
    pred = {(i,) + tuple(x[:3]) + (x[3],) for i, ps in enumerate(preds) for x in ps if x[3] in T}
    new, changed, harm, gain = set(), 0, 0, 0
    for p in pred:
        q = p
        for r in rules:
            q = (q[0],) + trim(q[1:], toks[q[0]], r)
        if q != p:
            changed += 1; harm += p in gold; gain += q in gold
        new.add(q)
    return {"before": f1(gold, pred), "after": f1(gold, new), "changed": changed, "were_exact": harm, "became_exact": gain}, gold, toks


def gold_endings(gold, toks):
    c = {"possessive": 0, "suffix": 0, "article": 0, "n_comp": 0}
    for (i, sid, s, e, t) in gold:
        w = toks[i][sid]
        c["n_comp"] += t == "COMP"
        c["possessive"] += e - s > 1 and w[e - 1] in POSS
        c["suffix"] += t == "COMP" and e - s > 1 and w[e - 1].lower().rstrip(".") in {x.rstrip(".") for x in LEGAL}
        c["article"] += e - s > 1 and w[s].lower() == "the"
    return c


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True); ap.add_argument("--runs", default="results/ner/runs")
    ap.add_argument("--out", required=True); ap.add_argument("--run", action="append", required=True)
    a = ap.parse_args()
    LIM = {"l_llama8b": 800, "l_llama70b": 300}
    out = {}
    for folder in a.run:
        for ds in ("fewnerd", "wnut17", "tweetner7"):
            try:
                preds = json.load(open(f"{a.runs}/{folder}/preds_{ds}.json"))
            except FileNotFoundError:
                continue
            docs = D.load(ds, a.data_dir, "test")
            meta = json.load(open(f"{a.runs}/{folder}/metrics.json")).get("args", {}) if folder not in LIM else {}
            if meta.get("strip_markup"):
                docs = [strip_handles(d) for d in docs]
            if folder in LIM:
                docs = random.Random(13).sample(docs, min(LIM[folder], len(docs)))
            res = {}
            for name, rules in [("possessive", ["possessive"]), ("suffix", ["suffix"]), ("article", ["article"]),
                                ("ext_suffix", ["ext_suffix"]), ("ext_possessive", ["ext_possessive"])]:
                res[name], gold, toks = evaluate(docs, preds, rules)
            res["gold_spans_with_token"] = gold_endings(gold, toks)
            out[f"{folder}/{ds}"] = res
            print(folder, ds, {k: (v["before"], v["after"]) for k, v in res.items() if k != "gold_spans_with_token"}, res["gold_spans_with_token"])
    json.dump(out, open(a.out, "w"), indent=1)
