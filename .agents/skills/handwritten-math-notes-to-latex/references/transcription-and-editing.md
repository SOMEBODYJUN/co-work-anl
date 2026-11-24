# Transcription and Scholarly Editing

## Source fidelity

Preserve the lecturer's progression and local strategy. Do not transcribe line by line when the page is clearly blackboard shorthand; organize nearby material into appropriate definitions, notation, remarks, examples, propositions, theorems, proofs, proof sketches, exercises, or geometric-intuition paragraphs.

Do not merge repeated lecture units merely because a textbook would present them once. Use cross-references and a short transition when later pages revisit earlier material.

## Confidence handling

- **High confidence:** write cleanly in the chapter.
- **Medium confidence:** use the best contextual reconstruction and add a nearby `% CHECK:` comment with the source page and uncertainty.
- **Low confidence:** do not guess. Retain a conspicuous working marker and add the item to the project's unresolved-issues record.

Coloured annotations of uncertain authorship remain source annotations; do not automatically treat them as lecturer corrections.

## Proof reconstruction

- If the proof is complete, polish it without replacing its argument.
- If the proof has the right idea but omits routine steps, add only enough detail to make the reasoning readable.
- If the proof is incomplete or appears wrong, preserve the intended strategy, verify the issue, and label a reconstructed argument or proof outline honestly. Do not claim imported material appeared in the lecture.

## LaTeX form

- Use semantic theorem environments and the project's existing macros.
- Prefer `\[...\]`, `equation`, `align`, `gather`, or `cases` according to mathematical structure.
- Label only objects referenced later; prefer stable semantic labels such as `type:short-description` unless the project uses another convention.
- Use `\cref` only when the active project provides it and has chosen that convention.
- Keep `% Source PDF page N` comments ascending and close to the corresponding content.
- Avoid reader-facing checkpoint terminology.

## Editorial additions

Add only material that directly clarifies the source and can be verified. Keep the lecturer's motivation, examples, and unusual but correct conventions. Record substantial additions or normalizations in the editorial decision or verification report.
