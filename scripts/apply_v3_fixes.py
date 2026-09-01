#!/usr/bin/env python3
"""
Apply v3 revision to automata_unified_revised_v3.tex:
  A2 - modular language delimiter-free form + residual-class justification
  A3 - numeric claim L=3 -> L=4
  A4 - two-step continuity argument + sandwiched-Renyi citations
  A5 - rewrite revision-seam text in prop:grounding-tracking(iii); drop 'Correction' label
  A6 - re-anchor prop:lsyncu-quadratic proof to Moore lemmas
  C1 - displayed multi-line lists in def:type-signature; break 5 overfull displays/paragraphs;
       load microtype
  BM  - global bold-Sigma update: covariance matrices -> \bm{\Sigma}
Anchors are exact-match and must each occur exactly once; the script aborts
before writing if any anchor fails (idempotent protection against double runs).
"""
import re, sys

TEX = "/home/z/my-project/download/automata_unified_revised_v3.tex"

with open(TEX, encoding="utf-8") as f:
    src = f.read()

edits = []  # (name, old, new)

# ---------------------------------------------------------------- E1: bm package
edits.append((
    "E1 preamble bm",
    "\\usepackage{amsmath,amssymb,amsthm,mathtools}\n\\usepackage{enumitem}",
    "\\usepackage{amsmath,amssymb,amsthm,mathtools}\n\\usepackage{bm}\n\\usepackage{enumitem}",
))

# ------------------------------------------------------- E2: microtype package
edits.append((
    "E2 preamble microtype",
    "\\usepackage{xcolor}\n\\usepackage[colorlinks=true,linkcolor=blue!55!black,citecolor=blue!55!black]{hyperref}",
    "\\usepackage{xcolor}\n\\usepackage{microtype}\n\\usepackage[colorlinks=true,linkcolor=blue!55!black,citecolor=blue!55!black]{hyperref}",
))

# ------------------------------------------------------------------- A2 fix
edits.append((
    "A2 modular language",
    """\\noindent\\textbf{Finite and tunable complexity.}
Replacing $L_{\\mathrm{sq}}$ by the modular language
\\[
L_N=\\{\\#1^n:n\\equiv0\\pmod N\\}
\\]
gives commitment complexity exactly $N$.  Varying the predictive separation in""",
    """\\noindent\\textbf{Finite and tunable complexity.}
Replacing $L_{\\mathrm{sq}}$ by the delimiter-free modular language
\\[
L_N=\\{1^n:n\\equiv0\\pmod N\\}
\\]
over the unary alphabet gives commitment complexity exactly $N$: the
Myhill--Nerode classes of $L_N$ are the $N$ residue classes, since the
residual after $1^n$ is $\\{1^k:n+k\\equiv0\\pmod N\\}$, which distinguishes
the $N$ residues of $n$.  Varying the predictive separation in""",
))

# ------------------------------------------------------------------- A3 fix
edits.append((
    "A3 numeric claim",
    "and the ratio is increasing in $L$, exceeding $0.23$ already at $L=3$.  Thus",
    "and the ratio is increasing in $L$, exceeding $0.23$ already at $L=4$.  Thus",
))

