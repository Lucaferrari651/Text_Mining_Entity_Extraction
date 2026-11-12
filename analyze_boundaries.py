"""What kind of error is each missed mention?  From saved predictions only (no GPU).

For every gold mention of PER/COMP/PROD that is not found exactly (same span and type):
  wrong_type    same span, other type
  boundary      a prediction of the same type overlaps it with different boundaries (too long / too short / shifted)
  boundary+type a prediction of another type overlaps it with different boundaries
  missed        no prediction touches it
For every predicted mention that is not exact: spurious = overlaps no gold mention of any target type.
Also the F1 when a prediction of the right type that overlaps the gold counts as correct ("lenient F1", one gold per prediction).

  python analyze_boundaries.py --data-dir ner_data --run s_all_rl --run m_raw --out results/ner/boundaries.json
"""
import argparse, json, random
from collections import Counter
from ldred import ner_datasets as D
from ldred.markup import strip_handles

ap = argparse.ArgumentParser()
ap.add_argument("--data-dir", required=True); ap.add_argument("--runs", default="results/ner/runs")
ap.add_argument("--out", required=True); ap.add_argument("--run", action="append", required=True)
a = ap.parse_args()
LIM = {"l_llama8b": 800, "l_llama70b": 300}
T = set(D.TARGET)


def overlap(x, y):
    return x[0] == y[0] and x[1] < y[2] and y[1] < x[2]


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
        cat = {t: Counter() for t in sorted(T)}; spurious = Counter(); lenient_tp = 0; n_gold = 0; n_pred = 0; exact = 0
        for d, ps in zip(docs, preds):
            gold = [(m["sent_id"], m["pos"][0], m["pos"][1], e["type"]) for e in d["entities"] for m in e["mentions"] if e["type"] in T]
            pred = [tuple(x) for x in ps if x[3] in T]
            gset, pset = set(gold), set(pred)
            n_gold += len(gold); n_pred += len(pred); exact += len(gset & pset)
            used = set()
            for g in gold:
                if g in pset:
                    cat[g[3]]["exact"] += 1; used.add(g); continue
                same_span = [p for p in pred if p[:3] == g[:3]]
                ov = [p for p in pred if overlap(p, g)]
                if same_span:
                    cat[g[3]]["wrong_type"] += 1
                elif any(p[3] == g[3] for p in ov):
                    cat[g[3]]["boundary"] += 1
                    p = next(p for p in ov if p[3] == g[3])
                    if p not in used and p not in gset: used.add(p); lenient_tp += 1
                elif ov:
                    cat[g[3]]["boundary+type"] += 1
                else:
                    cat[g[3]]["missed"] += 1
            lenient_tp += sum(1 for g in gold if g in pset)
            for p in pred:
                if p not in gset and not any(overlap(p, g) for g in gold):
                    spurious[p[3]] += 1
        r = {"gold": n_gold, "pred": n_pred, "exact_f1": round(2 * exact / (n_gold + n_pred), 3),
             "lenient_f1": round(2 * lenient_tp / (n_gold + n_pred), 3),
             "per_type": {t: dict(c) for t, c in cat.items()}, "spurious_by_type": dict(spurious)}
        r["share_of_missed_gold"] = {k: round(v / max(1, sum(sum(c[x] for x in ("wrong_type", "boundary", "boundary+type", "missed")) for c in cat.values())), 3)
                                     for k, v in {k: sum(c[k] for c in cat.values()) for k in ("wrong_type", "boundary", "boundary+type", "missed")}.items()}
        out[f"{folder}/{ds}"] = r
json.dump(out, open(a.out, "w"), indent=1)
for k, v in out.items():
    print(k, "exact", v["exact_f1"], "lenient", v["lenient_f1"], v["share_of_missed_gold"], "spurious", sum(v["spurious_by_type"].values()), "of", v["pred"])
