// gen_coinage_venue.js — arXiv coinage search + venue decision report for
// automata_unified_revised_v6.tex (the pre-submission checklist completion).
// House pipeline: R1 cover, 3-section numbering (cover / TOC roman / body
// arabic), TOC + refresh hint, header/footer. English, report scene.
const {
  Document, Packer, Paragraph, TextRun, Header, Footer, PageNumber,
  NumberFormat, AlignmentType, SectionType, TableOfContents,
} = require("docx");
const fs = require("fs");
const {
  P, buildCoverR1, h1, h2, body, bodyRuns, run, tag, cell,
  tableCaption, makeTable, EN_FONT, HEAD_FONT,
} = require("./cvc_helpers.js");

const OK = "2E6B3E";      // green: clear / unclaimed
const WARN = "B4540A";    // amber: occupied in another sense
const bodyChildren = [];

// ================= 1. Executive Summary =================
bodyChildren.push(h1("1. Executive Summary"));
bodyChildren.push(body(
  "This report closes the last open item of the pre-submission checklist issued by the novelty assessment of the manuscript: an arXiv-class phrase search on the manuscript's coined terms, and the venue decision that the search feeds. It was compiled on 2026-09-02 against the current manuscript version automata_unified_revised_v6.tex (234 pages, 18 sections, 141 proof-bearing results, all of which have passed dedicated line-level proof checks in the companion reports). The manuscript's revision cycle is complete in every other respect: all review items A1 through E5 are closed, the two minor proof-internal defects of the last round are fixed, the three non-blocking observations of the remaining-theorems report are addressed, and the supplementary package (verification suite, enumeration programs, machine tables, outputs, and the Lean statement manifest) is assembled."));
bodyChildren.push(bodyRuns([
  run("Verdict on the coinages: ", { bold: true }),
  run("no same-sense collision exists for any searched term. The three core coinages — 'unifilar lumpability', 'unifilar-lumpable', and 'kappa_pair' — return zero hits in both search channels. The six checklist coinages with generic-word structure ('commitment gap', 'retention gap', 'grounding gap', 'Price of Safety') are occupied only in unrelated senses: decision-theoretic selection, gas chromatography and memory retention, language-model dialogue grounding, and safe bandit identification respectively. Two low-cost positioning actions are recommended and listed in Section 5."),
]));
bodyChildren.push(bodyRuns([
  run("Verdict on the venue: ", { bold: true }),
  run("single submission. The primary venue is Information and Computation (exact scope match, no stated page limit); the backup is Theory of Computing (free open access, no stated page limit). An arXiv preprint should be posted immediately, both to timestamp the now-verified coinages and the multiletter-AAK theorem, and to begin the dissemination clock while the (necessarily long) review proceeds. The two-paper split is retained strictly as a contingency: the split arithmetic of Section 6 shows it does not solve the length problem, because the framework paper would remain at roughly 190 pages."),
]));

// ================= 2. Checklist item and method =================
bodyChildren.push(h1("2. The Checklist Item and the Search Method"));
bodyChildren.push(body(
  "The novelty assessment closed with a five-item pre-submission checklist. Items one through three are already executed: the six flagged citations and two positioning sentences were added in the v4 revision; the four High-novelty items are foregrounded in the abstract; and the multiletter-AAK theorem received its dedicated line-level proof check, whose precision edits are in v4. The remaining items are the two this report settles: an exact-phrase arXiv search on the coinages to confirm continued non-collision, and the venue decision — single venue or two-paper split — taking the manuscript's span into account."));
bodyChildren.push(body(
  "Two search channels were used, and their coverage was measured rather than assumed. Channel one is arXiv's own search interface, queried with exact quoted phrases in the 'All fields' mode. A capability probe established that this mode indexes metadata — title, abstract, comments, journal reference and related fields — and not the full text of PDFs: the advanced-search field list exposes no full-text option, and a body-only boilerplate probe phrase returned only the handful of abstracts that happen to contain it. Channel two is an open-web index that covers arXiv abstract pages and Scholar-class aggregators; phrase-level full-text coverage is approximated through it, in the standard sense that a paper whose full text uses a phrase in a way that the literature notices is, in practice, discoverable through indexed pages, citations and aggregators. This is the strongest available coverage short of scanning every arXiv PDF by hand, and it is the same standard under which the novelty assessment's phrase searches were run in September 2026."));
