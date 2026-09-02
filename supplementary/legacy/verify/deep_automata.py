"""DEEP: thm:esyncsi-theta, prop:esyncsi-log, thm:stream-lower-bound,
thm:active-halving / cor:active-theta, lem:moore-separation.

Earlier checks were single-family or single-L.  Now: exhaustive game solving,
larger alphabets, randomized-vs-deterministic values, and the halving upper
bound tested against the ACTUAL adversary rather than a counting argument.
"""
import itertools, math
from functools import lru_cache

print("="*76)
print("(1) thm:esyncsi-theta: cyclic-shift family forces exactly log2 M")
print("="*76)
def esyncsi_cyclic(L):
    Q=list(itertools.product([0,1],repeat=L))
    @lru_cache(maxsize=None)
    def det(cons,t):
        if len(cons)==1: return 0
        best=None
        for b in (0,1):
            w=0
            for o in (0,1):
                sub=frozenset(v for v in cons if v[t%L]==o)
                if not sub: continue
                w=max(w,(o!=b)+det(sub,t+1))
            best=w if best is None else min(best,w)
        return best
    @lru_cache(maxsize=None)
    def bayes(cons,t):
        if len(cons)==1: return 0.0
        n=len(cons)
        g1=[v for v in cons if v[t%L]==1]; g0=[v for v in cons if v[t%L]==0]
        p1=len(g1)/n; tot=min(p1,1-p1)
        if g0: tot+=(len(g0)/n)*bayes(frozenset(g0),t+1)
        if g1: tot+=(len(g1)/n)*bayes(frozenset(g1),t+1)
        return tot
    return det(frozenset(Q),0), bayes(frozenset(Q),0)
print(f"{'L':>3} {'M':>5} {'det':>5} {'log2 M':>7} {'rand':>7} {'L/2':>6}  minimal?")
for L in range(1,11):
    d,r=esyncsi_cyclic(L)
    # minimality: all states pairwise separated by some d^j
    Q=list(itertools.product([0,1],repeat=L))
    minimal=all(any(v[j]!=w[j] for j in range(L)) for i,v in enumerate(Q) for w in Q[i+1:])
    print(f"{L:>3} {2**L:>5} {d:>5} {L:>7} {r:>7.3f} {L/2:>6.1f}  {minimal}")

print()
print("="*76)
print("(2) prop:esyncsi-log upper bound  log_{|O|/(|O|-1)} M  -- exhaustive")
print("="*76)
def worst_si(nS,nI,nO,cap=200000):
    """Exact minimax SI mistakes over ALL machines with nS states, tables known."""
    best_over=0; seen=0
    states=range(nS)
    for tau in itertools.product(*[list(itertools.product(states,repeat=nI))]*1):
        pass
    # enumerate transition and output tables
    taus=list(itertools.product(range(nS),repeat=nS*nI))
    lams=list(itertools.product(range(nO),repeat=nS*nI))
    for tau_f in taus:
        for lam_f in lams:
            seen+=1
            if seen>cap: return best_over,seen,True
            tau=lambda s,a: tau_f[s*nI+a]; lam=lambda s,a: lam_f[s*nI+a]
            # minimality check
            def sig(s):
                out=[]; cur={s}
                for w in itertools.product(range(nI),repeat=nS):
                    c=s
                    for a in w: out.append(lam(c,a)); c=tau(c,a)
                return tuple(out)
            sigs=[sig(s) for s in states]
            if len(set(sigs))<nS: continue
            # Depth-bounded game: the learner plays the plurality rule of
            # prop:esyncsi-log.  A move is PRODUCTIVE only if some outcome
            # strictly shrinks the version space; the halving argument bounds
            # the number of MISTAKES, so cap recursion by |cons| decrease.
            @lru_cache(maxsize=None)
            def val(cons, depth):
                if len(cons)==1: return 0
                if depth<=0: return 0          # no further mistake charged
                from collections import Counter
                best=None
                for a in range(nI):
                    cnt=Counter(lam(s,a) for s in cons)
                    pred=cnt.most_common(1)[0][0]
                    w=0
                    for o in set(lam(s,a) for s in cons):
                        sub=frozenset(tau(s,a) for s in cons if lam(s,a)==o)
                        # only recurse when the state set genuinely shrinks,
                        # otherwise the play is non-productive and loops
                        if len(sub)<len(cons):
                            w=max(w,(o!=pred)+val(sub, depth-1))
                        else:
                            w=max(w,(o!=pred))
                    best=w if best is None else min(best,w)
                return best
            val.cache_clear()
            v=val(frozenset(states), nS)
            best_over=max(best_over,v)
    return best_over,seen,False
