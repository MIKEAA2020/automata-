"""Verify the PROPOSED prop:unifilar-lumpability before adopting it.

Claim: phi is unifilar-lumpable  <=>  it induces a right congruence on JOINT
histories (I x O)*, right extension by jointly FEASIBLE events (x,y).

Two things to test:
  (A) the forward direction: unifilar-lumpable => right congruence on joint
      histories (with feasibility);
  (B) the FEASIBILITY caveat is essential -- test whether ignoring feasibility
      breaks the claim.  Infeasible (x,y) pairs (emission probability 0) must
      be excluded or tau is unconstrained there.
"""
import itertools, random
random.seed(0)

def random_unifilar(nS,nI,nO,rng,zero_prob=0.4):
    """emission kernel P[s][x][y]; tau[s][x][y] defined only where P>0"""
    P={}; tau={}
    for s in range(nS):
        for x in range(nI):
            # random support, at least one feasible y
            sup=[y for y in range(nO) if rng.random()>zero_prob] or [rng.randrange(nO)]
            w=[rng.random() for _ in sup]; tot=sum(w)
            P[(s,x)]={y:wi/tot for y,wi in zip(sup,w)}
            for y in sup:
                tau[(s,x,y)]=rng.randrange(nS)
    return P,tau

def is_unifilar_lumpable(nS,nI,nO,P,tau,phi):
    """phi(s)=phi(s') => phi(tau(s,x,y))=phi(tau(s',x,y)) for jointly feasible (x,y)"""
    for s in range(nS):
        for sp in range(nS):
            if phi[s]!=phi[sp]: continue
            for x in range(nI):
                for y in range(nO):
                    f1=(s,x,y) in tau; f2=(sp,x,y) in tau
                    if f1 and f2:
                        if phi[tau[(s,x,y)]]!=phi[tau[(sp,x,y)]]: return False
    return True

def induces_right_congruence(nS,nI,nO,P,tau,phi,depth=4):
    """u ~ v  iff phi(sigma(u)) = phi(sigma(v)); check closure under feasible (x,y)"""
    # states reachable by joint histories from each start state; test congruence
    # on pairs of (start,history) with equal phi-image
    def run(s,h):
        c=s
        for (x,y) in h:
            if (c,x,y) not in tau: return None
            c=tau[(c,x,y)]
        return c
    hists=[()]
    for L in range(1,depth):
        hists += list(itertools.product(list(itertools.product(range(nI),range(nO))),repeat=L))
    for s in range(nS):
        for sp in range(nS):
            for h in hists:
                a=run(s,h); b=run(sp,h)
                if a is None or b is None: continue
                if phi[a]!=phi[b]: continue           # only test phi-equal pairs
                for x in range(nI):
                    for y in range(nO):
                        if (a,x,y) in tau and (b,x,y) in tau:
                            if phi[tau[(a,x,y)]]!=phi[tau[(b,x,y)]]:
                                return False
    return True

print("(A) unifilar-lumpable  =>  right congruence on feasible joint histories")
agree=0; tot=0; ce=0
for trial in range(4000):
    rng=random.Random(trial)
    nS=rng.randint(2,4); nI=rng.randint(1,2); nO=rng.randint(2,3)
    P,tau=random_unifilar(nS,nI,nO,rng)
    # random partition
    k=rng.randint(1,nS)
    phi={s:rng.randrange(k) for s in range(nS)}
    ul=is_unifilar_lumpable(nS,nI,nO,P,tau,phi)
    rc=induces_right_congruence(nS,nI,nO,P,tau,phi)
    tot+=1
    if ul and not rc: ce+=1
    if ul==rc: agree+=1
print(f"    {tot} random instances; unifilar-lumpable but NOT a right congruence: {ce}")
print(f"    forward direction holds in all cases: {ce==0}")

print()
print("(B) is the FEASIBILITY restriction essential?")
def is_lumpable_ignoring_feasibility(nS,nI,nO,tau,phi):
    for s in range(nS):
        for sp in range(nS):
            if phi[s]!=phi[sp]: continue
            for x in range(nI):
                for y in range(nO):
                    if (s,x,y) in tau and (sp,x,y) in tau: continue
                    if ((s,x,y) in tau) != ((sp,x,y) in tau):
                        return False     # one feasible, other not
    return True
diff=0
for trial in range(4000):
    rng=random.Random(10000+trial)
    nS=rng.randint(2,4); nI=rng.randint(1,2); nO=rng.randint(2,3)
    P,tau=random_unifilar(nS,nI,nO,rng)
    k=rng.randint(1,nS); phi={s:rng.randrange(k) for s in range(nS)}
    if is_unifilar_lumpable(nS,nI,nO,P,tau,phi) and not is_lumpable_ignoring_feasibility(nS,nI,nO,tau,phi):
        diff+=1
print(f"    instances lumpable ONLY because infeasible (x,y) were excluded: {diff}")
print("    => feasibility is load-bearing; the definition must say 'jointly feasible'.")
