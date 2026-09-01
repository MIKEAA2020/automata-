#!/usr/bin/env python3
"""v4 pass 2: C3 abstract compression + E1 (consolidation) + E2 (dedupe)
+ E3 + E4 + E5 (five nits). Anchored; aborts before writing on failure."""
import sys

PATH = "/home/z/my-project/download/automata_unified_revised_v4.tex"
src = open(PATH, encoding="utf-8").read()

edits = []  # (name, old, new)

# ---------------------------------------------------------------- C3: abstract compression
ABS_START = "\\begin{abstract}\n"
ABS_END = "\n\\end{abstract}"
i0 = src.find(ABS_START)
i1 = src.find(ABS_END, i0)
assert i0 >= 0 and i1 > i0, "abstract markers not found"
old_abs = src[i0 + len(ABS_START):i1]
assert old_abs.lstrip().startswith("We develop a comparative framework"), "abstract head changed"
assert old_abs.rstrip().endswith("symbolic deterministic grounding."), "abstract tail changed"

NEW_ABS = """We develop a comparative framework for finite-state approximation of
sequential objects: a rate--distortion theory of bounded sequential
transduction in which the rate is a state budget $M$ and the distortion is a
regime-specific task loss.  Three regimes share one syntax --- histories,
finite-index right congruences, quotient machines, stationary aggregation, and
variational gaps --- and differ in their semantic objects.  Commitment targets
deterministic specifications through deterministic Mealy machines and
Myhill--Nerode residuals.  Retention targets stochastic controlled processes
through stationary controlled unifilar causal machines (controlled
$\\epsilon$-machines, whose state update may read the realized output) and
their lumpable quotients.  Grounding targets stochastic channels through
linear finite-rank Hankel realizations, whose resource is operator rank rather
than quotient index; a closed-form finite-budget characterization of exact
symbolic deterministic grounding remains open, but an observable deterministic
floor, its finite-state limit, and certified finite-horizon and finite-section
intervals are established.  Every approximation claim carries an explicit type
signature fixing regime, feasible set, aggregation, support, protocol, and
analytical bridge, so that statements from different regimes are not
conflated.

The principal exact results are as follows.  The retention full-KL gap admits
an exact finite-state information-bottleneck decomposition over stationary
lumpable quotients, with a controlled analogue, conditional on the input, for
general unifilar machines, and a zero-retention threshold at the stationary
support size of distinct predictive states in the input-driven theory and at
the coarsest unifilar-lumpable refinement of the predictive-kernel partition
in general.  For finite output alphabets a global spectral converse holds in
probability coordinates with sharp constant $1$; under uniform interiority a
corresponding bound holds in a fixed minimal natural-parameter chart, and the
interiority hypothesis cannot be removed.  The unrestricted linear finite-rank
Hankel relaxation gap is $\\Dunres(M)=\\sigma_{M+1}(H_\\nu)$ by
Eckart--Young--Mirsky, while the Hankel-structured gap is bounded below by
$\\sigma_{M+1}(H_\\nu)$ and equals it under an Adamjan--Arov--Krein
Hardy-space embedding --- unconditional for one-letter alphabets, conditional
on a multiletter Nehari/AAK-type theorem otherwise, which is not established
here.  A superpolynomial, sub-exponential determinism gap separates formal
Hankel rank from deterministic state complexity.  Retention is NP-complete in
the Gaussian quadratic restricted regime and NP-hard under a promise with
APX-hardness for unrestricted full KL.  Mistake complexity is $\\Theta(M\\log
M)$ in the reset-word, persistent-stream, and active residual-identification
protocols, with agnostic regret $\\Theta(\\sqrt{TM\\log M})$.

The framework separates shared syntax from regime-specific analysis: a typed
variational schema; structural monotonicity and zero thresholds; a conditional
response-operator converse and Schatten template; adaptive oracle
inequalities with a matching minimax lower bound under explicit floors; and a
linear second-order Price-of-Safety surrogate with a Ky Fan majorization law.
A vertex correspondence organizes retention, commitment, and grounding by
R\\'enyi/Schatten labels $\\{0,1,\\infty\\}$ as a formal consistency rather
than a derivation, and no analytic theorem depends on it.  An independence
theorem shows that the three regimes' obstructions vary independently, so no
cross-regime ordering holds.  The average-case theory uses stationary
Ces\\`aro or discounted prefix aggregation throughout, finite prefixes not
defining a probability measure over all lengths.  The manuscript identifies a
small set of sharply posed open research programs in place of a single
undifferentiated open problem of exact symbolic deterministic grounding."""

