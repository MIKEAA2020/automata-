"""Audit 5.1 claimed: a lower bound of order inf_M[a_M+b_M] REQUIRES a
direct-sum construction forcing both axes at once.

But lem:discrete-bv-sandwich already gives  B <= A <= (1+kappa)B  where
   B = sup_M min{a(M), b(M)},     A = inf_M [a(M)+b(M)].
So a floor of  c*B  yields  minimax >= c*B >= c*A/(1+kappa)  automatically.
Test whether B <= A <= (1+kappa)B holds on random discrete envelopes.
"""
import numpy as np
rng = np.random.default_rng(0)

def trial(n, rng):
    # a nonincreasing positive, b nondecreasing positive
    a = np.sort(rng.uniform(0.01, 10, n))[::-1].copy()
    b = np.sort(rng.uniform(0.01, 10, n)).copy()
    if not (b[0] <= a[0]):  return None          # condition (a)
    idx = np.where(b >= a)[0]
    if len(idx) == 0:       return None          # condition (b)
    Ms = idx[0]                                   # 0-based crossing index
    kappa = b[Ms]/b[Ms-1] if Ms >= 1 else 1.0
    B = max(min(a[i], b[i]) for i in range(n))
    A = min(a[i]+b[i] for i in range(n))
    return B, A, kappa

bad_lo = bad_hi = 0; n_ok = 0; worst_ratio = 0.0; tight = 1e9
for _ in range(400000):
    r = trial(int(rng.integers(2, 12)), rng)
    if r is None: continue
    B, A, kappa = r; n_ok += 1
    if A < B - 1e-12:                 bad_lo += 1
    if A > (1+kappa)*B + 1e-12:       bad_hi += 1
    worst_ratio = max(worst_ratio, A/B)
    tight = min(tight, (1+kappa)*B/A)
print(f"instances satisfying (a),(b): {n_ok}")
print(f"violations of  B <= A          : {bad_lo}")
print(f"violations of  A <= (1+kappa)B : {bad_hi}")
print(f"max observed A/B ratio         : {worst_ratio:.6f}")
print(f"min slack (1+kappa)B/A (>=1)   : {tight:.6f}")
print()
print("=> a floor  minimax >= c*B  implies  minimax >= c/(1+kappa) * inf_M[a_M+b_M]")
print("   with NO direct-sum construction: the sandwich supplies the conversion.")
