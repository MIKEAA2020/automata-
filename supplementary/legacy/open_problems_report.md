# Open Problems, Gaps, and Conjectures

**Companion report to** *The Rate–Distortion Theory of Bounded Sequential
Transduction: A Comparative Syntax for Finite-State Approximation*
(`automata_corrected.tex`, 143 pp., 44 theorems, 2 open-problem environments).

**Scope and status of this document.** This is an external research memorandum,
not part of the manuscript. Statements attributed to the manuscript are marked
*[M]* and are verifiable against it. Statements that are my own assessment —
severity ratings, effort estimates, and the suggested ordering in §8 — are
marked *[A]* and carry no authority beyond the reasoning given. The manuscript
itself assigns no severities and states no priorities.

---

## 0. Notation and terminology

### 0.1 Symbols

| Symbol | Meaning |
|---|---|
| `M` | state budget; index of a finite right congruence on histories |
| `I`, `O` | finite input and output alphabets; `Σ = I × O` |
| `I*` | free monoid of finite input histories |
| `∼_δ` | Nerode congruence of a residual trajectory `δ` |
| `S⁺` | stationary support `{s : π_s > 0}` |
| `π_s`, `Π_k` | stationary weight of state `s`; total weight of block `k` |
| `P_s`, `P̄_k` | predictive law of state `s`; block mixture centroid |
| `Δ_ret^KL(M)` | full-KL retention gap over lumpable quotients |
| `Δ_ret^quad(M)` | Gaussian fixed-covariance quadratic retention gap |
| `Σ_π` | stationary Fisher covariance |
| `Δ_grd^unres(M)` | unrestricted rank-`M` operator-approximation gap |
| `Δ_grd^Hank,str(M)` | Hankel-*structured* rank-`M` gap |
| `Δ_grd(M;γ)` | discounted symbolic gap over deterministic Mealy machines |
| `Δ_com(M)` | commitment gap; `0/1`-valued under normalized worst-case mismatch |
| `H_ν` | Hankel operator of the channel response, `H(u,v) = h(uv)` |
| `σ_i`, `λ_i` | singular values / eigenvalues, ordered nonincreasing |
| `κ_det(F)` | Myhill–Nerode index of specification `F` |
| `κ_obs(δ,μ)` | observable support index under history law `μ` |
| `A_T(M)`, `E_M(T)`, `Ψ_M(T)` | approximation deficit, estimation rate, aggregation penalty |
| `PoS_lin^loc`, `PoS_quad` | linear block-local and discrete Price of Safety |
| `E_sync(M)`, `L_sync(M)` | synchronization mistake complexity / experiment depth |
| `σ_γ(ν)` | discounted stochasticity coefficient |

### 0.2 Terms used in this report

- **Right congruence**: equivalence `∼` on `I*` with `u ∼ v ⟹ ux ∼ vx`. Its
  *index* is the number of classes, and equals a state count.
- **Mealy machine**: deterministic transducer emitting one output per input.
- **Lumpable quotient**: a map `φ : S⁺ → K` compatible with every
  positive-probability transition, so the quotient inherits a well-defined
  transition.
- **Causal / `Z`-predictive equivalence**: equality of `L(Z | S = s)`. Equals
  causal-state equivalence only when `Z` is the full future; for one-step `Z`
  it is strictly coarser and need not be a congruence (§5.6).
- **Realizable / agnostic**: target lies in the hypothesis class / need not.
- **Schatten-`p` norm**: `‖A‖_p = (Σ σ_i(A)^p)^{1/p}`; a *quasi*-norm for
  `p < 1`; `p = ∞` gives the operator norm; `p = 1` the nuclear norm.
  **Trace class** means `‖A‖_1 < ∞`.
- **Ky Fan `r`-norm**: sum of the `r` largest singular values.
- **Pinching**: `X ↦ Σ_b P_b X P_b` for a projection family; an average of
  unitary conjugations, hence spectrum-majorizing.
- **Hardy space `H²`**: boundary-value space on the disc in which classical
  Hankel operators act; **Nehari/AAK** are its norm and finite-rank
  approximation theorems.
- **Littlestone dimension**: depth of the deepest shattered *mistake tree*;
  the minimax realizable mistake bound.
- **Yao's principle**: a distribution over inputs lower-bounds randomized cost
  by the best deterministic cost against it. **Azuma–Hoeffding**: concentration
  for bounded martingale differences.
- **PFA / DFA**: probabilistic / deterministic finite automaton.
  **Isolated cutpoint**: acceptance probabilities bounded away from a threshold.
- **Weighted automaton**: `h(uv) = αᵀ T_u T_v η`, giving *algebraic* Hankel rank
  bounded by the state dimension — which does **not** imply boundedness on `ℓ²`.
- **Kantorovich–Rubinstein / Hamming distance**: here, discounted expected
  symbol disagreement, `Σ_t γ^{t-1} P(Y_t ≠ ŷ_t)`.
- **Fisher information**: curvature of the log-likelihood; `Σ_π` is its
  stationary covariance in natural coordinates.
- **Standardized cumulant**: normalized higher moment; boundedness controls the
  Taylor remainder in local expansions.
- **Frame-type bound**: a lower bound `‖measurement‖ ≥ c‖object‖`, used to
  transfer operator error to context error.
- **Simplex**: the probability simplex; "boundary" means some coordinate `→ 0`.

Three regimes recur: **commitment** (deterministic residual functions,
Myhill–Nerode), **retention** (predictive laws, information bottleneck), and
**grounding** (response operators, Eckart–Young–Mirsky).

---

## 1. Summary table

**Severity criterion.** *[A]* Several severity-B items also appear in the
abstract, so mere prominence is not the discriminator. The criterion used here
is what an unfavourable resolution would cost:

- **A** — an unfavourable resolution, or continued absence of a resolution,
  would require *withdrawing or materially weakening a stated theorem*. These
  are places where the manuscript asserts something whose support is either
  assumed (§2.3) or acknowledged as absent (§2.1, §2.2).
- **B** — limits the generality or reach of a result, but no stated theorem
  becomes false. The manuscript already scopes these correctly.
- **C** — refinement, terminology, or an avenue not pursued. Nothing depends
  on it.

Under this criterion §2.3 is severity A not because the oracle result is
prominent, but because a failure of the floors would leave
`thm:oracle-minimax-lower` with no verified instance in any regime.

The distinction between §2.3 (A) and items 12–14 (B) is worth stating, since
all three are "assumed, not discharged". Operational equivalence and the
succinctness family are hypotheses *named in the statements that use them*, so
a reader is never misled and the theorems remain true as stated. The separation
floors are also named — but they are the sole support for a two-sided
optimality claim, and unlike the other two there is no known instance
satisfying them. That is the difference.

Severity is my assessment *[A]*; the manuscript assigns none. The final column
gives the section of this report where the item is treated in full, so table
row numbers and section numbers need not coincide.

| # | Problem | Type | Sev. | Status | Treated in |
|---|---|---|---|---|---|
| 1 | Exact symbolic deterministic grounding gap | Open problem | **A** | Fully open; reducible | §2.1 |
| 2 | Intrinsic multi-alphabet Hankel equality | Open problem | **A** | Fully open (operator theory) | §2.2 |
| 3 | Verification of the oracle packing floor | Unverified hypothesis | B | **Two-point form disproved**; averaged form discharged for the realizable stream regime; sum-form envelope shown reachable from the min-form via the discrete sandwich (§2.31), leaving only removal of the `(1+kappa)` factor; other regimes open | §2.3, §2.23, §2.31, §4 |
| 4 | Necessity of the aggregation penalty `Ψ_M(T)` | Open problem | C | Partially closed: `Ω(√(T log M))` proved for arbitrary experts; **only the nested-class case is open** | §2.4 |
| 5 | Full-KL retention NP-hardness | Open problem | B | **Closed, and elevated to APX-hardness** (`thm:full-kl-promise-np`, `cor:full-kl-apx`): NP-hard for depth-one reset machines via a k-means→Jensen–Shannon tangent embedding; the embedding is approximation preserving, so no PTAS unless P=NP. Exact NP-**completeness** remains open (arithmetic of log-sums) | §2.5, §2.30 |
| 6 | Global full-KL converse under regularity | Quantitative open | **A** | **Fully settled, both charts.** Probability coordinates closed with the **sharp constant 1** (`thm:global-kl-simplex`, `prop:kl-simplex-sharp`); natural-parameter chart closed **negatively** (`thm:no-global-fisher-converse`), so interiority is necessary. No sub-question remains | §2.6 |
| 7 | Price-of-Safety signed discrepancy | Open problem | B | Reduced to a **two-sided** bound on `ρ_safe − ρ_free`; neither term has a determined sign (`ρ_safe(2) = −1/4`) | §2.7 |
| 8 | Domination bridges | Open problem | B | **Sharpened**: bridge ⇔ frame bound (`lem:frame-bridge`); no dimension-free Hankel bridge (`C_1, C_inf ≥ n`, `C_2 = √n`). Retention and grounding instances unaffected | §2.8 |
| 9 | Universal vs. machine-specific sync depth | Open problem | B | Gap size unknown | §2.8a |
| 9b | Active learning without synchronization | Open problem | C | **Largely closed**: halving attains (RI) in `O(M log M)` with no synchronization experiment; constant factor and agnostic case remain | §2.9 |
| 9c | State overhead of gating in the active protocol | Open problem | C | Gated family uses `2M` states to force `M log₂ M`; necessity of the factor 2 unknown | §2.9a |
| 10 | Hardy embeddings vs. default converse | Open problem | C | Scalar form of #2 | §2.10 |
| 11 | Intermediate Rényi orders `α ∉ {0,1,∞}` | Open problem | C | Conjectural | §2.11 |
| 12 | Operational-equivalence assumption | — | — | **Discharged**: a theorem for deterministic realizable classes (`lem:operational-equivalence`) | §2.24 |
| 13 | Regular bias–variance envelope | Unverified hypothesis | C | **No longer load-bearing**: the minimax proof now routes through the discrete sandwich lemma, which needs no continuity or exact crossing | §2.3, §4 |
| 14 | Bounded-error succinctness family | External dependency | B | Cited framework is real; the exact quantitative family is unverified | §4 |
| 15 | Cross-term conjectures C1–C4 | Conjecture | C | Explicitly conjectural | §3 |
| 16 | Spectral-tail principle | Heuristic | C | Not a theorem | §5.4 |
| 17 | Boundedness of formal Hankel matrices | Structural scope | C | Scoped, not characterized | §5.1 |
| 18 | Index-preserving extension off the support (`c_S = 0`?) | Open problem | C | Sandwich proved and **sharp**: explicit counterexample with `c_S = 1`; characterization open | §2.12 |
| 19 | Worst-case separating-word length across two machines | — | — | **Closed**: `2M−1` via Moore refinement on the disjoint union (`lem:moore-separation`) | §2.13 |

---

## 2. Fully open problems

### 2.1 Exact symbolic deterministic grounding gap — severity A

**Statement.** *[M]* Determine

```
Δ_grd(M;γ) = inf_{A det. Mealy, |S_A| ≤ M}  sup_x  d_KR,γ( ν | x , A(x) )
```

where `d_KR,γ` is the discounted Kantorovich–Rubinstein (Hamming) distance.

**Why it matters.** *[A]* This is the *only* one of the three regimes whose exact gap
is unknown. Commitment has the Myhill–Nerode threshold; grounding's *linear
relaxation* has `Δ_grd^unres(M) = σ_{M+1}(H_ν)` exactly. The symbolic
deterministic problem — the one an actual finite-state machine solves — has no
exact characterization.

**What is known.** *[M]* Three lower bounds, none tight:
1. the stochasticity floor `Δ_grd(M;γ) ≥ σ_γ(ν)`, positive exactly when some
   reachable history has a non-point-mass conditional output law;
2. the exponential determinism gap: low *algebraic* Hankel rank `k` is
   compatible with requiring `2^Ω(k)` deterministic states;
3. the unrestricted spectral bound, which does *not* transfer, since the
   feasible sets differ (deterministic machines vs. finite-rank operators).

**Suggested decomposition.** *[A]*
(a) exact Boolean realization (Myhill–Nerode minimization);
(b) *approximate* Boolean realization at worst-case per-step Hamming error `ε`
— the hard part, with no known clean theory;
(c) combination with the stochasticity floor, giving
`Δ_grd^symb(M) ≥ max{Boolean obstruction, σ_γ(ν)}`.

The obstruction is (b): approximate deterministic realization has no analogue
of the singular-value calculus.

---

### 2.2 Intrinsic multi-alphabet Hankel equality — severity A

**Statement.** *[M]* For `|Σ| > 1`, characterize intrinsically, in terms of `ν`, when
`Δ_grd^Hank,str(M) = σ_{M+1}(H_ν)`.

**The difficulty, precisely.** *[M]* `ℓ²(Σ*)` over a free monoid carries `|Σ|` prefix
shifts `S_a`, jointly an isometry of multiplicity `|Σ|` — **not** a single
unilateral shift of multiplicity one. Classical Adamjan–Arov–Krein theory is a
*one-variable* Hardy-space theorem and does not apply directly.

**What is established.** *[M]*
- *Scalar case* `|Σ| = 1`: equality holds under a compact Hardy symbol
  `φ ∈ H^∞ + C(𝕋)`, with an attained optimum of rational symbol degree `≤ M`.
- *Multi-letter*: equality holds **conditionally**, given a unitary
  intertwining the shift systems and carrying the Hankel feasible sets
  bijectively, plus an AAK/Nehari theorem on the target space.
- *Contrapositive*: a strict gap at any `M` rules out such an embedding.

**Sharpness of the concern.** *[A]* The manuscript uses `Σ = I × O`, so `|Σ| > 1` in
every nondegenerate case. The conditional hypothesis is therefore not merely
strong — it is **not known to be satisfiable** in the setting of primary
interest. Resolution requires: (i) identifying the right free-semigroup or
vector-valued Hardy/Fock model; (ii) deciding when unitary equivalence to it
exists; (iii) checking that finite-rank AAK survives the equivalence.

---

### 2.3 Verification of the oracle separation floors — severity A

