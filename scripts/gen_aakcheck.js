// Dedicated line-level proof check of the multiletter-AAK theorem
// (thm:aak-multiletter, plus thm:aak-equality and supporting results)
// in automata_unified_revised_v3.tex / v4. Follows the validated R1 + 3-section
// pattern from gen_novelty.js (docx skill: create route, report scene, R1 recipe).
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, PageNumber, NumberFormat, AlignmentType, HeadingLevel,
  WidthType, BorderStyle, ShadingType, TableOfContents, PageBreak,
  SectionType, TableLayoutType,
} = require("docx");
const fs = require("fs");

// ---------------- Palette (same family as prior deliverables) ----------------
const P = {
  primary: "16324F", body: "1C2A3D", secondary: "5B6B7D",
  accent: "8B7E5A", surface: "F5F7FA",
  cover: {
    bg: "16324F", titleColor: "FFFFFF", subtitleColor: "C9D4E0",
    metaColor: "AFC0D0", accent: "C8B896", footerColor: "8FA3B8",
  },
};
const OK = "2E6B3E", WARN = "B4540A", INFO = "4E7A2E";

const NB = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: NB, bottom: NB, left: NB, right: NB };
const allNoBorders = { top: NB, bottom: NB, left: NB, right: NB,
                       insideHorizontal: NB, insideVertical: NB };

function splitTitleLines(title, charsPerLine) {
  if (title.length <= charsPerLine) return [title];
  const breakAfter = new Set([...",.;:!? ", ..."-_/"]);
  const lines = [];
  let remaining = title;
  while (remaining.length > charsPerLine) {
    let breakAt = -1;
    for (let i = charsPerLine; i >= Math.floor(charsPerLine * 0.6); i--) {
      if (i < remaining.length && breakAfter.has(remaining[i - 1])) { breakAt = i; break; }
    }
    if (breakAt === -1) {
      const limit = Math.min(remaining.length, Math.ceil(charsPerLine * 1.3));
      for (let i = charsPerLine + 1; i < limit; i++) {
        if (breakAfter.has(remaining[i - 1])) { breakAt = i; break; }
      }
    }
    if (breakAt === -1) breakAt = charsPerLine;
    lines.push(remaining.slice(0, breakAt).trim());
    remaining = remaining.slice(breakAt).trim();
  }
  if (remaining) lines.push(remaining);
  if (lines.length > 1 && lines[lines.length - 1].length <= 2) {
    const last = lines.pop();
    lines[lines.length - 1] += last;
  }
  return lines;
}

function calcTitleLayout(title, maxWidthTwips, preferredPt = 40, minPt = 24) {
  const estWidth = (text, pt) => {
    let w = 0;
    for (const ch of text) {
      const code = ch.codePointAt(0);
      const isCJK = (code >= 0x4E00 && code <= 0x9FFF) || (code >= 0x3000 && code <= 0x303F);
      w += isCJK ? pt * 20 : pt * 11;
    }
    return w;
  };
  let titlePt = preferredPt, lines;
  while (titlePt >= minPt) {
    const avgChar = estWidth(title, titlePt) / title.length;
    const cpl = Math.max(2, Math.floor(maxWidthTwips / avgChar));
    lines = splitTitleLines(title, cpl);
    if (lines.length <= 3) break;
    titlePt -= 2;
  }
  if (!lines || lines.length > 3) {
    const avgChar = estWidth(title, minPt) / title.length;
    lines = splitTitleLines(title, Math.max(2, Math.floor(maxWidthTwips / avgChar)));
    titlePt = minPt;
  }
  return { titlePt, titleLines: lines };
}

function calcCoverSpacing(params) {
  const { titleLineCount = 1, titlePt = 36, hasSubtitle = false, hasEnglishLabel = false,
    metaLineCount = 0, fixedHeight = 800, pageHeight = 16838 } = params;
  const SAFETY = 1200;
  const usableHeight = pageHeight - SAFETY;
  const titleHeight = titleLineCount * (titlePt * 23 + 200);
  const subtitleHeight = hasSubtitle ? (12 * 23 + 600) : 0;
  const englishLabelHeight = hasEnglishLabel ? (9 * 23 + 600) : 0;
  const metaHeight = metaLineCount * (10 * 23 + 100);
  const implicitParaHeight = 3 * 300;
  const contentHeight = titleHeight + subtitleHeight + englishLabelHeight + metaHeight + fixedHeight + implicitParaHeight;
  const safeRemaining = Math.max(usableHeight - contentHeight, 400);
  const FOOTER_MIN = 800;
  const rawTop = Math.floor(safeRemaining * 0.45);
  const rawBottom = Math.floor(safeRemaining * 0.45);
  const bottomSpacing = Math.max(rawBottom, FOOTER_MIN);
  const topSpacing = Math.max(rawTop - Math.max(0, FOOTER_MIN - rawBottom), 400);
  return { topSpacing, midSpacing: Math.max(safeRemaining - topSpacing - bottomSpacing, 0), bottomSpacing };
}

