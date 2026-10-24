# Editorial and anti-AIGC review (round 2)

## Scope

This is the final owner-side editorial gate after the prior humanizer and
academic-humanizer pass recorded in `REVISION-NOTES.md`. It reads the current
`main.tex` from the beginning as a mathematical reader, checks the abstract,
Introduction, section transitions, theorem statements, and proof prose, and
compares the round-2 proof audit for terminology drift. The isolated proof
reviewer independently checked the same proof transitions; no prose edit is
accepted unless it preserves the mathematical diff.

## Must fix

None. The current text states the exact client-equilibrium and continuation
quantifiers, distinguishes covered from unserved clients, separates finite
exhaustive construction from polynomial search, and gives the heavy-singleton
exception in the same terms in the lemma and both deviation cases.

## Suggestions considered and rejected

- No paragraph was shortened merely to save space: the source-disappearance
  case, packing argument, and potential calculation each carry a proof duty.
- No synonym cycling was introduced. “Facility,” “client,” “location,”
  “load,” and “continuation” remain stable technical terms.
- No promotional, vague, or chatbot phrasing remains in the abstract or
  Introduction. The result is stated with its common-location restriction and
  its lack of a polynomial search claim.

## Accepted round-2 clarity edits

The three independent S4 findings were adopted in the source:

1. the old target load comparison is displayed before the lexicographic
   contradiction;
2. a fixed total order resolves ties in the finite lexicographic maximum; and
3. the certificate explicitly calls the unlisted-layout continuation a
   succinct default-rule program rather than an expanded table.

The final `\enlargethispage` line is a layout-only change that keeps the single
reference entry on the last page; it does not alter the text or mathematics.

## Verdict

**Pass for language and proof presentation.** No further cleaning has a clear
value-to-risk advantage. The remaining publisher work is template conversion,
author metadata, keywords, and MSC codes, not prose repair.

## Verification

- `tex-proof-sanity.py`: passed with zero hard failures.
- Final build log: no LaTeX errors, undefined references/citations, overfull
  boxes, or underfull boxes.
- PDF render: all eight pages checked; no clipping, overflow, or orphaned
  reference page remains.
