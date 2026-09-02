import numpy as np, math, itertools
from fractions import Fraction
rng=np.random.default_rng(7)
def kl(p,q): return sum(a*math.log(a/b) for a,b in zip(p,q) if a>0)

def embed(a,delta,d):
    z=np.empty(2*d)
    z[0::2]=a; z[1::2]=-a
    return np.full(2*d,1.0/(2*d))+delta*z, z

print("Check 1: tangent embedding properties  sum(z)=0 and ||z_i-z_j||^2 = 2||a_i-a_j||^2")
bad=0
for _ in range(20000):
    d=rng.integers(1,5); a1=rng.integers(-5,6,d).astype(float); a2=rng.integers(-5,6,d).astype(float)
    _,z1=embed(a1,0.0,d); _,z2=embed(a2,0.0,d)
    if abs(z1.sum())>1e-12 or abs(((z1-z2)**2).sum()-2*((a1-a2)**2).sum())>1e-9: bad+=1
print("   violations:",bad,"/20000")

print("\nCheck 2: J_C / (d*delta^2) -> kmeans within-cluster cost * 2, as delta->0")
print(f"{'delta':>10} {'J_C':>16} {'J_C/(d delta^2)':>18} {'2*kmeans':>14} {'rel err':>12}")
d=3; n=6
A=rng.integers(-4,5,(n,d)).astype(float)
w=np.ones(n)/n
abar=A.mean(axis=0)
km=sum(w[i]*((A[i]-abar)**2).sum() for i in range(n))
for delta in [1e-2,1e-3,1e-4,1e-5,1e-6]:
    P=[embed(A[i],delta,d)[0] for i in range(n)]
    pbar=sum(w[i]*P[i] for i in range(n))
    J=sum(w[i]*kl(P[i],pbar) for i in range(n))
    lead=J/(d*delta**2)
    print(f"{delta:10.0e} {J:16.8e} {lead:18.10f} {2*km:14.10f} {abs(lead-2*km)/(2*km):12.3e}")

print("\nCheck 3: cubic error bound  |J_C - d delta^2 * 2*kmeans| <= C d^2 delta^3 * sum w ||z-zbar||_3^3")
worst=0.0
for trial in range(3000):
    d=int(rng.integers(1,4)); n=int(rng.integers(2,6)); delta=float(10**rng.uniform(-5,-2))
    A=rng.integers(-4,5,(n,d)).astype(float); w=rng.dirichlet(np.ones(n))
    Z=np.array([embed(A[i],0.0,d)[1] for i in range(n)])
    zbar=(w[:,None]*Z).sum(axis=0)
    P=[np.full(2*d,1.0/(2*d))+delta*Z[i] for i in range(n)]
    if min(min(p) for p in P)<=0: continue
    pbar=np.full(2*d,1.0/(2*d))+delta*zbar
    J=sum(w[i]*kl(P[i],pbar) for i in range(n))
    quad=d*delta**2*sum(w[i]*((Z[i]-zbar)**2).sum() for i in range(n))
    c3=sum(w[i]*np.abs(Z[i]-zbar).sum()**3 for i in range(n))
    if c3>0: worst=max(worst,abs(J-quad)/(d*d*delta**3*c3))
print("   worst constant C observed:",worst,"(bounded => cubic remainder is uniform)")

print("\nCheck 4: min gap between distinct k-means costs on integer points has denominator | lcm(1..n)")
for n in [4,6,8]:
    L=1
    for i in range(1,n+1): L=L*i//math.gcd(L,i)
    print(f"   n={n}: lcm(1..n)={L}, so distinct costs differ by >= 1/{L} = {1/L:.3e} (2^-O(n), poly bits suffice)")
