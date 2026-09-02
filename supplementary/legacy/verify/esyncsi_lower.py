import itertools
# Cyclic-shift family: Q={0,1}^L, input d, tau(v,d)=left cyclic shift, lambda(v,d)=v_1.
# Tables KNOWN, initial state unknown. Objective (SI): pin down current state.
# Learner predicts the output each round before seeing it. Count mistakes.
def run(L):
    Q=list(itertools.product([0,1],repeat=L))
    # Deterministic learner vs adversary: game on the set of consistent states.
    from functools import lru_cache
    @lru_cache(maxsize=None)
    def val(cons,t):
        # cons: frozenset of ORIGINAL initial states still consistent; t = #steps taken
        if len(cons)==1: return 0
        # learner predicts bit b for output of round t (which is v_{t+1} of the initial state)
        best=None
        for b in (0,1):
            # adversary picks actual output o; mistakes += (o!=b)
            worst=0
            for o in (0,1):
                sub=frozenset(v for v in cons if v[t%L]==o)
                if not sub: continue
                worst=max(worst,(o!=b)+val(sub,t+1))
            best=worst if best is None else min(best,worst)
        return best
    det=val(frozenset(Q),0)
    # randomized (learner may randomize): value of the zero-sum game = expected mistakes
    # under uniform prior each fresh bit is fair -> L/2 ; compute Bayes-optimal expected mistakes
    @lru_cache(maxsize=None)
    def bayes(cons,t):
        if len(cons)==1: return 0.0
        n=len(cons); tot=0.0
        g0=[v for v in cons if v[t%L]==0]; g1=[v for v in cons if v[t%L]==1]
        p1=len(g1)/n
        # optimal prediction minimizes expected mistake: min(p1,1-p1)
        exp_mis=min(p1,1-p1)
        if g0: tot+=(len(g0)/n)*bayes(frozenset(g0),t+1)
        if g1: tot+=(len(g1)/n)*bayes(frozenset(g1),t+1)
        return exp_mis+tot
    ran=bayes(frozenset(Q),0)
    return det,ran

print(f"{'L':>3} {'M=2^L':>7} {'det mistakes':>14} {'log2 M':>8} {'randomized (uniform prior)':>28} {'L/2':>6}")
for L in range(1,10):
    d,r=run(L)
    print(f"{L:>3} {2**L:>7} {d:>14} {L:>8} {r:>28.4f} {L/2:>6.1f}")
print("\n=> EsyncSI(M) = log_2 M exactly for deterministic learners on this family;")
print("   >= (1/2) log_2 M for randomized.  Matches upper bound prop:esyncsi-log => Theta(log M).")
