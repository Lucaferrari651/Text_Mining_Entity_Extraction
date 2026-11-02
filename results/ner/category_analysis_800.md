# fewnerd

## Share of gold mentions found (exact span and right type)

| Gold category | type | n | RoBERTa | GLiNER 0.5 | GLiNER 0.8 | LLM 8B |
|---|---|---|---|---|---|---|
| person-other | PER | 201 | 88% | 77% | 73% | 53% |
| person-artist/author | PER | 92 | 89% | 84% | 80% | 62% |
| person-actor | PER | 53 | 100% | 98% | 96% | 75% |
| person-politician | PER | 45 | 78% | 53% | 44% | 49% |
| person-athlete | PER | 42 | 93% | 83% | 83% | 76% |
| person-director | PER | 15 | 100% | 93% | 87% | 93% |
| person-soldier | PER | 15 | 87% | 80% | 80% | 67% |
| person-scholar | PER | 8 | 100% | 100% | 100% | 88% |
| organization-company | COMP | 95 | 67% | 62% | 55% | 57% |
| product-other | PROD | 25 | 60% | 56% | 44% | 52% |
| product-software | PROD | 23 | 74% | 48% | 48% | 65% |
| product-airplane | PROD | 14 | 79% | 64% | 57% | 43% |
| product-food | PROD | 14 | 57% | 57% | 21% | 29% |
| product-ship | PROD | 13 | 92% | 46% | 31% | 46% |
| product-car | PROD | 13 | 85% | 46% | 23% | 46% |
| product-weapon | PROD | 13 | 54% | 46% | 38% | 31% |

## What the wrong predictions of each type land on (same span, different gold category)

- **RoBERTa**, predicted PER (484): wrong on same span as gold organization-company (4), location-GPE (3), organization-sportsteam (2), art-music (1), organization-other (1), organization-showorganization (1); no gold entity at that span: 45
- **RoBERTa**, predicted COMP (100): wrong on same span as gold location-road/railway/highway/transit (3), organization-other (3), building-restaurant (2), product-other (2), building-other (1), product-software (1); no gold entity at that span: 20
- **RoBERTa**, predicted PROD (125): wrong on same span as gold organization-company (2), organization-media/newspaper (1), building-other (1); no gold entity at that span: 38
- **GLiNER 0.5**, predicted PER (587): wrong on same span as gold location-GPE (5), organization-company (5), other-astronomything (5), location-other (3), organization-showorganization (3), other-god (3); no gold entity at that span: 174
- **GLiNER 0.5**, predicted COMP (246): wrong on same span as gold organization-media/newspaper (17), organization-other (16), organization-sportsteam (14), person-other (8), organization-education (5), building-theater (5); no gold entity at that span: 77
- **GLiNER 0.5**, predicted PROD (244): wrong on same span as gold art-film (9), other-chemicalthing (5), art-broadcastprogram (5), art-music (5), other-medical (4), building-other (4); no gold entity at that span: 113
- **GLiNER 0.8**, predicted PER (450): wrong on same span as gold other-astronomything (5), organization-company (3), organization-showorganization (2), art-music (1), building-other (1), other-god (1); no gold entity at that span: 75
- **GLiNER 0.8**, predicted COMP (161): wrong on same span as gold organization-sportsteam (9), organization-other (8), organization-media/newspaper (8), person-other (7), product-software (4), location-road/railway/highway/transit (3); no gold entity at that span: 48
- **GLiNER 0.8**, predicted PROD (97): wrong on same span as gold other-chemicalthing (3), art-film (3), other-biologything (3), person-artist/author (2), organization-showorganization (1), art-broadcastprogram (1); no gold entity at that span: 32
- **LLM 8B**, predicted PER (366): wrong on same span as gold location-GPE (10), organization-sportsteam (4), other-god (3), organization-showorganization (2), art-other (1), organization-other (1); no gold entity at that span: 54
- **LLM 8B**, predicted COMP (224): wrong on same span as gold organization-other (25), organization-sportsteam (18), organization-education (17), organization-media/newspaper (11), organization-politicalparty (6), organization-government/governmentagency (6); no gold entity at that span: 50
- **LLM 8B**, predicted PROD (223): wrong on same span as gold other-astronomything (8), other-livingthing (8), art-music (8), building-other (7), organization-company (6), building-airport (6); no gold entity at that span: 54

# wnut17

## Share of gold mentions found (exact span and right type)

| Gold category | type | n | RoBERTa | GLiNER 0.5 | GLiNER 0.8 | LLM 8B |
|---|---|---|---|---|---|---|
| person | PER | 270 | 59% | 74% | 47% | 44% |
| corporation | COMP | 43 | 9% | 53% | 28% | 19% |
| product | PROD | 60 | 22% | 27% | 17% | 10% |

## What the wrong predictions of each type land on (same span, different gold category)

