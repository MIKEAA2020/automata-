#!/usr/bin/env python3
"""Fetch abstracts of the near-collision arXiv papers for precise classification."""
import re, urllib.parse, urllib.request, pathlib, json

UA = {"User-Agent": "Mozilla/5.0 (research-verification script)"}
TITLES = [
    "Commitment Gap via Correlation Gap",
    "Price of Safety in Linear Best Arm Identification",
    "Grounding Gaps in Language Model Generations",
    "Thermodynamics of Learning: A Typed Four-Component Accounting of Memory, Fit, and Value",
]
out = {}
for t in TITLES:
    q = urllib.parse.quote(f'ti:"{t}"')
    url = f"http://export.arxiv.org/api/query?search_query={q}&max_results=3"
    xml = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read().decode("utf-8", "ignore")
    entries = re.findall(r"<entry>(.*?)</entry>", xml, re.S)
    recs = []
    for e in entries:
        title = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", re.search(r"<title>(.*?)</title>", e, re.S).group(1))).strip()
        aid = re.search(r"<id>(.*?)</id>", e).group(1)
        summ = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", re.search(r"<summary>(.*?)</summary>", e, re.S).group(1))).strip()
        recs.append({"arxiv_id": aid, "title": title, "abstract": summ[:1400]})
    out[t] = recs
    print(f"=== {t} ===")
    for r in recs:
        print(f"  {r['arxiv_id']}\n  {r['abstract'][:500]}\n")

pathlib.Path("/home/z/my-project/automata-repo/scripts/coinage_search/near_collisions.json").write_text(json.dumps(out, indent=1))
print("saved -> scripts/coinage_search/near_collisions.json")
