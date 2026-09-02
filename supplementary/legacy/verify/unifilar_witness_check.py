"""T39.  Verify the two explicit witnesses written into
rem:unifilar-support-not-automatic, exactly as stated in the manuscript."""
import math, numpy as np
from fractions import Fraction as F

def parts(n):
    def rec(i,mx,cur):
        if i==n: yield tuple(cur); return
        for b in range(mx+1):
            cur.append(b); yield from rec(i+1,max(mx,b+1),cur); cur.pop()
    yield from rec(0,0,[])

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

print("="*72)
print("WITNESS 1  (feasible-set separation), exactly as printed")
print("="*72)
nS,nI=3,2
tau0=[[0,1],[0,2],[0,0]]     # s0:(0->s0,1->s1)  s1:(0->s0,1->s2)  s2:(0->s0,1->s0)
supp=[[{0},{0}],[{0},{0}],[{1},{1}]]   # s0,s1 emit 0 a.s.; s2 emits 1 a.s.
print(f"  tau0 = {tau0}")
print(f"  supports: s0->{sorted(supp[0][0])}, s1->{sorted(supp[1][0])}, s2->{sorted(supp[2][0])}")
# irreducibility + stationary
T=np.zeros((nS,nS))
for s in range(nS):
    for x in range(nI): T[s][tau0[s][x]]+=0.5
pi=np.ones(nS)/nS
for _ in range(100000): pi=pi@T
pi/=pi.sum()
print(f"  stationary pi = {np.round(pi,6)}   min = {pi.min():.6f} > 0 : {pi.min()>1e-12}")
reach=set([0]); st=[0]
while st:
    a=st.pop()
    for x in range(nI):
        b=tau0[a][x]
        if b not in reach: reach.add(b); st.append(b)
print(f"  reachable from s0: {sorted(reach)}  irreducible: {len(reach)==nS}")
phi=(0,1,0)   # {s0,s2},{s1}
U=unif_lumpable(phi,tau0,supp,nS,nI); L=lumpable(phi,tau0,nS,nI)
print(f"  phi = {{{{s0,s2}},{{s1}}}} : unifilar-lumpable={U}  lumpable={L}")
print(f"  tau0(s0,1)=s{tau0[0][1]} (block {phi[tau0[0][1]]}), "
      f"tau0(s2,1)=s{tau0[2][1]} (block {phi[tau0[2][1]]}) -> differ, so not lumpable")
assert U and not L
print("  WITNESS 1 CONFIRMED.")

print()
print("="*72)
print("WITNESS 2  (strict value separation), exactly as printed")
print("="*72)
nS,nI,nO=3,2,3
tau0=[[1,2],[2,0],[0,0]]
supp_sets=[[2],[0,1,2],[1]]
supp=[[set(supp_sets[s]) for _ in range(nI)] for s in range(nS)]
P=[[0.0,0.0,1.0],[0.38299,0.374,0.24301],[0.0,1.0,0.0]]
print(f"  tau0 = {tau0}   (rows=states, cols=inputs)")
print(f"  P_s0 = delta_2, P_s2 = delta_1, P_s1 = {P[1]}")
T=np.zeros((nS,nS))
for s in range(nS):
    for x in range(nI): T[s][tau0[s][x]]+=0.5
pi=np.ones(nS)/nS
for _ in range(100000): pi=pi@T
pi/=pi.sum()
print(f"  stationary pi = {np.round(pi,6)}  all positive: {pi.min()>1e-12}")
def kl(p,q):
    t=0.0
    for a,b in zip(p,q):
        if a>0:
            if b<=0: return float('inf')
            t+=a*math.log(a/b)
    return t
def cost(phi):
    z=0.0
    for k in set(phi):
        C=[s for s in range(nS) if phi[s]==k]
        w=sum(pi[s] for s in C)
        bar=[sum(pi[s]*P[s][y] for s in C)/w for y in range(nO)]
        z+=sum(pi[s]*kl(P[s],bar) for s in C)
    return z
print("\n  partition        unif-lump  lump    cost")
for phi in parts(nS):
    if len(set(phi))>2: continue
    print(f"   {phi}         {str(unif_lumpable(phi,tau0,supp,nS,nI)):5s}     "
          f"{str(lumpable(phi,tau0,nS,nI)):5s}  {cost(phi):.8f}")
u=min(cost(p) for p in parts(nS) if len(set(p))<=2 and unif_lumpable(p,tau0,supp,nS,nI))
l=min(cost(p) for p in parts(nS) if len(set(p))<=2 and lumpable(p,tau0,nS,nI))
print(f"\n  min over unifilar-lumpable, 2 blocks : {u:.10f}")
print(f"  min over ordinary lumpable,  2 blocks : {l:.10f}")
print(f"  strict gap = {l-u:.10f}")
assert l-u>1e-6
print("  WITNESS 2 CONFIRMED: the retention VALUES differ, not just the")
print("  feasible sets.")
