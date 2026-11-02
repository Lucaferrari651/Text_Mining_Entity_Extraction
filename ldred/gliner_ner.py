"""Zero-shot NER with GLiNER (entity types given as plain-text labels), adapted to our token-level documents.

GLiNER works on raw text and returns character offsets; our gold spans are token spans. So we rebuild the text by
joining tokens with single spaces, remember where each token starts/ends, and map every predicted character span back to
token boundaries. A prediction that cuts a token in half is widened to the tokens it touches (a real model does this
rarely). Everything except `predict_docs` is pure Python and unit-tested without the model.
"""

# text label given to the model -> unified type
DEFAULT_LABELS = {"person": "PER", "company": "COMP", "product": "PROD"}


def tokens_to_text(tokens):
    """Join tokens with single spaces -> (text, [(char_start, char_end) per token])."""
    text, offs, pos = [], [], 0
    for t in tokens:
        offs.append((pos, pos + len(t)))
        text.append(t)
        pos += len(t) + 1
    return " ".join(text), offs


def char_to_token_span(offs, c0, c1):
    """Character span [c0, c1) -> (first_token, last_token_exclusive) of the tokens it overlaps, or None."""
    idx = [i for i, (a, b) in enumerate(offs) if a < c1 and b > c0]
    return (idx[0], idx[-1] + 1) if idx else None


def resolve_overlaps(spans):
    """Keep the highest-score span among overlapping ones. spans: (start, end, type, score)."""
    kept = []
    for s in sorted(spans, key=lambda s: (-s[3], s[0])):
        if all(s[1] <= k[0] or s[0] >= k[1] for k in kept):
            kept.append(s)
    return sorted(kept)


def predict_docs(model, docs, labels=None, threshold=0.5, batch_log=None):
    """One predicted span set per document: {(sent_id, start, end, type)}. Documents here are single sentences."""
    labels = labels or DEFAULT_LABELS
    out = []
    for n, doc in enumerate(docs):
        found = set()
        for sid, sent in enumerate(doc["sents"]):
            text, offs = tokens_to_text(sent)
            ents = model.predict_entities(text, list(labels), threshold=threshold)
            spans = []
            for e in ents:
                span = char_to_token_span(offs, e["start"], e["end"])
                if span and e["label"] in labels:
                    spans.append((span[0], span[1], labels[e["label"]], float(e.get("score", 1.0))))
            for a, b, t, _ in resolve_overlaps(spans):
                found.add((sid, a, b, t))
        out.append(found)
        if batch_log and (n + 1) % 500 == 0:
            batch_log(f"  {n + 1}/{len(docs)} sentences")
    return out
