"""Extra NER datasets with explicit company / product types, mapped to one label set.

Unified types:  PER (person), COMP (company / corporation), PROD (product), OTHER (every other entity type).
Every sentence becomes one "document" in the same structure Linked-DocRED uses ({"sents": [tokens], "entities": [...]}),
so the metrics and the transformer code work on it unchanged.

Files are the .jsonl dumps written by the Colab cell (one example per line, tags stored as integer ids).
The integer-id -> label-name tables below come from the dataset cards (printed by `load_dataset(...).features`).
Few-NERD has no B/I distinction: a maximal run of the same fine tag is one entity.
"""
import json
from pathlib import Path

UNIFIED = ["PER", "COMP", "PROD", "OTHER"]
TARGET = ["PER", "COMP", "PROD"]          # what we report; OTHER only keeps e.g. locations from being mistaken for companies

WNUT17 = ["O", "B-corporation", "I-corporation", "B-creative-work", "I-creative-work", "B-group", "I-group",
          "B-location", "I-location", "B-person", "I-person", "B-product", "I-product"]
TWEETNER7 = ["B-corporation", "B-creative_work", "B-event", "B-group", "B-location", "B-person", "B-product",
             "I-corporation", "I-creative_work", "I-event", "I-group", "I-location", "I-person", "I-product", "O"]
FEWNERD_FINE = [
    "O", "art-broadcastprogram", "art-film", "art-music", "art-other", "art-painting", "art-writtenart",
    "building-airport", "building-hospital", "building-hotel", "building-library", "building-other",
    "building-restaurant", "building-sportsfacility", "building-theater",
    "event-attack/battle/war/militaryconflict", "event-disaster", "event-election", "event-other", "event-protest",
    "event-sportsevent", "location-GPE", "location-bodiesofwater", "location-island", "location-mountain",
    "location-other", "location-park", "location-road/railway/highway/transit", "organization-company",
    "organization-education", "organization-government/governmentagency", "organization-media/newspaper",
    "organization-other", "organization-politicalparty", "organization-religion", "organization-showorganization",
    "organization-sportsleague", "organization-sportsteam", "other-astronomything", "other-award",
    "other-biologything", "other-chemicalthing", "other-currency", "other-disease", "other-educationaldegree",
    "other-god", "other-language", "other-law", "other-livingthing", "other-medical", "person-actor",
    "person-artist/author", "person-athlete", "person-director", "person-other", "person-politician",
    "person-scholar", "person-soldier", "product-airplane", "product-car", "product-food", "product-game",
    "product-other", "product-ship", "product-software", "product-train", "product-weapon"]


def unify(raw_type):
    """Dataset-specific type name -> one of UNIFIED."""
    if raw_type == "person" or raw_type.startswith("person-"):
        return "PER"
    if raw_type in ("corporation", "organization-company"):
        return "COMP"
    if raw_type == "product" or raw_type.startswith("product-"):
        return "PROD"
    return "OTHER"


def bio_spans(tag_names):
    """Names such as O / B-x / I-x -> list of (start, end, raw_type). A stray I- opens a span."""
    out, start, typ = [], None, None
    for i, t in enumerate(list(tag_names) + ["O"]):
        if t == "O" or t.startswith("B-") or (t.startswith("I-") and t[2:] != typ):
            if start is not None:
                out.append((start, i, typ)); start = typ = None
            if t != "O":
                start, typ = i, t[2:]
    return out


def run_spans(tag_names):
    """Few-NERD (no B/I): maximal runs of the same non-O tag -> (start, end, raw_type)."""
    out, start, typ = [], None, None
    for i, t in enumerate(list(tag_names) + ["O"]):
        if t != typ:
            if start is not None:
                out.append((start, i, typ))
            start, typ = (i, t) if t != "O" else (None, None)
    return out


def to_doc(doc_id, tokens, spans):
    ents = [{"id": k, "type": unify(t), "raw_type": t, "mentions": [{"sent_id": 0, "pos": [a, b]}]}
            for k, (a, b, t) in enumerate(spans)]
    return {"title": str(doc_id), "sents": [list(tokens)], "entities": ents}


