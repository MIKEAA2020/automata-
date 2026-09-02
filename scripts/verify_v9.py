#!/usr/bin/env python3
r"""Structural verification of v9 against frozen v8.

Checks:
 1. v8 byte-unchanged (md5 39c1b519...) and still frozen (444).
 2. E1 present: five unifilar environments now in S3, ordered
    ex:onestep-not-congruence < block < \subsection{Full-KL Retention Gap};
    block gone from S9 (seam = rem:rd-nonconvex-mechanism -> def:approx-deficit);
    model precedes the theory (subsec:unifilar-retention).
 3. E2 present: retention-gap disambiguation footnote at the Introduction
    anchor, citing sudo2026; old plain wording absent.
 4. E3 present: bibitem sudo2026, well-formed, before \end{thebibliography};
    Notation Index still after the bibliography; bibitem/cite integrity
    both directions.
 5. Label/ref integrity: no duplicates, no undefined; counts 509 labels.
 6. Environment pairing for theorem-like envs; count equals v8 (no renumber).
 7. Brace balance.
 8. PDF: page count, footnote and bibitem render (pdftotext).
"""
import re, sys, hashlib, os, subprocess

V8 = '/home/z/my-project/automata/download/automata_unified_revised_v8.tex'
V9 = '/home/z/my-project/automata/download/automata_unified_revised_v9.tex'
V8_MD5 = '39c1b519e626841235be0fe5676020ca'
PDF = '/home/z/my-project/automata/scripts/build_v9/automata_unified_revised_v9.pdf'

t8 = open(V8, errors='replace').read()
t9 = open(V9, errors='replace').read()

checks = []
def ck(name, cond):
    checks.append((name, bool(cond)))
    print(('PASS' if cond else 'FAIL') + f'  {name}')

# 1. v8 integrity
ck('v8 md5 unchanged', hashlib.md5(open(V8,'rb').read()).hexdigest() == V8_MD5)
ck('v8 still frozen (no write perms)', not (os.stat(V8).st_mode & 0o222))

# 2. E1: block relocation
lab_pos = lambda lab: t9.find('\\label{%s}' % lab)
ex_i, sub_i = lab_pos('ex:onestep-not-congruence'), t9.find('\\subsection{Full-KL Retention Gap}')
blk_labels = ['rem:unifilar-feasibility', 'prop:unifilar-lumpability',
              'rem:unifilar-converse-hypothesis', 'prop:input-driven-specialization',
              'rem:epsilon-machine-relation']
ck('E1 all five labels present exactly once',
   all(t9.count('\\label{%s}' % l) == 1 for l in blk_labels))
ck('E1 block between example and Full-KL subsection in S3',
   ex_i != -1 and sub_i != -1 and all(ex_i < lab_pos(l) < sub_i for l in blk_labels))
ck('E1 block start marker occurs exactly once',
   t9.count('\\begin{remark}[Necessity of the Feasibility Restriction]') == 1)
ck('E1 S9 seam: rd-nonconvex remark now precedes def:approx-deficit',
   '\\end{remark}\n\n\\begin{definition}[Finite-Horizon Approximation Deficit]' in t9)
ck('E1 model now precedes the unifilar retention theory',
   lab_pos('rem:epsilon-machine-relation') < t9.find('\\label{subsec:unifilar-retention}'))
ck('E1 unified machine-model run: def:unifilar-machine ... rem:epsilon-machine '
   'all before Full-KL subsection',
   all(lab_pos(l) < sub_i for l in ['def:unifilar-machine', 'rem:unifilar-proper-subclass',
       'def:unifilar-lumpable', 'rem:unifilar-support-not-automatic'] + blk_labels))

# 3. E2: footnote
ck('E2 footnote inserted at Introduction anchor',
   'The full-KL retention gap\\footnote{Here and throughout' in t9)
ck('E2 footnote cites sudo2026', '\\cite{sudo2026}.}' in t9)
ck('E2 old plain wording absent',
   'through a stationary lumpable quotient.\n\nThe full-KL retention gap is\n\\[' not in t9)
ck('E2 footnote refs resolvable targets exist',
   all(('\\label{%s}' % l) in t9 for l in
       ['def:full-kl-retention', 'def:controlled-full-kl', 'def:gaussian-quadratic']))

# 4. E3: bibitem
ck('E3 bibitem sudo2026 present',
   '\\bibitem{sudo2026}\nA.~Sudo,\n``Thermodynamics of learning: a typed '
   'four-component accounting of\nmemory, fit, and value,\'\'\narXiv:2608.12791 '
   '[cond-mat.stat-mech], 2026.' in t9)
bib_items = re.findall(r'\\bibitem\{([^}]+)\}', t9)
ck('E3 bibliography grew 39 -> 40, all unique', len(bib_items) == 40 and len(set(bib_items)) == 40)
cited = set(re.findall(r'\\cite\{([^}]+)\}', t9))
cited = {c for group in cited for c in group.split(',')}
ck('E3 every bibitem cited (incl. sudo2026 exactly once)',
   cited == set(bib_items) and t9.count('\\cite{sudo2026}') == 1)
ck('E3 notation index still after bibliography',
   t9.find('\\end{thebibliography}') < t9.find('\\section*{Notation Index}'))

# 5. label/ref integrity
labels = re.findall(r'\\label\{([^}]+)\}', t9)
ck('509 labels, no duplicates', len(labels) == 509 and len(set(labels)) == 509)
refs = set()
for group in re.findall(r'\\(?:ref|eqref)\{([^}]+)\}', t9):
    refs.update(group.split(','))
ck('no undefined refs (all %d resolve)' % len(refs), refs <= set(labels))

# 6. environment pairing + count parity with v8
ENVS = ['theorem','lemma','proposition','corollary','definition','remark',
        'example','proof','table','figure']
def counts(t):
    out = {}
    for e in ENVS:
        out[e] = (len(re.findall(r'\\begin\{%s\}' % e, t)),
                  len(re.findall(r'\\end\{%s\}' % e, t)))
    return out
c8, c9 = counts(t8), counts(t9)
ck('env begin/end paired in v9', all(b == e for b, e in c9.values()))
ck('theorem-like env count identical to v8 (no renumbering)',
   all(c8[e] == c9[e] for e in ENVS))

# 7. brace balance
body = re.sub(r'(?m)%.*$', '', t9)
ck('brace balance zero', body.count('{') - body.count('}') == 0)

# 8. PDF checks
if os.path.exists(PDF):
    txt = subprocess.run(['pdftotext', PDF, '-'], capture_output=True,
                         text=True).stdout
    ck('PDF: disambiguation footnote renders',
       'thermodynamics-of-learning' in txt and 'Sudo' in txt)
    ck('PDF: moved remark renders in early pages',
       'Necessity of the Feasibility Restriction' in txt)
    pages = txt.count('\x0c')
    print(f'       (PDF pages: ~{pages})')
else:
    ck('PDF exists', False)

bad = [n for n, ok in checks if not ok]
print('\n%d/%d PASS' % (len(checks) - len(bad), len(checks)))
sys.exit(1 if bad else 0)
