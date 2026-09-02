import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.MeanInequalities

open Real

example (x : ℝ) (hx : 0 < x) : Real.log x ≤ x - 1 := Real.log_le_sub_one_of_pos hx
