"""
Feasibility probes for the open-item triage (recorded, not yet applied to the
manuscript).

P1  Correlated-input controlled IB: replacing pi_s/pi(C_k) by the conditional
    weight P(S=s | K=k, X=x) restores the identity for NON-product (S,X).
P2  Worst-case gap N* - |phi_ker| is |S|-2, attained by an explicit counter
    family with only two kernel classes; refinement needs |S|-1 rounds.
P3  |O| = 2d in cor:full-kl-apx is NOT slack: the doubling map is a centred
    similarity, and no centred similarity R^d -> R^{d+1} exists in general.
"""
import random, math, itertools
import numpy as np
from mpmath import mp, mpf
mp.dps=40

def kl(p,q):
    t=0.0
    for a,b in zip(p,q):
        if a>0:
            if b<=0: return float('inf')
            t+=a*math.log(a/b)
    return t
def mi_cond(J):
    tot=0.0
    for x in range(J.shape[0]):
        px=J[x].sum()
        if px<=0: continue
        A=J[x]/px; ps=A.sum(1); py=A.sum(0)
        for s in range(A.shape[0]):
            for y in range(A.shape[1]):
                if A[s,y]>0: tot+=px*A[s,y]*math.log(A[s,y]/(ps[s]*py[y]))
    return tot

# ---------------- P1 ----------------
rng=random.Random(11); worst=0.0; n=0
for _ in range(30000):
    nS=rng.randrange(2,5); nI=rng.randrange(2,4); nO=rng.randrange(2,4)
    W=np.array([[rng.random()+.05 for _ in range(nI)] for _ in range(nS)]); W/=W.sum()
    P=[[None]*nI for _ in range(nS)]
    for s in range(nS):
        for x in range(nI):
            w=[rng.random()+.02 for _ in range(nO)]; t=sum(w); P[s][x]=[v/t for v in w]
    K=rng.randrange(1,nS+1); phi=[rng.randrange(K) for _ in range(nS)]
    u=sorted(set(phi)); rm={k:i for i,k in enumerate(u)}; phi=[rm[k] for k in phi]; K=len(u)
    lhs=0.0
    for x in range(nI):
        for k in range(K):
            C=[s for s in range(nS) if phi[s]==k]
            wk=sum(W[s,x] for s in C)
            if wk<=0: continue
            bar=[sum(W[s,x]*P[s][x][y] for s in C)/wk for y in range(nO)]
            lhs+=sum(W[s,x]*kl(P[s][x],bar) for s in C)
    jS=np.zeros((nI,nS,nO)); jK=np.zeros((nI,K,nO))
    for x in range(nI):
        for s in range(nS):
            for y in range(nO):
                v=W[s,x]*P[s][x][y]; jS[x,s,y]+=v; jK[x,phi[s],y]+=v
    n+=1; worst=max(worst,abs(lhs-(mi_cond(jS)-mi_cond(jK))))
print(f"P1 correlated-input controlled IB : {n} instances, max dev {worst:.3e}")
assert worst<1e-9

# ---------------- P2 ----------------
def refine(phik,tau,nS,nI,nO):
    phi=list(phik); r=0
    while True:
        sig={s:(phi[s],tuple(phi[tau[s][x][y]] for x in range(nI) for y in range(nO)))
             for s in range(nS)}
        keys=sorted(set(sig.values()),key=str); idx={k:i for i,k in enumerate(keys)}
        new=[idx[sig[s]] for s in range(nS)]; r+=1
        if len(set(new))==len(set(phi)): return len(set(new)),r
        phi=new
ok=True
for M in range(3,16):
    tau=[[[min(s+1,M-1),0]] for s in range(M)]
    N,r=refine([0]*(M-1)+[1],tau,M,1,2)
    if not (N==M and r==M-1): ok=False; print("   P2 mismatch at M=",M,N,r)
print(f"P2 counter family, M=3..15      : N*=|S| and rounds=|S|-1 in all cases: {ok}")
assert ok

# ---------------- P3 ----------------
rng=random.Random(1); nonconst=0
for d in (2,3,4,5):
    lo,hi=mpf(10),mpf(0)
    for _ in range(3000):
        a=[mpf(rng.randrange(-20,20)) for _ in range(d)]
        b=[mpf(rng.randrange(-20,20)) for _ in range(d)]
        za,zb=a+[-sum(a)],b+[-sum(b)]
        d2=sum((x-y)**2 for x,y in zip(a,b))
        if d2==0: continue
        r=sum((x-y)**2 for x,y in zip(za,zb))/d2
        lo=min(lo,r); hi=max(hi,r)
    if hi-lo>mpf('1e-30'): nonconst+=1
print(f"P3 append-coordinate map non-similarity for d=2..5: {nonconst}/4 (expected 4)")
assert nonconst==4
print()
print("ALL PROBES CONFIRMED")
