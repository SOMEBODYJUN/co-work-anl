# Reconstruction Workflow

## 1. Establish scope before transcription

Inspect the manuscript coarsely and record:

- total pages and scan quality;
- topic, readability, and figure maps;
- recurring notation and likely conflicts;
- dense or verification-sensitive arguments;
- natural checkpoint boundaries.

Choose a checkpoint size appropriate to scan density, mathematical difficulty, and available context; twenty to fifty source pages is often practical for a long manuscript, but is not a requirement. Move every boundary to complete the surrounding definition, theorem, proof, construction, example sequence, or coherent topic.

## 2. Resume from persistent state

Before a new checkpoint, read the previous chapter and the project's registries:

- notation and terminology;
- style and theorem conventions;
- established mathematical dependencies;
- labels and cross-references;
- figures and provenance;
- editorial decisions;
- unresolved issues;
- prior checkpoint handoff.

Do not redefine established objects or silently change a locked convention. If later pages clarify an earlier ambiguity, update all affected locations and record the retrospective correction.

## 3. Run the complete checkpoint pipeline

For every checkpoint:

1. inspect source pages at usable resolution;
2. reconstruct the text and mathematics in source order;
3. verify mathematical claims and resolve or register ambiguities;
4. process only useful figures under the active figure policy;
5. integrate with previous chapters and registries;
6. compile the full project;
7. check continuity, references, and source coverage;
8. write the checkpoint handoff and freeze the completed scope.

A chapter-only compilation is a diagnostic, not final checkpoint acceptance.

## 4. Checkpoint handoff content

Record at minimum:

- exact source-page interval and any intentional shared boundary page;
- chapter file and topic summary;
- new or changed notation, terminology, dependencies, and labels;
- figures created, cropped, omitted, or deferred;
- mathematical corrections and consulted references;
- remaining `% CHECK:` items and unresolved passages;
- compilation and QA results;
- continuity guidance for the next checkpoint.

## 5. Final integration

After the final source page, perform a whole-manuscript audit. Check notation drift, duplicate or intentionally repeated material, definitions used before introduction, theorem hypotheses, chapter transitions, labels, figures, bibliography, and every unresolved issue. The checkpoint mechanism must not be visible as a discontinuity in the reader-facing notes.
