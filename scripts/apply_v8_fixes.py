#!/usr/bin/env python3
"""v8 revision: three anchored edits (abort-before-write).

Findings from the five-part deep review of v7 (full 18,100-line read +
automated sentence-level scan, 327 raw flags adjudicated to 2 genuine).

E1  Q2/Q3 fix: rem:infinite-support-grounding (Sec. 7) near-verbatim
    duplicates rem:infinite-support (Sec. 3) without a cross-reference.
    Add the cross-reference tying the grounding-side instance to the
    abstract-impulse-response remark.
E2  Q2 fix: the normalized-vs-structural valuation discussion after
    thm:commitment-spec (Sec. 6) re-derives the point of cor:boolean-01
    (Sec. 4 meta-layer) without linking it.  Add the schema-layer
    cross-reference.
E3  Q1/Q5 addition: a Notation Index --- the manuscript defines ~60
    bespoke macro symbols (\RetKL, \ComRD, \Lsyncu, \Esync, \PoSlin, ...)
    across 234 pages with no lookup table and zero figures; four
    booktabs tables (one page each, no new packages) with defining-site
    cross-references, placed after the bibliography, linked into the ToC.

Deliberately NOT implemented (adjudicated as decorative or already
saturated): further pedagogical remarks (168 already present), reading-path
paragraph in the roadmap (ToC + roadmap + type tables already serve
navigation), any figure (graphics infrastructure absent by design; no
comprehension gap is resolved by one), and a master results-map table
(Sec. 17's classification + Sec. 16's type tables already cover it).
"""
import sys, hashlib

SRC = '/home/z/my-project/automata/download/automata_unified_revised_v7.tex'
DST = '/home/z/my-project/automata/download/automata_unified_revised_v8.tex'
V7_MD5 = 'fe3da4d5fbc37d6a58fef11b566aeb67'

text = open(SRC, errors='replace').read()
if hashlib.md5(text.encode()).hexdigest() != V7_MD5:
    sys.exit('ABORT: v7 md5 mismatch - frozen file was modified')

edits = []

# ---------------------------------------------------------------- E1
e1_old = """\\begin{remark}[Infinite Support Does Not Imply Unboundedness]
\\label{rem:infinite-support-grounding}
A deterministic Mealy machine may induce an impulse response with infinite
support.  Infinite support alone does not imply that the associated Hankel
operator is unbounded.  Boundedness requires decay or summability conditions.
For example,
\\[
h(u)=\\gamma^{|u|}
\\]
with $0<\\gamma<1/|\\Sigma|$ defines a bounded Hankel-type operator by the
Schur-test domination of Proposition~\\ref{prop:stable-decay}.  Bounded symbolic
impulse responses that fail to decay may or may not define bounded Hankel
operators; boundedness is checked case by case.
\\end{remark}"""
e1_new = """\\begin{remark}[Infinite Support Does Not Imply Unboundedness]
\\label{rem:infinite-support-grounding}
A deterministic Mealy machine may induce an impulse response with infinite
support.  Infinite support alone does not imply that the associated Hankel
operator is unbounded: this is the grounding-side instance of
Remark~\\ref{rem:infinite-support}, whose content --- boundedness requires
decay or summability conditions, decay suffices, and non-decaying bounded
symbolic responses are decided case by case --- transfers verbatim from the
abstract impulse-response setting of Section~\\ref{subsec:hilbert-module}.
For example,
\\[
h(u)=\\gamma^{|u|}
\\]
with $0<\\gamma<1/|\\Sigma|$ defines a bounded Hankel-type operator by the
Schur-test domination of Proposition~\\ref{prop:stable-decay}, the same
criterion as there.  Bounded symbolic impulse responses that fail to decay
may or may not define bounded Hankel operators; boundedness is checked case
by case.
\\end{remark}"""
edits.append(('E1 infinite-support cross-ref', e1_old, e1_new))

# ---------------------------------------------------------------- E2
e2_old = """The normalized operational version uses the $\\{0,1\\}$ valuation.  The threshold
is the same; only the positive mismatch value changes.

%----------------------------------------------------------------------
\\subsection{Quantitative Commitment: A Distributional Rate--Distortion Gap}"""
e2_new = """The normalized operational version uses the $\\{0,1\\}$ valuation.  The threshold
is the same; only the positive mismatch value changes; the schema-layer
statement of this separation for arbitrary separated task theories is
Corollary~\\ref{cor:boolean-01}, of which the present pair of valuations is
the commitment instance.

%----------------------------------------------------------------------
\\subsection{Quantitative Commitment: A Distributional Rate--Distortion Gap}"""
edits.append(('E2 boolean-01 cross-ref', e2_old, e2_new))

