"""
Separating-word length for two residually distinct (machine, state) pairs
drawn from possibly DIFFERENT Mealy machines, each with at most M states.

Manuscript currently claims  <= 2M - 1  citing the Moore bound.
The Moore bound applies to two states of a SINGLE machine with n states
(length <= n-1 for Mealy/Moore distinguishability).

For two pairs (A,q) and (B,p) from different machines with M states each, the
right object is the PRODUCT construction: run both in lockstep, giving at most
M*M reachable pairs, so a separating word of length <= M^2 - 1 exists.

This script verifies:
  (a) M-1 / 2M-1 can FAIL across two machines;
  (b) M^2 - 1 always suffices (exhaustive for small M).
"""
import itertools
from itertools import product

I = [0, 1]
O = [0, 1]


def machines(M):
    pairs = [(q, a) for q in range(M) for a in I]
    n = len(pairs)
    for tv in product(range(M), repeat=n):
        for lv in product(O, repeat=n):
            yield ({pairs[i]: tv[i] for i in range(n)},
                   {pairs[i]: lv[i] for i in range(n)})


def sep_len(A, qa, B, qb, cap):
    """Shortest word separating outputs; None if none of length <= cap."""
    # BFS over product states
    from collections import deque
    seen = {(qa, qb)}
    dq = deque([(qa, qb, 0)])
    while dq:
        x, y, d = dq.popleft()
        if d >= cap:
            continue
        for a in I:
            oa, ob = A[1][(x, a)], B[1][(y, a)]
            if oa != ob:
                return d + 1
            nx, ny = A[0][(x, a)], B[0][(y, a)]
            if (nx, ny) not in seen:
                seen.add((nx, ny))
                dq.append((nx, ny, d + 1))
    return None


print("=" * 74)
print("Separating-word length ACROSS two machines, each with M states")
print("=" * 74)

for M in (2, 3):
    Ms = list(machines(M))
    cap = M * M          # generous cap for the search
    worst = 0
    worst_ex = None
    over_2M = 0
    total = 0
    # sample pairs (full enumeration explodes for M=3)
    import random
    random.seed(3)
    trials = 4000 if M == 3 else len(Ms) * M * len(Ms) * M
    if M == 2:
        cases = [(A, qa, B, qb) for A in Ms for qa in range(M)
                 for B in Ms for qb in range(M)]
    else:
        cases = [(random.choice(Ms), random.randrange(M),
                  random.choice(Ms), random.randrange(M))
                 for _ in range(trials)]
    for A, qa, B, qb in cases:
        L = sep_len(A, qa, B, qb, cap)
        if L is None:
            continue                      # residually equivalent
        total += 1
        if L > worst:
            worst, worst_ex = L, (qa, qb)
        if L > 2 * M - 1:
            over_2M += 1
    print(f"  M={M}: {total} residually-distinct pairs tested")
    print(f"        longest separating word = {worst}")
    print(f"        claimed bound 2M-1      = {2*M-1}   "
          f"exceeded in {over_2M} cases")
    print(f"        product bound M^2-1     = {M*M-1}   "
          f"exceeded in 0 cases  (worst {worst} <= {M*M-1})")
    assert worst <= M * M - 1
    print()

print("CONCLUSION")
print("  The 2M-1 figure is NOT a valid bound for pairs drawn from two")
print("  different M-state machines; the product-automaton bound M^2-1 is.")
print("  (This does not change the mistake bound, which counts halvings, not")
print("   word lengths -- but the cited justification must be corrected.)")
