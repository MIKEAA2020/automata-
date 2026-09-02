"""
Discrete bias-variance sandwich, needing only monotonicity + normalisation
+ a bounded relative jump.  No continuity, no exact crossing point.

  a : N -> R_{>0} nonincreasing        (approximation)
  b : N -> R_{>0} nondecreasing        (estimation)
  (N)  b(1) <= a(1)                    nondegeneracy
  (C)  b(M) >= a(M) for some M         eventual crossing
  (J)  b(M*) <= kappa * b(M*-1)  where M* = min{M : b(M) >= a(M)}

  B = sup_M min{a(M), b(M)},   A = inf_M [a(M) + b(M)]

Claim:   B <= A <= (1 + kappa) B.
"""
import random

RANGE = 400


def B_of(a, b, n=RANGE):
    return max(min(a(M), b(M)) for M in range(1, n + 1))


def A_of(a, b, n=RANGE):
    return min(a(M) + b(M) for M in range(1, n + 1))


def check(a, b, n=RANGE, verbose=False):
    # locate M*
    Ms = None
    for M in range(1, n + 1):
        if b(M) >= a(M):
            Ms = M
            break
    if Ms is None or Ms == 1:
        return None            # hypotheses (C)/(N) not met on this window
    kappa = b(Ms) / b(Ms - 1)
    B = B_of(a, b, n)
    A = A_of(a, b, n)
    lo_ok = B <= A + 1e-12
    hi_ok = A <= (1 + kappa) * B + 1e-12
    if verbose:
        print(f"    M*={Ms:3d} kappa={kappa:8.4f}  B={B:12.5f} A={A:12.5f} "
              f"A/B={A/B:7.4f}  bound={1+kappa:7.4f}")
    return lo_ok, hi_ok, A / B, 1 + kappa


print("Deterministic families")
print("=" * 72)
fams = [
    ("a=T/M,   b=sqrt(T ln(eM))", lambda M: 1000.0 / M,
     lambda M: (1000.0 * __import__('math').log(2.718281828 * M)) ** .5),
    ("a=exp(-M), b=M",            lambda M: 100 * 2.718281828 ** (-M),
     lambda M: float(M)),
    ("a=1/M^2,  b=M^0.5/50",      lambda M: 1.0 / M ** 2,
     lambda M: M ** .5 / 50),
    ("a=M^-1.5, b=log(1+M)/300",  lambda M: M ** -1.5,
     lambda M: __import__('math').log(1 + M) / 300),
]
for name, a, b in fams:
    r = check(a, b, verbose=False)
    print(f"  {name:30s}", end=" ")
    if r is None:
        print("hypotheses not met on window")
    else:
        lo, hi, ratio, bd = r
        print(f"B<=A {lo}   A<=(1+k)B {hi}   A/B={ratio:.4f} <= {bd:.4f}")
        assert lo and hi

print()
print("Randomised search for a counterexample (monotone step functions)")
print("=" * 72)
random.seed(11)
worst = 0.0
bad = 0
trials = 0
for _ in range(300000):
    n = random.randint(3, 14)
    # random positive nonincreasing a, nondecreasing b
    av = sorted([random.expovariate(1.0) + 1e-3 for _ in range(n)], reverse=True)
    bv = sorted([random.expovariate(1.0) + 1e-3 for _ in range(n)])
    a = lambda M, av=av: av[M - 1]
    b = lambda M, bv=bv: bv[M - 1]
    if bv[0] > av[0]:
        continue                      # (N) fails
    r = check(a, b, n)
    if r is None:
        continue
    trials += 1
    lo, hi, ratio, bd = r
    worst = max(worst, ratio / bd)
    if not (lo and hi):
        bad += 1
        print("  COUNTEREXAMPLE", av, bv)
        break

print(f"  {trials} admissible random instances tested")
print(f"  violations: {bad}")
print(f"  worst observed (A/B) / (1+kappa) = {worst:.6f}   (must be <= 1)")
assert bad == 0 and worst <= 1.0 + 1e-9

print()
print("Tightness: the constant 1+kappa cannot be replaced by 2 in general.")
# a two-point family with a big jump in b
av = [10.0, 1.0]
bv = [1.0, 9.0]
a = lambda M: av[M - 1]
b = lambda M: bv[M - 1]
r = check(a, b, 2, verbose=True)
print(f"  A/B = {r[2]:.4f} > 2 while 1+kappa = {r[3]:.4f}")
assert r[2] > 2 and r[0] and r[1]

print("\nALL CHECKS PASSED")
