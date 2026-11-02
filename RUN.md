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


## Transformer mention detector (Colab, GPU)
In Google Colab choose Runtime > Change runtime type > T4 GPU, then in a cell:
```python
!git clone https://github.com/Lucaferrari651/Text_Mining_Entity_Extraction
%cd Text_Mining_Entity_Extraction
!git clone https://github.com/alteca/Linked-DocRED
!pip install -q transformers scikit-learn sklearn-crfsuite
!python ner_transformer.py Linked-DocRED/Linked-DocRED --model roberta-base --epochs 5 --out ner_roberta
```
Quick check first: add `--limit-docs 50 --epochs 1`. For the model used in the paper's baseline add
`--model allenai/longformer-base-4096 --max-len 4096 --batch-size 2`. It prints mention F1 per epoch and per type,
and writes `ner_roberta/preds_dev.json`. Download that file, then use it in the pipeline instead of the CRF:
```bash
python3 run_baseline.py Linked-DocRED/Linked-DocRED --ner-preds ner_roberta/preds_dev.json
python3 run_wiki_eval.py Linked-DocRED/Linked-DocRED --cache wiki_cache_dev.json --ner-preds ner_roberta/preds_dev.json
```


## Person / company / product on Few-NERD, WNUT-17, TweetNER7 (Colab, GPU)
Unified labels: PER, COMP (company), PROD (product), OTHER. The headline number is the micro F1 over PER+COMP+PROD.
Put the `.jsonl` files made by the dataset-download cell in `ner_data/` (the folder is git-ignored), then:
```python
!pip install -q transformers
# quick check (a few minutes)
!python ner_unified.py ner_data --train fewnerd --eval wnut17 --train-limit 2000 --eval-limit 300 --epochs 1 --out u_quick
# train on Few-NERD, test on all three (transfer to the two tweet sets)
!python ner_unified.py ner_data --train fewnerd --eval fewnerd,wnut17,tweetner7 --model roberta-base --epochs 3 --out u_fewnerd_roberta
# train on the tweet sets, test on Few-NERD and WNUT-17
!python ner_unified.py ner_data --train wnut17,tweetner7 --eval fewnerd,wnut17 --epochs 5 --out u_tweets_roberta
```
Results are in `<out>/metrics.json` (per type) and `<out>/preds_<set>.json`. Other encoders: `--model microsoft/deberta-v3-base`
(see `--help`; `--seed` changes the seed, run 3 seeds for the report).


## GLiNER, zero-shot (Colab, GPU; no training)
The labels "person", "company", "product" are given to the model as text; same data and metric as `ner_unified.py`.
```python
!pip install -q gliner
!python gliner_eval.py ner_data --eval wnut17,tweetner7,fewnerd --model urchade/gliner_multi-v2.1 --out g_zero
# quick check: --eval wnut17 --eval-limit 200
```
Results: `g_zero/metrics.json`, `g_zero/preds_<set>.json`. `--labels person,organization,product` tries another wording for
the company label; `--threshold` defaults to 0.5 (fixed in advance, not tuned on the test sets).
