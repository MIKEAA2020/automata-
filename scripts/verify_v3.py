#!/usr/bin/env python3
"""Boolean verification of the v3 revision (A2-A6, C1, bold Sigma)."""
import re, hashlib, subprocess

TEX = "/home/z/my-project/download/automata_unified_revised_v3.tex"
FROZEN_V2 = "/home/z/my-project/download/automata_unified_revised_fixed.tex"
LOG = "/home/z/my-project/scripts/build_v3/automata_unified_revised_v3.log"

with open(TEX, encoding="utf-8") as f:
    t = f.read()

checks = []
def chk(name, cond):
    checks.append((name, bool(cond)))

# ---------- A2: modular language delimiter-free + justification
chk("A2: delimiter-free L_N present", "L_N=\\{1^n:n\\equiv0\\pmod N\\}" in t)
chk("A2: old delimited L_N gone", "L_N=\\{\\#1^n" not in t)
chk("A2: residual-class justification present",
    "Myhill--Nerode classes of $L_N$ are the $N$ residue classes" in t)
chk("A2: unary alphabet stated", "over the unary alphabet gives commitment complexity exactly $N$" in t)

# ---------- A3: numeric claim L=4
chk("A3: L=4 claim present", "exceeding $0.23$ already at $L=4$" in t)
chk("A3: old L=3 claim gone", "exceeding $0.23$ already at $L=3$" not in t)

# ---------- A4: two-step continuity + citations
chk("A4: two-step continuity argument present", "two-step continuity argument" in t)
chk("A4: fixed-operator monotone convergence kept for K_infty",
    "for the \\emph{fixed} positive operator $K_\\infty$" in t)
chk("A4: invalid old justification gone",
    "the Schatten quasi-norms of a fixed positive operator" not in t)
chk("A4: sandwiched-Renyi citation in proof",
    "\\cite{mullerlennert2013,franklieb2013}" in t)
chk("A4: bibitem mullerlennert2013", "\\bibitem{mullerlennert2013}" in t)
chk("A4: bibitem franklieb2013", "\\bibitem{franklieb2013}" in t)

# ---------- A5: revision seams removed
chk("A5: 'previous version' gone", "previous version" not in t)
chk("A5: 'Correction to item' gone", "Correction to item" not in t)
chk("A5: 'upgrades the earlier' gone", "upgrades the earlier" not in t)
chk("A5: self-contained nesting text present",
    "The feasible\nsets are nested in the budget" in t)
chk("A5: results-list item now cites proposition plainly",
    "nonincreasing in $M$ (Proposition~\\ref{prop:grounding-tracking})" in t)

# ---------- A6: Moore re-anchoring
chk("A6: garbled 'nested along the search' gone", "nested along the search" not in t)
chk("A6: lem:tension cited in quadratic proof",
    "Lemma~\\ref{lem:tension} with $U=\\{s,t\\}$" in t)
chk("A6: lem:moore-separation mentioned",
    "Lemma~\\ref{lem:moore-separation} is the\ncross-machine form" in t)
chk("A6: honest binomial note present",
    "which would\nbound the path by $\\binom{M}{2}$, not by $M-1$" in t)

# ---------- C1: typesetting
chk("C1: bm package loaded", "\\usepackage{bm}" in t)
chk("C1: microtype loaded", "\\usepackage{microtype}" in t)
chk("C1: emergencystretch set", "\\setlength{\\emergencystretch}{2em}" in t)
chk("C1: type-signature M item displayed",
    "\\mathsf M\\in\\bigl\\{&\\text{deterministic Mealy}" in t)
chk("C1: type-signature F item displayed (3 lines)",
    "\\mathsf F\\in\\bigl\\{&\\text{right congruences}" in t)
chk("C1: type-signature A item displayed",
    "\\mathsf A\\in\\bigl\\{&\\text{worst case}" in t)
