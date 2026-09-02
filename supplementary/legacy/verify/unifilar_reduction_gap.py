"""
=============================================================================
SUPERSEDED -- retained for provenance only.  DO NOT CITE.

This probe quotes the pre-T39 wording of def:unifilar-lumpable ("for an
output-independent update the condition reduces to def:lumpable-quotient"),
which was found FALSE and removed in T39.  The manuscript now carries
rem:unifilar-support-not-automatic and prop:input-driven-specialization,
which state the correct connected-support condition.

The live successor, registered in tools/traceability.py, is
  verify/unifilar_reduction_gap2.py   (feasible-set AND value separation)
  verify/connected_support.py         (connectedness sufficient, non-droppable)
=============================================================================

T39.  Does unifilar lumpability reduce to ordinary lumpability for
OUTPUT-INDEPENDENT (input-driven) updates?

Under test:
  (M) manuscript def:unifilar-lumpable: "for an output-independent update the
      condition reduces to Definition~\ref{def:lumpable-quotient}."
  (A) audit prop:input-driven-specialization(i): the two are "equivalent".

Mechanism: unifilar lumpability constrains phi(tau0(s,x))=phi(tau0(s',x)) only
for s,s' in a common block sharing a COMMON feasible output y.  Ordinary
lumpability constrains it for ALL s,s' in the block.  So unifilar lumpability
is WEAKER whenever within-block emission supports are disjoint.
"""
import itertools, random, sys
from fractions import Fraction as F
from itertools import product

def partitions(n):
    def rec(i,mx,cur):
        if i==n: yield tuple(cur); return
        for b in range(mx+1):
            cur.append(b); yield from rec(i+1,max(mx,b+1),cur); cur.pop()
    yield from rec(0,0,[])

def stationary(tau0,nS,nI):
    P=[[F(0)]*nS for _ in range(nS)]
    for s in range(nS):
        for x in range(nI): P[s][tau0[s][x]]+=F(1,nI)
    v=[F(1,nS)]*nS
    for _ in range(4*nS+50):
        v=[sum(v[s]*P[s][t] for s in range(nS)) for t in range(nS)]
    return v

def lumpable(phi,tau0,nS,nI,live):
    for x in range(nI):
        img={}
        for s in live:
            k=phi[s]; val=phi[tau0[s][x]]
            if img.get(k,val)!=val: return False
            img[k]=val
    return True

def unif_lumpable(phi,tau0,supp,nS,nI,live):
    for x in range(nI):
        img={}
        for s in live:
            k=phi[s]; val=phi[tau0[s][x]]
            for y in supp[s][x]:
                if img.get((k,y),val)!=val: return False
                img[(k,y)]=val
    return True

# ---------------- (a) exhaustive search for a STATIONARY witness -------------
print("="*72)
print("(a) exhaustive search: input-driven machine, ALL states of positive")
print("    stationary mass, partition unifilar-lumpable but NOT lumpable.")
best=None
nO=2
for nS in (3,4):
  if best: break
  for nI in (1,2):
    if best: break
    for tau0t in product(product(range(nS),repeat=nI),repeat=nS):
        tau0=[list(r) for r in tau0t]
        pi=stationary(tau0,nS,nI)
        if any(p==0 for p in pi): continue      # need full support
        live=list(range(nS))
        subs=[tuple(S) for r in range(1,nO+1) for S in itertools.combinations(range(nO),r)]
        for supptup in product(product(subs,repeat=nI),repeat=nS):
            supp=[[set(c) for c in r] for r in supptup]
            for phi in partitions(nS):
                if len(set(phi))>=nS: continue
                U=unif_lumpable(phi,tau0,supp,nS,nI,live)
                L=lumpable(phi,tau0,nS,nI,live)
                if U and not L:
                    best=(nS,nI,tau0,supptup,phi,pi); break
                if L and not U:
                    print("*** FAILED: lumpable but not unifilar-lumpable",tau0,supptup,phi); sys.exit(1)
            if best: break
        if best: break

nS,nI,tau0,supptup,phi,pi=best
print(f"   |S|={nS} |I|={nI} |O|={nO}")
print(f"   tau0 (rows = states, cols = inputs) = {tau0}")
print(f"   emission supports = {[[sorted(c) for c in r] for r in supptup]}")
print(f"   stationary pi = {[str(p) for p in pi]}  (all > 0)")
print(f"   phi = {phi}  ->  unifilar-lumpable = True, lumpable = False")
print("   The two definitions are therefore NOT equivalent for input-driven")
print("   machines.  Manuscript sentence and audit item (A) are both FALSE.")

# ---------------- (b) does the gap change the retention VALUE? --------------
print("="*72)
print("(b) does the enlarged feasible set strictly lower the retention gap?")
import math
def kl(p,q):
    return sum(pi_*math.log(pi_/qi) for pi_,qi in zip(p,q) if pi_>0)
def retkl(phi,pi,P):
    blocks={}
    for s,k in enumerate(phi): blocks.setdefault(k,[]).append(s)
    tot=0.0
    for C in blocks.values():
        w=sum(pi[s] for s in C)
        if w==0: continue
        bar=[sum(pi[s]*P[s][j] for s in C)/w for j in range(len(P[0]))]
        tot+=sum(pi[s]*kl(P[s],bar) for s in C)
    return tot

# use the witness machine; assign predictive laws consistent with the supports
pif=[float(p) for p in pi]
supp=[[set(c) for c in r] for r in supptup]
random.seed(5); found=None
for trial in range(200000):
    # laws on O={0,1} respecting supports at the (single) marginal level:
    # P_s must be supported in the union over x of supp[s][x] (i.i.d. inputs)
    P=[]
    ok=True
    for s in range(nS):
        S=set().union(*supp[s])
        if S=={0}: P.append([1.0,0.0])
        elif S=={1}: P.append([0.0,1.0])
        else:
            a=random.uniform(0.05,0.95); P.append([a,1-a])
    for M in range(1,nS):
        vals_L=[retkl(p,pif,P) for p in partitions(nS)
                if len(set(p))<=M and lumpable(p,tau0,nS,nI,range(nS))]
        vals_U=[retkl(p,pif,P) for p in partitions(nS)
                if len(set(p))<=M and unif_lumpable(p,tau0,supp,nS,nI,range(nS))]
        if not vals_L or not vals_U: continue
        if min(vals_U) < min(vals_L)-1e-12:
            found=(M,min(vals_U),min(vals_L),P); break
    if found: break
if found:
    M,u,l,P=found
    print(f"   *** STRICT SEPARATION at M={M}:")
    print(f"       predictive laws P_s = {[[round(v,4) for v in r] for r in P]}")
    print(f"       RetKL over unifilar-lumpable quotients = {u:.8f}")
    print(f"       RetKL over ordinary  lumpable quotients = {l:.8f}")
    print(f"       gap = {l-u:.8f}   (so cor:controlled-reduces as proposed is FALSE)")
else:
    print("   no strict separation found in 200000 trials on this machine")
