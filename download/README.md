# Automata Manuscript — Version Manifest

All deliverables live in this directory. Per the revision policy, **each new
revision creates a NEW version file; earlier versions are frozen and never
modified**.

| Version | File | Status | Contents |
|---------|------|--------|----------|
| v1 | `automata_unified_revised.tex` (in `upload/`, backup in `scripts/pre_fix_backup.tex`) | frozen (original) | original manuscript as reviewed |
| v2 | `automata_unified_revised_fixed.tex` / `.pdf` | FROZEN 2026-09-01 (read-only, md5 `287b28e5…`) | review findings A1 + B1–B7 applied |
| v3 | `automata_unified_revised_v3.tex` / `.pdf` | FROZEN 2026-09-01 (read-only, md5 `eec4bad1…`) | A2–A6 + C1 + global bold-Σ (`\bm{\Sigma}`); 234 pp. |
| v4 | `automata_unified_revised_v4.tex` / `.pdf` | FROZEN 2026-09-02 (read-only, md5 `7ea7be4f…`) | three flagged citations + two positioning sentences; C2 + C3; D1–D3; E1–E5; AAK proof-check precision edits; 233 pp. |
| v5 | `automata_unified_revised_v5.tex` / `.pdf` | **current latest** | two precision fixes from the remaining-theorems proof check: corrected display in `prop:grounding-tracking`(iii) (partition-independent term is the total modal mass 1−σ₁, not σ₁) and partition-reading convention added at `def:safe-right-cong`; 234 pp. |

## Companion documents

- `line_level_review_automata_unified_revised.docx` — full line-level review
  of v1 (findings A1–A6, B1–B7, C1–C3, D, E, severity-ranked table).
- `novelty_assessment_automata_unified.docx` — deep-web novelty assessment of
  the framework (20 queries, 8 literature families; verdict: framework-level
  novelty High, three citation gaps to close).
- `aak_multiletter_proof_check.docx` — dedicated line-level proof check of
  `thm:aak-multiletter`, its scalar anchor `thm:aak-equality`, and its
  dependency cone (verdict: sound; two precision edits, two observations,
  all applied in v4; external corroboration via Lacroce LearnAut 2022).
- `remaining_theorems_proof_check.docx` — dedicated line-level proof check of
  all 135 remaining proof-bearing results (50 theorems, 21 lemmas,
  37 propositions, 29 corollaries, 4 meta-theorems; verdict: 133 sound as
  stated, 2 minor proof-internal defects fixed in v5; 42/42 independent
  numerical checks pass, including the counter-family values, both
  non-convexity instances, the Csiszár identity, and the depth-6 witness
  machine).

## v4 change log (relative to v3)

- **Citations (novelty-report gaps closed)** — six verified references added
  and cited in the introduction's two new positioning paragraphs: Shalizi &
  Crutchfield 2002 (ACS 5:1–5); Marzen & Crutchfield, arXiv:1412.2859;
  Geiger, Petrov, Kubin & Koeppl, IEEE TAC 60(4):1010–1022, 2015; Geiger,
  Comput. Sci. Rev. 59:100802, 2026; Balle, Lacroce, Panangaden, Precup &
  Rabusseau, ICALP 2021 (LIPIcs 198:118); Lacroce, Balle, Panangaden &
  Rabusseau, MSCS 34:807–833, 2024. Attribution corrections found during
  verification: the IB–causal-states paper is by Shalizi & Crutchfield (not
  Still), and arXiv 1412.2859 is by Marzen & Crutchfield.
- **Positioning sentences** — retention: extends the causal-state program to
  controlled input-driven transductions and tracks the full budget-M gap
  curve (vs. the bottleneck-for-causal-states and KL-aggregation lines).
  Grounding: transports the AAK program for weighted automata from weighted
  languages to transductions, separates unrestricted vs. Hankel-restricted
  feasible sets, multiletter extension conditional.
