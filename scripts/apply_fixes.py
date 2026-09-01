#!/usr/bin/env python3
"""Apply A1 + B1-B7 fixes to automata_unified_revised.tex in one pass.

Fixes (from the line-level review report):
  A1  : thm:com-rd-formula zero threshold -> pair-based kappa_pair (def + theorem
        clause + proof + new remark + Open Problem 8 update).
  B1  : move def:unifilar-machine, rem:unifilar-proper-subclass (-> after
        def:controlled-markov) and def:unifilar-lumpable,
        rem:unifilar-support-not-automatic (-> after def:lumpable-quotient)
        out of subsec:oracle-setup into Section 3; touch up
        rem:unifilar-feasibility opening.
  B2  : drop |O| subscripts at lines 249, 15539, 15637, 17657.
  B3  : roadmap sentence for sec:type-discipline.
  B4  : Com -> ComGame in cor:stateless proof (line 6797).
  B5  : beta -> gamma for the discounted-prefix law (lines 2414-2415, 6200-6201),
        + cross-ref to def:discounted-agg.
  B6  : sec:right-cong -> subsec:right-cong (no refs); drop double label
        sec:openproblems (update 3 refs to subsec:open-problems); delete one
        duplicated separator comment.
  B7  : pinching map macro \EA: \mathcal E_{\mathcal A} -> \operatorname{Pinch}_{\mathcal A}.

Every edit asserts its anchor on the ORIGINAL file content before applying.
The rewrite is a single pass over original line numbers.
"""
import sys

PATH = "/home/z/my-project/upload/automata_unified_revised.tex"

with open(PATH, "r", encoding="utf-8") as f:
    lines = f.readlines()  # keep line terminators

n = len(lines)


def L(i):
    """1-indexed accessor, newline stripped."""
    return lines[i - 1].rstrip("\n")


# ---------------- anchor assertions ----------------
ANCHORS = {
    75:  r"\newcommand{\EA}{\mathcal E_{\mathcal A}}",
    249: r"$\Theta_{|\mathcal O|}(\log M)$ mistakes",
    778: "Theorem.",
    10843: r"(Section~\ref{sec:openproblems}).",
    10921: r"(Section~\ref{sec:openproblems}).  Those regimes are stochastic, and by",
    1149: r"\label{sec:right-cong}",
    1867: r"\end{definition}",
    1868: "",
    1869: r"\begin{definition}[$Z$-predictive equivalence]",
    1965: r"\end{definition}",
    1966: "",
    1967: r"\begin{proposition}[Right-Congruence Correspondence in Synchronized Machines]",
    2414: "aggregation, where",
    2415: r"$\mu(u)=(1-\beta)\beta^{|u|}\Pr[\text{prefix }u]$ is a probability measure on",
    6200: r"\mu(u)=(1-\beta)\beta^{|u|}\Pr[\text{prefix }u],",
    6201: r"\qquad \beta\in(0,1),",
    6265: "",
    6266: r"\begin{theorem}[Exact Fixed-Budget Commitment Rate--Distortion Formula]",
    6287: r"Moreover $\ComRD(M)=0$ if and only if $M\ge\kappa_{\mathrm{obs}}(F^{(1)},\mu)$,",
    6293: r"strictly smaller than $\kappa_{\det}(F)$ of Theorem~\ref{thm:commitment-spec}.",
    6315: "For the zero threshold: $\\ComRD(M)=0$ for a given $\\sim$ if and only if every",
    6327: r"symbol for $\mu$-almost every continuation.",
    6328: r"\end{proof}",
    6329: "",
    6330: r"\begin{remark}[Relation to the Three Commitment Notions]",
    6797: r"\Com(M)",
    9305: r"\end{remark}",
    9306: "",
    9307: r"\begin{definition}[Stationary Controlled Unifilar Causal Machine]",
    9332: r"\begin{remark}[The Input-Driven Model Is a Proper Subclass]",
    9358: r"\end{remark}",
    9360: r"\begin{definition}[Unifilar Lumpability]",
    9426: r"\end{remark}",
    9427: "",
    9428: r"\begin{remark}[Necessity of the Feasibility Restriction]",
    9430: "The restriction to feasible triples is not dispensable.  If",
    13874: r"%----------------------------------------------------------------------",
    13875: r"%----------------------------------------------------------------------",
    13876: r"\subsection{Active Realizable Setting}",
    15539: r"minimal skeleton costs $\Theta_{|\mathcal O|}(\log M)$ mistakes, so no",
    15637: r"state-identification mistake complexity is $O_{|\mathcal O|}(\log M)$, so a",
    17239: r"\subsection{Open Problems}",
    17240: r"\label{sec:openproblems}",
    17241: r"\label{subsec:open-problems}",
    17399: r"$M=\kappa_{\mathrm{obs}}(F^{(1)},\mu)$; Remark~\ref{rem:com-rd-scope} shows",
    17594: r"instance-dependent.  See Section~\ref{sec:openproblems}.",
    17657: r"a known minimal skeleton costs only $O_{|\mathcal O|}(\log M)$ mistakes",
}

