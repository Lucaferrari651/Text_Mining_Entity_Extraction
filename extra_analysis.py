"""Four CPU analyses on saved predictions of the RoBERTa-large (all three sets) runs.

  1. vote       majority vote (>= 2 of 3) over seeds 13, 14, 15
  2. combine    RoBERTa-large (seed 13) with Llama 3.3 70B on the 300 sentences the LLM was scored on: union, intersection
                (GLiNER predictions were not saved, so it cannot be combined)
  3. bootstrap  paired bootstrap over sentences for the differences between runs (2,000 resamples, 95% interval)
  4. confusion  gold type vs predicted type for the best run, as a figure (results/ner/confusion.png) and a table

  python extra_analysis.py --data-dir ner_data --out results/ner/extra_analysis.json --fig results/ner/confusion.png
"""
import argparse, json, random
from collections import Counter
import numpy as np
from ldred import ner_datasets as D
from ldred.markup import strip_handles

T = ("PER", "COMP", "PROD"); DS = ("fewnerd", "wnut17", "tweetner7")


def gold_set(d):
    return {(m["sent_id"], m["pos"][0], m["pos"][1], e["type"]) for e in d["entities"] for m in e["mentions"] if e["type"] in T}


def pred_set(ps):
    return {tuple(x[:3]) + (x[3],) for x in ps if x[3] in T}


def counts(gold, pred):
    return np.array([len(gold & pred), len(pred), len(gold)])


def f1(c):
    tp, p, g = np.asarray(c).sum(0) if np.ndim(c) > 1 else c
    return 0.0 if tp == 0 else float(2 * tp / (p + g))


def vote(sets, k=2):
    c = Counter(x for s in sets for x in s)
    return {x for x, n in c.items() if n >= k}


def overlap(x, y):
    return x[0] == y[0] and x[1] < y[2] and y[1] < x[2]


def confusion(golds, preds):
    """rows: gold PER/COMP/PROD and 'none' (prediction touching no gold mention); columns: predicted PER/COMP/PROD,
    'other span' (a prediction overlaps with different boundaries) and 'missed' (nothing overlaps)."""
    cols = list(T) + ["other span", "missed"]; rows = list(T) + ["none"]
    M = np.zeros((len(rows), len(cols)), int)
    for g, p in zip(golds, preds):
        spans = {(x[0], x[1], x[2]): x[3] for x in p}
        for x in g:
            if x[:3] in spans: M[rows.index(x[3]), cols.index(spans[x[:3]])] += 1
            elif any(overlap(x, y) for y in p): M[rows.index(x[3]), cols.index("other span")] += 1
            else: M[rows.index(x[3]), cols.index("missed")] += 1
        for y in p:
            if not any(overlap(y, x) for x in g): M[rows.index("none"), cols.index(y[3])] += 1
    return rows, cols, M


