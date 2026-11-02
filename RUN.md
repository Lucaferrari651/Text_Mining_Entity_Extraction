# Running the Wikipedia/Wikidata linking baseline on your computer

You only need Python 3.10+ and an internet connection. No account, no API key.

## 0. One-time setup
```bash
cd ~/Text_mining_final_project/Text_Mining_Entity_Extraction     # the root of this repo
git clone https://github.com/alteca/Linked-DocRED          # the data (about 100 MB, ignored by git)
python3 -m venv .venv && source .venv/bin/activate
pip install requests numpy scikit-learn sklearn-crfsuite pytest
python3 -m pytest -q tests                                   # should print: 6 passed
```
The data folder used below is `Linked-DocRED/Linked-DocRED` (it holds `dev.json`, `train_annotated.json`).

## 1. Quick test (about 30 seconds)
```bash
python3 fetch_wiki_candidates.py Linked-DocRED/Linked-DocRED --split dev \
    --extra surfaces_extra_dev.txt --out wiki_cache_test.json --contact YOUR_EMAIL --limit 50
```
It should print "50/50" and write `wiki_cache_test.json`. Open it: every string has two lists,
`wikipedia` (page titles) and `wikidata` (Q-ids). Delete the test file afterwards.

## 2. Full run (about 14,400 strings = 28,800 requests; expect roughly 30-60 minutes)
```bash
python3 fetch_wiki_candidates.py Linked-DocRED/Linked-DocRED --split dev \
    --extra surfaces_extra_dev.txt --out wiki_cache_dev.json --contact YOUR_EMAIL
```
* You can stop it (Ctrl-C) and restart with the same command: finished strings are kept.
* If it ends with "N failed", run the same command again to retry those.
* Be polite to the servers: do not raise `--workers` above 4-6.
* `--contact` puts your e-mail in the User-Agent, which Wikimedia asks for. It is sent only to Wikipedia/Wikidata.

## 3. Evaluate (offline, about 5-10 minutes; trains the CRF the first time)
```bash
python3 run_wiki_eval.py Linked-DocRED/Linked-DocRED --cache wiki_cache_dev.json
```
It prints Hit@1 / Hit@5 / Not found / Mean rank / MRR for Wikipedia vs Wikidata search, the paper's
rank-sum vs our probability-sum, and the combination with the alias dictionary, first on gold entities
(part A), then on the entities our own pipeline predicts (part B). Results go to `results/wiki_metrics.json`.

Then tell Claude when `wiki_cache_dev.json` exists so the evaluation can also be run there.