function buildCoverR1(config) {
  const PC = config.palette;
  const padL = 1200, padR = 800;
  const availableWidth = 11906 - padL - padR - 300;
  const { titlePt, titleLines } = calcTitleLayout(config.title, availableWidth, 40, 24);
  const titleSize = titlePt * 2;
  const spacing = calcCoverSpacing({
    titleLineCount: titleLines.length, titlePt,
    hasSubtitle: !!config.subtitle, hasEnglishLabel: !!config.englishLabel,
    metaLineCount: (config.metaLines || []).length, fixedHeight: 400,
  });
  const accentLeft = { style: BorderStyle.SINGLE, size: 8, color: PC.accent, space: 12 };
  const children = [];
  children.push(new Paragraph({ spacing: { before: spacing.topSpacing } }));
  if (config.englishLabel) {
    children.push(new Paragraph({
      indent: { left: padL, right: padR }, spacing: { after: 500 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: PC.accent, space: 8 } },
      children: [new TextRun({ text: config.englishLabel.split("").join("  "),
        size: 18, color: PC.accent, font: { ascii: "Calibri", eastAsia: "SimHei" }, characterSpacing: 40 })],
    }));
  }
  for (let i = 0; i < titleLines.length; i++) {
    children.push(new Paragraph({
      indent: { left: padL },
      spacing: { after: i < titleLines.length - 1 ? 100 : 300, line: Math.ceil(titlePt * 23), lineRule: "atLeast" },
      children: [new TextRun({ text: titleLines[i], size: titleSize, bold: true,
        color: PC.titleColor, font: { eastAsia: "SimHei", ascii: "Arial" } })],
    }));
  }
  if (config.subtitle) {
    children.push(new Paragraph({
      indent: { left: padL, right: padR }, spacing: { after: 800 },
      children: [new TextRun({ text: config.subtitle, size: 24, color: PC.subtitleColor,
        font: { eastAsia: "Microsoft YaHei", ascii: "Arial" } })],
    }));
  }
  for (const line of (config.metaLines || [])) {
    children.push(new Paragraph({
      indent: { left: padL + 200 }, spacing: { after: 80 },
      border: { left: accentLeft },
      children: [new TextRun({ text: line, size: 24, color: PC.metaColor,
        font: { eastAsia: "Microsoft YaHei", ascii: "Arial" } })],
    }));
  }
  children.push(new Paragraph({ spacing: { before: spacing.bottomSpacing } }));
  children.push(new Paragraph({
    indent: { left: padL, right: padR },
    border: { top: { style: BorderStyle.SINGLE, size: 2, color: PC.accent, space: 8 } },
    spacing: { before: 200 },
    children: [
      new TextRun({ text: config.footerLeft || "", size: 16, color: PC.footerColor, font: { ascii: "Arial" } }),
      new TextRun({ text: "                                        " }),
      new TextRun({ text: config.footerRight || "", size: 16, color: PC.footerColor, font: { ascii: "Arial" } }),
    ],
  }));
  return [new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    layout: TableLayoutType.FIXED,
    borders: allNoBorders,
    rows: [new TableRow({
      height: { value: 16838, rule: "exact" },
      children: [new TableCell({
        shading: { type: ShadingType.CLEAR, fill: PC.bg }, borders: noBorders,
        children,
      })],
    })],
  })];
}

// ---------------- Text helpers ----------------
const EN_FONT = { ascii: "Times New Roman", eastAsia: "SimSun" };
const HEAD_FONT = { ascii: "Times New Roman", eastAsia: "SimHei" };

