"""CRF check of the media-as-company mapping on CPU (Few-NERD, 20,000 training sentences): normal mapping vs media organisations counted as COMP.
Each mapping is trained and scored with its own definition, so the scores are about two definitions, not one model beating another.

  python crf_media.py --data-dir ner_data --out results/ner/crf_media.json
"""
import argparse, json
from ldred import ner_datasets as D
from ldred.metrics import ner_f1
from ldred.ner_crf import CRFTagger

ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--train-limit", type=int, default=20000); ap.add_argument("--max-iter", type=int, default=60)
a = ap.parse_args()
res = {}
for name, on in (("normal", False), ("media_as_company", True)):
    D.media_as_company(on)
    m = CRFTagger(max_iter=a.max_iter).fit(D.load("fewnerd", a.data_dir, "train", limit=a.train_limit))
    test = D.load("fewnerd", a.data_dir, "test")
    r = ner_f1(test, [m.predict_doc(d) for d in test], types=D.TARGET)
    res[name] = {k: round(v[2], 3) for k, v in r.items() if k in D.TARGET + ["ALL"]}
    res[name]["gold_COMP"] = sum(1 for d in test for e in d["entities"] if e["type"] == "COMP" for _ in e["mentions"])
D.media_as_company(False)
json.dump(res, open(a.out, "w"), indent=1); print(json.dumps(res, indent=1))
