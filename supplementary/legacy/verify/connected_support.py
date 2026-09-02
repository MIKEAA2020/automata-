"""
T39.  Verify prop:input-driven-specialization(i) as now stated:

  connected support-overlap graph on every block, at every input
      =>  unifilar-lumpable  <=>  lumpable
  and connectedness is NOT droppable.

Also verify block-uniform and full-support are special cases.
"""
import random, itertools

def parts(n):
    def rec(i,mx,cur):
        if i==n: yield tuple(cur); return
        for b in range(mx+1):
            cur.append(b); yield from rec(i+1,max(mx,b+1),cur); cur.pop()
    yield from rec(0,0,[])
PARTS={n:list(parts(n)) for n in range(2,6)}

def lumpable(phi,tau0,nS,nI):
    for x in range(nI):
        img={}
        for s in range(nS):
            k=phi[s]; v=phi[tau0[s][x]]
            if img.get(k,v)!=v: return False
            img[k]=v
    return True

def unif_lumpable(phi,tau0,supp,nS,nI):
    for x in range(nI):
        img={}
        for s in range(nS):
            k=phi[s]; v=phi[tau0[s][x]]
            for y in supp[s][x]:
                if img.get((k,x,y),v)!=v: return False
                img[(k,x,y)]=v
    return True

def connected(phi,supp,nS,nI):
    blocks={}
    for s in range(nS): blocks.setdefault(phi[s],[]).append(s)
    for x in range(nI):
        for C in blocks.values():
            par=list(range(len(C)))
            def find(a):
                while par[a]!=a: par[a]=par[par[a]]; a=par[a]
                return a
            for i in range(len(C)):
                for j in range(i+1,len(C)):
                    if supp[C[i]][x] & supp[C[j]][x]: par[find(i)]=find(j)
            if len({find(i) for i in range(len(C))})>1: return False
    return True

def block_uniform(phi,supp,nS,nI):
    for x in range(nI):
        rep={}
        for s in range(nS):
            k=phi[s]
            if k in rep and rep[k]!=supp[s][x]: return False
            rep[k]=supp[s][x]
    return True

rng=random.Random(20260807)
nconn=nbu=nfull=0
bad_conn=bad_bu=bad_full=0
n_notconn=0; n_notconn_differ=0
tot=0
for _ in range(400000):
    nS=rng.randrange(2,6); nI=rng.randrange(1,4); nO=rng.randrange(2,4)
    tau0=[[rng.randrange(nS) for _ in range(nI)] for _ in range(nS)]
    supp=[[set(rng.sample(range(nO),rng.randrange(1,nO+1))) for _ in range(nI)]
          for _ in range(nS)]
    phi=rng.choice(PARTS[nS])
    tot+=1
    L=lumpable(phi,tau0,nS,nI); U=unif_lumpable(phi,tau0,supp,nS,nI)
    if L and not U:
        print("*** FAILED: lumpable but not unifilar-lumpable"); raise SystemExit(1)
    if connected(phi,supp,nS,nI):
        nconn+=1
        if U!=L: bad_conn+=1
    else:
        n_notconn+=1
        if U!=L: n_notconn_differ+=1
    if block_uniform(phi,supp,nS,nI):
        nbu+=1
        if U!=L: bad_bu+=1
    if all(len(supp[s][x])==nO for s in range(nS) for x in range(nI)):
        nfull+=1
        if U!=L: bad_full+=1

print("="*72)
print("prop:input-driven-specialization(i)  --  connected support")
print("="*72)
print(f"  random (machine, partition) instances       : {tot}")
print(f"  lumpable => unifilar-lumpable failures      : 0")
print()
print(f"  connected support instances                 : {nconn}")
print(f"    disagreements unifilar-lumpable vs lumpable: {bad_conn}")
print(f"  block-uniform support instances             : {nbu}")
print(f"    disagreements                              : {bad_bu}")
print(f"  full support instances                      : {nfull}")
print(f"    disagreements                              : {bad_full}")
print()
print(f"  NON-connected support instances             : {n_notconn}")
print(f"    of which the two notions DIFFER           : {n_notconn_differ}"
      f"   ({100.0*n_notconn_differ/max(n_notconn,1):.2f}%)")
assert bad_conn==0 and bad_bu==0 and bad_full==0 and n_notconn_differ>0
print()
print("  VERIFIED: connectedness is sufficient, and is not droppable.")
