import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from ldred.gliner_ner import tokens_to_text, char_to_token_span, resolve_overlaps, predict_docs, DEFAULT_LABELS
from ldred import ner_datasets as D
from ldred.metrics import ner_f1


def test_text_offsets_roundtrip():
    toks = ["Apple", "makes", "iPhone", "."]
    text, offs = tokens_to_text(toks)
    assert text == "Apple makes iPhone ." and all(text[a:b] == t for (a, b), t in zip(offs, toks))
    assert char_to_token_span(offs, 0, 5) == (0, 1) and char_to_token_span(offs, 13, 19) == (2, 3)
    assert char_to_token_span(offs, 2, 8) == (0, 2)          # cuts tokens -> widened to the tokens it touches
    assert char_to_token_span(offs, 5, 6) is None            # only the space


def test_overlaps_keep_best_score():
    assert resolve_overlaps([(0, 2, "PER", .6), (1, 3, "COMP", .9), (4, 5, "PROD", .5)]) == [(1, 3, "COMP", .9), (4, 5, "PROD", .5)]


class Stub:
    def predict_entities(self, text, labels, threshold=0.5):
        assert labels == list(DEFAULT_LABELS)
        return [{"start": 0, "end": 5, "label": "company", "score": .9},
                {"start": 13, "end": 19, "label": "product", "score": .8},
                {"start": 0, "end": 5, "label": "weapon", "score": .99}]     # label we did not ask for: ignored


def test_predict_docs_and_metric():
    doc = D.to_doc(0, ["Apple", "makes", "iPhone", "."], [(0, 1, "corporation"), (2, 3, "product")])
    pred = predict_docs(Stub(), [doc])
    assert pred == [{(0, 0, 1, "COMP"), (0, 2, 3, "PROD")}]
    assert ner_f1([doc], pred, D.TARGET)["ALL"][2] == 1.0
