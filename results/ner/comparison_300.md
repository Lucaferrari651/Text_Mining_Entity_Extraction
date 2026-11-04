## fewnerd

**same sampled sentences (n=300)**

| System | P | R | F1 | PER F1 | COMP F1 | PROD F1 |
|---|---|---|---|---|---|---|
| RoBERTa, Few-NERD only | 0.818 | 0.876 | **0.846** | 0.905 | 0.753 | 0.632 |
| RoBERTa, all three train sets | 0.816 | 0.895 | **0.854** | 0.905 | 0.712 | 0.736 |
| GLiNER 0.5 | 0.481 | 0.745 | **0.584** | 0.726 | 0.403 | 0.279 |
| GLiNER 0.8 | 0.661 | 0.700 | **0.680** | 0.790 | 0.465 | 0.364 |
| LLM Llama 3.1 8B | 0.500 | 0.551 | **0.524** | 0.675 | 0.400 | 0.192 |
| LLM Llama 3.3 70B | 0.526 | 0.805 | **0.636** | 0.843 | 0.312 | 0.311 |

**full test set (n=37648)**

| System | P | R | F1 | PER F1 | COMP F1 | PROD F1 |
|---|---|---|---|---|---|---|
| RoBERTa, Few-NERD only | 0.825 | 0.845 | **0.835** | 0.902 | 0.680 | 0.699 |
| RoBERTa, all three train sets | 0.824 | 0.845 | **0.834** | 0.901 | 0.677 | 0.701 |
| GLiNER 0.5 | 0.445 | 0.727 | **0.552** | 0.691 | 0.358 | 0.334 |
| GLiNER 0.8 | 0.611 | 0.653 | **0.632** | 0.746 | 0.447 | 0.382 |

**Gold company / product mentions on the sampled sentences: what happened**

- RoBERTa, Few-NERD only, gold COMP (n=37): found: 29 (78%), overlapping, different boundaries: 5 (14%), same span, other type: PER: 2 (5%), same span, other type: OTHER: 1 (3%)
- RoBERTa, Few-NERD only, gold PROD (n=37): found: 24 (65%), overlapping, different boundaries: 7 (19%), missed: 4 (11%), same span, other type: OTHER: 1 (3%), same span, other type: COMP: 1 (3%)
- RoBERTa, all three train sets, gold COMP (n=37): found: 26 (70%), overlapping, different boundaries: 6 (16%), same span, other type: PER: 2 (5%), same span, other type: PROD: 2 (5%), same span, other type: OTHER: 1 (3%)
- RoBERTa, all three train sets, gold PROD (n=37): found: 32 (86%), overlapping, different boundaries: 5 (14%)
- GLiNER 0.5, gold COMP (n=37): found: 26 (70%), overlapping, different boundaries: 5 (14%), missed: 4 (11%), same span, other type: PER: 2 (5%)
- GLiNER 0.5, gold PROD (n=37): found: 17 (46%), overlapping, different boundaries: 10 (27%), missed: 8 (22%), same span, other type: COMP: 2 (5%)
- GLiNER 0.8, gold COMP (n=37): found: 23 (62%), missed: 8 (22%), overlapping, different boundaries: 5 (14%), same span, other type: PER: 1 (3%)
- GLiNER 0.8, gold PROD (n=37): missed: 15 (41%), found: 12 (32%), overlapping, different boundaries: 9 (24%), same span, other type: COMP: 1 (3%)
- LLM Llama 3.1 8B, gold COMP (n=37): found: 25 (68%), missed: 7 (19%), overlapping, different boundaries: 2 (5%), same span, other type: PROD: 2 (5%), same span, other type: PER: 1 (3%)
- LLM Llama 3.1 8B, gold PROD (n=37): missed: 20 (54%), found: 10 (27%), overlapping, different boundaries: 6 (16%), same span, other type: COMP: 1 (3%)
- LLM Llama 3.3 70B, gold COMP (n=37): found: 27 (73%), missed: 6 (16%), overlapping, different boundaries: 2 (5%), same span, other type: PER: 2 (5%)
- LLM Llama 3.3 70B, gold PROD (n=37): missed: 15 (41%), found: 14 (38%), overlapping, different boundaries: 7 (19%), same span, other type: COMP: 1 (3%)

