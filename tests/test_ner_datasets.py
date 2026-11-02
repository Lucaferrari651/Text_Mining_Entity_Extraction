import sys, json, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from ldred import ner_datasets as D
from ldred.metrics import ner_f1
from ldred.ner_transformer import make_labels, doc_labels


def test_unify():
    assert D.unify("person") == "PER" and D.unify("person-actor") == "PER"
    assert D.unify("corporation") == "COMP" and D.unify("organization-company") == "COMP"
    assert D.unify("organization-sportsteam") == "OTHER" and D.unify("group") == "OTHER"
    assert D.unify("product") == "PROD" and D.unify("product-car") == "PROD"


def test_bio_and_run_spans():
    assert D.bio_spans(["O", "B-person", "I-person", "B-person", "I-product"]) == \
        [(1, 3, "person"), (3, 4, "person"), (4, 5, "product")]
    # Few-NERD has no B/I: runs of one tag are one entity, a different tag starts a new one
    assert D.run_spans(["O", "person-actor", "person-actor", "person-director", "O", "product-car"]) == \
        [(1, 3, "person-actor"), (3, 4, "person-director"), (5, 6, "product-car")]


def test_label_tables_match_dataset_cards():
    assert len(D.FEWNERD_FINE) == 67 and D.FEWNERD_FINE[0] == "O" and D.FEWNERD_FINE[28] == "organization-company"
    assert D.TWEETNER7[-1] == "O" and D.WNUT17[0] == "O"


def test_loader_and_unified_bio(tmp_path):
    rows = [{"id": "1", "tokens": ["Apple", "makes", "iPhone", "in", "Paris"], "ner_tags": [1, 0, 11, 0, 7]}]
    (tmp_path / "wnut17_test.jsonl").write_text("\n".join(json.dumps(r) for r in rows))
    docs = D.load("wnut17", tmp_path, "test")
    assert [(e["type"], e["mentions"][0]["pos"]) for e in docs[0]["entities"]] == \
        [("COMP", [0, 1]), ("PROD", [2, 3]), ("OTHER", [4, 5])]
    labels, l2i = make_labels(D.UNIFIED)
    assert [labels[i] for i in doc_labels(docs[0], l2i)] == ["B-COMP", "O", "B-PROD", "O", "B-OTHER"]


def test_target_micro_ignores_other():
    doc = D.to_doc(0, ["a", "b", "c"], [(0, 1, "person"), (1, 2, "location")])
    pred = [{(0, 0, 1, "PER"), (0, 2, 3, "OTHER")}]            # an OTHER mistake must not hurt the target score
    r = ner_f1([doc], pred, D.TARGET)
    assert r["ALL"][2] == 1.0 and r["OTHER"][0] == 0.0
