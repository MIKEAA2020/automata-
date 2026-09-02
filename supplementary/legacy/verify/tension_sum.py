"""Does the tension lemma give M(M-1)/2, beating (M-1)^2?

Episode accounting: U starts at size M.  Each episode costs d(U_i) steps and
strictly decreases |U|.  With d(U) <= M - |U| + 1:

  sizes visited are m = M, M-1, ..., 2  (at worst, dropping by 1 each time)
  total <= sum_{m=2}^{M} (M - m + 1) = sum_{j=1}^{M-1} j = M(M-1)/2.
"""
import itertools, math
from collections import deque

def sep_len(M,nI,tau,lam,s,t):
    if s==t: return None
    seen={(min(s,t),max(s,t))}; dq=deque([(s,t,0)])
    while dq:
        a_,b_,d=dq.popleft()
        for x in range(nI):
            if lam[a_][x]!=lam[b_][x]: return d+1
        for x in range(nI):
            na,nb=tau[a_][x],tau[b_][x]
            k=(min(na,nb),max(na,nb))
            if na!=nb and k not in seen: seen.add(k); dq.append((na,nb,d+1))
    return None

def minimal(M,nI,tau,lam):
    return all(sep_len(M,nI,tau,lam,s,t) is not None
               for s in range(M) for t in range(s+1,M))

def homing(M,nI,tau,lam,cap=10**6):
    sig={}
    for s in range(M):
        o=[]; 
        for L in range(1,M+1):
            for w in itertools.product(range(nI),repeat=L):
                c=s
                for a in w: o.append(lam[c][a]); c=tau[c][a]
        sig[s]=tuple(o)
    memo={}
    def val(U,seen):
        if U in memo: return memo[U]
        if len(set(sig[s] for s in U))<=1: return 0
        if U in seen: return cap
        best=cap
        for a in range(nI):
            w=0
            for o in set(lam[s][a] for s in U):
                nxt=frozenset(tau[s][a] for s in U if lam[s][a]==o)
                r=val(nxt,seen|{U})
                if r>=cap: w=cap; break
                w=max(w,1+r)
            best=min(best,w)
        memo[U]=best; return best
    return val(frozenset(range(M)),frozenset())

print("Arithmetic: sum_{m=2}^{M} (M-m+1) = M(M-1)/2 ?")
for M in range(2,12):
    s=sum(M-m+1 for m in range(2,M+1))
    print(f"  M={M:>2}: sum={s:>3}  M(M-1)/2={M*(M-1)//2:>3}  (M-1)^2={(M-1)**2:>3}  "
          f"{'MATCH' if s==M*(M-1)//2 else 'MISMATCH'}   improvement factor "
          f"{((M-1)**2)/(M*(M-1)/2) if M>1 else 0:.2f}x")

print()
print("Exhaustive: is actual homing length <= M(M-1)/2 (and <= the tension sum)?")
print(f"  {'M':>2} {'|I|':>4} {'|O|':>4} {'max L':>6} {'M(M-1)/2':>9} {'(M-1)^2':>8} {'ok':>4}")
allok=True
for (M,nI,nO) in [(2,1,2),(3,1,2),(4,1,2),(5,1,2),(2,2,2),(3,2,2),(4,2,2),(3,1,3),(4,1,3)]:
    best=-1
    for tau in itertools.product(itertools.product(range(M),repeat=nI),repeat=M):
        for lam in itertools.product(itertools.product(range(nO),repeat=nI),repeat=M):
            if not minimal(M,nI,tau,lam): continue
            v=homing(M,nI,tau,lam)
            if v<10**6: best=max(best,v)
    ok=best<=M*(M-1)//2; allok&=ok
    print(f"  {M:>2} {nI:>4} {nO:>4} {best:>6} {M*(M-1)//2:>9} {(M-1)**2:>8} {str(ok):>5}")
print(f"\n  all <= M(M-1)/2 : {allok}")
