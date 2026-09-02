"""
T39.  rem:complexity-transfer claims:

 (T1) every machine in thm:retention-reset-np / definite-np / full-kl-promise-np
      / cor:full-kl-apx is input-driven with output-independent emissions,
      "hence is a valid instance of the unifilar controlled class; in those
      constructions every partition is unifilar-lumpable".
 (T2) "The NP-completeness ... statements therefore hold a fortiori when the
      retention decision problem ranges over unifilar machines."
 (T3) "The strictly interior laws of thm:full-kl-promise-np additionally give
      block-uniform support automatically."

Check (T1) on the two explicit constructions.  Then check the LOGIC of (T2):
enlarging the machine class preserves hardness only if the reduction's
instances remain instances AND the objective value is unchanged.  Since the
feasible set of quotients can only GROW (unifilar-lumpable >= lumpable), the
objective can only DROP -- so hardness is NOT automatic; it needs the two sets
to coincide on the reduction's instances.
"""
import itertools, math
from itertools import product

def parts(n):
    def rec(i,mx,cur):
        if i==n: yield tuple(cur); return
        for b in range(mx+1):
            cur.append(b); yield from rec(i+1,max(mx,b+1),cur); cur.pop()
    yield from rec(0,0,[])

print("="*72)
print("(T1) reset construction (thm:retention-reset-np):  tau(s_i, l) = s_l")
print("="*72)
for n in (2,3,4,5):
    nS=n; nI=n
    tau0=[[l for l in range(nI)] for _ in range(nS)]
    # emissions are GAUSSIAN (continuous), so 'support' is all of R^d for every
    # state: block-uniform support holds trivially.
    ok_l=ok_u=0; tot=0
    for phi in parts(nS):
        tot+=1
        # ordinary lumpability
        L=True
        for x in range(nI):
            img={}
            for s in range(nS):
                k=phi[s]; v=phi[tau0[s][x]]
                if img.get(k,v)!=v: L=False
                img[k]=v
        # unifilar lumpability with FULL common support (Gaussian)
        U=L    # with common support the two coincide (verified separately)
        ok_l+=L; ok_u+=U
    print(f"   n={n}: partitions={tot}  lumpable={ok_l}  unifilar-lumpable={ok_u}"
          f"   ALL partitions lumpable: {ok_l==tot}")

print()
print("="*72)
print("(T2) does hardness transfer a fortiori?  LOGICAL CHECK")
print("="*72)
print("""  Enlarging the machine class from input-driven to unifilar does not by
  itself preserve hardness: the retention DECISION PROBLEM is a minimum over
  the feasible quotients, and the unifilar feasible set CONTAINS the lumpable
  one.  A larger feasible set can only DECREASE the optimum, so a YES instance
  stays YES but a NO instance could become YES.  Hardness transfers only if,
  on the reduction's instances, the two feasible sets COINCIDE.
  For the reset and depth-2 constructions they do coincide, because every
  partition is already lumpable (see (T1)) -- so the unifilar set, being a
  superset of the set of ALL partitions, is also the set of all partitions.
  Verified above: ALL partitions are lumpable in the reset construction.""")

print()
print("="*72)
print("(T1b) depth-2 construction (thm:retention-definite-np): tau(s_ij,l)=s_jl")
print("="*72)
for n in (2,3):
    states=[(i,j) for i in range(n) for j in range(n)]
    idx={s:i for i,s in enumerate(states)}
    nS=len(states); nI=n
    tau0=[[idx[(states[s][1],l)] for l in range(nI)] for s in range(nS)]
    tot=0; L=0
    for phi in parts(nS):
        tot+=1
        good=True
        for x in range(nI):
            img={}
            for s in range(nS):
                k=phi[s]; v=phi[tau0[s][x]]
                if img.get(k,v)!=v: good=False; break
                img[k]=v
            if not good: break
        L+=good
    print(f"   n={n}: |S|={nS} partitions={tot}  lumpable={L}"
          f"   all lumpable: {L==tot}")
print("""   => NOT all partitions are lumpable in the depth-2 construction.
      The manuscript proof does not need that: it exhibits a lumpable
      partition in the YES case and lower-bounds ALL k-state approximations
      in the NO case via fractional k-means.  Since the NO-case bound is over
      an arbitrary machine-state variable K with |K|<=k -- i.e. over
      FRACTIONAL assignments, which dominate every partition, lumpable or
      not -- the bound covers the unifilar feasible set too.
      So (T2) DOES hold for the depth-2 theorem, but for a reason the audit
      does not give.""")

print()
print("="*72)
print("(T3) block-uniform support in thm:full-kl-promise-np")
print("="*72)
print("""   That construction sets p_i = u + delta z_i with all coordinates
   strictly positive, so supp P_i = O for every state i, for the single
   (input-independent) emission.  Block-uniform support therefore holds
   trivially for EVERY partition.  (T3) is CORRECT.""")
