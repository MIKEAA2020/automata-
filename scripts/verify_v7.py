#!/usr/bin/env python3
"""verify_v7: 19+ checks — v6 frozen-unchanged, six edits present, structural integrity."""
import re, sys, hashlib, os

V6 = '/home/z/my-project/automata/download/automata_unified_revised_v6.tex'
V7 = '/home/z/my-project/automata/download/automata_unified_revised_v7.tex'
PDF = '/home/z/my-project/scripts/build_v7/automata_unified_revised_v7.pdf'

checks = []
def ck(name, ok):
    checks.append((name, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

v6 = open(V6, errors='replace').read()
v7 = open(V7, errors='replace').read()

print("== freeze and lineage ==")
ck('v6 byte-unchanged (md5 df384d6f...)', hashlib.md5(v6.encode()).hexdigest() == 'df384d6facf47ba36776261adb948850')
ck('v7 exists and is longer than v6', len(v7) > len(v6) and len(v7) - len(v6) < 20000)
ck('v7 line count = 18101', v7.count('\n') + 1 == 18101)

print("== six edits present ==")
ck('E1 PoS footnote (corrected cite 2309.08709 via shang2023)',
   'Price of\nSafety\\footnote{Here and throughout' in v7 and '\\cite{shang2023}' in v7 and '2508.20246' not in v7)
ck('E1 old string absent', 'Price of Safety\nwithout relaxation-error control' not in v7)
ck('E2 grounding-gap footnote', 'gap\\footnote{As used here' in v7 and '\\cite{shaikh2023grounding}' in v7)
ck('E2 old string absent', 'grounding gap, over deterministic Mealy\nmachines, whose resource' not in v7)
ck('E3 seventeen statements', 'Seventeen statements are checked\nin total, across seven modules' in v7)
ck('E3 fifteen absent from rem', 'Fifteen statements are checked in\ntotal' not in v7)
ck('E4 availability updated', 'the Lean~4 development of' in v7 and 'axiom-audit gate that recompiles' in v7)
ck('E4 old manifest wording absent', 'which documents its fifteen\nmachine-checked statements' not in v7)
ck('E5 cap fix', 'The Price of Safety is' in v7 and 'The price of safety is' not in v7)
ck('E6 shang2023 bibitem', '\\bibitem{shang2023}' in v7 and 'arXiv:2309.08709' in v7)
ck('E6 shaikh2023grounding bibitem', '\\bibitem{shaikh2023grounding}' in v7 and 'arXiv:2311.09144' in v7)

print("== structural integrity ==")
labels = re.findall(r'\\label\{([^}]+)\}', v7)
ck('504 labels, 0 duplicates', len(labels) == 504 and len(set(labels)) == 504)
refs = re.findall(r'\\(?:ref|eqref)\{([^}]+)\}', v7)
ck('all refs resolve (0 undefined)', set(refs) <= set(labels))
ck('877 refs total (873 + 4 footnote refs)', len(refs) == 877)
begins = re.findall(r'\\begin\{([a-zA-Z*]+)\}', v7)
ends = re.findall(r'\\end\{([a-zA-Z*]+)\}', v7)
from collections import Counter
ck('environments matched', Counter(begins) == Counter(ends))
ck('brace balance 0', v7.count('{') - v7.count('}') == 0)
cite_keys = [k.strip() for m in re.findall(r'\\cite\{([^}]+)\}', v7) for k in m.split(',')]
ck('new cites used (shang2023, shaikh2023grounding)', 'shang2023' in cite_keys and 'shaikh2023grounding' in cite_keys)
bibitems = re.findall(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}', v7)
ck('39 bibitems, all cited', len(bibitems) == 39 and set(bibitems) == set(cite_keys))
ck('pdf built (1.1 MiB)', os.path.exists(PDF) and os.path.getsize(PDF) > 1000000)
ck('no stray "Fifteen" anywhere', 'Fifteen' not in v7)

fails = [n for n, ok in checks if not ok]
print(f"\n{len(checks) - len(fails)}/{len(checks)} PASS")
if fails:
    print("FAILED:", fails); sys.exit(1)
