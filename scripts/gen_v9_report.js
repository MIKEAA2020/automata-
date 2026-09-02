// gen_v9_report.js — v9 decision report: the three delegated editorial
// decisions (Q13a block relocation, the arXiv 2608.12791 citation decision,
// and the Q12 single-publication-versus-split assessment), each actioned or
// recorded in automata_unified_revised_v9.tex. House pipeline: R1 cover,
// 3-section numbering (cover / TOC roman / body arabic), TOC + refresh hint,
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
const WARN = "B4540A";    // amber: declined / contingent
const FIX = "1F5FA8";     // blue: implemented in v9
const bodyChildren = [];

// ================= 1. Executive Summary =================
bodyChildren.push(h1("1. Executive Summary"));
bodyChildren.push(body(
  "This report records the execution of the three-part decision instruction issued against the current latest manuscript, automata_unified_revised_v8.tex: (1) address question Q13a of the open-questions ledger, the measured misplacement of the unifilar machine-model block relative to the theory that depends on it; (2) decide whether to cite arXiv 2608.12791, the thermodynamics-of-learning work that the coinage search had flagged as a same-phrase, different-sense near-collision on the term 'retention gap'; and (3) assess whether the paper is coherent enough to merit single publication, or should be split along the boundary proposed in question Q12. Each decision was delegated to this session, and each has been made, actioned where action was warranted, and recorded in the ledger file."));
bodyChildren.push(body(
  "The outcomes are as follows. Q13a is resolved by its option (a): the five-environment block comprising rem:unifilar-feasibility, prop:unifilar-lumpability, rem:unifilar-converse-hypothesis, prop:input-driven-specialization, and rem:epsilon-machine-relation has been moved from Section 9, where it had been left as a scope note and then stranded by the growth of dependent theory elsewhere, to Section 3's Stationary Controlled Causal Machines subsection, where the other four machine-model environments already live; the full nine-environment model apparatus now precedes the unifilar retention theory by roughly 2,500 lines instead of following it by 3,622. The arXiv 2608.12791 decision is to cite: the work's identity was verified against the live arXiv record, and a disambiguation footnote now stands at the first body occurrence of 'retention gap' in the Introduction, with a matching bibliography entry, following exactly the pattern already established for 'Price of Safety' and 'grounding gap'. And the Q12 assessment concludes that the paper is coherent enough to merit single publication: the proposed split boundary cuts through the retention theory rather than around it, the two papers it would produce are a technical core and its framing rather than two independent contributions, and the length objection is already absorbed by the venue decision. All changes live in the new version file automata_unified_revised_v9.tex; v8 was frozen before any edit and is byte-unchanged at md5 39c1b519e626841235be0fe5676020ca."));
bodyChildren.push(tableCaption(
  "Table 1: The three decisions, their verdicts, and the v9 actions they produced."));
bodyChildren.push(makeTable(
  [cell("Decision", { bold: true, w: 26 }), cell("Verdict and grounds", { bold: true, w: 44 }), cell("v9 action", { bold: true, w: 30 })],
  [
    [cell("Q13a unifilar machine-model placement", { w: 26 }),
     cell("Genuine ordering inversion, not taste: the theory preceded its own machine model by 3,622 lines, and 11 of the 36 body forward references longer than 2,000 lines point into the stranded block; the simulated repair predicted a clean move with only two benign residuals", { w: 44 }),
     cell("E1: block moved to Section 3, after ex:onestep-not-congruence, before the Full-KL Retention Gap subsection", { w: 30, color: FIX })],
    [cell("Cite arXiv 2608.12791?", { w: 26 }),
     cell("Cite. Contemporaneous neighbor in spirit (typed accounting for finite-state devices) and stranger in substance; the shared phrase 'retention gap' carries unrelated senses; citing with a disambiguation footnote pre-empts referee confusion and protects the coinage", { w: 44 }),
     cell("E2 footnote at first body occurrence + E3 bibitem sudo2026 (39 to 40 entries, all cited)", { w: 30, color: FIX })],
    [cell("Q12 single publication or split", { w: 26 }),
     cell("Keep unified. The extraction boundary requires 25 bridge items and leaves 70 residual-to-core back-references; every unification result sits in the residual; coherence evidence is strong; the venue decision already absorbs length", { w: 44 }),
     cell("No content moved; decision and grounds recorded in the ledger; split remains a desk-rejection contingency", { w: 30, color: WARN })],
  ]));