function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 160, line: 312 },
    children: [new TextRun({ text, bold: true, size: 32, color: P.primary, font: HEAD_FONT })],
  });
}
function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 280, after: 120, line: 312 },
    children: [new TextRun({ text, bold: true, size: 28, color: P.primary, font: HEAD_FONT })],
  });
}
function body(text, opts = {}) {
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { line: 312, after: 120 },
    children: [new TextRun({ text, size: 22, color: P.body, font: EN_FONT, ...opts })],
  });
}
function bodyRuns(runs) {
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { line: 312, after: 120 },
    children: runs,
  });
}
function run(text, opts = {}) {
  return new TextRun({ text, size: 22, color: P.body, font: EN_FONT, ...opts });
}
function mono(text) {
  return new TextRun({ text, size: 19, color: "3B5C7A", font: { ascii: "Courier New", eastAsia: "SimSun" } });
}
function findingTag(status) {
  const color = status === "Sound" ? OK : (status === "Precision" ? WARN : INFO);
  return new TextRun({ text: "  [" + status + "]", bold: true, size: 22, color, font: EN_FONT });
}
function cell(text, opts = {}) {
  const { bold = false, fill = null, w = 20, size = 19, color = P.body } = opts;
  return new TableCell({
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    width: { size: w, type: WidthType.PERCENTAGE },
    shading: fill ? { type: ShadingType.CLEAR, fill } : undefined,
    children: [new Paragraph({
      spacing: { line: 276 },
      children: [new TextRun({ text, bold, size, color, font: EN_FONT })],
    })],
  });
}
function verdictRow(a, b, c, d) {
  return new TableRow({
    tableHeader: false, cantSplit: true,
    children: [
      cell(a, { w: 8, bold: true }),
      cell(b, { w: 30 }),
      cell(c, { w: 14, color: c === "Sound" ? OK : (c === "Precision" ? WARN : INFO), bold: true }),
      cell(d, { w: 48 }),
    ],
  });
}

// ================= BODY =================
const bodyChildren = [];

// ---- 1. Executive Summary ----
bodyChildren.push(h1("1. Executive Summary"));
bodyChildren.push(body(
  "This report documents a dedicated line-level proof check of the multiletter Adamjan-Arov-Krein theorem of the manuscript 'The Rate-Distortion Theory of Bounded Sequential Transduction' (Theorem thm:aak-multiletter, 'Multi-Letter Case, Conditional Form'), requested because it is the manuscript's highest-exposure technical claim without external corroboration. The check covered the theorem itself, the scalar theorem thm:aak-equality from which it transports, the five supporting results in its dependency cone (Theorem thm:spectral-grounding, Propositions prop:grounding-finite-section and prop:grounding-structured-zero, Corollary cor:hankel-strict, and Open Problem open:hankel-multiletter), and the surrounding shift-structure claims. Every algebraic step was re-derived by hand, the operator-theoretic statements were checked against the classical literature (Adamjan-Arov-Krein 1971; Peller 2003; Hartman's compactness characterization), and the open-problem status was verified against the current approximate-minimization literature through fresh web searches."
));
bodyChildren.push(bodyRuns([
  run("The verdict is: "),
  run("the theorem and its proof are sound as stated", { bold: true, color: OK }),
  run(". The theorem is an honestly conditional transport statement: it assumes a structure-preserving embedding and an AAK/Nehari-type theorem on the target space, and correctly derives the equality of the Hankel-structured and unrestricted gaps at the Eckart-Young-Mirsky value. No mathematical error was found in the statement, the proof, or any supporting result. Two precision improvements were identified and have been applied in the v4 revision: the third hypothesis is now explicitly tied to the transported operator U H-nu U* (including the exact distance identity it must supply), and the four-line proof now displays the full transport chain instead of referring to the scalar case. Two further precision notes (the redundancy of the intertwining clause, and the automatic status of the canonical unitary in the one-letter case) were likewise incorporated into v4 as explanatory sentences.")
]));
bodyChildren.push(body(
  "External corroboration is unusually strong for a conditional result of this kind. A fresh search located the paper 'Towards an AAK Theory Approach to Approximate Minimization' (C. Lacroce, LearnAut 2022, arXiv:2206.00172), which states verbatim that extending AAK-style approximate minimization to multi-letter alphabets requires, first, a noncommutative Hankel reformulation and, second, a constructive version of noncommutative AAK theory, and that in that paper the first step is achieved while the second challenge remains open. This matches the manuscript's framing exactly: the multiletter equality is conditional on a theorem the operator-theory community has not yet supplied. The check therefore closes with the assessment that the theorem is correct, honestly scoped, and correctly positioned with respect to the state of the art, with the v4 precision edits making the hypotheses auditable line by line."
));

