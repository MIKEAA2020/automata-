"""
Audit 2.1: proposed GLOBAL full-KL spectral converse via probability-vector
covariance.

Claim chain:
  (a) Phi(p) = sum p_i log p_i is 1-strongly convex on the simplex in ||.||_2,
      so D_KL(p||q) >= (1/2)||p-q||_2^2.
  (b) mixture centroid is the optimal block representative for weighted KL.
  (c) ANOVA: Sigma_p = W_phi + B_phi, rank(B_phi) <= M-1.
  (d) Ky Fan: tr(B_phi) <= sum_{i<M} lambda_i(Sigma_p).
  (e) => RetKL(phi) >= (1/2) tr(W_phi) >= (1/2) sum_{i>=M} lambda_i(Sigma_p).

CRITICAL CHECK on (a): is Phi 1-strongly convex in the EUCLIDEAN norm on the
simplex?  Standard result: negative entropy is 1-strongly convex w.r.t. the
L1 norm (Pinsker).  In L2 the Hessian is diag(1/p_i), whose min eigenvalue is
1/max_i p_i >= 1.  So D_KL(p||q) >= (1/2)||p-q||_2^2 should hold since
p_i <= 1.  Verify numerically -- this is the crux.
"""
import numpy as np

rng = np.random.default_rng(0)

print("=" * 76)
print("A. IS  D_KL(p||q) >= (1/2)||p-q||_2^2  ON THE SIMPLEX?")
print("=" * 76)
worst = np.inf
worst_case = None
n_bad = 0
for _ in range(500000):
    k = rng.integers(2, 7)
    p = rng.dirichlet(np.ones(k) * rng.uniform(0.2, 3))
    q = rng.dirichlet(np.ones(k) * rng.uniform(0.2, 3))
    if np.any(q < 1e-12):
        continue
    kl = float(np.sum(p * np.log(p / q, where=p > 0, out=np.zeros_like(p))))
    l2 = float(np.sum((p - q) ** 2))
    slack = kl - 0.5 * l2
    if slack < worst:
        worst, worst_case = slack, (p, q)
    if slack < -1e-12:
        n_bad += 1

print(f"  500k random pairs: violations = {n_bad}")
print(f"  min (KL - 0.5*||p-q||_2^2) = {worst:.3e}")
print(f"  => inequality {'HOLDS' if n_bad == 0 else 'FAILS'}")
print()
print("  (Pinsker gives KL >= 0.5||p-q||_1^2 >= 0.5||p-q||_2^2 since")
print("   ||.||_2 <= ||.||_1.  So (a) is immediate from Pinsker.)")

print()
print("=" * 76)
print("B. FULL PIPELINE: RetKL(phi) >= (1/2) sum_{i>=M} lambda_i(Sigma_p)?")
print("=" * 76)


def retkl(pi, P, labels):
    """Weighted KL to mixture centroids."""
    tot = 0.0
    for b in set(labels):
        idx = [i for i, l in enumerate(labels) if l == b]
        w = pi[idx]
        if w.sum() <= 0:
            continue
        cen = (w[:, None] * P[idx]).sum(0) / w.sum()
        for i, wi in zip(idx, w):
            p = P[i]
            m = p > 0
            tot += wi * float(np.sum(p[m] * np.log(p[m] / cen[m])))
    return tot


def spectral_tail(pi, P, M):
    bar = (pi[:, None] * P).sum(0)
    D = P - bar
    Sig = (pi[:, None] * D).T @ D
    ev = np.sort(np.linalg.eigvalsh(Sig))[::-1]
    return 0.5 * ev[M - 1:].sum() if M - 1 < len(ev) else 0.0


import itertools
viol = 0
tested = 0
minslack = np.inf
for trial in range(4000):
    S = int(rng.integers(3, 6))
    K = int(rng.integers(2, 5))
    pi = rng.dirichlet(np.ones(S))
    P = np.array([rng.dirichlet(np.ones(K) * rng.uniform(0.3, 2.0))
                  for _ in range(S)])
    for M in range(1, S + 1):
        # exact min over partitions into <= M blocks
        best = np.inf
        for labels in itertools.product(range(M), repeat=S):
            if len(set(labels)) > M:
                continue
            best = min(best, retkl(pi, P, list(labels)))
        rhs = spectral_tail(pi, P, M)
        tested += 1
        slack = best - rhs
        minslack = min(minslack, slack)
        if slack < -1e-9:
            viol += 1
            if viol <= 3:
                print(f"  VIOLATION M={M}: RetKL={best:.6f} < bound={rhs:.6f}")

print(f"  {tested} (instance, M) pairs tested exactly")
print(f"  violations: {viol}")
print(f"  min slack (RetKL - bound) = {minslack:.3e}")
print(f"  => proposed converse {'HOLDS' if viol == 0 else 'FAILS'} on all tests")

print()
print("=" * 76)
print("C. IS IT NONTRIVIAL? (does it beat the trivial bound 0?)")
print("=" * 76)
pos = 0
tot = 0
for trial in range(2000):
    S, K = 5, 4
    pi = rng.dirichlet(np.ones(S))
    P = np.array([rng.dirichlet(np.ones(K) * 0.5) for _ in range(S)])
    for M in (2, 3):
        rhs = spectral_tail(pi, P, M)
        tot += 1
        if rhs > 1e-6:
            pos += 1
print(f"  bound strictly positive in {pos}/{tot} cases "
      f"({100*pos/tot:.1f}%) -- nontrivial")
