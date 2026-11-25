# RA07 adversarial blind checklist

This checklist was written before reading the RA07 reviewer conclusions. It defines the independent checks for the recovery and integration artifacts.

## Identity and provenance

- [ ] Assignment identifies one source PDF, expected 13 pages, and the SHA-256 is the same in assignment, manifest, and the actual `project/source.pdf`.
- [ ] Source PDF path/name and page range are consistent; no duplicate or substituted upload is silently used.
- [ ] Render metadata (DPI, page dimensions, grid geometry, overlap) is reproducible from the page and region assets.
- [ ] Every page image and every declared region exists and hashes to the manifest; page IDs and page numbers are monotone and complete.
- [ ] The final ledger points to the intended source, artifacts, mapping, observations, recoveries, issues, and final-round record rather than stale first-pass files.

## Coverage and geometry

- [ ] Each of the 13 pages has the expected six regions, with valid row/column order and in-bounds boxes.
- [ ] Region boxes cover the page with the stated overlap, and no declared source unit falls outside its page or its listed region(s).
- [ ] Source-unit IDs are unique and page-scoped; every unit has a transcription target, study target, evidence reference, and an explicit status.
- [ ] Transcription and study-note targets have one-to-one or explicitly documented many-to-one mappings; no orphan targets, duplicate IDs, or silent omissions.
- [ ] Crop evidence has a valid source page/bounding box and is sufficient to check the claim; evidence IDs resolve to real files.
- [ ] Unresolved or low-confidence units are visible in the ledger and recovery plan, with no claim of full resolution unsupported by evidence.

## Content fidelity and mathematics

- [ ] Transcription preserves symbols, quantifiers, subscripts/superscripts, set complements, inequalities, arrows, and Chinese labels from the page.
- [ ] Formula candidates are compared against source pixels and neighboring context; ambiguous glyphs are marked as candidates rather than asserted as facts.
- [ ] Definitions and theorem statements are mathematically well-typed (domains/codomains, measures, set operations, quantifier scopes, indexing ranges).
- [ ] Arithmetic/cardinality, measure-theoretic, and topology claims pass independent sanity checks; no notation drift between transcript, study notes, and ledger.
- [ ] Recovered annotations are separated from original writing and clearly attributed to evidence, not presented as source text.

## Draft and integration consistency

- [ ] Both candidate drafts contain the same resolved source content where they claim agreement, and differences are traceable to explicit issue IDs or editorial policy.
- [ ] Drafts cover all source pages/units and do not introduce unsupported examples, theorems, or corrections.
- [ ] The integrated ledger's statuses, mappings, issue dispositions, recovery entries, and final-round flags agree with the actual draft files.
- [ ] Final-round artifacts are complete, reproducible, and newer than the drafts they certify; no final pass points at a pre-revision output.
- [ ] Recovery plan entries identify owner/action/evidence and are either completed with proof or remain open; no closed item lacks closure evidence.

## Visual and handoff checks

- [ ] Full-page images and selected crops are readable at their stated resolution; important marks are not lost at region seams or margins.
- [ ] Cross-page continuations, split formulas, and page-edge notes are joined in logical reading order.
- [ ] Page/region checks identify every substantive issue and their coordinates; “clean” claims are not based solely on OCR or metadata.
- [ ] Hashes in manifests, ledgers, reports, and handoffs are internally consistent and generated from the files that are actually present.
- [ ] Handoff names the authoritative outputs and records remaining uncertainty, blockers, and the exact next audit action.

## Adversarial probes to run after the blind record

1. Recompute all listed SHA-256 values and compare across assignment, manifest, ledger, final rounds, and recovery outputs.
2. Parse every JSON artifact and resolve all relative paths from the project root; report missing, duplicated, or stale references.
3. Crosswalk source-unit IDs through mapping, transcript anchors, study-note anchors, observations, recoveries, and issues; look for gaps and many-to-one collisions.
4. Independently inspect the highest-risk formula/crop evidence (especially unresolved p0001 question and symbols flagged by recovery) against the rendered page/region images.
5. Compare both drafts line-by-line for dropped units, changed notation, unsupported claims, and inconsistent treatment of unresolved material.
6. Check final-round and audit timestamps/statuses against the bytes and hashes of the current artifacts; reject a pass whose inputs changed afterward.
7. Verify that visual/page/region checks cover all 13 pages and do not infer blankness or resolution from unreviewed regions.
