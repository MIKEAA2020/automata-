"""
Exhaustive minimax solve of the ACTIVE game on the GATED family G^act_M.

States: Q x {free,read}, Q = {0,1}^L, so 2M states, M = 2^L.
  (free,v): r->(free,0^L)/0  e->(free,flip_L v)/0  d->(free,rot v)/v_1  c->(read,g(v))/0
  (read,u): r->(free,0^L)/0  e->(read,u)/0        d->(read,rot u)/u_1  c->(read,u)/0
                                                                        ^^^ gated

Objective (RI): the learner must reach a state of information from which every
future output is predictable, i.e. it must know g on all of Q.

Because c is a no-op in read mode there is no chaining: the argument of every
readout is the free-mode state at the moment c was played, which the learner
chose itself.  So the adversary's knowledge state is exactly a partial
assignment K : Q -> ({0,1} u {*})^L.

Zero-cost moves form cycles, so we solve by LAYERED value iteration: layers are
indexed by K (revealing moves strictly decrease the number of unknown bits);
inside a layer we run Dijkstra over the 0-cost move graph.
"""
import itertools
import heapq

STAR = 2


def solve(L, verbose=False):
    M = 2 ** L
    Q = [tuple(b) for b in itertools.product([0, 1], repeat=L)]
    zero = tuple([0] * L)
    qi = {v: i for i, v in enumerate(Q)}

    def rot(v):
        return v[1:] + v[:1]

    def flip(v):
        return v[:-1] + (1 - v[-1],)

    # ---- nodes inside one layer -------------------------------------------
    # ('f', v)          free mode at v
    # ('r', arg, off)   read mode, register = rot^off(g(arg))
    nodes = [('f', v) for v in Q] + \
            [('r', a, o) for a in Q for o in range(L)]

    # zero-cost moves (independent of K)
    zmoves = {}
    for n in nodes:
        out = []
        if n[0] == 'f':
            v = n[1]
            out.append(('f', zero))              # r
            out.append(('f', flip(v)))           # e
            out.append(('f', rot(v)))            # d, output v_1 known
            out.append(('r', v, 0))              # c
        else:
            _, a, o = n
            out.append(('f', zero))              # r
            out.append(('r', a, o))              # e  (no-op)
            out.append(('r', a, o))              # c  (gated no-op)
        zmoves[n] = out

    # all knowledge states, ordered by number of known bits (descending unknown)
    rows = list(itertools.product([0, 1, STAR], repeat=L))
    allK = list(itertools.product(rows, repeat=M))

    def n_unknown(K):
        return sum(1 for row in K for b in row if b == STAR)

    allK.sort(key=n_unknown)          # solve layers with fewest unknowns first

    def setbit(K, a, j, val):
        lst = [list(r) for r in K]
        lst[qi[a]][j] = val
        return tuple(tuple(r) for r in lst)

    V = {}   # V[K][node]

    for K in allK:
        if n_unknown(K) == 0:
            V[K] = {n: 0 for n in nodes}
            continue

        # exit values: the read-mode 'd' move on an unknown bit
        exit_val = {}
        for n in nodes:
            if n[0] == 'f':
                continue
            _, a, o = n
            j = o % L
            if K[qi[a]][j] == STAR:
                # learner predicts, adversary answers worst case
                best = float('inf')
                for pred in (0, 1):
                    worst = 0
                    for ans in (0, 1):
                        nk = setbit(K, a, j, ans)
                        c = (1 if ans != pred else 0) + V[nk][('r', a, (o + 1) % L)]
                        worst = max(worst, c)
                    best = min(best, worst)
                exit_val[n] = best

        # read-mode 'd' on a KNOWN bit is a zero-cost move
        zk = {n: list(zmoves[n]) for n in nodes}
        for n in nodes:
            if n[0] == 'f':
                continue
            _, a, o = n
            if K[qi[a]][o % L] != STAR:
                zk[n].append(('r', a, (o + 1) % L))

        # Dijkstra: dist[n] = min(exit_val[n], min over 0-cost moves of dist[n'])
        # reverse the 0-cost graph and relax from the exit sources
        rev = {n: [] for n in nodes}
        for n in nodes:
            for m in zk[n]:
                rev[m].append(n)

        dist = {n: float('inf') for n in nodes}
        pq = []
        for n, val in exit_val.items():
            if val < dist[n]:
                dist[n] = val
                heapq.heappush(pq, (val, n))
        while pq:
            d, n = heapq.heappop(pq)
            if d > dist[n]:
                continue
            for p in rev[n]:
                if d < dist[p]:
                    dist[p] = d
                    heapq.heappush(pq, (d, p))
        V[K] = dist

    full = tuple(tuple([STAR] * L) for _ in range(M))
    return V[full][('f', zero)], M * L, M


print("Exhaustive minimax on the GATED active family  G^act_M")
print("=" * 66)
for L in (1, 2):
    got, want, M = solve(L)
    ok = (got == want)
    print(f"  L={L}  M={M:3d}  states=2M={2*M:3d}   minimax mistakes = {got:3d}"
          f"   M*log2 M = {want:3d}   MATCH = {ok}")
    assert ok, (L, got, want)

print()
print("The gated family forces exactly M log2 M mistakes against every")
print("deterministic active learner -- the same bound as the passive")
print("thm:stream-lower-bound -- while keeping every readout argument")
print("learner-known, so the lazy adversary and the Yao conditional-")
print("uniformity step are both valid in the active protocol.")
