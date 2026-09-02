import numpy as np, math
from mpmath import mp, mpf, log as mlog
mp.dps=50

def Ediv(p,q,g):
    return sum(qi*g(mpf(pi)/mpf(qi)) for pi,qi in zip(p,q))

def defect(g,u,v,eps):
    e=mpf(eps)
    q=[e,1-e]; p=[u*e,1-u*e]
    q2=[e,1-e]; p2=[v*e,1-v*e]
    P=[a*b for a in p for b in p2]; Q=[a*b for a in q for b in q2]
    return Ediv(P,Q,g)-Ediv(p,q,g)-Ediv(p2,q2,g)

gs={'forward KL  g=t log t':lambda t:t*mlog(t),
    'reverse KL  g=-log t':lambda t:-mlog(t),
    'chi^2       g=(t-1)^2':lambda t:(t-1)**2}
u,v=mpf('2.0'),mpf('3.0')
print("Product-additivity defect Delta(eps), and manuscript's claimed eps^2 coefficient")
print("claimed coeff = g(uv) - u g(v) - v g(u)\n")
for name,g in gs.items():
    claimed=g(u*v)-u*g(v)-v*g(u)
    print(f"{name}:  claimed eps^2 coeff = {float(claimed):+.6f}")
    for eps in ['1e-3','1e-4','1e-5']:
        D=defect(g,u,v,mpf(eps))
        print(f"      eps={eps}:  Delta={float(D):+.6e}   Delta/eps^2={float(D/mpf(eps)**2):+.8f}")
    print()

# correct eps^2 coefficient derived by hand:
# D2 = g(uv)-g(u)-g(v) + u(1-v)g'(u) + v(1-u)g'(v) + g''(1)(1-u)(1-v) + g'(1)[(1-u)(1-v)-(1-u)-(1-v)]
def d2(g,gp,gpp1,gp1,u,v):
    return (g(u*v)-g(u)-g(v)+u*(1-v)*gp(u)+v*(1-u)*gp(v)
            +gpp1*(1-u)*(1-v)+gp1*((1-u)*(1-v)-(1-u)-(1-v)))
print("Correct eps^2 coefficient (derived):")
data=[('forward KL',lambda t:t*mlog(t),lambda t:mlog(t)+1,mpf(1),mpf(1)),
      ('reverse KL',lambda t:-mlog(t),lambda t:-1/t,mpf(1),mpf(-1)),
      ('chi^2     ',lambda t:(t-1)**2,lambda t:2*(t-1),mpf(2),mpf(0))]
for name,g,gp,gpp1,gp1 in data:
    print(f"  {name}: D2 = {float(d2(g,gp,gpp1,gp1,u,v)):+.10f}")
