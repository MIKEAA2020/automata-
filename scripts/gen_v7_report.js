// gen_v7_report.js — v7 revision report: the five-task instruction (wording
// evaluation, corrected-lineage restoration analysis, sentence-level flaw
// search, supplementary/Lean integration, open-questions assessment).
// House pipeline: R1 cover, 3-section numbering (cover / TOC roman / body
// arabic), TOC + refresh hint, header/footer. English, report scene.
const {
  Document, Packer, Paragraph, TextRun, Header, Footer, PageNumber,
  NumberFormat, AlignmentType, SectionType, TableOfContents,
} = require("docx");
const fs = require("fs");
const {
  P, buildCoverR1, h1, h2, body, bodyRuns, run, mono, bullet,
  quoteBlock, cell, tableCaption, makeTable, EN_FONT, HEAD_FONT,
} = require("./v7_helpers.js");

const OK = "2E6B3E";      // green: verified / resolved
const WARN = "B4540A";    // amber: open / partial
const FIX = "1F5FA8";     // blue: corrected in v7
const bodyChildren = [];

// ================= 1. Executive Summary =================
bodyChildren.push(h1("1. Executive Summary"));
bodyChildren.push(body(
  "This report records the execution of the five-part instruction issued against the current manuscript chain: (1) evaluate, verify, strengthen or correct the two suggested disambiguation wordings before implementing them; (2) determine whether anything in the superseded automata_corrected.tex is worth restoring in the final version; (3) conduct a dedicated sentence-level search for remaining flaws in that final version; (4) examine the supplementary and Lean files shipped with the superseded manuscript and bring over whatever is worth keeping; and (5) determine which items of the open-questions queue still apply. The work was performed on 2026-09-02 against the frozen latest version automata_unified_revised_v6.tex (234 pages, 18 sections, 504 labelled environments, all prior review families closed), and it produced a new version file, automata_unified_revised_v7.tex, under the standing version-freeze policy: v6 was verified byte-unchanged before any edit and remains frozen at md5 df384d6facf47ba36776261adb948850."));
bodyChildren.push(body(
  "The five verdicts are as follows. First, the two suggested wordings were implemented after two substantive corrections: the suggested arXiv identifier for the Price-of-Safety footnote, 2508.20246, is the wrong paper (it is the commitment-gap-in-CICS preprint of Chawla, Christou and Dang), and the manuscript uses the term for a family of three formalizations rather than the single quantity the suggested wording assumes; the implemented footnote cites the correct preprint, arXiv:2309.08709 of Shang, Colin, Barlier and Cherkaoui, and names all three instantiations. Second, nothing in automata_corrected.tex is worth restoring: a label-level and line-level comparison shows the current manuscript strictly contains the corrected file's content, the only differences being deliberate improvements from the review cycle. Third, the dedicated sentence-level search found exactly two genuine defects, both minor and both fixed in v7: a single lowercase use of the Price of Safety coinage, and the inherited fifteen-versus-seventeen miscount of the Lean statements. Fourth, the companion package was located, verified against its own SHA-256 manifest (154 files, zero mismatches), and integrated: the actual Lean 4 project (seven modules, seventeen tracked declarations, sorry-free sources, build script, axiom-audit gate) is now part of the supplementary package, and the availability statement is re-hardened accordingly. Fifth, of the thirteen open-questions items, ten are settled by the current state, two remain genuinely open but carry a recommendation to leave them (Q2 and Q7), and one applies only partially (Q13a) with two benign residual forward references."));

// ================= 2. Task 1 =================
bodyChildren.push(h1("2. Task 1 — The Two Suggested Wordings: Evaluation, Corrections, Implementation"));
bodyChildren.push(h2("2.1 Price of Safety footnote"));
bodyChildren.push(body(
  "The suggested footnote reads, in its first variant: \u201cHere and throughout, \u2018Price of Safety\u2019 refers to the quantity defined in [Section/Definition number]. It is unrelated to the same phrase used in a recent preprint on safe linear bandits (arXiv:2508.20246), which studies a different trade-off.\u201d Evaluation against the evidence on record produced two corrections before implementation."));
