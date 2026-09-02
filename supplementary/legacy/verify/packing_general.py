"""
A GENERAL sufficient condition for the packing floor, then a retention instance.

General lemma (log loss):  the floor
    (1/m) sum_i KL(P^i || Q_h) >= Delta_M   for every predictor h
is EXACTLY  I(V;Y_{1:T}) >= Delta_M  with V uniform on [m], because
    min_Q (1/m) sum_i KL(P^i||Q) = I(V;Y).
So the floor holds iff the family carries Delta_M nats of information about
its index.  No per-regime argument is needed beyond exhibiting such a family.

Retention instance: controlled Bernoulli machine.
  inputs [M] select a hidden state; state i emits Bernoulli(q_{b_i}),
  b in [M]^M, so m = M^M and log m = M log M.
  Cycle the input 1,2,...,M repeatedly.
Verify I(V;Y_{1:T}) -> log m = M log M as T grows.
"""
import numpy as np, itertools, math

def IVY_exact(P):
    """P: m x |Y| matrix of transcript probabilities. I(V;Y), V uniform."""
    m = P.shape[0]
    Pbar = P.mean(axis=0)
    I = 0.0
    for i in range(m):
        pi = P[i]; msk = pi > 0
        I += (1.0/m)*np.sum(pi[msk]*np.log(pi[msk]/Pbar[msk]))
    return I

print("="*76)
print("A. THE FLOOR IS EXACTLY  I(V;Y) >= Delta_M   (identity re-checked)")
print("="*76)
rng = np.random.default_rng(0)
worst = 0.0
for _ in range(50000):
    m = int(rng.integers(2,6)); n = int(rng.integers(2,7))
    P = np.array([rng.dirichlet(np.ones(n)) for _ in range(m)])
    base = IVY_exact(P)
    for _ in range(4):
        Q = 0.8*P.mean(axis=0) + 0.2*rng.dirichlet(np.ones(n))
        val = np.mean([np.sum(P[i][P[i]>0]*np.log(P[i][P[i]>0]/Q[P[i]>0])) for i in range(m)])
        worst = min(worst, val-base)
print(f"  min (competitor - mixture) over 50k trials: {worst:.3e}  (>=0 required)")
assert worst >= -1e-9
print("  identity confirmed: min_Q average-KL = I(V;Y)")

print()
print("="*76)
print("B. RETENTION INSTANCE: controlled Bernoulli, m = M^M")
print("="*76)
print(f"{'M':>3}{'m=M^M':>8}{'T':>5}{'I(V;Y) nats':>14}{'log m':>10}{'ratio':>8}")
for M in (2,3):
    q = np.array([0.5 + 0.35*(j+1)/M for j in range(M)])   # M distinct biases
    idx = list(itertools.product(range(M), repeat=M))       # b in [M]^M
    m = len(idx)
    for T in (M*4, M*8, M*16):
        xs = [t % M for t in range(T)]                      # cycle inputs
        # exact over all output strings is 2^T; use per-coordinate factorisation:
        # transcripts factorise, so I(V;Y) = H(Ybar) - mean_i H(Y|V=i) computed
        # coordinatewise only if outputs independent given V -- they are.
        # H(Y|V=i) = sum_t h(q[b_{x_t}])
        def h(p): return -(p*np.log(p)+(1-p)*np.log(1-p))
        HYgV = np.mean([sum(h(q[b[x]]) for x in xs) for b in idx])
        # H(Y): outputs are NOT independent unconditionally; compute exactly
        # for small T by enumerating 2^T strings.
        if T <= 16:
            P = np.zeros((m, 2**T))
            for i,b in enumerate(idx):
                probs = np.array([q[b[x]] for x in xs])
                for code in range(2**T):
                    bits = np.array([(code>>t)&1 for t in range(T)])
                    P[i,code] = np.prod(np.where(bits==1, probs, 1-probs))
            I = IVY_exact(P)
        else:
            I = float('nan')
        print(f"{M:>3}{m:>8}{T:>5}{I:>14.4f}{math.log(m):>10.4f}{I/math.log(m):>8.3f}")

print()
print("="*76)
print("C. LIMIT: I(V;Y) -> log m = M log M as T grows")
print("="*76)
print("  The processes are pairwise distinguishable (distinct bias vectors),")
print("  so V is recoverable from a long enough transcript and I(V;Y) -> H(V).")
for M in (2,4,8,16,32):
    print(f"    M={M:>3}: log m = M ln M = {M*math.log(M):8.3f} nats"
          f"  = {M*math.log2(M):8.1f} bits")
print()
print("  Est_M(T) = Theta(M log M), so Delta_M <= Est_M(T) is covered by this")
print("  packing for T large enough that V is recoverable.")
