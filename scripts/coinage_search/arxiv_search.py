#!/usr/bin/env python3
"""arXiv search for the manuscript's coinages (Task 2 of the pre-submission checklist).

Queries arxiv.org/search with exact quoted phrases, parses hit counts and titles.
Also probes whether arXiv's search indexes full text (vs. metadata only) by
searching a body-only probe phrase; the result is recorded so the decision
document can state precisely what was searched."""
import json, pathlib, re, time, urllib.parse, urllib.request

OUT = pathlib.Path("/home/z/my-project/automata-repo/scripts/coinage_search")
OUT.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"}

PHRASES = [
    ("unifilar lumpability", "unifilar_lumpability"),
    ("unifilar-lumpable", "unifilar_lumpable"),
    ("commitment gap", "commitment_gap"),
    ("retention gap", "retention_gap"),
    ("grounding gap", "grounding_gap"),
    ("Price of Safety", "price_of_safety"),
    ("kappa_pair", "kappa_pair"),
    ("determination index", "determination_index"),
    ("protocol stratification", "protocol_stratification"),
]

def arxiv_search(phrase):
    q = urllib.parse.quote(f'"{phrase}"')
    url = f"https://arxiv.org/search/?query={q}&searchtype=all&size=25"
    req = urllib.request.Request(url, headers=UA)
    html = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "ignore")
    m = re.search(r"of\s+([\d,]+)\s+results", html)
    total = int(m.group(1).replace(",", "")) if m else 0
    zero = "your search returned zero results" in html or "Sorry" in html and total == 0
    titles = []
    if not zero:
        titles = re.findall(r'<p class="title is-5 mathjax">\s*(.*?)\s*</p>', html, re.S)
        titles = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).strip() for t in titles]
    return {"phrase": phrase, "total_results": total, "zero_results": zero, "top_titles": titles[:10], "url": url}

def probe_fulltext():
    # Body-only probe: a boilerplate phrase that appears in paper bodies but never in
    # abstracts/titles/metadata. Non-zero results => full-text indexing is active.
    probe = "this paper is organized as follows"
    r = arxiv_search(probe)
    return {"probe_phrase": probe, "total_results": r["total_results"],
            "conclusion": "FULL-TEXT search appears ACTIVE on arxiv.org/search"
            if r["total_results"] > 100 else
            "full-text indexing NOT confirmed; treat results as metadata-level"}

results = {}
print("=== arXiv full-text capability probe ===")
p = probe_fulltext()
print(json.dumps(p, indent=1)[:400])
results["_probe"] = p

print("\n=== coinage searches ===")
for phrase, key in PHRASES:
    try:
        r = arxiv_search(phrase)
    except Exception as e:
        r = {"phrase": phrase, "error": str(e)}
    results[key] = r
    print(f"[{key}] total={r.get('total_results')} zero={r.get('zero_results')} titles={r.get('top_titles', [])[:3]}")
    time.sleep(4)

(OUT / "arxiv_coinage_search.json").write_text(json.dumps(results, indent=1))
print(f"\nsaved -> {OUT / 'arxiv_coinage_search.json'}")
