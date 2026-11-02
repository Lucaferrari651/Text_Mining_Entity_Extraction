"""Zero-shot GLiNER on person / company / product (no training): same data and metric as ner_unified.py.

  pip install gliner
  python3 gliner_eval.py ner_data --eval fewnerd,wnut17,tweetner7 --model urchade/gliner_multi-v2.1 --out g_zero

The model sees the labels "person", "company", "product" as text and returns spans; labels the dataset has but GLiNER is
not asked about (locations, creative works, ...) count as O. Headline = micro F1 over PER+COMP+PROD, as in ner_unified.py.
`--threshold` is the only knob; it is fixed in advance (0.5) and not tuned on the test sets.

CrossNER (from B2NERD, test only; pass --b2nerd-dir .../NER_en) is scored as PER / ORG / PROD: for those sets the labels are
"person", "organization", "product" (CrossNER has organizations, not companies).
"""
import argparse, json
from pathlib import Path
from ldred import metrics as M
from ldred import ner_datasets as D
from ldred.gliner_ner import DEFAULT_LABELS, CROSSNER_LABELS, predict_docs

ap = argparse.ArgumentParser(); ap.add_argument("data_dir")
ap.add_argument("--eval", required=True, help="comma-separated: fewnerd,wnut17,tweetner7")
ap.add_argument("--eval-split", default="test", choices=["validation", "test"])
ap.add_argument("--model", default="urchade/gliner_multi-v2.1")
ap.add_argument("--threshold", type=float, default=0.5)
ap.add_argument("--labels", help="text labels for person,company,product in that order, e.g. 'person,organization,product'")
ap.add_argument("--b2nerd-dir", help="B2NERD NER_en folder, needed for crossner_ai,crossner_literature,crossner_music,crossner_politics,crossner_science")
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
    cross = D.is_cross(name)
    docs = D.load(name, a.b2nerd_dir if cross else a.data_dir, a.eval_split, a.eval_limit)
    print(name, len(docs), "sentences", flush=True)
    use = CROSSNER_LABELS if cross else labels
    preds = predict_docs(model, docs, use, a.threshold, batch_log=lambda s: print(s, flush=True))
    types = D.target_types(name)
    r = M.ner_f1(docs, preds, types)
    res[name] = {t: list(v) for t, v in r.items()}
    line = "  ".join(f"{t} F1={r[t][2]:.3f}" for t in types if t in r)
    print(f"{name:10s} [{a.eval_split}] {'+'.join(types)} micro P={r['ALL'][0]:.3f} R={r['ALL'][1]:.3f} F1={r['ALL'][2]:.3f} | {line}")
    json.dump([sorted(map(list, p)) for p in preds], open(out / f"preds_{name}.json", "w"))
json.dump({"args": vars(a), "labels": labels, "results": res}, open(out / "metrics.json", "w"), indent=1)
