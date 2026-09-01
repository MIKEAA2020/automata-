#!/usr/bin/env python3
"""Automated structural checks on the LaTeX file."""
import re
from collections import Counter, defaultdict

PATH = "/home/z/my-project/download/automata_unified_revised_v3.tex"

with open(PATH, encoding="utf-8", errors="replace") as f:
    text = f.read()

lines = text.split("\n")
print(f"Total lines: {len(lines)}")
print(f"Total chars: {len(text)}")

# ---------- 1. Labels ----------
labels = []
for i, line in enumerate(lines, 1):
    for m in re.finditer(r"\\label\{([^}]*)\}", line):
        labels.append((m.group(1), i))

label_names = [l for l, _ in labels]
dupes = [l for l, c in Counter(label_names).items() if c > 1]
print(f"\n=== LABELS ===\nTotal labels: {len(labels)}")
print(f"Duplicate labels ({len(dupes)}):")
for d in dupes:
    locs = [i for l, i in labels if l == d]
    print(f"  {d} -> lines {locs}")

# ---------- 2. References ----------
refs = []
for i, line in enumerate(lines, 1):
    for m in re.finditer(r"\\(?:eq)?ref\{([^}]*)\}", line):
        refs.append((m.group(1), i))

undefined = [r for r, _ in refs if r not in set(label_names)]
print(f"\n=== REFERENCES ===\nTotal \\ref/\\eqref: {len(refs)}")
print(f"Undefined references ({len(set(undefined))}):")
for u in sorted(set(undefined)):
    locs = [i for r, i in refs if r == u][:6]
    print(f"  {u} -> referenced at lines {locs}{' ...' if len(locs) == 6 else ''}")

unreferenced = [l for l in label_names if l not in set(r for r, _ in refs)]
print(f"\nLabels never referenced ({len(unreferenced)}):")
for u in unreferenced[:40]:
    print(f"  {u}")

# ---------- 3. Environments ----------
env_open = defaultdict(list)
env_close = defaultdict(list)
stack = []
errors = []
env_re = re.compile(r"\\begin\{(\w+\*?)\}")
env_end_re = re.compile(r"\\end\{(\w+\*?)\}")
for i, line in enumerate(lines, 1):
    for m in env_re.finditer(line):
        stack.append((m.group(1), i))
    for m in env_end_re.finditer(line):
        if stack and stack[-1][0] == m.group(1):
            stack.pop()
        else:
            # try to find matching in stack (mismatched)
            errors.append(f"line {i}: \\end{{{m.group(1)}}} without matching \\begin (stack top: {stack[-1] if stack else 'EMPTY'})")
if stack:
    print(f"\n=== ENVIRONMENTS ===\nUnclosed environments ({len(stack)}):")
    for name, ln in stack[:30]:
        print(f"  {name} opened at line {ln}")
if errors:
    print(f"\nMismatched \\end ({len(errors)}):")
    for e in errors[:30]:
        print(f"  {e}")
else:
    print(f"\n=== ENVIRONMENTS ===\nAll begin/end matched (checking by stack).")

# count environments
env_counts = Counter()
for i, line in enumerate(lines, 1):
    for m in env_re.finditer(line):
        env_counts[m.group(1)] += 1
print("\nEnvironment counts:")
for env, c in env_counts.most_common():
    print(f"  {env}: {c}")

# ---------- 4. Theorem-like environments and numbering ----------
thm_re = re.compile(r"\\begin\{(theorem|lemma|proposition|corollary|definition|remark|example|conjecture|claim|fact|problem|question|notation|assumption)\}\s*(\[[^\]]*\])?\s*")
thms = []
for i, line in enumerate(lines, 1):
    for m in re.finditer(r"\\begin\{(theorem|lemma|proposition|corollary|definition|remark|example|conjecture|claim|fact|problem|question|notation|assumption)\}", line):
        thms.append((m.group(1), i))
print(f"\n=== THEOREM-LIKE ===\nTotal: {len(thms)}")
tc = Counter(t for t, _ in thms)
for t, c in tc.most_common():
    print(f"  {t}: {c}")

# ---------- 5. Basic brace balance ----------
depth = 0
min_depth = 0
issues = []
for i, line in enumerate(lines, 1):
    # skip comment lines
    stripped = line.split("%", 1)[0] if not line.lstrip().startswith("%") else ""
    # crude: ignore braces preceded by backslash
    for ch in stripped:
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth < 0:
                issues.append(f"line {i}: brace underflow")
                depth = 0
    if depth > 20:
        issues.append(f"line {i}: brace depth suspiciously high ({depth})")
print(f"\n=== BRACES ===\nFinal depth: {depth}")
if issues:
    print(f"Issues ({len(issues)}):")
    for iss in issues[:20]:
        print(f"  {iss}")

# ---------- 6. Common typos / patterns ----------
print("\n=== PATTERN CHECKS ===")
patterns = {
    "Double space": r"[a-zA-Z]  [a-zA-Z]",
    "Trailing whitespace": r"[ \t]+$",
    "Repeated word (the the)": r"\b(\w+) \1\b",
    "?! combo": r"\?!",
    "comma comma": r",,",
    "period period": r"\.\.",
    ".. period after display": r"\$\$.*\.\.",
}
for name, pat in patterns.items():
    matches = [(i, line.strip()[:80]) for i, line in enumerate(lines, 1) if re.search(pat, line)]
    if matches and name in ("Repeated word (the the)", "comma comma", "?! combo"):
        print(f"\n{name} ({len(matches)}):")
        for i, l in matches[:15]:
            print(f"  line {i}: {l}")

ws = sum(1 for line in lines if line != line.rstrip())
print(f"\nLines with trailing whitespace: {ws}")

# ---------- 7. Preamble ----------
# print first 80 lines
print("\n=== FIRST 40 LINES ===")
for i, line in enumerate(lines[:40], 1):
    print(f"{i}: {line}")
