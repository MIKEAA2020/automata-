"""T51.  Repaired finite-state grounding decomposition (audit E1).

Repaired E1.  For a deterministic Mealy machine the emission at a state is a
FIXED symbol.  If phi maps channel states to machine states, the best symbol at
block k is bhat_k = argmax_b sum_{s in C_k} pi_s P_s(b)  (maximises hit rate).

Claim to verify (one-step stationary form):
   E[1 - P_{S}(bhat_{phi(S)})]  =  sigma_1  +  D(phi)
   sigma_1 = sum_s pi_s (1 - max_b P_s(b))            [irreducible]
   D(phi)  = sum_s pi_s ( max_b P_s(b) - P_s(bhat_{phi(s)}) )   [tracking]
and D(phi) >= 0 with equality iff every block's best symbol attains each
member's mode.  Also: is D(phi) minimised by the SINGLETON partition?
"""
from fractions import Fraction as F
import random, itertools
def mx(p): return max(p)
def amax(p): return max(range(len(p)), key=lambda i:(p[i],-i))
def parts(n):
    def rec(i,m,c):
        if i==n: yield tuple(c); return
        for b in range(m+1):
            c.append(b); yield from rec(i+1,max(m,b+1),c); c.pop()
    yield from rec(0,0,[])

rng=random.Random(31)
bad_decomp=bad_nonneg=bad_mono=tot=0
for _ in range(120000):
    n=rng.randrange(2,5); o=rng.randrange(2,4)
    pi=[F(rng.randrange(1,30)) for _ in range(n)]; T=sum(pi); pi=[x/T for x in pi]
    P=[]
    for _ in range(n):
        v=[F(rng.randrange(0,30)) for _ in range(o)]
        if sum(v)==0: v[0]=F(1)
        t=sum(v); P.append([x/t for x in v])
    sigma1=sum(pi[s]*(1-mx(P[s])) for s in range(n))
    for phi in parts(n):
        blocks={}
        for s in range(n): blocks.setdefault(phi[s],[]).append(s)
        bhat={}
        for k,C in blocks.items():
            w=[sum(pi[s]*P[s][b] for s in C) for b in range(o)]
            bhat[k]=amax(w)
        err=sum(pi[s]*(1-P[s][bhat[phi[s]]]) for s in range(n))
        D=sum(pi[s]*(mx(P[s])-P[s][bhat[phi[s]]]) for s in range(n))
        tot+=1
        if err != sigma1+D: bad_decomp+=1
        if D<0: bad_nonneg+=1
    # monotone: singleton partition attains D=0
    sing=tuple(range(n))
    bh={s:amax(P[s]) for s in range(n)}
    Ds=sum(pi[s]*(mx(P[s])-P[s][bh[s]]) for s in range(n))
    if Ds!=0: bad_mono+=1
print("="*76)
print("REPAIRED grounding decomposition")
print("="*76)
print(f"  (phi,instance) pairs tested        : {tot}")
print(f"  decomposition err = sigma1 + D fails: {bad_decomp}")
print(f"  tracking deficit D(phi) < 0        : {bad_nonneg}")
print(f"  singleton partition has D != 0     : {bad_mono}")
assert bad_decomp==0 and bad_nonneg==0 and bad_mono==0
print()
print("  VERIFIED: with bhat = argmax of the pi-weighted BLOCK mixture,")
print("    err(phi) = sigma_1 + D(phi),   D(phi) >= 0,   D(singleton) = 0.")
print()
print("  Note the contrast with the audit's version:")
print("    audit deficit  = max_b P_s(b) - max_b P_phi(s)(b)   -> can be NEGATIVE")
print("    correct deficit= max_b P_s(b) - P_s(bhat_phi(s))    -> always >= 0")
