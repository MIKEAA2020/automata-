"""Correct test: rank-<=1 Hankel n x n matrices are EXACTLY the homogeneous
family h_k = c * alpha^k * beta^(N-k), N = 2n-2, (alpha:beta) projective.

Proof: Hankel rank<=1 <=> h_{i+j} = a_i b_j <=> f(i+j)f(0) = f(i)f(j) up to
degeneracy.  The homogeneous form covers the closure, including beta=0 (only
the corner h_N nonzero), which the geometric ansatz c*lam^k misses.
"""
import numpy as np
from scipy.optimize import minimize_scalar
rng = np.random.default_rng(0)

def hank(h, n):
    return np.array([[h[i+j] for j in range(n)] for i in range(n)])

def best_rank1(H, n, grid=4001):
    N = 2*n-2
    best = np.inf
    # theta parameterizes (alpha,beta)=(cos,sin); c optimal in closed form
    for theta in np.linspace(0, np.pi, grid):
        a, b = np.cos(theta), np.sin(theta)
        base = np.array([a**k * b**(N-k) for k in range(N+1)])
        B = hank(base, n)
        nb = np.linalg.norm(B, 'fro')
        if nb < 1e-14:
            continue
        # minimize ||H - c*B||_2 over c : 1-D convex, solve numerically
        r = minimize_scalar(lambda c: np.linalg.norm(H - c*B, 2),
                            bounds=(-50, 50), method='bounded',
                            options={'xatol': 1e-13})
        best = min(best, r.fun)
    return best

print("AAK equality for FINITE n x n Hankel matrices:")
print("  dist(H, {Hankel, rank<=1})  vs  sigma_2(H)\n")
print(f"{'n':>3} {'sigma_2(H)':>14} {'dist rank<=1':>15} {'ratio':>9}")
viol = 0
for n in [3, 4, 5, 6]:
    for _ in range(4):
        h = rng.normal(size=2*n-1)
        H = hank(h, n)
        s = np.linalg.svd(H, compute_uv=False)
        d = best_rank1(H, n)
        flag = ""
        if d > s[1]*(1+1e-6):
            viol += 1; flag = "  <-- exceeds sigma_2"
        print(f"{n:>3} {s[1]:>14.8f} {d:>15.8f} {d/s[1]:>9.4f}{flag}")
print(f"\ncases where distance strictly exceeds sigma_2: {viol}/16")
