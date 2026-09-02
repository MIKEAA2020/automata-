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

"""Regenerate automata_pastesafe.tex from automata_corrected.tex.

Rewrites the BODY so that no control sequence begins with backslash-n,
defeating transmission pipelines that interpret backslash-n as a newline.
Preamble declaration lines must keep \newcommand/\newtheorem literally.
"""
import io, re, sys

SRC = _p('automata_corrected.tex')
DST = _p('automata_pastesafe.tex')

s = io.open(SRC, encoding='utf-8', newline='').read()

# split preamble (declarations) from body at \begin{document}
i = s.index(r'\begin{document}')
pre, body = s[:i], s[i:]

# body-level renames: macro -> alias with no leading 'n'
REN = [(r'\norm',   r'\Vnorm'),
       (r'\nu',     r'\Nuu'),
       (r'\noindent', r'\Noind'),
       (r'\nabla',  r'\Nabla'),
       (r'\neq',    r'\Neq'),
       (r'\notin',  r'\Notin'),
       (r'\ne',     r'\Neq'),
       (r'\not',    r'\Nott')]

counts = {}
# longest-first so \norm/\noindent/\nabla/\notin/\neq beat \nu and \ne
for old, new in sorted(REN, key=lambda kv: -len(kv[0])):
    pat = re.compile(re.escape(old) + r'(?![A-Za-z])')
    body, n = pat.subn(new.replace('\\', '\\\\'), body)
    counts[old] = counts.get(old, 0) + n

# alias definitions, built with \csname so the source has no backslash-n
alias = r"""
%% ---- paste-safe aliases (no control sequence begins with backslash-n) ----
%% Each alias expands to the original macro via \csname, so the ORIGINAL
%% definitions in the preamble remain the single source of truth.
%% \def (not \let) is required: \let would bind the literal \csname token.
\expandafter\def\csname Vnorm\endcsname{\csname norm\endcsname}
\expandafter\def\csname Nuu\endcsname{\csname nu\endcsname}
\expandafter\def\csname Noind\endcsname{\csname noindent\endcsname}
\expandafter\def\csname Nabla\endcsname{\csname nabla\endcsname}
\expandafter\def\csname Neq\endcsname{\csname neq\endcsname}
\expandafter\def\csname Notin\endcsname{\csname notin\endcsname}
\expandafter\def\csname Nott\endcsname{\csname not\endcsname}
%% -------------------------------------------------------------------------
"""
body = body.replace(r'\begin{document}',
                    alias.replace('\n', '\r\n') + '\r\n' + r'\begin{document}', 1)

nvn  = len(re.findall(r'\\Vnorm', body))
nnuu = len(re.findall(r'\\Nuu', body))

header = f"""%% =================================================================
%% PASTE-SAFE EDITION
%%
%% Identical mathematics to automata_corrected.tex.  The body of this
%% file contains NO control sequence beginning with backslash-n, so a
%% transmission pipeline that interprets backslash-n as a newline
%% cannot corrupt it.  Only the preamble declaration lines use
%% \\newcommand / \\newtheorem, which LaTeX requires literally.
%%
%% Integrity check after any copy/paste:
%%   grep -c 'ewtheorem{{' FILE  -> must be 12 (the preamble
%%                                 declarations, which LaTeX
%%                                 requires literally); a mangled
%%                                 copy shows MORE than 12, and the
%%                                 body count below drops to 0.
%%   grep -c 'Vnorm'       FILE   -> must be {nvn}
%%   grep -c 'Nuu'         FILE   -> must be {nnuu}
%% If the first exceeds 12, or either of the others is 0, your copy
%% was mangled in transit; the source on disk is intact.
%% =================================================================
""".replace('\n', '\r\n')

out = header + pre + body
io.open(DST, 'w', encoding='utf-8', newline='').write(out)

print('renames applied:', {k: v for k, v in counts.items() if v})
print(f'\\Vnorm={nvn}  \\Nuu={nnuu}')

# integrity: no bare backslash-n control sequence in the BODY
j = out.index(r'\begin{document}')
bad = re.findall(r'\\n[a-zA-Z]+', out[j:])
print('backslash-n control sequences in body:', len(set(bad)), sorted(set(bad))[:10])
sys.exit(1 if bad else 0)
