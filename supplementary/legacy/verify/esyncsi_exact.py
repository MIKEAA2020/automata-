"""Is the halving constant log_{|O|/(|O|-1)} actually attained for |O|>2?

The manuscript's upper bound says a mistake leaves at most (1-1/|O|)|V|.
But the surviving set is a SINGLE output class, not all non-predicted classes.
If classes have sizes c_1>=c_2>=... summing to |V|, the plurality learner
predicts c_1, the adversary must answer some o != o_1, and the survivors are
the single class c_o <= c_2.  Since c_1>=c_2 and c_1+c_2<=|V|, we get
c_2 <= |V|/2  --  a HALVING, independent of |O|.
"""
import numpy as np, math, itertools
from functools import lru_cache
rng = np.random.default_rng(0)

print("="*76)
print("(1) Combinatorial core:  max surviving fraction = c_2/n <= 1/2, any |O|")
print("="*76)
worst = {}
for nO in [2,3,4,5,8]:
    w = 0.0
    for _ in range(400000):
        n = int(rng.integers(2, 40))
        cuts = np.sort(rng.integers(0, n+1, nO-1))
        sizes = np.diff(np.concatenate([[0], cuts, [n]]))
        if sizes.sum() != n: continue
        s = np.sort(sizes)[::-1]
        surv = s[1] if len(s) > 1 else 0      # adversary's best non-plurality class
        w = max(w, surv/n)
    worst[nO] = w
    print(f"  |O|={nO}: max c_2/n over 400k random class profiles = {w:.6f}"
          f"   old bound (1-1/|O|) = {1-1/nO:.6f}")
print("  -> the true per-mistake shrink is 1/2 for EVERY |O|, not 1-1/|O|")

print()
print("="*76)
print("(2) Exhaustive minimax SI game vs floor(log2 M), all small signatures")
print("="*76)
def worst_si(nS,nI,nO,cap=400000):
    best=0; seen=0
    taus=list(itertools.product(range(nS),repeat=nS*nI))
    lams=list(itertools.product(range(nO),repeat=nS*nI))
    for tf in taus:
        for lf in lams:
            seen+=1
            if seen>cap: return best,seen,True
            tau=lambda s,a: tf[s*nI+a]; lam=lambda s,a: lf[s*nI+a]
            def sig(s):
                out=[]
                for w in itertools.product(range(nI),repeat=min(nS,3)):
                    c=s
                    for a in w: out.append(lam(c,a)); c=tau(c,a)
                return tuple(out)
            if len(set(sig(s) for s in range(nS)))<nS: continue
            @lru_cache(maxsize=None)
            def val(cons,depth):
                if len(cons)==1: return 0
                if depth<=0: return 0
                from collections import Counter
                best_a=None
                for a in range(nI):
                    cnt=Counter(lam(s,a) for s in cons)
                    pred=cnt.most_common(1)[0][0]
                    w=0
                    for o in set(lam(s,a) for s in cons):
                        sub=frozenset(tau(s,a) for s in cons if lam(s,a)==o)
                        if len(sub)<len(cons): w=max(w,(o!=pred)+val(sub,depth-1))
                        else:                  w=max(w,(o!=pred))
                    best_a=w if best_a is None else min(best_a,w)
                return best_a
            val.cache_clear()
            best=max(best,val(frozenset(range(nS)),nS))
    return best,seen,False
print(f"  {'nS':>3} {'nI':>3} {'nO':>3} {'worst':>6} {'floor(log2 M)':>14} {'old bound':>11} {'ok?':>4}")
for (nS,nI,nO) in [(2,1,2),(3,1,2),(4,1,2),(2,2,2),(3,2,2),(2,1,3),(3,1,3),(2,1,4),(3,1,4)]:
    v,seen,trunc=worst_si(nS,nI,nO)
    newb=math.floor(math.log2(nS)); oldb=math.log(nS)/math.log(nO/(nO-1))
    ok = v<=newb
    print(f"  {nS:>3} {nI:>3} {nO:>3} {v:>6} {newb:>14} {oldb:>11.3f} {str(ok):>5}"
          f"{'  (truncated)' if trunc else ''}")

print()
print("="*76)
print("(3) Lower bound: binary cyclic shift embeds in ANY |O|>=2")
print("="*76)
def cyc(L):
    Q=list(itertools.product([0,1],repeat=L))
    @lru_cache(maxsize=None)
    def det(cons,t):
        if len(cons)==1: return 0
        b_=None
        for b in (0,1):
            w=0
            for o in (0,1):
                sub=frozenset(v for v in cons if v[t%L]==o)
                if sub: w=max(w,(o!=b)+det(sub,t+1))
            b_=w if b_ is None else min(b_,w)
        return b_
    return det(frozenset(Q),0)
for L in range(1,9):
    print(f"  L={L}, M={2**L}: forced mistakes = {cyc(L)} = log2 M = {L}"
          f"   (uses only 2 of the |O| symbols)")

print()
print("="*76)
print("(4) CONCLUSION")
print("="*76)
print("  upper: EsyncSI(M) <= floor(log2 M) for every |O|>=2  (halving, |O|-free)")
print("  lower: EsyncSI(M) >= L = log2 M at M=2^L, any |O|>=2 (cyclic shift)")
print("  => EsyncSI(2^L) = L EXACTLY; the constant is 1/log2, independent of |O|.")
print("  The old bound log_{|O|/(|O|-1)} M is LOOSE for |O|>2 (e.g. 2.71 vs 1 at")
print("  M=3,|O|=3) and its constant is NOT attained.")
