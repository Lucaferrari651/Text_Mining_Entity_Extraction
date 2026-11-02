"""Stage 1, transformer version - mention detection as token classification (BIO over the 6 Linked-DocRED types).

Whole documents are encoded at once when they fit in `max_len` sub-words (Longformer: 4096); longer documents are
split into overlapping windows and every word takes the prediction of the window in which it is most central.
The label of a word sits on its first sub-word; the other sub-words are ignored (-100) in the loss.
Everything except `train_and_predict` is pure Python (no torch), so it can be unit-tested anywhere.
"""
from .data import TYPES, bio_tags, decode_bio

def make_labels(types):
    """BIO label list (and label -> id) for a list of entity types."""
    labels = ["O"] + [f"{p}-{t}" for t in types for p in ("B", "I")]
    return labels, {l: i for i, l in enumerate(labels)}


LABELS, L2I = make_labels(TYPES)       # Linked-DocRED types, kept as the default
IGNORE = -100


def doc_words(doc):
    """Flatten the sentences of a document -> (words, sent_id of each word, position in its sentence)."""
    words, sid, pos = [], [], []
    for s, sent in enumerate(doc["sents"]):
        for i, w in enumerate(sent):
            words.append(w); sid.append(s); pos.append(i)
    return words, sid, pos


def doc_labels(doc, l2i=L2I):
    return [l2i[t] for sent in bio_tags(doc) for t in sent]


def word_pieces(tokenizer, words):
    """Sub-word ids of every word (list of lists), without special tokens."""
    ids = tokenizer(list(words), add_special_tokens=False)["input_ids"]
    return [p if p else [tokenizer.unk_token_id] for p in ids]      # a word that vanishes becomes [UNK]


def flatten(pieces, labels=None):
    """-> sub-word ids, first-subword flag per sub-word, word index per sub-word, label per sub-word."""
    ids, first, widx, lab = [], [], [], []
    for w, p in enumerate(pieces):
        for k, t in enumerate(p):
            ids.append(t); first.append(k == 0); widx.append(w)
            lab.append(labels[w] if (labels is not None and k == 0) else IGNORE)
    return ids, first, widx, lab


def make_windows(n, max_len, overlap=128):
    """Windows (start, end) over n sub-words; each leaves 2 slots for the special tokens."""
    size = max_len - 2
    if n <= size:
        return [(0, n)]
    step = max(size - overlap, 1)
    wins, s = [], 0
    while True:
        e = min(s + size, n)
        wins.append((s, e))
        if e == n:
            return wins
        s += step


def best_window(windows, n):
    """For each sub-word position, the index of the window where it is farthest from the window edges."""
    best, dist = [0] * n, [-1] * n
    for w, (s, e) in enumerate(windows):
        for p in range(s, e):
            d = min(p - s, e - 1 - p)
            if d > dist[p]:
                dist[p], best[p] = d, w
    return best


def words_to_sentence_tags(doc, word_tags):
    """Per-word label strings -> set of (sent, start, end, type), decoding sentence by sentence."""
    out, k = set(), 0
    for sid, sent in enumerate(doc["sents"]):
        tags = word_tags[k:k + len(sent)]; k += len(sent)
        for a, b, t in decode_bio(tags):
            out.add((sid, a, b, t))
    return out


