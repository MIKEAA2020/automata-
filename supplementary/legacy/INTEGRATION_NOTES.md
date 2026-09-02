# Legacy Companion Package — Integration Notes

This directory is the **pristine companion package** of the superseded
shorter manuscript `automata_corrected.tex` (shipped here as
`manuscript.tex`, byte-identical modulo line endings to
`shorter vsuperseded/automata_corrected.tex` in the repository). It was
produced in a companion effort and is preserved **unmodified**: every one of
its 154 files verifies against its own `MANIFEST.txt` (SHA-256 + size).
Nothing in this directory has been edited; all integration for the current
manuscript happens one level up, in `supplementary/lean/`, `supplementary/programs/`,
`supplementary/machine_tables/`, and `supplementary/outputs/`.

## Why it is kept

1. **Provenance and auditability.** It is the source of the Lean 4
   development (hoisted to `../lean/`), and its `MANIFEST.txt` lets any
   reviewer confirm that the hoisted copy is byte-faithful.
2. **Breadth of computational observations.** Its `verify/` tree contains 120
   standalone programs covering far more of the manuscript's computational
   claims than the curated v7-anchored suite in `../programs/`: controlled-IB
   identities, rate–distortion non-convexity witnesses, alphabet-similarity
   constructions, grounding-tracking decompositions, PoS feasibility
   enumeration, and so on.
3. **The consistency gates.** Its `tools/` tree contains ten gates
   (`regression_all.py` — 681 assertions pinned to mathematical content,
   `traceability.py`, `lossscan.py`, `convention.py`, `check_active.py`,
   `dag.py`, `check_report.py`, `register.py`, `lean_check.py`,
   `partition.py`) with a documented design that separates "computational
   observation" from "proof".

## Caveats for use against the current manuscript

- **Label lineage.** The gates and traceability map were written against
  `manuscript.tex` (= `automata_corrected.tex`). The current manuscript
  (`download/automata_unified_revised_v7.tex`) descends from that file with
  the same label namespace: a full label-set comparison finds only two
  renames (`sec:right-cong` → `subsec:right-cong`; the `sec:openproblems`
  label on the gap-symbol remark was dropped while the remark itself
  survives) and v7-only additions. Run the gates from this directory with
  `BST_ROOT` pointing here if you want them to resolve against the shipped
  `manuscript.tex`.
- **Verification status.** The programs were verified against the companion
  manuscript's claims. The headline claims of the current manuscript are
  re-verified by the curated suite in `../programs/` and its archived logs in
  `../outputs/`; the legacy programs provide **additional, broader**
  computational observations, not the authoritative reproduction path.
- **Lean.** The `lean4/` copy here is the pristine original;
  `../lean/` is the integrated one (identical sources; the gate script there
  resolves both layouts).

## Quick start (from this directory)

```sh
python3 tools/regression_all.py     # 681 assertions
python3 tools/traceability.py       # programs -> manuscript artefacts
python3 verify/controlled_ib.py     # a representative verification
```