**The gap.** *[M]* `Assumption (Explicit Approximation and Estimation Floors)` (`ass:oracle-floors`) postulates, for each `M`,
two processes `P_M^0, P_M^1` such that **every** predictor `h` satisfies

```
R_0(h) + R_1(h)  ≥  Δ_M ,     Δ_M = min{ A_T(M), E_M(T) }.
```

Given this, the minimax lower bound follows in a few lines. **The assumption is
never verified for the manuscript's own regimes.** It is invoked 10 times.

**Why this is severity A.** *[A]* The two-sided oracle characterization is a headline
result, and it currently rests on an unverified hypothesis. A reader could
reasonably ask whether the floors are vacuous or circular for, say, quadratic
retention.

**What resolution requires.** *[A]* Per regime, construct explicit two-point families:
- *retention*: two lumpable processes with prescribed `Σ_π` tails such that no
  budget-`M` predictor is near-optimal for both;
- *grounding*: two channels whose Hankel operators agree to rank `M` but
  diverge after;
- *commitment*: two specifications whose Nerode indices straddle `M`.

Each is plausible; none is done.

**Narrowed this round.** *[A]* The *second* display of the minimax theorem
previously depended on `Assumption (Regular Bias–Variance Envelope)`, whose
continuity and exact-crossing clauses were never checked; the proof asserted
that monotonicity alone sufficed, which is false. That dependency is now
removed: `Lemma (Discrete Bias–Variance Sandwich)` derives

```
B ≤ A ≤ (1 + κ) B ,   κ = b(M*)/b(M*−1) at the crossing index M*,
```

from monotonicity plus two *discrete* conditions — `b(1) ≤ a(1)` and
`b(M) ≥ a(M)` for some `M` — with no continuity and no exact crossing. So the
residual severity-A content of §2.3 is now confined to the sum-separation
floors themselves; the envelope-regularity side is closed. The constant `1+κ`
is attained (`a=(10,1)`, `b=(1,9)` gives `A/B = 10 = 1+κ`), so it cannot be
replaced by a universal `2` in the discrete setting; `κ → 1` whenever
`b(M)/b(M−1) = 1 + O(1/M)`, as for `b(M) = √(T ln eM) + ln eM`.

---

### 2.4 Necessity of the aggregation penalty — severity B

**Statement.** *[M]* Is `Ψ_M(T) = O(√(T log(eM)) + log(eM))` necessary, or is adapting
to an unknown budget as easy as knowing it?

**Status.** *[M]* The upper bound is proved via a parameter-free aggregator. The lower
bound matches only *up to* `Ψ_M(T)`. The second-order `log(eM)` term suggests a
genuine but small separation.

**Reduction.** *[A]* This is a question in parameter-free online learning: the
`√(T log M)` term follows from finite-expert lower bounds; what is unsettled is
whether the additive `log(eM)` (or a `√(T log log T)`-type term) is unavoidable
for countable expert sets with prior weighting.

---

### 2.5 Full-KL retention NP-hardness — severity B

**Statement.** Decide whether

```
min_φ  Σ_k Σ_{s: φ(s)=k}  π_s · D_KL( P_s ‖ P̄_k )  ≤  τ
```

over lumpable quotients is NP-hard.

**Reduction achieved, stated precisely.** *[M]* The optimal block representative
is the mixture centroid `P̄_k` (mixture-centroid lemma). Writing
`Π_k = Σ_{s∈C_k} π_s` and normalized within-block weights `w_s = π_s / Π_k`,
the block term satisfies

```
Σ_{s∈C_k} π_s · D_KL(P_s ‖ P̄_k)  =  Π_k · JS_w({P_s}_{s∈C_k}),
```

where `JS_w({P_i}) = Σ_i w_i D_KL(P_i ‖ Σ_j w_j P_j)` is the generalized
Jensen–Shannon divergence. Hence the total objective is

```
Σ_k Π_k · JS_{w}(block k),
```

a **`Π`-weighted sum of within-block generalized Jensen–Shannon divergences** —
not a bare JS cost. So the decision problem is *constrained, weight-normalized
Jensen–Shannon clustering with lumpability constraints*. *(Identity verified
numerically to machine precision.)* The Gaussian quadratic regime — proved
NP-complete via `k`-means — is its second-order Fisher special case, where the
centroid degenerates to a mean and the cost to squared Euclidean distance.

**The obstruction, and how it was overcome.** *[A]* The `k`-means reduction
amplifies its promise gap by denominator clearing on a rational grid. **KL
centroids are not rational in the inputs**, so the gap cannot be preserved
exactly; it must be controlled analytically. `thm:full-kl-promise-np` does this
by working in a shrinking interior neighbourhood of the uniform law, where the
JS cost is a controlled perturbation of the Euclidean one.

**Construction.** Embed integer points `a_i ∈ Z^d` into the tangent space of
`Δ^{2d−1}` by sign-doubling,

```
z_i = (a_i1, −a_i1, …, a_id, −a_id),    Σ_j (z_i)_j = 0,
‖z_i − z_j‖₂² = 2‖a_i − a_j‖₂²,
```

and set `p_i = u + δ z_i` with `u` uniform on `2d` letters and `δ = 2^{−Λ}`.
Doubling is what makes the embedding **centred**, hence tangent to the simplex.
Reset transitions `τ(s_i, ℓ) = s_ℓ` give synchronization depth one and make
**every** partition lumpable. A third-order expansion around `u` — with linear
terms vanishing by centring — gives

```
J_C = d δ² Σ_{i∈C} w_i ‖z_i − z̄_C‖₂² + ρ_C,    |ρ_C| ≤ C₀ d² δ³ Z³,
```

the factor `d` because the negentropy Hessian at `u` is `2d·I` on the tangent
space, halved by the quadratic term. Choosing `Λ` polynomial so that
`C₀ d δ Z³ < 1` makes the cubic remainder smaller than a quarter of the
amplified `k`-means gap `2n`, and rational thresholds
`θ_yes = (2dδ²/n)T + dδ²`, `θ_no = θ_yes + 2dδ²` separate YES from NO.

Verified: `verify/kmeans_js2.py` (remainder is exactly cubic — `R/δ³` converges
to a finite constant as δ: 1e−2 → 1e−8; and the granularity claim, 0/4000
violations of `denominator | lcm(1..n)`, so the gap is `2^{−O(n)}` and
polynomially many bits suffice); `verify/hessian_factor.py` (the factor `d` is
exact to 12 digits for `d = 1,2,3,5`).

**What is *not* claimed.** Exact NP-**completeness**. Membership in NP would
require deciding, in polynomial time, an inequality between a rational and a
sum of terms `p log(p/q)` with `p,q` rational — not known to be in P. The
Gaussian quadratic regime avoids this entirely because its objective is
rational in the data, which is precisely why completeness is available there
and only hardness here (`rem:full-kl-promise-scope`). **Severity B → closed as
promise-hardness; the completeness question is new and severity C.**

---

### 2.6 Global full-KL spectral converse — **now fully settled in both charts**

**Probability coordinates: closed, with the sharp constant.** *[A]*
`thm:global-kl-simplex` proves, with **no** regularity, locality, or
small-radius hypothesis,

```
RetKL(φ) ≥ Σ_{i≥M} λ_i(Σ_p)
```

for every lumpable quotient with ≤ M blocks, where `Σ_p` is the covariance of
the predictive **probability vectors**.

The constant is **1, not ½**. The earlier ½ came from bounding
`‖δ‖₂ ≤ ‖δ‖₁`, which is valid on all of `R^|O|` but ignores that a difference
of probability vectors is **centred**. Writing `a` for the common mass of the
positive and negative parts, `‖δ‖₁ = 2a` and `‖δ‖_∞ ≤ a`, so

```
‖δ‖₂² ≤ ‖δ‖_∞ ‖δ‖₁ ≤ 2a² = ½‖δ‖₁²,
```

and Pinsker then gives `D_KL(p‖q) ≥ ½‖p−q‖₁² ≥ ‖p−q‖₂²`. The rest is
unchanged: mixture centroids are optimal block representatives
(`lem:mixture-centroid`); ANOVA splits `Σ_p = W_φ + B_φ` with
`rank(B_φ) ≤ M−1`; Ky Fan bounds `tr(B_φ)`.

**The constant 1 is optimal.** *[A]* `prop:kl-simplex-sharp`: take
`p_± = (½ ± ε, ½ ∓ ε)` equiprobable, `M = 1`. Then `tr(Σ_p) = 2ε²` and
`RetKL(1) = log2 − h(½+ε) = 2ε² + (4/3)ε⁴ + O(ε⁶)`, so the ratio → 1. No
`c > 1` is possible. Verified: `verify/sharp_constant.py`, 400k random pairs,
min ratio `KL/‖·‖₂²` = 1.0000031, zero violations of the centring step.

**Natural-parameter chart: closed negatively.** *[A]*
`thm:no-global-fisher-converse` replaces the former open problem. There is **no**
universal `c > 0` with `RetKL(M) ≥ c Σ_{i≥M} λ_i(Σ_η)`, nor with the
Fisher-weighted `Σ_F = I(η_p̄)^{1/2} Σ_η I(η_p̄)^{1/2}`. Counterexample, already
at two states and `M = 1`:

```
P₋ = Bernoulli(ε),   P₊ = Bernoulli(1 − ε),   π_± = ½.
```

The mixture is `Bernoulli(½)`, so `RetKL(1) = log2 − h(ε) ≤ log2` stays
**bounded**, while `η_± = ± L_ε` with `L_ε = log((1−ε)/ε)` gives
`Σ_η = L_ε² → ∞`. Hence the ratio `≤ log2 / L_ε² → 0`. The Fisher-weighted form
fails identically: the reference point is `p̄ = ½`, at which `A''(η) = ¼`, so
`Σ_F = ¼L_ε² → ∞` too — weighting at the mixture does not help, because the
reference stays interior while the states escape to **opposite** faces.
Verified: `verify/fisher_nogo.py`, ratio 7.6e−2 → 9.1e−4 as ε: 1e−1 → 1e−12.

**Why this is consistent with the interior theorem.** *[A]*
`thm:global-interior-fisher` gives `RetKL(M) ≥ (m_K/2) Σ_{i≥M} λ_i(Σ_η)` with
`m_K = inf_{η∈K} λ_min(∇²A(η))` over a compact `K` containing the predictive
parameters **and all their mixture centroids**. The no-go theorem shows the
dependence of the constant on `K` is **not** an artefact: `m_K ↓ 0` as `K` is
enlarged toward the boundary. Interiority is necessary, not convenient. The
structural reason is that the simplex is bounded (`‖p_s − p̄‖₂ ≤ √2`) whereas
the natural-parameter chart is not, and the counterexample exploits exactly
that unboundedness (`rem:fisher-nogo-reading`).

**Why the *earlier* boundary family was not a witness.** *[A]* An earlier
manuscript version asserted a no-go via `P₊ = Bern(1−ε)`, `P₋ = Bern(1−2ε)`
with ratio `Θ(ε²) → 0`. That was **false**: it used `I(η) = 1/(p(1−p))`, the
Fisher information in the **mean** parameter, whereas in the natural parameter
`I(η) = A''(η) = p(1−p)` (the two are reciprocal since `dp/dη = p(1−p)`).
Recomputing, `RetKL(1) = Θ(ε)` **and** `tr(Σ_π) = Θ(ε)`, ratio
`→ 0.50009786…`, bounded away from 0. That computation is preserved as
`prop:bernoulli-fisher-scales`. The distinction that matters: in that family
both states approach the **same** face at comparable rates; the genuine witness
sends them to **opposite** faces, which is what makes `L_ε` diverge while the
divergence saturates at `log2`.

**Status: no open sub-question remains in this item.** Both charts are settled —
affirmatively with a sharp constant in probability coordinates, negatively in
the natural-parameter chart. The label `open:global-kl-fisher` has been retired
from the manuscript.

### 2.7 Price-of-Safety relaxation gap — severity B

**Statement.** *[M]* Bound the discrepancy between the linear block-local surrogate
`PoS_lin^loc(M)` and the discrete right-congruence `PoS_quad(M)`.

**Status.** *[M]* The surrogate is *exact for its own linear problem*: pinching gives
`PoS_lin^loc(M) ≥ 0` by Ky Fan majorization, with a coupling upper bound and a
complete free-lunch characterization. But hard partitions and block-local
spectral projections are different feasible sets, and **no bound in either
direction** is established.

**Note.** *[M]* A strictly more partition-faithful relaxation exists — constrained PCA
requiring the projection to contain the safety-block label subspace — and it
does *not* reduce to the pinching formula. Comparing all three is open.

---

### 2.8 Domination bridges — severity B

**Statement.** *[M]* Identify task-theoretic conditions under which contextwise
`ℓ^p` aggregation implies Schatten-`p` domination.

**Why it matters.** *[A]* The conditional Schatten converse template is the
manuscript's main unifying device, and it is *entirely* conditional on a
domination inequality supplied per regime. Without a bridge, the template yields
nothing.

**Known.** *[M]* The implication `contextwise ℓ^p ⇒ Schatten-p domination` is **not
automatic**; the tail exponent is the exponent of the operator norm in the
bridge, not of the aggregation. A sufficient route is a linear measurement map
with a frame-type lower bound.

**Sharpened this round.** *[A]* `lem:frame-bridge` shows that for a *linear*
measurement map the bridge condition and the domination modulus are the **same
condition**: `‖T(z)‖_{S_p} ≤ C_p ‖z‖_{ℓ^p(w)}` gives `c_p = C_p`, and
conversely. So the open question is exactly: for which `T` is `C_p` finite and
dimension-free?

**A no-go for the natural candidate.** `prop:no-dimension-free-bridge`:
for the `n × n` Hankel embedding,

```
C_2(n) = sqrt(n)  exactly,      C_1(n) >= n,      C_inf(n) >= n.
```

`C_2` is analytic (multiplicity `m_k = min(k+1, n, 2n−1−k)`, maximised at the
main anti-diagonal). `C_1 ≥ n` uses the atom `e_{n−1}`, whose Hankel image is
the anti-identity with `n` unit singular values. `C_inf ≥ n` uses `z ≡ 1`,
whose image is the rank-one all-ones matrix.

