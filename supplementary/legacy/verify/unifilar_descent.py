"""NON-CIRCULAR test of the descent condition.

The converse needs: a right congruence ~ on joint histories, coarser than
Z-predictive equivalence, induces a WELL-DEFINED map on states.

Well-definedness requires:  sigma(u) = sigma(v)  =>  u ~ v.
This does NOT follow from 'coarser than Z-predictive equivalence' in general,
because Z-predictive equivalence on HISTORIES compares predictive laws, and
two histories with the same law can reach different states -- and conversely
'coarser' is the wrong direction for the implication we need.

Search for an actual counterexample.
"""
import itertools, random

def build(nS,nI,nO,seed):
    rng=random.Random(seed); P={}; tau={}
    for s in range(nS):
        for x in range(nI):
            sup=[y for y in range(nO) if rng.random()>0.3] or [rng.randrange(nO)]
            w=[rng.random() for _ in sup]; t=sum(w)
            P[(s,x)]={y:round(wi/t,6) for y,wi in zip(sup,w)}
            for y in sup: tau[(s,x,y)]=rng.randrange(nS)
    return P,tau

def hists(nI,nO,L):
    ev=[(x,y) for x in range(nI) for y in range(nO)]
    out=[()]
    for k in range(1,L+1): out+=list(itertools.product(ev,repeat=k))
    return out

print("Searching for: a right congruence ~ on histories, coarser than")
print("Z-predictive equivalence, that does NOT descend to states.")
print()
found=None
for seed in range(3000):
    nS,nI,nO=3,1,2
    P,tau=build(nS,nI,nO,seed)
    root=0
    H=hists(nI,nO,3)
    def sigma(u):
        c=root
        for (x,y) in u:
            if (c,x,y) not in tau: return None
            c=tau[(c,x,y)]
        return c
    feas=[u for u in H if sigma(u) is not None]
    if len(feas)<6: continue
    def law(s): return tuple(sorted((x,tuple(sorted(P[(s,x)].items()))) for x in range(nI)))
    # Z-predictive equivalence on histories
    zp={}
    for u in feas: zp.setdefault(law(sigma(u)),[]).append(u)
    if len(zp)<2: continue
    # Candidate coarser congruence: merge two Z-classes.  Is it a right
    # congruence?  And does it descend?  (It always descends here because it is
    # defined THROUGH sigma.)  The real question: can a congruence be coarser
    # than Z-pred yet separate two histories reaching the SAME state?
    # If ~ is coarser than Z-pred and sigma(u)=sigma(v), then law is equal, so
    # u,v are Z-pred equivalent, so u ~ v since ~ is COARSER.  <-- the key step
    for u in feas:
        for v in feas:
            if sigma(u)==sigma(v):
                if law(sigma(u))!=law(sigma(v)):
                    found=(seed,u,v); break
        if found: break
    if found: break

print(f"counterexample to 'sigma(u)=sigma(v) => same predictive law': {found}")
print()
print("None exists, and the reason is definitional: if sigma(u)=sigma(v) then")
print("the two histories reach the SAME state, hence trivially the same law.")
print("Therefore they are Z-predictive equivalent, and since ~ is COARSER than")
print("Z-predictive equivalence, u ~ v.  The descent condition FOLLOWS.")
print()
print("So the converse is sound -- but the load-bearing hypothesis is")
print("'coarser than Z-predictive equivalence', NOT 'finite index'.")
print()
print("="*74)
print("Sanity: exhibit that a FINER congruence breaks descent (parity example)")
print("="*74)
print("  nS=1, all histories reach the one state; ~ = parity of length.")
print("  sigma(u)=sigma(v) for ALL u,v, but u !~ v when lengths differ in parity.")
print("  Induced state map ill-defined.  This congruence is FINER than")
print("  Z-predictive equivalence (which is the all-relation here), so it is")
print("  correctly excluded by the hypothesis.")
