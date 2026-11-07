"""Company dictionary (gazetteer) lookup on token-level sentences, e.g. built from DBpedia company names.

A name is normalised the same way as the sentence tokens: split into word / punctuation tokens, lower-cased, Twitter markup
({@name@}, @name, #name) reduced to the bare name. Matching is the longest dictionary entry starting at each token,
left to right, without overlaps. Everything here is pure Python and unit-tested on a tiny fake dictionary; the real name
list comes from `fetch_dbpedia_companies.py` (needs internet).
"""
import re
from pathlib import Path

LEGAL = {"inc", "inc.", "corp", "corp.", "corporation", "ltd", "ltd.", "limited", "llc", "plc", "co", "co.", "company",
         "gmbh", "ag", "sa", "s.a.", "nv", "n.v.", "bv", "b.v.", "ab", "oy", "as", "spa", "s.p.a."}
_TOKEN = re.compile(r"\w+(?:[.'’&-]\w+)*|[^\w\s]", re.UNICODE)
_MARKUP = re.compile(r"^\{@(.+)@\}$")


def norm_token(tok):
    """One sentence token -> comparison form: handle markup removed, lower-cased."""
    m = _MARKUP.match(tok)
    tok = m.group(1) if m else tok
    return tok.lstrip("@#").lower()


def tokenize_name(name):
    """A dictionary name -> normalised tokens, split like the datasets split text (words and punctuation apart)."""
    name = re.sub(r"\s*\((?:company|corporation|business|brand)[^)]*\)\s*$", "", name.strip(), flags=re.I)
    return [norm_token(t) for t in _TOKEN.findall(name)]


class Gazetteer:
    def __init__(self, names=(), add_legal_variants=True, min_chars=2, max_len=8):
        self.keys, self.max_len, self.min_chars = set(), max_len, min_chars
        for n in names:
            self.add(n, add_legal_variants)

    @classmethod
    def from_file(cls, path, **kw):
        return cls((l.strip() for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()), **kw)

    def add(self, name, add_legal_variants=True):
        toks = tokenize_name(name)
        if not toks:
            return
        variants = [toks]
        if add_legal_variants:
            t = list(toks)
            while len(t) > 1 and (t[-1] in LEGAL or t[-1] in {",", "."}):      # 'Foo , Inc .' -> 'Foo'
                t = t[:-1]
                if t[-1] not in {",", "."}:
                    variants.append(list(t))
        for v in variants:
            if v and len(v) <= self.max_len and sum(len(x) for x in v) >= self.min_chars:
                self.keys.add(" ".join(v))

    def __len__(self):
        return len(self.keys)

    def __contains__(self, tokens):
        """True if the (raw) token list as a whole is a dictionary entry."""
        return " ".join(norm_token(t) for t in tokens) in self.keys

    def find(self, tokens, single_word="any", stop=frozenset()):
        """Longest-match spans [(start, end)] over a raw token list.
        single_word: 'any' accepts one-token matches as they are; 'capitalised' only if the surface token starts with a capital
        letter (or is a handle), which drops common lower-case words ('sun', 'apple', 'orange').
        stop: normalised words never accepted as a one-token match (see `common_words`)."""
        norm = [norm_token(t) for t in tokens]
        spans, i = [], 0
        while i < len(tokens):
            hit = None
            for n in range(min(self.max_len, len(tokens) - i), 0, -1):
                if " ".join(norm[i:i + n]) in self.keys:
                    if n == 1 and ((single_word == "capitalised" and not _capitalised(tokens[i])) or norm[i] in stop):
                        continue
                    hit = n
                    break
            if hit:
                spans.append((i, i + hit)); i += hit
            else:
                i += 1
        return spans


def _capitalised(tok):
    return bool(_MARKUP.match(tok)) or tok.lstrip("@#")[:1].isupper()


def common_words(train_docs, min_count=5, min_ratio=0.9):
    """Normalised tokens that are almost never part of an entity in the training split ('the', 'good', 'who'): used as a stop
    list for one-token dictionary matches. Needs only the training labels, never the test split."""
    total, outside = {}, {}
    for d in train_docs:
        inside = {i for e in d["entities"] for m in e["mentions"] for i in range(*m["pos"])}
        for i, t in enumerate(d["sents"][0]):
            k = norm_token(t)
            total[k] = total.get(k, 0) + 1
            if i not in inside:
                outside[k] = outside.get(k, 0) + 1
    return {k for k, n in total.items() if n >= min_count and outside.get(k, 0) / n >= min_ratio}


def predict_docs(gaz, docs, single_word="any", label="COMP", stop=frozenset()):
    """Dictionary-only predictions in the same format as the models: one {(sent, start, end, type)} set per document."""
    return [{(0, a, b, label) for a, b in gaz.find(d["sents"][0], single_word, stop)} for d in docs]


def hybrid(model_preds, gaz, docs, mode="add", single_word="capitalised", stop=frozenset()):
    """Combine model predictions with dictionary matches.
    mode 'add'     : add a COMP span where a dictionary match overlaps no model prediction;
    mode 'relabel' : additionally change a model span of another type to COMP when it is exactly a dictionary match;
    mode 'both'    : same as 'relabel' (which already includes 'add')."""
    out = []
    for pred, d in zip(model_preds, docs):
        pred = set(pred)
        for a, b in gaz.find(d["sents"][0], single_word, stop):
            same = {p for p in pred if p[1] == a and p[2] == b}
            overlap = {p for p in pred if p[1] < b and p[2] > a}
            if not overlap:
                pred.add((0, a, b, "COMP"))
            elif mode in ("relabel", "both") and same and not any(p[3] == "COMP" for p in same):
                pred -= same
                pred.add((0, a, b, "COMP"))
        out.append(pred)
    return out