## wnut17

**same sampled sentences (n=300)**

| System | P | R | F1 | PER F1 | COMP F1 | PROD F1 |
|---|---|---|---|---|---|---|
| RoBERTa, Few-NERD only | 0.605 | 0.487 | **0.540** | 0.649 | 0.250 | 0.300 |
| RoBERTa, all three train sets | 0.572 | 0.643 | **0.606** | 0.723 | 0.455 | 0.271 |
| GLiNER 0.5 | 0.324 | 0.708 | **0.445** | 0.499 | 0.364 | 0.289 |
| GLiNER 0.8 | 0.514 | 0.481 | **0.497** | 0.557 | 0.450 | 0.316 |
| LLM Llama 3.1 8B | 0.542 | 0.377 | **0.444** | 0.582 | 0.345 | 0.149 |
| LLM Llama 3.3 70B | 0.677 | 0.571 | **0.620** | 0.715 | 0.578 | 0.261 |

**full test set (n=1287)**

| System | P | R | F1 | PER F1 | COMP F1 | PROD F1 |
|---|---|---|---|---|---|---|
| RoBERTa, Few-NERD only | 0.582 | 0.463 | **0.516** | 0.615 | 0.122 | 0.302 |
| RoBERTa, all three train sets | 0.526 | 0.609 | **0.564** | 0.647 | 0.424 | 0.308 |
| GLiNER 0.5 | 0.300 | 0.619 | **0.404** | 0.472 | 0.245 | 0.268 |
| GLiNER 0.8 | 0.497 | 0.405 | **0.446** | 0.520 | 0.284 | 0.280 |

**Gold company / product mentions on the sampled sentences: what happened**

- RoBERTa, Few-NERD only, gold COMP (n=17): missed: 6 (35%), same span, other type: OTHER: 5 (29%), found: 3 (18%), overlapping, different boundaries: 2 (12%), same span, other type: PROD: 1 (6%)
- RoBERTa, Few-NERD only, gold PROD (n=33): missed: 10 (30%), found: 9 (27%), overlapping, different boundaries: 9 (27%), same span, other type: OTHER: 3 (9%), same span, other type: PER: 1 (3%), same span, other type: COMP: 1 (3%)
- RoBERTa, all three train sets, gold COMP (n=17): found: 10 (59%), overlapping, different boundaries: 3 (18%), same span, other type: OTHER: 2 (12%), missed: 2 (12%)
- RoBERTa, all three train sets, gold PROD (n=33): missed: 12 (36%), found: 8 (24%), overlapping, different boundaries: 8 (24%), same span, other type: COMP: 3 (9%), same span, other type: OTHER: 2 (6%)
- GLiNER 0.5, gold COMP (n=17): found: 12 (71%), missed: 5 (29%)
- GLiNER 0.5, gold PROD (n=33): found: 12 (36%), missed: 9 (27%), overlapping, different boundaries: 7 (21%), same span, other type: COMP: 4 (12%), same span, other type: PER: 1 (3%)
- GLiNER 0.8, gold COMP (n=17): found: 9 (53%), missed: 8 (47%)
- GLiNER 0.8, gold PROD (n=33): missed: 16 (48%), found: 9 (27%), overlapping, different boundaries: 5 (15%), same span, other type: COMP: 3 (9%)
- LLM Llama 3.1 8B, gold COMP (n=17): missed: 11 (65%), found: 5 (29%), overlapping, different boundaries: 1 (6%)
- LLM Llama 3.1 8B, gold PROD (n=33): missed: 21 (64%), overlapping, different boundaries: 6 (18%), found: 5 (15%), same span, other type: COMP: 1 (3%)
- LLM Llama 3.3 70B, gold COMP (n=17): found: 13 (76%), missed: 4 (24%)
- LLM Llama 3.3 70B, gold PROD (n=33): missed: 19 (58%), overlapping, different boundaries: 7 (21%), found: 6 (18%), same span, other type: COMP: 1 (3%)

## tweetner7

**same sampled sentences (n=300)**