// ================= 2. Decision 1: Q13a =================
bodyChildren.push(h1("2. Decision 1 — Q13a: Relocating the Unifilar Machine-Model Block"));
bodyChildren.push(h2("2.1 The finding"));
bodyChildren.push(body(
  "The structural scan recorded in the open-questions ledger found exactly one genuine ordering inversion in the manuscript, and Q13a named it. The unifilar machine model — the definitions and their immediate scoping apparatus — sat in Section 9, The Two-Axis Oracle Inequality, inside the subsection Type-Correct Axes on One Clock, at lines 8592 through 8880 of the version then current. The unifilar theory built on that model — the controlled full-KL retention gap, the controlled information-bottleneck identity, the zero-retention characterization, and the refinement-extremality proposition — sat in Section 5, Retention, thousands of lines earlier. The theory therefore preceded its own machine model, and every use of the model in that theory was a forward reference. The ledger's measurement made the defect precise: of the 36 body forward references spanning more than 2,000 lines, 11 point into this single block, making it the largest concentrated contributor; the block landed in Section 9 because it was introduced there as a terminology scope note, and the dependent theory then grew elsewhere around it."));
bodyChildren.push(body(
  "In the v8 source the same inversion persists with the block at lines 9515 through 9685 and the receiving theory at the unifilar-retention subsection of Section 5 at line 4703 and following: 4,868 lines of separation, with the four foundational environments (the machine definition, the proper-subclass remark, the unifilar-lumpable definition, and the support remark) already resident in Section 3's Stationary Controlled Causal Machines subsection, split off from their five displaced companions. The simulated repair recorded in the ledger — move the block to immediately before the unifilar retention material — predicted that total forward references fall from 197 to 194, that only two residual dependencies remain (rem:complexity-transfer and the retention-complexity subsection pointer), and that both residuals are benign roadmap-style references. The modest headline reduction was itself informative: most forward references are short-range or come from the Introduction and Schema, where signposting is normal; the defect was concentrated, not diffuse, which is exactly the profile that a surgical move fixes cleanly."));
bodyChildren.push(h2("2.2 The choice and the repair as implemented"));
bodyChildren.push(body(
  "Of the three recorded options — move the block, leave it with an explicit pointer at first use, or leave it as is — option (a) was selected and implemented, with the insertion point adapted to the current structure: the ledger's phrasing targeted Section 5, but in v8 the four foundational machine-model environments already live in Section 3, so uniting all nine there is the strictly stronger repair, completing the machine-model subsection where it begins rather than splitting the apparatus across two homes. The move is a pure cut-and-paste of 171 lines (8,953 characters) carrying five environments, placed immediately after Example ex:onestep-not-congruence — the example that exhibits why one-step predictive equivalence fails to be a congruence, and therefore the natural last exhibit of the model's definition layer — and immediately before the Full-KL Retention Gap subsection, which opens the theory that consumes the model. The Section 9 seam left behind is clean: the non-convexity mechanism remark now runs directly into the finite-horizon approximation-deficit definition with no dangling references, and the two residual dependencies the simulation predicted are exactly the two that remain, both ordinary pointers."));
bodyChildren.push(body(
  "The effect on the reader is the point of the repair. A reader who reaches the unifilar retention theory in Section 5 now meets a machine model that was fully defined, scoped, and exemplified roughly 2,500 lines earlier, in the same subsection run as the lumpability machinery the model generalizes; the eleven long forward references that used to reach 3,600-plus lines forward into an oracle-inequality section now resolve backward or locally. The block's own internal cross-references (to the lumpable-quotient definition, the controlled-Markov subclass, the lumpability proposition) all point backward after the move, which was verified mechanically: every one of the fifty-nine references that cross the moved region's boundaries was checked for direction after the edit. No numbering changed anywhere — the move carries environments, not creates them, so theorem numbering, table numbering, and the notation index are untouched."));