edits.append(("C3-abstract", old_abs, NEW_ABS))

# ---------------------------------------------------------------- C3 companion: temporal summary in intro
edits.append((
    "C3-intro-temporal",
    """The equality of vertex labels
\\[
\\alpha=p\\in\\{0,1,\\infty\\}
\\]
is a formal consistency, not a derivation of the Mirsky converses from
R\\'enyi identities.
""",
    """The equality of vertex labels
\\[
\\alpha=p\\in\\{0,1,\\infty\\}
\\]
is a formal consistency, not a derivation of the Mirsky converses from
R\\'enyi identities.

\\paragraph{Temporal protocols.}
On the deterministic Mealy classes $\\mathcal H_M$, the reset-word,
persistent-stream, and active residual-identification protocols each have
mistake complexity $\\Theta(M\\log M)$, the persistent-stream and active
lower bounds being explicit forcing constructions rather than Littlestone
transfers, and agnostic regret is $\\Theta(\\sqrt{T M\\log M})$.
""",
))

# ---------------------------------------------------------------- E3: discounted-law collapse note
edits.append((
    "E3-discounted-collapse",
    """whenever the extension of Lemma~\\ref{lem:support-extension} is
index-preserving.
In general the average-case index may be strictly smaller than the worst-case""",
    """whenever the extension of Lemma~\\ref{lem:support-extension} is
index-preserving.
For discounted-prefix laws the right-closed case never bites: since
$\\mu(\\varepsilon)=1-\\gamma>0$ one has $\\varepsilon\\in S$, and right-closure
then forces $S=\\mathcal I^*$, whence $c_S=0$ and the sandwich collapses to the
equality (Remark~\\ref{rem:support-extension-sharp}).  The sandwich is
therefore informative only for average-case history laws whose support is not
right-closed.
In general the average-case index may be strictly smaller than the worst-case""",
))

# ---------------------------------------------------------------- E4: transient-state note
edits.append((
    "E4-transient-note",
    """Since input-driven machines are unifilar
(Remark~\\ref{rem:unifilar-proper-subclass}), the same example shows that
one-step predictive equivalence need not be a support-relative right
congruence on joint histories in the general model.
\\end{example}""",
    """Since input-driven machines are unifilar
(Remark~\\ref{rem:unifilar-proper-subclass}), the same example shows that
one-step predictive equivalence need not be a support-relative right
congruence on joint histories in the general model.

A scope note: with a single input letter and this transition structure, every
stationary distribution is supported on the absorbing pair $\\{s_2,s_3\\}$,
while $s_0$ and $s_1$ --- the states carrying the one-step equivalence --- are
transient.  The example therefore concerns the transition structure and the
reachability of the equivalence, not an instance posed on the stationary
support in the sense of Definition~\\ref{def:unifilar-machine}; the structural
point is unaffected by making all four states recurrent with a second input
letter.
\\end{example}""",
))

