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

"""Convention-flip audit: singular/eigenvalue tail indices vs rank budgets.

Two DIFFERENT and both-correct conventions coexist in this manuscript:

  (G) Grounding / Hankel:  budget M  ->  rank <= M      ->  tail sigma_{M+1}
  (R) Retention / ANOVA:   budget M  ->  rank <= M-1    ->  tail sum_{i>=M}

They differ because centring removes one degree of freedom in (R): the M
block centroids satisfy one affine relation, so rank(B_phi) <= M-1.

A FLIP is an occurrence of one convention's tail paired with the other's
rank budget.  This script flags every co-occurrence for inspection.
"""
import io, re, sys

s = io.open(_p('automata_corrected.tex'), encoding='utf-8',
            newline='').read().replace('\r\n', '\n')
lines = s.split('\n')
flat = ' '.join(s.split())

fails, notes = [], []

def ck(name, cond, detail=''):
    if cond:
        print(f'  PASS  {name}')
    else:
        print(f'  FAIL  {name}' + (f'  -- {detail}' if detail else ''))
        fails.append(name)

print('=' * 74)
print('CONVENTION AUDIT: rank budgets vs spectral-tail indices')
print('=' * 74)

# --- 1. Grounding side: sigma_{M+1} must always pair with rank <= M ---
print('\n(G) Grounding / Hankel  --  expect  rank<=M  with  sigma_{M+1}')
ck('Dunres defined with rank<=M',
   r'\Dunres(M) = \inf_{\operatorname{rank}B\le M}' in flat)
ck('Dunres equals sigma_{M+1}',
   r'\Dunres(M) = \sigma_{M+1}(H_\nu)' in flat)
ck('DHankstr uses rank<=M under Hankel constraint',
   r'\operatorname{rank}B\le M\\ B\ \text{Hankel}' in flat)
ck('no sigma_M tail anywhere (would be the flipped form)',
   not re.search(r'\\sigma_\{M\}\(H', s), 'found sigma_M(H...)')
ck('no sigma_{M-1} tail anywhere',
   not re.search(r'\\sigma_\{M-1\}', s))

# --- 2. Retention side: sum_{i>=M} must pair with rank <= M-1 ---
print('\n(R) Retention / ANOVA  --  expect  rank<=M-1  with  sum_{i>=M}')
ck('rank(B_phi) <= M-1 stated in simplex converse',
   r'\rank(B_\phi)\le M-1' in flat)
ck('Ky Fan sums to M-1',
   r'\sum_{i=1}^{M-1} \lambda_i' in flat or r'\sum_{i=1}^{M-1}\lambda_i' in flat)
# sum_{i>M} is CORRECT for the grounding/Hankel spectrum (sigma_i, rank<=M)
# and WRONG for the retention spectrum (lambda_i(Sigma), rank<=M-1).
# Distinguish by which spectrum the tail indexes.
bad_tail = []
for m in re.finditer(r'\\sum_\{i>M\}', s):
    ctx = ' '.join(s[m.start():m.start()+140].split())
    pre = ' '.join(s[max(0,m.start()-60):m.start()].split())
    tail_ctx = pre.rstrip()
    negated = (tail_ctx.endswith('not') or tail_ctx.endswith('not $')
               or 'Writing the retention tail as' in pre)
    if '\\lambda_i' in ctx and not negated:
        bad_tail.append(ctx[:80])
ck('no sum_{i>M} over the RETENTION spectrum lambda_i (grounding sigma_i is fine)',
   not bad_tail, '; '.join(bad_tail))
ck('index convention explicitly defended',
   'not $\\sum_{i>M}$: the effective rank is $M-1$' in flat)
ck('effective rank budget M-1 recorded in schema',
   'their effective rank budgets are \\[ M, \\qquad M-1, \\qquad M, \\]' in flat)

# --- 3. Cross-regime: the two must never be silently equated ---
print('\n(X) Cross-regime hygiene')
ck('schema warns budgets differ across regimes',
   'does not unify the operators, the effective rank budgets' in flat)
ck('retention listed as M-1 in the epistemic summary',
   'retention uses the effective rank $M-1$' in flat)

# --- 4. Kronecker / degree wording ---
print('\n(K) Kronecker degree wording')
n_mcm = len(re.findall(r'McMillan', s))
print(f'       "McMillan" occurrences: {n_mcm}')
print('       NOTE: Peller (MSRI survey) writes deg P_-phi, never "McMillan".')
print('       deg r := max(deg p, deg q) in lowest terms = sum of pole')
print('       multiplicities INCLUDING a possible pole at infinity.')
if n_mcm:
    notes.append(f'{n_mcm} "McMillan" uses -- consider Peller wording deg P_-phi')

# --- 5. Report every line where a tail index and a rank budget co-occur ---
print('\n(Co-occurrence scan: lines carrying both a tail and a rank budget)')
hits = 0
for i, L in enumerate(lines, 1):
    has_sig = re.search(r'\\sigma_\{M\+1\}', L)
    has_tail = re.search(r'\\sum_\{i\\ge M\}', L)
    has_rM = re.search(r'rank\}?B?\\le M(?!-)', L) or re.search(r'\\rank\(B[^)]*\)\\le M(?!-)', L)
    has_rM1 = re.search(r'\\le M-1', L)
    if (has_sig and has_rM1) or (has_tail and has_rM and not has_rM1):
        print(f'  *** POSSIBLE FLIP  L{i}: {L.strip()[:90]}')
        hits += 1
if not hits:
    print('  none -- no line pairs a tail index with the opposite rank budget')

print('\n' + '=' * 74)
if fails:
    print(f'{len(fails)} CONVENTION FAILURE(S)')
    for f in fails: print('   -', f)
    sys.exit(1)
print('CONVENTIONS CONSISTENT: (G) and (R) each internally coherent, not conflated')
for n in notes: print('NOTE:', n)
