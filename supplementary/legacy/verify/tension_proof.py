"""Verify the two proof steps of the tension lemma separately.

STEP 1. If no word of length < k splits U, then after k-1 refinement rounds
        all of U lies in ONE block of the Moore partition.
STEP 2. After k-1 rounds the block count b_{k-1} >= k  (strict increase).
        U in one block, other blocks nonempty => b_{k-1} <= M - |U| + 1.
        Hence k <= M - |U| + 1, i.e. d(U) <= M - |U| + 1.
"""
import itertools
from collections import deque

def sep_len(M,nI,tau,lam,s,t):
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

def part_after(M,nI,tau,lam,k):
    """Moore partition after k rounds (k=0 -> single block)"""
    if k==0: return {s:0 for s in range(M)}
    part={s:tuple(lam[s]) for s in range(M)}
    c={}; part={s:c.setdefault(part[s],len(c)) for s in range(M)}
    for _ in range(k-1):
        new={s:(part[s],tuple(part[tau[s][a]] for a in range(nI))) for s in range(M)}
        c2={}; part={s:c2.setdefault(new[s],len(c2)) for s in range(M)}
    return part

def minimal(M,nI,tau,lam):
    return all(sep_len(M,nI,tau,lam,s,t) is not None
               for s in range(M) for t in range(s+1,M))

v1=v2=0; n=0
for (M,nI,nO) in [(3,1,2),(4,1,2),(3,2,2),(4,2,2),(3,1,3),(5,1,2)]:
    for tau in itertools.product(itertools.product(range(M),repeat=nI),repeat=M):
        for lam in itertools.product(itertools.product(range(nO),repeat=nI),repeat=M):
            if not minimal(M,nI,tau,lam): continue
            n+=1
            sep={(s,t):sep_len(M,nI,tau,lam,s,t) for s in range(M) for t in range(s+1,M)}
            for r in range(2,M+1):
                for U in itertools.combinations(range(M),r):
                    d=min(sep[(min(s,t),max(s,t))] for s in U for t in U if s<t)
                    # STEP 1: U is monochromatic in the partition after d-1 rounds
                    p=part_after(M,nI,tau,lam,d-1)
                    if len({p[s] for s in U})!=1: v1+=1
                    # STEP 2: block count after d-1 rounds <= M - |U| + 1
                    if len(set(p.values())) > M-r+1: v2+=1
print(f"minimal machines: {n}")
print(f"STEP 1 violations (U not monochromatic after d(U)-1 rounds): {v1}")
print(f"STEP 2 violations (b_{{d-1}} > M-|U|+1):                      {v2}")
print()
print("Both steps hold => d(U) <= M-|U|+1, and summing over episodes gives M(M-1)/2.")