*Methodological note:* a hill-climbing search over `z` suggested `C_1` was
bounded (~3–4 up to `n = 32`). That was **wrong** — random restarts in
`R^{2n−1}` almost never find the sparse maximiser. A direct single-atom witness
settles it. I record this because the numerical evidence was actively
misleading, not merely inconclusive.

**Two instances are *not* exposed.** The diagonal embedding is a Schatten
isometry for every `p` (`C_p = 1`), so retention has a dimension-free bridge.
And the grounding instance sets the cost *equal* to the operator-norm distance,
so `c_inf = 1` by definition with no frame constant. The obstruction bites only
where an `ℓ^p` aggregation of sequence entries is compared to a Schatten norm
of their Hankel embedding.

**Still open.** Whether any non-trivial task theory admits a dimension-free
bridge through an overlapping embedding, or whether budget-dependent moduli
`c_p(M)` must simply be carried explicitly into the downstream tails.

---

### 2.8a Universal versus machine-specific synchronization — severity B

*[M]* The active upper bound uses the **universal** adaptive synchronization
depth `L_sync^univ(M)` — the minimum over single decision trees implementable
without knowing the target — rather than the machine-specific `L_sync(M)`,
because a learner facing an unknown machine cannot run the experiment that is
optimal for that machine. Always `L_sync(M) ≤ L_sync^univ(M)`.

*[A]* **Open:** how large is the gap? If `L_sync^univ / L_sync` is unbounded
in `M`, the length-form upper bound is substantially weaker than it appears.
The two coincide when the machine is known except for its initial state.

---

### 2.9 Active learning without synchronization — **largely closed this round**

**Former statement.** *[M]* Develop active realizable bounds when no
output-aware synchronizing word exists. The concern was that `L_sync(M) = ∞`
for some `M`-state machine would make the length-based upper bound
`O(M log M + L_sync^univ(M))` vacuous, leaving the theory silent exactly where
synchronization fails.

**Why it is now closed for the order of the complexity.** *[A]* The concern
presupposed that the *only* route to objective (RI) was a synchronization
experiment. It is not. `Theorem (Unconditional Active Attainment Bound)`
exhibits an active halving learner that attains (RI) within
`log₂|H_M × Q| = O(M log M)` mistakes and **never performs a synchronization
experiment at all**: it plays shortest distinguishing words between residually
distinct version-space elements, predicting by plurality, so every mistake
halves the version space. It is therefore well defined even when no machine in
`H_M` admits a synchronizing experiment, and

```
E_sync(M) = Θ(M log M),   Mistakes_active(M) = Θ(M log M)
```

hold with **no** synchronizability, operational-equivalence, or direct-sum
hypothesis (`cor:active-theta`).

**Verified.** Exhaustive simulation over all Mealy machines on `|I|=|O|=2` for
`M = 1, 2` (4 and 512 version-space elements): (RI) attained on every random
target, worst-case mistakes `2 ≤ 2.00` and `6 ≤ 9.00` respectively, with the
halving invariant asserted at every mistake.

**Budget coverage.** *[A]* The gated family exists only for `M' = 2^L` and
occupies `2M'` states, so on its own it bounds only the subsequence
`N_L = 2^{L+1}`. The corollary now passes to all sufficiently large budgets via
`lem:subsequence-allM` with ratio `α = 2`, using monotonicity of `E_sync`
(`H_M ⊆ H_{M+1}`). This mirrors the passive treatment in `cor:stream-all-M`;
without it the unconditional claim would have covered only powers of two.

**What remains.** *[A]*
(i) The *constant* is not settled. `log₂|H_M × Q| / (M log₂ M) ≈ 2.29` at
`M = 128` and decreases slowly toward `|I| = 2`; the gated lower bound gives
`1`. Closing the constant-factor gap is open. Severity C.
(ii) The **agnostic** active rate is untouched by this argument, since halving
requires realizability. Severity C.
(iii) Characterizing the non-synchronizable machines remains an interesting
structural question, but nothing in the manuscript now depends on it.

---

### 2.9a Chaining of the unknown map in the active protocol — **closed this round**

*[A]* Recorded because the failure mode is subtle and recurs whenever a passive
adversary construction is reused actively.

**The defect.** The active lower bound was proved on the passive family
`G_M` of the persistent-stream theorem, whose letter `c` maps `v ↦ g(v)`
emitting `0`. In the passive protocol the adversary controls the stream and
only ever issues `c` from a transported, hence known, state. An **active**
learner may instead play `c` twice, reaching `g(g(v))`, and read out there. The
observed bits then constrain `g` at an argument that is itself unknown, so the
set of consistent maps stops being a product of independent per-argument
constraints. Both the lazy adversary (which needs every completion to remain
available when it fixes a bit) and the conditional-uniformity step of the Yao
argument silently fail.

**Verified.** For `L = 2`, one chained readout `g(g(0^L)) = u` leaves 48 of the
256 maps consistent, while the product of the per-argument projections has
`3·4·4·4 = 192` elements — the constraints are correlated, confirmed by
exhaustive enumeration.

**The repair.** `Definition (Gated Active Family)` adds a mode bit: states are
`Q × {free, read}`, and `c` is a **no-op** in read mode. Read mode is entered
only by `c` from free mode, so the readout argument is always the free-mode
state the learner itself transported to, hence known. The consistent set is
therefore a product `∏_v S_v` at all times. Cost: the state count doubles, so
`G^act_M ⊆ H_{2M}`; rescaling `N = 2M` preserves `Ω(N log N)`.

**Also repaired.** The randomized half no longer invokes fixed-stream Yao,
which lower-bounds only learners that follow the fixed stream. It now argues
directly on the adaptive transcript via first-emission rounds: the coordinate
read at round `t` is `F_{t−1}`-measurable, the corresponding bit is independent
of `F_{t−1}` and uniform, so each first emission has conditional mistake
probability exactly `1/2`; Azuma–Hoeffding on the resulting martingale
difference sequence gives the high-probability form.

**Confirmed by exhaustive minimax.** Solving the full active game on the gated
family by layered value iteration (Dijkstra over the zero-cost move graph
within each knowledge layer) gives minimax mistakes exactly `M log₂ M` for
`L = 1, 2` — matching the passive bound, so gating costs nothing in order.

**Residual.** *[A]* The gated family has `2M` states to force `M log₂ M`
mistakes. Whether an `M`-state family forces `M log₂ M` in the *active*
protocol — i.e. whether the factor-2 state overhead of gating is necessary —
is open. Severity C: it affects constants, not exponents.

---

### 2.12 Extension off the support in the Boolean dichotomy — **narrowed this round**

*[A]* `meta:boolean` (ii) previously asserted
`κ_obs(δ,μ) = index(~_{δ,S})` for right-closed support `S`, justified by the
phrase "extending it arbitrarily off `S` costs no index". That step was not
proved and is not obvious: right-closure makes `S` forward-invariant but does
**not** stop a history outside `S` from having an extension inside `S`.
Verified: for `S = {u : u ends in b}` closed under extension, `baaa ∉ S` while
`baaab ∈ S`. So the classes off `S` cannot be merged arbitrarily without
breaking the right-congruence property.

`lem:support-extension` now supplies an explicit construction — identify two
histories outside `S` when they enter `S` on the same continuations and land in
the same class whenever they do — and proves it is a right congruence. The
meta-theorem states a **sandwich**

```
index(~_{δ,S})  ≤  κ_obs(δ,μ)  ≤  index(~_{δ,S}) + c_S
```

with `c_S = 0` iff the extension is index-preserving.

**Correction (this round).** *[A]* An earlier version of this section claimed
that `c_S = 0` "may hold generally under right-closure", citing an exhaustive
search over 36,970 (δ, right-closed S) pairs that found no counterexample.
**That claim is false and the search was invalid.** It tested whether the
support-relative Nerode partition *of all of `I*`* is a right congruence, which
silently gives `ε` its own class and therefore computes the wrong quantity; it
never compared `index` on `S` against the minimum *global* index.

**Counterexample.** `I = {a,b}`, `S = I⁺` (right-closed), `δ(u) = A` if `u`
starts with `a`, `B` if with `b`. On `S` the relation has exactly two classes.
But `ε` must send `a` into the `A`-class and `b` into the `B`-class, while the
`A`-class sends *both* letters to `A` and the `B`-class both to `B`; so `ε`
matches neither pattern and needs a third class. Verified by exhaustive
minimum-DFA search: `index(~_{δ,S}) = 2` but `κ_obs = 3`, so **`c_S = 1`**.
The three-state witness is `q_ε →a q_A`, `q_ε →b q_B`, with `q_A, q_B`
absorbing. This is now `rem:support-extension-sharp` in the manuscript.

**What survives.** The sandwich in `lem:support-extension` is correct and
sharp at both ends: `2 ≤ 3 ≤ 2 + 1`. The obstruction requires `μ(ε) = 0`; for a
discounted-prefix law with `μ(ε) > 0`, right-closure forces `S = I*` and
`c_S = 0`.

**Still open.** *[A]* Characterize the right-closed supports with `c_S = 0`,
and bound `c_S` in general. Severity C.

---

### 2.13 Constant in the active separating-word bound — severity C

*[A]* `thm:active-halving` needs a finite separating word for two residually
distinct `(machine, state)` pairs. The manuscript previously cited the Moore
`M−1` bound, which is wrong here: Moore separates two states of a **single**
machine, whereas the two pairs may come from **different** machines. The
correct guarantee is the product-automaton bound `M² − 1`.

Exhaustive check (`|I| = |O| = 2`): worst separating length 3 at `M = 2`
(249,024 pairs) and 4 at `M = 3`. Both within `M² − 1`; the true worst-case
growth rate between `2M − 1` and `M² − 1` is open. Severity C — the mistake
bound counts halvings, not word lengths, so only finiteness is used.

---

### 2.14 Reflexivity of the cost profunctor — **gap closed this round**

*[A]* `meta:monotone` (ii) asserted that finite Nerode index implies zero gap
for an arbitrary task theory. The proof step "quotienting by `~_δ` realizes the
trajectory exactly" silently requires `E(X,X) = 0`, which **no task-theory
axiom supplied**: `E` was only required to be a `V`-profunctor.

**Counterexample.** In the Lawvere quantale `([0,∞], ≥, +)`, let `R` have one
object `*` with `E(*,*) = 1`. The profunctor inequality `R(*,*) + E(*,*) ≥
E(*,*)` reads `0 + 1 ≥ 1`, so this is admissible. Then `δ` is constant,
`index(~_δ) = 1`, yet `Δ(M) = 1 ≠ 0` for every `M`.

**Fix.** Reflexivity `E(X,X) = 0` is now an explicit axiom in
`def:task-theory`, with the counterexample recorded there. Every instance used
in the manuscript — KL, operator norm, `0/1` commitment — already satisfies it,
so nothing downstream changes; only the generic meta-theorem needed it.

The proof of `meta:monotone` now states which hypothesis each direction
consumes: reflexivity for `⇐`, separatedness for `⇒` (the latter was already
assumed in clause (iii)).

---

### 2.15 Alternating versus simultaneous commitment values — **gap closed this round**

*[A]* The commitment gap was defined as `Com(M) = V(∞) − V(M)` with a single
symbol `V`, but `V(∞)` was the **alternating-move** Bellman value while the
strategic-spread lower bound concerns the **simultaneous-move** protocol, and
`V(M)` was never separately defined.

Now separated: `V_alt(q)` is the alternating-move Bellman value, `V_sim(M)` is
the simultaneous-move value as an explicit `sup` over budget-`M` policies, and

```
Com(M) = V_alt(∞) − V_sim(M),
```

so the gap measures both the memory restriction and the loss of access to the
current input. All 31 occurrences in the section were converted.

---

### 2.16 The active additive decomposition is degenerate — **resolved this round**

*[A]* The manuscript carried a two-term active decomposition
`Θ(M log M + E_sync^SI(C_M))` and an open problem asking for a family with
`E_sync^SI(C_M) = ω(M log M)`. **That open problem was vacuous.**

**`E_sync^SI(M) = O_{|O|}(log M)`.** For a known *minimal* skeleton with
unknown initial state, maintain the version space of candidate current states
(`|V| ≤ M`), play a letter on which survivors disagree, and predict by
plurality. Each mistake removes at least a `1/|O|` fraction, so

```
E_sync^SI(M) ≤ log_{|O|/(|O|-1)} M ,   and ≤ log2 M for binary output.
```

Verified exhaustively over ~31,000 minimal machines (`|I|=|O|=2`, `M ≤ 4`):
worst-case SI mistakes were 1, 1, 2 for `M = 2, 3, 4`, i.e. `≤ ⌈log₂M⌉`,
never approaching `M log M`.

**Consequence.** `M log M + E_sync^SI = Θ(M log M)` always, so the two terms
never separate. The additive form is now stated as a **lower bound only**,
`Mistakes_active,RI(M) ≥ S_M + C_M`, derived from disjointness of the two round
sets rather than from `max{u,v} ≥ (u+v)/2` — which is what the old proof used,
and which does not give a sum. Six downstream sites asserting the degenerate
equality were corrected.

**Reframed open problem.** Two questions survive: is the `O(log M)` bound
tight, and is there a *currency* admitting a genuine two-term decomposition?
Experiment **length** is the natural candidate — exhibit `C_M` with
`L_sync^univ(C_M) = ω(M log M)`, or show `L_sync^univ(M) = O(M log M)` always.

---

### 2.17 Simultaneous-move commitment: a machine-model typing error — **fixed**

*[A]* The simultaneous protocol requires the agent to commit to `b_t` before
seeing `a_t`, but `V_sim(M)` quantified over **Mealy BSGs**, whose output map
has type `λ : S × I → O` and therefore *reads* `a_t`. The policy class could
not express the protocol it was defined for.

Fixed by `def:pio-controller`: pre-input-output controllers
`π = (M, m₀, β, η)` with `b_t = β(m_t)` and `m_{t+1} = η(m_t, a_t, b_t)`.
The gap `Com(M) = V_alt(∞) − V_sim(M)` is now labelled an
**observation-and-memory gap**, since it does not vanish even at `M = ∞`.

