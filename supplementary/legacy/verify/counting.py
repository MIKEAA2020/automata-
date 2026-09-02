"""
Verify the counting bound restored into lem:littlestone.

Number of M-state Mealy machines over alphabets I, O with a designated
initial state:
    M                     choices of initial state
  * M^(M|I|)              transition table tau: Q x I -> Q
  * |O|^(M|I|)            output table lam: Q x I -> O

so  |H_M| = M^(M|I|+1) * |O|^(M|I|),  and
    log2|H_M| = (M|I|+1) log2 M + M|I| log2|O| = O(M log M) for fixed alphabets.
"""
import math
import itertools

print("=" * 72)
print("A. EXHAUSTIVE COUNT vs FORMULA (tiny cases)")
print("=" * 72)
for M in (1, 2):
    for nI, nO in ((1, 2), (2, 2), (2, 3)):
        I = list(range(nI))
        O = list(range(nO))
        pairs = [(q, a) for q in range(M) for a in I]
        n = len(pairs)
        # brute force
        cnt = 0
        for q0 in range(M):
            for tv in itertools.product(range(M), repeat=n):
                for lv in itertools.product(O, repeat=n):
                    cnt += 1
        formula = M ** (M * nI + 1) * nO ** (M * nI)
        ok = cnt == formula
        print(f"  M={M} |I|={nI} |O|={nO}:  brute={cnt:<8d} formula={formula:<8d} match={ok}")
        assert ok

print()
print("=" * 72)
print("B. log2|H_M| = Theta(M log M) for fixed alphabets")
print("=" * 72)
nI, nO = 2, 2
print(f"  |I|={nI}, |O|={nO}")
print(f"  {'M':>6} {'log2|H_M|':>12} {'M log2 M':>12} {'ratio':>8}")
for M in (2, 4, 8, 16, 32, 64, 128, 256, 512):
    lg = (M * nI + 1) * math.log2(M) + M * nI * math.log2(nO)
    mlm = M * math.log2(M)
    print(f"  {M:>6} {lg:>12.1f} {mlm:>12.1f} {lg/mlm:>8.3f}")

print()
print("  ratio -> |I| = 2 as M grows, confirming log2|H_M| = Theta(M log M)")
print("  with constants depending only on |I|,|O|.")

print()
print("=" * 72)
print("C. Ldim <= log2|H| (halving) and Ldim >= VCdim")
print("=" * 72)
print("  Halving: each mistake at least halves the version space, so any")
print("  shattered tree has depth <= log2|H|.  Hence Ldim <= log2|H_M| = O(M log M).")
print("  Ldim >= VCdim always, since a shattered SET yields a shattered TREE")
print("  (present every point in a fixed order).  With the automata VC bound")
print("  VCdim(H_M) = Omega(M log M), the two give Theta(M log M).")
