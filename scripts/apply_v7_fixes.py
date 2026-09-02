#!/usr/bin/env python3
"""v7 revision: six anchored edits (abort-before-write).

E1  Price of Safety disambiguation footnote at first occurrence (Introduction),
    with corrected citation (arXiv:2309.08709, not 2508.20246) and
    multi-instantiation strengthening (PoSquad / PoSlin / cor:price-safety).
E2  Grounding-gap disambiguation footnote at first occurrence (Introduction).
E3  Lean count correction: fifteen -> seventeen statements, seven modules,
    named axioms, sources/build/audit shipped (matches the actual BST project
    and the companion manuscript's own wording).
E4  Availability statement: Lean component points at the actual development
    (17 statements, 7 modules, build script, axiom-audit gate).
E5  Capitalization consistency: "The price of safety is" -> "The Price of
    Safety is" (cor:price-safety body; only lowercase lapse in the file).
E6  Two bibliography entries: shang2023 (2309.08709), shaikh2023grounding
    (2311.09144).
"""
import sys, hashlib

SRC = '/home/z/my-project/automata/download/automata_unified_revised_v6.tex'
DST = '/home/z/my-project/automata/download/automata_unified_revised_v7.tex'
V6_MD5 = 'df384d6facf47ba36776261adb948850'

text = open(SRC, errors='replace').read()
if hashlib.md5(text.encode()).hexdigest() != V6_MD5:
    sys.exit('ABORT: v6 md5 mismatch - frozen file was modified')

edits = []

# ---------------------------------------------------------------- E1
e1_old = """block-local problem but is not the discrete right-congruence Price of Safety
without relaxation-error control."""
e1_new = """block-local problem but is not the discrete right-congruence Price of
Safety\\footnote{Here and throughout, ``Price of Safety'' is this manuscript's
safety-constraint gap --- the free optimum minus the safety-constrained
optimum --- instantiated as the discrete right-congruence quantity $\\PoSquad$
and its linear surrogate $\\PoSlin$ of Section~\\ref{sec:pos-linear}, and in
mutual-information form as the $\\operatorname{PoS}(M)$ of
Corollary~\\ref{cor:price-safety}.  It is unrelated to the same phrase in the
safe-bandits literature, where it denotes the additional sample complexity
incurred under stage-wise safety constraints in best-arm identification
\\cite{shang2023}.}
without relaxation-error control."""
edits.append(('E1 PoS footnote', e1_old, e1_new))

# ---------------------------------------------------------------- E2
e2_old = """quotient-typed \\emph{symbolic} grounding gap, over deterministic Mealy
machines, whose resource is again a right-congruence index and which is"""
e2_new = """quotient-typed \\emph{symbolic} grounding
gap\\footnote{As used here, a ``grounding gap'' is a quotient-typed
approximation cost: the discounted symbolic quantity
$\\Delta_{\\mathrm{grd}}(M;\\gamma)$ of
Definition~\\ref{def:symbolic-grounding-gap} together with its linear
finite-rank relatives $\\Dunres(M)$ and $\\DHankstr(M)$ of
Section~\\ref{sec:grounding}.  The term has no connection to its
natural-language-processing sense, where a grounding gap is a language
model's failure to establish conversational common ground or to connect its
generated outputs to the external world \\cite{shaikh2023grounding}.}, over
deterministic Mealy machines, whose resource is again a right-congruence
index and which is"""
edits.append(('E2 grounding-gap footnote', e2_old, e2_new))

# ---------------------------------------------------------------- E3
e3_old = """block count admits at most $M-1$ increases.  Fifteen statements are checked in
total, with no appeal to \\texttt{sorry} and no axioms beyond Lean's standard
three."""
e3_new = """block count admits at most $M-1$ increases.  Seventeen statements are checked
in total, across seven modules, with no appeal to \\texttt{sorry} and no axioms
beyond Lean's standard three, namely propositional extensionality, the axiom
of choice, and quotient soundness.  The sources, a build script, and the axiom
audit accompany the manuscript as supplementary material."""
edits.append(('E3 Lean seventeen', e3_old, e3_new))

# ---------------------------------------------------------------- E4
e4_old = """the machine tables of the
extremal witnesses, and the statement manifest of the Lean development of
Remark~\\ref{rem:lean-formalization}, which documents its fifteen
machine-checked statements and their scope."""
e4_new = """the machine tables of the
extremal witnesses, and the Lean~4 development of
Remark~\\ref{rem:lean-formalization} itself: the seventeen machine-checked
statements in their seven modules, together with the build script and the
axiom-audit gate that recompiles the development and verifies every statement
against Lean's standard three axioms."""
edits.append(('E4 availability', e4_old, e4_new))

# ---------------------------------------------------------------- E5
e5_old = """See Remark~\\ref{rem:no-lower-constraint}.
The price of safety is"""
e5_new = """See Remark~\\ref{rem:no-lower-constraint}.
The Price of Safety is"""
edits.append(('E5 cap fix', e5_old, e5_new))

# ---------------------------------------------------------------- E6
e6_old = """\\end{thebibliography}"""
e6_new = """\\bibitem{shang2023}
X.~Shang, I.~Colin, M.~Barlier, and H.~Cherkaoui,
``Price of safety in linear best arm identification,''
arXiv:2309.08709 [cs.LG], 2023.

\\bibitem{shaikh2023grounding}
O.~Shaikh, K.~Gligori\\'c, A.~Khetan, M.~Gerstgrasser, D.~Yang, and
D.~Jurafsky,
``Grounding gaps in language model generations,''
arXiv:2311.09144 [cs.CL], 2023.

\\end{thebibliography}"""
edits.append(('E6 bibitems', e6_old, e6_new))

# ---------------------------------------------------------------- apply
for name, old, new in edits:
    n = text.count(old)
    if n != 1:
        sys.exit(f'ABORT: anchor for {name} found {n} times (need exactly 1)')
    text = text.replace(old, new, 1)
    print(f'applied {name}')

open(DST, 'w').write(text)
print(f'wrote {DST} ({len(text)} chars, {text.count(chr(10))+1} lines)')
