"""DEEP: lem:packing-criterion compensation identity, prop:floors-instance,
and the disproof of the two-point floor.
"""
import numpy as np, math
rng=np.random.default_rng(4)
def kl(p,q):
    s=0.0
    for a,b in zip(p,q):
        if a>0:
            if b<=0: return float('inf')
            s+=a*math.log(a/b)
    return s

print("="*76)
print("(1) Compensation identity:  min_Q (1/m) sum_i KL(P^i||Q) = I(V;Y), V~Unif[m]")
print("    attained at the mixture Q = (1/m) sum_i P^i")
print("="*76)
worst=0.0; worst_opt=0.0
for _ in range(120000):
    m=int(rng.integers(2,7)); k=int(rng.integers(2,7))
    P=rng.dirichlet(np.ones(k)*rng.choice([0.3,1.0,3.0]),size=m)
    mix=P.mean(0)
    lhs=sum(kl(P[i],mix) for i in range(m))/m
    # I(V;Y) = H(mix) - (1/m) sum H(P_i)
    H=lambda p: -sum(x*math.log(x) for x in p if x>0)
    rhs=H(mix)-sum(H(P[i]) for i in range(m))/m
    worst=max(worst,abs(lhs-rhs))
    # confirm the mixture is the minimizer
    for _ in range(6):
        Q=rng.dirichlet(np.ones(k))
        alt=sum(kl(P[i],Q) for i in range(m))/m
        worst_opt=min(worst_opt, alt-lhs)
print(f"  120000 packings: max |avg-KL at mixture - I(V;Y)| = {worst:.3e}")
print(f"                   min (competitor - mixture) value = {worst_opt:.3e}  (>=0 required)")

print()
print("="*76)
print("(2) Two-point floor is UNSATISFIABLE for Delta > 2 log 2")
print("    min_Q [KL(P0||Q)+KL(P1||Q)] = 2 JS(P0,P1) <= 2 log 2 = 1.3863")
print("="*76)
mx=0.0
for _ in range(300000):
    k=int(rng.integers(2,9))
    P0=rng.dirichlet(np.ones(k)*rng.choice([0.05,0.2,1.0]))
    P1=rng.dirichlet(np.ones(k)*rng.choice([0.05,0.2,1.0]))
    mix=(P0+P1)/2
    v=kl(P0,mix)+kl(P1,mix)
    mx=max(mx,v)
print(f"  300000 pairs: max sum-separation = {mx:.6f}   ceiling 2log2 = {2*math.log(2):.6f}")
print(f"  => any floor Delta_M > 1.3863 nats is unsatisfiable in the two-point form.")

print()
print("="*76)
print("(3) prop:floors-instance: deterministic transcripts => I(V;Y) = log m = M log M")
print("="*76)
for L in [1,2,3]:
    M=2**L; m=M**M
    print(f"  L={L} M={M}: m=M^M={m}, all transcripts distinct (deterministic),")
    print(f"           I(V;Y)=H(V)=log2 m = {math.log2(m):.0f} bits = M log2 M = {M*L}"
          f"  {'OK' if abs(math.log2(m)-M*L)<1e-9 else 'MISMATCH'}")

print()
print("="*76)
print("(4) rem:packing-per-regime: stochastic packings need T = Omega(M^3)")
print("="*76)
print("  M Bernoulli biases spaced ~1/M; resolving one needs ~M^2 samples.")
print(f"  {'M':>4} {'log2 m = M log2 M':>18} {'T=M log M':>10} {'T=M^3':>8}")
for M in [4,8,16,32]:
    print(f"  {M:>4} {M*math.log2(M):>18.0f} {M*math.log2(M):>10.0f} {M**3:>8}")
print("  => at T = Theta(M log M) the information is a small fraction of log m;")
print("     the floor in a stochastic regime needs an explicit horizon hypothesis.")
