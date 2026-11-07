import bz2, json
from ldred.gazetteer import Gazetteer, norm_token, tokenize_name, predict_docs, hybrid
from fetch_dbpedia_companies import query_for, parse_bindings, read_dumps


def doc(tokens, *mentions):
    return {"sents": [tokens],
            "entities": [{"type": t, "mentions": [{"sent_id": 0, "pos": [a, b]}]} for a, b, t in mentions]}


def test_normalisation_of_tweet_markup_and_names():
    assert norm_token("{@FordPerformance@}") == "fordperformance"
    assert norm_token("@Ford") == "ford" and norm_token("#Ford") == "ford"
    assert tokenize_name("Interplay Productions, Inc.") == ["interplay", "productions", ",", "inc", "."]
    assert tokenize_name("Acme (company)") == ["acme"]


def test_legal_suffix_variants_and_longest_match():
    g = Gazetteer(["Interplay Productions, Inc.", "Twin Galaxies", "Twin"])
    toks = "TSR awarded Interplay Productions , Inc . a license ; Twin Galaxies banned him".split()
    assert g.find(toks) == [(2, 7), (10, 12)]                 # 'Twin Galaxies' wins over 'Twin'
    assert g.find("Interplay Productions rocks".split()) == [(0, 2)]       # variant without the legal suffix


def test_single_word_capitalised_rule_drops_common_words():
    g = Gazetteer(["Sun", "Apple"])
    toks = "the sun and Apple".split()
    assert g.find(toks, "any") == [(1, 2), (3, 4)]
    assert g.find(toks, "capitalised") == [(3, 4)]
    assert g.find(["{@apple@}"], "capitalised") == [(0, 1)]   # handles count as names


def test_membership_and_predict_docs():
    g = Gazetteer(["Flybe"])
    assert ["Flybe"] in g and ["flybe", "x"] not in g
    d = doc("painted in the Flybe livery".split(), (3, 4, "COMP"))
    assert predict_docs(g, [d]) == [{(0, 3, 4, "COMP")}]


def test_hybrid_add_and_relabel():
    g = Gazetteer(["Flybe", "Centrelink"])
    d = doc("Flybe livery and Centrelink".split())
    model = [{(0, 0, 1, "PROD")}]                                  # model calls Flybe a product, misses Centrelink
    added = hybrid(model, g, [d], "add")
    assert added == [{(0, 0, 1, "PROD"), (0, 3, 4, "COMP")}]       # Centrelink added, Flybe left as the model said
    relabelled = hybrid(model, g, [d], "relabel")
    assert relabelled == [{(0, 0, 1, "COMP"), (0, 3, 4, "COMP")}]
    assert hybrid([{(0, 0, 1, "COMP")}], g, [d], "relabel") == [{(0, 0, 1, "COMP"), (0, 3, 4, "COMP")}]


def test_sparql_query_and_bindings():
    q = query_for(["Company", "Organisation"], "A", True, 20000)
    assert "dbo:Company dbo:Organisation" in q and "STRSTARTS(UCASE(STR(?l)), 'A')" in q
    assert "dbo:wikiPageRedirects" in q and q.endswith("LIMIT 10000 OFFSET 20000")
    assert "REGEX" in query_for(["Company"], "other", False, 0) and "UNION" not in query_for(["Company"], "A", False, 0)
    assert parse_bindings({"results": {"bindings": [{"l": {"value": "IBM"}}, {"l": {"value": "Apple Inc."}}]}}) == ["IBM", "Apple Inc."]


def test_read_dumps(tmp_path):
    types = tmp_path / "types.ttl.bz2"
    labels = tmp_path / "labels.ttl"
    rdf = "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>"
    types.write_bytes(bz2.compress((
        f"<http://dbpedia.org/resource/Flybe> {rdf} <http://dbpedia.org/ontology/Company> .\n"
        f"<http://dbpedia.org/resource/Paris> {rdf} <http://dbpedia.org/ontology/City> .\n").encode()))
    labels.write_text(
        '<http://dbpedia.org/resource/Flybe> <http://www.w3.org/2000/01/rdf-schema#label> "Flybe"@en .\n'
        '<http://dbpedia.org/resource/Flybe> <http://www.w3.org/2000/01/rdf-schema#label> "Flybe"@fr .\n'
        '<http://dbpedia.org/resource/Paris> <http://www.w3.org/2000/01/rdf-schema#label> "Paris"@en .\n', encoding="utf-8")
    assert read_dumps(types, labels, ["Company"]) == ["Flybe"]


def test_common_words_stoplist_blocks_one_token_matches():
    from ldred.gazetteer import common_words
    train = [doc("the Apple is good".split(), (1, 2, "COMP")) for _ in range(6)] + \
            [doc("the thing".split()) for _ in range(6)]
    stop = common_words(train)
    assert "the" in stop and "good" in stop and "apple" not in stop
    g = Gazetteer(["The", "Apple"])
    assert g.find("The Apple".split(), "capitalised", stop) == [(1, 2)]


def test_hybrid_relabel_only_and_multiword_add():
    g = Gazetteer(["Flybe", "Twin Galaxies"])
    d = doc("Flybe and Twin Galaxies".split())
    model = [{(0, 0, 1, "PROD")}]
    assert hybrid(model, g, [d], "relabel_only") == [{(0, 0, 1, "COMP")}]          # relabel, nothing added
    assert hybrid([set()], g, [d], "add", min_add_tokens=2) == [{(0, 2, 4, "COMP")}]   # one-word match not added
