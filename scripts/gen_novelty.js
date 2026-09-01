// Novelty assessment report for automata_unified_revised_v3.tex
// Part 1: helpers, cover, sections 1-3
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, PageNumber, NumberFormat, AlignmentType, HeadingLevel,
  WidthType, BorderStyle, ShadingType, TableOfContents, PageBreak,
  SectionType, TableLayoutType,
} = require("docx");
const fs = require("fs");

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
function url(text) {
  return new TextRun({ text, size: 18, color: "3B5C7A", font: { ascii: "Courier New", eastAsia: "SimSun" } });
}
// source line: authors/title + url
function srcLine(text, link) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { line: 280, after: 60 },
    indent: { left: 360 },
    border: { left: { style: BorderStyle.SINGLE, size: 6, color: P.accent, space: 8 } },
    children: [run(text), new TextRun({ text: "  " }), url(link)],
  });
}
const NV = { High: "2E6B3E", "Moderate-High": "4E7A2E", Moderate: "6B6B23", Incremental: "B4540A" };
function noveltyTag(level) {
  return new TextRun({ text: "  [" + level + "]", bold: true, size: 22, color: NV[level] || P.secondary, font: EN_FONT });
}

// data table cell
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

// ================= BODY CONTENT =================
const bodyChildren = [];

// ---- 1. Executive Summary ----
bodyChildren.push(h1("1. Executive Summary"));
bodyChildren.push(body(
  "This report assesses the novelty of the manuscript 'The Rate-Distortion Theory of Bounded Sequential Transduction: A Comparative Syntax for Finite-State Approximation' (automata_unified_revised_v3.tex, 234 compiled pages, 378 theorem-like environments) against the published and preprint literature reachable through a deep open-web search. Twenty targeted search queries were run across eight literature families: computational mechanics and epsilon-machines; information bottleneck and Markov aggregation; lumpability; Hankel/AAK approximate minimization of weighted automata; Myhill-Nerode-based complexity; automata synchronization and active learning; individual-sequence and causal rate-distortion; and communication complexity. Each query returned ten ranked results, which were screened by title and snippet and then mapped against the manuscript's ten core contributions."
));
bodyChildren.push(body(
  "The headline verdict is that the manuscript's framework-level contribution appears genuinely novel. No prior work was found that unifies finite-state approximation of sequential transductions across the three regimes the manuscript calls commitment, retention, and grounding, under a single resource accounting (the index of a finite right congruence on histories), and no prior work states an independence theorem showing that the three regime obstructions can be varied independently, or a type discipline that tags every approximation statement with a seven-coordinate signature. The exact phrase 'rate-distortion theory of bounded sequential transduction' and its near variants return no matches in the open-web index. Within each individual regime, however, there is deep and active prior art, and the manuscript's contribution there is compositional: it re-derives or transports known tools (Myhill-Nerode, information bottleneck, Ky Fan, Eckart-Young-Mirsky, Adamjan-Arov-Krein, halving) into the unified accounting."
));
bodyChildren.push(body(
  "Three citation gaps deserve attention before submission, because the missing references are the closest conceptual neighbors of three of the manuscript's regimes: Still and Crutchfield's work connecting information bottlenecks to causal states; Geiger's line of work on optimal Kullback-Leibler aggregation of Markov chains; and the Balle-Giraud-Lacroce line on optimal spectral-norm approximate minimization of weighted automata, which is the closest modern prior for the grounding regime. None of the three is currently in the manuscript's bibliography. Section 7 lists them with URLs and concrete recommendations. Overall, the assessment is: novelty High at the framework level, Moderate-High for the composite theorems, with a small set of well-defined positioning tasks that would make the novelty defensible under referee scrutiny."
));