// ---- 2. Scope and Method ----
bodyChildren.push(h1("2. Scope, Sources, and Method"));
bodyChildren.push(body(
  "The object under check is Theorem thm:aak-multiletter of the grounding chapter (Section 'Linear Finite-Rank Spectral Converse'), stated for joint alphabets with |Sigma| > 1, together with its proof, its scalar anchor Theorem thm:aak-equality, and the dependency cone listed above. The version under review is automata_unified_revised_v3.tex (18,026 source lines, 234 compiled pages), with the v4 revision (this deliverable's companion) carrying the precision edits. The manuscript was read at line level in full, and every display in the theorem's cone was re-derived rather than skimmed: the Hankel condition was recomputed from the matrix entries, the intertwining identities were verified algebraically, the singular-value conventions were checked against the standard literature conventions, and the Kronecker degree claim was checked against Peller's treatment."
));
bodyChildren.push(body(
  "The method had three layers. Layer one, internal re-derivation: each proof step was reproduced independently, including the conjugation algebra US = S+U implies US*U* = S+*, the subset argument for the Hankel-restricted gap, the Cauchy interlacing step of the finite-section certificates, and the norm-closedness argument for the structured zero threshold. Layer two, classical-reference verification: the AAK theorem's statement form (distance from a compact Hankel operator to the rank-at-most-M Hankel class equals the (M+1)-st singular value, attained, with rational antianalytic part of degree at most M), Hartman's theorem (H-phi compact iff phi in H-infinity + C), and the Kronecker rank-degree equality were each confirmed against the standard sources cited by the manuscript (aak1971; peller2003, Chapters 2 and 4). Layer three, external status check: fresh web searches verified whether any published multiletter AAK-type theorem exists that the manuscript could have cited instead of stating a conditional form; the searches covered the Balle-Lacroce-Panangaden-Precup-Rabusseau ICALP 2021 line, the Lacroce one-letter follow-up (Mathematical Structures in Computer Science, 2024), the Lacroce PhD thesis, and the Popescu multivariable operator theory line (multi-analytic operators on Fock spaces, Mathematische Annalen 1995 onward)."
));

// ---- 3. Scalar anchor ----
bodyChildren.push(h1("3. The Scalar Anchor: Theorem thm:aak-equality"));
bodyChildren.push(body(
  "The multiletter theorem transports from the scalar case, so the scalar theorem was checked first and in full. Its content: for a one-letter alphabet, if a unitary U from l2(Sigma*) to Hardy space H2 intertwines the unilateral shift S with the Hardy shift S+ (hypothesis a), and transports the Hankel operator H-nu to a compact Hardy-space Hankel operator H-phi (hypothesis b, equivalent by Hartman's theorem to a symbol in H-infinity + C), then the Hankel-structured gap equals the unrestricted gap equals the (M+1)-st singular value, the optimum is attained, and the optimal approximant may be taken with rational antianalytic symbol part of degree at most M. Uniqueness is explicitly not asserted except under the classical simplicity hypothesis on adjacent singular values."
));
bodyChildren.push(bodyRuns([
  run("The structural backbone of the theorem is the conjugation identity: from US = S+U one obtains, by taking adjoints, S*U* = U*S+*, hence S* = U*S+*U and therefore US*U* = S+. Consequently, for any bounded operator B, the Hankel condition S*B = BS is equivalent to S+*(UBU*) = (UBU*)S+, which is the classical Hardy-space Hankel condition. "),
  run("This step was verified by direct computation and is correct.", { bold: true, color: OK }),
  run(" It is the load-bearing algebra of hypothesis (a): it is exactly what makes U carry the Hankel feasible set bijectively onto the classical one, so that the two constrained infima agree and the AAK value descends to H-nu.")
]));
bodyChildren.push(bodyRuns([
  run("The remaining claims were checked as follows. The application of the Adamjan-Arov-Krein theorem (dist to rank-at-most-M Hankel operators equals the (M+1)-st singular value, attained by an operator whose symbol has rational antianalytic part of degree at most M) matches the theorem's standard form as presented in Peller's Chapter 4, including the source convention s_m = sigma_(m+1) that the manuscript disambiguates explicitly. The Kronecker claim (rank H-psi equals the degree of the antianalytic part, with degree defined as max of numerator and denominator degrees in lowest terms, equivalently the total pole count including a possible pole at infinity) is the classical statement. The assertion that rank budget and symbol degree carry the same index because Kronecker's theorem is an equality (no off-by-one) is correct. The honest non-claims (existence and value but not uniqueness; uniqueness only under the simplicity hypothesis) are correctly stated and correctly attributed. "),
  run("Verdict: sound, with the v4 addition of one explanatory sentence recording that for a one-letter alphabet the canonical basis-to-monomial unitary satisfies hypothesis (a) automatically, aligning the body with the abstract's remark.", { bold: true, color: OK })
]));

