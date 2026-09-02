"""
ITEM 1 write-up verification.

General controlled IB, WITHOUT input independence.  Define the fiber-conditional
weights  pi_s^x = P(S_t = s | X_t = x)  and

  RetKL^gen(phi) = sum_x p(x) sum_k sum_{s in C_k} pi_s^x D( P_s^x || Q_k^x ).

Claims to verify on NON-PRODUCT stationary laws of (S,X):
 (A) optimal Q_k^x is the fiber-conditional centroid, = P(Y | K=k, X=x)
 (B) RetKL^gen(phi) = I(S;Y|K,X) = I(S;Y|X) - I(K;Y|X)
 (C) reduces to thm:controlled-ib when X _||_ S
 (D) FIBERWISE spectral converse survives with the reweighted covariance
       RetKL^gen(M) >= sum_x p(x) sum_{i>=M} lambda_i(Sigma_p^x),
     Sigma_p^x built from pi_s^x  (NOT from the unconditional pi_s)
 (E) using the UNCONDITIONAL pi_s in Sigma_p^x instead is NOT valid
 (F) elementary corollary: RetKL^gen(1) = I(S;Y|X), monotone in M
"""
import random, math, itertools
import numpy as np

def kl(p,q):
    t=0.0
    for a,b in zip(p,q):
        if a>0:
            if b<=0: return float('inf')
            t+=a*math.log(a/b)
    return t

def mi_cond(J):
    """J[x,s,y] = P(X=x,S=s,Y=y) -> I(S;Y|X)"""
    tot=0.0
    for x in range(J.shape[0]):
        px=J[x].sum()
        if px<=0: continue
        A=J[x]/px; ps=A.sum(1); py=A.sum(0)
        for s in range(A.shape[0]):
            for y in range(A.shape[1]):
                if A[s,y]>0: tot+=px*A[s,y]*math.log(A[s,y]/(ps[s]*py[y]))
    return tot

def parts(n):
    def rec(i,mx,cur):
        if i==n: yield tuple(cur); return
        for b in range(mx+1):
            cur.append(b); yield from rec(i+1,max(mx,b+1),cur); cur.pop()
    yield from rec(0,0,[])
PARTS={n:list(parts(n)) for n in range(1,6)}

def instance(rng,product_law=False):
    nS=rng.randrange(2,5); nI=rng.randrange(2,4); nO=rng.randrange(2,4)
    if product_law:
        pi=np.array([rng.random()+.05 for _ in range(nS)]); pi/=pi.sum()
        p =np.array([rng.random()+.05 for _ in range(nI)]); p/=p.sum()
        W=np.outer(pi,p)
    else:
        W=np.array([[rng.random()+.05 for _ in range(nI)] for _ in range(nS)])
        W/=W.sum()
    P=[[None]*nI for _ in range(nS)]
    for s in range(nS):
        for x in range(nI):
            w=[rng.random()+.02 for _ in range(nO)]; t=sum(w); P[s][x]=[v/t for v in w]
    return nS,nI,nO,W,P

def gen_cost(phi,nS,nI,nO,W,P):
    """RetKL^gen with fiber-conditional weights"""
    px=W.sum(0); tot=0.0
    for x in range(nI):
        if px[x]<=0: continue
        for k in set(phi):
            C=[s for s in range(nS) if phi[s]==k]
            wk=sum(W[s,x] for s in C)
            if wk<=0: continue
            bar=[sum(W[s,x]*P[s][x][y] for s in C)/wk for y in range(nO)]
            tot+=sum(W[s,x]*kl(P[s][x],bar) for s in C)
    return tot

rng=random.Random(20260807)

# ---------------- A, B ----------------
worstB=0.0; n=0; badA=0
for _ in range(30000):
    nS,nI,nO,W,P=instance(rng)
    K=rng.randrange(1,nS+1); phi=[rng.randrange(K) for _ in range(nS)]
    u=sorted(set(phi)); rm={k:i for i,k in enumerate(u)}; phi=[rm[k] for k in phi]
    lhs=gen_cost(phi,nS,nI,nO,W,P)
    jS=np.zeros((nI,nS,nO)); jK=np.zeros((nI,len(set(phi)),nO))
    for x in range(nI):
        for s in range(nS):
            for y in range(nO):
                v=W[s,x]*P[s][x][y]; jS[x,s,y]+=v; jK[x,phi[s],y]+=v
    rhs=mi_cond(jS)-mi_cond(jK)
    n+=1; worstB=max(worstB,abs(lhs-rhs))
    # (A) perturb representatives
    for _ in range(4):
        alt=0.0; px=W.sum(0)
        for x in range(nI):
            for k in set(phi):
                C=[s for s in range(nS) if phi[s]==k]
                wk=sum(W[s,x] for s in C)
                if wk<=0: continue
                bar=np.array([sum(W[s,x]*P[s][x][y] for s in C)/wk for y in range(nO)])
                nz=np.array([rng.random() for _ in range(nO)]); nz/=nz.sum()
                q=0.85*bar+0.15*nz
                alt+=sum(W[s,x]*kl(P[s][x],list(q)) for s in C)
        if alt<lhs-1e-12: badA+=1
