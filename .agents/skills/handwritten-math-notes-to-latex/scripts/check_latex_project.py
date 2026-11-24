#!/usr/bin/env python3
"""Read-only structural checks for a reconstructed LaTeX manuscript."""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path


PAGE_RE = re.compile(r"^\s*%\s*Source PDF page\s+(\d+)", re.IGNORECASE)
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
ENV_RE = re.compile(r"\\(begin|end)\{([^}]+)\}")
INCLUDE_RE = re.compile(r"\\(?:include|input)\{([^}]+)\}")


def strip_comment(line: str) -> str:
    """Remove a LaTeX comment while retaining escaped percent signs."""
    for index, character in enumerate(line):
        if character != "%":
            continue
        backslashes = 0
        cursor = index - 1
        while cursor >= 0 and line[cursor] == "\\":
            backslashes += 1
            cursor -= 1
        if backslashes % 2 == 0:
            return line[:index]
    return line


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--main", default="main.tex", help="Main TeX file relative to the project root")
    parser.add_argument("--expected-start", type=int)
    parser.add_argument("--expected-end", type=int)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.project_root.resolve()
    if not root.is_dir():
        print(f"Project directory not found: {root}", file=sys.stderr)
        return 2

    tex_files = sorted(
        path
        for path in root.rglob("*.tex")
        if ".cache" not in path.relative_to(root).parts
    )
    if not tex_files:
        print(f"No TeX files found under {root}", file=sys.stderr)
        return 2

    labels: dict[str, list[str]] = defaultdict(list)
    page_records: list[tuple[int, Path, int]] = []
    check_markers: list[str] = []
    unclear_markers: list[str] = []
    structural_problems: list[str] = []

    for tex_file in tex_files:
        lines = tex_file.read_text(encoding="utf-8-sig").splitlines()
        stack: list[tuple[str, int]] = []
        last_page: int | None = None
        for line_number, line in enumerate(lines, start=1):
            page_match = PAGE_RE.match(line)
            if page_match:
                page = int(page_match.group(1))
                page_records.append((page, tex_file, line_number))
                if last_page is not None and page < last_page:
                    structural_problems.append(
                        f"Out-of-order source page {page}: {tex_file}:{line_number}"
                    )
                last_page = page

            if re.search(r"%\s*CHECK:", line):
                check_markers.append(f"{tex_file}:{line_number}")
            if "Unclear in the original manuscript" in line or r"\textcolor{red}" in line:
                unclear_markers.append(f"{tex_file}:{line_number}")
            for label in LABEL_RE.findall(line):
                labels[label].append(f"{tex_file}:{line_number}")

            for kind, environment in ENV_RE.findall(strip_comment(line)):
                if kind == "begin":
                    stack.append((environment, line_number))
                elif not stack:
                    structural_problems.append(
                        f"Unmatched end{{{environment}}}: {tex_file}:{line_number}"
                    )
                else:
                    opened, opened_line = stack.pop()
                    if opened != environment:
                        structural_problems.append(
                            f"Environment mismatch begin{{{opened}}} at line {opened_line} "
                            f"and end{{{environment}}}: {tex_file}:{line_number}"
                        )
        for environment, line_number in reversed(stack):
            structural_problems.append(
                f"Unclosed begin{{{environment}}}: {tex_file}:{line_number}"
            )

    duplicate_labels = {label: owners for label, owners in labels.items() if len(owners) > 1}

    main_path = root / args.main
    missing_includes: list[Path] = []
    if main_path.is_file():
        main_text = main_path.read_text(encoding="utf-8-sig")
        for relative in INCLUDE_RE.findall(main_text):
            candidates = [root / relative, root / f"{relative}.tex"]
            if not any(candidate.is_file() for candidate in candidates):
                missing_includes.append(candidates[-1])

    unique_pages = sorted({record[0] for record in page_records})
    missing_pages: list[int] = []
    if args.expected_start is not None or args.expected_end is not None:
        if args.expected_start is None or args.expected_end is None:
            print("Use --expected-start and --expected-end together.", file=sys.stderr)
            return 2
        expected = set(range(args.expected_start, args.expected_end + 1))
        missing_pages = sorted(expected.difference(unique_pages))

    observed_range = f"{unique_pages[0]}-{unique_pages[-1]}" if unique_pages else "none"
    print(f"Project root: {root}")
    print(f"TeX files: {len(tex_files)}")
    print(f"Source-page comments: {len(page_records)}")
    print(f"Unique source pages: {len(unique_pages)}")
    print(f"Observed source range: {observed_range}")
    print(f"Missing expected pages: {', '.join(map(str, missing_pages)) or 'none'}")
    print(f"Duplicate labels: {len(duplicate_labels)}")
    print(f"Missing includes: {len(missing_includes)}")
    print(f"Environment/order problems: {len(structural_problems)}")
    print(f"CHECK markers: {len(check_markers)}")
    print(f"Unclear markers: {len(unclear_markers)}")

    if duplicate_labels:
        print("\nDuplicate labels:")
        for label, owners in sorted(duplicate_labels.items()):
            print(f"  {label}: {'; '.join(owners)}")
    if missing_includes:
        print("\nMissing includes:")
        for path in missing_includes:
            print(f"  {path}")
    if structural_problems:
        print("\nEnvironment or ordering problems:")
        for problem in structural_problems:
            print(f"  {problem}")
    if check_markers:
        print("\nCHECK markers:")
        for marker in check_markers:
            print(f"  {marker}")
    if unclear_markers:
        print("\nUnclear markers:")
        for marker in unclear_markers:
            print(f"  {marker}")

    failed = duplicate_labels or missing_includes or structural_problems or missing_pages
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
