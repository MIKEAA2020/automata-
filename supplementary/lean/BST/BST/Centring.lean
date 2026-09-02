/-
  Centring lemma behind `thm:global-kl-simplex` (constant 1).

  If `d : ι → ℝ` sums to zero then  ‖d‖₂² ≤ (1/2)‖d‖₁².
  This is the step that upgrades Pinsker's `KL ≥ (1/2)‖·‖₁²` to
  `KL ≥ ‖·‖₂²`, i.e. the constant 1 rather than 1/2.

  Proof: let a = Σ (d i)⁺ = Σ (d i)⁻, so ‖d‖₁ = 2a and ‖d‖_∞ ≤ a.
  Then ‖d‖₂² ≤ ‖d‖_∞ ‖d‖₁ ≤ a · 2a = 2a² = (1/2)‖d‖₁².
-/
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Analysis.MeanInequalities

open Finset

variable {ι : Type*}

/-- `Σ |d i| = Σ (d i)⁺ + Σ (d i)⁻`. -/
lemma abs_sum_eq (s : Finset ι) (d : ι → ℝ) :
    ∑ i ∈ s, |d i| = (∑ i ∈ s, max (d i) 0) + ∑ i ∈ s, max (-d i) 0 := by
  rw [← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl (fun i _ => ?_)
  rcases le_total 0 (d i) with h | h
  · rw [abs_of_nonneg h, max_eq_left h, max_eq_right (by linarith), add_zero]
  · rw [abs_of_nonpos h, max_eq_right h, max_eq_left (by linarith), zero_add]

/-- If `d` sums to zero, the positive and negative parts carry equal mass. -/
lemma pos_eq_neg_part (s : Finset ι) (d : ι → ℝ) (h : ∑ i ∈ s, d i = 0) :
    ∑ i ∈ s, max (d i) 0 = ∑ i ∈ s, max (-d i) 0 := by
  have key : ∑ i ∈ s, (max (d i) 0 - max (-d i) 0) = ∑ i ∈ s, d i := by
    refine Finset.sum_congr rfl (fun i _ => ?_)
    rcases le_total 0 (d i) with hi | hi
    · rw [max_eq_left hi, max_eq_right (by linarith : -d i ≤ 0), sub_zero]
    · rw [max_eq_right hi, max_eq_left (by linarith : (0:ℝ) ≤ -d i), zero_sub, neg_neg]
  rw [Finset.sum_sub_distrib] at key
  linarith [key, h]

/-- Each coordinate is bounded by the mass of its own sign class. -/
lemma abs_le_half_l1 (s : Finset ι) (d : ι → ℝ) (h : ∑ i ∈ s, d i = 0)
    {i : ι} (hi : i ∈ s) : |d i| ≤ (∑ j ∈ s, |d j|) / 2 := by
  have hpn := pos_eq_neg_part s d h
  have hsplit := abs_sum_eq s d
  -- |d i| ≤ Σ (d j)⁺  when d i ≥ 0, and ≤ Σ (d j)⁻ otherwise
  have hp : ∀ j ∈ s, (0:ℝ) ≤ max (d j) 0 := fun j _ => le_max_right _ _
  have hn : ∀ j ∈ s, (0:ℝ) ≤ max (-d j) 0 := fun j _ => le_max_right _ _
  rcases le_total 0 (d i) with hd | hd
  · have : max (d i) 0 ≤ ∑ j ∈ s, max (d j) 0 :=
      Finset.single_le_sum hp hi
    rw [abs_of_nonneg hd]
    rw [max_eq_left hd] at this
    rw [hsplit, ← hpn]
    linarith
  · have : max (-d i) 0 ≤ ∑ j ∈ s, max (-d j) 0 :=
      Finset.single_le_sum hn hi
    rw [abs_of_nonpos hd]
    rw [max_eq_left (by linarith : (0:ℝ) ≤ -d i)] at this
    rw [hsplit, hpn]
    linarith

/-- **Centring lemma.** For a centred vector, `‖d‖₂² ≤ (1/2)‖d‖₁²`. -/
theorem sq_sum_le_half_abs_sum_sq (s : Finset ι) (d : ι → ℝ)
    (h : ∑ i ∈ s, d i = 0) :
    ∑ i ∈ s, (d i)^2 ≤ (∑ i ∈ s, |d i|)^2 / 2 := by
  have hL1 : (0:ℝ) ≤ ∑ i ∈ s, |d i| := Finset.sum_nonneg (fun i _ => abs_nonneg _)
  calc ∑ i ∈ s, (d i)^2
      = ∑ i ∈ s, |d i| * |d i| := by
        refine Finset.sum_congr rfl (fun i _ => ?_)
        rw [sq, abs_mul_abs_self]
    _ ≤ ∑ i ∈ s, ((∑ j ∈ s, |d j|) / 2) * |d i| := by
        refine Finset.sum_le_sum (fun i hi => ?_)
        exact mul_le_mul_of_nonneg_right (abs_le_half_l1 s d h hi) (abs_nonneg _)
    _ = ((∑ j ∈ s, |d j|) / 2) * ∑ i ∈ s, |d i| := by rw [← Finset.mul_sum]
    _ = (∑ i ∈ s, |d i|)^2 / 2 := by ring