// ---- 4. The multiletter theorem ----
bodyChildren.push(h1("4. The Multiletter Theorem: Statement and Proof Re-Derivation"));
bodyChildren.push(h2("4.1 The shift-structure preamble"));
bodyChildren.push(bodyRuns([
  run("The theorem's preamble asserts that for |Sigma| > 1 the free monoid carries |Sigma| prefix shifts S_a (a in Sigma), which jointly form an isometry of multiplicity |Sigma|, so that no single unilateral shift of multiplicity one is available and the classical scalar AAK theorem does not apply. "),
  run("This was verified from first principles and is correct.", { bold: true, color: OK }),
  run(" With the prefix convention S_a e_u = e_(au), the ranges of S_a and S_b for distinct letters are orthogonal (their words begin with different letters), the joint map from the direct sum of |Sigma| copies of l2(Sigma*) is an isometry, and its range has codimension exactly one (the empty word is missed), which is the standard free-semigroup-shift geometry. The manuscript's inference - that the scalar theorem cannot be applied as stated to a multiletter Hankel operator - is therefore structurally justified, not rhetorical.")
]));
bodyChildren.push(h2("4.2 The conditional transport"));
bodyChildren.push(body(
  "The theorem then hypothesizes three data: a Hilbert space K carrying a multi-shift or free-semigroup Hankel structure; a unitary U that intertwines the respective shift systems and carries the rank-at-most-M Hankel class of l2(Sigma*) bijectively onto the corresponding Hankel class on K; and an Adamjan-Arov-Krein/Nehari-type finite-rank approximation theorem valid on K. Under these hypotheses it concludes that the Hankel-structured gap, the unrestricted gap, and the (M+1)-st singular value all coincide. The proof argues by transport: U preserves rank, norm, and (by hypothesis) the Hankel feasible sets, so the two constrained infima agree, and the assumed theorem supplies the value."
));
bodyChildren.push(bodyRuns([
  run("The proof logic was checked by writing out the chain it abbreviates: the Hankel-structured gap equals the infimum of the operator-norm distance from U H-nu U* to the Hankel class of K at rank at most M (by the feasible-set bijection and unitary invariance of the norm); the hypothesized theorem on K supplies the value sigma_(M+1)(U H-nu U*) for this infimum; unitary invariance identifies this with sigma_(M+1)(H-nu); and Eckart-Young-Mirsky independently identifies the unrestricted gap with the same value, so the three quantities coincide. "),
  run("Every implication in the chain is valid, and nothing beyond transport of structure is used, exactly as the proof claims.", { bold: true, color: OK }),
  run(" The proof is therefore sound. What it is not is self-contained: all mathematical content beyond transport sits in the hypotheses, which is the honest architecture the theorem's title ('Conditional Form') advertises.")
]));
bodyChildren.push(h2("4.3 Precision findings and their v4 disposition"));
bodyChildren.push(body(
  "Four precision findings were recorded during the check; none is an error, and all four have been incorporated into the v4 revision."
));
bodyChildren.push(bodyRuns([
  run("P1 - the third hypothesis was not tied to the transported operator. ", { bold: true }),
  findingTag("Precision"),
  run(" As stated in v3, 'an AAK/Nehari-type finite-rank approximation theorem valid on K' does not name the operator to which the theorem must apply, nor the conclusion it must deliver. A reader auditing the proof has to reconstruct both. v4 sharpens the hypothesis: U H-nu U* must belong to the class to which the theorem applies (in particular it is compact, consistently with the standing spectral-admissibility hypothesis of the Hilbert-module definition), and the theorem must supply the displayed distance identity at rank at most M for that operator. This makes the proof mechanically checkable: each hypothesis is consumed by exactly one step of the displayed chain.")
]));
bodyChildren.push(bodyRuns([
  run("P2 - the proof referred to the scalar case instead of displaying the chain. ", { bold: true }),
  findingTag("Precision"),
  run(" The v3 proof is four lines and leans on 'identical to the scalar case'. The transport is indeed identical in structure, but a theorem carrying this much exposure (the manuscript's type-discipline section flags it as the theorem whose hypothesis 'is not known to be checkable in general') deserves a self-contained proof. v4 replaces the four lines with the full chain, including the Eckart-Young-Mirsky identification of the unrestricted gap and an explicit closing sentence that only transport of structure is used.")
]));
bodyChildren.push(bodyRuns([
  run("P3 - the intertwining clause is not consumed by the proof. ", { bold: true }),
  findingTag("Observation"),
  run(" The proof uses the Hankel-class bijection, not the intertwining of the shift systems; the bijection hypothesis subsumes the work the intertwining clause suggests it does. This is redundancy, not error. v4 adds one sentence to the proof recording this: the clause is retained because any natural candidate for U would have to satisfy it, and because it excludes transporting the feasible sets by a unitary unrelated to the shift systems. Stating the redundancy prevents a reader from hunting for a phantom proof step.")
]));
bodyChildren.push(bodyRuns([
  run("P4 - the automatic-unitary status in the scalar case is asserted in the abstract but not in the theorem. ", { bold: true }),
  findingTag("Observation"),
  run(" The v3 abstract states that for a one-letter alphabet the shift-intertwining Hardy unitary 'is the canonical basis-to-monomial correspondence and is therefore automatic', but Theorem thm:aak-equality presents hypothesis (a) as a hypothesis without noting this. v4 adds a parenthetical note in the theorem: the canonical unitary satisfies (a) automatically in the one-letter case, and (a) is retained as a hypothesis because the theorem is quoted in the generality in which U is arbitrary. The body and abstract are now consistent on this point.")
]));

