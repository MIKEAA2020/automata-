"""Generalize the extremal machines to arbitrary M and measure the rate.

At M=4 the extremal tau is:
   input 1 (permutation): [0,2,3,1]  -- fixes 0, cycles (1 2 3)
   input 0 (collapsing) : [0,0,3,2]  -- merges 0,1 -> 0 ; swaps 2,3
   output: lam[s][0] = 1 iff s==1, else 0 ; lam[.][1] constant
At M=3:
   input 1: [0,2,1]  -- fixes 0, swaps (1 2)
   input 0: [0,0,2]  -- merges 0,1 -> 0 ; fixes 2
   output: lam[s][0] = 1 iff s==1

Read: state 0 is a SINK under the permutation's fixed point; the permutation
cycles the remaining M-1 states past the single "probe" position (state 1),
where input 0 reveals one bit and merges.  So each elimination costs a full
rotation ~ M-1 steps, and there are ~M eliminations => Theta(M^2)?

Build the family for general M and measure.
"""
import itertools, math, sys
sys.setrecursionlimit(100000)

def build(M):
    """input 1: fix 0, cycle 1->2->...->M-1->1 ; input 0: merge {0,1}->0, fix rest
       output on input 0: 1 iff s==1 ; on input 1: constant 0"""
    tau=[[0,0] for _ in range(M)]
    lam=[[0,0] for _ in range(M)]
    for s in range(M):
        # input 1 = permutation
        if s==0: tau[s][1]=0
        else:    tau[s][1]= 1 + (s-1+1)%(M-1)
        # input 0 = collapsing probe
        tau[s][0]= 0 if s in (0,1) else s
        lam[s][0]= 1 if s==1 else 0
        lam[s][1]= 0
    return tau,lam

def sep_ok(M,tau,lam):
    from collections import deque
    def sep(s,t):
        if s==t: return None
        seen={(min(s,t),max(s,t))}; dq=deque([(s,t,0)])
        while dq:
            a_,b_,d=dq.popleft()
            for x in range(2):
                if lam[a_][x]!=lam[b_][x]: return d+1
            for x in range(2):
                na,nb=tau[a_][x],tau[b_][x]
                k=(min(na,nb),max(na,nb))
                if na!=nb and k not in seen: seen.add(k); dq.append((na,nb,d+1))
        return None
    return all(sep(s,t) is not None for s in range(M) for t in range(s+1,M))

def homing(M,tau,lam,cap=10**7):
    sig={}
    for s in range(M):
        o=[]
        for L in range(1,2*M+2):
            c=s
            for _ in range(L): o.append(lam[c][0]); c=tau[c][0]
            c=s
            for _ in range(L): o.append(lam[c][1]); c=tau[c][1]
        sig[s]=tuple(o)
    memo={}
    def val(U,seen):
        if U in memo: return memo[U]
        if len(set(sig[s] for s in U))<=1: return 0
        if U in seen: return cap
        best=cap
        for a in range(2):
            w=0
            for o in set(lam[s][a] for s in U):
                nxt=frozenset(tau[s][a] for s in U if lam[s][a]==o)
                r=val(nxt,seen|{U})
                if r>=cap: w=cap; break
                w=max(w,1+r)
            best=min(best,w)
        memo[U]=best; return best
    return val(frozenset(range(M)),frozenset())

print(f"{'M':>3} {'minimal?':>9} {'L_adapt':>8} {'binom(M,2)':>11} {'M log2 M':>9} {'L/(M log2M)':>12} {'L/M^2':>7}")
for M in range(3,13):
    tau,lam=build(M)
    mn=sep_ok(M,tau,lam)
    L=homing(M,tau,lam)
    Ls = 'no homing' if L>=10**7 else str(L)
    r1 = (L/(M*math.log2(M))) if L<10**7 else float('nan')
    r2 = (L/M**2) if L<10**7 else float('nan')
    print(f"{M:>3} {str(mn):>9} {Ls:>8} {M*(M-1)//2:>11} {M*math.log2(M):>9.1f} {r1:>12.3f} {r2:>7.3f}")
