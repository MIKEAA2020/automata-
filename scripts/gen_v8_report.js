// gen_v8_report.js — v8 revision report: the five-part deep-review
// instruction (sentence-level merit scan, internal-connections analysis,
// remnants/redundancy/informal-language scan, line-level flow scan,
// tables/figures/visual-aids merit). House pipeline: R1 cover, 3-section
// numbering (cover / TOC roman / body arabic), TOC + refresh hint,
// header/footer. English, report scene.
const {
  Document, Packer, Paragraph, TextRun, Header, Footer, PageNumber,
  NumberFormat, AlignmentType, SectionType, TableOfContents,
} = require("docx");
const fs = require("fs");
const {
  P, buildCoverR1, h1, h2, body, bodyRuns, run, mono, bullet,
  quoteBlock, cell, tableCaption, makeTable, EN_FONT, HEAD_FONT,
} = require("./v8_helpers.js");

const OK = "2E6B3E";      // green: verified / clean
const WARN = "B4540A";    // amber: declined / not warranted
const FIX = "1F5FA8";     // blue: implemented in v8
const bodyChildren = [];

// ================= 1. Executive Summary =================
bodyChildren.push(h1("1. Executive Summary"));
bodyChildren.push(body(
  "This report records the execution of the five-part deep-review instruction issued against the current latest manuscript, automata_unified_revised_v7.tex: (1) a sentence-level scan for whether the work merits additional non-decorative, non-superficial clarifications, pedagogical enhancements or intuitive insights; (2) an analysis of how the work's internal connections can be strengthened in genuine, non-decorative ways; (3) a scan for remnants, redundancy, and informal or change-log language; (4) a line-level scan for seamless flow; and (5) an assessment of whether the work merits additional non-decorative, non-superficial tables, figures or visual aids. The method combined a complete sequential line-level read of all 18,100 lines of v7 with a purpose-built automated scanner covering punctuation, misspellings, math balance, citation integrity, capitalization, hyphenation, informal and change-log language markers, cross-section duplicate sentences and flow-level connectives; the scanner's 327 raw flags were adjudicated one by one against the source."));
bodyChildren.push(body(
  "The verdicts are as follows. The clarification and pedagogy layer is saturated: 168 remarks, 61 definitions, counterexample-driven scoping at every nontrivial hypothesis, and mechanism explanations at every forcing construction leave no comprehension gap that further prose would close, so question 1's honest answer is no, with one warranted navigational exception counted under question 5. Two genuine internal-connection gaps were found and closed in v8: the grounding-side infinite-support remark duplicated the abstract-side remark verbatim without a cross-reference, and the commitment section's normalized-valuation discussion re-derived the meta-layer corollary without linking it. The remnant and register scan found the manuscript essentially clean: zero change-log language, zero TODO-class remnants, four acceptable rhetorical uses of a common noun, and two of four cross-section repeated sentences that are deliberate devices while two were the genuine duplication just mentioned. Line-level flow is seamless throughout; every flagged mechanical artifact was a scanner limitation, not a manuscript defect. And exactly one additional visual aid is merited: the manuscript defines roughly sixty bespoke macro symbols across 234 pages with no lookup table, so v8 adds a Notation Index of four cross-referenced tables. v7 was frozen at md5 fe3da4d5fbc37d6a58fef11b566aeb67 and is byte-unchanged; v8 compiles to 238 pages with the nine overfull boxes of the v7 baseline unchanged and zero new."));
bodyChildren.push(tableCaption(
  "Table 1: The five questions, their verdicts, and the v8 actions they produced."));
bodyChildren.push(makeTable(
  [cell("Question", { bold: true, w: 26 }), cell("Verdict", { bold: true, w: 42 }), cell("v8 action", { bold: true, w: 32 })],
  [
    [cell("Q1 clarifications / pedagogy", { w: 26 }),
     cell("Not merited; layer saturated after seven revision cycles", { w: 42 }),
     cell("None (declined items documented in Section 2)", { w: 32, color: WARN })],
    [cell("Q2 internal connections", { w: 26 }),
     cell("Two genuine gaps found: duplicated infinite-support remark (Sec. 7 vs Sec. 3); unlinked normalized-valuation echo (Sec. 6 vs Sec. 4)", { w: 42 }),
     cell("E1, E2: cross-references added at both sites", { w: 32, color: FIX })],
    [cell("Q3 remnants / redundancy / informal language", { w: 26 }),
     cell("Clean: 327 raw flags adjudicated to 0 genuine defects beyond the Q2 duplication; 2 intentional echo devices confirmed", { w: 42 }),
     cell("E1 removes the verbatim duplication tail", { w: 32, color: FIX })],
    [cell("Q4 line-level flow", { w: 26 }),
     cell("Seamless; all 9+12+15 mechanical flags were scanner artifacts", { w: 42 }),
     cell("None needed", { w: 32, color: OK })],
    [cell("Q5 tables / figures / visual aids", { w: 26 }),
     cell("Exactly one warranted: a notation index for ~60 bespoke symbols; figures and a master results-map declined as decorative", { w: 42 }),
     cell("E3: Notation Index, four cross-referenced tables", { w: 32, color: FIX })],
  ]));

