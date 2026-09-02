# Lean 4 Development — Statement Manifest

This directory is the designated home of the manuscript's Lean 4 formalization
described in the remark *Machine-Checked Fragments* (`rem:lean-formalization`)
of the manuscript (Section 5). The development was produced and
machine-checked in Lean 4 against Mathlib in a companion effort; this manifest
records, verbatim from the manuscript, what is claimed, so that the checked
`.lean` sources can be integrated here and audited against the claims.

## What the manuscript claims

Fifteen statements are checked in total, with no appeal to `sorry` and no
axioms beyond Lean's standard three. The named statement blocks are:

1. **The centring step of `thm:global-kl-simplex`** — that
   $\sum_i d_i = 0$ implies $\Vert d\Vert_2^2 \le \tfrac12 \Vert d\Vert_1^2$ —
   together with its two supporting lemmas. *(3 statements.)*
2. **The halving step of `prop:esyncsi-log`** — that
   $c_2 \le c_1$ and $c_1 + c_2 \le n$ imply $2c_2 \le n$ — in a form making
   its independence of $|\mathcal O|$ explicit. *(1 statement.)*
3. **The comparison underlying `lem:discrete-bv-sandwich`** —
   $\min\{a(M), b(M)\} \le a(N) + b(N)$. *(1 statement.)*
4. **The mediant inequality underlying `lem:kappa-bounded`.** *(1 statement.)*
5. **The parallel-axis identity** behind the ANOVA split. *(1 statement.)*
6. **The minimality of the weighted mean.** *(1 statement.)*
7. **The counting core of `prop:lsyncu-single-input`** — that a bounded
   strictly increasing block count admits at most $M-1$ increases. *(1
   statement.)*

The remaining statements of the fifteen are the auxiliary lemmas supporting
these blocks (in the manner of item 1's "two supporting lemmas").

## Scope (also as claimed by the manuscript)

What is verified is the arithmetic skeleton: the inequalities, identities and
counting arguments. Pinsker's inequality is taken as a hypothesis rather than
imported; Ky Fan's maximum principle, the Kullback–Leibler functional itself,
and all automata-theoretic constructions — Mealy machines, version spaces,
the adaptive games — are **not** formalized, so the surrounding theorems are
not verified end to end.

## Integration protocol for the checked sources

1. Place the machine-checked `.lean` file(s) of the companion development in
   this directory.
2. Verify, in a Mathlib-capable Lean 4 toolchain, that the file compiles with
   no `sorry` and that `#print axioms` on each of the fifteen statement names
   reports only Lean's standard three axioms
   (`propext`, `Quot.sound`, `Classical.choice`).
3. Check that the statement names/numbering match the blocks above; any
   discrepancy is a manuscript-level finding to be recorded before submission.

The Data and Code Availability statement of the manuscript references this
package; the statement manifest above is what it points to for the Lean
component.
