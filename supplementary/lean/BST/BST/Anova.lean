/-
  ANOVA / variance decomposition used in `thm:global-kl-simplex`:
      Σ_p = W_φ + B_φ.
  Scalar form: for weights w summing to 1 and values x, with mean m,
      Σ w i (x i - c)² = Σ w i (x i - m)² + (m - c)²
  (bias-variance / parallel-axis).  Taking c the global mean and summing over
  blocks gives total = within + between, which is what Ky Fan is applied to.
-/
import Mathlib.Algebra.BigOperators.Field
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

open Finset

variable {ι : Type*}

/-- **Parallel axis / bias–variance identity.** -/
theorem parallel_axis (s : Finset ι) (w x : ι → ℝ) (c : ℝ)
    (hw : ∑ i ∈ s, w i = 1) :
    ∑ i ∈ s, w i * (x i - c)^2
      = (∑ i ∈ s, w i * (x i - (∑ j ∈ s, w j * x j))^2)
        + ((∑ j ∈ s, w j * x j) - c)^2 := by
  set m := ∑ j ∈ s, w j * x j with hm
  -- cross term vanishes
  have hcross : ∑ i ∈ s, w i * (x i - m) = 0 := by
    have h1 : ∑ i ∈ s, w i * (x i - m) = (∑ i ∈ s, w i * x i) - (∑ i ∈ s, w i * m) := by
      rw [← Finset.sum_sub_distrib]
      exact Finset.sum_congr rfl (fun i _ => by ring)
    have h2 : ∑ i ∈ s, w i * m = m := by rw [← Finset.sum_mul, hw, one_mul]
    rw [h1, h2, hm]; ring
  -- expand the LHS termwise into three summands
  have hexp : ∑ i ∈ s, w i * (x i - c)^2
      = ∑ i ∈ s, (w i * (x i - m)^2 + (2*(m-c)) * (w i * (x i - m)) + (m-c)^2 * w i) :=
    Finset.sum_congr rfl (fun i _ => by ring)
  rw [hexp, Finset.sum_add_distrib, Finset.sum_add_distrib,
      ← Finset.mul_sum, ← Finset.mul_sum, hcross, hw]
  ring

/-- Consequence: the within-block cost is minimized at the block mean. -/
theorem mean_minimizes (s : Finset ι) (w x : ι → ℝ) (c : ℝ)
    (hw : ∑ i ∈ s, w i = 1) :
    ∑ i ∈ s, w i * (x i - (∑ j ∈ s, w j * x j))^2 ≤ ∑ i ∈ s, w i * (x i - c)^2 := by
  rw [parallel_axis s w x c hw]
  linarith [sq_nonneg ((∑ j ∈ s, w j * x j) - c)]
