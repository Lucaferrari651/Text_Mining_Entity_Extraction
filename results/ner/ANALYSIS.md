# Why entities are missed: findings, causes, fixes

Numbers are the share of gold mentions found with the exact span and the right type, copied from `category_analysis_full_test.md`
(Few-NERD, TweetNER7), `category_analysis_800.md` (WNUT-17 sample shared with the LLM) and `category_analysis_crossner.md`.
Examples with the gold entity in bold are in `mismatch_analysis_*.md` (section E).

## 0. Summary (read this first)
Task: mark every person (PER), company (COMP) and product (PROD) in a sentence. Score: micro-F1, exact span and type, test split of each dataset, one run per setting unless said.

**Best scores.**

| Test set | Best system | F1 | Note |
|---|---|---|---|
| Few-NERD | RoBERTa-base, Few-NERD only | 0.835 | the large model trained on all three sets gets 0.824 (30,000 of 131,767 training sentences, section 11) |
| WNUT-17 | RoBERTa-large, WNUT-17 only | 0.636 | the large model trained on all three sets: 0.630, a difference far inside the interval (±0.035) |
| TweetNER7 | RoBERTa-large, all three sets | 0.733 | base model on all three sets 0.719; Few-NERD-only base model 0.375 |

Best single model for the three sets: **RoBERTa-large trained on all three** (3 seeds: 0.825 / 0.627 / 0.731, mean 0.728; seed std ≤ 0.004, section 15). Without training on the target sets: GLiNER (threshold 0.8) 0.632 / 0.446 / 0.508;
Llama 3.3 70B 0.636 / 0.620 / 0.458 on 300 sentences; Llama 3.1 8B 0.532 / 0.444 / 0.358 on 800 sentences. The 70B is better than the 8B on the same sentences (section 9), but its samples are small and it is not ranked against the trained models.

**What explains the errors (measured).**

| Cause | Evidence | Section |
|---|---|---|
| Different text domain and label definitions | the Few-NERD-only RoBERTa-base gets 0.835 on Few-NERD and 0.375 on TweetNER7; adding the tweet sets brings TweetNER7 to 0.719 | 2, 8 |
| `{@name@}` markup in TweetNER7 | 65% of product and 43% of company mentions in the test set; stripping it lifts the Few-NERD-trained RoBERTa-base from 0.380 to 0.545 (+0.165, interval [0.152, 0.178]), but **lowers** the tweet-trained RoBERTa-large (0.733 → 0.686) | 2, 9, 10, 16 |
| Names never seen | 98% of the gold company and product strings of WNUT-17 are not in its training set | 2, error_examples.md |
| Not found at all | 53% to 67% of the unmatched gold mentions (large model), 80% to 94% for the Wikipedia-trained base model on tweets | 13 |
| Boundaries | counting overlapping right-type predictions as correct adds only +0.03 to +0.06 | 13 |
| Company vs product label | merging the two adds +0.01 to +0.04 for trained models, +0.14 for the 70B on TweetNER7 | 12 |
| Media organisations are OTHER in Few-NERD | examples in `error_examples.md`; company F1 +0.05 (CRF) / +0.02 (RoBERTa-large), overall F1 unchanged | 14, 17 |

**Ideas that did not help.** A DBpedia company dictionary (covers 18% to 39% of gold companies; the overall F1 never improves, section 5); a written guideline in the 8B prompt (the 6-shot baseline is best or tied, section 7); a bigger encoder on Few-NERD alone (0.831 vs 0.835, section 8).
**Sparse sentences.** The paper's pattern (worse in sparse text) does not show up; instead GLiNER and the 8B LLM fire on sentences with nothing to find: 30 to 57 false positives per 100 such sentences for GLiNER, 55 to 60 for the 8B, against 7 to 12 for RoBERTa (section 6).

**Boundary rules (section 20).** Cutting or adding "Inc." / "'s" on the predictions does not help (changes of −0.05 to 0).

**Also run (sections 15 to 19).** Three seeds (std ≤ 0.004); CrossNER (persons transfer, organisations do not); a transformer on Linked-DocRED (0.900 vs CRF 0.771, own metric).

**Not done / open.** Seeds for the other systems (single run), the full Few-NERD training set, DFKI as extra test, a manual review of the false positives
(`review_sheet.csv`, instructions in `review_instructions.md`), a transformer on Linked-DocRED to compare with the paper's 77.2 (our CRF: 0.771, own metric).

**Files.** Scripts: `ner_unified.py` (training, `--strip-markup`, `--media-as-comp`), `bootstrap_llm.py`, `merged_cp.py`, `analyze_boundaries.py`, `strip_markup_eval.py`, `crf_media.py`,
`error_examples.py` (output `error_examples.md`: real examples for each cause), `review_sheet.py`. Runs and predictions: `runs/`. How to run each one: `RUN.md`.

## 1. Which categories are not detected

| Subcategory | Dataset | RoBERTa (Few-NERD) | GLiNER 0.8 |
|---|---|---|---|
| organization -> political party (953) | CrossNER politics | 0% | 65% |
| organization -> band (462) | CrossNER music | 0% | 52% |
| organization -> university (28) | CrossNER AI | 0% | 82% |
| person / corporation / product as `{@handle@}` | TweetNER7 | 0% | 71% / 23% / 1% |
| corporation | WNUT-17 sample | 9% | 28% |
| corporation | TweetNER7 | 7% | 20% |
| product name (197) | CrossNER AI | 59% | 23% |
| product-ship / software / other | Few-NERD | 79% / 81% / 60% | 21% / 32% / 30% |

Persons are easy on Few-NERD (RoBERTa 89-98%, GLiNER 0.8 62-88%). Companies and products are the hard classes, most of all on
tweets. Product written as a handle is found by almost nobody (GLiNER 0.5: 2%).

