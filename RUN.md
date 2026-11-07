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


## Few-shot LLM baseline (Cloudflare Workers AI; run on your Mac or Colab, the sandbox cannot reach the API)
Needs a free Cloudflare account, its Account ID and an API token with Workers AI permission (never commit them):
```bash
export CF_ACCOUNT_ID=...  CF_API_TOKEN=...
python3 llm_eval.py ner_data --eval wnut17 --eval-limit 50 --out l_quick                  # small test, shows the Neuron cost
python3 llm_eval.py ner_data --eval fewnerd,wnut17,tweetner7 --eval-limit 300 --out l_llama8b
```
A fixed random sample of `--eval-limit` sentences per dataset is used (one API call each). Answers are cached in `<out>/cache.jsonl`;
if the free daily limit (10,000 Neurons) stops the run, run it again the next day and it continues from the cache.
Colab: `!pip install -q requests`, set the two variables with `os.environ[...] = ...` in a cell (do not save the notebook with the token visible).

## Comparing systems on the same sentences (no GPU, no network)
`llm_eval.py` scores a random sample (seed 13), GLiNER / RoBERTa score the full test sets. `compare_ner.py` rebuilds the LLM's
sample from its `metrics.json` and scores every system on exactly those sentences (and on the full set where available), then
shows what happened to each gold COMPANY / PRODUCT mention (found / other type / other boundaries / missed):
```bash
python3 compare_ner.py ner_data --sample-from l_llama8b/metrics.json \
  --system "LLM 8B=l_llama8b" --system "GLiNER 0.5=g_zero" --system "GLiNER 0.8=g_zero_t08" \
  --system "RoBERTa (Few-NERD)=u_fewnerd_roberta" --out comparison
```
Each folder needs `preds_<dataset>.json`. Systems without a given dataset are skipped.

## CrossNER (test-only benchmark, from the B2NERD English release)
CrossNER (AI, literature, music, politics, science) has persons, **organizations** (not companies) and, only in the AI subset, products,
so it is scored as PER / ORG / PROD. The five sets are named `crossner_ai`, `crossner_literature`, `crossner_music`,
`crossner_politics`, `crossner_science`; `--b2nerd-dir` points at the `NER_en` folder of the B2NERD download.
```bash
# zero-shot GLiNER (labels person / organization / product), threshold chosen on the validation sets of the other benchmarks
python3 gliner_eval.py ner_data --b2nerd-dir b2nerd/NER_en --threshold 0.8 --out g_cross \
  --eval crossner_ai,crossner_literature,crossner_music,crossner_politics,crossner_science
# a trained model (training uses only the three company/product datasets; its COMP predictions are scored as ORG)
python3 ner_unified.py ner_data --b2nerd-dir b2nerd/NER_en --train fewnerd --model roberta-base --epochs 3 --out u_fewnerd_cross \
  --eval crossner_ai,crossner_literature,crossner_music,crossner_politics,crossner_science
```
Read the numbers with care: PROD exists only in `crossner_ai` (197 test mentions), the other four sets have none, so their PROD column
is meaningless; and a model trained on "company" can only recover part of CrossNER's broader "organization" type (low ORG recall).

## Company dictionary (DBpedia), suggested by the professor
Step 1 needs internet (run it on your own machine or Colab; the sandbox cannot reach DBpedia). Either page the public SPARQL endpoint
(about a few minutes to an hour; restartable) or read the DBpedia dump files (instance types + English labels, from databus.dbpedia.org):
```bash
python3 fetch_dbpedia_companies.py sparql --out dbpedia_companies.txt                      # add --classes Company,Organisation for CrossNER
python3 fetch_dbpedia_companies.py dumps --types instance-types_lang=en_specific.ttl.bz2 --labels labels_lang=en.ttl.bz2 --out dbpedia_companies.txt
```
The SPARQL queries have been unit-tested as text only, not against the live endpoint, so expect to adjust them if DBpedia rejects one.
Step 2 needs no model: coverage of gold company strings, a dictionary-only baseline, and (with saved predictions) model + dictionary:
```bash
python3 analyze_gazetteer.py ner_data --names dbpedia_companies.txt --datasets fewnerd,wnut17,tweetner7 --stoplist \
  --system "RoBERTa=u_fewnerd_roberta" --system "GLiNER 0.8=g_zero_t08" --out gazetteer_analysis.md
```
`--stoplist` never accepts one-token matches of words that are almost never entities in the training split (the, good, who).
Few-NERD is built from Wikipedia, so its DBpedia coverage is optimistic; the tweet datasets are the fair test.

## Guideline prompt for the LLM, and recall by sentence density
`llm_eval.py --prompt` chooses the system message: `shots` (default, short type list plus 6 examples), `guide` (written annotation guidelines,
no examples) or `guide+shots`. The guideline text is `GUIDELINE` in `ldred/llm_ner.py`; it was written from the datasets' public annotation
schemes before any run and is not tuned on the test sentences. Use the same sample (`--eval-limit`, seed 13) as the run you compare with:
```bash
python3 llm_eval.py ner_data --eval fewnerd,wnut17,tweetner7 --eval-limit 300 --out l_llama8b_300            # baseline prompt, same 300 sentences
python3 llm_eval.py ner_data --eval fewnerd,wnut17,tweetner7 --eval-limit 300 --prompt guide --out l_guide
python3 llm_eval.py ner_data --eval fewnerd,wnut17,tweetner7 --eval-limit 300 --prompt guide+shots --out l_guide_shots
```
`analyze_density.py` splits the test sentences by gold entity density (entity tokens / tokens) and reports recall and false positives per group:
```bash
python3 analyze_density.py ner_data --system "RoBERTa=u_fewnerd_roberta" --system "GLiNER 0.8=g_zero_t08" --out density.md
python3 analyze_density.py ner_data --sample-from l_llama8b/metrics.json --system "LLM 8B=l_llama8b" --system "RoBERTa=u_fewnerd_roberta" --system "GLiNER 0.8=g_zero_t08" --out density_800.md
```

## Supervised runs for the best score (Colab GPU)
`ner_unified.py` trains on the training split(s) you list and scores the test split once at the end. `--keep-best` restores the epoch with the
best validation F1 (validation of all training datasets), so nothing is selected on the test sets. Use a GPU runtime (T4 is enough for base models;
for large models lower `--batch-size` to 16 if memory runs out).
```bash
# own-data models, one per dataset
python3 ner_unified.py ner_data --train wnut17 --eval wnut17 --model roberta-large --epochs 10 --lr 2e-5 --batch-size 16 --keep-best --out s_wnut_rl
python3 ner_unified.py ner_data --train fewnerd --eval fewnerd --model roberta-large --epochs 3 --lr 2e-5 --batch-size 16 --keep-best --out s_fewnerd_rl
# one model trained on all three, scored on all three
python3 ner_unified.py ner_data --train fewnerd,wnut17,tweetner7 --eval fewnerd,wnut17,tweetner7 --model roberta-large --epochs 3 --lr 2e-5 --batch-size 16 --keep-best --out s_all_rl
# same with DeBERTa-v3-large for comparison
python3 ner_unified.py ner_data --train fewnerd,wnut17,tweetner7 --eval fewnerd,wnut17,tweetner7 --model microsoft/deberta-v3-large --epochs 3 --lr 1e-5 --batch-size 16 --keep-best --out s_all_deb
```
Do a quick check first with `--train-limit 2000 --eval-limit 300 --epochs 1`. TweetNER7 alone is the partner's task.
