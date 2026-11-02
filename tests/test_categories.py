import json
from analyze_categories import category, text


def test_category_splits_out_twitter_handles():
    doc = {"sents": [["via", "{@YouTube@}", "and", "Twitter"]]}
    assert text(doc, 1, 2) == "{@YouTube@}"
    assert category(doc, 1, 2, "product") == "product (handle)"
    assert category(doc, 3, 4, "corporation") == "corporation"


def test_script_runs_on_tiny_data(tmp_path, capsys, monkeypatch):
    import sys, analyze_categories as ac
    rows = [{"id": "1", "tokens": ["Apple", "makes", "iPhone", "."], "tags": [0, 14, 6, 14]}]
    (tmp_path / "tweetner7_test.jsonl").write_text("\n".join(json.dumps(r) for r in rows))
    (tmp_path / "tweetner7_train.jsonl").write_text("\n".join(json.dumps(r) for r in rows))
    f = tmp_path / "sys"; f.mkdir()
    (f / "preds_tweetner7.json").write_text(json.dumps([[[0, 0, 1, "COMP"], [0, 2, 3, "COMP"]]]))
    monkeypatch.setattr(sys, "argv", ["x", str(tmp_path), "--system", f"S={f}", "--datasets", "tweetner7", "--min-count", "1"])
    ac.main()
    out = capsys.readouterr().out
    assert "| corporation | COMP | 1 | 100% |" in out and "| product | PROD | 1 | 0% |" in out
    assert "predicted COMP (2): wrong on same span as gold product (1)" in out
