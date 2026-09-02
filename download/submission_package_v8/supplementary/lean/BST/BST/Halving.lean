/-
  The sharpened halving step behind `prop:esyncsi-log` (Turn 24).

  Version space V partitioned by output symbol into classes of sizes
  c₁ ≥ c₂ ≥ … .  The learner predicts the plurality class.  On a mistake the
  survivors are a SINGLE non-plurality class, of size ≤ c₂.

  Key inequality:  c₁ ≥ c₂  and  c₁ + c₂ ≤ n   ⟹   c₂ ≤ n/2.

  This is what makes the bound ⌊log₂ M⌋ *independent of the alphabet size*,
  replacing the loose factor (1 - 1/|O|).
-/
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Data.Nat.Log
import Mathlib.Tactic.Linarith

/-- **Halving step.** If `c₂ ≤ c₁` and `c₁ + c₂ ≤ n` then `2 * c₂ ≤ n`. -/
theorem halving_step {c₁ c₂ n : ℕ} (hle : c₂ ≤ c₁) (hsum : c₁ + c₂ ≤ n) :
    2 * c₂ ≤ n := by omega

/-- The same over the reals, as used in the manuscript's display. -/
theorem halving_step_real {c₁ c₂ n : ℝ} (hle : c₂ ≤ c₁) (hsum : c₁ + c₂ ≤ n) :
    c₂ ≤ n / 2 := by linarith

/-- Alphabet-freeness: the bound `2 * c₂ ≤ n` makes no reference to the number
of classes `r`.  Formally, for any list of class sizes with the plurality
first, the runner-up is at most half the total, however many classes there are. -/
theorem halving_alphabet_free {r : ℕ} (c : Fin r → ℕ) (hr : 2 ≤ r)
    (i j : Fin r) (hij : i ≠ j)
    (hmax : ∀ k, c k ≤ c i)                      -- i is a plurality class
    (n : ℕ) (htot : c i + c j ≤ n) :             -- two classes fit in the total
    2 * c j ≤ n :=
  halving_step (hmax j) htot

/-- Halving `t` times from `M` leaves at most `M / 2^t`. -/
theorem halve_iterate (M t : ℕ) : M / 2^t ≤ M := Nat.div_le_self _ _

/-- If every mistake at least halves the version space, then after `t`
mistakes the space has size `≤ M / 2^t`; hence at most `Nat.log 2 M`
mistakes can occur before the space is a singleton. -/
theorem mistakes_le_log (M : ℕ) (hM : 1 ≤ M) :
    ∀ t, 2^t ≤ M → t ≤ Nat.log 2 M := by
  intro t ht
  exact (Nat.le_log_iff_pow_le (by norm_num) (by omega)).mpr ht