# ---------------------------------------------------------------- E3
e3_old = """\\end{thebibliography}

%======================================================================
\\section*{Data and Code Availability}
%======================================================================"""
e3_new = """\\end{thebibliography}

%======================================================================
\\section*{Notation Index}
\\addcontentsline{toc}{section}{Notation Index}
\\label{sec:notation-index}
%======================================================================

The tables below collect the principal recurring symbols of the manuscript,
grouped by layer, with a cross-reference to the site at which each is fixed.
Symbols used only locally --- the witness machines of the explicit
constructions, the forcing alphabets $\\{\\mathtt r,\\mathtt e,\\mathtt d,
\\mathtt c\\}$, the block witnesses, the game-theoretic state variables ---
are defined at their site of use and are not repeated here.  Macro families
indexed by a regime superscript $\\mathsf r$ (as in
$\\Aapp^{\\mathsf r}$, $\\Est_M^{\\mathsf r}$, $\\Hcal_M^{\\mathsf r}$) share one
meaning across regimes; only the base entry is listed.

\\begin{table}[htbp]
\\centering
\\small
\\caption{Shared schema objects.}
\\label{tab:notation-schema}
\\begin{tabular}{@{}p{3.5cm}p{7.7cm}p{2.8cm}@{}}
\\toprule
\\textbf{Symbol} & \\textbf{Meaning} & \\textbf{Fixed at} \\\\
\\midrule
$\\mathbf V$ & Lawvere cost poset $([0,\\infty],\\ge,+,0)$ &
\\ref{subsec:enriching-poset} \\\\[2pt]
$\\mathbf H$ & history $\\mathbf V$-category on $\\mathcal I^*$ &
\\ref{subsec:history-category} \\\\[2pt]
$\\widehat{\\mathbf H}$ & profinite completion of $\\mathbf H$ &
\\ref{def:profinite-completion} \\\\[2pt]
$\\mathsf H$ & history system $(H,h_\\varnothing,\\mathcal A,\\cdot)$, pruned or
total & \\ref{def:history-system} \\\\[2pt]
$\\mathbb T$ & task theory
$(\\mathbf H,\\mathbf R,\\mathcal E,\\delta,\\mathrm{Agg},\\mathcal L)$ &
\\ref{def:task-theory} \\\\[2pt]
$\\mathcal E$ & cost profunctor (reflexive; separated where stated) &
\\ref{def:task-theory} \\\\[2pt]
$\\sim_\\delta$ & Myhill--Nerode equivalence of the trajectory &
\\ref{def:nerode} \\\\[2pt]
$\\operatorname{index}(\\sim)$ & number of classes of a right congruence &
\\ref{def:right-cong} \\\\[2pt]
$\\Delta_{\\mathbb T}(M)$ & budget-$M$ variational gap of a task theory &
\\ref{def:M-state-gap} \\\\[2pt]
$\\mu_\\gamma(u)$ & discounted prefix law
$(1-\\gamma)\\gamma^{|u|}\\Pr[\\text{prefix }u]$ &
\\ref{def:discounted-agg} \\\\[2pt]
$\\kappa_{\\mathrm{obs}}(\\delta,\\mu)$ & observable support index &
\\ref{def:observable-support-index} \\\\[2pt]
$\\Sigma=\\mathcal I\\times\\mathcal O$ & joint (grounding) alphabet; $|\\Sigma|$
alphabet size & \\ref{subsec:hilbert-module} \\\\
\\bottomrule
\\end{tabular}
\\end{table}

\\begin{table}[htbp]
\\centering
\\small
\\caption{Regime gaps and thresholds.}
\\label{tab:notation-gaps}
\\begin{tabular}{@{}p{3.5cm}p{7.7cm}p{2.8cm}@{}}
\\toprule
\\textbf{Symbol} & \\textbf{Meaning} & \\textbf{Fixed at} \\\\
\\midrule
$\\Com(M)$, $\\Comex(M)$ & exact (worst-case Boolean) commitment gap &
\\ref{thm:commitment-spec} \\\\[2pt]
$\\kappa_{\\det}(F)$ & Myhill--Nerode index of a specification $F$ &
\\ref{subsec:det-spec} \\\\[2pt]
$\\ComRD(M)$ & distributional rate--distortion commitment gap under $\\mu$ &
\\ref{def:com-rd-gap} \\\\[2pt]
$\\kappa_{\\mathrm{pair}}(F,\\mu)$ & one-step determination index &
\\ref{def:pair-determination-index} \\\\[2pt]
$\\ComGame(M)$ & simultaneous-move strategic commitment gap &
\\ref{subsec:quant-simul} \\\\[2pt]
$\\kappa_{\\mathrm{ctrl}}(\\Lambda)$ & controller complexity of a safety
property & \\ref{def:controller-complexity} \\\\[2pt]
$\\RetKL(M)$ & full-KL retention gap (input-driven) &
\\ref{def:full-kl-retention} \\\\[2pt]
$\\RetKLc(M)$, $\\RetKLg(M)$ & controlled and fiberwise controlled gaps &
\\ref{def:controlled-full-kl}, \\ref{def:controlled-full-kl-general} \\\\[2pt]
$\\RetKLr{r}$ & full-KL gap of the $r$-perturbed family &
\\ref{cor:fisher-uniform-remainder} \\\\[2pt]
$\\RetQuad(M)$, $\\RetQuadc(M)$ & quadratic restricted gaps (input-driven,
controlled) & \\ref{def:gaussian-quadratic} \\\\[2pt]
$N^{\\ast}$ & index of the stable kernel refinement (zero-retention
threshold, unifilar) & \\ref{def:kernel-refinement} \\\\[2pt]
$\\Dunres(M)$ & unrestricted linear finite-rank Hankel relaxation gap &
\\ref{def:linear-hankel-gap} \\\\[2pt]
$\\DHankstr(M)$ & Hankel-structured finite-rank gap &
\\ref{def:hankel-structured-gap} \\\\[2pt]
$\\GrdLin(M)$ & linear finite-rank residual-cost gap &
\\ref{cor:grounding-domination} \\\\[2pt]
$\\Delta_{\\mathrm{grd}}(M;\\gamma)$ & discounted symbolic grounding gap over
Mealy machines & \\ref{def:symbolic-grounding-gap} \\\\[2pt]
$\\sigma_\\gamma(\\nu)$, $F_\\gamma(\\nu)$ & stochasticity floor; observable
deterministic floor & \\ref{subsec:stochasticity-floor},
\\ref{thm:observable-floor} \\\\[2pt]
$D(\\phi)$ & tracking deficit above the one-step floor &
\\ref{def:tracking-deficit} \\\\[2pt]
$\\PoSlin(M)$, $\\PoSquad(M)$, $\\operatorname{PoS}(M)$ & Price-of-Safety
surrogate, discrete quadratic, mutual-information forms &
\\ref{def:poslin}, \\ref{subsec:pos-discrete}, \\ref{cor:price-safety} \\\\
\\bottomrule
\\end{tabular}
\\end{table}

\\begin{table}[htbp]
\\centering
\\small
\\caption{Divergences, operators, and spectral objects.}
\\label{tab:notation-operators}
\\begin{tabular}{@{}p{3.5cm}p{7.7cm}p{2.8cm}@{}}
\\toprule
\\textbf{Symbol} & \\textbf{Meaning} & \\textbf{Fixed at} \\\\
\\midrule
$\\KL$, $\\Ren{\\alpha}$ & Kullback--Leibler; classical R\\'enyi order
$\\alpha$ & \\ref{def:classical-renyi} \\\\[2pt]
$\\sRen{\\alpha}$ & sandwiched (operator) R\\'enyi divergence &
\\ref{def:sandwiched-renyi} \\\\[2pt]
$\\Dmax$, $\\Dmaxsym$ & max-divergence and symmetrization &
\\ref{def:dmax} \\\\[2pt]
$H_\\nu$ & Hankel operator of the channel $\\nu$ on $\\ell^2(\\Sigma^*)$ &
\\ref{def:hilbert-module} \\\\[2pt]
$\\sigma_{M+1}(\\cdot)$ & $(M+1)$-st singular value (indexed from
$\\sigma_1=\\norm{\\cdot}_{\\mathrm{op}}$) & \\ref{thm:aak-equality} \\\\[2pt]
$\\Phi^{(p)}_r(A)$ & Schatten-$p$ tail beyond rank $r$ &
\\ref{sec:schatten} \\\\[2pt]
$\\norm{\\cdot}_{\\Sp{p}}$ & Schatten-$p$ norm of a compact operator &
\\ref{sec:schatten} \\\\[2pt]
$A_\\delta$, $r_{\\mathbb T}(M)$, $c_p$ & response operator, effective rank
budget, domination modulus & \\ref{def:response} \\\\[2pt]
$\\bm{\\Sigma}_\\pi$ & stationary Fisher (or feature) covariance &
\\ref{subsec:quad-spectral} \\\\[2pt]
$\\bm{\\Sigma}_p$, $\\bm{\\Sigma}_\\eta$ & covariances of predictive probability
vectors / natural parameters & \\ref{thm:global-kl-simplex},
\\ref{thm:global-interior-fisher} \\\\[2pt]
$G$ & state-indexed centered Gram matrix &
\\ref{subsec:pos-objects} \\\\[2pt]
$\\EA$ & pinching (block conditional expectation) $\\operatorname{Pinch}_{\\mathcal A}$ &
\\ref{subsec:pos-objects} \\\\[2pt]
$\\KyF{X}{r}$ & Ky Fan $r$-norm & \\ref{subsec:pos-objects} \\\\[2pt]
$N_\\Lambda$, $\\rankBdet N_\\Lambda$ & Boolean Hankel matrix and
deterministic Boolean realization rank & \\ref{def:boolean-hankel-rank} \\\\
\\bottomrule
\\end{tabular}
\\end{table}

\\begin{table}[htbp]
\\centering
\\small
\\caption{Temporal, online-learning, and strategic quantities.}
\\label{tab:notation-temporal}
\\begin{tabular}{@{}p{3.5cm}p{7.7cm}p{2.8cm}@{}}
\\toprule
\\textbf{Symbol} & \\textbf{Meaning} & \\textbf{Fixed at} \\\\
\\midrule
$\\mathcal H_M$ & deterministic Mealy transductions with at most $M$ states &
\\ref{subsec:temporal-models} \\\\[2pt]
$\\Ldim$ & Littlestone dimension & \\ref{lem:littlestone} \\\\[2pt]
$\\MistRI(M)$ & active minimax mistakes to objective (RI) &
\\ref{def:residual-knowledge} \\\\[2pt]
$\\Esync(M)$, $\\EsyncSI$ & synchronization mistake complexities for
objectives (RI), (SI) & \\ref{def:sync-mistake-complexity} \\\\[2pt]
$\\Lsync(M)$, $\\Lsyncu(M)$ & machine-specific and universal adaptive
synchronization depths & \\ref{def:output-aware-sync} \\\\[2pt]
$\\Gact_M$ & gated active family (free/read modes $\\free,\\rd$) &
\\ref{def:gated-active-family} \\\\[2pt]
$\\Valt(q)$, $\\Vsim(M)$ & alternating-move value; simultaneous-move value at
budget $M$ & \\ref{subsec:quant-alt} \\\\[2pt]
$\\alpha(q)$ & strategic spread at reward state $q$ &
\\ref{subsec:quant-simul} \\\\[2pt]
$L_T^{\\star,\\mathsf r}$ & unrestricted finite-state benchmark loss &
\\ref{def:finite-state-benchmark} \\\\[2pt]
$\\Aapp^{\\mathsf r}(M)$ & budget-$M$ approximation deficit &
\\ref{def:approx-deficit} \\\\[2pt]
$\\Est_M^{\\mathsf r}(T)$ & online estimation rate for budget $M$ &
\\ref{def:estimation-rate} \\\\[2pt]
$\\Reg_T$ & cumulative regret against the benchmark &
\\ref{prop:fixed} \\\\[2pt]
$\\PsiAgg_M(T)$ & adaptive aggregation penalty over the budget index &
\\ref{thm:oracle-agnostic} \\\\
\\bottomrule
\\end{tabular}
\\end{table}

%======================================================================
\\section*{Data and Code Availability}
%======================================================================"""
edits.append(('E3 notation index', e3_old, e3_new))

# ---------------------------------------------------------------- apply
for name, old, new in edits:
    n = text.count(old)
    if n != 1:
        sys.exit(f'ABORT: anchor for {name} found {n} times (need exactly 1)')
    if new in text and new != old:
        sys.exit(f'ABORT: {name} target text already present')
    text = text.replace(old, new)

open(DST, 'w').write(text)
print(f'OK: {len(edits)} edits applied -> {DST}')
print(f'    lines: {text.count(chr(10)) + 1}')
