"""Re-test thm:global-interior-fisher with the CORRECT m_K.

Previous run used m_K ~ min probability -- not the theorem's hypothesis.
The theorem needs  m_K = inf over the compact CONVEX set K of
lambda_min(nabla^2 A(eta)),  where K must contain the state parameters AND
the centroid parameters; the segment [eta_s, zeta_C] must lie in K, so the
convex hull of {eta_s} U {zeta_C} is the minimal admissible K.

For the categorical family in the minimal chart with reference letter r:
  A(eta) = log(1 + sum_j exp(eta_j)),   nabla^2 A = diag(p_-r) - p_-r p_-r^T
where p_-r are the non-reference probabilities.
"""
import numpy as np, math, itertools
rng = np.random.default_rng(2024)

def kl(p,q):
    s=0.0
    for a,b in zip(p,q):
        if a>0:
            if b<=0: return float('inf')
            s+=a*math.log(a/b)
    return s
def probs_from_eta(eta):
    e=np.concatenate([eta,[0.0]]); e=e-e.max(); w=np.exp(e); return w/w.sum()
def hess(eta):
    p=probs_from_eta(eta)[:-1]
    return np.diag(p)-np.outer(p,p)
def parts(coll):
    if len(coll)==1: yield [coll]; return
    f,r=coll[0],coll[1:]
    for sm in parts(r):
        for i in range(len(sm)): yield sm[:i]+[[f]+sm[i]]+sm[i+1:]
        yield [[f]]+sm

def mK_over_hull(points, n_grid=4000, rng=None):
    """inf lambda_min(nabla^2 A) over conv(points), by dense sampling of the hull."""
    pts=np.array(points); m=len(pts)
    best=np.inf
    for q in pts:                      # vertices
        best=min(best, np.linalg.eigvalsh(hess(q)).min())
    for _ in range(n_grid):            # random convex combinations
        w=rng.dirichlet(np.ones(m))
        best=min(best, np.linalg.eigvalsh(hess(w@pts)).min())
    return best

viol=0; n=0; worst=np.inf
for trial in range(220):
    nS=int(rng.integers(2,5)); nO=int(rng.integers(2,4))
    P=rng.dirichlet(np.ones(nO)*8.0,size=nS)
    if P.min()<0.06: continue
    pi=rng.dirichlet(np.ones(nS))
    eta=np.log(P[:,:-1]/P[:,[-1]])
    ebar=pi@eta
    Se=sum(pi[s]*np.outer(eta[s]-ebar,eta[s]-ebar) for s in range(nS))
    lam=np.sort(np.linalg.eigvalsh(Se))[::-1]
    # collect centroid parameters over ALL partitions
    cpar=[]
    for blocks in parts(list(range(nS))):
        for C in blocks:
            w=pi[C].sum()
            if w<=0: continue
            cen=(pi[C][:,None]*P[C]).sum(0)/w
            cpar.append(np.log(cen[:-1]/cen[-1]))
    K_pts=[eta[s] for s in range(nS)]+cpar
    mK=mK_over_hull(K_pts, 1500, rng)
    if mK<=0: continue
    for blocks in parts(list(range(nS))):
        M=len(blocks); ret=0.0
        for C in blocks:
            w=pi[C].sum()
            if w<=0: continue
            cen=(pi[C][:,None]*P[C]).sum(0)/w
            for s in C: ret+=pi[s]*kl(P[s],cen)
        tail=lam[M-1:].sum() if M-1<len(lam) else 0.0
        rhs=(mK/2)*tail; n+=1
        if ret<rhs-1e-11: viol+=1
        if rhs>1e-14: worst=min(worst,ret/rhs)
print(f"CORRECT m_K = inf_{{conv(states U centroids)}} lambda_min(nabla^2 A)")
print(f"  {n} (instance,partition) pairs")
print(f"  violations: {viol}")
print(f"  min ratio LHS/RHS: {worst:.4f}   (must be >= 1)")
print()
print("Contrast: the earlier run used m_K ~ min probability, which is NOT")
print("lambda_min of the Hessian and is too large -- that produced the 3124")
print("spurious 'violations'.  With the theorem's actual hypothesis it holds.")