- **D1** — `thm:exp-gap`: Ambainis bound now attributed to Theorem 1 of
  ISAAC'96 with the PFA/DFA statement made explicit; added the
  Freivalds-2008 nuance (logarithmic regime reached non-constructively,
  strongest form on Artin's conjecture; no unconditional exponential value).
  Form `S(k)=Ω(2^{k log log k / log k})` verified against the paper's
  official abstract.
- **C2** — font-shape warning `TU/lmr/m/scit` eliminated: `\textsc` problem
  names (`RationalExpCompare`, `PosSLP`) wrapped in `\textup` at all sites
  (trigger: small caps inside the italic proposition body, line 6081).
- **C3** — abstract compressed from ~170 lines / 10+ displays to three
  paragraphs with inline math only; a temporal-protocols summary paragraph
  added to the introduction ("Components of the framework").
- **D2** — availability statement softened: programs, machine tables, outputs,
  and the Lean fragment "will be made available upon publication"; explicitly
  not part of the present package.
- **D3** — new `rem:computational-conventions` (distinct-machine counting up
  to renaming, minimality by Moore refinement, lexicographic tie-breaking,
  named structured subclasses, arithmetic precision, search protocols), with
  five cross-references at the enumeration sites.
- **E1** — repeated scope statements consolidated: `rem:grounding-aak`,
  `rem:grounding-unrestricted-restricted`, `rem:grounding-supremum-organization`,
  the second half of `cor:grd-schatten`, and `rem:grounding-interpretations`
  now cross-reference `thm:spectral-grounding`/`thm:aak-equality` instead of
  re-displaying; retention-instantiation and conclusion finite-prefix
  sentences now point to `rem:prefixes-versus-states`.
- **E2** — exponent-layer duplicates converted to cross-reference anchors:
  `def:dmax-exponent` and `thm:grounding-alpha-infty` now name
  `def:dmax` / `thm:grounding-vertex` as the single maintained copies.
- **E3** — `meta:boolean(ii)`: added the note that discounted-prefix laws
  force `S = I*` in the right-closed case, so the sandwich never bites there.
- **E4** — `ex:onestep-not-congruence`: added the transient-state scope note
  (stationary support is the absorbing pair; structural point unaffected).
- **E5** — (1) `prop:lumpability` converse: `τ_K` now defined by the displayed
  intertwining with well-definedness derived; (2) `def:com-rd-gap`: attainment
  justified (finitely many machines up to renaming); (3)
  `thm:passive-realizable`: "all sufficiently large M" qualifier copied up
  from `cor:stream-all-M`; (4) "Myhill–Nerode" standardized at four remaining
  bare-"Nerode" sites; (5) comma splice in `meta:monotone(ii)` fixed.
- **AAK proof-check precision edits** — `thm:aak-multiletter`: third
  hypothesis tied to the transported operator `U H_ν U*` with the required
  distance identity displayed; proof now shows the full transport chain and
  notes the (retained) redundancy of the intertwining clause;
  `thm:aak-equality`: parenthetical that the canonical one-letter unitary
  satisfies hypothesis (a) automatically.

Verification: `scripts/verify_v4.py` — 47/47 checks PASS; tectonic compile
exit 0 (233 pp., 1.09 MiB, 0 undefined refs, no font warnings; 9 overfull
boxes, 8 inherited from v3, worst 12.4 pt).

## v5 change log (relative to v4)

- **F1 — `prop:grounding-tracking`(iii) display corrected.** The proof's
  intermediate identity read `D(φ)=σ₁−Σ_C max_b W_C(b)`; the correct identity
  is `D(φ)=Σ_s max_b w_s(b)−Σ_C max_b W_C(b)`, the first term being the
  partition-independent total modal mass `1−σ₁` (as displayed, the identity
  contradicted clause (ii) of the same proposition on the singleton
  compression). The stated result (refinement monotonicity of the tracking
  deficit) is unaffected; three anchored edits.
- **F2 — discrete Price-of-Safety convention made explicit.** A convention
  paragraph added at `def:safe-right-cong`: the free/safe optima of that
  subsection are read over *partitions* of S⁺ (transition-compatibility
  deliberately relaxed, matching the reading the subsection's own proofs
  use), with the strict-reading caveat recorded (under transition
  compatibility, `prop:pos-quad-consistent`(i)'s witness requires the safety
  partition to be a right congruence; the singleton partition always
  witnesses existence for M ≥ |S⁺|); the proposition's proof notes the
  witness is admissible under the stated convention. Two anchored edits.

Verification: anchored edits confirmed in place; tectonic compile exit 0
(234 pp., 1.09 MiB; 504 labels / 0 duplicates; 871 refs / 0 undefined;
environments matched; brace balance 0; 9 overfull boxes, identical count and
magnitudes to the v4 baseline, so no new overfull from the inserted text).
