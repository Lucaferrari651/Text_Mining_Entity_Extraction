"""Few-shot NER with a chat LLM (Cloudflare Workers AI): prompt building, answer parsing, mapping answers to token spans.

The LLM sees a sentence and is asked for a bullet list "- mention | TYPE" (the format used in the Nishida et al. 2026
prompt, Figure 6). We then tag every exact occurrence of each listed mention in the sentence. Only the network call
(`CloudflareChat`) needs internet; everything else is pure Python and unit-tested with a fake model.
"""
import hashlib, json, os, re, time
from pathlib import Path
from .gliner_ner import char_to_token_span, resolve_overlaps, tokens_to_text

TYPES = ("PER", "COMP", "PROD")
INSTRUCTION = (
    "Given a sentence, extract all entity mentions of the types below. Each mention must be an exact copy of a text span "
    "of the sentence. Give one line per mention in the form `- mention | TYPE`. If there is none, answer `None`.\n\n"
    "Types:\n"
    "- PER: names of people (real or fictional), including nicknames and handles of persons.\n"
    "- COMP: names of companies, corporations and businesses.\n"
    "- PROD: names of products and services (devices, software, apps, games, vehicles, weapons, food brands).\n"
    "Do not extract places, groups, bands, teams, creative works, events or generic nouns.")


def fmt_answer(doc):
    rows = []
    for e in doc["entities"]:
        if e["type"] in TYPES:
            a, b = e["mentions"][0]["pos"]
            rows.append(f"- {' '.join(doc['sents'][0][a:b])} | {e['type']}")
    return "\n".join(rows) if rows else "None"


def build_messages(doc, shots):
    """Chat messages: system instruction, then each example as a user/assistant pair, then the test sentence."""
    msgs = [{"role": "system", "content": INSTRUCTION}]
    for s in shots:
        msgs += [{"role": "user", "content": "Sentence: " + " ".join(s["sents"][0])},
                 {"role": "assistant", "content": fmt_answer(s)}]
    msgs.append({"role": "user", "content": "Sentence: " + " ".join(doc["sents"][0])})
    return msgs


def parse_answer(text):
    """'- mention | TYPE' lines -> list of (mention, TYPE); unknown types and malformed lines are dropped."""
    out = []
    for line in text.splitlines():
        m = re.match(r"^\s*[-*•]?\s*(.+?)\s*\|\s*([A-Za-z]+)\s*$", line)
        if m and m.group(2).upper() in TYPES:
            out.append((m.group(1).strip(" `\"'"), m.group(2).upper()))
    return out


def to_spans(doc, mentions):
    """Every exact occurrence of each mention in the sentence that lines up with token boundaries -> {(0, a, b, TYPE)}."""
    tokens = doc["sents"][0]
    text, offs = tokens_to_text(tokens)
    starts, ends = {a for a, _ in offs}, {b for _, b in offs}
    spans = []
    for mention, typ in mentions:
        if not mention:
            continue
        for m in re.finditer(re.escape(mention), text):
            if m.start() in starts and m.end() in ends:
                a, b = char_to_token_span(offs, m.start(), m.end())
                spans.append((a, b, typ, float(len(mention))))          # longer mention wins an overlap
    return {(0, a, b, t) for a, b, t, _ in resolve_overlaps(spans)}


def pick_shots(train_docs, k=6, seed=13):
    """Fixed few-shot examples: half with at least one target entity, half without (so 'None' is demonstrated)."""
    import random
    rng = random.Random(seed)
    pos = [d for d in train_docs if any(e["type"] in TYPES for e in d["entities"])]
    neg = [d for d in train_docs if not any(e["type"] in TYPES for e in d["entities"])]
    shots = rng.sample(pos, k - k // 3) + rng.sample(neg, k // 3)
    rng.shuffle(shots)
    return shots


class Cache:
    """Append-only jsonl cache, so a rerun (or a crash) never pays twice for the same prompt."""
    def __init__(self, path):
        self.path, self.data = Path(path), {}
        if self.path.exists():
            for line in self.path.read_text(encoding="utf-8").splitlines():
                r = json.loads(line); self.data[r["key"]] = r["answer"]

    @staticmethod
    def key(model, messages):
        return hashlib.sha1(json.dumps([model, messages], sort_keys=True).encode()).hexdigest()

    def get(self, k):
        return self.data.get(k)

    def put(self, k, answer):
        self.data[k] = answer
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps({"key": k, "answer": answer}) + "\n")


class CloudflareChat:
    """Minimal client for Workers AI text generation. Credentials come from CF_ACCOUNT_ID and CF_API_TOKEN."""
    def __init__(self, model, account=None, token=None, retries=5):
        self.model, self.retries = model, retries
        self.account = account or os.environ["CF_ACCOUNT_ID"]
        self.token = token or os.environ["CF_API_TOKEN"]

    def __call__(self, messages):
        import requests
        url = f"https://api.cloudflare.com/client/v4/accounts/{self.account}/ai/run/{self.model}"
        for attempt in range(self.retries):
            r = requests.post(url, headers={"Authorization": f"Bearer {self.token}"},
                              json={"messages": messages, "temperature": 0, "max_tokens": 256}, timeout=60)
            if r.status_code == 200 and r.json().get("success"):
                res = r.json()["result"]
                return res.get("response") if isinstance(res, dict) else str(res)
            if r.status_code in (429, 500, 502, 503):
                time.sleep(2 ** attempt); continue
            raise RuntimeError(f"Cloudflare error {r.status_code}: {r.text[:300]}")      # e.g. daily Neuron limit
        raise RuntimeError("Cloudflare: too many retries")


def predict_docs(chat, docs, shots, model_name, cache, log=print):
    """One predicted span set per sentence. `chat(messages) -> str`."""
    out = []
    for n, doc in enumerate(docs):
        msgs = build_messages(doc, shots)
        k = Cache.key(model_name, msgs)
        ans = cache.get(k)
        if ans is None:
            ans = chat(msgs) or ""
            cache.put(k, ans)
        out.append(to_spans(doc, parse_answer(ans)))
        if (n + 1) % 50 == 0:
            log(f"  {n + 1}/{len(docs)} sentences")
    return out
