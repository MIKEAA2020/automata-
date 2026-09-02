"""
=============================================================================
SUPERSEDED -- retained for provenance only.  DO NOT CITE.

This script probed the claim that PRODUCT additivity forces the multiplicative
Cauchy equation  g(uv) = u g(v) + v g(u).  That derivation was later DISPROVED
(Turn 19): reverse KL, g(t) = -log t, is product-additive yet is not a multiple
of forward KL, and the claimed eps^2 coefficient evaluates to +2.4849 for it
while the true defect is 0 to 50 digits.

The correct argument uses a NON-PRODUCT conditional and is in
  verify/csiszar_defect.py   (exhibits the failure)
  verify/csiszar_repair.py   (the replacement identity)
  verify/deep_csiszar.py     (alpha-divergence sweep isolating alpha = 1)
Manuscript: lem:csiszar-representation, rem:csiszar-conditional-needed.
=============================================================================
"""

"""
Audit item 12: does the P-weighted chain rule for f-divergences force the
multiplicative Cauchy equation  g(uv) = u g(v) + v g(u)  ?

Chain rule as written in the manuscript:
  sum_{x,y} q_x q_{y|x} f( p_x p_{y|x} / (q_x q_{y|x}) )
    = sum_x q_x f(p_x/q_x)  +  sum_x p_x sum_y q_{y|x} f( p_{y|x} / q_{y|x} ).

Test 1: does g(t) = t log t satisfy the Cauchy equation?
Test 2: does g(t) = t log t satisfy the chain rule on random joints?
Test 3: does the chain rule IMPLY the Cauchy equation, i.e. is the derivation
        'transparent'?  Probe by checking whether the chain rule with
        DEGENERATE (product) joints already pins g, and whether the step needs
        extra structure.
"""
import numpy as np
from math import log

rng = np.random.default_rng(0)


def g(t):
    return t * log(t) if t > 0 else 0.0


print("=" * 76)
print("TEST 1: does g(t)=t log t satisfy g(uv) = u g(v) + v g(u)?")
print("=" * 76)
worst = 0.0
for _ in range(200000):
    u, v = rng.uniform(0.01, 10), rng.uniform(0.01, 10)
    lhs = g(u * v)
    rhs = u * g(v) + v * g(u)
    worst = max(worst, abs(lhs - rhs))
print(f"  max |g(uv) - u g(v) - v g(u)| over 200k pairs = {worst:.3e}")
assert worst < 1e-9
print("  YES -- t log t satisfies the Cauchy equation.")

print()
print("=" * 76)
print("TEST 2: does f = t log t satisfy the P-weighted chain rule?")
print("=" * 76)


def divergence(p, q, f):
    return float(sum(qi * f(pi / qi) for pi, qi in zip(p, q) if qi > 0))


worst = 0.0
for _ in range(50000):
    nx, ny = rng.integers(2, 4), rng.integers(2, 4)
    px = rng.dirichlet(np.ones(nx)); qx = rng.dirichlet(np.ones(nx))
    pyx = np.array([rng.dirichlet(np.ones(ny)) for _ in range(nx)])
    qyx = np.array([rng.dirichlet(np.ones(ny)) for _ in range(nx)])
    if qx.min() < 1e-6 or qyx.min() < 1e-6:
        continue
    lhs = 0.0
    for x in range(nx):
        for y in range(ny):
            P = px[x] * pyx[x][y]
            Q = qx[x] * qyx[x][y]
            lhs += Q * g(P / Q)
    rhs = divergence(px, qx, g)
    for x in range(nx):
        rhs += px[x] * divergence(pyx[x], qyx[x], g)
    worst = max(worst, abs(lhs - rhs))
print(f"  max |chain-rule defect| for f = t log t = {worst:.3e}")
assert worst < 1e-8
print("  YES -- the chain rule holds for t log t.")

print()
print("=" * 76)
print("TEST 3: does the NORMALIZED representative satisfy the Cauchy equation?")
print("=" * 76)


def gn(t):
    return t * log(t) - t + 1 if t > 0 else 1.0


bad = 0
mx = 0.0
for _ in range(100000):
    u, v = rng.uniform(0.01, 10), rng.uniform(0.01, 10)
    d = abs(gn(u * v) - (u * gn(v) + v * gn(u)))
    mx = max(mx, d)
    if d > 1e-9:
        bad += 1
print(f"  violations for t log t - t + 1: {bad}/100000, max defect {mx:.3f}")
print("  As the manuscript states, the NORMALIZED form does NOT satisfy it;")
print("  only t log t does.  That caveat in the text is correct.")

print()
print("=" * 76)
print("TEST 4: is the Cauchy equation DERIVABLE from the chain rule as written?")
print("=" * 76)
print("  Take the joint with independent structure: p_{y|x} = p_y, q_{y|x} = q_y")
print("  for all x.  Then the chain rule reads")
print("     D(p_x p_y || q_x q_y) = D(p_x||q_x) + D(p_y||q_y),")
print("  i.e. ADDITIVITY over products, not the pointwise Cauchy equation.")
print()
print("  Check: does additivity over product distributions alone force")
print("  g(uv) = u g(v) + v g(u) pointwise?  Additivity gives, for the")
print("  two-point case, a family of constraints indexed by distributions,")
print("  not the free two-variable identity.  Probe with a candidate that is")
print("  additive on products but not Cauchy:")


# f_alpha for Renyi-like: check whether some non-(t log t) f is additive
def try_f(f, trials=4000):
    w = 0.0
    for _ in range(trials):
        nx = ny = 2
        px = rng.dirichlet(np.ones(nx)); qx = rng.dirichlet(np.ones(nx))
        py = rng.dirichlet(np.ones(ny)); qy = rng.dirichlet(np.ones(ny))
        if min(qx.min(), qy.min()) < 1e-6:
            continue
        lhs = 0.0
        for x in range(nx):
            for y in range(ny):
                P, Q = px[x]*py[y], qx[x]*qy[y]
                lhs += Q * f(P/Q)
        rhs = divergence(px, qx, f) + divergence(py, qy, f)
        w = max(w, abs(lhs - rhs))
    return w


print(f"    f = t log t          : max product-additivity defect {try_f(g):.3e}")
print(f"    f = (t-1)^2 (chi^2)  : max product-additivity defect {try_f(lambda t:(t-1)**2):.3e}")
print(f"    f = |t-1| (TV)       : max product-additivity defect {try_f(lambda t:abs(t-1)):.3e}")
print()
print("  Only t log t is additive, consistent with the claim -- but the")
print("  DERIVATION of the pointwise Cauchy equation from the distributional")
print("  chain rule needs an argument (choose two-point distributions and vary")
print("  the ratios independently).  The manuscript asserts the step without")
print("  giving it.  AUDIT ITEM 12 IS CORRECT that the step is not transparent.")
