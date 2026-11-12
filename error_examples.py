"""Five real examples for each cause of error, taken from saved predictions (random with a fixed seed).

  python error_examples.py --data-dir ner_data --out results/ner/error_examples.md
"""
import argparse, json, random
from ldred import ner_datasets as D
from ldred.markup import HANDLE

ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--runs", default="results/ner/runs"); ap.add_argument("--n", type=int, default=5)
a = ap.parse_args()
T = set(D.TARGET); rng = random.Random(13)


def load(ds, split="test"):
    return D.load(ds, a.data_dir, split)


def preds(run, ds):
    return json.load(open(f"{a.runs}/{run}/preds_{ds}.json"))


def span(doc, s, x, y):
    return " ".join(doc["sents"][s][x:y])


def sent(doc, s, x, y):
    w = doc["sents"][s]; return " ".join(w[:x] + ["[[" + " ".join(w[x:y]) + "]]"] + w[y:])


def gold(doc):
    return [(m["sent_id"], m["pos"][0], m["pos"][1], e["type"], e["raw_type"] if "raw_type" in e else "") for e in doc["entities"] for m in e["mentions"] if e["type"] in T]


def pick(rows):
    return rng.sample(rows, min(a.n, len(rows)))


out = ["# Real examples for each cause of error", "",
       "Taken from saved predictions with a fixed seed (13). The mention in `[[double brackets]]` is the gold (or predicted) one.", ""]

# 1. markup (TweetNER7, RoBERTa-base trained on Few-NERD, test as it is)
tw, pr = load("tweetner7"), preds("m_raw", "tweetner7"); rows = []
for d, p in zip(tw, pr):
    pp = {tuple(x) for x in p}
    for g in gold(d):
        if HANDLE.match(span(d, g[0], g[1], g[2])) and g[3] in ("COMP", "PROD") and (g[0], g[1], g[2], g[3]) not in pp:
            rows.append((d, g))
out += ["## 1. The `{@name@}` markup: the Wikipedia-trained model does not find it (RoBERTa-base, TweetNER7)", ""]
out += [f"- gold **{g[3]}**: `{span(d, *g[:3])}`. {sent(d, *g[:3])}" for d, g in pick(rows)] + [""]

# 2. never seen in training (WNUT-17, gold company or product missed by the large model)
train = {" ".join(d["sents"][0][m["pos"][0]:m["pos"][1]]).lower() for d in load("wnut17", "train") for e in d["entities"] for m in e["mentions"] if e["type"] in ("COMP", "PROD")}
w, pr = load("wnut17"), preds("s_all_rl", "wnut17"); rows = []
for d, p in zip(w, pr):
    pp = {tuple(x) for x in p}
    for g in gold(d):
        if g[3] in ("COMP", "PROD") and (g[0], g[1], g[2], g[3]) not in pp and span(d, *g[:3]).lower() not in train:
            rows.append((d, g))
out += ["## 2. A name never seen in training (WNUT-17, RoBERTa-large trained on all three sets)", ""]
out += [f"- gold **{g[3]}**: `{span(d, *g[:3])}` (not in the WNUT-17 training set). {sent(d, *g[:3])}" for d, g in pick(rows)] + [""]

# 3. wrong type (TweetNER7, same span, other type)
pr = preds("s_all_rl", "tweetner7"); rows = []
for d, p in zip(tw, pr):
    pp = {tuple(x[:3]): x[3] for x in p}
    for g in gold(d):
        t = pp.get(g[:3])
        if g[3] in ("COMP", "PROD") and t in ("COMP", "PROD") and t != g[3]:
            rows.append((d, g, t))
out += ["## 3. Same words, other label: company or product? (TweetNER7, RoBERTa-large)", ""]
out += [f"- gold **{g[3]}**, predicted **{t}**: {sent(d, *g[:3])}" for d, g, t in pick(rows)] + [""]

# 4. boundaries (Few-NERD, prediction overlaps a gold company/product with other boundaries)
fn, pr = load("fewnerd"), preds("s_all_rl", "fewnerd"); rows = []
for d, p in zip(fn, pr):
    pl = [tuple(x) for x in p]
    for g in gold(d):
        if g[3] in ("COMP", "PROD") and (g[0], g[1], g[2], g[3]) not in pl:
            for q in pl:
                if q[3] == g[3] and q[0] == g[0] and q[1] < g[2] and g[1] < q[2]:
                    rows.append((d, g, q)); break
out += ["## 4. Right type, other boundaries (Few-NERD, RoBERTa-large)", ""]
out += [f"- gold **{g[3]}** `{span(d, *g[:3])}`, predicted `{span(d, *q[:3])}`. {sent(d, *g[:3])}" for d, g, q in pick(rows)] + [""]

# 5. media organisations are OTHER in the gold but the model says company
rows = []
for d, p in zip(fn, pr):
    for e in d["entities"]:
        if e["raw_type"].startswith("organization-media"):
            for m in e["mentions"]:
                if any(x[3] == "COMP" and x[1] == m["pos"][0] and x[2] == m["pos"][1] for x in p):
                    rows.append((d, m))
out += ["## 5. Media organisations (BBC, newspapers) are not companies in Few-NERD: the model says COMP", ""]
out += [f"- gold OTHER (`organization-media/newspaper`), predicted COMP: {sent(d, m['sent_id'], *m['pos'])}" for d, m in pick(rows)] + [""]
open(a.out, "w", encoding="utf-8").write("\n".join(out))
print("\n".join(out))
