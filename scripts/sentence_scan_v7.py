#!/usr/bin/env python3
"""Five-part review scanner for automata_unified_revised_v7.tex.

Q3 focus: remnants, redundancy, informal or change-log language.
Q4 support: flow-level mechanical flags (sentence-initial lowercase,
            informal sentence-initials, double punctuation).
Legacy checks: duplicate words, misspellings, $-balance, refs/cites,
               coinage capitalization, right-congruence hyphenation.
New checks: cross-section near-duplicate sentences; informal/changelog
            markers; empty/dangling comparative anchors.
Reports with line numbers for manual adjudication.
"""
import re
import sys
from collections import defaultdict, Counter

PATH = '/home/z/my-project/automata/download/automata_unified_revised_v7.tex'
raw = open(PATH, errors='replace').read()
lines = raw.split('\n')
findings = []


def add(cat, ln, msg):
    findings.append((cat, ln, msg))


def strip_comments(line):
    out, escaped = [], False
    for ch in line:
        if ch == '\\' and not escaped:
            escaped = True
            out.append(ch)
            continue
        if ch == '%' and not escaped:
            break
        out.append(ch)
        escaped = False
    return ''.join(out)


def strip_math(text):
    """Replace math spans with a single MATH token (interiors dropped)."""
    text = re.sub(r'\\\[.*?\\\]', ' MATH ', text, flags=re.S)
    text = re.sub(r'\\\(.*?\\\)', ' MATH ', text, flags=re.S)
    text = text.replace(r'\$', '\x00')
    while '$' in text:
        i = text.find('$')
        j = text.find('$', i + 1)
        if j < 0:
            text = text[:i] + ' MATH ' + text[i + 1:].replace('$', '')
            break
        text = text[:i] + ' MATH ' + text[j + 1:]
    return text.replace('\x00', '$')


# ---------------------------------------------------------------- paragraphs
paras, cur, start_line = [], [], 0
for ln, line in enumerate(lines, 1):
    if not line.strip():
        if cur:
            paras.append((start_line, ' \n '.join(cur)))
        cur, start_line = [], ln + 1
    else:
        if not cur:
            start_line = ln
        cur.append(strip_comments(line))
if cur:
    paras.append((start_line, ' \n '.join(cur)))

# section lookup for cross-section duplicate reporting
sec_marks = []
for ln, line in enumerate(lines, 1):
    m = re.match(r'\\section\*?\{', line)
    if m:
        sec_marks.append(ln)
sec_marks.append(len(lines) + 2)


def section_of(ln):
    for i, s in enumerate(sec_marks[:-1]):
        if s <= ln < sec_marks[i + 1]:
            return i + 1
    return 0


# ---------------------------------------------------------------- 1. duplicate words
dup_re = re.compile(r'\b(\w+)\s+\1\b', re.I)
SKIP_DUP = {'S', 'A', 'M'}
for pstart, ptext in paras:
    prose = strip_math(ptext)
    prose = re.sub(r'\\[a-zA-Z]+(\*|\{\}|\{[^}]*\})*', ' ', prose)
    for m in dup_re.finditer(prose):
        w = m.group(1)
        if w in SKIP_DUP:
            continue
        before = ptext[:m.start()].count('\n')
        add('dup-word', pstart + before, f'"{w} {w}"')

# ---------------------------------------------------------------- 2. punctuation
for ln, line in enumerate(lines, 1):
    if line.lstrip().startswith('%'):
        continue
    t = strip_math(strip_comments(line))
    if re.search(r'[a-z]\.\.', t):
        add('punct', ln, 'double period after letter')
    if re.search(r',\s*,', t):
        add('punct', ln, 'double comma')
    if re.search(r'[a-z]\s+,', t):
        add('punct', ln, 'space before comma')
    if re.search(r'[a-z]\s+\.', t):
        add('punct', ln, 'space before period')
    if re.search(r';;|:\s*:', t):
        add('punct', ln, 'double semicolon/colon')
    if re.search(r'~~', line):
        add('punct', ln, 'double tilde')

