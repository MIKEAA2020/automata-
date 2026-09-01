#!/usr/bin/env python3
"""verify_v4.py — boolean checks for the v4 revision."""
import re, sys

P = "/home/z/my-project/download/automata_unified_revised_v4.tex"
s = open(P, encoding="utf-8").read()
checks = []

def chk(name, cond):
    checks.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name)

# --- citations
for key in ["shalizicrutchfield2002", "marzencrutchfield2014", "geiger2015",
            "geiger2026", "balle2021", "lacroce2024", "freivalds2008"]:
    cited = len(re.findall(r"\\cite\{[^}]*\b" + key + r"\b[^}]*\}", s))
    bib = s.count("\\bibitem{" + key + "}")
    chk(f"citation {key}: cited={cited} bibitem={bib}", cited >= 1 and bib == 1)

# --- positioning sentences present in the introduction
chk("positioning retention present", "The retention chapter extends the causal-state program" in s)
chk("positioning grounding present", "The grounding chapter transports the" in s)

# --- C2: no bare \textsc problem names (all wrapped in \textup)
chk("C2 all RationalExpCompare wrapped",
    s.count("\\textup{\\textsc{RationalExpCompare}}") == s.count("\\textsc{RationalExpCompare}"))
chk("C2 all PosSLP wrapped",
    s.count("\\textup{\\textsc{PosSLP}}") == s.count("\\textsc{PosSLP}"))
chk("C2 textup-wrapped count >= 6", s.count("\\textup{\\textsc{") >= 6)

# --- C3: abstract compressed
i0 = s.find("\\begin{abstract}\n"); i1 = s.find("\n\\end{abstract}", i0)
abstract = s[i0:i1]
n_disp = abstract.count("\\[")
n_par = abstract.count("\n\n") + 1
chk("C3 abstract has at most 2 displays", n_disp <= 2)
chk("C3 abstract <= 4 paragraphs", n_par <= 4)
chk("C3 abstract mentions all three regimes",
    all(k in abstract for k in ["Commitment", "Retention", "Grounding"]))
chk("C3 intro temporal paragraph present", "Temporal protocols" in s)

# --- D1
chk("D1 Theorem 1 attribution", "Theorem~1 of \\cite{ambainis1996}" in s)
chk("D1 Freivalds 2008 nuance", "Artin's conjecture on primitive roots" in s)

# --- D2
chk("D2 softened availability", "will be made available upon publication" in s)
chk("D2 no old claim", "accompany the manuscript as\nsupplementary material" not in s)

# --- D3
chk("D3 conventions remark present",
    "\\label{rem:computational-conventions}" in s)
nref = len(re.findall(r"Remark~\\ref\{rem:computational-conventions\}", s))
chk(f"D3 cross-references ({nref} >= 5)", nref >= 5)

# --- E1
chk("E1 rem:grounding-aak is compact cross-ref",
    "once, in Remarks~\\ref{rem:aak-eym-hilbert}" in s)
chk("E1 grounding-unrestricted-restricted trimmed", s.count("because restricting the feasible set\ncannot decrease the infimum.  Equality is\nnot guaranteed without additional structure.") == 0)
chk("E1 supremum-org trimmed", "operator-norm tail of\nTheorem~\\ref{thm:spectral-grounding}" in s)
chk("E1 interpretations trimmed", "relaxation gap of\nTheorem~\\ref{thm:spectral-grounding}, the Hankel-structured gap" in s)
chk("E1 retention prefix cross-ref", "recorded once in Remark~\\ref{rem:prefixes-versus-states}" in s)
chk("E1 conclusion prefix cross-ref", "prefix measures, finite prefixes not defining a probability measure over all\nlengths (Remark~\\ref{rem:prefixes-versus-states})" in s)

# --- E2
chk("E2 def:dmax-exponent is anchor", "An anchor for the exponent layer" in s)
chk("E2 thm:grounding-alpha-infty is anchor", "which is the single maintained copy" in s)
chk("E2 no duplicated Dmax display in exponent section",
    s.count("\\sigma^{-1/2}\\rho\\sigma^{-1/2}") <= 3)  # def:dmax, DPI area, rem

# --- E3
chk("E3 discounted collapse note", "For discounted-prefix laws the right-closed case never bites" in s)

# --- E4
chk("E4 transient note", "every\nstationary distribution is supported on the absorbing pair" in s)

# --- E5
chk("E5 tauK defined by intertwining", "\\tau_{\\mathcal K}(k,x)\\eqdef\\phi\\bigl(\\tau(s,x)\\bigr)" in s)
chk("E5 attainment sentence", "The minimum is attained: up to renaming of the quotient states" in s)
chk("E5 sufficiently-large-M qualifier", "and all sufficiently large\n$M$, the passage from the subsequences" in s)
chk("E5 comma splice fixed", "then, $\\mathcal E$ being reflexive by" not in s)
chk("E5 no bare Nerode Equivalence def", "\\begin{definition}[Nerode Equivalence]" not in s)
bare = re.findall(r"(?<!Myhill--)(?<!Myhill-)\bNerode\b(?! classes)", s)
bare = [b for b in bare if "Myhill" not in b]
# count remaining bare uses (some are inside \kappaMN macro etc.)
n_bare = len(re.findall(r"Nerode", s)) - len(re.findall(r"Myhill--Nerode", s)) - len(re.findall(r"Myhill-Nerode", s))
chk(f"E5 bare Nerode uses remaining = {n_bare} (= 0)", n_bare == 0)

# --- AAK precision
chk("AAK multiletter hyp sharpened", "for the transported operator} $UH_\\nu U^{*}$" in s)
chk("AAK multiletter proof chain", "The transport is the same as in the scalar case" in s)
chk("AAK scalar automatic note", "satisfies hypothesis~(a)\nbelow automatically" in s)

# --- structural: labels/refs
labels = re.findall(r"\\label\{([^}]+)\}", s)
refs = re.findall(r"\\ref\{([^}]+)\}", s)
chk("no duplicate labels", len(labels) == len(set(labels)))
undef = set(refs) - set(labels)
chk(f"no undefined refs ({len(undef)})", not undef)
if undef:
    print("  undefined:", sorted(undef)[:10])

# --- structural: environments
envs = re.findall(r"\\begin\{(\w+\*?)\}", s)
ends = re.findall(r"\\end\{(\w+\*?)\}", s)
from collections import Counter
chk("environments matched", Counter(envs) == Counter(ends))

# --- structural: brace balance
chk("brace balance 0", s.count("{") - s.count("}") == 0)

# --- bold Sigma census unchanged vs v3
v3 = open("/home/z/my-project/download/automata_unified_revised_v3.tex", encoding="utf-8").read()
def census(txt):
    return (txt.count("\\bm{\\Sigma}"), txt.count("\\Sigma^*"), txt.count("|\\Sigma|"))
c3, c4 = census(v3), census(s)
# C3 removed the old abstract's 3 bm{Sigma} and 2 |Sigma|; new text added 2 Sigma^*
chk(f"bold Sigma census delta consistent with C3 {c3} -> {c4}",
    c3[0] - c4[0] == 3 and c4[1] - c3[1] == 2 and c3[2] - c4[2] == 2)

nf = sum(1 for _, ok in checks if not ok)
print(f"\n{len(checks)-nf}/{len(checks)} checks PASS")
sys.exit(1 if nf else 0)