## 2. Why (causes)

1. **Label definitions differ between datasets.** Few-NERD "company" does not include parties, bands or universities, which
   CrossNER calls organization. RoBERTa finds 0% of them; GLiNER, prompted with "organization", finds 52-82%. This is not a model
   defect, so scores across different label sets should not be compared directly.
2. **Twitter handle markup.** TweetNER7 writes handles as `{@name@}`: 65% of gold product mentions and 43% of gold company mentions (55% of the two together) in the test set. RoBERTa gets 0% on all of them.
3. **Long tail.** In WNUT-17, 98% of gold company and product strings never occur in training. A trained model cannot cover them.
4. **Inconsistent annotation.** The same string carries different labels (e.g. "London": OTHER 777 times, PROD 3 times; "iTunes":
   company and product). In Few-NERD, 15% of company and product mentions come from strings that are OTHER elsewhere.
5. **Company vs product confusion.** Wrong predictions mostly land on neighbouring classes: GLiNER predicts COMP for sports teams,
   media and parties; on tweets RoBERTa predicts PROD for 66 gold corporations; GLiNER marks programming languages and algorithms as ORG on CrossNER AI.
6. **Boundaries.** Long names get the wrong span (e.g. "Evelyn Hunter Nordhoff 's Elephant Bindery").
7. **Different training signal.** Few-NERD product subtypes (ship, train, car, software) work for RoBERTa, which saw those labels,
   but poorly for zero-shot GLiNER, which only gets the word "product".

## 3. Examples (gold entity in bold)

> The new aircraft can seat up to 68 passengers and was the second aircraft to be painted in the **Flybe** livery .
> Gold: COMP | RoBERTa: same span, other type PROD | GLiNER 0.8: found

> 3 weeks from now a **Centrelink** recipient kills himself .
> Gold: PROD | RoBERTa: same span, other type OTHER | GLiNER 0.8: missed

> RT @ jzaffos : Hey federal scientists : @ **highcountrynews** is collecting reports of interference or intimidation .
> Gold: COMP | RoBERTa, GLiNER 0.8 and LLM 8B: missed

## 4. What could be done

1. Normalise the `{@handle@}` markup in TweetNER7 before tokenising (would address the 0% cases; not implemented yet).
2. Use the label wording that matches the dataset (organization on CrossNER) and report the scale used.
3. Train or fine-tune on tweet data (RoBERTa on tweets; GLiNER fine-tuning); the partner's tweet-trained run is not in yet.
4. Tune the GLiNER threshold per type; 0.5 gives more recall and 0.8 more precision.
5. Report relaxed-boundary F1 next to exact-match F1 to separate boundary errors from real misses.

## 5. Company dictionary (DBpedia), suggested by the professor

Dictionary: English labels of DBpedia's `Company` class plus the labels of pages that redirect to it (117,440 names; 128,471 normalised
entries after adding versions without legal suffixes such as "Inc."). Matching is longest-match on tokens, lower-cased, with Twitter markup
removed; one-word matches must be capitalised and are never accepted for words that are almost never entities in the training split.
Code: `fetch_dbpedia_companies.py`, `ldred/gazetteer.py`, `analyze_gazetteer.py`. Few-NERD comes from Wikipedia, so its coverage is optimistic.

**Coverage and dictionary-only baseline** (test sets)

| Dataset | gold COMP in dictionary | gold PROD in the company list | dictionary-only COMP F1 |
|---|---|---|---|
| Few-NERD | 39% (n=3903) | 4% | 0.142 |
| WNUT-17 | 18% (n=66) | 7% | 0.100 |
| TweetNER7 | 18% (n=1091) | 11% | 0.145 |

Coverage is low even on Few-NERD. In a sample of uncovered gold companies the main reasons are abbreviations and short names (NBC, CVS, FBI, MLB),
brands DBpedia probably does not type as Company (Reddit, Spotify, Mercedes, Viacom; not verified), sports and media organisations (Ohio State,
Sky Sports), handle-style concatenations (CocaColaPH, FordPerformance) and annotation noise. Splitting camel-case names recovers only 3 of 1,091
(TweetNER7) and 2 of 66 (WNUT-17) gold companies, so text cleaning is not what limits coverage. False matches come from generic one-word entries
("House", "King", "World", "Night") and, with the legal-suffix variants, from names such as "Air Company" becoming "Air". Dropping the variants
raises precision and lowers recall (company F1 0.12 vs 0.10 on WNUT-17, 0.14 vs 0.145 on TweetNER7, 0.21 vs 0.14 on Few-NERD): no clear winner.

**Model + dictionary** (company P / R / F1 and PER+COMP+PROD micro F1)

- `+ add`: add a company where a dictionary match overlaps no model prediction;
- `+ add (multi-word only)`: the same, only for matches of two or more tokens;
- `+ relabel only`: change a model span of another type to company when it is exactly a dictionary entry, adding nothing;
- `+ add + relabel`: both.

Few-NERD

| System | COMP P | COMP R | COMP F1 | PER+COMP+PROD F1 |
|---|---|---|---|---|
| RoBERTa model | 0.667 | 0.695 | **0.680** | 0.835 |
| RoBERTa + add | 0.465 | 0.698 | **0.558** | 0.812 |
| RoBERTa + add (multi-word only) | 0.557 | 0.695 | **0.618** | 0.824 |
| RoBERTa + relabel only | 0.429 | 0.734 | **0.541** | 0.798 |
| RoBERTa + add + relabel | 0.340 | 0.738 | **0.465** | 0.777 |
| GLiNER 0.8 model | 0.344 | 0.638 | **0.447** | 0.632 |
| GLiNER 0.8 + add | 0.145 | 0.687 | **0.240** | 0.545 |
| GLiNER 0.8 + add (multi-word only) | 0.289 | 0.661 | **0.402** | 0.618 |
| GLiNER 0.8 + relabel only | 0.327 | 0.649 | **0.435** | 0.622 |
| GLiNER 0.8 + add + relabel | 0.144 | 0.699 | **0.239** | 0.537 |

