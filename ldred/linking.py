"""Stage 3 - link an entity (a set of mentions) to a Wikipedia title.

Candidate generation
  PriorIndex      alias -> Wikipedia title counts learned on the training set (offline)
  FuzzyIndex      char-3gram TF-IDF cosine nearest aliases, used when the exact alias is unknown
  (a live Wikipedia-search backend can be plugged in with the same `candidates(surface)` interface)
Entity ranking
  each mention votes for its candidates with a score in [0,1]; an entity's score for a title is the
  sum of its mentions' votes, so titles supported by several mentions rise to the top.
"""
import re
from collections import Counter, defaultdict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from .data import NOT_LINKABLE, wiki_target


def key(s):
    return re.sub(r"\s+", " ", s.lower().strip())


class PriorIndex:
    def __init__(self):
        self.counts = defaultdict(Counter)

    def fit(self, docs):
        for d in docs:
            for e in d["entities"]:
                t = wiki_target(e)
                if t is None or e["type"] in NOT_LINKABLE:
                    continue
                for m in e["mentions"]:
                    self.counts[key(m["name"])][t] += 1
        return self

    def candidates(self, surface):
        c = self.counts.get(key(surface))
        if not c:
            return []
        tot = sum(c.values())
        return [(t, n / tot) for t, n in c.most_common()]


class FuzzyIndex:
    def __init__(self, prior, top_k=5, min_sim=0.6):
        self.prior, self.top_k, self.min_sim = prior, top_k, min_sim
        self.aliases = list(prior.counts)
        self.vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 3), lowercase=False, sublinear_tf=True)
        self.M = self.vec.fit_transform(self.aliases)

    def candidates(self, surface):
        exact = self.prior.candidates(surface)
        if exact:
            return exact
        sims = (self.M @ self.vec.transform([key(surface)]).T).toarray().ravel()
        order = np.argsort(-sims)[: self.top_k]
        out = Counter()
        for j in order:
            if sims[j] < self.min_sim:
                break
            for t, p in self.prior.candidates(self.aliases[j]):
                out[t] = max(out[t], p * sims[j])
        return out.most_common()


def rank_entity(surfaces, index):
    score = Counter()
    for s in surfaces:
        for t, v in index.candidates(s):
            score[t] += v
    return [t for t, _ in score.most_common()]


class CacheIndex:
    """Candidates from a search-API cache written by fetch_wiki_candidates.py.
    field = 'wikipedia' (page titles) or 'wikidata' (Q-ids). Scores are 1/(1+rank) so that the
    'prob-sum' aggregation still works; the ranked list itself is what 'rank-sum' uses."""
    def __init__(self, cache, field):
        self.cache, self.field = cache, field

    def candidates(self, surface):
        ranked = self.cache.get(key(surface), {}).get(self.field, [])
        return [(t, 1.0 / (1 + i)) for i, t in enumerate(ranked)]


def rank_entity_ranksum(surfaces, index):
    """Aggregation used in the Linked-DocRED paper (Eq. 2-3): a candidate gets, for each mention, its 0-based
    rank in that mention's list, or len(list)+1 if absent; scores are summed over mentions, lowest wins."""
    per_mention = [[t for t, _ in index.candidates(s)] for s in surfaces]
    per_mention = [c for c in per_mention if c]
    cands = {t for c in per_mention for t in c}
    score = {t: sum(c.index(t) if t in c else len(c) + 1 for c in per_mention) for t in cands}
    return sorted(cands, key=lambda t: (score[t], t))


def merge_ranked(*rankings):
    """Interleave several ranked lists (best first) without duplicates - used to combine search + dictionary."""
    out, seen = [], set()
    for rank in range(max((len(r) for r in rankings), default=0)):
        for r in rankings:
            if rank < len(r) and r[rank] not in seen:
                seen.add(r[rank]); out.append(r[rank])
    return out
