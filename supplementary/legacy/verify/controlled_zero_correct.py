"""
T39.  CORRECTED controlled zero-retention threshold.

Claim (to be proved in the manuscript):
  RetKL^ctrl(M) = 0  <=>  M >= |S^+ / ~_ker^stable|,
where ~_ker^stable is the COARSEST unifilar-lumpable quotient REFINING the
predictive-kernel partition, computed by Moore/Hopcroft partition refinement:
   start from the kernel partition; repeatedly split a block whenever two of
   its states have a feasible event (x,y) leading to different blocks.
This is exactly epsilon-machine (causal-state) minimization.

Also verify: the refinement terminates at the unique coarsest such quotient
(the greatest fixed point), so the threshold is well defined.
"""
import random, math, itertools
import numpy as np

def parts(n):
    def rec(i,mx,cur):
        if i==n: yield tuple(cur); return
        for b in range(mx+1):
            cur.append(b); yield from rec(i+1,max(mx,b+1),cur); cur.pop()
    yield from rec(0,0,[])

def unif_lumpable(phi,tau,supp,nS,nI,nO):
    for x in range(nI):
        img={}
        for s in range(nS):
            k=phi[s]
            for y in supp[s][x]:
                v=phi[tau[s][x][y]]
                if img.get((k,x,y),v)!=v: return False
                img[(k,x,y)]=v
    return True

def refine(phi0,tau,supp,nS,nI):
    """coarsest unifilar-lumpable refinement of phi0 (Moore refinement)"""
    phi=list(phi0)
    while True:
        sig={}
        for s in range(nS):
            key=(phi[s],tuple(sorted((x,y,phi[tau[s][x][y]])
                                     for x in range(nI) for y in supp[s][x])))
            sig[s]=key
        keys=sorted(set(sig.values()), key=str)
        idx={k:i for i,k in enumerate(keys)}
        new=[idx[sig[s]] for s in range(nS)]
        if len(set(new))==len(set(phi)): return tuple(new)
        phi=new

def kl(p,q):
    t=0.0
    for a,b in zip(p,q):
        if a>0:
            if b<=0: return float('inf')
            t+=a*math.log(a/b)
    return t

rng=random.Random(31337)
tested=0; bad_thresh=0; bad_coarsest=0; nontriv=0
for trial in range(120000):
    nS=rng.choice([3,4,5]); nI=rng.choice([1,2]); nO=rng.choice([2,3])
    tau=[[[rng.randrange(nS) for _ in range(nO)] for _ in range(nI)] for _ in range(nS)]
    supp=[[set(range(nO)) for _ in range(nI)] for _ in range(nS)]
    # force kernel collisions: draw kernels from a small pool
    pool=[]
    for _ in range(rng.randrange(1,nS)):
        row=[]
        for x in range(nI):
            w=[rng.random()+.05 for _ in range(nO)]; t=sum(w); row.append([v/t for v in w])
        pool.append(row)
    P=[pool[rng.randrange(len(pool))] for _ in range(nS)]
    pin=[rng.random()+.05 for _ in range(nI)]; t=sum(pin); pin=[v/t for v in pin]
    T=np.zeros((nS,nS))
    for s in range(nS):
        for x in range(nI):
            for y in range(nO): T[s][tau[s][x][y]]+=pin[x]*P[s][x][y]
    pi=np.ones(nS)/nS
    for _ in range(2000): pi=pi@T
    if pi.min()<1e-8: continue
    pi=pi/pi.sum()

    # kernel partition
    kern={}
    phi_k=[]
    for s in range(nS):
        key=tuple(tuple(round(v,12) for v in P[s][x]) for x in range(nI))
        phi_k.append(kern.setdefault(key,len(kern)))
    nk=len(kern)
    phi_star=refine(phi_k,tau,supp,nS,nI)
    Mstar=len(set(phi_star))
    tested+=1
    if Mstar>nk: nontriv+=1

    def rc(phi):
        z=0.0
        for x in range(nI):
            for k in set(phi):
                Cb=[s for s in range(nS) if phi[s]==k]
                w=sum(pi[s] for s in Cb)
                bar=[sum(pi[s]*P[s][x][y] for s in Cb)/w for y in range(nO)]
                z+=pin[x]*sum(pi[s]*kl(P[s][x],bar) for s in Cb)
        return z

    # brute force: minimal M with a zero-cost unifilar-lumpable quotient
    bestM=None
    for phi in parts(nS):
        if unif_lumpable(phi,tau,supp,nS,nI,nO) and rc(phi)<1e-12:
            m=len(set(phi))
            if bestM is None or m<bestM: bestM=m
    if bestM!=Mstar: bad_thresh+=1
    # coarsest: phi_star must be unifilar-lumpable and refine phi_k
    if not unif_lumpable(phi_star,tau,supp,nS,nI,nO): bad_coarsest+=1
    for s in range(nS):
        for u in range(nS):
            if phi_star[s]==phi_star[u] and phi_k[s]!=phi_k[u]: bad_coarsest+=1

print("="*72)
print("CORRECTED controlled zero-retention threshold")
print("="*72)
print(f"  instances tested (positive stationary mass)      : {tested}")
print(f"  instances where refinement is strictly finer than")
print(f"    the kernel partition (audit's claim would fail): {nontriv}"
      f"  ({100.0*nontriv/tested:.1f}%)")
print(f"  threshold mismatches   min-blocks != |refinement|: {bad_thresh}")
print(f"  refinement not unifilar-lumpable / not refining  : {bad_coarsest}")
assert bad_thresh==0 and bad_coarsest==0
print("  VERIFIED: RetKL^ctrl(M)=0  iff  M >= index of the coarsest")
print("            unifilar-lumpable refinement of the kernel partition.")
