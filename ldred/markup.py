"""Strip the TweetNER7 handle markup: the single token {@Name Of Thing@} becomes the tokens of the bare name.

The gold mentions are remapped to the new token positions, so the same mentions are scored on the cleaned text.
"""
import copy
import re

HANDLE = re.compile(r"^\{@(.+)@\}$")


def strip_handles(doc):
    """-> new doc with every {@...@} token expanded to its words; entity spans follow the new positions."""
    new = copy.deepcopy(doc)
    maps = []                                   # per sentence: old token index -> (new start, new end)
    new_sents = []
    for sent in doc["sents"]:
        out, mp = [], []
        for w in sent:
            m = HANDLE.match(w)
            words = m.group(1).split() if m else [w]
            mp.append((len(out), len(out) + len(words)))
            out.extend(words)
        new_sents.append(out); maps.append(mp)
    new["sents"] = new_sents
    for e in new["entities"]:
        for m in e["mentions"]:
            mp = maps[m["sent_id"]]
            a, b = m["pos"]
            m["pos"] = [mp[a][0], mp[b - 1][1]]
    return new


def count_handles(docs):
    return sum(1 for d in docs for s in d["sents"] for w in s if HANDLE.match(w))