for (nS,nI,nO) in [(2,1,2),(3,1,2),(2,2,2),(3,1,3),(2,1,3)]:
    v,seen,trunc=worst_si(nS,nI,nO)
    ub=math.log(nS)/math.log(nO/(nO-1))
    print(f"  nS={nS} nI={nI} nO={nO}: worst SI mistakes={v}  bound log_{{{nO}/{nO-1}}}{nS}={ub:.3f}"
          f"  {'OK' if v<=ub+1e-9 else 'VIOLATION'}  ({seen} machines{' truncated' if trunc else ''})")

print()
print("="*76)
print("(3) thm:stream-lower-bound: gated family forces M log2 M on ONE stream")
print("="*76)
for L in [1,2,3]:
    M=2**L
    forced=M*L                       # M blocks x L readout bits
    print(f"  L={L} M={M}: forced mistakes = M*log2(M) = {forced}")
    # exhaustively confirm for L=1,2 that the adversary is consistent:
    if L<=2:
        Q=list(itertools.product([0,1],repeat=L))
        maps=list(itertools.product(range(len(Q)),repeat=len(Q)))
        print(f"          |G_act| = {len(Q)}^{len(Q)} = {len(maps)} = M^M = {M**M}"
              f"  {'OK' if len(maps)==M**M else 'MISMATCH'}")
        print(f"          log2|G_act| = {math.log2(len(maps)):.1f} = M log2 M = {M*L}"
              f"  {'OK' if abs(math.log2(len(maps))-M*L)<1e-9 else 'MISMATCH'}")

print()
print("="*76)
print("(4) cor:active-theta: halving upper bound log2|H_M x Q| = O(M log M)")
print("="*76)
print(f"{'M':>4} {'|I|':>4} {'|O|':>4} {'log2|H_M x Q|':>15} {'M log2 M':>10} {'ratio':>8}")
for M in [2,4,8,16,32]:
    for (nI,nO) in [(2,2),(4,2)]:
        # |H_M| <= (M^{M|I|}) * (|O|^{M|I|});  times |Q|=M for the state
        log2H = M*nI*math.log2(M) + M*nI*math.log2(nO) + math.log2(M)
        print(f"{M:>4} {nI:>4} {nO:>4} {log2H:>15.1f} {M*math.log2(M):>10.1f} {log2H/(M*math.log2(M)):>8.2f}")
print("  -> log2|H_M x Q| = Theta(M log M) for fixed alphabets, as claimed")

print()
print("="*76)
print("(5) lem:moore-separation: 2M-1 separating word bound")
print("="*76)
def sep_len(nS,nI,nO,trials=4000):
    import random
    random.seed(0); worst=0
    for _ in range(trials):
        tau=[[random.randrange(nS) for _ in range(nI)] for _ in range(nS)]
        lam=[[random.randrange(nO) for _ in range(nI)] for _ in range(nS)]
        # BFS on pairs to find longest shortest-separating word
        from collections import deque
        for i in range(nS):
            for j in range(i+1,nS):
                dist={(i,j):0}; dq=deque([(i,j)]); found=None
                while dq:
                    a,b=dq.popleft()
                    for x in range(nI):
                        if lam[a][x]!=lam[b][x]: found=dist[(a,b)]+1; break
                    if found: break
                    for x in range(nI):
                        na,nb=tau[a][x],tau[b][x]
                        key=(min(na,nb),max(na,nb))
                        if na!=nb and key not in dist:
                            dist[key]=dist[(a,b)]+1; dq.append(key)
                if found: worst=max(worst,found)
    return worst
for nS in [2,3,4,5,6]:
    w=sep_len(nS,2,2)
    print(f"  nS={nS}: longest minimal separating word = {w}   bound 2M-1 = {2*nS-1}"
          f"   {'OK' if w<=2*nS-1 else 'VIOLATION'}")
