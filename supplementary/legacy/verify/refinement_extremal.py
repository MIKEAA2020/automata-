"""
ITEM 2 write-up verification: the counter family C_M.

  |I| = 1 (single input, suppressed), O = {0,1}, states 0..M-1
  tau(s, 0) = min(s+1, M-1)      "advance"
  tau(s, 1) = 0                  "reset"
  P_s = Bernoulli(b)  for s <= M-2      (all share ONE kernel)
  P_{M-1} = Bernoulli(c),  c != b       (distinct kernel)

Claims:
 (i)   |phi_ker| = 2
 (ii)  N* = M  (refinement separates every state)
 (iii) the recursion needs exactly M-1 rounds
 (iv)  therefore worst-case gap N* - |phi_ker| = M-2, and the |S|-round
       bound of prop:kernel-refinement-exists is tight to within one
 (v)   the chain is irreducible with strictly positive stationary law
 (vi)  RetKL^ctrl(M-1) > 0  while RetKL^ctrl(M) = 0
 (vii) N* <= |S+| always (upper bound), so M is the max possible
"""
import math, itertools
import numpy as np
from fractions import Fraction as F

def build(M,b,c):
    nS,nI,nO=M,1,2
    tau=[[[min(s+1,M-1), 0]] for s in range(M)]
    P=[[[1-b,b]] for _ in range(M-1)]+[[[1-c,c]]]
    return nS,nI,nO,tau,P

def refine_rounds(phik,tau,nS,nI,nO,supp=None):
    phi=list(phik); r=0; hist=[tuple(phi)]
    while True:
        sig={}
        for s in range(nS):
            key=(phi[s],tuple(phi[tau[s][x][y]] for x in range(nI) for y in range(nO)))
            sig[s]=key
        keys=sorted(set(sig.values()),key=str); idx={k:i for i,k in enumerate(keys)}
        new=[idx[sig[s]] for s in range(nS)]; r+=1
        hist.append(tuple(new))
        if len(set(new))==len(set(phi)): return len(set(new)), r, hist
        phi=new

def unif_lumpable(phi,tau,nS,nI,nO):
    for x in range(nI):
        img={}
        for s in range(nS):
            k=phi[s]
            for y in range(nO):
                v=phi[tau[s][x][y]]
                if img.get((k,x,y),v)!=v: return False
                img[(k,x,y)]=v
    return True

def kl(p,q): return sum(a*math.log(a/b) for a,b in zip(p,q) if a>0)

def parts(n):
    def rec(i,mx,cur):
        if i==n: yield tuple(cur); return
        for b in range(mx+1):
            cur.append(b); yield from rec(i+1,max(mx,b+1),cur); cur.pop()
    yield from rec(0,0,[])

print("="*74)
print("ITEM 2  extremal counter family for the stable refinement")
print("="*74)
b,c=0.5,0.1
allok=True
for M in range(3,16):
    nS,nI,nO,tau,P=build(M,b,c)
    phik=[0]*(M-1)+[1]
    N,r,hist=refine_rounds(phik,tau,nS,nI,nO)
    # stationary law
    T=np.zeros((nS,nS))
    for s in range(nS):
        for y in range(nO): T[s][tau[s][0][y]]+=P[s][0][y]
    pi=np.ones(nS)/nS
    for _ in range(200000): pi=pi@T
    pi/=pi.sum()
    # irreducible?
    reach=set([0]); st=[0]
    while st:
        a=st.pop()
        for y in range(nO):
            bb=tau[a][0][y]
            if bb not in reach: reach.add(bb); st.append(bb)
    irr=len(reach)==nS
    ok=(len(set(phik))==2 and N==M and r==M-1 and irr and pi.min()>1e-12)
    allok&=ok
    print(f"  M={M:2d}: |phi_ker|={len(set(phik))}  N*={N:2d}  rounds={r:2d}  "
          f"gap={N-2:2d}  irred={irr}  pi_min={pi.min():.2e}  {'ok' if ok else '**FAIL**'}")
print(f"\n  all M: {allok}")
assert allok

print()
print("="*74)
print("  (vi) retention values at M-1 vs M  (small M, exhaustive over quotients)")
print("="*74)
for M in range(3,8):
    nS,nI,nO,tau,P=build(M,b,c)
    T=np.zeros((nS,nS))
    for s in range(nS):
        for y in range(nO): T[s][tau[s][0][y]]+=P[s][0][y]
    pi=np.ones(nS)/nS
    for _ in range(200000): pi=pi@T
    pi/=pi.sum()
    def rc(phi):
        z=0.0
        for k in set(phi):
            C=[s for s in range(nS) if phi[s]==k]
            w=sum(pi[s] for s in C)
            bar=[sum(pi[s]*P[s][0][y] for s in C)/w for y in range(nO)]
            z+=sum(pi[s]*kl(P[s][0],bar) for s in C)
        return z
    v={}
    for m in (M-1,M):
        cand=[p for p in parts(nS) if len(set(p))<=m and unif_lumpable(p,tau,nS,nI,nO)]
        v[m]=min(rc(p) for p in cand) if cand else float('nan')
    print(f"   M={M}: RetKL^ctrl({M-1}) = {v[M-1]:.8f} > 0 ;  RetKL^ctrl({M}) = {v[M]:.1e}")
    assert v[M-1]>1e-9 and v[M]<1e-12

