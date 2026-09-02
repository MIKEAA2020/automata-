#!/usr/bin/env python3
"""Exhaustive enumeration of Mealy machines under the manuscript's Computational
Conventions, for the supplementary package.

Conventions implemented (remark on Computational Conventions):
  * labelled transition/output table pairs, counted up to renaming of the state
    set (canonical-form counting: a machine's canonical code is the minimum,
    over all state relabelings, of its base-(M*O) table code);
  * minimality decided by Moore partition refinement before counting;
  * tie-breaking lexicographic on the canonical encoding (representatives are
    the first raw machine attaining each canonical code);
  * search is exhaustive over the stated classes.

Quantities computed per machine:
  * adaptive synchronization depth (Lsync-style): the exact minimax number of
    inputs needed to drive the uncertainty set to a singleton (INF if some
    uncertainty set cannot be driven to a singleton);
  * state-identification cost in mistakes (EsyncSI-style): the minimax number
    of wrong predictions, the learner predicting an output symbol per query
    and the adversary answering consistently with some state.

Stages:
  1. Cyclic-shift family, L = 1..10: deterministic minimax depth == L,
     Bayes-optimal expected mistakes == L/2 under the uniform prior,
     minimality.  (Theorem thm:esyncsi-theta and the game-solving remark.)
  2. Signature grid: all (M, I, O) with M in {2,3,4}, I in {1,2}, O in {2,4}
     whose raw table-pair space fits the exhaustive budget (<= 2^24 raw pairs;
     the (4,2,4) signature is excluded by budget and covered instead by the
     output-alphabet-independence remark).  Per signature: raw table-pair
     count, raw minimal count, renaming-class count, canonical minimal count,
     worst-case identification mistakes, worst-case adaptive depth over
     minimal machines, and the number of minimal machines attaining the worst
     depth.  The (3,2,2) row reproduces the manuscript's quoted largest
     signature (46,656 table pairs); the (4,2,2) row reproduces the quoted
     maximum adaptive depth 6 with its realizer count.
  3. Structured subclass at M = 5 (documented interpretation of the
     quotation: minimal binary machines whose first input acts as a
     permutation, whose first-input output function is constant, and whose
     second-input output function has a single probe state): renaming-class
     count, worst adaptive depth (manuscript: 9, short of C(5,2) = 10).

Usage:  python3 enumerate_machines.py   (requires numpy; ~10 min)
Outputs: console log (tee to ../outputs/enumeration.log), summary JSON
         (../outputs/enumeration_summary.json), extremal machine tables
         (../machine_tables/).
"""
import itertools, json, pathlib, sys, time
import numpy as np

SUP = pathlib.Path(__file__).resolve().parent.parent
TAB = SUP / "machine_tables"
TAB.mkdir(parents=True, exist_ok=True)
STAGE = sys.argv[1] if len(sys.argv) > 1 else "all"

t0 = time.time()
def log(msg):
    print(f"[{time.time()-t0:7.1f}s] {msg}", flush=True)

def save_summary(summary):
    (SUP / "outputs").mkdir(exist_ok=True)
    (SUP / "outputs" / "enumeration_summary.json").write_text(
        json.dumps(summary, indent=1))

summary = {"cyclic_shift": [], "signatures": [], "m5_structured": {}}

# =====================================================================
# Generic machinery (vectorized across machines)
# =====================================================================

def decode(ids, M, I, O):
    """Raw machine ids -> (T, L) arrays of shape (n, M, I)."""
    ids = np.asarray(ids, dtype=np.int64)
    n = ids.shape[0]
    MI = M * I
    T = np.empty((n, MI), dtype=np.int8)
    L = np.empty((n, MI), dtype=np.int8)
    rem = ids.copy()
    for k in range(MI - 1, -1, -1):
        digit = rem % (M * O)
        rem //= (M * O)
        T[:, k] = digit // O
        L[:, k] = digit % O
    return T.reshape(n, M, I), L.reshape(n, M, I)