errors = []
for ln, needle in ANCHORS.items():
    if ln > n:
        errors.append(f"line {ln} out of range")
        continue
    if needle not in L(ln):
        errors.append(f"anchor mismatch at line {ln}: expected {needle!r}, got {L(ln)!r}")
if errors:
    print("ABORT — anchor check failed:")
    for e in errors:
        print("  " + e)
    sys.exit(1)
print(f"All {len(ANCHORS)} anchors verified on original file ({n} lines).")

# ---------------- new content blocks ----------------

B3_SENTENCE = [
    "Section~\\ref{sec:type-discipline} fixes the type signature that every",
    "approximation statement carries.",
]

DEF_PAIR = [
    r"\begin{definition}[One-Step Determination Index]",
    r"\label{def:pair-determination-index}",
    r"The \textbf{one-step determination index} $\kappa_{\mathrm{pair}}(F,\mu)$ is",
    r"the minimum index of a right congruence $\sim$ on $\mathcal I^*$ for which",
    r"$F(u)_{|u|}$ is $\mu$-almost-surely determined by the pair",
    r"$\bigl([u_{1:|u|-1}]_\sim,\,u_{|u|}\bigr)$: explicitly, there exists a map",
    r"$\rho:\bigl(\mathcal I^*/\!\sim\bigr)\times\mathcal I\to\mathcal O$ with",
    r"$\rho\bigl([u_{1:|u|-1}]_\sim,u_{|u|}\bigr)=F(u)_{|u|}$ for $\mu$-almost",
    r"every nonempty $u$.  Only nonempty $u$ carry a one-step output, so the empty",
    r"word --- which has positive mass, $\mu(\varepsilon)=1-\gamma$, under a",
    r"discounted law (Definition~\ref{def:discounted-agg}) --- does not enter the",
    r"condition; the index depends on $\mu$ only through its support.",
    r"\end{definition}",
    "",
]

THM_CLAUSE = [
    r"Moreover $\ComRD(M)=0$ if and only if",
    r"$M\ge\kappa_{\mathrm{pair}}(F,\mu)$, the one-step determination index of",
    r"Definition~\ref{def:pair-determination-index}.  In particular",
    r"$\kappa_{\mathrm{pair}}(F,\mu)\le\kappa_{\det}(F)$, the threshold of",
    r"Theorem~\ref{thm:commitment-spec}: the two indices coincide when $\mu$ has",
    r"full support, and the inequality is strict under restricted supports",
    r"(Remark~\ref{rem:pair-vs-class}).",
]