WNUT-17

| System | COMP P | COMP R | COMP F1 | PER+COMP+PROD F1 |
|---|---|---|---|---|
| RoBERTa model | 0.312 | 0.076 | **0.122** | 0.516 |
| RoBERTa + add | 0.082 | 0.091 | **0.086** | 0.492 |
| RoBERTa + add (multi-word only) | 0.172 | 0.076 | **0.105** | 0.510 |
| RoBERTa + relabel only | 0.250 | 0.167 | **0.200** | 0.505 |
| RoBERTa + add + relabel | 0.119 | 0.182 | **0.144** | 0.483 |
| GLiNER 0.8 model | 0.267 | 0.303 | **0.284** | 0.446 |
| GLiNER 0.8 + add | 0.134 | 0.348 | **0.193** | 0.416 |
| GLiNER 0.8 + add (multi-word only) | 0.217 | 0.303 | **0.253** | 0.440 |
| GLiNER 0.8 + relabel only | 0.250 | 0.318 | **0.280** | 0.439 |
| GLiNER 0.8 + add + relabel | 0.133 | 0.364 | **0.194** | 0.409 |

TweetNER7

| System | COMP P | COMP R | COMP F1 | PER+COMP+PROD F1 |
|---|---|---|---|---|
| RoBERTa model | 0.417 | 0.039 | **0.072** | 0.375 |
| RoBERTa + add | 0.200 | 0.143 | **0.167** | 0.371 |
| RoBERTa + add (multi-word only) | 0.222 | 0.041 | **0.070** | 0.370 |
| RoBERTa + relabel only | 0.287 | 0.075 | **0.119** | 0.370 |
| RoBERTa + add + relabel | 0.203 | 0.179 | **0.190** | 0.367 |
| GLiNER 0.8 model | 0.366 | 0.210 | **0.267** | 0.508 |
| GLiNER 0.8 + add | 0.190 | 0.283 | **0.227** | 0.474 |
| GLiNER 0.8 + add (multi-word only) | 0.309 | 0.214 | **0.253** | 0.502 |
| GLiNER 0.8 + relabel only | 0.351 | 0.210 | **0.263** | 0.504 |
| GLiNER 0.8 + add + relabel | 0.187 | 0.283 | **0.225** | 0.471 |

**Reading.** The dictionary does not improve over the models. On Few-NERD every variant is worse than the model alone. For GLiNER the best
variant at most ties the model on every dataset. The overall PER+COMP+PROD F1 never improves; the added company spans are mostly false
positives. It helps only RoBERTa (trained on Few-NERD) on tweets and WNUT-17, where that model almost never predicts a company (recall 4% and 8%),
and even then it stays below GLiNER alone (0.19 vs 0.27 on TweetNER7). WNUT-17 has only 66 gold companies, so a change of a few mentions moves F1 a lot.

**Most of the gain on tweets is probably the markup problem.** 470 of the 1,091 gold companies in TweetNER7 are written as `{@name@}`, and RoBERTa
finds only 43 of the 1,091. Of the 113 correct companies the dictionary adds for RoBERTa on TweetNER7, 100 are handle-markup strings. So the dictionary
mostly compensates for the model not handling the markup. If the markup is normalised before the model sees it, RoBERTa should improve on its own and
the dictionary's gain should shrink. This is a hypothesis, not yet tested (it needs a rerun on normalised tweets).

**Why a dictionary cannot decide between company and product.** The same string can be a company in one sentence and a product in another
("Etsy" and "Poshmark" are product in some gold tweets), and relabelling every exact match to company can turn a correct product prediction into a
wrong company. This is a likely explanation of the drops with relabelling on Few-NERD; it has not been checked case by case.

Limits: one dictionary setting (Company class only), one prediction file per model, single run.

## 6. Does detection get worse when the sentence has few entities? (idea from the information-density paper)

`analyze_density.py`: density of a test sentence = gold entity tokens (all types) / tokens; sentences with at least one person, company or product are
split into three equal groups (low / middle / high), and sentences with none are kept apart because only false positives can happen there.
Full test sets, RoBERTa trained on Few-NERD and GLiNER 0.8 (recall of gold mentions with exact span and type; FP = false positives per 100 sentences).

| Dataset | Group | RoBERTa recall all / COMP | RoBERTa FP | GLiNER recall all / COMP | GLiNER FP |
|---|---|---|---|---|---|
| Few-NERD | no target entity | - | 7.2 | - | 30.1 |
| Few-NERD | low density | 84% / 66% | 19.7 | 65% / 70% | 36.5 |
| Few-NERD | middle density | 85% / 72% | 24.8 | 64% / 67% | 41.0 |
| Few-NERD | high density | 85% / 69% | 31.4 | 66% / 59% | 46.3 |
| WNUT-17 | no target entity | - | 10.7 | - | 19.1 |
| WNUT-17 | low density | 48% / 15% | 23.5 | 36% / 30% | 16.7 |
| WNUT-17 | middle density | 52% / 5% | 19.7 | 43% / 29% | 16.3 |
| WNUT-17 | high density | 40% / 4% | 34.2 | 41% / 32% | 30.3 |
| TweetNER7 | no target entity | - | 11.6 | - | 57.1 |
| TweetNER7 | low density | 18% / 2% | 17.3 | 45% / 27% | 38.0 |
| TweetNER7 | middle density | 27% / 6% | 22.6 | 43% / 20% | 31.8 |
| TweetNER7 | high density | 30% / 4% | 33.1 | 41% / 18% | 42.4 |