bodyChildren.push(bullet([
  run("Citation error (verified against both the recorded coinage-search evidence and the live arXiv record). ", { bold: true }),
  run("arXiv:2508.20246 is \u201cCommitment Gap via Correlation Gap\u201d (Chawla, Christou and Dang, August 2025), a paper about the commitment gap of costly-information combinatorial selection. The safe-linear-bandits paper that actually uses the phrase is "),
  run("arXiv:2309.08709, \u201cPrice of Safety in Linear Best Arm Identification\u201d (Shang, Colin, Barlier and Cherkaoui, September 2023)", { bold: true }),
  run(", where the term denotes the additional sample-complexity term incurred by forced exploration under stage-wise safety constraints. Implementing the suggested identifier verbatim would have cited the wrong work; the implemented footnote cites the correct one, as a proper bibliography entry (shang2023) rather than a bare identifier, consistent with the manuscript's citation practice."),
]));
bodyChildren.push(bullet([
  run("Single-quantity assumption (verified against the manuscript's own usage map). ", { bold: true }),
  run("The phrase \u201cPrice of Safety\u201d does not denote one quantity in this manuscript: it is the safety-constraint gap pattern instantiated three ways — the discrete right-congruence quantity PoS_quad of Section 11 (defined around def:safe-right-cong), its linear surrogate PoS_lin (def:poslin), and the mutual-information form PoS(M) = \u0394_ret^safe(M) \u2212 \u0394_ret^free(M) of Corollary cor:price-safety in Section 12. The manuscript's own open-problems section confirms the family reading, speaking of \u201cthe discrete right-congruence Price of Safety PoSquad(M) or the full-KL Price of Safety.\u201d The implemented footnote therefore says what the pattern is (the free optimum minus the safety-constrained optimum) and names all three instantiations, rather than pointing at a single definition number."),
]));
bodyChildren.push(body(
  "Two smaller points were also adjusted. \u201cA recent preprint\u201d was dropped as a descriptor: the correct paper is from September 2023 and its phrase usage is stable. And the anchor point was chosen as the first unhyphenated occurrence of the phrase in the body, line 649 of v6, inside the Introduction's Price-of-Safety surrogate paragraph — footnotes in the abstract are poor practice, and the hyphenated adjectival compounds earlier in the abstract and introduction are covered by the \u201chere and throughout\u201d scope of the note."));
bodyChildren.push(body("The implemented footnote (v7, first occurrence, Introduction):"));
bodyChildren.push(quoteBlock(
  "Here and throughout, \u201cPrice of Safety\u201d is this manuscript's safety-constraint gap — the free optimum minus the safety-constrained optimum — instantiated as the discrete right-congruence quantity PoSquad and its linear surrogate PoSlin of Section [sec:pos-linear], and in mutual-information form as the PoS(M) of Corollary [cor:price-safety]. It is unrelated to the same phrase in the safe-bandits literature, where it denotes the additional sample complexity incurred under stage-wise safety constraints in best-arm identification [shang2023]."));
bodyChildren.push(body(
  "The second suggested variant (no citation, \u201cthe safe-learning literature\u201d) remains available as a fallback, but the corrected citation is strictly stronger: the coinage search on record already established that the collision is same-phrase, different-sense, and the footnote now documents that with a precise reference. The suggested \u201creplace the bracketed parts with the correct section/definition numbers\u201d instruction is satisfied by the three anchors sec:pos-linear, def:poslin / def:safe-right-cong (via the section reference) and cor:price-safety."));

bodyChildren.push(h2("2.2 Grounding-gap clause"));
bodyChildren.push(body(
  "The suggested parenthetical assumes the term needs a brief definition at first use; the manuscript, however, already binds the term to a definition at that exact point — the first occurrence, line 360 of v6, reads \u201cDefinition [def:symbolic-grounding-gap] below supplies a quotient-typed symbolic grounding gap, over deterministic Mealy machines,\u201d and the definition itself (the discounted symbolic grounding gap \u0394_grd(M;\u03b3), an infimum over M-state deterministic Mealy approximants of a worst-case discounted Kantorovich\u2013Rubinstein distance) follows in Section 7. The suggested shortened variant is therefore the right shape, and it was strengthened in two ways: the NLP sense is described precisely rather than loosely, and it carries a citation."));
bodyChildren.push(body(
  "On precision: the suggested text describes the NLP sense as \u201ca language model's failure to connect its outputs to the external world.\u201d That is a fair one-line summary of the broader usage (the arXiv full-text search returned 21 hits, spanning conversational grounding, visual grounding in vision-language models, and abstract-concept anchoring), but the canonical collision the coinage search actually near-matched is arXiv:2311.09144, \u201cGrounding Gaps in Language Model Generations\u201d (Shaikh, Gligori\u0107, Khetan, Gerstgrasser, Yang and Jurafsky), where the grounding gap is specifically about conversational common ground — grounding acts such as clarification and acknowledgment — rather than world-contact at large. The implemented clause covers both readings: failure to establish conversational common ground, or to connect generated outputs to the external world."));
bodyChildren.push(body("The implemented footnote (v7, first occurrence, Introduction):"));
bodyChildren.push(quoteBlock(
  "As used here, a \u201cgrounding gap\u201d is a quotient-typed approximation cost: the discounted symbolic quantity \u0394_grd(M;\u03b3) of Definition [def:symbolic-grounding-gap] together with its linear finite-rank relatives \u0394_grd^unres(M) and \u0394_grd^Hank,str(M) of Section [sec:grounding]. The term has no connection to its natural-language-processing sense, where a grounding gap is a language model's failure to establish conversational common ground or to connect its generated outputs to the external world [shaikh2023grounding]."));
