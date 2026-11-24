# QA, Storage, Backup, and Delivery

## Storage policy

Keep rendered PDF pages, OCR intermediates, temporary crops, generated figures, TeX auxiliary files, and experiments inside a project-owned cache such as `.cache/<checkpoint-or-task>/` or another location approved by the user. Reuse valid caches and honor any storage constraints stated by the user.

Place durable source in the project tree, final PDFs in the documented output location, and backups in the configured backup directory. Never delete or overwrite a user backup merely to reduce space.

## Backup policy

Before experimental figure replacement, bulk normalization, or a high-impact retrospective correction, copy only the affected source files and assets to a timestamped backup folder. Record the purpose and original paths. Ordinary, reviewable text edits may rely on version control or the user's existing backup policy unless the user requests a separate backup.

## Build

Compile from the project root and route auxiliary/output files to the project's configured directories. Run the full build at least twice after changes affecting the table of contents, labels, citations, or cross-references. A standalone chapter build may help isolate an error but does not replace the full build.

## Static and visual QA

Check:

- every intended source page is represented by a source-page comment;
- page comments are ordered within each chapter;
- `main.tex` includes every intended chapter and all include paths exist;
- no duplicate labels or broken references remain;
- LaTeX environments and braces are balanced;
- all figures exist, compile, and have unique labels and provenance entries;
- `% CHECK:` and low-confidence markers agree with `unresolved_points.md`;
- mathematical corrections agree with the verification and decision logs;
- title, author, date, bibliography, table of contents, and chapter order are correct;
- representative PDF pages have been visually inspected.

Run `python scripts/check_latex_project.py <project-root>` for a read-only structural report. Add `--expected-start` and `--expected-end` when continuous source-page coverage should be enforced. Then perform the mathematical and visual checks the script cannot automate.

## Delivery

Deliver the modular LaTeX source, compiled PDF, reconnaissance report, verification report, all registries and decision logs, unresolved-issues report, figure log, and checkpoint handoffs. State any build limitation or unresolved ambiguity honestly; do not call a partially verified chapter final.