PROOF_ZERO = [
    r"For the zero threshold: $\ComRD(M)=0$ for a given $\sim$ if and only if every",
    r"visited pair $(k,a)$ has $q_{k,a}$ a point mass, i.e.\ $F(u)_{|u|}$ is",
    r"$\mu$-almost surely determined by $([u_{1:|u|-1}]_\sim,u_{|u|})$, which is",
    r"precisely the determination condition of Definition~\ref{def:pair-determination-index};",
    r"hence $\ComRD(M)=0$ exactly for $M\ge\kappa_{\mathrm{pair}}(F,\mu)$.  The",
    r"inequality $\kappa_{\mathrm{pair}}(F,\mu)\le\kappa_{\det}(F)$ holds because",
    r"the full Myhill--Nerode congruence $\sim_F$ determines the one-step output",
    r"through the pair: $[u_{1:|u|-1}]_{\sim_F}$ determines the residual",
    r"$F_{u_{1:|u|-1}}$, whose value on the one-letter continuation $u_{|u|}$ is",
    r"$F(u)_{|u|}$, so the residual automaton of Theorem~\ref{thm:commitment-spec}",
    r"is one-step exact on all of $\mathcal I^*$.  When $\mu$ has full support the",
    r"reverse inequality holds as well: a pair-determining right congruence then",
    r"forces $u\sim v$ to imply $F_u=F_v$, because each continuation output",
    r"$F(uw)_{|u|+j}$ is a function of $([uw_{1:j-1}]_\sim,w_j)$ and right",
    r"invariance identifies the two arguments along $u$ and $v$.  The two indices",
    r"then coincide, and strictness of the inequality is a support phenomenon, as",
    r"in Remark~\ref{rem:pair-vs-class}.",
]

REM_PAIR = [
    r"\begin{remark}[Why the Pair, Not the Class]",
    r"\label{rem:pair-vs-class}",
    r"Determination by the pair $([u_{1:|u|-1}]_\sim,u_{|u|})$ is strictly weaker",
    r"than determination by the class $[u]_\sim$ alone: the pair refines the",
    r"class, since $[u]_\sim=[u_{1:|u|-1}]_\sim\cdot u_{|u|}$, but a single class",
    r"is reached by many distinct pairs, so a class-level representative is a",
    r"stronger requirement than a pair-level output rule.  For the identity",
    r"transduction $F(u)=u$ over a binary alphabet under a full-support $\mu$,",
    r"every residual coincides, so $\kappa_{\det}(F)=1$: the one-state rule",
    r"$\rho(*,x)=x$ is one-step exact, $\ComRD(1)=0$, and",
    r"$\kappa_{\mathrm{pair}}(F,\mu)=1$, whereas determining $u_{|u|}$ from the",
    r"class $[u]_\sim$ alone requires two classes.  The gap between",
    r"$\kappa_{\mathrm{pair}}$ and $\kappa_{\det}$, by contrast, is a support",
    r"phenomenon: for the transduction $F(u)_t=u_t\oplus u_{t-1}$ (with $u_0=0$)",
    r"the two indices coincide at $2$ under a full-support law, but if the input",
    r"process is supported on strictly alternating words, then $u_{t-1}=1-u_t$ on",
    r"the support, the one-step output is constant there, and",
    r"$\kappa_{\mathrm{pair}}(F,\mu)=1$.",
    r"\end{remark}",
    "",
]

FEAS_TOUCHUP = [
    r"The restriction to feasible triples in Definition~\ref{def:unifilar-lumpable}",
    r"is not dispensable.  If",
]

# B1: extract the moved blocks verbatim from the original lines.
block1 = lines[9307 - 1: 9358] + ["\n"]      # def:unifilar-machine + rem:unifilar-proper-subclass
block2 = lines[9360 - 1: 9426] + ["\n"]      # def:unifilar-lumpable + rem:unifilar-support-not-automatic
assert block1[0].startswith(r"\begin{definition}[Stationary Controlled Unifilar")
assert block1[-2].rstrip("\n") == r"\end{remark}"
assert block2[0].startswith(r"\begin{definition}[Unifilar Lumpability]")
assert block2[-2].rstrip("\n") == r"\end{remark}"

