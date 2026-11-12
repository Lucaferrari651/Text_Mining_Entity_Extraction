"""Manual review of "false positives": predicted PER/COMP/PROD mentions that touch no gold mention (Ford, Disney... are they really not entities?).

make:   python review_sheet.py make  --data-dir ner_data --run s_all_rl --per-set 50 --out results/ner/review_sheet.csv
score:  python review_sheet.py score --sheet reviewed.csv [--run s_all_rl]      (two reviewers fill columns reviewer_a and reviewer_b)

Reviewer values: yes = the predicted text really is a mention of that type (the gold annotation missed it), no = not an entity or wrong type, unsure.
"""
import argparse, csv, json, random
from collections import Counter
from ldred import ner_datasets as D

T = set(D.TARGET)
SETS = ("fewnerd", "wnut17", "tweetner7")
FIELDS = ["id", "dataset", "pred_type", "sentence", "reviewer_a", "reviewer_b", "note"]


def overlap(p, g):
    return p[0] == g[0] and p[1] < g[2] and g[1] < p[2]


def spurious(docs, preds):
    out = []
    for i, (d, ps) in enumerate(zip(docs, preds)):
        gold = [(m["sent_id"], m["pos"][0], m["pos"][1]) for e in d["entities"] for m in e["mentions"] if e["type"] in T]
        for p in ps:
            if p[3] in T and not any(overlap(p, g) for g in gold):
                out.append((i, tuple(p)))
    return out


def mark(sent, a, b):
    return " ".join(sent[:a] + ["[[" + " ".join(sent[a:b]) + "]]"] + sent[b:])


def make(a):
    rows, rng = [], random.Random(13)
    for ds in SETS:
        docs = D.load(ds, a.data_dir, "test")
        preds = json.load(open(f"{a.runs}/{a.run}/preds_{ds}.json"))
        sp = spurious(docs, preds)
        for i, p in rng.sample(sp, min(a.per_set, len(sp))):
            rows.append({"id": f"{ds}-{i}-{p[1]}-{p[2]}", "dataset": ds, "pred_type": p[3],
                         "sentence": mark(docs[i]["sents"][p[0]], p[1], p[2]), "reviewer_a": "", "reviewer_b": "", "note": ""})
    rng.shuffle(rows)                                  # reviewers do not see which dataset comes next
    with open(a.out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, FIELDS); w.writeheader(); w.writerows(rows)
    print(len(rows), "rows ->", a.out)


def kappa(x, y):
    n = len(x)
    po = sum(i == j for i, j in zip(x, y)) / n
    cx, cy = Counter(x), Counter(y)
    pe = sum(cx[k] * cy[k] for k in set(cx) | set(cy)) / n ** 2
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def score(a):
    rows = [r for r in csv.DictReader(open(a.sheet, encoding="utf-8-sig")) if r["reviewer_a"].strip() and r["reviewer_b"].strip()]
    norm = lambda v: v.strip().lower()
    A, B = [norm(r["reviewer_a"]) for r in rows], [norm(r["reviewer_b"]) for r in rows]
    res = {"rows_reviewed": len(rows), "agreement": round(sum(i == j for i, j in zip(A, B)) / len(rows), 3), "cohen_kappa": round(kappa(A, B), 3)}
    res["share_yes_by_reviewer"] = {"a": round(A.count("yes") / len(A), 3), "b": round(B.count("yes") / len(B), 3)}
    both = [r for r, x, y in zip(rows, A, B) if x == y]            # only agreed labels decide
    res["per_dataset"] = {}
    for ds in SETS:
        sub = [(r, x) for r, x in zip(both, [norm(r["reviewer_a"]) for r in both]) if r["dataset"] == ds]
        if sub:
            res["per_dataset"][ds] = {"n_agreed": len(sub), "share_yes": round(sum(x == "yes" for _, x in sub) / len(sub), 3)}
    # what would the score be if the "yes" cases were in the gold? uses the run's own counts
    if a.run:
        bnd = json.load(open(a.counts))
        for ds, v in res["per_dataset"].items():
            c = bnd[f"{a.run}/{ds}"]
            exact_f1, gold, pred = c["exact_f1"], c["gold"], c["pred"]
            tp = exact_f1 * (gold + pred) / 2
            fp_spur = sum(c["spurious_by_type"].values())
            x = v["share_yes"] * fp_spur                               # estimated spurious predictions that are right
            v["estimated_f1_if_yes_were_gold"] = round(2 * (tp + x) / (gold + x + pred), 3)
            v["exact_f1_now"] = exact_f1
    print(json.dumps(res, indent=1))
    if a.out:
        json.dump(res, open(a.out, "w"), indent=1)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("make"); m.add_argument("--data-dir", required=True); m.add_argument("--runs", default="results/ner/runs")
    m.add_argument("--run", default="s_all_rl"); m.add_argument("--per-set", type=int, default=50); m.add_argument("--out", required=True)
    s = sub.add_parser("score"); s.add_argument("--sheet", required=True); s.add_argument("--run"); s.add_argument("--out")
    s.add_argument("--counts", default="results/ner/boundaries.json")
    a = ap.parse_args()
    make(a) if a.cmd == "make" else score(a)
