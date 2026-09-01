#!/usr/bin/env python3
"""
Second-pass C1 fixes on automata_unified_revised_v3.tex:
  - display the long inline formula in prop:grounding-tracking proof (74pt box)
  - display the numeric weights tuple in thm:retention-reset-np proof (40.7pt)
  - display the direct-sum lower bound inline (38.3pt)
  - display the minimax Littlestone inline (36.3pt)
  - display the alpha-divergence generator family inline (34.0pt)
  - reword right-congruence/lumpability compound (27.0pt)
  - three-line break for the F-item value list in def:type-signature (27.4pt)
  - \\emergencystretch for the small-box tail (C1: 'a pass with \\sloppy or
    microtype would clear most of them' - emergencystretch is the safe variant)
Anchor-asserted, abort before write on failure.
"""
import sys

TEX = "/home/z/my-project/download/automata_unified_revised_v3.tex"

with open(TEX, encoding="utf-8") as f:
    text = f.read()

edits = []

# ---- emergencystretch (safe rescue for small overfulls; rescues only bad lines)
edits.append((
    "preamble emergencystretch",
    "\\usepackage{xcolor}\n\\usepackage{microtype}",
    "\\usepackage{xcolor}\n\\usepackage{microtype}\n\\setlength{\\emergencystretch}{2em}",
))

# ---- A5 residue: display the sum comparison (74pt box)
edits.append((
    "display sum comparison",
    """Applying this to every block of $\\mathcal P_\\psi$ and summing gives
$\\sum_{C'\\in\\mathcal P_\\phi}\\max_b\\sum_{s\\in C'}w_s(b)
\\ge\\sum_{C\\in\\mathcal P_\\psi}\\max_b\\sum_{s\\in C}w_s(b)$, and subtracting from
$\\sigma_1$ reverses the inequality to $D(\\phi)\\le D(\\psi)$.""",
    """Applying this to every block of $\\mathcal P_\\psi$ and summing gives
\\[
\\sum_{C'\\in\\mathcal P_\\phi}\\max_b\\sum_{s\\in C'}w_s(b)
\\ \\ge\\
\\sum_{C\\in\\mathcal P_\\psi}\\max_b\\sum_{s\\in C}w_s(b),
\\]
and subtracting from $\\sigma_1$ reverses the inequality to $D(\\phi)\\le D(\\psi)$.""",
))

# ---- numeric weights tuple -> display (40.7pt box)
edits.append((
    "display weights tuple",
    """partition is lumpable, stationary weights proportional to
$(0.0344,0.3506,0.1906,0.2176,0.2068)$, and predictive laws the row
normalizations of""",
    """partition is lumpable, stationary weights proportional to
\\[
(0.0344,\\ 0.3506,\\ 0.1906,\\ 0.2176,\\ 0.2068),
\\]
and predictive laws the row normalizations of""",
))

# ---- direct-sum lower bound inline -> display (38.3pt box)
edits.append((
    "display direct-sum bound",
    """A direct-sum instance forces its two components on disjoint rounds, giving
$\\MistRI(M)\\ge S_M+C_M$, but no non-degenerate two-term decomposition of the""",
    """A direct-sum instance forces its two components on disjoint rounds, giving
\\[
\\MistRI(M)\\ \\ge\\ S_M+C_M,
\\]
but no non-degenerate two-term decomposition of the""",
))

# ---- minimax Littlestone inline -> display (36.3pt box)
edits.append((
    "display minimax bound",
    """\\cite{bendavid2009,daniely2014} gives
$R_T^{\\mathrm{agn}}=\\Omega(\\sqrt{T\\,\\Ldim(\\mathcal H_M)})$ whenever the
Littlestone dimension is witnessed by a mistake tree realizable in the""",
    """\\cite{bendavid2009,daniely2014} gives
\\[
R_T^{\\mathrm{agn}}=\\Omega\\bigl(\\sqrt{T\\,\\Ldim(\\mathcal H_M)}\\bigr)
\\]
whenever the Littlestone dimension is witnessed by a mistake tree realizable in the""",
))

# ---- alpha-divergence family inline -> display (34.0pt box)
edits.append((
    "display divergence family",
    """Sweeping the $\\alpha$-divergence family
$g_\\alpha(t)=(t^\\alpha-1-\\alpha(t-1))/(\\alpha(\\alpha-1))$ through
$\\alpha\\in\\{-1,0,\\tfrac12,0.9,0.99,1,1.01,\\tfrac32,2,3\\}$, the defect in""",
    """Sweeping the $\\alpha$-divergence family
\\[
g_\\alpha(t)=\\frac{t^\\alpha-1-\\alpha(t-1)}{\\alpha(\\alpha-1)}
\\]
through $\\alpha\\in\\{-1,0,\\tfrac12,0.9,0.99,1,1.01,\\tfrac32,2,3\\}$, the defect in""",
))

# ---- right-congruence/lumpability compound (27.0pt box)
edits.append((
    "reword slash compound",
    """\\item \\textbf{Right-congruence constraint.}
The linear surrogate drops the right-congruence/lumpability constraint.""",
    """\\item \\textbf{Right-congruence constraint.}
The linear surrogate drops the right-congruence and lumpability constraints.""",
))

# ---- F-item three-line break (27.4pt box)
edits.append((
    "F item three lines",
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
    """\\item the feasible set
\\[
\\begin{aligned}
\\mathsf F\\in\\bigl\\{&\\text{right congruences},\\
\\text{support-relative right congruences},\\\\
&\\text{lumpable quotients},\\ \\text{unifilar-lumpable quotients},\\
\\text{history factors},\\\\
&\\text{unrestricted rank-}M,\\ \\text{Hankel-restricted}\\bigr\\};
\\end{aligned}
\\]""",
))

text2 = text
failures = []
for name, old, new in edits:
    n = text2.count(old)
    if n != 1:
        failures.append(f"{name}: anchor count = {n} (expected 1)")
        continue
    text2 = text2.replace(old, new)

if failures:
    print("ABORT — anchor failures (file NOT written):")
    for f in failures:
        print("  -", f)
    sys.exit(1)

with open(TEX, "w", encoding="utf-8") as f:
    f.write(text2)
print(f"OK: {len(edits)} second-pass C1 fixes applied.")
