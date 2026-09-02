"""
Audit counterexample, computed correctly.

I={a,b}, S=I^+ (right-closed), delta(u)=first letter of u for u in S.

(1) index(~_{delta,S}) : u ~ v iff for EVERY w with uw,vw in S,
    delta(uw)=delta(vw).  For u,v in S, uw in S always, and
    delta(uw)=first(u).  So u~v iff first(u)=first(v).  Index = 2.
    (Computed by pairwise comparison, not by signature tuples.)

(2) kappa_obs : minimum states of a reachable deterministic transition system
    over I with initial state eps and a label per state, correct on S.
"""
from itertools import product

I = ['a', 'b']
MAX = 6
W = ['']
for L in range(1, MAX + 1):
    W += [''.join(p) for p in product(I, repeat=L)]
S = [w for w in W if w]


def delta(u):
    return 'A' if u[0] == 'a' else 'B'


print("=" * 74)
print("A. index(~_{delta,S})  -- pairwise, no signature truncation")
print("=" * 74)


def related(u, v):
    for w in W:
        if len(u + w) <= MAX and len(v + w) <= MAX:
            if (u + w) in Sset and (v + w) in Sset:
                if delta(u + w) != delta(v + w):
                    return False
    return True


Sset = set(S)
reps = []
for u in S:
    if not any(related(u, r) for r in reps):
        reps.append(u)
print(f"  index(~_delta,S) = {len(reps)}   reps = {reps}")
assert len(reps) == 2, reps

print()
print("=" * 74)
print("B. kappa_obs = min states of a global right congruence exact on S")
print("=" * 74)


def feasible(k):
    states = range(k)
    for trans in product(states, repeat=k * len(I)):
        T = {(q, x): trans[q * len(I) + j]
             for q in states for j, x in enumerate(I)}
        lab, ok, reach = {}, True, set()
        for u in W:
            q = 0
            for x in u:
                q = T[(q, x)]
            reach.add(q)
            if u in Sset:
                d = delta(u)
                if q in lab and lab[q] != d:
                    ok = False
                    break
                lab[q] = d
        if ok and len(reach) == k:
            return T, lab
    return None


kmin, wit = None, None
for k in (1, 2, 3, 4):
    got = feasible(k)
    print(f"  k={k}: {'FEASIBLE' if got else 'infeasible'}")
    if got:
        kmin, wit = k, got
        break

T, lab = wit
print()
print(f"  kappa_obs = {kmin}")
print(f"  transitions {dict(sorted(T.items()))}")
print(f"  labels {lab}   (state 0 = eps, unlabelled since eps not in S)")

print()
print("=" * 74)
print("C. VERDICT")
print("=" * 74)
print(f"  index(~_delta,S) = 2,   kappa_obs = {kmin},   c_S = {kmin - 2}")
assert kmin == 3
print()
print("  AUDIT COUNTEREXAMPLE CONFIRMED.")
print("  The unqualified equality kappa_obs = index(~_{delta,S}) is FALSE.")
print()
print("  lem:support-extension sandwich  2 <= 3 <= 2+1  -- LEMMA CORRECT.")
print("  open_problems_report 2.12 claim 'c_S = 0 may hold generally'")
print("  -- REFUTED, c_S = 1 here.")
print()
print("=" * 74)
print("D. PREFIX-MEASURE ESCAPE CLAUSE")
print("=" * 74)
print("  If mu(eps) > 0 then eps in S; with S right-closed this forces")
print("  S = I^*, hence c_S = 0.  So discounted-prefix laws with mu(eps)>0")
print("  never hit this obstruction; the counterexample needs mu(eps)=0.")