# ------------------------------------------------------------------- A4 fix
edits.append((
    "A4 renyi limit",
    """For $\\alpha\\to\\infty$, the Schatten quasi-norms of a fixed positive operator
converge to the operator norm,
$\\norm{K_\\alpha}_{\\Sp{\\alpha}}\\to\\norm{\\sigma^{-1/2}\\rho\\sigma^{-1/2}}_\\infty$,
by monotone convergence of $\\ell^\\alpha$ norms of the singular-value sequence,
and $\\alpha/(\\alpha-1)\\to1$; combining the two gives $\\Dmax$.""",
    """For $\\alpha\\to\\infty$, the operator
$K_\\alpha=\\sigma^{\\frac{1-\\alpha}{2\\alpha}}\\rho\\,
\\sigma^{\\frac{1-\\alpha}{2\\alpha}}$ itself depends on $\\alpha$, so the
monotone-convergence argument for a fixed singular-value sequence does not
apply to it directly; the limit holds by a two-step continuity argument.
First, on the support of $\\sigma$ --- where $\\sigma$ is positive definite,
and $\\supp\\rho\\subseteq\\supp\\sigma$ is assumed for finite divergence ---
the map $\\alpha\\mapsto K_\\alpha$ is continuous, by continuity of the matrix
power in the functional calculus, so
$K_\\alpha\\to K_\\infty=\\sigma^{-1/2}\\rho\\,\\sigma^{-1/2}$ and
$\\norm{K_\\alpha-K_\\infty}_{\\Sp{1}}\\to0$; for $\\alpha\\ge1$ the Schatten
norms obey the triangle inequality and decrease in the exponent, so
\\[
\\bigl|
\\norm{K_\\alpha}_{\\Sp{\\alpha}}-\\norm{K_\\infty}_{\\Sp{\\alpha}}
\\bigr|
\\le
\\norm{K_\\alpha-K_\\infty}_{\\Sp{\\alpha}}
\\le
\\norm{K_\\alpha-K_\\infty}_{\\Sp{1}}
\\to
0 .
\\]
Second, for the \\emph{fixed} positive operator $K_\\infty$, monotone
convergence of $\\ell^\\alpha$ norms of its singular-value sequence gives
$\\norm{K_\\infty}_{\\Sp{\\alpha}}\\to\\norm{K_\\infty}_\\infty$.  Combining the
two steps gives
$\\norm{K_\\alpha}_{\\Sp{\\alpha}}\\to\\norm{\\sigma^{-1/2}\\rho\\sigma^{-1/2}}_\\infty$,
and $\\alpha/(\\alpha-1)\\to1$, whence $\\Dmax$; this is the standard
sandwiched-R\\'enyi $\\alpha\\to\\infty$ limit
\\cite{mullerlennert2013,franklieb2013}.""",
))

# ------------------------------------------------------ A5(a): display D(phi)
edits.append((
    "A5a display D(phi)",
    """so that $D(\\phi)=\\sigma_1-\\sum_{C\\in\\mathcal P_\\phi}\\max_b\\sum_{s\\in C}w_s(b)$
for the partition $\\mathcal P_\\phi$ induced by $\\phi$, and likewise for
$\\psi$.""",
    """so that
\\[
D(\\phi)=\\sigma_1-\\sum_{C\\in\\mathcal P_\\phi}\\max_b\\sum_{s\\in C}w_s(b)
\\]
for the partition $\\mathcal P_\\phi$ induced by $\\phi$, and likewise for
$\\psi$.""",
))

# ------------------------------------------- A5(a): rewrite revision seam text
edits.append((
    "A5a revision seam",
    """$\\sigma_1$ reverses the inequality to $D(\\phi)\\le D(\\psi)$.  Since every
budget-$M$ feasible partition is refined by every budget-$M'$ feasible
partition for $M'\\ge M$ that further splits it (nesting of feasible sets, as
in the previous version of this claim), monotonicity of $D$ under
refinement upgrades the earlier feasible-set nesting argument to the sharper
conclusion that $\\min_{|\\mathcal K|\\le M}D(\\phi)$ is nonincreasing in $M$.""",
    """$\\sigma_1$ reverses the inequality to $D(\\phi)\\le D(\\psi)$.  The feasible
sets are nested in the budget: every partition with at most $M$ blocks is
feasible at every budget $M'\\ge M$, and each budget-$M'$ feasible partition
that splits a budget-$M$ feasible partition refines it.  Combining the
nesting of the feasible sets with the refinement monotonicity of $D$ just
established therefore gives the conclusion: enlarging the budget admits
refinements of each budget-$M$ feasible partition, and $D$ cannot increase
under refinement, so $\\min_{|\\mathcal K|\\le M}D(\\phi)$ is nonincreasing in
$M$.""",
))