(The full tables with person and product recall, sentence counts and the 800-sentence version with the 8B LLM are produced by the script.)

**Reading.** The paper's pattern (worse in sparse text) does not show up here. Recall is flat in Few-NERD, goes up with density for RoBERTa on tweets
(18% to 30%; but that model fails on the `{@handle@}` markup, and denser sentences are shorter, so length and markup are mixed in), and falls with
density for GLiNER's company recall (70% to 59% on Few-NERD, 27% to 18% on TweetNER7). Two things are clear instead:
- **False positives rise with density** for every system (more entities, more chances to mark a wrong span).
- **GLiNER fires on sentences with nothing to find**: 30 false positives per 100 sentences on Few-NERD and 57 on TweetNER7 where the gold has no person, company
  or product, against 7 and 12 for RoBERTa. On the 800-sentence sample the 8B LLM does the same (55 and 60 per 100 sentences on Few-NERD and TweetNER7).
This is a different question from the paper's: the paper trains on WNUT-17 subsets of different density, while we measure how already-trained or zero-shot
systems behave on test sentences of different density, so we do not test the paper's claim about training data. Few-NERD and TweetNER7 sentences with no
target entity are 56% and 21% of the test sets, so this false-positive rate matters for precision.

## 7. Written annotation guidelines in the LLM prompt (GuideNER idea)

Llama 3.1 8B, same 300 sampled test sentences per dataset, one run each. `guide`: the system message is a written guideline (`GUIDELINE` in
`ldred/llm_ner.py`; person / company / product definitions with explicit exclusions such as governments, universities, parties, sports teams, bands,
creative works), no examples. `guide+shots`: the guideline plus the same 6 examples as the baseline. The guideline was written from the datasets' public
annotation schemes before these runs, but after the error analyses above, so it is not independent of what we saw on the test data. Unlike GuideNER, it is
written by hand, not derived from training data.

| Dataset | Prompt | P | R | F1 | PER F1 | COMP F1 | PROD F1 |
|---|---|---|---|---|---|---|---|
| Few-NERD | 6 shots | 0.495 | 0.543 | **0.518** | 0.671 | 0.393 | 0.187 |
| Few-NERD | guide | 0.314 | 0.704 | 0.434 | 0.598 | 0.263 | 0.218 |
| Few-NERD | guide+shots | 0.446 | 0.479 | 0.462 | 0.593 | 0.367 | 0.200 |
| WNUT-17 | 6 shots | 0.514 | 0.351 | **0.417** | 0.543 | 0.345 | 0.147 |
| WNUT-17 | guide | 0.243 | 0.513 | 0.330 | 0.463 | 0.273 | 0.138 |
| WNUT-17 | guide+shots | 0.558 | 0.312 | 0.400 | 0.513 | 0.176 | 0.200 |
| TweetNER7 | 6 shots | 0.445 | 0.307 | **0.364** | 0.543 | 0.227 | 0.074 |
| TweetNER7 | guide | 0.285 | 0.398 | 0.332 | 0.472 | 0.281 | 0.108 |
| TweetNER7 | guide+shots | 0.506 | 0.284 | **0.364** | 0.534 | 0.241 | 0.070 |

Gold company mentions found (exact span and type) / predicted companies that are wrong:

| Dataset (gold COMP) | 6 shots | guide | guide+shots |
|---|---|---|---|
| Few-NERD (37) | 24 found / 61 wrong | 27 / 141 | 27 / 83 |
| WNUT-17 (17) | 5 / 7 | 12 / 59 | 3 / 14 |
| TweetNER7 (84) | 20 / 72 | 38 / 148 | 19 / 55 |

Gold product mentions found / wrong predicted products:

| Dataset (gold PROD) | 6 shots | guide | guide+shots |
|---|---|---|---|
| Few-NERD (37) | 10 / 60 | 21 / 135 | 10 / 53 |
| WNUT-17 (33) | 5 / 30 | 10 / 102 | 5 / 12 |
| TweetNER7 (116) | 7 / 66 | 16 / 165 | 6 / 50 |

**Reading.**
- The guideline does not improve overall F1: the 6-shot baseline is best or tied in every dataset.
- Without examples, the guideline makes the model find more companies and products (companies found on TweetNER7 20 to 38, on WNUT-17 5 to 12; products found on
  Few-NERD 10 to 21), but it also more than doubles the number of wrong company and product predictions, so precision collapses (Few-NERD 0.50 to 0.31).
  The exclusion lists did not teach the model to stay quiet; it labels more things as company or product.
- With examples added, the model falls back to roughly the baseline behaviour: no gain in found mentions, slightly fewer wrong predictions, and a small
  loss of overall F1. The examples dominate the guideline.
- The only company F1 gain is TweetNER7 with the guideline alone (0.227 to 0.281); the WNUT-17 company F1 of guide+shots (0.176) rests on 17 gold mentions.
- Samples are small (17 to 116 gold mentions per type), single run, one hand-written guideline: differences of a few mentions are within noise.
This agrees with the over-triggering found in section 6: the weakness of the small LLM is precision, and a text description alone does not fix it.

## 8. Supervised RoBERTa-large (training on the dataset's own training split)

Goal of this part: the highest score, so the model is trained on the dataset's own data (`ner_unified.py --keep-best`: the epoch with the best validation F1
is restored; the test split is scored once). Unified labels PER / COMP / PROD / OTHER, same metric as before (mention-level, exact span and type).
These are supervised results and are not directly comparable with the zero-shot and few-shot systems above.
Numbers are copied from the console output of the Colab runs; the prediction files of these two runs were lost when the Colab runtime was reset, so
no per-entity comparison is available for them.

