"""Does the AAK equality hold for FINITE Hankel matrices?

AAK: dist(H, {Hankel, rank<=n}) == sigma_{n+1}(H)  [1-indexed]
For infinite Hankel operators this is the AAK theorem.  Check the finite
analogue, since if it FAILS the prompt must warn against finite-matrix sources.
"""
import numpy as np
from scipy.optimize import minimize
rng = np.random.default_rng(0)

def hankel_from(h, n):
    return np.array([[h[i+j] for j in range(n)] for i in range(n)])

# rank-1 Hankel matrices have h_k = c * lam^k  (geometric sequence)
def best_rank1_hankel(H, n, tries=60):
    best = np.inf
    for _ in range(tries):
        x0 = np.array([rng.normal()*2, rng.normal()])
        def obj(p):
            c, lam = p
            h = np.array([c*(lam**k) for k in range(2*n-1)])
            return np.linalg.norm(H - hankel_from(h, n), 2)
        r = minimize(obj, x0, method='Nelder-Mead',
                     options={'xatol':1e-12,'fatol':1e-14,'maxiter':20000})
        best = min(best, r.fun)
    return best

print(f"{'n':>3} {'sigma_2(H)':>14} {'dist to rank<=1 Hankel':>24} {'ratio':>10}")
for n in [3, 4, 5, 6]:
    for trial in range(3):
        h = rng.normal(size=2*n-1)
        H = hankel_from(h, n)
        s = np.linalg.svd(H, compute_uv=False)
        d = best_rank1_hankel(H, n)
        print(f"{n:>3} {s[1]:>14.8f} {d:>24.8f} {d/s[1]:>10.4f}")