print()
print("="*74)
print("  (vii) N* <= |S| over random machines (upper bound never violated)")
print("="*74)
import random
rng=random.Random(5)
bad=0; tot=0
for _ in range(200000):
    nS=rng.randrange(2,7); nI=rng.randrange(1,3); nO=rng.randrange(2,4)
    tau=[[[rng.randrange(nS) for _ in range(nO)] for _ in range(nI)] for _ in range(nS)]
    npool=rng.randrange(1,nS+1)
    phik=[rng.randrange(npool) for _ in range(nS)]
    u=sorted(set(phik)); rm={k:i for i,k in enumerate(u)}; phik=[rm[k] for k in phik]
    N,r,_=refine_rounds(phik,tau,nS,nI,nO)
    tot+=1
    if N>nS or r>nS: bad+=1
    if not unif_lumpable(tuple(_[-1]),tau,nS,nI,nO): bad+=1
print(f"   {tot} random instances; violations of N*<=|S|, rounds<=|S|, or")
print(f"   non-lumpable fixed point: {bad}")
assert bad==0
print()
print("ITEM 2 VERIFIED")

# ---------------------------------------------------------------- induction
print()
print("="*74)
print("  (viii) the INDUCTION CLAIM in prop:refinement-extremal, step by step")
print("="*74)
print("  claim: phi^(m) separates exactly the top m+1 states, i.e.")
print("         phi^(m)(s)=phi^(m)(s') iff s=s' or s,s' <= M-2-m")
allok2=True
for M in range(3,14):
    nS,nI,nO,tau,P=build(M,0.5,0.1)
    phi=[0]*(M-1)+[1]
    m=0
    while True:
        # predicted partition at level m
        pred={}
        for s in range(M):
            pred[s]= 0 if s<=M-2-m else 1+(s-(M-1-m))
        # compare as partitions (same blocks)
        def blocks(f):
            d={}
            for s in range(M): d.setdefault(f[s] if not isinstance(f,dict) else f[s],set()).add(s)
            return frozenset(frozenset(v) for v in d.values())
        got=blocks(phi); want=blocks(pred)
        if got!=want:
            print(f"   M={M} m={m}: MISMATCH got={sorted(map(sorted,got))} want={sorted(map(sorted,want))}")
            allok2=False; break
        if len(set(phi))==M: break
        sig={s:(phi[s],tuple(phi[tau[s][x][y]] for x in range(nI) for y in range(nO)))
             for s in range(M)}
        keys=sorted(set(sig.values()),key=str); idx={k:i for i,k in enumerate(keys)}
        phi=[idx[sig[s]] for s in range(M)]; m+=1
    if allok2: print(f"   M={M:2d}: induction holds at every level m=0..{m}, discrete at m={M-2}: {m==M-2}")
    allok2 &= (m==M-2)
print(f"\n  induction claim verified for M=3..13: {allok2}")
assert allok2
print()
print("ITEM 2 INDUCTION VERIFIED")

# ------------------------------------------------------- T49 hypothesis check
print()
print("="*74)
print("  (ix) T49: is beta,gamma in (0,1) EXACTLY the right hypothesis?")
print("="*74)
import numpy as np
def irred_and_pos(M,b,c):
    tau=[[min(s+1,M-1),0] for s in range(M)]
    P=[[1-b,b] for _ in range(M-1)]+[[1-c,c]]
    adj={s:{tau[s][y] for y in (0,1) if P[s][y]>0} for s in range(M)}
    for s in range(M):
        seen={s}; st=[s]
        while st:
            a=st.pop()
            for t in adj[a]:
                if t not in seen: seen.add(t); st.append(t)
        if len(seen)!=M: return False
    T=np.zeros((M,M))
    for s in range(M):
        for y in (0,1): T[s][tau[s][y]]+=P[s][y]
    v=np.ones(M)/M
    for _ in range(50000): v=v@T
    return v.min()>1e-12

print("  boundary values (excluded by the corrected hypothesis):")
allbad=True
for M in (3,4,5,6):
    for b,c in [(0.5,0.0),(1.0,0.5)]:
        ok=irred_and_pos(M,b,c)
        allbad &= (not ok)
        print(f"    M={M} beta={b} gamma={c}: claim (i) holds = {ok}   (must be False)")
assert allbad, "a boundary case unexpectedly satisfies (i)"

print()
print("  interior values (admitted by the corrected hypothesis):")
import random
rng=random.Random(3); allok=True
for M in (3,4,5,6,7):
    for _ in range(60):
        b=rng.uniform(0.02,0.98); c=rng.uniform(0.02,0.98)
        if abs(b-c)<1e-6: continue
        if not irred_and_pos(M,b,c): allok=False; print("    FAIL",M,b,c)
print(f"    300 random (beta,gamma) in (0,1)^2, M=3..7: claim (i) holds throughout = {allok}")
assert allok

print()
print("  note: beta=0 and gamma=1 are individually harmless, but the corrected")
print("  hypothesis excludes them too -- it is sufficient and simple, not")
print("  minimal.  The two genuinely fatal cases are gamma=0 and beta=1.")
for M in (4,5):
    for b,c in [(0.0,0.5),(0.5,1.0)]:
        print(f"    M={M} beta={b} gamma={c}: claim (i) holds = {irred_and_pos(M,b,c)}")
print()
print("T49 HYPOTHESIS VERIFIED")
