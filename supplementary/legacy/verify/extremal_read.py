"""Read the ACTUAL M=4 extremal machine and trace why it costs 6."""
import itertools
tau=[[0,0],[0,2],[3,3],[2,1]]
lam=[[0,0],[1,0],[0,0],[0,0]]
M=4
print("M=4 extremal:  tau =",tau,"  lam =",lam)
print()
print("input 0: s ->", [tau[s][0] for s in range(M)], " outputs", [lam[s][0] for s in range(M)])
print("input 1: s ->", [tau[s][1] for s in range(M)], " outputs", [lam[s][1] for s in range(M)])
print()
print("Only input 0 from state 1 emits 1; every other (state,input) emits 0.")
print("So the ONLY way to learn anything is to play input 0 while the true")
print("state might be 1.  input 1 permutes: 0->0, 1->2, 2->3, 3->1  (3-cycle).")
print()
# trace the optimal game
sig={}
for s in range(M):
    o=[]
    for L in range(1,M+1):
        for w in itertools.product(range(2),repeat=L):
            c=s
            for a in w: o.append(lam[c][a]); c=tau[c][a]
    sig[s]=tuple(o)
memo={}
def val(U,seen):
    if U in memo: return memo[U]
    if len(set(sig[s] for s in U))<=1: return 0
    if U in seen: return 10**6
    best=10**6; arg=None
    for a in range(2):
        w=0; br={}
        for o in set(lam[s][a] for s in U):
            nxt=frozenset(tau[s][a] for s in U if lam[s][a]==o)
            r=val(nxt,seen|{U})
            br[o]=(nxt,r)
            if r>=10**6: w=10**6; break
            w=max(w,1+r)
        if w<best: best,arg=w,(a,br)
    memo[U]=best
    return best
top=val(frozenset(range(M)),frozenset())
print(f"optimal adaptive homing length = {top}  (= binom(4,2) = 6)")
print()
print("Optimal play, worst-case branch:")
U=frozenset(range(M)); step=0
while len(set(sig[s] for s in U))>1 and step<12:
    best=None
    for a in range(2):
        w=0; br={}
        ok=True
        for o in set(lam[s][a] for s in U):
            nxt=frozenset(tau[s][a] for s in U if lam[s][a]==o)
            r=memo.get(nxt, val(nxt,frozenset()))
            br[o]=(nxt,r)
            if r>=10**6: ok=False; break
            w=max(w,1+r)
        if ok and (best is None or w<best[0]): best=(w,a,br)
    w,a,br=best
    worst_o=max(br, key=lambda o: br[o][1])
    nxt,r=br[worst_o]
    step+=1
    print(f"  step {step}: play input {a}; worst output {worst_o}; "
          f"U {sorted(U)} -> {sorted(nxt)}   (remaining cost {r})")
    U=nxt