def train_and_predict(train_docs, dev_docs, model_name, out_dir, epochs=5, lr=5e-5, batch_size=8, max_len=512,
                      overlap=128, seed=13, log=print, eval_fn=None, types=None, eval_sets=None):
    """Fine-tune `model_name` on train_docs; return predicted span sets for dev_docs (one set per document).
    `types` = entity types to tag (default: the 6 Linked-DocRED types).
    `eval_sets` = {name: docs}: if given, return {name: predicted span sets} for each set instead (dev_docs may be [])."""""
    import random
    import numpy as np
    import torch
    from transformers import AutoModelForTokenClassification, AutoTokenizer, get_linear_schedule_with_warmup

    labels, l2i = (LABELS, L2I) if types is None else make_labels(types)
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    dev_ = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    try:
        tok = AutoTokenizer.from_pretrained(model_name, add_prefix_space=True)   # roberta/longformer need it
    except TypeError:
        tok = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForTokenClassification.from_pretrained(
        model_name, num_labels=len(labels), id2label=dict(enumerate(labels)), label2id=l2i).to(dev_)
    cls_id = tok.cls_token_id if tok.cls_token_id is not None else tok.bos_token_id
    sep_id = tok.sep_token_id if tok.sep_token_id is not None else tok.eos_token_id
    pad_id = tok.pad_token_id or 0

    def encode(doc, with_labels):
        words, _, _ = doc_words(doc)
        ids, first, widx, lab = flatten(word_pieces(tok, words), doc_labels(doc, l2i) if with_labels else None)
        return ids, first, widx, lab

    def batchify(seqs):
        n = max(len(s[0]) for s in seqs)
        x = torch.full((len(seqs), n), pad_id); m = torch.zeros((len(seqs), n), dtype=torch.long)
        y = torch.full((len(seqs), n), IGNORE)
        for i, (ids, lab) in enumerate(seqs):
            x[i, :len(ids)] = torch.tensor(ids); m[i, :len(ids)] = 1; y[i, :len(ids)] = torch.tensor(lab)
        return x.to(dev_), m.to(dev_), y.to(dev_)

    def windows_of(doc, with_labels):
        ids, first, widx, lab = encode(doc, with_labels)
        wins = make_windows(len(ids), max_len, overlap)
        seqs = [([cls_id] + ids[s:e] + [sep_id], [IGNORE] + lab[s:e] + [IGNORE]) for s, e in wins]
        return seqs, (ids, first, widx, wins)

    train_seqs = [sq for d in train_docs for sq in windows_of(d, True)[0]]
    log(f"{len(train_docs)} train docs -> {len(train_seqs)} windows; device {dev_}; model {model_name}")
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01)
    steps = epochs * ((len(train_seqs) + batch_size - 1) // batch_size)
    sched = get_linear_schedule_with_warmup(opt, int(0.1 * steps), steps)
    amp = dev_.type == "cuda"
    scaler = torch.amp.GradScaler(enabled=amp)

    @torch.no_grad()
    def predict(docs):
        model.eval(); out = []
        for doc in docs:
            seqs, (ids, first, widx, wins) = windows_of(doc, False)
            logits = []
            for i in range(0, len(seqs), batch_size):
                x, m, _ = batchify([(s[0], s[1]) for s in seqs[i:i + batch_size]])
                with torch.autocast(device_type=dev_.type, enabled=amp):
                    logits.append(model(input_ids=x, attention_mask=m).logits.float().cpu())
            best = best_window(wins, len(ids))
            n_words = len(doc_words(doc)[0]); tags = ["O"] * n_words
            for p in range(len(ids)):
                if first[p]:
                    w = best[p]; s0 = wins[w][0]
                    lg = logits[w // batch_size][w % batch_size, 1 + p - s0]
                    tags[widx[p]] = labels[int(lg.argmax())]
            out.append(words_to_sentence_tags(doc, tags))
        model.train(); return out

    model.train()
    for ep in range(epochs):
        random.shuffle(train_seqs); tot = 0.0
        for i in range(0, len(train_seqs), batch_size):
            x, m, y = batchify(train_seqs[i:i + batch_size])
            with torch.autocast(device_type=dev_.type, enabled=amp):
                loss = model(input_ids=x, attention_mask=m, labels=y).loss
            opt.zero_grad(); scaler.scale(loss).backward(); scaler.unscale_(opt)
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            scaler.step(opt); scaler.update(); sched.step(); tot += loss.item()
        msg = f"epoch {ep + 1}/{epochs}  train loss {tot / max(1, len(train_seqs) / batch_size):.4f}"
        if eval_fn is not None:
            msg += f"  dev mention F1 {eval_fn(predict(dev_docs)):.4f}"
        log(msg)
    preds = {k: predict(v) for k, v in eval_sets.items()} if eval_sets is not None else predict(dev_docs)
    if out_dir:
        model.save_pretrained(out_dir); tok.save_pretrained(out_dir)
    return preds
