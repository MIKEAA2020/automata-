"""
T39 (deep).  Two questions:
 (Q1) Is there an IRREDUCIBLE (ergodic state chain), full-support input-driven
      machine with a partition unifilar-lumpable but not lumpable?
 (Q2) Does the enlarged feasible set strictly LOWER RetKL(M)?
      i.e. is the proposed cor:controlled-reduces ("RetKL^ctrl = RetKL for
      output-independent emissions") actually false?
"""
import itertools, random, math, sys
from fractions import Fraction as F
from itertools import product

def partitions(n):
    def rec(i,mx,cur):
        if i==n: yield tuple(cur); return
        for b in range(mx+1):
            cur.append(b); yield from rec(i+1,max(mx,b+1),cur); cur.pop()
    yield from rec(0,0,[])
PARTS={n:list(partitions(n)) for n in (2,3,4)}

def chain(tau0,nS,nI):
    P=[[F(0)]*nS for _ in range(nS)]
    for s in range(nS):
        for x in range(nI): P[s][tau0[s][x]]+=F(1,nI)
    return P

def irreducible(tau0,nS,nI):
    reach={s:set() for s in range(nS)}
    for s in range(nS):
        st=[s]; seen=set()
        while st:
            a=st.pop()
            for x in range(nI):
                b=tau0[a][x]
                if b not in seen: seen.add(b); st.append(b)
        reach[s]=seen
    return all(len(reach[s])==nS for s in range(nS))

def stationary(tau0,nS,nI):
    P=chain(tau0,nS,nI); v=[F(1,nS)]*nS
    for _ in range(500):
        v=[sum(v[s]*P[s][t] for s in range(nS)) for t in range(nS)]
    return v

def lumpable(phi,tau0,nS,nI):
    for x in range(nI):
        img={}
        for s in range(nS):
            k=phi[s]; val=phi[tau0[s][x]]
            if img.get(k,val)!=val: return False
            img[k]=val
    return True

def unif_lumpable(phi,tau0,supp,nS,nI):
    for x in range(nI):
        img={}
        for s in range(nS):
            k=phi[s]; val=phi[tau0[s][x]]
            for y in supp[s][x]:
                if img.get((k,y),val)!=val: return False
                img[(k,y)]=val
    return True

# ---------------- Q1 ----------------
print("="*72)
print("Q1  irreducible, aperiodic-or-not, full-support witness")
nO=2; found=None
for nS in (3,4):
  if found: break
  for nI in (2,):
    for tau0t in product(product(range(nS),repeat=nI),repeat=nS):
        tau0=[list(r) for r in tau0t]
        if not irreducible(tau0,nS,nI): continue
        pi=stationary(tau0,nS,nI)
        if any(p==0 for p in pi): continue
        subs=[tuple(S) for r in range(1,nO+1) for S in itertools.combinations(range(nO),r)]
        for supptup in product(subs,repeat=nS):     # support indep of input
            supp=[[set(supptup[s])]*nI for s in range(nS)]
            for phi in PARTS[nS]:
                if len(set(phi))>=nS: continue
                if unif_lumpable(phi,tau0,supp,nS,nI) and not lumpable(phi,tau0,nS,nI):
                    found=(nS,nI,tau0,supptup,phi,pi); break
            if found: break
        if found: break
nS,nI,tau0,supptup,phi,pi=found
print(f"  |S|={nS} |I|={nI} |O|={nO}   tau0={tau0}")
print(f"  irreducible: {irreducible(tau0,nS,nI)}   stationary pi={[str(p) for p in pi]}")
print(f"  emission supports (input-independent) = {[sorted(c) for c in supptup]}")
print(f"  phi={phi}: unifilar-lumpable=True  lumpable=False")
print("  => on an irreducible, full-support, input-driven machine the two")
print("     definitions differ.  Manuscript line ~7453 is FALSE as stated.")

# ---------------- Q2 ----------------
print("="*72)
print("Q2  does the enlarged feasible set strictly lower RetKL(M)?")
def kl(p,q): return sum(a*math.log(a/b) for a,b in zip(p,q) if a>0)
def retkl(phi,pif,P,nO):
    blocks={}
    for s,k in enumerate(phi): blocks.setdefault(k,[]).append(s)
    t=0.0
    for C in blocks.values():
        w=sum(pif[s] for s in C)
        if w<=0: continue
        bar=[sum(pif[s]*P[s][j] for s in C)/w for j in range(nO)]
        t+=sum(pif[s]*kl(P[s],bar) for s in C)
    return t

random.seed(2024)
nO=3
hits=0; tested=0; example=None
for trial in range(30000):
    nS=random.choice([3,4]); nI=2
    tau0=[[random.randrange(nS) for _ in range(nI)] for _ in range(nS)]
    if not irreducible(tau0,nS,nI): continue
    pi=stationary(tau0,nS,nI)
    if any(p==0 for p in pi): continue
    pif=[float(p) for p in pi]
    # random supports (input-independent), random laws on those supports
    supp_sets=[]
    P=[]
    for s in range(nS):
        r=random.randrange(1,nO+1)
        S=sorted(random.sample(range(nO),r))
        supp_sets.append(S)
        w=[random.uniform(.1,1) for _ in S]; tot=sum(w)
        row=[0.0]*nO
        for j,y in enumerate(S): row[y]=w[j]/tot
        P.append(row)
    supp=[[set(supp_sets[s])]*nI for s in range(nS)]
    Lset=[p for p in PARTS[nS] if lumpable(p,tau0,nS,nI)]
    Uset=[p for p in PARTS[nS] if unif_lumpable(p,tau0,supp,nS,nI)]
    if len(Uset)==len(Lset): continue
    tested+=1
    for M in range(1,nS):
        vl=[retkl(p,pif,P,nO) for p in Lset if len(set(p))<=M]
        vu=[retkl(p,pif,P,nO) for p in Uset if len(set(p))<=M]
        if vl and vu and min(vu)<min(vl)-1e-10:
            hits+=1
            if example is None:
                example=(nS,nI,tau0,supp_sets,[[round(v,5) for v in r] for r in P],
                         M,min(vu),min(vl),
                         [p for p in Uset if len(set(p))<=M and abs(retkl(p,pif,P,nO)-min(vu))<1e-12])
            break
print(f"  instances where the two feasible sets differ : {tested}")
print(f"  instances where RetKL strictly drops         : {hits}")
if example:
    nS,nI,tau0,ss,P,M,u,l,arg=example
    print("  EXAMPLE:")
    print(f"    |S|={nS} tau0={tau0}  supports={ss}")
    print(f"    P = {P}")
    print(f"    M={M}:  min over unifilar-lumpable = {u:.10f}")
    print(f"            min over ordinary lumpable = {l:.10f}")
    print(f"    strict gap = {l-u:.10f}   optimizing quotient(s): {arg}")
    print("  => RetKL^ctrl(M) < RetKL(M) can hold even with output-independent")
    print("     emissions.  The proposed cor:controlled-reduces is FALSE.")
else:
    print("  no strict drop found")
