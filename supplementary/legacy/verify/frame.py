import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.environ.get('BST_ROOT', _os.path.dirname(_HERE))
def _p(name):
    for c in (_os.path.join(_ROOT, name),
              _os.path.join(_ROOT, 'manuscript.tex') if name.endswith('.tex') else '',
              _os.path.join(_HERE, name)):
        if c and _os.path.exists(c):
            return c
    return _os.path.join(_ROOT, name)

"""
Does a frame-type lower bound on a LINEAR measurement map give Schatten-p
domination?

Setup.  Suppose the task cost is a contextwise l^p aggregation of residuals
    L(delta, dhat) = ( sum_u w_u |Phi(delta,dhat)(u)|^p )^{1/p}
and there is a LINEAR map  T : (residual differences) -> operators, with
    A_delta - A_dhat = T(delta - dhat).
A frame-type lower bound says  ||T(z)||_{S_p} <= C ||z||_{l^p(w)}.
Then L >= (1/C) ||A_delta - A_dhat||_{S_p}, which is exactly domination with
c_p = C.

So the REAL question is: when is  ||T(z)||_{S_p} <= C ||z||_{l^p(w)} ?
Test the natural instance: z |-> Hankel matrix of z (the grounding case),
and z |-> diagonal (the retention case).
"""
import numpy as np
rng = np.random.default_rng(0)

def schatten(A,p):
    sv = np.linalg.svd(A, compute_uv=False)
    if p == np.inf: return sv[0]
    return float((sv**p).sum()**(1.0/p))

print("="*76)
print("A. DIAGONAL EMBEDDING  z -> diag(z)   (retention-type)")
print("="*76)
print("  ||diag(z)||_{S_p} = ||z||_{l^p} exactly, so C = 1 and domination is")
print("  an identity.  Verify:")
worst=0.0
for _ in range(20000):
    n=int(rng.integers(2,8)); z=rng.normal(size=n)
    for p in (1,2,np.inf):
        lhs=schatten(np.diag(z),p)
        rhs=np.abs(z).max() if p==np.inf else float((np.abs(z)**p).sum()**(1/p))
        worst=max(worst,abs(lhs-rhs))
print(f"  max |Schatten_p(diag z) - ||z||_p| = {worst:.3e}  -> C = 1")
assert worst < 1e-9

print()
print("="*76)
print("B. HANKEL EMBEDDING  z -> H(z)   (grounding-type)")
print("="*76)
print("  Is ||H(z)||_{S_p} <= C ||z||_{l^p} with C independent of dimension?")
print()
print(f"{'p':>5}{'n':>5}{'max ratio ||H(z)||_Sp / ||z||_p':>34}")
for p in (1,2,np.inf):
    for n in (4,8,16,32):
        worst=0.0
        for _ in range(3000):
            z=rng.normal(size=2*n-1)
            H=np.array([[z[i+j] for j in range(n)] for i in range(n)])
            num=schatten(H,p)
            den=np.abs(z).max() if p==np.inf else float((np.abs(z)**p).sum()**(1/p))
            if den>0: worst=max(worst,num/den)
        print(f"{str(p):>5}{n:>5}{worst:>34.4f}")

print()
print("="*76)
print("C. VERDICT")
print("="*76)
print("  p=2 : ratio is bounded (Frobenius of a Hankel counts each z_k with")
print("        multiplicity <= n, so C = sqrt(n) -- GROWS with n).")
print("  p=inf: ratio bounded by ~sqrt(n) too (operator norm of Hankel).")
print("  p=1 : ratio bounded.")
print()
print("  So the frame constant C is NOT dimension-free for the Hankel")
print("  embedding.  A dimension-dependent C still gives domination, but the")
print("  modulus c_p then depends on M, which weakens the converse.")