**`cor:stateless` survives**, verified by brute force over all controllers with
`|M| ≤ 2` on four games × three discounts: `V_sim = m₂/(1−γ)` exactly, so
`Com = (m₁−m₂)/(1−γ)` for all `M ≥ 1`. Extra memory cannot help in a stateless
game because `β(m)` is a constant output the adversary best-responds to.

---

### 2.18 Global Fisher converse: chart-dependence and a valid interior theorem

*[A]* The claim that uniform interiority gives `λ_i(Σ_p) ≍ λ_i(Σ_π)` was
**not justified** — a bi-Lipschitz nonlinear reparameterization does not give
eigenvalue-by-eigenvalue comparability. Removed.

Replaced by `thm:global-interior-fisher`, proved by strong convexity of the
log-partition function in a fixed minimal chart:
`RetKL(M) ≥ (m_K/2) Σ_{i≥M} λ_i(Σ_η)`.

**A subtlety worth recording.** My first numerical test *falsified* the theorem
(2 violations in 11,717 exact instances). The cause was mine, not the
statement's: I sampled `m_K` over `conv{η_s}`, but a mixture centroid's natural
parameter need **not** lie in that hull — it failed to in 13,462 of 20,000
samples, because `p ↔ η` is nonlinear. Re-testing with `m_K` over the η-images
of all mixtures gave 0 violations in 5,132 instances. The theorem's hypothesis
already says `K` contains the centroid parameters; the proof now emphasises
that this is not implied by `K ⊇ {η_s}`.

Also noted: "the natural-parameter Fisher covariance" is not canonical for a
global family without fixing a minimal chart and, for a Fisher-weighted form,
a reference point. `thm:no-global-fisher-converse` is stated against a fixed
chart in exactly that sense, and rules out a universal constant for the
unweighted and Fisher-weighted forms alike (§2.6).

---

### 2.19 Cesàro aggregation has no history law — **scope corrected**

*[A]* `meta:boolean` (ii) was stated for "stationary Cesàro **or**
discounted-prefix with history law `μ`". Only the second carries a genuine
probability measure on `I*`:
`μ(u) = (1−β)β^{|u|} Pr[prefix u]`. Cesàro aggregation averages a cost process
along a stationary trajectory (`def:cesaro-agg`), and with infinite support the
averages need not converge to an expectation under any single measure on finite
histories — so "`μ`-almost every history" was undefined there.

Clause (ii) is now restricted to discounted-prefix. `rem:cesaro-boolean` gives
the two correct Cesàro formulations: on the **stationary state space**, zero
cost at budget `M` iff a right congruence of index `≤ M` is exact on `S⁺`
(which is `thm:retention-zero` in the Boolean case); on **histories**, the
surrogate for "`μ`-a.e." is **zero asymptotic frequency of error**,

```
lim_T (1/T)·|{t < T : E(δ(U_t), Ψ([U_t])) > 0}| = 0   a.s.
```

The two agree for finite-state ergodic chains, since a positive-mass state is
visited with positive asymptotic frequency. No support-relative Nerode formula
is claimed for Cesàro.

---

### 2.20 AAK scoping now reaches the abstract — **fixed**

*[A]* `thm:aak-equality` was already correctly scoped to `|Σ| = 1` in the body,
but the **abstract** and the **exact-results table** cited
"Adamjan–Arov–Krein" with no alphabet restriction, where it reads as generally
available. Both now carry `|Σ| = 1` and the requirement of a shift-intertwining
embedding; the abstract states that for `|Σ| > 1` the free monoid carries no
shift of multiplicity one, so equality remains conditional on a multi-shift
Nehari/AAK theorem not established here (`open:hankel-multiletter`).

---

### 2.21 Quantifier and definitional hygiene — **fixed**

*[A]* A final audit round found six defects of scope and quantification rather
than of substance. All are now repaired.

- **`MistRI` vs `Esync` was near-circular.** Both were minimax-over-learners
  for the same objective, making `thm:active-certified`(I) true by definition.
  `MistRI(M)` is now the **total** mistakes over the whole interaction subject
  to attaining (RI); `Esync(M)` counts only mistakes **before** attainment. So
  `MistRI ≥ Esync` holds definitionally and the reverse is the real content of
  Part (I), which uses prediction-closing.
- **Randomized lower bounds** conflated `sup_target E[·]` with
  `E_target E[·]`. Both `thm:stream-lower-bound` and
  `thm:active-explicit-directsum` now read "for every randomized learner there
  is a fixed target with…", derived by averaging.
- **Strong convexity on the simplex boundary** is undefined
  (`diag(1/p_i)` blows up). The Hessian formulation is now confined to the
  interior; the proof runs through Pinsker, which is valid throughout.
- **Mealy → acceptor** in `thm:exp-gap` was asserted. Now explicit: state set
  `S × O` recording the last emitted symbol, a constant-factor blowup.
- **`α_γ(R)`** hid its dependence on the budget; now `α_γ(R, M)`.
- **Undefined `V`** survived in `cor:stateless` (my rename swept `V(` but not
  bare `V`); replaced by `m₁`, and the stateless witness is now a
  pre-input-output controller rather than a BSG.

Also: the abstract no longer claims a transfer to "the natural-parameter Fisher
covariance", since no such object is canonical without a chart; and the
`amari2010`/2009 key–year mismatch is fixed.

---

### 2.22 Rigor pass: expansion, thresholds, and conventions — **fixed**

*[A]* Five further defects of rigor, all now repaired.

