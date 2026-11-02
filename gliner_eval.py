"""Zero-shot GLiNER on person / company / product (no training): same data and metric as ner_unified.py.

  pip install gliner
  python3 gliner_eval.py ner_data --eval fewnerd,wnut17,tweetner7 --model urchade/gliner_multi-v2.1 --out g_zero

The model sees the labels "person", "company", "product" as text and returns spans; labels the dataset has but GLiNER is
not asked about (locations, creative works, ...) count as O. Headline = micro F1 over PER+COMP+PROD, as in ner_unified.py.
`--threshold` is the only knob; it is fixed in advance (0.5) and not tuned on the test sets.
"""
import argparse, json
from pathlib import Path
from ldred import metrics as M
from ldred import ner_datasets as D
from ldred.gliner_ner import DEFAULT_LABELS, predict_docs

ap = argparse.ArgumentParser(); ap.add_argument("data_dir")
ap.add_argument("--eval", required=True, help="comma-separated: fewnerd,wnut17,tweetner7")
ap.add_argument("--eval-split", default="test", choices=["validation", "test"])
ap.add_argument("--model", default="urchade/gliner_multi-v2.1")
ap.add_argument("--threshold", type=float, default=0.5)
ap.add_argument("--labels", help="text labels for person,company,product in that order, e.g. 'person,organization,product'")
ap.add_argument("--eval-limit", type=int, help="max sentences per evaluation dataset")
ap.add_argument("--out", default="g_out")
a = ap.parse_args()

labels = DEFAULT_LABELS
if a.labels:
    names = [x.strip() for x in a.labels.split(",")]
    labels = dict(zip(names, ["PER", "COMP", "PROD"]))
from gliner import GLiNER                       # imported late so the file can be read/tested without the package
model = GLiNER.from_pretrained(a.model)
try:
    model = model.to("cuda")
except Exception:
    pass
out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
res = {}
for name in a.eval.split(","):
    docs = D.load(name, a.data_dir, a.eval_split, a.eval_limit)
    print(name, len(docs), "sentences", flush=True)
    preds = predict_docs(model, docs, labels, a.threshold, batch_log=lambda s: print(s, flush=True))
    r = M.ner_f1(docs, preds, D.TARGET)
    res[name] = {t: list(v) for t, v in r.items()}
    line = "  ".join(f"{t} F1={r[t][2]:.3f}" for t in D.TARGET if t in r)
    print(f"{name:10s} [{a.eval_split}] PER+COMP+PROD micro P={r['ALL'][0]:.3f} R={r['ALL'][1]:.3f} F1={r['ALL'][2]:.3f} | {line}")
    json.dump([sorted(map(list, p)) for p in preds], open(out / f"preds_{name}.json", "w"))
json.dump({"args": vars(a), "labels": labels, "results": res}, open(out / "metrics.json", "w"), indent=1)