// ---- 2. Method and Coverage ----
bodyChildren.push(h1("2. Search Method and Coverage"));
bodyChildren.push(body(
  "The search was conducted through an aggregated web-search backend that indexes the open web, including arXiv, Springer, Elsevier ScienceDirect, ACM Digital Library, IEEE Xplore, Dagstuhl LIPIcs, PubMed Central, university repositories, and technical blogs. Twenty queries were executed, each returning the top ten ranked results. The queries were designed in two layers: a framing layer, probing the manuscript's own headline concepts (rate-distortion plus sequential transduction; comparative syntax; bounded sequential transduction), and a per-regime layer, probing the literature of each regime the manuscript draws on, plus the specific technical instruments (unifilar lumpability, determination indices, Hankel-restricted rank, Moore separation, halving mistake bounds, Fisher covariance lower bounds, streaming lower bounds)."
));
bodyChildren.push(body(
  "Coverage map of the twenty queries: (1) rate-distortion theory sequential transduction finite-state approximation; (2) Myhill-Nerode index complexity measure; (3) computational mechanics epsilon-machine information bottleneck; (4) unifilar lumpability controlled Markov chains; (5) Hankel operator AAK approximation of automata; (6) synchronizing automata reset words Moore refinement; (7) active learning halving mistake bounds; (8) predictive-state KL aggregation; (9) individual-sequence lossy compression; (10) comparative unification of approximation guarantees; (11) commitment and state complexity; (12) spectral learning of weighted automata; (13) epsilon-machine minimality and statistical complexity; (14) price of safety; (15) exact-phrase search for the manuscript's title concepts; (16) information bottleneck and lumpability; (17) streaming lower bounds for prediction; (18) Fisher information lower bounds for KL reduction; (19) controlled Markov information bottleneck; (20) communication complexity of automata minimization. Result sets are stored under scripts/novelty_search/ (files q01-q20) for reproducibility."
));
bodyChildren.push(body(
  "Two limitations should be stated plainly. First, the assessment is based on titles, snippets, and abstract-level knowledge of the returned literature, not on full-text reading of every hit; the findings below therefore carry the confidence level of a thorough literature scan rather than a systematic survey. Second, the open-web index weights recent and well-linked sources; very recent arXiv preprints that are not yet indexed or discussed anywhere could be missed. For a journal submission, a complementary arXiv full-text search on the exact terms 'unifilar lumpability', 'commitment gap', 'retention gap', and 'grounding gap' is recommended; this report already ran phrase-level searches for the headline terms and found no collisions."
));

// ---- 3. The Manuscript's Core Contributions ----
bodyChildren.push(h1("3. The Manuscript's Core Contributions, Distilled"));
bodyChildren.push(body(
  "To make the comparison concrete, the manuscript's claims were distilled into ten contributions. C1: a typed variational schema in which every regime gap has the form Delta_T(M) = inf over budget-M feasible B of L(delta, B), with a regime-specific feasible class (right congruences for commitment, lumpable or unifilar-lumpable quotients for retention, finite-rank or Hankel-restricted operators for grounding). C2: the commitment regime, with the Myhill-Nerode index as the exact zero threshold and a distributional commitment gap (ComRD) whose zero threshold is characterized by a pair-based one-step determination index kappa_pair. C3: the retention regime, with a full-KL retention gap over quotient machines, an observable support index kappa_obs, spectral tail converses via Ky Fan, and Fisher covariance expansions. C4: the grounding regime, with Hankel-structured rank-M gaps, an Adamjan-Arov-Krein-type equality in the one-letter case, a multiletter extension, and computable finite-section certificates. C5: protocol stratification (reset word, persistent stream, active query) with reset-word realizable mistake complexity Theta(M log M) and an unconditional Theta(M log M) active attainment bound by a halving learner. C6: independence of the three regime obstructions. C7: the seven-coordinate type discipline for approximation statements. C8: a Price of Safety in mutual-information form. C9: NP-hardness and decidability results for retention decisions with rational certificates. C10: the comparative state-complexity sandwich and interaction results tying the regimes together."
));
bodyChildren.push(body(
  "The v3 revision strengthens two of these claims in ways relevant to novelty. The A1 correction replaces a mischaracterized class-level threshold with the pair-based determination index kappa_pair, which is now defined and separated from both kappa_obs and kappa_det by explicit counterexamples (identity transduction, XOR with alternating support); no prior occurrence of a determination-index ladder of this shape was found in the search. The A4 correction grounds the alpha-to-infinity vertex limit in the standard sandwiched-Renyi literature with explicit citations, which moves that specific claim from 'derivation' to 'transport of a known result', an honest and referee-safe position."
));