| Dataset | Training data | Setup | P | R | F1 | PER F1 | COMP F1 | PROD F1 |
|---|---|---|---|---|---|---|---|---|
| WNUT-17 | WNUT-17 train (3,394 sentences) | roberta-large, 10 epochs, lr 2e-5, batch 16, best epoch 10 (dev F1 0.697) | 0.700 | 0.582 | **0.636** | 0.740 | 0.496 | 0.262 |
| Few-NERD | Few-NERD train (131,767 sentences) | roberta-large, 3 epochs, lr 2e-5, batch 16, best epoch 1 (dev F1 0.864) | 0.824 | 0.838 | **0.831** | 0.897 | 0.687 | 0.695 |

Comparison on the same full test sets (all systems in sections above):

| Dataset | RoBERTa-large own data | RoBERTa-base trained on all three | RoBERTa-base trained on Few-NERD | GLiNER 0.8 zero-shot | Llama 3.3 70B few-shot (300 sent.) |
|---|---|---|---|---|---|
| WNUT-17 | **0.636** | 0.564 | 0.516 | 0.446 | 0.620 |
| Few-NERD | 0.831 | 0.834 | 0.835 | 0.632 | 0.636 |

**Reading.**
- On WNUT-17, training on the dataset's own data gives the best result so far (+0.07 over the base model trained on all three sets, +0.12 over the
  Few-NERD model). Precision and recall both improve. The company F1 (0.496) is still below the 70B LLM (0.578, 300 sentences), and product F1 (0.262) is no better than the other systems.
- On Few-NERD, the large model does not improve on the base model (0.831 vs 0.835); the best validation epoch was the first, and two more epochs did not help.
  So Few-NERD seems saturated for this approach, and more model size or more epochs is not where the gain is.
- Products remain the weakest type on WNUT-17; companies and products on Few-NERD stay near 0.69.
- Not done: the run on all three datasets together and the TweetNER7 run, because the free Colab GPU quota ran out; WNUT-17 is a single run with 66 gold companies in the test set.

## 9. Strip the `{@Name@}` markup (CRF, CPU) and bootstrap intervals
Test: replace each `{@Name@}` token (3,306 in the TweetNER7 test set) by the words of the name and map the gold mentions to the new positions
(`ldred/markup.py`, `strip_markup_eval.py`). Model: our CRF (not RoBERTa), Few-NERD training capped at 20,000 sentences, 60 iterations, one run.
Micro-F1 over PER/COMP/PROD on the TweetNER7 test set.

| CRF trained on | Test as is | Test stripped |
|---|---|---|
| Few-NERD (Wikipedia, no markup) | 0.210 (PROD 0.026) | **0.309** (PROD 0.160) |
| TweetNER7 as is | **0.636** | 0.391 |
| TweetNER7 stripped | 0.405 | **0.584** |

**Reading.**
- For a model trained on Wikipedia, stripping the markup raises the tweet score by 0.10 (product F1 from 0.03 to 0.16). So the markup is a real part of the
  drop, but not all of it: 0.31 is still far below the in-domain scores.
- For a model trained on tweets the markup is a useful cue (it marks a handle that is usually an entity): training and testing as is gives 0.636, stripped
  gives 0.584. So stripping is not a free gain when the training data has the markup.
- Caveat: this is the CRF. The RoBERTa version needs a GPU (`--strip-markup` in `ner_unified.py`, see RUN.md); the effect could differ.

Bootstrap (2,000 resamples of the sentences, 95% interval, `bootstrap_llm.py`; micro-F1 over PER/COMP/PROD):

| Dataset | Llama 8B (800 sent.) | Llama 70B (300 sent.) | 70B minus 8B, same sentences |
|---|---|---|---|
| Few-NERD | 0.532 [0.486, 0.572] | 0.636 [0.576, 0.691] | +0.113 [0.056, 0.176] |
| WNUT-17 | 0.444 [0.388, 0.498] | 0.620 [0.537, 0.694] | +0.181 [0.099, 0.274] |
| TweetNER7 | 0.358 [0.327, 0.387] | 0.458 [0.411, 0.504] | +0.093 [0.043, 0.143] |

The 70B is better than the 8B on the same sentences (the interval excludes zero). The 70B intervals are wide (WNUT-17: 154 gold mentions), so a gap of a few points to the trained models is not meaningful.

## 10. Strip the markup with RoBERTa-base (GPU run)
Same model as section 9 but RoBERTa-base: trained on Few-NERD only (first 30,000 training sentences, 3 epochs, best validation epoch, seed 13), scored on the
TweetNER7 test set (5,591 gold mentions of PER/COMP/PROD) as it is (`m_raw`) and with every `{@Name@}` token replaced by the words of the name (`m_strip`,
`--strip-markup`; the gold mentions are the same, remapped to the new positions).

| Test set | PER | COMP | PROD | All (micro-F1) | Precision | Recall |
|---|---|---|---|---|---|---|
| As it is | 0.532 | 0.083 | 0.106 | 0.380 | 0.650 | 0.268 |
| Markup stripped | 0.728 | 0.150 | 0.152 | **0.545** | 0.695 | 0.448 |

- Stripping the markup raises the TweetNER7 F1 of the Wikipedia-trained model from 0.380 to 0.545 (+0.165, bootstrap 95% interval [0.152, 0.178] over the
  test sentences; `results/ner/strip_markup_roberta_bootstrap.json`). Almost all of the gain is recall (0.268 → 0.448).
- Person improves most (0.53 → 0.73): many of the marked-up strings are people and organisation accounts. Company (0.08 → 0.15) and product (0.11 → 0.15)
  also improve but stay low. So the markup is a large part of the drop from Few-NERD (0.835) to tweets, and the rest (company/product definitions,
  unseen names) is still there.
