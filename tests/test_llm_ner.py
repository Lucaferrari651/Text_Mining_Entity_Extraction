import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from ldred import ner_datasets as D
from ldred.llm_ner import build_messages, parse_answer, to_spans, fmt_answer, Cache, predict_docs, pick_shots
from ldred.metrics import ner_f1


def mk(tokens, spans):
    return D.to_doc(0, tokens, spans)


def test_parse_answer():
    txt = "- Apple | COMP\n* iPhone | prod\n- Paris | LOC\nnot a line\n- `Tim Cook` | PER"
    assert parse_answer(txt) == [("Apple", "COMP"), ("iPhone", "PROD"), ("Tim Cook", "PER")]
    assert parse_answer("None") == []


def test_to_spans_all_occurrences_and_boundaries():
    doc = mk("Apple sells Apple Watch and Applesauce".split(), [])
    # "Apple" matches tokens 0 and 2; inside "Applesauce" it does not line up with a token end
    assert to_spans(doc, [("Apple", "COMP")]) == {(0, 0, 1, "COMP"), (0, 2, 3, "COMP")}
    # the longer mention wins the overlap with the shorter one
    assert to_spans(doc, [("Apple", "COMP"), ("Apple Watch", "PROD")]) == {(0, 0, 1, "COMP"), (0, 2, 4, "PROD")}


def test_prompt_and_answer_format():
    shot = mk(["Tim", "Cook", "runs", "Apple", "."], [(0, 2, "person"), (3, 4, "corporation"), ])
    test = mk(["Nothing", "here"], [])
    assert fmt_answer(shot) == "- Tim Cook | PER\n- Apple | COMP" and fmt_answer(test) == "None"
    msgs = build_messages(test, [shot])
    assert [m["role"] for m in msgs] == ["system", "user", "assistant", "user"] and msgs[-1]["content"] == "Sentence: Nothing here"


def test_predict_uses_cache(tmp_path):
    doc = mk("Tim Cook runs Apple".split(), [(0, 2, "person"), (3, 4, "corporation")])
    calls = []
    def fake(msgs):
        calls.append(1); return "- Tim Cook | PER\n- Apple | COMP"
    cache = Cache(tmp_path / "c.jsonl")
    p = predict_docs(fake, [doc], [], "m", cache, log=lambda s: None)
    assert ner_f1([doc], p, D.TARGET)["ALL"][2] == 1.0
    p2 = predict_docs(fake, [doc], [], "m", Cache(tmp_path / "c.jsonl"), log=lambda s: None)   # fresh object, same file
    assert p2 == p and len(calls) == 1


def test_pick_shots_mix():
    pos = [mk(["a", "b"], [(0, 1, "person")]) for _ in range(10)]
    neg = [mk(["x", "y"], []) for _ in range(10)]
    shots = pick_shots(pos + neg, 6)
    assert len(shots) == 6 and sum(1 for s in shots if not s["entities"]) == 2