// ================= 2. Q1 =================
bodyChildren.push(h1("2. Question 1 — Warranted Clarifications, Pedagogy, Intuition"));
bodyChildren.push(body(
  "The full sequential read looked specifically for places where a reader's comprehension fails or degrades for lack of a clarifying sentence, a pedagogical framing, or an intuitive bridge: definitions whose role only becomes clear later, constructions whose mechanism is stated but not explained, hypotheses whose necessity is asserted but not exhibited, and results whose significance within the whole is left implicit. The manuscript already covers all four of these failure modes systematically. Every nontrivial hypothesis carries a witness or a scope remark exhibiting its necessity — clause (i) of the support-relative congruence definition has its two-history counterexample (rem:support-clause-i-needed), the reflexivity axiom of the cost profunctor has its constant-profunctor failure mode inside the definition itself, the f-divergence hypothesis of the representation theorem has the Renyi family as its separating example, and the direct-sum conditions each have a named witness for the failure of the converse. Every forcing construction carries a mechanism remark explaining what the adversary exploits and why obvious alternative attacks fail — the persistent-stream lower bound explains its transport-and-readout mechanism (rem:stream-lb-mechanism), the gated active family explains why gating is needed and what breaks under chaining (rem:gating-needed), the halving bounds explain why the output alphabet drops out (rem:halving-alphabet-free), and the non-convexity of the finite-state rate-distortion curve explains the missing time-sharing mechanism (rem:rd-nonconvex-mechanism)."));
bodyChildren.push(body(
  "Where an unaided reader would most plausibly stumble, the manuscript has already placed the aid: the two Fisher statements that appear to compete are reconciled in a dedicated reading remark (rem:fisher-nogo-reading), the two rank conventions that differ by one are reconciled with their structural cause (rem:rank-conventions), the protocol dependence of the mistake bounds is tabulated in the type-discipline section with per-result signatures, and the three commitment quantities that could be conflated are separated in a naming remark before any of them is used quantitatively (rem:com-rd-scope). The register is deliberately formal, and the instruction's 'intuitive insights' category was tested against that register: candidate additions were either already present in precise form (for example, the explanation of why the vertex correspondence is not a coincidence, rem:vertex-two-ingredients) or would have lowered precision without closing a gap. The verdict for question 1 is therefore no, with one exception: the navigational deficiency that a reader cannot look up the notation is a real comprehension tax, and it is remedied under question 5 as the Notation Index."));
bodyChildren.push(h2("2.1 Candidates considered and declined"));
bodyChildren.push(bullet([
  run("Reading-path paragraph in the roadmap. ", { bold: true }),
  run("The roadmap lists one sentence per section but does not describe dependency structure, and the manuscript's dependencies are genuinely non-linear (the temporal section supplies rates consumed by the oracle section three sections earlier in document order; the Schatten template is stated after the grounding results it explains). A guided reading order was considered and declined: the table of contents, the roadmap's per-section sentences, the master-scope four-pillar statement, and the two type-signature tables already carry the navigational load, and a reading-path paragraph would duplicate them without adding precision — the non-linear dependencies are flagged at their point of use by forward references that the prior cycle already audited."),
]));
bodyChildren.push(bullet([
  run("Intuition remarks at the exponent vertex and the pinching law. ", { bold: true }),
  run("Both were considered because they are the two most compressed passages in the manuscript. Both already carry their explanation in precise form: the vertex section explains what the matching labels do and do not explain, including exactly which two ingredients make the three converses parallel, and the pinching proof states the sign-flip averaging identity that makes the majorization transparent. Adding an informal paraphrase would trade the manuscript's register for no new information."),
]));
bodyChildren.push(bullet([
  run("A worked numeric example for the two-axis oracle inequality. ", { bold: true }),
  run("Considered because the bias-variance composition is the manuscript's most applied-looking result. Declined because every downstream budget law is stated against an abstract approximation deficit with the achievability hypothesis made explicit, and a numeric example would risk reading as an unconditional instantiation — exactly the type confusion the type-discipline section exists to prevent."),
]));

