#!/usr/bin/env python3
"""v4 pass 1: citations + positioning sentences + C2 + D1 + D2 + D3 + AAK precision.
Anchored replacements on download/automata_unified_revised_v4.tex.
Aborts before writing if any anchor fails or matches != 1."""
import sys

PATH = "/home/z/my-project/download/automata_unified_revised_v4.tex"
src = open(PATH, encoding="utf-8").read()

edits = []  # (name, old, new)

# ---------------------------------------------------------------- 1. C2: font shape TU/lmr/m/scit
# Wrap \textsc problem names in \textup so small caps stay upright inside the
# italic (plain-style) proposition body; applied at all sites for consistency.
edits.append((
    "C2-problemnames",
    "&\\textsc{RationalExpCompare}:\\\\",
    "&\\textup{\\textsc{RationalExpCompare}}:\\\\",
))
edits.append((
    "C2-remark-1",
    "representation stays in the low thousands.  \\textsc{RationalExpCompare} must",
    "representation stays in the low thousands.  \\textup{\\textsc{RationalExpCompare}} must",
))
edits.append((
    "C2-remark-2",
    "program, and it is in that form that it is a \\textsc{PosSLP}-type question.",
    "program, and it is in that form that it is a \\textup{\\textsc{PosSLP}}-type question.",
))
edits.append((
    "C2-remark-3",
    "membership in NP: it is \\textsc{RationalExpCompare}, and not the number of",
    "membership in NP: it is \\textup{\\textsc{RationalExpCompare}}, and not the number of",
))
edits.append((
    "C2-remark-4",
    "\\textsc{RationalExpCompare} admits polynomial-time verifiable certificates.",
    "\\textup{\\textsc{RationalExpCompare}} admits polynomial-time verifiable certificates.",
))
edits.append((
    "C2-scope-posslp",
    "problem lies in NP as soon as this $\\textsc{PosSLP}$-type comparison admits",
    "problem lies in NP as soon as this $\\textup{\\textsc{PosSLP}}$-type comparison admits",
))

# ---------------------------------------------------------------- 2. Positioning sentence: retention
edits.append((
    "POS-retention",
    """When the predictive family is restricted to common-covariance Gaussians, one
obtains a quadratic restricted gap
\\[
\\RetQuad(M).
\\]
The full-KL gap and the quadratic restricted gap are distinct objects.
""",
    """When the predictive family is restricted to common-covariance Gaussians, one
obtains a quadratic restricted gap
\\[
\\RetQuad(M).
\\]
The full-KL gap and the quadratic restricted gap are distinct objects.

\\emph{Positioning.}  The retention chapter extends the causal-state program of
computational mechanics \\cite{shalizi2001} from output processes to
controlled, input-driven transductions: the objects approximated are lumpable
quotients of a \\emph{controlled} unifilar causal machine rather than
partitions of a stationary process, and the feasibility notion of unifilar
lumpability is correspondingly stricter than ordinary lumpability.  Unlike the
information-bottleneck-for-causal-states line
\\cite{shalizicrutchfield2002,marzencrutchfield2014}, which characterizes the
optimal causal statistic, and unlike the Kullback--Leibler aggregation line for
regular Markov chains \\cite{geiger2015,geiger2026}, which computes the optimal
reduction, the manuscript tracks the full budget-$M$ gap curve: the zero
threshold at the stable kernel refinement, NP-hardness below it, and spectral
lower certificates from the predictive covariance, rather than only the
optimum.
""",
))

