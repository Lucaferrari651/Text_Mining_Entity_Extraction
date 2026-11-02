"""Error analysis of a mention-detection prediction file (preds_dev.json from ner_transformer.py).

  python3 analyze_ner_errors.py Linked-DocRED/Linked-DocRED ner_roberta/preds_dev.json [--type ORG] [--examples 12]

Each gold mention is: correct (same span + type), type error (same span, other type), boundary error (overlapping span, same
type), overlap + other type, or missed. Each predicted span that is not correct is the mirror case or spurious.
"""
import argparse, json
from collections import Counter, defaultdict
from ldred.data import load_split, mention_spans
from ldred.data import load_ner_preds

ap = argparse.ArgumentParser(); ap.add_argument("data_dir"); ap.add_argument("preds")
ap.add_argument("--split", default="dev"); ap.add_argument("--type"); ap.add_argument("--examples", type=int, default=10)
a = ap.parse_args()
docs, preds = load_split(a.data_dir, a.split), load_ner_preds(a.preds)
assert len(docs) == len(preds), "prediction file does not match the split"
overlap = lambda x, y: x[0] == y[0] and x[1] < y[2] and y[1] < x[2]
gold_c, pred_c = defaultdict(Counter), defaultdict(Counter)
confusion, ex = Counter(), defaultdict(list)
for doc, pred in zip(docs, preds):
    gold = set(mention_spans(doc))
    for g in gold:
        text = " ".join(doc["sents"][g[0]][g[1]:g[2]])
        if g in pred:
            kind = "correct"
        elif any(p[:3] == g[:3] for p in pred):
            kind = "type error"; confusion[(g[3], next(p[3] for p in pred if p[:3] == g[:3]))] += 1
        elif any(overlap(p, g) and p[3] == g[3] for p in pred):
            kind = "boundary error"
        elif any(overlap(p, g) for p in pred):
            kind = "overlap, other type"
        else:
            kind = "missed"
        gold_c[g[3]][kind] += 1
        if kind != "correct" and (not a.type or g[3] == a.type) and len(ex[(g[3], kind)]) < a.examples:
            near = [p for p in pred if overlap(p, g)]
            ex[(g[3], kind)].append((text, g[3], [(" ".join(doc["sents"][p[0]][p[1]:p[2]]), p[3]) for p in near]))
    for p in pred:
        if p in gold: kind = "correct"
        elif any(g[:3] == p[:3] for g in gold): kind = "type error"
        elif any(overlap(g, p) and g[3] == p[3] for g in gold): kind = "boundary error"
        elif any(overlap(g, p) for g in gold): kind = "overlap, other type"
        else: kind = "spurious"
        pred_c[p[3]][kind] += 1
print("GOLD mentions by outcome")
for t, c in sorted(gold_c.items()):
    n = sum(c.values()); print(f"  {t:5s} n={n:6d} " + "  ".join(f"{k} {v / n:.1%}" for k, v in c.most_common()))
print("PREDICTED spans by outcome")
for t, c in sorted(pred_c.items()):
    n = sum(c.values()); print(f"  {t:5s} n={n:6d} " + "  ".join(f"{k} {v / n:.1%}" for k, v in c.most_common()))
print("type confusions (gold -> predicted, same span):", confusion.most_common(8))
for (t, kind), items in sorted(ex.items()):
    print(f"\n[{t} / {kind}]")
    for text, gt, near in items:
        print(f"  gold {gt}: '{text}'  | predicted: {near}")