// ---- 4. Prior Art by Regime ----
bodyChildren.push(h1("4. Prior Art by Regime"));

bodyChildren.push(h2("4.1 Commitment: Myhill-Nerode, state complexity, communication complexity"));
bodyChildren.push(body(
  "The Myhill-Nerode theorem is classical, and its use as a minimality and zero-threshold certificate for deterministic acceptors is textbook material. Active recent literature uses the Nerode index as a complexity measure for ordering regular languages (D'Agostino, 'Ordering regular languages and automata: Complexity', 2023) and generalizes the Myhill-Nerode characterization to weighted and generalized automata (Cotumaccio, STACS 2024). None of this literature treats the Nerode index as the budget coordinate of a rate-distortion problem over transductions, and none introduces a determination-index ladder (kappa_pair below kappa_obs below kappa_det) with separation counterexamples. Communication complexity is a mature field with approximation-norm lower-bound frameworks (Lee, Shraibman, and others), and 'atomic commitment' in the distributed-database sense (Wolfson, 1989) is unrelated terminology. The manuscript's commitment games (Com, ComRD, ComGame) as strategic and distributional gaps on transductions have no direct match found; the nearest neighbor conceptually is the state-complexity literature, which counts states rather than quantifying commitment cost."
));

bodyChildren.push(h2("4.2 Retention: computational mechanics, bottleneck methods, lumpability"));
bodyChildren.push(body(
  "This is the regime with the closest prior art. Causal states and epsilon-machines (Crutchfield and Young 1989; Shalizi and Crutchfield, 'Computational Mechanics: Pattern and Prediction') define the minimal sufficient statistic for prediction, and the causal-state construction is exactly the zero-retention optimum of the manuscript's full-KL gap. Still and Crutchfield explicitly connected information bottlenecks, causal states, and statistical complexity, and Still's later causal rate-distortion work ('Causal Rate-Distortion for Infinite-Order Markov Processes', arXiv 1412.2859) studies rate-distortion under a causal constraint, which is the closest published framing to the manuscript's title concept. On the aggregation side, Geiger's 'Optimal Kullback-Leibler Aggregation via Information Bottleneck' (arXiv 1304.6603) reduces regular Markov chains in KL optimality, and the 2026 survey 'Information-theoretic reduction of Markov chains' consolidates that line; classical lumpability (strong and weak, exact and ordinary) is decades old, and recent work extends it to uncertain chains (Cardelli) and block-model aggregation (Faccin et al., PRL 2021)."
));
bodyChildren.push(body(
  "Against this background, the manuscript's specifically new objects are: the controlled, input-driven extension (retention of an input-output channel rather than of an output process), in which the feasible class is the unifilar-lumpable quotients of a controlled unifilar machine rather than arbitrary partitions; the budget-M gap curve rather than the optimum alone; the spectral tail converse (eigenvalue tails of the Fisher covariance via Ky Fan) as a lower bound certificate for the gap; and the explicit type separation between input-driven lumpability and unifilar lumpability with the warning that unifilarity is not automatic. The phrase 'unifilar lumpability' itself returned no matches anywhere in the open-web index, which supports the coinage being new. The still-unresolved overlap risk is positioning: a referee from the computational-mechanics community will ask how the retention chapter relates to causal states and to Still's causal rate-distortion, and the current bibliography, which cites Tishby, Bialek, and Shalizi, does not yet contain those two anchors."
));

