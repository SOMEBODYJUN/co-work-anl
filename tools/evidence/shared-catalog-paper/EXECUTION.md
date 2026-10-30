# Shared-catalog paper: actual reads and independent exact modules

Seven canonical originals were fully read and preserved byte-for-byte.
source-manifest.json records their IDs, sizes, both complete frozen commit/path
routes, hashes and preservation paths. Current TeX/PDF/Bib are in
archives/facility-games/papers/shared-catalog-golden-ratio/; four original
Markdown records are under original/ with their complete original paths.

Actual read-only PDF operations used system Poppler:

```sh
/usr/bin/pdfinfo archives/facility-games/papers/shared-catalog-golden-ratio/main.pdf
/usr/bin/pdftotext -layout archives/facility-games/papers/shared-catalog-golden-ratio/main.pdf tools/evidence/shared-catalog-paper/pdf-text-layout.txt
/usr/bin/pdftoppm -r 90 -png archives/facility-games/papers/shared-catalog-golden-ratio/main.pdf /workspace/scratch/37f0f9248cfc/shared-catalog-paper-render/page
```

All 1132 newline-terminated extracted text lines, from the abstract through three references,
were actually read. All 26 page renders were actually inspected in seven
contact sheets in visual/. Pillow pasted unscaled pages into a two-by-two
canvas with 28-pixel filename rows. No body clipping or formula spill was
observed. Page26 contains only continuation bibliography lines; it is a real
reference-only tail page, not an absent page. Two empty slots in the last
contact sheet are only canvas layout. No PDF was recompiled or edited.

The unchanged first full finite script was executed from the external cache:

```sh
python /workspace/scratch/37f0f9248cfc/boss4-next-cache/shared-catalog-math-run/audit_math.py
```

It completed exit 0. Its exact executed bytes are preserved as
audit_math.initial-executed.py, SHA-256
44331bc02f7f40f7ef90d36c92d9b84a3ada4a6a009975be30a1c608cbfb042a.
The initial output is preserved as math-audit-initial.json. The numerical
domains passed: 3529 box slices (maximum observed four moves, 1330 pivot
changes), 1089 local P/E/T menus, 13995 pure-repair seeds, 143 finite C calls
across local/catalog modules, 320 finite catalogs with 2560 ordered layouts,
and 320 cycles for the selected minimum-index response maps.

Menu C in these checks is supplied by independent exponential support
enumeration. It is not the manuscript's claimed polynomial constructor.
Finite catalog success is not a proof of arbitrary cycles/tie maps or the
universal phi theorem. The largest-client/strong-chord polynomial constructor
and general cycle-transport targeted review remain uncompleted historical
obligations. The three-mixer example's exact support classification and the
box-slice local-versus-global example are separate self-contained objects.

One explanatory, unused metadata field in the initial report mistakenly
identified the E half-load 1/2 with the one-location finite-menu d value.
The full catalog loops always computed d from actual menus and did not use
that field. On reviewing the source referee's 'E only member' sentence, the
P pure endpoints were checked directly: p=0 and p=1 are exact one-client NE,
so the nonnegative finite-menu minimum is d=0. E still fails the strong qR
quota, while satisfying the actual qd=0 threshold.

Only that explanatory example was rechecked, without repeating passed finite
domains. The corrected script was executed in the external cache with:

```sh
python /workspace/scratch/37f0f9248cfc/boss4-next-cache/shared-catalog-math-run/audit_math.py --correct-colocation-only
```

It completed exit 0, preserving the initial report and writing math-audit.json
with the old value, corrected value, reason and three checked P/E profiles.
The corrected script is audit_math.py, SHA-256
7caf30785e83556069e0dd6cf6b97a9f88dc73f33c87438ceb0830ebeeb3de2c.
Its default full-run code has the corrected explanatory value; the optional
flag exists to document/reproduce this narrow correction of the initial run.
Neither a source failure nor a universal theorem was inferred from this error.

verify_assets.py was separately executed and produced asset-verification.json.
It verifies seven hashes/417987 bytes, 1125 TeX lines, eight formal blocks,
five proof environments, 76 labels, 117 reference calls, seven citations,
33 equation plus 69 bracket displays, correctly nested environments and 26
nonempty PDF extractions matching the preserved text. It records current
fingerprints, full-read/visual scope and the reference-only last page. This is
a limited syntax/current-byte check, not a proof checker or historical diff.

All mathematical finite tests use stdlib Fraction and exact a+bq signs via
q*q+q=1, no floating-point thresholds or randomized probability grid. No old
author program was imported or relabeled as a new run. No previous eight-page
factor-two PDF or its 419-game audit was repeated. No third-party skill clone,
official publisher class, author metadata or journal submission was created.
Historical external readings and novelty/venue claims retain their own scope;
the current repaired global manuscript remains targeted-review pending.

Extraction metric clarification: the saved text has 1132 newline terminators and 26 form-feed page terminators. Python splitlines counts both kinds, yielding 1158 records in asset-verification.json; these are two counts of the same fully read bytes. This final check only counted preserved text and compared existing reports; it did not repeat PDF rendering or finite mathematics.
