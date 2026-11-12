"""Bootstrap confidence intervals for the LLM runs (the only systems whose predictions are saved per sentence).

Sentences are resampled with replacement; micro-F1 over PER/COMP/PROD is recomputed each time.
Also the paired difference 70B - 8B on the sentences both models were scored on.

  python bootstrap_llm.py --data-dir ner_data --out results/ner/bootstrap_llm.json
"""
import argparse, json, random
import numpy as np
from ldred import ner_datasets as D

ap = argparse.ArgumentParser()
ap.add_argument("--data-dir", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--runs", default="results/ner/runs"); ap.add_argument("--boots", type=int, default=2000)
a = ap.parse_args()
T = set(D.TARGET)


def counts(doc, pred):
    gold = {(m["sent_id"], m["pos"][0], m["pos"][1], e["type"]) for e in doc["entities"] for m in e["mentions"] if e["type"] in T}
    pred = {tuple(p) if len(p) == 4 else tuple(p[1:]) for p in pred}
    pred = {(s, x, y, t) for s, x, y, t in pred if t in T}
    return np.array([len(gold & pred), len(pred), len(gold)])


def f1(c):
    tp, p, g = c.sum(0)
    return 0.0 if tp == 0 else 2 * tp / (p + g)


def load_run(name, ds, test, limit, seed=13):
    docs = random.Random(seed).sample(test, min(limit, len(test)))
    preds = json.load(open(f"{a.runs}/{name}/preds_{ds}.json"))
    by_doc = {}
    for d, p in zip(docs, preds):
        by_doc[json.dumps(d["sents"])] = counts(d, p)
    return by_doc


rng = np.random.default_rng(13)
out = {}
for ds in ("fewnerd", "wnut17", "tweetner7"):
    test = D.load(ds, a.data_dir, "test")
    big = load_run("l_llama8b", ds, test, 800)
    small = load_run("l_llama70b", ds, test, 300)
    shared = [k for k in small if k in big]
    r = {"n70": len(small), "n8": len(big), "shared": len(shared)}

    def ci(x):
        return [round(float(np.percentile(x, 2.5)), 3), round(float(np.percentile(x, 97.5)), 3)]
    for name, runs, keys in (("llama8b_800", big, list(big)), ("llama70b_300", small, list(small)),
                             ("llama8b_on_shared", big, shared)):
        c = np.array([runs[k] for k in keys]); n = len(c)
        bs = [f1(c[rng.integers(0, n, n)]) for _ in range(a.boots)]
        r[name] = {"f1": round(float(f1(c)), 3), "ci95": ci(bs), "gold": int(c[:, 2].sum())}
    if shared:
        c8 = np.array([big[k] for k in shared]); c70 = np.array([small[k] for k in shared]); n = len(shared)
        diff = []
        for _ in range(a.boots):
            i = rng.integers(0, n, n)
            diff.append(f1(c70[i]) - f1(c8[i]))
        r["diff_70b_minus_8b"] = {"mean": round(float(np.mean(diff)), 3), "ci95": ci(diff)}
    out[ds] = r
json.dump(out, open(a.out, "w"), indent=1)
print(json.dumps(out, indent=1))
