"""Does the 1/2 halving factor apply to thm:active-halving (RI, machine-state pairs)?

My manuscript claims NO: "a mistake retains the COMPLEMENT of the predicted
class". The evaluator claims YES: each candidate (A,q) predicts ONE deterministic
symbol under input x, so the version space partitions by predicted symbol, and
observing the true output retains exactly ONE class.

Settle it: each element of V is a pair (A,q).  Under input x, that pair emits
lambda_A(q,x) -- a SINGLE deterministic symbol.  So V partitions into classes
by emitted symbol, exactly as in the SI case.  A mistake => observed symbol
o != predicted => survivors = the single class emitting o.
"""
import itertools, random
random.seed(0)

print("Model: V = set of (machine, state) pairs.  Input x fixed.")
print("Each pair emits ONE symbol lambda_A(q,x).  So V partitions by symbol.")
print()
print("Simulate: random version spaces of (A,q) pairs, count survivors after a mistake.")
print(f"{'|V|':>5} {'|O|':>4} {'plurality c1':>13} {'worst survivor':>15} {'<= |V|/2?':>10} {'(1-1/|O|)|V|':>13}")
bad=0
for trial in range(200000):
    nV=random.randint(2,40); nO=random.randint(2,6)
    # each pair emits a deterministic symbol
    emit=[random.randrange(nO) for _ in range(nV)]
    cnt=[emit.count(o) for o in range(nO)]
    c1=max(cnt)
    # learner predicts plurality symbol; adversary picks worst OTHER class
    others=[c for c in cnt if c!=c1] or [c for c in cnt]
    # careful: if several classes tie at c1, the survivor can be another c1-class
    srt=sorted(cnt,reverse=True)
    worst_survivor = srt[1] if len(srt)>1 else 0
    if worst_survivor > nV/2 + 1e-9: bad+=1
    if trial<6:
        print(f"{nV:>5} {nO:>4} {c1:>13} {worst_survivor:>15} {str(worst_survivor<=nV/2):>10} {(1-1/nO)*nV:>13.1f}")
print()
print(f"200000 random version spaces: cases where survivors > |V|/2 : {bad}")
print()
print("=> Each (A,q) emits exactly one symbol, so the survivors after a mistake")
print("   are a SINGLE class of size <= c_2 <= |V|/2.  The halving factor 1/2")
print("   DOES apply.  My manuscript's 'retains the complement' is WRONG:")
print("   the complement would be the union of all non-predicted classes, but")
print("   only one of them is consistent with the OBSERVED output.")