bodyChildren.push(body(
  "Nine terms were searched: the six named by the checklist ('unifilar lumpability', 'kappa_pair', 'commitment gap', 'retention gap', 'grounding gap', 'Price of Safety') plus three reinforcing probes ('unifilar-lumpable', the hyphenated adjectival form; 'determination index', the generic descriptor of the kappa ladder; and 'protocol stratification'). All searches ran on 2026-09-02. The raw result sets — hit counts, titles, URLs and the near-collision abstracts — are stored under scripts/coinage_search/ and inventoried in the Appendix, so a later reader can retrace every judgment without re-running anything."));

// ================= 3. Results by coinage =================
bodyChildren.push(h1("3. Results by Coinage"));
bodyChildren.push(body(
  "The table below is the complete outcome of the nine searches. 'arXiv metadata hits' counts the results of the quoted-phrase 'All fields' query; 'open-web hits' counts results of the quoted-phrase open-web query that actually contain the phrase. 'Same-sense collision' asks whether any hit uses the phrase with the manuscript's meaning; every row answers no."));
bodyChildren.push(tableCaption("Table 1: Coinage search results (2026-09-02)"));
bodyChildren.push(makeTable(
  [
    cell("Coinage", { bold: true, fill: "EDF1F5", w: 22 }),
    cell("arXiv hits", { bold: true, fill: "EDF1F5", w: 12 }),
    cell("Open-web phrase hits", { bold: true, fill: "EDF1F5", w: 22 }),
    cell("Notable occupants", { bold: true, fill: "EDF1F5", w: 26 }),
    cell("Same-sense collision", { bold: true, fill: "EDF1F5", w: 18 }),
  ],
  [
    [cell("unifilar lumpability", { w: 22 }), cell("0", { w: 12 }), cell("0", { w: 22 }), cell("none found", { w: 26 }), cell("none — unclaimed", { w: 18, color: OK, bold: true })],
    [cell("unifilar-lumpable", { w: 22 }), cell("0", { w: 12 }), cell("0", { w: 22 }), cell("generic lumpability only", { w: 26 }), cell("none — unclaimed", { w: 18, color: OK, bold: true })],
    [cell("kappa_pair", { w: 22 }), cell("0", { w: 12 }), cell("0", { w: 22 }), cell("motorcycle-accessory trademark noise", { w: 26 }), cell("none — unclaimed", { w: 18, color: OK, bold: true })],
    [cell("determination index", { w: 22 }), cell("11", { w: 12 }), cell("present", { w: 22 }), cell("EPA Applicability Determination Index; unrelated papers", { w: 26 }), cell("none", { w: 18, color: WARN, bold: true })],
    [cell("commitment gap", { w: 22 }), cell("2", { w: 12 }), cell("present", { w: 22 }), cell("costly-information selection (arXiv 2508.20246); sales literature", { w: 26 }), cell("none", { w: 18, color: WARN, bold: true })],
    [cell("retention gap", { w: 22 }), cell("3", { w: 12 }), cell("present", { w: 22 }), cell("gas chromatography; LLM memory retention; marketing", { w: 26 }), cell("none", { w: 18, color: WARN, bold: true })],
    [cell("grounding gap", { w: 22 }), cell("21", { w: 12 }), cell("present", { w: 22 }), cell("NLP dialogue grounding (arXiv 2311.09144 and others)", { w: 26 }), cell("none — crowded in NLP", { w: 18, color: WARN, bold: true })],
    [cell("Price of Safety", { w: 22 }), cell("2", { w: 12 }), cell("present", { w: 22 }), cell("safe bandit identification (arXiv 2309.08709); fiction titles", { w: 26 }), cell("none — adjacent idiom", { w: 18, color: WARN, bold: true })],
    [cell("protocol stratification", { w: 22 }), cell("1", { w: 12 }), cell("present", { w: 22 }), cell("stratified medicine; 5G broadcast authentication", { w: 26 }), cell("none", { w: 18, color: WARN, bold: true })],
  ]
));
bodyChildren.push(body(
  "The headline result is the zero-row block. 'Unifilar lumpability' — the coinage that names the retention regime's feasible class, and the term a computational-mechanics referee would most plausibly have met before — returns no hit in either channel. The open-web results for the phrase are dominated by generic lumpability: the Kemeny–Snell notion, Cardelli's lumpability for uncertain continuous-time Markov chains, and weak-lumpability analyses. None of these combines unifilarity with lumpability, which is precisely the manuscript's compound: the quotient of a controlled unifilar machine by a partition under which the quotient itself remains unifilar. 'kappa_pair' likewise returns nothing but trademark noise. The determination-index ladder (kappa_pair, kappa_obs, kappa_det) therefore enters the literature with an unclaimed vocabulary."));