# ---------------------------------------------------------------- E5(1): tau_K well-definedness
edits.append((
    "E5-tauK",
    """Conversely, let $\\sim$ be a finite-index right congruence coarser than
$\\sim_Z$, and assume $\\sim_Z$ is a right congruence.  Each $\\sim$-class is then
a union of $\\sim_Z$-classes.  Define $\\phi(s)$ to be the $\\sim$-class of any
long history $u$ with $\\sigma(u)=s$.  This is well defined: two long histories
with the same $\\sim_Z$-state are $\\sim_Z$-equivalent, hence $\\sim$-equivalent
because $\\sim$ is coarser.  The right-congruence property gives
\\[
\\phi(\\tau(s,x))=\\tau_{\\mathcal K}(\\phi(s),x),
\\]
so $\\phi$ is lumpable.""",
    """Conversely, let $\\sim$ be a finite-index right congruence coarser than
$\\sim_Z$, and assume $\\sim_Z$ is a right congruence.  Each $\\sim$-class is
then a union of $\\sim_Z$-classes.  Define $\\phi(s)$ to be the $\\sim$-class of
any sufficiently long history $u$ with $\\sigma(u)=s$.  This is well defined:
$\\sigma(u)=\\sigma(v)=s$ makes $u$ and $v$ $\\sim_Z$-equivalent, hence
$\\sim$-equivalent because $\\sim$ is coarser, so the assigned $\\sim$-class does
not depend on the chosen history.  Define the quotient transition \\emph{by}
the intertwining,
\\[
\\tau_{\\mathcal K}(k,x)\\eqdef\\phi\\bigl(\\tau(s,x)\\bigr)
\\qquad\\text{for any }s\\in\\Splus\\text{ with }\\phi(s)=k,
\\]
whose well-definedness is exactly the content of the right-congruence
property: if $\\phi(s)=\\phi(s')=k$ and $u,u'$ are long histories with
$\\sigma(u)=s$ and $\\sigma(u')=s'$, then $u\\sim u'$, hence $ux\\sim u'x$ for
every input $x$ in the support, so $\\phi(\\tau(s,x))=\\phi(\\tau(s',x))$ and
$\\tau_{\\mathcal K}(k,x)$ is independent of the representative $s$.  The pair
$(\\phi,\\tau_{\\mathcal K})$ is thus a lumpable quotient in the sense of
Definition~\\ref{def:lumpable-quotient}.""",
))

# ---------------------------------------------------------------- E5(2): attainment in def:com-rd-gap
edits.append((
    "E5-attainment",
    """\\begin{definition}[Distributional Commitment Rate--Distortion Gap]
\\label{def:com-rd-gap}
\\[
\\ComRD(M)
=
\\min_{\\substack{\\sim\\ \\text{right congruence}\\\\ \\operatorname{index}(\\sim)\\le M}}
\\ \\min_{\\rho}
\\ \\sum_{u\\in\\mathcal I^*\\setminus\\{\\varepsilon\\}}
\\mu(u)\\,
\\mathrm e_{\\sim,\\rho}(u).
\\]
\\end{definition}""",
    """\\begin{definition}[Distributional Commitment Rate--Distortion Gap]
\\label{def:com-rd-gap}
\\[
\\ComRD(M)
=
\\min_{\\substack{\\sim\\ \\text{right congruence}\\\\ \\operatorname{index}(\\sim)\\le M}}
\\ \\min_{\\rho}
\\ \\sum_{u\\in\\mathcal I^*\\setminus\\{\\varepsilon\\}}
\\mu(u)\\,
\\mathrm e_{\\sim,\\rho}(u).
\\]
The minimum is attained: up to renaming of the quotient states there are only
finitely many Mealy machines with at most $M$ states over the finite alphabets
$\\mathcal I$ and $\\mathcal O$, and the objective depends on $(\\sim,\\rho)$ only
through the induced machine's transition structure and one-step output rule.
\\end{definition}""",
))

# ---------------------------------------------------------------- E5(3): sufficiently-large-M qualifier
edits.append((
    "E5-qualifier",
    """for $T$ at least the length of the forcing stream.  The same conclusion holds
a fortiori in the reset-word protocol, where a reset is a special case of the
input letter $\\mathtt r$ below.""",
    """for $T$ at least the length of the forcing stream and all sufficiently large
$M$, the passage from the subsequences $M=2^L$ and $M'=3\\cdot2^L$ on which
the forcing constructions act to all large budgets being
Lemma~\\ref{lem:subsequence-allM}, as recorded in
Corollary~\\ref{cor:stream-all-M}.  The same conclusion holds
a fortiori in the reset-word protocol, where a reset is a special case of the
input letter $\\mathtt r$ below.""",
))

