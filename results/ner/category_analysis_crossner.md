# crossner_ai

## Share of gold mentions found (exact span and right type)

| Gold category | type | n | RoBERTa (Few-NERD) | GLiNER 0.8 |
|---|---|---|---|---|
| person -> researcher | PER | 160 | 94% | 83% |
| person -> others | PER | 67 | 85% | 84% |
| organization -> others | ORG | 145 | 28% | 72% |
| organization -> university | ORG | 28 | 0% | 82% |
| product name | PROD | 197 | 59% | 23% |

## What the wrong predictions of each type land on (same span, different gold category)

- **RoBERTa (Few-NERD)**, predicted PER (225): wrong on same span as gold organization -> others (1); no gold entity at that span: 16
- **RoBERTa (Few-NERD)**, predicted ORG (58): wrong on same span as gold product name (5), person -> others (2); no gold entity at that span: 10
- **RoBERTa (Few-NERD)**, predicted PROD (253): wrong on same span as gold AI algorithm (33), programming language (32), research task (5), organization -> others (5), research field (2), experiment metrics (1); no gold entity at that span: 58
- **GLiNER 0.8**, predicted PER (212): wrong on same span as gold product name (1); no gold entity at that span: 22
- **GLiNER 0.8**, predicted ORG (229): wrong on same span as gold academic conference (35), product name (11), person -> researcher (6), experiment metrics (5), location (without country) (4), person -> others (3); no gold entity at that span: 32
- **GLiNER 0.8**, predicted PROD (75): wrong on same span as gold programming language (4), organization -> others (2), research task (2), research field (1), location (without country) (1), academic conference (1); no gold entity at that span: 18

# crossner_literature

## Share of gold mentions found (exact span and right type)

| Gold category | type | n | RoBERTa (Few-NERD) | GLiNER 0.8 |
|---|---|---|---|---|
| person -> writer | PER | 566 | 88% | 85% |
| person -> others | PER | 174 | 90% | 67% |
| organization | ORG | 110 | 14% | 65% |

## What the wrong predictions of each type land on (same span, different gold category)

- **RoBERTa (Few-NERD)**, predicted PER (761): wrong on same span as gold creative work -> book (5), creative work -> poem (3), location (without country) (2), organization (1); no gold entity at that span: 94
- **RoBERTa (Few-NERD)**, predicted ORG (20): wrong on same span as gold -; no gold entity at that span: 5
- **RoBERTa (Few-NERD)**, predicted PROD (9): wrong on same span as gold creative work -> book (3); no gold entity at that span: 6
- **GLiNER 0.8**, predicted PER (645): wrong on same span as gold creative work -> book (8), creative work -> poem (2), organization (2), location (without country) (1); no gold entity at that span: 33
- **GLiNER 0.8**, predicted ORG (167): wrong on same span as gold creative work -> magazine (31), location (without country) (12), country (11), creative work -> book (8), event name (5), creative work -> poem (2); no gold entity at that span: 23
- **GLiNER 0.8**, predicted PROD (27): wrong on same span as gold creative work -> book (12); no gold entity at that span: 15

# crossner_music

## Share of gold mentions found (exact span and right type)

| Gold category | type | n | RoBERTa (Few-NERD) | GLiNER 0.8 |
|---|---|---|---|---|
| person -> musical artist | PER | 515 | 91% | 86% |
| person -> others | PER | 80 | 94% | 86% |
| organization -> band | ORG | 462 | 0% | 52% |
| organization -> others | ORG | 208 | 8% | 69% |

## What the wrong predictions of each type land on (same span, different gold category)

- **RoBERTa (Few-NERD)**, predicted PER (649): wrong on same span as gold organization -> band (22), creative work -> album (3), creative work -> song (3), organization -> others (1); no gold entity at that span: 77
- **RoBERTa (Few-NERD)**, predicted ORG (30): wrong on same span as gold person -> musical artist (1); no gold entity at that span: 12
- **RoBERTa (Few-NERD)**, predicted PROD (13): wrong on same span as gold musical instrument (9); no gold entity at that span: 4
- **GLiNER 0.8**, predicted PER (590): wrong on same span as gold organization -> band (26), creative work -> song (6), creative work -> album (4), organization -> others (1); no gold entity at that span: 40
- **GLiNER 0.8**, predicted ORG (513): wrong on same span as gold location (without country) (45), person -> musical artist (13), creative work -> album (9), award (7), event name (4), music genre (4); no gold entity at that span: 43
- **GLiNER 0.8**, predicted PROD (91): wrong on same span as gold creative work -> album (61), creative work -> song (12), organization -> band (10), organization -> others (2); no gold entity at that span: 6

# crossner_politics

## Share of gold mentions found (exact span and right type)

| Gold category | type | n | RoBERTa (Few-NERD) | GLiNER 0.8 |
|---|---|---|---|---|
| person -> politician | PER | 479 | 93% | 83% |
| person -> others | PER | 352 | 97% | 89% |
| organization -> political party | ORG | 953 | 0% | 65% |
| organization -> others | ORG | 513 | 1% | 67% |

## What the wrong predictions of each type land on (same span, different gold category)

- **RoBERTa (Few-NERD)**, predicted PER (849): wrong on same span as gold organization -> political party (6), location (without country) (3), organization -> others (3); no gold entity at that span: 47
- **RoBERTa (Few-NERD)**, predicted ORG (12): wrong on same span as gold country (1); no gold entity at that span: 4
- **RoBERTa (Few-NERD)**, predicted PROD (2): wrong on same span as gold -; no gold entity at that span: 2
- **GLiNER 0.8**, predicted PER (767): wrong on same span as gold location (without country) (2), organization -> political party (1); no gold entity at that span: 51
- **GLiNER 0.8**, predicted ORG (1177): wrong on same span as gold country (46), event name -> others (10), person -> politician (5), person -> others (4), location (without country) (4); no gold entity at that span: 145
- **GLiNER 0.8**, predicted PROD (4): wrong on same span as gold -; no gold entity at that span: 4

# crossner_science

## Share of gold mentions found (exact span and right type)

| Gold category | type | n | RoBERTa (Few-NERD) | GLiNER 0.8 |
|---|---|---|---|---|
| person -> scientist | PER | 471 | 95% | 93% |
| person -> others | PER | 230 | 93% | 80% |
| organization -> others | ORG | 273 | 1% | 75% |
| organization -> university | ORG | 130 | 0% | 78% |

## What the wrong predictions of each type land on (same span, different gold category)

- **RoBERTa (Few-NERD)**, predicted PER (704): wrong on same span as gold astronomical object name (3); no gold entity at that span: 37
- **RoBERTa (Few-NERD)**, predicted ORG (9): wrong on same span as gold academic journal (2); no gold entity at that span: 3
- **RoBERTa (Few-NERD)**, predicted PROD (27): wrong on same span as gold location (without country) (2); no gold entity at that span: 25
- **GLiNER 0.8**, predicted PER (683): wrong on same span as gold astronomical object name (19), academic journal (2); no gold entity at that span: 41
- **GLiNER 0.8**, predicted ORG (471): wrong on same span as gold academic journal (63), location (without country) (20), event name (2), person -> others (1), person -> scientist (1); no gold entity at that span: 77
- **GLiNER 0.8**, predicted PROD (31): wrong on same span as gold chemical compound (13), protein name (2), chemical element (1), person -> others (1); no gold entity at that span: 14