# ------------------------------------------------------ A5(b): 'Correction' label
edits.append((
    "A5b correction label",
    """nonincreasing in $M$ (Correction to item (iii) of
Proposition~\\ref{prop:grounding-tracking}).""",
    """nonincreasing in $M$ (Proposition~\\ref{prop:grounding-tracking}).""",
))

# ------------------------------------------------------------------- A6 fix
edits.append((
    "A6 moore re-anchor",
    """\\emph{Step: one separation episode.}  Suppose $U$ contains two states $s\\ne t$
that are not observationally equivalent.  Consider the pair automaton on
unordered pairs of states of $A$: from $\\{u,v\\}$ and input $x$ there is an edge
to $\\{\\tau(u,x),\\tau(v,x)\\}$, and $\\{u,v\\}$ is \\emph{immediately separated} by
$x$ when $\\lambda(u,x)\\ne\\lambda(v,x)$.  Breadth-first search from $\\{s,t\\}$
reaches an immediately separated pair, since $s\\not\\sim t$; the pair automaton
has at most $\\binom{M}{2}$ nodes, but the standard argument bounds the distance
by $M-1$, because a shortest such path visits pairwise distinct pairs whose
underlying state sets are nested along the search and cannot repeat.  Let $w$
be the corresponding word, $|w|\\le M-1$.""",
    """\\emph{Step: one separation episode.}  Suppose $U$ contains two states $s\\ne t$
that are not observationally equivalent, so their continuation functions in
$A$ differ.  Lemma~\\ref{lem:tension} with $U=\\{s,t\\}$ bounds the length of
the shortest word separating them by
\\[
d(\\{s,t\\})\\ \\le\\ M-|\\{s,t\\}|+1\\ =\\ M-1,
\\]
via Moore partition refinement; Lemma~\\ref{lem:moore-separation} is the
cross-machine form of the same bound.  Let $w$ be such a separating word,
$|w|\\le M-1$.

In pair-automaton terms: from $\\{u,v\\}$ and input $x$ there is an edge to
$\\{\\tau(u,x),\\tau(v,x)\\}$, and $\\{u,v\\}$ is \\emph{immediately separated} by
$x$ when $\\lambda(u,x)\\ne\\lambda(v,x)$.  Breadth-first search from $\\{s,t\\}$
reaches an immediately separated pair, since $s\\not\\sim t$; but the distance
bound is the Moore bound $M-1$ above, not a distinctness-of-pair-nodes
argument --- distinct pair nodes number at most $\\binom{M}{2}$, which would
bound the path by $\\binom{M}{2}$, not by $M-1$.""",
))

# ------------------------------------------- C1: def:type-signature items M, F, A
edits.append((
    "C1 type-signature M item",
    """\\item $\\mathsf M\\in\\{\\text{deterministic Mealy},\\text{stochastic lumped
predictor},\\text{unifilar controlled }\\epsilon\\text{-machine},
\\text{linear finite-rank realization}\\}$;""",
    """\\item the machine type
\\[
\\begin{aligned}
\\mathsf M\\in\\bigl\\{&\\text{deterministic Mealy},\\ \\text{stochastic lumped
predictor},\\\\
&\\text{unifilar controlled }\\epsilon\\text{-machine},\\
\\text{linear finite-rank realization}\\bigr\\};
\\end{aligned}
\\]""",
))

edits.append((
    "C1 type-signature F item",
    """\\item $\\mathsf F\\in\\{\\text{right congruences},
\\text{support-relative right congruences},\\text{lumpable quotients},
\\text{unifilar-lumpable quotients},\\text{history factors},
\\text{unrestricted rank-}M,\\text{Hankel-restricted}\\}$;""",
    """\\item the feasible set
\\[
\\begin{aligned}
\\mathsf F\\in\\bigl\\{&\\text{right congruences},\\
\\text{support-relative right congruences},\\
\\text{lumpable quotients},\\\\
&\\text{unifilar-lumpable quotients},\\ \\text{history factors},\\
\\text{unrestricted rank-}M,\\ \\text{Hankel-restricted}\\bigr\\};
\\end{aligned}
\\]""",
))

