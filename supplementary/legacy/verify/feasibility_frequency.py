"""
T43.  Precise frequencies for two claims currently stated as 'a majority'.

(A) rem:unifilar-feasibility: among quotients satisfying the FEASIBLE-triple
    condition (def:unifilar-lumpable), what fraction FAIL the same condition
    stated without the feasibility restriction (i.e. over all triples)?

(B) rem:controlled-zero-not-kernels: among unifilar machines with a forced
    kernel collision, what fraction have the kernel partition NOT
    unifilar-lumpable (equivalently N* > |phi_ker|)?
"""
import random, itertools
import numpy as np

def parts(n):
    def rec(i,mx,cur):
        if i==n: yield tuple(cur); return
        for b in range(mx+1):
            cur.append(b); yield from rec(i+1,max(mx,b+1),cur); cur.pop()
    yield from rec(0,0,[])
PARTS={n:list(parts(n)) for n in range(2,6)}

def ul_feasible(phi,tau,supp,nS,nI):
    for x in range(nI):
        img={}
        for s in range(nS):
            k=phi[s]
            for y in supp[s][x]:
                v=phi[tau[s][x][y]]
                if img.get((k,x,y),v)!=v: return False
                img[(k,x,y)]=v
    return True

def ul_alltriples(phi,tau,nS,nI,nO):
    for x in range(nI):
        img={}
        for s in range(nS):
            k=phi[s]
            for y in range(nO):
                v=phi[tau[s][x][y]]
                if img.get((k,x,y),v)!=v: return False
                img[(k,x,y)]=v
    return True

# ---------------- (A) ----------------
rng=random.Random(4242)
tot=0; fail=0
for _ in range(400000):
    nS=rng.randrange(2,5); nI=rng.randrange(1,3); nO=rng.randrange(2,4)
    tau=[[[rng.randrange(nS) for _ in range(nO)] for _ in range(nI)] for _ in range(nS)]
    supp=[[set(rng.sample(range(nO),rng.randrange(1,nO+1))) for _ in range(nI)]
          for _ in range(nS)]
    phi=rng.choice(PARTS[nS])
    if not ul_feasible(phi,tau,supp,nS,nI): continue
    tot+=1
    if not ul_alltriples(phi,tau,nS,nI,nO): fail+=1
print("="*72)
print("(A) rem:unifilar-feasibility")
print("="*72)
print(f"  quotients satisfying the feasible-triple condition : {tot}")
print(f"  of these, failing the all-triples condition        : {fail}")
print(f"  fraction                                           : {100.0*fail/tot:.1f}%")

# ---------------- (B) ----------------
def refine(phi0,tau,supp,nS,nI):
    phi=list(phi0)
    while True:
        sig={s:(phi[s],tuple(sorted((x,y,phi[tau[s][x][y]])
             for x in range(nI) for y in supp[s][x]))) for s in range(nS)}
        keys=sorted(set(sig.values()),key=str); idx={k:i for i,k in enumerate(keys)}
        new=[idx[sig[s]] for s in range(nS)]
        if len(set(new))==len(set(phi)): return tuple(new)
        phi=new

rng=random.Random(777)
tot2=0; gap=0
for _ in range(200000):
    nS=rng.randrange(3,6); nI=rng.randrange(1,3); nO=rng.randrange(2,4)
    tau=[[[rng.randrange(nS) for _ in range(nO)] for _ in range(nI)] for _ in range(nS)]
    supp=[[set(range(nO)) for _ in range(nI)] for _ in range(nS)]
    pool=[]
    for _ in range(rng.randrange(1,nS)):
        row=[]
        for x in range(nI):
            w=[rng.random()+.05 for _ in range(nO)]; t=sum(w); row.append(tuple(v/t for v in w))
        pool.append(tuple(row))
    P=[pool[rng.randrange(len(pool))] for _ in range(nS)]
    pin=[rng.random()+.05 for _ in range(nI)]; t=sum(pin); pin=[v/t for v in pin]
    T=np.zeros((nS,nS))
    for s in range(nS):
        for x in range(nI):
            for y in range(nO): T[s][tau[s][x][y]]+=pin[x]*P[s][x][y]
    pi=np.ones(nS)/nS
    for _ in range(1200): pi=pi@T
    if pi.min()<1e-8: continue
    kern={}; phik=[kern.setdefault(P[s],len(kern)) for s in range(nS)]
    if len(kern)>=nS: continue          # need a genuine collision
    tot2+=1
    if len(set(refine(phik,tau,supp,nS,nI)))>len(kern): gap+=1
print()
print("="*72)
print("(B) rem:controlled-zero-not-kernels")
print("="*72)
print(f"  machines with a genuine kernel collision : {tot2}")
print(f"  of these, with N* > |phi_ker|            : {gap}")
print(f"  fraction                                 : {100.0*gap/tot2:.1f}%")
