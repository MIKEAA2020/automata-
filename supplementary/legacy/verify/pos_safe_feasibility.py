"""
T52.  Feasibility of safe right congruences.

A safe right congruence has every class inside a safety block.  Claims:
 (1) such a partition exists at index M iff M >= r, r = number of safety
     blocks of POSITIVE MASS (the singleton refinement always works, and any
     safe partition has at least one class per nonempty block);
 (2) hence Safe_quad(M) is infeasible exactly for M < r;
 (3) Free_quad(M) >= Safe_quad(M) whenever the latter is feasible, so
     PoS_quad(M) >= 0 there.
"""
from fractions import Fraction as F
import itertools, random

def parts(n):
    def rec(i,m,c):
        if i==n: yield tuple(c); return
        for b in range(m+1):
            c.append(b); yield from rec(i+1,max(m,b+1),c); c.pop()
    yield from rec(0,0,[])

def safe(phi,B):
    """every class contained in some safety block"""
    blocks={}
    for s,k in enumerate(phi): blocks.setdefault(k,set()).add(s)
    return all(any(C<=set(b) for b in B) for C in blocks.values())

def Iquad(phi,pi,y):
    ybar=sum(pi[s]*y[s] for s in range(len(pi)))
    tot=F(0)
    bl={}
    for s,k in enumerate(phi): bl.setdefault(k,[]).append(s)
    for C in bl.values():
        P=sum(pi[s] for s in C)
        c=sum(pi[s]*y[s] for s in C)/P
        tot+=P*(c-ybar)**2
    return tot/2

rng=random.Random(5)
bad1=bad3=tot=0
for _ in range(60000):
    n=rng.randrange(2,6)
    # random safety partition
    r=rng.randrange(1,n+1)
    lab=[rng.randrange(r) for _ in range(n)]
    used=sorted(set(lab)); rm={k:i for i,k in enumerate(used)}
    lab=[rm[x] for x in lab]; r=len(used)
    B=[[s for s in range(n) if lab[s]==b] for b in range(r)]
    pi=[F(rng.randrange(1,20)) for _ in range(n)]; T=sum(pi); pi=[x/T for x in pi]
    y=[F(rng.randrange(-10,10)) for _ in range(n)]
    allp=list(parts(n))
    for M in range(1,n+1):
        feas=[p for p in allp if len(set(p))<=M and safe(p,B)]
        tot+=1
        # (1)/(2) feasibility iff M >= r
        if bool(feas) != (M>=r): bad1+=1
        if feas:
            S=max(Iquad(p,pi,y) for p in feas)
            Fr=max(Iquad(p,pi,y) for p in allp if len(set(p))<=M)
            if Fr < S: bad3+=1
print("="*74)
print("safe right congruence feasibility")
print("="*74)
print(f"  (M, instance) pairs tested            : {tot}")
print(f"  feasibility != (M >= r) violations    : {bad1}")
print(f"  Free_quad < Safe_quad violations      : {bad3}")
assert bad1==0 and bad3==0
print()
print("  VERIFIED: safe congruences of index <= M exist iff M >= r, and where")
print("  feasible the free optimum dominates the safe one, so PoS_quad >= 0.")
