"""Search for a family with L_sync^adapt = omega(M log M).

Candidate: the classical "counter/chain" worst cases for homing sequences.
Known extremal structure (Lee-Yannakakis style): a machine where only ONE
pair is distinguishable per phase, forcing sequential elimination.

Construction attempt: states 0..M-1 on a single input 'a' acting as a cyclic
counter, with output 1 only at state 0.  Uncertainty shrinks by 1 per full
revolution => length ~ M per elimination => Theta(M^2)?
"""
import itertools, math, sys
sys.setrecursionlimit(100000)

def homing_len(nS, tau, lam, nI=1, cap=10**7):
    """adaptive homing length for single/multi input machine given as lists"""
    def sig(s):
        out=[]
        c=s
        for _ in range(2*nS):
            out.append(lam[c][0]); c=tau[c][0]
        return tuple(out)
    S={s:sig(s) for s in range(nS)}
    memo={}
    def val(U,seen):
        if U in memo: return memo[U]
        if len(set(S[s] for s in U))<=1: return 0
        if U in seen: return cap
        best=cap
        for a in range(nI):
            worst=0
            for o in set(lam[s][a] for s in U):
                nxt=frozenset(tau[s][a] for s in U if lam[s][a]==o)
                r=val(nxt,seen|{U})
                if r>=cap: worst=cap; break
                worst=max(worst,1+r)
            best=min(best,worst)
        memo[U]=best
        return best
    return val(frozenset(range(nS)),frozenset())

print("FAMILY 1: cyclic counter, output 1 only at state 0, single input")
print(f"  {'M':>4} {'L_adapt':>9} {'M log2 M':>10} {'M(M-1)/2':>10} {'L/(M log2 M)':>13}")
for M in range(2,13):
    tau=[[(s+1)%M] for s in range(M)]
    lam=[[1 if s==0 else 0] for s in range(M)]
    L=homing_len(M,tau,lam)
    if L>=10**7: print(f"  {M:>4} {'no homing':>9}"); continue
    print(f"  {M:>4} {L:>9} {M*math.log2(M):>10.1f} {M*(M-1)//2:>10} {L/(M*math.log2(M)):>13.3f}")

print()
print("FAMILY 2: cyclic shift on {0,1}^L reading one bit per step (the EsyncSI family)")
print(f"  {'L':>3} {'M':>5} {'L_adapt':>9} {'M log2 M':>10} {'log2 M':>8}")
for Lb in range(1,6):
    M=2**Lb
    Q=list(itertools.product([0,1],repeat=Lb))
    idx={q:i for i,q in enumerate(Q)}
    tau=[[idx[q[1:]+q[:1]]] for q in Q]
    lam=[[q[0]] for q in Q]
    v=homing_len(M,tau,lam)
    print(f"  {Lb:>3} {M:>5} {v:>9} {M*math.log2(M):>10.1f} {Lb:>8}")

print()
print("FAMILY 3: 'slow counter' -- output reveals a bit only every other step")
print(f"  {'M':>4} {'L_adapt':>9} {'M log2 M':>10} {'ratio':>8}")
for M in range(4,15,2):
    tau=[[(s+1)%M] for s in range(M)]
    lam=[[1 if s==0 else 0] for s in range(M)]
    L=homing_len(M,tau,lam)
    if L<10**7:
        print(f"  {M:>4} {L:>9} {M*math.log2(M):>10.1f} {L/(M*math.log2(M)):>8.3f}")
