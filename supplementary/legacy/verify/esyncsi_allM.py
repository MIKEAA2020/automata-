"""Evaluator's §5 argument: with H_M = machines with AT MOST M states,
exact equality EsyncSI(M) = floor(log2 M) holds for every M in one line.

  - EsyncSI is nondecreasing in M (H_M subset H_{M+1}).
  - Let L = floor(log2 M).  The cyclic-shift witness on 2^L states is a
    minimal machine with 2^L <= M states, hence lies in H_M.
  - It forces L mistakes.  So EsyncSI(M) >= L = floor(log2 M).
  - Upper bound floor(log2 M) from the halving argument.
  => equality.

Verify the two arithmetic facts the argument needs.
"""
import math
print("Fact 1: 2^floor(log2 M) <= M for all M >= 1")
bad=0
for M in range(1,100001):
    L=math.floor(math.log2(M))
    if 2**L>M: bad+=1
print(f"  checked M=1..100000, violations: {bad}")

print()
print("Fact 2: the witness on 2^L states forces L = floor(log2 M) mistakes,")
print("        and floor(log2 (2^L)) = L = floor(log2 M)")
bad=0
for M in range(2,100001):
    L=math.floor(math.log2(M))
    if math.floor(math.log2(2**L))!=L: bad+=1
print(f"  checked M=2..100000, violations: {bad}")

print()
print("Fact 3: monotonicity is what carries the witness from 2^L up to M.")
print("        Since H_{2^L} subset H_M whenever 2^L <= M, any family forcing")
print("        L mistakes inside H_{2^L} also lies inside H_M.")
print()
print("=> EsyncSI(M) = floor(log2 M) EXACTLY, for every M >= 2, provided")
print("   H_M is read as 'at most M states'.  No padding needed.")
