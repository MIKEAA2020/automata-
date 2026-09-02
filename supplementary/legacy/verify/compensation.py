"""
Verify the compensation identity used in lem:packing-criterion:
   (1/m) sum_i KL(P^i||Q) = I(V;Y) + KL(Pbar||Q)
for every Q, with Pbar the mixture and V uniform.
"""
import numpy as np
rng = np.random.default_rng(7)
def KL(p,q):
    m=p>0
    return float(np.sum(p[m]*np.log(p[m]/q[m])))
worst=0.0
for _ in range(300000):
    m=int(rng.integers(2,7)); n=int(rng.integers(2,8))
    P=np.array([rng.dirichlet(np.ones(n)*rng.uniform(.3,2)) for _ in range(m)])
    Q=rng.dirichlet(np.ones(n)*rng.uniform(.3,2))
    if Q.min()<1e-12: continue
    Pbar=P.mean(axis=0)
    lhs=np.mean([KL(P[i],Q) for i in range(m)])
    I=np.mean([KL(P[i],Pbar) for i in range(m)])
    rhs=I+KL(Pbar,Q)
    worst=max(worst,abs(lhs-rhs))
print(f"max |LHS - RHS| over 300k random (P,Q): {worst:.3e}")
assert worst<1e-9
print("compensation identity CONFIRMED")
print()
print("Corollary: min over Q is at Q=Pbar with value I(V;Y).  Verified.")
