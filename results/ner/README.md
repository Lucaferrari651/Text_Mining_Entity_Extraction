# NER results (person / company / product)

Everything here comes from the scripts in the repo root; the commands are in `RUN.md`. One seed (13) per run, no tuning on test sets
(GLiNER threshold 0.8 was chosen on the validation splits, see below).

## Headline (micro F1 over PER+COMP+PROD, full test sets)
| System | Few-NERD | WNUT-17 | TweetNER7 |
|---|---|---|---|
| RoBERTa-base, trained on Few-NERD | 0.835 | 0.516 | 0.375 |
| RoBERTa-base, trained on Few-NERD + WNUT-17 + TweetNER7 | 0.834 | 0.564 | 0.719 |
| GLiNER zero-shot, threshold 0.5 | 0.552 | 0.404 | 0.479 |
| GLiNER zero-shot, threshold 0.8 (chosen on validation) | 0.632 | 0.446 | 0.508 |
| Llama 3.1 8B, 6 shots (800 random sentences per set) | 0.532 | 0.444 | 0.358 |

The LLM was run on a fixed random sample, so `comparison.md` also scores every system on exactly those sentences. The second
RoBERTa row is no longer a transfer test for the tweet sets (their training splits are in its training data).
CrossNER (test only, from B2NERD; scored as PER/ORG/PROD) is in `runs/g_cross_t08` and `runs/u_fewnerd_roberta_cross`.

## Files
- `comparison.md/.json`: all systems on the same sentences, plus what happened to each gold company/product mention.
- `category_analysis_*.md`: share of gold mentions found per fine-grained category, and which gold categories the wrong predictions land on.
- `mismatch_analysis_*.md`: why systems disagree with the gold (profile, label consistency, outcomes by kind, examples with the gold entity in bold).
- `runs/<name>/metrics.json`: arguments and P/R/F1 of every run (`g_*` GLiNER, `u_*` trained RoBERTa, `l_*` LLM). For the LLM run the sentence
  predictions and the raw answer cache are included (small). The prediction files of the other runs are about 10 MB in total and are not committed.

## Label sensitivity of GLiNER (validation, threshold 0.7, first 1000 sentences per set; mean F1 over the three sets)
company/product 0.564, organization/product 0.533, business/product 0.591, company name/product name 0.565. "business" scores best overall but
worst on companies (mean COMP F1 0.227 against 0.332 for "company"), so the default words were kept.