def canonical_codes(T, L, M, I, O):
    """Canonical code per machine: min over state relabelings of the
    base-(M*O) code of the relabeled (T, L) pair."""
    n = T.shape[0]
    MI = M * I
    Tf = T.reshape(n, MI).astype(np.int64)
    Lf = L.reshape(n, MI).astype(np.int64)
    base = M * O
    best = None
    for p_tup in itertools.permutations(range(M)):
        p = np.array(p_tup, dtype=np.int64)
        v = p[Tf] * O + Lf                       # relabeled entry values
        pos = (p[:, None] * I + np.arange(I)[None, :]).reshape(-1)
        w = base ** (MI - 1 - pos)               # positional weights
        code = v @ w
        if best is None:
            best = code
        else:
            np.minimum(best, code, out=best)
    return best

def moore_minimal(T, L, M, I):
    """Moore partition refinement to fixpoint; True where discrete."""
    n = T.shape[0]
    part = np.zeros((n, M), dtype=np.int64)
    prev_total = 1
    for _ in range(M + 2):
        idx = np.arange(n)[:, None, None]
        partT = part[idx, T]                      # (n, M, I)
        sig = part * 1
        for x in range(I):
            sig = sig * (M + 1) + partT[:, :, x]
            sig = sig * 256 + L[:, :, x]
        flat = sig.reshape(-1)
        _, inv = np.unique(flat, return_inverse=True)
        part = inv.reshape(n, M).astype(np.int64)
        total = part.max() + 1
        ps = np.sort(part, axis=1)
        if np.all(ps[:, 1:] != ps[:, :-1]):
            return np.ones(n, dtype=bool)
        if total == prev_total:
            break
        prev_total = total
    ps = np.sort(part, axis=1)
    return np.all(ps[:, 1:] != ps[:, :-1], axis=1)

def branch_masks(T, L, M, I, O, chunk=400_000):
    """BM[n, subset_mask, x, y] = bitmask of {tau(s,x) : s in subset,
    lambda(s,x) = y}. Subset indexed by its own bitmask value."""
    n = T.shape[0]
    for lo in range(0, n, chunk):
        Tc = T[lo:lo+chunk]
        Lc = L[lo:lo+chunk]
        m = Tc.shape[0]
        BM = np.zeros((m, 1 << M, I, O), dtype=np.int16)
        for x in range(I):
            for y in range(O):
                sel = (Lc[:, :, x] == y)
                bits = (1 << Tc[:, :, x].astype(np.int16))
                contrib = np.where(sel, bits, 0)
                for mask in range(1, 1 << M):
                    states = [s for s in range(M) if (mask >> s) & 1]
                    BM[:, mask, x, y] = np.bitwise_or.reduce(
                        contrib[:, states], axis=1)
        yield lo, BM

def depth_game(T, L, M, I, O, chunk=400_000):
    """Minimax number of inputs to singleton (BIG = unreachable)."""
    n = T.shape[0]
    BIG = np.int32(10**6)
    full = (1 << M) - 1
    singleton = np.array([bin(m).count("1") == 1 for m in range(1 << M)])
    out = np.full(n, BIG, dtype=np.int32)
    for lo, BM in branch_masks(T, L, M, I, O, chunk):
        m = BM.shape[0]
        val = np.full((m, 1 << M), BIG, dtype=np.int32)
        val[:, singleton] = 0
        rows = np.arange(m)[:, None]
        for rounds in range((1 << M) + 2):
            new = val.copy()
            for mask in range(1, 1 << M):
                if singleton[mask]:
                    continue
                best = None
                for x in range(I):
                    worst = None
                    for y in range(O):
                        bmask = BM[:, mask, x, y]
                        valid = bmask != 0
                        bv = val[rows[:, 0], bmask]
                        bv = np.where(valid, bv, np.int32(-1))
                        worst = bv if worst is None else np.maximum(worst, bv)
                    cand = worst + 1
                    best = cand if best is None else np.minimum(best, cand)
                new[:, mask] = best
            if np.array_equal(new, val):
                break
            val = new
        out[lo:lo+m] = val[:, full]
    return out

