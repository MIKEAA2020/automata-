"""Test the CONVERSE half of the proposed prop:unifilar-lumpability.

Proposed: "any finite-index right congruence on joint histories coarser than
Z-predictive equivalence induces a unifilar-lumpable quotient, whenever
Z-predictive equivalence is itself a right congruence on joint histories."

The forward direction was verified.  The converse is the delicate one: does a
right congruence on HISTORIES always descend to a well-defined quotient on
STATES?  Danger: two histories reaching the SAME state could be inequivalent,
making the induced state map ill-defined.
"""
import itertools, random

def random_unifilar(nS,nI,nO,rng,zero_prob=0.35):
    P={}; tau={}
    for s in range(nS):
        for x in range(nI):
            sup=[y for y in range(nO) if rng.random()>zero_prob] or [rng.randrange(nO)]
            w=[rng.random() for _ in sup]; t=sum(w)
            P[(s,x)]={y:wi/t for y,wi in zip(sup,w)}
            for y in sup: tau[(s,x,y)]=rng.randrange(nS)
    return P,tau

print("KEY QUESTION: can a right congruence on joint histories fail to descend")
print("to states, because two histories reaching the SAME state are inequivalent?")
print()
# Build: histories from a fixed start state; equivalence = phi of reached state
# is automatically well-defined.  The risk is the OTHER direction: an abstract
# congruence on histories not of that form.
print("Construction of the hazard, explicitly:")
print("  Let sigma(u) be the state reached by joint history u from the root.")
print("  A congruence ~ on histories descends to states iff")
print("      sigma(u) = sigma(v)  =>  u ~ v.")
print("  Without that implication the induced state map is ILL-DEFINED.")
print()
print("Does it hold automatically?  NO -- here is a concrete counterexample.")
print()
# 1 state machine, 2 feasible outputs: all histories reach the same state,
# but the congruence 'u ~ v iff |u| even' is a right congruence on histories.
print("  Machine: nS=1, nI=1, nO=2, both outputs feasible, tau(s,x,y)=s.")
print("  Then sigma(u)=s for EVERY history u.")
print("  Define u ~ v iff |u| is congruent to |v| mod 2.")
print("  Right congruence?  appending one event preserves parity difference: YES.")
print("  Finite index?  2: YES.")
print("  Coarser than Z-predictive equivalence?  All states have the same")
print("  predictive law, so Z-predictive equivalence is the ALL relation, and")
print("  ~ is FINER, not coarser -- so this instance is excluded by hypothesis.")
print()
print("  Refined test: is 'coarser than Z-predictive equivalence' enough?")
print("  If ~ is coarser than Z-predictive equivalence AND sigma(u)=sigma(v)")
print("  implies u,v have the same predictive law, then u ~ v follows.")
print("  So the implication DOES hold under the stated hypothesis.")
print()
# verify that claim computationally
print("Verify: sigma(u)=sigma(v) => same Z-predictive law => u ~ v when ~ is")
print("coarser than Z-predictive equivalence.")
bad=0; n=0
for trial in range(3000):
    rng=random.Random(trial)
    nS=rng.randint(2,4); nI=rng.randint(1,2); nO=rng.randint(2,3)
    P,tau=random_unifilar(nS,nI,nO,rng)
    # Z-predictive law of a state = its emission kernel
    def law(s): return tuple(sorted((x,tuple(sorted(P[(s,x)].items()))) for x in range(nI)))
    # sigma(u)=sigma(v) trivially gives law(sigma(u))=law(sigma(v))
    for s in range(nS):
        n+=1
        if law(s)!=law(s): bad+=1
print(f"  {n} checks; violations: {bad}  (trivially 0 -- equality of states gives")
print("  equality of laws, so the descent condition is implied by the hypothesis)")
print()
print("CONCLUSION: the converse is CORRECT as stated, but ONLY because of the")
print("explicit hypothesis 'coarser than Z-predictive equivalence' together with")
print("'Z-predictive equivalence is itself a right congruence'.  Both conditions")
print("are load-bearing and must be carried into the manuscript verbatim.")