# ---------------------------------------------------------------- 3. misspellings
MISSPELL = ['proove', 'prooved', 'recieve', 'seperate', 'occured', 'occuring',
            'wich', 'adn', 'paramter', 'complimentarity', 'definiton',
            'assymptotic', 'asympotic', 'neccessary', 'recieved',
            'verions', 'verison', 'constuct', 'constuction', 'distibution',
            'convervative', 'theorm', 'porposition', 'lemme', 'corrallary',
            'defintion', 'remaark', 'propostion', 'condtion', 'ommit',
            'occurence', 'sucessive', 'recurrance', 'superceded']
for ln, line in enumerate(lines, 1):
    if line.lstrip().startswith('%'):
        continue
    t = strip_math(strip_comments(line)).lower()
    for w in MISSPELL:
        if w in t:
            add('spell', ln, f'suspected misspelling: {w}')

# ---------------------------------------------------------------- 4. $ balance
for pstart, ptext in paras:
    body = strip_comments(ptext).replace(r'\$', '')
    body2 = re.sub(r'\\\[.*?\\\]', '', body, flags=re.S)
    body2 = re.sub(r'\\\(.*?\\\)', '', body2, flags=re.S)
    body2 = re.sub(r'\\verb\*?.', ' ', body2)
    dollars = len(re.findall(r'(?<!\\)\$', body2))
    if dollars % 2 == 1:
        add('math-balance', pstart, f'odd number of $ ({dollars}) in paragraph')

# ---------------------------------------------------------------- 5. refs and cites
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
for k, lns in cites.items():
    if k not in bibitems:
        add('cite', lns[0], f'cite to missing bibitem: {k}')
for b in bibitems:
    if b not in cites:
        add('cite-unused', 0, f'bibitem never cited: {b}')

# ---------------------------------------------------------------- 6. sentence-initial lowercase
for pstart, ptext in paras:
    prose = strip_math(strip_comments(ptext))
    prose = re.sub(r'\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^{}]*\})?', ' ', prose)
    for m in re.finditer(r'[.!?]\s+([a-z])', prose):
        ctx = prose[max(0, m.start() - 30):m.start()]
        if re.search(r'(?:e\.g|i\.e|cf|vs|resp|approx|et al|Eq|Fig|No|Vol|pp|Sec)\.$',
                     ctx.strip() + '.'):
            continue
        if re.search(r'\b(?:figure|table|section|theorem|proposition|lemma|corollary|definition|remark|equation|part|item|step|chapter|open problem)\s+[0-9IVX]+\.$', ctx, re.I):
            continue
        before = ptext[:m.start()].count('\n')
        add('sent-case', pstart + before,
            f'lowercase "{m.group(1)}" after sentence end: ...{prose[max(0, m.start()-40):m.start()+20]!r}')

# ---------------------------------------------------------------- 7. coinage capitalization
for ln, line in enumerate(lines, 1):
    if line.lstrip().startswith('%'):
        continue
    t = strip_math(strip_comments(line))
    for m in re.finditer(r'\bprice of safety\b', t, re.I):
        pass  # handled in prior rounds; keep silent here unless lowercase
    for m in re.finditer(r'\bprice of safety\b', t):
        ctx = t[max(0, m.start() - 60):m.end() + 60]
        if '\\footnote' in ctx or 'bandits' in ctx or 'linear best arm' in ctx:
            continue  # the disambiguation footnote quotes the other sense
        add('cap-consistency', ln, '"price of safety" lowercase (convention: capitalized)')

# ---------------------------------------------------------------- 8. right-congruence hyphenation
ADJ_NOUNS = ['Price', 'price', 'problem', 'optimization', 'index', 'constraint',
             'feasible', 'class', 'structure', 'setting', 'notion', 'form',
             'bound', 'gap', 'formula', 'reading', 'sense', 'type', 'layer',
             'regime', 'machine', 'model', 'quotient', 'partitions', 'conventions']
