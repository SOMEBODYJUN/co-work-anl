"""Compile the authoritative main.tex; never regenerate its mathematical text."""
from pathlib import Path
import os
import subprocess

out = Path(__file__).resolve().parent
build = out / 'build'
build.mkdir(exist_ok=True)
env = os.environ.copy()
# This runtime's filename database is unavailable; a direct TeX tree is enough.
tex_tree = Path('/usr/share/texlive/texmf-dist')
if tex_tree.exists():
    env.setdefault('TEXMF', str(tex_tree))
command = ['pdflatex']
local_format = build / 'pdflatex.fmt'
if local_format.exists():
    command.append('-fmt=' + str(local_format))
command += ['-interaction=nonstopmode', '-halt-on-error', 'main.tex']
for pass_number in (1, 2):
    completed = subprocess.run(command, cwd=out, env=env,
                               text=True, capture_output=True)
    log = build / ('compile_polynomial_pass%d.log' % pass_number)
    log.write_text(completed.stdout + completed.stderr)
    if completed.returncode:
        raise SystemExit('Compilation failed; inspect ' + str(log))
print(out / 'main.pdf')
