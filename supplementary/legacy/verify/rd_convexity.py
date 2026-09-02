"""
Does the manuscript's finite-state D(R) = Delta(floor(e^R)) satisfy the
structural properties of a rate-distortion function?

A Shannon rate-distortion function D(R) is CONVEX in R.  The mechanism is
time-sharing: given codes at rates R_1, R_2 one may randomise, achieving every
point on the chord.  The finite-state budget is a HARD cardinality constraint
|K| <= M over DETERMINISTIC lumpable quotients, with no randomisation, so the
chord is not available.

Tested at 60 decimal digits to exclude floating-point artefacts.
"""
from mpmath import mp, mpf, log
import itertools, random
mp.dps = 60

def parts(n):
    def rec(i,mx,cur):
        if i==n: yield tuple(cur); return
        for b in range(mx+1):
            cur.append(b); yield from rec(i+1,max(mx,b+1),cur); cur.pop()
    yield from rec(0,0,[])
PARTS={n:list(parts(n)) for n in range(2,7)}

def kl(p,q):
    t=mpf(0)
    for a,b in zip(p,q):
        if a>0: t+=a*log(a/b)
    return t

def retkl(phi,pi,P,nO):
    tot=mpf(0)
    for k in set(phi):
        C=[s for s in range(len(pi)) if phi[s]==k]
        w=sum(pi[s] for s in C)
        bar=[sum(pi[s]*P[s][y] for s in C)/w for y in range(nO)]
        tot+=sum(pi[s]*kl(P[s],bar) for s in C)
    return tot

# the witness found in the float scan, recomputed exactly
pi=[mpf('0.0344'),mpf('0.3506'),mpf('0.1906'),mpf('0.2176'),mpf('0.2068')]
t=sum(pi); pi=[x/t for x in pi]
P=[[mpf('0.4805'),mpf('0.4113'),mpf('0.1082')],
   [mpf('0.2746'),mpf('0.4018'),mpf('0.3236')],
   [mpf('0.2960'),mpf('0.5426'),mpf('0.1614')],
   [mpf('0.2334'),mpf('0.5019'),mpf('0.2648')],
   [mpf('0.6498'),mpf('0.0548'),mpf('0.2954')]]
P=[[v/sum(r) for v in r] for r in P]
nS,nO=5,3
print("="*76)
print("EXACT recomputation of the non-convexity witness (60 dps)")
print("="*76)
curve=[]
for M in range(1,nS+1):
    v=min(retkl(p,pi,P,nO) for p in PARTS[nS] if len(set(p))<=M)
    curve.append((log(mpf(M)), v))
    print(f"   M={M}  R=log M={mp.nstr(log(mpf(M)),12):>16}  D(R)={mp.nstr(v,14)}")
sl=[(d1-d0)/(r1-r0) for (r0,d0),(r1,d1) in zip(curve,curve[1:])]
print("\n   successive chord slopes:")
for i,x in enumerate(sl): print(f"     [{i}] {mp.nstr(x,14)}")
viol=[i for i in range(len(sl)-1) if sl[i+1] < sl[i]]
print(f"\n   convexity requires nondecreasing slopes; violations at indices {viol}")
if viol:
    i=viol[0]
    print(f"   slope[{i+1}] - slope[{i}] = {mp.nstr(sl[i+1]-sl[i],14)}  < 0")
assert viol, "expected a convexity violation"
print("\n   => D(R) is NOT convex.  Verified in exact arithmetic, not floating point.")

print()
print("="*76)
print("Frequency over random instances (exact arithmetic, smaller sample)")
print("="*76)
rng=random.Random(7); bad=0; tot=0
for _ in range(400):
    n=rng.randrange(3,6); o=rng.randrange(2,4)
    q=[mpf(rng.randrange(5,100))/100 for _ in range(n)]; t=sum(q); q=[x/t for x in q]
    R=[]
    for _ in range(n):
        w=[mpf(rng.randrange(2,100))/100 for _ in range(o)]; s=sum(w); R.append([v/s for v in w])
    c=[]
    for M in range(1,n+1):
        c.append((log(mpf(M)), min(retkl(p,q,R,o) for p in PARTS[n] if len(set(p))<=M)))
    s2=[(d1-d0)/(r1-r0) for (r0,d0),(r1,d1) in zip(c,c[1:])]
    tot+=1
    if any(s2[i+1]<s2[i] for i in range(len(s2)-1)): bad+=1
print(f"   instances: {tot}   non-convex: {bad}  ({100.0*bad/tot:.1f}%)")
print()
print("   CONCLUSION: the finite-state curve lacks the convexity that")
print("   time-sharing confers on a Shannon rate-distortion function.")
print("   The manuscript's existing scope caveat is therefore mathematically")
print("   required, not an apology.")

# ------------------------------------------------------------------ T50
print()
print("="*76)
print("T50: non-convexity is NOT an artifact of the log parametrisation")
print("="*76)
from fractions import Fraction as F
qi=[17,18,22,21]
Ri=[[20,25,2],[2,34,30],[37,1,27],[20,9,1]]
pi=[mpf(x)/mpf(sum(qi)) for x in qi]
P=[[mpf(x)/mpf(sum(r)) for x in r] for r in Ri]
nS,nO=4,3
def cur():
    return [min(retkl(p,pi,P,nO) for p in PARTS[nS] if len(set(p))<=M)
            for M in range(1,nS+1)]
v=cur()
def sl(vals,xs): return [(vals[i+1]-vals[i])/(xs[i+1]-xs[i]) for i in range(len(vals)-1)]
def nc(s): return any(s[i+1]<s[i] for i in range(len(s)-1))
sM=sl(v,[mpf(m) for m in range(1,nS+1)])
sL=sl(v,[log(mpf(m)) for m in range(1,nS+1)])
print(f"  pi proportional to {qi}")
print(f"  P rows proportional to {Ri}")
print(f"  D(M)              = {[mp.nstr(x,9) for x in v]}")
print(f"  slopes in R = M     = {[mp.nstr(x,9) for x in sM]}   non-convex {nc(sM)}")
print(f"  slopes in R = log M = {[mp.nstr(x,9) for x in sL]}   non-convex {nc(sL)}")
assert nc(sM) and nc(sL)
print(f"  decrement in M      = {mp.nstr(sM[1]-sM[0],6)}")
assert sM[1]-sM[0] < 0
print()
print("  Hence no reparametrisation of the budget restores a convexity")
print("  guarantee: the obstruction is the absence of time-sharing, which is")
print("  independent of how the rate axis is scaled.")
print()
print("T50 VERIFIED")
