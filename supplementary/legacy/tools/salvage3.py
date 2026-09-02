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
DEEP salvage sweep -- looks for loss that title/label matching cannot see.

  (1) CONDENSED PROOFS: same result present in both, but the source proof is
      substantially longer than the deliverable proof.
  (2) SHRUNK STATEMENTS: same result, source statement longer (dropped
      hypotheses / clauses).
  (3) LOST DISPLAY EQUATIONS: distinctive \[...\] displays in a source with no
      counterpart in the deliverable.
  (4) LOST SECTIONS: \section/\subsection titles absent.
  (5) LOST BIBITEMS: bib keys in sources absent from the deliverable.
"""
import io
import os
import re
import sys
from collections import defaultdict

CUR = _p('automata_corrected.tex')
SRC_DIRS = [_p('uploads'), _p('archive/superseded_snapshots')]
ENV = (r'theorem|thm|lemma|lem|proposition|prop|corollary|cor|definition|def'
       r'|assumption|ass|remark|rem|metatheorem|example|ex|conjecture')


def read(p):
    return io.open(p, encoding='utf-8', errors='replace',
                   newline='').read().replace('\r\n', '\n')


def ntitle(t):
    t = re.sub(r'\$[^$]*\$', '', t)
    t = t.replace('--', '-').replace('—', '-').replace('–', '-')
    t = re.sub(r'\\[a-zA-Z]+', '', t)
    t = re.sub(r"[^a-z0-9 ]", ' ', t.lower())
    return ' '.join(t.split())


def words(x):
    x = re.sub(r'\\[a-zA-Z]+', ' ', x)
    return len(re.findall(r'\w+', x))


def blocks_with_proofs(s):
    """title -> (statement, proof)."""
    out = {}
    for m in re.finditer(
            r'\\begin\{(' + ENV + r')\}\s*\[([^\]]*)\](.*?)\\end\{\1\}', s, re.S):
        n = ntitle(m.group(2))
        if not n:
            continue
        stmt = m.group(3)
        tail = s[m.end():m.end() + 200]
        proof = ''
        if re.match(r'\s*\\begin\{proof\}', tail):
            pm = re.search(r'\\begin\{proof\}(?:\[[^\]]*\])?(.*?)\\end\{proof\}',
                           s[m.end():], re.S)
            if pm and pm.start() < 200:
                proof = pm.group(1)
        prev = out.get(n)
        if prev is None or words(stmt) + words(proof) > words(prev[0]) + words(prev[1]):
            out[n] = (stmt, proof, m.group(2))
    return out


cur = read(CUR)
cur_blocks = blocks_with_proofs(cur)
cur_disp = set()
for m in re.finditer(r'\\\[(.*?)\\\]', cur, re.S):
    cur_disp.add(' '.join(m.group(1).split()))
cur_secs = {ntitle(m.group(2)) for m in
            re.finditer(r'\\(sub)*section\*?\{([^}]*)\}', cur)}
cur_bibs = set(re.findall(r'\\bibitem\{([^}]*)\}', cur))
cur_tok = set(re.findall(r'\\[A-Za-z]+', cur))

files = []
for d in SRC_DIRS:
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            if f.endswith(('.tex', '.txt')):
                files.append(os.path.join(d, f))

cond_proof = {}
shrunk_stmt = {}
lost_secs = defaultdict(list)
lost_bibs = defaultdict(list)

for p in files:
    s = read(p)
    base = os.path.basename(p)
    for n, (stmt, proof, raw) in blocks_with_proofs(s).items():
        if n not in cur_blocks:
            continue
        cs, cp, _ = cur_blocks[n]
        sw, cw = words(proof), words(cp)
        if sw >= 40 and cw > 0 and sw > 1.5 * cw:
            key = (n, raw)
            if key not in cond_proof or sw > cond_proof[key][1]:
                cond_proof[key] = (base, sw, cw, proof, cp)
        if sw >= 40 and cw == 0:
            key = (n, raw)
            cond_proof.setdefault(key, (base, sw, 0, proof, ''))
        ss, cs_w = words(stmt), words(cs)
        if ss >= 40 and ss > 1.4 * cs_w:
            shrunk_stmt[(n, raw)] = (base, ss, cs_w, stmt, cs)
    for m in re.finditer(r'\\(sub)*section\*?\{([^}]*)\}', s):
        t = ntitle(m.group(2))
        if t and t not in cur_secs:
            lost_secs[t].append(base)
    for b in re.findall(r'\\bibitem\{([^}]*)\}', s):
        if b not in cur_bibs:
            lost_bibs[b].append(base)

print('=' * 78)
print('(1) CONDENSED OR MISSING PROOFS  (source proof >1.5x deliverable)')
print('=' * 78)
if not cond_proof:
    print('  none')
for (n, raw), (base, sw, cw, sp, cp) in sorted(
        cond_proof.items(), key=lambda kv: -(kv[1][1] - kv[1][2])):
    print(f'  [{raw}]')
    print(f'      source {sw}w vs deliverable {cw}w   (+{sw-cw})   src={base}')

print()
print('=' * 78)
print('(2) SHRUNK STATEMENTS  (source statement >1.4x deliverable)')
print('=' * 78)
if not shrunk_stmt:
    print('  none')
for (n, raw), (base, ss, cw, a, b) in sorted(
        shrunk_stmt.items(), key=lambda kv: -(kv[1][1] - kv[1][2])):
    print(f'  [{raw}]  source {ss}w vs deliverable {cw}w  src={base}')

print()
print('=' * 78)
print(f'(4) SECTION TITLES ABSENT: {len(lost_secs)}')
print('=' * 78)
for t in sorted(lost_secs):
    print(f'  {t[:66]:68s} {sorted(set(lost_secs[t]))[0]}')

print()
print('=' * 78)
print(f'(5) BIBITEMS ABSENT: {len(lost_bibs)}')
print('=' * 78)
for b in sorted(lost_bibs):
    print(f'  {b:24s} {", ".join(sorted(set(lost_bibs[b]))[:2])}')

io.open(_p('tools/_cond.txt'), 'w', encoding='utf-8').write(
    '\n\n'.join(
        f'### [{raw}]  src={base}  {sw}w vs {cw}w\n'
        f'--- SOURCE PROOF ---\n{sp.strip()}\n'
        f'--- DELIVERABLE PROOF ---\n{cp.strip()}'
        for (n, raw), (base, sw, cw, sp, cp) in cond_proof.items()))
print()
print('full proof texts written to tools/_cond.txt')
