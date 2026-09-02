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
Second pass: for each titled result absent from the deliverable BY TITLE,
decide whether the underlying MATHEMATICS is absent too.

Heuristic: extract the body of the environment, pull out its distinctive
mathematical tokens (macros, operators, distinctive words), and test whether a
sufficiently large fraction of them occur in the deliverable. Low coverage =>
genuinely missing content worth reading by hand.
"""
import io
import os
import re
from collections import defaultdict

CUR = _p('automata_corrected.tex')
SRC_DIRS = [_p('uploads'), _p('archive/superseded_snapshots')]
ENV = (r'theorem|thm|lemma|lem|proposition|prop|corollary|cor|definition|def'
       r'|assumption|ass|remark|rem|metatheorem|example|ex|conjecture|openproblem|open')


def read(p):
    return io.open(p, encoding='utf-8', errors='replace',
                   newline='').read().replace('\r\n', '\n')


def norm_title(t):
    t = re.sub(r'\$[^$]*\$', '', t)
    t = t.replace('--', '-').replace('—', '-').replace('–', '-')
    t = re.sub(r'\\[a-zA-Z]+', '', t)
    t = re.sub(r"[^a-z0-9 ]", ' ', t.lower())
    return ' '.join(t.split())


cur = read(CUR)
cur_titles = set()
for m in re.finditer(r'\\begin\{(' + ENV + r')\}\s*\[([^\]]*)\]', cur):
    n = norm_title(m.group(2))
    if n:
        cur_titles.add(n)

# tokens present in the deliverable
cur_tokens = set(re.findall(r'\\[A-Za-z]+', cur))
cur_words = set(re.findall(r'[A-Za-z]{6,}', cur.lower()))

STOP = {'begin', 'end', 'label', 'ref', 'emph', 'textbf', 'item', 'frac',
        'left', 'right', 'text', 'mathrm', 'mathcal', 'quad', 'qquad',
        'cite', 'bigl', 'bigr', 'sum', 'log', 'infty', 'ldots', 'cdots'}

blocks = {}   # normtitle -> (file, raw, body)
for d in SRC_DIRS:
    if not os.path.isdir(d):
        continue
    for f in sorted(os.listdir(d)):
        if not f.endswith(('.tex', '.txt')):
            continue
        p = os.path.join(d, f)
        s = read(p)
        for m in re.finditer(
                r'\\begin\{(' + ENV + r')\}\s*\[([^\]]*)\](.*?)\\end\{\1\}',
                s, re.S):
            n = norm_title(m.group(2))
            if not n or n in cur_titles:
                continue
            body = m.group(3)
            if n not in blocks or len(body) > len(blocks[n][2]):
                blocks[n] = (f, m.group(2), body)

rows = []
for n, (f, raw, body) in blocks.items():
    toks = {t for t in re.findall(r'\\[A-Za-z]+', body)
            if t[1:] not in STOP}
    words = {w for w in re.findall(r'[A-Za-z]{6,}', body.lower())}
    allt = toks | words
    if not allt:
        continue
    present = sum(1 for t in allt
                  if (t in cur_tokens if t.startswith('\\') else t in cur_words))
    cov = present / len(allt)
    rows.append((cov, len(body), raw, f, body))

rows.sort()

print('=' * 78)
print('CANDIDATES: titled results absent by title, ranked by token coverage')
print('(low coverage = mathematics likely absent too)')
print('=' * 78)
for cov, blen, raw, f, body in rows:
    flag = 'INSPECT' if cov < 0.80 else '   ok  '
    print(f'{flag}  cov={cov:5.2f}  len={blen:5d}  [{raw}]')
    print(f'                     src: {f}')

print()
print('=' * 78)
low = [r for r in rows if r[0] < 0.80]
print(f'{len(low)} candidates below 0.80 coverage -> read these by hand')
print('=' * 78)
for cov, blen, raw, f, body in low:
    print()
    print('#' * 78)
    print(f'# [{raw}]   cov={cov:.2f}  src={f}')
    print('#' * 78)
    print(body.strip()[:1400])
