"""The decisive test of MOVE 3: a two-branch generator with c1 != c2.

If gluing were unnecessary, a g that is c1(t log t -t+1)+a(t-1) on (0,1] and
c2(t log t -t+1)+a(t-1) on [1,inf) with c1 != c2 would satisfy (dagger).
The proposal says it CANNOT.  Test directly.

Note such a g IS convex when c1,c2 > 0 and continuous at 1 with matching
one-sided derivatives (both equal a), so it is a genuine C^1 convex candidate
that only the GLUING step excludes.
"""
from mpmath import mp, mpf, log as mlog
import random
mp.dps = 40
random.seed(1)

def two_branch(c1, c2, a):
    def g(t):
        c = c1 if t <= 1 else c2
        return c*(t*mlog(t)-t+1) + a*(t-1)
    return g

def dagger_defect(g, u, qp, pp):
    t = [x/y for x, y in zip(pp, qp)]
    L = sum(y*g(u*tj) for y, tj in zip(qp, t))
    R = g(u) + u*sum(y*g(tj) for y, tj in zip(qp, t))
    return L - R

# verify the candidate is C^1 and convex
print("Two-branch candidate: c1 on (0,1], c2 on [1,inf), affine a.")
c1, c2, a = mpf('1.0'), mpf('2.0'), mpf('0.3')
g = two_branch(c1, c2, a)
h = mpf('1e-20')
dl = (g(1)-g(1-h))/h
dr = (g(1+h)-g(1))/h
print(f"  continuity at 1: g(1)={mp.nstr(g(mpf(1)),8)}  (should be 0)")
print(f"  left derivative at 1  = {mp.nstr(dl,10)}")
print(f"  right derivative at 1 = {mp.nstr(dr,10)}   (both should be a={a}: C^1)")

print()
print("Now test (dagger) on random instances:")
worst = mpf(0); nviol = 0
for _ in range(300):
    u = mpf(random.uniform(0.15, 5.0))
    k = random.randint(2,4)
    q = [mpf(random.uniform(0.1,1)) for _ in range(k)]; s=sum(q); q=[x/s for x in q]
    p = [mpf(random.uniform(0.1,1)) for _ in range(k)]; s=sum(p); p=[x/s for x in p]
    d = abs(dagger_defect(g,u,q,p))
    worst = max(worst,d)
    if d > mpf('1e-25'): nviol += 1
print(f"  c1={c1}, c2={c2}: max |defect| = {mp.nstr(worst,12)}   violations {nviol}/300")

print()
print("Sweep c2 with c1 fixed at 1:")
print(f"  {'c2':>6} {'max |defect|':>20}")
for x in ['0.5','0.9','0.99','1.0','1.01','1.5','3.0']:
    g2 = two_branch(mpf(1), mpf(x), a)
    w = max(abs(dagger_defect(g2,mpf(random.uniform(0.15,5)),
            [mpf('0.4'),mpf('0.6')],[mpf('0.7'),mpf('0.3')])) for _ in range(50))
    print(f"  {x:>6} {mp.nstr(w,12):>20}")
print()
print("=> defect vanishes ONLY at c2=c1.  The gluing step is genuinely needed")
print("   and genuinely works: two-branch C^1 convex candidates are excluded.")

print()
print("Explicit check of the gluing identity  0 = (c1-c2)(log u - u + 1):")
c1x, c2x = mpf(1), mpf(2)
for uu in ['0.2','0.5','0.8']:
    U = mpf(uu); V = 1/U
    g3 = two_branch(c1x, c2x, a)
    # (ddagger) with minus sign, u<1, v=1/u>1, uv=1 so g(uv)=0
    gpm_u = c1x*mlog(U) + a          # g'_-(u) for u<1 (smooth there)
    gpm_1 = a                        # g'_-(1)
    lhs = mpf(0) - g3(U) + U*(1-V)*gpm_u
    rhs = U*g3(V) + U*(1-V)*gpm_1
    pred = (c1x-c2x)*(mlog(U)-U+1)
    print(f"  u={uu}: LHS-RHS = {mp.nstr(lhs-rhs,12)}   -(c1-c2)(log u-u+1) = {mp.nstr(-pred,12)}")
