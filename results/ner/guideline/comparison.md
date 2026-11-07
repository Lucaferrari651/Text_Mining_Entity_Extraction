## fewnerd

**same sampled sentences (n=300)**

| System | P | R | F1 | PER F1 | COMP F1 | PROD F1 |
|---|---|---|---|---|---|---|
| 6 shots | 0.495 | 0.543 | **0.518** | 0.671 | 0.393 | 0.187 |
| guide | 0.314 | 0.704 | **0.434** | 0.598 | 0.263 | 0.218 |
| guide+shots | 0.446 | 0.479 | **0.462** | 0.593 | 0.367 | 0.200 |

**Gold company / product mentions on the sampled sentences: what happened**

- 6 shots, gold COMP (n=37): found: 24 (65%), missed: 9 (24%), same span, other type: PROD: 2 (5%), overlapping, different boundaries: 1 (3%), same span, other type: PER: 1 (3%)
- 6 shots, gold PROD (n=37): missed: 22 (59%), found: 10 (27%), overlapping, different boundaries: 4 (11%), same span, other type: COMP: 1 (3%)
- guide, gold COMP (n=37): found: 27 (73%), missed: 7 (19%), overlapping, different boundaries: 2 (5%), same span, other type: PER: 1 (3%)
- guide, gold PROD (n=37): found: 21 (57%), overlapping, different boundaries: 8 (22%), missed: 5 (14%), same span, other type: COMP: 3 (8%)
- guide+shots, gold COMP (n=37): found: 27 (73%), missed: 7 (19%), overlapping, different boundaries: 1 (3%), same span, other type: PROD: 1 (3%), same span, other type: PER: 1 (3%)
- guide+shots, gold PROD (n=37): missed: 22 (59%), found: 10 (27%), overlapping, different boundaries: 4 (11%), same span, other type: COMP: 1 (3%)

## wnut17

**same sampled sentences (n=300)**

| System | P | R | F1 | PER F1 | COMP F1 | PROD F1 |
|---|---|---|---|---|---|---|
| 6 shots | 0.514 | 0.351 | **0.417** | 0.543 | 0.345 | 0.147 |
| guide | 0.243 | 0.513 | **0.330** | 0.463 | 0.273 | 0.138 |
| guide+shots | 0.558 | 0.312 | **0.400** | 0.513 | 0.176 | 0.200 |

**Gold company / product mentions on the sampled sentences: what happened**

- 6 shots, gold COMP (n=17): missed: 11 (65%), found: 5 (29%), overlapping, different boundaries: 1 (6%)
- 6 shots, gold PROD (n=33): missed: 22 (67%), found: 5 (15%), overlapping, different boundaries: 5 (15%), same span, other type: COMP: 1 (3%)
- guide, gold COMP (n=17): found: 12 (71%), missed: 3 (18%), overlapping, different boundaries: 2 (12%)
- guide, gold PROD (n=33): found: 10 (30%), overlapping, different boundaries: 9 (27%), same span, other type: COMP: 7 (21%), missed: 7 (21%)
- guide+shots, gold COMP (n=17): missed: 13 (76%), found: 3 (18%), overlapping, different boundaries: 1 (6%)
- guide+shots, gold PROD (n=33): missed: 25 (76%), found: 5 (15%), overlapping, different boundaries: 2 (6%), same span, other type: COMP: 1 (3%)

## tweetner7

**same sampled sentences (n=300)**

| System | P | R | F1 | PER F1 | COMP F1 | PROD F1 |
|---|---|---|---|---|---|---|
| 6 shots | 0.445 | 0.307 | **0.364** | 0.543 | 0.227 | 0.074 |
| guide | 0.285 | 0.398 | **0.332** | 0.472 | 0.281 | 0.108 |
| guide+shots | 0.506 | 0.284 | **0.364** | 0.534 | 0.241 | 0.070 |

**Gold company / product mentions on the sampled sentences: what happened**

- 6 shots, gold COMP (n=84): missed: 61 (73%), found: 20 (24%), same span, other type: PROD: 2 (2%), overlapping, different boundaries: 1 (1%)
- 6 shots, gold PROD (n=116): missed: 85 (73%), same span, other type: COMP: 18 (16%), found: 7 (6%), overlapping, different boundaries: 5 (4%), same span, other type: PER: 1 (1%)
- guide, gold COMP (n=84): missed: 39 (46%), found: 38 (45%), overlapping, different boundaries: 5 (6%), same span, other type: PER: 2 (2%)
- guide, gold PROD (n=116): missed: 85 (73%), found: 16 (14%), same span, other type: COMP: 9 (8%), overlapping, different boundaries: 5 (4%), same span, other type: PER: 1 (1%)
- guide+shots, gold COMP (n=84): missed: 63 (75%), found: 19 (23%), overlapping, different boundaries: 1 (1%), same span, other type: PROD: 1 (1%)
- guide+shots, gold PROD (n=116): missed: 95 (82%), same span, other type: COMP: 12 (10%), found: 6 (5%), overlapping, different boundaries: 2 (2%), same span, other type: PER: 1 (1%)
