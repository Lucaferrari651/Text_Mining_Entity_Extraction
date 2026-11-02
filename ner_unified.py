"""Train a token classifier on one or more NER datasets and evaluate it on several (cross-dataset transfer).

Unified types: PER, COMP (company), PROD (product), OTHER. Headline number = micro F1 over PER+COMP+PROD.

  # train on Few-NERD, test on all three (GPU, e.g. Colab T4)
  python3 ner_unified.py NER_DATA_DIR --train fewnerd --eval fewnerd,wnut17,tweetner7 --model roberta-base --out u_fewnerd_roberta
  # train on the two tweet sets, test on Few-NERD
  python3 ner_unified.py NER_DATA_DIR --train wnut17,tweetner7 --eval fewnerd --epochs 5 --out u_tweets_roberta

NER_DATA_DIR holds the jsonl files made by the Colab cell (fewnerd_train.jsonl, wnut17_test.jsonl, ...).
Writes <out>/metrics.json and <out>/preds_<set>.json. Fixed number of epochs, no model selection on the test sets.
"""
import argparse, json
from pathlib import Path
from ldred import metrics as M
from ldred import ner_datasets as D
from ldred.ner_transformer import train_and_predict

ap = argparse.ArgumentParser(); ap.add_argument("data_dir")
ap.add_argument("--train", required=True, help="comma-separated: fewnerd,wnut17,tweetner7")
ap.add_argument("--eval", required=True, help="comma-separated datasets to evaluate on")
ap.add_argument("--eval-split", default="test", choices=["validation", "test"])
ap.add_argument("--model", default="roberta-base"); ap.add_argument("--epochs", type=int, default=3)
ap.add_argument("--lr", type=float, default=3e-5); ap.add_argument("--batch-size", type=int, default=32)
ap.add_argument("--max-len", type=int, default=128); ap.add_argument("--seed", type=int, default=13)
ap.add_argument("--train-limit", type=int, help="max sentences per training dataset")
ap.add_argument("--eval-limit", type=int, help="max sentences per evaluation dataset")
ap.add_argument("--b2nerd-dir", help="B2NERD NER_en folder; needed to evaluate on crossner_ai,crossner_literature,crossner_music,"
                "crossner_politics,crossner_science (scored as PER/ORG/PROD, our COMP predictions count as ORG)")
ap.add_argument("--out", default="u_out"); ap.add_argument("--save-model", action="store_true")
a = ap.parse_args()

train = [d for n in a.train.split(",") for d in D.load(n, a.data_dir, "train", a.train_limit)]
dev = D.load(a.train.split(",")[0], a.data_dir, "validation", 1000)      # only for the per-epoch printout
ev = {n: D.load(n, a.b2nerd_dir if D.is_cross(n) else a.data_dir, a.eval_split, a.eval_limit) for n in a.eval.split(",")}
print("train", len(train), D.stats(train), flush=True)
out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
f1 = lambda preds: M.ner_f1(dev, preds, D.TARGET)["ALL"][2]
preds = train_and_predict(train, dev, a.model, str(out / "model") if a.save_model else None, a.epochs, a.lr,
                          a.batch_size, a.max_len, 0, a.seed, eval_fn=f1, log=lambda s: print(s, flush=True),
                          types=D.UNIFIED, eval_sets=ev)
res = {}
for name, docs in ev.items():
    cross = D.is_cross(name)
    scored = D.to_org_scale(preds[name]) if cross else preds[name]
    r = M.ner_f1(docs, scored, D.target_types(name))
    res[name] = {t: list(v) for t, v in r.items()}
    line = "  ".join(f"{t} F1={r[t][2]:.3f}" for t in (D.CROSS_TARGET if cross else D.UNIFIED) if t in r)
    print(f"{name:10s} [{a.eval_split}] {'PER+ORG+PROD' if cross else 'PER+COMP+PROD'} micro P={r['ALL'][0]:.3f} R={r['ALL'][1]:.3f} F1={r['ALL'][2]:.3f} | {line}")
    json.dump([sorted(map(list, p)) for p in preds[name]], open(out / f"preds_{name}.json", "w"))
json.dump({"args": vars(a), "results": res}, open(out / "metrics.json", "w"), indent=1)
