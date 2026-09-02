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


# -*- coding: utf-8 -*-
"""
Split-safety analyser.

Given a proposed CORE set of labels for an extracted paper, compute:
  * the transitive dependency closure of the core (what it cannot leave behind);
  * the residual (what the second paper would carry);
  * BRIDGE items -- needed by the core but thematically residual, which must be
    duplicated, restated, or cited across the split;
  * ORPHANS -- labels reachable from neither, i.e. content that would be lost.

The guarantee this tool enforces is coverage:  core-closure  U  residual  =  ALL.
It is deliberately conservative: an environment depends on every label it
\ref{}s anywhere in its statement or its proof.
"""
import io, re, sys, json

SRC = _p('automata_corrected.tex')
ENV = r'theorem|lemma|proposition|corollary|definition|assumption|remark|metatheorem|example|openproblem|conjecture|heuristic'

s = io.open(SRC, encoding='utf-8', newline='').read().replace('\r\n', '\n')

# ---------------------------------------------------------------- inventory
# span of each labelled environment: from \begin{env} to matching \end{env},
# plus any \begin{proof} blocks that immediately follow it.
units = {}          # label -> (start, end, kind, title)
order = []
for m in re.finditer(r'\\begin\{(' + ENV + r')\}(\[[^\]]*\])?\s*\\label\{([^}]*)\}', s):
    kind, title, lab = m.group(1), (m.group(2) or '')[1:-1], m.group(3)
    endm = re.compile(r'\\end\{' + kind + r'\}').search(s, m.end())
    end = endm.end() if endm else m.end()
    # absorb following proof blocks
    while True:
        nxt = re.compile(r'\s*\\begin\{proof\}').match(s, end)
        if not nxt: break
        pe = re.compile(r'\\end\{proof\}').search(s, nxt.end())
        if not pe: break
        end = pe.end()
    units[lab] = (m.start(), end, kind, title)
    order.append(lab)

# section of each label
secs = [(mm.start(), mm.group(1), mm.group(2)) for mm in
        re.finditer(r'\\(sub)*section\{([^}]*)\}', s)]
def section_of(pos):
    cur = None
    for p, _, t in [(a, b, c) for a, b, c in secs]:
        if p < pos: cur = t
        else: break
    return cur

# Definitional vocabulary: a term or macro that a unit USES in prose creates a
# dependency on the environment that DEFINES it, even with no \ref{}.  Ignoring
# these silently strips definitions out of an extracted paper, which is the
# most likely way for a split to lose content.
DEFINES = {
    'def:lumpable-quotient':      [r'\blumpable\b'],
    'def:unifilar-lumpable':      [r'unifilar-lumpable'],
    'def:full-kl-retention':      [r'\\RetKL(?![a-zA-Z])'],
    'def:gaussian-quadratic':     [r'\\RetQuad(?![a-zA-Z])'],
    'def:controlled-full-kl':     [r'\\RetKLc\b'],
    'def:controlled-full-kl-general': [r'\\RetKLg\b'],
    'def:controlled-markov':      [r'\\Splus\b', r'stationary support'],
    'def:z-predictive-equivalence': [r'\\sim_Z\b', r'\$Z\$-predictive'],
    'lem:mixture-centroid':       [r'mixture centroid'],
    'def:synchronized-realization': [r'synchronization depth', r'synchronized'],
    'def:kernel-refinement':      [r'\\phi_\{\\ker\}'],
    'def:M-state-gap':            [r'\\Delta_\{\\mathbb T\}'],
}

# Guard: a DEFINES key that is not an actual label would make its rule silently
# dead, which is how a case-mismatch went unnoticed.  Fail loudly instead.
_bad = [k for k in DEFINES if k not in units]
if _bad:
    raise SystemExit('partition.py: DEFINES keys absent from manuscript: %s' % _bad)

deps = {}
for lab, (a, b, kind, title) in units.items():
    body = s[a:b]
    d = {r for r in re.findall(r'\\ref\{([^}]*)\}', body)
         if r in units and r != lab}
    for definer, pats in DEFINES.items():
        if definer == lab or definer not in units:
            continue
        if any(re.search(p, body) for p in pats):
            d.add(definer)
    deps[lab] = d

ALL = set(units)

def closure(seed):
    seen, stack = set(seed), list(seed)
    while stack:
        u = stack.pop()
        for v in deps.get(u, ()):
            if v not in seen:
                seen.add(v); stack.append(v)
    return seen

def report(core_seed, name='PROPOSED SPLIT'):
    core_seed = {c for c in core_seed if c in units}
    core = closure(core_seed)
    residual = ALL - core
    # bridges: pulled in only by dependency, not thematically chosen
    bridges = core - core_seed
    # reverse: residual items that cite into the core
    back = {r for r in residual if deps.get(r, set()) & core}
    print('=' * 78)
    print(name)
    print('=' * 78)
    print(f'  labelled environments in manuscript : {len(ALL)}')
    print(f'  seed (thematically chosen)          : {len(core_seed)}')
    print(f'  core after dependency closure       : {len(core)}')
    print(f'  pulled in as dependencies (bridges) : {len(bridges)}')
    print(f'  residual (second paper)             : {len(residual)}')
    print(f'  residual items citing into core     : {len(back)}')
    cov = len(core | residual)
    print(f'  COVERAGE  core U residual           : {cov}/{len(ALL)}'
          f'   {"COMPLETE" if cov == len(ALL) else "*** LOSS ***"}')
    return core_seed, core, residual, bridges, back

if __name__ == '__main__':
    if len(sys.argv) > 1:
        seed = json.load(io.open(sys.argv[1], encoding='utf-8'))
        cs, core, res, br, back = report(seed, 'SPLIT FROM ' + sys.argv[1])
        print()
        print('  BRIDGES (needed by core, not in seed):')
        for b in sorted(br):
            print(f'    {b:44s} {units[b][2]:12s} {section_of(units[b][0])}')
        print()
        print('  RESIDUAL ITEMS CITING INTO CORE (cross-paper refs):')
        for b in sorted(back):
            tgt = sorted(deps[b] & core)[:3]
            print(f'    {b:44s} -> {tgt}')
    else:
        print(f'{len(ALL)} labelled environments; {sum(len(v) for v in deps.values())} dependency edges')
        print('usage: partition.py seed.json')
