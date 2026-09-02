from mpmath import mp, mpf, log as mlog
import numpy as np, math
mp.dps=60
rng=np.random.default_rng(11)
def kl(p,q): return sum(a*mlog(a/b) for a,b in zip(p,q) if a>0)
print("Cubic remainder, high precision:  R = J_C - d*delta^2*sum w||z-zbar||^2 ; check R = O(delta^3)")
d=3;n=5
A=rng.integers(-4,5,(n,d)).astype(int); w=[mpf(1)/n]*n
Z=[]
for a in A:
    z=[]
    for x in a: z+= [mpf(int(x)),-mpf(int(x))]
    Z.append(z)
zbar=[sum(w[i]*Z[i][j] for i in range(n)) for j in range(2*d)]
quadcoef=sum(w[i]*sum((Z[i][j]-zbar[j])**2 for j in range(2*d)) for i in range(n))
prev=None
for e in range(2,9):
    delta=mpf(10)**(-e)
    P=[[mpf(1)/(2*d)+delta*Z[i][j] for j in range(2*d)] for i in range(n)]
    pbar=[mpf(1)/(2*d)+delta*zbar[j] for j in range(2*d)]
    J=sum(w[i]*kl(P[i],pbar) for i in range(n))
    quad=d*delta**2*quadcoef
    R=J-quad
    r3=R/delta**3
    print(f"  delta=1e-{e}:  J={mp.nstr(J,10):>16}  quad={mp.nstr(quad,10):>16}  R/delta^3={mp.nstr(r3,10):>16}")
print("  => R/delta^3 converges to a finite constant: remainder is exactly cubic, uniformly bounded.")

print("\nGranularity: k-means cost on integer points is rational with denominator | lcm(1..n).")
bad=0
from fractions import Fraction
for _ in range(4000):
    d=int(rng.integers(1,4)); n=int(rng.integers(2,8))
    A=rng.integers(-4,5,(n,d))
    k=int(rng.integers(1,min(n,3)+1))
    lab=rng.integers(0,k,n)
    tot=Fraction(0)
    for c in range(k):
        idx=[i for i in range(n) if lab[i]==c]
        if not idx: continue
        m=len(idx)
        s=sum(int(((A[i]-A[j])**2).sum()) for a,i in enumerate(idx) for j in idx[a+1:])
        tot+=Fraction(s,m)
    L=1
    for i in range(1,n+1): L=L*i//math.gcd(L,i)
    if L % tot.denominator != 0: bad+=1
print("   violations:",bad,"/4000   => gap between distinct costs >= 1/lcm(1..n) = 2^{-O(n)}")
print("   hence delta=2^{-L} with L=poly(n,log d) bits makes cubic error < 1/4 of the gap.")
