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
| v5 | `automata_unified_revised_v5.tex` / `.pdf` | FROZEN 2026-09-02 (read-only, md5 `21db11d2…`) | two precision fixes from the remaining-theorems proof check: corrected display in `prop:grounding-tracking`(iii) (partition-independent term is the total modal mass 1−σ₁, not σ₁) and partition-reading convention added at `def:safe-right-cong`; 234 pp. |
| v6 | `automata_unified_revised_v6.tex` / `.pdf` | FROZEN 2026-09-02 (read-only, md5 `df384d6f…`) | the three non-blocking observations of the remaining-theorems proof check addressed (O1 forward references flagged at both sites; O2 Hadamard/Sylvester qualification at both sites, d = 11 of order 12 named; O3 verification suite recorded in the conventions remark) and the Data and Code Availability statement re-hardened to the assembled supplementary package; 234 pp. |
| v7 | `automata_unified_revised_v7.tex` / `.pdf` | FROZEN 2026-09-02 (read-only, md5 `fe3da4d5…`) | the two disambiguation footnotes implemented after verification and correction (Price of Safety — corrected citation arXiv:2309.08709 Shang–Colin–Barlier–Cherkaoui, three-instantiation strengthening; grounding gap — precise two-part NLP-sense description, arXiv:2311.09144 Shaikh et al.); Lean count corrected to seventeen statements across seven modules with sources/build/axiom-audit stated as shipped; availability statement re-hardened to the actual development; one capitalization consistency fix; two bibliography entries added; 234 pp. |
| v8 | `automata_unified_revised_v8.tex` / `.pdf` | **current latest** | five-part deep review of v7 (full 18,100-line read + extended automated scan, 327 raw flags adjudicated): two internal-connection cross-references (the §7 infinite-support remark now names the §3 remark it duplicates; the §6 normalized-valuation discussion now names `cor:boolean-01` as its schema-layer statement) and a new back-matter **Notation Index** — four cross-referenced booktabs tables covering ~50 principal symbols, ToC-linked, no new packages; verdicts: clarification layer saturated, register clean, flow seamless, one visual aid merited; 238 pp. |

## The supplementary package

`supplementary/` (repository root) is the actual package referenced by the
manuscript's availability statement since v6: the numerical verification suite
(41 checks, all PASS, log identical to the archived proof-check run), the
exhaustive machine enumeration programs (renaming classes, Moore minimality,
exact minimax games — reproducing the quoted 46,656/35,640 counts, the depth-6
maximum with its 3,072 raw realizers at M = 4, and the depth-9 maximum at
M = 5, all exactly), the extremal machine tables (CSV + LaTeX), the exact run
outputs, and — since v7 — **the actual Lean 4 development** (the `BST` Lake
project: seven modules, seventeen tracked declarations, sorry-free sources,
the build script, and the axiom-audit gate) together with the pristine
companion package of the superseded shorter manuscript at `supplementary/legacy/`
(120 verification programs, 10 consistency gates, SHA-256-manifest-verified;
gates re-run here: 681/681 regression assertions, 98/98 traceability, lossscan
PASS, controlled_ib VERIFIED at 1.8e-16). Its
README documents the reproduction status of every quoted computational
observation. The machine-checked `.lean` sources are integrated in
`supplementary/lean/BST/` (integrated this round from the companion effort,
whose package is preserved verbatim at `supplementary/legacy/`).

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
- `coinage_search_venue_decision.docx` — completion of the novelty report's
  pre-submission checklist: arXiv-class phrase search on the nine coinages
  (verdict: no same-sense collision; the core coinages unclaimed) and the
  venue decision (single submission, Information and Computation primary,
  Theory of Computing backup, arXiv preprint immediately, two-paper split
  retained only as a desk-rejection contingency). Search evidence under
  `scripts/coinage_search/`.
- `v7_revision_report.docx` — the five-task round: evaluation and correction of
  the two suggested disambiguation wordings (the arXiv:2508.20246 →
  2309.08709 citation fix and the three-instantiation strengthening; both
  footnotes as implemented), the automata_corrected.tex restoration analysis
  (label-level and line-level evidence; verdict: nothing to restore), the
  dedicated sentence-level flaw search (two genuine findings, both fixed in
  v7; full clean inventory), the supplementary/Lean integration (SHA-256-
  verified companion package, the fifteen→seventeen reconciliation, gate runs),
  and the open-questions assessment against v7 (ten settled, two open with
  recommendations, one partial).
- `v8_deep_review_report.docx` — the five-part deep-review round on v7:
  sentence-level merit scan (verdict: clarification/pedagogy layer saturated —
  hypothesis witnesses, mechanism remarks and reconciliation remarks cover
  all four failure modes; declined candidates documented), internal-connections
  analysis (two genuine gaps, closed as E1/E2; three connection candidates
  examined and left alone with reasons), the remnants/redundancy/informal-
  language scan (327 raw flags → 0 genuine defects beyond the E1 duplication;
  full adjudication table), the line-level flow verdict (seamless; all
  mechanical flags were scanner artifacts), and the visual-aids assessment
  (exactly one warranted addition, the Notation Index, implemented; figures
  and a master results-map declined as decorative).

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

