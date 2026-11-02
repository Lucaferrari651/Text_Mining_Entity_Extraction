import random
from compare_ner import fate, sample_indices


def doc(*mentions):
    """mentions: (start, end, type) in sentence 0."""
    return {"entities": [{"type": t, "mentions": [{"sent_id": 0, "pos": [a, b]}]} for a, b, t in mentions]}


def test_sample_indices_match_llm_eval_sampling():
    docs = list(range(1287))
    assert [docs[i] for i in sample_indices(len(docs), 300, 13)] == random.Random(13).sample(docs, 300)
    assert len(sample_indices(10, 300, 13)) == 10


def test_fate_counts_each_outcome():
    gold = [doc((0, 1, "COMP"), (2, 3, "COMP"), (4, 6, "PROD"), (8, 9, "PROD"))]
    pred = [{(0, 0, 1, "COMP"),      # found
             (0, 2, 3, "PROD"),      # same span, other type
             (0, 4, 5, "PROD")}]     # overlapping, different boundaries; (8,9) is missed
    f = fate(gold, pred)
    assert f["COMP"] == {"found": 1, "same span, other type: PROD": 1}
    assert f["PROD"] == {"overlapping, different boundaries": 1, "missed": 1}
