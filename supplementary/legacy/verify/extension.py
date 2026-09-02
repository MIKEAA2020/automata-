"""
meta:boolean (ii): is  kappa_obs(delta,mu) = index(~_{delta,S})  when
S = supp(mu) is right-closed with positive mass?

kappa_obs = min index of a GLOBAL right congruence ~ on I* admitting a
representative map correct mu-a.e. (i.e. on S).

~_{delta,S} = support-relative Nerode relation on I*:
    u ~ v  iff  for all w with uw, vw in S: delta(uw) = delta(vw).

The audit's worry: a congruence on S need not extend to a GLOBAL right
congruence of the same index, because histories outside S may re-enter S.

KEY OBSERVATION (to test): if S is RIGHT-CLOSED (u in S, then uw in S for all
w), then no history outside S can ever re-enter S -- right-closure means S is
forward-invariant, so I* \\ S is also forward-invariant in the reverse sense:
if u not in S then uw not in S?  NO -- right-closed means closed under
extension, so the complement is closed under PREFIX. A word outside S can
never become a word inside S by extension. Let's verify that and then verify
the extension lemma by brute force.
"""
import itertools
from itertools import product

I = ['a', 'b']


def words(maxlen):
    out = ['']
    for L in range(1, maxlen + 1):
        out += [''.join(p) for p in product(I, repeat=L)]
    return out


MAXLEN = 5
W = words(MAXLEN)
Widx = {w: i for i, w in enumerate(W)}


def right_closed(S):
    """u in S and |uw|<=MAXLEN  =>  uw in S."""
    for u in S:
        for x in I:
            if len(u) + 1 <= MAXLEN and (u + x) not in S:
                return False
    return True


def sr_nerode(delta, S):
    """Partition W by the support-relative Nerode relation."""
    def sig(u):
        s = []
        for w in W:
            if len(u) + len(w) <= MAXLEN and (u + w) in S:
                s.append((w, delta[u + w]))
        return tuple(s)
    classes = {}
    for u in W:
        classes.setdefault(sig(u), []).append(u)
    return list(classes.values())


def is_right_congruence(part):
    """Partition of W is a right congruence (w.r.t. one-letter extension)."""
    cls = {}
    for i, block in enumerate(part):
        for u in block:
            cls[u] = i
    for u in W:
        for x in I:
            uu = u + x
            if len(uu) > MAXLEN:
                continue
            for v in W:
                if cls.get(v) != cls.get(u) or len(v) + 1 > MAXLEN:
                    continue
                vv = v + x
                if cls.get(uu) != cls.get(vv):
                    return False
    return True


print("=" * 76)
print("A. RIGHT-CLOSURE MEANS THE COMPLEMENT CANNOT RE-ENTER S")
print("=" * 76)
print("  If S is right-closed (u in S => uw in S), then u not in S implies")
print("  no extension uw is in S ONLY IF S is also prefix-closed-complement.")
print("  Check: is that automatic?  Counterexample search.")
found = None
# S right-closed but some u outside S has an extension inside S
for trial in range(200000):
    import random
    random.seed(trial)
    S = set()
    # build a right-closed set: pick some minimal words, close under extension
    seeds = random.sample(W, random.randint(1, 3))
    for s in seeds:
        for w in W:
            if len(s) + len(w) <= MAXLEN:
                S.add(s + w)
    if not right_closed(S):
        continue
    for u in W:
        if u in S:
            continue
        for x in I:
            if len(u) + 1 <= MAXLEN and (u + x) in S:
                found = (sorted(S)[:6], u, u + x)
                break
        if found:
            break
    if found:
        break

if found:
    print(f"  FOUND: S (sample) = {found[0]}...,  u = '{found[1]}' not in S,")
    print(f"         but u+x = '{found[2]}' IS in S.")
    print("  => right-closure does NOT prevent re-entry. The audit's worry is REAL.")
else:
    print("  none found")

print()
print("=" * 76)
print("B. DOES THE INDEX-PRESERVING EXTENSION ACTUALLY FAIL?")
print("=" * 76)
print("  Search: delta and right-closed S where")
print("     min index of a GLOBAL right congruence correct on S")
print("   > index of the support-relative Nerode relation.")

import random
worst = None
tested = 0
for trial in range(60000):
    random.seed(trial + 10 ** 6)
    seeds = random.sample(W, random.randint(1, 2))
    S = set()
    for s in seeds:
        for w in W:
            if len(s) + len(w) <= MAXLEN:
                S.add(s + w)
    if not right_closed(S) or len(S) < 3:
        continue
    delta = {w: random.randint(0, 1) for w in W}
    part = sr_nerode(delta, S)
    k_sr = len(part)
    tested += 1
    # brute force: smallest global right congruence correct on S
    # search partitions of W with <= k_sr blocks is huge; instead test whether
    # the sr-Nerode partition ITSELF is a global right congruence.
    if not is_right_congruence(part):
        worst = (sorted(S)[:5], k_sr, dict(list(delta.items())[:6]))
        break

print(f"  tested {tested} (delta, right-closed S) pairs")
if worst:
    print("  FOUND a case where the support-relative Nerode partition is NOT")
    print("  itself a global right congruence:")
    print(f"    S (sample) = {worst[0]}...   index = {worst[1]}")
    print("  => the equality kappa_obs = index(~_{delta,S}) needs an extension")
    print("     lemma; it is not immediate.  AUDIT ITEM CONFIRMED.")
else:
    print("  the sr-Nerode partition was a global right congruence in every")
    print("  case tested, so the equality survived these tests.")
