"""
T39.  Audit's proposed cor:controlled-zero states:

  "RetKL^ctrl(M)=0 if and only if M is at least the number of distinct
   predictive kernels s -> (P_s^x)_x on S^+."

and its proof ends: "Hence zero cost requires exactly one block per distinct
kernel, and the singleton partition is unifilar-lumpable, so one block per
kernel suffices."

The last clause is a non sequitur: the singleton partition being lumpable
says nothing about whether the KERNEL partition is lumpable.  We test the
'if' direction.
"""
import itertools, math, random
from itertools import product
import numpy as np

def unif_lumpable(phi,tau,supp,nS,nI,nO):
    for x in range(nI):
        img={}
        for s in range(nS):
            k=phi[s]
            for y in range(nO):
                if y not in supp[s][x]: continue
                v=phi[tau[s][x][y]]
                if img.get((k,x,y),v)!=v: return False
                img[(k,x,y)]=v
    return True

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

print("="*72)
print("Explicit counterexample to the 'if' direction of cor:controlled-zero")
print("="*72)
# |I|=1 (call it x=0), |O|=2, three states A=0,B=1,C=2
nS,nI,nO=3,1,2
# A and B carry the SAME kernel: Bernoulli(1/2).  C carries delta-ish law.
P=[[[0.5,0.5]],[[0.5,0.5]],[[0.9,0.1]]]
supp=[[{0,1}],[{0,1}],[{0,1}]]
# unifilar update: A and B are separated by where they GO, not by what they emit
#   A --y=0--> A , A --y=1--> C
#   B --y=0--> C , B --y=1--> B
#   C --y=0--> A , C --y=1--> B
tau=[[[0,2]],[[2,1]],[[0,1]]]
# stationary distribution
T=np.zeros((nS,nS))
for s in range(nS):
    for y in range(nO): T[s][tau[s][0][y]]+=P[s][0][y]
pi=np.ones(nS)/nS
for _ in range(50000): pi=pi@T
pi=pi/pi.sum()
print(f"  stationary pi = {np.round(pi,6)}   (all positive: {pi.min()>1e-12})")
print(f"  predictive kernels: A={P[0][0]}, B={P[1][0]}, C={P[2][0]}")
kern=sorted({tuple(P[s][0]) for s in range(nS)})
print(f"  number of DISTINCT predictive kernels = {len(kern)}")

def retctrl(phi):
    tot=0.0
    for x in range(nI):
        for k in set(phi):
            C=[s for s in range(nS) if phi[s]==k]
            w=sum(pi[s] for s in C)
            bar=[sum(pi[s]*P[s][x][y] for s in C)/w for y in range(nO)]
            tot+=sum(pi[s]*kl(P[s][x],bar) for s in C)   # p(x)=1
    return tot

print("\n  all partitions, unifilar-lumpability and controlled cost:")
best={}
for phi in parts(nS):
    ul=unif_lumpable(phi,tau,supp,nS,nI,nO)
    c=retctrl(phi)
    nb=len(set(phi))
    print(f"    phi={phi}  blocks={nb}  unifilar-lumpable={str(ul):5s}  cost={c:.6f}")
    if ul: best[nb]=min(best.get(nb,9e9),c)
print()
for M in (1,2,3):
    v=min(v for b,v in best.items() if b<=M)
    print(f"    RetKL^ctrl(M={M}) = {v:.8f}")
M=len(kern)
v=min(x for b,x in best.items() if b<=M)
print(f"\n  #distinct kernels = {M}, but RetKL^ctrl({M}) = {v:.8f} > 0")
assert v>1e-9
print("  *** The 'if' direction of the proposed cor:controlled-zero is FALSE. ***")
print("  Reason: the kernel partition {{A,B},{C}} is NOT unifilar-lumpable")
print("          (A and B agree on emissions but their y-indexed successors")
print("           land in different blocks), so it is not in the feasible set.")

print()
print("="*72)
print("How often does the failure occur?  random search")
print("="*72)
rng=random.Random(7)
tot=0; fail=0
for _ in range(200000):
    nS=rng.choice([3,4]); nI=rng.choice([1,2]); nO=2
    tau=[[[rng.randrange(nS) for _ in range(nO)] for _ in range(nI)] for _ in range(nS)]
    # force a kernel collision: pick a random law and assign to >=2 states
    laws=[]
    base=[rng.uniform(.1,.9)]; base=[base[0],1-base[0]]
    for s in range(nS):
        if s<2: laws.append([[base[0],base[1]] for _ in range(nI)])
        else:
            a=rng.uniform(.05,.95); laws.append([[a,1-a] for _ in range(nI)])
    P=laws; supp=[[{0,1} for _ in range(nI)] for _ in range(nS)]
    pin=[rng.random()+.05 for _ in range(nI)]; t=sum(pin); pin=[v/t for v in pin]
    T=np.zeros((nS,nS))
    for s in range(nS):
        for x in range(nI):
            for y in range(nO): T[s][tau[s][x][y]]+=pin[x]*P[s][x][y]
    pi=np.ones(nS)/nS
    for _ in range(3000): pi=pi@T
    if pi.min()<1e-8: continue
    pi=pi/pi.sum()
    kern={tuple(tuple(r) for r in P[s]) for s in range(nS)}
    nk=len(kern)
    if nk>=nS: continue
    tot+=1
    def rc(phi):
        z=0.0
        for x in range(nI):
            for k in set(phi):
                Cb=[s for s in range(nS) if phi[s]==k]
                w=sum(pi[s] for s in Cb)
                bar=[sum(pi[s]*P[s][x][y] for s in Cb)/w for y in range(nO)]
                z+=pin[x]*sum(pi[s]*kl(P[s][x],bar) for s in Cb)
        return z
    vals=[rc(phi) for phi in parts(nS)
          if len(set(phi))<=nk and unif_lumpable(phi,tau,supp,nS,nI,nO)]
    if not vals or min(vals)>1e-9: fail+=1
print(f"  instances with a genuine kernel collision (nk < |S|) : {tot}")
print(f"  instances where RetKL^ctrl(nk) > 0 (claim FAILS)     : {fail}"
      f"   ({100.0*fail/max(tot,1):.1f}%)")
