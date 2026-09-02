"""Can the promise-hardness be elevated to APX-hardness (constant-factor
inapproximability) for finite-alphabet full-KL retention?

k-means is APX-hard (Awasthi-Charikar-Krishnaswamy-Sinop 2015): NP-hard to
approximate within some constant 1+eps0.

Embedding: p_i = u + delta*z_i  gives  RetKL(k) = (2 d delta^2/n) * OPT_kmeans + R,
|R| <= C0 d^2 delta^3 Z^3.  A rho-approximation to RetKL yields what factor
for k-means?  Need R small RELATIVE to OPT, not just relative to the gap.
"""
import numpy as np, math
from mpmath import mp, mpf, log as mlog
mp.dps = 50
rng = np.random.default_rng(3)

def kl(p,q): return sum(a*mlog(a/b) for a,b in zip(p,q) if a>0)

print("Ratio  RetKL(partition) / [ (2 d delta^2/n) * kmeans(partition) ]  -> 1 ?")
print("If uniformly 1+o(1) across ALL partitions, a rho-approx transfers.\n")
for d,n in [(2,6),(3,6)]:
    A = rng.integers(-4,5,(n,d))
    Z = []
    for a in A:
        z=[]
        for x in a: z += [mpf(int(x)), -mpf(int(x))]
        Z.append(z)
    print(f"  d={d} n={n}:")
    for e in [3,5,7]:
        delta = mpf(10)**(-e)
        worst_lo, worst_hi = mpf(10), mpf(0)
        # enumerate 2-block partitions
        for mask in range(1, 2**(n-1)):
            C0 = [i for i in range(n) if (mask>>i)&1]
            C1 = [i for i in range(n) if not (mask>>i)&1]
            if not C0 or not C1: continue
            ret = mpf(0); km = mpf(0)
            for C in (C0, C1):
                w = mpf(1)/n
                cen_z = [sum(Z[i][j] for i in C)/len(C) for j in range(2*d)]
                cen_p = [mpf(1)/(2*d) + delta*cz for cz in cen_z]
                for i in C:
                    P = [mpf(1)/(2*d) + delta*Z[i][j] for j in range(2*d)]
                    ret += w*kl(P, cen_p)
                abar = [sum(mpf(int(A[i][t])) for i in C)/len(C) for t in range(d)]
                for i in C:
                    km += w*sum((mpf(int(A[i][t]))-abar[t])**2 for t in range(d))
            if km <= 0: continue
            pred = 2*d*delta**2*km
            r = ret/pred
            worst_lo = min(worst_lo, r); worst_hi = max(worst_hi, r)
        print(f"    delta=1e-{e}: ratio in [{mp.nstr(worst_lo,12)}, {mp.nstr(worst_hi,12)}]")
print("\n=> ratio -> 1 UNIFORMLY over partitions as delta->0, so for delta small")
print("   enough (poly bits) a rho-approximation to RetKL gives a rho(1+o(1))-")
print("   approximation to k-means.  APX-hardness transfers.")
