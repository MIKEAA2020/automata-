#!/usr/bin/env python3
"""v6 structural + edit verification.
Part A: the 6 anchored edits present, pre-edit text absent, v5 frozen intact.
Part B: labels / refs / environments / brace balance on v6."""
import re, hashlib, pathlib
from collections import Counter

repo = pathlib.Path("/home/z/my-project/automata-repo")
v6 = (repo / "download/automata_unified_revised_v6.tex").read_text()
v5 = (repo / "download/automata_unified_revised_v5.tex").read_text()

ok = True
def check(name, cond, detail=""):
    global ok
    print(f"[{'PASS' if cond else 'FAIL'}] {name} {detail}")
    if not cond: ok = False

# ---- Part A: edits ----
check("v5 frozen and untouched", v5 != v6 and hashlib.md5(v5.encode()).hexdigest() == "21db11d21455980caf86013ac501edee")
check("E1 present", "stated immediately\nbelow, there exists a constant $C<\\infty$" in v6)
check("E1 old absent", "Theorem~\\ref{thm:local-full-kl}, there exists a" not in v6)
check("E2 present", "the independent-input special\ncase stated below" in v6)
check("E2 old absent", "As in Corollary~\\ref{cor:controlled-elementary}, every step" not in v6)
check("E3 present", "the Sylvester orders\n$2^{k}-1$ --- and for every other Hadamard order" in v6)
check("E3 old absent", "suffices for $d=3,7,15,\\dots$, and there the factor two is" not in v6)
check("E4 present", "the smallest being $d=11$ of\norder $12$" in v6)
check("E4 old absent", "qualifies for $d=3,7,15,\\dots$, by the\nnon-constant rows" not in v6)
check("E5 present", "An independent verification suite reproduces the recomputable subset" in v6)
check("E5 old absent", v6.count("These conventions apply to the retention checks") == 1)
check("E6 present", "accompany this manuscript as\nsupplementary material" in v6)
check("E6 old absent", "are being prepared as supplementary" not in v6)
check("O1/O2 sites count: Sylvester mentions", v6.count("Sylvester") >= 3)
check("d=11 named at both sites", v6.count("d=11") == 2 or v6.count("d=11") >= 2)

# ---- Part B: structure ----
labels = re.findall(r"\\label\{([^}]*)\}", v6)
dupes = [l for l, c in Counter(labels).items() if c > 1]
refs = re.findall(r"\\(?:eq)?ref\{([^}]*)\}", v6)
undefined = [r for r in refs if r not in set(labels)]
check("labels: no duplicates", not dupes, f"{len(labels)} labels, dupes={dupes}")
check("refs: none undefined", not undefined, f"{len(refs)} refs, undefined={list(set(undefined))[:5]}")

begins = re.findall(r"\\begin\{(\w+\*?)\}", v6)
ends = re.findall(r"\\end\{(\w+\*?)\}", v6)
env_mismatch = [e for e in Counter(begins) if Counter(begins)[e] != Counter(ends)[e]]
check("environments matched", not env_mismatch, f"{len(begins)} begins")

bal = v6.count("{") - v6.count("}")
check("brace balance 0", bal == 0, f"delta={bal}")

print()
print("ALL v6 CHECKS:", "PASS" if ok else "SOME FAILED")
