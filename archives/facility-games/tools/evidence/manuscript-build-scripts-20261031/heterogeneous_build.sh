#!/usr/bin/env bash
set -euo pipefail
paper_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
cd "$paper_dir"
mkdir -p build
# A normal TeX installation needs only the two final pdflatex invocations.
# This fallback also supports the minimal TeX Live layout in the research workspace.
if ! kpsewhich article.cls >/dev/null 2>&1 || ! kpsewhich pdflatex.fmt >/dev/null 2>&1; then
  export TEXMF='{/usr/share/texlive/texmf-dist,/usr/share/texmf}'
  export TEXINPUTS='/usr/share/texlive/texmf-dist/tex//:/usr/share/texmf/tex//:'
  export TEXFORMATS="$paper_dir/build:"
  if [[ ! -f build/pdflatex.fmt ]]; then
    pdftex -ini -etex -interaction=nonstopmode -halt-on-error -jobname=pdflatex -output-directory=build pdflatex.ini > build/format.log
  fi
fi
pdflatex -interaction=nonstopmode -halt-on-error main.tex > build/pass1.log
pdflatex -interaction=nonstopmode -halt-on-error main.tex > build/pass2.log
