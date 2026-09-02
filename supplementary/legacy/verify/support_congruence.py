"""
T39.  Schema-side claims of the audit's Block A.

(S1) rem:"Cofilteredness Persists": the intersection of two support-relative
     right congruences is again one, with index <= product.
(S2) prop:unifilar-residually-finite: the proof asserts
     "feasibility of (x,y) from a history depends only on the support of
      P_{sigma(.)}^x at y".   TRUE by definition of sigma -- check.
     But it ALSO needs sigma(u)=sigma(v) => Feas(u)=Feas(v), which is fine,
     AND it needs the relation ~_N to be well defined at the BOUNDARY
     (|w|=N-1 extending to length N).  Check whether ~_N as literally defined
     is a support-relative right congruence.
(S3) prop:unifilar-lumpability(i) WITHOUT block-uniform support: the audit says
     "the same relation still satisfies clause (ii) ... on commonly feasible
      events".  Check whether that is enough to make the quotient a machine.
"""
import random, itertools, sys
from itertools import product

# ---------------- S1 ----------------
print("="*72)
print("(S1) intersection of two support-relative right congruences")
print("="*72)
# Model a history system abstractly: states of a pruned automaton.
rng=random.Random(4)
bad=0; tot=0
for _ in range(40000):
    n=rng.randrange(2,6); nA=rng.randrange(1,4)
    feas=[set(a for a in range(nA) if rng.random()<0.7) for _ in range(n)]
    for i in range(n):
        if not feas[i]: feas[i]={rng.randrange(nA)}
    act=[[rng.randrange(n) if a in feas[i] else None for a in range(nA)] for i in range(n)]
    def is_src(phi):
        for i in range(n):
            for j in range(n):
                if phi[i]!=phi[j]: continue
                if feas[i]!=feas[j]: return False
                for a in feas[i]:
                    if phi[act[i][a]]!=phi[act[j][a]]: return False
        return True
    p1=[rng.randrange(1,n+1) for _ in range(n)]
    p2=[rng.randrange(1,n+1) for _ in range(n)]
    if not (is_src(p1) and is_src(p2)): continue
    tot+=1
    inter=[(p1[i],p2[i]) for i in range(n)]
    if not is_src(inter): bad+=1; print("  *** FAILED",feas,act,p1,p2); break
    if len(set(inter))>len(set(p1))*len(set(p2)): bad+=1
print(f"  pairs of support-relative right congruences tested: {tot}")
print(f"  failures (closure or index bound)                 : {bad}")

# ---------------- S2 ----------------
print()
print("="*72)
print("(S2) prop:unifilar-residually-finite, the relation ~_N as literally written")
print("="*72)
print("""  Audit's definition:  w ~_N w'  iff  w = w'  OR
                       ( |w|,|w'| >= N  and  sigma(w) = sigma(w') ).
  Clause (i) of def:support-right-cong requires Feas(w)=Feas(w') whenever
  w ~_N w'.  For the identity case this is trivial; for the state case it
  holds because feasibility of (x,y) from w depends only on sigma(w).
  Clause (ii): if |w|,|w'| >= N and sigma(w)=sigma(w'), then
  sigma(w.(x,y)) = tau(sigma(w),x,y) = sigma(w'.(x,y)) and both have length
  >= N+1 >= N, so w.(x,y) ~_N w'.(x,y).   OK.
  The identity case gives w.(x,y) = w'.(x,y).   OK.
  Index: at most |A|^0 + ... + |A|^{N-1} singleton classes below length N,
  plus at most |S| classes above.  FINITE.  OK.""")
# machine check of the argument on random pruned unifilar machines
bad=0; tot=0
for _ in range(600):
    nS=rng.randrange(2,5); nI=rng.randrange(1,3); nO=rng.randrange(2,4)
    supp=[[set(y for y in range(nO) if rng.random()<0.6) for _ in range(nI)] for _ in range(nS)]
    for s in range(nS):
        for x in range(nI):
            if not supp[s][x]: supp[s][x]={rng.randrange(nO)}
    tau=[[[rng.randrange(nS) for _ in range(nO)] for _ in range(nI)] for _ in range(nS)]
    N=rng.randrange(1,4)
    # enumerate feasible histories up to length N+2 with a start state
    start=0
    hist=[((),start)]
    allh=[]
    for _ in range(N+2):
        nxt=[]
        for h,s in hist:
            allh.append((h,s))
            for x in range(nI):
                for y in supp[s][x]:
                    nxt.append((h+((x,y),),tau[s][x][y]))
        hist=nxt
    allh+= hist
    D=dict(allh)
    def cls(h):
        s=D[h]
        return ('id',h) if len(h)<N else ('st',s)
    tot+=1
    for h1,s1 in allh:
        for h2,s2 in allh:
            if cls(h1)!=cls(h2): continue
            # clause (i)
            f1={(x,y) for x in range(nI) for y in supp[s1][x]}
            f2={(x,y) for x in range(nI) for y in supp[s2][x]}
            if f1!=f2: bad+=1; break
            # clause (ii)
            for (x,y) in f1:
                a=h1+((x,y),); b=h2+((x,y),)
                if a in D and b in D and cls(a)!=cls(b): bad+=1; break
print(f"  random pruned unifilar machines tested : {tot}")
print(f"  violations of clauses (i)/(ii)         : {bad}")

# ---------------- S3 ----------------
print()
print("="*72)
print("(S3) prop:unifilar-lumpability(i) WITHOUT block-uniform support")
print("="*72)
print("""  Audit text: "Without block-uniform support the same relation still
  satisfies clause (ii) of Definition ref{def:support-right-cong} on commonly
  feasible events."
  This is TRUE but vacuous as a congruence statement: clause (i) can fail, and
  then the quotient has no well-defined FEASIBILITY, so it is not a history
  system quotient.  Demonstrate: two histories with the same phi-image but
  different feasible sets.""")
# explicit: two states in one block, disjoint emission supports
nS,nI,nO=2,1,2
supp=[[{0}],[{1}]]
tau=[[[0,0]],[[1,1]]]
phi=(0,0)
f0={(0,y) for y in supp[0][0]}; f1={(0,y) for y in supp[1][0]}
print(f"    supports: s0 -> {sorted(supp[0][0])}, s1 -> {sorted(supp[1][0])}")
print(f"    phi = {phi} (one block)")
print(f"    Feas(s0) = {sorted(f0)},  Feas(s1) = {sorted(f1)}   equal? {f0==f1}")
print("    => clause (i) fails; the block has no well-defined feasible-event set.")
print("    The audit's fallback sentence is therefore correct but does NOT")
print("    yield a history-system quotient.  Block-uniform support (or the")
print("    weaker connectedness condition) is genuinely required.")
