"""
T39.  prop:unifilar-lumpability(ii), final paragraph of the audit's proof:

  "Finally, when Z is the full controlled future, ~_Z is a support-relative
   right congruence: conditioning both sides of an equality of conditional
   future laws on a commonly realized next event preserves the equality, and
   common feasibility is PART OF THE HYPOTHESIS."

The last clause is wrong bookkeeping: clause (i) of def:support-right-cong
(Feas(u)=Feas(v)) is not a hypothesis, it is a CONSEQUENCE of equality of the
full controlled future laws.  Verify:  if the conditional law of
(Y_t,Y_{t+1},...) given the input program agrees for u and v, then the
one-step supports agree, hence Feas(u)=Feas(v).
"""
import random
import numpy as np

def future_law(s,tau,P,nI,nO,depth):
    """law of (Y_t..Y_{t+depth-1}) as a dict keyed by input program"""
    out={}
    def rec(st,prog,seq,pr,d):
        if d==0:
            out[(prog,seq)]=out.get((prog,seq),0.0)+pr; return
        for x in range(nI):
            for y in range(nO):
                p=P[st][x][y]
                if p<=0: continue
                rec(tau[st][x][y],prog+(x,),seq+(y,),pr*p,d-1)
    rec(s,(),(),1.0,depth)
    return out

rng=random.Random(1234)
tested=0; viol=0
for _ in range(30000):
    nS=rng.randrange(2,5); nI=rng.randrange(1,3); nO=rng.randrange(2,4)
    tau=[[[rng.randrange(nS) for _ in range(nO)] for _ in range(nI)] for _ in range(nS)]
    P=[]
    pool=[]
    for _ in range(rng.randrange(1,nS+1)):
        row=[]
        for x in range(nI):
            k=rng.randrange(1,nO+1)
            S=rng.sample(range(nO),k)
            w=[0.0]*nO
            for y in S: w[y]=rng.random()+.05
            t=sum(w); row.append([v/t for v in w])
        pool.append(row)
    P=[pool[rng.randrange(len(pool))] for _ in range(nS)]
    D=4
    laws={s:future_law(s,tau,P,nI,nO,D) for s in range(nS)}
    for a in range(nS):
        for b in range(a+1,nS):
            la,lb=laws[a],laws[b]
            keys=set(la)|set(lb)
            same=all(abs(la.get(k,0.0)-lb.get(k,0.0))<1e-12 for k in keys)
            if not same: continue
            tested+=1
            fa={(x,y) for x in range(nI) for y in range(nO) if P[a][x][y]>0}
            fb={(x,y) for x in range(nI) for y in range(nO) if P[b][x][y]>0}
            if fa!=fb: viol+=1
print("="*72)
print("Full-controlled-future equality => equality of feasible event sets")
print("="*72)
print(f"  pairs with equal depth-{4} controlled future laws : {tested}")
print(f"  pairs with DIFFERENT feasible sets (violations)  : {viol}")
assert viol==0
print("  VERIFIED: clause (i) is DERIVED, not hypothesised.")
print("  The audit's phrase 'common feasibility is part of the hypothesis'")
print("  understates the result and should be replaced by a derivation.")
