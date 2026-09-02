"""EXHAUSTIVE at M=5, |I|=2, |O|=2: what is the true maximum?
5^10 * 2^10 = 9.7e6 * 1024 -- too many.  Restrict: |O|=2 fixed, and exploit
that the max over lam for a given tau is what matters; enumerate tau fully
(5^10 = 9,765,625) is still too many.

Instead: exhaustive over M=5 with |I|=2 but tau restricted to those where
input 1 is a PERMUTATION (the structure every extremal machine had).
5! = 120 permutations x 5^5 = 3125 for input 0 x 2^10 outputs = 384M -- still
too many.  Restrict outputs to the 'single probe' shape seen in extremals:
lam[s][a] = 1 for exactly one (s,a) pair.  That is 10 choices.
120 * 3125 * 10 = 3.75M.  Feasible.
"""
import itertools, math, sys
from collections import deque
sys.setrecursionlimit(200000)
M=5; nI=2

def minimal(tau,lam):
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

def homing(tau,lam,cap=10**7):
    sig={}
    for s in range(M):
        o=[]
        for L in range(1,M+2):
            for w in itertools.product(range(nI),repeat=2):
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

best=-1; arg=None; n=0
for perm in itertools.permutations(range(M)):
    for t0 in itertools.product(range(M),repeat=M):
        tau=[[t0[s],perm[s]] for s in range(M)]
        for ps in range(M):
            for pa in range(nI):
                lam=[[0,0] for _ in range(M)]
                lam[ps][pa]=1
                if not minimal(tau,lam): continue
                n+=1
                v=homing(tau,lam)
                if v<10**7 and v>best:
                    best=v; arg=([r[:] for r in tau],[r[:] for r in lam])
print(f"minimal single-probe machines examined: {n}")
print(f"max adaptive homing depth at M=5 (perm+single-probe): {best}")
print(f"binom(5,2) = {M*(M-1)//2};  M log2 M = {M*math.log2(M):.1f}")
if arg: print("witness tau,lam =",arg)