// ---- 5. Supporting results ----
bodyChildren.push(h1("5. Supporting Results in the Dependency Cone"));
bodyChildren.push(body(
  "Five results surround the multiletter theorem and were checked because a defect in any of them would infect the theorem's use. All five are sound."
));
bodyChildren.push(bodyRuns([
  run("Theorem thm:spectral-grounding (unrestricted equality by Eckart-Young-Mirsky; structured lower bound by the subset argument). ", { bold: true }),
  findingTag("Sound"),
  run(" The unrestricted equality is the Eckart-Young-Mirsky theorem for compact operators, invoked under the standing compactness hypothesis; the structured inequality is the correct observation that restricting an infimum to a subset cannot decrease it. The v4 revision consolidated three remark-level repetitions of this pair of statements into cross-references to this theorem (the E1 consolidation), which reduces exactly the drift risk this check was designed to catch: two statements of the same fact drifting apart.")
]));
bodyChildren.push(bodyRuns([
  run("Proposition prop:grounding-finite-section (finite-section certificates). ", { bold: true }),
  findingTag("Sound"),
  run(" The two-sided certificate combines finite-dimensional Eckart-Young-Mirsky on the truncation P_N H P_N, the Lipschitz property of singular values under operator-norm perturbation, and the strong convergence P_N to I together with compactness, which gives norm convergence of the truncation. Each step is standard and correctly applied; the claim that rational finite-section entries give algebraic certificates is correct.")
]));
bodyChildren.push(bodyRuns([
  run("Proposition prop:grounding-structured-zero (exact zero threshold rank(H) at most M). ", { bold: true }),
  findingTag("Sound"),
  run(" The forward direction is trivial (H itself is an admissible structured approximant). The reverse direction uses that the set of operators of rank at most M is norm closed, via the Gram-determinant argument: M+1 linearly independent images remain linearly independent under sufficiently small perturbations. The argument is correct; the hypothesis 'bounded Hankel operator' (rather than compact) is exactly what is needed and is correctly not strengthened.")
]));
bodyChildren.push(bodyRuns([
  run("Corollary cor:hankel-strict (strict gap obstructs Hardy representability). ", { bold: true }),
  findingTag("Sound"),
  run(" This is the contrapositive of the scalar theorem and is correctly scoped: the surrounding remark (rem:hankel-strict-scope) explicitly confines the obstruction reading to the scalar shift model, noting that in the multiletter setting the contrapositive has no content absent the embedding hypothesis. The scoping is accurate and important; it is one of the passages that the external literature check (next section) independently validates.")
]));
bodyChildren.push(bodyRuns([
  run("Open Problem open:hankel-multiletter (intrinsic characterization). ", { bold: true }),
  findingTag("Sound"),
  run(" The problem statement - characterize intrinsically in terms of the channel when the Hankel operator admits a structure-preserving embedding into a vector-valued Hardy or full Fock space Hankel class carrying an AAK/Nehari theorem, or prove no intrinsic characterization exists - is well-posed, carries a falsifiable success criterion, and honestly records the scalar baseline. Its open status is externally corroborated in Section 6.")
]));

