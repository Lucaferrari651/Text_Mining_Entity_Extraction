## fewnerd

**same sampled sentences (n=800)**

| System | P | R | F1 | PER F1 | COMP F1 | PROD F1 |
|---|---|---|---|---|---|---|
| RoBERTa, Few-NERD only | 0.803 | 0.827 | **0.815** | 0.884 | 0.656 | 0.672 |
| RoBERTa, all three train sets | 0.801 | 0.830 | **0.815** | 0.888 | 0.604 | 0.703 |
| GLiNER 0.5 | 0.462 | 0.724 | **0.564** | 0.711 | 0.346 | 0.344 |
| GLiNER 0.8 | 0.647 | 0.666 | **0.656** | 0.780 | 0.406 | 0.429 |
| LLM Llama 3.1 8B | 0.491 | 0.580 | **0.532** | 0.691 | 0.339 | 0.325 |

**full test set (n=37648)**

| System | P | R | F1 | PER F1 | COMP F1 | PROD F1 |
|---|---|---|---|---|---|---|
| RoBERTa, Few-NERD only | 0.825 | 0.845 | **0.835** | 0.902 | 0.680 | 0.699 |
| RoBERTa, all three train sets | 0.824 | 0.845 | **0.834** | 0.901 | 0.677 | 0.701 |
| GLiNER 0.5 | 0.445 | 0.727 | **0.552** | 0.691 | 0.358 | 0.334 |
| GLiNER 0.8 | 0.611 | 0.653 | **0.632** | 0.746 | 0.447 | 0.382 |

**Gold company / product mentions on the sampled sentences: what happened**

- RoBERTa, Few-NERD only, gold COMP (n=95): found: 64 (67%), overlapping, different boundaries: 14 (15%), same span, other type: OTHER: 10 (11%), same span, other type: PER: 4 (4%), same span, other type: PROD: 2 (2%), missed: 1 (1%)
- RoBERTa, Few-NERD only, gold PROD (n=122): found: 83 (68%), overlapping, different boundaries: 19 (16%), same span, other type: OTHER: 10 (8%), missed: 6 (5%), same span, other type: COMP: 3 (2%), same span, other type: PER: 1 (1%)
- RoBERTa, all three train sets, gold COMP (n=95): found: 58 (61%), overlapping, different boundaries: 20 (21%), same span, other type: OTHER: 10 (11%), same span, other type: PER: 4 (4%), same span, other type: PROD: 3 (3%)
- RoBERTa, all three train sets, gold PROD (n=122): found: 91 (75%), overlapping, different boundaries: 15 (12%), same span, other type: OTHER: 10 (8%), missed: 3 (2%), same span, other type: COMP: 2 (2%), same span, other type: PER: 1 (1%)
- GLiNER 0.5, gold COMP (n=95): found: 59 (62%), overlapping, different boundaries: 17 (18%), missed: 12 (13%), same span, other type: PER: 5 (5%), same span, other type: PROD: 2 (2%)
- GLiNER 0.5, gold PROD (n=122): found: 63 (52%), missed: 28 (23%), overlapping, different boundaries: 23 (19%), same span, other type: COMP: 6 (5%), same span, other type: PER: 2 (2%)
- GLiNER 0.8, gold COMP (n=95): found: 52 (55%), missed: 25 (26%), overlapping, different boundaries: 14 (15%), same span, other type: PER: 3 (3%), same span, other type: PROD: 1 (1%)
- GLiNER 0.8, gold PROD (n=122): missed: 52 (43%), found: 47 (39%), overlapping, different boundaries: 17 (14%), same span, other type: COMP: 5 (4%), same span, other type: PER: 1 (1%)
- LLM Llama 3.1 8B, gold COMP (n=95): found: 54 (57%), missed: 24 (25%), overlapping, different boundaries: 10 (11%), same span, other type: PROD: 6 (6%), same span, other type: PER: 1 (1%)
- LLM Llama 3.1 8B, gold PROD (n=122): found: 56 (46%), missed: 48 (39%), overlapping, different boundaries: 16 (13%), same span, other type: COMP: 1 (1%), same span, other type: PER: 1 (1%)