bodyChildren.push(body(
  "Both new citations were added as proper bibliography entries (shang2023 for arXiv:2309.08709, shaikh2023grounding for arXiv:2311.09144), formatted exactly like the manuscript's existing arXiv-style entries; the bibliography grows from 37 to 39 entries and every entry remains cited, with the two new keys used from the respective footnotes. The venue-decision report's watch item (arXiv:2608.12791, \u201cThermodynamics of Learning,\u201d which uses \u201cretention gap\u201d in a typed-accounting sense) remains a monitor-only item, since the manuscript's own term there is unhyphenated running prose rather than a capitalized coinage and the collision is again same-phrase, different-sense."));

// ================= 3. Task 2 =================
bodyChildren.push(h1("3. Task 2 — automata_corrected.tex: Restoration Analysis"));
bodyChildren.push(body(
  "The superseded file shorter vsuperseded/automata_corrected.tex (17,014 lines, 483 labelled environments, CRLF line endings) is the base from which the current chain descends: the unified manuscript was built on it and then passed through the full review cycle (A1\u2013A6, B1\u2013B7, C1\u2013C3, D1\u2013D3, E1\u2013E5, the positioning citations, the two dedicated proof-check rounds, and the three Section-5 observations). The question is whether the passage to the unified chain dropped anything of value. Two independent comparisons say no."));
bodyChildren.push(h2("3.1 Label-level comparison"));
bodyChildren.push(body(
  "Every labelled environment in automata_corrected.tex was checked against the v6 label set. Exactly two labels of the corrected file are absent from v6, and both are naming artifacts rather than content: the cofilteredness lemma for support-relative congruences survives at the same position with its label renamed from sec:right-cong to subsec:right-cong, and the \u201cHow to read a gap symbol\u201d remark survives intact with its section label dropped. Conversely, v6 carries 23 labelled environments that corrected lacks — the review-driven additions (the pair-determination-index family behind the A1 fix, the finite-monitor and observable-floor theorems, the grounding finite-section and structured-zero propositions, the computational-conventions remark, and the scope remarks added by the positioning round). At the level of labelled content, v6 is a strict superset."));
bodyChildren.push(tableCaption("Table 1. Label-level comparison (corrected vs v6)."));
bodyChildren.push(makeTable(
  [cell("Quantity", { bold: true, fill: P.surface, w: 40 }), cell("corrected.tex", { bold: true, fill: P.surface, w: 30 }), cell("v6.tex", { bold: true, fill: P.surface, w: 30 })],
  [
    [cell("Lines", { w: 40 }), cell("17,014", { w: 30 }), cell("18,066", { w: 30 })],
    [cell("Labelled environments", { w: 40 }), cell("483", { w: 30 }), cell("504", { w: 30 })],
    [cell("Labels in corrected absent from v6", { w: 40 }), cell("2 (both renames, content survives)", { w: 30 }), cell("\u2014", { w: 30 })],
    [cell("Labels in v6 absent from corrected", { w: 40 }), cell("\u2014", { w: 30 }), cell("23 (review-driven additions)", { w: 30 })],
    [cell("Bibliography entries", { w: 40 }), cell("28", { w: 30 }), cell("37", { w: 30 })],
  ]));
bodyChildren.push(h2("3.2 Line-level comparison"));
bodyChildren.push(body(
  "A full unified diff was computed after normalizing the line endings (the corrected file is CRLF, the current chain LF). The delta is +1,740 / \u2212688 lines across 166 hunks, and its structure rules out silent content loss: there is exactly one pure-deletion hunk in the entire diff, and it deletes a single comment separator line. Every other minus-line participates in a replacement pair. The six replacement hunks in which v6 is materially shorter than corrected are all deliberate review-cycle improvements, verified individually:"));
bodyChildren.push(bullet([run("The abstract was rewritten (the C3 fix, three-paragraph form). All substantive claims of the old abstract survive, either in the new abstract or more precisely in the body; the one clause dropped at abstract level \u2014 that the input-driven synchronized subclass contains all complexity constructions \u2014 is stated more precisely in the body at the machine-model remark, which says the complexity constructions are stated for the input-driven model and transfer to the unifilar class by the complexity-transfer remark.")]));
bodyChildren.push(bullet([run("Four hunks in the exponent-vertex section replace definitions and theorems restated verbatim from earlier sections (def:dmax, thm:grounding-vertex, the grounding-gap displays) with pointers to their original statements. This is the E-item deduplication: the corrected file repeated material \u201cso the section is self-contained,\u201d which invites drift between copies; v6 keeps one statement and cross-references it. Nothing was lost, and restoring the duplicates would reintroduce a maintenance hazard the review cycle deliberately removed.")]));
bodyChildren.push(bullet([run("The unifilar machine-model block (Definition def:unifilar-machine and its three companion definitions, 122 lines) was moved from Section 9 (Two-Axis Oracle) to Section 3 (Specialized Task Theories). This is the Q13a ordering fix discussed in Section 6 below: the definitions now precede every use, where in corrected they followed their own theory by 3,622 lines.")]));
bodyChildren.push(h2("3.3 The six-tables question and verdict"));
bodyChildren.push(body(
  "The one substantive thing automata_corrected.tex lacks that its own open-questions queue discusses is the six summary tables (tab:proven-open-1 and -2, tab:schatten-template, tab:oracle-budget-laws, tab:spectral-tail, tab:exponent-vertex-correspondence, roughly 590 lines). Those tables were never in the corrected file: they belong to an older sibling (\u201cglued 6\u201d) that is not present in the repository, so they cannot be restored from the folder under review. The corrected lineage itself chose to present that material as itemized lists, and the current manuscript inherits that choice; the venue decision (a single archival-length paper at a journal without a page cap) does not pressure a change. Verdict: nothing from automata_corrected.tex is worth restoring, either as-is or after modification. The file's residual value is historical and provenance-related, and that role is now served by the pristine copy shipped in supplementary/legacy/ (Task 4)."));

