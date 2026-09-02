"""Random + local search for machines maximizing L_sync^adapt / (M log2 M).

If a superlinearithmic family existed, hill-climbing on this ratio at
moderate M should show the ratio GROWING with M.  If it stays bounded (or
falls), that is evidence Lsyncu(M) = O(M log M) -- or at least that no
easily-constructed family beats it.
"""
import random, math, sys
sys.setrecursionlimit(100000)

def homing_len(nS,nI,tau,lam,cap=10**7):
    def sig(s):
        out=[]; frontier=[(s,)]
        # signature by BFS over words up to length nS (enough for minimality)
        c=s; seq=[]
        for _ in range(2*nS):
            seq.append(tuple(lam[c][a] for a in range(nI)))
            c=tau[c][0]
        return tuple(seq)
    S={s:sig(s) for s in range(nS)}
    memo={}
    def val(U,seen):
        if U in memo: return memo[U]
        if len(U)<=1: return 0
        if U in seen: return cap
        best=cap
        for a in range(nI):
            worst=0
            for o in set(lam[s][a] for s in U):
                nxt=frozenset(tau[s][a] for s in U if lam[s][a]==o)
                if nxt==U: worst=cap; break
                r=val(nxt,seen|{U})
                if r>=cap: worst=cap; break
                worst=max(worst,1+r)
            best=min(best,worst)
        memo[U]=best
        return best
    return val(frozenset(range(nS)),frozenset())

def rand_machine(M,nI,nO,rng):
    tau=[[rng.randrange(M) for _ in range(nI)] for _ in range(M)]
    lam=[[rng.randrange(nO) for _ in range(nI)] for _ in range(M)]
    return tau,lam

def search(M,nI,nO,iters=3000,restarts=8,seed=0):
    rng=random.Random(seed); best=-1; bestml=None
    for _ in range(restarts):
        tau,lam=rand_machine(M,nI,nO,rng)
        cur=homing_len(M,nI,tau,lam)
        if cur>=10**7: cur=-1
        for _ in range(iters):
            s=rng.randrange(M); a=rng.randrange(nI)
            which=rng.random()<0.5
            old=tau[s][a] if which else lam[s][a]
            new=rng.randrange(M) if which else rng.randrange(nO)
            if which: tau[s][a]=new
            else:     lam[s][a]=new
            v=homing_len(M,nI,tau,lam)
            if v>=10**7: v=-1
            if v>=cur: cur=v
            else:
                if which: tau[s][a]=old
                else:     lam[s][a]=old
        if cur>best: best,bestml=cur,([r[:] for r in tau],[r[:] for r in lam])
    return best,bestml

print("Hill-climbing on L_sync^adapt, binary alphabets")
print(f"{'M':>4} {'best L':>7} {'M-1':>5} {'M log2 M':>9} {'L/(M log2 M)':>13} {'L/M':>6}")
for M in [4,6,8,10,12,14,16]:
    b,ml=search(M,2,2,iters=1200,restarts=5,seed=M)
    print(f"{M:>4} {b:>7} {M-1:>5} {M*math.log2(M):>9.1f} {b/(M*math.log2(M)):>13.3f} {b/M:>6.2f}")

print()
print("Same, single input (|I|=1) where homing is hardest")
print(f"{'M':>4} {'best L':>7} {'M-1':>5} {'M log2 M':>9} {'L/(M log2 M)':>13}")
for M in [4,6,8,10,12,14,16,20]:
    b,ml=search(M,1,2,iters=800,restarts=5,seed=100+M)
    print(f"{M:>4} {b:>7} {M-1:>5} {M*math.log2(M):>9.1f} {b/(M*math.log2(M)):>13.3f}")