bodyChildren.push(h2("4.3 Grounding: Hankel, AAK, and spectral minimization of automata"));
bodyChildren.push(body(
  "The Adamjan-Arov-Krein theory of optimal Hankel-norm approximation is classical (1971) and is the backbone of model reduction in control theory. A modern and directly relevant line applies it to automata: Balle and Giraud, 'Optimal Spectral-Norm Approximate Minimization of Weighted Finite Automata' (ICALP 2021), the follow-up 'Optimal Approximate Minimization of One-Letter Weighted Finite Automata' (2023, arXiv 2306.00135), and the Lacroce PhD thesis (McGill) all recast approximate minimization of weighted automata as low-rank approximation of infinite Hankel matrices solved by AAK theory; the companion 'Singular Value Automata' line (Balle et al.) builds the SVD-based tractable theory, and spectral learning of weighted automata (Balle, Rabusseau, and colleagues, NeurIPS 2012 onward) is an established adjacent field. This is the closest modern prior for the manuscript's grounding regime, and it is currently absent from the manuscript's bibliography."
));
bodyChildren.push(body(
  "The differentiators the manuscript can legitimately claim are: the transduction (input-output channel) object rather than a weighted language; the explicit regime split between unrestricted finite-rank relaxation (where Eckart-Young-Mirsky applies) and Hankel-restricted relaxation (where AAK applies), with the warning that the two feasible sets differ; the multiletter case, where the published one-letter AAK-for-automata results do not directly transfer, and the manuscript's multiletter extension and its scope caveats appear to go beyond the published state; the grounded finite-section certificates with explicit lower bounds; and the zero-threshold characterization rank(H) <= M. The one-letter results, by contrast, substantially coincide with the published Balle-Giraud-Lacroce line and should be positioned as transport rather than as new."
));

bodyChildren.push(h2("4.4 Protocols: synchronization, reset words, and active learning"));
bodyChildren.push(body(
  "Synchronizing automata and the Cerny conjecture are a major classical field: reset words, reset thresholds, the NP-completeness of shortest-reset-word decision problems (Markey and others), and randomized analyses of short synchronizing words. Moore's partition-refinement underlies both minimization and separation arguments, and the M-1 separating-word bound the manuscript's A6-corrected proof now cites is standard. On the learning side, the halving algorithm's log2|H| mistake bound and Littlestone's winnow analysis are textbook; Angluin's L* and its descendants dominate exact active automata learning, with recent lower-bound work (Kruger et al., 'Lower Bounds for Active Automata Learning', 2023) and surveys of the active automata learning literature; Freund's 1997 work on learning typical finite automata and mistake-bounded learning of automata is the closest classical neighbor to the manuscript's mistake-complexity accounting."
));
bodyChildren.push(body(
  "What the search did not find is the manuscript's specific protocol stratification: the distinction between machine-specific synchronization depth (a search in the target's pair automaton) and universal decision-tree depth (one fixed tree against every machine), the separation of the two at M = 2, the persistent-stream never-reset adversary with its transport-plus-readout construction and Omega(M log M) forced mistakes, and the unconditional active Theta(M log M) attainment with no synchronizability or direct-sum hypothesis. These composites are assembled from standard parts, but the accounting framework and the exact statements appear new. The nearest terminology collision is 'synchronization depth' in the distributed-systems sense, which is unrelated."
));

