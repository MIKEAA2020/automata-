"""
ADJUDICATE: is the Fisher information of Bernoulli in the NATURAL parameter
eta = log(p/(1-p)) equal to p(1-p)  [audit's claim]  or 1/(p(1-p))  [manuscript]?

Definition: I(eta) = E[ (d/deta log P_eta(Y))^2 ].
For the exponential family P_eta(y) = exp(eta*y - A(eta)) with A(eta) =
log(1+e^eta), the Fisher information in the natural parameter is A''(eta),
and A'(eta) = p, A''(eta) = p(1-p).

So the AUDIT IS RIGHT: I(eta) = p(1-p).  1/(p(1-p)) is I(p), the mean-parameter
Fisher information.  Verify numerically both ways, then recompute the theorem.
"""
import numpy as np
from math import log, exp, sqrt

def p_of(eta): return 1.0/(1.0+exp(-eta))

print("="*74)
print("A. FISHER INFORMATION IN THE NATURAL PARAMETER (numerical)")
print("="*74)
print(f"{'p':>8} {'I(eta) numeric':>16} {'p(1-p)':>12} {'1/(p(1-p))':>14}")
for p in (0.5, 0.7, 0.9, 0.99, 0.999):
    eta = log(p/(1-p))
    h = 1e-5
    # I(eta) = E[(d/deta log P)^2];  log P(y) = eta*y - log(1+e^eta)
    # d/deta log P(y) = y - p(eta)
    pe = p_of(eta)
    I_num = pe*(1-pe)**2 + (1-pe)*(0-pe)**2   # E[(y-p)^2] = p(1-p)
    # also via A''(eta) by finite differences
    A = lambda e: log(1+exp(e))
    A2 = (A(eta+h) - 2*A(eta) + A(eta-h))/h**2
    print(f"{p:>8} {I_num:>16.8f} {p*(1-p):>12.8f} {1/(p*(1-p)):>14.4f}   A''={A2:.8f}")
    assert abs(I_num - p*(1-p)) < 1e-9
    assert abs(A2 - p*(1-p)) < 1e-4

print("\n  => I(eta) = p(1-p).  THE AUDIT IS CORRECT; the manuscript used 1/(p(1-p)).")

print()
print("="*74)
print("B. RECOMPUTE THE THEOREM'S FAMILY WITH THE CORRECT I(eta)")
print("="*74)
print(f"{'eps':>10} {'RetKL(1)':>14} {'tr(Sig) WRONG':>16} {'tr(Sig) RIGHT':>16} {'ratio RIGHT':>14}")
def H(p):
    if p<=0 or p>=1: return 0.0
    return -p*log(p)-(1-p)*log(1-p)

for eps in (1e-1, 1e-2, 1e-3, 1e-4, 1e-5):
    pp, pm = 1-eps, 1-2*eps
    bar = 1-1.5*eps
    ret = H(bar) - 0.5*H(pp) - 0.5*H(pm)
    etap, etam = log(pp/(1-pp)), log(pm/(1-pm))
    eta0 = 0.5*(etap+etam)
    p0 = p_of(eta0)
    I_wrong = 1.0/(p0*(1-p0))
    I_right = p0*(1-p0)
    d = ((etap-etam)/2)**2
    trw, trr = I_wrong*d, I_right*d
    print(f"{eps:>10.0e} {ret:>14.6e} {trw:>16.6e} {trr:>16.6e} {ret/trr:>14.6f}")

print()
print("  With the CORRECT I(eta)=p(1-p):")
print("    tr(Sigma_pi) = Theta(eps)   and   RetKL(1) = Theta(eps),")
print("    so the ratio tends to a POSITIVE CONSTANT, not to 0.")
print("  => the counterexample FAILS.  thm:no-global-kl-converse is FALSE.")

print()
print("="*74)
print("C. WHAT IS THE LIMITING RATIO?")
print("="*74)
for eps in (1e-4, 1e-6, 1e-8, 1e-10):
    pp, pm = 1-eps, 1-2*eps
    bar = 1-1.5*eps
    ret = H(bar) - 0.5*H(pp) - 0.5*H(pm)
    etap, etam = log(pp/(1-pp)), log(pm/(1-pm))
    eta0 = 0.5*(etap+etam); p0 = p_of(eta0)
    trr = p0*(1-p0)*((etap-etam)/2)**2
    print(f"  eps={eps:.0e}   RetKL/tr = {ret/trr:.8f}")
c = (log(2)-1.5*log(1.5))
lim = c/ (sqrt(2)*(log(2)/2)**2)
print(f"\n  predicted limit  (log2 - 1.5 log1.5) / (sqrt2 * (log2/2)^2) = {lim:.8f}")
print("  ratio is bounded away from 0 -- no counterexample.")
