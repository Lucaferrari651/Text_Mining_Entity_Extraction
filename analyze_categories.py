"""Which categories does each system detect, and which does it miss? (per fine-grained gold category, from saved predictions)

  python3 analyze_categories.py ner_data --system "RoBERTa=u_fewnerd_roberta" --system "GLiNER 0.8=g_zero_t08" \
      --datasets fewnerd,wnut17,tweetner7 --out categories.md
  python3 analyze_categories.py ner_data --b2nerd-dir b2nerd/NER_en --system "GLiNER 0.8=g_cross" \
      --datasets crossner_ai,crossner_politics --out categories_cross.md

Table 1, per gold category (the dataset's own label, e.g. product-software, person-actor, corporation): number of gold mentions
and the share each system found (exact span AND the right unified type). Table 2, per system and predicted type: which gold
categories its wrong predictions fall on (same span, different gold label), and how many fall where the gold has no entity.
Prediction files must cover the whole test split (preds_<dataset>.json). Models trained with COMP count as ORG on CrossNER.
"""
import argparse, collections, json
from pathlib import Path
from ldred import ner_datasets as D


def text(doc, a, b):
    return " ".join(doc["sents"][0][a:b])


def category(doc, a, b, raw):
    """Fine category; for TweetNER7 the Twitter-handle markup is split out because it behaves very differently."""
    return raw + " (handle)" if text(doc, a, b).startswith("{@") else raw


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("data_dir"); ap.add_argument("--b2nerd-dir")
    ap.add_argument("--system", action="append", required=True)
    ap.add_argument("--datasets", default="fewnerd,wnut17,tweetner7"); ap.add_argument("--out")
    ap.add_argument("--min-count", type=int, default=15, help="hide categories with fewer gold mentions")
    a = ap.parse_args()
    systems = [s.split("=", 1) for s in a.system]
    md = []
    for name in a.datasets.split(","):
        cross = D.is_cross(name)
        docs = D.load(name, a.b2nerd_dir if cross else a.data_dir, "test")
        targets = D.target_types(name)
        preds = {}
        for label, folder in systems:
            p = Path(folder) / f"preds_{name}.json"
            if p.exists():
                x = [{tuple(s) for s in doc} for doc in json.load(open(p))]
                if len(x) == len(docs):
                    preds[label] = D.to_org_scale(x) if cross else x
        if not preds:
            continue
        md.append(f"# {name}\n")
        gold = collections.defaultdict(list)           # (unified, category) -> [(doc, a, b)]
        for i, d in enumerate(docs):
            for e in d["entities"]:
                for m in e["mentions"]:
                    gold[(e["type"], category(d, *m["pos"], e["raw_type"]))].append((i, m["pos"][0], m["pos"][1]))
        names = list(preds)
        md.append("## Share of gold mentions found (exact span and right type)\n")
        md.append("| Gold category | type | n | " + " | ".join(names) + " |\n|---|---|---|" + "---|" * len(names))
        for (u, cat), ms in sorted(gold.items(), key=lambda kv: (targets.index(kv[0][0]) if kv[0][0] in targets else 9, -len(kv[1]))):
            if u not in targets or len(ms) < a.min_count:
                continue
            cells = [f"{sum(any(s[1] == a_ and s[2] == b_ and s[3] == u for s in P[i]) for i, a_, b_ in ms) / len(ms):.0%}"
                     for P in preds.values()]
            md.append(f"| {cat} | {u} | {len(ms)} | " + " | ".join(cells) + " |")
        md.append("\n## What the wrong predictions of each type land on (same span, different gold category)\n")
        for label, P in preds.items():
            for T in targets:
                hit, none, total = collections.Counter(), 0, 0
                for i, pr in enumerate(P):
                    at = {(m["pos"][0], m["pos"][1]): (e["type"], category(docs[i], *m["pos"], e["raw_type"]))
                          for e in docs[i]["entities"] for m in e["mentions"]}
                    for s in pr:
                        if s[3] != T:
                            continue
                        total += 1
                        g = at.get((s[1], s[2]))
                        if g is None:
                            none += 1
                        elif g[0] != T:
                            hit[g[1]] += 1
                top = ", ".join(f"{c} ({n})" for c, n in hit.most_common(6)) or "-"
                md.append(f"- **{label}**, predicted {T} ({total}): wrong on same span as gold {top}; no gold entity at that span: {none}")
        md.append("")
    out = "\n".join(md)
    print(out)
    if a.out:
        Path(a.out).write_text(out, encoding="utf-8")


if __name__ == "__main__":
    main()