def mistake_game(T, L, M, I, O, chunk=400_000):
    """Minimax number of wrong predictions to identify the state."""
    n = T.shape[0]
    full = (1 << M) - 1
    singleton = np.array([bin(m).count("1") == 1 for m in range(1 << M)])
    out = np.zeros(n, dtype=np.int32)
    for lo, BM in branch_masks(T, L, M, I, O, chunk):
        m = BM.shape[0]
        val = np.zeros((m, 1 << M), dtype=np.int32)
        rows = np.arange(m)[:, None]
        for rounds in range((1 << M) + 2):
            new = val.copy()
            for mask in range(1, 1 << M):
                if singleton[mask]:
                    continue
                best = None
                for x in range(I):
                    for pred in range(O):
                        worst = None
                        for y in range(O):
                            bmask = BM[:, mask, x, y]
                            valid = bmask != 0
                            bv = val[rows[:, 0], bmask] + (y != pred)
                            bv = np.where(valid, bv, np.int32(-1))
                            worst = bv if worst is None else np.maximum(worst, bv)
                        best = worst if best is None else np.minimum(best, worst)
                new[:, mask] = best
            if np.array_equal(new, val):
                break
            val = np.maximum(val, new)
        out[lo:lo+m] = val[:, full]
    return out

# =====================================================================
# Stage 1: cyclic-shift family, L = 1..10
# =====================================================================
if STAGE in ("all", "1"):
    log("Stage 1: cyclic-shift family, L=1..10")

def cyclic_machine(L):
    n = 1 << L
    Q = list(itertools.product([0, 1], repeat=L))
    tau, lam = {}, {}
    for s, v in enumerate(Q):
        rot_v = v[1:] + v[:1]
        tau[(s, 0)] = Q.index(rot_v)
        lam[(s, 0)] = v[0]
        tau[(s, 1)] = s
        lam[(s, 1)] = 0
    return tau, lam

def adaptive_depth_generic(n_states, tau, lam, n_in):
    """Exact minimax input count to singleton (INF on non-progress)."""
    memo, inprog = {}, set()
    INF = float("inf")
    def depth(U):
        U = frozenset(U)
        if len(U) <= 1:
            return 0
        if U in memo:
            return memo[U]
        if U in inprog:
            return INF
        inprog.add(U)
        best = INF
        for x in range(n_in):
            branches = {}
            for s in U:
                branches.setdefault(lam[(s, x)], set()).add(tau[(s, x)])
            worst = max(depth(frozenset(v)) for v in branches.values())
            if worst < best:
                best = worst
        inprog.discard(U)
        memo[U] = 1 + best if best < INF else INF
        return memo[U]
    return depth(frozenset(range(n_states)))

def minimal_generic(n, tau, lam, n_in):
    classes = [tuple(range(n))]
    part = list(range(n))
    for _ in range(n):
        part2 = [0] * n
        m = {}
        for s in range(n):
            sig = (part[s], tuple((lam[(s, x)], part[tau[(s, x)]]) for x in range(n_in)))
            if sig not in m:
                m[sig] = len(m)
            part2[s] = m[sig]
        part = part2
        if len(set(part)) == len(part):
            return True
    return len(set(part)) == n

def bayes_expected(n_states, tau, lam, n_in, n_out):
    """Bayes-optimal expected mistakes, uniform prior over the initial set."""
    memo = {}
    def E(U):
        U = frozenset(U)
        if len(U) <= 1:
            return 0.0
        if U in memo:
            return memo[U]
        memo[U] = float("inf")   # cycle guard
        best = float("inf")
        for x in range(n_in):
            classes = {}
            for s in U:
                classes.setdefault(lam[(s, x)], set()).add(tau[(s, x)])
            tot = len(U)
            # optimal prediction: the largest output class
            yhat = max(classes, key=lambda y: len([s for s in U if lam[(s, x)] == y]))
            acc = 0.0
            for y, img in classes.items():
                p = len([s for s in U if lam[(s, x)] == y]) / tot
                acc += p * ((y != yhat) + E(img))
            best = min(best, acc)
        memo[U] = best
        return best
    return E(range(n_states))

for L in range(1, 11):
    tau, lam = cyclic_machine(L)
    d = adaptive_depth_generic(1 << L, tau, lam, 2)
    b = bayes_expected(1 << L, tau, lam, 2, 2)
    mini = minimal_generic(1 << L, tau, lam, 2)
    ok = (d == L) and abs(b - L / 2) < 1e-9 and mini
    log(f"  L={L:2d}: depth={d} (claim {L}), bayes={b:.6f} (claim {L/2}), "
        f"minimal={mini} -> {'PASS' if ok else 'CHECK'}")
    summary["cyclic_shift"].append({"L": L, "depth": d, "bayes": b,
                                    "minimal": bool(mini)})