// ---- 6. External corroboration ----
bodyChildren.push(h1("6. External Corroboration of the Open Status"));
bodyChildren.push(body(
  "The check's final layer asked whether the conditional form is necessary: does the literature already contain a multiletter AAK-type theorem that the manuscript could cite outright? Fresh searches were run against the approximate-minimization line (the closest programmatic neighbor of the manuscript's grounding regime) and the multivariable operator theory line. The strongest evidence found is the following."
));
bodyChildren.push(bodyRuns([
  run("C. Lacroce, 'Towards an AAK Theory Approach to Approximate Minimization' (LearnAut 2022, arXiv:2206.00172), states in its abstract, verbatim: "),
  run("'Extending the result to multi-letter alphabets requires solving the following two steps. First, we need to reformulate the approximation problem in terms of noncommutative Hankel operators and noncommutative functions, in order to apply results from multivariable operator theory. Secondly, to obtain the optimal approximation we need a version of noncommutative AAK theory that is constructive. In this paper, we successfully tackle the first step, while the second challenge remains open.'", { italics: true }),
  run(" This is direct, current, programmatic confirmation from the research line that has done the most to extend AAK theory to automata: the multiletter equality theorem does not exist in the published state of the art, and its absence is a recognized open challenge rather than an oversight of the manuscript.")
]));
bodyChildren.push(body(
  "The surrounding literature is consistent with this. The published exact results concern one-letter alphabets: Balle, Lacroce, Panangaden, Precup, and Rabusseau (ICALP 2021, LIPIcs 198) for the spectral-norm optimal approximate minimization of weighted finite automata over one letter, and the follow-up (Lacroce, Balle, Panangaden, Rabusseau, Mathematical Structures in Computer Science 34, 2024, pp. 807-833) for the one-letter optimal minimization in the same circle of ideas. The multivariable operator theory that a multiletter theorem would need exists as machinery rather than as a ready-made AAK theorem: Popescu's multi-analytic operators on Fock spaces (Mathematische Annalen 303, 1995) and the subsequent free-semigroup operator algebra literature supply the shift geometry (the same multiplicity-|Sigma| isometry structure the manuscript's preamble verifies), and recent work on Hankel operators on Fock spaces develops the analytic side; but the constructive noncommutative AAK step is, per the Lacroce quotation, exactly the open part. The manuscript's conditional Theorem thm:aak-multiletter and Open Problem open:hankel-multiletter are therefore calibrated correctly against the literature: neither overclaiming an available theorem nor understating what the one-letter published results already deliver."
));

// ---- 7. Verdict table ----
bodyChildren.push(h1("7. Verdict Table"));
bodyChildren.push(body(
  "The table summarizes the check. 'Sound' means every step was re-derived and found correct. 'Precision' means the mathematics is correct but the statement or proof was tightened in v4 for auditability. 'Observation' means a non-defect note incorporated into v4 as an explanatory sentence."
));
bodyChildren.push(new Paragraph({
  keepNext: true,
  spacing: { before: 120, after: 60 },
  children: [new TextRun({ text: "Table 1. Proof-check verdicts by item", bold: true, size: 21, color: P.secondary, font: EN_FONT })],
}));
bodyChildren.push(new Table({
  width: { size: 100, type: WidthType.PERCENTAGE },
  layout: TableLayoutType.FIXED,
  borders: {
    top: { style: BorderStyle.SINGLE, size: 2, color: "9AA6B2" },
    bottom: { style: BorderStyle.SINGLE, size: 2, color: "9AA6B2" },
    left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE },
    insideHorizontal: { style: BorderStyle.SINGLE, size: 1, color: "D0D0D0" },
    insideVertical: { style: BorderStyle.SINGLE, size: 1, color: "E2E2E2" },
  },
  rows: [
    new TableRow({
      tableHeader: true, cantSplit: true,
      children: [
        cell("Item", { w: 8, bold: true, fill: "EFF3F7" }),
        cell("Content checked", { w: 30, bold: true, fill: "EFF3F7" }),
        cell("Verdict", { w: 14, bold: true, fill: "EFF3F7" }),
        cell("Notes", { w: 48, bold: true, fill: "EFF3F7" }),
      ],
    }),
    verdictRow("S1", "thm:aak-equality: hypotheses, AAK application, Kronecker degree, indexing", "Sound", "Conjugation algebra verified; honest non-claims confirmed; v4 adds automatic-unitary note"),
    verdictRow("S2", "thm:aak-multiletter: statement and proof", "Sound", "Transport logic valid; hypotheses carry all content; no error found"),
    verdictRow("S3", "Multiletter preamble: prefix shifts, multiplicity |Sigma| isometry", "Sound", "Orthogonal ranges and one-dimensional deficiency verified from first principles"),
    verdictRow("P1", "Third hypothesis not tied to transported operator", "Precision", "v4 names U H-nu U*, compactness, and the required distance identity"),
    verdictRow("P2", "Proof referred to scalar case without displaying chain", "Precision", "v4 displays the full transport chain and closes with the transport-only statement"),
    verdictRow("P3", "Intertwining clause not consumed by proof", "Observation", "v4 records the redundancy and the reason the clause is retained"),
    verdictRow("P4", "Automatic-unitary status absent from scalar theorem body", "Observation", "v4 parenthetical aligns body with abstract"),
    verdictRow("C1", "thm:spectral-grounding", "Sound", "EYM plus subset argument; remark-level repetitions consolidated in v4 (E1)"),
    verdictRow("C2", "prop:grounding-finite-section", "Sound", "Interlacing plus strong-convergence argument standard and correct"),
    verdictRow("C3", "prop:grounding-structured-zero", "Sound", "Gram-determinant closedness argument correct; hypotheses minimal"),
    verdictRow("C4", "cor:hankel-strict and its scoping remark", "Sound", "Contrapositive correct; scalar-model scoping accurate"),
    verdictRow("C5", "open:hankel-multiletter", "Sound", "Well-posed with falsifiable criterion; open status externally corroborated"),
    verdictRow("X1", "External status of multiletter AAK", "Corroborated", "Lacroce LearnAut 2022: second step 'remains open'; one-letter state is Balle et al. 2021 and Lacroce et al. 2024"),
  ],
}));

