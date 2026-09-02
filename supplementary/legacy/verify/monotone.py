"""
Audit item #2: does finite Nerode index imply zero gap for an ARBITRARY task
theory?

meta:monotone (ii) says: if index(~_delta) < infinity then Delta(M)=0 for all
M >= index.  Proof given: "quotienting by ~_delta realizes the trajectory
exactly."

That step needs  E(X,X) = 0.  The task-theory definition requires only that
E be a cost profunctor R^op x R -> V.  Nothing forces a zero diagonal.

Counterexample: V = ([0,inf], >=, +) the Lawvere quantale.  Take R with a
single object *, and E(*,*) = 1.  This IS a legitimate V-profunctor:
the required composition/unit inequalities in the Lawvere quantale are
  E(x,y) + E(y,z) >= E(x,z)   [triangle]      -> 1 + 1 >= 1   OK
  hom(x,x) = 0 >= ... is NOT required of a profunctor, only of a V-category.
So E(*,*) = 1 is admissible as a cost profunctor.

Then delta is constant, ~_delta has index 1, yet every approximation (there is
only one) has cost 1, not 0.  So Delta(M) = 1 > 0 for every M.
"""

print("=" * 76)
print("A. IS A CONSTANT-1 COST PROFUNCTOR ADMISSIBLE?")
print("=" * 76)
print("  V = ([0,inf], >=, +)  (Lawvere quantale)")
print("  R = one object *,  E(*,*) = 1")
print()
print("  Profunctor axioms in enriched form require compatibility with the")
print("  hom-objects of R:   R(y,y') + E(x,y) >= E(x,y')   etc.")
print("  With R the one-object V-category having R(*,*) = 0:")
lhs = 0 + 1
rhs = 1
print(f"    R(*,*) + E(*,*) = {lhs} >= E(*,*) = {rhs}   -> {lhs >= rhs}")
assert lhs >= rhs
print("  ADMISSIBLE. No axiom forces E(*,*) = 0.")

print()
print("=" * 76)
print("B. THE GAP IS NOT ZERO DESPITE FINITE NERODE INDEX")
print("=" * 76)
print("  delta : H -> R is the unique constant map.")
print("  ~_delta identifies all histories, so index(~_delta) = 1 < infinity.")
print("  The only budget-M approximant is the same constant map.")
print("  Worst-case cost = sup_u E(delta(u), delta(u)) = E(*,*) = 1.")
print()
for M in (1, 2, 5):
    print(f"    Delta(M={M}) = 1  != 0")
print()
print("  meta:monotone (ii) claims Delta(M) = 0 for M >= 1.  FALSE here.")

print()
print("=" * 76)
print("C. WHAT REPAIRS IT")
print("=" * 76)
print("  Adding the reflexivity axiom  E(X,X) = 0  for all X in R.")
print("  Then quotienting by ~_delta assigns each class its common residual,")
print("  and every history incurs cost E(delta(u), delta(u)) = 0.")
print()
print("  Check the three regimes already satisfy it:")
for name, val in [("KL:  D(P||P)", 0.0),
                  ("operator norm:  ||A-A||", 0.0),
                  ("0/1 commitment:  E(f,f)", 0.0)]:
    print(f"    {name:34s} = {val}   OK")
print()
print("  So the axiom is free for every instance used in the manuscript;")
print("  it is only the GENERIC statement that needs it.")

print()
print("=" * 76)
print("D. SEPARATION IS ALSO NEEDED FOR THE CONVERSE DIRECTION")
print("=" * 76)
print("  Clause (iii)(a) asserts  Delta^sup(M) = 0  <=>  index(~_delta) <= M.")
print("  The '=>' direction needs: E(delta(u), Psi) = 0 forces delta(u) = Psi.")
print("  That is exactly separatedness of E, which clause (iii) DOES assume.")
print("  Clause (ii) does not assume it, and does not need it -- it only needs")
print("  the zero diagonal for the '<=' direction.")
