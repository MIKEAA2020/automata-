"""
Diagnose the violation: is the audit's theorem false, or was m_K sampled on
too small a set?

The Bregman step needs  D_KL(p_eta || p_zeta) >= (m/2)||eta - zeta||^2  with m
a lower bound on the Hessian along the SEGMENT [eta_s, zeta_C].  zeta_C is the
natural parameter of the MIXTURE centroid, which need not lie in the convex
hull of {eta_s} in eta-coordinates (the map p <-> eta is nonlinear).

Re-test with m_K computed over a set that provably contains all needed points:
the eta-images of the whole probability simplex region spanned by the mixtures,
i.e. over all convex combinations of the p_s (in p-space), which is where every
centroid lives.
"""
import numpy as np
import itertools
from math import log

rng = np.random.default_rng(0)


def softmax(e):
    x = np.exp(e - e.max()); return x / x.sum()


def hess_chart(eta):
    full = np.concatenate([eta, [0.0]])
    p = softmax(full)
    H = np.diag(p) - np.outer(p, p)
    return H[:-1, :-1]


def kl(p, q):
    m = p > 0
    return float(np.sum(p[m] * np.log(p[m] / q[m])))


def eta_of(p):
    return np.log(p[:-1] / p[-1])


print("=" * 76)
print("A. IS THE CENTROID'S eta INSIDE THE HULL OF THE eta_s?")
print("=" * 76)
out = 0
for _ in range(20000):
    S, K = 3, 3
    P = np.array([rng.dirichlet(np.ones(K) * 4.0) for _ in range(S)])
    if P.min() < 0.05:
        continue
    w = rng.dirichlet(np.ones(S))
    cen = w @ P
    E = np.array([eta_of(p) for p in P])
    ec = eta_of(cen)
    # is ec in conv(E)?  solve a small LP-ish check via least squares on the simplex
    from itertools import product
    inside = False
    for _ in range(400):
        a = rng.dirichlet(np.ones(S))
        if np.linalg.norm(a @ E - ec) < 1e-2:
            inside = True; break
    if not inside:
        out += 1
print(f"  centroids whose eta was NOT matched inside conv(eta_s): {out}/20000 samples")
print("  (a positive count means the eta-hull is the wrong set for m_K)")

print()
print("=" * 76)
print("B. RE-TEST WITH m_K OVER THE CORRECT SET")
print("=" * 76)
print("  m_K := min eigenvalue of the chart Hessian over eta(conv{p_s}),")
print("  i.e. over the eta-images of all mixtures of the predictive laws.")

viol = 0; tested = 0; minslack = np.inf
for trial in range(1500):
    S = int(rng.integers(3, 5)); K = 3
    pi = rng.dirichlet(np.ones(S))
    P = np.array([rng.dirichlet(np.ones(K) * 4.0) for _ in range(S)])
    if P.min() < 0.05:
        continue
    E = np.array([eta_of(p) for p in P])
    # m_K over eta-images of mixtures in p-space  (the set containing every centroid)
    ms = []
    for _ in range(300):
        w = rng.dirichlet(np.ones(S))
        ms.append(np.linalg.eigvalsh(hess_chart(eta_of(w @ P))).min())
    # also include the vertices
    for p in P:
        ms.append(np.linalg.eigvalsh(hess_chart(eta_of(p))).min())
    mK = min(ms)
    if mK <= 0: continue
    bar = pi @ E
    D = E - bar
    Sig = (pi[:, None] * D).T @ D
    ev = np.sort(np.linalg.eigvalsh(Sig))[::-1]
    for M in range(1, S + 1):
        best = np.inf
        for labels in itertools.product(range(M), repeat=S):
            if len(set(labels)) > M: continue
            tot = 0.0
            for b in set(labels):
                idx = [i for i, l in enumerate(labels) if l == b]
                w = pi[idx]; cen = (w[:, None] * P[idx]).sum(0) / w.sum()
                for i, wi in zip(idx, w): tot += wi * kl(P[i], cen)
            best = min(best, tot)
        tail = ev[M-1:].sum() if M-1 < len(ev) else 0.0
        rhs = (mK/2) * tail
        tested += 1; slack = best - rhs; minslack = min(minslack, slack)
        if slack < -1e-9: viol += 1

print(f"  {tested} (instance,M) pairs, violations = {viol}, min slack = {minslack:.3e}")
print(f"  => {'HOLDS' if viol==0 else 'STILL FAILS'} with the corrected m_K")

print()
print("=" * 76)
print("VERDICT")
print("=" * 76)
if viol == 0:
    print("  The audit's theorem is CORRECT provided m_K bounds the Hessian on a")
    print("  set containing every mixture centroid, not merely on conv{eta_s}.")
    print("  The audit's own statement says 'all predictive laws AND all their")
    print("  mixture centroids belong to K', so its hypothesis is right; my")
    print("  first test simply sampled K too small.")
else:
    print("  Still failing -- the theorem needs more than the stated hypothesis.")