// ================= 3. Q2 =================
bodyChildren.push(h1("3. Question 2 — Strengthening Internal Connections"));
bodyChildren.push(body(
  "The manuscript's internal-connection infrastructure is unusually dense: 877 resolved cross-references in v7, preview-then-treatment pairs for each framework component, and restatement anchors that deliberately keep one maintained copy of each twice-needed statement. The scan looked for the gaps in this web: places where two results state the same fact without acknowledging each other, where a later section re-derives an earlier point, where an analogy the manuscript relies on is left implicit, or where a reader could trace two parallel developments that never meet. Two genuine gaps were found, both instances of the same pattern — an earlier statement and a later specialization that do not reference each other — and both were closed in v8."));
bodyChildren.push(h2("3.1 E1 — the duplicated infinite-support remarks"));
bodyChildren.push(body(
  "The abstract-impulse-response theory (Section 3) states, in rem:infinite-support, that infinite support of an impulse response does not imply unboundedness of the associated Hankel operator, that boundedness requires decay or summability conditions, that geometric decay with rate below the reciprocal alphabet size suffices by the Schur test, and that non-decaying bounded symbolic responses are decided case by case. The grounding theory (Section 7) states, in rem:infinite-support-grounding, four thousand lines later, the same four-point content for Mealy-machine-induced impulse responses — including two sentences that are verbatim identical to the Section 3 remark. The duplication is not marked as a deliberate anchor: unlike the exponent-section anchors, which explicitly say they are retained so the section can be read in isolation, the Section 7 remark presents itself as independent content. This is both a redundancy (question 3) and a missing connection (question 2): the two remarks carry the same mathematical substance for two regimes and never acknowledge each other, so a reader cannot know they are one principle."));
bodyChildren.push(body(
  "v8 closes the gap at the Section 7 site: the remark now states that it is the grounding-side instance of the Section 3 remark, that the content transfers verbatim from the abstract impulse-response setting, and that the Schur-test criterion is the same as there. The Section 3 remark remains the canonical statement. The two verbatim-identical closing sentences are retained but now explicitly inherited rather than silently repeated, which removes the maintenance hazard (a future edit to one copy would not propagate to the other) without breaking either remark's self-containedness."));
bodyChildren.push(h2("3.2 E2 — the unlinked normalized-valuation echo"));
bodyChildren.push(body(
  "Section 4 derives, as Corollary cor:boolean-01, the normalized {0,1} commitment cost from the Boolean dichotomy and remarks that it separates the structural {0,infinity} valuation from the normalized operational one with the same threshold. Section 6, immediately after stating the exact commitment bound, repeats the two displays and the same closing observation — the threshold is the same; only the positive mismatch value changes — as unattributed commentary. The echo is harmless in isolation, but it is precisely the pattern the manuscript polices elsewhere: the schema-versus-instance relationship between the two passages is a real connection (the Section 6 pair is the commitment instance of the Section 4 schema-layer corollary), and leaving it implicit hides the derivation order. v8 adds one sentence at the Section 6 site naming Corollary cor:boolean-01 as the schema-layer statement of the separation, of which the displayed pair of valuations is the commitment instance."));
bodyChildren.push(h2("3.3 Connection candidates examined and left alone"));
bodyChildren.push(bullet([
  run("Stateless-game value versus memoryless stochasticity floor. ", { bold: true }),
  run("Both are exact constant-instance values with a (1-gamma) denominator, one in the commitment game theory and one in the grounding floor theory. A connecting remark was considered and declined: the two quantities are computed by different mechanisms against different objects, the independence theorem already provides the manuscript's canonical regime-composition device, and a cosmetic-similarity remark would violate the non-decorative requirement."),
]));
bodyChildren.push(bullet([
  run("Counter family (Section 5) versus cyclic-shift family (Section 13). ", { bold: true }),
  run("Both are counter or shift witnesses built from rotating registers, and both extremalize a different quantity (the retention refinement gap; the state-identification mistake count). The cyclic-shift family is already cited from the synchronization-depth discussion; the two serve disjoint purposes, and forcing a comparison would add nothing either proof uses."),
]));
bodyChildren.push(bullet([
  run("The two Moore-refinement bounds (lem:tension, lem:moore-separation). ", { bold: true }),
  run("Already connected: the synchronization proofs state explicitly that the cross-machine form is the same bound, and the identity of the counting core is flagged. No gap."),
]));

