"""Compare NER systems (trained model, GLiNER, LLM) on the same sentences, from their saved predictions. No model, no network.

  python3 compare_ner.py ner_data --sample-from l_llama8b/metrics.json \
      --system "LLM 8B=l_llama8b" --system "GLiNER 0.5=g_zero" --system "GLiNER 0.8=g_zero_t08" --out comparison

Every system folder holds preds_<dataset>.json (as written by ner_unified.py, gliner_eval.py, llm_eval.py). A file is either
for the whole test set (GLiNER, RoBERTa) or for the random sample the LLM script drew; which one is detected from its length.
The sample is rebuilt from the LLM run's settings (--sample-from metrics.json: seed, eval_limit, eval_split), so the head-to-head
tables score every system on exactly the same sentences. Systems that only exist on the sample are skipped in the "full" table.

Also prints, per system, what happened to each gold COMPANY / PRODUCT mention: found (right span and type), same span but
another type (and which), overlapping span with other boundaries, or missed. This is the company-vs-product error analysis.
"""
import argparse, json, random
from collections import Counter
from pathlib import Path
from ldred import metrics as M
from ldred import ner_datasets as D


def sample_indices(n_docs, limit, seed):
    """Indices drawn by llm_eval.py: random.Random(seed).sample(docs, limit); sampling a list or a range of the same size picks
    the same positions."""
    return random.Random(seed).sample(range(n_docs), min(limit, n_docs))


def load_preds(path):
    return [{tuple(s) for s in doc} for doc in json.load(open(path))]


def gold_spans(doc):
    return {(m["sent_id"], m["pos"][0], m["pos"][1]): e["type"] for e in doc["entities"] for m in e["mentions"]}


def fate(gold_docs, preds, types=("COMP", "PROD")):
    """For each gold mention of `types`: 'found', 'other type: X', 'boundary' (overlaps a prediction of the right or another
    type with different span) or 'missed'."""
    out = {t: Counter() for t in types}
    for doc, pred in zip(gold_docs, preds):
        by_span = {}
        for s, a, b, t in pred:
            by_span.setdefault((s, a, b), set()).add(t)
        for (s, a, b), t in gold_spans(doc).items():
            if t not in types:
                continue
            here = by_span.get((s, a, b), set())
            if t in here:
                out[t]["found"] += 1
            elif here:
                out[t]["same span, other type: " + "/".join(sorted(here))] += 1
            elif any(ps == s and pa < b and pb > a for ps, pa, pb, _ in pred):
                out[t]["overlapping, different boundaries"] += 1
            else:
                out[t]["missed"] += 1
    return out


def row(label, r):
    cells = [f"{r[t][2]:.3f}" if t in r else "-" for t in D.TARGET]
    return f"| {label} | {r['ALL'][0]:.3f} | {r['ALL'][1]:.3f} | **{r['ALL'][2]:.3f}** | " + " | ".join(cells) + " |"


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("data_dir")
    ap.add_argument("--system", action="append", required=True, help='"label=folder" (repeatable)')
    ap.add_argument("--sample-from", required=True, help="metrics.json of the LLM run (gives seed, eval_limit, eval_split, datasets)")
    ap.add_argument("--out", help="write <out>.md and <out>.json")
    a = ap.parse_args()
    meta = json.load(open(a.sample_from))["args"]
    systems = [s.split("=", 1) for s in a.system]
    header = "| System | P | R | F1 | " + " | ".join(f"{t} F1" for t in D.TARGET) + " |\n|---|---|---|---|" + "---|" * len(D.TARGET)
    md, dump = [], {}
    for name in meta["eval"].split(","):
        docs = D.load(name, a.data_dir, meta["eval_split"])
        idx = sample_indices(len(docs), meta["eval_limit"], meta["seed"])
        sub = [docs[i] for i in idx]
        tables = {"same sampled sentences (n=%d)" % len(sub): [], "full %s set (n=%d)" % (meta["eval_split"], len(docs)): []}
        fates = []
        for label, folder in systems:
            p = Path(folder) / f"preds_{name}.json"
            if not p.exists():
                continue
            preds = load_preds(p)
            if len(preds) == len(docs):
                full, on_sub = preds, [preds[i] for i in idx]
                tables["full %s set (n=%d)" % (meta["eval_split"], len(docs))].append(row(label, M.ner_f1(docs, full, D.TARGET)))
            elif len(preds) == len(sub):
                on_sub = preds
            else:
                print(f"skip {label}/{name}: {len(preds)} predictions, expected {len(docs)} or {len(sub)}"); continue
            r = M.ner_f1(sub, on_sub, D.TARGET)
            tables["same sampled sentences (n=%d)" % len(sub)].append(row(label, r))
            dump.setdefault(name, {})[label] = {t: list(v) for t, v in r.items()}
            fates.append((label, fate(sub, on_sub)))
        md.append(f"## {name}")
        for title, rows in tables.items():
            if rows:
                md += [f"\n**{title}**\n", header, *rows]
        md.append("\n**Gold company / product mentions on the sampled sentences: what happened**\n")
        for label, f in fates:
            for t in ("COMP", "PROD"):
                total = sum(f[t].values())
                parts = ", ".join(f"{k}: {v} ({v / total:.0%})" for k, v in f[t].most_common()) if total else "no gold mentions"
                md.append(f"- {label}, gold {t} (n={total}): {parts}")
        md.append("")
    text = "\n".join(md)
    print(text)
    if a.out:
        Path(a.out + ".md").write_text(text, encoding="utf-8")
        json.dump(dump, open(a.out + ".json", "w"), indent=1)
