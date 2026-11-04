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