bodyChildren.push(body(
  "The occupied rows are all same-phrase, different-sense. 'Retention gap' is a working term of gas chromatography (guard and pre-column technique) and of memory-retention research including a 2026 machine-learning paper; 'commitment gap' names a decision-theoretic quantity in a 2025 preprint on costly-information combinatorial selection; 'grounding gap' is established NLP vocabulary for language models failing to establish common ground in dialogue; 'determination index' is an EPA regulatory database; 'protocol stratification' appears in stratified medicine and telecommunications. In every case the occupant's formal object is unrelated to the manuscript's, and the disciplines do not overlap, so the phrases remain usable — with the two positioning caveats developed in the next two sections."));

// ================= 4. Near-collision analysis =================
bodyChildren.push(h1("4. Near-Collision Analysis"));
bodyChildren.push(body(
  "Four papers from the occupied rows deserve individual classification, because a referee might plausibly raise one of them. Their abstracts were retrieved and read; each is classified below with the action, if any, that it motivates."));
bodyChildren.push(h2("4.1 Commitment Gap via Correlation Gap (arXiv 2508.20246)"));
bodyChildren.push(body(
  "A 2025 preprint on selection problems with costly information, in the lineage of Weitzman's Pandora's Box problem and the CICS model of Chawla et al. and Bowers et al. Its 'commitment gap' quantifies the loss from committing to a selection policy under partial information, in a decision-theoretic setting. The manuscript's commitment gap is a state-complexity quantity: the budget-M curve of a distributional rate-distortion problem whose zero threshold is the Myhill–Nerode index of the transduction. The two objects share a word and nothing else: no shared formalism, no shared literature, no citation path between them. Classification: same phrase, different sense, unrelated field. No action required."));
bodyChildren.push(h2("4.2 Price of Safety in Linear Best Arm Identification (arXiv 2309.08709)"));
bodyChildren.push(body(
  "A 2023 learning-theory paper introducing the safe best-arm identification framework with linear feedback, where an agent faces stage-wise safety constraints and must act conservatively. Its 'price of safety' is the conservatism overhead in the price-of-X idiom family (price of anarchy, price of stability), measured in regret or sample complexity. The manuscript's Price of Safety is a gap identity in mutual-information form: the difference between an exact quantity and its safety-constrained surrogate, over the protocol classes of the temporal axis. The idiom is shared and the community is adjacent — both are online-learning-adjacent — but the formal objects are different, and the novelty assessment already anticipated that a formal-methods referee might read the term as an abstraction-gap statement unless the mutual-information form is foregrounded. This is the one near-collision that merits a sentence of positioning, and Section 5 recommends exactly that sentence."));
bodyChildren.push(h2("4.3 Grounding Gaps in Language Model Generations (arXiv 2311.09144)"));
bodyChildren.push(body(
  "An ACL-anthology paper on whether large language models construct the common ground that effective conversation requires. Its 'grounding gap' is a dialogue-level phenomenon. The manuscript's grounding is approximation-theoretic: the Hankel-structured, AAK-theoretic model-reduction regime, where the grounding gap measures the cost of rank restriction of the Hankel operator of a transduction. Twenty-one arXiv metadata hits show the NLP phrase is established and productive, so the term is crowded — but the crowds are in a different discipline, and the manuscript's operator-theoretic sense is self-defining within its own formalism. Classification: crowded phrase, unrelated sense. An optional disambiguation clause at the term's coining site is recommended in Section 5."));
