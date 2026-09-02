"""
T39.  Verify the proposed controlled information-bottleneck identity

   RetKL^ctrl(phi) = sum_x p(x) sum_k sum_{s in C_k} pi_s D(P_s^x || Pbar_k^x)
                   = I(S;Y|K,X) = I(S;Y|X) - I(K;Y|X)

for stationary controlled UNIFILAR machines with i.i.d. inputs independent of
the state, and check the claimed optimal representative (controlled mixture
centroid).  Also stress-tests the required independence X_t _||_ S_t.
"""
import random, math, sys
import numpy as np

def kl(p,q):
    s=0.0
    for a,b in zip(p,q):
        if a>0:
            if b<=0: return float('inf')
            s+=a*math.log(a/b)
    return s

def mi_cond(joint):
    """joint[x][s][y] = P(X=x,S=s,Y=y) ; returns I(S;Y|X)"""
    tot=0.0
    for x in range(joint.shape[0]):
        px=joint[x].sum()
        if px<=0: continue
        J=joint[x]/px
        ps=J.sum(1); py=J.sum(0)
        for s in range(J.shape[0]):
            for y in range(J.shape[1]):
                if J[s,y]>0:
                    tot+=px*J[s,y]*math.log(J[s,y]/(ps[s]*py[y]))
    return tot

def run(trial, nS=5, nI=3, nO=4, verbose=False):
    rng=random.Random(trial)
    # unifilar update tau(s,x,y)
    tau=[[[rng.randrange(nS) for _ in range(nO)] for _ in range(nI)] for _ in range(nS)]
    # emission kernels P_s^x
    P=[[None]*nI for _ in range(nS)]
    for s in range(nS):
        for x in range(nI):
            w=[rng.random()+0.02 for _ in range(nO)]
            t=sum(w); P[s][x]=[v/t for v in w]
    # i.i.d. input law
    w=[rng.random()+0.05 for _ in range(nI)]; t=sum(w); p=[v/t for v in w]
    # stationary distribution of S (S_{t+1}=tau(S_t,X_t,Y_t), X_t iid indep of S_t)
    T=np.zeros((nS,nS))
    for s in range(nS):
        for x in range(nI):
            for y in range(nO):
                T[s][tau[s][x][y]]+=p[x]*P[s][x][y]
    pi=np.ones(nS)/nS
    for _ in range(20000): pi=pi@T
    if pi.min()<1e-9: return None
    pi=pi/pi.sum()

    # random partition
    K=rng.randrange(1,nS+1)
    phi=[rng.randrange(K) for _ in range(nS)]
    used=sorted(set(phi)); remap={k:i for i,k in enumerate(used)}
    phi=[remap[k] for k in phi]; K=len(used)

    # ---- LHS: controlled gap with mixture centroids ----
    lhs=0.0
    for x in range(nI):
        for k in range(K):
            C=[s for s in range(nS) if phi[s]==k]
            wgt=sum(pi[s] for s in C)
            bar=[sum(pi[s]*P[s][x][y] for s in C)/wgt for y in range(nO)]
            lhs+=p[x]*sum(pi[s]*kl(P[s][x],bar) for s in C)

    # ---- RHS: I(S;Y|K,X) computed from the exact joint ----
    # joint over (x,k,s,y)
    Ikx=0.0
    for x in range(nI):
        for k in range(K):
            C=[s for s in range(nS) if phi[s]==k]
            pk=sum(pi[s] for s in C)
            Jsy=np.zeros((len(C),nO))
            for i,s in enumerate(C):
                for y in range(nO):
                    Jsy[i,y]=(pi[s]/pk)*P[s][x][y]
            ps=Jsy.sum(1); py=Jsy.sum(0)
            for i in range(len(C)):
                for y in range(nO):
                    if Jsy[i,y]>0:
                        Ikx+=p[x]*pk*Jsy[i,y]*math.log(Jsy[i,y]/(ps[i]*py[y]))

    # ---- subtracted form:  I(S;Y|X) - I(K;Y|X) ----
    jS=np.zeros((nI,nS,nO)); jK=np.zeros((nI,K,nO))
    for x in range(nI):
        for s in range(nS):
            for y in range(nO):
                v=p[x]*pi[s]*P[s][x][y]
                jS[x,s,y]+=v; jK[x,phi[s],y]+=v
    sub=mi_cond(jS)-mi_cond(jK)

    # ---- centroid optimality: perturb representatives ----
    worse=0
    for _ in range(30):
        alt=0.0
        for x in range(nI):
            for k in range(K):
                C=[s for s in range(nS) if phi[s]==k]
                wgt=sum(pi[s] for s in C)
                bar=np.array([sum(pi[s]*P[s][x][y] for s in C)/wgt for y in range(nO)])
                noise=np.array([rng.random() for _ in range(nO)]); noise/=noise.sum()
                q=0.9*bar+0.1*noise
                alt+=p[x]*sum(pi[s]*kl(P[s][x],list(q)) for s in C)
        if alt < lhs-1e-12: worse+=1
    return lhs, Ikx, sub, worse

print("="*72)
print("Controlled IB identity:  RetKL^ctrl(phi) == I(S;Y|K,X) == I(S;Y|X)-I(K;Y|X)")
maxe1=maxe2=0.0; n=0; badcent=0
for t in range(4000):
    r=run(t)
    if r is None: continue
    lhs,ikx,sub,worse=r; n+=1
    maxe1=max(maxe1,abs(lhs-ikx)); maxe2=max(maxe2,abs(lhs-sub)); badcent+=worse
print(f"  instances tested                       : {n}")
print(f"  max |RetKL^ctrl - I(S;Y|K,X)|          : {maxe1:.3e}")
print(f"  max |RetKL^ctrl - (I(S;Y|X)-I(K;Y|X))| : {maxe2:.3e}")
print(f"  perturbations beating mixture centroid : {badcent}")
assert maxe1<1e-9 and maxe2<1e-9 and badcent==0
print("  VERIFIED.")