for L in range(1, 5):
    tau, lam = cyclic_machine(L)
    n = 1 << L
    rows = []
    for s in range(n):
        rows.append([s, tau[(s, 0)], lam[(s, 0)], tau[(s, 1)], lam[(s, 1)]])
    arr = "\n".join(",".join(map(str, r)) for r in rows)
    (TAB / f"cyclic_shift_L{L}.csv").write_text(
        "state,tau(s,0),lambda(s,0),tau(s,1),lambda(s,1)\n" + arr + "\n")

# =====================================================================
# Stage 2: signature grid
# =====================================================================
log("Stage 2: signature grid (M in {2,3,4}, I in {1,2}, O in {2,4}; raw <= 2^24)")

SIGS = [(2,1,2),(2,1,4),(2,2,2),(2,2,4),
        (3,1,2),(3,1,4),(3,2,2),(3,2,4),
        (4,1,2),(4,1,4),(4,2,2)]

def emit_table(name, T, L, M, I, O, note=""):
    """CSV + LaTeX tabular for one machine."""
    T0 = T.reshape(M, I)
    L0 = L.reshape(M, I)
    csv = ["state," + ",".join(f"tau(s,{x}),lambda(s,{x})" for x in range(I))]
    for s in range(M):
        cells = [str(s)]
        for x in range(I):
            cells += [str(int(T0[s, x])), str(int(L0[s, x]))]
        csv.append(",".join(cells))
    (TAB / f"{name}.csv").write_text("\n".join(csv) + "\n")
    cols = "l" * (1 + 2 * I)
    head = " & ".join(["$s$"] + sum([[f"$\\tau(s,{x})$", f"$\\lambda(s,{x})$"]
                                     for x in range(I)], []))
    body = " \\\\\n".join(
        " & ".join([str(s)] + sum([[str(int(T0[s, x])), str(int(L0[s, x]))]
                                   for x in range(I)], []))
        for s in range(M))
    tex = (f"% {name} — {note}\n\\begin{{tabular}}{{{cols}}}\n\\toprule\n"
           f"{head} \\\\\n\\midrule\n{body} \\\\\n\\bottomrule\n"
           f"\\end{{tabular}}\n")
    (TAB / f"{name}.tex").write_text(tex)

for (M, I, O) in SIGS:
    raw_total = (M * O) ** (M * I)
    log(f"  signature (M={M}, I={I}, O={O}): raw table pairs = {raw_total:,}")
    rec = {"M": M, "I": I, "O": O, "raw_total": raw_total}

    # --- raw pass: canonical codes (chunked) + raw minimality ---
    need_raw_realizers = (M >= 3 and I == 2 and O == 2)
    codes_list = []
    raw_min_flags = []
    raw_min_T, raw_min_L = [], []
    CH = 1_000_000
    for lo in range(0, raw_total, CH):
        ids = np.arange(lo, min(lo + CH, raw_total), dtype=np.int64)
        T, L = decode(ids, M, I, O)
        codes_list.append(canonical_codes(T, L, M, I, O))
        fm = moore_minimal(T, L, M, I)
        raw_min_flags.append(fm)
        if need_raw_realizers:
            raw_min_T.append(T[fm].copy())
            raw_min_L.append(L[fm].copy())
    codes = np.concatenate(codes_list)
    raw_minimal = np.concatenate(raw_min_flags)
    rec["raw_minimal"] = int(raw_minimal.sum())
    log(f"    raw minimal: {rec['raw_minimal']:,}")

    # --- renaming classes + representatives ---
    uniq, first = np.unique(codes, return_index=True)
    rec["renaming_classes"] = int(uniq.shape[0])
    log(f"    renaming classes: {rec['renaming_classes']:,}")
    Trep, Lrep = decode(first, M, I, O)
    minrep = moore_minimal(Trep, Lrep, M, I)
    rec["canonical_minimal"] = int(minrep.sum())
    log(f"    minimal renaming classes: {rec['canonical_minimal']:,}")

    # --- games on minimal canonical representatives ---
    if minrep.sum() > 0:
        Tm, Lm = Trep[minrep], Lrep[minrep]
        depth = depth_game(Tm, Lm, M, I, O)
        BIGV = 10**6
        finite = depth[depth < BIGV]
        rec["max_depth_canonical"] = int(finite.max()) if finite.size else None
        rec["unidentifiable_canonical"] = int((depth >= BIGV).sum())
        if rec["max_depth_canonical"] is not None:
            rec["depth_max_realizers_canonical"] = int(
                (depth == rec["max_depth_canonical"]).sum())
        mist = mistake_game(Tm, Lm, M, I, O)
        rec["max_mistakes_canonical"] = int(mist.max())
        log(f"    max depth (minimal, canonical): {rec['max_depth_canonical']}"
            f" (realizers {rec.get('depth_max_realizers_canonical')}); "
            f"unidentifiable: {rec['unidentifiable_canonical']:,}")
        log(f"    max identification mistakes: {rec['max_mistakes_canonical']}"
            f" (bound floor(log2 M) = {M.bit_length() - 1})")
        # --- raw realizer counts of the max depth (direct comparison numbers) ---
        if need_raw_realizers:
            dmax = rec["max_depth_canonical"]
            Tall = np.concatenate(raw_min_T)
            Lall = np.concatenate(raw_min_L)
            draw = depth_game(Tall, Lall, M, I, O)
            rec["depth_max_realizers_raw"] = int((draw == dmax).sum())
            rec["raw_minimal_checked"] = int(Tall.shape[0])
            log(f"    raw minimal realizers of max depth {dmax}: "
                f"{rec['depth_max_realizers_raw']:,}")
            # extremal table: first canonical minimal machine attaining dmax
            idx = np.where(minrep)[0]
            j = idx[int(np.argmax(depth == dmax))]
            emit_table(f"extremal_depth_M{M}_I{I}_O{O}", Trep[j], Lrep[j], M, I, O,
                       note=f"canonical minimal machine attaining adaptive depth {dmax}")
        del raw_min_T, raw_min_L
    summary["signatures"].append(rec)