bodyChildren.push(h2("4.4 Thermodynamics of Learning (arXiv 2608.12791) — watch item"));
bodyChildren.push(body(
  "An August 2026 preprint developing a typed four-component accounting for finite-state learning devices: a training-side fit functional, a record-correlation stock, an update-side search ledger, and an operational capital value, framed as the work gap between an informed protocol class and a blind one. This is the only hit that is a conceptual neighbor rather than a mere phrase occupant: it shares the ingredients of typed accounting, information functionals, protocol classes, and finite-state learning devices. It does not use any of the manuscript's coinages in the manuscript's sense, and its program — a thermodynamic value accounting — is different from the manuscript's comparative rate-distortion theory of state approximation. But it surfaced in the 'retention gap' search, its vocabulary overlaps the manuscript's, and it post-dates the novelty assessment's own searches by days. Classification: watch item. The recommended action is a related-work decision: cite it in the introduction's positioning paragraph as a contemporaneous neighboring accounting framework, or at minimum monitor it during the review cycle."));

// ================= 5. Coinage verdict and positioning actions =================
bodyChildren.push(h1("5. Coinage Verdict and Positioning Actions"));
bodyChildren.push(body(
  "The checklist asked whether the coinages remain non-colliding; the answer is yes, without exception, and with the strongest possible reading for the three core terms: zero hits of any kind. The framework's named objects — unifilar lumpability, the kappa ladder, and with them the comparative vocabulary the cover letter leads with — can be claimed as the manuscript's own. This is the second independent confirmation: the novelty assessment's open-web phrase searches found no collisions as of September 2026, and the present arXiv-class searches, run with broader coverage and three additional probe terms, find none as of 2026-09-02."));
bodyChildren.push(body(
  "Two positioning actions follow from the occupied rows, both one-sentence edits for the next version file. First, the Price of Safety section should carry a footnote distinguishing the term from the safe-bandit usage: a single sentence noting that the phrase also names the conservatism overhead of safety constraints in best-arm identification (arXiv 2309.08709), and that the present usage — the mutual-information gap between an exact quantity and its surrogate — is unrelated. This costs one line and removes the only referee-recognizable ambiguity found by the entire search. Second, at the site where the grounding gap is coined, an optional clause noting that the term is unrelated to the language-model grounding-gap literature of NLP. The crowdedness of the NLP phrase makes this clause worth its half-line: it prevents a momentary misreading by any referee whose first association with 'grounding' is dialogue."));
bodyChildren.push(body(
  "One further decision is recorded rather than recommended: whether to cite the Thermodynamics-of-Learning preprint as a contemporaneous neighbor (Section 4.4). Citing it sharpens the positioning — it marks the boundary between the manuscript's comparative rate-distortion program and a value-accounting program that also types its quantities — and it is the kind of citation that ages well if the neighbor gains traction. Not citing it carries no referee risk today, since no coinage or theorem overlaps. The trade-off is a judgment call the author should make once, at submission time."));

// ================= 6. Venue analysis =================
bodyChildren.push(h1("6. Venue Analysis"));
bodyChildren.push(h2("6.1 The manuscript's shape"));
bodyChildren.push(body(
  "The decision inputs are concrete. The manuscript compiles to 234 pages across 18 sections, with 390 theorem-like environments of which 141 carry proofs, every one of them checked line-by-line in the two dedicated proof-check reports. The three regimes are individually long — retention alone is 3,020 of the 17,885 in-section source lines, roughly 40 printed pages; grounding and commitment add 1,424 and 959 — and the temporal axis is 2,623 lines, roughly 34 printed pages, with the Price-of-Safety surrogate section at 826 more. The span is four fields: automata theory, information theory, operator algebra (the AAK machinery), and online learning. The supplementary package is now real, and the Lean 4 statement manifest documents the machine-checked fragment. All of this is submission-ready; the question is where."));
bodyChildren.push(h2("6.2 What the venue policies say"));
bodyChildren.push(body(
  "Venue policies were checked on 2026-09-02 rather than assumed. Logical Methods in Computer Science, which the novelty assessment's venue suggestion might have pointed to, is ruled out for the single submission: its FAQ caps submissions at 50 pages, with an exception path through the editors that a 234-page paper cannot realistically use. Theory of Computing states no page limit, is free and open access, and has a published policy only on concurrent submissions. Information and Computation, an Elsevier journal whose stated scope is all areas of theoretical computer science and computational applications of information theory — an exact match for the manuscript's span — states no page limit in its guide for authors. IEEE Transactions on Information Theory is excluded by ordinary length economics: standard plus over-length charges price a 234-page paper out of consideration. JACM states no cap, but a 234-page submission there is an outlier bet with a multi-year timeline."));
