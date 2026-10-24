#!/usr/bin/env python3
"""Build the three manuscripts without changing their source or page layout."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PAPERS = {
    "shared": HERE / "shared_catalog/main.tex",
    "multiple": HERE / "multiple_facilities/main.tex",
    "congestion": ROOT / "research/current/weighted_congestion/structural_reconstruction/structural_methods_article.tex",
}


def run(command: list[str], cwd: Path, env: dict[str, str], log: Path) -> None:
    result = subprocess.run(command, cwd=cwd, env=env, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log.write_text(result.stdout)
    if result.returncode:
        raise SystemExit(f"Build failed; inspect {log}\n{result.stdout[-3000:]}")


def build(source: Path) -> None:
    directory = source.parent
    temporary = directory / ".build"
    temporary.mkdir(exist_ok=True)
    env = os.environ.copy()
    # Some minimal TeX installations have source files but no generated format
    # or file-name database. Use the installed files directly, without installs.
    tree = Path("/usr/share/texlive/texmf-dist")
    if tree.is_dir():
        for variable, suffix in {
            "TEXINPUTS": "tex//", "TFMFONTS": "fonts/tfm//",
            "T1FONTS": "fonts/type1//", "BSTINPUTS": "bibtex/bst//",
        }.items():
            env[variable] = f".:{tree}/{suffix}:" + env.get(variable, "")
        env["TEXFORMATS"] = str(temporary) + ":" + env.get("TEXFORMATS", "")
        env["TEXFONTMAPS"] = f"{temporary}:{tree}/fonts/map//:"
        maps = [tree / "fonts/map/dvips/amsfonts" / name
                for name in ("cm.map", "cmextra.map", "symbols.map")]
        if all(path.is_file() for path in maps):
            (temporary / "pdftex.map").write_text("\n".join(path.read_text() for path in maps))
        found = subprocess.run(["kpsewhich", "pdflatex.fmt"], env=env,
                               text=True, stdout=subprocess.PIPE)
        if not found.stdout.strip():
            run(["pdftex", "-ini", "-etex", "-jobname=pdflatex",
                 "-progname=pdflatex", "-interaction=nonstopmode",
                 "-halt-on-error", f"-output-directory={temporary}", "pdflatex.ini"],
                directory, env, temporary / "format-build.txt")
    run(["latexmk", "-pdf", "-g", "-interaction=nonstopmode",
         "-halt-on-error", f"-outdir={temporary}", source.name],
        directory, env, temporary / "build.txt")
    log = (temporary / f"{source.stem}.log").read_text(errors="replace")
    problems = [line for line in log.splitlines()
                if "undefined" in line.lower() or line.startswith("!")
                or "LaTeX Warning:" in line or "Overfull" in line]
    if problems:
        raise SystemExit(f"Unresolved diagnostics in {source}:\n" + "\n".join(problems))
    output = source.with_suffix(".pdf")
    shutil.copyfile(temporary / output.name, output)
    print(output.relative_to(ROOT))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("papers", nargs="*", choices=tuple(PAPERS), default=list(PAPERS))
    arguments = parser.parse_args()
    for key in arguments.papers:
        build(PAPERS[key])


if __name__ == "__main__":
    main()