// ================= 3. Decision 2: arXiv 2608.12791 =================
bodyChildren.push(h1("3. Decision 2 — Citing arXiv 2608.12791"));
bodyChildren.push(h2("3.1 What the work is, verified"));
bodyChildren.push(body(
  "arXiv 2608.12791 is 'Thermodynamics of Learning: A Typed Four-Component Accounting of Memory, Fit, and Value' by Akihito Sudo, posted in August 2026, primary class cond-mat.stat-mech with cross-lists in cs.IT and cs.LG. Its identity was verified against the live arXiv record before anything was inserted into the manuscript: the author name, the title, the primary subject class, and the year all match the bibliography entry as written, and the entry follows the manuscript's established arXiv format (sentence-case title rendering, comma inside the closing quotes, initials-form author). The work develops a typed accounting for finite-state learning devices that separates four components: a training-side fit functional, a record-correlation stock, an update-side search ledger, and an operational capital value defined as the work gap between an informed protocol class and a blind class; it proves separation results showing that record correlation and capital gain can diverge, and it studies value retention under task-distribution shift through two quantities it names the retention gap and the retention ratio."));
bodyChildren.push(h2("3.2 The collision and the treatment"));
bodyChildren.push(body(
  "The coinage search had flagged this work as the only arXiv-level near-collision on the phrase 'retention gap', and had classified it monitor-only at the time, because the phrase collision is same-phrase, different-sense: this manuscript's retention gap is the state-compression cost — the stationary Kullback-Leibler price of lumping predictive states into at most M blocks, instantiated as the full-KL gap, its controlled relative, and the quadratic surrogate — while the thermodynamics-of-learning retention gap is a value-side quantity for finite-state learning devices under task-distribution shift, carrying no sign constraint by construction. The two senses are not merely different; they live in different layers of the accounting, one measuring compression cost and one measuring capital change, so there is no mathematical interaction to cite. What there is, is a referee risk: a reader who knows the Sudo work and meets this manuscript's unhyphenated 'retention gap' coinage could suspect unawareness rather than independence, and the cost of removing that suspicion is one footnote."));
bodyChildren.push(body(
  "The decision is to cite, and the treatment follows the exact pattern the manuscript already established twice: the Price of Safety footnote citing arXiv 2309.08709, and the grounding-gap footnote citing arXiv 2311.09144. A disambiguation footnote now stands at the first body occurrence of the phrase, in the Introduction's sentence opening the full-KL retention gap display. The footnote fixes this manuscript's sense by naming all three instantiating definitions — the full-KL gap of the retention definition, the controlled relative of the controlled full-KL definition, and the quadratic surrogate of the Gaussian-quadratic definition — and then states flatly that the phrase is unrelated to the same phrase in the thermodynamics-of-learning literature, where it denotes the value-side quantity for finite-state learning devices under task-distribution shift, with the citation attached. The bibliography grows from 39 to 40 entries, every entry remains cited, and the new entry is cited exactly once, from the footnote."));
bodyChildren.push(h2("3.3 Why cite rather than monitor"));
bodyChildren.push(body(
  "The monitor-only option was the recorded default in the submission notes, and it deserved its hearing. Against it stand three considerations. First, the precedent is now a family: with two coinage collisions already handled by cite-and-disambiguate footnotes, a third collision handled by silence would be an inconsistency a careful referee could notice. Second, the two works are genuine contemporaneous neighbors in spirit — both perform typed accounting of information-theoretic quantities for finite-state devices — so the citation is honest scholarship rather than defensive decoration; it tells the reader that the neighboring framework exists and where the boundary runs. Third, the asymmetry of costs: the footnote costs one paragraph of back matter and zero risk, while silence costs nothing only in the world where no referee knows the Sudo paper, and something in every other world. The submission-notes line recording 'not cited by default' is superseded by this decision, and the ledger records the resolution as a new settled entry."));

