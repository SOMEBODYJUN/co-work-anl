# Manuscript build/conversion interface evidence

Six canonical originals are preserved byte-for-byte under `original/` with
their complete original paths. `source-manifest.json` records all six IDs,
both frozen source commit/path routes, sizes, hashes and preservation paths.
The two original programs were fully read before execution. They were not
edited or run against the shared repository's live output files.

The new `replay_interfaces.py` copies unchanged programs to isolated canonical
`repository/research/manuscripts/` trees, since their source lookup depends on
`__file__`. It uses explicitly controlled command fixtures for `kpsewhich`,
`pdftex` and `latexmk`. Build output files are marker bytes saying NOT A PDF,
not generated documents. The four conversion template files are marked
NON-OFFICIAL COPY FIXTURE, not official classes or a real INFORMS logo. All of
these fixtures and generated MOR TeX stay in the external work directory.

The converter's mathematical input is the already preserved actual current
structural article TeX/Bib under
`archives/weighted-congestion/papers/structural-methods-current/`. Their hashes
are 5691d1b60f77794f016d1db5d307cd643c8cb91f5c02a8db4aec09b9c7f43c17
and dfdb646827092fba59647cc40bfd6c779a226ce4a9c61fa8ae772f5bd3e06a73.
No official/private 32-page PDF or production class was obtained or inspected.
No real TeX compiler, PDF authoring, template installation or journal upload
was performed in this batch. The previously read 27-page PDF was not recompiled.

Actual final command (Python 3.12.14):

```sh
python tools/evidence/manuscript-build/replay_interfaces.py \
  --cache tools/evidence/manuscript-build/original \
  --repo /workspace/scratch/37f0f9248cfc/boss4-research \
  --work /workspace/scratch/37f0f9248cfc/boss4-next-cache/manuscript-build-run-003 \
  --evidence tools/evidence/manuscript-build
```

This command was executed with absolute paths during the session and completed
exit 0. The work directory must not already exist. For another run, choose a
fresh external directory. When the cache lacks the transient assignment file,
the script loads the adjacent source manifest; therefore the six preserved
originals and current preserved article are sufficient replay inputs.

`interface-replay.json` is the actual generated report: 12 build control-flow
cases and 5 conversion cases, including original-program failures. It preserves
stdout/stderr, return codes, copy/no-copy results and mathematical comparisons.
The build's default empty argument list actually exits 2 due to the argparse
list/default/choices interaction. Explicit three-key invocation works against
the fixtures. Warning/Overfull/undefined and compiler/missing-log failures do
not copy the current target PDF; Underfull is allowed; a later failure in a
batch does not roll back an earlier copied paper.

Actual conversion of the current source produces main.tex SHA-256
0729d63bd9fb0e7f5d47c02f0a41461b5c983da37f2e0a7493941aba5ec2e422,
matching the historical privately delivered TeX hash. This establishes text
reproduction, not provenance/compilability of a template or a private PDF.
24 statements are byte-identical, 24 proof bodies agree after heading/Halmos
and whitespace normalization, label order is preserved, and all 119 displayed
math blocks agree after the documented one-block alignment change. Bib bytes
are unchanged. Root/inside-root output is refused. Missing template file
leaves a partially copied output. A deliberately missing appendix marker is
not rejected and yields unbalanced APPENDICES, recording the converter's
specific-input scope rather than certifying arbitrary TeX.

The first external run validated the same control flow. A second kept generated
source outside the evidence directory. A final portability change removed the
dependency on transient orchestration metadata; run-003 executed the delivered
harness using only preserved originals. None of these runs invoked real TeX.
No failure was converted into a mathematical counterexample or PASS claim.

`source-link-audit.json` resolves the four Markdown files' 26 local links against
inventory: 24 match, while the two old venue links to structural TeX/PDF go up
one directory too far. Correct canonical paths and target IDs are recorded,
without modifying the original source or treating navigation as proof review.

All venue policy, named reviewers' actions and external paper/skill readings in
the original Markdown remain historical attributions. This batch did not
revalidate current publisher rules, fetch third-party skill repositories or
complete any missing mathematical/editorial review.
