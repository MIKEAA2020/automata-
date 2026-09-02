# Open questions queue

Decisions parked for you. Nothing here is blocking — I'll keep assessing new
versions and adding to this file. Answer any of them whenever convenient, in
any order; several may resolve themselves as more versions arrive.

Status key: **OPEN** = needs your call · **DEFERRED** = waiting on more versions ·
**RESOLVED** = settled (kept for the record)

---

## Q1 — The `∼_δ ⊆ ∼` interaction conflict *(RESOLVED — v5 settled it)*

**Resolved by `automata_lean_v5`, and my turn-5 recommendation was WRONG.**

I had recommended restoring the two-sided `∼_δ ⊆ ∼ ⊆ ∼_com` form. v5 shows
that is incorrect as a *constraint*:

> A joint machine may **split** a causal state in order to carry commitment
> information. Exact commitment constrains **histories**, not predictive laws,
> so the machine state need not be a function of `S`.

Imposing `∼_δ ⊆ ∼` would wrongly shrink the feasible set and **overstate**
`M_joint`. The base's one-sided `∼ ⊆ ∼_com` was right all along.

**Action taken:** kept the one-sided form; added `rem:no-lower-constraint`
recording that `∼_δ ⊆ ∼` is *sufficient* (it makes `K_∼` a quotient of `S`)
but not imposable, plus the correct general history-factor formulation
`Δ_ret^safe(M) = I(S;Z) − sup_K I(K;Z)`.

---

## Q2 — The six tables *(OPEN)*

`glued 6` has `tab:proven-open-1`, `tab:proven-open-2`, `tab:schatten-template`,
`tab:oracle-budget-laws`, `tab:spectral-tail`,
`tab:exponent-vertex-correspondence` (~590 lines). These are the tables the
**original audit was written against**.

The current base presents the same material as **itemized lists**. Restoring
the tables means either replacing those lists or duplicating the content.

Note: `tab:proven-open-2` would still need the audit item 2 Oracle row
("Matching minimax lower bound … Open / conditional") added — `glued 6` never
had it.

**Options:** (a) tables replace the lists · (b) keep lists, no tables ·
(c) tables in an appendix, lists stay inline.

---

## Q3 — The Local Fisher upgrade *(RESOLVED — spliced; `lem:fisher-uniform-expansion` and `cor:fisher-uniform-remainder` are both in the manuscript)*

`glued 6` has a 341-line "Local Fisher Asymptotics" subsection containing
`lem:fisher-uniform-expansion` + `cor:fisher-uniform-remainder`: a **uniform**
second-order mixture-KL expansion with explicit `L³` and third-order remainder
control. The base states only a pointwise local Fisher theorem
(`thm:local-fisher`, line ~2629).

Both flagged dependency-safe. Genuinely stronger mathematics, but large, and
splicing risks duplicating the existing theorem.

**Options:** (a) splice in, subordinating the existing theorem · (b) skip ·
(c) wait for a version that already integrates it cleanly.

---

## Q4 — Target audience / venue *(DEFERRED — affects Q2 and Q5)*

Journal submission, arXiv preprint, or internal reference? This drives how much
recap/summary/tabulation to keep. `glued 6` is expansive (130 pp); the base is
leaner (120 pp). Not urgent, but it settles several presentation questions at once.

---

## Q5 — Summary + numerical subsections *(DEFERRED)*

`glued 6` has ~12 `subsec:*-summary` recap subsections and 3 "Numerical"
subsections (~98 lines). The numerical ones contain **caveats only**
("simulations cannot prove the theorem") — no actual numbers. Low risk, modest
value; may read as redundant. Depends largely on Q4.

---

## Q6 — Should `\GrdHank` be retired? *(RESOLVED — macro deleted; zero uses remain)*

The legacy macro `\GrdHank` is still defined in the preamble but now unused,
since audit item 6 split it into `\Dunres` / `\DHankstr`. Harmless, but dead.

**Options:** (a) delete it · (b) keep for compatibility with older drafts.

---

## Q7 — Presentation of the restored length bound *(OPEN — trivial)*

I restored the `O(M log M + \Lsync)` upper bound as a **`proposition`**
(`prop:active-length-upper`) to signal it is subordinate to
`thm:active-certified`. `glued 6` states the equivalent as a **`theorem`**
(`thm:active-realizable`).

**Options:** (a) leave as proposition · (b) promote to theorem.

---

## Q8 — Which branch's hypothesis style wins? *(PARTLY RESOLVED — the `thm:interaction-complexity` rationality qualifier was applied in T40; the broader style question remains deferred)*

