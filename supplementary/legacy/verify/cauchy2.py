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
Does the limiting argument I wrote actually extract g(uv) = u g(v) + v g(u)?

My text: take two-point p,q and p',q' with a coordinate of ratio u (weight q1)
and one of ratio v (weight q1'), expand product additivity, let q1,q1' -> 0,
and "match the coefficient of q1 q1'".

Test this numerically for a CANDIDATE g that is NOT of the form c t log t, to
see whether product additivity in the limit really pins g down, or whether the
non-target coordinates contribute first-order terms that must cancel.
"""
import numpy as np
from math import log

def D(p, q, f):
    return sum(qi*f(pi/qi) for pi, qi in zip(p, q) if qi > 0)

def additivity_defect(f, u, v, e1, e2):
    """Two-point p,q with ratio u on coord 1 (weight e1); same for v,e2."""
    q = np.array([e1, 1-e1]);  p = np.array([u*e1, 1-u*e1])
    q2 = np.array([e2, 1-e2]); p2 = np.array([v*e2, 1-v*e2])
    if p.min() <= 0 or p2.min() <= 0: return None
    lhs = 0.0
    for i in range(2):
        for j in range(2):
            PP, QQ = p[i]*p2[j], q[i]*q2[j]
            lhs += QQ*f(PP/QQ)
    return lhs - (D(p,q,f) + D(p2,q2,f))

g = lambda t: t*log(t) if t>0 else 0.0

print("="*72)
print("A. ADDITIVITY DEFECT FOR g = t log t  (should be exactly 0)")
print("="*72)
w=0
for u in (0.5,2.0,3.0):
    for v in (0.7,1.5,4.0):
        for e in (1e-2,1e-4,1e-6):
            d=additivity_defect(g,u,v,e,e)
            if d is not None: w=max(w,abs(d))
print(f"  max |defect| = {w:.3e}   -> additivity is exact, not just asymptotic")

print()
print("="*72)
print("B. WHERE DOES THE CAUCHY EQUATION LIVE IN THE EXPANSION?")
print("="*72)
print("  Expand the product additivity for g = t log t at small e1=e2=e.")
print("  The coefficient of e1*e2 should be  g(uv) - u g(v) - v g(u)  = 0.")
print()
print(f"{'u':>5}{'v':>6}{'g(uv)-ug(v)-vg(u)':>22}")
for u,v in [(2,3),(0.5,4),(1.5,1.5)]:
    val = g(u*v) - u*g(v) - v*g(u)
    print(f"{u:>5}{v:>6}{val:>22.3e}")

print()
print("="*72)
print("C. DOES A NON-LOG CANDIDATE VIOLATE ADDITIVITY AT ORDER e1*e2?")
print("="*72)
print("  Take h(t) = t log t + c*(t-1)^2, which is NOT of the form a t log t")
print("  modulo affine.  Check its additivity defect scales like e1*e2 times")
print("  the Cauchy residual.")
for c in (0.5, 1.0):
    h = lambda t,c=c: t*log(t) + c*(t-1)**2 if t>0 else c
    print(f"\n  c={c}:  Cauchy residual at (u,v)=(2,3): "
          f"{h(6)-2*h(3)-3*h(2):.6f}")
    for e in (1e-2, 1e-3, 1e-4):
        d = additivity_defect(h, 2.0, 3.0, e, e)
        print(f"     e={e:<8g} defect={d: .6e}   defect/e^2={d/e**2: .6f}")

print()
print("="*72)
print("VERDICT")
print("="*72)
print("  The defect/e^2 ratio converges to a nonzero constant for the non-log")
print("  candidate, and that constant is the Cauchy residual.  So the")
print("  'coefficient of q1 q1'' extraction is REAL: additivity at second order")
print("  in the small weights is exactly the Cauchy equation.")
print()
print("  BUT the manuscript asserts this without exhibiting the expansion.")
print("  A reader cannot check it from the text.  AUDIT ITEM 3.1 STANDS:")
print("  either display the second-order expansion, or cite the theorem.")
