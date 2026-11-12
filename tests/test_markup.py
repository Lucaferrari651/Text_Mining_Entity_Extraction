from ldred.markup import strip_handles, count_handles


def doc():
    return {"sents": [["Watch", "{@Fife Council@}", "now", "{@YouTube@}"]],
            "entities": [{"id": 0, "type": "COMP", "mentions": [{"sent_id": 0, "pos": [1, 2]}]},
                         {"id": 1, "type": "PROD", "mentions": [{"sent_id": 0, "pos": [3, 4]}]}]}


def test_tokens_expand_and_spans_follow():
    d = strip_handles(doc())
    assert d["sents"][0] == ["Watch", "Fife", "Council", "now", "YouTube"]
    assert d["entities"][0]["mentions"][0]["pos"] == [1, 3]
    assert d["entities"][1]["mentions"][0]["pos"] == [4, 5]


def test_original_untouched_and_counted():
    d = doc(); strip_handles(d)
    assert d["sents"][0][1] == "{@Fife Council@}" and count_handles([d]) == 2
