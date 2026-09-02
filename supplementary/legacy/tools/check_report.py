import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.environ.get('BST_ROOT', _os.path.dirname(_HERE))
def _p(name):
    for c in (_os.path.join(_ROOT, name),
              _os.path.join(_ROOT, 'manuscript.tex') if name.endswith('.tex') else '',
              _os.path.join(_HERE, name)):
        if c and _os.path.exists(c):
            return c
    return _os.path.join(_ROOT, name)

"""Verify every manuscript label cited in the memorandum actually exists."""
import io
import re
import sys

tex = io.open(_p('automata_corrected.tex'), encoding='utf-8',
              newline='').read().replace('\r\n', '\n')
rep = io.open(_p('open_problems_report.md'), encoding='utf-8').read()

labels = set(re.findall(r'\\label\{([^}]*)\}', tex))

# backtick-quoted tokens in the report that look like labels
cited = set(re.findall(r'`((?:thm|lem|prop|cor|def|rem|ass|open|sec|tab|eq|fig|subsec):[A-Za-z0-9\-]+)`', rep))

# A label the memo explicitly documents as withdrawn/retired is not drift:
# the memo is *supposed* to record that it no longer exists.  Recognise the
# pattern "`label`  ... retired|withdrawn" within the same paragraph.
retired = set()
for lab in cited - labels:
    for m in re.finditer(re.escape('`' + lab + '`'), rep):
        para = rep[max(0, m.start() - 400):m.start() + 400].lower()
        if 'retire' in para or 'withdraw' in para:
            retired.add(lab)
            break
if retired:
    print('retired-and-documented (not drift): ' + ', '.join(sorted(retired)))
missing = sorted(cited - labels - retired)

print(f'{len(labels)} labels in manuscript, {len(cited)} label-like tokens cited in report')
if missing:
    print('MISSING FROM MANUSCRIPT:')
    for m in missing:
        print('   -', m)
else:
    print('every cited label resolves')

# environment titles cited in prose (report uses `Assumption (...)` / `Lemma (...)`)
titles = re.findall(r'`(?:Assumption|Lemma|Theorem|Definition|Proposition|Corollary) \(([^)]*)\)`', rep)
tex_titles = re.findall(r'\\begin\{(?:assumption|lemma|theorem|definition|proposition|corollary)\}\[([^\]]*)\]', tex)


def norm(t):
    """Canonicalise: LaTeX -- vs en-dash, drop trailing math like $\\Gact_M$."""
    t = re.sub(r'\$[^$]*\$', '', t)          # strip math
    t = t.replace('--', '\u2013').replace('\u2014', '\u2013')
    return ' '.join(t.split()).lower()


tex_flat = {norm(t) for t in tex_titles}
bad = [t for t in titles if norm(t) not in tex_flat]
print()
print(f'{len(titles)} environment titles cited by name in report')
if bad:
    print('TITLES NOT FOUND IN MANUSCRIPT:')
    for b in bad:
        print('   -', repr(b))
else:
    print('every cited environment title resolves')

sys.exit(1 if (missing or bad) else 0)