// ---- 5. Verdict table ----
bodyChildren.push(h1("5. Novelty Verdict by Contribution"));
bodyChildren.push(body(
  "The table below rates each distilled contribution on a four-level scale. High means no prior art was found that states or closely anticipates the claim. Moderate-High means the components are known but the specific composite statement was not found. Moderate means substantial adjacent literature exists and the claim's novelty rests on the unified accounting. Incremental means the claim coincides in substance with published results and should be positioned as transport. The ratings reflect the search evidence of Section 2 and the per-regime findings of Section 4, not a full-text verification of every candidate paper."
));
const verdictRows = [
  ["C1", "Typed variational schema across three regimes", "High", "No prior unified schema found; regime-specific schemas exist separately"],
  ["C2", "Myhill-Nerode zero threshold + ComRD + kappa_pair", "Moderate-High", "Nerode threshold classical; ComRD games and the determination-index ladder not found"],
  ["C3", "Controlled full-KL retention + unifilar lumpability", "Moderate-High", "Closest neighbors: Still-Crutchfield, Geiger, classical lumpability; controlled + unifilar form new"],
  ["C4", "Hankel-restricted grounding + multiletter AAK", "Moderate", "One-letter case published (Balle-Giraud-Lacroce); multiletter extension and certificates go beyond"],
  ["C5", "Protocol-stratified mistake complexity Theta(M log M)", "Moderate-High", "Halving, L*, sync words classical; stratified accounting and persistent-stream adversary not found"],
  ["C6", "Independence of regime obstructions", "High", "No prior cross-regime independence theorem found"],
  ["C7", "Seven-coordinate type discipline", "High", "No prior type-signature discipline for approximation statements found"],
  ["C8", "Price of Safety in mutual-information form", "Moderate-High", "Term unclaimed in this sense; safety-game and ML-safety literatures are unrelated neighbors"],
  ["C9", "NP-hardness + decidability of retention decisions", "Moderate", "Hardness of clustering-style reductions is folklore-adjacent; the typed decision problems are specific"],
  ["C10", "Comparative sandwich + interaction results", "Moderate-High", "No prior sandwich tying the three regime gaps found"],
];
bodyChildren.push(new Paragraph({
  keepNext: true,
  spacing: { before: 120, after: 60 },
  children: [new TextRun({ text: "Table 1. Novelty verdict by distilled contribution", bold: true, size: 21, color: P.secondary, font: EN_FONT })],
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
        cell("ID", { bold: true, fill: "EEF2F6", w: 7 }),
        cell("Contribution", { bold: true, fill: "EEF2F6", w: 32 }),
        cell("Novelty", { bold: true, fill: "EEF2F6", w: 14 }),
        cell("Evidence", { bold: true, fill: "EEF2F6", w: 47 }),
      ],
    }),
    ...verdictRows.map(r => new TableRow({
      cantSplit: true,
      children: [
        cell(r[0], { w: 7 }),
        cell(r[1], { w: 32 }),
        cell(r[2], { w: 14, bold: true }),
        cell(r[3], { w: 47 }),
      ],
    })),
  ],
}));

// ---- 6. What is genuinely new ----
bodyChildren.push(h1("6. What the Search Supports as Genuinely New"));
bodyChildren.push(body(
  "Four items survive the search with no found prior art at all, and they should lead the novelty claim in any submission cover letter. First, the comparative syntax itself: one resource (the index of a finite right congruence on histories) shared by three semantic categories, with the negative results (independence theorem, absence of universal cross-regime inequalities) that make the comparison informative rather than merely notational. Second, the type discipline of Section 17, which turns the paper's own central failure mode, the silent reuse of a statement proved in one regime inside another, into a checkable signature; nothing similar was found in the automata-learning, model-reduction, or computational-mechanics literatures. Third, the determination-index ladder kappa_pair, kappa_obs, kappa_det with its separation counterexamples, which the v3 revision makes precise. Fourth, the protocol stratification of realizable mistake complexity, in particular the machine-specific versus universal synchronization-depth distinction and the persistent-stream lower bound."
));
bodyChildren.push(body(
  "Two further items are new as composites but should be claimed carefully. The Price of Safety is a new coinage with no competing occupant found, but its substance is a gap identity between an exact quantity and a surrogate, and referees from the formal-methods community may read it as an abstraction-gap statement unless the mutual-information form is foregrounded. The multiletter AAK extension is the most technically exposed novelty claim: the published AAK-for-automata results are one-letter, the multiletter setting is genuinely harder (the manuscript's own remark on the free monoid carrying no shift of multiplicity one), and if the manuscript's multiletter theorem is correct it is ahead of the published literature; this claim above all others deserves a careful self-contained proof check before submission, since no external corroboration exists to lean on."
));

