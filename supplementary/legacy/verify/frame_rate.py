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
Pin down the growth of C_p(n) = sup_z ||H(z)||_{S_p} / ||z||_{l^p}
for the n x n Hankel embedding, and identify the p for which it is
dimension-free.

Theory:
 - p=2: ||H(z)||_F^2 = sum_k m_k |z_k|^2 with multiplicity m_k <= n,
   so C_2 = sqrt(max multiplicity) = sqrt(n) exactly (attained at the
   anti-diagonal index k = n-1).
 - p=1 (nuclear): C_1 >= ||H(e_k)||_* / 1.  H(e_{n-1}) is the anti-identity,
   nuclear norm n.  So C_1 >= n?  test.
 - p=inf: ||H(e_{n-1})||_op = 1, but sup over general z is larger.
Determine empirically with a power-iteration style search.
"""
import numpy as np
rng = np.random.default_rng(1)

def H(z,n):
    return np.array([[z[i+j] for j in range(n)] for i in range(n)])

def schatten(A,p):
    sv=np.linalg.svd(A,compute_uv=False)
    return sv[0] if p==np.inf else float((sv**p).sum()**(1/p))

def maximize(n,p,iters=4000):
    best=0.0; bz=None
    # random restarts + local hill climb
    for _ in range(60):
        z=rng.normal(size=2*n-1)
        z/= (np.abs(z).max() if p==np.inf else (np.abs(z)**p).sum()**(1/p))
        cur=schatten(H(z,n),p)
        step=0.5
        for _ in range(iters//60):
            cand=z+step*rng.normal(size=2*n-1)
            cand/= (np.abs(cand).max() if p==np.inf else (np.abs(cand)**p).sum()**(1/p))
            v=schatten(H(cand,n),p)
            if v>cur: z,cur=cand,v
            else: step*=0.97
        if cur>best: best,bz=cur,z
    return best

print("="*74)
print("C_p(n) = sup ||H(z)||_{S_p} / ||z||_{l^p}")
print("="*74)
print(f"{'n':>4}{'C_1':>10}{'C_1/n':>9}{'C_2':>10}{'C_2/sqrt n':>12}{'C_inf':>10}{'C_inf/sqrt n':>14}")
import math
for n in (2,4,8,16,32):
    c1=maximize(n,1); c2=maximize(n,2); ci=maximize(n,np.inf)
    print(f"{n:>4}{c1:>10.3f}{c1/n:>9.3f}{c2:>10.3f}{c2/math.sqrt(n):>12.3f}"
          f"{ci:>10.3f}{ci/math.sqrt(n):>14.3f}")

print()
print("="*74)
print("EXACT p=2 CONSTANT (analytic)")
print("="*74)
for n in (2,4,8,16,32,64):
    # ||H(z)||_F^2 = sum_k m_k z_k^2, m_k = #{(i,j): i+j=k} = min(k+1, n, 2n-1-k)
    m=[min(k+1,n,2*n-1-k) for k in range(2*n-1)]
    print(f"  n={n:>3}: max multiplicity = {max(m):>3}  => C_2 = sqrt({max(m)}) = {math.sqrt(max(m)):.4f}")
print()
print("  C_2(n) = sqrt(n) exactly.  NOT dimension-free.")
