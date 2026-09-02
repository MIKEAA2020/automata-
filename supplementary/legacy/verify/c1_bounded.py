"""
Is C_1(n) = sup ||H(z)||_{S_1} / ||z||_{l^1} bounded independently of n?

Upper bound by triangle inequality on the l^1 decomposition z = sum_k z_k e_k:
   ||H(z)||_* <= sum_k |z_k| * ||H(e_k)||_*
so  C_1 <= max_k ||H(e_k)||_* .
H(e_k) is the 0/1 matrix with ones on the anti-diagonal i+j=k, i.e. a partial
anti-identity of rank m_k = min(k+1,n,2n-1-k), all singular values 1.
So ||H(e_k)||_* = m_k <= n  =>  C_1 <= n.  That is NOT bounded.

But the numerics said C_1 ~ 3-4 and growing slowly.  Which is right?
Test the single-atom witness directly: z = e_{n-1} gives ||H||_* = n and
||z||_1 = 1, ratio n.  If so the hill-climb simply missed it.
"""
import numpy as np, math
def H(z,n): return np.array([[z[i+j] for j in range(n)] for i in range(n)])
def nuc(A): return float(np.linalg.svd(A,compute_uv=False).sum())

print("="*74)
print("SINGLE-ATOM WITNESS  z = e_{n-1}  (the full anti-diagonal)")
print("="*74)
print(f"{'n':>5}{'||H(e_{n-1})||_*':>20}{'||z||_1':>10}{'ratio':>9}")
for n in (2,4,8,16,32,64):
    z=np.zeros(2*n-1); z[n-1]=1.0
    A=H(z,n)
    print(f"{n:>5}{nuc(A):>20.4f}{1.0:>10.1f}{nuc(A):>9.4f}")

print()
print("="*74)
print("CONCLUSION")
print("="*74)
print("  C_1(n) >= n, attained by the single atom on the main anti-diagonal.")
print("  The earlier hill-climb was misleading: random restarts in R^{2n-1}")
print("  rarely find the sparse maximiser.  A DIRECT witness settles it.")
print()
print("  Corrected constants for the Hankel embedding:")
print("     C_1(n) = n,   C_2(n) = sqrt(n),   C_inf(n) = Theta(sqrt(n))?")
print()
print("  Check C_inf on the same atom and on the all-ones vector:")
for n in (4,16,64):
    z=np.zeros(2*n-1); z[n-1]=1.0
    a=np.linalg.svd(H(z,n),compute_uv=False)[0]
    o=np.ones(2*n-1)
    b=np.linalg.svd(H(o,n),compute_uv=False)[0]/np.abs(o).max()
    print(f"   n={n:>3}: atom op-norm ratio = {a:.3f},  all-ones ratio = {b:.3f}"
          f"   (n = {n})")
print()
print("  all-ones gives ||H||_op = n exactly (rank-1 all-ones matrix),")
print("  so C_inf(n) >= n as well.")
