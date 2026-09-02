#!/usr/bin/env python3
"""v6 revision: address the three non-blocking observations O1/O2/O3 from
Section 5 of remaining_theorems_proof_check.docx, and re-harden the Data and
Code Availability statement for the assembled supplementary package.

Edits (anchored, abort-before-write):
  E1 (O1a) cor:fisher-uniform-remainder: forward reference to thm:local-full-kl
            flagged as "stated immediately below".
  E2 (O1b) cor:controlled-elementary-general proof: forward reference to
            cor:controlled-elementary flagged as the independent-input special
            case stated below.
  E3 (O2, site 1) alphabet-reduction remark: Sylvester-order list qualified;
            other Hadamard orders (d=11, order 12) named.
  E4 (O2, site 2) open-problems summary: same qualification, parallel wording.
  E5 (O3) rem:computational-conventions: independent verification suite and
            supplementary package recorded.
  E6      Data and Code Availability: re-hardened to the assembled package.
"""
import hashlib, sys, pathlib

V6 = pathlib.Path("/home/z/my-project/automata-repo/download/automata_unified_revised_v6.tex")

EDITS = [
    # ---- E1 (O1a): forward reference flagged -------------------------------
    (
        "E1 O1a forward-ref cor:fisher-uniform-remainder",
        "Under the hypotheses of Theorem~\\ref{thm:local-full-kl}, there exists a\n"
        "constant $C<\\infty$ such that, for all sufficiently small $r>0$ and all",
        "Under the hypotheses of Theorem~\\ref{thm:local-full-kl}, stated immediately\n"
        "below, there exists a constant $C<\\infty$ such that, for all sufficiently\n"
        "small $r>0$ and all",
    ),
    # ---- E2 (O1b): forward reference flagged -------------------------------
    (
        "E2 O1b forward-ref cor:controlled-elementary-general",
        "As in Corollary~\\ref{cor:controlled-elementary}, every step being conditional\n"
        "on $X$ and using Theorem~\\ref{thm:controlled-ib-general} in place of\n"
        "Theorem~\\ref{thm:controlled-ib}.",
        "As in Corollary~\\ref{cor:controlled-elementary}, the independent-input special\n"
        "case stated below, every step being conditional on $X$ and using\n"
        "Theorem~\\ref{thm:controlled-ib-general} in place of Theorem~\\ref{thm:controlled-ib}.",
    ),
    # ---- E3 (O2 site 1): Hadamard/Sylvester qualification ------------------
    (
        "E3 O2 site 1 Sylvester qualification",
        "alphabet may thus be taken of size $d+1=4$ rather than $2d=6$.  The same\n"
        "construction applies whenever a Hadamard matrix of order $d+1$ exists, so\n"
        "$|\\mathcal O|=d+1$ suffices for $d=3,7,15,\\dots$, and there the factor two is\n"
        "slack.",
        "alphabet may thus be taken of size $d+1=4$ rather than $2d=6$.  The same\n"
        "construction applies whenever a Hadamard matrix of order $d+1$ exists, so\n"
        "$|\\mathcal O|=d+1$ suffices for $d=3,7,15,\\dots$ --- the Sylvester orders\n"
        "$2^{k}-1$ --- and for every other Hadamard order as well: $d=11$, from the\n"
        "order-$12$ Hadamard matrix, is the smallest qualifier outside the Sylvester\n"
        "pattern.  Wherever an order-$(d+1)$ Hadamard matrix exists, the factor two is\n"
        "slack.",
    ),
    # ---- E4 (O2 site 2): parallel qualification ----------------------------
    (
        "E4 O2 site 2 Sylvester qualification",
        "by the doubling map; $n=d+1$ qualifies for $d=3,7,15,\\dots$, by the\n"
        "non-constant rows of a Hadamard matrix of order $d+1$; and $n=d+1$ fails for\n"
        "$d=2$, by a discriminant obstruction.",
        "by the doubling map; $n=d+1$ qualifies for $d=3,7,15,\\dots$ --- the Sylvester\n"
        "orders --- and for every other Hadamard order, the smallest being $d=11$ of\n"
        "order $12$, by the non-constant rows of a Hadamard matrix of order $d+1$; and\n"
        "$n=d+1$ fails for $d=2$, by a discriminant obstruction.",
    ),
    # ---- E5 (O3): verification suite recorded in the conventions remark ----
    (
        "E5 O3 conventions remark: verification suite",
        "These conventions apply to the retention checks of\n"
        "Remark~\\ref{rem:retention-numerical} and to the machine-table searches of\n"
        "Section~\\ref{sec:temporal}.\n"
        "\\end{remark}",
        "These conventions apply to the retention checks of\n"
        "Remark~\\ref{rem:retention-numerical} and to the machine-table searches of\n"
        "Section~\\ref{sec:temporal}.\n"
        "\n"
        "An independent verification suite reproduces the recomputable subset of these\n"
        "observations exactly --- the counter-family values, both non-convexity\n"
        "instances, the Csisz\\'ar identity, the adaptive-depth and cyclic-shift\n"
        "witnesses, and the random-instance minorant checks --- and re-implements the\n"
        "exhaustive searches of Section~\\ref{sec:temporal} under the conventions\n"
        "above; the suite, the machine tables of the extremal witnesses, and its\n"
        "exact outputs are distributed as part of the supplementary package.\n"
        "\\end{remark}",
    ),
    # ---- E6: availability statement re-hardened ----------------------------
    (
        "E6 availability re-hardened",
        "the dependence is stated in the theorem.  The corresponding programs, the\n"
        "extremal machine tables, the exact outputs, and the Lean development of\n"
        "Remark~\\ref{rem:lean-formalization} are being prepared as supplementary\n"
        "material and will be made available upon publication; they are not part of\n"
        "the present submission package.",
        "the dependence is stated in the theorem.  The corresponding programs, the\n"
        "extremal machine tables, and the exact outputs accompany this manuscript as\n"
        "supplementary material: the package contains the numerical verification\n"
        "suite together with the exact outputs of every check reported above, the\n"
        "enumeration programs implementing the conventions of\n"
        "Remark~\\ref{rem:computational-conventions}, the machine tables of the\n"
        "extremal witnesses, and the statement manifest of the Lean development of\n"
        "Remark~\\ref{rem:lean-formalization}, which documents its fifteen\n"
        "machine-checked statements and their scope.",
    ),
]

text = V6.read_text()
orig_md5 = hashlib.md5(text.encode()).hexdigest()
print(f"v6 before edits: {len(text.splitlines())} lines, md5 {orig_md5}")

for name, old, new in EDITS:
    n = text.count(old)
    if n != 1:
        print(f"ABORT: anchor for {name!r} found {n} times (expected 1)")
        sys.exit(1)

for name, old, new in EDITS:
    text = text.replace(old, new, 1)
    print(f"applied: {name}")

V6.write_text(text)
new_md5 = hashlib.md5(text.encode()).hexdigest()
print(f"v6 after edits: {len(text.splitlines())} lines, md5 {new_md5}")
print("OK")
