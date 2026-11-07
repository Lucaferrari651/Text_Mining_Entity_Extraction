"""Few-shot LLM baseline for person / company / product (Cloudflare Workers AI), same data and metric as ner_unified.py.

  export CF_ACCOUNT_ID=...   CF_API_TOKEN=...          # never commit these
  python3 llm_eval.py ner_data --eval wnut17 --eval-limit 50 --out l_quick          # small test first
  python3 llm_eval.py ner_data --eval fewnerd,wnut17,tweetner7 --eval-limit 300 --out l_llama8b
  python3 llm_eval.py ner_data --eval fewnerd,wnut17,tweetner7 --eval-limit 300 --prompt guide --out l_guide          # guidelines, no examples
  python3 llm_eval.py ner_data --eval fewnerd,wnut17,tweetner7 --eval-limit 300 --prompt guide+shots --out l_guide_shots

A random but fixed sample (--eval-limit sentences, seed 13) is used because every sentence is one API call. Answers are cached in
<out>/cache.jsonl, so a rerun or a crash does not cost anything twice. The free plan allows 10,000 Neurons a day; when the limit
is hit the script stops with the API error, and rerunning the next day continues from the cache.
"""
import argparse, json, random
from pathlib import Path
from ldred import metrics as M
from ldred import ner_datasets as D
from ldred.llm_ner import PROMPTS, Cache, CloudflareChat, pick_shots, predict_docs

ap = argparse.ArgumentParser(); ap.add_argument("data_dir")
ap.add_argument("--eval", required=True); ap.add_argument("--eval-split", default="test", choices=["validation", "test"])
ap.add_argument("--model", default="@cf/meta/llama-3.1-8b-instruct-fp8-fast")
ap.add_argument("--shots", type=int, default=6, help="few-shot examples taken from the training split of each dataset")
ap.add_argument("--prompt", default="shots", choices=list(PROMPTS),
                help="shots: short type list + examples (default); guide: written annotation guidelines, no examples; "
                     "guide+shots: guidelines and examples")
ap.add_argument("--eval-limit", type=int, default=300); ap.add_argument("--seed", type=int, default=13)
ap.add_argument("--out", default="l_out")
a = ap.parse_args()
out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
chat, cache = CloudflareChat(a.model), Cache(out / "cache.jsonl")
res = {}
for name in a.eval.split(","):
    docs = D.load(name, a.data_dir, a.eval_split)
    docs = random.Random(a.seed).sample(docs, min(a.eval_limit, len(docs)))
    shots = [] if a.prompt == "guide" else pick_shots(D.load(name, a.data_dir, "train"), a.shots, a.seed)
    print(name, len(docs), "sentences,", len(shots), "shots", flush=True)
    preds = predict_docs(chat, docs, shots, a.model, cache, log=lambda s: print(s, flush=True), system=PROMPTS[a.prompt])
    r = M.ner_f1(docs, preds, D.TARGET)
    res[name] = {t: list(v) for t, v in r.items()}
    line = "  ".join(f"{t} F1={r[t][2]:.3f}" for t in D.TARGET if t in r)
    print(f"{name:10s} [{a.eval_split}, {len(docs)} sent.] PER+COMP+PROD micro P={r['ALL'][0]:.3f} R={r['ALL'][1]:.3f} F1={r['ALL'][2]:.3f} | {line}")
    json.dump([sorted(map(list, p)) for p in preds], open(out / f"preds_{name}.json", "w"))
json.dump({"args": vars(a), "results": res}, open(out / "metrics.json", "w"), indent=1)
