"""
1. Is z -> diag(z) a Schatten-p isometry for ALL p in [1,inf]?
2. Does the manuscript's grounding instance actually use c_infty = 1,
   i.e. is it exposed to the Hankel no-go?
"""
import numpy as np
rng=np.random.default_rng(3)
def sch(A,p):
    sv=np.linalg.svd(A,compute_uv=False)
    return sv[0] if p==np.inf else float((sv**p).sum()**(1/p))

print("="*72)
print("1. DIAGONAL EMBEDDING IS A p-ISOMETRY")
print("="*72)
worst=0.0
for _ in range(50000):
    n=int(rng.integers(2,9)); z=rng.normal(size=n)
    for p in (1,1.5,2,3,np.inf):
        lhs=sch(np.diag(z),p)
        rhs=np.abs(z).max() if p==np.inf else float((np.abs(z)**p).sum()**(1/p))
        worst=max(worst,abs(lhs-rhs))
print(f"  max deviation over 50k trials, p in {{1,1.5,2,3,inf}}: {worst:.3e}")
assert worst<1e-9
print("  CONFIRMED: singular values of diag(z) are |z_i|, so equality for all p.")

print()
print("="*72)
print("2. THE GROUNDING INSTANCE: is c_inf = 1 legitimate?")
print("="*72)
print("  The manuscript's grounding instance sets A_delta = H_nu directly and")
print("  c_inf = 1, i.e. the cost IS the operator-norm distance between the")
print("  Hankel operators -- NOT an l^inf aggregation of a sequence that is")
print("  then embedded.  So there is no frame constant to pay: domination holds")
print("  with equality by definition of the cost.")
print()
print("  Check: cost = ||H_nu - H_nuhat||_op, response = same operator.")
for n in (4,16,64):
    z=rng.normal(size=2*n-1); w=rng.normal(size=2*n-1)
    H=lambda v: np.array([[v[i+j] for j in range(n)] for i in range(n)])
    cost=sch(H(z)-H(w),np.inf)
    resp=sch(H(z)-H(w),np.inf)
    print(f"   n={n:>3}: cost={cost:.6f}  ||A-Ahat||_op={resp:.6f}  ratio={cost/resp:.6f}")
print()
print("  ratio = 1 identically => c_inf = 1, dimension-free.")
print()
print("="*72)
print("3. SO WHO IS EXPOSED TO THE NO-GO?")
print("="*72)
print("  Only a regime whose cost is an l^p aggregation of RESIDUAL SEQUENCE")
print("  entries, which is then compared to a Schatten norm of the Hankel")
print("  embedding of those entries.  That is the 'contextwise l^p => Schatten-p'")
print("  implication the memo flags as not automatic.  The no-go quantifies")
print("  exactly how badly it fails: by a factor n at p=1,inf and sqrt(n) at p=2.")