# ---------------------------------------------------------------- 3. Positioning sentence: grounding
edits.append((
    "POS-grounding",
    """closed-form finite-budget value for that symbolic gap remains open; certified
bounds are given in
Propositions~\\ref{prop:grounding-finite-section},~\\ref{prop:symbolic-finite-horizon}
and Theorem~\\ref{thm:observable-floor}.
\\end{enumerate}
""",
    """closed-form finite-budget value for that symbolic gap remains open; certified
bounds are given in
Propositions~\\ref{prop:grounding-finite-section},~\\ref{prop:symbolic-finite-horizon}
and Theorem~\\ref{thm:observable-floor}.

\\emph{Positioning.}  The grounding chapter transports the
Adamjan--Arov--Krein program for weighted automata
\\cite{balle2021,lacroce2024} from weighted languages to transductions.  The
object approximated is the Hankel operator of a channel on the joint alphabet
rather than that of a weighted language; the unrestricted and
Hankel-restricted feasible sets are separated explicitly, the
Eckart--Young--Mirsky value being available for the former and only the
singular-value lower bound for the latter; and the published one-letter
results extend to the multiletter setting only conditionally
(Theorem~\\ref{thm:aak-multiletter}, Open Problem~\\ref{open:hankel-multiletter}),
with grounded finite-section certificates and the zero-threshold
characterization $\\rank(H)\\le M$ standing in for the exact minimization values
of the one-letter theory.
\\end{enumerate}
""",
))

# ---------------------------------------------------------------- 4. D1: Ambainis bound, thm:exp-gap
edits.append((
    "D1-ambainis",
    """The best unconditional value of $\\mathcal S$ available in the literature is
that of Ambainis \\cite{ambainis1996},
\\[
\\mathcal S(k)
=
\\Omega\\!\\left(2^{\\,k\\log\\log k/\\log k}\\right),
\\]
which is superpolynomial but \\emph{sub}-exponential, since the exponent is
$o(k)$.  A genuinely exponential $\\mathcal S(k)=2^{\\Omega(k)}$ is not
established by the classical references and is not assumed here.
""",
    """The best unconditional value of $\\mathcal S$ available in the literature is
that of Ambainis (Theorem~1 of \\cite{ambainis1996}): a $k$-state probabilistic
automaton with isolated cutpoint whose smallest equivalent deterministic
automaton has
\\[
\\mathcal S(k)
=
\\Omega\\!\\left(2^{\\,k\\log\\log k/\\log k}\\right),
\\]
states, a bound which is superpolynomial but \\emph{sub}-exponential, since the
exponent is $o(k)$.  A genuinely exponential $\\mathcal S(k)=2^{\\Omega(k)}$ is not
established unconditionally by the classical references and is not assumed
here: the later non-constructive constructions of Freivalds
\\cite{freivalds2008} reach the logarithmic state regime, but their strongest
form rests on Artin's conjecture on primitive roots, and no unconditional
exponential value is quoted here.
""",
))

# ---------------------------------------------------------------- 5. D2: soften availability
edits.append((
    "D2-availability",
    """the dependence is stated in the theorem.  The corresponding programs, the
extremal machine tables, and the exact outputs accompany the manuscript as
supplementary material.
""",
    """the dependence is stated in the theorem.  The corresponding programs, the
extremal machine tables, the exact outputs, and the Lean development of
Remark~\\ref{rem:lean-formalization} are being prepared as supplementary
material and will be made available upon publication; they are not part of
the present submission package.
""",
))