## wnut17

**same sampled sentences (n=800)**

| System | P | R | F1 | PER F1 | COMP F1 | PROD F1 |
|---|---|---|---|---|---|---|
| RoBERTa, Few-NERD only | 0.592 | 0.475 | **0.527** | 0.634 | 0.143 | 0.234 |
| RoBERTa, all three train sets | 0.554 | 0.633 | **0.591** | 0.680 | 0.444 | 0.239 |
| GLiNER 0.5 | 0.292 | 0.638 | **0.400** | 0.476 | 0.261 | 0.181 |
| GLiNER 0.8 | 0.484 | 0.399 | **0.438** | 0.520 | 0.276 | 0.189 |
| LLM Llama 3.1 8B | 0.580 | 0.359 | **0.444** | 0.569 | 0.229 | 0.107 |

**full test set (n=1287)**

| System | P | R | F1 | PER F1 | COMP F1 | PROD F1 |
|---|---|---|---|---|---|---|
| RoBERTa, Few-NERD only | 0.582 | 0.463 | **0.516** | 0.615 | 0.122 | 0.302 |
| RoBERTa, all three train sets | 0.526 | 0.609 | **0.564** | 0.647 | 0.424 | 0.308 |
| GLiNER 0.5 | 0.300 | 0.619 | **0.404** | 0.472 | 0.245 | 0.268 |
| GLiNER 0.8 | 0.497 | 0.405 | **0.446** | 0.520 | 0.284 | 0.280 |

**Gold company / product mentions on the sampled sentences: what happened**

- RoBERTa, Few-NERD only, gold COMP (n=43): same span, other type: OTHER: 18 (42%), missed: 15 (35%), found: 4 (9%), same span, other type: PROD: 3 (7%), overlapping, different boundaries: 2 (5%), same span, other type: PER: 1 (2%)
- RoBERTa, Few-NERD only, gold PROD (n=60): missed: 25 (42%), found: 13 (22%), overlapping, different boundaries: 11 (18%), same span, other type: OTHER: 8 (13%), same span, other type: COMP: 2 (3%), same span, other type: PER: 1 (2%)
- RoBERTa, all three train sets, gold COMP (n=43): found: 22 (51%), missed: 9 (21%), same span, other type: OTHER: 8 (19%), overlapping, different boundaries: 4 (9%)
- RoBERTa, all three train sets, gold PROD (n=60): missed: 25 (42%), found: 13 (22%), overlapping, different boundaries: 9 (15%), same span, other type: OTHER: 6 (10%), same span, other type: COMP: 5 (8%), same span, other type: PER: 2 (3%)
- GLiNER 0.5, gold COMP (n=43): found: 23 (53%), missed: 17 (40%), overlapping, different boundaries: 1 (2%), same span, other type: PER: 1 (2%), same span, other type: PROD: 1 (2%)
- GLiNER 0.5, gold PROD (n=60): missed: 24 (40%), found: 16 (27%), overlapping, different boundaries: 8 (13%), same span, other type: COMP: 8 (13%), same span, other type: PER: 4 (7%)
- GLiNER 0.8, gold COMP (n=43): missed: 30 (70%), found: 12 (28%), overlapping, different boundaries: 1 (2%)
- GLiNER 0.8, gold PROD (n=60): missed: 40 (67%), found: 10 (17%), overlapping, different boundaries: 5 (8%), same span, other type: COMP: 3 (5%), same span, other type: PER: 2 (3%)
- LLM Llama 3.1 8B, gold COMP (n=43): missed: 33 (77%), found: 8 (19%), overlapping, different boundaries: 1 (2%), same span, other type: PROD: 1 (2%)
- LLM Llama 3.1 8B, gold PROD (n=60): missed: 45 (75%), overlapping, different boundaries: 7 (12%), found: 6 (10%), same span, other type: COMP: 1 (2%), same span, other type: PER: 1 (2%)

## tweetner7

