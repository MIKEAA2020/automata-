"""Is binom(M,2) attained at M=5,6?  Hill-climb over MINIMAL machines,
|I|=2,3, maximizing adaptive homing depth.  If the max plateaus well below
binom(M,2), the M=3,4 attainment is sporadic and Lsyncu is likely subquadratic.
"""
import random, math, itertools, sys
from collections import deque
sys.setrecursionlimit(200000)

def minimal(M,nI,tau,lam):
    def sep(s,t):
        if s==t: return None
        seen={(min(s,t),max(s,t))}; dq=deque([(s,t,0)])
        while dq:
            a_,b_,d=dq.popleft()
            for x in range(nI):
                if lam[a_][x]!=lam[b_][x]: return d+1
            for x in range(nI):
                na,nb=tau[a_][x],tau[b_][x]
                k=(min(na,nb),max(na,nb))
                if na!=nb and k not in seen: seen.add(k); dq.append((na,nb,d+1))
        return None
    return all(sep(s,t) is not None for s in range(M) for t in range(s+1,M))

def homing(M,nI,tau,lam,cap=10**7):
    # signature via BFS-truncated behaviour
    sig={}
    for s in range(M):
        o=[]
        for L in range(1,M+2):
            for w in itertools.product(range(nI),repeat=min(L,2)):
                c=s
                for _ in range(L):
                    for a in w: o.append(lam[c][a]); c=tau[c][a]
        sig[s]=tuple(o)
    memo={}
    def val(U,seen):
        if U in memo: return memo[U]
        if len(set(sig[s] for s in U))<=1: return 0
        if U in seen: return cap
        best=cap
        for a in range(nI):
            w=0
            for o in set(lam[s][a] for s in U):
                nxt=frozenset(tau[s][a] for s in U if lam[s][a]==o)
                r=val(nxt,seen|{U})
                if r>=cap: w=cap; break
                w=max(w,1+r)
            best=min(best,w)
        memo[U]=best; return best
    return val(frozenset(range(M)),frozenset())

def search(M,nI,nO,iters,restarts,seed):
    rng=random.Random(seed); best=-1
    for _ in range(restarts):
        for _t in range(3000):
            tau=[[rng.randrange(M) for _ in range(nI)] for _ in range(M)]
            lam=[[rng.randrange(nO) for _ in range(nI)] for _ in range(M)]
            if minimal(M,nI,tau,lam): break
        else: continue
        cur=homing(M,nI,tau,lam); cur=-1 if cur>=10**7 else cur
        for _ in range(iters):
            s=rng.randrange(M); a=rng.randrange(nI); which=rng.random()<0.5
            old=tau[s][a] if which else lam[s][a]
            new=rng.randrange(M) if which else rng.randrange(nO)
            if which: tau[s][a]=new
            else: lam[s][a]=new
            if not minimal(M,nI,tau,lam):
                if which: tau[s][a]=old
                else: lam[s][a]=old
                continue
            v=homing(M,nI,tau,lam); v=-1 if v>=10**7 else v
            if v>=cur: cur=v
            else:
                if which: tau[s][a]=old
                else: lam[s][a]=old
        best=max(best,cur)
    return best

print(f"{'M':>3} {'|I|':>4} {'best L found':>13} {'binom(M,2)':>11} {'M log2 M':>9} {'attained?':>10}")
for M in [5,6,7,8]:
    for nI in [2,3]:
        b=search(M,nI,2,iters=900,restarts=6,seed=31*M+nI)
        att = 'YES' if b>=M*(M-1)//2 else f'no (gap {M*(M-1)//2-b})'
        print(f"{M:>3} {nI:>4} {b:>13} {M*(M-1)//2:>11} {M*math.log2(M):>9.1f} {att:>10}")