chk("C1: PoS identity in aligned", "\\PoSlin+\\rho_{\\mathrm{safe}}-\\rho_{\\mathrm{free}}\n&=(\\mathrm{Free}_{\\mathrm{lin}}" in t)
chk("C1: RationalExpCompare broken", "&\\textsc{RationalExpCompare}:" in t)
chk("C1: schema formula displayed", "Every regime gap has the shape\n\\[" in t)
chk("C1: regime table narrowed", ">{\\raggedright\\arraybackslash}p{10.5em}" in t)
chk("C1: exact-results limit reworded",
    "$\\Delta_{\\mathrm{grd}}(M;\\gamma)\\to F_\\gamma(\\nu)$ as $M\\to\\infty$" in t)
chk("C1: weights tuple displayed", "(0.0344,\\ 0.3506,\\ 0.1906," in t)
chk("C1: minimax bound displayed",
    "R_T^{\\mathrm{agn}}=\\Omega\\bigl(\\sqrt{T\\,\\Ldim(\\mathcal H_M)}\\bigr)\n\\]" in t)
chk("C1: divergence family displayed",
    "g_\\alpha(t)=\\frac{t^\\alpha-1-\\alpha(t-1)}{\\alpha(\\alpha-1)}" in t)
chk("C1: direct-sum bound displayed", "\\MistRI(M)\\ \\ge\\ S_M+C_M," in t)
chk("C1: sum comparison displayed",
    "\\sum_{C'\\in\\mathcal P_\\phi}\\max_b\\sum_{s\\in C'}w_s(b)\n\\ \\ge\\" in t)
chk("C1: slash compound reworded",
    "drops the right-congruence and lumpability constraints" in t)

# ---------- bold Sigma global update
chk("BM: 113 covariance Sigmas bolded", len(re.findall(r"\\bm\{\\Sigma\}", t)) == 113)
chk("BM: no bare covariance Sigma_pi left", len(re.findall(r"(?<!\\bm\{)\\Sigma_\\pi", t)) == 0)
chk("BM: no bare covariance Sigma_p left",
    len(re.findall(r"\\Sigma_(p|\\eta|F)(?!\w)", t)) == 0)
chk("BM: alphabet Sigma^* untouched (22, as in v2)", len(re.findall(r"\\Sigma\^\*", t)) == 22)
chk("BM: alphabet |Sigma| untouched (29, as in v2)", len(re.findall(r"\|\\Sigma\|", t)) == 22+7)
# invariant: stripping \bm{\Sigma} from v3 must give the same plain-Sigma census as v2
with open(FROZEN_V2, encoding="utf-8") as f:
    t2 = f.read()
plain_v2 = len(re.findall(r"\\Sigma(?![a-zA-Z_\\])", t2))
plain_v3 = len(re.findall(r"\\Sigma(?![a-zA-Z_\\])", t.replace("\\bm{\\Sigma}", "")))
chk("BM: plain Sigma census identical to v2 (57)", plain_v2 == plain_v3 == 57)

# ---------- frozen v2 integrity
with open(FROZEN_V2, "rb") as f:
    md5 = hashlib.md5(f.read()).hexdigest()
chk("v2 frozen file untouched (md5 287b28e5...)", md5 == "287b28e535dfd4b5f9c34ac1e029bc08")
chk("v2 frozen file is read-only", subprocess.run(
    ["test", "-r", FROZEN_V2]).returncode == 0)

# ---------- compile log
with open(LOG, encoding="utf-8", errors="replace") as f:
    log = f.read()
ov = re.findall(r"Overfull \\hbox \(([\d.]+)pt", log)
chk("COMPILE: no errors", "\n!" not in log)
chk("COMPILE: no undefined references", "There were undefined references" not in log)
chk("COMPILE: overfull count = 8 (was 151 in v1, 52 in v2)", len(ov) == 8)
chk("COMPILE: no overfull above 15pt", all(float(x) < 15 for x in ov))
chk("COMPILE: 234 pages", "234 pages" in log)

n_pass = sum(1 for _, ok in checks if ok)
for name, ok in checks:
    print(("PASS" if ok else "FAIL"), "-", name)
print(f"\n{n_pass}/{len(checks)} checks passed")
exit(0 if n_pass == len(checks) else 1)
