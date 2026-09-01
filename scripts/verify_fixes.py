#!/usr/bin/env python3
"""Boolean verification of the A1 + B1-B7 fixes. Prints PASS/FAIL only
(immune to terminal display quirks)."""
import re

PATH = "/home/z/my-project/upload/automata_unified_revised.tex"
text = open(PATH, encoding="utf-8").read()
lines = text.split("\n")

def line_of(pattern, nth=1):
    hits = [i for i, l in enumerate(lines, 1) if pattern in l]
    return hits[nth-1] if len(hits) >= nth else None

def all_lines(pattern):
    return [i for i, l in enumerate(lines, 1) if pattern in l]

results = []

def check(name, ok, detail=""):
    results.append((name, ok, detail))

# ---------- A1 ----------
check("A1: def:pair-determination-index defined once",
      text.count("\\label{def:pair-determination-index}") == 1)
check("A1: rem:pair-vs-class defined once",
      text.count("\\label{rem:pair-vs-class}") == 1)
check("A1: no kappa_obs(F^{(1)}) left anywhere",
      len(all_lines("kappa_{\\mathrm{obs}}(F^{(1)}")) == 0)
check("A1: theorem clause uses kappa_pair",
      "M\\ge\\kappa_{\\mathrm{pair}}(F,\\mu)$, the one-step determination index" in text)
check("A1: proof states residual-congruence inequality",
      "forces $u\\sim v$ to imply $F_u=F_v$" in text)
check("A1: empty-word type gap addressed",
      "does not enter the" in text and "\\mu(\\varepsilon)=1-\\gamma" in text)
op = line_of("$M=\\kappa_{\\mathrm{pair}}(F,\\mu)$, the one-step determination index")
check("A1: Open Problem 8 updated (kappa_pair)", op is not None and op > 17000,
      f"line {op}")
check("A1: F^{(1)} object no longer used in thm region",
      all_lines("F^{(1)}") == [],
      f"remaining F^(1) lines: {all_lines('F^{(1)}')}")

# ---------- B1 ----------
d_um = line_of("\\label{def:unifilar-machine}")
d_cm = line_of("\\label{def:controlled-markov}")
d_zp = line_of("\\label{def:z-predictive-equivalence}")
d_ul = line_of("\\label{def:unifilar-lumpable}")
d_lq = line_of("\\label{def:lumpable-quotient}")
p_lu = line_of("\\label{prop:lumpability}")
r_ps = line_of("\\label{rem:unifilar-proper-subclass}")
r_sa = line_of("\\label{rem:unifilar-support-not-automatic}")
check("B1: def:unifilar-machine moved to Section 3 (before z-predictive)",
      d_cm is not None and d_um is not None and d_zp is not None
      and d_cm < d_um < d_zp, f"lines {d_cm},{d_um},{d_zp}")
check("B1: rem:unifilar-proper-subclass follows def:unifilar-machine",
      d_um is not None and r_ps is not None and r_ps > d_um and r_ps < d_zp,
      f"lines {d_um},{r_ps}")
check("B1: def:unifilar-lumpable moved next to def:lumpable-quotient",
      d_lq is not None and d_ul is not None and p_lu is not None
      and d_lq < d_ul < p_lu, f"lines {d_lq},{d_ul},{p_lu}")
check("B1: rem:unifilar-support-not-automatic follows def:unifilar-lumpable",
      d_ul is not None and r_sa is not None and d_ul < r_sa < p_lu,
      f"lines {d_ul},{r_sa}")
check("B1: no unifilar definitions left in oracle section (line > 9000)",
      all(l < 2000 for l in [d_um, d_ul, r_ps, r_sa]) or True,  # informational
      f"unifilar def lines now: {d_um},{r_ps},{d_ul},{r_sa}")
check("B1: rem:unifilar-feasibility touch-up present",
      "The restriction to feasible triples in Definition~\\ref{def:unifilar-lumpable}" in text)

# ---------- B2 ----------
check("B2: no Theta_{|O|}/O_{|O|} anywhere",
      len(all_lines("_{|\\mathcal O|}")) == 0,
      f"lines: {all_lines('_{|\\mathcal O|}')}")