edits.append((
    "C1 type-signature A item",
    """\\item $\\mathsf A\\in\\{\\text{worst case},\\text{stationary Ces\\`aro},
\\text{discounted prefix},\\text{finite-horizon cumulative}\\}$;""",
    """\\item the aggregation
\\[
\\begin{aligned}
\\mathsf A\\in\\bigl\\{&\\text{worst case},\\ \\text{stationary Ces\\`aro},\\
\\text{discounted prefix},\\\\
&\\text{finite-horizon cumulative}\\bigr\\};
\\end{aligned}
\\]""",
))

# ------------------------------------------------- C1: PoS identity display
edits.append((
    "C1 PoS display",
    """\\[
\\PoSlin+\\rho_{\\mathrm{safe}}-\\rho_{\\mathrm{free}}
=
(\\mathrm{Free}_{\\mathrm{lin}}-\\mathrm{Safe}_{\\mathrm{lin}}^{\\mathrm{loc}})+(\\mathrm{Safe}_{\\mathrm{lin}}^{\\mathrm{loc}}-\\mathrm{Safe}_{\\mathrm{quad}})-(\\mathrm{Free}_{\\mathrm{lin}}-\\mathrm{Free}_{\\mathrm{quad}})
=
\\mathrm{Free}_{\\mathrm{quad}}-\\mathrm{Safe}_{\\mathrm{quad}}
=
\\PoSquad .
\\]""",
    """\\[
\\begin{aligned}
\\PoSlin+\\rho_{\\mathrm{safe}}-\\rho_{\\mathrm{free}}
&=(\\mathrm{Free}_{\\mathrm{lin}}-\\mathrm{Safe}_{\\mathrm{lin}}^{\\mathrm{loc}})
+(\\mathrm{Safe}_{\\mathrm{lin}}^{\\mathrm{loc}}-\\mathrm{Safe}_{\\mathrm{quad}})\\\\
&\\quad-(\\mathrm{Free}_{\\mathrm{lin}}-\\mathrm{Free}_{\\mathrm{quad}})
=\\mathrm{Free}_{\\mathrm{quad}}-\\mathrm{Safe}_{\\mathrm{quad}}
=\\PoSquad .
\\end{aligned}
\\]""",
))

# ------------------------------------------------- C1: RationalExpCompare display
edits.append((
    "C1 RationalExpCompare",
    """\\[
\\textsc{RationalExpCompare}:\\quad
\\text{given a factored positive rational }R\\text{ and a rational }s,
\\ \\text{decide whether }R\\ge e^{s}.
\\]""",
    """\\[
\\begin{aligned}
&\\textsc{RationalExpCompare}:\\\\
&\\quad\\text{given a factored positive rational }R
\\text{ and a rational }s,\\\\
&\\quad\\text{decide whether }R\\ge e^{s}.
\\end{aligned}
\\]""",
))

# ------------------------------------------------- C1: variational schema formula
edits.append((
    "C1 schema formula",
    """\\item \\textbf{Typed variational schema.}
Every regime gap has the shape
$\\Delta_{\\mathbb T}(M)=\\inf_{\\text{budget-}M\\text{ feasible }B}
\\mathcal L(\\delta,B)$,
but the feasible class carries a regime-specific type: a finite right""",
    """\\item \\textbf{Typed variational schema.}
Every regime gap has the shape
\\[
\\Delta_{\\mathbb T}(M)=\\inf_{\\text{budget-}M\\text{ feasible }B}
\\mathcal L(\\delta,B),
\\]
but the feasible class carries a regime-specific type: a finite right""",
))

# ------------------------------------------------- C1: regime table
edits.append((
    "C1 regime table",
    """\\begin{center}
\\begin{tabular}{llll}
\\toprule
regime & admissible factor & exact invariant & analytical bridge \\\\""",
    """\\begin{center}
\\small
\\setlength{\\tabcolsep}{4pt}
\\begin{tabular}{@{}l>{\\raggedright\\arraybackslash}p{10.5em}>{\\raggedright\\arraybackslash}p{10em}l@{}}
\\toprule
regime & admissible factor & exact invariant & analytical bridge \\\\""",
))

