from analyze_density import density, thresholds, group, score, GROUPS


def doc(n, *mentions):
    return {"sents": [["w"] * n],
            "entities": [{"type": t, "mentions": [{"sent_id": 0, "pos": [a, b]}]} for a, b, t in mentions]}


def test_density_counts_all_entity_types_and_groups():
    d_low = doc(10, (0, 1, "PER"))                      # 1/10
    d_mid = doc(10, (0, 2, "COMP"))                     # 2/10
    d_high = doc(4, (0, 2, "PROD"), (2, 3, "OTHER"))    # 3/4
    d_none = doc(5, (0, 1, "OTHER"))                    # an entity, but not a target type
    assert density(d_low) == 0.1 and density(d_high) == 0.75
    cuts = thresholds([d_low, d_mid, d_high, d_none])
    assert [group(d, cuts) for d in (d_none, d_low, d_mid, d_high)] == \
        ["no target entity", "low density", "middle density", "high density"]


def test_score_recall_and_false_positives_per_group():
    d_low = doc(10, (0, 1, "PER"), (3, 4, "COMP"))
    d_none = doc(5)
    cuts = (0.5, 0.9)
    pred = [{(0, 0, 1, "PER"), (0, 3, 4, "PROD"), (0, 5, 6, "COMP")}, {(0, 1, 2, "COMP")}]
    s = score([d_low, d_none], pred, cuts)
    low, none = s["low density"], s["no target entity"]
    assert low["gold"] == {"PER": 1, "COMP": 1, "PROD": 0} and low["found"] == {"PER": 1, "COMP": 0, "PROD": 0}
    assert low["fp"] == 2 and none["fp"] == 1 and none["sent"] == 1 and set(s) == set(GROUPS)