- **RoBERTa**, predicted PER (235): wrong on same span as gold group (2), creative-work (2), product (1), corporation (1), location (1); no gold entity at that span: 68
- **RoBERTa**, predicted COMP (13): wrong on same span as gold product (2); no gold entity at that span: 7
- **RoBERTa**, predicted PROD (51): wrong on same span as gold creative-work (7), corporation (3), person (2), location (2), group (1); no gold entity at that span: 23
- **GLiNER 0.5**, predicted PER (566): wrong on same span as gold group (6), product (4), creative-work (2), corporation (1), location (1); no gold entity at that span: 353
- **GLiNER 0.5**, predicted COMP (133): wrong on same span as gold group (18), person (11), product (8), location (6), creative-work (5); no gold entity at that span: 62
- **GLiNER 0.5**, predicted PROD (117): wrong on same span as gold creative-work (19), person (5), location (1), corporation (1); no gold entity at that span: 75
- **GLiNER 0.8**, predicted PER (218): wrong on same span as gold product (2), creative-work (1), group (1), location (1); no gold entity at that span: 86
- **GLiNER 0.8**, predicted COMP (44): wrong on same span as gold person (6), group (5), product (3), creative-work (2), location (1); no gold entity at that span: 15
- **GLiNER 0.8**, predicted PROD (46): wrong on same span as gold creative-work (6), person (4); no gold entity at that span: 26
- **LLM 8B**, predicted PER (152): wrong on same span as gold creative-work (3), group (1), product (1); no gold entity at that span: 27
- **LLM 8B**, predicted COMP (27): wrong on same span as gold group (7), creative-work (2), product (1), location (1); no gold entity at that span: 8
- **LLM 8B**, predicted PROD (52): wrong on same span as gold creative-work (9), person (5), group (3), location (2), corporation (1); no gold entity at that span: 26

# tweetner7

## Share of gold mentions found (exact span and right type)

| Gold category | type | n | RoBERTa | GLiNER 0.5 | GLiNER 0.8 | LLM 8B |
|---|---|---|---|---|---|---|
| person | PER | 480 | 67% | 70% | 59% | 53% |
| person (handle) | PER | 281 | 0% | 84% | 70% | 24% |
| corporation | COMP | 141 | 7% | 27% | 16% | 13% |
| corporation (handle) | COMP | 110 | 0% | 24% | 15% | 32% |
| product (handle) | PROD | 178 | 0% | 1% | 1% | 1% |
| product | PROD | 133 | 28% | 31% | 20% | 13% |

## What the wrong predictions of each type land on (same span, different gold category)

- **RoBERTa**, predicted PER (421): wrong on same span as gold corporation (4), creative_work (3), group (2), event (1), location (1), product (1); no gold entity at that span: 87
- **RoBERTa**, predicted COMP (26): wrong on same span as gold product (3), person (2), location (1), group (1), creative_work (1); no gold entity at that span: 8
- **RoBERTa**, predicted PROD (96): wrong on same span as gold corporation (15), creative_work (4), event (4), person (4), location (1), group (1); no gold entity at that span: 30
- **GLiNER 0.5**, predicted PER (1104): wrong on same span as gold group (handle) (22), group (11), product (handle) (8), corporation (8), location (6), creative_work (4); no gold entity at that span: 466
- **GLiNER 0.5**, predicted COMP (292): wrong on same span as gold product (handle) (38), group (36), group (handle) (29), person (13), product (12), creative_work (10); no gold entity at that span: 66
- **GLiNER 0.5**, predicted PROD (263): wrong on same span as gold creative_work (49), event (6), person (6), group (3), corporation (3), creative_work (handle) (2); no gold entity at that span: 151
- **GLiNER 0.8**, predicted PER (685): wrong on same span as gold group (handle) (8), group (6), corporation (5), creative_work (3), location (2), event (2); no gold entity at that span: 177
- **GLiNER 0.8**, predicted COMP (131): wrong on same span as gold product (handle) (15), group (11), group (handle) (7), person (7), product (6), creative_work (4); no gold entity at that span: 32
- **GLiNER 0.8**, predicted PROD (101): wrong on same span as gold creative_work (19), person (4), corporation (2), group (2), creative_work (handle) (2); no gold entity at that span: 44
- **LLM 8B**, predicted PER (443): wrong on same span as gold creative_work (5), group (handle) (5), group (5), corporation (3), event (2), location (2); no gold entity at that span: 97
- **LLM 8B**, predicted COMP (249): wrong on same span as gold group (handle) (49), group (37), product (handle) (32), person (handle) (7), event (handle) (6), location (5); no gold entity at that span: 44
- **LLM 8B**, predicted PROD (187): wrong on same span as gold creative_work (28), group (20), event (13), location (13), corporation (9), person (8); no gold entity at that span: 78