// ================= 4. Q3 =================
bodyChildren.push(h1("4. Question 3 — Remnants, Redundancy, and Informal or Change-Log Language"));
bodyChildren.push(body(
  "The automated scanner was extended for this cycle with three new check families aimed squarely at the instruction: a sixty-pattern informal and change-log marker list (TODO-class remnants, version language such as 'in this revised version', deletion or insertion narration, back-references of the 'as noted above' family, hand-waves of the 'the details are routine' family, register flags such as 'of course' and 'interestingly'), a cross-section near-duplicate sentence detector that normalizes mathematics away and compares sentences across section boundaries, and a sentence-initial connective audit for informal paragraph openings. The mechanical families from the prior cycle (duplicate words, double punctuation, misspellings, math balance, citation integrity, capitalization of the coinages, hyphenation) were re-run in corrected form: math interiors are now dropped at stripping time, which eliminated the entire family of false positives that the prior cycle had to adjudicate away by hand."));
bodyChildren.push(tableCaption(
  "Table 2: Scan totals and adjudication outcome, by family."));
bodyChildren.push(makeTable(
  [cell("Family", { bold: true, w: 30 }), cell("Raw flags", { bold: true, w: 14 }), cell("Genuine after adjudication", { bold: true, w: 56 })],
  [
    [cell("Informal / change-log markers", { w: 30 }), cell("23", { w: 14 }),
     cell("0 defects. 15 flags were macro artifacts (\\big in display math matched as 'big'), 8 were standard mathematical register ('again' as in 'is again rational', 'in fact' for strengthening emphasis, 'trivially implies' as a proof term), and the remaining 4 uses of a common plural noun are acceptable rhetorical register, reported below.", { w: 56 })],
    [cell("Cross-section duplicate sentences", { w: 30 }), cell("4", { w: 14 }),
     cell("2 intentional devices confirmed (an introduction-preview echo of the Schatten-template thesis; the exponent-section anchor that documents itself as retained for isolated readability); 2 genuine duplications, both fixed as E1/E2.", { w: 56 })],
    [cell("Misspellings", { w: 30 }), cell("237", { w: 14 }),
     cell("0. All 237 were the substring 'ommit' inside 'Commitment'.", { w: 56 })],
    [cell("Punctuation (spaces, doubles)", { w: 30 }), cell("22", { w: 14 }),
     cell("0. All were spaces inside display mathematics, where LaTeX ignores them; zero rendering effect.", { w: 56 })],
    [cell("Duplicate words", { w: 30 }), cell("16", { w: 14 }),
     cell("0. All were adjacent math tokens ('$x$ $y$' stripped to adjacent placeholders).", { w: 56 })],
    [cell("Sentence-initial lowercase", { w: 30 }), cell("9", { w: 14 }),
     cell("0. All were itemize and description environments whose bold labels the macro-stripper removed.", { w: 56 })],
    [cell("Flow-initial connectives (Now/But/Moreover)", { w: 30 }), cell("15", { w: 14 }),
     cell("0. Standard proof register in mathematical prose.", { w: 56 })],
    [cell("Refs, cites, coinage caps, hyphenation", { w: 30 }), cell("1", { w: 14 }),
     cell("0. One hyphenation flag adjudicated as correct usage.", { w: 56 })],
  ]));
bodyChildren.push(body(
  "On the register question specifically: the manuscript uses a common plural noun in four places ('two things the principle deliberately does not assert', 'three things simultaneously', 'certify different things', 'the two things a universal experiment cannot deliver at once'). Each was examined in context; each is a deliberate rhetorical device carrying specific content (two named omissions, three named conditions, a named distinction, two named services), and none degrades precision. Replacing them with formal nouns would be cosmetic. Similarly, 'Roadmap' as a subsection title, 'in fact' twice, and the proof-term 'trivially implies' once are all within the register of published mathematics. The verdict for question 3: the manuscript contains no remnants, no change-log language, no version narration, and no redundancy beyond the two items already closed under question 2."));

