"""
The gap the audit missed: in the ACTIVE protocol the learner may CHAIN the c letter.

c: v -> g(v), emitting 0.  So from v the learner can reach g(g(v)) without ever
reading out g(v).  A d^L readout there reveals bits of g at an argument the learner
does not know.  The adversary's "lazy, independent bit" bookkeeping then fails,
because the answer constrains g at an argument that itself depends on unrevealed bits.
"""
import itertools, random

L = 2
M = 2 ** L
Q = [tuple(b) for b in itertools.product([0, 1], repeat=L)]
zero = tuple([0] * L)
idx = {v: i for i, v in enumerate(Q)}


def rot(v):
    return v[1:] + v[:1]


# ---------------------------------------------------------------- chained readout
allg = list(itertools.product(Q, repeat=M))  # g as tuple indexed by Q order
target = Q[1]                                # pretend readout said g(g(0^L)) = target
cons = [g for g in allg if g[idx[g[idx[zero]]]] == target]

print("=" * 74)
print("A. CHAINING BREAKS THE PRODUCT STRUCTURE  (family of thm:stream-lower-bound)")
print("=" * 74)
print(f"L={L}, M={M}: |all g| = {len(allg)},  "
      f"|g consistent with ONE chained readout g(g(0^L))={target}| = {len(cons)}")

proj = [set(g[i] for g in cons) for i in range(M)]
prod_size = 1
for p in proj:
    prod_size *= len(p)
print("  per-argument projection sizes:", [len(p) for p in proj],
      " -> product =", prod_size)
print("  IS THE CONSISTENT SET A PRODUCT SET?", prod_size == len(cons))
assert prod_size != len(cons), "expected non-product"
print("  => chained readouts create CORRELATED constraints across arguments.")
print("     The per-bit lazy adversary (and the uniform-conditional-bit step of")
print("     the Yao argument) is INVALID as written in the active protocol.\n")

# ---------------------------------------------------------------- gated family
print("=" * 74)
print("B. THE GATED FAMILY RESTORES IT")
print("=" * 74)
print("states Q x {free,read}, so 2M states:")
print("  (free,v): r->(free,0^L)/0  e->(free,flip v)/0  d->(free,rot v)/v_1  c->(read,g(v))/0")
print("  (read,u): r->(free,0^L)/0  e->(read,u)/0       d->(read,rot u)/u_1  c->(read,u)/0")
print("                                                                       ^^^ c GATED\n")

bad = 0
distinct = set()
for trial in range(200000):
    g = {v: random.choice(Q) for v in Q}
    mode, st = 'free', zero
    free_at_c = None          # the argument the learner transported to
    for _ in range(14):
        x = random.choice('redc')
        if x == 'r':
            mode, st, free_at_c = 'free', zero, None
        elif x == 'e':
            if mode == 'free':
                st = st[:-1] + (1 - st[-1],)
        elif x == 'c':
            if mode == 'free':
                free_at_c = st
                mode, st = 'read', g[st]
            # in read mode c is a no-op: no chaining
        else:  # d
            if mode == 'read':
                # the register is a rotation of g(free_at_c); check the argument
                if free_at_c is None:
                    bad += 1
                else:
                    distinct.add(free_at_c)
            st = rot(st)

print(f"  200000 random active runs, 14 rounds each.")
print(f"  readouts whose argument was NOT a learner-chosen free-mode state: {bad}")
print(f"  distinct readout arguments observed: {len(distinct)} (<= M = {M})")
assert bad == 0
print("  => every readout argument is the free-mode state the learner itself")
print("     transported to, hence known to it.  The consistent set therefore")
print("     remains a PRODUCT of per-argument partial assignments at all times,")
print("     and conditional uniformity of each unrevealed bit holds.\n")

# ---------------------------------------------------------------- product check, gated
print("  Product check for the gated family: after readouts at a SET S of known")
print("  arguments with prescribed values, the consistent set is exactly the")
print("  product over v of ({those values} if v in S else Q).")
S = {zero: Q[1], Q[2]: Q[3]}
consg = [g for g in allg if all(g[idx[v]] == u for v, u in S.items())]
expect = 1
for v in Q:
    expect *= 1 if v in S else M
print(f"  |consistent| = {len(consg)},  predicted product size = {expect},  "
      f"MATCH = {len(consg) == expect}")
assert len(consg) == expect
print("\nALL CHECKS PASSED")
