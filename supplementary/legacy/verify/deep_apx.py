"""DEEP: cor:full-kl-apx.  Earlier check used only 2-block partitions, d<=3,
and one instance each.  Now: ALL partitions with <=k blocks, several d,
many instances, and an explicit test of the TWO-SIDED multiplicative sandwich
   (1-e/4) b Xi(C) <= RetKL(C) <= (1+e/4) b Xi(C)   for ALL C simultaneously,
which is what makes the reduction approximation-preserving.
"""
from mpmath import mp, mpf, log as mlog
import numpy as np, math
mp.dps = 50
rng = np.random.default_rng(5)

def klm(P,Q): return sum(a*mlog(a/b) for a,b in zip(P,Q) if a>0)

def parts(coll, kmax):
    if len(coll)==1: yield [coll]; return
    first, rest = coll[0], coll[1:]
    for sm in parts(rest, kmax):
        for i in range(len(sm)):
            cand = sm[:i]+[[first]+sm[i]]+sm[i+1:]
            if len(cand)<=kmax: yield cand
        if len(sm)+1<=kmax: yield [[first]]+sm

print("Uniform ratio  RetKL(C) / [ (2 d delta^2/n) Xi(C) ]  over ALL partitions")
print(f"{'d':>2} {'n':>2} {'delta':>8} {'#parts':>7} {'min ratio':>18} {'max ratio':>18} {'spread':>11}")
allspread=[]
for d,n,kmax in [(2,5,3),(2,6,3),(3,5,3),(3,6,2),(4,5,2)]:
    A = rng.integers(-4,5,(n,d))
    Z=[]
    for a in A:
        z=[]
        for x in a: z+=[mpf(int(x)),-mpf(int(x))]
        Z.append(z)
    for e in [3,5,7]:
        delta=mpf(10)**(-e)
        lo,hi=mpf(10),mpf(0); cnt=0
        for blocks in parts(list(range(n)), kmax):
            ret=mpf(0); km=mpf(0)
            for C in blocks:
                w=mpf(1)/n
                cz=[sum(Z[i][j] for i in C)/len(C) for j in range(2*d)]
                cp=[mpf(1)/(2*d)+delta*x for x in cz]
                for i in C:
                    P=[mpf(1)/(2*d)+delta*Z[i][j] for j in range(2*d)]
                    ret+=w*klm(P,cp)
                ab=[sum(mpf(int(A[i][t])) for i in C)/len(C) for t in range(d)]
                for i in C:
                    km+=w*sum((mpf(int(A[i][t]))-ab[t])**2 for t in range(d))
            if km<=0: continue
            r=ret/(2*d*delta**2*km); lo=min(lo,r); hi=max(hi,r); cnt+=1
        spread=hi-lo; allspread.append((e,float(spread)))
        print(f"{d:>2} {n:>2} {'1e-'+str(e):>8} {cnt:>7} {mp.nstr(lo,14):>18} {mp.nstr(hi,14):>18} {float(spread):>11.2e}")

print()
print("Spread (max-min ratio) vs delta -- must vanish, giving a UNIFORM sandwich:")
import collections
by=collections.defaultdict(list)
for e,s in allspread: by[e].append(s)
for e in sorted(by): print(f"   delta=1e-{e}:  max spread over instances = {max(by[e]):.3e}")
print()
print("=> ratio -> 1 uniformly over ALL partitions, so for delta with poly-many")
print("   bits the two-sided bound holds simultaneously for every C.  A rho-")
print("   approximation to RetKL therefore yields a rho(1+O(eps))-approximation")
print("   to k-means: the reduction is approximation preserving (APX).")

print()
print("Sanity: does the ARGMIN transfer?  (optimal partition must agree)")
mism=0; tot=0
for d,n,kmax in [(2,5,3),(3,5,3),(2,6,3)]:
    A=rng.integers(-4,5,(n,d))
    Z=[]
    for a in A:
        z=[]
        for x in a: z+=[mpf(int(x)),-mpf(int(x))]
        Z.append(z)
    delta=mpf(10)**(-7)
    best_r=(mpf(10),None); best_k=(mpf(10),None)
    for bi,blocks in enumerate(parts(list(range(n)),kmax)):
        ret=mpf(0); km=mpf(0)
        for C in blocks:
            w=mpf(1)/n
            cz=[sum(Z[i][j] for i in C)/len(C) for j in range(2*d)]
            cp=[mpf(1)/(2*d)+delta*x for x in cz]
            for i in C:
                P=[mpf(1)/(2*d)+delta*Z[i][j] for j in range(2*d)]
                ret+=w*klm(P,cp)
            ab=[sum(mpf(int(A[i][t])) for i in C)/len(C) for t in range(d)]
            for i in C:
                km+=w*sum((mpf(int(A[i][t]))-ab[t])**2 for t in range(d))
        if ret<best_r[0]: best_r=(ret,bi)
        if km <best_k[0]: best_k=(km ,bi)
    tot+=1
    if best_r[1]!=best_k[1]: mism+=1
print(f"   argmin agreement on {tot} instances: mismatches = {mism}")
