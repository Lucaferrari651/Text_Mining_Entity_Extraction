"""Step 1 (needs internet): query Wikipedia and Wikidata search for every mention string and save the ranked
candidates to a JSON cache. Safe to stop and restart: finished strings are never queried twice.

  python3 fetch_wiki_candidates.py DATA_DIR --split dev --out wiki_cache_dev.json \
          --extra surfaces_extra_dev.txt --contact you@example.com [--limit 50]

Cache format: {"<lower-cased mention>": {"wikipedia": [titles...], "wikidata": ["Q..", ...]}}
"""
import argparse, json, re, sys, threading, time, urllib.parse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import requests

sys.path.insert(0, str(Path(__file__).parent))
from ldred.data import load_split, NOT_LINKABLE

WIKIPEDIA = "https://en.wikipedia.org/w/api.php"
WIKIDATA = "https://www.wikidata.org/w/api.php"


def parse_opensearch(payload):
    """MediaWiki opensearch (formatversion=2) -> [query, titles, descriptions, urls]; keep the page titles
    as they appear in the URL (underscores, percent-decoding undone), the same form as Linked-DocRED."""
    return [urllib.parse.unquote(u.split("/wiki/", 1)[1]) for u in payload[3] if "/wiki/" in u]


def parse_wbsearch(payload):
    return [r["id"] for r in payload.get("search", [])]


def get_json(session, url, params, retries=6):
    for attempt in range(retries):
        try:
            r = session.get(url, params=params, timeout=30)
            if r.status_code == 200:
                return r.json()
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(min(2 ** attempt, 60) * (2 if r.status_code == 429 else 1))
                continue
            raise RuntimeError(f"HTTP {r.status_code} for {params.get('search')!r}")
        except (requests.RequestException, ValueError):
            time.sleep(min(2 ** attempt, 60))
    return None                                   # give up on this string for now; a re-run retries it


def query_one(session, surface, n):
    wp = get_json(session, WIKIPEDIA, {"action": "opensearch", "format": "json", "formatversion": 2,
                                       "search": surface, "namespace": 0, "limit": n})
    wd = get_json(session, WIKIDATA, {"action": "wbsearchentities", "format": "json", "language": "en",
                                      "uselang": "en", "type": "item", "limit": n, "search": surface})
    if wp is None or wd is None:
        return None
    return {"wikipedia": parse_opensearch(wp), "wikidata": parse_wbsearch(wd)}


def surfaces_of(data_dir, split, extra):
    out = set()
    for d in load_split(data_dir, split):
        for e in d["entities"]:
            if e["type"] in NOT_LINKABLE:
                continue
            for m in e["mentions"]:
                out.add(m["name"].strip().lower())
    if extra:
        out |= {l.strip().lower() for l in Path(extra).read_text(encoding="utf-8").splitlines() if l.strip()}
    out.discard("")
    return sorted(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data_dir"); ap.add_argument("--split", default="dev"); ap.add_argument("--out", required=True)
    ap.add_argument("--extra", help="text file with extra mention strings, one per line")
    ap.add_argument("--contact", default="", help="your e-mail, put in the User-Agent (Wikimedia asks for it)")
    ap.add_argument("--candidates", type=int, default=10); ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--limit", type=int, help="only the first N strings (quick test)")
    a = ap.parse_args()

    out = Path(a.out)
    cache = json.loads(out.read_text(encoding="utf-8")) if out.exists() else {}
    todo = [s for s in surfaces_of(a.data_dir, a.split, a.extra) if s not in cache]
    if a.limit:
        todo = todo[: a.limit]
    print(f"{len(cache)} already cached, {len(todo)} to fetch", flush=True)

    session = requests.Session()
    session.headers["User-Agent"] = f"TextMiningCourseProject/1.0 (student project; {a.contact or 'no contact given'})"
    lock, done, t0 = threading.Lock(), 0, time.time()

    def work(s):
        nonlocal done
        res = query_one(session, s, a.candidates)
        with lock:
            if res is not None:
                cache[s] = res
            done += 1
            if done % 200 == 0 or done == len(todo):
                out.write_text(json.dumps(cache), encoding="utf-8")
                rate = done / (time.time() - t0)
                print(f"{done}/{len(todo)}  {rate:.1f} strings/s  eta {(len(todo)-done)/max(rate,1e-9)/60:.0f} min", flush=True)

    with ThreadPoolExecutor(a.workers) as ex:
        list(ex.map(work, todo))
    out.write_text(json.dumps(cache), encoding="utf-8")
    missing = [s for s in todo if s not in cache]
    print(f"finished. cache has {len(cache)} strings; {len(missing)} failed (re-run the same command to retry them)")


if __name__ == "__main__":
    main()
