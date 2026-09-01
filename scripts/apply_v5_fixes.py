#!/usr/bin/env python3
"""Create v5 from frozen v4 with two precision fixes found by the dedicated
proof check of the remaining 135 theorems:

F1 (prop:grounding-tracking, proof of (iii)): the displayed intermediate
   identity D(phi) = sigma_1 - sum_C max_b W_C(b) is wrong; the correct
   identity is D(phi) = sum_s max_b w_s(b) - sum_C max_b W_C(b), the first
   term being the partition-independent total modal mass 1 - sigma_1.
   The stated result (iii) is correct; only the displayed constant is fixed.

F2 (def:safe-right-cong / prop:pos-quad-consistent): the discrete quadratic
   PoS subsection uses "right congruence" for objects its proofs treat as
   unconstrained partitions; the existence witness in (i) (the safety
   partition itself) is admissible only under the partition reading.  A
   convention paragraph makes the reading explicit and records the
   transition-compatible caveat.

Anchored, abort-before-write, idempotent.
"""
import hashlib, os, shutil, sys, subprocess

V4 = "/home/z/my-project/download/automata_unified_revised_v4.tex"
V5 = "/home/z/my-project/download/automata_unified_revised_v5.tex"

src = open(V4, encoding="utf-8").read()

edits = []

# ------------------------------------------------------------------ F1
old1 = r"""For~(iii), write $w_s(b)=\pi_sP_s(b)$.  The statewise first term
$\sum_s\pi_s(1-\max_bP_s(b))$ in the decomposition is constant across
partitions, whereas the blockwise accuracy is
\[
\sum_{C\in\mathcal P}\max_b\sum_{s\in C}w_s(b),
\]
so that
\[
D(\phi)=\sigma_1-\sum_{C\in\mathcal P_\phi}\max_b\sum_{s\in C}w_s(b)
\]
for the partition $\mathcal P_\phi$ induced by $\phi$, and likewise for
$\psi$."""
new1 = r"""For~(iii), write $w_s(b)=\pi_sP_s(b)$.  The statewise modal term
$\sum_s\pi_s\max_bP_s(b)=\sum_s\max_bw_s(b)=1-\sigma_1$ in the decomposition
is constant across partitions, whereas the blockwise accuracy is
\[
\sum_{C\in\mathcal P}\max_b\sum_{s\in C}w_s(b),
\]
so that
\[
D(\phi)=\sum_{s\in\Splus}\max_b w_s(b)-\sum_{C\in\mathcal P_\phi}\max_b\sum_{s\in C}w_s(b),
\]
the first term being the partition-independent total modal mass $1-\sigma_1$,
for the partition $\mathcal P_\phi$ induced by $\phi$, and likewise for
$\psi$."""
edits.append(("F1 display", old1, new1))

old1b = r"""Applying this to every block of $\mathcal P_\psi$ and summing gives
\[
\sum_{C'\in\mathcal P_\phi}\max_b\sum_{s\in C'}w_s(b)
\ \ge\
\sum_{C\in\mathcal P_\psi}\max_b\sum_{s\in C}w_s(b),
\]
and subtracting from $\sigma_1$ reverses the inequality to $D(\phi)\le D(\psi)$."""
new1b = r"""Applying this to every block of $\mathcal P_\psi$ and summing gives
\[
\sum_{C'\in\mathcal P_\phi}\max_b\sum_{s\in C'}w_s(b)
\ \ge\
\sum_{C\in\mathcal P_\psi}\max_b\sum_{s\in C}w_s(b),
\]
and subtracting from the partition-independent total $\sum_s\max_bw_s(b)$
reverses the inequality to $D(\phi)\le D(\psi)$."""
edits.append(("F1 subtraction", old1b, new1b))

