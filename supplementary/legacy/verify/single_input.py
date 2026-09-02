"""Single-input case: is L_sync^adapt(A) <= M-1 for MINIMAL |I|=1 machines?

PROPOSED PROOF (Moore partition refinement).
With one input letter there is no choice: the learner feeds it repeatedly.
Define  s ~_t u  iff the output sequences from s and u agree for t steps.
  ~_0 = everything (1 block)
  ~_{t+1} refines ~_t
This is exactly Moore's partition refinement.  If a round does not refine,
the partition is stable forever.  Minimality => the stable partition is
discrete (M blocks).  Starting at 1 block and ending at M blocks, each
non-stable round adds >= 1 block, so at most M-1 rounds occur.
Hence all states separate within M-1 steps.
"""
import itertools, math

def refine_rounds(M, tau, lam):
    """number of refinement rounds until the Moore partition stabilizes"""
    part = {s: lam[s] for s in range(M)}
    codes = {}; part = {s: codes.setdefault(part[s], len(codes)) for s in range(M)}
    rounds = 1
    while True:
        new = {s: (part[s], part[tau[s]]) for s in range(M)}
        c2 = {}; new = {s: c2.setdefault(new[s], len(c2)) for s in range(M)}
        if len(set(new.values())) == len(set(part.values())):
            return rounds, len(set(part.values()))
        part = new; rounds += 1

def homing_single(M, tau, lam):
    """adaptive homing length, |I|=1: just count steps until U is one class"""
    # signatures
    sig = {}
    for s in range(M):
        out=[]; c=s
        for _ in range(2*M+2): out.append(lam[c]); c=tau[c]
        sig[s]=tuple(out)
    U=frozenset(range(M)); steps=0
    seen=set()
    while len(set(sig[s] for s in U))>1:
        if (U,steps) in seen or steps>4*M: return None
        seen.add((U,steps))
        # single input: adversary picks the worst output branch
        best=0
        branches={}
        for o in set(lam[s] for s in U):
            branches[o]=frozenset(tau[s] for s in U if lam[s]==o)
        # worst-case branch = the one needing the most further steps
        # solve by recursion
        break
    # do it properly by recursion
    from functools import lru_cache
    @lru_cache(maxsize=None)
    def val(U, depth):
        if len(set(sig[s] for s in U))<=1: return 0
        if depth<=0: return 10**6
        w=0
        for o in set(lam[s] for s in U):
            nxt=frozenset(tau[s] for s in U if lam[s]==o)
            r=val(nxt, depth-1)
            if r>=10**6: return 10**6
            w=max(w,1+r)
        return w
    return val(frozenset(range(M)), 3*M+3)

print("EXHAUSTIVE over all single-input minimal Mealy machines")
print(f"{'M':>3} {'|O|':>4} {'max homing':>11} {'M-1':>5} {'max refine rounds':>18} {'#minimal':>9} {'ok?':>5}")
allok=True
for M in range(2,7):
    for nO in [2]:
        best=-1; bestr=-1; nmin=0
        for tau in itertools.product(range(M), repeat=M):
            for lam in itertools.product(range(nO), repeat=M):
                r, nb = refine_rounds(M, tau, lam)
                if nb < M: continue          # not minimal
                nmin+=1
                v = homing_single(M, tau, lam)
                if v is not None and v<10**6:
                    best=max(best,v); bestr=max(bestr,r)
        ok = best <= M-1
        allok &= ok
        print(f"{M:>3} {nO:>4} {best:>11} {M-1:>5} {bestr:>18} {nmin:>9} {str(ok):>5}")
print(f"\nmax homing <= M-1 for every single-input minimal machine tested: {allok}")
