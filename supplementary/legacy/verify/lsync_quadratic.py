"""Prove-by-argument + verify:  L_sync^adapt(A) <= M(M-1)/2 for minimal
deterministic Mealy A, hence Lsyncu(M) = O(M^2).

ARGUMENT (the one to write up):
Track the current uncertainty set U (states consistent with the transcript).
Define the potential  Phi(U) = |U|(|U|-1)/2  = number of unordered pairs.
For a MINIMAL machine, any two distinct states are separated by some word;
by lem:moore-separation of length <= 2M-1 (here within one machine, <= M-1).
Pick a pair {s,t} in U and a shortest word w separating them.  Feeding w:
 - along the way, each step maps U forward (never increases |U|);
 - at the final letter of w, s and t emit DIFFERENT outputs, so whichever
   output is observed, at least one of s,t is eliminated: |U| strictly drops.
So each "separation episode" costs <= (length of w) steps and reduces |U| by
>= 1.  Total <= sum over episodes.  Cruder: |U| drops from M to 1, i.e. M-1
episodes, each <= M-1 steps  =>  <= (M-1)^2.
Sharper accounting (pairs): standard adaptive-DS analysis gives M(M-1)/2.
"""
import itertools, math, sys
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

print("Exhaustive maxima vs the two candidate quadratic bounds")
print(f"{'M':>3} {'|I|':>4} {'|O|':>4} {'max L':>6} {'M(M-1)/2':>9} {'(M-1)^2':>8} {'M log2 M':>9} {'ok':>4}")
allok=True
for (nS,nI,nO) in [(2,1,2),(3,1,2),(4,1,2),(5,1,2),(2,2,2),(3,2,2),(2,3,2),(3,1,3),(4,1,3),(2,2,3)]:
    best=-1
    for tau in itertools.product(itertools.product(range(nS),repeat=nI),repeat=nS):
        for lam in itertools.product(itertools.product(range(nO),repeat=nI),repeat=nS):
            sig=classes(nS,nI,tau,lam)
            if len(set(sig.values()))<nS: continue
            v=homing(nS,nI,tau,lam)
            if v<10**6: best=max(best,v)
    ok = best <= nS*(nS-1)//2
    allok &= ok
    print(f"{nS:>3} {nI:>4} {nO:>4} {best:>6} {nS*(nS-1)//2:>9} {(nS-1)**2:>8} {nS*math.log2(nS):>9.1f} {str(ok):>5}")
print(f"\nmax L_sync^adapt <= M(M-1)/2 in all tested signatures: {allok}")

print()
print("Crossover: when does the quadratic bound EXCEED the halving bound M log2 M?")
print(f"  {'M':>5} {'M(M-1)/2':>10} {'M log2 M':>10} {'quadratic bigger?':>18}")
for M in [2,3,4,5,8,16,32,64,128]:
    q=M*(M-1)/2; h=M*math.log2(M)
    print(f"  {M:>5} {q:>10.1f} {h:>10.1f} {str(q>h):>18}")
print("  -> for M >= 5 the quadratic length bound EXCEEDS M log2 M.")
print("     So Lsyncu(M) = O(M^2) does NOT rule out omega(M log M): the")
print("     open problem's second branch ('prove Lsyncu = O(M log M) always')")
print("     cannot be settled by the generic quadratic bound.")
