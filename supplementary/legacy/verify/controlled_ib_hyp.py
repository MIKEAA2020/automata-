"""
T39.  Is the independence hypothesis in thm:controlled-ib load-bearing?

The proof uses  P(S_t=s | K_t=k, X_t=x) = pi_s / pi(C_k)  for s in C_k,
justified by "under input independence".  Test what happens when the input
process is stationary but CORRELATED with the state (allowed by
def:unifilar-machine, which only requires 'a stationary ergodic input
process').  Also verify cor:controlled-elementary.
"""
import random, math
import numpy as np

def kl(p,q):
    t=0.0
    for a,b in zip(p,q):
        if a>0:
            if b<=0: return float('inf')
            t+=a*math.log(a/b)
    return t

def mi_cond(J):
    tot=0.0
    for x in range(J.shape[0]):
        px=J[x].sum()
        if px<=0: continue
        A=J[x]/px; ps=A.sum(1); py=A.sum(0)
        for s in range(A.shape[0]):
            for y in range(A.shape[1]):
                if A[s,y]>0: tot+=px*A[s,y]*math.log(A[s,y]/(ps[s]*py[y]))
    return tot

print("="*72)
print("(1) INPUT CORRELATED WITH STATE:  does the identity survive?")
print("="*72)
rng=random.Random(77)
maxdev=0.0; n=0; worst=None
for trial in range(20000):
    nS=rng.randrange(2,5); nI=2; nO=rng.randrange(2,4)
    # joint stationary law of (S,X) that is NOT product
    W=np.array([[rng.random()+.05 for _ in range(nI)] for _ in range(nS)])
    W/=W.sum()
    piS=W.sum(1)
    P=[[None]*nI for _ in range(nS)]
    for s in range(nS):
        for x in range(nI):
            w=[rng.random()+.02 for _ in range(nO)]; t=sum(w); P[s][x]=[v/t for v in w]
    K=rng.randrange(1,nS+1)
    phi=[rng.randrange(K) for _ in range(nS)]
    used=sorted(set(phi)); rm={k:i for i,k in enumerate(used)}
    phi=[rm[k] for k in phi]; K=len(used)
    # "RetKL^ctrl" as literally DEFINED (uses pi_s and p(x) separately)
    px=W.sum(0)
    lhs=0.0
    for x in range(nI):
        for k in range(K):
            C=[s for s in range(nS) if phi[s]==k]
            w=sum(piS[s] for s in C)
            bar=[sum(piS[s]*P[s][x][y] for s in C)/w for y in range(nO)]
            lhs+=px[x]*sum(piS[s]*kl(P[s][x],bar) for s in C)
    # true I(S;Y|K,X) under the CORRELATED joint
    jS=np.zeros((nI,nS,nO)); jK=np.zeros((nI,K,nO))
    for x in range(nI):
        for s in range(nS):
            for y in range(nO):
                v=W[s,x]*P[s][x][y]
                jS[x,s,y]+=v; jK[x,phi[s],y]+=v
    rhs=mi_cond(jS)-mi_cond(jK)
    n+=1
    d=abs(lhs-rhs)
    if d>maxdev: maxdev=d; worst=(nS,nI,nO,phi,lhs,rhs)
print(f"  instances                                : {n}")
print(f"  max |RetKL^ctrl(def) - (I(S;Y|X)-I(K;Y|X))| : {maxdev:.6f}")
if maxdev>1e-6:
    nS,nI,nO,phi,l,r=worst
    print(f"  worst: |S|={nS} |O|={nO} phi={phi}  def={l:.6f}  true={r:.6f}")
    print("  => the independence hypothesis IS load-bearing; without it the")
    print("     definition and the information quantity come apart.")
else:
    print("  identity survives correlation (hypothesis not load-bearing)")

print()
print("="*72)
print("(2) cor:controlled-elementary  (range, one-state value, monotonicity)")
print("="*72)
def parts(n):
    def rec(i,mx,cur):
        if i==n: yield tuple(cur); return
        for b in range(mx+1):
            cur.append(b); yield from rec(i+1,max(mx,b+1),cur); cur.pop()
    yield from rec(0,0,[])
PARTS={n:list(parts(n)) for n in range(2,6)}
def unif_lumpable(phi,tau,supp,nS,nI):
    for x in range(nI):
        img={}
        for s in range(nS):
            k=phi[s]
            for y in supp[s][x]:
                v=phi[tau[s][x][y]]
                if img.get((k,x,y),v)!=v: return False
                img[(k,x,y)]=v
    return True
bad_range=bad_one=bad_mono=bad_ref=0; n=0
for trial in range(15000):
    nS=rng.randrange(2,6); nI=rng.randrange(1,3); nO=rng.randrange(2,4)
    tau=[[[rng.randrange(nS) for _ in range(nO)] for _ in range(nI)] for _ in range(nS)]
    supp=[[set(range(nO)) for _ in range(nI)] for _ in range(nS)]
    P=[[None]*nI for _ in range(nS)]
    for s in range(nS):
        for x in range(nI):
            w=[rng.random()+.02 for _ in range(nO)]; t=sum(w); P[s][x]=[v/t for v in w]
    pin=[rng.random()+.05 for _ in range(nI)]; t=sum(pin); pin=[v/t for v in pin]
    T=np.zeros((nS,nS))
    for s in range(nS):
        for x in range(nI):
            for y in range(nO): T[s][tau[s][x][y]]+=pin[x]*P[s][x][y]
    pi=np.ones(nS)/nS
    for _ in range(1500): pi=pi@T
    if pi.min()<1e-8: continue
    pi=pi/pi.sum(); n+=1
    def rc(phi):
        z=0.0
        for x in range(nI):
            for k in set(phi):
                C=[s for s in range(nS) if phi[s]==k]
                w=sum(pi[s] for s in C)
                bar=[sum(pi[s]*P[s][x][y] for s in C)/w for y in range(nO)]
                z+=pin[x]*sum(pi[s]*kl(P[s][x],bar) for s in C)
        return z
    jS=np.zeros((nI,nS,nO))
    for x in range(nI):
        for s in range(nS):
            for y in range(nO): jS[x,s,y]=pin[x]*pi[s]*P[s][x][y]
    ISYX=mi_cond(jS)
    feas=[p for p in PARTS[nS] if unif_lumpable(p,tau,supp,nS,nI)]
    vals={}
    for M in range(1,nS+1):
        c=[rc(p) for p in feas if len(set(p))<=M]
        if c: vals[M]=min(c)
    if abs(vals[1]-ISYX)>1e-9: bad_one+=1
    for M,v in vals.items():
        if v<-1e-12 or v>ISYX+1e-9: bad_range+=1
    ms=sorted(vals)
    for a,b in zip(ms,ms[1:]):
        if vals[b]>vals[a]+1e-12: bad_mono+=1
    # refinement monotonicity
    for p1 in feas:
        for p2 in feas:
            ref=all(p2[i]==p2[j] for i in range(nS) for j in range(nS) if p1[i]==p1[j])
            if ref and rc(p1)>rc(p2)+1e-12: bad_ref+=1
print(f"  instances                       : {n}")
print(f"  range 0<=RetKL^ctrl(M)<=I(S;Y|X) violations : {bad_range}")
print(f"  RetKL^ctrl(1)=I(S;Y|X) violations           : {bad_one}")
print(f"  monotonicity in M violations                : {bad_mono}")
print(f"  refinement monotonicity violations          : {bad_ref}")
