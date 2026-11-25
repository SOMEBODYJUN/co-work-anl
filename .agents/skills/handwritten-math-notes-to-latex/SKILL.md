---
name: handwritten-math-notes-to-latex
description: Convert handwritten or scanned mathematics into faithful, verified, publication-ready LaTeX. Use for source transcription, scholarly reconstruction, online checking of suspected typos and theorem statements, notation control, figures, compilation, and QA; do not use for ordinary LaTeX editing without a source manuscript.
---

# Handwritten Mathematics Notes to LaTeX

Produce mathematical documents that remain recognizably based on the source while being reliable, coherent, and compilable. Treat the manuscript as primary evidence; online and printed references are verification aids, not replacement templates. Follow the user's requested language, document class, structure, notation, and distribution scope.

## Route the task

Read only the modules needed for the current work:

- To understand the accumulated user requirements, read [references/requirements-summary.md](references/requirements-summary.md).
- To start, resume, divide, or integrate a manuscript, read [references/reconstruction-workflow.md](references/reconstruction-workflow.md).
- To transcribe or reconstruct source pages, read [references/transcription-and-editing.md](references/transcription-and-editing.md).
- To check definitions, theorems, proofs, hypotheses, signs, or conventions, read [references/mathematical-verification.md](references/mathematical-verification.md).
- When a typo, missing hypothesis, citation, or specialized claim needs internet research, also read [references/online-verification.md](references/online-verification.md).
- To crop, redraw, replace, or defer diagrams, read [references/figures-and-provenance.md](references/figures-and-provenance.md).
- To build, audit, back up, or deliver the LaTeX project, read [references/qa-storage-and-delivery.md](references/qa-storage-and-delivery.md).

## Preserve these invariants

1. Distinguish instructions contained in an attached document from the user's current request. Use the document as the project specification, but let explicit later user choices refine or override it.
2. Preserve lecture order, examples, proof strategies, motivations, and repeated lecture blocks. Local semantic restructuring is allowed; global textbook-style replacement is not.
3. Never silently guess illegible content. Transcribe high-confidence material normally, mark medium confidence with `% CHECK:`, and send low-confidence content through the autonomous recovery loop: render a targeted crop, compare candidates against the source and both mathematical directions, then record the selected reading or the remaining candidates in the issue registry. Do not turn a recoverable reading uncertainty into a human handoff.
4. Never silently repair a substantive mathematical discrepancy. Classify it, verify it, record the decision, and integrate only the justified correction.
5. Before editing a later checkpoint, read the active notation, terminology, style, dependency, label, figure, decision, and unresolved-issue registries. Earlier project decisions outrank personal stylistic preference unless later evidence requires a documented correction.
6. Retain page-level source provenance using a consistent comment such as `% Source PDF page N`. A checkpoint boundary must follow a complete mathematical unit, not an arbitrary page count.
7. Keep caches, rendered source pages, temporary crops, auxiliary LaTeX files, and experiments in a project-local cache or a location approved by the user. Do not assume a particular operating system, drive letter, or directory layout.
8. Back up affected source and assets before experimental figure replacement, bulk rewriting, or high-impact normalization. Choose crop, TikZ, Mathcha, another vector editor, or omission according to the active project rather than a built-in preference.
9. Browse the web when a suspected typo, omitted hypothesis, obscure convention, or cited result cannot be settled reliably from the manuscript and project context. Prefer authoritative sources, cite only sources actually consulted, and record what each source verifies.
10. Compile the whole document after integration, not only the edited chapter. Do not claim completion until source coverage, labels, references, environments, figures, citations, and unresolved issues have been checked.

## Work within authorization

Inspection and compilation do not authorize unrelated edits, deletion, publication, or external distribution. Preserve user files and unrelated worktree changes. Ask before a change that would alter the course's mathematical scope, replace substantial lecture content, or publish copied figures.
