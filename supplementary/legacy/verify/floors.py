"""
Is ass:oracle-floors(i) satisfiable?

It demands TWO processes P^0,P^1 with, for EVERY predictor h,
    R_0(h) + R_1(h) >= Delta_M = min{A_app(M), Est_M(T)}.

For LOG LOSS this is testable exactly.  With L*_T(P) = H(P) the entropy,
R_i(h) = KL(P^i || Q_h) where Q_h is the law h induces on transcripts.  So the
floor says
    min_Q [ KL(P^0||Q) + KL(P^1||Q) ]  >=  Delta_M.
But the minimising Q is the mixture Pbar = (P^0+P^1)/2, and
    min_Q [...] = 2 * JSD(P^0,P^1) <= 2 log 2.
So Delta_M can never exceed 2 log 2 ~ 1.386 nats, no matter what the two
processes are.  Since Est_M(T) grows without bound in T, the floor is
UNSATISFIABLE for large T.
"""
import numpy as np
import itertools

rng = np.random.default_rng(0)

def KL(p, q):
    m = p > 0
    return float(np.sum(p[m] * np.log(p[m] / q[m])))

print("=" * 74)
print("A. min_Q [KL(P0||Q) + KL(P1||Q)] = 2*JSD(P0,P1) <= 2 log 2")
print("=" * 74)
worst = 0.0
for trial in range(200000):
    n = rng.integers(2, 8)
    P0 = rng.dirichlet(np.ones(n) * rng.uniform(0.2, 3))
    P1 = rng.dirichlet(np.ones(n) * rng.uniform(0.2, 3))
    Pbar = 0.5 * (P0 + P1)
    val = KL(P0, Pbar) + KL(P1, Pbar)
    worst = max(worst, val)
    # confirm Pbar is the minimiser: perturb
    if trial < 2000:
        for _ in range(5):
            Q = 0.9 * Pbar + 0.1 * rng.dirichlet(np.ones(n))
            assert KL(P0, Q) + KL(P1, Q) >= val - 1e-12
print(f"  max over 200k random pairs: {worst:.6f}")
print(f"  2 log 2 = {2*np.log(2):.6f}")
print(f"  cap respected: {worst <= 2*np.log(2) + 1e-9}")
assert worst <= 2 * np.log(2) + 1e-9

print()
print("=" * 74)
print("B. THE CAP IS ATTAINED (mutually singular processes)")
print("=" * 74)
P0 = np.array([1.0, 0.0]); P1 = np.array([0.0, 1.0])
Pbar = 0.5 * (P0 + P1)
print(f"  P0=(1,0), P1=(0,1):  min_Q sum = {KL(P0,Pbar)+KL(P1,Pbar):.6f} = 2 log 2")

print()
print("=" * 74)
print("C. CONSEQUENCE FOR THE ASSUMPTION")
print("=" * 74)
print("  Delta_M = min{A_app(M), Est_M(T)}.  In any log-loss regime with")
print("  Est_M(T) -> infinity (e.g. Theta(M log M) realizable, or")
print("  Theta(sqrt(T M log M)) agnostic), Delta_M eventually exceeds 2 log 2.")
print("  => ass:oracle-floors(i) is then UNSATISFIABLE: no two processes exist.")
print()
print("  This is not a failure to verify the hypothesis.  It is a proof that")
print("  the hypothesis is FALSE as stated, for large T.")

print()
print("=" * 74)
print("D. THE m-POINT REPLACEMENT: min_Q (1/m) sum_i KL(P_i||Q) = I(V;Y) <= log m")
print("=" * 74)
for m in (2, 4, 8, 16, 64):
    # m mutually singular processes on m points: I = log m exactly
    P = np.eye(m)
    Pbar = P.mean(axis=0)
    val = np.mean([KL(P[i], Pbar) for i in range(m)])
    print(f"  m={m:3d}:  (1/m) sum KL(P_i||Pbar) = {val:.6f},  log m = {np.log(m):.6f},"
          f"  equal={abs(val-np.log(m))<1e-9}")
print()
print("  So an m-point floor can carry Delta_M up to log m.  To reach")
print("  Delta_M = Theta(M log M) one needs m = exp(Theta(M log M)) processes,")
print("  which is exactly |H_M|.  The two-point form was the error.")
