"""Fine-tune a transformer for mention detection on Linked-DocRED (use a GPU, e.g. Colab T4).

  python3 ner_transformer.py DATA_DIR --model roberta-base --epochs 5 --out ner_roberta
  python3 ner_transformer.py DATA_DIR --model allenai/longformer-base-4096 --max-len 4096 --batch-size 2 --out ner_longformer

Writes <out>/preds_dev.json (one list of [sent, start, end, type] per dev document) and <out>/ner_metrics.json.
Fixed number of epochs, no model selection on dev (the dev F1 printed per epoch is only for information).
"""
import argparse, json
from pathlib import Path
from ldred.data import load_split
from ldred import metrics as M
from ldred.ner_transformer import train_and_predict

ap = argparse.ArgumentParser(); ap.add_argument("data_dir")
ap.add_argument("--model", default="roberta-base"); ap.add_argument("--epochs", type=int, default=5)
ap.add_argument("--lr", type=float, default=5e-5); ap.add_argument("--batch-size", type=int, default=8)
ap.add_argument("--max-len", type=int, default=512); ap.add_argument("--overlap", type=int, default=128)
ap.add_argument("--out", default="ner_out"); ap.add_argument("--limit-docs", type=int, help="quick test on N docs")
ap.add_argument("--no-save-model", action="store_true")
a = ap.parse_args()
train, dev = load_split(a.data_dir, "train"), load_split(a.data_dir, "dev")
if a.limit_docs:
    train, dev = train[:a.limit_docs], dev[:max(10, a.limit_docs // 5)]
out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
f1 = lambda preds: M.ner_f1(dev, preds)["ALL"][2]
preds = train_and_predict(train, dev, a.model, None if a.no_save_model else str(out / "model"), a.epochs, a.lr,
                          a.batch_size, a.max_len, a.overlap, eval_fn=f1, log=lambda s: print(s, flush=True))
res = M.ner_f1(dev, preds)
for t, (p, r, f) in sorted(res.items()):
    print(f"ner {t:5s} P={p:.3f} R={r:.3f} F1={f:.3f}")
json.dump([sorted(map(list, p)) for p in preds], open(out / "preds_dev.json", "w"))
json.dump({k: list(v) for k, v in res.items()}, open(out / "ner_metrics.json", "w"), indent=1)
