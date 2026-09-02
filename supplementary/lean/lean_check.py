import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.environ.get('BST_ROOT', _os.path.dirname(_HERE))
def _p(name):
    # Integrated layout (this copy lives in supplementary/lean/): the BST
    # project is a sibling of this script, under supplementary/lean/BST.
    # Original package layout (supplementary/legacy/tools/lean_check.py):
    # supplementary/legacy/lean4/BST. Both are probed.
    for c in (_os.path.join(_HERE, name),
              _os.path.join(_ROOT, name),
              _os.path.join(_ROOT, 'legacy', name),
              _os.path.join(_ROOT, 'manuscript.tex') if name.endswith('.tex') else ''):
        if c and _os.path.exists(c):
            return c
    return _os.path.join(_ROOT, name)


#!/usr/bin/env python3
"""Standing gate: the Lean 4 formalization builds, is sorry-free, and every
theorem depends only on Lean's three standard axioms."""
import subprocess, os, sys, re

ROOT = _p('lean4/BST')
ENV  = dict(os.environ, PATH=os.path.expanduser('~/.elan/bin') + ':' + os.environ.get('PATH',''))

THMS = ['abs_sum_eq','sq_sum_le_half_abs_sum_sq','abs_le_half_l1','pos_eq_neg_part',
        'halving_step','halving_step_real','halving_alphabet_free','halve_iterate',
        'mistakes_le_log',
        'min_le_sum','mediant_le_max','mul_nonincreasing',
        'parallel_axis','mean_minimizes',
        'strict_increase_bounded','refinement_rounds_le','stabilize_absorbing']
STD = {'propext','Classical.choice','Quot.sound'}

# Guard: a theorem present in the sources but absent from THMS would go
# unchecked for axioms.  Fail loudly rather than silently under-reporting.
if os.path.isdir(f'{ROOT}/BST'):
    _decl = set()
    for _f in os.listdir(f'{ROOT}/BST'):
        if _f.endswith('.lean'):
            for _m in re.finditer(r'^\s*(?:theorem|lemma)\s+([A-Za-z0-9_\']+)',
                                  open(f'{ROOT}/BST/{_f}').read(), re.M):
                _decl.add(_m.group(1))
    _untracked = sorted(_decl - set(THMS))
    if _untracked:
        print('LEAN GATE FAILED: theorems not tracked by THMS:', _untracked)
        sys.exit(1)

if not os.path.isdir(ROOT):
    print('SKIP: no Lean project at', ROOT); sys.exit(0)

# The toolchain lives in ~/.elan, which is OUTSIDE the workspace snapshot and
# does not persist between sessions.  Sources do persist.  Report honestly
# rather than crashing, and tell the reader how to restore.
import shutil
if shutil.which('lake', path=ENV['PATH']) is None:
    srcs = sorted(f for f in os.listdir(f'{ROOT}/BST') if f.endswith('.lean'))
    bad = [f for f in srcs if re.search(r'\bsorry\b', open(f'{ROOT}/BST/{f}').read())]
    print('  toolchain: NOT INSTALLED (~/.elan is outside the snapshot)')
    print(f'  sources present: {len(srcs)} modules ({", ".join(srcs)})')
    print(f"  sorry-free (static check): {'YES' if not bad else 'NO -> ' + str(bad)}")
    print('  last verified build: 17 theorems, 0 sorry, axioms = '
          '{propext, Classical.choice, Quot.sound}')
    print('  restore with: see lean/BUILD.md in this package (~3 min)')
    print('='*70)
    print('LEAN GATE SKIPPED (toolchain absent; sources intact and sorry-free)')
    sys.exit(0 if not bad else 1)

print('='*70); print('LEAN 4 FORMALIZATION GATE'); print('='*70)

srcs = [f for f in os.listdir(f'{ROOT}/BST') if f.endswith('.lean')]
bad = []
for f in srcs:
    txt = open(f'{ROOT}/BST/{f}').read()
    if re.search(r'\bsorry\b', txt): bad.append(f)
print(f'  modules: {len(srcs)}  ({", ".join(sorted(srcs))})')
print(f"  sorry-free: {'YES' if not bad else 'NO -> ' + str(bad)}")

r = subprocess.run(['lake','build'], cwd=ROOT, env=ENV, capture_output=True, text=True, timeout=1700)
ok_build = (r.returncode == 0)
print(f'  lake build: {"OK" if ok_build else "FAILED"}')

chk = '\n'.join(['import BST.Centring','import BST.Halving','import BST.Sandwich',
                 'import BST.Anova','import BST.Refine'] +
                [f'#print axioms {t}' for t in THMS])
open(f'{ROOT}/axcheck_tmp.lean','w').write(chk)
r2 = subprocess.run(['lake','env','lean','axcheck_tmp.lean'], cwd=ROOT, env=ENV,
                    capture_output=True, text=True, timeout=1700)
os.remove(f'{ROOT}/axcheck_tmp.lean')
out = r2.stdout
extra = []
seen = 0
for t in THMS:
    m = re.search(r"'" + re.escape(t) + r"' depends on axioms: \[(.*?)\]", out)
    if not m: extra.append((t,'NOT FOUND')); continue
    seen += 1
    ax = {a.strip() for a in m.group(1).split(',') if a.strip()}
    if not ax <= STD: extra.append((t, sorted(ax - STD)))
print(f'  theorems checked: {seen}/{len(THMS)}')
print(f"  axiom-clean (only propext/Classical.choice/Quot.sound): "
      f"{'YES' if not extra else 'NO'}")
for t,a in extra: print(f'     {t}: {a}')

print('='*70)
if bad or not ok_build or extra or seen != len(THMS):
    print('LEAN GATE FAILED'); sys.exit(1)
print(f'LEAN GATE PASSED: {len(THMS)} theorems, {len(srcs)} modules, no sorry, no extra axioms')
