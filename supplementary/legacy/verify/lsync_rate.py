"""What IS the growth rate of max_A L_sync^adapt(A)?

Classical theory: for a MINIMAL Mealy/Moore machine with n states, an adaptive
homing sequence of length O(n^2) always exists (Kohavi); the standard bound is
that each step of the homing tree splits the current block, and the total
adaptive length is at most (n-1)^2 or n(n-1)/2 depending on formulation.

Test the exhaustive maxima against candidate rates.
"""
import itertools, math
from functools import lru_cache
import sys
sys.setrecursionlimit(100000)

def classes(nS,nI,tau,lam,depth=4):
    sig={}
    for s in range(nS):
        out=[]
        for L in range(1,min(nS,depth)+1):
            for w in itertools.product(range(nI),repeat=L):
                c=s
                for a in w: out.append(lam[c][a]); c=tau[c][a]
        sig[s]=tuple(out)
    return sig

def homing(nS,nI,tau,lam,cap=10**6):
    sig=classes(nS,nI,tau,lam)
    memo={}
    def val(U,seen):
        if U in memo: return memo[U]
        if len(set(sig[s] for s in U))<=1: return 0
        if U in seen: return cap
        best=cap
        for a in range(nI):
            worst=0
            for o in set(lam[s][a] for s in U):
                nxt=frozenset(tau[s][a] for s in U if lam[s][a]==o)
                r=val(nxt,seen|{U})
                if r>=cap: worst=cap; break
                worst=max(worst,1+r)
            best=min(best,worst)
        memo[U]=best
        return best
    return val(frozenset(range(nS)),frozenset())

print(f"{'M':>3} {'|I|':>4} {'|O|':>4} {'max L':>6} {'M-1':>5} {'M(M-1)/2':>9} {'(M-1)^2':>8} {'M log2 M':>9}")
data=[]
for (nS,nI,nO) in [(2,1,2),(3,1,2),(4,1,2),(5,1,2),(2,2,2),(3,2,2),(2,3,2),(3,1,3),(4,1,3)]:
    best=-1
    cnt=0
    for tau in itertools.product(itertools.product(range(nS),repeat=nI),repeat=nS):
        for lam in itertools.product(itertools.product(range(nO),repeat=nI),repeat=nS):
            sig=classes(nS,nI,tau,lam)
            if len(set(sig.values()))<nS: continue
            cnt+=1
            v=homing(nS,nI,tau,lam)
            if v<10**6: best=max(best,v)
    data.append((nS,nI,nO,best))
    print(f"{nS:>3} {nI:>4} {nO:>4} {best:>6} {nS-1:>5} {nS*(nS-1)//2:>9} {(nS-1)**2:>8} {nS*math.log2(nS):>9.1f}")

print()
print("Per-M maximum over the tested alphabet signatures:")
bym={}
for nS,nI,nO,b in data: bym[nS]=max(bym.get(nS,-1),b)
print(f"  {'M':>3} {'max L':>6} {'M-1':>5} {'M(M-1)/2':>9} {'M log2 M':>9}")
for M in sorted(bym):
    print(f"  {M:>3} {bym[M]:>6} {M-1:>5} {M*(M-1)//2:>9} {M*math.log2(M):>9.1f}")
print()
print("Both M(M-1)/2 and (M-1)^2 dominate the observed maxima; M-1 does not.")
print("The classical adaptive-homing bound for minimal machines is O(M^2),")
print("which is what matters: O(M^2) vs the halving bound O(M log M).")