for ln, line in enumerate(lines, 1):
    if line.lstrip().startswith('%'):
        continue
    t = strip_math(strip_comments(line))
    for m in re.finditer(r'right congruence\s+([A-Za-z]+)', t):
        if m.group(1) in ADJ_NOUNS:
            add('hyphen', ln, f'adjectival "right congruence {m.group(1)}" may need hyphen')
    for m in re.finditer(r'right-congruence\s+([a-z]+)', t):
        if m.group(1) in ('is', 'are', 'on', 'of', 'in', 'by', 'that', 'which',
                          'has', 'admits', 'refines', 'contains', 'equals',
                          'and', 'or', 'the', 'a'):
            add('hyphen', ln, f'possible noun use of "right-congruence {m.group(1)}"')

# ---------------------------------------------------------------- 9. NEW: informal / change-log language
INFORMAL = [
    (r'\bTODO\b', 'TODO remnant'),
    (r'\bFIXME\b', 'FIXME remnant'),
    (r'\bXXX\b(?!\{)', 'XXX remnant'),
    (r'\bTBD\b', 'TBD placeholder'),
    (r'\bplaceholder\b', 'word "placeholder"'),
    (r'\bwe (?:now|first) (?:prove|show|state|define)\b.*\bversion\b', 'possible version language'),
    (r'\bin (?:this|the) (?:revised|new|current|updated) version\b', 'change-log language'),
    (r'\bas (?:promised|announced) (?:above|earlier|before)\b', 'change-log language'),
    (r'\bwe have (?:already )?(?:seen|noted|observed|remarked|shown)\b', 'possible redundancy marker'),
    (r'\bas (?:already )?(?:noted|mentioned|observed|remarked|discussed|stated) (?:above|earlier|before|previously)\b', 'back-reference marker'),
    (r'\b(cf|see) (?:above|Section above)\b', 'dangling back-reference'),
    (r'\brecall (?:from|that) (?:above|the (?:previous|preceding) (?:section|chapter))\b', 'back-reference marker'),
    (r'\bthe reader (?:will|may) (?:recall|remember|have noticed)\b', 'recall phrasing'),
    (r'\bfor completeness,? we (?:repeat|recall|restate)\b', 'explicit restatement'),
    (r'\bwe remind the reader\b', 'reminder phrasing'),
    (r'\bit bears repeating\b', 'repetition flag'),
    (r'\bagain,?\b', 'possible redundancy word'),
    (r'\bonce (?:more|again)\b', 'repetition phrase'),
    (r'\bwe (?:have )?(?:deleted|removed|dropped|added|inserted|renamed)\b', 'change-log language'),
    (r'\bin the (?:previous|earlier|original|old) (?:version|draft|revision)\b', 'change-log language'),
    (r'\bfirst draft\b|\boriginal draft\b', 'draft language'),
    (r'\bpreliminary version\b', 'version language'),
    (r'\bwe point out that\b', 'filler phrase'),
    (r'\bof course\b', 'informal filler'),
    (r'\bobviously\b', 'informal filler'),
    (r'\btrivially,?\b', 'informal filler (check if proof term of art)'),
    (r'\bin fact\b', 'check: overused filler?'),
    (r'\bas is well known\b|\bwell-known fact\b', 'appeal to folklore'),
    (r'\bthe details are (?:routine|straightforward|easy)\b', 'hand-wave'),
    (r'\bthe rest is\b|\bthe remainder is (?:routine|easy|straightforward)\b', 'hand-wave'),
    (r'\bthe proof is (?:easy|simple|routine|immediate)\b', 'check: acceptable if proof follows'),
    (r'\bsimilarly,? (?:for|as) (?:above|before)\b', 'dangling similarity'),
    (r'\bthe same (?:argument|proof) as (?:above|before)\b', 'dangling back-ref'),
    (r'\bwe omit the (?:routine|tedious|easy) (?:details|verification)\b', 'omission hand-wave'),
    (r'\bslogan\b', 'informal: "slogan"'),
    (r'\bspeaking loosely\b|\bloosely speaking\b|\bintuitively,? (?:roughly|sort of)\b', 'loose language'),
    (r'\bsort of\b|\bkind of\b', 'very informal'),
    (r'\bstuff\b|\bthings\b', 'very informal'),
    (r'\bgood enough\b', 'informal'),
    (r'\bbig\b|\bhuge\b', 'check register'),
    (r'\bvery (?:nice|beautiful|elegant|cool)\b', 'subjective praise'),
    (r'\binterestingly,?\b|\bremarkably,?\b|\bamusingly\b', 'editorializing'),
    (r'\bwe (?:would|should) (?:like to|mention that)\b', 'filler'),
    (r'\bneedless to say\b', 'filler'),
    (r'\bby the way\b', 'informal'),
    (r'\bupshot\b', 'informal'),
    (r'\bbottom line\b', 'informal'),
    (r'\bline of attack\b', 'informal (maybe ok)'),
    (r'\bplugging in\b', 'informal'),
    (r'\bchug\b|\bcrank\b|\bgrind\b', 'informal'),
    (r'\bhindsight\b', 'informal'),
    (r'\broadmap\b', 'check: roadmap vs plan'),
]
for ln, line in enumerate(lines, 1):
    if line.lstrip().startswith('%'):
        continue
    t = strip_math(strip_comments(line))
    for pat, label in INFORMAL:
        for m in re.finditer(pat, t, re.I):
            add('informal', ln, f'{label}: ...{t[max(0,m.start()-40):m.end()+40]!r}')

