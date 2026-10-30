"""Prepare the third manuscript with the official INFORMS MOR class.

Usage: python3 research/manuscripts/prepare_mor.py TEMPLATE_DIR OUTPUT_DIR
The output directory should be outside the public research repository.
"""
import argparse
from pathlib import Path
import shutil

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('template_dir', type=Path, help='unpacked official INFORMS MOR template directory')
parser.add_argument('output_dir', type=Path, help='private destination')
args = parser.parse_args()

root = Path(__file__).resolve().parents[2]
src_dir = root / 'research/current/weighted_congestion/structural_reconstruction'
template = args.template_dir.resolve()
out = args.output_dir.resolve()
if root == out or root in out.parents:
    parser.error('output_dir must be outside the public repository')
out.mkdir(exist_ok=True)
for name in ('informs4.cls', 'eqndefns-left.sty', 'informs2014.bst', 'informs_Logo.pdf'):
    shutil.copy2(template / name, out / name)
shutil.copy2(src_dir / 'structural_methods_article.bib', out / 'main.bib')

source = (src_dir / 'structural_methods_article.tex').read_text()
abstract = source.split('\\begin{abstract}', 1)[1].split('\\end{abstract}', 1)[0].strip()
body = source.split('\\section{Introduction}', 1)[1]
body = '\\section{Introduction}' + body
body = body.rsplit('\\bibliographystyle', 1)[0]
intro_disclosure = '\\subsection{Research process and AI assistance}'
if intro_disclosure in body:
    front, tail = body.split(intro_disclosure, 1)
    body = front + '\\paragraph{Organization.}' + tail.split('\\paragraph{Organization.}', 1)[1]
body = body.replace('actual resource incidences in Appendix~\\ref{app:construction}',
                    'actual resource incidences in Section~\\ref{sec:application}')
body = body.replace('A test $(a,b,k,o)$, $a<b$, has a pair',
                    'A test $\\tau=(a,b,k,o)$, $a<b$, has a pair')
body = body.replace('All positive tools in the paper construct such scales;',
                    'The potential constructions below choose such scales;')
body = body.replace(
    r' C_i^B(s)\le B_*=(g+1)R^gT' + '\n'
    + r' \quad\text{for all players and all base states},\qquad' + '\n'
    + r' B_*/\eta\le64n(g+1)R^g.',
    r' \begin{aligned}' + '\n'
    + r' C_i^B(s)&\le B_*=(g+1)R^gT'
    + r'\quad\text{for all players and all base states},\\' + '\n'
    + r' B_*/\eta&\le64n(g+1)R^g.' + '\n'
    + r' \end{aligned}')
# The required disclosure follows the mathematics and precedes the reference list.
disclosure = r'''\subsection*{Use of generative AI in the research process}
OpenAI ChatGPT/Codex models, including GPT-6.1-sol, were used to explore
candidate constructions, check algebraic estimates and edge cases, write
finite exact audit programs, and critique drafts of the proofs and exposition.
The systems were directed to keep the mathematical objects, domains,
quantifiers, assumptions, and conclusions fixed; to attack all-state and
boundary cases; to separate finite computation from proof; and to retain
unresolved objections as such. The full mathematical arguments appear in the
paper; the finite checks are supplementary. The human authors remain
responsible for verifying the submitted work.

'''
body = body.replace(
    r'\begin{proof}[Proof of Theorem~\ref{thm:uniformfamily}]',
    r'\begin{proof}{Proof of Theorem~\ref{thm:uniformfamily}}')
body = body.replace('\\begin{proof}' + '\n', '\\begin{proof}{Proof}' + '\n')
body = body.replace('\\end{proof}', '\\Halmos\n\\end{proof}')
body = body.replace('\\appendix\n', disclosure + '\\begin{APPENDICES}\n')
body += '\\end{APPENDICES}\n'

header = r'''\documentclass[moor,dblanonrev]{informs4}
\usepackage{eqndefns-left}
\usepackage{mathtools,booktabs}
%% The minimal build image lacks the template's preferred Times font package.
\renewcommand{\rmdefault}{cmr}
\renewcommand{\sfdefault}{cmss}
\renewcommand{\ttdefault}{cmtt}
\OneAndAHalfSpacedXI
\EquationsNumberedThrough
\TheoremsNumberedBySection
\newcommand{\PNE}{\mathrm{PNE}}
\newcommand{\OPT}{\mathrm{OPT}}
\newcommand{\F}{\mathcal F}
\newcommand{\ind}{\mathbf 1}
\newcommand{\xor}{\mathbin{\oplus}}
\newcommand{\A}{\mathsf A}
\newcommand{\B}{\mathsf B}
\newcommand{\R}{\mathbb R}
\newcommand{\N}{\mathbb N}
\DeclareMathOperator{\pos}{pos}
\begin{document}
\RUNAUTHOR{Anonymous authors}
\RUNTITLE{Structural Methods for Approximate Stability}
\TITLE{Structural Methods for Approximate Stability in Weighted Congestion Games}
\ARTICLEAUTHORS{}
\ABSTRACT{%s}
\KEYWORDS{weighted congestion games, approximate pure Nash equilibria, approximate potentials, social cost}
\maketitle
''' % abstract
footer = r'''\bibliographystyle{amsplain}
\bibliography{main}
\end{document}
'''
(out / 'main.tex').write_text(header + body + footer)
