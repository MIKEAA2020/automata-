"""
AAK indexing check (audit 4.4).

Convention to verify:  for a Hankel operator H_psi with rational symbol psi,
  rank(H_psi) = McMillan degree of psi (Kronecker's theorem).
If so, "rank <= M" and "McMillan degree <= M" agree, and pairing both with
sigma_{M+1} is internally consistent.

Test: build Hankel matrices from rational symbols with known degree
(sums of d simple poles inside the disc) and check numerical rank = d.
"""
import numpy as np

rng = np.random.default_rng(0)

print("=" * 74)
print("KRONECKER: rank of a Hankel operator = McMillan degree of its symbol")
print("=" * 74)
print(f"{'degree d':>9} {'trials':>7} {'ranks observed':>18}")

N = 60  # Hankel truncation size
for d in (1, 2, 3, 4, 5):
    ranks = set()
    for _ in range(40):
        # strictly proper rational symbol with d distinct poles inside the disc
        poles = rng.uniform(-0.8, 0.8, d) + 1j*rng.uniform(-0.3, 0.3, d)
        res = rng.normal(size=d) + 1j*rng.normal(size=d)
        # impulse response h_k = sum_j res_j * poles_j^k
        k = np.arange(2*N)
        h = np.array([np.sum(res * poles**kk) for kk in k])
        H = np.array([[h[i+j] for j in range(N)] for i in range(N)])
        sv = np.linalg.svd(H, compute_uv=False)
        r = int(np.sum(sv > 1e-8 * sv[0]))
        ranks.add(r)
    print(f"{d:>9} {40:>7} {sorted(ranks)!s:>18}")
    assert ranks == {d}, (d, ranks)

print()
print("  rank(H) = d exactly, in every trial.  Kronecker's theorem confirmed.")

print()
print("=" * 74)
print("CONSEQUENCE FOR THE MANUSCRIPT'S INDEXING")
print("=" * 74)
print("  The theorem pairs:")
print("     distance to {Hankel, rank <= M}  =  sigma_{M+1}(H)")
print("     optimal approximant has McMillan degree <= M")
print()
print("  By Kronecker these two descriptions of the feasible set coincide,")
print("  so the indexing is internally consistent: with singular values")
print("  indexed from 1, the best rank-<=M approximation error is sigma_{M+1}.")
print()
print("  Sanity on the index convention itself (Eckart-Young, unstructured):")
for M in (0, 1, 2, 3):
    A = rng.normal(size=(30, 30))
    sv = np.linalg.svd(A, compute_uv=False)
    U, S, Vt = np.linalg.svd(A)
    Ak = (U[:, :M] * S[:M]) @ Vt[:M]
    err = np.linalg.norm(A - Ak, 2)
    print(f"    M={M}: ||A - A_M||_2 = {err:.6f},  sigma_(M+1) = {sv[M]:.6f}, "
          f"match={abs(err-sv[M])<1e-9}")