# ---------------- edit plan ----------------
# replace: start_line -> (end_line, new_lines)   [inclusive, 1-indexed]
R = {
    75:   (75,   [r"\newcommand{\EA}{\operatorname{Pinch}_{\mathcal A}}" + "\n"]),
    249:  (249,  [r"$\Theta(\log M)$ mistakes --- the halving upper bound is matched" + "\n"]),
    10843: (10843, [r"(Section~\ref{subsec:open-problems})." + "\n"]),
    10921: (10921, [r"(Section~\ref{subsec:open-problems}).  Those regimes are stochastic, and by" + "\n"]),
    1149: (1149, [r"\label{subsec:right-cong}" + "\n"]),
    2414: (2415, [
        "aggregation (Definition~\\ref{def:discounted-agg}), where\n",
        r"$\mu(u)=(1-\gamma)\gamma^{|u|}\Pr[\text{prefix }u]$ is a probability measure on" + "\n",
    ]),
    6200: (6201, [
        r"\mu(u)=(1-\gamma)\gamma^{|u|}\Pr[\text{prefix }u]," + "\n",
        r"\qquad \gamma\in(0,1)," + "\n",
    ]),
    6287: (6293, [x + "\n" for x in THM_CLAUSE]),
    6315: (6327, [x + "\n" for x in PROOF_ZERO]),
    6797: (6797, [r"\ComGame(M)" + "\n"]),
    9430: (9430, [x + "\n" for x in FEAS_TOUCHUP]),
    15539: (15539, [r"minimal skeleton costs $\Theta(\log M)$ mistakes, so no" + "\n"]),
    15637: (15637, [r"state-identification mistake complexity is $O(\log M)$, so a" + "\n"]),
    17399: (17399, [r"$M=\kappa_{\mathrm{pair}}(F,\mu)$, the one-step determination index; Remark~\ref{rem:com-rd-scope} shows" + "\n"]),
    17594: (17594, [r"instance-dependent.  See Section~\ref{subsec:open-problems}." + "\n"]),
    17657: (17657, [r"a known minimal skeleton costs only $O(\log M)$ mistakes" + "\n"]),
}

# insert_after: line -> new_lines (emitted after that original line)
I = {
    778:   [x + "\n" for x in B3_SENTENCE],
    1868:  block1,
    1966:  block2,
    6265:  [x + "\n" for x in DEF_PAIR],
    6329:  [x + "\n" for x in REM_PAIR],
}

# delete: set of individual lines (expanded from ranges)
D = set(range(9306, 9427))          # B1 cut: blank 9306 + block 9307-9426
D.add(13875)                          # B6c: duplicated separator
D.add(17240)                          # B6b: double label

# conflict check: no line both replaced and deleted or inserted
for s, (e, _) in R.items():
    for ln in range(s, e + 1):
        if ln in D:
            sys.exit(f"CONFLICT: line {ln} both replaced and deleted")
        if ln in I:
            sys.exit(f"CONFLICT: line {ln} both replaced and insert-anchor")

# ---------------- single-pass rewrite ----------------
# Expand replacements to a per-line action map FIRST, so that every line inside
# a replaced range (not only its start) is consumed exactly once.
action = {}  # orig line -> ('REP_FIRST', new_lines) | ('DEL', None)
for s, (e, new) in R.items():
    for ln in range(s, e + 1):
        if ln == s:
            action[ln] = ("REP_FIRST", new)
        else:
            action[ln] = ("DEL", None)
for ln in D:
    action[ln] = ("DEL", None)
# sanity: no line may be both a replacement start and an insert anchor
for ln in I:
    if action.get(ln, ("",))[0] == "REP_FIRST":
        sys.exit(f"CONFLICT: line {ln} is both replacement start and insert anchor")

out = []
for i in range(1, n + 1):
    a = action.get(i)
    if a is None:
        out.append(lines[i - 1])
    elif a[0] == "REP_FIRST":
        out.extend(a[1])
    # else DEL: skip
    if i in I:
        out.extend(I[i])

with open(PATH, "w", encoding="utf-8") as f:
    f.writelines(out)

print(f"Rewrote {PATH}: {n} -> {len(out)} lines "
      f"({len(R)} replacements, {len(I)} insertions, {len(D)} deletions).")
print("Delta:", len(out) - n, "lines (expected: -121 cut + 122 B1 reinsert + 5 A1 blocks/sentence + misc).")
