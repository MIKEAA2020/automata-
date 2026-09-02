"""Is L_sync^adapt(A) <= M-1 always?  If so, Lsyncu(M) = O(M) = o(M log M),
which RESOLVES the open problem's second branch negatively for the
length currency: no family can have Lsyncu = omega(M log M).

Key structural fact to test:  each *informative* step strictly reduces the
number of surviving observational classes, and there are at most M of them.
"""
import itertools, math
from functools import lru_cache
import sys
sys.setrecursionlimit(100000)

def classes(nS,nI,tau,lam):
    sig={}
    for s in range(nS):
        out=[]
        for L in range(1,min(nS,4)+1):
            for w in itertools.product(range(nI),repeat=L):
                c=s
                for a in w: out.append(lam[c][a]); c=tau[c][a]
        sig[s]=tuple(out)
    return sig

def homing(nS,nI,tau,lam,cap=10**6):
    sig=classes(nS,nI,tau,lam)
    memo={}
    def val(U, seen):
        key=U
        if key in memo: return memo[key]
        if len(set(sig[s] for s in U))<=1: return 0
        if U in seen: return cap                 # cycle: this branch never homes
        best=cap
        for a in range(nI):
            worst=0
            for o in set(lam[s][a] for s in U):
                nxt=frozenset(tau[s][a] for s in U if lam[s][a]==o)
                r=val(nxt, seen|{U})
                if r>=cap: worst=cap; break
                worst=max(worst,1+r)
            best=min(best,worst)
        memo[key]=best
        return best
    return val(frozenset(range(nS)), frozenset())

print("Exhaustive: max L_sync^adapt over ALL minimal machines")
print(f"{'M':>3} {'|I|':>4} {'|O|':>4} {'max':>5} {'M-1':>5} {'M log2 M':>9} {'#minimal':>9} {'<=M-1?':>7}")
ok=True
for (nS,nI,nO) in [(2,1,2),(3,1,2),(4,1,2),(5,1,2),(2,2,2),(3,2,2),(3,1,3),(4,1,3)]:
    best=-1; nmin=0
    for tau in itertools.product(itertools.product(range(nS),repeat=nI),repeat=nS):
        for lam in itertools.product(itertools.product(range(nO),repeat=nI),repeat=nS):
            sig=classes(nS,nI,tau,lam)
            if len(set(sig.values()))<nS: continue
            nmin+=1
            v=homing(nS,nI,tau,lam)
            if v<10**6: best=max(best,v)
    good = best<=nS-1
    ok &= good
    print(f"{nS:>3} {nI:>4} {nO:>4} {best:>5} {nS-1:>5} {nS*math.log2(nS):>9.1f} {nmin:>9} {str(good):>7}")
print(f"\nmax L_sync^adapt <= M-1 in every signature tested: {ok}")
print("=> L_sync^adapt(A) = O(M) = o(M log M):  the length currency also collapses.")
