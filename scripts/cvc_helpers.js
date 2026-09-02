// cvc_helpers.js — shared helpers for the coinage/venue decision report.
// Cloned from the validated house generator pattern (gen_novelty.js), which
// implements the docx skill's R1 cover recipe, 3-section numbering, TOC.
const {
  Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, HeadingLevel, WidthType, BorderStyle, ShadingType,
  TableLayoutType,
} = require("docx");

// ---------------- Palette (Deep Sea Academic / report) ----------------
const P = {
  primary: "16324F", body: "1C2A3D", secondary: "5B6B7D",
  accent: "8B7E5A", surface: "F5F7FA",
  cover: {
    bg: "16324F", titleColor: "FFFFFF", subtitleColor: "C9D4E0",
    metaColor: "AFC0D0", accent: "C8B896", footerColor: "8FA3B8",
  },
};

// ---------------- Border constants ----------------
const NB = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: NB, bottom: NB, left: NB, right: NB };
const allNoBorders = { top: NB, bottom: NB, left: NB, right: NB,
                       insideHorizontal: NB, insideVertical: NB };

// ---------------- Cover layout helpers (from design-system) ----------------
function splitTitleLines(title, charsPerLine) {
  if (title.length <= charsPerLine) return [title];
  const breakAfter = new Set([..." .,.;:!? ", ..."-_/"]);
  const lines = [];
  let remaining = title;
  while (remaining.length > charsPerLine) {
    let breakAt = -1;
    for (let i = charsPerLine; i >= Math.floor(charsPerLine / 2); i--) {
      if (breakAfter.has(remaining[i])) { breakAt = i; break; }
    }
    if (breakAt === -1) breakAt = charsPerLine;
    lines.push(remaining.slice(0, breakAt + 1).trim());
    remaining = remaining.slice(breakAt + 1).trim();
  }
  if (remaining) {
    if (remaining.length <= 2 && lines.length) {
      lines[lines.length - 1] += " " + remaining;
    } else {
      lines.push(remaining);
    }
  }
  return lines;
}

function calcTitleLayout(title, maxWidthTwips, preferredPt = 40, minPt = 24) {
  const estWidth = (s, pt) => {
    let w = 0;
    for (const ch of s) w += /[A-Z0-9]/.test(ch) ? pt * 13 : pt * 10;
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
    const avgChar = estWidth(title, minPt);
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

// ---------------- Cover Recipe R1 (Pure Paragraph Left) ----------------
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
function tag(text, color) {
  return new TextRun({ text: "  [" + text + "]", bold: true, size: 22, color, font: EN_FONT });
}
function cell(text, opts = {}) {
  const { bold = false, fill = null, w = 20, size = 20, color = P.body } = opts;
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
function tableCaption(text) {
  return new Paragraph({
    keepNext: true,
    spacing: { before: 160, after: 80 },
    children: [new TextRun({ text, bold: true, size: 21, color: P.secondary, font: EN_FONT })],
  });
}
function makeTable(headerCells, rows) {
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 2, color: P.accent },
      bottom: { style: BorderStyle.SINGLE, size: 2, color: P.accent },
      left: { style: BorderStyle.NONE },
      right: { style: BorderStyle.NONE },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 1, color: "D0D0D0" },
      insideVertical: { style: BorderStyle.NONE },
    },
    rows: [
      new TableRow({
        tableHeader: true, cantSplit: true,
        children: headerCells,
      }),
      ...rows.map(r => new TableRow({ cantSplit: true, children: r })),
    ],
  });
}

module.exports = { P, buildCoverR1, h1, h2, body, bodyRuns, run, tag, cell,
                   tableCaption, makeTable, EN_FONT, HEAD_FONT };