# ---------------------------------------------------------------- 6. D3: computational conventions remark
edits.append((
    "D3-conventions-remark",
    """These computations illustrate the
theorems; they do not establish their hypotheses.
\\end{remark}
""",
    """These computations illustrate the
theorems; they do not establish their hypotheses.
\\end{remark}

\\begin{remark}[Computational Conventions]
\\label{rem:computational-conventions}
The computational observations reported throughout this manuscript are held to
the following conventions, stated once here and cross-referenced wherever an
enumeration, search, or numerical evaluation is quoted.  \\emph{Distinct
machines} are labelled transition/output table pairs counted up to renaming of
the state set, so a count of $N$ machines means $N$ renaming classes, and
\\emph{minimality} is decided by Moore partition refinement before counting.
\\emph{Tie-breaking} is lexicographic on a canonical encoding of the tables, so
extremal machines are identified up to renaming.  \\emph{Structured subclasses}
are named at each site where they are searched (for example, minimal machines
whose first input acts as a permutation and whose output function has a single
probe state).  \\emph{Arithmetic} is exact rational where stated,
$60$-digit floating point where stated, and never double precision where a
near-degenerate comparison is at issue.  Search is either exhaustive over the
stated class or hill-climbing with the restart schedule reported at the site.
These conventions apply to the retention checks of
Remark~\\ref{rem:retention-numerical} and to the machine-table searches of
Section~\\ref{sec:temporal}.
\\end{remark}
""",
))
edits.append((
    "D3-xref-tablepairs",
    """$|\\mathcal O|\\le4$ --- $46{,}656$ table pairs in the largest, of which
$35{,}640$ are minimal ---""",
    """$|\\mathcal O|\\le4$ --- $46{,}656$ table pairs in the largest, of which
$35{,}640$ are minimal, counted under the conventions of
Remark~\\ref{rem:computational-conventions} ---""",
))
edits.append((
    "D3-xref-m4",
    """Attainment at $M=3,4$ is a computational observation rather than a proved
lower bound: exhaustive search over all minimal machines with
$|\\mathcal I|=|\\mathcal O|=2$ returns maximum adaptive depth exactly $3$ and
$6$ respectively, the latter realized by $3072$ machines.""",
    """Attainment at $M=3,4$ is a computational observation rather than a proved
lower bound: exhaustive search over all minimal machines with
$|\\mathcal I|=|\\mathcal O|=2$, under the conventions of
Remark~\\ref{rem:computational-conventions}, returns maximum adaptive depth
exactly $3$ and $6$ respectively, the latter realized by $3072$ machines.""",
))
edits.append((
    "D3-xref-m5",
    """Exhaustive search at $M=5$
over the $2{,}839{,}200$ minimal machines whose first input is a permutation
and whose output function has a single probe returns maximum depth $9$, short""",
    """Exhaustive search at $M=5$
over the $2{,}839{,}200$ minimal machines whose first input is a permutation
and whose output function has a single probe, in the sense of
Remark~\\ref{rem:computational-conventions}, returns maximum depth $9$, short""",
))
edits.append((
    "D3-xref-m7",
    """the maximum is exactly $M-1$; the block count increases strictly
at each round, verified over $9{,}313{,}920$ minimal machines at $M=7$.""",
    """the maximum is exactly $M-1$; the block count increases strictly
at each round, verified over $9{,}313{,}920$ minimal machines at $M=7$
(Remark~\\ref{rem:computational-conventions}).""",
))
edits.append((
    "D3-xref-m5all",
    """Exhaustive
computation over all minimal machines with $M\\le5$ states and
$|\\mathcal I|,|\\mathcal O|\\le3$ gives maximum adaptive depth""",
    """Exhaustive
computation over all minimal machines with $M\\le5$ states and
$|\\mathcal I|,|\\mathcal O|\\le3$, under the conventions of
Remark~\\ref{rem:computational-conventions}, gives maximum adaptive depth""",
))

# ---------------------------------------------------------------- 7. AAK precision: automatic unitary note
edits.append((
    "AAK-scalar-auto",
    """Let $S_+$ be the unilateral shift on the Hardy space $H^2$ of the disc.  (For
$|\\Sigma|>1$ see Theorem~\\ref{thm:aak-multiletter} and
Remark~\\ref{rem:aak-multialphabet-scope}: the free monoid $\\Sigma^*$ does
\\emph{not} carry a natural shift of multiplicity one, and the scalar theory
below does not apply directly.)  Assume there is a unitary""",
    """Let $S_+$ be the unilateral shift on the Hardy space $H^2$ of the disc.  (For
$|\\Sigma|>1$ see Theorem~\\ref{thm:aak-multiletter} and
Remark~\\ref{rem:aak-multialphabet-scope}: the free monoid $\\Sigma^*$ does
\\emph{not} carry a natural shift of multiplicity one, and the scalar theory
below does not apply directly.  In the present one-letter case, by contrast,
the canonical unitary $e_{a^n}\\mapsto z^n$ from
$\\ell^2(\\Sigma^*)\\cong\\ell^2(\\mathbb N)$ to $H^2$ satisfies hypothesis~(a)
below automatically, so that hypothesis is a checkable structural fact here
rather than an additional datum; it is nonetheless stated as a hypothesis
because the theorem is quoted in the generality in which $U$ is arbitrary.)
Assume there is a unitary""",
))

