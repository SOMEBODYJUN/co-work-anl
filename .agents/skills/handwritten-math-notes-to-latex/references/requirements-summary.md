# Requirements Summary

## Intended result

Convert handwritten or scanned mathematics into a professional LaTeX document in the user's requested language and format. The result should be:

- faithful to the lecturer's order, emphases, examples, and proof strategies;
- mathematically checked rather than merely OCR'd;
- coherent across the full source, whether it is a short note or a multi-chapter manuscript;
- modular, readable, and fully compilable;
- supported by persistent editorial records.

The source manuscript is authoritative evidence but may contain shorthand, omissions, handwriting ambiguity, inconsistent notation, and genuine mistakes. External references may verify or reconstruct specific points, but must not turn the notes into a substitute textbook.

## Functional requirements

### Source reconstruction

- Inspect the actual page image at adequate resolution.
- Preserve one traceable source-page comment for every covered PDF page.
- Turn rough blackboard prose into semantic LaTeX environments without changing the lecture's mathematical progression.
- Preserve lecturer-specific motivation and informal geometric insight.
- Distinguish complete proofs, routine omitted steps, and genuinely incomplete arguments.

### Mathematical reliability and research

- Check hypotheses, dimensions, domains and codomains, signs, boundary and orientation conventions, compactness, regularity, coefficients, and theorem applicability.
- Classify corrections as typographical, missing-hypothesis, substantive-discrepancy, or alternative-convention cases.
- Use internet research when a suspected typo, omitted hypothesis, theorem version, citation, or specialized convention cannot be settled locally.
- Prefer primary or authoritative sources and record what was corrected, why, and which source supports it. Never cite a reference that was not actually consulted.

### Global consistency

- For long sources, work in configurable checkpoints sized to the manuscript and available context, extending each boundary to finish a theorem, proof, construction, or topic.
- Maintain notation, terminology, style, dependency, label, figure, editorial-decision, and unresolved-issue registries.
- Carry all locks and unresolved questions forward. Later evidence may trigger documented retrospective repairs.

### Figures

- Retain only mathematically useful visuals.
- Choose among a legible source crop, an attributed external figure, TikZ/tikz-cd, Mathcha-assisted vector output, or omission.
- Track provenance and verify arrow directions, dimensions, orientations, labels, and conventions.
- Follow the user's chosen figure policy and back up affected files before experimental replacement.

### Build and storage

- Keep project cache and temporary products in a project-local or user-approved location.
- Compile the integrated document at every completed checkpoint and run twice after structural or reference changes.
- Audit source-page coverage, duplicate labels, missing includes, environment balance, unresolved markers, references, and visual layout before delivery.

## Project configuration

Do not embed course titles, people, institutions, absolute paths, drive letters, chapter names, subject-specific notation, or private unresolved issues in the reusable skill. Read those details from the active request, attached project specification, or project-local configuration. Explicit user instructions given later override earlier project defaults.
