"""FIX 3(b): is the version-space universal strategy VALID?

Claim:  Lsyncu(M) <= (M-1)(N_M - 1),  N_M = #{(A,q) : A in H_M, q in Q_A}.

Strategy: maintain V = {(A,q)} consistent with transcript.  While SOME
consistent machine A carries two observationally distinct candidate states
q,q', pick such a pair, compute a separating word w INSIDE A (length <= M-1),
feed it, delete every candidate whose predicted output sequence mismatches.

KEY POINT I MISSED IN TURN 31: this strategy is a function of the TRANSCRIPT
ONLY (V is determined by the transcript), so it IS a single universal decision
tree.  The learner never needs to know the true machine -- it picks *some*
candidate machine and separates two of *its* states.

Check three things:
 (1) two states of the SAME M-state machine separate within M-1 (not 2M-1);
 (2) feeding such a w always deletes >= 1 of the chosen pair;
 (3) the strategy terminates at the def:output-aware-sync objective.
"""
import itertools
from collections import deque

def sep_word(M,nI,tau,lam,q,qp):
    """shortest separating word for two states of the SAME machine; None if equiv"""
    if q==qp: return None
    seen={(min(q,qp),max(q,qp))}
    dq=deque([(q,qp,())])
    while dq:
        a,b,w=dq.popleft()
        for x in range(nI):
            if lam[a][x]!=lam[b][x]: return w+(x,)
        for x in range(nI):
            na,nb=tau[a][x],tau[b][x]
            k=(min(na,nb),max(na,nb))
            if na!=nb and k not in seen:
                seen.add(k); dq.append((na,nb,w+(x,)))
    return None

def classes(M,nI,tau,lam):
    part={s:tuple(lam[s]) for s in range(M)}
    c={}; part={s:c.setdefault(part[s],len(c)) for s in range(M)}
    for _ in range(M+1):
        new={s:(part[s],tuple(part[tau[s][a]] for a in range(nI))) for s in range(M)}
        c2={}; new={s:c2.setdefault(new[s],len(c2)) for s in range(M)}
        if len(set(new.values()))==len(set(part.values())): break
        part=new
    return part

print("="*76)
print("(1) separating word for two states of the SAME machine: length <= M-1 ?")
print("="*76)
worst=0; tot=0; viol=0
for (M,nI,nO) in [(2,1,2),(3,1,2),(4,1,2),(5,1,2),(2,2,2),(3,2,2),(4,2,2),(3,1,3)]:
    for tau in itertools.product(itertools.product(range(M),repeat=nI),repeat=M):
        for lam in itertools.product(itertools.product(range(nO),repeat=nI),repeat=M):
            cls=classes(M,nI,tau,lam)
            if len(set(cls.values()))<M: continue      # minimal only
            for q in range(M):
                for qp in range(q+1,M):
                    w=sep_word(M,nI,tau,lam,q,qp)
                    if w is None: continue
                    tot+=1; worst=max(worst,len(w))
                    if len(w)>M-1: viol+=1
print(f"  {tot} separable same-machine pairs; violations of |w| <= M-1: {viol}; max |w| = {worst}")

print()
print("="*76)
print("(2) does feeding w delete at least one of the chosen pair?")
print("="*76)
# exhaustive logical check: if lam_A(q,w) != lam_A(q',w) then at most one
# matches any observed sequence, so >=1 of the two is deleted.
import random
random.seed(0)
bad=0; n=0
for _ in range(200000):
    M=random.randint(2,5); nI=random.randint(1,2); nO=2
    tau=[[random.randrange(M) for _ in range(nI)] for _ in range(M)]
    lam=[[random.randrange(nO) for _ in range(nI)] for _ in range(M)]
    q,qp=random.sample(range(M),2)
    w=sep_word(M,nI,tau,lam,q,qp)
    if w is None: continue
    n+=1
    def trace(s,w):
        out=[];c=s
        for x in w: out.append(lam[c][x]); c=tau[c][x]
        return tuple(out)
    o1,o2=trace(q,w),trace(qp,w)
    if o1==o2: bad+=1     # must differ, else the word does not separate
print(f"  {n} trials; separating word failed to separate: {bad}")
print("  => for ANY observed sequence, at most one of the two matches: >=1 deleted.")
