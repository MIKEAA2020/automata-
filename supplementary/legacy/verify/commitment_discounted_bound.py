"""T54.  Salvage probe for a quantitative discounted commitment bound.

from fractions import Fraction as F
import itertools
print("="*76)
print("E2 salvage: is a correct discounted commitment lower bound available?")
print("="*76)
print("  mu_g(u) = (1-g) g^{|u|} P(X_{1:|u|}=u)")
print("  If A conflates residuals r_i, r_j, there is a separating continuation")
print("  w, |w|=d, and A errs on u_i w or u_j w.  That single history has")
print("  mu-weight (1-g) g^{|u_i|+d} P(X = u_i w).")
print()
print("  So a CORRECT bound needs |u| = length of the ACCESS word, not 0.")
print("  Let L = max over conflated pairs of min access length, D = separation")
print("  depth.  Then:")
print("      Delta >= (1-g) g^{L+D} * p_min^{L+D}")
print("  where p_min is the least positive input-letter probability.")
print()
k=2; pmin=F(1,2)
for g in (F(1,2),F(9,10)):
    for L,D in [(0,1),(1,1),(2,3),(3,2)]:
        b=(1-g)*g**(L+D)*pmin**(L+D)
        print(f"    g={g}, L={L}, D={D}, |I|={k}: bound = {b} = {float(b):.6g}")
print()
print("  The bound is POSITIVE but decays geometrically in L+D, so it is")
print("  far weaker than the audit's claim and depends on the access length,")
print("  which the audit's statement does not mention.")
print()
print("  Is L bounded by anything intrinsic?  For a minimal specification with")
print("  kappa residuals, each residual has an access word of length <= kappa-1,")
print("  and D <= kappa-1 (Moore separation).  So L+D <= 2(kappa-1).")
for kap in (2,3,4,5):
    g=F(9,10); b=(1-g)*g**(2*(kap-1))*pmin**(2*(kap-1))
    print(f"    kappa={kap}: L+D <= {2*(kap-1)}, bound >= {float(b):.6g}")
print()
print("  VERDICT: a correct statement exists but is exponentially weak in kappa")
print("  and requires two new parameters (access length, min input probability)")
print("  that the manuscript does not currently define.  It would add a")
print("  quantitative-looking result with no real strength.")
