"""Does the {@name@} markup explain the tweet drop?  CRF (CPU) trained on Few-NERD, scored on the TweetNER7 test set
as it is and with the markup stripped (same mentions, remapped).  Also: CRF trained and tested on tweets, raw vs stripped.

  python strip_markup_eval.py --data-dir ner_data --out results/ner/strip_markup.json
"""
import argparse, json
from ldred import ner_datasets as D
from ldred.metrics import ner_f1
from ldred.ner_crf import CRFTagger
from ldred.markup import strip_handles, count_handles

ap = argparse.ArgumentParser()
ap.add_argument("--data-dir", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--train-limit", type=int, default=20000)
ap.add_argument("--max-iter", type=int, default=60)
a = ap.parse_args()
T = D.TARGET


def score(model, docs):
    pred = [model.predict_doc(d) for d in docs]
    r = ner_f1(docs, pred, types=T)
    return {k: round(v[2], 3) for k, v in r.items() if k in T + ["ALL"]}


test = D.load("tweetner7", a.data_dir, "test")
test_s = [strip_handles(d) for d in test]
res = {"handle_tokens_in_test": count_handles(test)}
fn = D.load("fewnerd", a.data_dir, "train", limit=a.train_limit)
m = CRFTagger(max_iter=a.max_iter).fit(fn)
res["crf_fewnerd_to_tweetner7"] = {"raw": score(m, test), "stripped": score(m, test_s)}
tw = D.load("tweetner7", a.data_dir, "train")
m = CRFTagger(max_iter=a.max_iter).fit(tw)
res["crf_tweetner7_raw_train"] = {"raw": score(m, test), "stripped": score(m, test_s)}
m = CRFTagger(max_iter=a.max_iter).fit([strip_handles(d) for d in tw])
res["crf_tweetner7_stripped_train"] = {"raw": score(m, test), "stripped": score(m, test_s)}
json.dump(res, open(a.out, "w"), indent=1)
print(json.dumps(res, indent=1))
