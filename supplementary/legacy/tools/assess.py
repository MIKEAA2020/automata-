#!/usr/bin/env python3
"""
assess.py -- triage a candidate manuscript version against the current base.

Usage:
    python3 tools/assess.py <candidate.txt|.tex> [--base automata_corrected.tex]

Answers, in order:
  1. Is it an ancestor, a descendant, or a parallel branch?
  2. What does it uniquely contain (and of what kind)?
  3. Does it conflict with the base on any SHARED formal statement?
  4. Does it still satisfy the 8 audit items?
  5. Does it compile, and what are its own defects?
  6. Which unique items are dependency-safe to lift?
"""
import re, sys, os, subprocess, tempfile, shutil
from collections import Counter

ENVS = r'theorem|corollary|lemma|proposition|definition|metatheorem|assumption|heuristic|conjecture|openproblem'

def load(path):
    raw = open(path, encoding='utf-8', errors='replace').read().replace('\r\n', '\n')
    return re.sub(r'(?<!\\)%.*', '', raw)          # strip comments

def labels(t):
    return set(re.findall(r'\\label\{([^}]*)\}', t))

def statements(t):
    """label -> normalized body. Falls back to the bracketed title when a
    file uses no \\label commands (some rewrites don't)."""
    d = {}
    for m in re.finditer(r'\\begin\{(' + ENVS + r')\}(\[[^\]]*\])?\s*\\label\{([^}]*)\}(.*?)\\end\{\1\}', t, re.S):
        d[m.group(3)] = ' '.join(m.group(4).split())
    return d

def statements_by_title(t):
    """title (lowercased) -> (env, body). Works even with no labels."""
    d = {}
    for m in re.finditer(r'\\begin\{(' + ENVS + r')\}\[([^\]]*)\](.*?)\\end\{\1\}', t, re.S):
        title = re.sub(r'[^a-z0-9]', '', m.group(2).lower())
        body = re.sub(r'^\s*\\label\{[^}]*\}', '', m.group(3))
        d[title] = (m.group(1), ' '.join(body.split()))
    return d

def canon(x):
    """Collapse pure-notation differences so only real content diffs survive."""
    x = re.sub(r'\\norm\{([^}]*)\}', r'\1', x)
    x = re.sub(r'\\left|\\right|\\!|\\,|\\;|\\ |\\medskip|\\smallskip|\\noindent|\\displaystyle', '', x)
    x = re.sub(r'\\lVert|\\rVert|\\Vert|\\\|', '||', x)
    x = re.sub(r'\\operatorname\{([^}]*)\}', r'\1', x)
    x = re.sub(r'\\mathrm\{([^}]*)\}', r'\1', x)
    x = re.sub(r'\\Sp\{?\\?infty\}?', 'Sinf', x)
    return re.sub(r'[^a-z0-9|]', '', x.lower())

def paras(t):
    return [' '.join(p.split()) for p in re.split(r'\n\s*\n', t)
            if len(' '.join(p.split())) > 60]

def nrm(x):
    return re.sub(r'[^a-z0-9]', '', x.lower())

# ---------------- audit items ----------------
def audit(t, name):
    checks = [
        ("1 no dup Specialized/Meta sections",
         t.count('\\section{Specialized Task Theories}') <= 1 and
         t.count('\\section{Structural Meta-Theorems}') <= 1),
        ("1 no duplicate labels",
         not [l for l, c in Counter(re.findall(r'\\label\{([^}]*)\}', t)).items() if c > 1]),
        ("2 oracle minimax lower-bound recorded",
         'Matching minimax lower bound' in t),
        ("3 zero-retention uses |Splus|",
         '\\Splus' in t and 'M\\ge|\\mathcal S|' not in t.replace(' ', '')),
        ("4 no stale unconditional d_sync mistake bound",
         '\\tilde d_{\\mathrm{sync}}' not in t),
        ("5 self-loop vacuous NP thm removed",
         'thm:retention-vacuous' not in t),
        ("6 grounding unres/structured split",
         '\\Dunres' in t and '\\DHankstr' in t),
        ("7 faithfulness axiom in Clause I",
         'textbf{Faithfulness.}' in t),
        ("8 no stripped-backslash macro damage",
         not re.search(r'(?<![\\\w])(ewcommand|ewtheorem)', t)),
    ]
    print(f"\n--- audit compliance: {name} ---")
    for label, ok in checks:
        print(f"  {'PASS' if ok else 'FAIL'}  {label}")
    return checks

# ---------------- own defects ----------------
def defects(path, t):
    print("\n--- candidate's own known defect classes ---")
    d = {
        "missing xcolor (blue!55!black needs it)":
            ('blue!55!black' in t and '\\usepackage{xcolor}' not in t),
        "\\RetKLr double-superscript bug":
            ('\\newcommand{\\RetKLr}[1]{\\RetKL^{(#1)}}' in t),
        "\\Com_{...} double-subscript bug":
            bool(re.search(r'\\Com_\{', t)),
        "truncated (no \\end{document})":
            ('\\end{document}' not in t),
    }
    for k, v in d.items():
        print(f"  {'YES ' if v else 'no  '} {k}")
    return d