# ---------------------------------------------------------------- 8. AAK precision: multiletter hypothesis + proof
edits.append((
    "AAK-multiletter-hyp",
    """bijectively onto the corresponding rank-$\\le M$ Hankel class on $\\mathcal K$,
and an Adamjan--Arov--Krein/Nehari-type finite-rank approximation theorem valid
on $\\mathcal K$.  Then
\\[
\\DHankstr(M)=\\Dunres(M)=\\sigma_{M+1}(H_\\nu).
\\]""",
    """bijectively onto the corresponding rank-$\\le M$ Hankel class on $\\mathcal K$,
and an Adamjan--Arov--Krein/Nehari-type finite-rank approximation theorem
valid on $\\mathcal K$ \\emph{for the transported operator} $UH_\\nu U^{*}$ ---
that is, $UH_\\nu U^{*}$ belongs to the class to which the theorem applies (in
particular it is compact, consistently with the standing spectral
admissibility of Definition~\\ref{def:hilbert-module}), and the theorem
supplies
\\[
\\inf_{\\substack{C\\ \\text{Hankel on }\\mathcal K\\\\ \\operatorname{rank}C\\le M}}
\\norm{UH_\\nu U^{*}-C}_{\\mathrm{op}}
=
\\sigma_{M+1}(UH_\\nu U^{*}).
\\]
Then
\\[
\\DHankstr(M)=\\Dunres(M)=\\sigma_{M+1}(H_\\nu).
\\]""",
))
edits.append((
    "AAK-multiletter-proof",
    """\\begin{proof}
Identical to the scalar case: the hypothesised $U$ preserves rank, operator
norm, and by assumption the Hankel feasible sets, so the two constrained
infima agree, and the assumed approximation theorem on $\\mathcal K$ supplies
the value $\\sigma_{M+1}$.  Nothing beyond transport of structure is used.
\\end{proof}""",
    """\\begin{proof}
The transport is the same as in the scalar case, and only transport of
structure is used.  Unitary conjugation by $U$ preserves rank, the operator
norm, and singular values, and by hypothesis it carries the Hankel feasible
set of $\\ell^2(\\Sigma^*)$ bijectively onto the Hankel class of $\\mathcal K$, so
\\[
\\DHankstr(M)
=
\\inf_{\\substack{C\\ \\text{Hankel on }\\mathcal K\\\\ \\operatorname{rank}C\\le M}}
\\norm{UH_\\nu U^{*}-C}_{\\mathrm{op}}.
\\]
The hypothesized approximation theorem on $\\mathcal K$ supplies the value
$\\sigma_{M+1}(UH_\\nu U^{*})=\\sigma_{M+1}(H_\\nu)$ for this constrained infimum,
and Eckart--Young--Mirsky identifies $\\Dunres(M)=\\sigma_{M+1}(H_\\nu)$
unconditionally, so the three quantities coincide.  The intertwining clause of
the hypothesis is not separately consumed by this argument --- the bijectivity
of the Hankel classes is what is used --- but it is retained because it is the
property any natural candidate for $U$ would have to satisfy, and because it
excludes transporting the feasible sets by a unitary unrelated to the shift
systems.
\\end{proof}""",
))