- This agrees with the CRF test (section 9, 0.210 → 0.309), with a larger effect for RoBERTa. The CRF also showed that the markup is a useful cue when the
  training data has it (tweet-trained CRF: 0.636 as is, 0.584 stripped); this was not tested with RoBERTa.
- Limits: one seed, a 30,000-sentence training cap (the full-data run in the main table gave 0.375 as is), only the Few-NERD-trained model. The interval
  covers the test sentences, not seeds.

## 11. One RoBERTa-large model trained on all three datasets
Run `s_all_rl`: RoBERTa-large trained on Few-NERD (first 30,000 sentences), WNUT-17 and TweetNER7 training splits together, 2 epochs, learning rate 2e-5, batch
size 16, best validation epoch (validation of all three sets), seed 13, markup left as it is. Scored once on the full test split of each set (micro-F1 over PER/COMP/PROD,
exact span and type). 95% intervals: 2,000 bootstrap resamples of the test sentences (`results/ner/bootstrap_roberta_large_all.json`).

| Test set | PER | COMP | PROD | All | 95% interval |
|---|---|---|---|---|---|
| Few-NERD | 0.893 | 0.670 | 0.683 | 0.824 | [0.819, 0.829] |
| WNUT-17 | 0.722 | 0.406 | 0.365 | 0.630 | [0.593, 0.664] |
| TweetNER7 | 0.833 | 0.519 | 0.657 | 0.733 | [0.721, 0.744] |

Comparison with the other supervised runs (full test sets, one seed each):

| System | Few-NERD | WNUT-17 | TweetNER7 | Mean of the three |
|---|---|---|---|---|
| RoBERTa-base, Few-NERD only | 0.835 | 0.516 | 0.375 | 0.575 |
| RoBERTa-base, all three sets | 0.834 | 0.564 | 0.719 | 0.706 |
| RoBERTa-large, own data (one model per set) | 0.831 | 0.636 | not run | – |
| **RoBERTa-large, all three sets (this run)** | 0.824 | 0.630 | 0.733 | **0.729** |

**Reading.**
- This is the best single model across the three sets: it is the best system on TweetNER7 (0.733 against 0.719 for the base model trained on all three) and
  close to the best on WNUT-17 (0.630 against 0.636 for the large model trained on WNUT-17 alone, a difference far inside the WNUT-17 interval of about ±0.035).
- On Few-NERD it is 0.011 below the base model (0.824 against 0.835); this run used only 30,000 of the 131,767 Few-NERD training sentences and 2 epochs, so the gap may
  come from the smaller training data rather than from the model. The Few-NERD interval is narrow (±0.005), so this small difference is probably real for this setting.
- The gains over the base model trained on all three are small (+0.014 on TweetNER7, +0.066 on WNUT-17, −0.010 on Few-NERD) and come from one seed, so we do not claim that the
  large model is better in general. We can say it gives the best mean score, with one model for all three sets.
- Company and product stay the weak types outside Wikipedia: WNUT-17 COMP 0.406 and PROD 0.365 (PROD recall only 0.29), TweetNER7 COMP 0.519.
- Not done: the markup-stripped version of this model, other seeds, and the full Few-NERD training set.

## 12. Company and product scored as one type
Question: how much of the low company/product score is confusion between the two labels, and how much is not finding the mention (or its boundaries) at all?
`merged_cp.py` renames both gold and predicted COMP and PROD to one type CP and scores again (exact span still required), on the saved predictions
(`results/ner/merged_cp.json`). Micro-F1 over PER/COMP/PROD (`3 types`) against PER/CP (`merged`); `CP` is the F1 of the merged type alone.

| System | Test set | 3 types | merged | COMP | PROD | CP |
|---|---|---|---|---|---|---|
| RoBERTa-large, all three sets | Few-NERD | 0.824 | 0.832 | 0.670 | 0.683 | 0.703 |
| | WNUT-17 | 0.630 | 0.645 | 0.406 | 0.365 | 0.439 |
| | TweetNER7 | 0.733 | 0.770 | 0.519 | 0.657 | 0.680 |
| RoBERTa-base, Few-NERD only | TweetNER7, as is | 0.380 | 0.389 | 0.083 | 0.106 | 0.122 |
| | TweetNER7, markup stripped | 0.545 | 0.563 | 0.150 | 0.152 | 0.209 |
| Llama 3.3 70B (300 sent.) | Few-NERD / WNUT-17 / TweetNER7 | 0.636 / 0.620 / 0.458 | 0.639 / 0.627 / 0.595 | | | 0.319 / 0.440 / 0.497 |
| Llama 3.1 8B (800 sent.) | Few-NERD / WNUT-17 / TweetNER7 | 0.532 / 0.444 / 0.358 | 0.541 / 0.450 / 0.397 | | | 0.352 / 0.176 / 0.230 |

**Reading.**
- For the supervised models, merging company and product helps only a little (+0.008 on Few-NERD, +0.015 on WNUT-17, +0.037 on TweetNER7 for the large model). The
  low company and product scores are therefore mostly mentions that are missed or have the wrong boundaries, not company/product label swaps. Even merged, the CP F1 stays at 0.44 on WNUT-17
  and 0.21 for the Few-NERD-trained base model on stripped tweets.
- The one case with a large effect is the 70B LLM on TweetNER7 (0.458 → 0.595): it finds many company/product mentions but often with the other label, so a part of its
  low score is the definition gap (consistent with "Twitter" being 142 times company and 11 times product).
- On TweetNER7 the trained large model also gains most from merging (company 0.519, merged 0.680): its remaining company/product errors include the company-or-product choice.
- Caveat: the LLM rows are on the 300 / 800-sentence samples; all rows are single runs.