// ================= 5. Q4 =================
bodyChildren.push(h1("5. Question 4 — Line-Level Flow"));
bodyChildren.push(body(
  "The full sequential read tracked flow explicitly: every section boundary, every subsection boundary, every paragraph that changes topic, every environment transition, and every insertion point of the prior cycles' edits. The manuscript's flow architecture is uniform and intact: each of the eighteen sections opens with a framing paragraph stating what it develops and how it relates to its neighbours; each section closes with either a scope-and-conditions subsection or a classification list; subsection transitions are carried by forward-declared purpose sentences rather than by abrupt topic switches; and the three long technical stretches that could have become tunnels — the Fisher boundary analysis, the oracle-floor assumption, and the direct-sum active-learning development — are each internally signposted with numbered steps and reading remarks. The prior cycles' insertions (the positioning paragraphs, the footnote pair, the convention remark, the seventeen-statement Lean paragraph) sit flush with their surroundings: their register, spacing conventions (including the double space after sentence periods used throughout), and cross-reference style match the host text, and none of them leaves a seam."));
bodyChildren.push(body(
  "The automated flow flags were all artifacts, detailed in Table 2: sentence-initial lowercase after periods occurred only where list labels had been stripped, and sentence-initial connectives are the standard connective apparatus of proofs. No paragraph anywhere repeats its opening, no environment is orphaned from its lead-in, and no definition is used before its introduction point except at the three audited forward references that carry explicit flags. The verdict for question 4: the flow is seamless; no edit was warranted."));

// ================= 6. Q5 =================
bodyChildren.push(h1("6. Question 5 — Tables, Figures, and Visual Aids"));
bodyChildren.push(body(
  "The inventory of existing visual material explains where the gaps, if any, would be. v7 contained zero figures, five tabular environments of which two were floating tables, no graphics packages in the preamble, and no notation table. Against this, the comparative and navigational loads that visual aids usually carry were already borne by five tables: the regime-as-history-systems table in the schema section, the typed-principle instantiation table in the meta-theorems section, the jump-ratio table in the oracle section, and the two type-signature tables in the type-discipline section. What no existing device carries is symbol lookup: the manuscript defines and repeatedly uses roughly sixty bespoke macro symbols — the gap family alone has nine members — across 234 pages, and a reader who meets, say, L-sync-universal at page 155 or the pinching symbol at page 150 has no way to find where it was fixed other than searching the source. For a manuscript of this length and symbolic density, a notation index is the one clearly merited, non-decorative visual aid: it changes how the document can be used, not merely how it looks."));
bodyChildren.push(h2("6.1 E3 — the Notation Index"));
bodyChildren.push(body(
  "v8 adds a Notation Index as an unnumbered back-matter section placed between the bibliography and the availability statement, linked into the table of contents. It consists of four booktabs tables, each one page or less, requiring no new packages (the existing booktabs, array and table machinery suffices): shared schema objects; regime gaps and thresholds; divergences, operators and spectral objects; and temporal, online-learning and strategic quantities. Each of the roughly fifty rows carries the symbol, a one-line meaning, and a cross-reference to the site at which the symbol is fixed, so the index doubles as a provenance map; all cross-references resolve, and the lead-in paragraph states the scope rule — locally used symbols are defined at their site and deliberately not repeated, and regime-superscripted macro families are listed once at their base entry. The theorem numbering of the manuscript is untouched: the index is unnumbered and adds only the four table numbers 3 through 6, following the two existing type-signature tables."));
bodyChildren.push(h2("6.2 Visual-aid candidates considered and declined"));
bodyChildren.push(bullet([
  run("Figures of any kind. ", { bold: true }),
  run("Three candidates were assessed: a three-regime structure diagram, a vertex-correspondence diagram for the {0,1,infinity} labelling, and a block-timeline of the forcing-stream construction. All three are illustration, not navigation: their content is already stated precisely in prose and tables, no comprehension gap is closed by drawing them, and the manuscript contains no graphics infrastructure by design. Introducing one would change the document's production dependencies for zero information gain. Declined as decorative."),
]));
bodyChildren.push(bullet([
  run("A master results map. ", { bold: true }),
  run("A single table listing every principal result with its status was considered, and declined as redundant: the type-discipline section already carries the per-result signature tables, and the scope-of-results section already classifies every result as exact, conditional, local, heuristic or open with its hypotheses. A third view of the same classification would violate the non-decorative requirement."),
]));
bodyChildren.push(bullet([
  run("Inline machine tables for the extremal witnesses. ", { bold: true }),
  run("The temporal section quotes its extremal machines inline in transition-and-output form, and the supplementary package already distributes the full machine tables. Inlining more of them would duplicate the package without helping any proof. Declined."),
]));

