import csv, json
from argparse import Namespace
import review_sheet as R


def doc(ents):
    return {"sents": [["Ford", "and", "Disney", "met"]],
            "entities": [{"id": i, "type": t, "mentions": [{"sent_id": 0, "pos": [a, b]}]} for i, (t, a, b) in enumerate(ents)]}


def test_spurious_keeps_only_predictions_touching_no_gold():
    d = doc([("COMP", 0, 1)])
    sp = R.spurious([d], [[[0, 0, 1, "COMP"], [0, 2, 3, "COMP"], [0, 2, 3, "OTHER"]]])
    assert sp == [(0, (0, 2, 3, "COMP"))]


def test_mark_and_kappa():
    assert R.mark(["a", "Ford", "b"], 1, 2) == "a [[Ford]] b"
    assert R.kappa(["yes", "no", "yes", "no"], ["yes", "no", "yes", "no"]) == 1.0
    assert abs(R.kappa(["yes", "yes", "no", "no"], ["yes", "no", "yes", "no"])) < 1e-9


def test_score_reads_sheet(tmp_path, capsys):
    p = tmp_path / "s.csv"
    rows = [{"id": str(i), "dataset": "fewnerd", "pred_type": "COMP", "sentence": "x", "reviewer_a": a, "reviewer_b": b, "note": ""}
            for i, (a, b) in enumerate([("yes", "yes"), ("yes", "yes"), ("no", "no"), ("no", "yes")])]
    with open(p, "w", newline="") as f:
        w = csv.DictWriter(f, R.FIELDS); w.writeheader(); w.writerows(rows)
    c = tmp_path / "b.json"
    c.write_text(json.dumps({"r/fewnerd": {"exact_f1": 0.8, "gold": 100, "pred": 100, "spurious_by_type": {"COMP": 20}}}))
    R.score(Namespace(sheet=str(p), run="r", out=None, counts=str(c)))
    res = json.loads(capsys.readouterr().out)
    assert res["rows_reviewed"] == 4 and res["agreement"] == 0.75
    d = res["per_dataset"]["fewnerd"]
    assert d["n_agreed"] == 3 and abs(d["share_yes"] - 2 / 3) < 1e-3 and d["estimated_f1_if_yes_were_gold"] > 0.8
