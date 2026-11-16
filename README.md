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

Extra datasets with explicit company/product types: Few-NERD (`organization-company`, `product-*`), WNUT-17 and
TweetNER7 (`corporation`, `product`). `ldred/ner_datasets.py` loads the jsonl dumps and maps them to PER / COMP / PROD /
OTHER (see RUN.md for how they were downloaded and for the training commands in `ner_unified.py`).

## Run
See [RUN.md](RUN.md). Baseline on dev, offline: `python3 run_baseline.py Linked-DocRED/Linked-DocRED`.
Tests: `python3 -m pytest -q tests`.

## Entity extraction experiments (topic 2: PER / COMP / PROD)
Results and reading guide: `results/ner/ANALYSIS.md` (section 0 is the summary). How to run each script: `RUN.md`.

| Script | What it does | Needs GPU |
|---|---|---|
| `ner_unified.py` | train and evaluate a token classifier; `--strip-markup` expands `{@Name@}` tokens, `--media-as-comp` counts Few-NERD media organisations as COMP | yes |
| `strip_markup_eval.py` | CRF with and without the markup | no |
| `bootstrap_llm.py` | paired bootstrap intervals, Llama 70B vs 8B on the same sentences | no |
| `merged_cp.py` | F1 with company and product merged into one type | no |
| `analyze_boundaries.py` | missed / wrong type / boundary error counts and lenient F1 | no |
| `boundary_rules.py` | rule-based boundary repair ("Inc.", "'s", "the") on saved predictions | no |
| `extra_analysis.py` | seed vote, RoBERTa + LLM combination, paired bootstrap, confusion matrix figure (`results/ner/confusion.png`) | no |
| `crf_media.py` | CRF on Few-NERD with and without media-as-company | no |
| `error_examples.py` | real examples per error cause, written to `results/ner/error_examples.md` | no |
| `review_sheet.py` | `make`: sheet of false positives for two human reviewers; `score`: agreement (Cohen's kappa) and F1 if the accepted ones were gold | no |

The no-GPU scripts read saved predictions (`results/ner/runs/<run>/preds_<set>.json`). Smoke tests: `tests/test_analysis_scripts.py`, `tests/test_markup.py`, `tests/test_review_sheet.py`.

## Current results (dev split)
| Stage | Result |
|---|---|
| NER mention F1 (CRF) | 0.771 (PER 0.81, LOC 0.81, ORG 0.65, MISC 0.55) |
| Coreference, gold mentions | B3 F1 0.951, entity F1 0.871 |
| Linking, gold entities, alias dictionary + fuzzy | Hit@1 0.289, Hit@5 0.323 |
| End to end (NER + coref + linking) | 0.220 of linkable entities found and linked at rank 1 |

The Wikipedia/Wikidata search linker (the one used in the paper) is evaluated with `fetch_wiki_candidates.py`
and `run_wiki_eval.py`; results will be added here.
