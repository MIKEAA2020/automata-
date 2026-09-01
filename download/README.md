# Automata Manuscript — Version Manifest

All deliverables live in this directory. Per the revision policy, **each new
revision creates a NEW version file; earlier versions are frozen and never
modified**.

| Version | File | Status | Contents |
|---------|------|--------|----------|
| v1 | `automata_unified_revised.tex` (in `upload/`, backup in `scripts/pre_fix_backup.tex`) | frozen (original) | original manuscript as reviewed |
| v2 | `automata_unified_revised_fixed.tex` / `.pdf` | **FROZEN 2026-09-01** (read-only, md5 `287b28e5…`) | review findings A1 + B1–B7 applied |
| v3 | `automata_unified_revised_v3.tex` / `.pdf` | current latest | A2–A6 + C1 + global bold-Σ (`\bm{\Sigma}`) applied; compiles to 234 pp., 8 residual overfull boxes (none > 12.4 pt) |

## Companion documents

- `line_level_review_automata_unified_revised.docx` — full line-level review
  of v1 (findings A1–A6, B1–B7, C1–C3, D, E, severity-ranked table).
- `novelty_assessment_automata_unified.docx` — deep-web novelty assessment of
  the framework (20 queries, 8 literature families; verdict: framework-level
  novelty High, three citation gaps to close).

## v3 change log (relative to v2)

- **A2** — `thm:independence(iv)`: modular witness language switched to the
  delimiter-free unary form `L_N = {1^n : n ≡ 0 mod N}`; "exactly N" now
  justified by the N Myhill–Nerode residue classes.
- **A3** — `thm:stream-lb-binary`: numeric claim corrected, ratio exceeds
  0.23 first at `L = 4` (0.2387), not `L = 3` (0.218).
- **A4** — `prop:renyi-limits(iii)`: invalid "fixed operator" justification
  replaced by a two-step continuity argument (matrix-power continuity on the
  support, then monotone convergence for the fixed limit operator) with
  explicit sandwiched-Rényi citations (Müller-Lennert et al.; Frank–Lieb,
  both added to the bibliography).
- **A5** — revision-seam text ("previous version of this claim", "upgrades
  the earlier…") rewritten in self-contained terms; "Correction" label
  removed from the Exact Results list.
- **A6** — `prop:lsyncu-quadratic`: garbled pair-automaton "nested sets"
  justification replaced by a citation of the Moore lemmas
  (`lem:tension` with `U={s,t}`, cross-machine form `lem:moore-separation`),
  with an honest note that pair-node distinctness alone gives
  `binom(M,2)`, not `M−1`.
- **C1** — typesetting pass: the two page-overflowing admissible-value items
  of `def:type-signature` converted to displayed multi-line lists; five
  further overfull displays/paragraphs displayed or restructured; regime
  table narrowed; `microtype` + `\emergencystretch{2em}` loaded. Overfull
  boxes: 151 (v1) → 52 (v2) → **8 (v3)**, none above 12.4 pt.
- **Bold Σ** — all 113 covariance-matrix occurrences (`\Sigma_\pi`,
  `\Sigma_p`, `\Sigma_\eta`, `\Sigma_F`, and fiber variants) now set as
  `\bm{\Sigma}` (matrix nature emphasized, avoids the B7 symbol collision);
  alphabet `Σ` and summation uses untouched.

Verification: `scripts/verify_v3.py` — 51/51 checks PASS.