def compile_check(path):
    if not shutil.which('pdflatex'):
        print("\n  (pdflatex unavailable; skipping compile)")
        return
    tmp = tempfile.mkdtemp()
    tex = os.path.join(tmp, 'c.tex')
    src = open(path, encoding='utf-8', errors='replace').read()
    open(tex, 'w', encoding='utf-8').write(src)
    for _ in range(2):
        subprocess.run(['pdflatex', '-interaction=nonstopmode', 'c.tex'],
                       cwd=tmp, capture_output=True, timeout=600)
    log = os.path.join(tmp, 'c.log')
    if os.path.exists(log):
        L = open(log, encoding='utf-8', errors='replace').read()
        errs = re.findall(r'^!.*', L, re.M)
        pages = re.search(r'Output written.*?\((\d+) pages', L)
        print(f"\n--- compile: {len(errs)} errors, "
              f"{pages.group(1)+' pages' if pages else 'NO PDF'} ---")
        for e in errs[:6]:
            print("   ", e.strip())
        if len(errs) > 6:
            print(f"    ... +{len(errs)-6} more")
    shutil.rmtree(tmp, ignore_errors=True)

# ---------------- main ----------------
def main():
    cand = sys.argv[1]
    base = 'automata_corrected.tex'
    if '--base' in sys.argv:
        base = sys.argv[sys.argv.index('--base') + 1]

    C, B = load(cand), load(base)
    name = os.path.basename(cand)
    print("=" * 74)
    print(f"ASSESSING: {name}")
    print(f"BASE     : {base}")
    print("=" * 74)

    LC, LB = labels(C), labels(B)
    pc, pb = paras(C), paras(B)
    nb, nc = nrm(B), nrm(C)
    only_c = [p for p in pc if nrm(p) not in nb]
    only_b = [p for p in pb if nrm(p) not in nc]

    print(f"\n--- relationship ---")
    print(f"  labels: candidate={len(LC)}  base={len(LB)}  shared={len(LC & LB)}")
    print(f"  unique to candidate: {len(LC - LB)}   unique to base: {len(LB - LC)}")
    print(f"  paragraphs only in candidate: {len(only_c)}")
    print(f"  paragraphs only in base     : {len(only_b)}")
    truncated = '\\end{document}' not in C
    uc, ub = len(LC - LB), len(LB - LC)
    # ratio of unique *formal* content, ignoring prose reflow
    SCk, SBk = set(statements(C)), set(statements(B))
    uniq_stmts = len(SCk - SBk)
    if truncated:
        verdict = ("TRUNCATED DRAFT -- incomplete file; treat as ancestor unless "
                   "its unique items prove otherwise")
    elif uc == 0:
        verdict = "SUBSET / ANCESTOR -- nothing unique; nothing to restore"
    elif ub == 0:
        verdict = "SUPERSET / DESCENDANT -- candidate may be the better base"
    elif uniq_stmts <= 3 and uc <= 6:
        verdict = ("LIKELY ANCESTOR -- few unique items; check whether they are "
                   "superseded rather than lost")
    else:
        verdict = ("PARALLEL BRANCH -- substantive content flows both ways; "
                   "selective merge required")
    print(f"  >>> {verdict}")
    print(f"  (unique formal statements in candidate: {uniq_stmts}"
          f"{', FILE IS TRUNCATED' if truncated else ''})")

    if LC - LB:
        print(f"\n--- unique labels by kind ---")
        for k, v in sorted(Counter(l.split(':')[0] for l in (LC - LB)).items()):
            print(f"  {k:12} {v}")

    # conflicts on shared statements -- by label, then by title
    SC, SB = statements(C), statements(B)
    if not SC or not SB:
        TC, TB = statements_by_title(C), statements_by_title(B)
        SC = {k: v[1] for k, v in TC.items()}
        SB = {k: v[1] for k, v in TB.items()}
        print("\n  [no labels in one file -> matching formal statements by TITLE]")
        onlyC = sorted(set(TC) - set(TB))
        if onlyC:
            print(f"  titles only in candidate ({len(onlyC)}):")
            for t_ in onlyC:
                print(f"     + [{TC[t_][0]}] {t_}")
    shared = set(SC) & set(SB)
    diff = [k for k in shared if canon(SC[k]) != canon(SB[k])]
    print(f"\n--- shared formal statements: {len(shared)}; "
          f"differing after canonicalization: {len(diff)} ---")
    for k in sorted(diff)[:40]:
        print(f"  ~ {k}")
    if len(diff) > 40:
        print(f"  ... +{len(diff)-40} more")

    # dependency safety of unique formal items
    print(f"\n--- dependency-safe unique formal items (liftable as-is) ---")
    safe, unsafe = [], []
    for lab in sorted(set(SC) - set(SB)):
        m = re.search(r'\\begin\{(' + ENVS + r')\}(\[[^\]]*\])?\s*\\label\{'
                      + re.escape(lab) + r'\}(.*?)\\end\{\1\}', C, re.S)
        body = m.group(0) if m else ''
        missing = set(re.findall(r'\\ref\{([^}]*)\}', body)) - LB - LC
        dangling = set(re.findall(r'\\ref\{([^}]*)\}', body)) - LB
        (safe if not dangling else unsafe).append((lab, sorted(dangling)))
    for lab, _ in safe:
        print(f"  SAFE   {lab}")
    for lab, d in unsafe:
        print(f"  NEEDS  {lab}  -> refs not in base: {d}")

    audit(C, name)
    defects(cand, C)
    compile_check(cand)
    print("\nDone.\n")

if __name__ == '__main__':
    main()
