// gen_theorem_check.js — main assembly for the dedicated proof check of the
// remaining 135 theorems of automata_unified_revised_v4.tex.
// Pattern: R1 cover + 3-section numbering (cover / TOC roman / body arabic),
// per docx skill (SKILL.md, routes/create.md, references/design-system.md,
// references/common-rules.md, references/toc.md, scenes/report.md).
const H = require("./tpc_helpers.js");
const {
  Document, Packer, Paragraph, TextRun, Header, Footer, PageNumber, NumberFormat,
  AlignmentType, SectionType, BorderStyle, TableOfContents,
  P, EN_FONT, HEAD_FONT, buildCoverR1,
} = H;
const fs = require("fs");

const contentA = require("./tpc_content_a.js");
const contentB = require("./tpc_content_b.js");
const bodyChildren = [...contentA, ...contentB];

const coverConfig = {
  title: "Dedicated Proof Check of the Remaining Theorems",
  subtitle: "135 proof-bearing results beyond the multiletter-AAK family, verified at line level",
  englishLabel: "PROOF VERIFICATION REPORT",
  metaLines: [
    "Manuscript: The Rate-Distortion Theory of Bounded Sequential Transduction",
    "Version checked: automata_unified_revised_v4.tex (frozen, 18,032 lines)",
    "Results in scope: 50 theorems, 21 lemmas, 37 propositions, 29 corollaries, 4 meta-theorems",
    "Verdict: 133 sound as stated; 2 minor proof-internal defects, fixed in v5",
    "Numerical verification: 42 of 42 independent checks pass",
  ],
  footerLeft: "Proof Verification Series",
  footerRight: "September 2026",
  palette: P.cover,
};

const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: EN_FONT, size: 22, color: P.body },
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
    { // Section 1: Cover (margin 0, no page numbers, no footer)
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
          border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: P.accent, space: 4 } },
          children: [new TextRun({ text: "Remaining-Theorems Proof Check - automata_unified_revised", size: 16, color: P.secondary, font: EN_FONT })],
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
  fs.writeFileSync("/home/z/my-project/download/remaining_theorems_proof_check.docx", buf);
  console.log("WROTE docx, bytes:", buf.length);
});
