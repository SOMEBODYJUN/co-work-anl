# Current factor-two article: source/PDF reading and new finite reconstruction

All ten canonical originals were fully read and preserved byte-for-byte.
`source-manifest.json` records their IDs, sizes, hashes, both complete frozen
commit/path routes and preservation paths. TeX/PDF/Bib are under
`archives/facility-games/subarchives/common-many/papers/factor-two-current/`;
the seven Markdown files are under `original/` with original paths.

Actual read-only PDF operations:

```sh
/usr/bin/pdfinfo archives/facility-games/subarchives/common-many/papers/factor-two-current/main.pdf
/usr/bin/pdftotext -layout archives/facility-games/subarchives/common-many/papers/factor-two-current/main.pdf tools/evidence/multiple-facilities-paper/pdf-text-layout.txt
/usr/bin/pdftoppm -r 100 -png archives/facility-games/subarchives/common-many/papers/factor-two-current/main.pdf /workspace/scratch/37f0f9248cfc/multiple-facilities-paper-render/page
```

The complete text of all eight pages was read, then all eight page renders
were visually inspected in two four-page contact sheets, preserved in visual/.
Pillow pasted the original rendered pages without scaling in a two-by-two
canvas with 28-pixel filename label rows. No clipping, formula spill, header
collision or orphan reference page was observed. This was not a new TeX/PDF
build. pdfinfo.txt preserves actual metadata, including blank Title/Author,
8 letter pages and 230216 bytes.

Actual final program run:

```sh
python tools/evidence/multiple-facilities-paper/verify_current.py
```

It completed exit 0 and generated current-verification.json. The program is a
new independent stdlib/Fraction curation reconstruction, not an imported old
author audit or proof-sanity tool. It verifies ten original hashes, 228 source
lines, nine formal blocks, seven proofs, 25 labels, 35 reference calls, two
citations, 15 displays, balanced environment counts and eight nonempty PDF
extractions identical to the preserved text. Formal blocks and PDF pages have
current fingerprints. Syntax scanning is not a full TeX parser/proof checker.

The exact finite construction covers 419 games and completes every labeled
layout: 3658 candidate site profiles, 1000 positive-reach actual deviations
(852 surviving-source/new-target, 64 surviving/occupied, 80 disappearing/
occupied, 4 disappearing/new), 1099 default layouts, 217 capped strict moves
and 216 default strict moves. It checks literal client costs, all four budgets,
atomic packing, full-game best responses, cap/heavy isolation, potential
differences, exact NE, mover bounds and labeled-continuation compatibility.
Twenty zero-reach instances use the direct all-zero branch. Maximum observed
ratio 12/7 is only this finite constructor's output statistic.

Additional checks include 197 scalar packing cases, a weight-(5,1,1) isolated
heavy-client repair with one strict step, and a globally unreachable weight-100
client in a two-site/two-facility game. The latter records the difference
between a literal all-I heavy-isolation premise and the sufficient per-facility
or served-client formulation. It is not a counterexample to the main theorem.
The final output contains 419 instance/selection records and one explicit
seed/terminal witness per move category, not an expanded transcript of all
1000 assertions. The code deterministically regenerates the full finite domain.

An initial 417-instance run had no disappearing-source/unoccupied-target case
because its exhaustive games had only two sites. Two explicit three-site
instances were then added; the final 419-case run asserts all four categories.
No broadening after the relevant branches passed. No historical arithmetic
audit, proof-note linter or earlier compiler execution is claimed as this run.

One public primary-source request to the IJCAI 2024 PDF returned isError with
no content. Prior literature and publisher-policy readings remain historical
attributions in the original reports. This batch did not verify current SIAM
rules, obtain a publisher class, create author metadata or submit anything.
General theorem quantifiers, true review scope, finite evidence and publication
status remain separate in the formal resource/review/computation objects.
