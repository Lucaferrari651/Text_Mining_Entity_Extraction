"""Stage 1 - mention detection as BIO sequence labelling with a linear-chain CRF (classical baseline)."""
import re
import sklearn_crfsuite
from .data import bio_tags, decode_bio


def shape(w):
    s = re.sub("[A-Z]", "X", w)
    s = re.sub("[a-z]", "x", s)
    s = re.sub("[0-9]", "d", s)
    return re.sub(r"(.)\1{2,}", r"\1\1", s)


def token_features(sent, i):
    w = sent[i]
    f = {"bias": 1.0, "w": w.lower(), "shape": shape(w), "title": w.istitle(), "upper": w.isupper(),
         "digit": w.isdigit(), "has_digit": any(c.isdigit() for c in w), "len": min(len(w), 12),
         "p2": w[:2].lower(), "p3": w[:3].lower(), "s2": w[-2:].lower(), "s3": w[-3:].lower(),
         "first": i == 0, "last": i == len(sent) - 1}
    for d in (-2, -1, 1, 2):
        j = i + d
        if 0 <= j < len(sent):
            v = sent[j]
            f[f"{d}:w"] = v.lower(); f[f"{d}:shape"] = shape(v); f[f"{d}:title"] = v.istitle()
        else:
            f[f"{d}:pad"] = True
    return f


def featurize(sent):
    return [token_features(sent, i) for i in range(len(sent))]


class CRFTagger:
    def __init__(self, c1=0.05, c2=0.05, max_iter=100):
        self.crf = sklearn_crfsuite.CRF(algorithm="lbfgs", c1=c1, c2=c2, max_iterations=max_iter,
                                        all_possible_transitions=True)

    def fit(self, docs):
        X, y = [], []
        for d in docs:
            for s, t in zip(d["sents"], bio_tags(d)):
                X.append(featurize(s)); y.append(t)
        self.crf.fit(X, y)
        return self

    def predict_doc(self, doc):
        """-> set of (sent_id, start, end, type)"""
        out = set()
        tags = self.crf.predict([featurize(s) for s in doc["sents"]])
        for sid, t in enumerate(tags):
            for a, b, ty in decode_bio(t):
                out.add((sid, a, b, ty))
        return out
