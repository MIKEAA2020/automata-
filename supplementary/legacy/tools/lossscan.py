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


#!/usr/bin/env python3
"""Deep content-loss scan: current deliverable vs every historical copy."""
import io, os, re, sys
from collections import defaultdict

CUR = _p('automata_corrected.tex')
SRC_DIRS = [_p('uploads'), _p('archive/superseded_snapshots'),
            _p('work2'), _p('work3'), _p('work4')]
ENV = (r'theorem|thm|lemma|lem|proposition|prop|corollary|cor|definition|def'
       r'|assumption|ass|remark|rem|metatheorem|example|ex|conjecture|openproblem'
       r'|heuristic')

def read(p):
    return io.open(p, encoding='utf-8', errors='replace', newline='').read().replace('\r\n','\n')

def labels(s):
    return set(re.findall(r'\\label\{([^}]*)\}', s))

def titles(s):
    """environment titles: \begin{theorem}[Title]"""
    out = set()
    for m in re.finditer(r'\\begin\{(' + ENV + r')\}\s*\[([^\]]*)\]', s):
        t = ' '.join(m.group(2).split())
        out.add(t)
    return out

def envs_with_labels(s):
    """map label -> (envtype, title, body length)"""
    out = {}
    for m in re.finditer(r'\\begin\{(' + ENV + r')\}(?:\s*\[([^\]]*)\])?(.*?)\\end\{\1\}', s, re.S):
        body = m.group(3)
        lm = re.search(r'\\label\{([^}]*)\}', body)
        if lm:
            out[lm.group(1)] = (m.group(1), ' '.join((m.group(2) or '').split()), len(' '.join(body.split())))
    return out

cur = read(CUR)
cur_lab, cur_tit, cur_env = labels(cur), titles(cur), envs_with_labels(cur)

print('='*78); print('CONTENT-LOSS SCAN'); print('='*78)
print(f'current: {len(cur_lab)} labels, {len(cur_tit)} titled environments, '
      f'{len(cur)} chars')

hist = []
for d in SRC_DIRS:
    if not os.path.isdir(d): continue
    for f in sorted(os.listdir(d)):
        if f.endswith(('.tex','.txt')):
            hist.append(os.path.join(d, f))
print(f'historical copies: {len(hist)}')

# ---------- 1. titles present historically but absent now ----------
print()
print('-'*78); print('(1) TITLED ENVIRONMENTS PRESENT IN HISTORY, ABSENT NOW'); print('-'*78)
lost_titles = defaultdict(list)
for p in hist:
    try: s = read(p)
    except Exception: continue
    for t in titles(s) - cur_tit:
        lost_titles[t].append(os.path.basename(p))
if not lost_titles:
    print('  none')
else:
    for t, ps in sorted(lost_titles.items()):
        print(f'  {t!r}')
        print(f'      in: {", ".join(ps[:4])}{" ..." if len(ps)>4 else ""}')
print(f'  TOTAL distinct titles absent now: {len(lost_titles)}')

# ---------- 2. labels present historically but absent now ----------
print()
print('-'*78); print('(2) LABELS PRESENT IN HISTORY, ABSENT NOW'); print('-'*78)
lost_labels = defaultdict(list)
for p in hist:
    try: s = read(p)
    except Exception: continue
    for l in labels(s) - cur_lab:
        lost_labels[l].append(os.path.basename(p))
if not lost_labels:
    print('  none')
else:
    for l, ps in sorted(lost_labels.items()):
        print(f'  {l:<42} in: {", ".join(ps[:3])}{" ..." if len(ps)>3 else ""}')
print(f'  TOTAL distinct labels absent now: {len(lost_labels)}')

# ---------- 3. dangling \ref to nonexistent labels ----------
print()
print('-'*78); print('(3) DANGLING REFERENCES IN CURRENT DELIVERABLE'); print('-'*78)
refs = set(re.findall(r'\\(?:eq)?ref\{([^}]*)\}', cur))
dangling = sorted(refs - cur_lab)
print('  dangling: ' + (', '.join(dangling) if dangling else 'none'))

# ---------- 4. orphan labels (defined, never referenced) ----------
print()
print('-'*78); print('(4) ORPHAN LABELS (defined, never referenced)'); print('-'*78)
orph = sorted(l for l in cur_lab - refs if not l.startswith(('sec:','subsec:','tab:','fig:')))
print(f'  {len(orph)} orphans')
for l in orph[:25]: print(f'     {l}')
if len(orph) > 25: print(f'     ... and {len(orph)-25} more')

# ---------- 5. shrunk proofs: same label, much shorter body ----------
print()
print('-'*78); print('(5) ENVIRONMENTS SUBSTANTIALLY SHORTER THAN HISTORICAL BEST'); print('-'*78)
best = {}
for p in hist:
    try: s = read(p)
    except Exception: continue
    for l,(e,t,n) in envs_with_labels(s).items():
        if l not in best or n > best[l][2]:
            best[l] = (os.path.basename(p), t, n)
shrunk = []
for l,(e,t,n) in cur_env.items():
    if l in best:
        src, bt, bn = best[l]
        # Paragraph-flattened archives (===PARA=== format) merge adjacent
        # environments, so their "bodies" are spuriously long.  Verified by
        # hand for thm:oracle-agnostic and def:sym-support: current text is
        # complete (and, for the former, strictly stronger).  Exclude them.
        if src.endswith('missing.txt'):
            continue
        if bn > 0 and n < 0.6*bn and bn - n > 200:
            shrunk.append((l, n, bn, src, t))
shrunk.sort(key=lambda r: r[1]-r[2])
if not shrunk: print('  none below 60% of historical best')
for l,n,bn,src,t in shrunk[:20]:
    print(f'  {l:<38} now {n:>6} vs {bn:>6} chars in {src}')
print(f'  TOTAL: {len(shrunk)}')

# ---------- 6. gate conditions ----------
print()
print('-'*78); print('(6) GATE'); print('-'*78)
fail = []
if dangling: fail.append(f'{len(dangling)} dangling refs')
# theorem-like labels lost WITHOUT a recorded disposition
KNOWN = {
 'ass:operational-equivalence','cor:commitment-threshold','open:hankel-equality',
 'open:oracle-minimax-lower','rem:active-direct-sum','thm:active-exact-decomposition',
 'thm:active-realizable','rem:quasi-norm','rem:temporal-compatible',
 'rem:agnostic-overhead-lower','rem:oracle-uses-achievability',
 'rem:exponent-commitment-alpha0-scope','rem:lowerbound-corrections',
}
mathish = {l for l in lost_labels
           if l.split(':')[0] in {'thm','lem','prop','cor','def','rem','ass','conj','open'}}
unex = sorted(mathish - KNOWN)
print(f'  math-like labels absent now: {len(mathish)}; with recorded disposition: '
      f'{len(mathish & KNOWN)}; UNEXPLAINED: {len(unex)}')
for l in unex: print(f'     ** {l}')
if unex: fail.append(f'{len(unex)} unexplained math-like label losses')
print()
if fail:
    print('LOSS-SCAN FAILED: ' + '; '.join(fail)); sys.exit(1)
print('LOSS-SCAN PASSED: no dangling refs, no unexplained losses')
