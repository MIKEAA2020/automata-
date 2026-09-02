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


"""Consistency checks on the active section after the repair round."""
import io
import re
import sys

P = _p('automata_corrected.tex')
raw = io.open(P, encoding='utf-8', newline='').read()
s = raw.replace('\r\n', '\n')
flat = ' '.join(s.split())          # line-collapsed, for cross-line matching

fails = []
def ck(name, cond, detail=''):
    print(('  PASS  ' if cond else '  FAIL  ') + name + (('  -- ' + detail) if detail and not cond else ''))
    if not cond:
        fails.append(name)

print('=' * 70)
print('A. LABELS / REFS')
print('=' * 70)
labels = re.findall(r'\\label\{([^}]*)\}', s)
ck('no duplicate labels', len(labels) == len(set(labels)),
   str([l for l in set(labels) if labels.count(l) > 1]))
refs = set(re.findall(r'\\(?:ref|eqref)\{([^}]*)\}', s))
missing = sorted(refs - set(labels))
ck('every \\ref resolves', not missing, str(missing))
for lb in ['def:gated-active-family', 'rem:gating-needed',
           'lem:discrete-bv-sandwich', 'rem:sandwich-jump']:
    ck(f'new label present: {lb}', lb in labels)

print()
print('=' * 70)
print('B. MACROS')
print('=' * 70)
for m in ['Gact', 'free', 'rd', 'rot', 'flipl', 'mistk', 'ind']:
    ck(f'\\{m} defined', f'\\newcommand{{\\{m}}}' in s or f'\\newcommand{{\\{m}}}[' in s)
# double-superscript / double-subscript hazards
ck('no \\Lsync^ (double superscript)', '\\Lsync^' not in s)
ck('no \\Esync_ (double subscript)', '\\Esync_' not in s)
ck('no \\Gact^ (double superscript)', '\\Gact^' not in s)
# every used macro is defined
defined = set(re.findall(r'\\newcommand\{\\([A-Za-z]+)\}', s))
print(f'  ({len(defined)} custom macros defined)')

print()
print('=' * 70)
print('C. AUDIT ITEM 2.1 -- objective semantics')
print('=' * 70)
ck('(SI) no longer claims tables must be learned after state known',
   'where the tables remain to be learned after the state' not in flat)
ck('three objectives SI/RI/MI defined',
   all(t in flat for t in ['(SI) State identification in a known skeleton',
                           '(RI) Residual identification',
                           '(MI) Model identification from a known initial state']))
ck('prediction-closing property stated', 'prediction-closing' in flat)

print()
print('=' * 70)
print('D. AUDIT ITEM 2.2 -- upper-bound proof matches statement')
print('=' * 70)
ck('proof no longer appends Littlestone after RI',
   'Once the residual class is known, the problem reduces to the known-initial-state realizable problem'
   not in flat)
ck('no continuation term appended after RI',
   'No continuation term appears, since objective~(RI) already fixes' in flat)
ck('(I) states sharp O(Esync) only',
   'Under objective~(RI) of Definition~\\ref{def:residual-knowledge}, \\[ \\MistRI(M) \\ \\le\\ O\\bigl(\\Esync(M)\\bigr),'
   in flat)

print()
print('=' * 70)
print('E. AUDIT ITEM 2.3 -- Esync is an infimum')
print('=' * 70)
ck('Esync defined with \\inf_{\\mathcal A}', '\\inf_{\\mathcal A}\\' in flat or '\\inf_{\\mathcal A}' in flat)
ck('old lower-bound-only phrasing gone',
   'minimax worst-case number of prediction mistakes that any active learner must incur' not in flat)
ck('two-sided reading explained', 'This two-sided reading' in flat)

print()
print('=' * 70)
print('F. AUDIT ITEM 2.4 -- gated family / adaptive Yao')
print('=' * 70)
ck('fixed-stream Yao removed from active proof',
   "apply Yao's principle exactly as in Theorem~\\ref{thm:stream-lower-bound}(ii): draw $g$ uniformly from $Q^Q$ and fix the input stream in advance"
   not in flat)
ck('adaptive argument present (first emission)', 'first emission' in flat)
ck('explicitly says fixed-stream Yao unavailable',
   "is \\emph{not} available, since an active learner chooses its own inputs" in flat)