print("="*74)
print("ITEM 1  general controlled IB (correlated inputs allowed)")
print("="*74)
print(f"  (B) instances {n};  max |RetKL^gen - (I(S;Y|X)-I(K;Y|X))| = {worstB:.3e}")
print(f"  (A) perturbations beating the fiber-conditional centroid       = {badA}")
assert worstB<1e-9 and badA==0

# ---------------- C reduction ----------------
worstC=0.0
for _ in range(8000):
    nS,nI,nO,W,P=instance(rng,product_law=True)
    K=rng.randrange(1,nS+1); phi=[rng.randrange(K) for _ in range(nS)]
    u=sorted(set(phi)); rm={k:i for i,k in enumerate(u)}; phi=[rm[k] for k in phi]
    gen=gen_cost(phi,nS,nI,nO,W,P)
    # the T39 unconditional-weight form
    pi=W.sum(1); px=W.sum(0); old=0.0
    for x in range(nI):
        for k in set(phi):
            C=[s for s in range(nS) if phi[s]==k]
            wk=sum(pi[s] for s in C)
            bar=[sum(pi[s]*P[s][x][y] for s in C)/wk for y in range(nO)]
            old+=px[x]*sum(pi[s]*kl(P[s][x],bar) for s in C)
    worstC=max(worstC,abs(gen-old))
print(f"  (C) under X _||_ S, |RetKL^gen - RetKL^ctrl| = {worstC:.3e}")
assert worstC<1e-9

# ---------------- D, E fiberwise spectral converse ----------------
violD=0; violE=0; nD=0; minr=1e18
for _ in range(20000):
    nS,nI,nO,W,P=instance(rng)
    pi_uncond=W.sum(1); px=W.sum(0)
    for M in range(1,nS+1):
        cand=[p for p in PARTS[nS] if len(set(p))<=M]
        lhs=min(gen_cost(p,nS,nI,nO,W,P) for p in cand)
        # (D) covariance with CONDITIONAL weights
        rhsD=0.0
        for x in range(nI):
            if px[x]<=0: continue
            w=np.array([W[s,x]/px[x] for s in range(nS)])
            Y=np.array([P[s][x] for s in range(nS)])
            bar=(w[:,None]*Y).sum(0)
            Sg=sum(w[s]*np.outer(Y[s]-bar,Y[s]-bar) for s in range(nS))
            ev=np.sort(np.linalg.eigvalsh(Sg))[::-1]
            rhsD+=px[x]*ev[M-1:].sum()
        # (E) covariance with UNCONDITIONAL weights (the naive transfer)
        rhsE=0.0
        for x in range(nI):
            if px[x]<=0: continue
            w=pi_uncond
            Y=np.array([P[s][x] for s in range(nS)])
            bar=(w[:,None]*Y).sum(0)
            Sg=sum(w[s]*np.outer(Y[s]-bar,Y[s]-bar) for s in range(nS))
            ev=np.sort(np.linalg.eigvalsh(Sg))[::-1]
            rhsE+=px[x]*ev[M-1:].sum()
        nD+=1
        if lhs<rhsD-1e-11: violD+=1
        if lhs<rhsE-1e-11: violE+=1
        if rhsD>1e-12: minr=min(minr,lhs/rhsD)
print(f"  (D) reweighted-covariance converse: {nD} pairs, violations = {violD}, min ratio {minr:.6f}")
print(f"  (E) naive unconditional-covariance: violations = {violE}   <-- must be > 0")
assert violD==0 and violE>0

# ---------------- F elementary ----------------
bad1=badm=0; nF=0
for _ in range(8000):
    nS,nI,nO,W,P=instance(rng)
    jS=np.zeros((nI,nS,nO))
    for x in range(nI):
        for s in range(nS):
            for y in range(nO): jS[x,s,y]=W[s,x]*P[s][x][y]
    ISYX=mi_cond(jS)
    vals={}
    for M in range(1,nS+1):
        vals[M]=min(gen_cost(p,nS,nI,nO,W,P) for p in PARTS[nS] if len(set(p))<=M)
    nF+=1
    if abs(vals[1]-ISYX)>1e-9: bad1+=1
    ms=sorted(vals)
    for a,b in zip(ms,ms[1:]):
        if vals[b]>vals[a]+1e-12: badm+=1
print(f"  (F) {nF} instances: RetKL^gen(1)=I(S;Y|X) failures = {bad1}; monotonicity failures = {badm}")
assert bad1==0 and badm==0
print()
print("ITEM 1 VERIFIED")