// ---- 7. Overlap risks and citation gaps ----
bodyChildren.push(h1("7. Overlap Risks and Citation Gaps"));
bodyChildren.push(body(
  "The following works are the closest conceptual neighbors found and are not currently cited in the manuscript's bibliography. Adding them would not weaken the novelty claim; it would sharpen it, because each citation marks the boundary between the known component and the manuscript's new composite. The first gap is the most important: Still and Crutchfield's line connecting information bottlenecks, causal states, and statistical complexity, and Still's causal rate-distortion, are the nearest published antecedents of both the retention regime and the paper's title concept, and their absence would be the first thing a referee from the computational-mechanics community notices. The second is Geiger's Kullback-Leibler-aggregation line, which is the nearest neighbor of the full-KL retention problem over quotients. The third is the Balle-Giraud-Lacroce approximate-minimization line, the nearest neighbor of the grounding regime. The fourth is the active-automata-learning lower-bound literature, which is where a referee would look for prior art on the protocol chapter. The fifth, softer, is the individual-sequence lossy-compression tradition (Ziv-Lempel models, Merhav's 2024 revisit), which shares the 'finite-state machines distorting individual sequences' flavor of the commitment regime."
));
bodyChildren.push(srcLine(
  "Still & Crutchfield, 'Information Bottlenecks, Causal States, and Statistical Complexity'; Still, 'Causal Rate-Distortion for Infinite-Order Markov Processes'",
  "https://arxiv.org/abs/1412.2859"));
bodyChildren.push(srcLine(
  "Geiger et al., 'Optimal Kullback-Leibler Aggregation via Information Bottleneck' (arXiv 1304.6603); 'Information-theoretic reduction of Markov chains' (2026 survey)",
  "https://arxiv.org/pdf/1304.6603"));
bodyChildren.push(srcLine(
  "Balle & Giraud, 'Optimal Spectral-Norm Approximate Minimization of Weighted Finite Automata' (ICALP 2021); Balle et al. one-letter AAK (arXiv 2306.00135)",
  "https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2021.118"));
bodyChildren.push(srcLine(
  "Lacroce, PhD thesis, 'The approximate minimization problem of weighted finite automata' (McGill, 2022)",
  "https://claralacroce.github.io/static/LacroceClara_PhDthesis.pdf"));
bodyChildren.push(srcLine(
  "Kruger et al., 'Lower Bounds for Active Automata Learning' (COLT 2023)",
  "https://proceedings.mlr.press/v217/kruger23a/kruger23a.pdf"));
bodyChildren.push(srcLine(
  "Merhav, 'Lossy Compression of Individual Sequences Revisited' (2024); Vereshchagin & Vitanyi, 'Algorithmic Rate-Distortion Theory'",
  "https://arxiv.org/html/2401.01779v1"));
bodyChildren.push(body(
  "Two positioning sentences are recommended in the introduction. One should say that the retention regime extends the causal-state program from output processes to controlled, input-driven transductions, and that unlike the bottleneck-for-causal-states line the manuscript tracks the full budget-M gap curve with spectral lower certificates rather than only the optimum. The other should say that the grounding regime transports the AAK program for weighted automata from weighted languages to transductions, separates the unrestricted and Hankel-restricted feasible sets explicitly, and extends the one-letter published results to the multiletter setting. With those two sentences and the corresponding citations in place, the novelty claim of the framework becomes clean: nobody has unified these regimes, and the manuscript can prove the unification is nontrivial."
));

// ---- 8. Recommendations ----
bodyChildren.push(h1("8. Recommendations"));
bodyChildren.push(body(
  "First, add the six citations of Section 7 to the bibliography and the two positioning sentences to the introduction; this is a one-hour edit that removes the three largest referee risks found by the search. Second, foreground the four High-novelty items (comparative syntax with negative results, type discipline, determination-index ladder, protocol stratification) in the abstract and the cover letter, and state explicitly that the per-regime components are transports of known instruments into the unified accounting; claiming less makes the paper more credible. Third, subject the multiletter AAK theorem to a dedicated line-level proof check, since it is the one High-exposure technical claim with no external corroboration; the v3 revision's own history (the A1 correction) shows how a subtle threshold mischaracterization can survive self-review. Fourth, before submission, run an arXiv full-text search for the exact coinages ('unifilar lumpability', 'kappa_pair', 'commitment gap', 'retention gap', 'grounding gap', 'Price of Safety') to confirm continued non-collision; this report's open-web phrase searches found no collisions as of September 2026. Fifth, consider the venue implications: the manuscript's span (automata theory, information theory, operator algebra, online learning) exceeds the scope of most single journals, which suggests a general theoretical computer science venue with tolerance for long papers, or a split into two shorter papers, one for the framework and independence results, one for the protocol chapter."
));