## v6 change log (relative to v5)

- **O1 — forward references flagged (presentational).**
  `cor:fisher-uniform-remainder` now reads "Under the hypotheses of
  Theorem `thm:local-full-kl`, stated immediately below", and the proof of
  `cor:controlled-elementary-general` reads "As in Corollary
  `cor:controlled-elementary`, the independent-input special case stated
  below". Both references always resolved; the local reading order is now
  explicit. Reordering the results was deliberately avoided (churn risk).
- **O2 — Hadamard/Sylvester qualification, both sites.** The alphabet-reduction
  remark now says `d = 3, 7, 15, …` are the Sylvester orders `2^k − 1` and that
  every other Hadamard order also qualifies, `d = 11` (order-12 Hadamard
  matrix) being the smallest qualifier outside the Sylvester pattern; the
  open-problems summary carries the parallel qualification. The operative
  exact condition was already displayed and is unchanged.
- **O3 — independent verification suite recorded.** The Computational
  Conventions remark now records that the recomputable subset of the
  computational observations is reproduced exactly by an independent
  verification suite, and that the exhaustive searches are re-implemented
  under the stated conventions, distributed with the machine tables and exact
  outputs as part of the supplementary package (assembled in this round; see
  `supplementary/README.md` for the full reproduction table — the quoted
  46,656/35,640 counts, the 3,072 depth-6 realizers, and the M = 5 depth-9
  maximum all reproduce exactly).
- **Availability statement re-hardened.** "Are being prepared … and will be
  made available upon publication" replaced by a concrete statement of the
  package contents: the verification suite with exact outputs, the enumeration
  programs implementing the conventions, the machine tables of the extremal
  witnesses, and the statement manifest of the fifteen-statement Lean 4
  development.

Verification: `scripts/verify_v6.py` — 19/19 checks PASS (including v5 frozen
and byte-unchanged, md5 `21db11d2…`); tectonic compile exit 0 (234 pp.,
1.09 MiB; 504 labels / 0 duplicates; 873 refs / 0 undefined; environments
matched; brace balance 0; 9 overfull boxes, identical count and magnitudes to
the v5 baseline, so no new overfull from the inserted text).

## v7 change log (relative to v6)

- **E1 — Price of Safety disambiguation footnote** (first occurrence,
  Introduction, the surrogate paragraph): implemented after verification and
  two corrections. The suggested wording's citation arXiv:2508.20246 is the
  wrong paper (that is "Commitment Gap via Correlation Gap," Chawla–Christou–
  Dang); the safe-linear-bandits preprint using the phrase is arXiv:2309.08709
  (Shang, Colin, Barlier, Cherkaoui), now cited via the new `shang2023`
  bibitem. Strengthened to name the manuscript's three instantiations
  (`PoSquad`, `PoSlin` of sec:pos-linear; the mutual-information `PoS(M)` of
  `cor:price-safety`), since the term is a family, not a single quantity.
- **E2 — grounding-gap disambiguation footnote** (first occurrence,
  Introduction): the short variant applies (the term is bound to
  `def:symbolic-grounding-gap` at that exact point); strengthened with the
  two-part NLP-sense description (conversational common ground; outputs-to-
  world contact) and the citation `shaikh2023grounding` (arXiv:2311.09144,
  Shaikh, Gligorić, Khetan, Gerstgrasser, Yang, Jurafsky).
- **E3 — Lean statement count corrected** (`rem:lean-formalization`):
  "Fifteen statements" → "Seventeen statements are checked in total, across
  seven modules, with no appeal to sorry and no axioms beyond Lean's standard
  three, namely propositional extensionality, the axiom of choice, and
  quotient soundness. The sources, a build script, and the axiom audit
  accompany the manuscript as supplementary material." The shipped BST
  project's gate tracks exactly seventeen declarations and the companion
  manuscript itself says seventeen; the "shorter" repo copy had truncated
  the paragraph, and the error was inherited by v5/v6. (Fifteen counts the
  content statements; the other two declarations are technical helpers —
  mapping documented in `supplementary/lean/README.md`.)
- **E4 — availability statement re-hardened to the actual development**: the
  Lean component now names the development itself (seventeen machine-checked
  statements in seven modules) together with the build script and the
  axiom-audit gate that recompiles and verifies them.
- **E5 — capitalization consistency** (`cor:price-safety` body): "The price
  of safety is" → "The Price of Safety is" (the only lowercase use of the
  coinage in running text; 22 other occurrences are capitalized).
- **E6 — two bibliography entries** added (`shang2023`, `shaikh2023grounding`),
  formatted like the existing arXiv-style entries; all 39 entries cited.

Verification: `scripts/apply_v7_fixes.py` (six anchored, abort-before-write
edits against the md5-verified frozen v6); tectonic compile exit 0 (234 pp.,
1.10 MiB; 504 labels / 0 duplicates; 877 refs / 0 undefined; environments
matched; brace balance 0; 9 overfull boxes, identical count and magnitudes to
the v6 baseline, so no new overfull from the inserted footnotes);
`scripts/verify_v7.py` — 23/23 checks PASS; v6 frozen and byte-unchanged
(md5 `df384d6f…`).

