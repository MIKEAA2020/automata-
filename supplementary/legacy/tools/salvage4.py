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


"""Print the shrunk statements side by side for hand comparison."""
import io
import os
import re

CUR = _p('automata_corrected.tex')
SRC_DIRS = [_p('uploads'), _p('archive/superseded_snapshots')]
ENV = (r'theorem|thm|lemma|lem|proposition|prop|corollary|cor|definition|def'
       r'|assumption|ass|remark|rem|metatheorem|example|ex|conjecture')

TARGETS = [
    'No Universal Cross-Regime Inequality',
    'Grounding as $p=\\infty$',
    'Exact commitment with approximate retention',
    'Commitment Exact Threshold',
    'Realizable $0/1$ Model Selection',
    'Compatibility with Causal States',
    'Scope of the Grounding Instance',
    'Profinite uniformity for discrete residual categories',
    'Different Exponents Are Structural',
]


def read(p):
    return io.open(p, encoding='utf-8', errors='replace',
                   newline='').read().replace('\r\n', '\n')


def ntitle(t):
    t = re.sub(r'\$[^$]*\$', '', t)
    t = t.replace('--', '-').replace('—', '-').replace('–', '-')
    t = re.sub(r'\\[a-zA-Z]+', '', t)
    t = re.sub(r"[^a-z0-9 ]", ' ', t.lower())
    return ' '.join(t.split())


def blocks(s):
    out = {}
    for m in re.finditer(
            r'\\begin\{(' + ENV + r')\}\s*\[([^\]]*)\](.*?)\\end\{\1\}', s, re.S):
        n = ntitle(m.group(2))
        if n and (n not in out or len(m.group(3)) > len(out[n])):
            out[n] = m.group(3)
    return out


cur = blocks(read(CUR))
want = {ntitle(t): t for t in TARGETS}

best = {}
for d in SRC_DIRS:
    if not os.path.isdir(d):
        continue
    for f in sorted(os.listdir(d)):
        if not f.endswith(('.tex', '.txt')):
            continue
        b = blocks(read(os.path.join(d, f)))
        for n in want:
            if n in b and (n not in best or len(b[n]) > len(best[n][1])):
                best[n] = (f, b[n])

for n, raw in want.items():
    if n not in best:
        continue
    f, src = best[n]
    print('#' * 78)
    print(f'# [{raw}]   src={f}')
    print('#' * 78)
    print('--- SOURCE ---')
    print(src.strip()[:1200])
    print()
    print('--- DELIVERABLE ---')
    print(cur.get(n, '(ABSENT)').strip()[:1200])
    print()
