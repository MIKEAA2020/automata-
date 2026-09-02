#!/usr/bin/env python3
"""Sentence-level flaw scan v2 — proper math removal + macro unwrapping.

Produces adjudication-ready findings only:
  dup-word      : repeated English words (incl. across line breaks)
  punct         : double punctuation, space before comma/period (text mode)
  spell         : misspellings (word-boundary matched)
  sent-case     : lowercase sentence start (after unwrapping macros, refs→token)
  cap-coinage   : lowercase 'price of safety' in running text (convention: caps)
  hyphen        : right congruence adjectival/noun hyphenation misuse
  math-balance  : odd $ count per paragraph
  ref/cite      : undefined refs, missing bibitem targets, uncited bibitems
"""
import re
from collections import defaultdict, Counter

PATH = '/home/z/my-project/automata/download/automata_unified_revised_v6.tex'
raw = open(PATH, errors='replace').read()
lines = raw.split('\n')

def strip_comments(line):
    out, escaped = [], False
    for ch in line:
        if ch == '\\' and not escaped:
            escaped = True; out.append(ch); continue
        if ch == '%' and not escaped:
            break
        out.append(ch)
        escaped = False
    return ''.join(out)

# ---------------- paragraph assembly
paras, cur, start_line = [], [], 0
for ln, line in enumerate(lines, 1):
    if not line.strip():
        if cur: paras.append((start_line, ' \n '.join(cur)))
        cur, start_line = [], 0
    else:
        if not cur: start_line = ln
        cur.append(strip_comments(line))
if cur: paras.append((start_line, ' \n '.join(cur)))

MATHTOK = ' QMATQ '
def to_prose(text):
    """Remove math entirely (incl. content); unwrap formatting macros; refs→ Ref."""
    # display math
    text = re.sub(r'\\\[.*?\\\]', ' QDISPQ ', text, flags=re.S)
    text = re.sub(r'\\\(.*?\\\)', ' QDISPQ ', text, flags=re.S)
    # protect \$
    text = text.replace(r'\$', ' DOLLAR ')
    # inline math: remove $...$ INCLUDING content
    while '$' in text:
        i = text.find('$')
        j = text.find('$', i + 1)
        if j < 0: break
        text = text[:i] + MATHTOK + text[j+1:]
    # math environments inside paragraphs (tabular, align...)
    text = re.sub(r'\\begin\{(tabular|align|aligned|cases|array|matrix|pmatrix|bmatrix|vmatrix|smallmatrix|substack|split|gathered|gather)\*?\}.*?\\end\{\1\*?\}', ' QDISPQ ', text, flags=re.S)
    # unwrap formatting macros keeping content
    for _ in range(3):
        text = re.sub(r'\\(?:emph|textbf|textit|textsc|texttt|text|mathrm|mathbf|mathit|textrm|textsl)\{([^{}]*)\}', r' \1 ', text)
    # structural macros: drop entirely (incl. args)
    text = re.sub(r'\\(?:label|index|footnote|caption)\{[^{}]*\}', ' ', text)
    text = re.sub(r'\\(?:item|par|noindent|newline|\\)\b', ' ', text)
    text = re.sub(r'\\begin\{(?:enumerate|itemize|description)\}(?:\[[^\]]*\])?', ' STARTITEM ', text)
    text = re.sub(r'\\end\{(?:enumerate|itemize|description)\}', ' ', text)
    text = re.sub(r'\\(?:begin|end)\{[a-zA-Z*]+\}', ' ', text)
    # refs/cites -> capitalized token so sentence-case logic sees them
    text = re.sub(r'\\(?:ref|eqref|autoref|pageref)\{[^{}]*\}', ' REF ', text)
    text = re.sub(r'\\(?:cite|citep|citet|citealp)\{[^{}]*\}', ' REF ', text)
    # remaining simple macros -> drop
    text = re.sub(r'\\[a-zA-Z]+\*?', ' ', text)
    # braces
    text = re.sub(r'[{}]', ' ', text)
    # nonbreaking tilde -> space
    text = text.replace('~', ' ')
    text = text.replace(' DOLLAR ', ' dollar ')
    return re.sub(r'[ \t]+', ' ', text)

findings = []
def add(cat, ln, msg): findings.append((cat, ln, msg))

# ---------------- 1. duplicate words (prose only)
ENGLISH_STOP = {'that','had','very','now','so','also','more','most'}
for pstart, ptext in paras:
    prose = to_prose(ptext)
    for m in re.finditer(r'\b([A-Za-z]{3,})\s+\1\b', prose):
        w = m.group(1).lower()
        if w in ENGLISH_STOP:  # 'that that', 'had had' rare but grammatical
            continue
        before = ptext[:m.start()].count('\n')
        add('dup-word', pstart + before, f'"{m.group(1)} {m.group(1)}" :: context: {prose[max(0,m.start()-50):m.end()+30]!r}')

# ---------------- 2. punctuation (prose only)
for pstart, ptext in paras:
    prose = to_prose(ptext)
    for m in re.finditer(r'([a-z])\s+([,.])', prose):
        offset = m.start(); before = ptext[:offset].count('\n')
        add('punct', pstart + before, f'space before "{m.group(2)}" :: {prose[max(0,m.start()-40):m.end()+25]!r}')
    for m in re.finditer(r'(?:\.\s*[a-z]+\s*\.(?!\.))|(?:,,)|(?:;;)|(?::\s*:)', prose):
        if 'e.g' in m.group(0) or 'i.e' in m.group(0): continue
        offset = m.start(); before = ptext[:offset].count('\n')
        add('punct', pstart + before, f'double punct: {m.group(0)!r} :: {prose[max(0,m.start()-40):m.end()+25]!r}')

