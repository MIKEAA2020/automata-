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


"""Proof-dependency graph: does any proof cite a result proved later, cyclically?"""
import io
import re
import sys

s = io.open(_p('automata_corrected.tex'), encoding='utf-8',
            newline='').read().replace('\r\n', '\n')

ENV = r'theorem|lemma|proposition|corollary|definition|assumption|remark|metatheorem'

# position of each label
labpos = {}
for m in re.finditer(r'\\label\{([^}]*)\}', s):
    labpos[m.group(1)] = m.start()

# proofs and what they cite
edges = []
for m in re.finditer(r'\\begin\{proof\}(\[[^\]]*\])?(.*?)\\end\{proof\}', s, re.S):
    body, start = m.group(2), m.start()
    # A named proof "\begin{proof}[Proof of X~\ref{lab}]" belongs to lab,
    # regardless of what environment happens to precede it.
    named = None
    if m.group(1):
        nm = re.search(r'\\ref\{([^}]*)\}', m.group(1))
        if nm:
            named = nm.group(1)
    # owning label = the label of the nearest preceding THEOREM-LIKE environment
    # (a \label inside a later remark must not capture an earlier proof)
    owner = None
    best = -1
    for em in re.finditer(r'\\begin\{(' + ENV + r')\}(?:\[[^\]]*\])?\s*\\label\{([^}]*)\}', s):
        if em.start() < start and em.start() > best:
            best, owner = em.start(), em.group(2)
    if named:
        owner = named
    if owner is None:
        continue
    for r in set(re.findall(r'\\ref\{([^}]*)\}', body)):
        if r in labpos:
            edges.append((owner, r))

# cycle detection on the "cites" relation
adj = {}
for a, b in edges:
    adj.setdefault(a, set()).add(b)

WHITE, GREY, BLACK = 0, 1, 2
color = {}
cycles = []


def dfs(u, stack):
    color[u] = GREY
    stack.append(u)
    for v in adj.get(u, ()):
        if color.get(v, WHITE) == GREY:
            cycles.append(stack[stack.index(v):] + [v])
        elif color.get(v, WHITE) == WHITE:
            dfs(v, stack)
    stack.pop()
    color[u] = BLACK


sys.setrecursionlimit(100000)
for n in list(adj):
    if color.get(n, WHITE) == WHITE:
        dfs(n, [])

print(f'{len(labpos)} labels, {len(edges)} proof->result citation edges')
if cycles:
    print(f'{len(cycles)} CYCLE(S):')
    for c in cycles[:10]:
        print('   ', ' -> '.join(c))
    sys.exit(1)
print('proof-dependency graph is ACYCLIC')

# forward references from within proofs (legal but worth counting)
fwd = [(a, b) for a, b in edges if labpos[b] > labpos[a]]
print(f'{len(fwd)} forward references from inside proofs')
for a, b in sorted(fwd)[:12]:
    print(f'    {a}  ->  {b}')
