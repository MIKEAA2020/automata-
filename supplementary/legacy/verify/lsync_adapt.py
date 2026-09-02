"""L_sync^adapt(A): adaptive homing length for a KNOWN minimal Mealy machine
with unknown initial state.  Game: learner picks input x; adversary picks an
output o realizable from the current uncertainty set U; U <- {tau(s,x) :
s in U, lambda(s,x)=o}.  Done when U is a single observational class.

Since Lsync(M) = sup_A L_sync^adapt(A) <= Lsyncu(M), any family forcing
omega(M log M) here answers the open problem's first branch.
"""
import itertools, sys
from functools import lru_cache

def obs_classes(nS, nI, tau, lam, depth=None):
    """Myhill-Nerode classes of states by output behaviour."""
    if depth is None: depth = nS
    sig = {}
    for s in range(nS):
        out = []
        for L in range(1, depth+1):
            for w in itertools.product(range(nI), repeat=L):
                c = s
                for a in w:
                    out.append(lam[c][a]); c = tau[c][a]
        sig[s] = tuple(out)
    rep = {}
    for s in range(nS): rep[s] = sig[s]
    return rep

def adaptive_homing(nS, nI, tau, lam, cap=200):
    rep = obs_classes(nS, nI, tau, lam)
    @lru_cache(maxsize=None)
    def val(U):
        cur = set(rep[s] for s in U)
        if len(cur) <= 1: return 0
        best = None
        for a in range(nI):
            worst = 0
            outs = set(lam[s][a] for s in U)
            for o in outs:
                nxt = frozenset(tau[s][a] for s in U if lam[s][a] == o)
                if nxt == U:            # no progress on this branch
                    worst = cap; break
                worst = max(worst, 1 + val(nxt))
            if best is None or worst < best: best = worst
        return best if best is not None else cap
    v = val(frozenset(range(nS)))
    return v

def enumerate_max(nS, nI, nO, limit=None):
    best = -1; arg = None; seen = 0
    taus = itertools.product(itertools.product(range(nS), repeat=nI), repeat=nS)
    for tau in taus:
        for lamf in itertools.product(itertools.product(range(nO), repeat=nI), repeat=nS):
            seen += 1
            if limit and seen > limit: return best, arg, seen, True
            rep = obs_classes(nS, nI, tau, lamf)
            if len(set(rep.values())) < nS: continue      # not minimal
            v = adaptive_homing(nS, nI, tau, lamf)
            if v >= 200: continue                          # no homing sequence
            if v > best: best, arg = v, (tau, lamf)
    return best, arg, seen, False

print(f"{'M':>3} {'|I|':>4} {'|O|':>4} {'max L_sync^adapt':>17} {'M(M-1)/2':>9} {'M log2 M':>9} {'machines':>10}")
rows=[]
for (nS,nI,nO) in [(2,1,2),(3,1,2),(4,1,2),(5,1,2),(6,1,2),(2,2,2),(3,2,2)]:
    import math
    b,arg,seen,tr = enumerate_max(nS,nI,nO, limit=4_000_000)
    rows.append((nS,nI,nO,b))
    print(f"{nS:>3} {nI:>4} {nO:>4} {b:>17} {nS*(nS-1)//2:>9} {nS*math.log2(nS):>9.1f} {seen:>10}"
          f"{'  (truncated)' if tr else ''}")
    if arg and nS>=4:
        tau,lam=arg
        print(f"      extremal: tau={[t[0] for t in tau]}  lam={[l[0] for l in lam]}")
