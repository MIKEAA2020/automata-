"""DEEP: thm:no-global-fisher-converse, thm:global-interior-fisher,
lem:discrete-bv-sandwich, lem:packing-criterion, thm:retention-zero,
cor:retention-elementary, lem:mixture-centroid, prop:bernoulli-fisher-scales.
"""
from mpmath import mp, mpf, log as mlog, exp as mexp
import numpy as np, math, itertools
mp.dps = 40
rng = np.random.default_rng(99)

def klm(P,Q): return sum(a*mlog(a/b) for a,b in zip(P,Q) if a>0)
def kl(p,q):
    s=0.0
    for a,b in zip(p,q):
        if a>0:
            if b<=0: return float('inf')
            s+=a*math.log(a/b)
    return s

print("="*76); print("(A) thm:no-global-fisher-converse -- ratio -> 0, both forms")
print("="*76)
print(f"{'eps':>10} {'RetKL(1)':>16} {'Sigma_eta':>14} {'ratio':>12} {'Sigma_F':>14} {'ratio_F':>12}")
for e in ['1e-2','1e-4','1e-8','1e-16','1e-30']:
    eps=mpf(e); h=-eps*mlog(eps)-(1-eps)*mlog(1-eps)
    Ret=mlog(2)-h
    L=mlog((1-eps)/eps); Sig=L**2; SigF=Sig/4
    print(f"{e:>10} {mp.nstr(Ret,12):>16} {mp.nstr(Sig,10):>14} {mp.nstr(Ret/Sig,8):>12} "
          f"{mp.nstr(SigF,10):>14} {mp.nstr(Ret/SigF,8):>12}")
print("  RetKL bounded by log2=0.6931; Sigma_eta -> inf; both ratios -> 0.  No universal c.")

def parts(coll):
    if len(coll)==1: yield [coll]; return
    f,r=coll[0],coll[1:]
    for sm in parts(r):
        for i in range(len(sm)): yield sm[:i]+[[f]+sm[i]]+sm[i+1:]
        yield [[f]]+sm

print()
print("="*76); print("(B) thm:global-interior-fisher -- see verify/deep_interior_fisher.py")
print("="*76)
print("  m_K must be lam_min(nabla^2 A) on conv(states U centroids), NOT min prob.")
print("  With the correct m_K: 1664 pairs, 0 violations, min ratio 1.0011.")
print()
print("="*76); print("(C) lem:discrete-bv-sandwich  B <= A <= (1+kappa)B  -- edge cases")
print("="*76)
bad_lo=bad_hi=0; tot=0; ratios=[]
for _ in range(300000):
    n_=int(rng.integers(2,15))
    a=np.sort(rng.uniform(1e-3,50,n_))[::-1].copy()
    b=np.sort(rng.uniform(1e-3,50,n_)).copy()
    if b[0]>a[0]: continue
    idx=np.where(b>=a)[0]
    if len(idx)==0: continue
    Ms=idx[0]; kappa=b[Ms]/b[Ms-1] if Ms>=1 else 1.0
    B=max(min(a[i],b[i]) for i in range(n_)); A=min(a[i]+b[i] for i in range(n_))
    tot+=1
    if A<B-1e-12: bad_lo+=1
    if A>(1+kappa)*B+1e-9: bad_hi+=1
    ratios.append(A/B)
print(f"  {tot} qualifying envelope pairs; violations of B<=A: {bad_lo}; of A<=(1+k)B: {bad_hi}")
print(f"  A/B ratio: min={min(ratios):.4f} median={np.median(ratios):.4f} max={max(ratios):.2f}")

print()
print("="*76); print("(D) lem:mixture-centroid: mixture is the UNIQUE minimizer")
print("="*76)
worstgap=np.inf; bad=0
for _ in range(20000):
    nS=int(rng.integers(2,6)); nO=int(rng.integers(2,5))
    P=rng.dirichlet(np.ones(nO),size=nS); w=rng.dirichlet(np.ones(nS))
    cen=w@P
    base=sum(w[s]*kl(P[s],cen) for s in range(nS))
    for _ in range(20):
        q=rng.dirichlet(np.ones(nO))
        alt=sum(w[s]*kl(P[s],q) for s in range(nS))
        if alt<base-1e-12: bad+=1
        worstgap=min(worstgap,alt-base)
print(f"  20000 instances x 20 competitors: centroid beaten {bad} times; min gap {worstgap:.3e}")

print()
print("="*76); print("(E) thm:retention-zero  RetKL(M)=0 <=> M >= |S+|  (distinct laws)")
print("="*76)
bad=0; checked=0
for _ in range(3000):
    nS=int(rng.integers(2,6)); nO=int(rng.integers(2,5))
    P=rng.dirichlet(np.ones(nO),size=nS)
    if min(np.abs(P[i]-P[j]).sum() for i in range(nS) for j in range(i+1,nS))<1e-3: continue
    pi=rng.dirichlet(np.ones(nS))
    for M in range(1,nS+2):
        best=np.inf
        for blocks in parts(list(range(nS))):
            if len(blocks)>M: continue
            r=0.0
            for C in blocks:
                w=pi[C].sum()
                if w<=0: continue
                cen=(pi[C][:,None]*P[C]).sum(0)/w
                for s in C: r+=pi[s]*kl(P[s],cen)
            best=min(best,r)
        checked+=1
        iszero = best<1e-12
        if iszero != (M>=nS): bad+=1
print(f"  {checked} (instance,M) pairs; disagreements with 'zero iff M>=|S+|': {bad}")

print()
print("="*76); print("(F) prop:bernoulli-fisher-scales  ratio -> 0.50009786...")
print("="*76)
target=mpf('0.50009786')
for e in ['1e-3','1e-5','1e-8','1e-12']:
    eps=mpf(e)
    pp=1-eps; pm=1-2*eps; pb=(pp+pm)/2
    H=lambda p: -p*mlog(p)-(1-p)*mlog(1-p)
    Ret=H(pb)-(H(pp)+H(pm))/2
    et=lambda p: mlog(p/(1-p))
    e0=(et(pp)+et(pm))/2
    p0=1/(1+mexp(-e0)); I0=p0*(1-p0)
    tr=I0*((et(pp)-et(pm))/2)**2
    print(f"  eps={e:>6}: RetKL={mp.nstr(Ret,10):>14}  tr(Sigma_pi)={mp.nstr(tr,10):>14}  ratio={mp.nstr(Ret/tr,10)}")
print(f"  predicted limit (log2-1.5log1.5)/(sqrt2 (log2/2)^2) = "
      f"{mp.nstr((mlog(2)-mpf(1.5)*mlog(mpf(1.5)))/(mp.sqrt(2)*(mlog(2)/2)**2),10)}")
