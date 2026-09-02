"""
T39.  Fiberwise spectral converses proposed by the audit:

 (C1) cor:controlled-quad-spectral:
        RetQuad^ctrl(M) >= 1/2 sum_x p(x) sum_{i>=M} lambda_i(Sigma_pi^x)
 (C2) cor:controlled-simplex-spectral:
        RetKL^ctrl(M)  >= sum_x p(x) sum_{i>=M} lambda_i(Sigma_p^x)
 (C3) cor:controlled-fisher: interior natural-parameter version with min_x m_K^x.

Key structural point the audit relies on: "the lumpability constraint is
x-independent", so the SAME quotient is used on every fiber and the fiberwise
theorem applies.  Test that, plus the rank-(M-1) budget per fiber.
"""
import random, math
import numpy as np

def kl(p,q):
    t=0.0
    for a,b in zip(p,q):
        if a>0:
            if b<=0: return float('inf')
            t+=a*math.log(a/b)
    return t

def parts(n):
    def rec(i,mx,cur):
        if i==n: yield tuple(cur); return
        for b in range(mx+1):
            cur.append(b); yield from rec(i+1,max(mx,b+1),cur); cur.pop()
    yield from rec(0,0,[])
PARTS={n:list(parts(n)) for n in range(2,7)}

def unif_lumpable(phi,tau,supp,nS,nI):
    for x in range(nI):
        img={}
        for s in range(nS):
            k=phi[s]
            for y in supp[s][x]:
                v=phi[tau[s][x][y]]
                if img.get((k,x,y),v)!=v: return False
                img[(k,x,y)]=v
    return True

rng=random.Random(99)
print("="*72)
print("(C2) controlled probability-coordinate spectral converse")
print("="*72)
minratio=1e18; viol=0; n=0; worst=None
for trial in range(40000):
    nS=rng.choice([3,4,5]); nI=rng.choice([1,2,3]); nO=rng.choice([2,3,4])
    tau=[[[rng.randrange(nS) for _ in range(nO)] for _ in range(nI)] for _ in range(nS)]
    supp=[[set(range(nO)) for _ in range(nI)] for _ in range(nS)]
    P=[[None]*nI for _ in range(nS)]
    for s in range(nS):
        for x in range(nI):
            w=[rng.random()+.02 for _ in range(nO)]; t=sum(w); P[s][x]=[v/t for v in w]
    pin=[rng.random()+.05 for _ in range(nI)]; t=sum(pin); pin=[v/t for v in pin]
    T=np.zeros((nS,nS))
    for s in range(nS):
        for x in range(nI):
            for y in range(nO): T[s][tau[s][x][y]]+=pin[x]*P[s][x][y]
    pi=np.ones(nS)/nS
    for _ in range(2000): pi=pi@T
    if pi.min()<1e-8: continue
    pi=pi/pi.sum()
    feas=[p for p in PARTS[nS] if unif_lumpable(p,tau,supp,nS,nI)]
    for M in range(1,nS+1):
        cand=[p for p in feas if len(set(p))<=M]
        if not cand: continue
        lhs=min(sum(pin[x]*sum(
                      sum(pi[s]*kl(P[s][x],
                          [sum(pi[u]*P[u][x][y] for u in range(nS) if phi[u]==k)/
                           sum(pi[u] for u in range(nS) if phi[u]==k)
                           for y in range(nO)])
                          for s in range(nS) if phi[s]==k)
                      for k in set(phi))
                    for x in range(nI)) for phi in cand)
        rhs=0.0
        for x in range(nI):
            Y=np.array([P[s][x] for s in range(nS)])
            bar=(pi[:,None]*Y).sum(0)
            Sg=sum(pi[s]*np.outer(Y[s]-bar,Y[s]-bar) for s in range(nS))
            ev=np.sort(np.linalg.eigvalsh(Sg))[::-1]
            rhs+=pin[x]*ev[M-1:].sum()
        n+=1
        if lhs < rhs-1e-11:
            viol+=1
            if worst is None: worst=(nS,nI,nO,M,lhs,rhs)
        if rhs>1e-12:
            r=lhs/rhs
            if r<minratio: minratio=r
print(f"  (M,instance) pairs checked : {n}")
print(f"  violations                 : {viol}")
print(f"  min LHS/RHS ratio          : {minratio:.6f}   (must be >= 1)")
if worst: print("  worst:",worst)

print()
print("="*72)
print("(C1) controlled Gaussian quadratic spectral converse, factor 1/2")
print("="*72)
viol=0; n=0; minr=1e18
for trial in range(20000):
    nS=rng.choice([3,4,5]); nI=rng.choice([1,2,3]); nO=2; D=rng.choice([1,2,3])
    tau=[[[rng.randrange(nS) for _ in range(nO)] for _ in range(nI)] for _ in range(nS)]
    supp=[[set(range(nO)) for _ in range(nI)] for _ in range(nS)]
    m=[[np.array([rng.gauss(0,1) for _ in range(D)]) for _ in range(nI)] for _ in range(nS)]
    pin=[rng.random()+.05 for _ in range(nI)]; t=sum(pin); pin=[v/t for v in pin]
    pi=np.array([rng.random()+.05 for _ in range(nS)]); pi/=pi.sum()
    feas=[p for p in PARTS[nS] if unif_lumpable(p,tau,supp,nS,nI)]
    for M in range(1,nS+1):
        cand=[p for p in feas if len(set(p))<=M]
        if not cand: continue
        def cost(phi):
            z=0.0
            for x in range(nI):
                for k in set(phi):
                    C=[s for s in range(nS) if phi[s]==k]
                    w=sum(pi[s] for s in C)
                    bar=sum(pi[s]*m[s][x] for s in C)/w
                    z+=pin[x]*sum(pi[s]*np.dot(m[s][x]-bar,m[s][x]-bar) for s in C)
            return z
        lhs=min(cost(p) for p in cand)          # in mean coordinates = ||m-c||^2
        rhs=0.0
        for x in range(nI):
            Y=np.array([math.sqrt(2)*m[s][x] for s in range(nS)])   # Fisher features
            bar=(pi[:,None]*Y).sum(0)
            Sg=sum(pi[s]*np.outer(Y[s]-bar,Y[s]-bar) for s in range(nS))
            ev=np.sort(np.linalg.eigvalsh(Sg))[::-1]
            tail=ev[M-1:].sum() if M-1 < len(ev) else 0.0
            rhs+=pin[x]*0.5*tail
        n+=1
        if lhs<rhs-1e-10: viol+=1
        if rhs>1e-12: minr=min(minr,lhs/rhs)
print(f"  (M,instance) pairs checked : {n}")
print(f"  violations                 : {viol}")
print(f"  min LHS/RHS ratio          : {minr:.6f}")
