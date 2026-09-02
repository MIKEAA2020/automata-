"""THE TENSION, made precise.

Conjecture (T):  if U is not split by ANY word of length < k, then
                 |U| <= M - k + 1.
Equivalently  d(U) := min_{s != t in U} sep(s,t)  satisfies
                 d(U) <= M - |U| + 1.

WHY it should hold: after k rounds of Moore refinement the block count b_k
satisfies b_k >= 1 + k (strict increase each effective round).  If U survives
k rounds unsplit, all |U| states of U sit in ONE block, and the other blocks
hold >= 1 state each, so b_k <= M - |U| + 1.  Combining: 1 + k <= M - |U| + 1.

CONSEQUENCE:  total homing length <= sum over episodes of d(U_i)
              <= sum_{m=2}^{M} (M - m + 1) = M(M-1)/2,
which BEATS the (M-1)^2 bound of prop:lsyncu-quadratic.
"""
import itertools
from collections import deque

def moore_blocks(M,nI,tau,lam):
    """block count after each refinement round; returns list b[0..R]"""
    part={s:tuple(lam[s]) for s in range(M)}
    c={}; part={s:c.setdefault(part[s],len(c)) for s in range(M)}
    out=[len(set(part.values()))]
    while True:
        new={s:(part[s],tuple(part[tau[s][a]] for a in range(nI))) for s in range(M)}
        c2={}; new={s:c2.setdefault(new[s],len(c2)) for s in range(M)}
        n=len(set(new.values()))
        if n==out[-1]: return out
        out.append(n); part=new

def sep_len(M,nI,tau,lam,s,t):
    """shortest word length separating s,t; None if equivalent"""
    if s==t: return None
    seen={(min(s,t),max(s,t))}; dq=deque([(s,t,0)])
    while dq:
        a_,b_,d=dq.popleft()
        for x in range(nI):
            if lam[a_][x]!=lam[b_][x]: return d+1
        for x in range(nI):
            na,nb=tau[a_][x],tau[b_][x]
            k=(min(na,nb),max(na,nb))
            if na!=nb and k not in seen:
                seen.add(k); dq.append((na,nb,d+1))
    return None

def minimal(M,nI,tau,lam):
    return all(sep_len(M,nI,tau,lam,s,t) is not None
               for s in range(M) for t in range(s+1,M))

print("="*78)
print("(A) TENSION LEMMA:  d(U) <= M - |U| + 1   for every subset U, |U|>=2")
print("="*78)
worst=None; viol=0; tot=0; tight=0
for (M,nI,nO) in [(3,1,2),(4,1,2),(5,1,2),(3,2,2),(4,2,2),(3,1,3),(4,1,3)]:
    for tau in itertools.product(itertools.product(range(M),repeat=nI),repeat=M):
        for lam in itertools.product(itertools.product(range(nO),repeat=nI),repeat=M):
            if not minimal(M,nI,tau,lam): continue
            sep={}
            for s in range(M):
                for t in range(s+1,M):
                    sep[(s,t)]=sep_len(M,nI,tau,lam,s,t)
            for r in range(2,M+1):
                for U in itertools.combinations(range(M),r):
                    d=min(sep[(min(s,t),max(s,t))] for s in U for t in U if s<t)
                    bound=M-r+1
                    tot+=1
                    if d>bound:
                        viol+=1
                        if worst is None: worst=(M,nI,nO,U,d,bound,tau,lam)
                    if d==bound: tight+=1
print(f"  subsets tested: {tot}")
print(f"  violations of d(U) <= M-|U|+1 : {viol}")
print(f"  tight cases (d = M-|U|+1)     : {tight}")
if worst: print("  first violation:",worst[:6])

print()
print("="*78)
print("(B) block count grows: b_k >= 1 + k  (the other half of the argument)")
print("="*78)
viol2=0; n2=0
for (M,nI,nO) in [(3,1,2),(4,1,2),(5,1,2),(3,2,2),(4,2,2),(4,1,3)]:
    for tau in itertools.product(itertools.product(range(M),repeat=nI),repeat=M):
        for lam in itertools.product(itertools.product(range(nO),repeat=nI),repeat=M):
            if not minimal(M,nI,tau,lam): continue
            b=moore_blocks(M,nI,tau,lam); n2+=1
            for k,bk in enumerate(b):
                if bk < 1+k: viol2+=1
print(f"  minimal machines: {n2}; violations of b_k >= 1+k: {viol2}")
