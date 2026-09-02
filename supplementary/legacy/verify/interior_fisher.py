"""
Verify the proposed Global Interior Fisher-Coordinate Converse:

  RetKL(M) >= (m_K/2) * sum_{i>=M} lambda_i(Sigma_eta)

with Sigma_eta the covariance of the NATURAL PARAMETERS eta_s, and
m_K = min eigenvalue of Hessian A''(eta) over the compact set K.

Key step to check:  D_KL(p_eta || p_zeta) = B_A(zeta, eta) >= (m_K/2)||eta-zeta||^2
and then the ANOVA/Ky Fan argument in eta-coordinates.

Also check the subtle step: the mixture centroid's natural parameter zeta_C is
NOT generally the mean of the eta_s in the block, so the proof must pass from
zeta_C to the eta-mean.  That uses  sum w_s ||eta_s - zeta||^2 minimized at
zeta = eta-mean, which is fine.
"""
import numpy as np
import itertools
from math import log, exp

rng = np.random.default_rng(0)


def softmax(eta):
    e = np.exp(eta - eta.max())
    return e / e.sum()


def A(eta):
    return log(np.exp(eta).sum())


def hess(eta):
    p = softmax(eta)
    return np.diag(p) - np.outer(p, p)


def kl(p, q):
    m = p > 0
    return float(np.sum(p[m] * np.log(p[m] / q[m])))


def eta_of(p):
    # minimal chart: last coordinate as reference
    return np.log(p[:-1] / p[-1])


def p_of(eta):
    full = np.concatenate([eta, [0.0]])
    return softmax(full)


print("=" * 76)
print("GLOBAL INTERIOR FISHER-COORDINATE CONVERSE")
print("=" * 76)

viol = 0
tested = 0
minslack = np.inf
for trial in range(3000):
    S = int(rng.integers(3, 6))
    K = 3
    pi = rng.dirichlet(np.ones(S))
    # keep interior: bounded away from the boundary
    P = np.array([rng.dirichlet(np.ones(K) * 4.0) for _ in range(S)])
    rho = P.min()
    if rho < 0.05:
        continue
    E = np.array([eta_of(p) for p in P])

    # m_K over the convex hull of the etas (sample it)
    ms = []
    for _ in range(40):
        w = rng.dirichlet(np.ones(S))
        eta = w @ E
        full = np.concatenate([eta, [0.0]])
        H = hess(full)
        # restrict to the minimal chart: drop the reference coordinate
        Hm = H[:-1, :-1]
        ms.append(np.linalg.eigvalsh(Hm).min())
    mK = min(ms)
    if mK <= 0:
        continue

    bar = pi @ E
    D = E - bar
    Sig = (pi[:, None] * D).T @ D
    ev = np.sort(np.linalg.eigvalsh(Sig))[::-1]

    for M in range(1, S + 1):
        # exact RetKL over partitions into <= M blocks (mixture centroids)
        best = np.inf
        for labels in itertools.product(range(M), repeat=S):
            if len(set(labels)) > M:
                continue
            tot = 0.0
            for b in set(labels):
                idx = [i for i, l in enumerate(labels) if l == b]
                w = pi[idx]
                cen = (w[:, None] * P[idx]).sum(0) / w.sum()
                for i, wi in zip(idx, w):
                    tot += wi * kl(P[i], cen)
            best = min(best, tot)
        tail = ev[M - 1:].sum() if M - 1 < len(ev) else 0.0
        rhs = (mK / 2) * tail
        tested += 1
        slack = best - rhs
        minslack = min(minslack, slack)
        if slack < -1e-9:
            viol += 1
            if viol <= 3:
                print(f"  VIOLATION M={M}: RetKL={best:.6f} < bound={rhs:.6f} (mK={mK:.4f})")

print(f"  {tested} (instance, M) pairs tested exactly")
print(f"  violations: {viol}")
print(f"  min slack (RetKL - bound): {minslack:.3e}")
print(f"  => interior Fisher-chart converse {'HOLDS' if viol == 0 else 'FAILS'}")

print()
print("=" * 76)
print("SANITY: does the bound degrade as the family approaches the boundary?")
print("=" * 76)
for rho_target in (0.3, 0.1, 0.03, 0.01):
    P = np.array([[1 - 2*rho_target, rho_target, rho_target],
                  [rho_target, 1 - 2*rho_target, rho_target]])
    pi = np.array([0.5, 0.5])
    E = np.array([eta_of(p) for p in P])
    full = np.concatenate([pi @ E, [0.0]])
    mK = np.linalg.eigvalsh(hess(full)[:-1, :-1]).min()
    print(f"  min p = {rho_target:6.3f}   m_K = {mK:.6f}")
print("  m_K -> 0 at the boundary, so the constant degrades exactly there,")
print("  which is why the theorem is stated on a compact interior set.")