// ================= 4. Decision 3: Q12 =================
bodyChildren.push(h1("4. Decision 3 — Q12: Single Publication or Split"));
bodyChildren.push(h2("4.1 What the split would have to carry"));
bodyChildren.push(body(
  "The audit's split proposal, recorded as Q12, would extract a focused retention paper — Finite-State Information Bottlenecks: Spectral Converses, Sharp Global Bounds, and Computational Hardness — around seven named core results, and relegate the categorical schema, the grounding and AAK material, the commitment games, the online oracle theory, the active-learning theory, and the Price of Safety to a second, framing paper. The split-safety analysis already computed what that boundary actually requires. The seven named results close under cross-references to a 38-item core, but definitional dependencies in prose raise the required bridges from 8 to 25: the machine model, the feasible-set definition, and the two k-means lemmas must travel with the extracted paper or its statements do not typecheck. In the other direction, 68 residual items cite into the core in the version measured (70 after the later audits), so the second paper would lean on the first through seventy cross-paper references. Coverage under core-plus-residual remains complete, so no content is lost — but the condition to enforce is substantial: 25 bridges carried, 70 back-references converted to citations."));
bodyChildren.push(h2("4.2 Why the boundary fails as a split"));
bodyChildren.push(body(
  "The third audit's bearing on Q12 is decisive and was recorded in the ledger: every result the unification rests on — the typed rate-distortion metatheorem, the unified theorem, the response definition, the independence theorem, the Schatten no-go, the state-rate definition, the non-convexity proposition, and the vertex two-ingredients remark — lies in the residual, not the core. The extracted retention paper would therefore contain none of the unification apparatus, while the residual paper would retain all of it and simultaneously depend on 70 core results for its retention instance. The two papers would not be independent contributions; they would be a technical core and its framing, separated, each weakened: the core paper stripped of the reason its questions are interesting, the framing paper stripped of the results that answer them. Notably, the whole unifilar layer — which this session's Q13a repair just consolidated — depends on core results, so the proposed boundary cuts through the retention theory rather than around it. That is an argument against splitting on this boundary, and the analysis found no alternative boundary with a better profile."));
bodyChildren.push(h2("4.3 The coherence evidence"));
bodyChildren.push(body(
  "Coherence is not merely the absence of a good split; the manuscript shows positive structure that a split would break. The architecture is uniform across all eighteen sections: a schema layer fixes the typed accounting once, each regime section instantiates it, and the type-discipline section governs every statement's hypothesis discipline — one spine, many instantiations, and the cross-reference web (over 900 resolved references) is the spine's connective tissue. The audits corroborate: zero duplicate labels, every repeated environment title cross-referenced, the five-part review's flow verdict 'seamless', the 327-flag register scan adjudicated to zero genuine defects, and the section-balance finding of Q13b — that the retention and temporal sections are each roughly four times the median section — is a consequence of where the mathematics actually is, matched by the depth asymmetry the audits already noted, not evidence of disorder. The length objection, 239 pages, is real but already absorbed: Information and Computation accepts papers of this length, and the arXiv preprint establishes priority for the multiletter-AAK theorem regardless of journal page economics."));
bodyChildren.push(body(
  "The verdict is option (b): keep the unified manuscript, revisit only after referee reports. The split remains exactly what the venue decision already made it — a desk-rejection contingency — with option (c), moving the six named areas to appendices, as the intermediate fallback if a referee finds the unified body unwieldy but the mathematics sound. No content was moved for Q12 in this cycle, and the decision with its grounds is recorded in the ledger file."));

// ================= 5. Implementation and verification =================
bodyChildren.push(h1("5. Implementation and Verification"));
bodyChildren.push(body(
  "Under the standing version-freeze policy, v8 was frozen (permissions 444, md5 39c1b519e626841235be0fe5676020ca) and a byte-identical v9 copy created before any edit; all work went into automata_unified_revised_v9.tex through the anchored abort-before-write edit script retained at scripts/apply_v9_fixes.py. Each edit was located by unique multi-line anchors whose occurrence counts were required to be exactly one; the script's first run aborted cleanly on a bibliography anchor whose closing-quote comma placement followed a different convention than the anchor assumed, the anchor was corrected to the manuscript's comma-inside convention, and the second run applied all three edits atomically. v9 is 18,299 lines against v8's 18,293: 171 lines relocated, one line carrying the footnote, six lines of bibliography added."));
