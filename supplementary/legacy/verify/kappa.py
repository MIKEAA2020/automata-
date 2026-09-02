"""Is the jump ratio kappa = b(M*)/b(M*-1) bounded for the ACTUAL envelopes?

kappa is a ratio of CONSECUTIVE values of the estimation envelope at the
crossing index.  If b has bounded consecutive ratios ("doubling"), then
kappa <= that constant regardless of where the crossing falls.
"""
import numpy as np, math
print("="*78)
print("sup_{M>=2} b(M)/b(M-1) for the manuscript's estimation envelopes")
print("="*78)

def report(name, b, Mmax=200000):
    rs = [b(M)/b(M-1) for M in range(2, Mmax)]
    i = int(np.argmax(rs))
    print(f"  {name:<42} sup = {max(rs):.6f} at M={i+2:<6} limit = {rs[-1]:.9f}")
    return max(rs)

T = 10**6
report("sqrt(T ln(eM)) + ln(eM)      [agnostic]", lambda M: math.sqrt(T*math.log(math.e*M))+math.log(math.e*M))
report("M log(eM)                    [realizable]", lambda M: M*math.log(math.e*M))
report("M log M  (M>=2)              [realizable]", lambda M: M*math.log(M) if M>1 else 1e-12)
report("sqrt(T M log(eM))            [agnostic FS]", lambda M: math.sqrt(T*M*math.log(math.e*M)))
report("M                            [linear]",     lambda M: float(M))
report("log(eM)                      [log]",        lambda M: math.log(math.e*M))
report("M^2 log(eM)                  [quadratic]",  lambda M: M*M*math.log(math.e*M))

print()
print("="*78)
print("General family  b(M) = M^a (log(eM))^b :  is the sup attained at M=2?")
print("="*78)
print(f"  {'a':>4} {'b':>4} {'sup ratio':>12} {'2^a (1+log2)^b':>16} {'match':>7}")
ok=True
for a in [0,0.5,1,1.5,2,3]:
    for bb in [0,0.5,1,2]:
        if a==0 and bb==0: continue
        f=lambda M: (M**a)*(math.log(math.e*M)**bb)
        rs=[f(M)/f(M-1) for M in range(2,50000)]
        pred=(2**a)*((1+math.log(2))**bb)
        m=abs(max(rs)-pred)<1e-9
        ok &= m
        print(f"  {a:>4} {bb:>4} {max(rs):>12.6f} {pred:>16.6f} {str(m):>7}")
print(f"\n  sup is ALWAYS attained at M=2, equal to 2^a (1+log 2)^b : {ok}")

print()
print("="*78)
print("Why: both factors (M/(M-1))^a and (log(eM)/log(e(M-1)))^b decrease in M")
print("="*78)
for a,bb in [(1,1),(0,0.5),(0.5,1)]:
    f1=[( (M/(M-1))**a ) for M in range(2,12)]
    f2=[( (math.log(math.e*M)/math.log(math.e*(M-1)))**bb ) for M in range(2,12)]
    print(f"  a={a}, b={bb}")
    print(f"    (M/(M-1))^a         : {[round(x,4) for x in f1]}  decreasing={all(f1[i]>=f1[i+1]-1e-12 for i in range(len(f1)-1))}")
    print(f"    (log eM/log e(M-1))^b: {[round(x,4) for x in f2]}  decreasing={all(f2[i]>=f2[i+1]-1e-12 for i in range(len(f2)-1))}")

print()
print("="*78)
print("CONSEQUENCE for thm:oracle-minimax-lower: constant c/(1+kappa)")
print("="*78)
for name,a,bb in [("agnostic  sqrt(T log(eM))",0,0.5),("realizable  M log(eM)",1,1),
                  ("agnostic FS sqrt(T M log(eM))",0.5,0.5)]:
    k=(2**a)*((1+math.log(2))**bb)
    print(f"  {name:<32} kappa <= {k:.4f}   =>  1/(1+kappa) >= {1/(1+k):.4f}")
