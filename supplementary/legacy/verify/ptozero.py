"""
Verify the p->0 claims to be restored.

(1)  lim_{p->0+} sum_{i>r} sigma_i^p  =  #{i>r : sigma_i > 0}
(2)  Phi^{(p)}_r(A) = (sum_{i>r} sigma_i^p)^{1/p} does NOT generally converge
     to a {0,inf} valuation.
"""
import numpy as np

print("=" * 72)
print("(1) unpowered sum -> tail rank count")
print("=" * 72)
for sig, r in [([3.0, 2.0, 1.0, 0.0], 1),
               ([5.0, 0.4, 0.1], 0),
               ([1.0, 1e-3, 1e-6, 0.0, 0.0], 1)]:
    sig = np.array(sig)
    count = int((sig[r:] > 0).sum())
    print(f"  sigma={list(sig)}  r={r}  true count={count}")
    for p in [1e-1, 1e-2, 1e-3, 1e-4]:
        val = float(np.sum(sig[r:][sig[r:] > 0] ** p))
        print(f"     p={p:<8g} sum sigma^p = {val:.6f}")
    assert abs(float(np.sum(sig[r:][sig[r:] > 0] ** 1e-6)) - count) < 1e-3
    print("     -> converges to the count  OK")
    print()

print("=" * 72)
print("(2) the POWERED tail Phi^{(p)}_r = (sum)^{1/p} does not give {0,inf}")
print("=" * 72)
for sig, r in [([3.0, 2.0, 1.0], 1),
               ([3.0, 0.5, 0.25], 1),
               ([3.0, 0.9], 1)]:
    sig = np.array(sig)
    tail = sig[r:][sig[r:] > 0]
    print(f"  sigma={list(sig)}  r={r}  tail={list(tail)}")
    for p in [1.0, 0.5, 0.1, 0.01, 0.001]:
        val = float(np.sum(tail ** p)) ** (1.0 / p)
        print(f"     p={p:<7g} Phi = {val:.6g}")
    # limit behaviour: max(tail) if count==1 else diverges/converges by count
    n = len(tail)
    mx = tail.max()
    lim = "-> +inf" if n > 1 and mx >= 1 else ("-> " + f"{mx:g}" if n == 1 else "depends")
    print(f"     n={n}, max={mx:g}   behaviour {lim}")
    print()

print("  => Phi^{(p)}_r tends to +inf when the tail has >1 nonzero of size >=1,")
print("     and to the max when the tail is a single value; it is NOT a")
print("     {0,inf}-valued Boolean valuation.  An extra thresholding map")
print("     t |-> 1{t>0} is required.  CLAIM CONFIRMED.")