On ~10 shared statements the base states a hypothesis explicitly where
`glued 6` leaves it implicit (e.g. the oracle corollaries name the estimation
rate `Est_M(T)` as a premise; `glued 6` assumes it silently).

I've been preferring the **explicit** form, consistent with the audit's intent.
Flagging in case you want the terser style for readability.

One place `glued 6` is strictly better and I recommend adopting regardless:
`thm:interaction-complexity` says **"For rational data"** — a qualifier an
NP-hardness claim genuinely needs. *(Low risk; say the word and I'll apply it.)*

---

## Q11 — Citation density *(RESOLVED — all 28 bibitems now cited; `sakarovitch2009` and `boucheron2013` anchored in T40)*

Fixing the base's attribution gap this turn raised usage from 7 to **16** of
30 bibitems. Still uncited: `berstel2011`, `chatterjee2012`, `cover`,
`crutchfield1989`, `crutchfield2003`, `hsu2012`, `jaeger2000`, `lm`, `paz1971`,
`ramadge1989`, `sakarovitch2009`, `shalizi2001`, `shapley1953`, and others —
mostly background references with no inline anchor.

**Options:** (a) I place them at the obvious topical anchors (causal
states → `crutchfield1989`/`shalizi2001`; weighted automata → `berstel2011`;
supervisory control → `ramadge1989`; stochastic games → `shapley1953`) ·
(b) prune the unused entries · (c) leave as-is.

---

## Q9 — Streaming lower bound *(RESOLVED — proved in turn 10)*

Closed by `thm:stream-lower-bound`: an explicit transport-plus-readout
adversary forces `Ω(M log M)` on a single never-reset stream, so
`thm:passive-realizable` and `thm:agnostic` are now `Θ`. Superseded text below.

### Original question

v5 argues the `Ω(M log M)` **lower** bound does not transfer automatically from
reset-word VC bounds to a single persistent stream (no resets, dependent
rounds). I added `rem:streaming-lower-scope` flagging this, but left
`thm:passive-realizable` stating `Θ(M log M)`.

**Options:** (a) keep `Θ` + caveat *(current)* · (b) weaken the theorem to
`O(M log M)` upper + `Ω` for the reset protocol only · (c) supply the
in-stream mistake-tree construction.

---

## Q10 — Should the lean v5 rewrite become the base? *(OPEN — structural)*

v5 is a ~50 KB / ~1900-line condensed rewrite: same architecture, **zero
labels**, no tables, ~50 formal statements vs. the base's ~312. It is a
deliberate *distillation*, not a draft.

It is more careful in places (see corrections applied this turn) but drops the
Schatten template detail, exponent-vertex development, appendices, changelog,
and most remarks.

**Options:** (a) keep the full base, port v5's corrections *(current)* ·
(b) make v5 the base and port the full version's depth back in · (c) maintain
both as "full" and "letter" versions.

*Relates closely to Q4 (venue).*

---

## Answered along the way

- **Is `glued 6` worth merging?** Yes — ~90% shared ancestry, and the unique
  content is complementary (`glued 6` = exposition/tables/worked instances;
  base = explicit hypotheses/epistemic hygiene). *(turn 5)*
- **Which file should be the base?** The corrected one. Merging *into*
  `glued 6` would silently undo audit items 6 and 7 and re-loosen ~10
  hypotheses. *(turn 5)*
- **Where was the audit's "Oracle block"?** In `glued 6` — the only version with
  the `tab:proven-open-*` tables. *(turn 5)*
- **Q1, the `∼_δ` conflict.** Settled by v5 **against** my recommendation: the
  one-sided form is correct; `∼_δ ⊆ ∼` is sufficient, not imposable. *(turn 7)*


## Q12 — Split into a focused retention paper? *(RESOLVED — keep unified, option (b))*

The audit recommends extracting a narrower paper — *Finite-State Information
Bottlenecks: Spectral Converses, Sharp Global Bounds, and Computational
Hardness* — around: the lumpable IB identity, the sharp constant-1 global
converse, the interior Fisher converse, the boundary impossibility theorem,
Gaussian quadratic NP-completeness, full-KL promise-NP-hardness, and the
zero-retention threshold; relegating the categorical schema, grounding/AAK,
commitment games, online oracle theory, active learning, and Price of Safety.

This is an editorial decision with no mathematical content, so I have **not**
actioned it. All seven proposed core results now exist and are proved in the
current manuscript, so the split is a matter of cutting, not writing.

- **(a)** Split now — produce the focused paper as a second deliverable.
- **(b)** Keep the unified manuscript; revisit after referee reports.
- **(c)** Keep unified but move the six named areas to appendices.

### Decision (this session, user-delegated): keep unified — option (b)

Asked directly whether the paper is coherent enough to merit single
publication or should be split. Verdict: **coherent enough for one paper.**
Grounds, in order of weight:

1. **The boundary cuts through the theory, not around it.** The split-safety
   analysis above stands: 70 residual items cite into the core, and the whole
   unifilar layer depends on core results. The two papers would be a technical
   core and its framing, not two independent contributions — a split that
   weakens both while doubling the referee surface.
2. **The coherence evidence is strong.** Uniform schema-to-instantiation
   architecture across all 18 sections; one type discipline (§16) governing
every statement; zero duplicate labels; every repeated environment title
cross-referenced; the five-part review verdict on flow was "seamless"; the
327-flag audit left 0 genuine register defects. A paper that needs splitting
shows seams — this one shows a single spine (the schema) with regime
instantiations.
3. **The length objection is already absorbed.** Information and Computation
   accepts long papers; the arXiv preprint establishes priority for the
   multiletter-AAK theorem regardless. Section balance (Q13b) reflects where
   the mathematics is, not disorder.

The split remains what the venue decision already made it: a desk-rejection
contingency, with option (c) (six areas to appendices) as the intermediate
fallback. No content was moved for Q12.

### Split-safety analysis (added T47; decision now recorded)

`tools/partition.py` computes, for any proposed core, the transitive
dependency closure, the residual, the bridge items, and — the binding
constraint — whether `core ∪ residual` covers every labelled environment.
Validated: full seed ⇒ residual 0; empty seed ⇒ core 0; coverage holds on
random seeds.

Run against the audit's seven named results (13 labels):

| quantity | value |
|---|---|
| labelled environments | 360 |
| seed (thematically chosen) | 13 |
| **core after dependency closure** | **38** |
| bridges (pulled in, not chosen) | 25 |
| residual (second paper) | 322 |
| residual items citing into core | 68 |
| coverage | **360/360 complete** |

Two findings bear on the decision.

**The core is not self-contained as named.** Closing under `\ref` alone gives
21 items, but that undercounts: every core theorem uses *lumpable*, `\RetKL`,
`\Splus` and *mixture centroid* in prose without citing the defining
environment. Tracking those definitional dependencies raises the core to 38 and
the bridges from 8 to 25. The bridges include `def:controlled-markov`,
`def:lumpable-quotient`, `prop:lumpability`, `def:full-kl-retention`,
`def:gaussian-quadratic`, `lem:mixture-centroid`, `lem:kmeans-gap` and
`lem:fractional-kmeans` — i.e. the machine model, the feasible-set definition
and the two `k`-means lemmas must travel with the extracted paper. A split that
copies only the seven named results would produce a paper whose statements do
not typecheck.

**Sixty-eight residual items cite into the core.** These become cross-paper
references. Notably the whole unifilar layer (`cor:controlled-fisher`,
`cor:controlled-simplex-general`, `prop:refinement-extremal`,
`rem:complexity-transfer`) depends on core results, so the audit's proposed
boundary cuts *through* the retention theory rather than around it.

No content is lost under this split provided the 25 bridges are carried and the
back-references are converted to citations. That is the condition to enforce,
whichever option is chosen. Re-run after T48/T50: 363 environments, core 38,
bridges 25, residual 325, cross-references 70, coverage complete.

### Bearing of the third audit (T50)

The third audit confirms the rejection of the rate–distortion redefinition and
adds a checkable claim, that convexity in `R = M` is coincidental rather than a
theorem. Tested and correct: a rational witness (`|S|=4`, `|O|=3`, weights
`(17,18,22,21)`) is non-convex under **both** `R = M` and `R = log M`, so no
reparameterisation rescues the Shannon reading. Recorded in
`rem:rd-nonconvex-mechanism`.

This bears directly on Q12. Every result the unification rests on —
`meta:typed-rate-distortion`, `thm:unified`, `def:response`,
`thm:independence`, `thm:schatten-nogo`, `def:state-rate`, `prop:rd-nonconvex`,
`rem:vertex-two-ingredients` — lies in the **residual**, not the core. The
extracted retention paper would therefore contain none of the unification
apparatus, and the residual paper would retain all of it while depending on 70
core results for its retention instance.

That is an argument against splitting on this boundary, though not against
splitting as such: the two papers would not be independent contributions but a
technical core and its framing, separated. Options (b) keep unified and (c)
appendices both avoid this; option (a) is coherent only if the retention paper
is presented as self-contained and the framework paper cites it.


---

## Q13 — Structural reorganization? *(RESOLVED in v9 — (a) moved; (b) no action)*

Raised T56 after a structural scan. Two findings, of very different weight.

### (a) A genuine misplacement — RESOLVED (v9, option (a))

**Action taken:** the five-environment block (`rem:unifilar-feasibility`,
`prop:unifilar-lumpability`, `rem:unifilar-converse-hypothesis`,
`prop:input-driven-specialization`, `rem:epsilon-machine-relation`) moved from
§9 *Type-Correct Axes on One Clock* to §3 *Stationary Controlled Causal
Machines*, immediately after `ex:onestep-not-congruence` and before the
*Full-KL Retention Gap* subsection. All nine machine-model environments now
form one run in §3, roughly 2,500 lines ahead of the theory
(`subsec:unifilar-retention` in §5) that depends on them; the ordering
inversion is gone. The two residual dependencies the simulated repair
predicted (`rem:complexity-transfer`, `subsec:retention-complexity`) remain
benign roadmap-style pointers, as predicted. v9 verification: 509 labels, 0
duplicates, 0 undefined refs, theorem-environment count identical to v8 (no
renumbering), overfull baseline = v8's nine boxes at identical magnitudes
plus one new 0.9pt reflow transient, 239 pp.

The original finding, kept for the record:

The unifilar **machine model** — `def:unifilar-machine`,
`rem:unifilar-proper-subclass`, `def:unifilar-lumpable`,
`rem:unifilar-support-not-automatic`, `rem:unifilar-feasibility`,
`prop:unifilar-lumpability`, `rem:unifilar-converse-hypothesis`,
`prop:input-driven-specialization`, `rem:epsilon-machine-relation` — sits in
§9 *The Two-Axis Oracle Inequality*, subsection *Type-Correct Axes on One
Clock*, at lines 8592–8880.

The unifilar **theory built on it** — `def:controlled-full-kl`,
`thm:controlled-ib`, `thm:controlled-zero`, `prop:refinement-extremal` — sits
in §5 *Retention* at lines 4466–4970.

So the theory precedes its own machine model by **3,622 lines**, and every use
is a forward reference. This is a genuine ordering inversion, not a matter of
taste: the block was placed where it was because T36 introduced it as a scope
note about terminology, and T39–T44 then grew a full theory in §5 that depends
on it.

Measured cost: of 36 body forward references spanning more than 2,000 lines,
**11 are into this block** — the largest single contributor.

Simulated repair (move the block to just before
`subsec:unifilar-retention`): total forward references 197 → 194, and only
two residual dependencies remain, `rem:complexity-transfer` and
`subsec:retention-complexity`, both benign pointers that would become ordinary
forward references of the roadmap kind.

The modest headline reduction is itself informative: most forward references
are short-range or come from the Introduction and Schema, where signposting is
normal and desirable. The defect is concentrated, not diffuse.

**Options:** (a) move the block to §5, immediately before the unifilar
retention subsection · (b) leave it and add an explicit pointer at first use ·
(c) leave as is. — **(a) applied in v9**, adapted to the current structure:
§3, where the other four model environments already live.

### (b) Section balance — a judgment call, not a defect

§5 Retention (2,983 lines, 64 environments) and §13 Temporal (2,605 lines, 60)
are each roughly four times the median section. That is a consequence of where
the mathematics actually is, and matches the depth asymmetry already noted; it
is not evidence of disorder. Splitting either would be the Q12 decision in a
different guise.

No other ordering inversion was found: 0 duplicate labels, 0 near-duplicate
paragraphs, every repeated environment title cross-referenced.

---

## Q14 — Cite arXiv 2608.12791? *(RESOLVED — cited in v9)*

Raised by the coinage search: the "retention gap" near-collision, recorded as
a monitor-only watch item in the venue report and as "not cited by default"
in SUBMISSION_NOTES. Decision, on direct user delegation: **cite it**, as a
disambiguation footnote at the phrase's first body occurrence (Introduction),
matching the pattern already used for "Price of Safety" (arXiv 2309.08709)
and "grounding gap" (arXiv 2311.09144). The footnote fixes this manuscript's
sense (state-compression cost: the `\RetKL(M)` of `def:full-kl-retention`,
its controlled relative, and the quadratic surrogate) against the
thermodynamics-of-learning sense (value-side `L_gen` for finite-state
learning devices under task-distribution shift).

Rationale: the two works are contemporaneous neighbors in spirit (typed
accounting for finite-state devices) but strangers in substance; an explicit
disambiguation pre-empts referee confusion, protects the coinage, and is the
honest-scholarship default. Verified against the live arXiv record before
insertion: A. Sudo, "Thermodynamics of learning: a typed four-component
accounting of memory, fit, and value," arXiv:2608.12791 [cond-mat.stat-mech],
2026. Bibliography 39 → 40 entries, every entry still cited exactly; the
SUBMISSION_NOTES "not cited by default" line is superseded by this entry.
