import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from ldred.data import bio_tags, decode_bio
from ldred.metrics import b_cubed, prf, linking_scores, ner_f1
from ldred.coref import cluster

DOC = {"sents": [["John", "Smith", "met", "Smith", "in", "Paris", "."]],
       "entities": [{"id": 0, "type": "PER", "mentions": [{"sent_id": 0, "pos": [0, 2]}, {"sent_id": 0, "pos": [3, 4]}]},
                    {"id": 1, "type": "LOC", "mentions": [{"sent_id": 0, "pos": [5, 6]}]}]}

def test_bio_roundtrip():
    tags = bio_tags(DOC)[0]
    assert tags == ["B-PER", "I-PER", "O", "B-PER", "O", "B-LOC", "O"]
    assert decode_bio(tags) == [(0, 2, "PER"), (3, 4, "PER"), (5, 6, "LOC")]

def test_b3_perfect_and_split():
    g = [{1, 2, 3}, {4}]
    assert b_cubed(g, g) == (1.0, 1.0)
    p, r = b_cubed(g, [{1}, {2}, {3}, {4}])
    assert p == 1.0 and abs(r - (1 / 3 * 3 + 1) / 4) < 1e-9

def test_coref_subset_joins_surname():
    spans = {(0, 0, 2, "PER"), (0, 3, 4, "PER"), (0, 5, 6, "LOC")}
    cl = {m for _, m in cluster(DOC, spans)}
    assert frozenset({(0, 0, 2), (0, 3, 4)}) in cl and len(cl) == 2

def test_ner_f1_exact_boundaries():
    pred = [{(0, 0, 2, "PER"), (0, 3, 4, "PER"), (0, 5, 6, "ORG")}]   # LOC mislabelled ORG
    r = ner_f1([DOC], pred)
    assert r["PER"][2] == 1.0 and r["LOC"][1] == 0.0 and abs(r["ALL"][2] - 2 / 3) < 1e-9

def test_linking_unlinkable_counts_as_miss():
    s = linking_scores([["A", "B"], ["X"]], ["B", None])
    assert s["hit@1"] == 0 and s["hit@5"] == 0.5 and s["not_found"] == 0.5


def test_wiki_parsers_and_ranksum():
    import fetch_wiki_candidates as f
    from ldred.linking import CacheIndex, rank_entity_ranksum, merge_ranked
    op = ["lux", ["Luke Skywalker", "Luke"], ["", ""],
          ["https://en.wikipedia.org/wiki/Luke_Skywalker", "https://en.wikipedia.org/wiki/Caf%C3%A9"]]
    assert f.parse_opensearch(op) == ["Luke_Skywalker", "Café"]
    assert f.parse_wbsearch({"search": [{"id": "Q1"}, {"id": "Q2"}]}) == ["Q1", "Q2"]
    idx = CacheIndex({"a": {"wikipedia": ["X", "Y"]}, "b": {"wikipedia": ["Y", "Z"]}}, "wikipedia")
    # Y is rank 1 for "a" and rank 0 for "b" -> score 1 ; X: 0 + (2+1)=3 ; Z: (2+1) + 1 = 4
    assert rank_entity_ranksum(["a", "b"], idx) == ["Y", "X", "Z"]
    assert merge_ranked(["A", "B"], ["B", "C"]) == ["A", "B", "C"]


def test_windows_cover_everything_and_pick_central_window():
    from ldred.ner_transformer import make_windows, best_window
    assert make_windows(10, 512) == [(0, 10)]
    w = make_windows(1000, 512, overlap=128)
    assert w[0][0] == 0 and w[-1][1] == 1000 and all(e - s <= 510 for s, e in w)
    assert all(a[1] > b[0] for a, b in zip(w, w[1:]))                    # consecutive windows overlap
    covered = {p for s, e in w for p in range(s, e)}; assert covered == set(range(1000))
    best = best_window(w, 1000)
    assert best[0] == 0 and best[999] == len(w) - 1


def test_flatten_labels_on_first_subword_only():
    from ldred.ner_transformer import flatten, IGNORE, L2I
    ids, first, widx, lab = flatten([[5], [6, 7, 8], [9]], [L2I["B-PER"], L2I["O"], L2I["B-LOC"]])
    assert ids == [5, 6, 7, 8, 9] and first == [True, True, False, False, True]
    assert widx == [0, 1, 1, 1, 2] and lab == [L2I["B-PER"], 0, IGNORE, IGNORE, L2I["B-LOC"]]


def test_words_to_sentence_tags_does_not_cross_sentences():
    from ldred.ner_transformer import words_to_sentence_tags
    doc = {"sents": [["a", "b"], ["c", "d"]]}
    got = words_to_sentence_tags(doc, ["B-PER", "I-PER", "I-PER", "O"])      # I-PER at start of sentence 2
    assert got == {(0, 0, 2, "PER"), (1, 0, 1, "PER")}
