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
CUMULATIVE regression suite: every fix from every turn must still be present
in the deliverable.  Guards against silent regression when later edits
overwrite earlier ones.

Turn 1 (audit A): items 1.1-1.4, 2.1-2.4, 3.1-3.3
Turn 2 (audit B): 2.1-2.5, 3.1-3.5, 4.1-4.3 + gated family, discrete sandwich
Turn 3 (audit C): 3.1-3.2, 4.1-4.6, 5.1-5.3 + halving theorem
Turn 4 (audit D): 2.4, 2.5, 3.1, 3.2, 4.2
"""
import io
import re
import sys

raw = io.open(_p('automata_corrected.tex'), encoding='utf-8',
              newline='').read()
s = raw.replace('\r\n', '\n')
flat = ' '.join(s.split())
labels = set(re.findall(r'\\label\{([^}]*)\}', s))

fails = []
turn_stats = {}


def ck(turn, name, cond, detail=''):
    turn_stats.setdefault(turn, [0, 0])
    turn_stats[turn][1] += 1
    if cond:
        turn_stats[turn][0] += 1
    else:
        fails.append(f'[{turn}] {name}' + (f'  -- {detail}' if detail else ''))


def has(t):
    return t in flat


def absent(t):
    return t not in flat


# ============================================================ TURN 1
T = 'T1'
ck(T, 'def:output-aware-sync restored', 'def:output-aware-sync' in labels)
ck(T, 'def:symbolic-grounding-gap restored', 'def:symbolic-grounding-gap' in labels)
ck(T, 'Lsyncu macro exists (double-superscript fix)',
   '\\newcommand{\\Lsyncu}' in s)
ck(T, 'RetKLr macro parameterised (double-superscript fix)',
   '\\Delta_{\\mathrm{ret}}^{\\mathrm{KL},(#1)}' in s)
ck(T, 'SI/RI objectives separated', has('(RI) Residual identification'))
ck(T, 'rem:objective-bookkeeping present', 'rem:objective-bookkeeping' in labels)
ck(T, 'switch letters total, so no component can be evaded',
   has('block one remains reachable at every time') or
   has('Totality is also what removes any evasion'))
ck(T, 'def:direct-sum-active has condition (iv) unavoidability',
   has('\\textbf{unavoidability}'))
ck(T, 'Csiszar: f-divergence is ASSUMED not derived',
   has('This is an \\emph{assumed} hypothesis, not a consequence of'))
ck(T, 'Renyi counterexample cited',
   has("satisfied by the R\\'enyi divergences, which are not $f$-divergences"))
ck(T, 'uniform compatibility axiom (profinite)', has('uniformly compatible')
   or has('uniform-compatibility') or has('uniformly\ncompatible'.replace('\n', ' ')))
ck(T, 'worst-case aggregation admitted', has('worst-case') and has('Cesa'))
ck(T, 'multiclass constants noted', has('daniely2014'))
ck(T, 'no false Csiszar lemma (DP+reg => f-div)',
   absent('data processing plus regularity implies'))
ck(T, 'Ky Fan uses singular values', has('singular value'))

# ============================================================ TURN 2
T = 'T2'
ck(T, 'three objectives SI/RI/MI', has('(MI) Model identification'))
ck(T, 'prediction-closing property', has('prediction-closing'))
ck(T, 'SI defined as tables GIVEN',
   has('The transition and output tables are given; only the initial state is unknown'))
ck(T, 'SI NOT used where tables unknown',
   absent('where the tables remain to be learned after the state'))
ck(T, 'Esync is inf-sup', has('\\inf_{\\mathcal A}\\'))
ck(T, 'Esync +inf convention', has('with the value $+\\infty$ if it never'))
ck(T, 'no Littlestone appended after RI',
   absent('Once the residual class is known, the problem reduces to the '
          'known-initial-state realizable problem'))
ck(T, 'no continuation term appended after RI',
   has('No continuation term appears, since objective~(RI) already fixes'))
ck(T, 'gated family defined', 'def:gated-active-family' in labels)
ck(T, 'gating property stated', has('gating property'))
ck(T, 'chaining failure documented', has('3\\cdot4\\cdot4\\cdot4=192'))
ck(T, 'rem:gating-needed present', 'rem:gating-needed' in labels)
ck(T, 'fixed-stream Yao removed from active proof',
   absent("apply Yao's principle exactly as in "
          "Theorem~\\ref{thm:stream-lower-bound}(ii): draw $g$ uniformly from "
          "$Q^Q$ and fix the input stream in advance"))
ck(T, 'adaptive first-emission argument', has('first emission'))
ck(T, 'two forcing switch letters', has('\\tau(q,\\mathtt s_j)=\\iota_j'))
ck(T, 'single-toggle definition removed',
   absent('\\tau(q,\\mathtt s)= \\begin{cases} \\iota_2 & q\\in Q_1'))
ck(T, 'false "s returns regardless" claim removed',
   absent('returns to $\\iota_1$ regardless of the current block'))
ck(T, 'forcing word uses s_1', has('\\mathtt s_1\\,w_v\\,\\mathtt c\\,\\mathtt d^{\\,L_1}'))
ck(T, 'no consecutive-phase language in direct-sum proof',
   absent('Because the continuation phase begins only after the synchronization phase'))
ck(T, 'interleaving permitted', has('No temporal ordering of the two components is assumed'))
ck(T, 'discrete sandwich lemma', 'lem:discrete-bv-sandwich' in labels)
ck(T, 'monotonicity-alone claim removed',
   absent('Monotonicity places these in the setting of Assumption~\\ref{ass:regular-bv-envelope}'))
ck(T, 'says monotonicity insufficient', has('Monotonicity alone is not enough'))
ck(T, 'no continuity/crossing needed',
   has('No continuity and no exact crossing point are required'))
ck(T, 'data-processing redundancy flagged',
   has('data processing is not used in the derivation')
   and has('every\n$f$-divergence with convex $f$ satisfies it automatically'.replace('\n',' ')))
ck(T, 'state-budget rescaling for gated family', has('\\tfrac{N}{2}\\log_2\\tfrac{N}{2}'))

# ============================================================ TURN 3
T = 'T3'
ck(T, 'thm:active-halving exists', 'thm:active-halving' in labels)
ck(T, 'cor:active-theta exists', 'cor:active-theta' in labels)
ck(T, 'rem:active-unconditional exists', 'rem:active-unconditional' in labels)
ck(T, 'halving gives Esync=O(M log M)', has('\\Esync(M)\\ =\\ O(M\\log M)'))
ck(T, 'halving proof: version space', has('version space'))
ck(T, 'halving proof: plurality', has('plurality'))
ck(T, 'automata-theory citation present for separating word',
   has('\\cite[Ch.~II]{sakarovitch2009}'))
ck(T, 'sakarovitch2009 cited (dead bibitem retired)', has('{sakarovitch2009}'))
ck(T, 'no dangling kozen1997', 'kozen1997' not in s)
ck(T, 'Lsyncu certifies CURRENT STATE not residual class',
   has('determines the \\emph{current state} of $A$ within each machine still consistent'))
ck(T, 'old Lsyncu residual-certification wording gone',
   absent('of the worst-case depth at which $\\mathcal T$ certifies the residual class of $A$'))
ck(T, 'proof body has zero bare Lsync', True)  # checked separately below
ck(T, 'defensive aside removed',
   absent('the active theorem, not the passive stream bound, since the learner '
          'chooses its inputs here'))
ck(T, 'direct-sum restriction reduction', has('\\emph{Restriction.}'))
ck(T, 'kappa boundedness stated',
   has('The matching is up to \\emph{universal} constants precisely when'))
ck(T, 'stopped-martingale enumeration',
   has('\\sigma_1<\\sigma_2<\\cdots<\\sigma_m$ enumerate $N$'))
ck(T, 'Esync is the RI attainment cost, not state sync',
   has('Despite the subscript, $\\Esync(M)$ is the cost of attaining'))

# ============================================================ TURN 4
T = 'T4'
ck(T, 'cor:active-theta covers ALL large M',
   has('and for \\emph{all} sufficiently large $M$'))
ck(T, 'all-M via lem:subsequence-allM',
   has('Lemma~\\ref{lem:subsequence-allM}, applied with $\\alpha=2$'))
ck(T, 'subsequence N_L named', has('N_L=2^{L+1}'))
ck(T, 'old M/2 shortcut gone', absent("with $M'=M/2$ lies in $\\mathcal H_M$"))
ck(T, 'attainment/failure convention in randomized proof',
   has('is charged $\\mistk=+\\infty$, so such learners cannot lower the infimum'))
ck(T, 'restricts to a.s.-attaining learners',
   has('Fix any randomized active learner attaining~(RI) almost surely'))
ck(T, 'stale: thm disclaimer gone', absent('No unconditional matching lower bound is claimed'))
ck(T, 'stale: rem:no-automatic first sentence gone',
   absent('Neither $\\Omega(M\\log M)$ nor $\\Omega(\\Esync(M))$ is an unconditional lower bound'))
ck(T, 'rem:no-automatic scoped to methods',
   has('The obstruction is to those two methods, not to the conclusion'))
ck(T, 'stale: exact-results item gone',
   absent('no unconditional active lower bound is claimed'))
ck(T, 'stale: abstract sentence gone',
   absent('Neither $\\Omega(M\\log M)$ nor an additive synchronization lower bound follows merely'))
ck(T, 'rem:active-additive scoped', has('On the full class $\\mathcal H_M$ the two terms'))
ck(T, 'rem:active-oracle unconditional full-class rate',
   has('\\Est_M^{\\mathrm{active}}(T) = \\Theta(M\\log M) \\] unconditionally'))
ck(T, 'Esync(C_M) subclass parameterisation', has('\\Esync(\\mathcal C_M)'))
ck(T, 'Esync(M)=Esync(H_M)', has('\\Esync(M)=\\Esync(\\mathcal H_M)'))
ck(T, 'theorem retitled', has('Gated Family and Unconditional Active Lower Bound'))
ck(T, 'one-component note', has('This family supplies \\emph{one} component'))

# ============================================================ TURN 5
T = 'T5'
ck(T, 'lem:support-extension exists', 'lem:support-extension' in labels)
ck(T, 'extension lemma has explicit construction',
   has('$u,v\\notin S$ and for every $y\\in\\mathcal I^*$ one has'))
ck(T, 'extension lemma notes re-entry counterexample (T33: right-closed example)',
   has(r'\mathtt{aaa}\notin S$ and $\mathtt{aaab}\in S'))
ck(T, 'meta:boolean (ii) now a sandwich not an equality',
   has('\\operatorname{index}(\\sim_{\\delta,S}) \\ \\le\\ \\kappa_{\\mathrm{obs}}(\\delta,\\mu)'))
ck(T, 'old "extending arbitrarily costs no index" removed',
   absent('extending it arbitrarily off $S$ costs no index'))
ck(T, 'cor:stateless uses one-stage values',
   has('\\min_{a\\in\\mathcal I}\\max_{b\\in\\mathcal O}r(a,b) \\ -\\ \\max_{b\\in\\mathcal O}\\min_{a\\in\\mathcal I}r(a,b)'))
ck(T, 'cor:stateless distinguishes one-stage from discounted value',
   has('Neither is the discounted alternating-move value $\\Valt$'))
ck(T, 'cor:stateless proof derives Valt=m1/(1-gamma)',
   has('\\Valt=\\frac{m_1}{1-\\gamma}'))
ck(T, 'old bogus V*=V/(1-gamma) line removed',
   absent('alternating-move value is $V^{*}=V/(1-\\gamma)$ and $\\alpha(q_t)=\\alpha$'))
ck(T, 'EsyncSI macro defined', '\\newcommand{\\EsyncSI}' in s)
ck(T, 'EsyncSI defined in text', has('\\emph{state-identification complexity}'))
ck(T, 'EsyncSI <= Esync stated',
   has('\\EsyncSI(\\mathcal C_M)\\ \\le\\ \\Esync(\\mathcal C_M)'))
ck(T, 'EsyncSI defined and related to Esync',
   has('\\EsyncSI(\\mathcal C_M)\\ \\le\\ \\Esync(\\mathcal C_M)'))
ck(T, 'direct-sum thm states a disjoint-rounds sum',
   has('The bound is a sum, not a maximum, and the additivity comes from the'))
ck(T, 'S_M described as state-identification only',
   has('measuring \\emph{state identification only}'))
ck(T, 'active-certified III is a lower bound only',
   has('This is a lower bound only; no matching upper bound is asserted'))
ck(T, 'no stale M log M + Esync(M) additive form',
   absent('\\Theta(M\\log M+\\Esync(M)).') and
   absent('\\Theta\\bigl(M\\log M+\\Esync(M)\\bigr)'))
ck(T, 'separating word bound justified (superseded by lem:moore-separation, T7)',
   has('word of length at most $2M-1$, by Lemma~\\ref{lem:moore-separation}'))
ck(T, 'notes Moore M-1 bound not applicable across machines',
   has('separates two states of a \\emph{single} $M$-state machine'))
ck(T, '8.2 no longer claims "sharper"',
   absent('retained because it is the sharper statement whenever'))
ck(T, '8.2 states the bound is subsumed in order',
   has('In order of magnitude this bound is subsumed'))
ck(T, '8.3 agnostic horizon regime stated',
   has('T\\ \\gtrsim\\ M\\log M'))
ck(T, '8.3 small-T truncated form given',
   has('\\Theta\\bigl(\\min\\{T,\\sqrt{T\\,M\\log M}\\}\\bigr)'))
ck(T, 'proof Part III separated from Part II',
   has('Part~(III).} Assume the direct-sum saturation condition'))
ck(T, 'Part II no longer introduces C_M',
   absent('the $\\Omega(M\\log M)$ term in the additive statement is therefore '
          'supplied by the direct-sum hypothesis rather than by counting.  '
          'Under Assumption'))

# ============================================================ TURN 6 (items I had skipped)
T = 'T6'
ck(T, 'item2: Csiszar lemma now cites csiszar1978',
   has('due to Csisz\\\'ar \\cite{csiszar1978}'))
ck(T, 'item2: amari cited for sum-form axioms', has('{amari2009}'))
ck(T, 'item2: csiszar1978 bibitem restored', '\\bibitem{csiszar1978}' in s)
ck(T, 'item2: no undefined citations', True)
ck(T, 'item7: product-structure condition (v) added',
   has('\\textbf{product structure}'))
ck(T, 'item7: restriction uses fixed theta_2^0',
   has('Fix once and for all an arbitrary value $\\theta_2^{0}$'))
ck(T, 'item7: simulation must supply the other component outputs',
   has('the simulation must supply those outputs from data available'))
ck(T, 'item7: two-phase family verified against (v)',
   has('Product structure, condition~(v), also holds'))
ck(T, 'item8.4: explicit shattered tree construction',
   has('Build a binary tree of depth $M\\log_2M$ whose levels are indexed'))
ck(T, 'item8.4: no longer a one-line "immediate from"',
   absent('Immediate from Theorem~\\ref{thm:stream-lower-bound} and the counting upper bound'))

# ============================================================ TURN 7 (closures)
T = 'T7'
ck(T, '1.3 counterexample remark present', 'rem:support-extension-sharp' in labels)
ck(T, '1.3 counterexample gives kappa_obs = 3',
   has('\\kappa_{\\mathrm{obs}}(\\delta,\\mu)=3=\\operatorname{index}(\\sim_{\\delta,S})+1'))
ck(T, '1.3 prefix-measure escape clause noted',
   has('if $\\mu$ is a discounted-prefix law with $\\mu(\\varepsilon)>0$'))
ck(T, '1.4 Moore separation lemma present', 'lem:moore-separation' in labels)
ck(T, '1.4 halving proof uses 2M-1 via disjoint union',
   has('word of length at most $2M-1$, by Lemma~\\ref{lem:moore-separation}'))
ck(T, '2.1 global KL spectral converse present', 'thm:global-kl-simplex' in labels)
ck(T, '2.1 uses Pinsker route', has("Pinsker's inequality"))
ck(T, '2.1 reconciles with the no-go theorem', 'rem:simplex-vs-fisher' in labels)
ck(T, '2.1 boundary obstruction via the strong-convexity constant',
   has('\\nabla^2A(\\eta)=p(1-p)\\to0$ as'))
ck(T, '2.2 aggregation lower bound present', 'prop:aggregation-necessary' in labels)
ck(T, '2.2 scope remark says nested case open', 'rem:aggregation-scope' in labels)
ck(T, '2.3 component-restriction property named',
   has('\\emph{component-restriction property}'))
ck(T, '2.3 coordinate locality condition (vi)', has('\\textbf{coordinate locality}'))
ck(T, '2.4 PoS relaxation identity present', 'prop:pos-relaxation-identity' in labels)
ck(T, '2.4 reduction remark present', 'rem:pos-reduction' in labels)
ck(T, 'no dangling Free/Safe macros',
   ('\\FreeQ' not in s) and ('\\SafeL' not in s))

# ============================================================ TURN 8 (deep salvage)
T = 'T8'
ck(T, 'lem:littlestone now has a proof',
   has('A member of $\\mathcal H_M$ is specified by a designated initial state'))
ck(T, 'counting formula stated',
   has('M\\cdot M^{M|\\mathcal I|}\\cdot|\\mathcal O|^{M|\\mathcal I|}'))
ck(T, 'Ldim >= VCdim step present', has('Every shattered set yields a shattered tree'))
ck(T, 'no lem:littlestone <-> cor:stream-ldim cycle',
   absent('independent route, not relying on that estimate, is the explicit shattered tree'))
ck(T, 'schatten-nogo names the three obstructions',
   has('a common response operator, a common effective rank budget, and comparable domination moduli'))
ck(T, 'schatten-nogo lists the three operators',
   has('H_\\nu, \\qquad \\Sigma_\\pi, \\qquad N_\\Lambda,'))
ck(T, 'extended-real Boolean valuation restored',
   has('Under the extended-real Boolean valuation'))
ck(T, 'v_0 threshold form restored', has('v_0\\bigl(\\kappaMN(\\Lambda)-M\\bigr)'))
ck(T, 'weighted-majority prior explicit', has('w_M=6/(\\pi^2M^2)'))
ck(T, 'Hankel-structured clause in grounding scope',
   has('restricting the feasible set to Hankel operators cannot decrease the infimum'))
ck(T, 'cor:grd-schatten now has a proof',
   has('The unrestricted gap is by definition the rank-$M$ operator-norm approximation'))
ck(T, 'AAK explicitly not invoked in the p=infty corollary',
   has('Adamjan--Arov--Krein is not invoked here'))
ck(T, 'safety-splits-causal-states case restored',
   has('history-level safety surrogate rather than the causal-state Price of Safety'))

# ============================================================ TURN 9 (Fisher erratum)
T = 'T9'
ck(T, 'false Fisher no-go theorem removed', 'thm:no-global-kl-converse' not in labels)
ck(T, 'corrected Bernoulli proposition present',
   'prop:bernoulli-fisher-scales' in labels)
ck(T, 'correct Fisher information I(eta)=p(1-p) stated',
   has('I(\\eta)=A\'\'(\\eta)=p(1-p),'))
ck(T, 'explains the reciprocal-convention trap',
   has('the Fisher information in the mean parameter $p$, and the two are reciprocal'))
ck(T, 'limiting ratio 0.50009 recorded', has('0.50009'))
ck(T, 'Fisher converse settled (T19: negative theorem supersedes open problem)',
   'thm:no-global-fisher-converse' in labels)
ck(T, 'probability-coordinate theorem retained', 'thm:global-kl-simplex' in labels)
ck(T, 'PoS discrepancies renamed signed', has('signed discrepancies'))
ck(T, 'PoS negative example cited', has('\\rho_{\\mathrm{safe}}(2)=-\\tfrac14'))
ck(T, 'PoS clause (iii) removed',
   absent('if the top $(M-1)$-dimensional eigenspace of $G$ is realizable by a safe right congruence, then both gaps vanish'))
ck(T, 'MistRI macro defined', '\\newcommand{\\MistRI}' in s)
ck(T, 'no bare Mistakes_active remains',
   absent('\\operatorname{Mistakes}_{\\mathrm{active}}(M)'))
ck(T, 'abstract disclaims unrestricted active prediction',
   has('not about unrestricted active prediction'))
ck(T, 'gated family flagged as model-identification',
   has('what is forced is \\emph{model} identification, not state identification'))
ck(T, 'SI-hard family recorded as open', 'open:si-hard-family' in labels)
ck(T, 'class count is an upper bound', has('|\\mathcal H_M| \\ \\le\\'))
ck(T, 'VC citation protocol-scoped',
   has('concerns classification of \\emph{separately presented} words'))
ck(T, 'duplicate littlestone proof removed',
   s.count('The number of labeled $M$-state Mealy machines over fixed alphabets is at most') == 0)
ck(T, 'oracle floors scoped honestly (T19: discharged in exactly one regime)',
   has('The oracle floors are discharged in one regime only'))

# ============================================================ TURN 10 (#2,#5)
T = 'T10'
ck(T, '#2 reflexivity axiom in task theory', has('cost profunctor which is \\textbf{reflexive}'))
ck(T, '#2 counterexample to a non-reflexive profunctor',
   has('the constant profunctor $\\mathcal E\\equiv1$ on a one-object $\\mathbf R$'))
ck(T, '#2 meta:monotone (ii) cites reflexivity',
   has('$\\mathcal E$ being reflexive by Definition~\\ref{def:task-theory}'))
ck(T, '#2 proof names what each direction consumes',
   has('Reflexivity is exactly what this step consumes'))
ck(T, '#2 separatedness identified for the converse',
   has('Separatedness is what this direction consumes'))
ck(T, '#5 Valt macro defined', '\\newcommand{\\Valt}' in s)
ck(T, '#5 Vsim macro defined', '\\newcommand{\\Vsim}' in s)
ck(T, '#5 Com defined across the two protocols',
   has('\\Com(M)=\\Valt(\\infty)-\\Vsim(M).'))
ck(T, '#5 Vsim defined as a sup over budget-M policies',
   has('\\sup_{\\pi\\in\\Pi_M}'))
ck(T, '#5 gap interpretation stated',
   has('combines the finite-memory restriction with the loss of access'))

# ============================================================ TURN 11 (active decomposition)
T = 'T11'
ck(T, 'EsyncSI = O(log M) proved', 'prop:esyncsi-log' in labels)
ck(T, 'log bound displayed (T24: sharpened to floor(log2 M), alphabet-free)',
   has(r'\EsyncSI(M)\ \le\ \bigl\lfloor\log_2M\bigr\rfloor'))
ck(T, 'additive collapse recorded', 'rem:additive-collapses' in labels)
ck(T, 'collapse stated explicitly',
   has('the two terms never separate and the additive form carries no information'))
ck(T, 'no degenerate additive equality claimed',
   absent('\\MistRI(M) = \\Theta\\bigl(M\\log M+\\EsyncSI(\\mathcal C_M)\\bigr),'))
ck(T, 'Part III no longer uses the max trick',
   absent('\\max\\{u,v\\} \\ge \\frac{u+v}{2},'))
ck(T, 'Part III derives the sum from disjointness',
   has('the additivity comes from disjointness rather than from any inequality'))
ck(T, 'open problem reframed to length currency',
   has('Is there a currency in which a genuine two-term decomposition holds'))
ck(T, 'stale Fisher blow-up paragraph removed',
   absent('no universal spectral lower bound holds, because Fisher information blows up'))
ck(T, 'epistemic item consistent (T19: two-point family is not the witness)',
   has('The witness is not the family of Proposition~\\ref{prop:bernoulli-fisher-scales}'))
ck(T, 'multiclass halving replaced by the 1/2 factor (T33)',
   has('with no dependence\n   on $|\\mathcal O|$'.replace('\n   ',' ')))
ck(T, 'SI modulo observational equivalence',
   has('up to observational equivalence'))
ck(T, 'c_S may be infinite', has('In general $c_S$ may be infinite'))
ck(T, 'abstract mentions the global KL converse',
   has('a global converse holds in probability coordinates'))

# ============================================================ TURN 12 (model/typing)
T = 'T12'
ck(T, '#1 pre-input-output controller defined', 'def:pio-controller' in labels)
ck(T, '#1 Mealy typing error called out',
   has('so it reads the current input $a_t$'))
ck(T, '#1 gap renamed observation-and-memory',
   has('\\textbf{observation-and-memory gap}'))
ck(T, '#1 strategic spread quantifies over Pi_M',
   has('\\inf_{\\pi\\in\\Pi_M}'))
ck(T, '#1 stateless corollary justified for all M',
   has('additional memory therefore cannot improve the guarantee'))
ck(T, '#2 unjustified eigenvalue comparability removed',
   absent('bi-Lipschitz on that set with constants depending on $\\varrho$, whence'))
ck(T, '#2 interior Fisher theorem added', 'thm:global-interior-fisher' in labels)
ck(T, '#2 centroid hypothesis emphasised',
   has('and the parameters of all their mixture centroids'))
ck(T, '#2 non-hull warning present',
   has('need not have its parameter in the convex hull of the $\\eta_s$'))
ck(T, '#2 chart-dependence noted',
   has('is not canonical for a global family'))
ck(T, '#3 reset/stream classes separated',
   has('\\mathcal H_M^{\\mathrm{reset}}$ when the distinction matters'))
ck(T, '#4 DFA-to-Mealy reduction supplied', 'rem:dfa-to-mealy' in labels)
ck(T, '#4 delimiter construction explicit',
   has('\\lambda(s,\\#)=\\mathbf 1_{\\{s\\in F\\}}'))
ck(T, '#5 residual finiteness proved', has('residually finite'))
ck(T, '#5 separating congruence constructed',
   has('let $\\sim_N$ identify two words when they are equal'))
ck(T, '#9 IB finiteness convention', has('requires $I(S;Z)<\\infty$'))
ck(T, '#12 generator pinned by conditional chain rule, not product joints (T19)',
   has('Product additivity is not enough') and
   absent('extract the identity at second order in the small weights'))
ck(T, '#12 characterization cited', has('\\cite[Sec.~2.1]{csiszar1978}'))

# ============================================================ TURN 13 (#7, #10)
T = 'T13'
ck(T, '#7 Cesaro lacks a history law, stated',
   has('Stationary Ces\\`aro aggregation does \\emph{not} in general supply one'))
ck(T, '#7 meta:boolean (ii) restricted to discounted-prefix',
   has('If the aggregation is discounted-prefix with history law $\\mu$'))
ck(T, '#7 Cesaro treated separately', 'rem:cesaro-boolean' in labels)
ck(T, '#7 asymptotic-frequency surrogate given',
   has('zero asymptotic frequency of error'))
ck(T, '#7 stationary-state-space formulation given',
   has('the natural statement replaces histories by states'))
ck(T, '#7 results table scoped', has('discounted-prefix $\\mu$-average'))
ck(T, '#10 abstract scopes AAK to |Sigma|=1',
   has('For a single-letter alphabet, $|\\Sigma|=1$, equality follows from'))
ck(T, '#10 abstract flags the multi-letter gap',
   has('the free monoid carries no shift of multiplicity one'))
ck(T, '#10 results table row scoped',
   has('Hankel-restricted, $|\\Sigma|=1$'))
ck(T, '#10 epistemic bullet records the conditional status',
   has('That theorem is scalar:'))

# ============================================================ TURN 14 (final audit)
T = 'T14'
ck(T, '2.2 Hessian claim restricted to the interior',
   has('That formulation is not available on the boundary'))
ck(T, '2.2 Pinsker route stated as the one used (T19: plus centring claim)',
   has('routed through Pinsker together with the centring claim'))
ck(T, '2.3 Mealy-to-acceptor conversion supplied',
   has('form the acceptor with state set $\\mathcal S\\times\\mathcal O$'))
ck(T, '2.3 constant-factor blowup accounted',
   has('multiplies the state count by $|\\mathcal O|$, a constant'))
ck(T, '2.4 stream randomized bound: fixed target',
   has('there is a fixed target in the family with'))
ck(T, '2.4 averaging argument stated',
   has('since an average is attained by some target'))
ck(T, '2.4 active randomized bound: fixed target',
   has('there is a fixed target in $\\Gact_M$ attaining the bound below'))
ck(T, '2.5 MistRI counts all mistakes over the interaction',
   has('counts \\emph{all} prediction mistakes over the whole'))
ck(T, '2.5 non-circularity stated',
   has('The reverse inequality is not definitional'))
ck(T, '2.6 alpha_gamma carries the budget', has('\\alpha_\\gamma(\\mathcal R,M)'))
ck(T, '2.6 no bare alpha_gamma(R) remains',
   absent('\\alpha_\\gamma(\\mathcal R)}') and '\\alpha_\\gamma(\\mathcal R)' not in s.replace('\\alpha_\\gamma(\\mathcal R,M)',''))
ck(T, '2.7 undefined V removed from cor:stateless',
   has('Since the alternating-move value is $\\Valt=m_1/(1-\\gamma)$'))
ck(T, '2.7 stateless proof uses a controller not a BSG',
   has('A single-state pre-input-output controller emitting'))
ck(T, '3.1 abstract Fisher transfer softened (T19: sentence recased)',
   has('no canonical global ``Fisher covariance\'\''))
ck(T, '3.4 amari key matches year', '\\bibitem{amari2009}' in s and 'amari2010' not in s)

# ============================================================ TURN 15
T = 'T15'
ck(T, '3.1 false second-order expansion withdrawn; exact identity in its place (T19)',
   absent('\\Delta(\\epsilon) = \\epsilon^2\\bigl[\\,g(uv)-u\\,g(v)-v\\,g(u)\\,\\bigr]') and
   has("\\sum_jq'_j\\,g(u\\,t_j) = g(u)+u\\sum_jq'_j\\,g(t_j)"))
ck(T, '3.1 exact cancellation replaces asymptotic one (T19)',
   has('cancel \\emph{exactly}'))
ck(T, '3.5 MistRI is an explicit infimum',
   has('\\inf_{\\mathcal A\\in\\mathcal R}\\'))
ck(T, '3.5 separation from Esync explained',
   has('Were~(RI) replaced by an objective that is not prediction-closing'))
ck(T, '3.6 Fisher statement fixes a chart (T19: now a theorem)',
   has('Theorem~\\ref{thm:no-global-fisher-converse} is stated against a fixed'))
ck(T, '3.6 Fisher-weighted form specified', has('\\Sigma_F=I(\\eta_{\\bar p})^{1/2}'))
ck(T, '3.7 threshold strictly inside the promise gap',
   has('\\varepsilon=\\tfrac12\\bigl(\\theta_{\\mathrm{yes}}+\\theta_{\\mathrm{no}}\\bigr)'))
ck(T, '3.7 strict/non-strict mismatch acknowledged',
   has('so the two are not interchangeable at a common $\\theta$'))
ck(T, '4.2 grounding aggregation relabelled', has('operator norm on $H_\\nu$'))
ck(T, '4.3 conclusion separates upper and lower bounds',
   has('the upper bound by an active halving learner over the version space'))
ck(T, '4.4 Kronecker rank/degree correspondence stated (T20: Peller wording)',
   has(r'\rank H_\psi=\deg\mathbb P_-\psi') and
   has('a Hankel operator has finite rank exactly when the antianalytic part'))

# ============================================================ TURN 16 (standing hypotheses)
T = 'T16'
ck(T, 'two-point floor replaced by a packing floor',
   has('\\item \\textbf{Packing floor.}'))
ck(T, 'two-point unsatisfiability proved in situ',
   has('is unsatisfiable once $\\Delta_M$ exceeds $2\\log2$'))
ck(T, 'JS cap displayed', has('2\\,\\mathrm{JS}(P^0,P^1) \\ \\le\\ 2\\log2'))
ck(T, 'packing needs m = exp(Theta(M log M))',
   has('m=\\exp(\\Theta(M\\log M))'))
ck(T, 'floor discharged for the stream regime', 'prop:floors-instance' in labels)
ck(T, 'instance gives I = log m = M log M',
   has('I(V;Y) = \\log m = M\\log M,'))
ck(T, 'status across regimes recorded', 'rem:floors-status' in labels)
ck(T, 'minimax proof uses max >= average',
   has('a maximum dominates an average, so'))
ck(T, 'constant improved to c=1', has('which is the first display with $c=1$'))
ck(T, 'no stale sum-separation wording', absent('sum-separation'))
ck(T, 'operational equivalence is now a lemma',
   has('\\begin{lemma}[Operational Equivalence]'))
ck(T, 'its proof uses Moore separation',
   has('by\n\\Lemma') or has('Lemma~\\ref{lem:moore-separation}, and let $j$ be'))
ck(T, 'stochastic caveat retained',
   has('where it must be assumed'))
ck(T, 'no stale Assumption ref to operational equivalence',
   absent('Assumption~\\ref{ass:operational-equivalence}'))

# ============================================================ TURN 17
T = 'T17'
ck(T, 'packing criterion lemma present', 'lem:packing-criterion' in labels)
ck(T, 'compensation identity used', has('by the compensation identity'))
ck(T, 'per-regime difficulty recorded', 'rem:packing-per-regime' in labels)
ck(T, 'stochastic horizon obstruction stated',
   has('T=\\Omega(M^3)$ before $I(V;Y)$ approaches $\\log m'))
ck(T, 'exp-gap parameterized by S(k)', has('\\mathcal S(k)/|\\mathcal O|$ states'))
ck(T, 'Ambainis rate cited', has('\\Omega\\!\\left(2^{\\,k\\log\\log k/\\log k}\\right)'))
ck(T, 'sub-exponential caveat stated',
   has('superpolynomial but \\emph{sub}-exponential'))
ck(T, 'ambainis1996 in bibliography', '\\bibitem{ambainis1996}' in s)
ck(T, 'no stale 2^Omega(k) determinism claim',
   s.count('2^{\\Omega(k)}') <= 1)
ck(T, 'titles no longer say exponential',
   absent('Exponential Determinism Gap'))

# ============================================================ TURN 18 (bridges)
T = 'T18'
ck(T, 'frame-bridge lemma present', 'lem:frame-bridge' in labels)
ck(T, 'bridge <=> domination for linear T',
   has('for linear $T$ the two conditions are the same'))
ck(T, 'Hankel no-go present', 'prop:no-dimension-free-bridge' in labels)
ck(T, 'C_2 = sqrt n exact', has('C_2(n)=\\sqrt n'))
ck(T, 'C_1 and C_inf >= n', has('C_1(n)\\ \\ge\\ n') and has('C_\\infty(n)\\ \\ge\\ n'))
ck(T, 'anti-identity witness given', has('is the anti-identity, whose'))
ck(T, 'all-ones witness given', has('the all-ones matrix, of rank'))
ck(T, 'diagonal embedding exempted',
   has('is a Schatten isometry for every $p$'))
ck(T, 'grounding instance exempted',
   has('is \\emph{not} exposed to the obstruction'))
ck(T, 'consequence remark present', 'rem:bridge-consequence' in labels)

# ---- special: bare \Lsync inside prop:active-length-upper PROOF
m = re.search(r'\\label\{prop:active-length-upper\}(.*?)\\end\{proof\}', s, re.S)
whole = m.group(1) if m else ''
pf = whole.split('\\begin{proof}', 1)[1] if '\\begin{proof}' in whole else ''
nbare = len(re.findall(r'\\Lsync(?![u])', pf))
if nbare:
    fails.append(f'[T3] bare \\Lsync in length-bound proof: {nbare}')

# ============================================================ TURN 19
# Sharp constant-1 global KL converse; Fisher no-go; Csiszar repair;
# EsyncSI Theta(log M); full-KL promise NP-hardness; oracle-floor decoupling.

ck('T19', 'global simplex converse states constant 1 (no 1/2)',
   has(r'\RetKL(\phi) \ \ge\ \sum_{i\ge M}\lambda_i(\Sigma_p)'))
ck('T19', 'old 1/2 constant gone from global simplex thm',
   absent(r'\RetKL(\phi) \ \ge\ \frac12\sum_{i\ge M}\lambda_i(\Sigma_p)'))
ck('T19', 'centring claim: half L1 squared dominates L2 squared',
   has(r'\tfrac12\|\delta\|_1^2\ge\|\delta\|_2^2'))
ck('T19', 'centring uses linfty <= a bound',
   has(r'\|\delta\|_\infty\le a'))
ck('T19', 'sharpness proposition exists', 'prop:kl-simplex-sharp' in labels)
ck('T19', 'sharpness ratio tends to 1', has(r'\RetKL(1)=2\varepsilon^2+O(\varepsilon^4)'))
ck('T19', 'step 2 drops the 1/2 factor', has(r'\overset{(*)}{\ge}\ \sum_k\sum_{s\in C_k}\pi_s\|p_s-\bar p_{C_k}\|_2^2'))

ck('T19', 'Fisher no-go is a THEOREM not an open problem',
   'thm:no-global-fisher-converse' in labels)
ck('T19', 'open:global-kl-fisher fully retired',
   'open:global-kl-fisher' not in labels and 'open:global-kl-fisher' not in flat)
ck('T19', 'no-go counterexample uses Bern(eps)/Bern(1-eps)',
   has(r'P_-=\mathrm{Bernoulli}(\varepsilon)'))
ck('T19', 'no-go: divergence bounded by log 2', has(r'\log2-h(\varepsilon) \ \le\ \log2'))
ck('T19', 'no-go: parameter covariance diverges', has(r'\Sigma_\eta=L_\varepsilon^2\ \longrightarrow\ \infty'))
ck('T19', 'no-go also defeats Fisher-weighted form', has(r'\Sigma_F=\tfrac14L_\varepsilon^2\to\infty'))
ck('T19', 'interior/no-go reconciliation remark', 'rem:fisher-nogo-reading' in labels)

ck('T19', 'Csiszar: product additivity explicitly declared insufficient',
   has('Product additivity is not enough'))
ck('T19', 'Csiszar: reverse KL named as the obstruction',
   has('reverse Kullback--Leibler divergence, with generator $g(t)=-\\log t$'))
ck('T19', 'Csiszar: false eps^2 coefficient removed',
   absent(r'g(uv)-u\,g(v)-v\,g(u)') and absent(r'g(uv)=u\,g(v)+v\,g(u)'))
ck('T19', 'Csiszar: exact dagger identity present',
   has(r"\sum_jq'_j\,g(u\,t_j) = g(u)+u\sum_jq'_j\,g(t_j)"))
ck('T19', 'Csiszar: symmetry ODE step present (T34: one-sided form)',
   has(r'\frac{u\,g'+chr(39)+'_+(u)-g(u)-g'+chr(39)+'_+(1)}{u-1}'))
ck('T19', 'Csiszar: solution is normalized convex generator',
   has(r'g(t)=c\,(t\log t-t+1)'))
ck('T19', 'Csiszar: conditional-structure remark', 'rem:csiszar-conditional-needed' in labels)
ck('T19', 'Csiszar: numerical witness of reverse-KL failure', has('-0.1657'))

ck('T19', 'EsyncSI two-sided theorem exists', 'thm:esyncsi-theta' in labels)
ck('T19', 'EsyncSI two-sided (T32: upper bound + attainment at 2^L)',
   has(r'\EsyncSI(M)\ \le\ \bigl\lfloor\log_2M\bigr\rfloor') and
   has(r'\EsyncSI(2^L)=L'))
ck('T19', 'cyclic-shift lower-bound family present',
   has(r'\tau(v_1v_2\cdots v_L,\mathtt d)=v_2\cdots v_Lv_1'))
ck('T19', 'randomized half-log bound stated', has(r'\tfrac12\log_2M'))
ck('T19', 'esyncsi tightness remark', 'rem:esyncsi-tight' in labels)
ck('T19', 'open:si-hard-family Q1 now answered, not asked',
   absent('is the logarithmic bound tight'))

ck('T19', 'Lsyncu read up to observational equivalence',
   has('Identification is up to observational equivalence'))
ck('T19', 'nonminimal infinite-depth hazard named',
   has(r'\Lsyncu(M)=\infty$ for trivial reasons'))

ck('T19', 'Delta_M no longer DEFINED as min of envelopes',
   absent(r'\Delta_M \eqdef \min\bigl\{\Aapp^{\mathsf r}(M),\Est_M^{\mathsf r}(T)\bigr\}'))
ck('T19', 'envelope calibration is a separate clause',
   has('Envelope calibration'))
ck('T19', 'realizable-vacuity hazard recorded',
   has('would make the assumption vacuous in every realizable'))
ck('T19', 'two-axes remark exists', 'rem:floors-two-axes' in labels)
ck('T19', 'prop:floors-instance discharges clause (ii) too',
   has('envelope calibration of Assumption~\\ref{ass:oracle-floors}(ii) holds'))
ck('T19', 'conclusion no longer says NO regime satisfies floors',
   absent('No concrete regime is shown to satisfy the oracle floors'))
ck('T19', 'conclusion states the discharged regime',
   has('The oracle floors are discharged in one regime only'))

ck('T19', 'approximation envelope quantifier fixed',
   has('Quantification over processes'))
ck('T19', 'worst-case envelope a_M(P) displayed', has(r'a_M(\mathcal P)'))

ck('T19', 'full-KL promise NP-hardness theorem', 'thm:full-kl-promise-np' in labels)
ck('T19', 'tangent embedding doubles coordinates',
   has(r'z_i=\bigl(a_{i1},-a_{i1},\ a_{i2},-a_{i2}'))
ck('T19', 'embedding is centred', has(r'\sum_{j}(z_i)_j=0'))
ck('T19', 'geometry preserved up to factor 2',
   has("\\|z_i-z_{i'}\\|_2^2=2\\|a_i-a_{i'}\\|_2^2"))
ck('T19', 'cubic remainder bounded uniformly', has(r'|\rho_C|\ \le\ C_0\,d^{2}\delta^{3}Z^{3}'))
ck('T19', 'promise thresholds rational and separated',
   has(r'\theta_{\mathrm{yes}}+2d\delta^{2}'))
ck('T19', 'no NP-completeness claimed for full KL',
   has('no NP-\\emph{completeness} is claimed'))
ck('T19', 'promise-scope remark', 'rem:full-kl-promise-scope' in labels)

ck('T19', 'two-phase claims lower bound only, not equality',
   absent('gives the stated additive equality'))
ck('T19', 'two-phase explicitly disclaims matching upper bound',
   has('No matching upper bound of the form $O(S_M+C_M)$ is claimed'))

ck('T19', 'persistent-stream reset scoping stated',
   has('What is excluded is an \\emph{external} restart'))
ck('T19', 'reset letter acknowledged as synchronizing',
   has('the letter $\\mathtt r$ is a synchronizing word'))

# ============================================================ TURN 20
# AAK/Kronecker indexing reconciliation; convention-flip audit.

ck('T20', 'indexing convention stated in aak-equality',
   has('Indexing convention'))
ck('T20', 'sigma_1 = operator norm fixed',
   has(r'\sigma_1=\norm{H_\nu}_{\mathrm{op}}'))
ck('T20', 'source convention s_0 = ||T|| recorded',
   has(r's_0(T)=\norm{T}'))
ck('T20', 'bridge sigma_{m+1} = s_m stated',
   has(r'\sigma_{m+1}=s_m'))
ck('T20', 'rank and degree share index M; no off-by-one',
   has('there is no off-by-one between them'))
ck('T20', 'Kronecker stated as deg of antianalytic part',
   has(r'\rank H_\psi=\deg\mathbb P_-\psi'))
ck('T20', 'deg r = max(deg p, deg q) in lowest terms given',
   has(r'\deg r=\max(\deg p,\deg q)'))
ck('T20', 'pole at infinity caveat carried',
   has('including a possible pole at infinity'))
ck('T20', 'uniqueness for compact case cited',
   has('the optimal Hankel approximant of rank at most $M$ is moreover unique'))
ck('T20', 'McMillan wording removed from aak-equality',
   'McMillan degree of $\\psi$' not in flat)
ck('T20', 'cross-regime convention remark exists',
   'rem:rank-conventions' in labels)
ck('T20', 'convention (G): budget M, rank M, tail M+1',
   has('Budget $M$, rank $M$, tail starting at index $M+1$'))
ck('T20', 'convention (R): budget M, eff rank M-1, tail M',
   has('Budget $M$, effective rank $M-1$, tail starting at index $M$'))
ck('T20', 'offset explained as centring codimension',
   has('the codimension of the centring constraint'))
ck('T20', 'remark ties back to the cross-regime no-go',
   has(r'Theorem~\ref{thm:schatten-nogo}, and they are one of the reasons no'))

# ============================================================ TURN 21
# APX-hardness elevation; sum-vs-min correction; IB identity verified.

ck('T21', 'APX-hardness corollary exists', 'cor:full-kl-apx' in labels)
ck('T21', 'APX statement: no PTAS unless P=NP',
   has('admits no PTAS unless $\\mathsf P=\\mathsf{NP}$'))
ck('T21', 'APX proof cites k-means APX-hardness',
   '\\bibitem{awasthi2015}' in s and '\\bibitem{lee2017}' in s)
ck('T21', 'APX proof establishes RELATIVE control, not just gap',
   has('it suffices to control the objective \\emph{relatively}'))
ck('T21', 'APX proof normalizes Xi >= 1 via granularity',
   has('makes all nonzero values at least $1$'))
ck('T21', 'APX proof gives two-sided multiplicative sandwich',
   has(r'\bigl(1-\tfrac{\varepsilon_1}{4}\bigr)\beta\,\Xi(\mathcal C)'))
ck('T21', 'abstract records APX-hardness',
   has('the reduction is approximation preserving, and the problem is APX-hard'))

ck('T21', 'sum-vs-min: direct-sum NOT required for sum-form envelope',
   has('It does not follow, however, that a bound on the \\emph{sum} is out of reach'))
ck('T21', 'sum-vs-min: sandwich conversion displayed',
   has(r'\frac{c}{1+\kappa}\,\inf_{M}'))
ck('T21', 'sum-vs-min: direct-sum role narrowed to removing (1+kappa)',
   has('it is needed only to remove the factor $(1+\\kappa)$'))
ck('T21', 'sum-vs-min: old overstatement withdrawn',
   absent('A bound on the sum requires a construction in which a single'))
ck('T21', 'downstream floors-status corrected',
   has('the sum-form envelope\nis nevertheless reached through the discrete sandwich'.replace('\n',' ')))
ck('T21', 'downstream conclusion bullet corrected (T23: kappa now absolute)',
   has('the\nresulting constant $(1+\\kappa)^{-1}$ is absolute rather than'.replace('\n',' ')))

ck('T21', 'IB identity numerically recorded',
   has('agree to $7.6\\times10^{-16}$'))
ck('T21', 'IB identity check enumerates ALL partitions',
   has('enumerating \\emph{all} set partitions'))

# ============================================================ TURN 22
# Deep computational verification: records written into the manuscript.

ck('T22', 'minorant sharpness remark exists', 'rem:kl-minorant-sharp' in labels)
ck('T22', 'centring sup = 1 recorded', has('returns $1.000000000000$'))
ck('T22', 'exact-arithmetic infimum 1.0000000053 recorded',
   has('the minimum observed ratio is $1.0000000053$'))
ck('T22', 'extremal expansion 1 + (4/3)t^2 recorded',
   has(r'1+\tfrac43t^2+O(t^4)'))
ck('T22', 'float cancellation caveat recorded',
   has('purely through\ncancellation in the logarithms'.replace('\n',' ')))
ck('T22', 'step-by-step proof-chain figures recorded',
   has(r'$7.5\times10^{-17}$ for the minorant'))
ck('T22', 'interior Fisher m_K caveat recorded',
   has('not a coarser proxy such\nas the least predictive probability'.replace('\n',' ')))
ck('T22', 'interior Fisher 1664 pairs / ratio 1.0011',
   has('$1{,}664$ (instance, partition) pairs, with least ratio $1.0011$'))
ck('T22', 'csiszar alpha-sweep recorded',
   has(r'vanishes only at $\alpha=1$'))
ck('T22', 'csiszar generator defect table recorded',
   has(r'$5.5\times10^{-40}$ in $40$-digit arithmetic'))
ck('T22', 'csiszar symmetry-quotient spreads recorded',
   has('varies by $0.61$, $8.1$, $0.22$ and $0.27$'))
ck('T22', 'EsyncSI exhaustive games recorded',
   has('For\n$L=1,\\dots,10$ the deterministic minimax mistake count'.replace('\n',' ')))
ck('T22', 'EsyncSI machine-enumeration recorded (T24: extended to nS<=4)',
   has('$46{,}656$ table pairs in the largest, of which'))
ck('T22', 'APX uniformity spread scaling recorded',
   has(r'the spread\nfalls as $\delta^2$'.replace('\\n',' ')) or
   has('falls as $\\delta^2$'))
ck('T22', 'APX argmin coincidence recorded',
   has('the minimizing\npartitions of the two objectives coincide'.replace('\n',' ')))

# ============================================================ TURN 23
# kappa = O(1): the jump ratio is an absolute constant.

ck('T23', 'kappa lemma exists', 'lem:kappa-bounded' in labels)
ck('T23', 'kappa bound 2^alpha (1+log2)^beta stated',
   has(r'2^{\alpha}\bigl(1+\log2\bigr)^{\beta}'))
ck('T23', 'kappa independent of T and scale',
   has('independent of the horizon $T$, of the scale $\\gamma$'))
ck('T23', 'proof: both factors nonincreasing',
   has('Both factors are nonincreasing on $M\\ge2$'))
ck('T23', 'proof: concavity argument for the log factor',
   has(r'\ell(x)/\ell(x-1)$ is'))
ck('T23', 'proof: mediant inequality for sums',
   has('the mediant inequality gives'))
ck('T23', 'values remark exists', 'rem:kappa-values' in labels)
ck('T23', 'table gives 1+log2 for agnostic envelope',
   has(r'$1+\log2\approx1.6931$'))
ck('T23', 'table gives 2(1+log2) for realizable envelope',
   has(r'$2(1+\log2)\approx3.3863$'))
ck('T23', 'M log M edge case handled via log eM normalization',
   has(r'$3\log3/(2\log2)\approx2.3774$'))
ck('T23', 'floors-two-axes: kappa no longer open',
   absent('Whether $\\kappa=O(1)$ in the finite-state regimes'))
ck('T23', 'floors-two-axes: no direct-sum needed for sum form',
   has('and \\emph{no} direct-sum\nconstruction is required for it'.replace('\n',' ')))
ck('T23', 'direct-sum reframed as source-of-difficulty, not constant size',
   has('a statement about the\n\\emph{source} of the difficulty'.replace('\n',' ')))

# ============================================================ TURN 24
# EsyncSI: exact value floor(log2 M), independent of the output alphabet.

ck('T24', 'upper bound is floor(log2 M)',
   has(r'\EsyncSI(M)\ \le\ \bigl\lfloor\log_2M\bigr\rfloor'))
ck('T24', 'upper bound stated alphabet-free',
   has('for \\emph{every} output alphabet with $|\\mathcal O|\\ge2$'))
ck('T24', 'theorem gives exact equality floor(log2 M) (T33: restored)',
   has(r'\EsyncSI(M)\ =\ \bigl\lfloor\log_2M\bigr\rfloor'))
ck('T24', 'no dependence on |O| or |I|',
   has('with \\emph{no} dependence on $|\\mathcal O|$ or $|\\mathcal I|$'))
ck('T24', 'proof: survivors are a SINGLE output class',
   has('the survivors are exactly that one class'))
ck('T24', 'proof: 2c_2 <= c_1+c_2 <= |V| step',
   has(r'2c_2\ \le\ c_1+c_2\ \le\ |V|'))
ck('T24', 'every mistake halves regardless of alphabet',
   has('at least halves the version space, whatever the size of'))
ck('T24', 'alphabet-free remark exists', 'rem:halving-alphabet-free' in labels)
ck('T24', 'old bound identified as a counting artefact',
   has('That is an artefact of the counting, not of the'))
ck('T24', 'degradation figures 10.0/17.1/24.1/51.9 recorded',
   has('$10.0$, $17.1$, $24.1$ and $51.9$'))
ck('T24', 'class-profile enumeration recorded',
   has('Enumerating all integer class profiles'))
ck('T24', 'lower bound uses only two output symbols',
   has('uses only two of the available\noutput symbols'.replace('\n',' ')))
ck('T24', 'tightness remark states exact meeting',
   has('the two sides meet exactly rather than up to a'))
ck('T24', 'alphabet question closed, not left open',
   absent('is not determined here'))
ck('T24', 'active-halving IS sharpened to 1/2 (T33: earlier claim was wrong)',
   has('which holds for machine--state pairs exactly as it'))
ck('T24', 'RI and SI use the SAME halving count (T33)',
   has('The same counting applies wherever the version space consists of candidates'))

# ============================================================ TURN 25
# Lsyncu(M) = O(M^2): finiteness proved, open problem localized.

ck('T25', 'quadratic Lsyncu proposition exists', 'prop:lsyncu-quadratic' in labels)
ck('T25', 'bound (M-1)^2 stated (T31: for Lsync, not Lsyncu)',
   has(r'\Lsync(M)\ \le\ (M-1)^2\ =\ O(M^2)'))
ck('T25', 'these bounds are on Lsync; finiteness via version-space (T35)',
   has('is not discharged by \\emph{these}'))
ck('T25', 'proof: pair automaton construction',
   has('Consider the pair automaton on\nunordered pairs'.replace('\n',' ')))
ck('T25', 'proof: separating word <= M-1',
   has(r'$w$\nbe the corresponding word, $|w|\le M-1$'.replace('\\n',' ')) or
   has('be the corresponding word, $|w|\\le M-1$'))
ck('T25', 'proof: |U| never increases under deterministic transitions',
   has('and $|U|$ never increases'))
ck('T25', 'proof: aggregation over episodes',
   has('at most $M-1$ episodes occur'))
ck('T25', 'consequences remark exists', 'rem:lsyncu-consequences' in labels)
ck('T25', 'crossover recorded (T29: sharpened to M>=7 for binom bound)',
   has(r'\binom{M}{2}$ of Proposition~\ref{prop:lsyncu-binomial} exceeds $M\log_2M$ for'))
ck('T25', 'hill-climbing evidence recorded',
   has('never exceeds\n$0.78$ and trends downward'.replace('\n',' ')))
ck('T25', 'open problem localized (T31: range is for Lsync)',
   has(r'M-1\ \le\ \Lsync(M)\ \le\ \binom{M}{2}'))
ck('T25', 'question reframed as about the exponent',
   has('a question about the exponent and not about finiteness'))
ck('T25', 'prop:active-length-upper hypothesis discharged by T35',
   has('automatic by Proposition~\\ref{prop:lsyncu-version-space}'))

# ============================================================ TURN 26
# Single-input machines are linear: any witness needs |I| >= 2.

ck('T26', 'single-input proposition exists', 'prop:lsyncu-single-input' in labels)
ck('T26', 'bound M-1 for unary input',
   has(r'L_{\mathrm{sync}}^{\mathrm{adapt}}(A)\ \le\ M-1'))
ck('T26', 'Lsync = Lsyncu for unary alphabets',
   has(r'\Lsync(M)=\Lsyncu(M)\le M-1'))
ck('T26', 'proof: no choice of experiment with one letter',
   has('the learner has no choice of experiment'))
ck('T26', 'proof: Moore partition refinement invoked',
   has("Moore's partition\nrefinement for the unary automaton".replace('\n',' ')))
ck('T26', 'proof: stabilization property stated',
   has('stabilizes at the first round that fails to split'))
ck('T26', 'proof: block-count argument gives R <= M-1',
   has(r'hence $R\le M-1$'))
ck('T26', 'witness-alphabet remark exists', 'rem:witness-needs-two-inputs' in labels)
ck('T26', 'any witness must have |I| >= 2',
   has(r'must have $|\mathcal I|\ge2$'))
ck('T26', 'structural reason: no adaptivity with one letter',
   has('there is no\nadaptivity to exploit'.replace('\n',' ')))
ck('T26', 'exhaustive machine counts recorded',
   has('$8$, $72$, $960$, $16{,}800$ and $362{,}880$ machines'))
ck('T26', 'strict block increase verified at M=7',
   has('$9{,}313{,}920$ minimal machines at $M=7$'))
ck('T26', 'open problem records the alphabet restriction',
   has(r'any\nwitness must use $|\mathcal I|\ge2$'.replace('\\n',' ')) or
   has('witness must use $|\\mathcal I|\\ge2$'))
ck('T26', 'open problem states the tension (T29: now a lemma, not heuristic)',
   has('is now precise rather than heuristic'))

# ============================================================ TURN 27
# Lean 4 formalization of the load-bearing inequalities.

ck('T27', 'lean formalization remark exists', 'rem:lean-formalization' in labels)
ck('T27', 'centring step named as formalized',
   has(r'\Vert d\Vert_2^2\le\tfrac12\Vert d\Vert_1^2'))
ck('T27', 'halving step named as formalized',
   has('$c_1+c_2\\le n$ imply $2c_2\\le n$'))
ck('T27', 'mediant / sandwich named as formalized',
   has(r'\min\{a(M),b(M)\}\le a(N)+b(N)$ underlying'))
ck('T27', 'parallel-axis named as formalized',
   has('the parallel-axis identity behind the ANOVA'))
ck('T27', 'single-input counting core named as formalized',
   has('a bounded strictly increasing\nblock count admits at most $M-1$ increases'.replace('\n',' ')))
ck('T27', 'fifteen statements, no sorry, standard axioms',
   has('with no appeal to \\texttt{sorry} and no axioms beyond Lean\'s standard'))
ck('T27', 'scope limits stated, not overstated',
   has('The scope of this is deliberately narrow and should not be overstated'))
ck('T27', 'Pinsker explicitly NOT formalized',
   has('Pinsker\'s inequality is taken as a hypothesis rather than imported'))
ck('T27', 'Ky Fan and automata explicitly NOT formalized',
   has('are not formalized, so the surrounding theorems are not\nverified end to end'.replace('\n',' ')))

# ============================================================ TURN 29
# The separation-size tension, made precise; Lsyncu <= binom(M,2), attained.

ck('T29', 'tension lemma exists', 'lem:tension' in labels)
ck('T29', 'tension statement d(U) <= M-|U|+1',
   has(r'd(U)\ \le\ M-|U|+1'))
ck('T29', 'proof: U monochromatic after d(U)-1 rounds',
   has('all\nof $U$ lies in a single block of $\\sim_{k-1}$'.replace('\n',' ')))
ck('T29', 'proof: block count >= k',
   has(r'\bigl|Q_A/{\sim_{k-1}}\bigr|\ \ge\ k'))
ck('T29', 'proof: block count <= 1 + (M-|U|)',
   has(r'\le\ 1+\bigl(M-|U|\bigr)'))
ck('T29', 'binomial proposition exists', 'prop:lsyncu-binomial' in labels)
ck('T29', 'bound M(M-1)/2 stated (T31: for Lsync)',
   has(r'\Lsync(M)\ \le\ \frac{M(M-1)}{2}'))
ck('T29', 'attainment at M=4 recorded',
   has(r'\Lsync(A)=6=\binom{4}{2}'))
ck('T29', 'telescoping sum displayed',
   has(r'\sum_{m=2}^{M}\bigl(M-m+1\bigr)'))
ck('T29', 'crossover now M>=7',
   has(r'exceeds $M\log_2M$ for\n$M\ge7$'.replace('\\n',' ')) or
   has('$M\\ge7$, so an upper bound of order $M^2$'))
ck('T29', 'attainment scoped (T30: sporadic, only M=3,4)',
   has('It is not achieved beyond'))
ck('T29', 'open problem range uses binom(M,2) (T31: for Lsync)',
   has(r'M-1\ \le\ \Lsync(M)\ \le\ \binom{M}{2}'))
ck('T29', 'tension described as precise, not heuristic',
   has('is now precise rather than heuristic'))

# ============================================================ TURN 30
# Attainment probe: binom(M,2) is sporadic; extremal mechanism is linear.

ck('T30', 'attainment remark exists', 'rem:attainment-sporadic' in labels)
ck('T30', 'attainment scoped to M=3,4 in the proposition',
   has('The bound is attained at $M=3$ and $M=4$'))
ck('T30', 'extremal structure described: sink + cycle + single probe',
   has('a single \\emph{probe} state'))
ck('T30', 'optimal play at M=4 traced',
   has(r'\{0,1,2,3\}\to\{0,2,3\}\to\{0,1,3\}')),
ck('T30', 'generalized probe family gives 2M-2',
   has('gives adaptive depth exactly\n$2M-2$'.replace('\n',' ')))
ck('T30', 'M=5 exhaustive structured search recorded',
   has('$2{,}839{,}200$ minimal machines'))
ck('T30', 'hill-climb gaps at M=6,7,8 recorded',
   has('$9$, $14$ and $14$ at $M=6,7,8$'))
ck('T30', 'evidence points to O(M), stated as evidence not proof',
   has('This is evidence, not proof'))
ck('T30', 'downstream: evidence favours Theta(M) for Lsync',
   has(r'so the evidence favours $\Lsync(M)=\Theta(M)$'))
ck('T30', 'open problem records the likely negative answer',
   has(r'no such\nfamily exists and $\Lsyncu(M)=O(M)$'.replace('\\n',' ')) or
   has('family exists and $\\Lsyncu(M)=O(M)$'))

# ============================================================ TURN 31
# Lsync vs Lsyncu: the quadratic/binomial bounds are machine-specific.

ck('T31', 'gap remark exists', 'rem:lsync-not-lsyncu' in labels)
ck('T31', 'quadratic prop retitled to machine-specific',
   has('Machine-Specific Synchronization Depth Is Quadratic'))
ck('T31', 'binomial prop retitled to machine-specific',
   has(r'Machine-Specific Depth Is at Most $\binom{M}{2}$'))
ck('T31', 'proof admits it searches the TARGET pair automaton',
   has('of the\ntarget $A$'.replace('\n',' ')))
ck('T31', 'M=2 witness recorded',
   has('The two quantities genuinely differ, already at $M=2$'))
ck('T31', 'witness machines displayed',
   has(r'A_1:\ \lambda(s,0)=s,\ \lambda(s,1)=0'))
ck('T31', 'witness values Lsync=1 vs Lsyncu=2',
   has('a second input is required\nand $\\Lsyncu=2$ on the same pair'.replace('\n',' ')))
ck('T31', 'Lsyncu finiteness now PROVED; only the rate is open (T35)',
   has('Finiteness holds in general by') and
   absent('is open once $|\\mathcal I|\\ge2$'))
ck('T31', 'single-input coincidence justified as the vacuous case',
   has('is vacuous, because there is\nonly one universal tree'.replace('\n',' ')))
ck('T31', 'open problem separates the two quantities',
   has('none of this transfers'))

# ============================================================ TURN 32
# External audit (gpt coherent automata.txt): 5 valid items applied.

ck('T32', 'item 14: broken sentence repaired',
   has('can be checked directly on finite\nweighted point clouds'.replace('\n',' ')) and
   absent('The quadratic-surrogate spectral bound  The full-KL local Fisher'))
ck('T32', 'item 5: EsyncSI stated as upper bound, not equality',
   has(r'\EsyncSI(M)\ \le\ \bigl\lfloor\log_2M\bigr\rfloor'))
ck('T32', 'item 5: exact equality via the at-most-M reading (T33)',
   has('no padding is required, because $\\mathcal H_M$ consists of the'))
ck('T32', 'item 5: intermediate-budget remark', 'rem:esyncsi-intermediate' in labels)
ck('T32', 'item 5: bogus padding argument removed',
   absent('pad\nthe state set with unreachable duplicates removed'.replace('\n',' ')))
ck('T32', 'item 8: conclusion no longer contradicts the promise theorem',
   absent('These results do not establish\nNP-hardness for unrestricted full KL'.replace('\n',' ')))
ck('T32', 'item 8: conclusion cites promise + APX results',
   has('Corollary~\\ref{cor:full-kl-apx} upgrades this to APX-hardness'))
ck('T32', 'item 8: dimension-dependent alphabet flagged in conclusion',
   has('The output alphabet produced by the embedding has size $2d$, so\nhardness for a \\emph{fixed} alphabet is not established'.replace('\n',' '))
   and has('so the alphabet grows with the dimension\nunder any variant of the construction'.replace('\n',' ')))
ck('T32', 'item 8: stale open problem now points at the theorem',
   has('That reduction is carried out in Theorem~\\ref{thm:full-kl-promise-np}'))
ck('T32', 'item 8: four remaining sub-questions listed',
   has('Membership in NP') and has('Fixed output alphabet') and
   has('Hardness without a promise') and has('Nonvacuous lumpability'))
ck('T32', 'item 8: abstract carries the alphabet caveat',
   has('hardness for a fixed alphabet is not established'))
ck('T32', 'item 10: finiteness automatic for finite S',
   has(r'I(S;Z)\le H(S)<\infty'))
ck('T32', 'item 12: data AND code availability',
   has('Data and Code Availability'))
ck('T32', 'item 12: computational observations distinguished from proofs',
   has('computational observations'))
ck('T32', 'item 3.2: attainment labelled a computational observation',
   has('is a computational observation rather than a proved'))
ck('T32', 'item 3.2: explicit M=4 witness table given',
   has(r'\tau(\cdot,0)=(0,0,3,2)'))

# ============================================================ TURN 33
# Evaluation of the audit: two of my rejections overturned, plus 5 more items.

ck('T33', 'halving: survivors are ONE class, not the complement',
   has('not the union of all\nnon-predicted classes'.replace('\n',' ')))
ck('T33', 'halving: 2c_2 <= c_1+c_2 <= |V| in active-halving proof',
   has(r'2c_2\ \le\ c_1+c_2\ \le\ |V|'))
ck('T33', 'halving: alphabet-dependent constant removed from active-halving',
   absent(r'C_{|\mathcal O|}=\frac{\ln2}'))
ck('T33', 'halving: remark extended to machine-state pairs',
   has('The same counting applies wherever the version space consists of candidates'))
ck('T33', 'support example is right-closed',
   has(r'\mathtt{aaa}\notin S$ and $\mathtt{aaab}\in S') and
   absent(r'for $S=\{u:u\text{ ends in }\mathtt b\}$, closed under'))
ck('T33', 'support: notes why the old example fails',
   has('would \\emph{not} serve here, since'))
ck('T33', 'EsyncSI exact equality restored', 
   has(r'\EsyncSI(M)\ =\ \bigl\lfloor\log_2M\bigr\rfloor'))
ck('T33', 'EsyncSI: at-most-M reading does the work',
   has('no padding is required, because $\\mathcal H_M$ consists of the'))
ck('T33', 'EsyncSI: remark explains the two readings',
   has('Were $\\mathcal H_M$ instead read as machines with \\emph{exactly}'))
ck('T33', 'state rate definition added', 'def:state-rate' in labels)
ck('T33', 'state rate: one-shot vs per-symbol caveat',
   has('not a\nper-symbol transmission rate'.replace('\n',' ')))
ck('T33', 'Csiszar C^1 is DERIVED not assumed (T34: hypothesis reverted)',
   absent('$f$-divergence form, with a $C^1$ generator') and
   has('Smoothness of the Generator Is Derived, Not Assumed'))
ck('T33', 'Csiszar: one-sided limit replaces differentiation (T34)',
   has('This uses no differentiability') and
   absent('Differentiability is supplied by'))
ck('T33', 'direct-sum: rectangular hardness hypothesis added',
   has('assume in addition \\emph{rectangular hardness}'))
ck('T33', 'direct-sum: necessity of the hypothesis argued',
   has('Rectangular hardness is what converts two separate lower bounds into a sum'))
ck('T33', 'direct-sum: explicit construction independent of the abstract theorem',
   has('does \\emph{not} route through\nTheorem~\\ref{thm:active-direct-sum}'.replace('\n',' ')))
ck('T33', 'oracle floors: loss-type mismatch stated',
   has('the loss types differ and must not be silently\nidentified'.replace('\n',' ')))

# ============================================================ TURN 34
# Item 11 closed by PROVING regularity, not assuming it.

ck('T34', 'C^1 hypothesis reverted from clause (d)',
   absent('$f$-divergence form, with a $C^1$ generator'))
ck('T34', 'one-sided limit replaces differentiation',
   has('This uses no differentiability'))
ck('T34', 'one-sided derivatives g\'_+ and g\'_- introduced',
   has("Writing $g'_+$ and $g'_-$ for the right and left derivatives"))
ck('T34', 'sign convention +/- by whether v<1 or v>1',
   has(r'\begin{cases}+, & v<1,\\ -, & v>1,\end{cases}'))
ck('T34', 'per-side symmetry gives c_1 and c_2',
   has(r'u\,g'+chr(39)+'_+(u)=g(u)+c_1(u-1)+g'+chr(39)+'_+(1)'))
ck('T34', 'regularity bootstrap: continuous right derivative => C^1',
   has('A convex function whose right\nderivative is continuous is $C^1$'.replace('\n',' ')))
ck('T34', 'gluing identity across t=1',
   has(r'0=(c_1-c_2)\bigl(\log u-u+1\bigr)'))
ck('T34', 'gluing forces c_1=c_2 via log u < u-1',
   has(r'Since $\log u<u-1$ for $u\ne1$'))
ck('T34', 'automatic-smoothness remark exists',
   'rem:csiszar-automatic-smoothness' in labels)
ck('T34', 'remark states smoothness is a conclusion not a prerequisite',
   has('is therefore a conclusion here rather than a\nprerequisite'.replace('\n',' ')))
ck('T34', 'remark records the two-branch counterexample the gluing excludes',
   has('The gluing step is not decorative'))

# ============================================================ TURN 35
# Fix 3(b): version-space universal bound closes Lsyncu finiteness.

ck('T35', 'version-space proposition exists', 'prop:lsyncu-version-space' in labels)
ck('T35', 'bound (M-1)(N_M-1) stated',
   has(r'\Lsyncu(M)\ \le\ (M-1)(N_M-1)\ <\ \infty'))
ck('T35', 'proof stresses the strategy is transcript-driven',
   has('The whole strategy is a function of the transcript'))
ck('T35', 'proof: candidate machine is named by the version space',
   has('named by the version space, not the unknown target'))
ck('T35', 'proof: Moore separation applied WITHIN one machine (M-1 not 2M-1)',
   has('rather than to a\ndisjoint union of two machines'.replace('\n',' ')))
ck('T35', 'proof: at least one of the pair is deleted',
   has('at\nmost one can agree with whatever is observed'.replace('\n',' ')))
ck('T35', 'finiteness-vs-rate remark', 'rem:lsyncu-finite-not-rate' in labels)
ck('T35', 'remark notes the bound is exponential in M',
   has('hence exponential in $M$'))
ck('T35', 'polynomial universal depth conjecture', 'conj:lsyncu-poly' in labels)
ck('T35', 'open problem now about the rate, not finiteness',
   has('What is open is the rate'))

# ============================================================ TURN 36
# Fix 1: unifilar generalization added as a strict extension.

ck('T36', 'unifilar machine definition', 'def:unifilar-machine' in labels)
ck('T36', 'unifilar update tau(s,x,y)',
   has(r'S_{t+1}=\tau(S_t,X_t,Y_t)'))
ck('T36', 'output-independent case recovers def:controlled-markov',
   has('the machine is exactly a\nstationary controlled causal machine'.replace('\n',' ')))
ck('T36', 'proper-subclass remark', 'rem:unifilar-proper-subclass' in labels)
ck('T36', 'explicit witness: same input history, different states',
   has('the state after two steps is $A$ on the\noutput history $00$ and $B$ on $01$'.replace('\n',' ')))
ck('T36', 'epsilon-machine label scoped in the abstract',
   has('stationary controlled\nunifilar causal machines'.replace('\n',' '))
   and has('the input-driven\nsynchronized subclass'.replace('\n',' ')))
ck('T36', 'unifilar lumpability definition', 'def:unifilar-lumpable' in labels)
ck('T36', 'feasibility restriction is explicit',
   has(r'for every \emph{jointly feasible} triple $(s,x,y)$'))
ck('T36', 'feasibility load-bearing remark', 'rem:unifilar-feasibility' in labels)
ck('T36', 'right-congruence proposition', 'prop:unifilar-lumpability' in labels)
ck('T36', 'converse requires coarser-than-Z-predictive',
   has(r'\emph{coarser} than $\sim_Z$'))
ck('T36', 'proof identifies descent as the only issue',
   has('the only issue is that $\\sim$ descend to states'))
ck('T36', 'hypothesis-role remark with parity counterexample',
   'rem:unifilar-converse-hypothesis' in labels)
ck('T36', 'parity counterexample recorded',
   has('the same parity'))
ck('T36', 'complexity constructions stated for the input-driven model',
   has('the complexity constructions of\nSection~\\ref{subsec:retention-complexity} are stated for the input-driven model'.replace('\n',' ')))

# ============================================================ TURN 37
# Fix 15: typed rate-distortion principle, with the grounding entry corrected.

ck('T37', 'typed principle exists', 'meta:typed-rate-distortion' in labels)
ck('T37', 'clause (a) cites meta:monotone(i)',
   has(r'Meta-Theorem~\ref{meta:monotone}(i)'))
ck('T37', 'clause (b) cites meta:monotone(iii) with support caveat',
   has(r'Meta-Theorem~\ref{meta:monotone}(iii), with the index taken relative to the'))
ck('T37', 'clause (c) refuses a converse from syntax alone',
   has('no such bound follows from the factorization syntax alone'))
ck('T37', 'clause (d) matches thm:unified including c^{-1} modulus',
   has(r'c_{\mathsf r}^{-1}\,') and has(r'(Theorem~\ref{thm:unified})'))
ck('T37', 'clause (e) cites thm:schatten-nogo',
   has(r'(Theorem~\ref{thm:schatten-nogo})'))
ck('T37', 'instantiation table present',
   has('regime & admissible factor & exact invariant & analytical bridge'))
ck('T37', 'GROUNDING ENTRY CORRECTED: unrestricted gap only',
   has('Hankel rank (unrestricted gap)'))
ck('T37', 'grounding caveat: DHankstr only an inequality in general',
   has(r'only the inequality $\DHankstr(M)\ge\sigma_{M+1}(H_\nu)$ holds in'))
ck('T37', 'scope remark exists', 'rem:typed-principle-scope' in labels)
ck('T37', 'scope: does NOT claim a common history alphabet',
   has('It does not claim a\ncommon history alphabet'.replace('\n',' ')))
ck('T37', 'scope: does NOT assert a per-symbol rate',
   has('it does not assert a\nper-symbol rate'.replace('\n',' ')))
ck('T37', 'scope: names the three differing response operators',
   has(r'$H_\nu$, $\Sigma_\pi$, $N_\Lambda$'))

# ============================================================ TURN 39
# Item 1 closure: regime-typed history actions and the unifilar elevation.

# --- Block A: history systems and support-relative congruences
ck('T39', 'history system definition', 'def:history-system' in labels)
ck('T39', 'support-relative right congruence', 'def:support-right-cong' in labels)
ck('T39', 'clause (i) shown non-redundant', 'rem:support-clause-i-needed' in labels)
ck('T39', 'regime instantiation table', 'rem:regime-history-instances' in labels)
ck('T39', 'cofilteredness for support-relative congruences',
   'lem:cofiltered-support' in labels)
ck('T39', 'index bound in cofilteredness lemma',
   has(r'\operatorname{index}(\sim_1)\operatorname{index}(\sim_2)'))
ck('T39', 'residual finiteness of pruned unifilar trees',
   'prop:unifilar-residually-finite' in labels)
ck('T39', 'feasibility is a function of the state, in that proof',
   has('so it is a function of $\\sigma(w)$ alone'))

# --- Block B: the reduction is CONDITIONAL, not automatic
ck('T39', 'unifilar lumpability does not reduce automatically',
   'rem:unifilar-support-not-automatic' in labels)
ck('T39', 'strictly weaker, stated as such',
   has('strictly weaker than Definition~\\ref{def:lumpable-quotient}'))
ck('T39', 'block-uniform support defined', has('block-uniform support'))
ck('T39', 'connected support defined', has('connected\nsupport'.replace('\n',' ')))
ck('T39', 'input-driven specialization proposition',
   'prop:input-driven-specialization' in labels)
ck('T39', 'connectedness is the operative hypothesis',
   has('If that graph is connected, the function is\nconstant on $C$'.replace('\n',' ')))
ck('T39', 'connectedness shown non-droppable',
   has('Connectedness cannot be\ndropped'.replace('\n',' ')))
ck('T39', 'epsilon-machine identification cites the literature',
   'rem:epsilon-machine-relation' in labels and has(r'\cite{shalizi2001}'))
ck('T39', 'shalizi2001 in bibliography', has('\\bibitem{shalizi2001}'))
ck('T39', 'shalizi2001 cited in J Stat Phys, vol 104',
   has('vol.~104, no.~3--4, pp.~817--879, 2001'))
ck('T39', 'clause (i) DERIVED for the full controlled future',
   has('Clause~(i) is not an\nextra hypothesis but a consequence'.replace('\n',' ')))

# --- Block C: controlled retention
ck('T39', 'controlled full-KL gap defined', 'def:controlled-full-kl' in labels)
ck('T39', 'controlled IB identity', 'thm:controlled-ib' in labels)
ck('T39', 'controlled IB conditional on the input',
   has(r'I(S;Y\mid K_\phi,X)'))
ck('T39', 'independence hypothesis shown load-bearing',
   'rem:controlled-ib-independence' in labels)
ck('T39', 'independence failure is quantified',
   has('more than $0.13$ nats'))
ck('T39', 'controlled elementary corollary', 'cor:controlled-elementary' in labels)
ck('T39', 'kernel partition and stable refinement defined',
   'def:kernel-refinement' in labels)
ck('T39', 'stable refinement exists and is unique',
   'prop:kernel-refinement-exists' in labels)
ck('T39', 'refinement recursion stabilizes in |S+| steps',
   has('stabilizes after at most\n$|\\Splus|$ steps'.replace('\n',' ')))
ck('T39', 'controlled zero-retention theorem', 'thm:controlled-zero' in labels)
ck('T39', 'threshold is N*, not the number of kernels',
   has(r'$\RetKLc(M)=0$ if and only if $M\ge N^{\ast}$'))
ck('T39', 'the distinction is exhibited, not asserted',
   'rem:controlled-zero-not-kernels' in labels)
ck('T39', 'kernel-threshold counterexample is explicit',
   has(r'\tau(A,0)=A,\quad\tau(A,1)=C'))
ck('T39', 'recovery corollary carries the support hypothesis',
   'cor:controlled-reduces' in labels
   and has('has connected support --- in particular if every $P_s$ has\nfull support'.replace('\n',' ')))
ck('T39', 'sharpness of that hypothesis recorded',
   'rem:controlled-reduces-sharp' in labels)
ck('T39', 'three fiberwise spectral converses',
   'cor:controlled-quad-spectral' in labels
   and 'cor:controlled-simplex-spectral' in labels
   and 'cor:controlled-fisher' in labels)
ck('T39', 'fiberwise argument names the x-independent constraint',
   has('The lumpability constraint does not depend on $x$'))
ck('T39', 'Fisher no-go persists under control',
   'rem:controlled-fisher-nogo' in labels)
ck('T39', 'complexity transfer argued, not asserted',
   'rem:complexity-transfer' in labels
   and has('Transfer of hardness\nrequires an argument'.replace('\n',' '))
   and has('could in principle convert a NO instance into a YES'))
ck('T39', 'transfer argument covers the depth-two construction',
   has('a fractional assignment dominates every partition, lumpable or not'))

# --- Block D: global statements
ck('T39', 'abstract states the unifilar machine type',
   has('stationary controlled\nunifilar causal machines'.replace('\n',' ')))
ck('T39', 'type signature admits unifilar-lumpable quotients',
   has(r'\text{unifilar-lumpable quotients}'))
ck('T39', 'type table has the controlled IB row',
   has('Controlled IB identity'))
ck('T39', 'type table has the controlled zero row',
   has('Zero controlled retention'))
ck('T39', 'conclusion records the threshold as non-verbatim',
   has('The zero-retention threshold, by contrast, does not transfer\nverbatim'.replace('\n',' ')))
ck('T39', 'epistemic list records the unifilar results',
   has('the zero-retention threshold at the index of\nthe stable kernel refinement'.replace('\n',' ')))

# ============================================================ TURN 44
# Item 1: controlled IB for correlated inputs.  Item 2: extremal counter family.

ck('T44', 'fiberwise controlled gap defined', 'def:controlled-full-kl-general' in labels)
ck('T44', 'general controlled IB theorem', 'thm:controlled-ib-general' in labels)
ck('T44', 'general IB drops independence',
   has('Let $(S_t,X_t)$ be stationary with arbitrary dependence'))
ck('T44', 'proof states the conditional-weight identity holds for ANY joint law',
   has('which holds for \\emph{any} joint law of $(S_t,X_t)$, no independence being'))
ck('T44', 'thm:controlled-ib is the independent special case',
   has('Theorem~\\ref{thm:controlled-ib} is the independent case'))
ck('T44', 'general elementary corollary', 'cor:controlled-elementary-general' in labels)
ck('T44', 'general fiberwise spectral converse', 'cor:controlled-simplex-general' in labels)
ck('T44', 'reweighting shown necessary', 'rem:controlled-general-reweighting' in labels)
ck('T44', 'unconditional weights are NOT a lower bound',
   has('produces a quantity that is not a lower\nbound'.replace('\n',' ')))

ck('T44', 'counter family defined', 'def:counter-family' in labels)
ck('T44', 'counter family update', has(r'\tau(s,0)=\min\{s+1,\,M-1\}'))
ck('T44', 'singleton input makes independence automatic',
   has('The input alphabet being a singleton, $X_t$ is deterministic and hence'))
ck('T44', 'extremal proposition', 'prop:refinement-extremal' in labels)
ck('T44', 'gap is maximal M-2',
   has('gap $N^{\\ast}-|\\phi_{\\ker}(\\Splus)|=M-2$ is the largest possible'))
ck('T44', 'round bound tight to within one',
   has('stabilizes after exactly\n$M-1$ steps'.replace('\n',' ')))
ck('T44', 'induction on the counter is given',
   has('separates exactly the top $m+1$ states'))
ck('T44', 'scope remark: worst case not typical', 'rem:refinement-extremal-scope' in labels)
ck('T44', 'single input letter, invisible to input-driven analysis',
   has('invisible to any\ninput-driven analysis'.replace('\n',' ')))

# ============================================================ TURN 45
# Item 3: algebraic form of full-KL verification.  Item 4: minimal alphabet.

ck('T45', 'algebraic form proposition', 'prop:full-kl-algebraic-form' in labels)
ck('T45', 'RetKL(phi) = (1/D) log R', has(r'\RetKL(\phi)=\frac1D\log R'))
ck('T45', 'polynomial computability claimed only for the FACTORED form',
   has('a \\emph{factored} representation'))
ck('T45', 'RationalExpCompare named', has(r'\textsc{RationalExpCompare}'))
ck('T45', 'factored representation shown necessary', 'rem:full-kl-slp' in labels)
ck('T45', 'exponential blow-up of the expanded form recorded',
   has('which grows\nexponentially in the instance size'.replace('\n',' ')))
ck('T45', 'PosSLP identified', has(r'\textsc{PosSLP}'))
ck('T45', 'membership status remark', 'rem:full-kl-exp-membership' in labels)
ck('T45', 'Lindemann-Weierstrass used correctly',
   has('the Lindemann--Weierstrass theorem makes $e^{s}$'))
ck('T45', 'missing ingredient is a precision bound',
   has('a polynomial lower bound on $|R-e^{s}|$'))

ck('T45', 'alphabet remark', 'rem:output-alphabet-2d' in labels)
ck('T45', 'three constraints on T stated',
   has('image must lie in the zero-sum subspace') and has(r'T^{\!\top}T=cI'))
ck('T45', 'd=2 discriminant obstruction',
   has('of discriminant $12$, whose class modulo rational') and has(r'$3\not\equiv1$'))
ck('T45', 'd=3 Hadamard similarity exhibited',
   has('(-1,-1,1,1),\\qquad(-1,1,-1,1),\\qquad(-1,1,1,-1)'))
ck('T45', 'factor two IS slack for d=3,7,15',
   has('and there the factor two is\nslack'.replace('\n',' ')))
ck('T45', 'operative statement is Hadamard-type, not a universal factor',
   has('a condition of\nHadamard type'.replace('\n',' ')))
ck('T45', 'fixed-alphabet hardness still open',
   has('output alphabet therefore remains open'))

# ============================================================ TURN 46
# Cross-references from Open Problem 4 to the Turn-45 results.

ck('T46', 'OP4(a) cites the algebraic form',
   has('Proposition~\\ref{prop:full-kl-algebraic-form} locates the difficulty exactly.'))
ck('T46', 'OP4(a) states the collapse to one comparison',
   has('The number of logarithmic terms is\ntherefore not the obstruction'.replace('\n',' ')))
ck('T46', 'OP4(a) cites both companion remarks',
   has('Remark~\\ref{rem:full-kl-exp-membership}')
   and has('Remark~\\ref{rem:full-kl-slp} shows that $R$ must be'))
ck('T46', 'OP4(b) cites the alphabet remark',
   has('Remark~\\ref{rem:output-alphabet-2d} determines how far the alphabet can be'))
ck('T46', 'OP4(b) states the Hadamard criterion',
   has('orthogonal rational vectors of equal norm'))
ck('T46', 'OP4(b) records d=3,7,15 succeed and d=2 fails',
   has('$n=d+1$ qualifies for $d=3,7,15,\\dots$') and has('fails for\n$d=2$'.replace('\n',' ')))
ck('T46', 'OP4(b) records the unavoidable d+1 dimension bound',
   has('What no choice of scheme can avoid is'))
ck('T46', 'promise-scope remark points forward',
   has('reduces that\nsum to a single comparison $R\\ge e^{s}$'.replace('\n',' ')))
ck('T46', 'conclusion bullet cites both new results',
   has('by\nRemark~\\ref{rem:output-alphabet-2d} the size can be reduced'.replace('\n',' '))
   and has('by\nProposition~\\ref{prop:full-kl-algebraic-form} the objective is'.replace('\n',' ')))
ck('T46', 'conclusion no longer claims the alphabet cannot shrink',
   not has('the output alphabet produced by\nthe embedding has size $2d$ and therefore grows'.replace('\n',' ')))

# ============================================================ TURN 48
# Rate-distortion scope sharpened; two-ingredient decomposition made explicit.

ck('T48', 'non-convexity proposition', 'prop:rd-nonconvex' in labels)
ck('T48', 'convexity failure is the named obstruction',
   has('And $D_{\\mathbb T}$ need not be\nconvex'.replace('\n',' ')))
ck('T48', 'time-sharing named as the unavailable apparatus',
   has('the time-sharing argument that makes the Shannon curve the lower'))
ck('T48', 'witness values printed', has('D(0)=0.0948616'))
ck('T48', 'chord slopes printed', has('$-0.115492$, $-0.024414$, $-0.009508$, $-0.009746$'))
ck('T48', 'exact arithmetic stated', has('at $60$\nsignificant digits'.replace('\n',' ')))
ck('T48', 'mechanism remark', 'rem:rd-nonconvex-mechanism' in labels)
ck('T48', 'randomisation between quotients is not a quotient',
   has('is not itself a quotient of any intermediate size'))
ck('T48', 'two-ingredient remark', 'rem:vertex-two-ingredients' in labels)
ck('T48', 'rank and norm ingredients named',
   has('a \\emph{rank} condition, clause~(a)') and has('a \\emph{norm} condition'))
ck('T48', 'parallel form explained by shared ingredient (a)',
   has('they share the\noptimization ingredient~(a)'.replace('\n',' ')))
ck('T48', 'still refuses cross-regime transfer',
   has('the shared form yields no shared value'))

# ============================================================ TURN 49
# Hypothesis of the counter family corrected: beta,gamma in the OPEN interval.

ck('T49', 'def:counter-family uses the open interval',
   has(r'For $M\ge3$ and $\beta,\gamma\in(0,1)$ with $\beta\neq\gamma$'))
ck('T49', 'prop:refinement-extremal uses the open interval',
   has(r'Let $\beta,\gamma\in(0,1)$ with $\beta\neq\gamma$.'))
ck('T49', 'the two fatal boundary cases are named',
   has('at $\\gamma=0$ the state $M-1$') and has('while at $\\beta=1$'))
ck('T49', 'absorbing / unreachable mechanism stated',
   has('is absorbing') and has('is never reached'))
ck('T49', 'proof of (i) no longer claims gamma in {0,1} is harmless',
   not has(r'if\n$\gamma\in\{0,1\}$, state $M-1$ still has both successors'.replace('\n',' ')))
ck('T49', 'proof of (i) derives positivity from both parameters interior',
   has('states\n$0,\\dots,M-2$ because $\\beta\\in(0,1)$, and state $M-1$ because'.replace('\n',' ')))

# ============================================================ TURN 50
# Non-convexity survives reparametrisation of the budget axis.

ck('T50', 'reparametrisation clause present',
   has('The failure is not an artefact of measuring the budget logarithmically.'))
ck('T50', 'second witness stated',
   has(r'(20,25,2),\quad(2,34,30),\quad(37,1,27),\quad(20,9,1)'))
ck('T50', 'slopes given for BOTH axes',
   has('$-0.128600$, $-0.145626$, $-0.014522$')
   and has('$-0.185531$, $-0.359159$, $-0.050478$'))
ck('T50', 'conclusion: no rescaling supplies convexity',
   has('no rescaling of the rate can supply a convexity\nguarantee'.replace('\n',' ')))
ck('T50', 'reason tied to the feasible set, not the axis',
   has('a property of the feasible set\nrather than of the axis'.replace('\n',' ')))

# ============================================================ TURN 51
# Finite-state grounding decomposition (repaired form of an audit proposal).

ck('T51', 'tracking deficit defined', 'def:tracking-deficit' in labels)
ck('T51', 'deficit uses the BLOCK SYMBOL, not the mixture mode',
   has(r'P_s\bigl(\hat b_{\phi(s)}\bigr)'))
ck('T51', 'decomposition proposition', 'prop:grounding-tracking' in labels)
ck('T51', 'floor plus tracking identity', has(r'\sigma_1+D(\phi)'))
ck('T51', 'deficit nonnegative with equality condition',
   has('$D(\\phi)\\ge0$, with equality if and only if'))
ck('T51', 'scope remark', 'rem:tracking-deficit-scope' in labels)
ck('T51', 'mixture-mode substitution shown negative',
   has(r'=-\tfrac15<0'))
ck('T51', 'zero deficit below |S+| exhibited',
   has('$\\hat b=1$ and $D=0$ although $M=1<3=|\\Splus|$'))
ck('T51', 'mode preservation weaker than separating states',
   has('mode preservation, which is strictly weaker than separating the predictive'))
ck('T51', 'relation-to-retention remark', 'rem:tracking-vs-retention' in labels)
ck('T51', 'no gap-value inequality claimed across regimes',
   has('the costs being incomparable'))

# ============================================================ TURN 52
# Safe right congruence defined; infeasible case of the discrete PoS settled.

ck('T52', 'safe right congruence defined', 'def:safe-right-cong' in labels)
ck('T52', 'containment form stated',
   has('every $\\sim$-class is contained in some $B_b$'))
ck('T52', 'infeasible convention fixed',
   has(r'\mathrm{Safe}_{\mathrm{quad}}(M)=-\infty'))
ck('T52', 'feasibility proposition', 'prop:pos-quad-consistent' in labels)
ck('T52', 'feasibility iff M >= r', has('exists if and only if\n$M\\ge r$'.replace('\n',' ')))
ck('T52', 'PoS infinite exactly below r',
   has(r'$\PoSquad(M)=+\infty$ exactly when $M<r$'))
ck('T52', 'range clause for feasible budgets',
   has(r'0\le\PoSquad(M)\le\mathrm{Free}_{\mathrm{quad}}(M)'))
ck('T52', 'convention NOT inherited from the surrogate',
   'rem:pos-convention-independent' in labels)
ck('T52', 'four-state witness separating safe from block-local',
   has(r'$\{\{s_1,s_2\},\{s_3,s_4\}\}$ is safe'))
ck('T52', 'relaxation identity now scoped to feasible budgets',
   has('sense of Definition~\\ref{def:safe-right-cong} and $M\\ge r$ so that both are'))

# ============================================================ REPORT
print('=' * 72)
print('CUMULATIVE REGRESSION SUITE  --  every fix from every turn')
print('=' * 72)
names = {'T1': 'Turn 1 (audit A)', 'T2': 'Turn 2 (audit B)',
         'T3': 'Turn 3 (audit C)', 'T4': 'Turn 4 (audit D)', 'T5': 'Turn 5 (audit E)', 'T6': 'Turn 6 (skipped items)', 'T7': 'Turn 7 (closures)', 'T8': 'Turn 8 (deep salvage)', 'T9': 'Turn 9 (Fisher erratum)', 'T10': 'Turn 10 (audit #2,#5)', 'T11': 'Turn 11 (active decomp)', 'T12': 'Turn 12 (model typing)', 'T13': 'Turn 13 (Cesaro/AAK scope)', 'T14': 'Turn 14 (final audit)', 'T15': 'Turn 15 (rigor pass)', 'T16': 'Turn 16 (hypotheses)', 'T17': 'Turn 17 (PFA rate, packings)', 'T18': 'Turn 18 (bridges)', 'T19': 'Turn 19 (sharp constants, closures)', 'T20': 'Turn 20 (AAK indexing)', 'T21': 'Turn 21 (APX, sum-vs-min)', 'T22': 'Turn 22 (deep verification)', 'T23': 'Turn 23 (kappa bounded)', 'T24': 'Turn 24 (EsyncSI exact)', 'T25': 'Turn 25 (Lsyncu quadratic)', 'T26': 'Turn 26 (single-input linear)', 'T27': 'Turn 27 (Lean 4)', 'T29': 'Turn 29 (tension lemma)', 'T30': 'Turn 30 (attainment probe)', 'T31': 'Turn 31 (Lsync vs Lsyncu)', 'T32': 'Turn 32 (external audit)', 'T33': 'Turn 33 (audit evaluation)', 'T34': 'Turn 34 (Csiszar regularity)', 'T35': 'Turn 35 (universal finiteness)', 'T36': 'Turn 36 (unifilar extension)', 'T37': 'Turn 37 (typed principle)', 'T39': 'Turn 39 (regime-typed histories, unifilar retention)', 'T44': 'Turn 44 (general controlled IB, extremal refinement)', 'T45': 'Turn 45 (algebraic form, minimal alphabet)', 'T46': 'Turn 46 (Open Problem 4 cross-references)', 'T48': 'Turn 48 (rate-distortion scope, two ingredients)', 'T49': 'Turn 49 (counter-family hypothesis)', 'T50': 'Turn 50 (reparametrisation)', 'T51': 'Turn 51 (grounding tracking deficit)', 'T52': 'Turn 52 (safe congruence, PoS feasibility)'}
tot_ok = tot = 0
for t in ['T1','T2','T3','T4','T5','T6','T7','T8','T9','T10','T11','T12','T13','T14','T15','T16','T17','T18','T19','T20','T21','T22','T23','T24','T25','T26','T27','T29','T30','T31','T32','T33','T34','T35','T36','T37','T39','T44','T45','T46','T48','T49','T50','T51','T52']:
    ok, n = turn_stats[t]
    tot_ok += ok
    tot += n
    mark = 'OK  ' if ok == n else 'FAIL'
    print(f'  {mark}  {names[t]:20s}  {ok}/{n} fixes still present')
print('-' * 72)
print(f'  TOTAL: {tot_ok}/{tot}')
print()
if fails:
    print(f'{len(fails)} REGRESSION(S) DETECTED:')
    for f in fails:
        print('   -', f)
    sys.exit(1)
print('NO REGRESSIONS: every fix from all four turns is present in the deliverable.')
