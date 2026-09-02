"""
T39 / Item-1 audit.  Question: for an OUTPUT-INDEPENDENT (input-driven) machine,
does Definition (unifilar lumpability, restricted to jointly FEASIBLE triples)
coincide with Definition (ordinary lumpability, tau_0-based)?

The manuscript currently asserts (def:unifilar-lumpable):
   "for an output-independent update the condition reduces to
    Definition~\ref{def:lumpable-quotient}."
and the audit's proposed prop:input-driven-specialization(i) asserts equivalence.

We test both directions by exhaustive enumeration over small machines.
"""
import itertools, sys
from itertools import product

def partitions(n):
    # restricted growth strings
    def rec(i, mx, cur):
        if i == n:
            yield tuple(cur); return
        for b in range(mx+1):
            cur.append(b); yield from rec(i+1, max(mx, b+1), cur); cur.pop()
    yield from rec(0, 0, [])

def lumpable(phi, tau0, nS, nI):
    """ordinary lumpability: phi(tau0(s,x)) depends only on (phi(s),x)"""
    for x in range(nI):
        img = {}
        for s in range(nS):
            k = phi[s]; v = phi[tau0[s][x]]
            if k in img and img[k] != v: return False
            img[k] = v
    return True

def unif_lumpable(phi, tau0, supp, nS, nI):
    """unifilar lumpability restricted to feasible (s,x,y):
       need tau_K(k,x,y) well defined, i.e. for s,s' in same block and a
       COMMON feasible y, phi(tau(s,x,y))==phi(tau(s',x,y)).
       With output-independent tau, tau(s,x,y)=tau0(s,x)."""
    for x in range(nI):
        img = {}                      # (k,x,y) -> block
        for s in range(nS):
            k = phi[s]; v = phi[tau0[s][x]]
            for y in supp[s][x]:
                key = (k, y)
                if key in img and img[key] != v: return False
                img[key] = v
    return True

nS, nI, nO = 3, 1, 2
found_ul_not_l = None
cnt_ul = cnt_l = 0
tot = 0
for tau0 in product(product(range(nS), repeat=nI), repeat=nS):
    tau0 = [list(r) for r in tau0]
    # supports: nonempty subsets of O for each (s,x)
    subs = [tuple(S) for r in range(1, nO+1) for S in itertools.combinations(range(nO), r)]
    for supptup in product(product(subs, repeat=nI), repeat=nS):
        supp = [[set(c) for c in r] for r in supptup]
        for phi in partitions(nS):
            tot += 1
            L = lumpable(phi, tau0, nS, nI)
            U = unif_lumpable(phi, tau0, supp, nS, nI)
            cnt_l += L; cnt_ul += U
            if L and not U:
                print("*** FOUND lumpable but NOT unifilar-lumpable:", tau0, supptup, phi); sys.exit(1)
            if U and not L and found_ul_not_l is None:
                found_ul_not_l = (tau0, supptup, phi)

print(f"enumerated {tot} (machine,partition) pairs with |S|={nS},|I|={nI},|O|={nO}")
print(f"  lumpable: {cnt_l}   unifilar-lumpable: {cnt_ul}")
print("  direction lumpable => unifilar-lumpable: NO COUNTEREXAMPLE (as proved)")
if found_ul_not_l:
    tau0, supptup, phi = found_ul_not_l
    print("  direction unifilar-lumpable => lumpable: *** REFUTED ***")
    print("    tau0 =", tau0, " supports =", supptup, " phi =", phi)
else:
    print("  direction unifilar-lumpable => lumpable: no counterexample found")
