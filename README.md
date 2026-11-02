# Text mining final project: person, company and product extraction and linking

Course project (Text Mining / NLP, INSA Lyon, 2026), topic 2. We first re-implement the idea of the
Linked-DocRED baseline (NER, coreference, entity linking; Genest et al., SIGIR 2023) with our own code,
then try other methods.

## Pipeline (own implementation, `ldred/`)
| Stage | Module | Method |
|---|---|---|
| 1. Mention detection | `ner_crf.py` | BIO tagging with a CRF (transformer tagger to come) |
| 2. Coreference | `coref.py` | exact match + surname/subset rule per entity type |
| 3. Entity linking | `linking.py` | train-set alias dictionary, char-3gram fuzzy match, Wikipedia/Wikidata search (cached) |
| Metrics | `metrics.py` | mention F1, B-cubed, entity F1, Hit@k / not found / MRR |

## Data
Linked-DocRED (https://github.com/alteca/Linked-DocRED): `git clone` it next to this repo; it is not
committed here. Folder used by the scripts: `Linked-DocRED/Linked-DocRED`.

## Run
See [RUN.md](RUN.md). Baseline on dev, offline: `python3 run_baseline.py Linked-DocRED/Linked-DocRED`.
Tests: `python3 -m pytest -q tests`.

## Current results (dev split)
| Stage | Result |
|---|---|
| NER mention F1 (CRF) | 0.771 (PER 0.81, LOC 0.81, ORG 0.65, MISC 0.55) |
| Coreference, gold mentions | B3 F1 0.951, entity F1 0.871 |
| Linking, gold entities, alias dictionary + fuzzy | Hit@1 0.289, Hit@5 0.323 |
| End to end (NER + coref + linking) | 0.220 of linkable entities found and linked at rank 1 |

The Wikipedia/Wikidata search linker (the one used in the paper) is evaluated with `fetch_wiki_candidates.py`
and `run_wiki_eval.py`; results will be added here.
