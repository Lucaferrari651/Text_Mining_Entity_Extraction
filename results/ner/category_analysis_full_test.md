# fewnerd

## Share of gold mentions found (exact span and right type)

| Gold category | type | n | RoBERTa (Few-NERD) | GLiNER 0.5 | GLiNER 0.8 |
|---|---|---|---|---|---|
| person-other | PER | 8767 | 89% | 77% | 70% |
| person-artist/author | PER | 3464 | 93% | 86% | 80% |
| person-athlete | PER | 2907 | 94% | 84% | 81% |
| person-politician | PER | 2859 | 89% | 72% | 66% |
| person-actor | PER | 1638 | 98% | 92% | 88% |
| person-scholar | PER | 743 | 92% | 83% | 80% |
| person-soldier | PER | 647 | 89% | 68% | 62% |
| person-director | PER | 554 | 97% | 91% | 83% |
| organization-company | COMP | 3903 | 69% | 72% | 64% |
| product-other | PROD | 1614 | 60% | 42% | 30% |
| product-software | PROD | 889 | 81% | 46% | 32% |
| product-airplane | PROD | 794 | 74% | 57% | 43% |
| product-car | PROD | 688 | 78% | 43% | 38% |
| product-weapon | PROD | 625 | 66% | 50% | 33% |
| product-game | PROD | 496 | 79% | 62% | 51% |
| product-food | PROD | 432 | 57% | 58% | 40% |
| product-ship | PROD | 380 | 79% | 35% | 21% |
| product-train | PROD | 314 | 71% | 44% | 28% |

## What the wrong predictions of each type land on (same span, different gold category)

- **RoBERTa (Few-NERD)**, predicted PER (22089): wrong on same span as gold location-GPE (116), other-god (102), organization-company (98), organization-sportsteam (71), organization-showorganization (68), organization-other (40); no gold entity at that span: 1631
- **RoBERTa (Few-NERD)**, predicted COMP (4067): wrong on same span as gold organization-other (125), organization-media/newspaper (80), person-other (73), building-restaurant (44), location-GPE (38), location-road/railway/highway/transit (36); no gold entity at that span: 689
- **RoBERTa (Few-NERD)**, predicted PROD (6316): wrong on same span as gold organization-company (112), organization-other (43), location-GPE (39), person-other (20), other-livingthing (19), organization-media/newspaper (15); no gold entity at that span: 1546
- **GLiNER 0.5**, predicted PER (28403): wrong on same span as gold other-god (464), location-GPE (196), organization-showorganization (138), organization-company (103), organization-other (99), organization-sportsteam (65); no gold entity at that span: 9315
- **GLiNER 0.5**, predicted COMP (11779): wrong on same span as gold organization-sportsteam (762), organization-other (625), organization-media/newspaper (589), person-other (403), organization-education (238), building-other (217); no gold entity at that span: 3689
- **GLiNER 0.5**, predicted PROD (11630): wrong on same span as gold art-music (373), art-film (292), other-chemicalthing (228), other-medical (210), art-broadcastprogram (187), art-writtenart (178); no gold entity at that span: 5464
- **GLiNER 0.8**, predicted PER (21469): wrong on same span as gold other-god (372), organization-showorganization (94), location-GPE (85), organization-company (82), organization-sportsteam (53), organization-other (41); no gold entity at that span: 4279
- **GLiNER 0.8**, predicted COMP (7243): wrong on same span as gold organization-media/newspaper (369), organization-sportsteam (355), organization-other (326), person-other (276), person-athlete (132), building-other (111); no gold entity at that span: 1947
- **GLiNER 0.8**, predicted PROD (5172): wrong on same span as gold art-music (139), other-medical (132), organization-company (120), other-chemicalthing (111), art-film (90), art-writtenart (61); no gold entity at that span: 1778

# wnut17

## Share of gold mentions found (exact span and right type)

| Gold category | type | n | RoBERTa (Few-NERD) | GLiNER 0.5 | GLiNER 0.8 |
|---|---|---|---|---|---|
| person | PER | 429 | 58% | 72% | 47% |
| corporation | COMP | 66 | 8% | 52% | 30% |
| product | PROD | 127 | 27% | 35% | 23% |

