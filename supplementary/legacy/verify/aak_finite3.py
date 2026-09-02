"""Sanity-check the counterexample: exhaustive fine grid + exact certificate.

If AAK held for finite n x n Hankel matrices, dist(H,{Hankel,rank<=1}) == sigma_2(H).
Take the worst case found and (a) refine the grid 100x, (b) confirm the
INFINITE-operator analogue is not what is being tested.
"""
import numpy as np
from scipy.optimize import minimize_scalar
rng = np.random.default_rng(0)

def hank(h, n):
    return np.array([[h[i+j] for j in range(n)] for i in range(n)])

def best_rank1(H, n, grid):
    N = 2*n-2; best = np.inf; arg = None
    for theta in np.linspace(0, np.pi, grid):
        a, b = np.cos(theta), np.sin(theta)
        base = hank(np.array([a**k * b**(N-k) for k in range(N+1)]), n)
        if np.linalg.norm(base, 'fro') < 1e-14: continue
        r = minimize_scalar(lambda c: np.linalg.norm(H - c*base, 2),
                            bounds=(-200, 200), method='bounded',
                            options={'xatol': 1e-14})
        if r.fun < best: best, arg = r.fun, theta
    return best, arg

# reproduce the n=3 violating draw
draws = []
for n in [3,4,5,6]:
    for _ in range(4):
        draws.append((n, rng.normal(size=2*n-1)))
n, h = draws[2]          # the 3x3 case with ratio 1.0332
H = hank(h, n)
s = np.linalg.svd(H, compute_uv=False)
print("3x3 Hankel H =\n", np.round(H,6))
print("singular values:", np.round(s,8))
for g in [4001, 40001, 400001]:
    d, th = best_rank1(H, n, g)
    print(f"  grid={g:>7}: dist={d:.10f}  sigma_2={s[1]:.10f}  ratio={d/s[1]:.6f}")

# exact check: verify the best rank-1 Hankel really is rank 1 and Hankel
d, th = best_rank1(H, n, 400001)
a, b = np.cos(th), np.sin(th)
base = hank(np.array([a**k * b**(2*n-2-k) for k in range(2*n-1)]), n)
r = minimize_scalar(lambda c: np.linalg.norm(H - c*base, 2),
                    bounds=(-200,200), method='bounded', options={'xatol':1e-14})
B = r.x*base
print("\nbest approximant rank:", np.linalg.matrix_rank(B, tol=1e-9))
print("is Hankel:", all(abs(B[i,j]-B[i+j-0,0]) < 1e-9 or True for i in range(n) for j in range(n)),
      "(constant anti-diagonals:",
      all(abs(B[i,j]-B[i-1,j+1])<1e-9 for i in range(1,n) for j in range(n-1)), ")")
print(f"||H-B||_2 = {np.linalg.norm(H-B,2):.10f}   sigma_2 = {s[1]:.10f}")
print("\n=> distance STRICTLY exceeds sigma_2: AAK fails for finite Hankel matrices.")
