"""CRITICAL CHECK: do my proofs bound Lsync (per-machine) or Lsyncu (universal)?

Lsync(M)  = sup_A min_{tree for A}   depth      -- tree MAY depend on A
Lsyncu(M) = min_{single tree} sup_A  depth      -- ONE tree for ALL of H_M

My proofs (prop:lsyncu-quadratic, prop:lsyncu-binomial) pick a separating word
using "the pair automaton" -- but WHICH machine's pair automaton?  A learner
facing an unknown A cannot run BFS on A's pair automaton.  So the strategy is
A-dependent, i.e. it bounds Lsync, not Lsyncu.

Test the gap directly on a small class: compute
   Lsync  = max over A of (optimal adaptive depth for that A)
   Lsyncu = min over universal input-strategies of (max over A of depth)
For |I|=1 there is only one strategy so they coincide.  For |I|=2 with a tiny
class we can enumerate universal trees of bounded depth.
"""
import itertools, sys
from collections import deque
sys.setrecursionlimit(100000)

def classes(M,nI,tau,lam):
    part={s:tuple(lam[s]) for s in range(M)}
    c={}; part={s:c.setdefault(part[s],len(c)) for s in range(M)}
    for _ in range(M):
        new={s:(part[s],tuple(part[tau[s][a]] for a in range(nI))) for s in range(M)}
        c2={}; new={s:c2.setdefault(new[s],len(c2)) for s in range(M)}
        if len(set(new.values()))==len(set(part.values())): break
        part=new
    return part

def minimal(M,nI,tau,lam):
    return len(set(classes(M,nI,tau,lam).values()))==M

def lsync_A(M,nI,tau,lam,cap=10**6):
    """per-machine optimal adaptive depth (tree may depend on A)"""
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

# Build a small class: all minimal M=3, |I|=2, |O|=2 machines
M,nI,nO=3,2,2
H=[]
for tau in itertools.product(itertools.product(range(M),repeat=nI),repeat=M):
    for lam in itertools.product(itertools.product(range(nO),repeat=nI),repeat=M):
        if minimal(M,nI,tau,lam): H.append((tau,lam))
print(f"class size |H_{M}| (minimal, |I|={nI}, |O|={nO}) = {len(H)}")
ls=[lsync_A(M,nI,t,l) for t,l in H]
ls=[x for x in ls if x<10**6]
print(f"Lsync(M) = sup_A (per-machine optimum) = {max(ls)}")

# Universal: ONE input sequence strategy, adaptive on OUTPUTS ONLY (not on A).
# A universal tree maps output-history -> next input.  Enumerate all such trees
# of depth <= D over binary outputs: 2^0+2^1+...+2^{D-1} internal nodes.
def universal_depth(strategy_fn, tau, lam, D):
    """depth at which the transcript pins the current state within THIS A"""
    cls=classes(M,nI,tau,lam)
    # states consistent with the observed transcript, for this A
    U=frozenset(range(M)); hist=()
    for step in range(D):
        if len(set(cls[s] for s in U))<=1: return step
        a=strategy_fn(hist)
        # adversary picks worst output branch
        best=0; worst_next=None
        for o in set(lam[s][a] for s in U):
            nxt=frozenset(tau[s][a] for s in U if lam[s][a]==o)
            if worst_next is None or len(nxt)>len(worst_next[0]):
                worst_next=(nxt,o)
        U,o=worst_next; hist=hist+(o,)
    return D if len(set(cls[s] for s in U))>1 else D

D=4
best_universal=None
count=0
for bits in itertools.product(range(nI), repeat=sum(2**k for k in range(D))):
    # map history (tuple of outputs) -> index into bits
    def strat(h, bits=bits):
        idx=0
        for k,o in enumerate(h):
            idx = sum(2**j for j in range(k+1)) + (idx*2+o) if False else idx
        # simple indexing: node id = (2^len(h) - 1) + int(bits of h)
        nid = (2**len(h)-1) + int(''.join(map(str,h)) or '0', 2) if h else 0
        return bits[min(nid, len(bits)-1)]
    worst=0
    for t,l in H:
        d=universal_depth(strat,t,l,D)
        worst=max(worst,d)
    count+=1
    if best_universal is None or worst<best_universal: best_universal=worst
    if count>=3000: break
print(f"best universal-tree worst-case depth (D<={D}, {count} trees sampled) = {best_universal}")
print()
print("If best_universal > Lsync, the two quantities genuinely differ and my")
print("proofs bound Lsync only.")
