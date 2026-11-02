"""Run the 3-stage baseline on Linked-DocRED and print metrics.
usage: python3 run_baseline.py DATA_DIR [--skip-ner]"""
import argparse, json, pickle, time
from pathlib import Path
from ldred.data import load_split, wiki_target, NOT_LINKABLE
from ldred import metrics as M
from ldred.ner_crf import CRFTagger
from ldred.coref import cluster
from ldred.linking import PriorIndex, FuzzyIndex, rank_entity

ap = argparse.ArgumentParser(); ap.add_argument("data_dir"); ap.add_argument("--skip-ner", action="store_true")
ap.add_argument("--out", default="results")
ap.add_argument("--ner-preds", help="preds_dev.json from ner_transformer.py instead of the CRF")
a = ap.parse_args()
out = Path(a.out); out.mkdir(exist_ok=True)
train, dev = load_split(a.data_dir, "train"), load_split(a.data_dir, "dev")
res = {}

# ---- stage 2 alone: coreference on GOLD mentions
gold_spans = [{(m["sent_id"], *m["pos"], e["type"]) for e in d["entities"] for m in e["mentions"]} for d in dev]
variants = {"singletons": None, "exact": ()}
for name, sub in [("exact+subset(PER)", ("PER",)), ("exact+subset(PER,ORG)", ("PER", "ORG")),
                  ("exact+subset(PER,ORG,LOC,MISC)", ("PER", "ORG", "LOC", "MISC"))]:
    variants[name] = sub
res["coref_gold_mentions"] = {}
for name, sub in variants.items():
    cl = []
    for d, sp in zip(dev, gold_spans):
        if sub is None:
            cl.append([{(s, a, b)} for s, a, b, _ in sp])
        else:
            cl.append([set(m) for _, m in cluster(d, sp, sub)])
    p, r, f = M.coref_b3(dev, cl)
    ent = M.entity_f1(dev, [[(t, m) for t, m in cluster(d, sp, sub)] if sub is not None else
                            [(s[3], frozenset([s[:3]])) for s in sp] for d, sp in zip(dev, gold_spans)])
    res["coref_gold_mentions"][name] = {"B3_P": p, "B3_R": r, "B3_F1": f, "entity_F1": ent[2]}
    print(f"coref  {name:34s} B3 P={p:.3f} R={r:.3f} F1={f:.3f} | entity F1={ent[2]:.3f}")

# ---- stage 3 alone: linking on GOLD entities
prior = PriorIndex().fit(train); fuzzy = FuzzyIndex(prior)
ents = [(d, e) for d in dev for e in d["entities"] if e["type"] not in NOT_LINKABLE]
targets = [wiki_target(e) for _, e in ents]
res["linking_gold_entities"] = {}
for name, idx in [("prior (exact alias)", prior), ("prior + fuzzy char-3gram", fuzzy)]:
    t0 = time.time()
    ranked = [rank_entity([m["name"] for m in e["mentions"]], idx) for _, e in ents]
    s = M.linking_scores(ranked, targets)
    res["linking_gold_entities"][name] = s
    print(f"link   {name:28s} " + " ".join(f"{k}={v:.3f}" for k, v in s.items()) + f"  ({time.time()-t0:.0f}s)")

# ---- stage 1: NER, then full pipeline on PREDICTED mentions
if not a.skip_ner:
    if a.ner_preds:
        from ldred.data import load_ner_preds
        pred = load_ner_preds(a.ner_preds)
    else:
        pk = out / "crf.pkl"
        if pk.exists():
            tagger = pickle.load(open(pk, "rb"))
        else:
            t0 = time.time(); tagger = CRFTagger().fit(train); print(f"CRF trained in {time.time()-t0:.0f}s")
            pickle.dump(tagger, open(pk, "wb"))
        pred = [tagger.predict_doc(d) for d in dev]
    ner = M.ner_f1(dev, pred); res["ner_crf"] = ner
    for t, (p, r, f) in sorted(ner.items()): print(f"ner    {t:5s} P={p:.3f} R={r:.3f} F1={f:.3f}")
    pred_ent = [cluster(d, sp, ("PER",)) for d, sp in zip(dev, pred)]
    ef = M.entity_f1(dev, pred_ent); res["pipeline_entity_F1"] = ef
    print(f"pipeline entity F1 (NER+coref, exact entities) P={ef[0]:.3f} R={ef[1]:.3f} F1={ef[2]:.3f}")
    # linking of the predicted entities that are exactly right (type + all mentions), vs gold title
    ok = tot = hit = 0
    for d, pe in zip(dev, pred_ent):
        gold = {(e["type"], frozenset((m["sent_id"], *m["pos"]) for m in e["mentions"])): e for e in d["entities"]}
        for t, spans in pe:
            if t in NOT_LINKABLE: continue
            names = [" ".join(d["sents"][s][a:b]) for s, a, b in spans]
            top = (rank_entity(names, fuzzy) or [None])[0]
            tot += 1
            if (t, spans) in gold:
                ok += 1; hit += top is not None and top == wiki_target(gold[(t, spans)])
    n_gold = len(ents)
    res["pipeline_link"] = {"linked_correctly": hit, "n_gold_linkable": n_gold, "end_to_end_hit@1": hit / n_gold}
    print(f"end-to-end: {hit}/{n_gold} gold linkable entities recovered AND linked at rank 1 = {hit/n_gold:.3f}")
json.dump(res, open(out / "metrics.json", "w"), indent=1, default=list)
