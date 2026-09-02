"""T39.  Verify rem:controlled-zero-not-kernels witness EXACTLY as printed,
and prop:kernel-refinement-exists on it."""
import math, numpy as np

nS,nI,nO=3,1,2
# A=0,B=1,C=2 ; P_A=P_B=Bern(1/2) meaning P(y=1)=1/2 ; P_C=Bern(1/10)
P=[[[0.5,0.5]],[[0.5,0.5]],[[0.9,0.1]]]   # [P(y=0),P(y=1)]
# tau(A,0)=A, tau(A,1)=C ; tau(B,0)=C, tau(B,1)=B ; tau(C,0)=A, tau(C,1)=B
tau=[[[0,2]],[[2,1]],[[0,1]]]
supp=[[{0,1}],[{0,1}],[{0,1}]]

T=np.zeros((nS,nS))
for s in range(nS):
    for y in range(nO): T[s][tau[s][0][y]]+=P[s][0][y]
pi=np.ones(nS)/nS
for _ in range(200000): pi=pi@T
pi/=pi.sum()
names="ABC"
print("="*70)
print("rem:controlled-zero-not-kernels witness, as printed")
print("="*70)
print("  tau(A,0)=A tau(A,1)=C | tau(B,0)=C tau(B,1)=B | tau(C,0)=A tau(C,1)=B")
print(f"  P_A=P_B=Bern(1/2), P_C=Bern(1/10)")
print(f"  stationary pi = {dict(zip(names,np.round(pi,6)))}  min={pi.min():.6f} >0: {pi.min()>1e-12}")

def unif_lumpable(phi):
    for x in range(nI):
        img={}
        for s in range(nS):
            k=phi[s]
            for y in supp[s][x]:
                v=phi[tau[s][x][y]]
                if img.get((k,x,y),v)!=v: return False
                img[(k,x,y)]=v
    return True

kern={}
phik=[kern.setdefault(tuple(P[s][0]),len(kern)) for s in range(nS)]
print(f"  kernel partition phi_ker = {phik}  -> #distinct kernels = {len(kern)}")
print(f"  is {{{{A,B}},{{C}}}} unifilar-lumpable? {unif_lumpable((0,0,1))}")
print(f"    tau(A,0)=A (block {phik[tau[0][0][0]]}), tau(B,0)=C (block {phik[tau[1][0][0]]}) -> differ")

# refinement recursion exactly as in prop:kernel-refinement-exists
phi=list(phik); step=0
while True:
    sig={s:(phi[s],tuple(sorted((x,y,phi[tau[s][x][y]]) for x in range(nI) for y in supp[s][x])))
         for s in range(nS)}
    keys=sorted(set(sig.values()),key=str); idx={k:i for i,k in enumerate(keys)}
    new=[idx[sig[s]] for s in range(nS)]
    step+=1
    print(f"  refinement step {step}: {tuple(new)}  ({len(set(new))} blocks)")
    if len(set(new))==len(set(phi)): break
    phi=new
Nstar=len(set(phi)); phistar=tuple(phi)
print(f"  N* = {Nstar}   (vs #distinct kernels = {len(kern)})")
print(f"  phi* unifilar-lumpable: {unif_lumpable(phistar)}")

def kl(p,q):
    return sum(a*math.log(a/b) for a,b in zip(p,q) if a>0)
def rc(phi):
    z=0.0
    for k in set(phi):
        C=[s for s in range(nS) if phi[s]==k]
        w=sum(pi[s] for s in C)
        bar=[sum(pi[s]*P[s][0][y] for s in C)/w for y in range(nO)]
        z+=sum(pi[s]*kl(P[s][0],bar) for s in C)
    return z
def parts(n):
    def rec(i,mx,cur):
        if i==n: yield tuple(cur); return
        for b in range(mx+1):
            cur.append(b); yield from rec(i+1,max(mx,b+1),cur); cur.pop()
    yield from rec(0,0,[])
for M in (2,3):
    v=min(rc(p) for p in parts(nS) if len(set(p))<=M and unif_lumpable(p))
    print(f"  RetKL^ctrl({M}) = {v:.10f}")
v2=min(rc(p) for p in parts(nS) if len(set(p))<=2 and unif_lumpable(p))
v3=min(rc(p) for p in parts(nS) if len(set(p))<=3 and unif_lumpable(p))
assert v2>1e-9 and v3<1e-12 and Nstar==3 and len(kern)==2
print("  CONFIRMED: RetKL^ctrl(2)>0 and RetKL^ctrl(3)=0, N*=3 > 2 kernels.")