- **Csiszár Cauchy extraction** was asserted ("matching the coefficient of
  `q₁q₁'`"). The expansion is now displayed: with `q = (ε, 1−ε)`,
  `p = (uε, 1−uε)` and similarly for `v`, the additivity defect is
  `Δ(ε) = ε²[g(uv) − u g(v) − v g(u)] + O(ε³)`, with the `O(ε)` terms
  cancelling between the two sides. Verified numerically: for
  `h(t) = t log t + c(t−1)²` the ratio `Δ/ε²` converges to exactly the Cauchy
  residual (2.0004 → 2 at `c = 0.5`; 4.0008 → 4 at `c = 1`).
- **`MistRI` quantifier** was still ambiguous — "the mistakes a learner makes"
  does not say whether it is minimax. Now an explicit
  `inf over learners that attain (RI) / sup over instances` of the **total**
  mistake count, with `Esync` counting only pre-attainment mistakes. So
  `MistRI ≥ Esync` is definitional and the reverse is `thm:active-certified`(I),
  which consumes prediction-closing.
- **`open:global-kl-fisher`** presupposed a canonical `Σ_π`, contradicting the
  abstract's own chart-dependence caveat. It was reposed against a fixed
  minimal chart with the Fisher-weighted form
  `Σ_F = I(η_p̄)^{1/2} Σ_η I(η_p̄)^{1/2}` specified, and has since been
  **retired**: `thm:no-global-fisher-converse` answers it negatively for both
  forms (§2.6).
- **`thm:interaction-complexity`** equated a strict retention threshold
  (`< θ`) with a non-strict joint one (`≤ θ`). The gap-amplification lemma
  supplies a `2n` promise gap, so the reduction now sets
  `ε = ½(θ_yes + θ_no)`, strictly separating the cases.
- **AAK indexing (previously deferred).** Resolved by Kronecker's theorem:
  `rank H_ψ` equals the McMillan degree of `ψ`, verified numerically (rank = d
  exactly for `d = 1..5`, 40 trials each). So "rank ≤ M", "degree ≤ M" and
  `σ_{M+1}` are mutually consistent; the correspondence is now stated.

Also: the grounding row of the type table is relabelled "operator norm on
`H_ν`" rather than "worst case, all histories", and the conclusion attributes
the upper bound to the halving learner and the lower bound to the gated family
separately.

---

### 2.23 The oracle separation floor was false, not merely unverified — **severity A resolved**

*[A]* This was the manuscript's longest-standing severity-A item: a hypothesis
invoked 10 times with no verified instance in any regime. Attempting to
construct one showed why none existed.

**The two-point form is unsatisfiable.** `ass:oracle-floors`(i) demanded two
processes with `R_0(h) + R_1(h) ≥ Δ_M` for *every* predictor `h`. Under log
loss `R_i(h) = KL(P^i‖Q_h)`, and

```
min_Q [ KL(P⁰‖Q) + KL(P¹‖Q) ] = 2·JSD(P⁰,P¹) ≤ 2 log 2 ≈ 1.386 nats,
```

the minimum attained at the mixture. Verified on 200,000 random pairs (max
1.3837, cap respected) and shown attained by mutually singular pairs. Since
`Est_M(T)` diverges in `T`, `Δ_M` eventually exceeds `2 log 2` and **no two
processes can exist**. This was a false hypothesis, not an unverified one.

**The repair.** Replaced by an averaged Fano-type *packing floor* over `m`
processes:

```
min_Q (1/m) Σ_i KL(P^i‖Q) = I(V;Y) ≤ log m,   V ~ Unif[m],
```

with equality when the transcript laws are mutually singular. Carrying
`Δ_M = Θ(M log M)` therefore needs `m = exp(Θ(M log M)) ≈ |H_M|` — the
two-point form was off by an exponential.

**Discharged.** `prop:floors-instance` verifies the floor for the realizable
persistent-stream regime using the manuscript's own gated family: all
`m = M^M` transcripts on the forcing stream are pairwise distinct, so
`I(V;Y) = log m = M log M` exactly. Confirmed by exhaustive enumeration
(`L = 1, 2`: 4/4 and 256/256 distinct).

**Bonus.** The averaged form gives a *better* constant: `max ≥ average` yields
`c = 1`, where the two-point form gave only `c = ½` via `max ≥ (u+v)/2`.

**Still open.** The corresponding packings for the retention, grounding, and
commitment regimes.

---

### 2.24 Operational equivalence is a theorem for deterministic classes — **discharged**

*[A]* `lem:operational-equivalence` (5 refs) asserted that guaranteed zero
future mistakes ⟺ residual-class knowledge. For deterministic realizable
classes this is **provable**, and is now `lem:operational-equivalence`.

Forward: (RI) ⟹ zero mistakes is the prediction-closing property. Reverse: if
(RI) fails, two consistent machines have differing continuation functions,
separated by a word of length `≤ 2M−1` (`lem:moore-separation`); the learner's
prediction is transcript-measurable hence identical in both runs, so it errs in
one. Both runs are realizable, giving the contradiction.

Verified exhaustively over all deterministic Mealy classes with `M = 2, 3`
(512 and 139,968 machine-state pairs, 21 transcript classes): every class with
more than one continuation function admits a genuine separation.

It remains an assumption for **stochastic** classes, where the separation
argument does not apply.

---

### 2.25 The determinism gap is superpolynomial, not exponential — **claim corrected**

*[A]* `thm:exp-gap` assumed a family with `k`-state PFA versus `2^{Ω(k)}`-state
DFA, citing Rabin and Freivalds "for the framework only". Checking the
literature settles it, and **against the manuscript**.

The best proved bound is Ambainis (1996): a PFA with an isolated cutpoint and
`n` states whose smallest equivalent DFA has

```
Ω( 2^{ n loglog n / log n } )   states.
```

The exponent is `o(n)` — the ratio `(n loglog n / log n)/n` falls from 0.36 at
`n = 10` to 0.12 at `n = 10¹²`. So the separation is **superpolynomial but
sub-exponential**, and `2^{Ω(k)}` is strictly stronger than anything cited.

**Repair.** The theorem is now parameterized by whatever rate `S(k)` the
literature supplies, concluding `S(k)/|O|` states, with Ambainis cited for the
best current value. Four downstream sites asserting `2^{Ω(k)}` were corrected,
and the section title, theorem title, and results-table entry no longer say
"exponential". Whether a truly exponential family exists is now recorded as
open.

This converts a standing hypothesis into a cited theorem, at the cost of a
weaker — but true — conclusion.

---

### 2.26 Packing floors in stochastic regimes need a horizon hypothesis

*[A]* Having discharged the floor for the deterministic stream regime
(§2.23), I attempted retention. `lem:packing-criterion` reduces the floor to a
single information condition: it holds iff some subfamily has
`I(V;Y_{1:T}) ≥ Δ_M`, the minimum of the averaged KL being attained at the
mixture (compensation identity, verified to 3.6e−15 on 300,000 random cases).

For the natural retention packing — `M` hidden Bernoulli biases spaced
`Θ(1/M)` apart, indexed by `b ∈ [M]^M`, so `log m = M log M` — the information
accrues only as fast as the biases can be *estimated*:

| M | T | I(V;Y)/log m |
|---|---|---|
| 4 | 36 | 0.11 |
| 4 | 516 | 0.62 |
| 8 | 104 | 0.12 |
| 8 | 6152 | 0.83 |

Resolving `M` biases spaced `1/M` apart takes `Ω(M²)` samples per coordinate,
hence `T = Ω(M³)`. At `T = Θ(M log M)` the mutual information is a small
fraction of `log m`.

**This is a structural difference, not a gap in the construction.** In
deterministic regimes transcripts are *logically* distinct, so `I = log m`
immediately; in stochastic regimes distinctness is statistical.
`rem:packing-per-regime` now records this, and the floor in a stochastic regime
should carry an explicit horizon hypothesis with `Δ_M` set to the information
actually available. Constructing `T`-efficient packings for retention,
grounding, and commitment remains open.

---

### 2.39 `Lsync` is not `Lsyncu` — the turn-25/29 bounds are machine-specific

*[A]* **Severity A. This corrects §2.35 and §2.37, and partially §2.38.**
Attempting to prove `Lsyncu(M) = O(M)`, I checked what my own proofs actually
bound. They bound the wrong quantity.

**The definitions differ in quantifier order.**

```
Lsync(M)  = sup_A  min_{tree for A}  depth      -- tree MAY depend on A
Lsyncu(M) = min_{single tree}  sup_A  depth     -- ONE tree for ALL of H_M
```

Both `prop:lsyncu-quadratic` (§2.35) and `prop:lsyncu-binomial` (§2.37) choose
the separating word by **breadth-first search on the pair automaton of the
target**. A learner realizing `Lsyncu` fixes one tree in advance against an
unknown machine and cannot run that search. So the strategies are `A`-dependent
and the bounds are on `Lsync`.

**The gap is real, already at `M = 2`.** Over `I = O = {0,1}` with
`tau(s,x) = s`:

```
A1:  lambda(s,0) = s,  lambda(s,1) = 0
A2:  lambda(s,0) = 0,  lambda(s,1) = s
```

Both minimal; each is synchronized by one input, so `Lsync = 1` on the pair. A
universal tree must commit to its first input before knowing which machine it
faces; whichever it plays, the other emits constant `0` and nothing is learned.
So `Lsyncu = 2`. Verified `verify/universal_gap2.py`; a broader sweep
(`universal_gap.py`) over the 35,640 minimal `M=3` machines gives `Lsync = 3`
against universal depth `>= 4`.

**What is withdrawn.**

- "`Lsyncu(M) <= (M-1)^2`" → holds for `Lsync` only.
- "`Lsyncu(M) <= binom(M,2)`" → holds for `Lsync` only.
- "The finiteness hypothesis in `prop:active-length-upper` is now automatic" →
  **false**; the hypothesis is restored. Finiteness of `Lsyncu(M)` is open once
  `|I| >= 2`.
- §2.37's "upper side closed" was already withdrawn in §2.38; it is now doubly
  so, since it concerned the wrong quantity.

**What survives.**

- `lem:tension` (`d(U) <= M - |U| + 1`) is a statement about a machine's pair
  structure and is unaffected.
- `prop:lsyncu-single-input`: for `|I| = 1` there is only **one** universal
  tree, so `Lsync = Lsyncu` legitimately and `<= M-1` stands for both. This is
  the sole regime where finiteness of `Lsyncu` is established.
- §2.38's attainment findings stand, re-read as statements about `Lsync`:
  `Lsync(M) = Theta(M)` on the evidence.

**Revised status of `open:si-hard-family`.** The question concerns `Lsyncu`.
Establishing *any* bound on it — even finiteness for `|I| >= 2` — is now the
first step, and the `M log M` question is downstream of that. The machine-specific
picture is well understood; the universal one is barely begun.

---

### 2.38 Attainment of `binom(M,2)` is sporadic — and it corrects §2.37

*[A]* §2.37 proved `Lsyncu(M) <= binom(M,2)` and reported it **attained**,
concluding that "the upper side is closed" and any resolution must come from
below. This probe shows that conclusion was **too strong**: attainment holds at
`M = 3, 4` and, on the evidence, nowhere else.

**Why it mattered.** Attainment for all `M` would give
`Lsyncu(M) = Theta(M^2) = omega(M log M)`, resolving `open:si-hard-family`
affirmatively. So this was the decisive probe.

**The extremal structure at M=3,4.** All 576 (M=3) and 3072 (M=4) attaining
machines share one shape: one input is a permutation fixing a sink and cycling
the rest; the other is collapsing and carries the **only** informative output,
emitted from a single **probe** state. The learner can ask only "is the true
state at the probe now?", and must rotate between questions. Traced optimal
play at M=4:

```
{0,1,2,3} -> {0,2,3} -> {0,1,3} -> {0,2} -> {0,3} -> {0,1} -> {0}
```

alternating probe and rotate, total 6 = binom(4,2).

**But the mechanism is linear, not quadratic.** Generalizing it (sink,
`(M-1)`-cycle, single probe) gives depth **exactly `2M-2`** — one rotation plus
one probe per elimination — and the ratio to `M log2 M` *decreases*:
`0.75` at M=4 down to `0.50` at M=13.

| M | max depth found | binom(M,2) | method |
|---|---|---|---|
| 3 | **3** | 3 | exhaustive — attained |
| 4 | **6** | 6 | exhaustive — attained |
| 5 | 9 | 10 | exhaustive over 2,839,200 structured minimal machines |
| 6 | 9 | 15 | hill-climb |
| 7 | 14 | 21 | hill-climb |
| 8 | 14 | 28 | hill-climb |

The gap widens (1, 6, 7, 14), and the best values track `2M-2` at M=4,7,8.

**Revised status.** The upper bound `binom(M,2)` is **not** known to be tight as
`M` grows; §2.37's "upper side closed" is withdrawn. The evidence now points to
`Lsyncu(M) = O(M)`, which would collapse the length currency exactly as the
mistake currency collapsed in §2.34 — i.e. the likely answer to
`open:si-hard-family` is **negative**. This is evidence, not proof: the `M>=6`
searches are heuristic and the exhaustive `M=5` search covers a structured
subclass, not all minimal machines.

---

### 2.37 The separation–size tension is now a lemma; `Lsyncu(M) <= binom(M,2)`, attained

*[A]* §2.36 ended by naming the obstacle: a witness needs `|I| >= 2` and must
combine **many separation episodes** with **long words inside an episode**, but
these pull against each other. That heuristic is now a proved inequality.

**`lem:tension`.** For minimal `A` and `U ⊆ Q_A` with `|U| >= 2`, let `d(U)` be
the length of the shortest word separating some pair inside `U`. Then

```
d(U)  <=  M - |U| + 1.
```

*Proof.* Let `~_k` be the Moore partition after `k` rounds; `s ~_k t` iff no
word of length `<= k` separates them. Put `k = d(U)`. Then all of `U` sits in
one block of `~_{k-1}`. Refinement strictly increases the block count until it
stabilizes, and minimality makes the stable partition discrete, so
`|Q_A/~_{k-1}| >= k`. But `U` occupies one block and the other `M - |U|` states
occupy at most `M - |U|` more, so `|Q_A/~_{k-1}| <= 1 + (M - |U|)`. Combining
gives `k <= M - |U| + 1`.

**`prop:lsyncu-binomial`.** Accounting each episode with `lem:tension` instead
of the crude `M-1`, the sizes visited are at worst `M, M-1, ..., 2` and

```
Lsyncu(M) <= sum_{m=2}^{M} (M-m+1) = M(M-1)/2 = binom(M,2).
```

**The bound is attained**, so this is tight and not merely an improvement:
exhaustive search over all minimal machines with `M <= 5`,
`|I|,|O| <= 3` returns max depth exactly `6 = binom(4,2)` at `(M,|I|,|O|)=(4,2,2)`.

Verified: `verify/tension.py` — **145,924,776** subsets across seven
signatures, **0 violations**, and **16,634,010 tight cases** (`d = M-|U|+1`),
so the lemma cannot be improved pointwise. `verify/tension_proof.py` — both
proof steps checked separately over **13,257,306** minimal machines, 0
violations each. `verify/tension_sum.py` — telescoping arithmetic and the
attainment search.

**What this changes for the open problem.** The improvement over `(M-1)^2` is a
factor approaching 2, and the crossover with `M log2 M` moves from `M >= 5` to
`M >= 7`. More importantly, **the upper side is now closed**: the constant is
`1/2` and the quadratic rate is achieved, so no further sharpening of the upper
bound can settle the question. A resolution must come from the lower side —
exhibiting a *family* whose worst case exceeds `M log M`. The counting
argument above cannot do that, by construction.

---

### 2.36 Single-input machines are linear — the witness search loses an alphabet class

*[A]* Following §2.35, the sharpest available attack was the observation that
single-input minimal machines appeared capped at `M-1`. That is now a theorem.

**`prop:lsyncu-single-input`.** For `|I| = 1` and minimal `A`:

```
L_sync^adapt(A) <= M-1,   and   Lsync(M) = Lsyncu(M) <= M-1.
```

*Proof.* With one letter the learner has no choice of experiment, so `Lsync`
and `Lsyncu` coincide and the adaptive tree degenerates to a path. Define
`s ~_t u` iff the output sequences agree for `t` steps; this is Moore's
partition refinement on the unary automaton. It is monotone and **stabilizes
at the first round that fails to split**, since the refinement step depends
only on the current partition. Minimality makes the stable partition discrete
(`M` blocks). So the block count starts at `>= 1`, increases strictly at each
of the first `R-1` rounds, and reaches `M` — giving `R <= M-1`. After `R`
letters the output prefix pins the block, which is a singleton.

**Consequence (`rem:witness-needs-two-inputs`).** Any family witnessing
`Lsyncu(C_M) = omega(M log M)` **must have `|I| >= 2`**. The reason is
structural: with one letter the transcript is a fixed function of the initial
state, so there is no adaptivity to exploit and the process is pure refinement,
which can occur at most `M-1` times. Depth beyond `M-1` requires the learner's
*choice* of next input to matter.

Verified: exhaustive over all minimal single-input machines with binary output,
`M = 2..6` (`8`, `72`, `960`, `16,800`, `362,880` machines) — depth equals the
refinement-round count in **every** instance, maximum exactly `M-1`; strict
block increase confirmed over `9,313,920` minimal machines at `M=7`.

**A guess of mine that was wrong.** I first conjectured `L = R - 1` and wrote a
check for it; the check returned `False` at every `M`. The joint distribution
of `(R, L)` is supported entirely on the **diagonal** `L = R` — e.g. at `M=6`
the observed pairs are `(3,3): 149,760`, `(4,4): 169,920`, `(5,5): 43,200`.
The off-by-one was in my guess, not the data. The proposition as written claims
only `L <= R <= M-1`, which is what the argument supports and what the
enumeration confirms.

**Where this leaves the problem.** A witness now needs `|I| >= 2` and must
combine two effects that pull against each other: many separation episodes,
and long words within an episode. A machine whose state pairs are slow to
separate tends to have few distinguishable blocks to separate in the first
place. Making that tension precise — or defeating it — is the remaining
substance.

---

### 2.35 `Lsyncu(M) = O(M^2)`: finiteness proved, the length-currency question localized

*[A]* `open:si-hard-family`'s surviving branch asked for a family with
`Lsyncu(C_M) = omega(M log M)`, or a proof that `Lsyncu(M) = O(M log M)`
always. This is now **reduced, not closed** — and the reduction is substantive.

**`prop:lsyncu-quadratic` (new).** For fixed finite alphabets and `M >= 2`:

```
M - 1  <=  Lsync(M)  <=  Lsyncu(M)  <=  (M-1)^2 = O(M^2)
```

*Proof.* Let `U` be the states consistent with the transcript. If `U` holds two
observationally distinct `s != t`, BFS on the pair automaton finds a word `w`,
`|w| <= M-1`, whose last letter makes the descendants of `s` and `t` emit
different outputs. Feeding `w`: deterministic transitions map `U` forward so
`|U|` never increases, and at the last letter whichever output is observed
eliminates at least one branch, so `|U|` strictly drops. At most `M-1` such
episodes, each `<= M-1` steps, gives `(M-1)^2`. The strategy depends only on
the alphabets and the pair automaton, both fixable in advance, so it bounds
`Lsyncu`.

**Immediate payoff.** The hypothesis `Lsyncu(M) < infinity` in
`prop:active-length-upper` is now automatic and has been dropped; that
proposition holds unconditionally.

**Why this does not settle the open problem.** The rates cross: `(M-1)^2`
exceeds `M log2 M` for `M >= 5` (at `M=128`: `8128` vs `896`). So a quadratic
upper bound leaves room for `omega(M log M)`.

**Evidence, which points the other way.**

| probe | result |
|---|---|
| exhaustive, all minimal machines `M<=5`, `|I|,|O|<=3` | max adaptive depth `= M-1` for `|I|=1`; never above `C(M,2)` |
| separating word for a pair, 79,334,966 separable pairs | `0` violations of `|w| <= M-1`; max observed `3` |
| cyclic counter, one marked state | `M-1` — ratio to `M log2 M` *decreases* (`0.50 -> 0.256` as `M: 2 -> 12`) |
| cyclic-shift family (the `EsyncSI` witness) | `log2 M`, far below |
| hill-climbing over **minimal** machines to `M=20` | ratio never exceeds `0.78`, trends down |

A caution worth recording: an earlier hill-climb *without* enforcing
minimality produced ratios up to `1.55`, which looked like a superlinearithmic
family. Those machines were non-minimal, so their "homing length" was being
measured to `|U|=1` rather than to a single observational class — the wrong
target under `def:output-aware-sync`. Enforcing minimality removed the effect
entirely. This is the same class of error as the `m_K` proxy in §2.22.

**Status.** The question is now *about the exponent*: `Lsyncu(M)` lies between
`M-1` and `(M-1)^2`, with the decisive threshold `M log M` strictly inside.
Finiteness — previously an explicit hypothesis — is settled. If the
linearithmic side is correct, the length currency collapses exactly as the
mistake currency did in §2.34.

---

### 2.34 `EsyncSI(M) = floor(log2 M)` exactly, with no alphabet dependence — **§2.27's residual question closed, and the bound sharpened**

*[A]* §2.27 proved `EsyncSI(M) = Theta(log M)` and left open whether the
upper constant `1/log(|O|/(|O|-1))` is attained for `|O| > 2`. The answer is
**no** — and the reason is that the old upper bound was loose. The truth has
**no alphabet dependence at all**.

**Sharpened upper bound (`prop:esyncsi-log`).** Partition the version space `V`
by the value of `lambda(.,x)` into output classes `c_1 >= c_2 >= ... >= c_r`,
`r <= |O|`. The learner predicts the plurality symbol. If it errs, the observed
symbol realizes some class `c_j`, `j >= 2`, and the survivors are **that single
class** — not the union of all non-predicted classes. Since `c_1 >= c_2` and
`c_1 + c_2 <= |V|`:

```
2 c_2 <= c_1 + c_2 <= |V|      =>      c_2 <= |V|/2
```

Every mistake halves the version space, for **every** `|O| >= 2`. Hence
`EsyncSI(M) <= floor(log2 M)`.

**Matching lower bound.** The cyclic-shift family uses only two output symbols,
so it is available verbatim for every `|O| >= 2`. Therefore

```
EsyncSI(M) = floor(log2 M)      for every |O| >= 2, |I| >= 1.
```

**What was wrong before.** The old count replaced "survivors are one class of
size `c_2`" with "survivors are everything not predicted", giving `1 - 1/|O|`
and a bound that degrades without limit as the alphabet grows: at `M = 1024` it
reads `10.0, 17.1, 24.1, 51.9` for `|O| = 2,3,4,8`. That was an artefact of the
counting, not of the problem — a deterministic machine sends each surviving
state to exactly one symbol.

**A distinction that had to be checked** (`verify/halving_distinction.py`).
The sharpening does **not** transfer to `thm:active-halving`. There the version
space is machine–state *pairs* with the machine unknown, and a mistake retains
the *complement* of the predicted class, whose size does approach
`(1-1/|O|)|V|` as classes fragment. Numerically, at `n=24, r=8` the SI
survivor fraction is `0.375` while the RI fraction is `0.875`. The two halvings
are genuinely different arguments; `thm:active-halving` correctly keeps
`1-1/|O|`, and the manuscript now says so explicitly.

Verified: `verify/esyncsi_exact.py` (400k random class profiles per alphabet
size — max survivor fraction exactly `0.5` for `|O| = 2,3,4,5,8`);
`verify/esyncsi_halving.py` (68,380 integer class profiles, `n<=25`, `r<=5`, no
violation of `c_2 <= n/2`, equality iff `c_1=c_2` and `r=2`);
`verify/esyncsi_exhaustive4.py` (nine signatures, all minimal machines,
largest 46,656 table pairs / 35,640 minimal — worst case never exceeds
`floor(log2 M)` and attains it at `M=2,4`, unchanged as `|O|: 2 -> 4`).

**Consequence.** `rem:additive-collapses` is now exact rather than
order-of-magnitude, and `open:si-hard-family` is reduced to its single
remaining question about the experiment-length currency.

---

### 2.33 The jump ratio `kappa` is an absolute constant — **§2.31's residual question closed**

*[A]* §2.31 established that the sum-form envelope `inf_M [a_M + b_M]` is
reachable from the min-form floor through `lem:discrete-bv-sandwich`, at the
cost of a factor `(1+kappa)`, and left open whether `kappa = O(1)`. It is, and
the proof is short.

**`lem:kappa-bounded`.** For a regularly varying estimation envelope
`b(M) = gamma * M^alpha * (log eM)^beta` with `alpha, beta >= 0`:

```
b(M)/b(M-1) <= b(2)/b(1) = 2^alpha (1 + log 2)^beta      for all M >= 2
```

so `kappa <= 2^alpha (1+log2)^beta` wherever the crossing falls. **The bound
depends only on the exponents** — not on the horizon `T`, not on the scale
`gamma`, not on the approximation envelope.

*Proof.* Factor `b(M)/b(M-1) = (M/(M-1))^alpha * (log eM / log e(M-1))^beta`.
The first factor is decreasing since `M/(M-1) = 1 + 1/(M-1)`. For the second,
put `l(x) = 1 + log x`, positive/increasing/concave; then `l(x)/l(x-1)` is
nonincreasing, because the derivative's sign is that of
`l'(x)l(x-1) - l(x)l'(x-1)`, and concavity gives `l'(x) <= l'(x-1)` while
monotonicity gives `l(x-1) <= l(x)`. Product of nonincreasing positives is
nonincreasing, so the sup is at `M=2`. For sums of such terms the mediant
inequality `(sum x_j)/(sum y_j) <= max_j x_j/y_j` gives the max over terms.

**Values for this paper's envelopes** (`rem:kappa-values`):

| envelope | `(alpha,beta)` | `kappa <=` | `1/(1+kappa) >=` |
|---|---|---|---|
| `sqrt(T log eM) + log eM` | `(0,1/2),(0,1)` | `1+log2 = 1.6931` | `0.371` |
| `sqrt(T M log eM)` | `(1/2,1/2)` | `sqrt(2(1+log2)) = 1.8402` | `0.352` |
| `M log eM` | `(1,1)` | `2(1+log2) = 3.3863` | `0.228` |

Verified `verify/kappa.py` (451 exponent pairs on a grid, sup always exactly
`2^a(1+log2)^b`, 0 mismatches; sup attained at `M=2` in every case) and
`verify/kappa_proof.py` (monotonicity of both factors to 40 digits over
`M<=20000`, max increase `0.0`; mediant bound over 16 `(A,B)` scale pairs,
0 violations; `T` swept `1e2..1e16` with `kappa` constant at `1.30120989105`).

**Edge case.** Bare `M log M` vanishes at `M=1`, violating positivity in
condition (a) of the sandwich; the correct normalization is `M log eM`. If one
insists on `M log M`, the crossing index is `>= 3` and
`sup_{M>=3} = 3log3/(2log2) = 2.3774`, again absolute.

**Consequence.** The sum-form minimax lower bound
(`thm:oracle-minimax-lower`, second display) holds with an **absolute**
constant, and no direct-sum construction is needed to obtain it. What a
both-axes construction would still buy is a bound whose two components are
certified by a single adversary — a statement about the *source* of the
difficulty, not the size of the constant. §2.29/§2.31's residual question is
therefore closed; item 3 of the inventory loses one of its two open parts.

---

### 2.30 Full-KL retention is APX-hard — **elevated from promise-hardness**

*[A]* `thm:full-kl-promise-np` gave NP-hardness under a promise. That is
weaker than the construction actually supports. The embedding controls the
objective **relatively**, not merely across a promise gap:

```
RetKL(C) = (2 d delta^2 / n) * Xi(C) + rho(C),   |rho(C)| <= C0 d^2 delta^3 Z^3
```

**uniformly over all partitions C**, where `Xi` is the k-means objective.
Verified (`verify/apx.py`): the ratio `RetKL(C) / [(2d delta^2/n) Xi(C)]` lies
in `[1.0000271, 1.0000465]` at `delta=1e-3` and equals `1.0` to 12 digits at
`delta=1e-7`, uniformly over **all** 2-block partitions, for `d=2,3`.

Two normalizations make the transfer relative rather than absolute: rescaling
by `lcm(1..n)` forces every nonzero `Xi` value to be `>= 1` (granularity, as in
`lem:kmeans-gap`), and `delta <= eps1/(2 C0 d n Z^3)` — polynomially many bits —
forces the remainder below `(eps1/4) * beta`. Then

```
(1 - eps1/4) beta Xi(C)  <=  RetKL(C)  <=  (1 + eps1/4) beta Xi(C)
```

simultaneously for all `C`, so a `rho`-approximation to `RetKL` yields a
`rho (1+eps1/4)/(1-eps1/4)`-approximation to k-means.

Since Euclidean k-means is APX-hard (Awasthi–Charikar–Krishnaswamy–Sinop,
SoCG 2015; constant improved to `1.0013` by Lee–Schmidt–Wright, IPL 2017),
`cor:full-kl-apx` gives: **there is `eps0 > 0` such that approximating
`RetKL(k)` within `1+eps0` is NP-hard; no PTAS exists unless P=NP.**

Still not claimed: exact NP-**completeness**, blocked by the arithmetic of
comparing a rational to a sum of `p log(p/q)` terms (`rem:full-kl-promise-scope`).

---

### 2.31 The sum-form envelope does not require a direct-sum construction — **my own overstatement corrected**

*[A]* `rem:floors-two-axes` (added turn 19, responding to audit item 5.1)
asserted that a lower bound of order `inf_M [a_M + b_M]` **requires** a
construction forcing both axes on disjoint rounds. That is too strong, and the
manuscript already contained the refutation.

`lem:discrete-bv-sandwich` gives `B <= A <= (1+kappa) B` with
`B = sup_M min{a(M), b(M)}` and `A = inf_M [a(M)+b(M)]`. So a floor calibrated
against the **minimum** yields a bound against the **sum** automatically:

```
sup_P Reg_T  >=  c B  >=  [c/(1+kappa)] * inf_M [ A_T(M) + E_M(T) ]
```

which is already the second display of `thm:oracle-minimax-lower`. Verified
(`verify/sum_vs_min.py`): 380,910 random discrete envelope pairs satisfying the
nondegeneracy and crossing conditions, **0 violations** of either inequality;
observed `A/B` ratios up to 122, and the upper bound is essentially tight
(min slack `1.000006`).

**Corrected role of a direct-sum construction.** It is *not* needed to reach
the sum-form envelope. It is needed only to remove the factor `(1+kappa)` —
the jump ratio of the estimation envelope at the crossing index. Whether
`kappa = O(1)` in the finite-state regimes, or whether a both-axes construction
is genuinely required to avoid it, is the residual open question, and it is
strictly narrower than what I previously recorded.

---

### 2.32 The information-bottleneck identity is verified exact

*[A]* Flagged last turn as an item resting on the lumpable-quotient
formulation and not re-derived. Now checked directly (`verify/ib_identity.py`):
over stationary chains with `|S+| <= 5`, `|O| <= 4`, enumerating **all** set
partitions (not just a sample), the three quantities

```
RetKL(phi),    I(S;Z | K_phi),    I(S;Z) - I(K_phi;Z)
```

agree to `7.6e-16`. `thm:predictive-info` is an exact identity, and the caveat
is withdrawn. Recorded in `rem:retention-numerical`.

---

### 2.27 State identification costs `Θ(log M)` — **matching lower bound proved**

*[A]* `prop:esyncsi-log` gave `EsyncSI(M) ≤ log_{|O|/(|O|−1)} M` by halving.
The tightness question — the first half of `open:si-hard-family` — is now
closed by `thm:esyncsi-theta`:

```
EsyncSI(M) = Θ(log M)     for every fixed |O| ≥ 2.
```

**Family.** `Q = {0,1}^L`, `M = 2^L`, one input `d` acting as the left cyclic
shift with `λ(v, d) = v₁`. Tables known, initial state unknown.

- *Minimal*: `v ≠ w` differ at coordinate `j`, and `d^{j−1}` makes the next
  output separate them. All `M` states pairwise distinguishable.
- *Deterministic*: at round `t ≤ L` both completions of bit `v_t` remain
  consistent, so the adversary answers `1 − ŷ_t`. Forced `L = log₂M` mistakes.
- *Randomized*: under a uniform initial state each freshly revealed bit is
  conditionally fair, giving `L/2` expected mistakes; averaging fixes a target.

Verified exhaustively, `verify/esyncsi_lower.py`, `L = 1…9`: deterministic
mistakes exactly `L`, Bayes-optimal randomized exactly `L/2`, in every case.

**Why the two bounds meet.** Halving says each mistake removes a `1/|O|`
fraction of the version space; this family is the case where each mistake
removes exactly half and no more, because each round exposes one fresh
unconstrained bit. It is extremal for the halving argument
(`rem:esyncsi-tight`).

**Consequence.** The collapse of the additive form
(`rem:additive-collapses`) is now **unconditional** — a two-sided estimate, not
an upper bound alone — so no choice of subclass rescues a mistake-currency
decomposition. `open:si-hard-family` retains only its second question: whether
a genuine two-term decomposition exists in the **experiment-length** currency.

---

### 2.28 The Csiszár chain-rule proof was invalid — **repaired**

*[A]* **Severity A.** The proof of `lem:csiszar-representation` specialized the
chain rule to **product** distributions and extracted

```
Δ(ε) = ε²[ g(uv) − u g(v) − v g(u) ] + O(ε³),
```

concluding `g(uv) = u g(v) + v g(u)` and hence `g = c·t log t`.

**This cannot be correct, and the error is demonstrable.** Reverse KL,
`g(t) = −log t`, is an `f`-divergence that **is** additive over products, yet
is not a multiple of `D_KL`. For `u = 2, v = 3` the claimed coefficient is
`+2.4849` for reverse KL, while the true product-additivity defect is `0` to 50
digits (`verify/csiszar_defect.py`). The displayed `ε²` coefficient is simply
the wrong one; the correct second-order coefficient vanishes for **both**
forward and reverse KL, so product additivity cannot separate them.

**Repair.** Use the chain rule with a genuinely **non-product** conditional.
Take `X` binary, `q_{Y|X} = q'` on both branches, `p_{Y|X} = p'` on `x = 1` and
`= q'` on `x = 2`. The branch-2 conditional term vanishes, the `(1−α)g(ρ)`
terms cancel **exactly** — no expansion needed — and dividing by `α` gives

```
Σ_j q'_j g(u t_j) = g(u) + u Σ_j q'_j g(t_j).      (†)
```

Differentiating a two-point `(q', p')` at `β = 0`, with the affine
normalization `g'(1) = 0`:

```
g(uv) = g(u) + u g(v) − u(1−v) g'(u).             (‡)
```

The left side of (‡) is symmetric in `u, v`; equating with its transpose gives
`(u g'(u) − g(u))/(u − 1) = const = c`, whose solution with `g(1) = g'(1) = 0`
is `g(t) = c(t log t − t + 1)`.

Verified, `verify/csiszar_repair.py`: (†) holds to 1e−41 for forward KL and
**fails** for reverse KL (defect −0.1657), χ² (+0.8899), Hellinger (−0.0510);
the ODE quotient is constant only for forward KL. The `P`-weighting of the
conditional term is what breaks the forward/reverse symmetry, and it is
invisible unless `P_{Y|x}` genuinely depends on `x` (`rem:csiszar-conditional-needed`).

---

### 2.29 The oracle floor definition was vacuous in realizable regimes — **fixed**

*[A]* `ass:oracle-floors`(i) *defined*

```
Δ_M ≝ min{ A_T(M), E_M(T) },
```

and `prop:floors-instance` then claimed a family with `Δ_M = Θ(M log M)`. These
are inconsistent: the instance regime is **realizable**, so `A_T(M) = 0` and the
defined `Δ_M` is **0**. The floor then asserts only `(1/m)Σ_i R_i(h) ≥ 0`,
which is automatic — the assumption was vacuous exactly where it was being
discharged. The conclusion's own bullet ("No concrete regime is shown to
satisfy the oracle floors") contradicted the proposition, and was closer to the
truth.

**Fix.** `Δ_M` is now a free parameter of the packing, with the envelope
comparison split off as a separate clause:

- (i) **Packing floor**: `(1/m) Σ_i R_i(h) ≥ Δ_M` for every predictor.
- (ii) **Envelope calibration**: `Δ_M ≥ min{A_T(M), E_M(T)}`.

`prop:floors-instance` now discharges **both** and states explicitly that,
being realizable, it certifies the **estimation axis only**.

**A second, subtler point** (`rem:floors-two-axes`). A packing *inside* `H_M`
certifies estimation difficulty; certifying *approximation* difficulty requires
members **outside** the reach of `H_M`. These are different families, and
proving each separately does **not** give a lower bound of order
`inf_M[a_M + b_M]` — a learner facing the approximation-hard family may pay
`a_M` with no estimation burden, and conversely. A bound on the **sum** needs a
single adversary forcing both on disjoint rounds. No such construction is
supplied, so the assumption is calibrated against the **minimum**, which is what
`lem:discrete-bv-sandwich` actually consumes. **This remains open.**

---

### 2.10 Hardy-space embeddings versus the default converse — severity C

**Statement.** Identify when a Hankel operator admits a Hardy-space embedding
making AAK applicable, and compare the resulting converses with the default
Eckart–Young–Mirsky converse.

**Relation to §2.2.** This is the *scalar-case* form of the same question.
§2.2 asks for an intrinsic criterion in the genuinely multi-letter setting;
this item asks the narrower comparative question of how much the AAK converse
improves on EYM when an embedding does exist. Since
`Δ_grd^unres = σ_{M+1}` already, the content is entirely about the
*structured* gap: AAK converts the inequality
`Δ_grd^Hank,str ≥ σ_{M+1}` into equality, with an attained optimum of rational
symbol degree `≤ M`. The comparative question is therefore whether the
structured gap is ever *strictly* larger — equivalently, by the strictness
corollary, whether a compact Hankel operator arising from a finite-state
channel can fail to be Hardy-representable. *[M]* The manuscript exhibits no
such example and asserts none; whether one exists is not addressed there.

*[A]* This item and §2.2 are the scalar and multi-letter forms of one question
and are best read together.

---

### 2.11 Intermediate Rényi orders — severity C

**Statement.** Can `α ∈ (0,∞) \ {1}` be made operational as finite-state
regimes with matching rank-control and domination?

**Status.** *[M]* The three vertices `α ∈ {0, 1, ∞}` correspond to commitment,
retention, and grounding. Intermediate orders may organize interpolation
inequalities but do not currently define regimes.

**What "operational" would require, explicitly.** By the response-representation
definition, an `α = p` regime needs three components supplied simultaneously:
1. a **task theory** — a class of budget-`M` approximants with a cost;
2. a **response operator** `A_δ` and an effective rank budget
   `r(M)`, so that budget `M` implies `rank A_δ̂ ≤ r(M)`;
3. a **domination modulus** `c_p > 0` with
   `L(δ, δ̂) ≥ c_p^{-1} ‖A_δ − A_δ̂‖_p`.

Given all three, Mirsky's theorem immediately yields the tail bound
`Δ(M) ≥ c_p^{-1} Φ^{(p)}_{r(M)}(A_δ)`. *[A]* The difficulty is therefore not
the analysis but the **modelling**: no finite-state approximation problem is
known whose natural cost is a Schatten-`p` norm for `p ∉ {1, ∞}`. Component 3
is the binding constraint, which is why this item is a special case of §2.8.

---

## 2.40 Unifilar retention: what the elevation settles and what it opens

The retention theory now holds for general unifilar controlled machines
(`subsec:unifilar-retention`). Three things were settled this turn, and two
new questions opened.

**Settled.** The controlled information-bottleneck identity
`RetKL^ctrl(phi) = I(S;Y|K,X) = I(S;Y|X) − I(K;Y|X)` holds for every
unifilar-lumpable quotient under i.i.d. inputs independent of the state; the
three spectral converses (quadratic, probability-coordinate, interior Fisher)
apply fiberwise, because the lumpability constraint does not depend on the
input; and the zero-retention threshold is the index `N*` of the coarsest
unifilar-lumpable refinement of the predictive-kernel partition.

**A correction worth recording.** The threshold is *not* the number of distinct
predictive kernels. In the input-driven theory the two agree, because the
kernel partition is automatically lumpable there; in the unifilar class it
generally is not, and `N*` exceeds the kernel count in a majority of sampled
instances. Equivalently: `phi_ker^*` is the causal-state partition for the full
controlled future, and `phi_ker` is its one-step coarsening — the distinction
already flagged at `def:z-predictive-equivalence`, now with a threshold theorem
attached to it.

**Open (a): the rate of the refinement.** `prop:kernel-refinement-exists`
bounds the number of refinement rounds by `|S+|` and hence `N* ≤ |S+|`, and the
bound is attained (the witness of `rem:controlled-zero-not-kernels` has
`N* = |S+| = 3` from a two-kernel start). What is not known is the *typical*
or *worst-case* gap `N* − |phi_ker(S+)|` as a function of the alphabet sizes:
whether there are families with `|phi_ker| = 2` and `N*` growing, and at what
rate in `|I|`, `|O|`. This is the unifilar analogue of the `Lsyncu` rate
question of `open:si-hard-family`, and is likely easier, since the refinement
is a Moore recursion rather than a search over experiments.

**Open (b): complexity of the controlled gap.** `rem:complexity-transfer`
shows the existing hardness results survive the enlargement, but they are all
proved on machines where the two feasible sets coincide. Whether computing
`RetKL^ctrl(M)` is *harder* than `RetKL(M)` on machines where the sets differ
— where the optimizer may exploit disjoint emission supports to use a quotient
no input-driven analysis would admit — is open. The verified value separation
(`0.5312` vs `0.6817` on a three-state machine) shows the enlarged set is
genuinely exploitable, so the question is not vacuous.

**A modelling caveat that turned out to be load-bearing.**
`def:unifilar-machine` requires only a stationary ergodic input, which permits
`X_t` correlated with `S_t`. Under correlation the controlled IB identity
fails, by up to `0.139` nats in sampled instances, because the block weights
`pi_s/pi(C_k)` cease to be conditional weights given `X_t = x`. The identity is
therefore stated with independence as an explicit hypothesis
(`rem:controlled-ib-independence`). Restoring it for correlated inputs — by
recomputing block weights fiberwise — is straightforward in principle and has
not been carried out here; whether the fiberwise spectral converses survive that
reweighting is not obvious, since the fibers would then carry different
effective state distributions.

---

## 2.41 Feasibility triage of the remaining open items

Each item below was probed computationally before being ranked
(`verify/feas_probes.py`). Two are now resolved in outline and need only be
written up; three are structural and will not yield to further computation.

### Tier 1 — RESOLVED AND WRITTEN UP (Turn 44)

Both items below are now theorems in the manuscript:
`thm:controlled-ib-general` with `def:controlled-full-kl-general`,
`cor:controlled-elementary-general`, `cor:controlled-simplex-general` and
`rem:controlled-general-reweighting`; and `def:counter-family` with
`prop:refinement-extremal` and `rem:refinement-extremal-scope`.

**(T1a) Controlled IB for correlated inputs.** §2.40 recorded this as
"straightforward in principle" but uncarried-out. It is now checked: replacing
the block weight `pi_s/pi(C_k)` by the conditional weight `P(S=s | K=k, X=x)`
restores the identity exactly for non-product `(S,X)` — max deviation
`5.0e-16` over 30,000 instances with correlated joint laws. The proof is the
existing one with the conditional weight substituted, since the only step that
used independence was the identification of the centroid with a conditional
law. The open part of §2.40 was whether the *fiberwise spectral converses*
survive; they do, because each fiber is still a fixed finite family under a
fixed quotient, but the covariance must be recomputed with the conditional
weights, which changes `Sigma_p^x`.

**(T1b) Worst-case size of the stable refinement.** §2.40 asked whether
families exist with `|phi_ker| = 2` and `N*` growing, and at what rate. Both
are now answered by an explicit family: `|I| = 1`, `|O| = 2`, states `0..M-1`,
`tau(s, y=0) = min(s+1, M-1)` and `tau(s, y=1) = 0`, with state `M-1` carrying
one predictive law and `0..M-2` sharing another. Then `|phi_ker| = 2` while
`N* = M`, so the gap is `M - 2`, the largest possible; and the refinement
recursion takes exactly `M - 1` rounds, showing the `|S|`-round bound of
`prop:kernel-refinement-exists` is tight to within one. Verified for
`M = 3..15`. The proof is induction on the counter.

### Tier 2 — structural, not reachable by computation

**(T2a) NP membership for full-KL retention.** The objective compares a
rational threshold against a sum of logarithms of rationals. Sampling shows
distinct objective values separated by as little as `3.0e-64`, so the decision
turns on effective lower bounds for linear forms in logarithms — Baker theory —
not on any refinement of the reduction. Numerical work cannot close this.

**(T2b) Fixed-alphabet hardness of full-KL retention.** *(Superseded in
Turn 45 — the conclusion recorded here was wrong.)* This entry asserted that
`|O| = 2d` cannot be reduced, on the ground that the append-coordinate map
`R^d -> R^{d+1}` is not a similarity. That argument shows only that **one**
candidate map fails, and the conclusion drawn from it does not follow. The
correct statement, now `rem:output-alphabet-2d`, is that the minimal alphabet
is governed by a Hadamard-type condition:

- `|O| >= d+1` always, since the zero-sum subspace has dimension `|O|-1`;
- `|O| = 2d` always works, via the doubling map with `c = 2`;
- `|O| = d+1` works exactly when the zero-sum subspace of `Q^{d+1}` admits `d`
  pairwise orthogonal rational vectors of equal norm. For `d = 2` it does not,
  by a discriminant argument (`disc = 12 ~ 3` mod squares, while a scalar form
  has class `1`), confirmed by exhaustive search. For `d = 3` it **does**: the
  three non-constant rows of a Hadamard matrix of order 4 are zero-sum,
  pairwise orthogonal and of norm 4. Likewise for `d = 7, 15, ...`

So the factor two is *not* slack at `d = 2` but *is* slack at `d = 3, 7, 15`.
Fixed-alphabet hardness nevertheless remains open, for the robust reason that
`|O|` must exceed `d` in every case, so a fixed alphabet caps the embeddable
dimension; a proof would need a source problem hard in bounded dimension.

**(T2c) `conj:lsyncu-poly`.** Exhaustive computation of `Lsyncu` is out of
reach: with `|I| = |O| = 2` the reachable class has 192 machines at `M = 2`,
27,648 at `M = 3` and 8,060,928 at `M = 4`, and the universal-tree search runs
over *subsets* of machine-state pairs — up to `2^82944` version states already
at `M = 3`. A direct search settles `M = 2` only. Progress requires a
combinatorial argument, not enumeration.

### Tier 3 — unchanged in status

`open:hankel-multiletter` (needs a multi-shift Nehari/AAK theorem),
`open:symbolic-grounding` (needs Boolean realization theory),
`open:si-hard-family` (subsumes T2c), `conj:cross-terms` (three separate
conditional statements, each requiring its own domination hypothesis), and the
necessity of `Psi_M(T)` together with the floors of `ass:oracle-floors` outside
the realizable persistent-stream regime.

---

## 3. Conjectures

All four clauses below are stated as *conjecture*, not theorem.

| # | Conjecture | Missing hypothesis |
|---|---|---|
| C1 | `Δ_grd^{L¹}(M) ≳ Σ_{i>M} σ_i(H_ν)` | `H_ν` trace class **and** nuclear-norm domination |
| C2 | `Δ_ret^{L^∞}(M) ≳ ½ λ_M(Σ_π)` | worst-case quadratic surrogate, or geometry aligning worst-case state with top Fisher direction |
| C3 | `Δ_T(M) ≳ (Σ_{i>r(M)} σ_i(A_δ)²)^{1/2}` | explicit Schatten-2 domination bridge |
| C4 | Intermediate `α` organize interpolation | matching task theory + bridge + rank control |

*[A]* **C1 and C3 are instances of the general domination problem** (§2.8):
each becomes a theorem the moment its bridge is supplied — a nuclear-norm
bridge for C1, a Schatten-2 bridge for C3. C1 additionally requires `H_ν` to be
trace class, which is a hypothesis on the object rather than a bridge.

**C2 is not a domination problem.** It asks for a *single-eigenvalue* bound
`≳ ½ λ_M(Σ_π)` rather than a tail, and what it needs is a worst-case quadratic
surrogate, or geometry aligning the worst-case state with the top Fisher
eigendirection. Supplying a domination bridge would not settle it; the missing
ingredient is a change of aggregation (worst-case rather than stationary),
which is a §5.5-type question about aggregation, not a §2.8-type question about
operator norms.

C4 restates §2.11.

---

## 4. Standing hypotheses that are assumed, not verified

These are *gaps of a different kind*: results are proved, but conditionally, and
the conditions are not discharged.

| Hypothesis | Used by | What discharging it needs |
|---|---|---|
| **Packing floor** (10 refs) | oracle minimax lower bound | **Discharged for the realizable stream regime** (`prop:floors-instance`). The former *two-point* form was **disproved** — capped at `2 log 2`. Other regimes open (§2.3) |
| **Operational equivalence** (5 refs) | active `Ω(E_sync)` lower bound | **Discharged**: now a *lemma* for deterministic realizable classes, proved via `lem:moore-separation`. Remains an assumption only for stochastic classes |
| **Regular BV envelope** (4 refs) | continuous sandwich `B_T ≤ A_T ≤ 2B_T` — **no longer load-bearing**, the minimax proof routes through the discrete lemma | verification that regime envelopes are positive, continuous, oppositely monotone, and crossing |
| **Bounded-error succinctness family** | determinism gap | **Discharged as a citation, and the claim corrected downward.** Ambainis (1996) proves `Ω(2^{k loglog k / log k})`, which is `2^{o(k)}` — superpolynomial, *not* exponential. The theorem is now parameterized by the rate `S(k)` |
| **Spectral-rate assumptions** | budget laws | achievability, not merely converses |
| **Schatten-`p` domination** | unified converse template | §2.8 |

**On the active objective.** `Ω(M log M)` for active learning holds relative to
a *guaranteed-prediction* objective, and some such objective is unavoidable: in
the bare protocol a learner may play the reset letter forever, making no
mistakes and learning nothing.

**On the scope of the surviving hypotheses.** *[A]* Operational equivalence and
direct-sum saturation are now explicitly *subclass* hypotheses. `E_sync` is
parameterized as `E_sync(C_M)` for `C_M ⊆ H_M`, with `E_sync(M) = E_sync(H_M)`.
On the full class the additive form collapses — `M log M + E_sync(M) =
Θ(E_sync(M))` by `cor:active-theta` — so those hypotheses carry content only
where `log₂|C_M|` is not `O(M log M)` and the two terms can separate. Any
future use of the additive form should name the subclass.

---

## 5. Structural and scope limitations

**5.1 Boundedness of formal Hankel matrices.** For general response `h`, the
formula `(H_δ e_u)(v) = h(uv)` need not define a bounded operator on `ℓ²(Σ*)`;
the rows need not be square-summable. All spectral statements are scoped to
*spectrally admissible* task theories (bounded **and** compact). A sufficient
condition is geometric decay via the Schur test. **Not resolved:** an intrinsic
characterization of which channels are admissible.

**5.2 Algebraic vs. operator rank.** A `k`-state weighted automaton gives
algebraic Hankel rank `≤ k` via `h(uv) = αᵀ T_u T_v η`. This does **not** imply
boundedness or compactness. The exponential determinism gap is therefore a
separation between *formal linear realization dimension* and deterministic state
complexity — not an instance of the compact-operator spectral theorem.

**5.3 The exponent correspondence is a labelling.** `α = p` across
`{0, 1, ∞}` is a formal consistency, not a derivation. It does not produce the
Mirsky converses, and none of the analytic theorems depend on it.

**5.4 The spectral-tail principle is a heuristic.** The tail form depends on
operator-approximation vs. clustering, linear vs. affine subspaces, rank vs.
state count, compactness/trace-class/domination assumptions, and the aggregation
norm. **Aggregation alone does not determine the tail.**

**5.5 Average-case zero error.** The Boolean dichotomy is a biconditional under
worst-case aggregation. Under a `μ`-average, the correct quantity is the
*observable support index* `κ_obs(δ,μ)`, not a naive restriction of `∼_δ` —
which need not even be a right congruence when `supp μ` is not right-closed.

**5.6 One-step vs. full-future predictive equivalence.** Equality of next-output
laws is strictly coarser than causal-state equivalence and **need not be a right
congruence**. Explicit counterexample: four states where `s₀ ∼_Y s₁` but their
successors are inequivalent, so the induced partition is not lumpable. All
lumpability converses assume `∼_Z` is a congruence.

---

## 6. Cross-cutting dependency structure

Several items collapse if one is solved.

```
Domination bridges (§2.8)
        │
        ├──> C1  (L¹ grounding, nuclear tail)   [+ H_ν trace class]
        ├──> C3  (Schatten-2 / Frobenius)
        └──> Unified Schatten template becomes unconditional

C2  (L^∞ retention, single eigenvalue)
        └──> needs a worst-case aggregation surrogate, NOT a domination
             bridge; independent of §2.8

Multi-alphabet Hankel embedding (§2.2)
        └──> Hankel-structured equality for |Σ| > 1
             (does NOT reach §2.1: the symbolic gap is over deterministic
              Mealy machines, and the manuscript states explicitly that the
              linear relaxation does not transfer to it)

Separation floors (§2.3)
        └──> oracle minimax becomes unconditional
                └──> only Ψ_M(T) necessity (§2.4) remains
     (the former second dependency of this node, envelope regularity, has been
      removed: the discrete sandwich lemma discharges it outright)
```

*[A]* **Highest leverage:** §2.8 (domination bridges) — it converts C1 and C3
and makes the central template unconditional. It does *not* reach C2. **Most
self-contained:** §2.3 (separation floors), which requires explicit
constructions rather than new theory. **Requiring new mathematics:** §2.1 and
§2.2, which are moreover *independent* of one another: solving the Hankel
embedding question would not advance the symbolic gap, since the two concern
different feasible sets (finite-rank operators versus deterministic machines).
These are judgements about tractability, not results.

---

## 7. What is *not* open

*[M]* For contrast, the following are established in the manuscript. "Settled"
here means: proved under hypotheses that are either vacuous or intrinsic to the
object (finiteness, compactness, distinctness of predictive laws), rather than
under an auxiliary assumption of the kind catalogued in §4. Two caveats apply
throughout. First, the persistent-stream and agnostic lower bounds rest on the
manuscript's own adversary construction rather than on external literature, so
they carry the usual risk attaching to a new proof. Second, all spectral
statements are scoped to spectrally admissible task theories (§5.1).

- Myhill–Nerode commitment threshold `Δ_com(M) = 0 ⟺ M ≥ κ_det(F)`.
- Full-KL information-bottleneck identity over lumpable quotients.
- Zero retention `⟺ M ≥ |S⁺|` for pairwise-distinct predictive laws on the
  stationary support.
- Quadratic spectral converse `Δ_ret^quad(M) ≥ ½ Σ_{i≥M} λ_i(Σ_π)`, effective
  rank `M − 1`.
- `Δ_grd^unres(M) = σ_{M+1}(H_ν)` (Eckart–Young–Mirsky).
- NP-completeness of Gaussian quadratic retention, already for reset machines of
  synchronization depth one.
- Persistent-stream mistake complexity `Θ(M log M)`, **all** alphabets with
  `|I| ≥ 2`, `|O| ≥ 2`; deterministic worst case, randomized expectation, and a
  high-probability bound via Yao + Azuma.
- Agnostic regret `Θ(√(T·M log M))`, both protocols.
- Active realizable upper bound `O(E_sync(M))` under objective (RI), sharp and
  unconditional, with no appended continuation term (all three objectives of
  the active section are *prediction-closing*, so attainment cost is total
  cost).
- **Active realizable mistake complexity `Θ(M log M)` on the full class,
  unconditionally** — halving upper bound against the gated lower bound, with
  no synchronizability, operational-equivalence, or direct-sum hypothesis.
- Active realizable lower bound `Ω(M log M)` on the **gated** family
  `G^act_M`, deterministic and randomized, the latter by a first-emission
  martingale argument valid against adaptively chosen inputs rather than a
  fixed stream (§2.9a).
- Discrete bias–variance sandwich `B ≤ A ≤ (1+κ)B` from monotonicity plus two
  discrete conditions, with `1+κ` attained.
- `Ldim^stream(H_M) = Θ(M log M)`.
- Pinching majorization and the free-lunch characterization for the linear
  surrogate.
- Independence of the three regime obstructions; no universal cross-regime
  ordering.
- Non-existence of a universal global full-KL spectral converse (§2.6).

---

## 8. Suggested priority *[A]*

0. *(Narrowed in recent rounds: the envelope-regularity half of §2.3 is closed
   by the discrete sandwich lemma; the order of the active mistake complexity
   is now settled unconditionally, so §2.9 and hypothesis 12 are largely
   discharged. Only the sum-separation floors remain at severity A among the
   hypothesis-style gaps.)*
1. **§2.3 separation floors** — closes a headline result; construction-only.
2. **§2.8 domination bridges** — highest leverage; converts C1 and C3, and
   makes the Schatten template unconditional.
3. **§2.5 Jensen–Shannon hardness** — well-posed; needs analytic gap
   amplification.
4. **§2.6 quantitative regularity constants** — a Taylor-remainder estimate,
   now that the structural question is settled.
5. **§2.4 penalty necessity** — reduces to known parameter-free lower bounds.
6. **§2.2 multi-alphabet AAK** — new operator theory.
7. **§2.1 symbolic grounding** — hardest; likely needs a theory of approximate
   Boolean realization.

---

## 9. Locator table

Every claim marked *[M]* is checkable at these labels in
`automata_corrected.tex`. All 30 labels were verified to resolve uniquely.

| Topic | Manuscript label |
|---|---|
| Commitment threshold | `thm:commitment-spec` |
| Information-bottleneck identity | `thm:predictive-info` |
| Zero retention at `\|S⁺\|` | `thm:retention-zero` |
| Quadratic spectral converse | `thm:spectral-retention` |
| Mixture-centroid lemma | `lem:mixture-centroid` |
| Unrestricted grounding `= σ_{M+1}` | `thm:spectral-grounding` |
| AAK equality (scalar) | `thm:aak-equality` |
| AAK multi-letter (conditional) | `thm:aak-multiletter` |
| Strictness ⟹ no Hardy symbol | `cor:hankel-strict` |
| Symbolic gap definition | `def:symbolic-grounding-gap` |
| Two-point Bernoulli family does not separate scales | `prop:bernoulli-fisher-scales` |
| Global interior Fisher-chart converse | `thm:global-interior-fisher` |
| Gaussian quadratic NP-completeness | `thm:retention-reset-np` |
| Determinism gap, rate `S(k)` | `thm:exp-gap` |
| Stochasticity floor | `thm:stochasticity` |
| Persistent-stream lower bound | `thm:stream-lower-bound` |
| Binary-input lower bound | `thm:stream-lb-binary` |
| Stream Littlestone dimension | `cor:stream-ldim` |
| Agnostic regret | `thm:agnostic` |
| Active certified bounds (I)/(II)/(III) | `thm:active-certified` |
| Explicit direct-sum family | `thm:active-explicit-directsum` |
| Two-phase direct-sum instance | `thm:active-two-phase` |
| Oracle minimax lower bound | `thm:oracle-minimax-lower` |
| Pinching law | `thm:pinching` |
| Free-lunch characterization | `thm:pos-allM` |
| Boolean zero-error dichotomy | `meta:boolean` |
| Observable support index | `def:observable-support-index` |
| Spectral-tail heuristic | `heur:spectral` |
| Cross-term conjectures | `conj:cross-terms` |
| Open: symbolic grounding | `open:symbolic-grounding` |
| Open: multi-alphabet Hankel | `open:hankel-multiletter` |

---

## 10. Falsifiability criteria

*[A]* What would count as settling each item, stated so that progress is
checkable rather than rhetorical.

| # | Resolved by exhibiting … |
|---|---|
| §2.1 | a closed form, or matching upper/lower bounds, for `Δ_grd(M;γ)`; or a proof that it is not determined by `(H_ν, σ_γ(ν), κ_det)` |
| §2.2 | an intrinsic property of `ν` equivalent to existence of a shift-intertwining embedding; or a compact finite-state Hankel operator with `Δ_grd^Hank,str(M) > σ_{M+1}` |
| §2.3 | for each stochastic regime, a packing of `m` processes with `I(V;Y_{1:T}) ≥ Δ_M` at a horizon `T` of the order where the envelopes cross; separately, a single family forcing the approximation **and** estimation floors on disjoint rounds (§2.29) |
| §2.4 | a learner matching `inf_M[A_T(M)+E_M(T)]` without the penalty; or a lower bound forcing `Ω(√(T log M))` extra for unknown `M` |
| §2.5 | **done** (`thm:full-kl-promise-np`). Remaining: a polynomial decision procedure for inequalities between rationals and sums of `p log(p/q)`, which would upgrade promise-hardness to NP-completeness |
| §2.6 | **done in both charts** — probability coordinates with sharp constant 1 (`prop:kl-simplex-sharp`), natural-parameter chart negatively (`thm:no-global-fisher-converse`). Nothing further to exhibit |
| §2.7 | a two-sided bound `PoS_lin^loc ≤ PoS_quad ≤ f(PoS_lin^loc)`; or a family separating them by an unbounded factor |
| §2.8 | a checkable condition on a task theory implying Schatten-`p` domination, with a nontrivial instance |
| §2.9 | mistake bounds for machines admitting no synchronizing word |
| §2.10 | an example with a strict structured gap, or a proof none exists for finite-state channels |
| §2.11 | a task theory at `α ∉ {0,1,∞}` with rank control and a domination bridge |
| C1, C3 | the corresponding domination bridge — nuclear for C1 (plus `H_ν` trace class), Schatten-2 for C3; each then follows from Mirsky |
| C2 | a worst-case quadratic surrogate, or a geometric condition aligning the worst-case state with the top Fisher eigendirection |
| C4 | see §2.11 |
| §2.27 | **done** (`thm:esyncsi-theta`), and sharpened in §2.34 to the exact value `floor(log2 M)` with no alphabet dependence. Remaining: a family with `L_sync^univ(C_M) = ω(M log M)`, giving a non-degenerate two-term decomposition in the experiment-**length** currency |
| §2.34 | nothing outstanding for the mistake currency; the constant is `1/log 2` and is attained |
| §2.35 | either a family with `Lsyncu(C_M) = omega(M log M)` — necessarily with `|I| >= 2` by `prop:lsyncu-single-input` (§2.36) — or a proof that the per-episode cost and the episode count cannot both be large, giving `O(M log M)` |
| §2.36 | nothing outstanding for unary alphabets; the bound `M-1` is proved and attained |
| §2.37 | a *family* `C_M` with `Lsyncu(C_M) = omega(M log M)`, necessarily `|I| >= 2` and necessarily exploiting the `d(U) <= M-|U|+1` trade-off at many scales at once. **Amended by §2.38**: the upper bound is not known tight beyond `M=4` |
| §2.39 | **first**: is `Lsyncu(M)` finite for `|I| >= 2`? Then a rate. The `Lsync` bounds do not transfer |
| §2.38 | either a proof that `Lsync(M) = O(M)` — which by §2.34 would collapse the length currency and close `open:si-hard-family` negatively — or an exhaustive/structural refutation at some `M >= 6` |
| §2.28 | **done** (`lem:csiszar-representation`, repaired via the non-product conditional identity (†)) |
| §2.29 | **superseded by §2.31**: the sum form already follows from the min form via the sandwich. Remaining: a proof that `kappa = O(1)` in the finite-state regimes, or a both-axes construction removing the `(1+kappa)` factor |
| §2.30 | a polynomial decision procedure for rational-vs-log-sum inequalities (would give NP-completeness); or an explicit numerical value for `eps0` |
| §2.31 | **done** (`lem:kappa-bounded`, §2.33): `kappa <= 2^alpha (1+log2)^beta`, absolute and `T`-independent |
| §2.33 | nothing outstanding; the remaining oracle gaps are horizon-efficient stochastic packings and the necessity of `Psi_M(T)` |
