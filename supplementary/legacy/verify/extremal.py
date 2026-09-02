"""Extract the machines attaining binom(M,2) at M=3,4 and read their structure."""
import itertools
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
        o=[]
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

for (M,nI,nO) in [(3,2,2),(4,2,2)]:
    target=M*(M-1)//2
    found=[]
    for tau in itertools.product(itertools.product(range(M),repeat=nI),repeat=M):
        for lam in itertools.product(itertools.product(range(nO),repeat=nI),repeat=M):
            if not minimal(M,nI,tau,lam): continue
            if homing(M,nI,tau,lam)==target:
                found.append((tau,lam))
    print("="*72)
    print(f"M={M}, |I|={nI}, |O|={nO}: {len(found)} machines attain binom({M},2)={target}")
    print("="*72)
    for tau,lam in found[:3]:
        print("  tau (state -> [in0,in1]):", [list(t) for t in tau])
        print("  lam (state -> [in0,in1]):", [list(l) for l in lam])
        # describe: is one input a permutation? a reset? 
        for a in range(nI):
            img=[tau[s][a] for s in range(M)]
            kind = "permutation" if len(set(img))==M else f"collapsing (image size {len(set(img))})"
            outs=[lam[s][a] for s in range(M)]
            print(f"     input {a}: {img}  {kind}; outputs {outs}")
        print()
