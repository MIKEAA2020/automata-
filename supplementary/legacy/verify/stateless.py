"""
cor:stateless -- discounted vs one-stage value.

Global definition (Bellman, discounted):
    V(q) = min_a max_b [ r(q,a,b) + gamma V(delta(q,a,b)) ]

Strategic spread:
    alpha(q) = V(q) - max_b min_a [ r(q,a,b) + gamma V(delta(q,a,b)) ]

Stateless game: one state, delta trivial. Write
    m1 = min_a max_b r(a,b)      (one-stage alternating value)
    m2 = max_b min_a r(a,b)      (one-stage simultaneous guarantee)

Bellman:  V = m1 + gamma V   =>  V = m1/(1-gamma).
Spread:   alpha = V - (m2 + gamma V) = (1-gamma)V - m2 = m1 - m2.
Bound:    Com(M) >= sum_t gamma^t alpha = alpha/(1-gamma) = (m1-m2)/(1-gamma).

So the CORRECT alpha is  m1 - m2  with m1 the ONE-STAGE value, NOT the
discounted V.  The manuscript writes  alpha = V - max_b min_a r(a,b)  where V
is globally the DISCOUNTED value -- that is wrong unless V there means m1.
"""
import itertools
import random

random.seed(7)


def analyse(R, gamma, verbose=False):
    """R[a][b] payoff. Adversary picks a (min), agent picks b (max)."""
    na, nb = len(R), len(R[0])
    m1 = min(max(R[a][b] for b in range(nb)) for a in range(na))
    m2 = max(min(R[a][b] for a in range(na)) for b in range(nb))
    V = m1 / (1 - gamma)                    # solves V = m1 + gamma V
    # verify Bellman
    lhs = V
    rhs = min(max(R[a][b] + gamma * V for b in range(nb)) for a in range(na))
    assert abs(lhs - rhs) < 1e-9, (lhs, rhs)
    alpha_correct = m1 - m2
    # spread computed from the definition, with the discounted V
    alpha_def = V - max(min(R[a][b] + gamma * V for a in range(na))
                        for b in range(nb))
    assert abs(alpha_def - alpha_correct) < 1e-9, (alpha_def, alpha_correct)
    # what the manuscript's corollary literally says: alpha = V - m2
    alpha_manuscript = V - m2
    return m1, m2, V, alpha_correct, alpha_manuscript


print("=" * 78)
print("A. THE CORRECT SPREAD IS m1 - m2 (one-stage), NOT V - m2 (discounted)")
print("=" * 78)
print(f"{'game':>22} {'gamma':>6} {'m1':>7} {'m2':>7} {'V=m1/(1-g)':>11}"
      f" {'alpha=m1-m2':>12} {'V-m2 (MS)':>11} {'equal?':>7}")
games = [
    ("matching pennies", [[1, -1], [-1, 1]]),
    ("asymmetric",       [[3, 0], [1, 2]]),
    ("dominant",         [[2, 2], [1, 1]]),
    ("zero spread",      [[5, 5], [5, 5]]),
]
bad = 0
for name, R in games:
    for gamma in (0.0, 0.5, 0.9):
        m1, m2, V, ac, am = analyse(R, gamma)
        eq = abs(ac - am) < 1e-9
        if not eq:
            bad += 1
        print(f"{name:>22} {gamma:>6.2f} {m1:>7.3f} {m2:>7.3f} {V:>11.3f}"
              f" {ac:>12.3f} {am:>11.3f} {str(eq):>7}")

print()
print(f"  cases where V-m2 differs from the correct m1-m2: {bad} of {len(games)*3}")
print("  (they agree only when gamma = 0, i.e. when V = m1)")

print()
print("=" * 78)
print("B. THE DEFINITIONAL alpha ALWAYS EQUALS m1 - m2")
print("=" * 78)
print("  verified by assertion inside analyse() for every case above,")
print("  and on random games below.")
n = 0
for _ in range(200000):
    na, nb = random.randint(2, 4), random.randint(2, 4)
    R = [[random.uniform(-5, 5) for _ in range(nb)] for _ in range(na)]
    gamma = random.uniform(0, 0.99)
    analyse(R, gamma)          # assertions inside
    n += 1
print(f"  {n} random stateless games: Bellman consistent AND alpha == m1-m2 "
      f"in every case")

print()
print("=" * 78)
print("C. CONSEQUENCE FOR Com(M)")
print("=" * 78)
R = [[3, 0], [1, 2]]
gamma = 0.9
m1, m2, V, ac, am = analyse(R, gamma)
print(f"  game {R}, gamma={gamma}")
print(f"    m1 (one-stage alternating) = {m1}")
print(f"    m2 (one-stage simultaneous) = {m2}")
print(f"    V  (discounted)            = {V:.4f}")
print(f"    correct    Com(M) = (m1-m2)/(1-gamma) = {ac/(1-gamma):.4f}")
print(f"    manuscript Com(M) = (V -m2)/(1-gamma) = {am/(1-gamma):.4f}")
print(f"    overstatement factor = {am/ac:.2f}x")
print()
print("  => the corollary is off by using the discounted V where the")
print("     one-stage value m1 = min_a max_b r(a,b) is meant.")
print("     The PROOF is internally consistent (it writes V* = V/(1-gamma),")
print("     using V for the one-stage value), but that clashes with the")
print("     global Bellman definition of V(q) as the discounted value.")
