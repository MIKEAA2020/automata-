# arXiv Posting Notes — v8 Preprint

The venue decision (see the repository's `coinage_search_venue_decision.docx`)
directs that an arXiv preprint be posted **before** the journal submission,
to timestamp the coined vocabulary and the multiletter-AAK theorem while the
review cycle runs. This folder contains the ready-to-upload source bundle.

## The bundle

`arxiv_source_v8.tar.gz` — one file, upload as-is:

```
automata_unified_revised_v8.tex   # the complete, self-contained source
anc/supplementary_v8/             # ancillary files (NOT compiled by arXiv)
```

The manuscript source is fully self-contained: no `\input`, no `\include`,
no graphics, and the 39-entry bibliography is embedded as `thebibliography`
directly in the file, so no `.bbl` or `.bib` is needed. It compiles cleanly
with Tectonic 0.15.0 (238 pages, 0 errors, 0 undefined references, the 9-box
overfull baseline documented for v8); the package set is standard
(`amsmath`, `amssymb`, `amsthm`, `mathtools`, `bm`, `enumitem`, `booktabs`,
`array`, `geometry`, `parskip`, `xcolor`, `microtype`, `hyperref`) and is
pdfLaTeX-compatible.

Everything under `anc/` follows arXiv's ancillary-files convention: it is
attached to the preprint as downloadable ancillary material and is not part
of the compiled document. Its contents are exactly the journal-facing
supplementary package (verification suite, enumeration programs, machine
tables, exact outputs, Lean 4 development with build script and axiom-audit
gate), so the manuscript's Data and Code Availability statement holds
verbatim for the preprint.

## Metadata to enter in the submission form

**Title** (must match the manuscript exactly):

```
The Rate--Distortion Theory of Bounded Sequential Transduction:
A Comparative Syntax for Finite-State Approximation
```

(Enter the two lines as one title; arXiv preserves the line break if pasted
with it, but a single joined line is also fine.)

**Abstract**: paste the abstract of the manuscript verbatim (LaTeX math such
as `$M$` is accepted in arXiv abstracts). Source: `automata_unified_revised_v8.tex`,
the `abstract` environment immediately after `\maketitle`.

**Categories** (suggestion; primary first):

- `cs.FL` (Formal Languages and Automata Theory) — primary; the automata and
  transduction core.
- `cs.IT` / `math.IT` (Information Theory) — the rate-distortion framework,
  the information-bottleneck decomposition, the determination-index ladder.
- `stat.ML` (or `cs.LG`) — the mistake-bound and regret results on the
  temporal axis, and the Price-of-Safety surrogate.

**Comments** (suggestion):

```
238 pages; the supplementary verification package (numerical suite,
enumeration programs, machine tables, and the Lean 4 development) is
attached as ancillary files
```

**License**: the default arXiv non-exclusive license is sufficient; choose
another only deliberately. Do not enter a journal reference or DOI now —
those are added after acceptance.

## Sequencing (per the venue decision)

1. Personalize the author block first (see `SUBMISSION_NOTES.md`, Section 3):
   the preprint PDF should not ship with an empty `\author{}`. The
   personalization creates a new version file (v9) under the standing
   version-freeze policy; rebuild this tarball from v9 afterwards with:

   ```
   tar czf arxiv_source_v9.tar.gz automata_unified_revised_v9.tex anc/
   ```

   (copy v9's `.tex` into a staging directory together with `anc/` from this
   bundle, then run the command from that directory).

2. Post the preprint. Coinage clearance was verified on 2026-09-02; the
   clearance and the priority stamp are perishable, so posting should not
   wait on the journal.

3. Submit to Information and Computation (see `SUBMISSION_NOTES.md`), citing
   the preprint identifier in the cover letter's arXiv sentence.
