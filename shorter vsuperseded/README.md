# Supplementary material

*The Rate–Distortion Theory of Bounded Sequential Transduction:
A Comparative Syntax for Finite-State Approximation*

This package accompanies the manuscript. It contains the Lean 4 formalisation
of the machine-checked fragments, the verification programs behind the
computational observations reported in the text, and the consistency gates used
during preparation. Everything here is self-contained and runs from wherever
the package is unpacked; no path configuration is required.

---

## 1. Contents

```
supplementary/
  README.md              this file
  MANIFEST.txt           SHA-256 of every shipped file
  manuscript.tex         the submitted source, for cross-reference resolution
  open_problems_report.md  companion memorandum (§2.1–§2.41)
  lean4/
    BST/                 Lean 4 project: 7 modules, 17 theorems, 0 sorry
    BUILD.md             build instructions (~3 min from a clean machine)
    README.md            module-by-module description
  verify/                120 verification programs
  tools/                 10 consistency gates
```

Python 3.9 or later. Most programs use only the standard library; a few use
`numpy`, `scipy` or `mpmath` for high-precision arithmetic. Lean requires
`elan`, installed by the script in `lean4/BUILD.md`.

---

## 2. Quick start

```sh
# consistency gates over the manuscript source (seconds)
python3 tools/regression_all.py     # 681 assertions
python3 tools/traceability.py       # 98 programs -> manuscript artefacts
python3 tools/lossscan.py
python3 tools/register.py

# a representative verification (each is standalone)
python3 verify/controlled_ib.py     # controlled IB identity, 4000 machines
python3 verify/rd_convexity.py      # non-convexity witness, 60-digit arithmetic

# the Lean development
cd lean4/BST && lake update && lake build
python3 ../../tools/lean_check.py
```

Scripts locate the manuscript relative to their own directory. To point them at
a different copy, set `BST_ROOT`.

---

## 3. The Lean 4 development

Seven modules, **17 theorems, no `sorry`**, and no axioms beyond Lean's
standard three (`propext`, `Classical.choice`, `Quot.sound`). Verified against
Mathlib at the revision pinned in `lean4/BST/lean-toolchain` (Lean v4.33.0-rc2).

| Module | Theorems | Content |
|---|---|---|
| `Centring.lean` | 4 | `Σdᵢ = 0 ⟹ ‖d‖₂² ≤ ½‖d‖₁²`, the centring step of the sharp constant‑1 converse, with its supporting lemmas |
| `Halving.lean` | 5 | `c₂ ≤ c₁`, `c₁+c₂ ≤ n ⟹ 2c₂ ≤ n`; the alphabet-free halving step and its mistake-count consequence |
| `Sandwich.lean` | 3 | `min{a(M),b(M)} ≤ a(N)+b(N)`; the mediant inequality behind the bounded jump ratio |
| `Anova.lean` | 2 | parallel-axis identity; minimality of the weighted mean |
| `Refine.lean` | 3 | a bounded strictly increasing block count admits at most `M−1` increases; refinement termination |
| `Basic.lean`, `Smoke.lean` | 0 | imports and a build smoke test |

`tools/lean_check.py` rebuilds the project, confirms the absence of `sorry`,
and runs `#print axioms` on all 17 theorems, failing if any depends on an axiom
outside the standard three. It also fails if a theorem in the sources is
missing from its tracked list, so the count cannot drift.

**Scope.** What is formalised is the arithmetic skeleton: inequalities,
identities and counting arguments. Pinsker's inequality is a *hypothesis*
rather than an import; Ky Fan's maximum principle, the Kullback–Leibler
functional itself, and all automata-theoretic constructions — Mealy machines,
version spaces, the adaptive games — are **not** formalised. The surrounding
theorems are therefore not machine-checked end to end. This is stated in the
manuscript at Remark *Machine-Checked Fragments* and is repeated here so the
package cannot be read as claiming more.

---

## 4. The verification programs

The 120 programs in `verify/` are **computational observations**, not proofs.
They enumerate, evaluate or search, and they illustrate or falsify statements;
they do not establish them. Where a theorem's proof depends on a finite
computation, the dependence is stated in the theorem itself.

`tools/traceability.py` maps each tracked program to the manuscript artefact it
supports and reports any program whose target has disappeared.

Representative entries:

| Program | What it checks |
|---|---|
| `controlled_ib.py` | controlled information-bottleneck identity, 4,000 unifilar machines, max deviation 1.8e-16 |
| `controlled_ib_general.py` | the identity without input–state independence; and that the naive unconditional-covariance converse **fails** in 3,504 of 59,817 pairs |
| `controlled_zero_correct.py` | zero-retention threshold at the stable kernel refinement, 85,410 instances |
| `refinement_extremal.py` | the counter family: maximal gap, tight round count, induction checked level by level |
| `rd_convexity.py` | the finite-state curve is not convex; exact 60-digit witness, and non-convexity under both rate parameterisations |
| `alphabet_similarity.py` | `d=2` discriminant obstruction; `d=3` Hadamard similarity reducing `\|O\|` from `2d` to `d+1` |
| `connected_support.py` | connected support is sufficient and non-droppable, 400,000 instances |
| `grounding_tracking.py` | floor-plus-tracking decomposition, 882,447 pairs in exact rational arithmetic |
| `pos_safe_feasibility.py` | safe congruences exist iff `M ≥ r`, 210,010 pairs |

Four programs carry a `SUPERSEDED` banner and are retained for provenance only;
each names its live successor. They are excluded from the traceability map and
should not be cited.

---

## 5. The consistency gates

| Gate | Purpose |
|---|---|
| `regression_all.py` | 681 assertions pinned to mathematical content, one per fix across the revision history |
| `traceability.py` | every tracked verification program resolves to a manuscript artefact |
| `lossscan.py` | no dangling references; every removed label has a recorded disposition |
| `convention.py` | the two spectral conventions are internally coherent and never conflated |
| `check_active.py` | the active-learning claims stay within their protocol |
| `dag.py` | the proof-dependency graph is acyclic |
| `check_report.py` | every label cited in the memorandum resolves |
| `register.py` | detects changelog, strawman, self-praise and informal register |
| `lean_check.py` | rebuilds Lean, audits axioms, guards against untracked theorems |
| `partition.py` | split-safety: for a proposed core, computes closure, bridges and coverage |

All ten pass on the shipped source. `register.py` reports 2 flagged lines,
which is its documented baseline: both are ordinary prose ("the former",
"no longer") that the pattern matches incidentally.

---

## 6. Reproducing the reported figures

Every numeric claim in the manuscript that came from computation is produced by
a named program here. Sampling-based figures use a fixed seed and are
reproducible exactly. High-precision results use `mpmath` at the stated
precision, typically 40–60 significant digits, and the manuscript reports the
precision alongside the figure.

Two conventions are worth flagging to a reader checking the numbers:

- **Numerical checks refute but do not certify.** A search that finds no
  counterexample is reported as such and never as a proof.
- **Exhaustive enumerations state their range.** Where a claim is verified for
  all instances below a size bound, the bound is given, and the claim in the
  manuscript is scoped accordingly or carries a separate proof.
