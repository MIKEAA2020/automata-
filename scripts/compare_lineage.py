#!/usr/bin/env python3
"""Structural comparison: automata_corrected.tex (superseded) vs automata_unified_revised_v6.tex (current).

Extracts: sections, subsections, labels with environment types, tables, bibitems.
Goal: find content in corrected that is absent from v6 (restoration candidates),
and check which OPEN_QUESTIONS items still apply to v6.
"""
import re, sys, json
from collections import OrderedDict

def parse(path):
    env_re = re.compile(r'\\begin\{(theorem|lemma|proposition|corollary|definition|remark|example|metatheorem|conjecture|openproblem|question|table|figure)\}\s*(?:\[([^\]]*)\])?')
    label_re = re.compile(r'\\label\{([^}]+)\}')
    sec_re = re.compile(r'\\section\{([^}]+)\}')
    subsec_re = re.compile(r'\\subsection\{([^}]+)\}')
    bib_re = re.compile(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}')
    tab_env_re = re.compile(r'\\begin\{table\}')
    d = {'labels': OrderedDict(), 'sections': [], 'subsections': [], 'bibs': [], 'tables': 0, 'lines': 0}
    cur_env = None
    with open(path, errors='replace') as f:
        lines = f.readlines()
    d['lines'] = len(lines)
    for i, line in enumerate(lines, 1):
        for m in sec_re.finditer(line):
            d['sections'].append((i, m.group(1)))
        for m in subsec_re.finditer(line):
            d['subsections'].append((i, m.group(1)))
        m = env_re.search(line)
        if m:
            cur_env = (m.group(1), m.group(2))
        for m in label_re.finditer(line):
            kind = cur_env[0] if cur_env else 'other'
            title = (cur_env[1] or '').strip() if cur_env else ''
            d['labels'][m.group(1)] = {'line': i, 'env': kind, 'title': title}
        for m in bib_re.finditer(line):
            d['bibs'].append(m.group(1))
        if tab_env_re.search(line):
            d['tables'] += 1
    return d

CORR = '/home/z/my-project/automata/shorter vsuperseded/automata_corrected.tex'
V6 = '/home/z/my-project/automata/download/automata_unified_revised_v6.tex'
c = parse(CORR)
v = parse(V6)

print(f"corrected.tex : {c['lines']} lines, {len(c['labels'])} labels, {len(c['sections'])} sections, {c['tables']} tables, {len(c['bibs'])} bibitems")
print(f"v6.tex        : {v['lines']} lines, {len(v['labels'])} labels, {len(v['sections'])} sections, {v['tables']} tables, {len(v['bibs'])} bibitems")

cl = set(c['labels']); vl = set(v['labels'])
only_c = sorted(cl - vl)
only_v = sorted(vl - cl)
print(f"\nlabels only in corrected ({len(only_c)}):")
for k in only_c:
    e = c['labels'][k]
    print(f"  L{e['line']:>6} {e['env']:<12} {k:<45} {e['title'][:60]}")
print(f"\nlabels only in v6 ({len(only_v)}) — first 40:")
for k in only_v[:40]:
    e = v['labels'][k]
    print(f"  L{e['line']:>6} {e['env']:<12} {k:<45} {e['title'][:60]}")

# table labels
print("\n=== table labels in corrected ===")
for k, e in c['labels'].items():
    if e['env'] == 'table' or k.startswith('tab:'):
        print(f"  L{e['line']:>6} {k:<40} {e['title'][:60]}")
print("=== table labels in v6 ===")
for k, e in v['labels'].items():
    if e['env'] == 'table' or k.startswith('tab:'):
        print(f"  L{e['line']:>6} {k:<40} {e['title'][:60]}")

# check OPEN_QUESTIONS items against v6
print("\n=== OPEN_QUESTIONS checks against v6 ===")
checks = [
    ("Q2 tab:proven-open-1", 'tab:proven-open-1' in vl),
    ("Q2 tab:proven-open-2", 'tab:proven-open-2' in vl),
    ("Q2 tab:schatten-template", 'tab:schatten-template' in vl),
    ("Q2 tab:oracle-budget-laws", 'tab:oracle-budget-laws' in vl),
    ("Q2 tab:spectral-tail", 'tab:spectral-tail' in vl),
    ("Q2 tab:exponent-vertex-correspondence", 'tab:exponent-vertex-correspondence' in vl),
    ("Q3 lem:fisher-uniform-expansion", 'lem:fisher-uniform-expansion' in vl),
    ("Q3 cor:fisher-uniform-remainder", 'cor:fisher-uniform-remainder' in vl),
    ("Q7 prop:active-length-upper", 'prop:active-length-upper' in vl),
    ("Q9 thm:stream-lower-bound", 'thm:stream-lower-bound' in vl),
    ("Q1 rem:no-lower-constraint", 'rem:no-lower-constraint' in vl),
    ("Q13 def:unifilar-machine", 'def:unifilar-machine' in vl),
    ("Q13 def:unifilar-lumpable", 'def:unifilar-lumpable' in vl),
    ("Q13 prop:unifilar-lumpability", 'prop:unifilar-lumpability' in vl),
    ("Q13 subsec unifilar-retention", any('unifilar' in s.lower() for _, s in v['subsections'])),
]
for name, ok in checks:
    print(f"  {'[PRESENT]' if ok else '[ABSENT ]'} {name}")

# positions of key blocks in v6 for Q13
for k in ['def:unifilar-machine', 'def:unifilar-lumpable', 'prop:unifilar-lumpability', 'thm:controlled-ib', 'thm:controlled-zero']:
    if k in v['labels']:
        print(f"  v6 position of {k}: line {v['labels'][k]['line']}")
    if k in c['labels']:
        print(f"  corrected position of {k}: line {c['labels'][k]['line']}")

json.dump({'corr_labels': {k: e for k, e in c['labels'].items()},
           'v6_labels': {k: e for k, e in v['labels'].items()}},
          open('/home/z/my-project/scripts/lineage_cmp.json', 'w'), indent=1)
print("\nsaved /home/z/my-project/scripts/lineage_cmp.json")
