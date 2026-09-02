"""
=============================================================================
SUPERSEDED -- retained for provenance only.  DO NOT CITE.

This script compared "survivors = one class (c_2)" against "survivors =
complement (n - c_1)" and concluded that the RI setting of thm:active-halving
takes the complement form.  That was WRONG, and it tested the wrong model.

In the RI setting the version space is machine-STATE PAIRS.  Each pair (A,q)
is a DETERMINISTIC machine with a state, so under an input it emits exactly
ONE symbol.  The version space therefore partitions by emitted symbol just as
in the SI case, and a mistake retains a SINGLE class of size <= c_2 <= |V|/2.
The complement form never arises.

Corrected by verify/halving_ri.py (200,000 random version spaces, 0 cases with
survivors > |V|/2).  Manuscript: thm:active-halving proof and
rem:halving-alphabet-free now use the 1/2 factor uniformly.
=============================================================================
"""

"""Do the two halving arguments differ?  YES -- and the distinction is real.

(SI) prop:esyncsi-log : version space = STATES of a KNOWN machine.
     Each state maps to exactly ONE output under x.  A mistake leaves the
     survivors = ONE output class, of size <= c_2 <= |V|/2.   -> factor 1/2

(RI) thm:active-halving : version space = (machine,state) PAIRS, unknown
     machine.  A mistake DELETES the predicted class and keeps the REST,
     i.e. the union of all other classes, of size <= (1-1/|O|)|V|.
                                                       -> factor 1-1/|O|

The difference: in (SI) survivors are one class; in (RI) survivors are the
complement of one class.  Verify both extremes are attainable.
"""
import numpy as np, itertools
rng=np.random.default_rng(0)
print("Given class sizes c_1>=...>=c_r summing to n:")
print("  SI  survivors after a mistake = c_j for some j>=2   (a single class)")
print("  RI  survivors after a mistake = n - c_1             (the complement)")
print()
print(f"{'n':>4} {'r':>3} {'profile':>22} {'max c_2 (SI)':>13} {'n-c_1 (RI)':>11} {'SI/n':>7} {'RI/n':>7}")
for (n,r) in [(12,2),(12,3),(12,4),(12,6),(24,8)]:
    # adversary-optimal profile for each objective
    best_si=(0,None); best_ri=(0,None)
    for comp in itertools.combinations(range(1,n), r-1):
        p=np.diff(np.concatenate([[0],comp,[n]])); s=np.sort(p)[::-1]
        if s[1] > best_si[0]: best_si=(s[1],tuple(s))
        if n-s[0] > best_ri[0]: best_ri=(n-s[0],tuple(s))
    print(f"{n:>4} {r:>3} {str(best_si[1]):>22} {best_si[0]:>13} {best_ri[0]:>11}"
          f" {best_si[0]/n:>7.3f} {best_ri[0]/n:>7.3f}")
print()
print("=> SI ratio caps at 1/2 for every r; RI ratio grows to 1-1/r as r grows.")
print("   The sharpening applies to SI only.  thm:active-halving is unaffected.")