## v8 change log (relative to v7)

- **E1 — infinite-support remark cross-referenced** (§7,
  `rem:infinite-support-grounding`): the grounding-side remark had repeated the
  content of the §3 abstract-impulse-response remark (`rem:infinite-support`)
  nearly verbatim — including two byte-identical closing sentences — without
  acknowledging it. It now states that it is the grounding-side instance of
  `rem:infinite-support`, that the content (boundedness needs decay;
  geometric decay suffices; non-decaying cases are decided case by case)
  transfers verbatim from the abstract setting, and that the Schur-test
  criterion is the same as there. The §3 remark remains the canonical
  statement; the maintenance hazard of two unlinked identical passages is
  removed. (Found by the Q2/Q3 cross-section duplicate-sentence detector.)
- **E2 — normalized-valuation echo linked** (§6, discussion after
  `thm:commitment-spec`): the structural `{0,∞}` vs. normalized `{0,1}`
  valuation discussion re-derived the point of §4's `cor:boolean-01` without
  linking it. One sentence added naming `cor:boolean-01` as the schema-layer
  statement of the separation, of which the displayed pair of valuations is
  the commitment instance. (Found by the same detector.)
- **E3 — Notation Index added** (new back-matter section between the
  bibliography and the availability statement, ToC-linked): four cross-
  referenced booktabs tables — shared schema objects; regime gaps and
  thresholds; divergences, operators and spectral objects; temporal,
  online-learning and strategic quantities — covering the ~50 principal
  recurring symbols with a one-line meaning and a resolving cross-reference
  to the site at which each is fixed. Lead-in paragraph states the scope rule
  (locally used symbols not repeated; regime-superscripted macro families
  listed once). No new packages; the manuscript previously had zero notation
  lookup devices across 234 pages and ~60 bespoke macro symbols. (The one
  warranted answer to Q5; figures and a master results-map were considered
  and declined as decorative, reasons recorded in the report.)

Verification: `scripts/apply_v8_fixes.py` (three anchored, abort-before-write
edits against the md5-verified frozen v7); tectonic compile exit 0 (238 pp.,
1.12 MiB, 0 errors, 0 undefined refs); first compile exposed one 22pt overfull
in a notation-table row (symbol column too narrow for the $\Esync$-family
atoms) — column widths rebalanced, final compile reproduces exactly the 9
overfull boxes of the v7 baseline, identical positions and magnitudes, zero
new; `scripts/verify_v8.py` — 21/21 checks PASS (v7 frozen and byte-unchanged,
md5 `fe3da4d5…`; all three edits present, old strings absent; 509 labels /
0 duplicates; 942 refs / 0 undefined (v7: 877; the notation index adds 65); environment pairing; brace balance;
39/39 bibitems cited both directions; notation index correctly placed with
45+ resolving row references; theorem-like environment count unchanged, so no
numbering disturbed).

## Submission package (built on v8, 2026-09-02)

`submission_package_v8/` (zip: `automata_ic_submission_v8.zip`) — the
complete Information and Computation submission package per the venue
decision, plus the ready-to-upload arXiv preprint bundle. No manuscript
version was created or modified: v8 ships as-is.

- `SUBMISSION_NOTES.md` — the operating manual: contents map, the
  personalization protocol (author block → new version file v9 under the
  freeze policy; cover-letter placeholders), Editorial Manager upload
  order, the one open citation decision (arXiv 2608.12791, not cited by
  default), and the desk-rejection contingencies.
- `cover_letter/cover_letter.tex` + `.pdf` — the cover letter (2 pp.),
  drafted per the venue report's Section 7: the four High-novelty items
  foregrounded, the per-regime-instruments-are-transports positioning
  stated plainly, the multiletter-AAK status stated honestly
  (conditional-form theorem, hypothesis an explicit open problem, line-level
  proof-checked, computational support reproduced, no external
  corroboration), verification depth, and declarations. Placeholders for
  author details.
- `manuscript/` — v8 source and a PDF recompiled from that exact source at
  packaging time (integrity: 238 pp., 0 errors, 0 undefined refs, the
  documented 9-box overfull baseline reproduced).
- `supplementary/` + `supplementary_v8.zip` — the journal-facing
  supplementary package (programs, machine tables, outputs, Lean 4
  development; 43 files, byte-identical to the repository's
  `supplementary/`), exactly the material the availability statement
  enumerates; the internal `legacy/` provenance package is excluded.
- `optional_editor_material/` — the two proof-check reports (the venue
  report recommends attaching them; upload optional).
- `arxiv/arxiv_source_v8.tar.gz` + `ARXIV_NOTES.md` — the arXiv bundle
  (self-contained v8 `.tex` at root + the supplementary as `anc/` ancillary
  files, 54 entries) and the metadata notes (title, categories suggestion
  cs.FL / cs.IT / math.IT / stat.ML, comments field, sequencing).
- `highlights.txt` — optional Elsevier highlights (5 bullets, ≤85 chars).
