# Why entities are missed: findings, causes, fixes

Numbers are the share of gold mentions found with the exact span and the right type, copied from `category_analysis_full_test.md`
(Few-NERD, TweetNER7), `category_analysis_800.md` (WNUT-17 sample shared with the LLM) and `category_analysis_crossner.md`.
Examples with the gold entity in bold are in `mismatch_analysis_*.md` (section E).

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
2. **Twitter handle markup.** TweetNER7 writes handles as `{@name@}`: 43% of gold company and product mentions. RoBERTa gets 0% on all of them.
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
