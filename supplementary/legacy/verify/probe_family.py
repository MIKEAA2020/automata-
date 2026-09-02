"""The 'rotate-past-a-single-probe' family, built to match the M=4 extremal.

Structure (read off M=4: tau0=[0,0,3,2], tau1=[0,2,3,1], lam0=[0,1,0,0]):
  - state 0 is an absorbing sink (both inputs -> 0, output 0)
  - input 1 acts on {1,...,M-1} as the cycle 1->2->...->(M-1)->1, fixes 0
  - input 0 sends 1 -> 0 (emitting 1, the ONLY informative output),
    and acts as an involution/permutation on {2,...,M-1}, fixes 0
  - all other outputs are 0

So the learner can only test "is the true state currently at the probe
position 1?".  A negative answer removes one candidate; input 1 rotates the
rest.  Cost per elimination ~ distance to the probe.
"""
import itertools, math, sys
sys.setrecursionlimit(200000)
from collections import deque

def build(M, tau0_rest):
    """tau0_rest: permutation of {2..M-1} as a dict; state1 -> 0 under input 0"""
    tau=[[0,0] for _ in range(M)]
    lam=[[0,0] for _ in range(M)]
    tau[0]=[0,0]
    for s in range(1,M):
        tau[s][1] = 1 + (s % (M-1)) if M>2 else 0     # cycle on 1..M-1
    for s in range(1,M):
        tau[s][0] = 0 if s==1 else tau0_rest.get(s,s)
    lam[1][0]=1
    return tau,lam

def minimal(M,tau,lam):
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
            for w in itertools.product(range(2),repeat=min(L,2)):
                c=s
                for _ in range(L):
                    for a in w: o.append(lam[c][a]); c=tau[c][a]
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

# match M=4 exactly: tau0 = [0,0,3,2] -> on {2,3} it's the swap 2<->3
print("Variant A: input 0 swaps adjacent pairs on {2..M-1} (matches M=4)")
print(f"{'M':>3} {'min?':>5} {'L':>5} {'binom':>6} {'MlogM':>7} {'L/(MlogM)':>10} {'L/M^2':>7}")
for M in range(3,14):
    rest={}
    xs=list(range(2,M))
    for i in range(0,len(xs)-1,2):
        rest[xs[i]]=xs[i+1]; rest[xs[i+1]]=xs[i]
    tau,lam=build(M,rest)
    if not minimal(M,tau,lam):
        print(f"{M:>3} {'no':>5}  (not minimal)"); continue
    L=homing(M,tau,lam)
    Ls='inf' if L>=10**7 else str(L)
    r1=(L/(M*math.log2(M))) if L<10**7 else float('nan')
    r2=(L/M**2) if L<10**7 else float('nan')
    print(f"{M:>3} {'yes':>5} {Ls:>5} {M*(M-1)//2:>6} {M*math.log2(M):>7.1f} {r1:>10.3f} {r2:>7.3f}")
