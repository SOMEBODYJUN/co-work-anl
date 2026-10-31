# Comparison notes — BibTeX reference checker

## Read boundary

The claimed source is the 997-line, 37262-byte `check_references.py`, read in full. It is the implementation named by the problem-driven literature-review skill and protocol. No external Crossref request was made during this source review; the online branch is documented as capability and limitation, not as fresh metadata evidence.

## Compared local materials

- `问题驱动文献综述S-R-L-H-G-M-C-V与引用证据边界--资料.md`: claim-first citation roles, metadata integrity, direct-competitor coverage, negative-claim hygiene.
- `创新框架候选、缺口与证据反证合同--资料.md`: source and falsifier boundaries.
- `TeX安全润色、符号保全与源到输出审计--资料.md`: protected title/TeX content and source-level boundaries.
- `Artifact验证层级、执行渲染与证据新鲜度--资料.md`: distinction between static/source checks and execution/render evidence.

## Unique increment retained

The script supplies a self-contained BibTeX parser, required-field matrix by entry type, duplicate key/DOI checks, year/DOI/URL normalization, title capitalization and protected-term detection, author/page/venue warnings, and optional DOI/title Crossref checks. It exposes a CLI with `--online`, `--title-search`, `--strict`, `--limit`, and protected-title-term options. It makes warnings vs errors and strict-mode exit semantics explicit.

## Disposition rationale

Integrate as a resource/verification tool description with exact source evidence. The checker can flag malformed or suspicious metadata; it cannot establish that a cited paper supports a mathematical claim, that direct competitors are complete, or that an external priority statement is true. Crossref results are time-dependent and network-dependent; any online run requires its own timestamp, request context, output, and source receipt.
