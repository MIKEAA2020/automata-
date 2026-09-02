import numpy as np, itertools, math
rng=np.random.default_rng(0)

def kl(p,q):
    s=0.0
    for a,b in zip(p,q):
        if a>0:
            if b<=0: return float('inf')
            s+=a*math.log(a/b)
    return s

# CLAIM A: for p,q in simplex,  KL(p||q) >= ||p-q||_2^2   (constant 1, not 1/2)
# and the intermediate step  (1/2)||p-q||_1^2 >= ||p-q||_2^2.
worst_kl=float('inf'); worst_step=float('inf'); n_bad=0
for trial in range(400000):
    k=rng.integers(2,7)
    p=rng.dirichlet(np.ones(k)*rng.choice([0.1,0.3,1.0,3.0]))
    q=rng.dirichlet(np.ones(k)*rng.choice([0.1,0.3,1.0,3.0]))
    d=p-q
    l1=np.abs(d).sum(); l2sq=(d**2).sum()
    step = 0.5*l1**2 - l2sq          # must be >= 0
    if step < -1e-15: n_bad+=1
    worst_step=min(worst_step,step)
    K=kl(p,q)
    if np.isfinite(K) and l2sq>1e-18:
        worst_kl=min(worst_kl, K/l2sq)   # must be >= 1
print("CLAIM A  min over 400k pairs of  (1/2)||d||_1^2 - ||d||_2^2 =", worst_step, " violations:",n_bad)
print("CLAIM A  min over 400k pairs of  KL(p||q)/||p-q||_2^2      =", worst_kl, " (must be >= 1)")

# CLAIM B: sharpness. p_pm = (1/2 +- eps, 1/2 -+ eps), M=1.
print("\nCLAIM B  sharpness of constant 1:")
for eps in [1e-1,1e-2,1e-3,1e-4]:
    pp=np.array([0.5+eps,0.5-eps]); pm=np.array([0.5-eps,0.5+eps]); pbar=np.array([0.5,0.5])
    Ret=0.5*kl(pp,pbar)+0.5*kl(pm,pbar)
    Sig=0.5*np.outer(pp-pbar,pp-pbar)+0.5*np.outer(pm-pbar,pm-pbar)
    tr=np.trace(Sig)
    print(f"   eps={eps:8.0e}  RetKL(1)={Ret:.10e}  tr(Sigma_p)={tr:.10e}  ratio={Ret/tr:.10f}")
