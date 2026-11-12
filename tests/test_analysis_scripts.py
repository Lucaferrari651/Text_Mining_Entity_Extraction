"""Smoke tests: the analysis scripts run on a tiny fake run and give the expected numbers."""
import sys, json, pathlib, subprocess
ROOT = pathlib.Path(__file__).parent.parent


def _fake(tmp_path, pred):
    data = tmp_path / "data"; data.mkdir()
    rows = [{"id": "1", "tokens": ["Apple", "makes", "iPhone", "in", "Paris"], "ner_tags": [1, 0, 11, 0, 7]}]
    (data / "wnut17_test.jsonl").write_text("\n".join(json.dumps(r) for r in rows))
    run = tmp_path / "runs" / "r"; run.mkdir(parents=True)
    (run / "preds_wnut17.json").write_text(json.dumps([pred]))
    (run / "metrics.json").write_text(json.dumps({"args": {}}))
    return data, tmp_path / "runs"


def _run(script, data, runs, out):
    subprocess.run([sys.executable, str(ROOT / script), "--data-dir", str(data), "--runs", str(runs), "--run", "r", "--out", str(out)],
                   check=True, cwd=ROOT, capture_output=True)
    return json.load(open(out))


def test_merged_cp(tmp_path):
    # gold: Apple COMP (0,1), iPhone PROD (2,3). The prediction swaps the two types: wrong with 3 types, right once merged.
    data, runs = _fake(tmp_path, [[0, 0, 1, "PROD"], [0, 2, 3, "COMP"]])
    r = _run("merged_cp.py", data, runs, tmp_path / "o.json")["r/wnut17"]
    assert r["three_types"] == 0.0 and r["comp_prod_merged"] == 1.0


def test_boundaries_runs(tmp_path):
    data, runs = _fake(tmp_path, [[0, 0, 1, "COMP"], [0, 2, 3, "PROD"]])
    r = _run("analyze_boundaries.py", data, runs, tmp_path / "b.json")
    assert r  # produced a result for the run