## 13. Boundary errors: how many missed mentions are only a boundary problem?
`analyze_boundaries.py` (saved predictions only, `results/ner/boundaries.json`). Each gold mention of PER/COMP/PROD that is not found exactly is put in one class:
*wrong type* (same span, other type), *boundary* (a prediction of the right type overlaps it with other boundaries), *boundary + type* (overlap, other type), *missed* (no prediction touches it).
*Lenient F1*: a right-type prediction that overlaps a gold mention counts as correct (one prediction per gold mention); *exact F1* is the normal score (it reproduces the tables above).

Share of the not-exactly-found gold mentions:

| System | Test set | Exact F1 | Lenient F1 | Wrong type | Boundary | Boundary + type | Missed |
|---|---|---|---|---|---|---|---|
| RoBERTa-large, all three | Few-NERD | 0.824 | 0.881 | 10% | 35% | 2% | 53% |
| | WNUT-17 | 0.630 | 0.691 | 11% | 20% | 2% | 67% |
| | TweetNER7 | 0.733 | 0.765 | 25% | 13% | 3% | 60% |
| RoBERTa-base, Few-NERD only | TweetNER7 as is | 0.380 | 0.422 | 2% | 4% | 1% | 94% |
| | TweetNER7 stripped | 0.545 | 0.629 | 4% | 14% | 2% | 80% |
| Llama 70B (300 sent.) | Few-NERD / WNUT-17 / TweetNER7 | 0.636 / 0.620 / 0.458 | 0.669 / 0.641 / 0.470 | 10% / 2% / 31% | 21% / 5% / 2% | 4% / 6% / 1% | 65% / 88% / 65% |
| Llama 8B (800 sent.) | Few-NERD / WNUT-17 / TweetNER7 | 0.532 / 0.444 / 0.358 | 0.586 / 0.474 / 0.375 | 5% / 3% / 7% | 14% / 4% / 2% | 2% / 1% / 1% | 80% / 92% / 90% |

**Reading.**
- Boundaries are not the main problem. Counting overlapping right-type predictions as correct raises the large model by only +0.057 (Few-NERD), +0.061 (WNUT-17) and +0.032 (TweetNER7).
  The main loss is mentions that are not found at all (53% to 67% of the unmatched gold mentions for the large model, 80% to 94% for the Few-NERD-trained base model on tweets).
- Stripping the markup moves the base model's errors from "not found" (94% → 80%) to "found with other boundaries" (4% → 14%): the mentions are now seen but not always cut like the gold.
- Wrong type matters mainly on TweetNER7: 25% of the large model's unmatched gold mentions and 31% of the 70B's (the company/product definition issue of section 12).
- For company and product boundary errors of the large model on Few-NERD (1,106 cases), the prediction is shorter than the gold in 752 and longer in 346. The gold often includes a head noun or
  punctuation the model leaves out ("Wii model" gold, "Wii" predicted; "Kibi dango" gold, "Kibi" predicted; a trailing "'s", "." or ")"), and sometimes the model adds a name part the gold leaves out
  ("Boeing B-52 Stratofortress" against "Boeing B-52"). On TweetNER7 the same count is 62 shorter and 15 longer (often a leading "The" or place name in the gold).
- So a boundary-tolerant score would help a little, but not change the ranking; the larger gains must come from finding the mentions.
- Caveat: lenient F1 is our approximation (right type, any overlap); one run per system.

## 14. Media organisations counted as company (CRF, CPU)
Few-NERD labels newspapers, TV and radio stations as `organization-media/newspaper`, which we map to OTHER. Many people would call the BBC a company, and the models often predict COMP for such names (examples in `error_examples.md`, section 5).
`crf_media.py` trains our CRF on 20,000 Few-NERD sentences twice and scores each with its own definition: with the normal mapping (3,903 gold COMP in test) and with media organisations as COMP (5,137 gold COMP in test).

| Mapping | PER | COMP | PROD | ALL |
|---|---|---|---|---|
| normal | 0.756 | 0.381 | 0.374 | 0.656 |
| media as COMP | 0.755 | 0.429 | 0.385 | 0.652 |

Reading: with the broader company definition the company score rises by 0.048, and the overall score is unchanged (0.656 vs 0.652). The two rows are two label definitions, not one model beating another, and a CRF is not the transformer. So the definition of "company" moves the company score by about 5 points but not the total, because the extra gold mentions add as many misses as hits. The RoBERTa version of this test is in the Colab notebook (block 3) and is not run yet.
Single run, no interval.

## 15. Three seeds of RoBERTa-large trained on all three sets
Seeds 13 (section 11), 14 and 15, same settings (30,000 Few-NERD sentences, 2 epochs, lr 2e-5, batch 16). Runs `s_all_rl`, `s_all_rl_seed14`, `s_all_rl_seed15`.

| Seed | Few-NERD | WNUT-17 | TweetNER7 |
|---|---|---|---|
| 13 | 0.824 | 0.630 | 0.733 |
| 14 | 0.825 | 0.628 | 0.732 |
| 15 | 0.826 | 0.623 | 0.729 |
| mean (std) | 0.825 (0.001) | 0.627 (0.004) | 0.731 (0.002) |

The seed changes the score by at most 0.007 (WNUT-17), far less than the differences between systems (e.g. 0.731 vs 0.375 on TweetNER7 for the Few-NERD-only base model). Differences of 0.005 or less between two single runs elsewhere in this file are inside this noise. Mean over the three sets: 0.728.

## 16. Strip the markup, RoBERTa-large trained on all three sets
Run `s_all_rl_strip` (seed 13): `{@Name@}` expanded in train, validation and test, all three sets.

| Test set | markup kept (seed 13) | markup stripped |
|---|---|---|
| Few-NERD | 0.824 | 0.825 |
| WNUT-17 | 0.630 | 0.611 |
| TweetNER7 | 0.733 | 0.686 |

