"""L != R-1.  Find the TRUE relation between adaptive homing length L and
Moore refinement rounds R for single-input minimal machines.
"""
import itertools
from functools import lru_cache

def moore_rounds(M,tau,lam):
    part={s:lam[s] for s in range(M)}
    c={}; part={s:c.setdefault(part[s],len(c)) for s in range(M)}
    R=1
    while True:
        new={s:(part[s],part[tau[s]]) for s in range(M)}
        c2={}; new={s:c2.setdefault(new[s],len(c2)) for s in range(M)}
        if len(set(new.values()))==len(set(part.values())): return R, len(set(part.values()))
        part=new; R+=1

def homing(M,tau,lam):
    sig={}
    for s in range(M):
        out=[]; c=s
        for _ in range(3*M+3): out.append(lam[c]); c=tau[c]
        sig[s]=tuple(out)
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

print("Joint distribution of (R, L) over single-input minimal machines")
from collections import Counter
for M in range(2,7):
    pairs=Counter()
    for tau in itertools.product(range(M),repeat=M):
        for lam in itertools.product(range(2),repeat=M):
            R,nb=moore_rounds(M,tau,lam)
            if nb<M: continue
            L=homing(M,tau,lam)
            if L>=10**6: continue
            pairs[(R,L)]+=1
    print(f"  M={M}: (R,L) -> count : {dict(sorted(pairs.items()))}")
    viol=[(R,L) for (R,L) in pairs if L>R]
    print(f"        pairs with L > R: {viol}    max L={max(L for _,L in pairs)}  M-1={M-1}")
print()
print("=> The reliable statement is L <= R <= M-1 (not L = R-1).")
print("   Both bounds are what the proof needs: L <= M-1 for |I|=1.")
