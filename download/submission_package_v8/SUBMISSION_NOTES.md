# Submission Package — Information and Computation (v8)

This package assembles everything needed to submit the manuscript to
**Information and Computation** (primary venue) and to post the **arXiv
preprint** first, per the venue decision recorded in
`coinage_search_venue_decision.docx` (Section 7: single submission; primary
venue Information and Computation, exact scope match, no stated page limit;
backup Theory of Computing; arXiv preprint posted immediately).

The package is built on **`automata_unified_revised_v8.tex`**, the current
latest version (238 pages, 18 sections, 390 theorem-like environments of
which 141 carry proofs, 509 labels, 39-entry embedded bibliography,
back-matter Notation Index). Under the standing version-freeze policy, v7
and earlier are frozen and byte-unchanged; nothing in this package modifies
any frozen file.

## 1. Contents

| Path | Role | Editorial Manager file role |
|------|------|------------------------------|
| `cover_letter/cover_letter.tex` + `.pdf` | cover letter (2 pages), drafted per the venue report's Section 7 guidance | Cover Letter |
| `manuscript/automata_unified_revised_v8.tex` + `.pdf` | the manuscript; the PDF in this folder was recompiled from the `.tex` in this folder during packaging (integrity check: 238 pages, 0 errors, 0 undefined references, the documented 9-box overfull baseline) | Manuscript |
| `supplementary/` | the journal-facing supplementary package: verification suite (41 checks), enumeration programs, machine tables, exact outputs, and the Lean 4 development (17 statements, 7 modules, build script + axiom-audit gate). Exactly the material the manuscript's Data and Code Availability statement enumerates | Supplementary Material |
| `supplementary_v8.zip` | the same supplementary package, zipped for upload | Supplementary Material (upload this) |
| `optional_editor_material/aak_multiletter_proof_check.docx` | line-level proof check of the multiletter-AAK material | Optional: upload as a supplementary file if attaching the verification evidence (recommended by the venue report) |
| `optional_editor_material/remaining_theorems_proof_check.docx` | line-level proof check of the remaining 135 theorems | Optional, same as above |
| `arxiv/arxiv_source_v8.tar.gz` + `ARXIV_NOTES.md` | the ready-to-upload arXiv source bundle and its metadata notes | — (arXiv, not the journal) |
| `highlights.txt` | optional Elsevier highlights (5 bullets, ≤85 characters each) | paste into the form's Highlights field if present |

Internal documents (novelty assessment, venue decision, review reports) are
deliberately **not** included in this package so they cannot be uploaded by
mistake; they remain in the repository's `download/` directory.

## 2. What was verified at packaging time (2026-09-02)

- The manuscript source is fully self-contained (no `\input`, no
  `\include`, no graphics, embedded `thebibliography`) — verified by scan.
- The package's manuscript PDF was compiled from the package's manuscript
  source with Tectonic 0.15.0: exit 0, 238 pages, 0 errors, 0 undefined
  references, overfull boxes equal to the documented v8 baseline (9 stable
  boxes at identical positions and magnitudes).
- The supplementary copy is byte-identical to the repository's
  `supplementary/` (programs, machine tables, outputs, lean), verified by
  MD5 spot checks and a full file-set comparison (43 files, identical).
- `supplementary_v8.zip` is entry-for-entry identical to the
  `supplementary/` folder (43/43).
- The cover letter compiles cleanly (2 pages) and passed PDF QA (metadata,
  fonts embedded, no overflow, symmetric margins, no blank pages).
- The arXiv tarball contains exactly the main `.tex` plus `anc/` with the
  same supplementary file set (54 entries).

## 3. Personalization protocol (do this before anything else)

The manuscript ships with an empty `\author{}` (and `\date{}`), and the
cover letter ships with bracketed placeholders. Under the version-freeze
policy, filling the author block is a manuscript edit and therefore creates
a **new version file**:

1. `cp automata_unified_revised_v8.tex automata_unified_revised_v9.tex`
   (work from the repository's `download/` directory).
2. In v9, fill `\author{}` with your name and affiliation in the format
   Information and Computation expects (name, department, institution,
   city, country; keep `\date{}` empty or set it), and update the
   availability/acknowledgment back matter if your funding status differs
   from the declared "no funding".
3. Recompile: `tectonic automata_unified_revised_v9.tex` — expect the same
   238 pages, 0 errors, 0 undefined references. Adding only an author block
   cannot shift theorem numbering or labels.
4. Replace `manuscript/` in this package with v9's `.tex` and `.pdf`, and
   rebuild the arXiv tarball from v9 (commands in
   `arxiv/ARXIV_NOTES.md`).
5. Fill the cover letter placeholders: `[Author Name]`,
   `[Department, Institution]`, `[City, Country]`,
   `[email@institution.edu]` — four sites: the letterhead, the closing
   signature, and the `\pdfauthor` metadata. Adjust the arXiv sentence
   ("will be posted") if the preprint is already posted, then recompile
   `cover_letter.tex`.

## 4. Upload order in Editorial Manager

1. **Cover Letter** — `cover_letter.pdf` (or paste its text into the cover
   letter field and attach the PDF).
2. **Manuscript** — `manuscript/automata_unified_revised_v9.tex` and the
   compiled `.pdf` (after Section 3). The source uses only standard
   pdfLaTeX-compatible packages; it was compiled here with Tectonic 0.15.0.
3. **Supplementary Material** — `supplementary_v8.zip` (rebuilt from v9's
   supplementary if you changed anything else).
4. Optional — the two proof-check reports from `optional_editor_material/`
   (the venue report recommends attaching them as evidence of verification
   depth; they are not required by the journal).
5. If the form has a Highlights field — `highlights.txt`.

Declarations are already handled: funding and competing interests are
stated in the manuscript's back matter, and the generative-AI declaration
is in "Acknowledgments and Declaration of Generative AI". Editorial Manager
will also ask you to complete its declaration-of-interests form; the answer
consistent with the manuscript is "no competing interests".

## 5. The one open editorial decision

The venue report (Section 4.4) leaves one citation decision open: whether
to cite arXiv 2608.12791 ("Thermodynamics of Learning"), a contemporaneous
neighboring accounting framework, in the introduction's positioning
paragraph. This package **does not** cite it — the report's assessment is
that not citing it carries no referee risk today, since no coinage or
theorem overlaps, while citing it sharpens the boundary between the
manuscript's comparative rate-distortion program and a value-accounting
program. If you decide to cite it, that is a v9/v10 edit under the
version-freeze policy; the insertion site is the introduction's
positioning paragraph.

## 6. If the outcome is a rejection

The pre-planned contingencies (venue report, Section 7):

- **Length- or scope-driven desk rejection** — execute the two-paper split:
  the protocols paper (temporal axis plus Price of Safety, compressed
  toward 50 pages) to a standard venue; the framework paper to Theory of
  Computing (the backup no-limit, free open-access venue).
- **Both venues desk-reject on length** — the fallback is a structural
  compression pass targeting 140–160 pages as a new version file, not a
  third venue.

Both paths are analyses of the same measured line counts stored in the
repository; no decision needs to be re-derived.