# ---------------- 3. misspellings (word boundaries)
MISS = {'proove','prooved','recieve','recieved','seperate','occured','occuring','wich',
        'adn','paramter','definiton','assymptotic','neccessary','verions','verison',
        'constuct','constuction','distibution','convervative','theorm','porposition',
        'defintion','remaark','propostion','condtion','complimentary','complimentarity'}
for pstart, ptext in paras:
    prose = to_prose(ptext)
    for w in MISS:
        for m in re.finditer(rf'\b{w}\b', prose, re.I):
            offset = m.start(); before = ptext[:offset].count('\n')
            add('spell', pstart + before, f'possible misspelling "{m.group(0)}"')

# ---------------- 4. sentence-initial lowercase (prose, refs are REF tokens)
ABBR = {'e.g','i.e','cf','vs','resp','approx','et al','Eq','Fig','No','Vol','pp','Sec',
        'a.m','p.m','St','Dr','Prof','Ph.D','U.S','eq','fig','sec','tab','rem','thm',
        'prop','lem','cor','def','ex','item','part','step','subsec'}
for pstart, ptext in paras:
    prose = to_prose(ptext)
    # remove the STARTITEM boundary markers from matching (new list item)
    for m in re.finditer(r'[.!?](?:\s+|\s*STARTITEM\s+)([a-z]{2})', prose):
        ctx = prose[max(0, m.start()-45):m.start()].strip().lower()
        if any(ctx.endswith(a.lower().rstrip('.') + '.') or ctx.endswith(a.lower()) for a in ABBR):
            continue
        offset = m.start(); before = ptext[:offset].count('\n')
        add('sent-case', pstart + before, f'lowercase "{m.group(1)}" after sentence end :: {prose[max(0,m.start()-55):m.end()+30]!r}')

# ---------------- 5. coinage capitalization (case-sensitive, running text)
for ln, line in enumerate(lines, 1):
    if line.lstrip().startswith('%'): continue
    t = re.sub(r'\$[^$]*\$', ' QMATQ ', strip_comments(line))
    t = re.sub(r'\\\[.*?\\\]', ' QDISPQ ', t, flags=re.S)
    for m in re.finditer(r'(?<![A-Za-z-])price of safety(?![-A-Za-z])', t):
        add('cap-coinage', ln, 'lowercase "price of safety" in running text')
    for m in re.finditer(r'(?<![A-Za-z-])unifilar lumpab(le|ility)(?![-A-Za-z])', t, re.I):
        pass

# ---------------- 6. hyphenation: right congruence (adj) vs right-congruence (noun)
ADJ_NEXT = {'Price','price','problem','optimization','index','constraint','feasible','class','structure',
            'setting','notion','form','bound','gap','formula','reading','sense','type','layer','regime',
            'machine','model','quotient','partitions','conventions','approach','feasible','sub','vertex'}
NOUN_NEXT = {'is','are','was','were','on','of','in','by','that','which','has','have','admits','refines',
             'contains','equals','and','or','the','a','an','to','for','with','at','if','then','denote'}
for ln, line in enumerate(lines, 1):
    if line.lstrip().startswith('%'): continue
    t = re.sub(r'\$[^$]*\$', ' QMATQ ', strip_comments(line))
    for m in re.finditer(r'(?<![a-zA-Z-])right congruence\s+([A-Za-z]+)', t):
        if m.group(1) in ADJ_NEXT:
            add('hyphen', ln, f'"right congruence {m.group(1)}" — adjectival, consider "right-congruence"')
    for m in re.finditer(r'(?<![a-zA-Z])right-congruence\s+([a-z]+)', t):
        if m.group(1) in NOUN_NEXT:
            add('hyphen', ln, f'"right-congruence {m.group(1)}" — noun usage, consider "right congruence"')

# ---------------- 7. math balance per paragraph
for pstart, ptext in paras:
    body = strip_comments(ptext).replace(r'\$', '')
    body = re.sub(r'\\\[.*?\\\]', '', body, flags=re.S)
    body = re.sub(r'\\\(.*?\\\)', '', body, flags=re.S)
    body = re.sub(r'\\verb\*?.', ' ', body)
    if len(re.findall(r'(?<!\\)\$', body)) % 2 == 1:
        add('math-balance', pstart, 'odd number of $ in paragraph')

# ---------------- 8. refs/cites
labels = set(re.findall(r'\\label\{([^}]+)\}', raw))
bibitems = set(re.findall(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}', raw))
cites = defaultdict(list)
for ln, line in enumerate(lines, 1):
    for m in re.finditer(r'\\(?:cite|citep|citet)\{([^}]+)\}', line):
        for k in m.group(1).split(','):
            cites[k.strip()].append(ln)
    for m in re.finditer(r'\\ref\{([^}]+)\}', line):
        if m.group(1) not in labels:
            add('ref', ln, f'undefined \\ref{{{m.group(1)}}}')
for k, lns in sorted(cites.items()):
    if k not in bibitems:
        add('cite', lns[0], f'cite to missing bibitem: {k}')
for b in sorted(bibitems):
    if b not in cites:
        add('cite-unused', 0, f'bibitem never cited: {b}')

# ---------------- report
cats = Counter(c for c, _, _ in findings)
print(f"TOTAL findings: {len(findings)}")
for c, n in cats.most_common(): print(f"  {c}: {n}")
print()
for cat in ['dup-word','punct','spell','sent-case','cap-coinage','hyphen','math-balance','ref','cite','cite-unused']:
    items = [(l, m) for c, l, m in findings if c == cat]
    if items:
        print(f"===== {cat} ({len(items)}) =====")
        for l, m in items[:25]:
            print(f"  L{l}: {m}")
        if len(items) > 25: print(f"  ... and {len(items)-25} more")
        print()