// ================= 4. Task 3 =================
bodyChildren.push(h1("4. Task 3 — Dedicated Sentence-Level Flaw Search"));
bodyChildren.push(h2("4.1 Method"));
bodyChildren.push(body(
  "The search ran in three layers. The first layer was an automated sentence-level scanner written for this purpose: it strips comments, removes inline and display mathematics entirely (including their content), unwraps formatting macros while keeping their text, replaces cross-references and citations with neutral tokens, joins paragraphs across line breaks, and then tests the resulting prose for duplicated words (including duplicates spanning line breaks), double or misplaced punctuation, a curated misspellings list with word boundaries, lowercase sentence starts after genuine sentence endings, capitalization consistency of the coined terms, hyphenation misuse of \u201cright congruence\u201d versus \u201cright-congruence,\u201d unbalanced mathematics delimiters per paragraph, undefined references, citation keys without bibliography entries, and bibliography entries never cited. A first scanner pass produced 758 raw hits; every one was adjudicated by inspection of the source line, the false-positive mechanisms were identified (math-mode commas after inline formulas, \\\\emph lead-ins unwrapped with inserted spaces, list items read as continuations), and a corrected second pass reduced the findings to adjudicable candidates only. The second layer was targeted consistency greps over the raw source: spacing conventions before punctuation inside mathematics, \u201ce.g.\u201d and \u201ci.e.\u201d backslash-space usage, doubled determiners, non-breaking tildes before every \\ref, finite-state and zero-error hyphenation patterns, and the coinage spellings. The third layer was manual line-level reading of the layers least covered by prior passes — the material v6 itself added (the O1/O2/O3 edits), the conclusion, and the availability statement — since the v4 full read and the two proof-check rounds had already covered the theorem-bearing body in depth."));
bodyChildren.push(h2("4.2 Findings"));
bodyChildren.push(body(
  "Exactly two genuine defects surfaced, both minor, both fixed in v7. Everything else the scanners and reads probed came back clean, which is consistent with the four prior review passes this chain has undergone."));
bodyChildren.push(tableCaption("Table 2. Sentence-level findings and dispositions."));
bodyChildren.push(makeTable(
  [cell("Finding", { bold: true, fill: P.surface, w: 34 }), cell("Location (v6)", { bold: true, fill: P.surface, w: 16 }), cell("Disposition", { bold: true, fill: P.surface, w: 50 })],
  [
    [cell("Lowercase \u201cThe price of safety is\u201d in the body of Corollary cor:price-safety \u2014 the only lowercase use of the coinage in running text (22 other occurrences are capitalized).", { w: 34 }), cell("L13283", { w: 16 }), cell("Fixed in v7: capitalized to \u201cThe Price of Safety is\u201d.", { w: 50 })],
    [cell("The Lean remark and the availability statement claim \u201cfifteen\u201d machine-checked statements; the shipped project tracks seventeen declarations and the companion manuscript itself says seventeen. A factual accuracy defect inherited from the shortened copy of the corrected file.", { w: 34 }), cell("L4559, L18043", { w: 16 }), cell("Fixed in v7: seventeen statements across seven modules, axioms named, sources/build/audit stated as shipped (see Section 5).", { w: 50 })],
  ]));
bodyChildren.push(body(
  "The clean inventory, for the record: 504 labels with zero duplicates; 877 references in v7 (873 in v6 plus the four reference anchors inside the two new footnotes) with zero undefined; all 39 bibliography entries cited (the apparent uncited entries of a naive scan are multi-key citations such as \\cite{balle2021,lacroce2024}, which resolve once keys are split on commas); mathematics delimiters balanced in every paragraph; no misspellings from the curated list; no duplicated words in prose (all raw hits were mathematics tokens or macro-wrapping artifacts); \u201ce.g.\u201d and \u201ci.e.\u201d consistently use the backslash-space form; 100 percent of Section and Theorem references use the non-breaking tilde (57 of 57 and 256 of 256 respectively, zero exceptions); the three v6-added edits (O1 forward-reference flags at both corollary sites, the O2 Sylvester qualification at both sites including the d = 11 order-12 Hadamard qualifier, and the O3 verification-suite paragraph) are all present and correctly worded; the conclusion section reads clean at line level; and the v7 compile has exactly nine overfull boxes, identical in count and magnitude to the frozen v6 baseline (worst 12.4 pt, pre-existing), so the two footnotes introduced no new typographic defects. The sentence-case scanner's only two survivors were Dutch particle surnames in the bibliography (de Rooij, van Erven), which are correct as set."));

