# Lean 4 Development — Sources, Gate, and Statement Manifest

This directory contains the **actual Lean 4 formalization** referenced by the
manuscript remark *Machine-Checked Fragments* (`rem:lean-formalization`).
The development was produced and machine-checked in a companion effort
(Lake project `BST`, Lean `v4.33.0-rc2`, Mathlib at the revision pinned in
`BST/lean-toolchain` / `BST/lake-manifest.json`); the sources are integrated
here verbatim, and their integrity is cross-checkable against the pristine
companion snapshot in `../legacy/` via its `MANIFEST.txt` (SHA-256).

```
lean/
  BST/                  Lake project: 7 modules, 17 tracked declarations, 0 sorry
    BST.lean            root import
    BST/Basic.lean      imports
    BST/Centring.lean   4 declarations (1 theorem + 3 lemmas)
    BST/Halving.lean    5 theorems
    BST/Sandwich.lean   3 theorems
    BST/Anova.lean      2 theorems
    BST/Refine.lean     3 theorems
    BST/Smoke.lean      build smoke test
  BUILD.md              how to rebuild (~3 min from a clean machine)
  MODULES.md            module-by-module description (from the companion effort)
  lean_check.py         standing gate: rebuild, sorry-free, axiom audit
  README.md             this file
```

## Statement count — reconciliation note

The manuscript's remark originally said "fifteen statements"; the shipped
project tracks **seventeen declarations** and the companion manuscript
(`../legacy/manuscript.tex`) itself claims seventeen. The reconciliation,
confirmed against the sources (`BST/*.lean`), is:

| Manuscript claim (remark text) | Declarations in the project |
|---|---|
| centring step + "its two supporting lemmas" | `sq_sum_le_half_abs_sum` + `abs_sum_eq`, `pos_eq_neg_part` (and the auxiliary `abs_le_half_l1`) |
| halving step, |O|-independence explicit | `halving_step`, `halving_step_real`, `halving_alphabet_free` (+ `halve_iterate`, `mistakes_le_log`) |
| comparison min{a(M),b(M)} ≤ a(N)+b(N) | `min_le_sum` |
| mediant inequality | `mediant_le_max` (+ `mul_nonincreasing`) |
| parallel-axis identity | `parallel_axis` |
| minimality of the weighted mean | `mean_minimizes` |
| counting core (≤ M−1 increases) | `strict_increase_bounded`, `refinement_rounds_le` (+ `stabilize_absorbing`) |

Counted as declarations: 17. Counted as "statements" in the manuscript's
prose sense (main results + named supporting lemmas): 15, the other two
(`halve_iterate`, `stabilize_absorbing`) being purely technical helpers.
The manuscript (v7) states the directly auditable number — **seventeen
tracked declarations across seven modules** — which is exactly what
`lean_check.py` enforces: it fails if a declaration present in the sources
is missing from its tracked list, so the count cannot drift silently.

## The gate

```sh
python3 lean_check.py
```

It (1) rebuilds the project with `lake build`, (2) confirms the absence of
`sorry`, (3) runs `#print axioms` on all seventeen tracked declarations and
fails if any depends on an axiom outside Lean's standard three
(`propext`, `Classical.choice`, `Quot.sound`), and (4) fails if the sources
contain an untracked declaration. If the Lean toolchain is not installed
(`~/.elan` absent), it degrades to an honest static report (sources present,
sorry-free) rather than a false positive; install the toolchain per
`BUILD.md` to run the full gate.

## Scope (as claimed by the manuscript, and repeated here so the package
cannot be read as claiming more)

What is verified is the arithmetic skeleton: the inequalities, identities
and counting arguments. Pinsker's inequality is a *hypothesis* rather than an
import; Ky Fan's maximum principle, the Kullback–Leibler functional itself,
and all automata-theoretic constructions — Mealy machines, version spaces,
the adaptive games — are **not** formalized, so the surrounding theorems are
not verified end to end. `MODULES.md` records the manuscript-site mapping
for each module.