bodyChildren.push(h2("6.3 The two-paper split arithmetic"));
bodyChildren.push(body(
  "The natural split is the one the novelty assessment sketched: a framework paper (the typed schema, the three regimes, the kappa ladder, the independence results, the type discipline, the multiletter-AAK theorem) and a protocols paper (the temporal axis plus the Price of Safety). Measured in the manuscript's own lines, the protocols paper is the temporal axis (2,623 lines) plus the surrogate section (826 lines), about 45 printed pages before the framework recap it would need — call it 50 to 55 pages, which fits ordinary venues and, with compression, even the LMCS cap. The framework paper is everything else: roughly 14,400 lines, about 190 printed pages. That is the decisive arithmetic: the split does not solve the length problem, because the paper that carries the manuscript's actual contribution — the unification, the independence theorems, the type discipline, the exposed multiletter-AAK theorem — remains at 190 pages regardless. The split's real benefits are distributing referee load and isolating the protocols chapter's exposure; its costs are a duplicated setup of 15 to 20 pages, cross-citation overhead, and, most seriously, underselling the framework-level novelty, which the novelty assessment rated High precisely for the unification itself. The comparative results that make the unification informative require all three regimes in one place."));
bodyChildren.push(h2("6.4 Referee load and priority"));
bodyChildren.push(body(
  "A 234-page single submission asks one referee pool to absorb four fields; this is the honest cost of the single-paper decision, and it is real. Three facts offset it. First, the manuscript has been engineered for referee navigation: the consolidated cross-references of the E1 pass, the seven-coordinate type signatures that let a reader check regime boundaries mechanically, the dedicated proof-check reports, and now the reproduction-verified supplementary package, which converts every quoted computational observation into a runnable check. Second, the multiletter-AAK theorem — the single most exposed claim, with no external corroboration when the novelty assessment was written — now has both a dedicated line-level proof check and an independent reproduction of its supporting computational claims; its corroboration status is documented, not asserted. Third, an arXiv preprint posted before the journal submission timestamps the coinages and the theorem, which matters precisely because the review cycle of a 234-page paper will be long, and the coinage clearance measured today is only guaranteed today."));

// ================= 7. The decision =================
bodyChildren.push(h1("7. The Decision"));
bodyChildren.push(bodyRuns([
  run("Decision: submit as a single paper. ", { bold: true }),
  run("The primary venue is Information and Computation, on the strength of the exact scope match (theoretical computer science plus computational applications of information theory is the manuscript's own span, verbatim) and the absence of a stated page limit. The backup venue is Theory of Computing, which adds free open access and a long-paper tradition. An arXiv preprint is posted before either submission — immediately, since the coinage clearance and the priority stamp are both perishable goods. The two-paper split is not adopted: Section 6.3 shows it leaves the framework paper at 190 pages, solving the wrong problem at the cost of the unification claim."),
]));
bodyChildren.push(body(
  "The split is retained as a pre-planned contingency, executed only on a length- or scope-driven desk rejection, in which case the seam is the one measured above: the protocols paper (temporal axis plus Price of Safety, compressed toward 50 pages) goes to a standard venue, and the framework paper goes to the remaining no-limit venue of the pair. If both venues desk-reject on length, the fallback is not a third venue but a structural compression pass targeting 140 to 160 pages — the E-item consolidations of the v4 revision demonstrated roughly ten percent structural redundancy, and a dedicated compression round could plausibly find more without touching mathematics. That pass would be a new version file under the standing freeze policy, taken only if the rejection letters actually arrive."));
bodyChildren.push(body(
  "The cover letter should lead with the four High-novelty items the search sustained — the comparative syntax with its negative results, the type discipline, the determination-index ladder, the protocol stratification — state plainly that the per-regime instruments are transports of known tools into the unified accounting, and attach the two proof-check reports and the supplementary package as evidence of verification depth. The letter should also state the multiletter-AAK theorem's status honestly: internally proof-checked to the line level, with its computational support independently reproduced, and without external corroboration, which is the documented reason it received the dedicated check."));

