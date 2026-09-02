"""Clean confirmation: Lsync(M) < Lsyncu(M) is possible.

Simplest decisive instance: two machines in H_M that a SINGLE tree must
handle, where the A-dependent optimum is smaller than any universal tree's
worst case.  Exhibit explicitly and verify by exhaustive search over
universal trees (histories are output strings; strategy = map history -> input).
"""
import itertools, sys
from collections import deque
sys.setrecursionlimit(100000)

def classes(M,nI,tau,lam):
    part={s:tuple(lam[s]) for s in range(M)}
    c={}; part={s:c.setdefault(part[s],len(c)) for s in range(M)}
    for _ in range(M+1):
        new={s:(part[s],tuple(part[tau[s][a]] for a in range(nI))) for s in range(M)}
        c2={}; new={s:c2.setdefault(new[s],len(c2)) for s in range(M)}
        if len(set(new.values()))==len(set(part.values())): break
        part=new
    return part

def per_machine_opt(M,nI,tau,lam,cap=10**6):
    cls=classes(M,nI,tau,lam); memo={}
    def val(U,seen):
        if U in memo: return memo[U]
        if len(set(cls[s] for s in U))<=1: return 0
        if U in seen: return cap
        best=cap
        for a in range(nI):
            w=0
            for o in set(lam[s][a] for s in U):
                nxt=frozenset(tau[s][a] for s in U if lam[s][a]==o)
                if nxt==U: w=cap; break
                r=val(nxt,seen|{U})
                if r>=cap: w=cap; break
                w=max(w,1+r)
            best=min(best,w)
        memo[U]=best; return best
    return val(frozenset(range(M)),frozenset())

# Two 2-state machines over |I|=2, |O|=2 that need OPPOSITE first inputs.
# A1: input 0 separates, input 1 is useless.  A2: input 1 separates, input 0 useless.
A1=([[0,0],[1,1]], [[0,0],[1,0]])   # tau, lam : input0 outputs differ (0 vs 1)
A2=([[0,0],[1,1]], [[0,0],[0,1]])   # input1 outputs differ
M,nI=2,2
for nm,(tau,lam) in [('A1',A1),('A2',A2)]:
    print(f"{nm}: tau={tau} lam={lam}  minimal={len(set(classes(M,nI,tau,lam).values()))==M}"
          f"  per-machine optimum={per_machine_opt(M,nI,tau,lam)}")
print()
# universal tree over BOTH: enumerate strategies as (first input, then by output)
best=None
for first in range(nI):
    for nxt0 in range(nI):
        for nxt1 in range(nI):
            worst=0
            for tau,lam in [A1,A2]:
                cls=classes(M,nI,tau,lam)
                U=frozenset(range(M)); d=0
                seq=[first]
                for step in range(4):
                    if len(set(cls[s] for s in U))<=1: break
                    a = first if step==0 else (nxt0 if last==0 else nxt1)
                    # adversary picks the branch keeping U largest
                    cand=[]
                    for o in set(lam[s][a] for s in U):
                        n=frozenset(tau[s][a] for s in U if lam[s][a]==o)
                        cand.append((len(n),o,n))
                    cand.sort(reverse=True)
                    _,last,U=cand[0]; d+=1
                worst=max(worst,d)
            if best is None or worst<best: best=worst
print(f"Lsync over {{A1,A2}}  (tree may depend on A) = {max(per_machine_opt(M,nI,*m) for m in [A1,A2])}")
print(f"Lsyncu over {{A1,A2}} (ONE tree for both)    = {best}")
print()
print("=> the quantities differ: a universal tree cannot pick the right first")
print("   input without knowing which machine it faces.")
