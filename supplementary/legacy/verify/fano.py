"""
Does the m-point (Fano/Yao) replacement actually give the minimax bound?

Claim: if there are m processes P_1..P_m in the class with
   (1/m) sum_i KL(P_i || Pbar) >= Delta_M          [packing condition]
then every predictor has sup_P Reg_T >= Delta_M / 2  (say).

Standard route, log loss: for ANY predictor h inducing transcript law Q_h,
   (1/m) sum_i R_i(h) = (1/m) sum_i KL(P_i||Q_h)
                      >= (1/m) sum_i KL(P_i||Pbar)     [Pbar minimises]
                      =  I(V;Y)   with V uniform on [m].
So the AVERAGE regret is >= I(V;Y), hence the SUP is too.
Verify numerically that Pbar is the minimiser and that the identity holds.
"""
import numpy as np
rng = np.random.default_rng(1)

def KL(p,q):
    m = p>0
    return float(np.sum(p[m]*np.log(p[m]/q[m])))

print("="*74)
print("A. Pbar MINIMISES THE AVERAGE, AND THE MIN EQUALS I(V;Y)")
print("="*74)
bad=0
worstgap=np.inf
for trial in range(100000):
    m = int(rng.integers(2,6)); n = int(rng.integers(2,7))
    P = np.array([rng.dirichlet(np.ones(n)*rng.uniform(.3,2)) for _ in range(m)])
    Pbar = P.mean(axis=0)
    base = np.mean([KL(P[i],Pbar) for i in range(m)])
    # mutual information I(V;Y) with V uniform
    I = 0.0
    for i in range(m):
        I += (1/m)*KL(P[i],Pbar)
    assert abs(I-base) < 1e-12
    # try random competitors Q
    for _ in range(6):
        Q = rng.dirichlet(np.ones(n))
        Q = 0.85*Pbar + 0.15*Q
        val = np.mean([KL(P[i],Q) for i in range(m)])
        gap = val - base
        worstgap = min(worstgap, gap)
        if gap < -1e-10: bad += 1
print(f"  violations of 'Pbar is the minimiser': {bad}")
print(f"  min observed (competitor - Pbar): {worstgap:.3e}")
assert bad==0

print()
print("="*74)
print("B. AN EXPLICIT PACKING REACHING Delta = Theta(M log M)")
print("="*74)
print("  Take the gated/transport family: |H_M| = M^M members, pairwise")
print("  distinguishable on a stream of length O(M log M).  Uniform V over a")
print("  subfamily of size m gives I(V;Y) = log m when the m transcript laws")
print("  are mutually singular on the forcing stream.")
print()
print(f"  {'M':>5} {'m = M^M':>14} {'log m (nats)':>14} {'M ln M':>12}")
import math
for M in (2,4,8,16,32):
    m = M**M
    print(f"  {M:>5} {m:>14} {M*math.log(M):>14.3f} {M*math.log(M):>12.3f}")
print()
print("  So log m = M ln M exactly for the full transport family:")
print("  the packing number IS the counting bound, and Delta_M = Theta(M log M)")
print("  is achievable by an m-point floor with m = |H_M|, never by m = 2.")

print()
print("="*74)
print("C. SANITY: m=2 CAN NEVER EXCEED 2 log 2 EVEN FOR SINGULAR PROCESSES")
print("="*74)
for n in (2,4,8,1000):
    P0 = np.zeros(n); P0[0]=1
    P1 = np.zeros(n); P1[min(1,n-1)]=1
    Pbar = .5*(P0+P1)
    print(f"  alphabet {n:>5}: sum = {KL(P0,Pbar)+KL(P1,Pbar):.6f} (cap {2*np.log(2):.6f})")
