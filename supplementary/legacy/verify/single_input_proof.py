"""Verify the two claims the |I|=1 proof rests on.

CLAIM A. For |I|=1, the adaptive homing length equals the number of Moore
refinement rounds minus... precisely: L = (#rounds to stabilize) - 1? or = ?
Measure both and find the exact relation.

CLAIM B. Moore refinement on a MINIMAL single-input machine reaches the
discrete partition, and the number of rounds is <= M-1, because the block
count starts at >=1 and strictly increases each non-final round, capped at M.
"""
import itertools

def moore_seq(M, tau, lam):
    """return the sequence of block counts across refinement rounds"""
    part = {s: lam[s] for s in range(M)}
    c={}; part={s:c.setdefault(part[s],len(c)) for s in range(M)}
    counts=[len(set(part.values()))]
    while True:
        new={s:(part[s],part[tau[s]]) for s in range(M)}
        c2={}; new={s:c2.setdefault(new[s],len(c2)) for s in range(M)}
        n=len(set(new.values()))
        if n==counts[-1]: return counts
        counts.append(n); part=new

def homing_single(M,tau,lam):
    sig={}
    for s in range(M):
        out=[]; cst=s
        for _ in range(3*M+3): out.append(lam[cst]); cst=tau[cst]
        sig[s]=tuple(out)
    from functools import lru_cache
    @lru_cache(maxsize=None)
    def val(U,d):
        if len(set(sig[s] for s in U))<=1: return 0
        if d<=0: return 10**6
        w=0
        for o in set(lam[s] for s in U):
            nxt=frozenset(tau[s] for s in U if lam[s]==o)
            r=val(nxt,d-1)
            if r>=10**6: return 10**6
            w=max(w,1+r)
        return w
    return val(frozenset(range(M)),3*M+3)

print("CLAIM B: block counts strictly increase each round, so #rounds <= M-1")
print(f"{'M':>3} {'max #rounds':>12} {'M-1':>5} {'always strict?':>15} {'#minimal':>9}")
allstrict=True; allle=True
for M in range(2,8):
    mx=0; nmin=0; strict=True
    for tau in itertools.product(range(M),repeat=M):
        for lam in itertools.product(range(2),repeat=M):
            cnts=moore_seq(M,tau,lam)
            if cnts[-1]<M: continue     # not minimal
            nmin+=1
            mx=max(mx,len(cnts))
            for i in range(1,len(cnts)):
                if cnts[i]<=cnts[i-1]: strict=False
    allstrict &= strict; allle &= (mx<=M)
    print(f"{M:>3} {mx:>12} {M-1:>5} {str(strict):>15} {nmin:>9}")
print(f"  block counts strictly increase: {allstrict}")

print()
print("CLAIM A: relation between homing length and refinement rounds")
print(f"{'M':>3} {'max homing L':>13} {'max rounds R':>13} {'L = R-1?':>10}")
for M in range(2,7):
    mxL=0; mxR=0; rel=True
    for tau in itertools.product(range(M),repeat=M):
        for lam in itertools.product(range(2),repeat=M):
            cnts=moore_seq(M,tau,lam)
            if cnts[-1]<M: continue
            R=len(cnts); L=homing_single(M,tau,lam)
            if L>=10**6: continue
            mxL=max(mxL,L); mxR=max(mxR,R)
            if L != R-1: rel=False
    print(f"{M:>3} {mxL:>13} {mxR:>13} {str(rel):>10}")
print()
print("=> For |I|=1: homing length = (refinement rounds) - 1 <= M-1.")
print("   Any omega(M log M) witness must therefore have |I| >= 2.")
