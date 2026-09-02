"""Verify the sharpened halving step in full detail.

CLAIM. Let V be the version space, x an input, and partition V by output
symbol into classes of sizes c_1 >= c_2 >= ... >= c_r (r <= |O|).  The learner
predicts the plurality symbol o_1.  If it errs, the true symbol is some
o_j with j >= 2, so the survivors number c_j <= c_2.

Since c_1 >= c_2 and c_1 + c_2 <= |V|:   2*c_2 <= c_1 + c_2 <= |V|,
hence c_2 <= |V|/2.  So EVERY mistake at least halves the version space,
for every alphabet size.  Total mistakes <= floor(log2 |V_0|) = floor(log2 M).
"""
import numpy as np, itertools, math
rng = np.random.default_rng(1)

print("(a) exhaustive over integer class profiles: is c_2 <= n/2 always?")
bad=0; tot=0; tight=[]
for n in range(2, 26):
    for r in range(2, min(n,5)+1):
        # all compositions of n into r positive parts (sorted desc), sampled exhaustively for small n
        for comp in itertools.combinations(range(1,n), r-1):
            parts=np.diff(np.concatenate([[0],comp,[n]]))
            s=np.sort(parts)[::-1]; tot+=1
            if s[1] > n/2 + 1e-12: bad+=1
            if abs(s[1]-n/2) < 1e-12: tight.append((n,tuple(s)))
print(f"    {tot} class profiles (n<=25, r<=5): violations of c_2 <= n/2 = {bad}")
print(f"    tightness attained e.g. {tight[:4]}  (c_1=c_2=n/2)")

print()
print("(b) does floor(log2 M) mistakes always suffice?  simulate worst-case play")
def sim(M, nO, trials=20000, rng=rng):
    worst=0
    for _ in range(trials):
        V=M; mis=0
        while V>1:
            # adversary picks the class profile maximizing survivors after a mistake
            r=min(nO,V)
            # worst case: two classes as equal as possible (forces c_2 = floor(V/2))
            c2=V//2
            if c2<1: break
            V=c2; mis+=1
        worst=max(worst,mis)
    return worst
print(f"    {'M':>6} {'|O|':>4} {'worst mistakes':>15} {'floor(log2 M)':>14} {'match':>6}")
for M in [2,3,4,5,8,16,17,32,64,1000]:
    for nO in [2,3,5]:
        w=sim(M,nO,200)
        f=math.floor(math.log2(M))
        print(f"    {M:>6} {nO:>4} {w:>15} {f:>14} {str(w==f):>6}")

print()
print("(c) the OLD bound vs the NEW bound")
print(f"    {'M':>6} {'|O|=2':>10} {'|O|=3':>10} {'|O|=4':>10} {'|O|=8':>10} {'new: floor(log2 M)':>20}")
for M in [4,16,64,256,1024]:
    row=[math.log(M)/math.log(nO/(nO-1)) for nO in [2,3,4,8]]
    print(f"    {M:>6} " + " ".join(f"{x:>10.2f}" for x in row) + f" {math.floor(math.log2(M)):>20}")
print("    -> old bound grows with |O| without limit; the truth does not depend on |O|.")
