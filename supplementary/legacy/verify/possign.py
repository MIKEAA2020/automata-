"""
Audit item 6: is rho_safe = Safe_lin^loc - Safe_quad a NONNEGATIVE
'relaxation gap'?  Test on the manuscript's own singleton example.

Two states, weights 1/2,1/2, scalar features y1=1, y2=-1, singleton safety
blocks.  G = [[1/2,-1/2],[-1/2,1/2]],  E_A G = diag(1/2,1/2).
"""
import numpy as np

G = np.array([[0.5, -0.5], [-0.5, 0.5]])
EAG = np.array([[0.5, 0.0], [0.0, 0.5]])


def kyfan(A, r):
    ev = np.sort(np.linalg.eigvalsh(A))[::-1]
    return float(ev[:r].sum())


print("=" * 74)
print("Manuscript's singleton example, M = 2  (so r = M-1 = 1)")
print("=" * 74)
r = 1
free_lin = 0.5 * kyfan(G, r)
safe_lin = 0.5 * kyfan(EAG, r)
print(f"  Free_lin(2)          = 1/2 * KyFan_1(G)      = {free_lin}")
print(f"  Safe_lin^loc(2)      = 1/2 * KyFan_1(E_A G)  = {safe_lin}")
print(f"  PoS_lin(2)           = {free_lin - safe_lin}")

# discrete quadratic values: both free and safe partitions separate the states,
# so both achieve the full separation value 1/2 (per the manuscript's text).
free_quad = 0.5
safe_quad = 0.5
print(f"  Free_quad(2)         = {free_quad}")
print(f"  Safe_quad(2)         = {safe_quad}")
print(f"  PoS_quad(2)          = {free_quad - safe_quad}")

rho_free = free_lin - free_quad
rho_safe = safe_lin - safe_quad
print()
print(f"  rho_free(2) = Free_lin - Free_quad = {free_lin} - {free_quad} = {rho_free}")
print(f"  rho_safe(2) = Safe_lin - Safe_quad = {safe_lin} - {safe_quad} = {rho_safe}")

print()
print("=" * 74)
print("VERDICT")
print("=" * 74)
print(f"  rho_safe(2) = {rho_safe} < 0   ->  NOT a nonnegative 'relaxation gap'.")
assert rho_safe < 0
print("  AUDIT ITEM 6 CONFIRMED.")
print()
print("  Check the identity still holds (it is pure algebra):")
lhs = free_quad - safe_quad
rhs = (free_lin - safe_lin) + rho_safe - rho_free
print(f"    PoS_quad = {lhs};   PoS_lin + rho_safe - rho_free = {rhs}")
assert abs(lhs - rhs) < 1e-12
print("    identity holds.  So the PROPOSITION is fine as an identity;")
print("    it is clause (ii)'s nonnegativity premise and clause (iii) that fail.")

print()
print("  Clause (iii) test: top (M-1)-eigenspace of G realizable by a safe")
print("  right congruence?  Here safety blocks are singletons, the discrete")
print("  safe partition separates both states, and PoS_quad = 0 while")
print(f"  PoS_lin = {free_lin - safe_lin} != 0.  So clause (iii) is FALSE.")
assert (free_lin - safe_lin) != (free_quad - safe_quad)
print("  AUDIT ITEM 6 (iii) CONFIRMED as a counterexample.")
