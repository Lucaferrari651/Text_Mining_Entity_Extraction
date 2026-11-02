"""Stage 2 - group mentions of one document into entities (rule-based, string evidence only).

Rules, applied per entity type:
  exact   : identical normalised strings          -> same entity
  subset  : a mention whose tokens are a subset of one longer mention's tokens joins it
            (e.g. "Smith" -> "John Smith"); only if exactly one longer candidate exists
"""
import re

STOP = {"the", "a", "an", "of", "de", "la", "le"}


def norm_tokens(tokens):
    toks = [re.sub(r"\W+", "", t.lower()) for t in tokens]
    return tuple(t for t in toks if t and t not in STOP)


class _UF:
    def __init__(self, n): self.p = list(range(n))
    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]; x = self.p[x]
        return x
    def union(self, a, b): self.p[self.find(a)] = self.find(b)


def cluster(doc, spans, subset_types=("PER",)):
    """spans: iterable of (sent, start, end, type). Returns list of (type, frozenset of (sent, start, end))."""
    spans = sorted(spans)
    toks = [norm_tokens(doc["sents"][s][a:b]) for s, a, b, _ in spans]
    uf = _UF(len(spans))
    seen = {}
    for i, (sp, tk) in enumerate(zip(spans, toks)):
        key = (sp[3], tk)
        if tk and key in seen:
            uf.union(i, seen[key])
        else:
            seen[key] = i
    for i, (sp, tk) in enumerate(zip(spans, toks)):
        if sp[3] not in subset_types or not tk:
            continue
        longer = {uf.find(j) for j, (sq, tl) in enumerate(zip(spans, toks))
                  if sq[3] == sp[3] and len(tl) > len(tk) and set(tk) <= set(tl)}
        if len(longer) == 1:
            uf.union(i, longer.pop())
    groups = {}
    for i, sp in enumerate(spans):
        groups.setdefault(uf.find(i), []).append(sp)
    return [(g[0][3], frozenset((s, a, b) for s, a, b, _ in g)) for g in groups.values()]