| System | P | R | F1 | PER F1 | COMP F1 | PROD F1 |
|---|---|---|---|---|---|---|
| RoBERTa, Few-NERD only | 0.677 | 0.274 | **0.390** | 0.551 | 0.045 | 0.133 |
| RoBERTa, all three train sets | 0.682 | 0.703 | **0.692** | 0.801 | 0.469 | 0.597 |
| GLiNER 0.5 | 0.398 | 0.512 | **0.448** | 0.592 | 0.254 | 0.185 |
| GLiNER 0.8 | 0.599 | 0.400 | **0.480** | 0.635 | 0.250 | 0.140 |
| LLM Llama 3.1 8B | 0.470 | 0.309 | **0.373** | 0.557 | 0.244 | 0.073 |
| LLM Llama 3.3 70B | 0.444 | 0.474 | **0.458** | 0.689 | 0.270 | 0.128 |

**full test set (n=3383)**

| System | P | R | F1 | PER F1 | COMP F1 | PROD F1 |
|---|---|---|---|---|---|---|
| RoBERTa, Few-NERD only | 0.665 | 0.261 | **0.375** | 0.525 | 0.072 | 0.119 |
| RoBERTa, all three train sets | 0.702 | 0.737 | **0.719** | 0.826 | 0.510 | 0.628 |
| GLiNER 0.5 | 0.432 | 0.537 | **0.479** | 0.627 | 0.303 | 0.129 |
| GLiNER 0.8 | 0.629 | 0.426 | **0.508** | 0.675 | 0.267 | 0.118 |

**Gold company / product mentions on the sampled sentences: what happened**

- RoBERTa, Few-NERD only, gold COMP (n=84): missed: 47 (56%), same span, other type: OTHER: 19 (23%), overlapping, different boundaries: 8 (10%), same span, other type: PROD: 7 (8%), found: 2 (2%), same span, other type: PER: 1 (1%)
- RoBERTa, Few-NERD only, gold PROD (n=116): missed: 91 (78%), same span, other type: OTHER: 13 (11%), found: 10 (9%), overlapping, different boundaries: 2 (2%)
- RoBERTa, all three train sets, gold COMP (n=84): found: 41 (49%), same span, other type: OTHER: 22 (26%), same span, other type: PROD: 8 (10%), overlapping, different boundaries: 5 (6%), missed: 5 (6%), same span, other type: PER: 3 (4%)
- RoBERTa, all three train sets, gold PROD (n=116): found: 69 (59%), missed: 20 (17%), same span, other type: OTHER: 11 (9%), same span, other type: COMP: 10 (9%), same span, other type: PER: 3 (3%), overlapping, different boundaries: 3 (3%)
- GLiNER 0.5, gold COMP (n=84): missed: 54 (64%), found: 26 (31%), same span, other type: PER: 3 (4%), same span, other type: PROD: 1 (1%)
- GLiNER 0.5, gold PROD (n=116): missed: 64 (55%), same span, other type: COMP: 21 (18%), found: 20 (17%), overlapping, different boundaries: 7 (6%), same span, other type: PER: 4 (3%)
- GLiNER 0.8, gold COMP (n=84): missed: 63 (75%), found: 17 (20%), same span, other type: PER: 3 (4%), same span, other type: PROD: 1 (1%)
- GLiNER 0.8, gold PROD (n=116): missed: 91 (78%), found: 10 (9%), same span, other type: COMP: 9 (8%), overlapping, different boundaries: 6 (5%)
- LLM Llama 3.1 8B, gold COMP (n=84): missed: 58 (69%), found: 20 (24%), same span, other type: PROD: 4 (5%), overlapping, different boundaries: 1 (1%), same span, other type: PER: 1 (1%)
- LLM Llama 3.1 8B, gold PROD (n=116): missed: 90 (78%), same span, other type: COMP: 13 (11%), found: 7 (6%), overlapping, different boundaries: 5 (4%), same span, other type: PER: 1 (1%)
- LLM Llama 3.3 70B, gold COMP (n=84): found: 42 (50%), missed: 37 (44%), same span, other type: PROD: 2 (2%), overlapping, different boundaries: 2 (2%), same span, other type: PER: 1 (1%)
- LLM Llama 3.3 70B, gold PROD (n=116): same span, other type: COMP: 65 (56%), missed: 37 (32%), found: 11 (9%), overlapping, different boundaries: 2 (2%), same span, other type: PER: 1 (1%)