# ------------------------------------------------- C1: exact-results limit item
edits.append((
    "C1 exact-results limit",
    """$F_\\gamma(\\nu)$ the exact input-only deterministic floor and
$\\lim_{M\\to\\infty}\\Delta_{\\mathrm{grd}}(M;\\gamma)=F_\\gamma(\\nu)$
(Theorem~\\ref{thm:observable-floor}).""",
    """$F_\\gamma(\\nu)$ the exact input-only deterministic floor and
$\\Delta_{\\mathrm{grd}}(M;\\gamma)\\to F_\\gamma(\\nu)$ as $M\\to\\infty$
(Theorem~\\ref{thm:observable-floor}).""",
))

# ------------------------------------------------- A4 bib: sandwiched Renyi refs
edits.append((
    "A4 bibliography",
    """\\bibitem{amari2009}
S.-I. Amari,
``$\\alpha$-divergence is unique, belonging to both $f$-divergence and
Bregman divergence classes,''
\\emph{IEEE Trans. Inform. Theory}, vol.~55, no.~11, pp.~4925--4931, 2009.""",
    """\\bibitem{amari2009}
S.-I. Amari,
``$\\alpha$-divergence is unique, belonging to both $f$-divergence and
Bregman divergence classes,''
\\emph{IEEE Trans. Inform. Theory}, vol.~55, no.~11, pp.~4925--4931, 2009.

\\bibitem{mullerlennert2013}
M.~M\\"uller-Lennert, F.~Dupuis, O.~Fawzi, S.~Wehner, and H.~M.~Wiseman,
``On quantum R\\'enyi entropies: a new definition and limitations,''
\\emph{IEEE Transactions on Information Theory}, vol.~60, no.~12,
pp.~7801--7807, 2014.

\\bibitem{franklieb2013}
R.~L.~Frank and E.~H.~Lieb,
``Monotonicity properties and relative entropy bounds for quantum
R\\'enyi entropies,''
\\emph{Journal of Mathematical Physics}, vol.~54, no.~12, 122203, 2013.""",
))

# ---------------------------------------------------------------- apply edits
text = src
failures = []
for name, old, new in edits:
    n = text.count(old)
    if n != 1:
        failures.append(f"{name}: anchor count = {n} (expected 1)")
        continue
    text = text.replace(old, new)

# ------------------------------------------------ bold Sigma global replacement
SIG_RULES = [
    (r"\\Sigma_\\pi", r"\\bm{\\Sigma}_\\pi"),
    (r"\\Sigma_\\eta", r"\\bm{\\Sigma}_\\eta"),
    (r"\\Sigma_F", r"\\bm{\\Sigma}_F"),
    (r"\\Sigma_p", r"\\bm{\\Sigma}_p"),
]
sig_counts = {}
for pat, rep in SIG_RULES:
    sig_counts[pat] = len(re.findall(pat, text))
    text = re.sub(pat, rep, text)

# safety: no bolded alphabet uses (Sigma^* / |Sigma|) should have changed
alphabet_left = len(re.findall(r"\\Sigma(?![_\\])", text))  # plain Sigma remaining
bolded = len(re.findall(r"\\bm\{\\Sigma\}", text))

if failures:
    print("ABORT — anchor failures (file NOT written):")
    for f in failures:
        print("  -", f)
    sys.exit(1)

with open(TEX, "w", encoding="utf-8") as f:
    f.write(text)

print(f"OK: {len(edits)} anchored edits applied.")
print("Bold-Sigma replacement counts:")
for k, v in sig_counts.items():
    print(f"  {k}: {v}")
print(f"total bolded: {bolded}")
print(f"plain (alphabet/other) Sigma remaining: {alphabet_left}")
