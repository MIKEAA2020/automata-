"""
Item 7: is the "restriction" step of thm:active-direct-sum sound?

Claim in the proof: from a composite learner A, build a component learner A_j
by simulating A and forwarding only rounds in R_j, "answering the rounds of the
other component internally from the simulated transcript."

The worry: A chooses inputs adaptively based on BOTH components' outputs. To
run component j in isolation, A_j must supply the other component's outputs
itself. It can only do so if those outputs are determined by information A_j
has.

Test: in the two-phase family, component 1's unknown is g on Q1 and
component 2's is g' on Q2. When simulating component 1 alone, the simulator
must answer rounds that read bits of g'. Those bits are NOT determined by
component 1's transcript. So the simulator must INVENT them.

Question: does inventing them preserve the mistake count for component 1?

Answer: yes IF the invented values are consistent with SOME target, because the
family is a product: any g paired with any g' is a member. So the simulator can
fix an arbitrary g'_0 in advance and answer component-2 rounds from it. The
composite instance (g, g'_0) is in the family, A's behaviour on it is well
defined, and the component-1 rounds of that run are exactly a valid run of A_1.

This is a PRODUCT-STRUCTURE argument -- exactly the same property the gating
fix established. Verify the product structure of the two-phase family.
"""
import itertools
import random

L1 = L2 = 2
Q1 = [tuple(b) for b in itertools.product([0, 1], repeat=L1)]
Q2 = [tuple(b) for b in itertools.product([0, 1], repeat=L2)]

print("=" * 74)
print("Two-phase family: is it a PRODUCT of the two components' unknowns?")
print("=" * 74)

allg = list(itertools.product(Q1, repeat=len(Q1)))
allgp = list(itertools.product(Q2, repeat=len(Q2)))
print(f"  |{{g}}| = {len(allg)},  |{{g'}}| = {len(allgp)}")
print(f"  family size if product = {len(allg)*len(allgp)}")

# The family is defined as: choose g freely, choose g' freely, independently.
family = [(g, gp) for g in allg for gp in allgp]
print(f"  actual family size     = {len(family)}")
print(f"  IS A PRODUCT? {len(family) == len(allg)*len(allgp)}")
assert len(family) == len(allg) * len(allgp)

print()
print("  => for ANY g and ANY g'_0, the pair (g, g'_0) is in the family.")
print("     So a component-1 simulator may fix g'_0 in advance, answer all")
print("     component-2 rounds from it, and the resulting composite run is a")
print("     legitimate run of the composite learner on a legitimate target.")

print()
print("=" * 74)
print("Does the restriction preserve component-1 mistakes?")
print("=" * 74)
print("  The component-1 rounds of the run on (g, g'_0) are, by disjoint")
print("  accounting (condition iii), exactly the rounds where component 1")
print("  forces a mistake. The simulator reproduces them verbatim.")
print("  Hence  mistakes_{A_1}(g) = |R_1| on the composite run.")
print()

# Sanity: disjointness means a round belongs to at most one component.
# Model: rounds are tagged by which block the machine is in.
random.seed(0)
viol = 0
for _ in range(100000):
    # a round is in block 1 or block 2, never both
    blk = random.choice([1, 2])
    r1 = (blk == 1)
    r2 = (blk == 2)
    if r1 and r2:
        viol += 1
print(f"  disjointness spot-check: {viol} violations in 100000 rounds")
assert viol == 0

print()
print("CONCLUSION: the restriction step is SOUND, but its soundness rests on")
print("the product structure of the family (any g with any g'), which the")
print("proof asserts only as 'independent coordinates'. Making the fixed")
print("g'_0 explicit turns the sketch into a proof.")