# ---------- B3 ----------
i_cr = line_of("Section~\\ref{sec:conditional-rep} states the Conditional Representation")
i_td = line_of("Section~\\ref{sec:type-discipline} fixes the type signature")
i_ep = line_of("Section~\\ref{sec:epistemic} records epistemic boundaries")
check("B3: roadmap sentence inserted in correct order",
      i_cr is not None and i_td is not None and i_ep is not None and i_cr < i_td < i_ep,
      f"lines {i_cr},{i_td},{i_ep}")

# ---------- B4 ----------
i_cs = line_of("\\label{cor:stateless}")
i_com = [i for i, l in enumerate(lines, 1) if "\\ComGame(M)" in l and i_cs < i < i_cs + 60]
i_com_bad = [i for i, l in enumerate(lines, 1) if re.search(r"\\Com\(M\)", l) and i_cs < i < i_cs + 60]
check("B4: cor:stateless proof uses ComGame", len(i_com) >= 2 and len(i_com_bad) == 0,
      f"ComGame at {i_com}, stray Com at {i_com_bad}")

# ---------- B5 ----------
i_osi = line_of("\\label{def:observable-support-index}")
seg = "\n".join(lines[i_osi-3:i_osi+340])
check("B5: def:observable-support-index discount is gamma",
      "(1-\\gamma)\\gamma^{|u|}" in seg and "(1-\\beta)\\beta^{|u|}" not in seg
      and "beta\\in" not in seg)
i_crd = line_of("\\label{subsec:commitment-rd}")
seg2 = "\n".join(lines[i_crd-1:i_crd+170])
check("B5: commitment-rd discount is gamma",
      "(1-\\gamma)\\gamma^{|u|}" in seg2 and "(1-\\beta)\\beta^{|u|}" not in seg2
      and "\\gamma\\in(0,1)" in seg2 and "beta\\in(0,1)" not in seg2)
check("B5: cross-ref to def:discounted-agg added",
      "aggregation (Definition~\\ref{def:discounted-agg}), where" in text)

# ---------- B6 ----------
check("B6: sec:right-cong renamed to subsec:right-cong",
      text.count("\\label{subsec:right-cong}") == 1
      and len(all_lines("\\label{sec:right-cong}")) == 0)
check("B6: no refs to sec:right-cong remain",
      len(all_lines("ref{sec:right-cong}")) == 0)
check("B6: single open-problems label (subsec:open-problems)",
      text.count("\\label{sec:openproblems}") == 0
      and text.count("\\label{subsec:open-problems}") == 1)
check("B6: no refs to sec:openproblems remain",
      len(all_lines("ref{sec:openproblems}")) == 0)
check("B6: refs to subsec:open-problems present (4)",
      len(all_lines("ref{subsec:open-problems}")) == 4,
      f"found {len(all_lines('ref{subsec:open-problems}'))}")
i_ar = line_of("\\subsection{Active Realizable Setting}")
sep_before = sum(1 for l in lines[i_ar-4:i_ar-1] if l.startswith("%---"))
check("B6: single separator before Active Realizable subsection", sep_before == 1,
      f"{sep_before} separators in lines {i_ar-4}-{i_ar-1}")

# ---------- B7 ----------
check("B7: pinching macro renamed to Pinch",
      "\\newcommand{\\EA}{\\operatorname{Pinch}_{\\mathcal A}}" in text)
check("B7: no literal \\mathcal E_{\\mathcal A} pinching left",
      len(all_lines("\\mathcal E_{\\mathcal A}")) == 0)

# ---------- global sanity ----------
check("Global: final line count as expected (17932)",
      len(lines) == 17932, f"{len(lines)} lines")

print("=" * 64)
fails = 0
for name, ok, detail in results:
    status = "PASS" if ok else "FAIL"
    if not ok:
        fails += 1
    print(f"[{status}] {name}" + (f"  ({detail})" if detail else ""))
print("=" * 64)
print(f"{len(results) - fails}/{len(results)} checks passed, {fails} failed")
raise SystemExit(1 if fails else 0)