Stripping **lowers** the score of a model that was trained on tweets (TweetNER7 −0.047, WNUT-17 −0.019). It is the opposite of section 10 (Few-NERD-trained model, +0.165). Reading: the markup is a problem for a model that never saw it, but it also carries information (a `{@...@}` token is a mention of a person, company or product almost by itself), which a tweet-trained model uses. The CRF showed the same sign (section 9). So the markup explains the Wikipedia-to-tweets drop, but not the gap of the best model, and removing it is not a general improvement. Single seed; the TweetNER7 change is 20 times the seed std.

## 17. Media organisations as company, RoBERTa-large
Run `s_all_rl_media`: media organisations (BBC, NBC...) are COMP in train, validation and test (Few-NERD test COMP 3,903 → 5,137). Compare with section 11 and 15.

| Test set | normal (3 seeds) | media as COMP |
|---|---|---|
| Few-NERD, ALL | 0.825 | 0.823 |
| Few-NERD, COMP | 0.670 to 0.673 | 0.695 |
| WNUT-17 | 0.627 | 0.621 |
| TweetNER7 | 0.731 | 0.737 |

Same result as the CRF (section 14): the company score on Few-NERD rises by about 0.02 and the overall score does not move. The WNUT-17 and TweetNER7 test sets are unchanged by the option, so their differences (−0.006, +0.006) are training effects of the same size as seed noise. Company and overall F1 are measured against two different gold definitions on Few-NERD, so this is about the definition, not an improvement of the model.

## 18. CrossNER (other domains, labels PER / ORG / PROD)
Run `s_all_rl_cross`: the same model as section 11, tested on the five CrossNER domains; our COMP predictions count as ORG, scored on PER+ORG+PROD (`--b2nerd-dir`).

| Domain | micro F1 | P | R | PER | ORG | PROD |
|---|---|---|---|---|---|---|
| AI | 0.658 | 0.706 | 0.616 | 0.956 | 0.389 | 0.493 |
| Literature | 0.891 | 0.927 | 0.858 | 0.952 | 0.220 | 0.000 |
| Music | 0.607 | 0.887 | 0.461 | 0.930 | 0.049 | 0.000 |
| Politics | 0.512 | 0.945 | 0.351 | 0.958 | 0.008 | 0.000 |
| Science | 0.739 | 0.922 | 0.617 | 0.962 | 0.020 | 0.000 |

Persons transfer (0.93 to 0.96 everywhere). ORG is near zero in politics, music and science and PROD is 0 outside AI: precision stays high (0.89 to 0.95) and recall is low, which is the label-definition effect of section 2 (CrossNER "organization" includes parties, bands, universities, which Few-NERD company does not). The high literature micro F1 comes from persons dominating that set, not from better organisations. These scores should not be compared with the Few-NERD/WNUT/Tweet scores.

## 19. A transformer on Linked-DocRED (dev)
`roberta_ldred_metrics.json`: RoBERTa trained on the Linked-DocRED NER annotation, same own mention-level metric as our CRF (section on the pipeline in README).

| Type | CRF | RoBERTa |
|---|---|---|
| ALL | 0.771 | 0.900 |
| PER | 0.81 | 0.953 |
| LOC | 0.81 | 0.926 |
| ORG | 0.65 | 0.844 |
| MISC | 0.55 | 0.803 |

The CRF is far below a transformer on this data (+0.13); the paper's PURE reports 77.2 on its own metric, so the CRF was close to the paper and the transformer is clearly above it. Dev split only, one run, our metric (not the paper's scorer), so we do not claim to beat the paper.

## 20. Repairing boundaries with rules ("Inc.", "'s", leading "the")
`boundary_rules.py` edits the saved predictions and re-scores (no GPU). Rules: cut a final legal-form token (Inc, Ltd, Corp...), cut a final `'s`, cut a leading "the"; and the opposite direction, add a following "Inc."/`'s`. Test sets, exact span and type, micro-F1 before → after.

| Run / test set | cut suffix | cut `'s` | cut "the" | add suffix | add `'s` |
|---|---|---|---|---|---|
| RoBERTa-large all three / Few-NERD | 0.824 → 0.814 | 0.824 → 0.824 | 0.824 → 0.824 | 0.824 → 0.824 | 0.824 → 0.779 |
| same / WNUT-17 | 0.630 → 0.628 | 0.630 → 0.630 | 0.630 → 0.630 | 0.630 → 0.630 | 0.630 → 0.592 |
| same / TweetNER7 | 0.733 → 0.732 | 0.733 → 0.733 | 0.733 → 0.732 | 0.733 → 0.733 | 0.733 → 0.711 |
| Llama 70B / Few-NERD (300 sent.) | 0.636 → 0.633 | 0.636 → 0.636 | 0.636 → 0.636 | 0.636 → 0.636 | 0.636 → 0.583 |

No rule improves any score; several lower it. Reasons, from the counts in `boundary_rules.json`:
- In Few-NERD 358 gold company spans end in a legal-form token, so the annotators keep "Inc." in the name. Cutting it changed 489 predictions, of which 344 were exact before and only 21 became exact (−0.010).
- The opposite rule almost never fires (6 predictions in Few-NERD): the model already includes "Inc." when the gold does.
- Adding `'s` changes 1,937 predictions in Few-NERD, 1,516 of them correct before, and 77 become correct: the gold excludes the possessive almost always.
- The other rules touch 0 to 58 predictions.

So the "Inc." / `'s` errors are not systematic enough to fix with a rule; they follow the annotation conventions of each dataset, and the models have already learned them. This matches section 13 (boundary errors are a minor part, and lenient F1 only gains +0.03 to +0.06): the remaining boundary errors are individual cases such as "TRS-80 computer" vs "TRS-80" in `error_examples.md`. Rules tested on predictions of one run per system; the Llama rows use the 300-sentence sample.
