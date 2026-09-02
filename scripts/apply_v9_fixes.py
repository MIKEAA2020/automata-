#!/usr/bin/env python3
r"""v9 edits on automata_unified_revised_v9.tex (v8 frozen, byte-identical base).

E1 (Q13a): relocate the five-environment unifilar machine-model block
     (rem:unifilar-feasibility, prop:unifilar-lumpability,
      rem:unifilar-converse-hypothesis, prop:input-driven-specialization,
      rem:epsilon-machine-relation)
     from S9 'Type-Correct Axes on One Clock' (after rem:rd-nonconvex-mechanism)
     to S3 'Stationary Controlled Causal Machines', immediately after
     ex:onestep-not-congruence and before \subsection{Full-KL Retention Gap}.
E2 (arXiv 2608.12791): disambiguation footnote at the first body occurrence of
     'retention gap' (Introduction, 'The full-KL retention gap is ...').
E3: bibitem sudo2026 = arXiv:2608.12791 [cond-mat.stat-mech] 2026.

All edits anchored; abort before write if any anchor is not unique/present.
"""
import io, sys, re

SRC = '/home/z/my-project/automata/download/automata_unified_revised_v9.tex'
s = io.open(SRC, encoding='utf-8', newline='').read().replace('\r\n', '\n')
orig = s

def die(msg):
    sys.exit('ABORT (no write): ' + msg)

def must_count(anchor, n=1, what='anchor'):
    c = s.count(anchor)
    if c != n:
        die('%s count = %d, expected %d: %r' % (what, c, n, anchor[:80]))
    return s.find(anchor)

# ---------------------------------------------------------------- E1: move
BLOCK_START = '\\begin{remark}[Necessity of the Feasibility Restriction]'
must_count(BLOCK_START, 1, 'block start')
start = s.find(BLOCK_START)
if s[start-2:start] != '\n\n':
    die('block start not preceded by blank line')

EPS = '\\label{rem:epsilon-machine-relation}'
must_count(EPS, 1, 'epsilon-machine label')
eps_i = s.find(EPS)
if not (start < eps_i < start + 12000):
    die('epsilon-machine label not inside block range')
endm = s.find('\\end{remark}', eps_i)
if endm == -1 or endm > start + 14000:
    die('block end not found in range')
block_end = endm + len('\\end{remark}')
block = s[start:block_end]

# sanity: the five labels live inside the block
for lab in ['rem:unifilar-feasibility', 'prop:unifilar-lumpability',
            'rem:unifilar-converse-hypothesis', 'prop:input-driven-specialization',
            'rem:epsilon-machine-relation']:
    if ('\\label{%s}' % lab) not in block:
        die('label %s not inside extracted block' % lab)
    if s.count('\\label{%s}' % lab) != 1:
        die('label %s not unique in file' % lab)

# insertion point: end of ex:onestep-not-congruence
EXL = '\\label{ex:onestep-not-congruence}'
must_count(EXL, 1, 'example label')
exl_i = s.find(EXL)
ex_end = s.find('\\end{example}', exl_i)
if ex_end == -1:
    die('example end not found')
insert_at = ex_end + len('\\end{example}')
if not (insert_at < start):
    die('insertion point not before block (ordering guard)')

# perform: cut (with one preceding blank line), then insert
cut_from = start - 2
s2 = s[:cut_from] + s[block_end:]
# recompute insertion index in s2 (text before it is unchanged)
insert_at2 = s2.find('\\end{example}', s2.find(EXL)) + len('\\end{example}')
s2 = s2[:insert_at2] + '\n\n' + block + s2[insert_at2:]
s = s2

# guard: block now sits between the example and the Full-KL subsection
k_ex = s.find('\\label{ex:onestep-not-congruence}')
k_block = s.find(BLOCK_START)
k_sub = s.find('\\subsection{Full-KL Retention Gap}')
if not (k_ex < k_block < k_sub):
    die('block not positioned between example and Full-KL subsection')
# guard: §9 seam is now remark -> definition directly
if '\\end{remark}\n\n\\begin{definition}[Finite-Horizon Approximation Deficit]' not in s:
    die('S9 seam after block removal not as expected')

# ---------------------------------------------------------------- E2: footnote
FOOT = (
    '\\footnote{Here and throughout, ``retention gap\'\' is this manuscript\'s '
    'state-compression cost --- the stationary Kullback--Leibler price of '
    'lumping predictive states into at most $M$ blocks --- instantiated as '
    'the $\\RetKL(M)$ of Definition~\\ref{def:full-kl-retention}, its '
    'controlled relative $\\RetKLc$ of Definition~\\ref{def:controlled-full-kl}, '
    'and the quadratic surrogate $\\RetQuad$ of '
    'Definition~\\ref{def:gaussian-quadratic}.  It is unrelated to the same '
    'phrase in the thermodynamics-of-learning literature, where a retention '
    'gap is a value-side quantity $L_{\\mathrm{gen}}$ for finite-state '
    'learning devices under task-distribution shift \\cite{sudo2026}.}'
)
ANCH2 = 'through a stationary lumpable quotient.\n\nThe full-KL retention gap is\n\\['
must_count(ANCH2, 1, 'footnote anchor')
s = s.replace(ANCH2,
    'through a stationary lumpable quotient.\n\nThe full-KL retention gap' +
    FOOT + ' is\n\\[')

# ---------------------------------------------------------------- E3: bibitem
ANCH3 = ('``Grounding gaps in language model generations,\'\'\n'
         'arXiv:2311.09144 [cs.CL], 2023.\n\n\\end{thebibliography}')
must_count(ANCH3, 1, 'bibitem anchor')
NEWBIB = ('``Grounding gaps in language model generations,\'\'\n'
          'arXiv:2311.09144 [cs.CL], 2023.\n\n'
          '\\bibitem{sudo2026}\n'
          'A.~Sudo,\n'
          '``Thermodynamics of learning: a typed four-component accounting of\n'
          'memory, fit, and value,\'\'\n'
          'arXiv:2608.12791 [cond-mat.stat-mech], 2026.\n\n'
          '\\end{thebibliography}')
s = s.replace(ANCH3, NEWBIB)

# ---------------------------------------------------------------- write
if s == orig:
    die('no changes produced')
io.open(SRC, 'w', encoding='utf-8', newline='\n').write(s)
print('v9 written: %d chars (was %d)' % (len(s), len(orig)))
print('E1: block (%d chars, 5 environments) moved S9 -> S3' % len(block))
print('E2: retention-gap footnote inserted at first body occurrence')
print('E3: bibitem sudo2026 added (arXiv:2608.12791)')
