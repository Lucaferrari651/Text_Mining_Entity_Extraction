from analyze_mismatches import classify, mentions, string_labels


def test_classify_outcomes():
    pred = {(0, 0, 2, "COMP"), (0, 5, 6, "PER"), (0, 8, 10, "PROD")}
    assert classify(pred, 0, 2, "COMP") == "found"
    assert classify(pred, 5, 6, "COMP") == "same span, other type: PER"
    assert classify(pred, 8, 9, "PROD") == "overlapping, other boundaries"
    assert classify(pred, 12, 13, "PROD") == "missed"


def test_string_labels_counts_types_per_lowercased_string():
    doc = {"sents": [["Apple", "sells", "apple", "."]],
           "entities": [{"type": "COMP", "mentions": [{"sent_id": 0, "pos": [0, 1]}]},
                        {"type": "PROD", "mentions": [{"sent_id": 0, "pos": [2, 3]}]}]}
    assert dict(string_labels([doc])["apple"]) == {"COMP": 1, "PROD": 1}
    assert mentions(doc, only=("PROD",)) == [(2, 3, "PROD")]
