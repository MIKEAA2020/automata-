"""Verify thm:predictive-info:  RetKL(phi) = I(S;Z|K_phi) = I(S;Z) - I(K_phi;Z).

S = predictive state (weights pi), Z = emitted symbol, K_phi = block label.
RetKL(phi) = sum_s pi_s KL(P_s || Pbar_{phi(s)})  with mixture centroids.
"""
import numpy as np, itertools, math
rng = np.random.default_rng(0)

def H(p):
    p = np.asarray(p, float); p = p[p > 0]
    return float(-(p*np.log(p)).sum())

def check(nS, nO, rng):
    pi = rng.dirichlet(np.ones(nS))
    P  = rng.dirichlet(np.ones(nO), size=nS)          # P[s] = law of Z given S=s
    pz = pi @ P
    ISZ = H(pz) - sum(pi[s]*H(P[s]) for s in range(nS))
    worst = 0.0
    # all partitions of nS states
    def parts(coll):
        if len(coll) == 1: yield [coll]; return
        first, rest = coll[0], coll[1:]
        for sm in parts(rest):
            for i in range(len(sm)):
                yield sm[:i] + [[first]+sm[i]] + sm[i+1:]
            yield [[first]] + sm
    for blocks in parts(list(range(nS))):
        # RetKL(phi) with mixture centroids
        ret = 0.0
        for C in blocks:
            w = pi[C].sum()
            if w <= 0: continue
            cen = (pi[C][:,None]*P[C]).sum(0)/w
            for s in C:
                if pi[s] > 0:
                    ret += pi[s]*sum(P[s][j]*math.log(P[s][j]/cen[j])
                                     for j in range(nO) if P[s][j] > 0)
        # I(K;Z)
        IKZ = 0.0
        pk = np.array([pi[C].sum() for C in blocks])
        Pk = np.array([ (pi[C][:,None]*P[C]).sum(0)/max(pi[C].sum(),1e-300) for C in blocks])
        IKZ = H(pk @ Pk) - sum(pk[k]*H(Pk[k]) for k in range(len(blocks)))
        # I(S;Z|K) directly
        ISZgK = 0.0
        for C,wk in zip(blocks, pk):
            if wk <= 0: continue
            wsub = pi[C]/wk
            cen  = (wsub[:,None]*P[C]).sum(0)
            ISZgK += wk*(H(cen) - sum(wsub[i]*H(P[C][i]) for i in range(len(C))))
        worst = max(worst, abs(ret-(ISZ-IKZ)), abs(ret-ISZgK))
    return worst

w = 0.0
for nS in [2,3,4,5]:
    for nO in [2,3,4]:
        for _ in range(60):
            w = max(w, check(nS, nO, rng))
print(f"max |RetKL(phi) - (I(S;Z)-I(K;Z))| and |RetKL(phi) - I(S;Z|K)|  over all partitions: {w:.3e}")
print("=> predictive-information identity holds as an exact identity." if w < 1e-9 else "=> VIOLATION")
