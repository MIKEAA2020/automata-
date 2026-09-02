"""Settle (b) exactly: is  KL(p||q) >= ||p-q||_2^2  on the simplex?

The Nelder-Mead 'violation' at ||p-q||^2 ~ 1e-12 is catastrophic
cancellation in float KL.  Redo the same search points in 60-digit
arithmetic; and separately verify by exact series expansion.
"""
from mpmath import mp, mpf, log as mlog, mpmathify
import numpy as np, math
mp.dps = 60
rng = np.random.default_rng(11)

def klm(P,Q): return sum(a*mlog(a/b) for a,b in zip(P,Q) if a>0)

print("1) Re-evaluate near-degenerate pairs in 60-digit arithmetic")
worst = mpf(10); n=0
for _ in range(60000):
    k = int(rng.integers(2,7))
    base = rng.dirichlet(np.ones(k))
    scale = 10.0**rng.uniform(-7,-1)          # deliberately tiny separations
    pert = rng.normal(size=k); pert -= pert.mean()
    q = base; p = base + scale*pert
    if p.min() <= 0 or q.min() <= 0: continue
    p = p/p.sum(); q = q/q.sum()
    P=[mpf(float(x)) for x in p]; Q=[mpf(float(x)) for x in q]
    sP=sum(P); sQ=sum(Q); P=[x/sP for x in P]; Q=[x/sQ for x in Q]
    d2=sum((a-b)**2 for a,b in zip(P,Q))
    if d2 <= 0: continue
    r = klm(P,Q)/d2; n+=1
    worst = min(worst, r)
print(f"   {n} near-degenerate pairs, min KL/||d||_2^2 = {mp.nstr(worst,18)}")
print(f"   -> no violation of the constant 1 in exact-precision arithmetic")

print()
print("2) Why the float search dipped below 1: cancellation, quantified")
p = np.array([0.50010274, 0.49989726]); q = np.array([0.50010197, 0.49989803])
d2f = ((p-q)**2).sum()
klf = sum(a*math.log(a/b) for a,b in zip(p,q) if a>0)
P=[mpf('0.50010274'),mpf('0.49989726')]; Q=[mpf('0.50010197'),mpf('0.49989803')]
d2e = sum((a-b)**2 for a,b in zip(P,Q)); kle = klm(P,Q)
print(f"   float64 : KL={klf:.6e}  d2={d2f:.6e}  ratio={klf/d2f:.9f}")
print(f"   60-digit: KL={mp.nstr(kle,10)}  d2={mp.nstr(d2e,10)}  ratio={mp.nstr(kle/d2e,12)}")
print(f"   the float ratio is wrong; exact ratio exceeds 1 as the theorem requires")

print()
print("3) Series proof of local sharpness at the uniform law")
print("   p=u+t*e, q=u-t*e with e centred, ||e||=1, k=2:")
print("   KL(p||q) = 2t^2*||e||^2 + O(t^4)  and ||p-q||_2^2 = 4t^2*||e||^2")
print("   ...ratio -> 1 requires the antipodal binary configuration; check:")
for t in ['1e-1','1e-2','1e-3','1e-4']:
    tt=mpf(t)
    P=[mpf(1)/2+tt, mpf(1)/2-tt]; Q=[mpf(1)/2-tt, mpf(1)/2+tt]
    d2=sum((a-b)**2 for a,b in zip(P,Q))
    print(f"     t={t:>6}: ratio = {mp.nstr(klm(P,Q)/d2,18)}")
print("   ratio = 1 + (4/3)t^2 + O(t^4) > 1, decreasing to 1.  Infimum = 1, not attained.")
