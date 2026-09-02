# Lean 4 formalization

Machine-checked fragments of *The Rate–Distortion Theory of Bounded Sequential
Transduction*. Lean 4 (v4.33.0-rc2) + Mathlib.

Build: `cd BST && lake build`.  Gate: `python3 ../../tools/lean_check.py`.

## Status: 15 theorems, 5 substantive modules, no `sorry`, no extra axioms

Every theorem depends only on `propext`, `Classical.choice`, `Quot.sound` —
Lean's three standard axioms — verified via `#print axioms`.

| Module | Formalizes | Manuscript site |
|---|---|---|
| `Centring.lean` | `Σd=0 ⟹ ‖d‖₂² ≤ ½‖d‖₁²`, with the two supporting lemmas (`|d i| ≤ ½‖d‖₁`, positive/negative parts equal) | Step 1 of `thm:global-kl-simplex` — the step giving **constant 1**, not ½ |
| `Halving.lean` | `c₂ ≤ c₁ ∧ c₁+c₂ ≤ n ⟹ 2c₂ ≤ n`; alphabet-freeness; `2^t ≤ M ⟹ t ≤ log₂M` | `prop:esyncsi-log`, the sharpened halving (Turn 24) |
| `Sandwich.lean` | `min(a M, b M) ≤ a N + b N` for monotone envelopes; mediant inequality; product of nonincreasing is nonincreasing | `lem:discrete-bv-sandwich`, `lem:kappa-bounded` (Turns 21, 23) |
| `Anova.lean` | Parallel-axis identity; mean minimizes weighted squared error | ANOVA split `Σ_p = W_φ + B_φ`; `lem:mixture-centroid` (scalar case) |
| `Refine.lean` | Strictly increasing bounded counter ⟹ `R ≤ M-1`; stabilization is absorbing | `prop:lsyncu-single-input` (Turn 26) |

## What is NOT formalized

Deliberately scoped. The following remain proved on paper and checked
numerically only:

- **Pinsker's inequality** — used as a hypothesis; in Mathlib but not wired in.
- **Ky Fan's maximum principle** — the eigenvalue half of the spectral chain.
  `Anova.lean` formalizes the scalar variance decomposition, not the matrix
  trace inequality.
- **KL divergence itself** — `Centring`/`Anova` are the real-analysis skeleton;
  no `Real`-valued KL object is defined.
- **All automata-theoretic content** — Mealy machines, version spaces, the
  adaptive games. `Halving`/`Refine` formalize the *counting cores* of those
  arguments, abstracted from the automata.
- **The APX reduction, the Csiszár characterization, the Fisher no-go.**

So: the load-bearing *inequalities* are machine-checked; the surrounding
constructions are not. A reader should treat this as verification of the
arithmetic skeleton, not of the theorems end to end.