// ================= 5. Task 4 =================
bodyChildren.push(h1("5. Task 4 — Supplementary and Lean Integration"));
bodyChildren.push(h2("5.1 The package and its integrity"));
bodyChildren.push(body(
  "The folder shorter vsuperseded/ contains, besides the corrected manuscript, supplementary.tar.gz: the complete companion package of the other chat in which the Lean 4 proofs were done. Extraction yields 154 files. The package carries its own SHA-256 manifest (MANIFEST.txt, hash plus byte size per file); all 154 files verify with zero mismatches, so the sources are pristine. The package contains: a Lean 4 Lake project (lean4/BST: seven modules, toolchain pinned at Lean v4.33.0-rc2, Mathlib via the pinned lake manifest, a GitHub CI workflow), a build script (lean4/BUILD.md, about three minutes from a clean machine), an axiom-audit gate (tools/lean_check.py), 120 standalone verification programs (verify/), ten consistency gates (tools/), the companion manuscript (manuscript.tex), and a companion memorandum (open_problems_report.md)."));
bodyChildren.push(h2("5.2 The fifteen-versus-seventeen reconciliation"));
bodyChildren.push(body(
  "The current manuscript's remark \u201cMachine-Checked Fragments\u201d claims fifteen checked statements. The package tells a different story, in three independent voices. The gate's tracked list names exactly seventeen declarations (four in Centring, five in Halving, three in Sandwich, two in Anova, three in Refine), and the gate is written to fail loudly if the sources contain any declaration missing from the list, so seventeen is the number the artifact enforces. The package's outer README says \u201c7 modules, 17 theorems, 0 sorry.\u201d And the companion manuscript.tex — which differs from the repository's automata_corrected.tex in exactly one paragraph, this one — says: \u201cSeventeen statements are checked in total, across seven modules, with no appeal to sorry and no axioms beyond Lean's standard three, namely propositional extensionality, the axiom of choice, and quotient soundness. The sources, a build script and the axiom audit accompany the manuscript as supplementary material.\u201d The repository's \u201cshorter\u201d copy truncated that paragraph to \u201cFifteen statements are checked in total, with no appeal to sorry and no axioms beyond Lean's standard three\u201d, and the unified chain inherited the truncated form. The count of content statements (main results plus the named supporting lemmas the remark enumerates) is fifteen, with the other two declarations being purely technical helpers (halve_iterate is literally Nat.div_le_self; stabilize_absorbing is a generic fixed-point helper), so the old number was not baseless — but the auditable number, the one a reviewer can check by running the gate, is seventeen. v7 adopts the companion manuscript's full wording, and the supplementary README documents the 15-content-plus-2-helpers mapping explicitly so neither number can be misread."));
bodyChildren.push(h2("5.3 What was brought over"));
bodyChildren.push(tableCaption("Table 3. Integration map (companion package to current supplementary package)."));
bodyChildren.push(makeTable(
  [cell("Component", { bold: true, fill: P.surface, w: 30 }), cell("Destination", { bold: true, fill: P.surface, w: 30 }), cell("Status and notes", { bold: true, fill: P.surface, w: 40 })],
  [
    [cell("Lean 4 project lean4/BST (7 modules, 17 declarations, lake files, toolchain, CI)", { w: 30 }), cell("supplementary/lean/BST/", { w: 30 }), cell("Copied verbatim; sources sorry-free by static check; full gate needs the elan toolchain per BUILD.md (not installable in this environment; the gate reports this honestly rather than passing silently).", { w: 40 })],
    [cell("Build script lean4/BUILD.md", { w: 30 }), cell("supplementary/lean/BUILD.md", { w: 30 }), cell("Copied verbatim.", { w: 40 })],
    [cell("Module description lean4/README.md", { w: 30 }), cell("supplementary/lean/MODULES.md", { w: 30 }), cell("Copied verbatim (module-to-manuscript-site table).", { w: 40 })],
    [cell("Axiom-audit gate tools/lean_check.py", { w: 30 }), cell("supplementary/lean/lean_check.py", { w: 30 }), cell("Copied with a path-resolution patch so it resolves both the integrated layout (lean/BST) and the legacy layout (legacy/lean4/BST); run: sources present, sorry-free, honest toolchain-absent report.", { w: 40 })],
    [cell("Statement manifest (was lean/README.md, manifest-only)", { w: 30 }), cell("supplementary/lean/README.md", { w: 30 }), cell("Rewritten: the actual development, the 15/17 reconciliation table, the gate description, the scope statement.", { w: 40 })],
    [cell("Whole pristine package (154 files: 120 programs, 10 gates, manuscript.tex, memorandum, manifest)", { w: 30 }), cell("supplementary/legacy/", { w: 30 }), cell("Copied byte-identical; INTEGRATION_NOTES.md added alongside (provenance, label-lineage caveats, how to run the gates); the tarball remains in shorter vsuperseded/ as well.", { w: 40 })],
    [cell("The v6-era programs, machine tables, outputs (already present)", { w: 30 }), cell("supplementary/programs, machine_tables, outputs", { w: 30 }), cell("Unchanged; they remain the authoritative reproduction path for the manuscript's quoted numbers.", { w: 40 })],
  ]));
