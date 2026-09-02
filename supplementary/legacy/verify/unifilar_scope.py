"""Is the manuscript's def:controlled-markov a genuine restriction, and is the
'epsilon-machine' label an overclaim?

Manuscript model:  S_t = tau(S_{t-1}, X_t)          -- INPUT-driven
General unifilar:  S_{t+1} = tau(S_t, X_t, Y_t)     -- JOINT-driven

Question 1: is there a unifilar machine whose state is NOT a function of the
            input history alone?  (If yes, the manuscript model is a proper
            subclass and the label is an overclaim.)
Question 2: does the manuscript's sufficiency condition (9) still hold in the
            input-driven model?  (If yes, the model is internally consistent.)
"""
import itertools
from collections import defaultdict

print("="*76)
print("Q1: a unifilar machine whose state depends on the OUTPUT")
print("="*76)
# Classic: the 'even process' style machine. 2 states, |I|=1 (no real input),
# |O|={0,1}.  State A emits 0 w.p. 1/2 -> stay A ; emits 1 -> go to B.
# State B emits 1 w.p. 1 -> go to A.
tau = {('A',0):'A', ('A',1):'B', ('B',1):'A'}
emit = {'A':{0:0.5, 1:0.5}, 'B':{1:1.0}}
print("  even-process-like machine:")
print("    tau(A,y=0)=A, tau(A,y=1)=B, tau(B,y=1)=A")
print("    so the next state is a function of (state, OUTPUT), not of input.")
# Is state a function of input history?  There is only ONE input, so the input
# history of length t is unique; yet the state after t steps varies.
print()
print("  With |I|=1 the input history of length t is the unique word a^t.")
print("  Trace two output histories of the same length from A:")
for ys in [(0,0),(0,1),(1,1)]:
    s='A'; ok=True
    for y in ys:
        if (s,y) not in tau: ok=False; break
        s=tau[(s,y)]
    print(f"    outputs {ys} -> state {s if ok else 'infeasible'}")
print()
print("  Same input history a^2, DIFFERENT final states => the state is NOT a")
print("  function of the input history.  The manuscript's S_t = tau(S_{t-1},X_t)")
print("  cannot represent this machine.  => proper subclass CONFIRMED.")

print()
print("="*76)
print("Q2: does sufficiency (condition 9) hold in the input-driven model?")
print("="*76)
print("  In the input-driven model S_t is a deterministic function of")
print("  (S_0, X_1..X_t).  Emissions depend only on S_t.  So")
print("     Z_t = Y_t  is conditionally independent of the past given S_t,")
print("  by construction.  The model is internally consistent; it is the")
print("  CLASS that is restricted, not the axioms that are contradictory.")

print()
print("="*76)
print("Q3: is the input-driven model the OUTPUT-INDEPENDENT special case?")
print("="*76)
print("  If tau(s,x,y) = tau_0(s,x) for all y, the unifilar recursion")
print("  S_{t+1} = tau(S_t,X_t,Y_t) collapses to S_{t+1} = tau_0(S_t,X_t),")
print("  which is the manuscript's model after an index shift.")
print("  => the proposed generalization is a strict extension, and the")
print("     manuscript's theorems become the special case tau independent of y.")
