# Comparison notes — preservation checker tests

## Read boundary

The claimed source is `paper-polisher/tests/test_check_preservation.py`, read in full (1479 lines, 60524 bytes). It imports a sibling `scripts/check_preservation.py`; that implementation is a separate clean source and is not claimed by this receipt. The tests therefore document an expected contract and edge-case suite, not an independent proof that the implementation is sound.

## Compared local materials

- `TeX安全润色、符号保全与源到输出审计--资料.md` and `TeX安全润色与受保护内容验证边界--资料.md`: workflow modes and protected categories.
- `Artifact验证层级、执行渲染与证据新鲜度--资料.md`: text/source/execution/render separation.
- `论文论证重构与主张证据对齐--资料.md` and `数学写作反防御功能审计与证据量词边界--资料.md`: claim boundaries and protected negatives.
- `paper-polisher/SKILL.md` evidence: mode and output contract.

## Unique increment retained

The test source contributes concrete executable examples for math-region normalization, comment and opaque-command boundaries, numeric/unit/sign/marker protection, quantity heuristics that leave ordinary prose editable, TeX structure and environment options, table alignment, labels/references/citation families, literal and comment boundaries, approved symbol maps, bibliography display numbers, recursive project/import/subfile traversal, missing targets, fallback directory semantics, and dynamic-import fail-closed behavior. It also makes explicit that `--allow-additions` does not relax protected content and that approved symbol maps cannot alter text-mode names, keys, numbers, comments, or literals.

## Disposition rationale

Integrate as a resource/verification specification. Preserve the source verbatim and cite it as an expected test contract. Do not treat passing these tests as a mathematical theorem, a proof that all TeX dialects are covered, or evidence that a particular manuscript was executed or rendered. The implementation and its test environment must be checked separately; failures, missing optional dependencies, and untested macros remain open.
