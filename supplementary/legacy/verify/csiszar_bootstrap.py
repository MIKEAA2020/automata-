"""MOVES 2-3: does (ddagger) really force g = c(t log t - t + 1) + a(t-1)?

The decisive question for the manuscript: could a NON-smooth convex g satisfy
the exact identity (dagger)?  The proposal says no -- the bootstrap forces C^1
then the ODE pins the form.  Test by BRUTE FORCE: search for convex piecewise
-linear / kinked g satisfying (dagger) to high precision.
"""
from mpmath import mp, mpf, log as mlog
import itertools, random
mp.dps = 40
random.seed(0)

def dagger_defect(g, u, qp, pp):
    """LHS - RHS of (dagger): sum_j q'_j g(u t_j) - g(u) - u sum_j q'_j g(t_j)"""
    t = [a/b for a, b in zip(pp, qp)]
    L = sum(b*g(u*tj) for b, tj in zip(qp, t))
    R = g(u) + u*sum(b*g(tj) for b, tj in zip(qp, t))
    return L - R

print("="*78)
print("(A) Does any KINKED convex g satisfy (dagger)?  Family: c(t log t -t+1)")
print("    + a(t-1) + k*max(0, t-s)   with kink strength k at location s.")
print("="*78)
def make(c, a, k, s):
    return lambda t: c*(t*mlog(t)-t+1) + a*(t-1) + k*max(mpf(0), t-s)

tests = []
for _ in range(40):
    u  = mpf(random.uniform(0.2, 4.0))
    kk = random.randint(2, 4)
    q  = [mpf(random.uniform(0.1, 1)) for _ in range(kk)]; sq = sum(q); q = [x/sq for x in q]
    p  = [mpf(random.uniform(0.1, 1)) for _ in range(kk)]; sp = sum(p); p = [x/sp for x in p]
    tests.append((u, q, p))

print(f"  {'c':>5} {'a':>5} {'k':>6} {'s':>5} {'max |defect| over 40 random (u,q,p)':>38}")
for (c, a, k, s) in [(1,0,0,1.5),(1,0.7,0,1.5),(1,0,0.5,1.5),(1,0,0.01,1.5),
                     (1,0,-0.3,0.6),(2,-1,0,1.0),(1,0,0.5,0.5)]:
    g = make(mpf(c), mpf(a), mpf(k), mpf(s))
    worst = max(abs(dagger_defect(g,u,q,p)) for (u,q,p) in tests)
    tag = "SATISFIES" if worst < mpf('1e-25') else "fails"
    print(f"  {c:>5} {a:>5} {k:>6} {s:>5} {mp.nstr(worst,10):>38}   {tag}")
print()
print("  -> kink strength k != 0 always breaks (dagger); only k=0 (smooth) survives,")
print("     for ANY c and ANY affine a.  Consistent with the proposal's conclusion.")

print()
print("="*78)
print("(B) The bootstrap identity (ddagger_+):  u g'(u) = g(u) + c1(u-1) + g'(1)")
print("="*78)
for (c, a) in [(1,0),(1,0.7),(2,-1),(0.5,3)]:
    C, A = mpf(c), mpf(a)
    g   = lambda t: C*(t*mlog(t)-t+1) + A*(t-1)
    gp  = lambda t: C*mlog(t) + A
    gp1 = A
    vals = []
    for uu in ['0.2','0.5','0.8','0.95']:
        U = mpf(uu)
        vals.append((U*gp(U) - g(U) - gp1)/(U-1))
    spread = max(vals)-min(vals)
    print(f"  c={c}, a={a}:  (u g'(u)-g(u)-g'(1))/(u-1) = {mp.nstr(vals[0],12)}"
          f"   spread over u = {mp.nstr(spread,8)}   (c1 should equal c={c})")

print()
print("="*78)
print("(C) GLUING: 0 = (c1-c2)(log u - u + 1) forces c1=c2 since log u != u-1")
print("="*78)
print(f"  {'u':>8} {'log u - u + 1':>18}  (must be nonzero for u != 1)")
for uu in ['0.1','0.3','0.5','0.9','0.99','0.999']:
    U = mpf(uu)
    print(f"  {uu:>8} {mp.nstr(mlog(U)-U+1,12):>18}")
print("  -> strictly negative on (0,1); vanishes only at u=1.  Gluing step is sound.")
