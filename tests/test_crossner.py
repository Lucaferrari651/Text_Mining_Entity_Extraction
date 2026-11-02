import json
from ldred import ner_datasets as D


def write(tmp_path, rows):
    d = tmp_path / "CrossNER_AI"; d.mkdir()
    for sp in ("train", "dev", "test"):
        (d / f"{sp}.json").write_text(json.dumps(rows))
    return tmp_path


ROWS = [{"sentence": "Geoffrey Hinton works at Google on TensorFlow .",
         "entities": [{"name": "Geoffrey Hinton", "type": "person -> researcher", "pos": [0, 15]},
                      {"name": "Google", "type": "organization -> others", "pos": [25, 31]},
                      {"name": "TensorFlow", "type": "product name", "pos": [35, 45]},
                      {"name": "Hint", "type": "AI algorithm", "pos": [9, 13]}]}]     # not on a token boundary: skipped


def test_unify_b2():
    assert [D.unify_b2(t) for t in ("person -> others", "organization -> university", "product name", "country")] == \
           ["PER", "ORG", "PROD", "OTHER"]


def test_load_crossner_maps_char_offsets_to_tokens(tmp_path):
    docs = D.load("crossner_ai", write(tmp_path, ROWS), "test")
    d = docs[0]
    assert d["sents"][0][:3] == ["Geoffrey", "Hinton", "works"]
    got = {(e["type"], tuple(e["mentions"][0]["pos"])) for e in d["entities"]}
    assert got == {("PER", (0, 2)), ("ORG", (4, 5)), ("PROD", (6, 7))}
    assert D.load("crossner_ai", tmp_path, "validation")[0]["title"] == "0"       # 'validation' reads dev.json
    assert D.stats(docs)["ORG"] == 1


def test_to_org_scale_and_targets():
    assert D.to_org_scale([{(0, 1, 2, "COMP"), (0, 3, 4, "PER")}]) == [{(0, 1, 2, "ORG"), (0, 3, 4, "PER")}]
    assert D.target_types("crossner_music") == ["PER", "ORG", "PROD"] and D.target_types("wnut17") == ["PER", "COMP", "PROD"]
