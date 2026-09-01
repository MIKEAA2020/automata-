#!/usr/bin/env python3
"""v4 pass 3: remaining bare-Nerode standardization (E5 item 4)."""
import sys

PATH = "/home/z/my-project/download/automata_unified_revised_v4.tex"
src = open(PATH, encoding="utf-8").read()

edits = [
    ("NER-task-theory",
     "For any task theory $\\mathbb T$, the \\textbf{Nerode equivalence}",
     "For any task theory $\\mathbb T$, the \\textbf{Myhill--Nerode equivalence}"),
    ("NER-joint",
     "space and induce Nerode right congruences",
     "space and induce Myhill--Nerode right congruences"),
    ("NER-joint2",
     "that refines every component Nerode congruence and therefore realizes every",
     "that refines every component Myhill--Nerode congruence and therefore realizes every"),
    ("NER-typedisc",
     "holds only with the Nerode relation restricted to $\\operatorname{supp}\\mu$",
     "holds only with the Myhill--Nerode relation restricted to $\\operatorname{supp}\\mu$"),
]

nfail = 0
for name, old, new in edits:
    c = src.count(old)
    if c != 1:
        print(f"ANCHOR FAIL [{name}]: count = {c}")
        nfail += 1
if nfail:
    sys.exit(1)
for name, old, new in edits:
    src = src.replace(old, new, 1)
    print(f"applied: {name}")
open(PATH, "w", encoding="utf-8").write(src)
print(f"PASS 3 complete: {len(edits)} edits applied")