// ---- 8. Residual risks ----
bodyChildren.push(h1("8. Residual Risks and Recommendations"));
bodyChildren.push(body(
  "No mathematical defect was found, so the residual risks are positioning and auditability risks rather than correctness risks. First, the theorem's exposure is asymmetric: because it is the manuscript's only high-visibility conditional claim in the grounding chapter, a referee will read its hypotheses with above-average care, and the v4 sharpening (P1, P2) is the appropriate response; the recommendation is to keep the displayed distance identity in the hypothesis rather than paraphrasing it, since that is the form a referee can check against the assumed theorem on K. Second, the external literature is moving: the Lacroce program has announced the noncommutative reformulation as achieved and the constructive step as open, so a submission should re-run the search at proof stage and, if a constructive noncommutative AAK theorem has appeared in the interim, either cite it as discharging the hypothesis or re-scope the conditional theorem. Third, the v4 consolidation of the repeated unrestricted-versus-structured statements (the E1 fix) directly reduces the drift risk that motivated this check; maintaining the single-statement convention going forward is recommended."
));
bodyChildren.push(body(
  "A final note on method. This check was deliberately confined to the theorem's dependency cone and to verifiable claims: every internal step was re-derived, every classical invocation was checked against its standard source, and every external statement quoted in this report was retrieved from the primary source during the check. Statements about the broader literature (for example, that no constructive noncommutative AAK theorem exists anywhere) are reported only at the confidence level the searches support: the strongest available programmatic statement (Lacroce 2022) declares the step open, and no counter-evidence was found."
));

// ================= DOCUMENT =================
const coverConfig = {
  title: "Dedicated Proof Check: The Multiletter AAK Theorem",
  subtitle: "Line-level verification of thm:aak-multiletter, its scalar anchor, and its dependency cone",
  englishLabel: "PROOF VERIFICATION REPORT",
  metaLines: [
    "Manuscript: automata_unified_revised (v3 audited, v4 disposition)",
    "Object: Theorem thm:aak-multiletter and supporting results",
    "Method: step re-derivation, classical-reference and literature checks",
    "Verdict: sound; two precision edits applied in v4",
  ],
  footerLeft: "automata- manuscript series",
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
    { // Section 1: Cover
      properties: {
        page: { size: { width: 11906, height: 16838 }, margin: { top: 0, bottom: 0, left: 0, right: 0 } },
      },
      children: buildCoverR1(coverConfig),
    },
    { // Section 2: TOC (roman)
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
          children: [new TextRun({ text: "Multiletter AAK Proof Check - automata_unified_revised", size: 16, color: P.secondary, font: EN_FONT })],
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
  fs.writeFileSync("/home/z/my-project/download/aak_multiletter_proof_check.docx", buf);
  console.log("WROTE docx, bytes:", buf.length);
});
