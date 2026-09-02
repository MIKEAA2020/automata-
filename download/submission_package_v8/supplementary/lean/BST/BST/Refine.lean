/-
  `prop:lsyncu-single-input` (Turn 26): Moore refinement on a unary automaton
  stabilizes within M-1 rounds.

  Abstract core: a sequence of partition block-counts `f : ℕ → ℕ` that
  (i) starts at ≥ 1, (ii) is bounded by M, and (iii) STRICTLY increases until
  it stabilizes, can have at most M-1 strict increases.
-/
import Mathlib.Data.Nat.Basic
import Mathlib.Tactic.Common
import Mathlib.Tactic.Linarith

/-- If `f` is strictly monotone on `[0,R)` with `1 ≤ f 0` and `f i ≤ M`,
then `R ≤ M - 1`. -/
theorem strict_increase_bounded {f : ℕ → ℕ} {M R : ℕ}
    (h1 : 1 ≤ f 0) (hM : ∀ i, f i ≤ M)
    (hstrict : ∀ i, i < R → f i < f (i+1)) :
    R ≤ M - 1 := by
  -- f R ≥ f 0 + R by induction on the strict increases
  have key : ∀ k, k ≤ R → f 0 + k ≤ f k := by
    intro k
    induction k with
    | zero => intro _; omega
    | succ n ih =>
      intro hn
      have hn' : n ≤ R := by omega
      have h := ih hn'
      have hs := hstrict n (by omega)
      omega
  have := key R (le_refl R)
  have hb := hM R
  omega

/-- Each effective refinement round splits at least one block, so the number
of rounds before stabilization is at most `M - 1` for an `M`-state machine. -/
theorem refinement_rounds_le {blocks : ℕ → ℕ} {M R : ℕ}
    (hstart : 1 ≤ blocks 0)
    (hbound : ∀ i, blocks i ≤ M)
    (hsplit : ∀ i, i < R → blocks i < blocks (i+1)) :
    R ≤ M - 1 :=
  strict_increase_bounded hstart hbound hsplit

/-- Stabilization is absorbing: if a refinement step fails to split, the
partition is fixed forever.  Abstractly: if `g` is idempotent-on-fixpoints and
`g p = p`, then iterating `g` keeps `p`. -/
theorem stabilize_absorbing {α : Type*} (g : α → α) (p : α) (h : g p = p) :
    ∀ n, g^[n] p = p := by
  intro n
  induction n with
  | zero => simp
  | succ k ih => rw [Function.iterate_succ_apply', ih, h]
