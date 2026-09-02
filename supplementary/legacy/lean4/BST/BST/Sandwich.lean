/-
  `lem:discrete-bv-sandwich` and `lem:kappa-bounded` (Turns 21, 23).

  a nonincreasing, b nondecreasing, both positive.
    B = sup_M min(a M, b M),   A = inf_M (a M + b M).
  Then B ≤ A.  (The reverse A ≤ (1+κ)B needs the crossing index; the
  direction below is the one used to convert a min-floor into a sum bound.)

  Plus: the mediant inequality behind the κ bound for sums of envelopes.
-/
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-- **Sandwich, left inequality, pointwise form.**
For any `M` and any `N`: `min (a M) (b M) ≤ a N + b N`,
given `a` nonincreasing and `b` nondecreasing and both nonnegative. -/
theorem min_le_sum {a b : ℕ → ℝ}
    (ha : ∀ {i j}, i ≤ j → a j ≤ a i)          -- a nonincreasing
    (hb : ∀ {i j}, i ≤ j → b i ≤ b j)          -- b nondecreasing
    (ha0 : ∀ i, 0 ≤ a i) (hb0 : ∀ i, 0 ≤ b i)
    (M N : ℕ) : min (a M) (b M) ≤ a N + b N := by
  rcases le_total M N with h | h
  · -- N ≥ M : b N ≥ b M ≥ min
    have : b M ≤ b N := hb h
    calc min (a M) (b M) ≤ b M := min_le_right _ _
      _ ≤ b N := this
      _ ≤ a N + b N := by linarith [ha0 N]
  · -- N < M : a N ≥ a M ≥ min
    have : a M ≤ a N := ha h
    calc min (a M) (b M) ≤ a M := min_le_left _ _
      _ ≤ a N := this
      _ ≤ a N + b N := by linarith [hb0 N]

/-- **Mediant inequality**, the step behind `κ` for a sum of envelopes:
`(x₁+x₂)/(y₁+y₂) ≤ max (x₁/y₁) (x₂/y₂)` for positive denominators. -/
theorem mediant_le_max {x₁ x₂ y₁ y₂ : ℝ}
    (hy₁ : 0 < y₁) (hy₂ : 0 < y₂) (hx₁ : 0 ≤ x₁) (hx₂ : 0 ≤ x₂) :
    (x₁ + x₂) / (y₁ + y₂) ≤ max (x₁ / y₁) (x₂ / y₂) := by
  set m := max (x₁ / y₁) (x₂ / y₂) with hm
  have hy : 0 < y₁ + y₂ := by linarith
  have e₁ : x₁ = (x₁ / y₁) * y₁ := (div_mul_cancel₀ x₁ (ne_of_gt hy₁)).symm
  have e₂ : x₂ = (x₂ / y₂) * y₂ := (div_mul_cancel₀ x₂ (ne_of_gt hy₂)).symm
  have h₁ : x₁ ≤ m * y₁ := by
    rw [e₁]; exact mul_le_mul_of_nonneg_right (le_max_left _ _) (le_of_lt hy₁)
  have h₂ : x₂ ≤ m * y₂ := by
    rw [e₂]; exact mul_le_mul_of_nonneg_right (le_max_right _ _) (le_of_lt hy₂)
  rw [div_le_iff₀ hy]
  nlinarith [h₁, h₂]

/-- **Jump-ratio monotonicity, multiplicative core.**
If `u` and `v` are nonincreasing and positive then so is their product,
so the supremum of `b M / b (M-1)` is attained at the smallest index. -/
theorem mul_nonincreasing {u v : ℕ → ℝ}
    (hu : ∀ {i j}, i ≤ j → u j ≤ u i) (hv : ∀ {i j}, i ≤ j → v j ≤ v i)
    (hu0 : ∀ i, 0 ≤ u i) (hv0 : ∀ i, 0 ≤ v i)
    {i j : ℕ} (hij : i ≤ j) : u j * v j ≤ u i * v i :=
  mul_le_mul (hu hij) (hv hij) (hv0 j) (hu0 i)
