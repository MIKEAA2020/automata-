from mpmath import mp, mpf, log as mlog, diff
mp.dps=40
# EXACT identity from the P-WEIGHTED chain rule with a NON-PRODUCT conditional:
#   X binary, Q_{Y|x}=q' both branches; P_{Y|x=1}=p', P_{Y|x=2}=q'.
#   =>  sum_j q'_j g(u t_j) = g(u) + u sum_j q'_j g(t_j),   t_j=p'_j/q'_j
def lhs_rhs(g,u,pp,qq):
    t=[a/b for a,b in zip(pp,qq)]
    L=sum(b*g(u*tj) for b,tj in zip(qq,t))
    R=g(u)+u*sum(b*g(tj) for b,tj in zip(qq,t))
    return L,R
gens={'fwd KL  t log t -t+1':lambda t:t*mlog(t)-t+1,
      'rev KL  -log t +t-1':lambda t:-mlog(t)+t-1,
      'chi^2   (t-1)^2     ':lambda t:(t-1)**2,
      'Hellinger (sqrt t-1)^2':lambda t:(t**mpf('0.5')-1)**2}
u=mpf('2.3'); qq=[mpf('0.3'),mpf('0.7')]; pp=[mpf('0.55'),mpf('0.45')]
print("EXACT chain-rule identity  sum_j q'_j g(u t_j) = g(u) + u sum_j q'_j g(t_j)")
for n,g in gens.items():
    L,R=lhs_rhs(g,u,pp,qq); print(f"  {n}: LHS={float(L):+.10f} RHS={float(R):+.10f} defect={float(L-R):+.3e}")

print("\nFirst-order-in-delta consequence:  g(uv) = g(u) + u g(v) - u(1-v) g'(u),  g'(1)=0")
for n,g in gens.items():
    gp=lambda t: diff(g,t)
    if abs(gp(mpf(1)))>mpf('1e-25'):
        a=gp(mpf(1)); gn=(lambda g,a: (lambda t: g(t)-a*(t-1)))(g,a)
    else: gn=g
    gpn=lambda t: diff(gn,t)
    u2,v2=mpf('2.0'),mpf('3.0')
    L=gn(u2*v2); R=gn(u2)+u2*gn(v2)-u2*(1-v2)*gpn(u2)
    print(f"  {n}: g(uv)={float(L):+.8f}  RHS={float(R):+.8f}  defect={float(L-R):+.6f}")

print("\nODE solution check: symmetry F(u,v)=F(v,u) => u g'(u)-g(u)=c(u-1) => g=c(t log t -t+1)")
for n,g in gens.items():
    gp0=diff(g,mpf(1)); gn=(lambda g,a:(lambda t:g(t)-a*(t-1)))(g,gp0)
    vals=[(u2*diff(gn,u2)-gn(u2))/(u2-1) for u2 in [mpf('1.7'),mpf('2.9'),mpf('4.3')]]
    print(f"  {n}: (u g'-g)/(u-1) at u=1.7,2.9,4.3 -> "+", ".join(f"{float(x):+.6f}" for x in vals)
          +("   CONSTANT (=> forward KL)" if max(vals)-min(vals)<mpf('1e-20') else "   NOT constant (=> excluded)"))
