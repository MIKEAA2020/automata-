"""
Does an ACTIVE learner attain objective (RI) within O(M log M) mistakes
unconditionally?  If so, E_sync(M) = O(M log M), and combined with the gated
family's Omega(M log M) lower bound this gives E_sync(M) = Theta(M log M) --
which would make the active mistake complexity unconditionally Theta(M log M)
and remove the need for L_sync^univ in the length bound entirely.

Algorithm (active halving with separation):
  V = all (machine, current-state) pairs consistent with the transcript.
  while two elements of V disagree on some continuation:
      pick a shortest distinguishing word w;
      play w one symbol at a time, predicting the MAJORITY over V each round;
      after each observed output, delete from V every element that predicted
      a different symbol.
  Claim 1 (mistakes):  each mistake at least halves |V|, so
                       #mistakes <= log2 |V_0|.
  Claim 2 (termination/attainment): each play of a distinguishing word strictly
                       shrinks V, so V collapses to one residual class -> (RI).
"""
import itertools
import math
import random

I = [0, 1]          # input alphabet
O = [0, 1]          # output alphabet


def all_machines(M):
    """All Mealy machines on state set range(M): tau, lam : Q x I -> Q, O."""
    pairs = [(q, a) for q in range(M) for a in I]
    n = len(pairs)
    for tv in itertools.product(range(M), repeat=n):
        for lv in itertools.product(O, repeat=n):
            tau = {pairs[i]: tv[i] for i in range(n)}
            lam = {pairs[i]: lv[i] for i in range(n)}
            yield (tau, lam)


def out(mach, q, w):
    tau, lam = mach
    r = []
    for a in w:
        r.append(lam[(q, a)])
        q = tau[(q, a)]
    return tuple(r), q


def residual_sig(mach, q, depth):
    """Signature of the continuation function up to `depth` (Moore: depth 2M-1
    suffices to separate inequivalent states of <=M-state machines)."""
    sig = []
    for L in range(1, depth + 1):
        for w in itertools.product(I, repeat=L):
            sig.append(out(mach, q, w)[0])
    return tuple(sig)


def run(M, trials=200, seed=0):
    rng = random.Random(seed)
    machs = list(all_machines(M))
    depth = 2 * M                      # separation depth
    V0 = [(m, q) for m in machs for q in range(M)]
    logV0 = math.log2(len(V0))
    print(f"M={M}: |H_M x Q| = {len(V0)},  log2 = {logV0:.2f},  "
          f"M*log2(M)+... reference O(M log M)")

    worst_mist = 0
    for t in range(trials):
        target = rng.choice(V0)
        V = list(V0)
        mistakes = 0
        rounds = 0
        while True:
            # group V by residual signature
            sigs = {}
            for (m, q) in V:
                sigs.setdefault(residual_sig(m, q, depth), []).append((m, q))
            if len(sigs) == 1:
                break                                   # (RI) attained
            # shortest distinguishing word between two signature groups
            reps = [v[0] for v in sigs.values()]
            (m1, q1), (m2, q2) = reps[0], reps[1]
            w = None
            for L in range(1, depth + 1):
                for cand in itertools.product(I, repeat=L):
                    if out(m1, q1, cand)[0] != out(m2, q2, cand)[0]:
                        w = cand
                        break
                if w:
                    break
            assert w is not None
            before = len(V)
            for a in w:
                # majority prediction over V
                votes = {}
                for (m, q) in V:
                    y = m[1][(q, a)]
                    votes[y] = votes.get(y, 0) + 1
                pred = max(votes, key=lambda k: votes[k])
                truth = target[0][1][(target[1], a)]
                if pred != truth:
                    mistakes += 1
                    assert votes[pred] >= len(V) / 2 - 1e-9
                    newV = [(m, q) for (m, q) in V if m[1][(q, a)] == truth]
                    assert len(newV) <= len(V) / 2 + 1e-9, "halving failed"
                    V = newV
                else:
                    V = [(m, q) for (m, q) in V if m[1][(q, a)] == truth]
                # advance everyone
                V = [(m, m[0][(q, a)]) for (m, q) in V]
                target = (target[0], target[0][0][(target[1], a)])
                rounds += 1
            assert len(V) < before, "no progress on distinguishing word"
        assert mistakes <= logV0 + 1e-9, (mistakes, logV0)
        worst_mist = max(worst_mist, mistakes)

    print(f"   {trials} random targets: (RI) attained every time")
    print(f"   worst mistakes = {worst_mist}  <=  log2|V0| = {logV0:.2f}   OK")
    return worst_mist, logV0


print("=" * 70)
print("ACTIVE HALVING ATTAINS (RI) WITHIN log2|H_M| MISTAKES")
print("=" * 70)
run(1, trials=50)
run(2, trials=60)

print()
print("Asymptotics of log2|H_M x Q| for fixed alphabets |I|=|O|=2:")
for M in [2, 4, 8, 16, 32, 64, 128]:
    # |H_M| = M^(M|I|) * |O|^(M|I|) * M   (transitions, outputs, initial state)
    lg = M * len(I) * math.log2(M) + M * len(I) * math.log2(len(O)) + math.log2(M)
    print(f"   M={M:4d}:  log2|H_M x Q| = {lg:10.1f}   M*log2 M = {M*math.log2(M):10.1f}"
          f"   ratio = {lg/(M*math.log2(M)):.3f}")
print()
print("=> log2|H_M| = Theta(M log M) for fixed alphabets, so active halving")
print("   attains (RI) with O(M log M) mistakes UNCONDITIONALLY.")
print("   With the gated-family lower bound Omega(M log M):")
print("        E_sync(M) = Theta(M log M),")
print("   hence Mistakes_active(M) = Theta(M log M) with NO hypotheses.")