bodyChildren.push(h2("5.4 Verification actually run here"));
bodyChildren.push(body(
  "The gates were executed in this environment to confirm the brought-over package is functional, not decorative: regression_all.py reports 681 of 681 assertions present (no fix from the companion lineage's revision history has regressed); traceability.py reports 98 tracked verification programs landed, zero not landed; lossscan.py passes with zero unexplained losses; and a representative verification program, controlled_ib.py, runs to VERIFIED with maximum deviation 1.8e-16 on 4,000 machines — matching the figure its own README quotes. The Lean gate itself runs in its honest degraded mode (the elan toolchain cannot be installed in this environment): it confirms the seven modules are present and statically sorry-free, reports the companion effort's last verified build, and points at BUILD.md for the three-minute full rebuild. Consistent with the user's note that the Lean proofs were completed in the other chat, no Lean content was rewritten, and no compiler verification is claimed here that was not performed here."));
bodyChildren.push(body(
  "The manuscript side of the integration is the re-hardened availability statement of v7: the Lean component now points at the development itself \u2014 the seventeen machine-checked statements in their seven modules, together with the build script and the axiom-audit gate that recompiles the development and verifies every statement against Lean's standard three axioms \u2014 replacing the v6 wording that pointed at a statement manifest documenting fifteen statements."));

// ================= 6. Task 5 =================
bodyChildren.push(h1("6. Task 5 — Open Questions: Which Still Apply"));
bodyChildren.push(body(
  "The queue in shorter vsuperseded/OPEN_QUESTIONS.md (thirteen items, status keys OPEN / DEFERRED / RESOLVED) was written for the corrected lineage. Each item was checked against the current v7 state; the table records the verdict. Ten items are settled by the current state of the manuscript or by decisions already on record; two remain formally open with a recommendation to leave them; one applies partially."));
bodyChildren.push(tableCaption("Table 4. Open-questions status against automata_unified_revised_v7.tex."));
bodyChildren.push(makeTable(
  [cell("Item", { bold: true, fill: P.surface, w: 8 }), cell("Question (short form)", { bold: true, fill: P.surface, w: 34 }), cell("Status against v7", { bold: true, fill: P.surface, w: 36 }), cell("Verdict", { bold: true, fill: P.surface, w: 22 })],
  [
    [cell("Q1", { w: 8 }), cell("\u223c_\u03b4 \u2286 \u223c interaction conflict", { w: 34 }), cell("Resolved in-file and inherited: rem:no-lower-constraint present; the one-sided form with the correct history-factor formulation stands.", { w: 36 }), cell("Settled", { w: 22, color: OK })],
    [cell("Q2", { w: 8 }), cell("Restore the six summary tables?", { w: 34 }), cell("Still open in principle, but not actionable: the tables' source (glued 6) is not in the repository; corrected itself presents the material as itemized lists, which v7 inherits; the venue decision (no page cap) removes the pressure. Recommendation: keep the lists.", { w: 36 }), cell("Open, recommend (b)", { w: 22, color: WARN })],
    [cell("Q3", { w: 8 }), cell("Local Fisher upgrade", { w: 34 }), cell("Resolved: lem:fisher-uniform-expansion and cor:fisher-uniform-remainder are both in the manuscript (the latter carries the O1 forward-reference flag).", { w: 36 }), cell("Settled", { w: 22, color: OK })],
    [cell("Q4", { w: 8 }), cell("Audience / venue", { w: 34 }), cell("Resolved by the coinage/venue decision: single submission, Information and Computation primary, Theory of Computing backup, arXiv preprint first, split only as desk-rejection contingency.", { w: 36 }), cell("Settled", { w: 22, color: OK })],
    [cell("Q5", { w: 8 }), cell("Summary + numerical subsections", { w: 34 }), cell("Resolved by substitution: the computational-conventions remark with its appended verification-suite paragraph, and the conventions cross-referenced at every quoted site, serve the role the glued-6 subsections would have played.", { w: 36 }), cell("Settled (substitution)", { w: 22, color: OK })],
    [cell("Q6", { w: 8 }), cell("Retire \\GrdHank?", { w: 34 }), cell("Resolved: zero occurrences in v7 (split into \\Dunres / \\DHankstr).", { w: 36 }), cell("Settled", { w: 22, color: OK })],
    [cell("Q7", { w: 8 }), cell("prop:active-length-upper: proposition or theorem?", { w: 34 }), cell("Still open, trivial: it remains a proposition in v7, deliberately subordinate to the certified theorem. Recommendation: leave as proposition.", { w: 36 }), cell("Open, recommend (a)", { w: 22, color: WARN })],
    [cell("Q8", { w: 8 }), cell("Hypothesis style; \u201cFor rational data\u201d qualifier", { w: 34 }), cell("Resolved: thm:interaction-complexity opens \u201cFor rational data \u2014 rational predictive means and a rational tolerance \u03b5\u201d; the explicit-hypothesis style is used throughout.", { w: 36 }), cell("Settled", { w: 22, color: OK })],
    [cell("Q9", { w: 8 }), cell("Streaming lower bound", { w: 34 }), cell("Resolved: thm:stream-lower-bound present (transport-plus-readout adversary, \u03a9(M log M) on a never-reset stream).", { w: 36 }), cell("Settled", { w: 22, color: OK })],
    [cell("Q10", { w: 8 }), cell("Make the condensed rewrite the base?", { w: 34 }), cell("Resolved by the venue decision's structure: the full unified manuscript is retained; the condensed form survives as the two-paper split contingency.", { w: 36 }), cell("Settled", { w: 22, color: OK })],
    [cell("Q11", { w: 8 }), cell("Citation density", { w: 34 }), cell("Resolved and re-verified: all 39 bibliography entries (37 + the 2 new disambiguation entries) are cited; no orphans either direction.", { w: 36 }), cell("Settled", { w: 22, color: OK })],
    [cell("Q12", { w: 8 }), cell("Split into a focused retention paper?", { w: 34 }), cell("Resolved by the venue decision (option b: keep unified, revisit after referee reports), with the split-safety analysis (core 38, bridges 25, residual citing in: 68\u201370) preserved as the contingency playbook in the queue file.", { w: 36 }), cell("Settled", { w: 22, color: OK })],
    [cell("Q13a", { w: 8 }), cell("Unifilar machine model misplacement", { w: 34 }), cell("Partially applies: the definitional core (def:unifilar-machine, def:unifilar-lumpable and companions) now sits in Section 3, before all uses \u2014 the inversion is largely fixed. Two forward references from Section 5 to prop:input-driven-specialization (still in Section 9) remain, both roadmap-style. Options: move the proposition too, add a pointer at first use, or leave; recommendation: leave.", { w: 36 }), cell("Partially applies", { w: 22, color: WARN })],
    [cell("Q13b", { w: 8 }), cell("Section balance", { w: 34 }), cell("Inherent to where the mathematics is; the venue decision accepts it. No action.", { w: 36 }), cell("Settled (accepted)", { w: 22, color: OK })],
  ]));
