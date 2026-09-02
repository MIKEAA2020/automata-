#!/usr/bin/env python3
"""Emit the machine tables of the manuscript's fixed example machines
(those defined inline in proofs and remarks, as opposed to the enumeration
extremals emitted by enumerate_machines.py):
  * the counter family C_M, M = 3..7 (retention refinement-extremal scope);
  * the 5-state and 4-state rd-nonconvex instances;
  * the explicit M=4 adaptive-depth witness of prop:lsyncu-binomial.
Tables are written as CSV (program-readable) and LaTeX tabular
(manuscript-consistent) into ../machine_tables/."""
import pathlib

TAB = pathlib.Path(__file__).resolve().parent.parent / "machine_tables"
TAB.mkdir(parents=True, exist_ok=True)

def emit(name, header, rows, tex_head, tex_body, note):
    (TAB / f"{name}.csv").write_text(",".join(header) + "\n" +
                                     "\n".join(",".join(map(str, r)) for r in rows) + "\n")
    (TAB / f"{name}.tex").write_text(
        f"% {name} — {note}\n\\begin{{tabular}}{{{'l' * len(header)}}}\n\\toprule\n"
        f"{tex_head} \\\\\n\\midrule\n{tex_body} \\\\\n\\bottomrule\n\\end{{tabular}}\n")

# ---- counter family C_M, M = 3..7 (beta = 1/2, gamma = 1/10) ----
rows = []
for M in range(3, 8):
    for s in range(M):
        p1 = "1/2" if s <= M - 2 else "1/10"
        p0 = "1/2" if s <= M - 2 else "9/10"
        rows.append([f"C_{M}", s, min(s + 1, M - 1), 0, p0, p1])
emit("counter_family_C_M",
     ["machine", "state", "tau(s,0)", "tau(s,1)", "P_s(y=0)", "P_s(y=1)"],
     rows,
     "machine & $s$ & $\\tau(s,0)$ & $\\tau(s,1)$ & $P_s(0)$ & $P_s(1)$",
     " \\\\\n".join(" & ".join(map(str, r)) for r in rows),
     "counter family C_M; stationary retention witnesses (RetKLc(M-1) = "
     "0.0481/0.0321/0.0192/0.0107/0.0057 for M = 3..7)")

# ---- 5-state rd-nonconvex instance ----
w5 = [0.0344, 0.3506, 0.1906, 0.2176, 0.2068]
raw5 = [(0.4805, 0.4113, 0.1082), (0.2746, 0.4018, 0.3236), (0.2960, 0.5426, 0.1614),
        (0.2334, 0.5019, 0.2648), (0.6498, 0.0548, 0.2954)]
rows = []
for s, (w, r) in enumerate(zip(w5, raw5)):
    tot = sum(r)
    rows.append([s, f"{w:.4f}"] + [f"{v / tot:.6f}" for v in r])
emit("nonconvex_instance_5state",
     ["state", "weight pi_s", "P_s(0)", "P_s(1)", "P_s(2)"],
     rows,
     "$s$ & $\\pi_s$ & $P_s(0)$ & $P_s(1)$ & $P_s(2)$",
     " \\\\\n".join(" & ".join(map(str, r)) for r in rows),
     "5-state instance of prop:rd-nonconvex; D(M) = "
     "0.0948616/0.0148089/0.0049099/0.0021747/0, log-convexity fails")

# ---- 4-state rd-nonconvex remark instance ----
w4 = [17, 18, 22, 21]
raw4 = [(20, 25, 2), (2, 34, 30), (37, 1, 27), (20, 9, 1)]
rows = []
for s, (w, r) in enumerate(zip(w4, raw4)):
    tot = sum(r)
    rows.append([s, f"{w / 78:.6f}"] + [f"{v / tot:.6f}" for v in r])
emit("nonconvex_instance_4state",
     ["state", "weight pi_s", "P_s(0)", "P_s(1)", "P_s(2)"],
     rows,
     "$s$ & $\\pi_s$ & $P_s(0)$ & $P_s(1)$ & $P_s(2)$",
     " \\\\\n".join(" & ".join(map(str, r)) for r in rows),
     "4-state remark instance; D(M) = 0.2887482/0.1601480/0.0145216/0")

# ---- M=4 adaptive-depth witness (prop:lsyncu-binomial) ----
rows = [[s, t0, y0, t1, 0]
        for s, (t0, y0, t1) in enumerate(zip([0, 0, 3, 2], [0, 1, 0, 0], [0, 2, 3, 1]))]
emit("adaptive_witness_M4",
     ["state", "tau(s,0)", "lambda(s,0)", "tau(s,1)", "lambda(s,1)"],
     rows,
     "$s$ & $\\tau(s,0)$ & $\\lambda(s,0)$ & $\\tau(s,1)$ & $\\lambda(s,1)$",
     " \\\\\n".join(" & ".join(map(str, r)) for r in rows),
     "explicit M=4 witness of prop:lsyncu-binomial; adaptive depth 6 = C(4,2); "
     "identical (up to the conventions) to the canonical extremal emitted by "
     "the enumeration program")

print("machine tables written:", sorted(p.name for p in TAB.glob('*.csv')))
