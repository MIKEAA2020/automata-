"""
With the corrected simultaneous model (pre-input-output controllers), is
cor:stateless still right?

Stateless game, one reward state.  A pre-input-output controller of ANY budget
emits b_t = beta(m_t) without seeing a_t.  The adversary sees nothing either
but may pick the worst a_t AFTER the controller's b_t is determined by m_t
(inf over adversary sequences, sup over controllers).

Claim to test:  Vsim(M) = m2/(1-gamma) for every M >= 1, where
m2 = max_b min_a r(a,b).  Then Com(M) = Valt - Vsim = (m1-m2)/(1-gamma).
"""
import itertools
import numpy as np

def analyse(R, gamma, Mmax=3):
    R = np.array(R, dtype=float)
    na, nb = R.shape
    m1 = min(max(R[a][b] for b in range(nb)) for a in range(na))
    m2 = max(min(R[a][b] for a in range(na)) for b in range(nb))
    Valt = m1/(1-gamma)
    # brute-force Vsim over pre-input-output controllers with <= M states
    best = -np.inf
    for M in range(1, Mmax+1):
        for beta in itertools.product(range(nb), repeat=M):
            for eta in itertools.product(range(M), repeat=M*na*nb):
                E = {}
                i = 0
                for m in range(M):
                    for a in range(na):
                        for b in range(nb):
                            E[(m,a,b)] = eta[i]; i += 1
                # adversary minimizes discounted reward; value iteration on m
                # W[m] = min_a [ r(a, beta(m)) + gamma W[E[m,a,beta(m)]] ]
                W = np.zeros(M)
                for _ in range(600):
                    Wn = np.empty(M)
                    for m in range(M):
                        b = beta[m]
                        Wn[m] = min(R[a][b] + gamma*W[E[(m,a,b)]] for a in range(na))
                    if np.max(np.abs(Wn-W)) < 1e-12: 
                        W = Wn; break
                    W = Wn
                best = max(best, W[0])
    return m1, m2, Valt, best

print("="*74)
print("Vsim over PRE-INPUT-OUTPUT controllers vs the claim m2/(1-gamma)")
print("="*74)
print(f"{'game':>22} {'gamma':>6} {'m2/(1-g)':>10} {'Vsim brute':>11} {'match':>6}")
games = [("matching pennies", [[1,-1],[-1,1]]),
         ("asymmetric",       [[3,0],[1,2]]),
         ("dominant",         [[2,2],[1,1]]),
         ("zero spread",      [[5,5],[5,5]])]
allok = True
for name,R in games:
    for gamma in (0.0, 0.5, 0.9):
        m1,m2,Valt,vs = analyse(R,gamma,Mmax=2)
        pred = m2/(1-gamma)
        ok = abs(pred-vs) < 1e-6
        allok &= ok
        print(f"{name:>22} {gamma:>6.2f} {pred:>10.4f} {vs:>11.4f} {str(ok):>6}")
print()
print("  Vsim = m2/(1-gamma) in every case:", allok)
print()
print("="*74)
print("CONSEQUENCE FOR cor:stateless")
print("="*74)
for name,R in games:
    m1,m2,Valt,vs = analyse(R,0.9,Mmax=2)
    com = Valt - vs
    alpha = m1-m2
    print(f"  {name:>20}: Com = {com:.4f},  alpha/(1-g) = {alpha/(1-0.9):.4f},  "
          f"equal={abs(com-alpha/(1-0.9))<1e-6}")
print()
print("  So Com(M) = (m1-m2)/(1-gamma) for ALL M>=1 remains correct under the")
print("  corrected controller model -- extra memory cannot help in a stateless")
print("  game, since beta(m) is a constant output and the adversary best-responds.")