def paired_boot(ca, cb, boots, rng):
    n = len(ca); diffs = []
    for _ in range(boots):
        i = rng.integers(0, n, n)
        diffs.append(f1(cb[i].sum(0)) - f1(ca[i].sum(0)))
    d = np.array(diffs)
    return float(f1(cb.sum(0)) - f1(ca.sum(0))), [float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True); ap.add_argument("--runs", default="results/ner/runs")
    ap.add_argument("--out", required=True); ap.add_argument("--fig"); ap.add_argument("--boots", type=int, default=2000)
    a = ap.parse_args()
    P = lambda run, ds: json.load(open(f"{a.runs}/{run}/preds_{ds}.json"))
    out = {"vote": {}, "combine": {}, "bootstrap": {}, "confusion": {}}
    rng = np.random.default_rng(13); docs = {}
    for ds in DS:
        docs[ds] = D.load(ds, a.data_dir, "test")
        gold = [gold_set(d) for d in docs[ds]]
        seeds = [[pred_set(p) for p in P(r, ds)] for r in ("s_all_rl", "s_all_rl_seed14", "s_all_rl_seed15")]
        ens = [vote(t) for t in zip(*seeds)]
        out["vote"][ds] = {"seeds": [round(f1(sum(counts(g, p) for g, p in zip(gold, s))), 3) for s in seeds],
                           "majority_vote": round(f1(sum(counts(g, p) for g, p in zip(gold, ens))), 3)}
        # 2. RoBERTa + Llama 70B on the LLM sample
        idx = random.Random(13).sample(range(len(docs[ds])), 300)
        llm = [pred_set(p) for p in P("l_llama70b", ds)]
        rob = [seeds[0][i] for i in idx]; gs = [gold[i] for i in idx]
        sc = lambda ps: round(f1(sum(counts(g, p) for g, p in zip(gs, ps))), 3)
        out["combine"][ds] = {"roberta": sc(rob), "llama70b": sc(llm), "union": sc([x | y for x, y in zip(rob, llm)]),
                              "intersection": sc([x & y for x, y in zip(rob, llm)])}
        # 3. paired bootstrap
        cnt = lambda ps, g=gold: np.array([counts(x, y) for x, y in zip(g, ps)])
        base = cnt(seeds[0]); res = {}
        res["seed14 - seed13"] = paired_boot(base, cnt(seeds[1]), a.boots, rng)
        res["seed15 - seed13"] = paired_boot(base, cnt(seeds[2]), a.boots, rng)
        res["vote - seed13"] = paired_boot(base, cnt(ens), a.boots, rng)
        sdocs = [strip_handles(d) for d in docs[ds]]
        res["markup stripped - kept"] = paired_boot(base, cnt([pred_set(p) for p in P("s_all_rl_strip", ds)], [gold_set(d) for d in sdocs]), a.boots, rng)
        if ds != "fewnerd":      # media-as-company changes the Few-NERD gold, so only the tweet sets are comparable
            res["media as COMP - normal"] = paired_boot(base, cnt([pred_set(p) for p in P("s_all_rl_media", ds)]), a.boots, rng)
        out["bootstrap"][ds] = {k: {"diff": round(v[0], 3), "ci95": [round(v[1][0], 3), round(v[1][1], 3)]} for k, v in res.items()}
        # 4. confusion for the seed-13 run
        rows, cols, M = confusion([sorted(g) for g in gold], [sorted(p) for p in seeds[0]])
        out["confusion"][ds] = {"rows": rows, "cols": cols, "counts": M.tolist()}
        print(ds, out["vote"][ds], out["combine"][ds]); [print("  ", k, v) for k, v in out["bootstrap"][ds].items()]
    json.dump(out, open(a.out, "w"), indent=1)
    if a.fig:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        names = {"fewnerd": "Few-NERD", "wnut17": "WNUT-17", "tweetner7": "TweetNER7"}
        fig, axes = plt.subplots(1, 3, figsize=(16, 4.6))
        for ax, ds in zip(axes, DS):
            c = out["confusion"][ds]; M = np.array(c["counts"], float)
            pct = M / np.maximum(M.sum(1, keepdims=True), 1) * 100
            ax.imshow(pct, cmap="Blues", vmin=0, vmax=100)
            ax.set_xticks(range(len(c["cols"]))); ax.set_xticklabels(c["cols"], rotation=30, ha="right")
            ax.set_yticks(range(len(c["rows"]))); ax.set_yticklabels(["gold " + r if r != "none" else "no gold mention" for r in c["rows"]])
            for i in range(M.shape[0]):
                for j in range(M.shape[1]):
                    if M[i, j]: ax.text(j, i, f"{pct[i, j]:.0f}%\n({int(M[i, j])})", ha="center", va="center", fontsize=8, color="white" if pct[i, j] > 55 else "black")
            ax.set_title(names[ds])
        fig.suptitle("RoBERTa-large (all three sets, seed 13): what happens to each gold mention (row %, counts in brackets)", fontsize=11)
        fig.tight_layout(); fig.savefig(a.fig, dpi=160)
