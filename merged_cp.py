"""Company and product scored as one type: how much of the COMP/PROD error is the boundary between the two definitions?

Uses saved predictions only (no GPU). Gold and predicted COMP and PROD are both renamed CP; the span must still be exact.
Compared with the normal 3-type micro-F1 and with the CP-only F1.

  python merged_cp.py --data-dir ner_data --run s_all_rl --runs results/ner/runs --out results/ner/merged_cp.json
"""
import argparse, json
from ldred import ner_datasets as D

ap = argparse.ArgumentParser()
ap.add_argument("--data-dir", required=True); ap.add_argument("--runs", default="results/ner/runs")
ap.add_argument("--out", required=True)
ap.add_argument("--run", action="append", required=True, help="run folder; repeat. Optional label: name=folder")
a = ap.parse_args()
LIM = {"l_llama8b": 800, "l_llama70b": 300}


def sets(docs, preds, merge):
    g = {(i,) + (m["sent_id"], m["pos"][0], m["pos"][1], "CP" if merge and e["type"] in ("COMP", "PROD") else e["type"])
         for i, d in enumerate(docs) for e in d["entities"] for m in e["mentions"] if e["type"] in D.TARGET}
    p = {(i,) + tuple(x[:3]) + ("CP" if merge and x[3] in ("COMP", "PROD") else x[3],)
         for i, ps in enumerate(preds) for x in ps if x[3] in D.TARGET}
    return g, p


def f1(g, p, types=None):
    if types:
        g = {x for x in g if x[4] in types}; p = {x for x in p if x[4] in types}
    tp = len(g & p)
    return round(2 * tp / (len(g) + len(p)), 3) if g or p else 0.0


import random
out = {}
for spec in a.run:
    name, _, folder = spec.partition("=") if "=" in spec else (spec, "", spec)
    folder = folder or name
    for ds in ("fewnerd", "wnut17", "tweetner7"):
        try:
            preds = json.load(open(f"{a.runs}/{folder}/preds_{ds}.json"))
        except FileNotFoundError:
            continue
        docs = D.load(ds, a.data_dir, "test")
        if json.load(open(f"{a.runs}/{folder}/metrics.json")).get("args", {}).get("strip_markup"):
            from ldred.markup import strip_handles          # the run scored the text with the markup stripped
            docs = [strip_handles(d) for d in docs]
        if folder in LIM:
            docs = random.Random(13).sample(docs, min(LIM[folder], len(docs)))
        g3, p3 = sets(docs, preds, False); gm, pm = sets(docs, preds, True)
        out[f"{name}/{ds}"] = {"three_types": f1(g3, p3), "comp_prod_merged": f1(gm, pm),
                               "COMP": f1(g3, p3, {"COMP"}), "PROD": f1(g3, p3, {"PROD"}), "CP_merged_only": f1(gm, pm, {"CP"})}
json.dump(out, open(a.out, "w"), indent=1)
for k, v in out.items():
    print(k, v)
