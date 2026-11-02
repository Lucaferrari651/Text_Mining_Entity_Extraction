"""Step 2 (offline): evaluate search-based linking from the cache written by fetch_wiki_candidates.py.

  python3 run_wiki_eval.py DATA_DIR --cache wiki_cache_dev.json [--out results]

Part A  gold entities     -> linking quality alone
Part B  predicted entities (CRF mentions + rule coreference) -> what the full pipeline achieves
Compared: Wikipedia search vs Wikidata search, paper-style rank-sum vs our probability-sum aggregation,
and the combination with the train-set alias dictionary.
"""
import argparse, json, pickle
from pathlib import Path
from ldred.data import load_split, wiki_target, wikidata_target, NOT_LINKABLE
from ldred import metrics as M
from ldred.coref import cluster
from ldred.linking import (PriorIndex, FuzzyIndex, CacheIndex, rank_entity, rank_entity_ranksum, merge_ranked)

ap = argparse.ArgumentParser(); ap.add_argument("data_dir"); ap.add_argument("--cache", required=True)
ap.add_argument("--out", default="results")
ap.add_argument("--ner-preds", help="preds_dev.json from ner_transformer.py (default: train/use the CRF)")
a = ap.parse_args()
cache = json.loads(Path(a.cache).read_text(encoding="utf-8"))
train, dev = load_split(a.data_dir, "train"), load_split(a.data_dir, "dev")
fuzzy = FuzzyIndex(PriorIndex().fit(train))
wp, wd = CacheIndex(cache, "wikipedia"), CacheIndex(cache, "wikidata")

# every method: name -> (function names -> ranked list, which gold id to compare with)
methods = {
    "Wikipedia search, rank-sum (paper)": (lambda n: rank_entity_ranksum(n, wp), wiki_target),
    "Wikipedia search, prob-sum":         (lambda n: rank_entity(n, wp), wiki_target),
    "Wikidata search, rank-sum (paper)":  (lambda n: rank_entity_ranksum(n, wd), wikidata_target),
    "Wikidata search, prob-sum":          (lambda n: rank_entity(n, wd), wikidata_target),
    "Wikipedia search + dictionary":      (lambda n: merge_ranked(rank_entity(n, fuzzy), rank_entity_ranksum(n, wp)), wiki_target),
}
res = {"gold_entities": {}, "predicted_entities": {}}
fmt = lambda s: " ".join(f"{k}={v:.3f}" for k, v in s.items())

# ---- Part A: gold entities
ents = [e for d in dev for e in d["entities"] if e["type"] not in NOT_LINKABLE]
missing = {m["name"].strip().lower() for e in ents for m in e["mentions"]} - cache.keys()
print(f"gold entities: {len(ents)}  | mention strings missing from cache: {len(missing)}")
for name, (fn, tgt) in methods.items():
    s = M.linking_scores([fn([m["name"] for m in e["mentions"]]) for e in ents], [tgt(e) for e in ents])
    res["gold_entities"][name] = s; print(f"A gold  {name:38s} {fmt(s)}")

# ---- Part B: predicted entities. Credit = the predicted entity is exactly a gold entity AND linked right,
#      plus a softer variant: each gold entity is matched to the predicted entity sharing most mentions.
if a.ner_preds:
    from ldred.data import load_ner_preds
    ner_spans = load_ner_preds(a.ner_preds)
else:
    pk = Path(a.out) / "crf.pkl"
    if pk.exists():
        tagger = pickle.load(open(pk, "rb"))
    else:                                       # train the CRF mention detector (about 2-4 minutes)
        from ldred.ner_crf import CRFTagger
        Path(a.out).mkdir(exist_ok=True); tagger = CRFTagger().fit(train); pickle.dump(tagger, open(pk, "wb"))
    ner_spans = [tagger.predict_doc(d) for d in dev]
pred = [(d, cluster(d, sp, ("PER",))) for d, sp in zip(dev, ner_spans)]
for name, (fn, tgt) in methods.items():
    ranked, targets = [], []
    for d, ents_pred in pred:
        by_span = {}
        for t, spans in ents_pred:
            if t in NOT_LINKABLE: continue
            by_span[(t, spans)] = fn([" ".join(d["sents"][s][x:y]) for s, x, y in spans])
        for e in d["entities"]:
            if e["type"] in NOT_LINKABLE: continue
            gold = (e["type"], frozenset((m["sent_id"], *m["pos"]) for m in e["mentions"]))
            # soft: the predicted entity of the same type that overlaps most with the gold mention set
            best = max((k for k in by_span if k[0] == e["type"]), key=lambda k: len(k[1] & gold[1]), default=None)
            ranked.append(by_span[best] if best is not None and len(best[1] & gold[1]) > 0 else [])
            targets.append(tgt(e))
    s = M.linking_scores(ranked, targets); res["predicted_entities"][name] = s
    print(f"B pred  {name:38s} {fmt(s)}")
Path(a.out).mkdir(exist_ok=True)
json.dump(res, open(Path(a.out) / "wiki_metrics.json", "w"), indent=1)
