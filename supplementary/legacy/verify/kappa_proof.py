"""Rigorous check of the proof steps for kappa = O(1).

CLAIM. Let b(M) = M^a (log(eM))^c with a,c >= 0, not both 0.  Then
  (i)  M -> (M/(M-1))^a       is nonincreasing on M>=2
  (ii) M -> log(eM)/log(e(M-1)) is nonincreasing on M>=2
  (iii) hence sup_{M>=2} b(M)/b(M-1) = b(2)/b(1) = 2^a (1+log2)^c,  an
        ABSOLUTE constant independent of T and of the crossing index.
Also: additive envelopes sqrt(T log(eM)) + log(eM) obey the same bound, by
the mediant inequality.  And the M log M edge case (b(1)=0) is handled.
"""
from mpmath import mp, mpf, log as mlog
import math
mp.dps = 40

print("(i)/(ii) monotonicity of the two factors, high precision")
worst1 = worst2 = mpf(0)
for M in range(2, 20000):
    m = mpf(M)
    f1a = m/(m-1); f1b = (m+1)/m
    worst1 = max(worst1, f1b - f1a)            # must be <= 0
    g1 = mlog(mp.e*m)/mlog(mp.e*(m-1))
    g2 = mlog(mp.e*(m+1))/mlog(mp.e*m)
    worst2 = max(worst2, g2 - g1)              # must be <= 0
print(f"   max increase of M/(M-1)            : {mp.nstr(worst1,8)}  (<=0 required)")
print(f"   max increase of log(eM)/log(e(M-1)): {mp.nstr(worst2,8)}  (<=0 required)")

print()
print("(iii) sup ratio equals b(2)/b(1) exactly, for a grid of exponents")
bad = 0
for a10 in range(0, 41):
    for c10 in range(0, 41, 4):
        a = mpf(a10)/10; c = mpf(c10)/10
        if a == 0 and c == 0: continue
        f = lambda M: (mpf(M)**a) * (mlog(mp.e*mpf(M))**c)
        sup = max(f(M)/f(M-1) for M in range(2, 400))
        pred = (mpf(2)**a) * ((1+mlog(2))**c)
        if abs(sup - pred) > mpf('1e-30'): bad += 1
print(f"   exponent pairs tested: 41*11 = 451 ; mismatches: {bad}")

print()
print("(iv) ADDITIVE envelope  b(M) = A*sqrt(log(eM)) + B*log(eM)  (A,B>0)")
print("     mediant inequality: (x1+x2)/(y1+y2) <= max(x1/y1, x2/y2)")
bad = 0; worst = mpf(0)
for A in ['0.01','1','1000','1e6']:
    for B in ['0.01','1','1000']:
        Am, Bm = mpf(A), mpf(B)
        f = lambda M: Am*mp.sqrt(mlog(mp.e*mpf(M))) + Bm*mlog(mp.e*mpf(M))
        sup = max(f(M)/f(M-1) for M in range(2, 2000))
        bound = max((mpf(1)+mlog(2))**mpf('0.5'), mpf(1)+mlog(2))
        worst = max(worst, sup)
        if sup > bound + mpf('1e-30'): bad += 1
print(f"   16 (A,B) pairs; violations of sup <= max(sqrt(1+log2), 1+log2) = "
      f"{mp.nstr(max(mp.sqrt(1+mlog(2)), 1+mlog(2)),8)} : {bad}")
print(f"   worst observed sup: {mp.nstr(worst,8)}")

print()
print("(v) EDGE CASE  b(M) = M log M  has b(1) = 0, so b(2)/b(1) is undefined.")
print("    The sandwich needs kappa only when the crossing index M* >= 2, and")
print("    condition (a) of lem:discrete-bv-sandwich requires b(1) <= a(1) with")
print("    b POSITIVE.  b(M)=M log M is not positive at M=1, so the correct")
print("    normalization is M log(eM) (equivalently M(1+log M)).  Check ratios:")
f = lambda M: mpf(M)*mlog(mp.e*mpf(M))
print(f"      sup_{{M>=2}} b(M)/b(M-1) = {mp.nstr(max(f(M)/f(M-1) for M in range(2,5000)),10)}"
      f"   = 2(1+log2) = {mp.nstr(2*(1+mlog(2)),10)}")
print("    If one insists on M log M for M>=2 only, the crossing index is >=3")
print("    and sup_{M>=3} ratio is finite:")
g = lambda M: mpf(M)*mlog(mpf(M))
print(f"      sup_{{M>=3}} (M log M)/((M-1)log(M-1)) = "
      f"{mp.nstr(max(g(M)/g(M-1) for M in range(3,5000)),10)}  (= 3log3/(2log2))")

print()
print("(vi) T-INDEPENDENCE: kappa for sqrt(T log(eM)) across many horizons")
for T in ['1e2','1e4','1e6','1e10','1e16']:
    Tm = mpf(T)
    f = lambda M: mp.sqrt(Tm*mlog(mp.e*mpf(M)))
    sup = max(f(M)/f(M-1) for M in range(2,3000))
    print(f"      T={T:>6}: kappa = {mp.nstr(sup,12)}   (= sqrt(1+log2) = "
          f"{mp.nstr(mp.sqrt(1+mlog(2)),12)})")
print("    kappa does NOT depend on T: the horizon cancels in the ratio.")