# ---------------------------------------------------------------- E5(5): comma splice
edits.append((
    "E5-comma-splice",
    """\\item If $\\sim_\\delta$ has finite index, then, $\\mathcal E$ being reflexive by
Definition~\\ref{def:task-theory},""",
    """\\item If $\\sim_\\delta$ has finite index, then, since $\\mathcal E$ is reflexive
by Definition~\\ref{def:task-theory},""",
))

# ---------------------------------------------------------------- E5(4): Myhill--Nerode standardization
edits.append((
    "E5-nerode-def",
    "\\begin{definition}[Nerode Equivalence]",
    "\\begin{definition}[Myhill--Nerode Equivalence]",
))
edits.append((
    "E5-nerode-prose",
    "its Nerode index is $1$.",
    "its Myhill--Nerode index is $1$.",
))
edits.append((
    "E5-nerode-always",
    "The Nerode equivalence is always a right congruence.",
    "The Myhill--Nerode equivalence is always a right congruence.",
))
edits.append((
    "E5-nerode-support1",
    "the \\emph{support-relative Nerode relation}",
    "the \\emph{support-relative Myhill--Nerode relation}",
))
edits.append((
    "E5-nerode-support2",
    "terms of a support-relative Nerode relation is claimed.",
    "terms of a support-relative Myhill--Nerode relation is claimed.",
))

