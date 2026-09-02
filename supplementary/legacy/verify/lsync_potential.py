"""Verify the POTENTIAL-FUNCTION proof of L_sync^adapt(A) <= (M-1)^2,
and the sharper pair-counting bound M(M-1)/2, on exhaustive small cases.

PROOF TO WRITE UP.
Let U be the current uncertainty set (states consistent with the transcript),
initially all M states of a minimal machine A.
Claim: from any U with >= 2 observationally distinct states, the learner can
force |U| to strictly decrease within at most M-1 steps.
  - pick s != t in U; minimality gives a separating word w, |w| <= M-1
    (BFS on the M(M-1)/2 state pairs of A: the pair-graph has <= M(M-1)/2
    nodes, but the shortest separating word for a SPECIFIC pair is <= M-1
    by the standard product-automaton argument restricted to a single machine)
  - feed w.  Deterministic transitions map U forward; |U| never increases.
    At the last letter of w, s and t emit different outputs, so the observed
    output eliminates at least one of them: |U| strictly decreases.
Hence <= M-1 decreases, each costing <= M-1 steps: L <= (M-1)^2 = O(M^2).
"""
import itertools, math, sys
from collections import deque
sys.setrecursionlimit(100000)

def sigs(M,nI,tau,lam):
    part={s: tuple(lam[s]) for s in range(M)}
    for _ in range(M):
        new={s:(part[s],tuple(part[tau[s][a]] for a in range(nI))) for s in range(M)}
        codes={}; out={}
        for s in range(M):
            codes.setdefault(new[s],len(codes)); out[s]=codes[new[s]]
        if out==part: break
        part=out
    return part

def sep_len(M,nI,tau,lam,s,t):
    """shortest word separating s,t (BFS on pairs)"""
    if s==t: return None
    dist={(min(s,t),max(s,t)):0}; dq=deque([(s,t)])
    while dq:
        a_,b_=dq.popleft(); d=dist[(min(a_,b_),max(a_,b_))]
        for x in range(nI):
            if lam[a_][x]!=lam[b_][x]: return d+1
        for x in range(nI):
            na,nb=tau[a_][x],tau[b_][x]
            k=(min(na,nb),max(na,nb))
            if na!=nb and k not in dist:
                dist[k]=d+1; dq.append((na,nb))
    return None

def homing_len(M,nI,tau,lam,cap=10**7):
    cls=sigs(M,nI,tau,lam)
    memo={}
    def val(U,seen):
        if U in memo: return memo[U]
        if len(set(cls[s] for s in U))<=1: return 0
        if U in seen: return cap
        best=cap
        for a in range(nI):
            worst=0
            for o in set(lam[s][a] for s in U):
                nxt=frozenset(tau[s][a] for s in U if lam[s][a]==o)
                if nxt==U: worst=cap; break
                r=val(nxt,seen|{U})
                if r>=cap: worst=cap; break
                worst=max(worst,1+r)
            best=min(best,worst)
        memo[U]=best
        return best
    return val(frozenset(range(M)),frozenset())

print("(1) shortest separating word for a PAIR is <= M-1 (exhaustive)")
bad=0; tot=0; mx=0
for (M,nI,nO) in [(2,1,2),(3,1,2),(4,1,2),(2,2,2),(3,2,2),(4,2,2),(3,1,3)]:
    for tau in itertools.product(itertools.product(range(M),repeat=nI),repeat=M):
        for lam in itertools.product(itertools.product(range(nO),repeat=nI),repeat=M):
            if len(set(sigs(M,nI,tau,lam).values()))<M: continue
            for s in range(M):
                for t in range(s+1,M):
                    L=sep_len(M,nI,tau,lam,s,t)
                    if L is None: continue
                    tot+=1; mx=max(mx,L)
                    if L>M-1: bad+=1
print(f"    {tot} separable pairs; violations of |w| <= M-1: {bad}; max observed {mx}")

print()
print("(2) homing length vs (M-1)^2 and M(M-1)/2 (exhaustive, minimal machines)")
print(f"    {'M':>3} {'|I|':>4} {'|O|':>4} {'max L':>6} {'M(M-1)/2':>9} {'(M-1)^2':>8}")
allok=True
for (M,nI,nO) in [(2,1,2),(3,1,2),(4,1,2),(5,1,2),(2,2,2),(3,2,2),(3,1,3),(4,1,3)]:
    best=-1
    for tau in itertools.product(itertools.product(range(M),repeat=nI),repeat=M):
        for lam in itertools.product(itertools.product(range(nO),repeat=nI),repeat=M):
            if len(set(sigs(M,nI,tau,lam).values()))<M: continue
            v=homing_len(M,nI,tau,lam)
            if v<10**7: best=max(best,v)
    ok = best<=M*(M-1)//2
    allok &= ok
    print(f"    {M:>3} {nI:>4} {nO:>4} {best:>6} {M*(M-1)//2:>9} {(M-1)**2:>8}  {'OK' if ok else 'VIOLATION'}")
print(f"\n    all within M(M-1)/2: {allok}")
