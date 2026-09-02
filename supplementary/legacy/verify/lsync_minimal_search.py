"""Redo the search enforcing MINIMALITY (Myhill-Nerode distinct states).

Lsyncu / Lsync are defined over H_M = machines with at most M states, and
Definition def:output-aware-sync reads identification up to observational
equivalence.  A non-minimal machine has fewer classes, so its 'homing length'
in the previous script was measured against |U|=1 rather than one CLASS --
that inflated the numbers.  Enforce minimality and re-measure.
"""
import random, math, itertools, sys
sys.setrecursionlimit(100000)

def sigs(M,nI,tau,lam):
    """Myhill-Nerode signature via Moore partition refinement."""
    part={s: lam[s][0] if nI==1 else tuple(lam[s]) for s in range(M)}
    for _ in range(M):
        new={s: (part[s], tuple(part[tau[s][a]] for a in range(nI))) for s in range(M)}
        # canonicalize
        codes={}; out={}
        for s in range(M):
            codes.setdefault(new[s],len(codes)); out[s]=codes[new[s]]
        if out==part: break
        part=out
    return part

def is_minimal(M,nI,tau,lam):
    return len(set(sigs(M,nI,tau,lam).values()))==M

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

def search(M,nI,nO,iters,restarts,seed):
    rng=random.Random(seed); best=-1; arg=None
    for _ in range(restarts):
        # start from a random MINIMAL machine
        for _try in range(500):
            tau=[[rng.randrange(M) for _ in range(nI)] for _ in range(M)]
            lam=[[rng.randrange(nO) for _ in range(nI)] for _ in range(M)]
            if is_minimal(M,nI,tau,lam): break
        else: continue
        cur=homing_len(M,nI,tau,lam); cur = -1 if cur>=10**7 else cur
        for _ in range(iters):
            s=rng.randrange(M); a=rng.randrange(nI); which=rng.random()<0.5
            old=tau[s][a] if which else lam[s][a]
            new=rng.randrange(M) if which else rng.randrange(nO)
            if which: tau[s][a]=new
            else:     lam[s][a]=new
            if not is_minimal(M,nI,tau,lam):
                if which: tau[s][a]=old
                else: lam[s][a]=old
                continue
            v=homing_len(M,nI,tau,lam); v = -1 if v>=10**7 else v
            if v>=cur: cur=v
            else:
                if which: tau[s][a]=old
                else: lam[s][a]=old
        if cur>best: best,arg=cur,([r[:] for r in tau],[r[:] for r in lam])
    return best,arg

print("Hill-climbing over MINIMAL machines only")
print(f"{'M':>4} {'|I|':>4} {'best L':>7} {'M-1':>5} {'M(M-1)/2':>9} {'M log2 M':>9} {'L/(M log2M)':>12}")
for nI in [1,2]:
    for M in [4,6,8,10,12,14,16,20]:
        b,arg=search(M,nI,2,iters=600,restarts=4,seed=7*M+nI)
        if b<0: print(f"{M:>4} {nI:>4} {'none':>7}"); continue
        print(f"{M:>4} {nI:>4} {b:>7} {M-1:>5} {M*(M-1)//2:>9} {M*math.log2(M):>9.1f} {b/(M*math.log2(M)):>12.3f}")
    print()