def _read(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def load_wnut17(data_dir, split):
    return [to_doc(r["id"], r["tokens"], bio_spans([WNUT17[i] for i in r["ner_tags"]]))
            for r in _read(Path(data_dir) / f"wnut17_{split}.jsonl")]


def load_tweetner7(data_dir, split):
    return [to_doc(r["id"], r["tokens"], bio_spans([TWEETNER7[i] for i in r["tags"]]))
            for r in _read(Path(data_dir) / f"tweetner7_{split}.jsonl")]


def load_fewnerd(data_dir, split):
    return [to_doc(r["id"], r["tokens"], run_spans([FEWNERD_FINE[i] for i in r["fine_ner_tags"]]))
            for r in _read(Path(data_dir) / f"fewnerd_{split}.jsonl")]


LOADERS = {"wnut17": load_wnut17, "tweetner7": load_tweetner7, "fewnerd": load_fewnerd}

# --- CrossNER (from the B2NERD English release): test-only benchmark with PER / ORG / PROD ------------------------------
# CrossNER has a generic "organization" type, not "company", so its types are scored as PER / ORG / PROD (see `to_org_scale`).
CROSSNER = {"crossner_ai": "CrossNER_AI", "crossner_literature": "CrossNER_literature", "crossner_music": "CrossNER_music",
            "crossner_politics": "CrossNER_politics", "crossner_science": "CrossNER_science"}
CROSS_TARGET = ["PER", "ORG", "PROD"]


def unify_b2(raw_type):
    """B2NERD type name ('person -> researcher', 'organization -> university', 'product name', ...) -> PER / ORG / PROD / OTHER."""
    head = raw_type.split(" ->")[0].strip()
    return {"person": "PER", "organization": "ORG", "product name": "PROD"}.get(head, "OTHER")


def load_crossner(name, b2_dir, split):
    """One document per sentence. B2NERD sentences are space-separated tokens with character offsets; an entity that does not
    start and end on a token boundary (2 of 27,000) is skipped."""
    path = Path(b2_dir) / CROSSNER[name] / f"{'dev' if split == 'validation' else split}.json"
    docs = []
    for k, r in enumerate(json.load(open(path, encoding="utf-8"))):
        tokens, starts, ends, pos = r["sentence"].split(" "), {}, {}, 0
        for i, t in enumerate(tokens):
            starts[pos], ends[pos + len(t)] = i, i + 1
            pos += len(t) + 1
        ents = []
        for e in r["entities"]:
            a, b = e["pos"]
            if a in starts and b in ends:
                ents.append({"id": len(ents), "type": unify_b2(e["type"]), "raw_type": e["type"],
                             "mentions": [{"sent_id": 0, "pos": [starts[a], ends[b]]}]})
        docs.append({"title": str(k), "sents": [tokens], "entities": ents})
    return docs


def is_cross(name):
    return name in CROSSNER


def target_types(name):
    return CROSS_TARGET if is_cross(name) else TARGET


def to_org_scale(preds):
    """Predictions of a model trained with COMP -> ORG, so company predictions are scored against CrossNER's organizations
    (a company is an organization; the reverse does not hold, so recall on ORG is expected to be low for such models)."""
    return [{(s, a, b, "ORG" if t == "COMP" else t) for s, a, b, t in p} for p in preds]


def load(name, data_dir, split, limit=None):
    """`data_dir` is the jsonl folder for wnut17 / tweetner7 / fewnerd and the B2NERD `NER_en` folder for crossner_*."""
    docs = load_crossner(name, data_dir, split) if is_cross(name) else LOADERS[name](data_dir, split)
    return docs[:limit] if limit else docs


def stats(docs):
    """Number of mentions per unified type."""
    c = {t: 0 for t in UNIFIED}
    for d in docs:
        for e in d["entities"]:
            c[e["type"]] = c.get(e["type"], 0) + len(e["mentions"])
    return c
