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
Traceability audit: did every verification script produce a manuscript change?

For each verify/*.py, look for the manuscript artefact it was written to
support. Report LANDED / NOT LANDED so the answer is evidence, not assertion.
"""
import io
import os
import re

tex = io.open(_p('automata_corrected.tex'), encoding='utf-8',
              newline='').read().replace('\r\n', '\n')
flat = ' '.join(tex.split())
labels = set(re.findall(r'\\label\{([^}]*)\}', tex))

# script -> (what it verified, manuscript artefact that must exist)
TRACE = [
 ('chain.py',            'c-chaining breaks product structure',
                         lambda: 'rem:gating-needed' in labels and '3\\cdot4\\cdot4\\cdot4=192' in flat),
 ('gated_minimax.py',    'gated family forces M log M',
                         lambda: 'def:gated-active-family' in labels),
 ('sandwich.py',         'discrete bias-variance sandwich',
                         lambda: 'lem:discrete-bv-sandwich' in labels),
 ('sepword.py',          'separating word across two machines',
                         lambda: 'lem:moore-separation' in labels),
 ('stateless.py',        'stateless game: one-stage vs discounted',
                         lambda: 'm_1-m_2' in flat.replace(' ', '')),
 ('possign.py',          'rho_safe can be negative',
                         lambda: '\\rho_{\\mathrm{safe}}(2)=-\\tfrac14' in flat),
 ('counterex3.py',       'c_S = 1 counterexample',
                         lambda: 'rem:support-extension-sharp' in labels),
 ('klspectral.py',       'global KL simplex converse',
                         lambda: 'thm:global-kl-simplex' in labels),
 ('restriction.py',      'direct-sum restriction needs product structure',
                         lambda: '\\textbf{product structure}' in flat),
 ('halving.py',          'active halving attains RI in O(M log M)',
                         lambda: 'thm:active-halving' in labels),
 ('counting.py',         'class count / Littlestone proof',
                         lambda: 'lem:littlestone' in labels and 'Every shattered set yields a shattered tree' in flat),
 ('ptozero.py',          'p->0 limit is not the Boolean vertex',
                         lambda: 'rem:p-to-zero' in labels),
 ('fisher.py',           'Fisher no-go was FALSE',
                         lambda: 'prop:bernoulli-fisher-scales' in labels and 'thm:no-global-kl-converse' not in labels),
 ('monotone.py',         'reflexivity axiom needed',
                         lambda: 'cost profunctor which is \\textbf{reflexive}' in flat),
 ('stateless2.py',       'cor:stateless survives the controller model',
                         lambda: 'def:pio-controller' in labels),
 ('interior_fisher.py',  'interior Fisher converse (first, falsified)',
                         lambda: 'thm:global-interior-fisher' in labels),
 ('interior2.py',        'interior Fisher converse (corrected m_K)',
                         lambda: 'and the parameters of all their mixture centroids' in flat),
 ('csiszar_onesided.py', 'one-sided limits valid for kinked convex g',
                         lambda: 'This uses no differentiability' in flat),
 ('csiszar_bootstrap.py','kinked generators break (dagger); bootstrap constant',
                         lambda: 'rem:csiszar-automatic-smoothness' in labels),
 ('csiszar_glue.py',     'two-branch c1!=c2 excluded only by gluing',
                         lambda: 'The gluing step is not decorative' in flat),
 ('csiszar_defect.py',   'product additivity does NOT pin the generator '
                         '(reverse KL is a counterexample)',
                         lambda: 'Product additivity is not enough' in flat),
 ('csiszar_repair.py',   'exact conditional chain-rule identity selects t log t',
                         lambda: "\\sum_jq'_j\\,g(u\\,t_j) = g(u)+u\\sum_jq'_j\\,g(t_j)" in flat),
 ('sharp_constant.py',   'global simplex converse has sharp constant 1',
                         lambda: 'prop:kl-simplex-sharp' in labels),
 ('fisher_nogo.py',      'no universal Fisher-chart constant',
                         lambda: 'thm:no-global-fisher-converse' in labels),
 ('esyncsi_lower.py',    'EsyncSI = Theta(log M), matching lower bound',
                         lambda: 'thm:esyncsi-theta' in labels),
 ('kmeans_js2.py',       'full-KL promise NP-hardness via JS embedding',
                         lambda: 'thm:full-kl-promise-np' in labels),
 ('hessian_factor.py',   'negentropy Hessian factor d in the JS expansion',
                         lambda: '|\\rho_C|\\ \\le\\ C_0\\,d^{2}\\delta^{3}Z^{3}' in flat),
 ('esyncsi.py',          'EsyncSI = O(log M)',
                         lambda: 'prop:esyncsi-log' in labels),
 ('unifilar_scope.py',   'input-driven model is a proper subclass',
                         lambda: 'rem:unifilar-proper-subclass' in labels),
 ('unifilar_lump.py',    'unifilar lumpability => right congruence; feasibility essential',
                         lambda: 'rem:unifilar-feasibility' in labels),
 ('unifilar_descent.py', 'converse descends only under the coarseness hypothesis',
                         lambda: 'rem:unifilar-converse-hypothesis' in labels),
 ('unifilar_lump_vs_lump.py',
                         'unifilar lumpability is strictly weaker for input-driven machines',
                         lambda: 'rem:unifilar-support-not-automatic' in labels),
 ('unifilar_reduction_gap2.py',
                         'the enlarged feasible set strictly lowers the retention value',
                         lambda: 'rem:controlled-reduces-sharp' in labels),
 ('unifilar_witness_check.py',
                         'both printed witnesses reproduce exactly as stated',
                         lambda: 'rem:unifilar-support-not-automatic' in labels),
 ('connected_support.py', 'connected support is sufficient and non-droppable',
                         lambda: 'prop:input-driven-specialization' in labels),
 ('controlled_ib.py',    'controlled IB identity and centroid optimality',
                         lambda: 'thm:controlled-ib' in labels),
 ('controlled_ib_hyp.py','input independence is load-bearing; elementary corollary',
                         lambda: 'rem:controlled-ib-independence' in labels),
 ('controlled_zero.py',  'kernel-count threshold fails in the unifilar class',
                         lambda: 'rem:controlled-zero-not-kernels' in labels),
 ('controlled_zero_correct.py',
                         'zero controlled retention at the stable kernel refinement',
                         lambda: 'thm:controlled-zero' in labels),
 ('controlled_zero_witness.py',
                         'printed zero-threshold witness reproduces exactly',
                         lambda: 'rem:controlled-zero-not-kernels' in labels),
 ('controlled_spectral.py',
                         'fiberwise quadratic and probability-coordinate converses',
                         lambda: 'cor:controlled-simplex-spectral' in labels),
 ('support_congruence.py',
                         'cofilteredness and residual finiteness, support-relative',
                         lambda: 'lem:cofiltered-support' in labels),
 ('zfuture_congruence.py',
                         'full-future equality forces equality of feasible sets',
                         lambda: 'prop:unifilar-lumpability' in labels),
 ('complexity_transfer.py',
                         'hardness transfer verified per construction',
                         lambda: 'rem:complexity-transfer' in labels),
 ('feasibility_frequency.py',
                         'exact frequencies replace the vague "a majority" claims',
                         lambda: 'rem:unifilar-feasibility' in labels),
 ('feas_probes.py',      'feasibility triage: correlated IB, refinement gap, |O|=2d',
                         lambda: 'prop:kernel-refinement-exists' in labels),
 ('controlled_ib_general.py',
                         'general controlled IB; reweighting necessary for the converse',
                         lambda: 'thm:controlled-ib-general' in labels),
 ('refinement_extremal.py',
                         'counter family: maximal gap, tight round count, induction',
                         lambda: 'prop:refinement-extremal' in labels),
 ('alphabet_similarity.py',
                         'd=2 discriminant obstruction; d=3 Hadamard similarity',
                         lambda: 'rem:output-alphabet-2d' in labels),
 ('rd_convexity.py',     'finite-state D(R) is not convex; exact 60-dps witness',
                         lambda: 'prop:rd-nonconvex' in labels),
 ('grounding_tracking.py','floor+tracking decomposition; deficit nonnegative',
                         lambda: 'prop:grounding-tracking' in labels),
 ('pos_safe_feasibility.py',
                         'safe congruences exist iff M >= r; PoS nonnegative there',
                         lambda: 'prop:pos-quad-consistent' in labels),
 ('universal_vs.py',     'same-machine separation <= M-1 over 79.5M pairs',
                         lambda: 'prop:lsyncu-version-space' in labels),
 ('universal_vs2.py',    'version-space strategy is transcript-driven and terminates',
                         lambda: 'The whole strategy is a function of the transcript' in flat),
 ('universal_gap2.py',   'Lsync < Lsyncu already at M=2 (two-machine witness)',
                         lambda: 'rem:lsync-not-lsyncu' in labels),
 ('extremal.py',         'extremal machines at M=3,4: sink+cycle+single probe',
                         lambda: 'rem:attainment-sporadic' in labels),
 ('extremal_read.py',    'traced optimal play at M=4',
                         lambda: r'\{0,1,2,3\}\to\{0,2,3\}\to\{0,1,3\}' in flat),
 ('probe_family.py',     'generalized probe family has depth 2M-2',
                         lambda: '$2M-2$' in flat),
 ('attain_exhaustive5.py','M=5 exhaustive structured: max 9 < binom(5,2)=10',
                         lambda: '$2{,}839{,}200$ minimal machines' in flat),
 ('attain_search.py',    'hill-climb gaps widen at M=6,7,8',
                         lambda: '$9$, $14$ and $14$ at $M=6,7,8$' in flat),
 ('tension.py',          'd(U) <= M-|U|+1 over 145.9M subsets',
                         lambda: 'lem:tension' in labels),
 ('tension_proof.py',    'both proof steps over 13.26M minimal machines',
                         lambda: r'\bigl|Q_A/{\sim_{k-1}}\bigr|\ \ge\ k' in flat),
 ('tension_sum.py',      'telescoping to binom(M,2), attained at M=4',
                         lambda: 'prop:lsyncu-binomial' in labels),
 ('single_input.py',     'exhaustive |I|=1 minimal machines: depth = M-1',
                         lambda: 'prop:lsyncu-single-input' in labels),
 ('single_input_proof.py','block counts strictly increase, 9.3M machines at M=7',
                         lambda: '$9{,}313{,}920$ minimal machines at $M=7$' in flat),
 ('single_input_relation.py','depth equals refinement rounds for |I|=1',
                         lambda: 'the depth equals the number of refinement rounds' in flat),
 ('lsync_potential.py',  'separating word <= M-1; homing <= M(M-1)/2',
                         lambda: 'prop:lsyncu-quadratic' in labels),
 ('lsync_minimal_search.py','hill-climbing over minimal machines stays below M log M',
                         lambda: 'never exceeds' in flat and '$0.78$ and trends downward' in flat),
 ('lsync_family.py',     'counter and cyclic-shift families realize M-1 and log M',
                         lambda: 'cyclic counters with a single marked state' in flat),
 ('kappa.py',            'jump ratio bounded, sup attained at M=2',
                         lambda: 'lem:kappa-bounded' in labels),
 ('kappa_proof.py',      'kappa proof steps: monotonicity, mediant, T-independence',
                         lambda: 'independent of the horizon $T$, of the scale $\\gamma$' in flat),
 ('deep_kl_sharp.py',    'constant 1 sharp; proof chain step-by-step',
                         lambda: 'rem:kl-minorant-sharp' in labels),
 ('deep_kl_infimum.py',  'infimum KL/||.||^2 = 1 in exact arithmetic',
                         lambda: 'the minimum observed ratio is $1.0000000053$' in flat),
 ('deep_apx.py',         'APX ratio uniform over all partitions',
                         lambda: 'falls as $\\delta^2$' in flat),
 ('deep_csiszar.py',     'alpha-sweep isolates alpha=1',
                         lambda: 'vanishes only at $\\alpha=1$' in flat),
 ('deep_automata.py',    'EsyncSI games solved exactly, L=1..10',
                         lambda: 'the deterministic minimax mistake count on the cyclic-shift' in flat),
 ('esyncsi_exact.py',    'halving is 1/2 for every |O|; alphabet drops out',
                         lambda: 'rem:halving-alphabet-free' in labels),
 ('esyncsi_halving.py',  'c_2 <= |V|/2 exhaustively over class profiles',
                         lambda: 'Enumerating all integer class profiles' in flat),
 ('esyncsi_exhaustive4.py','exhaustive minimal machines nS<=4, |O|<=4',
                         lambda: '$46{,}656$ table pairs in the largest, of which' in flat),
 ('halving_ri.py',       'halving factor 1/2 applies to machine-state pairs too',
                         lambda: 'which holds for machine--state pairs exactly as it' in flat),
 ('deep_interior_fisher.py','interior Fisher with correct m_K',
                         lambda: '$1{,}664$ (instance, partition) pairs' in flat),
 ('deep_packing.py',     'compensation identity + two-point disproof',
                         lambda: 'lem:packing-criterion' in labels),
 ('ib_identity.py',      'predictive-information identity exact (all partitions)',
                         lambda: 'enumerating \\emph{all} set partitions' in flat),
 ('sum_vs_min.py',       'sandwich converts min-floor to sum-form envelope',
                         lambda: r'\frac{c}{1+\kappa}\,\inf_{M}' in flat),
 ('apx.py',              'embedding is approximation preserving (APX)',
                         lambda: 'cor:full-kl-apx' in labels),
 ('mcmillan.py',         'Kronecker rank = deg of antianalytic part (Peller)',
                         lambda: r'\rank H_\psi=\deg\mathbb P_-\psi' in flat),
 ('floors.py',           'two-point floor is FALSE',
                         lambda: '\\item \\textbf{Packing floor.}' in flat),
 ('fano.py',             'm-point floor works',
                         lambda: 'I(V;Y)' in flat),
 ('instance.py',         'floor discharged for stream regime',
                         lambda: 'prop:floors-instance' in labels),
 ('compensation.py',     'compensation identity',
                         lambda: 'lem:packing-criterion' in labels),
 ('opequiv.py',          'operational equivalence is a theorem',
                         lambda: '\\begin{lemma}[Operational Equivalence]' in flat),
 ('packing_general.py',  'general packing criterion',
                         lambda: 'lem:packing-criterion' in labels),
 ('retention_rate.py',   'stochastic packings need T = Omega(M^3)',
                         lambda: 'rem:packing-per-regime' in labels),
 ('frame.py',            'frame constants for Hankel',
                         lambda: 'lem:frame-bridge' in labels),
 ('frame_rate.py',       'C_2 = sqrt n',
                         lambda: 'C_2(n)=\\sqrt n' in flat),
 ('c1_bounded.py',       'C_1 >= n via the atom witness',
                         lambda: 'prop:no-dimension-free-bridge' in labels),
 ('diag_iso.py',         'diagonal isometry; grounding exempt',
                         lambda: 'is \\emph{not} exposed to the obstruction' in flat),
 ('extension.py',        'right-closure does not prevent re-entry',
                         lambda: 'lem:support-extension' in labels),
]

print('=' * 78)
print('TRACEABILITY: verification script -> manuscript artefact')
print('=' * 78)
landed = notlanded = 0
for script, what, test in TRACE:
    path = _p(f'verify/{script}')
    exists = os.path.exists(path)
    ok = False
    try:
        ok = bool(test())
    except Exception:
        ok = False
    tag = 'LANDED    ' if ok else '*** NOT LANDED ***'
    if ok:
        landed += 1
    else:
        notlanded += 1
    print(f'  {tag} {script:22s} {what}')
    if not exists:
        print(f'             (script missing: {path})')

print()
print('=' * 78)
print(f'{landed} landed, {notlanded} not landed, of {len(TRACE)} tracked verifications')
print('=' * 78)
