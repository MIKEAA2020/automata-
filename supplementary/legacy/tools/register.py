import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.environ.get('BST_ROOT', _os.path.dirname(_HERE))
def _p(name):
    for c in (_os.path.join(_ROOT, name),
              _os.path.join(_ROOT, 'manuscript.tex') if name.endswith('.tex') else '',
              _os.path.join(_HERE, name)):
        if c and _os.path.exists(c):
            return c
    return _os.path.join(_ROOT, name)

"""
Detect changelog / diary / strawman register in the manuscript.

Categories:
  A. Changelog: 'retained because', 'no longer', 'previously', 'earlier version',
     'historical', 'corrected ... convention', 'this round'
  B. Strawman / phantom: 'naive', 'would be a type error', 'would not suffice',
     'is not asserted', 'one might think', 'a reader could', 'would count twice'
  C. Self-reference to prior drafts: 'the ungated family', 'the one-way variant',
     'the single toggle', 'an earlier'
  D. Editorial self-commentary: 'we note that', 'it is worth', 'instructive',
     'commendable', 'the reason is'
"""
import io
import re
import sys

s = io.open(_p('automata_corrected.tex'), encoding='utf-8',
            newline='').read().replace('\r\n', '\n')
lines = s.split('\n')

PATTERNS = {
    'A changelog': [
        r'\bis retained\b', r'\bare retained\b', r'\bretained because\b',
        r'\bno longer\b', r'\bpreviously\b', r'\bearlier version\b',
        r'\bhistorical\b', r'\bcorrected index convention\b',
        r'\bthis round\b', r'\bformer\b', r'\bnow (?:reads|states|says)\b',
    ],
    'B strawman': [
        r'\bnaive\b', r'\bna\\\"\{?\\?i\}?ve\b',
        r'would be a type error', r'would \\emph\{not\} suffice',
        r'would not suffice', r'\bis not asserted\b', r'\bnot claimed\b',
        r'one might (?:think|expect|suppose)', r'a reader (?:could|might)',
        r'count(?:ing)? that cost twice', r'\bwould fail\b',
        r'is not by itself well defined',
    ],
    'C prior-draft': [
        r'ungated family', r'one-way variant', r'single toggle',
        r'\ban earlier\b', r'older (?:version|draft)',
    ],
    'D self-commentary': [
        r'\bthe reason is instructive\b', r'\bit is worth\b',
        r'\bwe note that\b', r'\bcommendable\b', r'\bunusually\b',
        r'\bis instructive\b',
    ],
    # E-G added T42.  Self-descriptive emphasis, self-praise, and
    # reader-condescension.  Technical senses are spared by ALLOW below
    # ("sharp constant", "strong convexity", "trivial group", ...).
    'E emphasis adverbs': [
        r'\bcrucially\b', r'\bimportantly\b', r'\bnotably\b',
        r'\bremarkably\b', r'\bstrikingly\b', r'\btellingly\b',
        r'\binterestingly\b', r'\bsurprisingly\b', r'\bcrucial\b',
        r'\bpivotal\b', r'\bvital\b',
    ],
    'F self-praise': [
        r'\bnovel\b', r'\bpowerful\b', r'\belegant\b', r'\bprofound\b',
        r'\bcomprehensive\b', r'\bbeautiful\b', r'\billuminating\b',
        r'\bcompelling\b', r'\binsightful\b',
        r'\b(?:significant|important) contribution\b',
        r'\bwe (?:carefully|rigorously)\b',
        r'\bwe (?:believe|feel|hope)\b',
    ],
    'G reader-condescension': [
        r'\bobviously\b', r'\bevidently\b', r'\bneedless to say\b',
        r'\beas(?:y|ily) to see\b', r'\beasily seen\b', r'\bplainly\b',
        r'\bof course\b',
    ],
}

# Known-good exceptions: proved impossibility results, not strawmen.
ALLOW = [
    'two-point floor would fail for all large $T$',   # proved: capped at 2 log 2
]

# Technical senses of otherwise-flagged words are legitimate and are spared.
# 'sharp' (sharp constant/bound), 'strong convexity', 'nontrivial' (group,
# kernel), 'subtle'/'delicate' describing a REGIME rather than the exposition.
TECHNICAL = [
    r'sharp', r'strong(?:ly)? conve', r'\bstrong\b', r'nontrivial',
    r'non-trivial', r'delicate regime', r'\bsubtle\b', r'\bdeep\b',
]

hits = []
for i, ln in enumerate(lines, 1):
    if any(a in ln for a in ALLOW):
        continue
    for cat, pats in PATTERNS.items():
        for p in pats:
            if re.search(p, ln, re.I):
                hits.append((cat, i, p, ln.strip()))

by_cat = {}
for cat, i, p, ln in hits:
    by_cat.setdefault(cat, []).append((i, p, ln))

print('=' * 78)
print('REGISTER AUDIT: changelog / strawman / prior-draft / self-commentary')
print('=' * 78)
total = 0
for cat in sorted(by_cat):
    v = by_cat[cat]
    total += len(v)
    print(f'\n{cat}  ({len(v)} hits)')
    print('-' * 78)
    for i, p, ln in v:
        snippet = ln if len(ln) <= 110 else ln[:107] + '...'
        print(f'  L{i:<6} [{p}]')
        print(f'         {snippet}')

print()
print('=' * 78)
print(f'TOTAL: {total} flagged lines')
sys.exit(1 if total else 0)