**same sampled sentences (n=800)**

| System | P | R | F1 | PER F1 | COMP F1 | PROD F1 |
|---|---|---|---|---|---|---|
| RoBERTa, Few-NERD only | 0.680 | 0.279 | **0.395** | 0.545 | 0.072 | 0.182 |
| RoBERTa, all three train sets | 0.696 | 0.717 | **0.707** | 0.816 | 0.488 | 0.622 |
| GLiNER 0.5 | 0.408 | 0.512 | **0.454** | 0.611 | 0.236 | 0.150 |
| GLiNER 0.8 | 0.598 | 0.414 | **0.489** | 0.664 | 0.209 | 0.136 |
| LLM Llama 3.1 8B | 0.448 | 0.298 | **0.358** | 0.535 | 0.216 | 0.072 |

**full test set (n=3383)**

| System | P | R | F1 | PER F1 | COMP F1 | PROD F1 |
|---|---|---|---|---|---|---|
| RoBERTa, Few-NERD only | 0.665 | 0.261 | **0.375** | 0.525 | 0.072 | 0.119 |
| RoBERTa, all three train sets | 0.702 | 0.737 | **0.719** | 0.826 | 0.510 | 0.628 |
| GLiNER 0.5 | 0.432 | 0.537 | **0.479** | 0.627 | 0.303 | 0.129 |
| GLiNER 0.8 | 0.629 | 0.426 | **0.508** | 0.675 | 0.267 | 0.118 |

**Gold company / product mentions on the sampled sentences: what happened**

- RoBERTa, Few-NERD only, gold COMP (n=251): missed: 151 (60%), same span, other type: OTHER: 52 (21%), overlapping, different boundaries: 19 (8%), same span, other type: PROD: 15 (6%), found: 10 (4%), same span, other type: PER: 4 (2%)
- RoBERTa, Few-NERD only, gold PROD (n=311): missed: 239 (77%), found: 37 (12%), same span, other type: OTHER: 20 (6%), overlapping, different boundaries: 11 (4%), same span, other type: COMP: 3 (1%), same span, other type: PER: 1 (0%)
- RoBERTa, all three train sets, gold COMP (n=251): found: 127 (51%), same span, other type: OTHER: 49 (20%), same span, other type: PROD: 31 (12%), missed: 21 (8%), overlapping, different boundaries: 14 (6%), same span, other type: PER: 9 (4%)
- RoBERTa, all three train sets, gold PROD (n=311): found: 198 (64%), missed: 38 (12%), same span, other type: OTHER: 28 (9%), same span, other type: COMP: 27 (9%), overlapping, different boundaries: 15 (5%), same span, other type: PER: 5 (2%)
- GLiNER 0.5, gold COMP (n=251): missed: 169 (67%), found: 64 (25%), same span, other type: PER: 10 (4%), overlapping, different boundaries: 5 (2%), same span, other type: PROD: 3 (1%)
- GLiNER 0.5, gold PROD (n=311): missed: 188 (60%), same span, other type: COMP: 50 (16%), found: 43 (14%), overlapping, different boundaries: 21 (7%), same span, other type: PER: 9 (3%)
- GLiNER 0.8, gold COMP (n=251): missed: 202 (80%), found: 40 (16%), same span, other type: PER: 6 (2%), same span, other type: PROD: 2 (1%), overlapping, different boundaries: 1 (0%)
- GLiNER 0.8, gold PROD (n=311): missed: 247 (79%), found: 28 (9%), same span, other type: COMP: 21 (7%), overlapping, different boundaries: 15 (5%)
- LLM Llama 3.1 8B, gold COMP (n=251): missed: 182 (73%), found: 54 (22%), same span, other type: PROD: 9 (4%), same span, other type: PER: 4 (2%), overlapping, different boundaries: 2 (1%)
- LLM Llama 3.1 8B, gold PROD (n=311): missed: 248 (80%), same span, other type: COMP: 34 (11%), found: 18 (6%), overlapping, different boundaries: 10 (3%), same span, other type: PER: 1 (0%)