bodyChildren.push(body(
  "Net: the queue contains no blocking item for submission. The two items with residual openness (Q2, Q7) and the partial item (Q13a) are presentation-level judgment calls, each with a recommendation on record; none affects correctness, and none should hold the arXiv preprint or the journal submission."));

// ================= 7. v7 Change Log =================
bodyChildren.push(h1("7. v7 Change Log and Deliverables"));
bodyChildren.push(body(
  "v7 was created from the frozen v6 by six anchored, abort-before-write edits (the edit script verifies the frozen file's md5 before touching anything, and aborts unless every anchor matches exactly once). The manuscript compiles cleanly (tectonic, exit 0, 234 pages, 1.10 MiB, 9 overfull boxes identical to the v6 baseline), and the v7 verification suite passes 23 of 23 checks: v6 byte-unchanged, all six edits present with their old strings absent, 504 labels with zero duplicates, 877 references with zero undefined, environments matched, brace balance zero, all 39 bibliography entries cited, and no stray \u201cfifteen\u201d anywhere."));
bodyChildren.push(tableCaption("Table 5. The six v7 edits."));
bodyChildren.push(makeTable(
  [cell("Edit", { bold: true, fill: P.surface, w: 8 }), cell("Content", { bold: true, fill: P.surface, w: 56 }), cell("Anchor (v6 line)", { bold: true, fill: P.surface, w: 36 })],
  [
    [cell("E1", { w: 8 }), cell("Price of Safety disambiguation footnote at first occurrence, with the corrected citation (arXiv:2309.08709, Shang et al.) and the three-instantiation strengthening.", { w: 56 }), cell("L649, Introduction, surrogate paragraph", { w: 36 })],
    [cell("E2", { w: 8 }), cell("Grounding-gap disambiguation footnote at first occurrence, with the precise two-part NLP-sense description and citation (arXiv:2311.09144, Shaikh et al.).", { w: 56 }), cell("L360, Introduction, symbolic grounding gap sentence", { w: 36 })],
    [cell("E3", { w: 8 }), cell("Lean count correction: seventeen statements, across seven modules, axioms named (propositional extensionality, axiom of choice, quotient soundness), sources/build script/axiom audit stated as shipped.", { w: 56 }), cell("L4559, rem:lean-formalization", { w: 36 })],
    [cell("E4", { w: 8 }), cell("Availability statement re-hardened: the Lean component names the development itself (seventeen statements, seven modules) with the build script and the axiom-audit gate.", { w: 56 }), cell("L18040\u201344, Data and Code Availability", { w: 36 })],
    [cell("E5", { w: 8 }), cell("Capitalization consistency: \u201cThe Price of Safety is\u201d in the body of Corollary cor:price-safety.", { w: 56 }), cell("L13283, Corollary cor:price-safety", { w: 36 })],
    [cell("E6", { w: 8 }), cell("Two bibliography entries: shang2023 (arXiv:2309.08709 [cs.LG], 2023) and shaikh2023grounding (arXiv:2311.09144 [cs.CL], 2023).", { w: 56 }), cell("thebibliography, before \\end{thebibliography}", { w: 36 })],
  ]));
