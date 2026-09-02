"""DEEP: lem:csiszar-representation repaired proof.

Earlier: checked (dagger) on ONE (u,q',p') triple for 4 generators.
Now: (i) (dagger) over thousands of random triples for a family of generators;
     (ii) the derived (ddagger) identity;
     (iii) the symmetry->ODE step, i.e. (u g'(u)-g(u))/(u-1) constant iff fwd KL;
     (iv) confirm product-additivity does NOT separate fwd/rev KL (the flaw);
     (v) alpha-divergence family swept: only alpha->1 (fwd KL) survives.
"""
from mpmath import mp, mpf, log as mlog, diff
import numpy as np
mp.dps = 40
rng = np.random.default_rng(3)

# normalized generators g with g(1)=0
G = {
 'fwd KL   t log t - t + 1': lambda t: t*mlog(t)-t+1,
 'rev KL   -log t + t - 1' : lambda t: -mlog(t)+t-1,
 'chi^2    (t-1)^2'        : lambda t: (t-1)**2,
 'Hellinger (sqrt t -1)^2' : lambda t: (mp.sqrt(t)-1)**2,
 'JS-like  t log t -(1+t)log((1+t)/2)': lambda t: t*mlog(t)-(1+t)*mlog((1+t)/2),
 'TV       |t-1|/2'        : lambda t: abs(t-1)/2,
}

print("="*76)
print("(i) EXACT conditional chain-rule identity (dagger):")
print("    sum_j q'_j g(u t_j)  ==  g(u) + u sum_j q'_j g(t_j)")
print("="*76)
for name,g in G.items():
    worst = mpf(0)
    for _ in range(400):
        u = mpf(float(rng.uniform(0.15,6.0)))
        k = int(rng.integers(2,6))
        q = rng.dirichlet(np.ones(k)); p = rng.dirichlet(np.ones(k))
        Q=[mpf(float(x)) for x in q]; P=[mpf(float(x)) for x in p]
        sQ=sum(Q); sP=sum(P); Q=[x/sQ for x in Q]; P=[x/sP for x in P]
        T=[a/b for a,b in zip(P,Q)]
        L=sum(b*g(u*t) for b,t in zip(Q,T))
        R=g(u)+u*sum(b*g(t) for b,t in zip(Q,T))
        worst=max(worst, abs(L-R))
    tag = "SATISFIES  (candidate)" if worst<mpf('1e-25') else "FAILS      (excluded)"
    print(f"  {name:<40} max|LHS-RHS| = {mp.nstr(worst,8):>12}   {tag}")

print()
print("="*76)
print("(ii) PRODUCT additivity alone (the flawed route) -- does NOT separate")
print("="*76)
for name,g in G.items():
    worst=mpf(0)
    for _ in range(200):
        k1=int(rng.integers(2,5)); k2=int(rng.integers(2,5))
        p1=rng.dirichlet(np.ones(k1)); q1=rng.dirichlet(np.ones(k1))
        p2=rng.dirichlet(np.ones(k2)); q2=rng.dirichlet(np.ones(k2))
        f=lambda P,Q: sum(mpf(float(b))*g(mpf(float(a))/mpf(float(b))) for a,b in zip(P,Q))
        P=np.outer(p1,p2).ravel(); Q=np.outer(q1,q2).ravel()
        worst=max(worst, abs(f(P,Q)-f(p1,q1)-f(p2,q2)))
    # tolerance must reflect float->mpf input conversion (~1e-16), not mp.dps
    tag="ADDITIVE (not excluded!)" if worst<mpf('1e-12') else "not additive"
    print(f"  {name:<40} max defect = {mp.nstr(worst,8):>12}   {tag}")
print("  -> fwd KL AND rev KL are both product-additive: the old proof could")
print("     not have selected the logarithm.  The conditional form is required.")

print()
print("="*76)
print("(iii) SYMMETRY -> ODE:  (u g'(u) - g(u))/(u-1) constant  <=>  fwd KL")
print("="*76)
for name,g in G.items():
    if 'TV' in name: continue     # not differentiable at 1
    gp0=diff(g,mpf(1))
    gn=(lambda g,a:(lambda t: g(t)-a*(t-1)))(g,gp0)
    vals=[]
    for u in ['1.3','2.1','3.7','5.9','9.4']:
        uu=mpf(u)
        vals.append((uu*diff(gn,uu)-gn(uu))/(uu-1))
    spread=max(vals)-min(vals)
    tag="CONSTANT => c(t log t - t + 1)" if spread<mpf('1e-25') else "not constant => excluded"
    print(f"  {name:<40} spread={mp.nstr(spread,8):>12}   {tag}")

print()
print("="*76)
print("(iv) alpha-divergence sweep: only alpha -> 1 satisfies (dagger)")
print("="*76)
def g_alpha(a):
    a=mpf(a)
    if abs(a-1)<mpf('1e-30'): return lambda t: t*mlog(t)-t+1
    if abs(a)<mpf('1e-30'):   return lambda t: -mlog(t)+t-1
    return lambda t: (t**a - 1 - a*(t-1))/(a*(a-1))
u=mpf('2.3'); Q=[mpf('0.3'),mpf('0.7')]; P=[mpf('0.55'),mpf('0.45')]
T=[a/b for a,b in zip(P,Q)]
print(f"  {'alpha':>8} {'|LHS-RHS| of (dagger)':>26}")
for a in ['-1.0','0.0','0.5','0.9','0.99','1.0','1.01','1.5','2.0','3.0']:
    g=g_alpha(a)
    L=sum(b*g(u*t) for b,t in zip(Q,T)); R=g(u)+u*sum(b*g(t) for b,t in zip(Q,T))
    print(f"  {a:>8} {mp.nstr(abs(L-R),12):>26}")
print("  -> vanishes exactly at alpha=1 (forward KL); nonzero elsewhere.")