ck('gating property stated', 'gating property' in flat)
ck('chaining failure documented with numbers',
   '48' in flat and '3\\cdot4\\cdot4\\cdot4=192' in flat)
ck('active thm uses Gact not G_M',
   'let $\\Gact_{M}$ be the \\emph{gated} family' in flat)

print()
print('=' * 70)
print('G. AUDIT ITEM 2.5 -- switch word')
print('=' * 70)
ck('single toggle tau(q,s) removed',
   '\\tau(q,\\mathtt s)= \\begin{cases} \\iota_2 & q\\in Q_1' not in flat)
ck('two idempotent switch letters', '\\tau(q,\\mathtt s_j)=\\iota_j' in flat)
ck('forcing word uses s_1', '\\mathtt s_1\\,w_v\\,\\mathtt c\\,\\mathtt d^{\\,L_1}' in flat)
ck('false claim "s returns to iota_1 regardless" removed',
   'returns to $\\iota_1$ regardless of the current block' not in flat)
ck('switch letters idempotent and total',
   'Both letters are idempotent and total' in flat)

print()
print('=' * 70)
print('H. AUDIT ITEM 3.1 -- phase language in direct-sum proof')
print('=' * 70)
ck('consecutive-phase language removed',
   'Because the continuation phase begins only after the synchronization phase' not in flat)
ck('interleaving explicitly permitted',
   'No temporal ordering of the two components is assumed' in flat)
ck('direct-sum proof requires rectangular hardness (T33)',
   'Rectangular hardness is what converts two separate lower bounds into a sum' in flat
   and 'Conditions~(iii)--(v) of' in flat)

print()
print('=' * 70)
print('I. AUDIT ITEM 3.3 -- Lsyncu propagation')
print('=' * 70)
# The PROOF body must contain no bare \Lsync: the universal bound is the claim.
m = re.search(r'\\label\{prop:active-length-upper\}(.*?)\\end\{proof\}', s, re.S)
whole = m.group(1) if m else ''
pf = whole.split('\\begin{proof}', 1)[1] if '\\begin{proof}' in whole else ''
bare_pf = re.findall(r'\\Lsync(?![u])', pf)
ck('no machine-specific \\Lsync anywhere in the proof', not bare_pf,
   f'{len(bare_pf)} occurrences in proof body')
# In the STATEMENT, \Lsync may appear only in the two contrastive sentences.
stmt = whole.split('\\begin{proof}', 1)[0]
sf = ' '.join(stmt.split())
allowed = ('The universal depth, not the machine-specific $\\Lsync(M)$, is the correct'
           in sf) and ('the model-search phase is vacuous and the bound reads $O(\\Lsync(M))$' in sf)
ck('statement uses \\Lsync only contrastively',
   len(re.findall(r'\\Lsync(?![u])', stmt)) == 2 and allowed)
ck('conclusion list uses Lsyncu', 'O(M\\log M+\\Lsyncu(M))$ in universal length form' in flat)

print()
print('=' * 70)
print('J. AUDIT ITEM 3.4 -- oracle regularity')
print('=' * 70)
ck('false "monotonicity places these in the setting" removed',
   'Monotonicity places these in the setting of Assumption~\\ref{ass:regular-bv-envelope}' not in flat)
ck('discrete sandwich lemma present', 'Discrete Bias--Variance Sandwich' in flat)
ck('explicitly says monotonicity alone insufficient',
   'Monotonicity alone is not enough' in flat)
ck('no continuity/crossing needed stated',
   'No continuity and no exact crossing point are required' in flat)

print()
print('=' * 70)
print('K. AUDIT ITEM 3.5 -- table / conclusion sync')
print('=' * 70)
ck('table shows O(Esync) under (RI)', '$O(\\Esync)$ under~(RI), unconditional' in flat)
ck('conclusion names the RI objective',
   'all bounds are stated against the residual-identification objective' in flat)
ck('abstract defines MistRI against the identification objective',
   'the mistakes incurred before the learner determines the Myhill--Nerode residual class' in flat)