bodyChildren.push(body(
  "Deliverables pushed to the repository with this round: download/automata_unified_revised_v7.tex and .pdf (the new frozen-lineage latest; v6 remains frozen and byte-unchanged); the integrated supplementary package (supplementary/lean/ with the BST project, BUILD.md, MODULES.md, the patched gate and the rewritten README; supplementary/legacy/ with the pristine 154-file companion package and its integration notes; the updated top-level supplementary README); this report (download/v7_revision_report.docx); the updated download/README.md manifest; and the retained scripts (the diff and comparison tooling, the sentence-level scanners, the v7 edit and verification scripts, the report generator). The standing rules were honored throughout: English responses, the version-freeze policy (one new version file per revision, predecessors frozen and verified by checksum), and a commit-and-push of every created document at the end of the round."));

// ================= Assembly =================
const coverConfig = {
  palette: P.cover,
  englishLabel: "REVISION REPORT",
  title: "v7 Revision: Wording Verification, Lineage Restoration Analysis, Sentence-Level Audit, and Lean Integration",
  subtitle: "automata_unified_revised_v7.tex \u2014 companion report to the five-task instruction",
  metaLines: [
    "Manuscript: automata_unified_revised (v7, from frozen v6)",
    "Scope: Tasks 1\u20135 of the 2026-09-02 instruction",
    "Basis: repo at MIKEAA2020/automata-, coinage-search evidence, companion package",
    "Date: 2026-09-02",
  ],
  footerLeft: "automata- repository",
  footerRight: "2026-09-02",
};

const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: { ascii: "Times New Roman", eastAsia: "SimSun" }, size: 22, color: P.body },
        paragraph: { spacing: { line: 312 } },
      },
      heading1: {
        run: { font: HEAD_FONT, size: 32, bold: true, color: P.primary },
        paragraph: { spacing: { before: 360, after: 160, line: 312 } },
      },
      heading2: {
        run: { font: HEAD_FONT, size: 28, bold: true, color: P.primary },
        paragraph: { spacing: { before: 280, after: 120, line: 312 } },
      },
    },
  },
  sections: [
    { // Section 1: Cover (margin 0, no footer)
      properties: {
        page: { size: { width: 11906, height: 16838 }, margin: { top: 0, bottom: 0, left: 0, right: 0 } },
      },
      children: buildCoverR1(coverConfig),
    },
    { // Section 2: TOC (roman numerals)
      properties: {
        type: SectionType.NEXT_PAGE,
        page: {
          size: { width: 11906, height: 16838 },
          margin: { top: 1440, bottom: 1440, left: 1701, right: 1417 },
          pageNumbers: { start: 1, formatType: NumberFormat.UPPER_ROMAN },
        },
      },
      footers: {
        default: new Footer({ children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ children: [PageNumber.CURRENT], size: 18, color: P.secondary, font: EN_FONT })],
        })] }),
      },
      children: [
        new Paragraph({
          spacing: { before: 200, after: 200 },
          children: [new TextRun({ text: "Contents", bold: true, size: 32, color: P.primary, font: HEAD_FONT })],
        }),
        new TableOfContents("Contents", { hyperlink: true, headingStyleRange: "1-2" }),
        new Paragraph({
          spacing: { before: 200 },
          children: [new TextRun({
            text: "Note: open in Word/WPS and right-click the table of contents, then choose Update Field, to refresh page numbers.",
            italics: true, size: 18, color: "8A8A8A", font: EN_FONT })],
        }),
      ],
    },
    { // Section 3: Body (arabic, restart at 1)
      properties: {
        type: SectionType.NEXT_PAGE,
        page: {
          size: { width: 11906, height: 16838 },
          margin: { top: 1440, bottom: 1440, left: 1701, right: 1417 },
          pageNumbers: { start: 1, formatType: NumberFormat.DECIMAL },
        },
      },
      headers: {
        default: new Header({ children: [new Paragraph({
          alignment: AlignmentType.RIGHT,
          border: { bottom: { style: "single", size: 2, color: P.accent, space: 4 } },
          children: [new TextRun({ text: "v7 Revision Report - automata_unified_revised_v7.tex", size: 16, color: P.secondary, font: EN_FONT })],
        })] }),
      },
      footers: {
        default: new Footer({ children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ children: [PageNumber.CURRENT], size: 18, color: P.secondary, font: EN_FONT })],
        })] }),
      },
      children: bodyChildren,
    },
  ],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("/home/z/my-project/automata/download/v7_revision_report.docx", buf);
  console.log("WROTE docx, bytes:", buf.length);
});