## What the wrong predictions of each type land on (same span, different gold category)

- **RoBERTa (Few-NERD)**, predicted PER (381): wrong on same span as gold group (3), product (3), creative-work (2), location (2), corporation (1); no gold entity at that span: 121
- **RoBERTa (Few-NERD)**, predicted COMP (16): wrong on same span as gold product (4); no gold entity at that span: 7
- **RoBERTa (Few-NERD)**, predicted PROD (98): wrong on same span as gold creative-work (11), corporation (5), person (3), location (3), group (1); no gold entity at that span: 41
- **GLiNER 0.5**, predicted PER (871): wrong on same span as gold group (15), product (6), creative-work (3), corporation (3), location (1); no gold entity at that span: 536
- **GLiNER 0.5**, predicted COMP (211): wrong on same span as gold group (28), person (19), product (15), location (9), creative-work (8); no gold entity at that span: 98
- **GLiNER 0.5**, predicted PROD (201): wrong on same span as gold creative-work (33), person (8), corporation (2), group (1), location (1); no gold entity at that span: 112
- **GLiNER 0.8**, predicted PER (352): wrong on same span as gold product (3), creative-work (2), corporation (2), group (2), location (1); no gold entity at that span: 139
- **GLiNER 0.8**, predicted COMP (75): wrong on same span as gold group (9), product (9), person (8), creative-work (3), location (2); no gold entity at that span: 24
- **GLiNER 0.8**, predicted PROD (80): wrong on same span as gold creative-work (12), person (4); no gold entity at that span: 35

# tweetner7

## Share of gold mentions found (exact span and right type)

| Gold category | type | n | RoBERTa (Few-NERD) | GLiNER 0.5 | GLiNER 0.8 |
|---|---|---|---|---|---|
| person | PER | 1954 | 68% | 68% | 56% |
| person (handle) | PER | 1354 | 0% | 87% | 71% |
| corporation | COMP | 621 | 7% | 31% | 20% |
| corporation (handle) | COMP | 470 | 0% | 37% | 23% |
| product (handle) | PROD | 771 | 0% | 2% | 1% |
| product | PROD | 421 | 22% | 30% | 19% |

## What the wrong predictions of each type land on (same span, different gold category)

- **RoBERTa (Few-NERD)**, predicted PER (1721): wrong on same span as gold group (25), corporation (14), creative_work (11), event (7), location (6), product (1); no gold entity at that span: 336
- **RoBERTa (Few-NERD)**, predicted COMP (103): wrong on same span as gold product (10), person (6), group (5), creative_work (3), location (2), event (1); no gold entity at that span: 33
- **RoBERTa (Few-NERD)**, predicted PROD (366): wrong on same span as gold corporation (66), creative_work (35), person (11), group (10), event (10), location (6); no gold entity at that span: 135
- **GLiNER 0.5**, predicted PER (4655): wrong on same span as gold group (handle) (68), group (64), creative_work (27), product (handle) (20), corporation (18), event (12); no gold entity at that span: 1913
- **GLiNER 0.5**, predicted COMP (1335): wrong on same span as gold product (handle) (158), group (151), group (handle) (112), person (64), product (45), person (handle) (37); no gold entity at that span: 289
- **GLiNER 0.5**, predicted PROD (960): wrong on same span as gold creative_work (200), event (29), corporation (22), group (22), person (19), creative_work (handle) (5); no gold entity at that span: 516
- **GLiNER 0.8**, predicted PER (2804): wrong on same span as gold group (33), group (handle) (24), creative_work (19), corporation (14), event (6), location (6); no gold entity at that span: 630
- **GLiNER 0.8**, predicted COMP (625): wrong on same span as gold group (64), product (handle) (63), group (handle) (33), person (32), product (26), location (14); no gold entity at that span: 120
- **GLiNER 0.8**, predicted PROD (356): wrong on same span as gold creative_work (82), person (12), corporation (12), group (10), event (7), creative_work (handle) (4); no gold entity at that span: 135