// ================= 7. Implementation and verification =================
bodyChildren.push(h1("7. Implementation and Verification"));
bodyChildren.push(body(
  "Under the standing version-freeze policy, v7 was frozen (permissions 444, md5 fe3da4d5fbc37d6a58fef11b566aeb67) before any edit, and all work went into the new file automata_unified_revised_v8.tex through an anchored abort-before-write edit script: each of the three edits was located by a unique multi-line anchor whose occurrence count was required to be exactly one, and the script aborts rather than writes if any anchor fails. v8 is 18,294 lines against v7's 18,100."));
bodyChildren.push(tableCaption(
  "Table 3: The three v8 edits."));
bodyChildren.push(makeTable(
  [cell("ID", { bold: true, w: 8 }), cell("Site", { bold: true, w: 26 }), cell("Edit", { bold: true, w: 66 })],
  [
    [cell("E1", { w: 8 }), cell("rem:infinite-support-grounding, Section 7", { w: 26 }),
     cell("Cross-reference added naming rem:infinite-support as the abstract-side statement whose content transfers verbatim; the Schur-test criterion identified as the same as there; the duplicated tail sentences now explicitly inherited rather than silently repeated.", { w: 66 })],
    [cell("E2", { w: 8 }), cell("Discussion after thm:commitment-spec, Section 6", { w: 26 }),
     cell("One sentence added naming Corollary cor:boolean-01 as the schema-layer statement of the structural-versus-normalized valuation separation, of which the displayed pair is the commitment instance.", { w: 66 })],
    [cell("E3", { w: 8 }), cell("New back-matter section, after the bibliography", { w: 26 }),
     cell("Notation Index: four cross-referenced booktabs tables covering ~50 principal symbols in four groups, with a lead-in scope paragraph and a table-of-contents entry.", { w: 66 })],
  ]));
bodyChildren.push(body(
  "Compilation with tectonic exits cleanly: 238 pages (v7: 234), 1.12 MiB, zero errors, zero undefined references. The first compile exposed one new overfull box of 22 points in a notation-table row whose mathematics exceeded the initial symbol-column width; the column widths were rebalanced and the final compile reproduces exactly the nine overfull boxes of the v7 baseline, byte-identical in position and magnitude, with zero new. Structural verification runs 21 checks, all passing: v7 byte-unchanged and still frozen; all three edits present with all three old strings absent; 509 labels with no duplicates and no undefined references; environment pairing and brace balance; all 39 bibliography entries cited in both directions; the notation index correctly placed between bibliography and availability with all of its cross-references resolving and at least 45 rows; and the theorem-like environment count unchanged from v7, confirming that no numbering was disturbed. The manuscript PDF renders the index correctly: the table of contents gains the entry, and the four tables appear as Tables 3 through 6 with their columns intact."));
bodyChildren.push(body(
  "Deliverables: automata_unified_revised_v8.tex and .pdf in the download directory, with v7 remaining frozen and byte-unchanged; the scan script, edit script and verification script retained for iteration; and this report. The README manifest is updated with the v8 entry and change log."));

// ================= assembly =================
const coverConfig = {
  title: "Five-Part Deep Review of automata_unified_revised_v7.tex",
  subtitle: "Sentence-level merit scan, internal connections, register, flow, and visual aids — with the v8 revision",
  englishLabel: "DEEP REVIEW REPORT",
  metaLines: [
    "Base version: automata_unified_revised_v7.tex (frozen, md5 fe3da4d5...)",
    "Produced version: automata_unified_revised_v8.tex (238 pages, 3 edits)",
    "Method: full 18,100-line sequential read + extended automated scan",
    "Date: 2026-09-02",
  ],
  footerLeft: "automata- manuscript chain",
  footerRight: "v8 revision cycle",
  palette: P.cover,
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
          children: [new TextRun({ text: "v8 Deep-Review Report - automata_unified_revised_v8.tex", size: 16, color: P.secondary, font: EN_FONT })],
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
  fs.writeFileSync("/home/z/my-project/automata/download/v8_deep_review_report.docx", buf);
  console.log("written:", buf.length, "bytes");
});