bodyChildren.push(tableCaption(
  "Table 2: The three v9 edits."));
bodyChildren.push(makeTable(
  [cell("ID", { bold: true, w: 8 }), cell("Site", { bold: true, w: 30 }), cell("Edit", { bold: true, w: 62 })],
  [
    [cell("E1", { w: 8 }), cell("Section 9 to Section 3, after ex:onestep-not-congruence", { w: 30 }),
     cell("Five-environment unifilar machine-model block (171 lines) relocated to complete the Stationary Controlled Causal Machines model run; the Section 9 seam closes to remark-then-definition with no dangling references.", { w: 62 })],
    [cell("E2", { w: 8 }), cell("Introduction, first body occurrence of the phrase", { w: 30 }),
     cell("Disambiguation footnote fixing the manuscript's state-compression sense of 'retention gap' (three named instantiating definitions) against the thermodynamics-of-learning value-side sense, citing the new entry.", { w: 62 })],
    [cell("E3", { w: 8 }), cell("Bibliography, final position", { w: 30 }),
     cell("New entry sudo2026: A. Sudo, 'Thermodynamics of learning: a typed four-component accounting of memory, fit, and value,' arXiv:2608.12791 [cond-mat.stat-mech], 2026 — verified against the live arXiv record before insertion.", { w: 62 })],
  ]));
bodyChildren.push(body(
  "Compilation with tectonic exits cleanly: 239 pages (v8: 238), 1.12 MiB, zero errors, zero undefined references. The overfull baseline carries over intact: the nine v8 boxes reproduce at identical magnitudes, with positions shifted exactly as the 171-line relocation predicts, plus one new 0.9-point reflow transient at the Section 17 active-bound item — the same class of sub-perceptual transient the v8 packaging already documented, caused purely by changed pagination, and left in place rather than chased. Structural verification runs 23 checks, all passing: v8 byte-unchanged and still frozen; the block present in Section 3, absent from Section 9, and ordered before the theory; the footnote present at its anchor with all three target definitions resolvable; the bibliography well-formed at 40 entries, every entry cited in both directions; 509 labels with no duplicates and no undefined references; environment pairing and brace balance; and the theorem-like environment count identical to v8, confirming no numbering was disturbed. The rendered PDF spot-checks confirm the footnote and the citation render on the Introduction page and the bibliography's new final entry, with the notation index still in place after the bibliography. v9 was frozen after verification at md5 341707e86a9c1a998e79c3cb981a23fd."));
bodyChildren.push(body(
  "Deliverables: automata_unified_revised_v9.tex and .pdf in the download directory, with v8 frozen and byte-unchanged; the edit and verification scripts retained for iteration; the ledger updated with the Q13a resolution, the Q12 decision, and a new settled entry recording the citation decision; and this report. The README manifest is updated with the v9 entry and change log, including the note that the submission package remains the built v8 artifact and that the author-block personalization protocol now targets a v10, since v9 is taken. The Q13b section-balance judgment call and the remaining open ledger items (Q2, Q7, Q10's structural successor) are unchanged by this cycle."));

// ================= assembly =================
const coverConfig = {
  title: "Q13a, the Retention-Gap Citation, and the Q12 Split Question",
  subtitle: "Three delegated editorial decisions, each actioned or recorded in automata_unified_revised_v9.tex",
  englishLabel: "DECISION REPORT",
  metaLines: [
    "Base version: automata_unified_revised_v8.tex (frozen, md5 39c1b519...)",
    "Produced version: automata_unified_revised_v9.tex (239 pages, 3 edits)",
    "Method: ledger evidence + anchored edits + 23-check verification",
    "Date: 2026-09-02",
  ],
  footerLeft: "automata- manuscript chain",
  footerRight: "v9 decision cycle",
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
          children: [new TextRun({ text: "v9 Decision Report - automata_unified_revised_v9.tex", size: 16, color: P.secondary, font: EN_FONT })],
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
  fs.writeFileSync("/home/z/my-project/automata/download/v9_decision_report.docx", buf);
  console.log("written:", buf.length, "bytes");
});
