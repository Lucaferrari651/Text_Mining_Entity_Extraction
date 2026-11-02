"""Evaluation written from the metric definitions (mention F1, B-cubed, entity F1, linking ranks)."""
from collections import defaultdict


def prf(tp, n_pred, n_gold):
    p = tp / n_pred if n_pred else 0.0
    r = tp / n_gold if n_gold else 0.0
    return p, r, (2 * p * r / (p + r) if p + r else 0.0)


def ner_f1(gold_docs, pred_spans, types=None):
    """Mention level, exact boundaries + type. pred_spans[i] = set of (sent, start, end, type) for doc i.
    Returns {type: (P, R, F1)} plus 'ALL' (micro). With `types`, 'ALL' only counts those types."""
    c = defaultdict(lambda: [0, 0, 0])     # tp, pred, gold
    for doc, pred in zip(gold_docs, pred_spans):
        gold = {(m["sent_id"], m["pos"][0], m["pos"][1], e["type"])
                for e in doc["entities"] for m in e["mentions"]}
        for s in gold:
            c[s[3]][2] += 1
            if types is None or s[3] in types:
                c["ALL"][2] += 1
        for s in pred:
            c[s[3]][1] += 1
            if types is None or s[3] in types:
                c["ALL"][1] += 1
            if s in gold:
                c[s[3]][0] += 1
                if types is None or s[3] in types:
                    c["ALL"][0] += 1
    return {t: prf(*v) for t, v in c.items()}


def b_cubed(gold_clusters, pred_clusters):
    """B-cubed over one document. Clusters: list of sets of hashable mentions (same mention universe)."""
    g_of = {m: i for i, c in enumerate(gold_clusters) for m in c}
    p_of = {m: i for i, c in enumerate(pred_clusters) for m in c}
    mentions = [m for m in g_of if m in p_of]
    if not mentions:
        return 0.0, 0.0
    ps = rs = 0.0
    for m in mentions:
        g, p = gold_clusters[g_of[m]], pred_clusters[p_of[m]]
        inter = len(g & p)
        ps += inter / len(p); rs += inter / len(g)
    return ps / len(mentions), rs / len(mentions)


def coref_b3(gold_docs, pred_clusters_per_doc):
    """Macro-averaged B-cubed P/R/F1 over documents. pred_clusters_per_doc[i]: list of sets of
    (sent, start, end) spans."""
    P = R = 0.0
    for doc, pred in zip(gold_docs, pred_clusters_per_doc):
        gold = [{(m["sent_id"], *m["pos"]) for m in e["mentions"]} for e in doc["entities"]]
        p, r = b_cubed(gold, pred)
        P += p; R += r
    n = max(len(gold_docs), 1)
    P, R = P / n, R / n
    return P, R, (2 * P * R / (P + R) if P + R else 0.0)


def entity_f1(gold_docs, pred_entities_per_doc):
    """Entity level: a predicted entity is right only if its type AND its full set of mention spans equal a
    gold entity's. pred entity = (type, frozenset of (sent, start, end))."""
    tp = npred = ngold = 0
    for doc, pred in zip(gold_docs, pred_entities_per_doc):
        gold = {(e["type"], frozenset((m["sent_id"], *m["pos"]) for m in e["mentions"]))
                for e in doc["entities"]}
        pred = set(pred)
        tp += len(gold & pred); npred += len(pred); ngold += len(gold)
    return prf(tp, npred, ngold)


def linking_scores(ranked_lists, targets, ks=(1, 5)):
    """ranked_lists[i]: ranked Wikipedia titles for entity i; targets[i]: gold title (None = not in Wikipedia).
    Entities without a Wikipedia target count as misses (they cannot be found), as in a full-pipeline run."""
    n = len(targets)
    ranks = []
    for ranked, t in zip(ranked_lists, targets):
        ranks.append(ranked.index(t) + 1 if t is not None and t in ranked else None)
    out = {f"hit@{k}": sum(r is not None and r <= k for r in ranks) / n for k in ks}
    found = [r for r in ranks if r is not None]
    out["not_found"] = 1 - len(found) / n
    out["mean_rank_found"] = sum(found) / len(found) if found else float("nan")
    out["mrr"] = sum(1 / r for r in found) / n
    return out
