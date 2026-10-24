# Second manuscript: venue and template review (round 2)

## Team decision

The manuscript's primary target is **SIAM Journal on Discrete Mathematics
(SIDMA)**. The earlier venue memo and the current review agree that the paper's
strongest identity is a discrete existence theorem: lexicographic load
selection, transfer budgets, atomic packing, and a finite continuation repair.
The result is not currently a polynomial-time search theorem, so SIDMA is a
better first target than an algorithms journal. ACM Transactions on Economics
and Computation remains a conditional fallback only after a stronger
algorithmic-game-theory framing and a separate submission-format conversion.

## Official scope and submission facts checked

- SIAM describes SIDMA as publishing work in combinatorics, discrete
  optimization and operations research, theoretical computer science, and
  related discrete mathematics. This manuscript fits the discrete
  optimization/game-theory boundary through its common-location restriction
  and factor-two existence theorem.
- SIAM's author instructions require an electronic manuscript and cover letter
  through the SIAM submission system; figures, if any, must be inline. The
  current paper has no figures.
- The instructions strongly encourage SIAM's standard LaTeX macros. They also
  require an abstract of at most 250 words, keywords and AMS subject
  classifications, and an abbreviated running title of at most 50 characters
  without abbreviations. The current abstract is below 250 words, but the
  source still needs the keyword/MSC block, author metadata, and a compliant
  running title before submission.
- The current SIAM macro distribution advertises the `siamart251216` class.
  The repository does not yet contain that publisher class, so the checked and
  reproducible reading PDF remains the `amsart` proof draft. The final source
  conversion must use the official SIAM macro bundle, then be rebuilt and
  visually inspected before upload.

## Required conversion checklist

1. Obtain the official SIAM macro bundle and use `siamart251216` (or the
   successor class supplied by SIAM at submission time).
2. Add the real author, affiliation, email, keywords, and AMS MSC codes; do
   not invent these fields.
3. Set a short running title of no more than 50 characters and keep the title
   specific to the factor-two common-location theorem.
4. Preserve the exact theorem scope, the distinction between finite exhaustive
   construction and polynomial-time search, and the one-reference SIAM
   bibliography style.
5. Submit the rebuilt PDF together with the cover letter; no submission is
   made in this workspace.

## Current judgement

The venue choice is closed at the recommendation level: **SIDMA / SIAM
standard LaTeX macros**. Publisher conversion is a submission-stage task,
blocked only by the unavailable author metadata and the need to fetch the
official macro bundle. This is a format blocker, not a mathematical defect.

## Sources checked

- SIAM SIDMA scope: <https://www.siam.org/publications/siam-journals/siam-journal-on-discrete-mathematics/>
- SIAM instructions for authors: <https://wwwarchive.z13.web.core.windows.net/journals/sidma/authors.php.html>
- Current SIAM class record: <https://epubs.siam.org/pb-assets/macros/standard/siamart251216.cls>
- SIAM documentation record: <https://epubs.siam.org/pb-assets/macros/standard/docsiamart.tex>