# ---------------------------------------------------------------- E1: consolidation trims
edits.append((
    "E1-rem-grounding-aak",
    """\\begin{remark}[AAK Scope]
\\label{rem:grounding-aak}
The default spectral converse is Eckart--Young--Mirsky.  Adamjan--Arov--Krein
applies only if a Hardy-space embedding is separately established.  The
grounding theory does not assume such an embedding by default.
\\end{remark}""",
    """\\begin{remark}[AAK Scope]
\\label{rem:grounding-aak}
The default spectral converse is Eckart--Young--Mirsky; the precise role of
the Hardy-space embedding in making Adamjan--Arov--Krein applicable is stated
once, in Remarks~\\ref{rem:aak-eym-hilbert} and~\\ref{rem:aak-eym-meta} and
Theorems~\\ref{thm:aak-equality} and~\\ref{thm:aak-multiletter}, and no such
embedding is assumed by default anywhere in the grounding theory.
\\end{remark}""",
))
edits.append((
    "E1-rem-unrestricted-restricted",
    """\\begin{remark}[Unrestricted versus Hankel-Restricted Feasible Sets]
\\label{rem:grounding-unrestricted-restricted}
The equality
\\[
\\Dunres(M)
=
\\sigma_{M+1}(H_\\nu)
\\]
is for the unrestricted rank-$M$ operator-norm approximation problem.  The
Hankel-structured finite-rank realization gap satisfies
\\[
\\DHankstr(M)
\\ge
\\sigma_{M+1}(H_\\nu),
\\]
because restricting the feasible set cannot decrease the infimum.  Equality is
not guaranteed without additional structure.
\\end{remark}""",
    """\\begin{remark}[Unrestricted versus Hankel-Restricted Feasible Sets]
\\label{rem:grounding-unrestricted-restricted}
The two gaps stand in the relation recorded in
Theorem~\\ref{thm:spectral-grounding}: the unrestricted equality
$\\Dunres(M)=\\sigma_{M+1}(H_\\nu)$ is Eckart--Young--Mirsky for the rank-$M$
operator-norm problem; the Hankel-structured gap obeys
$\\DHankstr(M)\\ge\\sigma_{M+1}(H_\\nu)$ because restricting the feasible set
cannot decrease the infimum; and equality is not guaranteed without the
additional structure of Theorems~\\ref{thm:aak-equality}
and~\\ref{thm:aak-multiletter}.
\\end{remark}""",
))
edits.append((
    "E1-rem-supremum-org",
    """\\begin{remark}[Supremum Vertex as Organization]
\\label{rem:grounding-supremum-organization}
The max-divergence vertex is the divergence-face analogue of worst-case or
supremum aggregation.  It organizes the grounding regime conceptually, but the
exact spectral converse remains the Schatten-$\\infty$ / operator-norm tail for
the unrestricted linear finite-rank Hankel relaxation:
\\[
\\Dunres(M)
=
\\sigma_{M+1}(H_\\nu).
\\]
The Hankel-structured finite-rank realization gap satisfies the lower bound
\\[
\\DHankstr(M)
\\ge
\\sigma_{M+1}(H_\\nu),
\\]
with equality only under additional structural hypotheses.
\\end{remark}""",
    """\\begin{remark}[Supremum Vertex as Organization]
\\label{rem:grounding-supremum-organization}
The max-divergence vertex is the divergence-face analogue of worst-case or
supremum aggregation.  It organizes the grounding regime conceptually, but the
exact spectral converse remains the Schatten-$\\infty$ / operator-norm tail of
Theorem~\\ref{thm:spectral-grounding} for the unrestricted linear finite-rank
Hankel relaxation, with the Hankel-structured gap obeying only the lower bound
recorded there and equality requiring the additional structural hypotheses of
Theorems~\\ref{thm:aak-equality} and~\\ref{thm:aak-multiletter}.
\\end{remark}""",
))
edits.append((
    "E1-cor-grd-schatten",
    """For the Hankel-structured finite-rank realization gap,
\\[
\\DHankstr(M)
=
\\inf_{\\substack{
\\rank B\\le M\\\\
B\\ \\text{Hankel}
}}
\\norm{H_\\nu-B}_{\\Sp{\\infty}},
\\]
the feasible set is restricted, and therefore
\\[
\\DHankstr(M)
\\ge
\\sigma_{M+1}(H_\\nu).
\\]
Equality requires additional structure, for example an optimal Hankel
truncation or a valid Hardy-space Adamjan--Arov--Krein embedding.
\\end{corollary}""",
    """For the Hankel-structured finite-rank realization gap the feasible set is
restricted to Hankel operators of rank at most $M$, so
Theorem~\\ref{thm:spectral-grounding} gives
$\\DHankstr(M)\\ge\\sigma_{M+1}(H_\\nu)$, with equality requiring the additional
structure of Theorems~\\ref{thm:aak-equality} and~\\ref{thm:aak-multiletter}.
\\end{corollary}""",
))
edits.append((
    "E1-rem-interpretations",
    """The manuscript uses interpretation (1).  The exact spectral converse is the
unrestricted linear finite-rank Hankel relaxation gap
\\[
\\Dunres(M)=\\sigma_{M+1}(H_\\nu),
\\]
while the Hankel-structured finite-rank realization gap satisfies
\\[
\\DHankstr(M)\\ge\\sigma_{M+1}(H_\\nu),
\\]
with equality only under additional structural hypotheses.
\\end{remark}""",
    """The manuscript uses interpretation (1).  The exact spectral converse is the
unrestricted linear finite-rank Hankel relaxation gap of
Theorem~\\ref{thm:spectral-grounding}, the Hankel-structured gap satisfying
the lower bound recorded there, with equality only under additional structural
hypotheses.
\\end{remark}""",
))
edits.append((
    "E1-retention-prefix",
    """The default aggregation is stationary average cost, either Ces\\`aro or
discounted.  Finite prefixes do not define a probability measure over all
lengths.""",
    """The default aggregation is stationary average cost, either Ces\\`aro or
discounted; that finite prefixes do not define a probability measure over all
lengths, and that this is what forces the two average-case schemes, is
recorded once in Remark~\\ref{rem:prefixes-versus-states}.""",
))
edits.append((
    "E1-conclusion-prefix",
    """\\item \\textbf{Stationary aggregation.}
The average-case theory uses stationary Ces\\`aro aggregation or discounted
prefix measures.  Finite prefixes do not define a probability measure over
all lengths.""",
    """\\item \\textbf{Stationary aggregation.}
The average-case theory uses stationary Ces\\`aro aggregation or discounted
prefix measures, finite prefixes not defining a probability measure over all
lengths (Remark~\\ref{rem:prefixes-versus-states}).""",
))