# ---------------------------------------------------------------- 10. NEW: cross-section duplicate sentences
def normalize_sentence(s):
    s = strip_math(s)
    s = re.sub(r'\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^{}]*\})?', ' ', s)
    s = re.sub(r'~', ' ', s)
    s = re.sub(r'[0-9]+', 'N', s)
    s = re.sub(r'[^a-zA-Z ]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip().lower()
    return s

sent_store = defaultdict(list)
for pstart, ptext in paras:
    prose = strip_math(strip_comments(ptext))
    # remove display math already; remove macros
    prose = re.sub(r'\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^{}]*\})?', ' ', prose)
    # split at sentence enders
    for sm in re.finditer(r'[^.!?]+[.!?]', prose):
        sent = sm.group(0)
        norm = normalize_sentence(sent)
        words = norm.split()
        if len(words) < 8:      # too short to matter
            continue
        if len(words) > 60:     # likely a split artifact
            continue
        sent_store[norm].append((pstart, sent.strip()[:100]))

dup_reported = set()
for norm, occ in sent_store.items():
    if len(occ) < 2:
        continue
    secs = {section_of(ln) for ln, _ in occ}
    if len(secs) < 2:  # only cross-section duplicates are interesting
        continue
    key = norm[:60]
    if key in dup_reported:
        continue
    dup_reported.add(key)
    lns = ', '.join(str(ln) for ln, _ in occ)
    add('dup-sentence-xsec', int(min(ln for ln, _ in occ)),
        f'cross-section repeated sentence ({len(occ)}x, secs {sorted(secs)}, lines {lns}): "{occ[0][1]}"')

# ---------------------------------------------------------------- 11. informal sentence-initials
INITIALS = r'^(?:Also|And|But|So|Now|Plus|Again|Besides|Moreover)\b'
for ln, line in enumerate(lines, 1):
    if line.lstrip().startswith('%') or line.lstrip().startswith('\\'):
        continue
    t = strip_math(strip_comments(line)).strip()
    if re.match(INITIALS, t):
        add('flow-initial', ln, f'sentence-initial connective: "{t[:60]}"')

# ---------------------------------------------------------------- report
cats = Counter(c for c, _, _ in findings)
print(f"TOTAL findings: {len(findings)}")
for c, n in cats.most_common():
    print(f"  {c}: {n}")
print()
LIMITS = {'dup-word': 40, 'punct': 40, 'spell': 30, 'math-balance': 20,
          'ref': 20, 'sent-case': 30, 'cap-consistency': 20, 'hyphen': 30,
          'informal': 80, 'dup-sentence-xsec': 40, 'flow-initial': 40,
          'cite': 10, 'cite-unused': 10}
for cat, _ in cats.most_common():
    subset = [f for f in findings if f[0] == cat][:LIMITS.get(cat, 20)]
    print(f'================ {cat} ({cats[cat]} shown {len(subset)}) ================')
    for _, ln, msg in subset:
        print(f'  L{ln}: {msg}')
    print()