# ---------------------------------------------------------------- 9. Bibliography insertions
edits.append((
    "BIB-freivalds2008",
    """\\bibitem{freivalds1981}
R.~Freivalds,
``Probabilistic two-way machines,''
in \\emph{Mathematical Foundations of Computer Science 1981},
Lecture Notes in Computer Science, vol.~118,
Springer, 1981, pp.~33--45.
""",
    """\\bibitem{freivalds1981}
R.~Freivalds,
``Probabilistic two-way machines,''
in \\emph{Mathematical Foundations of Computer Science 1981},
Lecture Notes in Computer Science, vol.~118,
Springer, 1981, pp.~33--45.

\\bibitem{freivalds2008}
R.~Freivalds,
``Non-constructive methods for finite probabilistic automata,''
\\emph{International Journal of Foundations of Computer Science},
vol.~19, no.~3, pp.~565--580, 2008.
""",
))
edits.append((
    "BIB-balle-lacroce",
    """\\bibitem{aak1971}
V.~M.~Adamjan, D.~Z.~Arov, and M.~G.~Kre\\u{\\i}n,
``Analytic properties of Schmidt pairs for a Hankel operator and the
generalized Schur--Takagi problem,''
\\emph{Math. USSR Sb.}, vol.~15, no.~1, pp.~31--73, 1971.
""",
    """\\bibitem{aak1971}
V.~M.~Adamjan, D.~Z.~Arov, and M.~G.~Kre\\u{\\i}n,
``Analytic properties of Schmidt pairs for a Hankel operator and the
generalized Schur--Takagi problem,''
\\emph{Math. USSR Sb.}, vol.~15, no.~1, pp.~31--73, 1971.

\\bibitem{balle2021}
B.~Balle, C.~Lacroce, P.~Panangaden, D.~Precup, and G.~Rabusseau,
``Optimal spectral-norm approximate minimization of weighted finite automata,''
in \\emph{48th International Colloquium on Automata, Languages, and
Programming (ICALP 2021)}, Leibniz International Proceedings in Informatics
(LIPIcs), vol.~198, Schloss Dagstuhl, 2021, pp.~118:1--118:20.

\\bibitem{lacroce2024}
C.~Lacroce, B.~Balle, P.~Panangaden, and G.~Rabusseau,
``Optimal approximate minimization of one-letter weighted finite automata,''
\\emph{Mathematical Structures in Computer Science}, vol.~34, pp.~807--833,
2024.
""",
))
edits.append((
    "BIB-computational-mechanics",
    """\\bibitem{shalizi2001}
C.~R.~Shalizi and J.~P.~Crutchfield,
``Computational mechanics: Pattern and prediction, structure and simplicity,''
\\emph{Journal of Statistical Physics}, vol.~104, no.~3--4, pp.~817--879, 2001.
""",
    """\\bibitem{shalizi2001}
C.~R.~Shalizi and J.~P.~Crutchfield,
``Computational mechanics: Pattern and prediction, structure and simplicity,''
\\emph{Journal of Statistical Physics}, vol.~104, no.~3--4, pp.~817--879, 2001.

\\bibitem{shalizicrutchfield2002}
C.~R.~Shalizi and J.~P.~Crutchfield,
``Information bottlenecks, causal states, and statistical relevance bases:
How to represent relevant information in memoryless transduction,''
\\emph{Advances in Complex Systems}, vol.~5, no.~1, pp.~1--5, 2002.

\\bibitem{marzencrutchfield2014}
S.~E.~Marzen and J.~P.~Crutchfield,
``Circumventing the curse of dimensionality in prediction: Causal
rate--distortion for infinite-order Markov processes,''
arXiv:1412.2859 [cond-mat.stat-mech], 2014.

\\bibitem{geiger2015}
B.~C.~Geiger, T.~Petrov, G.~Kubin, and H.~Koeppl,
``Optimal Kullback--Leibler aggregation via information bottleneck,''
\\emph{IEEE Transactions on Automatic Control},
vol.~60, no.~4, pp.~1010--1022, 2015.

\\bibitem{geiger2026}
B.~C.~Geiger,
``Information-theoretic reduction of Markov chains,''
\\emph{Computer Science Review}, vol.~59, 100802, 2026.
""",
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
print(f"PASS 1 complete: {len(edits)} edits applied to {PATH}")
