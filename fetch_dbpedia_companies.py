"""Build a company name list from DBpedia (needs internet; not run from the sandbox, whose network blocks DBpedia).

Two ways, same output (one name per line, UTF-8):

  # A) public SPARQL endpoint, paged by name prefix (the endpoint caps every answer at about 10,000 rows)
  python3 fetch_dbpedia_companies.py sparql --out dbpedia_companies.txt [--classes Company] [--no-redirects]

  # B) offline, from the DBpedia dump files (download once from https://databus.dbpedia.org, English):
  #    instance-types (e.g. instance-types_lang=en_specific.ttl.bz2) and labels (labels_lang=en.ttl.bz2)
  python3 fetch_dbpedia_companies.py dumps --types instance_types.ttl.bz2 --labels labels_lang=en.ttl.bz2 \
          --out dbpedia_companies.txt [--classes Company]

--classes takes DBpedia ontology class names separated by commas (Company; add Organisation for CrossNER-style
organizations). Names are the English rdfs:label of each resource and, with redirects (SPARQL mode), the labels of the
pages that redirect to it (aliases such as 'IBM' for 'International Business Machines').
Safe to stop and restart in SPARQL mode: finished prefixes are stored in <out>.progress and are not queried again.
"""
import argparse, bz2, gzip, json, re, string, sys, time
from pathlib import Path

ENDPOINT = "https://dbpedia.org/sparql"
PREFIXES = list(string.ascii_uppercase) + list(string.digits)       # plus everything else, handled as 'other'
PAGE = 10000


def query_for(classes, prefix, redirects, offset):
    """SPARQL text for one page of labels whose first character is `prefix` ('other' = anything not A-Z / 0-9)."""
    cls = " ".join(f"dbo:{c}" for c in classes)
    if prefix == "other":
        flt = "FILTER(!REGEX(STR(?l), '^[A-Za-z0-9]'))"
    else:
        flt = f"FILTER(STRSTARTS(UCASE(STR(?l)), '{prefix}'))"
    body = f"?c a ?t . VALUES ?t {{ {cls} }} ?c rdfs:label ?l . FILTER(LANG(?l) = 'en') {flt}"
    if redirects:
        body = "{ " + body + " } UNION { ?c a ?t . VALUES ?t { " + cls + " } ?r dbo:wikiPageRedirects ?c . " \
               "?r rdfs:label ?l . FILTER(LANG(?l) = 'en') " + flt + " }"
    return ("PREFIX dbo: <http://dbpedia.org/ontology/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> "
            f"SELECT DISTINCT ?l WHERE {{ {body} }} ORDER BY ?l LIMIT {PAGE} OFFSET {offset}")


def parse_bindings(payload):
    return [b["l"]["value"] for b in payload["results"]["bindings"]]


def run_sparql(classes, out, redirects, contact):
    import requests
    out = Path(out)
    prog_path = Path(str(out) + ".progress")
    done = set(prog_path.read_text().split()) if prog_path.exists() else set()
    sess = requests.Session()
    sess.headers["User-Agent"] = f"text-mining-course-project ({contact})"
    with open(out, "a", encoding="utf-8") as f:
        for prefix in PREFIXES + ["other"]:
            if prefix in done:
                continue
            offset, n = 0, 0
            while True:
                for attempt in range(6):
                    r = sess.get(ENDPOINT, params={"query": query_for(classes, prefix, redirects, offset),
                                                   "format": "application/sparql-results+json"}, timeout=120)
                    if r.status_code == 200:
                        break
                    time.sleep(min(2 ** attempt, 60))
                else:
                    raise RuntimeError(f"DBpedia answered HTTP {r.status_code} for prefix {prefix}, offset {offset}")
                labels = parse_bindings(r.json())
                f.write("".join(l.replace("\n", " ") + "\n" for l in labels)); f.flush()
                n += len(labels)
                if len(labels) < PAGE:
                    break
                offset += PAGE
                time.sleep(1)
            with open(prog_path, "a") as p:
                p.write(prefix + "\n")
            print(f"prefix {prefix}: {n} names", file=sys.stderr)


_TRIPLE = re.compile(r'^<([^>]+)>\s+<([^>]+)>\s+(.+?)\s*\.\s*$')


def _open(path):
    path = str(path)
    return bz2.open(path, "rt", encoding="utf-8") if path.endswith(".bz2") else \
        gzip.open(path, "rt", encoding="utf-8") if path.endswith(".gz") else open(path, encoding="utf-8")


def read_dumps(types_path, labels_path, classes):
    """N-Triples / Turtle one-triple-per-line dumps -> sorted unique English labels of resources of the wanted classes."""
    wanted = {f"http://dbpedia.org/ontology/{c}" for c in classes}
    members = set()
    with _open(types_path) as f:
        for line in f:
            m = _TRIPLE.match(line)
            if m and m.group(2).endswith("22-rdf-syntax-ns#type") and m.group(3).strip("<>") in wanted:
                members.add(m.group(1))
    names = set()
    with _open(labels_path) as f:
        for line in f:
            m = _TRIPLE.match(line)
            if m and m.group(1) in members and m.group(2).endswith("rdf-schema#label"):
                lit = re.match(r'^"(.*)"@en$', m.group(3))
                if lit:
                    inner = lit.group(1)
                    try:                                    # N-Triples escapes (\" \\ \uXXXX) are valid JSON escapes
                        inner = json.loads('"' + inner + '"')
                    except ValueError:
                        pass
                    names.add(inner)
    return sorted(names)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="mode", required=True)
    s = sub.add_parser("sparql"); s.add_argument("--out", required=True); s.add_argument("--classes", default="Company")
    s.add_argument("--no-redirects", action="store_true"); s.add_argument("--contact", default="course project")
    d = sub.add_parser("dumps"); d.add_argument("--types", required=True); d.add_argument("--labels", required=True)
    d.add_argument("--out", required=True); d.add_argument("--classes", default="Company")
    a = ap.parse_args()
    classes = [c.strip() for c in a.classes.split(",") if c.strip()]
    if a.mode == "sparql":
        run_sparql(classes, a.out, not a.no_redirects, a.contact)
    else:
        names = read_dumps(a.types, a.labels, classes)
        Path(a.out).write_text("\n".join(names) + "\n", encoding="utf-8")
        print(f"{len(names)} names -> {a.out}", file=sys.stderr)