# =====================================================================
# Stage 3: M=5 structured subclass
# =====================================================================
log("Stage 3: M=5 structured subclass (first input a permutation, "
    "constant first-input outputs, single probe on the second input)")

M, I, O = 5, 2, 2
perms = np.array(list(itertools.permutations(range(5))), dtype=np.int8)   # (120,5)
tau1 = []
for t in itertools.product(range(5), repeat=5):
    tau1.append(t)
tau1 = np.array(tau1, dtype=np.int8)                                       # (3125,5)
N = perms.shape[0] * tau1.shape[0] * 5
log(f"  raw machines: {N:,}")
T = np.empty((N, 5, 2), dtype=np.int8)
L = np.zeros((N, 5, 2), dtype=np.int8)
k = 0
for pi in range(120):
    for ti in range(3125):
        for probe in range(5):
            T[k, :, 0] = perms[pi]
            T[k, :, 1] = tau1[ti]
            L[k, probe, 1] = 1
            k += 1
codes = np.concatenate([
    canonical_codes(T[lo:lo+250_000], L[lo:lo+250_000], 5, 2, 2)
    for lo in range(0, N, 250_000)])
uniq, first = np.unique(codes, return_index=True)
log(f"  renaming classes: {uniq.shape[0]:,}")
Trep, Lrep = T[first], L[first]
minrep = moore_minimal(Trep, Lrep, 5, 2)
log(f"  minimal renaming classes: {int(minrep.sum()):,}")
Tm, Lm = Trep[minrep], Lrep[minrep]
depth = depth_game(Tm, Lm, 5, 2, 2)
BIGV = 10**6
finite = depth[depth < BIGV]
dmax = int(finite.max()) if finite.size else None
log(f"  max adaptive depth: {dmax} (manuscript: 9; C(5,2) = 10)")
summary["m5_structured"] = {
    "raw_total": int(N), "renaming_classes": int(uniq.shape[0]),
    "minimal_canonical": int(minrep.sum()), "max_depth": dmax,
    "depth_max_realizers_canonical": int((depth == dmax).sum()),
}
if dmax is not None:
    idx = np.where(minrep)[0]
    j = idx[np.argmax(depth == dmax)]
    emit_table("extremal_depth_M5_structured", Trep[j], Lrep[j], 5, 2, 2,
               note="M=5 structured-class machine attaining the maximum adaptive depth")

(SUP / "outputs").mkdir(exist_ok=True)
(SUP / "outputs" / "enumeration_summary.json").write_text(json.dumps(summary, indent=1))
log(f"summary saved -> outputs/enumeration_summary.json")
log("DONE")
