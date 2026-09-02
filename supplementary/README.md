# Supplementary Package — Machine-Checked and Computational Material

This package accompanies the manuscript *automata unified (revised)* (current
version: `automata_unified_revised_v6.tex`). It contains the programs, the
extremal machine tables, and the exact outputs referenced by the manuscript's
Data and Code Availability statement, together with the statement manifest of
its Lean 4 development.

## Contents

| Path | Contents |
|------|----------|
| `programs/verify_numerical_claims.py` | numerical verification suite: reproduces every recomputable computational observation quoted in the manuscript (41 boolean checks) |
| `programs/enumerate_machines.py` | exhaustive enumeration of Mealy machines under the manuscript's Computational Conventions: renaming-class counting, Moore minimality, exact minimax adaptive-depth and identification-mistake games |
| `programs/gen_machine_tables.py` | emits the tables of the manuscript's fixed example machines |
| `machine_tables/` | extremal and example machines, each as CSV (program-readable) and LaTeX tabular (manuscript-consistent) |
| `outputs/` | exact run logs (`verify_numerical_claims.log`, `enumeration.log`) and the machine-readable `enumeration_summary.json` |
| `lean/` | statement manifest of the fifteen-statement Lean 4 / Mathlib development (`rem:lean-formalization`), with its integration protocol |

## Conventions

The enumerations implement the manuscript's remark *Computational Conventions*
(`rem:computational-conventions`) exactly:

- **Distinct machines** are labelled transition/output table pairs counted up
  to renaming of the state set; a count of `N` machines means `N` renaming
  classes, computed by canonical-form minimization over all `M!` relabelings.
- **Minimality** is decided by Moore partition refinement before counting.
- **Tie-breaking** is lexicographic on the canonical encoding (the
  representative kept is the first raw machine attaining each canonical code).
- **Arithmetic**: the verification suite uses exact rational arithmetic where
  the manuscript states it and double precision where the manuscript itself
  does; the enumeration is exact (integer game values).
- **Search** is exhaustive over the stated classes.

## How to run

```
python3 programs/verify_numerical_claims.py   # ~30 s, requires numpy
python3 programs/enumerate_machines.py        # ~4 min, requires numpy
python3 programs/gen_machine_tables.py        # instant
```

All runs are deterministic; the shipped logs are reproducible byte-for-byte
(the verification log is identical to the one produced during the dedicated
proof-check round).

## Reproduction status of the manuscript's quoted observations

| Manuscript claim | Quoted | Reproduced here | Status |
|---|---|---|---|
| Counter family `RetKLc(M-1)`, M = 3..7 | 0.0481 / 0.0321 / 0.0192 / 0.0107 / 0.0057 | same, 7 decimals | exact |
| `prop:rd-nonconvex` 5-state and 4-state `D(M)` tables | 0.0948616 … / 0.2887482 … | same, 7 decimals | exact |
| Csiszár (dagger) identity for the KL generator | defect < 1e-15; reverse-KL −0.1657 | 1e-16; −0.1657 | exact |
| M = 4 witness adaptive depth (`prop:lsyncu-binomial`) | 6, minimal | 6, minimal | exact |
| Forcing-stream at L = 2 (`thm:stream-lower-bound`) | 8 forced mistakes | 8 | exact |
| Bernoulli–Fisher ratio | 0.50009 | 0.50009 | exact |
| `prop:kl-simplex-sharp` expansion | 2ε² + (4/3)ε⁴ | matches to O(ε⁶) | exact |
| Cyclic-shift depths (`thm:esyncsi-theta`) | depth = L, Bayes = L/2, L = 1..10 | L = 1..10 all PASS | exact |
| Ky Fan minorant on random instances | no violations | 400 instances, 0 violations | exact |
| Largest signature table pairs | 46,656 raw; 35,640 minimal | (M=3, I=2, O=2): 46,656 raw; 35,640 minimal | exact |
| Max adaptive depth, M = 3 and M = 4 (binary) | 3 and 6 | 3 and 6 | exact |
| M = 4 depth-6 realizers | 3,072 machines | 3,072 (raw minimal; 128 renaming classes × 24) | exact |
| Identification mistakes ≤ ⌊log₂ M⌋; attained at M = 2, M = 4 | yes | 1, 1, 2 for M = 2, 3, 4 (attained at M = 2 and M = 4 as claimed; also at M = 3, which the claim does not exclude) | exact |
| Enlarging \|O\| from 2 to 4 leaves the worst case unchanged | yes | unchanged at M = 2, 3, 4 | exact |
| M = 5 structured class max depth | 9 (short of C(5,2) = 10) | 9 | exact |
| M = 5 structured class size | 2,839,200 minimal machines | under the interpretation documented in the program (first input a permutation, constant first-input outputs, single probe state on the second input): 1,875,000 raw, 16,100 renaming classes, 11,830 minimal — the load-bearing extremal claim (depth 9) reproduces exactly | partial (class reading) |
| M = 7 refinement-round verification over 9,313,920 minimal machines | as quoted | not re-executed: the structured-class reading at M = 7 and the instance sampling are not fully pinned down by the quotation; the enumeration program is parameterized for it | not re-run |
| Hill-climbing values at M = 6..8 | 9, 14, 14 | not re-executed: depends on the restart schedule quoted only at the site | not re-run |
| Retention-numerical pair counts (2,434 / 1,664 pairs) | as quoted | the inequalities are reproduced on fresh random instances (400, 0 violations); the quoted counts depend on the original instance draws | partial (instance set) |

The one signature in the grid whose raw space exceeds the exhaustive budget
((M, I, O) = (4, 2, 4), 16⁸ ≈ 4.3·10⁹ table pairs) is excluded from the
exhaustive run; the manuscript's output-alphabet-independence remark covers it.

## Lean 4 development

The fifteen-statement Lean 4 / Mathlib development of `rem:lean-formalization`
was produced and machine-checked in a companion effort; `lean/README.md` is
its statement manifest and integration protocol. The manuscript's availability
statement points to this package for it.

## Machine-table inventory

- `counter_family_C_M` — retention counter family, M = 3..7.
- `nonconvex_instance_5state`, `nonconvex_instance_4state` — rate-distortion
  non-convexity witnesses (weights and emission tables).
- `adaptive_witness_M4` — the explicit depth-6 witness of
  `prop:lsyncu-binomial`; identical, under the conventions, to the canonical
  extremal emitted by the enumeration program
  (`extremal_depth_M4_I2_O2`), which confirms the lexicographic tie-breaking
  convention.
- `cyclic_shift_L1..L4` — the cyclic-shift family of `thm:esyncsi-theta`.
- `extremal_depth_M3_I2_O2`, `extremal_depth_M4_I2_O2` — canonical minimal
  machines attaining the maximum adaptive depth of the binary signatures.
- `extremal_depth_M5_structured` — canonical minimal machine attaining depth 9
  in the M = 5 structured class.