# ---------------------------------------------------------------- E2: dedupe exponent-layer copies
edits.append((
    "E2-def-dmax-exponent",
    """\\begin{definition}[Symmetrized Max-Divergence]
\\label{def:dmax-exponent}
This is Definition~\\ref{def:dmax}, repeated here so that the exponent layer is
self-contained; the hypotheses are the same, namely finite-dimensional positive
definite states.  For such $\\rho,\\sigma$, define
\\[
\\Dmax(\\rho\\Vert\\sigma)
=
\\log
\\left\\|
\\sigma^{-1/2}\\rho\\sigma^{-1/2}
\\right\\|_\\infty,
\\]
with $+\\infty$ if $\\supp\\rho\\not\\subseteq\\supp\\sigma$.  Define the
symmetrized version
\\[
\\Dmaxsym(\\rho\\Vert\\sigma)
=
\\max\\{
\\Dmax(\\rho\\Vert\\sigma),
\\Dmax(\\sigma\\Vert\\rho)
\\}.
\\]
\\end{definition}""",
    """\\begin{definition}[Symmetrized Max-Divergence]
\\label{def:dmax-exponent}
An anchor for the exponent layer, retained so that
Subsection~\\ref{subsubsec:exponent-grounding} can be read in isolation: the
max-divergence $\\Dmax$ and its symmetrization $\\Dmaxsym$ are exactly the
objects of Definition~\\ref{def:dmax} on finite-dimensional positive definite
states, with the same conventions there, and no independent content is
asserted at this vertex.  All properties used below are those of
Definition~\\ref{def:dmax} and
Proposition~\\ref{prop:grounding-local-equivalence}.
\\end{definition}""",
))
edits.append((
    "E2-thm-grounding-alpha",
    """\\begin{theorem}[Grounding Vertex]
\\label{thm:grounding-alpha-infty}
This is Theorem~\\ref{thm:grounding-vertex}, restated at the exponent vertex.
The grounding cost is the $C^*$-norm / Schatten-$\\infty$ distance
\\[
\\text{grounding cost}
=
\\norm{a-b}_\\infty
\\]
between residual operators or kernels, while the $\\alpha=\\infty$ R\\'enyi vertex
is the max-divergence $\\Dmax$, or its symmetrization $\\Dmaxsym$.  These are
distinct functionals:
\\[
\\Dmax(p\\Vert q)
=
\\log\\max_i\\frac{p_i}{q_i},
\\qquad
\\norm{\\operatorname{diag}(p)-\\operatorname{diag}(q)}_\\infty
=
\\max_i|p_i-q_i|.
\\]
They are related by Proposition~\\ref{prop:grounding-local-equivalence} under
bounded-overlap hypotheses, but they are not identical.
\\end{theorem}""",
    """\\begin{theorem}[Grounding Vertex]
\\label{thm:grounding-alpha-infty}
This is Theorem~\\ref{thm:grounding-vertex}, restated at the exponent vertex:
the grounding cost is the $C^*$-norm / Schatten-$\\infty$ distance
$\\norm{a-b}_\\infty$ between residual operators or kernels, the
$\\alpha=\\infty$ R\\'enyi vertex is the max-divergence $\\Dmax$ or its
symmetrization $\\Dmaxsym$, and the two are distinct functionals, related
locally under the bounded-overlap hypotheses of
Proposition~\\ref{prop:grounding-local-equivalence}.  The canonical statement,
its diagonal-state comparison, and its scope restrictions are those of
Theorem~\\ref{thm:grounding-vertex}, which is the single maintained copy.
\\end{theorem}""",
))

# ---------------------------------------------------------------- run
nfail = 0
for name, old, new in edits:
    c = src.count(old)
    if c != 1:
        print(f"ANCHOR FAIL [{name}]: count = {c}")
        nfail += 1
if nfail:
    print(f"{nfail} anchor failures; aborting, file NOT modified.")
    sys.exit(1)

for name, old, new in edits:
    src = src.replace(old, new, 1)
    print(f"applied: {name}")

open(PATH, "w", encoding="utf-8").write(src)
print(f"PASS 2 complete: {len(edits)} edits applied to {PATH}")
