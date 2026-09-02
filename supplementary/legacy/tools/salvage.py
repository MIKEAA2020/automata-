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
Systematic salvage sweep.

For every source version, extract:
  - every theorem-like environment TITLE  (\begin{thm}[Title])
  - every \label
  - every \bibitem key
and report what exists in a source but NOT in the current deliverable.

Title matching is canonicalised (case, whitespace, LaTeX dashes, math stripped)
because the lean v5 rewrite has zero \labels and renames freely.
"""
import io
import os
import re
import sys
from collections import defaultdict

CUR = _p('automata_corrected.tex')
SRC_DIRS = [_p('uploads'), _p('archive/superseded_snapshots')]

ENV = (r'theorem|thm|lemma|lem|proposition|prop|corollary|cor|definition|def'
       r'|assumption|ass|remark|rem|metatheorem|example|ex|conjecture|openproblem|open')


def read(p):
    return io.open(p, encoding='utf-8', errors='replace', newline='').read().replace('\r\n', '\n')


def norm_title(t):
    t = re.sub(r'\$[^$]*\$', '', t)              # strip math
    t = t.replace('--', '-').replace('—', '-').replace('–', '-')
    t = re.sub(r'\\[a-zA-Z]+', '', t)            # strip control seqs
    t = re.sub(r"[^a-z0-9 ]", ' ', t.lower())
    return ' '.join(t.split())


def titles_of(s):
    out = {}
    for m in re.finditer(r'\\begin\{(' + ENV + r')\}\s*\[([^\]]*)\]', s):
        n = norm_title(m.group(2))
        if n:
            out.setdefault(n, []).append(m.group(2))
    return out


def labels_of(s):
    return set(re.findall(r'\\label\{([^}]*)\}', s))


def bibs_of(s):
    return set(re.findall(r'\\bibitem\{([^}]*)\}', s))


cur = read(CUR)
cur_titles = titles_of(cur)
cur_labels = labels_of(cur)
cur_bibs = bibs_of(cur)

print('=' * 78)
print('SALVAGE SWEEP  --  content present in a source but absent from the deliverable')
print('=' * 78)
print(f'deliverable: {len(cur_titles)} titled results, {len(cur_labels)} labels, '
      f'{len(cur_bibs)} bibitems\n')

files = []
for d in SRC_DIRS:
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            if f.endswith(('.tex', '.txt')):
                files.append(os.path.join(d, f))

missing_titles = defaultdict(list)   # normtitle -> [(file, raw)]
missing_labels = defaultdict(list)

for p in files:
    s = read(p)
    t = titles_of(s)
    l = labels_of(s)
    b = bibs_of(s)
    mt = {k: v for k, v in t.items() if k not in cur_titles}
    ml = l - cur_labels
    mb = b - cur_bibs
    base = os.path.basename(p)
    print(f'--- {base}')
    print(f'    {len(t)} titled results, {len(l)} labels, {len(b)} bibitems')
    print(f'    NOT in deliverable: {len(mt)} titles, {len(ml)} labels, {len(mb)} bibitems')
    for k, v in mt.items():
        missing_titles[k].append((base, v[0]))
    for k in ml:
        missing_labels[k].append(base)

print()
print('=' * 78)
print(f'UNIQUE TITLED RESULTS ABSENT FROM DELIVERABLE: {len(missing_titles)}')
print('=' * 78)
for k in sorted(missing_titles):
    srcs = missing_titles[k]
    raw = srcs[0][1]
    where = ', '.join(sorted({x[0] for x in srcs}))
    print(f'  [{raw}]')
    print(f'      in: {where}')

print()
print('=' * 78)
print(f'LABELS ABSENT FROM DELIVERABLE: {len(missing_labels)}')
print('=' * 78)
for k in sorted(missing_labels):
    print(f'  {k:45s} {", ".join(sorted(set(missing_labels[k])))[:60]}')