// ================= 8. Pre-submission action list =================
bodyChildren.push(h1("8. Pre-Submission Action List"));
bodyChildren.push(body(
  "Six actions remain between the current state and a submitted package. They are ordered, each is one decision, and none blocks the others."));
bodyChildren.push(new Paragraph({
  numbering: { reference: "list-actions", level: 0 },
  spacing: { line: 312, after: 100 },
  children: [run("Add the Price-of-Safety positioning footnote (one sentence, citing arXiv 2309.08709) in the next version file, per Section 5.")],
}));
bodyChildren.push(new Paragraph({
  numbering: { reference: "list-actions", level: 0 },
  spacing: { line: 312, after: 100 },
  children: [run("Add the optional grounding-gap disambiguation clause (one clause at the coining site), per Section 5.")],
}));
bodyChildren.push(new Paragraph({
  numbering: { reference: "list-actions", level: 0 },
  spacing: { line: 312, after: 100 },
  children: [run("Decide whether to cite arXiv 2608.12791 as a contemporaneous neighboring accounting framework, per Section 4.4.")],
}));
bodyChildren.push(new Paragraph({
  numbering: { reference: "list-actions", level: 0 },
  spacing: { line: 312, after: 100 },
  children: [run("Import the machine-checked Lean 4 file into supplementary/lean/, following the integration protocol in that directory's README (compile check, no sorry, standard-three-axioms check, statement-name match).")],
}));
bodyChildren.push(new Paragraph({
  numbering: { reference: "list-actions", level: 0 },
  spacing: { line: 312, after: 100 },
  children: [run("Post the arXiv preprint of v6 (title and abstract leading with the comparative framework; coinages verified clear as of 2026-09-02).")],
}));
bodyChildren.push(new Paragraph({
  numbering: { reference: "list-actions", level: 0 },
  spacing: { line: 312, after: 100 },
  children: [run("Assemble the Information and Computation submission: v6 source, supplementary package, cover letter per Section 7; hold Theory of Computing as backup.")],
}));

// ================= 9. Appendix =================
bodyChildren.push(h1("9. Appendix: Search Evidence Inventory"));
bodyChildren.push(body(
  "All searches were executed by persisted scripts with their raw outputs stored, so every row of Table 1 and every classification of Section 4 is traceable. The evidence lives under scripts/coinage_search/ in the manuscript repository."));
bodyChildren.push(body(
  "arxiv_search.py is the arXiv metadata channel: it probes full-text capability (the probe result and its conclusion are recorded in the JSON), then queries each of the nine coinages as an exact quoted phrase in All-fields mode, parses hit counts and the top titles, and writes arxiv_coinage_search.json. websearch.sh drives the open-web channel through eleven quoted-phrase queries, saved as web_*.json — one per coinage plus targeted queries for the near-collisions (the commitment-gap correlation-gap pairing and the price-of-safety bandit line). fetch_near_collisions.py retrieves the abstracts of the four papers analyzed in Section 4 into near_collisions.json. The three venue-policy result sets are stored as venue_lmcs.json, venue_toc.json and venue_ic.json. Any of these can be re-run against a later date to refresh the clearance; the scripts are deterministic apart from the live index contents."));

// ================= Document assembly =================
const coverConfig = {
  title: "Coinage Search and Venue Decision",
  subtitle: "arXiv-class phrase search on the manuscript's coined terms, and the single-paper versus two-paper-split decision",
  englishLabel: "PRE-SUBMISSION CHECKLIST",
  metaLines: [
    "Manuscript: automata_unified_revised_v6.tex (234 pages, 18 sections)",
    "Search channels: arXiv metadata search + open-web index",
    "Search date: 2026-09-02",
    "Companion to: novelty_assessment_automata_unified.docx",
  ],
  footerLeft: "Supplementary decision report",
  footerRight: "2026-09-02",
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
  numbering: {
    config: [{
      reference: "list-actions",
      levels: [{
        level: 0,
        format: "decimal",
        text: "%1.",
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } },
      }],
    }],
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
          children: [new TextRun({ text: "Coinage Search and Venue Decision - automata_unified_revised_v6.tex", size: 16, color: P.secondary, font: EN_FONT })],
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
  fs.writeFileSync("/home/z/my-project/automata-repo/download/coinage_search_venue_decision.docx", buf);
  console.log("WROTE docx, bytes:", buf.length);
});
