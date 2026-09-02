"""Verify the proposed Item-11 repair, step by step.

MOVE 1 is the novel step: replace differentiation at beta=0 by a ONE-SIDED
limit, valid for any convex g (which has one-sided derivatives everywhere).
Test it on a convex g WITH A KINK exactly at the evaluation point u -- the
case where naive differentiation is illegal.
"""
from mpmath import mp, mpf, log as mlog
mp.dps = 50

print("="*78)
print("MOVE 1: one-sided limits.  Convex g with a KINK at u0=1.5, tested at u=u0.")
print("="*78)
u0 = mpf('1.5')
def gk(t):            # convex, g(1)=0, kink at u0>1
    return (t-1)**2 + max(mpf(0), 3*(t-u0))
gp_plus  = 2*(u0-1) + 3      # right derivative at u0
gp_minus = 2*(u0-1)          # left derivative at u0
print(f"  g'_+(u0) = {gp_plus},  g'_-(u0) = {gp_minus}   (genuine kink)")
print(f"  g is smooth at 1, so g'_+(1) = g'_-(1) = 0")

def sigma(v, b): return (1-v*b)/(1-b)

for v in [mpf('0.7'), mpf('1.4')]:
    u = u0
    side = '+' if v < 1 else '-'
    gpu = gp_plus if v < 1 else gp_minus
    gp1 = mpf(0)
    lhs_pred = gk(u*v) - gk(u) + u*(1-v)*gpu
    rhs_pred = u*gk(v) + u*(1-v)*gp1
    print(f"\n  v={v}  (expect one-sided derivative g'_{side})")
    print(f"    {'beta':>10} {'[LHS-g(u)]/beta':>22} {'RHS/beta':>22}")
    for e in [3,5,7,9]:
        b = mpf(10)**(-e)
        s = sigma(v,b)
        L = (b*gk(u*v) + (1-b)*gk(u*s) - gk(u))/b
        R = (u*b*gk(v) + u*(1-b)*gk(s))/b
        print(f"    {'1e-'+str(e):>10} {mp.nstr(L,14):>22} {mp.nstr(R,14):>22}")
    print(f"    predicted limits:  LHS -> {mp.nstr(lhs_pred,14)}   RHS -> {mp.nstr(rhs_pred,14)}")

print()
print("="*78)
print("MOVE 1 check: does the WRONG one-sided derivative give the wrong limit?")
print("="*78)
v = mpf('0.7')
wrong = gk(u0*v) - gk(u0) + u0*(1-v)*gp_minus   # using g'_- when v<1
right = gk(u0*v) - gk(u0) + u0*(1-v)*gp_plus
print(f"  with g'_+ (correct for v<1): {mp.nstr(right,14)}")
print(f"  with g'_- (incorrect)      : {mp.nstr(wrong,14)}")
print("  -> the side matters; the proposal's sign convention is the operative point")