// ---- 9. Search result inventory ----
bodyChildren.push(h1("9. Search Result Inventory"));
bodyChildren.push(body(
  "The twenty result sets are stored as JSON under scripts/novelty_search/ with the file names q01 through q20, ten results each, in execution order. The most consequential hits, beyond those already cited in Section 7, are inventoried below by family, so that a later reader can retrace the assessment without re-running the searches. Computational mechanics: Shalizi and Crutchfield's 'Computational Mechanics: Pattern and Prediction' (arXiv cond-mat/9907176) and the epsilon-machine explainer literature, including the 'emic' software line; these define the retention regime's classical optimum. Aggregation: Faccin et al., 'State Aggregations in Markov Chains and Block Models' (PRL 2021); Cardelli's lumpability for uncertain chains; weak-lumpability analyses; and the Markov-state-space-aggregation-via-IB line. Hankel and spectral: Adamyan-Arov-Krein's original 1971 article; Balle-Rabusseau 'Singular Value Automata and Approximate Minimization' (arXiv 1711.05994); spectral learning of general weighted automata (NeurIPS 2012). Synchronization: the Cerny-conjecture literature, shortest-sync-word algorithms, and the NP-completeness of bounded reset-word decision. Learning: halving-algorithm mistake-bound lecture notes (Princeton, UPenn), Freund's 1997 typical-automata paper, and the active-automata-learning survey repository. Rate-distortion: the Wikipedia survey article, phase-transition connections to deep learning (Grohs et al.), rate-distortion generalization bounds (Sefidgaran et al., 2022), and the individual-sequence tradition."
));
bodyChildren.push(body(
  "Search executed September 2026 through the aggregated web-search backend; result sets frozen under scripts/novelty_search/. This report was prepared against manuscript version v3 (automata_unified_revised_v3.tex, incorporating the A1 and B-series corrections of v2 and the A2-A6, C1, and bold-Sigma revisions of v3)."
));

// ================= ASSEMBLY =================
const coverConfig = {
  title: "Novelty Assessment Report",
  subtitle: "Deep web literature search on the core contributions of 'The Rate-Distortion Theory of Bounded Sequential Transduction'",
  englishLabel: "LITERATURE SCAN",
  metaLines: [
    "Object: automata_unified_revised_v3.tex (framework, regimes, protocols, type discipline)",
    "Method: 20 targeted web queries across 8 literature families, 200 results screened",
    "Verdict: framework-level novelty High; three citation gaps to close before submission",
    "Date: September 2026",
  ],
  footerLeft: "Novelty assessment of the comparative finite-state approximation framework",
  footerRight: "automata_unified_revised_v3.tex",
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
      heading3: {
        run: { font: HEAD_FONT, size: 24, bold: true, color: P.primary },
        paragraph: { spacing: { before: 220, after: 100, line: 312 } },
      },
    },
  },
  sections: [
    // Section 1: Cover (margin 0, no footer)
    {
      properties: {
        page: { size: { width: 11906, height: 16838 }, margin: { top: 0, bottom: 0, left: 0, right: 0 } },
      },
      children: buildCoverR1(coverConfig),
    },
    // Section 2: TOC (roman numerals)
    {
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
    // Section 3: Body (arabic, restart at 1)
    {
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
          children: [new TextRun({ text: "Novelty Assessment - automata_unified_revised_v3.tex", size: 16, color: P.secondary, font: EN_FONT })],
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
  fs.writeFileSync("/home/z/my-project/download/novelty_assessment_automata_unified.docx", buf);
  console.log("WROTE docx, bytes:", buf.length);
});
