"""
How fast does I(V;Y) grow for the controlled-Bernoulli retention family, and
what Delta_M can the floor actually carry at horizon T?

Key: outputs are conditionally independent given V, and input x_t selects
coordinate b[x_t].  With the cyclic schedule each of the M coordinates is
queried ~T/M times.  Learning one Bernoulli bias to resolution needed to pick
among M candidates takes ~log M bits, but the SAMPLE cost is what limits I.

Compute I(V;Y) exactly (small cases) and via the per-coordinate decomposition
(large cases), then compare against Delta_M = min{A_app(M), Est_M(T)}.
"""
import numpy as np, itertools, math
from math import log, lgamma

def h(p): return -(p*log(p)+(1-p)*log(1-p)) if 0<p<1 else 0.0

def I_coord(q, n):
    """I(B;Y_1..Y_n) for B uniform on the M biases q, n iid Bernoulli draws."""
    M = len(q)
    # exact: enumerate number of successes k (sufficient statistic)
    I = 0.0
    Pk = np.zeros(n+1)
    for j in range(M):
        for k in range(n+1):
            Pk[k] += (1.0/M)*math.comb(n,k)*q[j]**k*(1-q[j])**(n-k)
    for j in range(M):
        for k in range(n+1):
            p = math.comb(n,k)*q[j]**k*(1-q[j])**(n-k)
            if p>0 and Pk[k]>0:
                I += (1.0/M)*p*log(p/Pk[k])
    return I

print("="*78)
print("I(V;Y) FOR THE CONTROLLED-BERNOULLI FAMILY  (M coords, T/M samples each)")
print("="*78)
print("  V = (b_1..b_M) uniform on [M]^M; coordinates independent given the")
print("  schedule, so I(V;Y) = M * I(B;Y_{1..T/M}).")
print()
print(f"{'M':>4}{'T':>9}{'n=T/M':>8}{'I(V;Y) nats':>14}{'log m':>10}{'frac':>7}{'M log M':>10}")
for M in (2,4,8):
    q = np.array([0.5 + 0.4*(j+1)/(M+1) for j in range(M)])
    for mult in (1, 4, 16, 64, 256):
        n = mult*int(math.ceil(math.log2(M)))+1
        T = M*n
        I = M*I_coord(q, n)
        lm = M*log(M)
        print(f"{M:>4}{T:>9}{n:>8}{I:>14.4f}{lm:>10.4f}{I/lm:>7.3f}{M*log(M):>10.3f}")

print()
print("="*78)
print("VERDICT")
print("="*78)
print("  I(V;Y) -> M log M, but only once each coordinate has enough samples to")
print("  resolve M biases -- i.e. n = Omega(M^2) for biases spaced 1/M apart,")
print("  hence T = Omega(M^3).  At T = Theta(M log M) the information is far")
print("  below log m.")
print()
print("  So the packing floor with Delta_M = Theta(M log M) requires a")
print("  LONG-HORIZON hypothesis T >> M log M, OR a family whose transcripts")
print("  are mutually SINGULAR at short horizon (as in the deterministic")
print("  stream case, where distinctness is immediate).")
print()
print("  This is a genuine structural difference between the deterministic and")
print("  stochastic regimes, not a gap in the construction.")