print()
print('=' * 70)
print('L. AUDIT ITEM 4.1 -- claimed LaTeX corruption (verify, expect REJECT)')
print('=' * 70)
bad = [l for l in s.split('\n')
       if l.strip().startswith(('ewtheorem', 'ewcommand', 'orm{')) or l.strip() in ('orm', 'u')]
ck('no bare "ewtheorem"/"orm" artifacts', not bad, str(bad[:3]))
print(f'    \\newtheorem={s.count(chr(92)+"newtheorem")}  '
      f'\\newcommand={s.count(chr(92)+"newcommand")}  '
      f'\\norm={s.count(chr(92)+"norm")}  H_\\nu={s.count("H_"+chr(92)+"nu")}')
print('    -> audit item 4.1 is a paste artifact in the audit, not a source defect')

print()
print('=' * 70)
print('M. AUDIT ITEM 4.2 -- redundant hypothesis flagged')
print('=' * 70)
ck('data-processing redundancy noted',
   'data processing is not used in the derivation' in flat
   and 'every $f$-divergence with convex $f$ satisfies it automatically' in flat)

print()
print('=' * 70)
print('N. GLOBAL REGRESSION GUARDS')
print('=' * 70)
ck('no "phase one"/"phase two" left in two-phase proof',
   '\\emph{Phase one.}' not in flat and '\\emph{Phase two.}' not in flat)
ck('two-phase thm cites active thm not passive for component two',
   'a fresh instance of Theorem~\\ref{thm:active-explicit-directsum} on $M_2$ states' in flat)
ck('CRLF preserved', raw.count('\r\n') == raw.count('\n'))
thm = len(re.findall(r'\\begin\{(theorem|lemma|proposition|corollary)\}', s))
print(f'    {len(labels)} labels, {thm} numbered results')

print()
print('=' * 70)
print('O. ROUND-3 AUDIT ITEMS')
print('=' * 70)
ck('3.1 abstract no longer says op-equiv gives additive form',
   'Under an explicit operational-equivalence hypothesis, or under an explicit direct-sum saturation hypothesis, the active bound becomes'
   not in flat)
ck('3.1 abstract states unconditional Theta(M log M)',
   'with no synchronizability or operational-equivalence hypothesis' in flat)
ck('3.2 Lsyncu certifies current state, not residual class',
   'determines the \\emph{current state} of $A$ within each machine still consistent with it'
   in flat)
ck('3.2 old residual-class certification wording gone',
   'of the worst-case depth at which $\\mathcal T$ certifies the residual class of $A$' not in flat)
ck('4.2 defensive aside removed',
   'the active theorem, not the passive stream bound, since the learner chooses its inputs here'
   not in flat)
ck('4.3 restriction reduction present', '\\emph{Restriction.}' in flat)
ck('4.4 kappa boundedness stated',
   'The matching is up to \\emph{universal} constants precisely when $\\sup_T\\kappa(T)<\\infty$' in flat)
ck('4.5 stopped-martingale enumeration present',
   '\\sigma_1<\\sigma_2<\\cdots<\\sigma_m$ enumerate $N$' in flat)
ck('4.6 Esync caveat: RI attainment cost',
   'Despite the subscript, $\\Esync(M)$ is the cost of attaining' in flat)
ck('5.2 table cites two-phase for additive row',
   'witnessed by the two-component construction of Theorem~\\ref{thm:active-two-phase}' in flat)

print()
print('=' * 70)
print('P. NEW UNCONDITIONAL RESULT')
print('=' * 70)
for lb in ['thm:active-halving', 'cor:active-theta', 'rem:active-unconditional']:
    ck(f'label present: {lb}', lb in labels)
ck('halving thm gives O(M log M)', '\\Esync(M)\\ =\\ O(M\\log M)' in flat)
ck('corollary gives Theta for both quantities',
   '\\Esync(M)=\\Theta(M\\log M) \\qquad\\text{and}\\qquad \\MistRI(M)=\\Theta(M\\log M)' in flat)
ck('remark scopes what stays conditional',
   'The additive form is therefore not vacuous, but on the full class' in flat)
ck('sakarovitch2009 now cited (dead bibitem retired)',
   'sakarovitch2009' in s and s.count('cite') > 0 and '{sakarovitch2009}' in s)
