"""Loading Linked-DocRED and turning it into the views each pipeline stage needs."""
import json
from pathlib import Path

TYPES = ["PER", "ORG", "LOC", "MISC", "TIME", "NUM"]
NOT_LINKABLE = {"TIME", "NUM"}          # entities the dataset marks as '#ignored#'


def load_split(data_dir, split):
    name = {"train": "train_annotated", "dev": "dev", "test": "test"}[split]
    return json.loads((Path(data_dir) / f"{name}.json").read_text(encoding="utf-8"))


def mention_spans(doc):
    """Gold mentions as (sent_id, start, end, type) -> entity id, for one document."""
    out = {}
    for e in doc["entities"]:
        for m in e["mentions"]:
            out[(m["sent_id"], m["pos"][0], m["pos"][1], e["type"])] = e["id"]
    return out


def bio_tags(doc):
    """One BIO tag list per sentence. Overlapping mentions (~1%) keep the longest span."""
    tags = [["O"] * len(s) for s in doc["sents"]]
    spans = sorted(((m["sent_id"], m["pos"][0], m["pos"][1], e["type"])
                    for e in doc["entities"] for m in e["mentions"]),
                   key=lambda s: (s[0], s[1], -(s[2] - s[1])))
    for sid, a, b, t in spans:
        if any(x != "O" for x in tags[sid][a:b]):
            continue
        tags[sid][a] = "B-" + t
        for i in range(a + 1, b):
            tags[sid][i] = "I-" + t
    return tags


def decode_bio(tags):
    """BIO tags of one sentence -> list of (start, end, type). Tolerates a stray I-."""
    spans, start, typ = [], None, None
    for i, t in enumerate(list(tags) + ["O"]):
        if t == "O" or t.startswith("B-") or (t.startswith("I-") and t[2:] != typ):
            if start is not None:
                spans.append((start, i, typ))
                start = typ = None
            if t != "O":
                start, typ = i, t[2:]
    return spans


def wiki_target(entity):
    """Wikipedia title of an entity, or None when it is not in Wikipedia / not linkable."""
    w = entity["entity_linking"]["wikipedia_resource"]
    return None if w.startswith("#") else w


def wikidata_target(entity):
    """Wikidata id of an entity, or None when it has none (new entity / NUM / TIME)."""
    if entity["type"] in NOT_LINKABLE:
        return None
    return entity["entity_linking"].get("wikidata_resource") or None


def load_ner_preds(path):
    """preds_dev.json written by ner_transformer.py -> list (one per document) of sets of (sent, start, end, type)."""
    return [{(s, a, b, t) for s, a, b, t in doc} for doc in json.loads(Path(path).read_text(encoding="utf-8"))]
