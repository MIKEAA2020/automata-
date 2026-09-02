"""ITEM 3.3: for |I|=1, is Lsyncu(M) <= M-1, or must it be larger?

My claim: with one letter there is only ONE universal tree, so Lsync=Lsyncu.
Auditor's claim: candidates come from DIFFERENT machines in H_M; their
disjoint union has up to 2M states, so the safe bound is 2M-1.

Who is right?  The universal learner must identify the current state within
each CONSISTENT machine.  With |I|=1 the input sequence is forced, so the
"tree" is trivially unique -- but the STOPPING TIME is what matters: the
learner must wait until the transcript pins the state in EVERY consistent
machine simultaneously, not just in the true one.
"""
import itertools
from collections import deque

def classes(M,tau,lam):
    part={s:lam[s] for s in range(M)}
    c={}; part={s:c.setdefault(part[s],len(c)) for s in range(M)}
    for _ in range(M+1):
        new={s:(part[s],part[tau[s]]) for s in range(M)}
        c2={}; new={s:c2.setdefault(new[s],len(c2)) for s in range(M)}
        if len(set(new.values()))==len(set(part.values())): break
        part=new
    return part

def minimal(M,tau,lam):
    return len(set(classes(M,tau,lam).values()))==M

def per_machine_depth(M,tau,lam):
    """rounds until the output prefix pins the state (known machine)"""
    cls=classes(M,tau,lam)
    U=frozenset(range(M)); d=0
    while len(set(cls[s] for s in U))>1 and d<=3*M+3:
        # single input; adversary picks worst output branch
        best=None
        for o in set(lam[s] for s in U):
            nxt=frozenset(tau[s] for s in U if lam[s]==o)
            if best is None or len(nxt)>len(best[0]): best=(nxt,o)
        U=best[0]; d+=1
    return d

# Enumerate all minimal unary machines with M states, binary output
for M in [2,3,4,5]:
    H=[]
    for tau in itertools.product(range(M),repeat=M):
        for lam in itertools.product(range(2),repeat=M):
            if minimal(M,tau,lam): H.append((tau,lam))
    per=[per_machine_depth(M,t,l) for t,l in H]
    print(f"M={M}: |H|={len(H)} minimal unary machines; max per-machine depth = {max(per)}  (M-1 = {M-1})")

    # UNIVERSAL: one forced input sequence; learner must pin the state within
    # EVERY machine consistent with the observed output prefix.
    # Track: for each length n, is there an output prefix consistent with >=2
    # (machine,state) candidates having DIFFERENT current states?
    worst_n=0
    # candidate set = all (machine index, initial state)
    cands=[(i,q) for i,(t,l) in enumerate(H) for q in range(M)]
    def trace(i,q,n):
        t,l=H[i]; out=[]; c=q
        for _ in range(n): out.append(l[c]); c=t[c]
        return tuple(out), c
    for n in range(0, 3*M+4):
        # group candidates by observed output prefix
        groups={}
        for (i,q) in cands:
            pref,cur=trace(i,q,n)
            groups.setdefault(pref,[]).append((i,q,cur))
        # a prefix is ambiguous if two candidates end in states that are NOT
        # observationally equivalent *within their own machines* -- for the
        # universal objective we need the CURRENT STATE pinned in each
        # consistent machine, i.e. per machine the surviving states agree
        amb=False
        for pref,g in groups.items():
            bym={}
            for (i,q,cur) in g: bym.setdefault(i,set()).add(cur)
            for i,curs in bym.items():
                cls=classes(M,*H[i])
                if len({cls[c] for c in curs})>1: amb=True; break
            if amb: break
        if not amb:
            worst_n=n; break
    print(f"      universal stopping length (state pinned in every consistent machine) = {worst_n}")
    print(f"      auditor's proposed safe bound 2M-1 = {2*M-1}")