# ------------------------------------------------------------------ F2
old2 = r"""A right congruence $\sim$ on
$\Splus$ is \textbf{safe} if every $\sim$-class is contained in some $B_b$;
equivalently, if $\sim$ refines the safety equivalence
$s\sim_{\mathcal B}s'\iff s,s'$ lie in a common $B_b$.  When no safe right
congruence of index at most $M$ exists we set
$\mathrm{Safe}_{\mathrm{quad}}(M)=-\infty$, so that $\PoSquad(M)=+\infty$.
\end{definition}"""
new2 = r"""A right congruence $\sim$ on
$\Splus$ is \textbf{safe} if every $\sim$-class is contained in some $B_b$;
equivalently, if $\sim$ refines the safety equivalence
$s\sim_{\mathcal B}s'\iff s,s'$ lie in a common $B_b$.  When no safe right
congruence of index at most $M$ exists we set
$\mathrm{Safe}_{\mathrm{quad}}(M)=-\infty$, so that $\PoSquad(M)=+\infty$.

\emph{Convention.}  Throughout this subsection the free and safe optima are
read over \emph{partitions} of $\Splus$: the transition-compatibility
carried by the term ``right congruence'' in the general theory is
deliberately relaxed here, exactly as
Remark~\ref{rem:poslin-measures} reads it, so that the discrete quadratic
problem and the linear surrogate of
Proposition~\ref{prop:pos-relaxation-identity} are posed on comparable
feasible classes.  Under the stricter, transition-compatible reading, the
existence clause of Proposition~\ref{prop:pos-quad-consistent} holds with
the safety partition $\mathcal B$ itself as witness only when $\mathcal B$
is a right congruence; in all cases the singleton partition witnesses
existence for $M\ge|\Splus|$.
\end{definition}"""
edits.append(("F2 convention", old2, new2))

old2b = r"""\emph{(i)} If $M\ge r$, the safety partition $\mathcal B$ itself is safe, each
class being a block, and has index $r\le M$.  Conversely, a safe congruence has
every class inside a single $B_b$, so each of the $r$ positive-mass blocks
contains at least one class, whence the index is at least $r$."""
new2b = r"""\emph{(i)} If $M\ge r$, the safety partition $\mathcal B$ itself is safe, each
class being a block, has index $r\le M$, and is admissible under the
partition convention of Definition~\ref{def:safe-right-cong}.  Conversely,
a safe congruence has every class inside a single $B_b$, so each of the $r$
positive-mass blocks contains at least one class, whence the index is at
least $r$."""
edits.append(("F2 witness", old2b, new2b))

# ------------------------------------------------------------------ apply
for name, old, new in edits:
    n = src.count(old)
    if n != 1:
        print(f"ABORT: anchor for {name!r} matched {n} times (expected 1).")
        sys.exit(1)
for name, old, new in edits:
    src = src.replace(old, new, 1)
    print(f"applied: {name}")

if os.path.exists(V5):
    os.remove(V5)
open(V5, "w", encoding="utf-8").write(src)

# freeze v4
md5_v4 = hashlib.md5(open(V4, "rb").read()).hexdigest()
os.chmod(V4, 0o444)
print(f"v4 frozen: md5 {md5_v4}")
print(f"v5 written: {V5} ({len(src.splitlines())} lines)")

# post-checks
checks = [
    (r"D(\phi)=\sum_{s\in\Splus}\max_b w_s(b)", 1),
    (r"partition-independent total modal mass $1-\sigma_1$", 1),
    (r"subtracting from the partition-independent total $\sum_s\max_bw_s(b)$", 1),
    (r"\emph{Convention.}  Throughout this subsection the free and safe optima", 1),
    (r"admissible under the" + "\n" + r"partition convention of Definition", 0),  # multiline variant below
    (r"partition convention of Definition~\ref{def:safe-right-cong}", 1),
    (r"D(\phi)=\sigma_1-\sum_{C\in\mathcal P_\phi}", 0),
]
v5src = open(V5, encoding="utf-8").read()
ok = True
for pat, want in checks:
    got = v5src.count(pat)
    status = "PASS" if got == want else "FAIL"
    if got != want: ok = False
    print(f"[{status}] {pat[:60]!r}: {got} (want {want})")
print("V5 EDITS:", "ALL OK" if ok else "PROBLEM")