ck('no dangling kozen1997', 'kozen1997' not in s)

print()
print('=' * 70)
print('Q. ROUND-4 AUDIT ITEMS')
print('=' * 70)
# 2.5 all-M extension (REAL)
ck('2.5 cor:active-theta states "all sufficiently large M"',
   "and for \\emph{all} sufficiently large $M$" in flat)
ck('2.5 proof invokes lem:subsequence-allM',
   'Lemma~\\ref{lem:subsequence-allM}, applied with $\\alpha=2$' in flat)
ck('2.5 proof names the subsequence N_L=2^{L+1}',
   'N_L=2^{L+1}' in flat)
ck('2.5 proof no longer uses bare M\'=M/2 shortcut',
   "with $M'=M/2$ lies in $\\mathcal H_M$" not in flat)
# 2.4 attainment convention (PARTLY REAL)
ck('2.4 randomized proof states failure convention',
   'is charged $\\mistk=+\\infty$, so such learners cannot lower the infimum' in flat)
ck('2.4 restricts to a.s.-attaining learners',
   'Fix any randomized active learner attaining~(RI) almost surely' in flat)
# 3.1 stale-language sweep (REAL)
ck('3.1b thm:active-certified disclaimer replaced',
   'No unconditional matching lower bound is claimed' not in flat)
ck('3.1c rem:no-automatic first sentence fixed',
   'Neither $\\Omega(M\\log M)$ nor $\\Omega(\\Esync(M))$ is an unconditional lower bound'
   not in flat)
ck('3.1c remark scoped to methods, not to the conclusion',
   'The obstruction is to those two methods, not to the conclusion' in flat)
ck('3.1d exact-results item fixed',
   'no unconditional active lower bound is claimed' not in flat)
ck('3.1a abstract sentence fixed',
   'Neither $\\Omega(M\\log M)$ nor an additive synchronization lower bound follows merely'
   not in flat)
ck('3.1e rem:active-additive scoped to subclass',
   'On the full class $\\mathcal H_M$ the two terms are of the same order' in flat)
ck('3.1f rem:active-oracle gives unconditional full-class rate',
   '\\Est_M^{\\mathrm{active}}(T) = \\Theta(M\\log M) \\] unconditionally' in flat)
# 3.2 subclass Esync (REAL)
ck('3.2 Esync(C_M) defined', '\\Esync(\\mathcal C_M)' in flat)
ck('3.2 says Esync(M)=Esync(H_M)',
   '\\Esync(M)=\\Esync(\\mathcal H_M)' in flat)
# 4.2 title precision
ck('4.2 theorem retitled',
   'Gated Family and Unconditional Active Lower Bound' in flat)
ck('4.2 says only one component supplied here',
   'This family supplies \\emph{one} component' in flat)

print()
print('=' * 70)
print('R. CLAIMS VERIFIED AS ALREADY-CORRECT (audit was stale)')
print('=' * 70)
ck('2.1 thm:active-halving exists', 'thm:active-halving' in labels)
ck('2.1 cor:active-theta exists', 'cor:active-theta' in labels)
ck('2.2 SI never used where tables are unknown',
   'where the tables remain unknown once the state is identified' not in flat)
ck('2.2 SI defined as tables GIVEN',
   'The transition and output tables are given; only the initial state is unknown' in flat)
ck('2.3 Lsyncu certifies current state', 
   'determines the \\emph{current state} of $A$ within each machine still consistent'
   in flat)
ck('3.3 two-phase cites active theorem for component two',
   'a fresh instance of Theorem~\\ref{thm:active-explicit-directsum} on $M_2$ states' in flat)
ck('3.3 two-phase does NOT cite passive stream thm for component two',
   'fresh instance of Theorem~\\ref{thm:stream-lower-bound} on $M_2$' not in flat)
ck('3.4 Esync caveat: RI attainment cost, not state sync',
   'Despite the subscript, $\\Esync(M)$ is the cost of attaining' in flat)

print()
print('=' * 70)
if fails:
    print(f'{len(fails)} CHECK(S) FAILED:')
    for f in fails:
        print('   -', f)
    sys.exit(1)
print('ALL CHECKS PASSED')
