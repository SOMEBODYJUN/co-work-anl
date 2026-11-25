# Handwritten Math Notes to LaTeX

[English](#english) | [简体中文](#简体中文)

## English

A Codex skill for reconstructing handwritten or scanned mathematics as faithful, verified, publication-ready LaTeX.

This is not a plain OCR workflow. The skill preserves the source's mathematical order and intent, manages uncertainty explicitly, checks suspected errors against authoritative online sources, maintains notation across long manuscripts, and verifies the integrated LaTeX project before delivery.

## Features

- **Source-faithful reconstruction** — preserves definitions, examples, proof strategies, motivations, and intentional repetition.
- **Confidence-aware transcription** — distinguishes readable content, plausible reconstructions, and genuinely unresolved handwriting.
- **Mathematical verification** — checks hypotheses, signs, dimensions, domains, compactness, conventions, and coefficient systems.
- **Online typo research** — consults authoritative sources for suspected typos, missing hypotheses, named results, and specialized claims.
- **Long-manuscript continuity** — uses logical checkpoints plus persistent notation, terminology, label, figure, decision, and issue registries.
- **Figure handling** — chooses among source crops, attributed references, TikZ, Mathcha or other vector tools, and omission according to the project.
- **Integrated QA** — checks page provenance, includes, labels, environments, unresolved markers, compilation, and representative rendered pages.
- **Portable structural checker** — includes a read-only Python script with no third-party dependencies.

## Core Principle

The manuscript is the primary source. External material is evidence for verification, not a template for replacing the author's presentation.

The skill classifies discrepancies before editing:

1. typographical error;
2. missing standard hypothesis;
3. substantive mathematical discrepancy;
4. alternative or concealed convention.

Uncertain content stays uncertain until the source or reliable evidence resolves it.

## Requirements

- Codex or another compatible skill runner;
- access to the source PDF or page images;
- a LaTeX distribution for compilation;
- internet access when online verification is needed;
- Python 3 only if using the optional structural QA script.

The QA script uses only the Python standard library.

## Installation

### Project-scoped installation

Copy this directory into the project's skill folder:

```text
your-project/
└── .agents/
    └── skills/
        └── handwritten-math-notes-to-latex/
```

### Personal installation

Copy the directory into the Codex skills directory:

```text
$CODEX_HOME/skills/handwritten-math-notes-to-latex/
```

If `CODEX_HOME` is not configured, use the skill directory supported by your Codex installation.

## Usage

Invoke the skill explicitly:

```text
$handwritten-math-notes-to-latex
```

Example requests:

```text
Use $handwritten-math-notes-to-latex to convert this handwritten algebra manuscript into a modular English LaTeX project.
```

```text
Use $handwritten-math-notes-to-latex to continue pages 81–110, preserving the notation registry and existing chapter style.
```

```text
Use $handwritten-math-notes-to-latex to investigate the suspected sign error on page 27 using authoritative online sources, record the evidence, and update the LaTeX only if justified.
```

```text
Use $handwritten-math-notes-to-latex to run a final consistency and compilation audit without changing unresolved mathematical passages.
```

## Workflow

For a long source, the skill follows a cumulative workflow:

```text
Reconnaissance
    ↓
Logical checkpoint selection
    ↓
Transcription and reconstruction
    ↓
Mathematical and online verification
    ↓
Figure processing
    ↓
Cross-checkpoint integration
    ↓
Full-project compilation and QA
    ↓
Checkpoint handoff or final audit
```

Checkpoint size is configurable. Boundaries follow complete mathematical units rather than a fixed page count.

## Online Verification

Internet research is triggered when the manuscript and local context cannot reliably settle a suspected typo, omitted hypothesis, theorem version, citation, or specialized convention.

The skill prefers:

1. the cited original paper or an author-hosted version;
2. official journal, publisher, university, or author pages;
3. standard reference texts or authoritative lecture notes;
4. peer-reviewed papers that explicitly state or use the result.

Search snippets, forums, and informal posts may provide leads but are not sufficient evidence for substantive corrections. Every online-supported change should record the source, stable locator, relevant theorem or section, and the exact claim verified.

See [Online Verification of Mathematical Content](references/online-verification.md) for the full protocol.

## Structural QA

Run the included read-only checker from the skill directory:

```bash
python scripts/check_latex_project.py /path/to/latex-project
```

To enforce continuous source-page coverage:

```bash
python scripts/check_latex_project.py /path/to/latex-project \
  --expected-start 1 \
  --expected-end 250
```

The checker reports:

- source-page comments and expected gaps;
- duplicate labels;
- missing `\input` or `\include` targets;
- mismatched LaTeX environments;
- out-of-order page markers;
- `% CHECK:` and unresolved-content markers.

It does not replace LaTeX compilation, rendered-page inspection, or mathematical review.

## Skill Structure

```text
handwritten-math-notes-to-latex/
├── SKILL.md
├── README.md
├── LICENSE
├── agents/
│   └── openai.yaml
├── references/
│   ├── figures-and-provenance.md
│   ├── mathematical-verification.md
│   ├── online-verification.md
│   ├── qa-storage-and-delivery.md
│   ├── reconstruction-workflow.md
│   ├── requirements-summary.md
│   └── transcription-and-editing.md
└── scripts/
    └── check_latex_project.py
```

`SKILL.md` contains the routing and essential invariants. Detailed procedures are loaded from `references/` only when relevant to the current task.

## What This Skill Does Not Do

- It does not silently guess illegible mathematics.
- It does not replace the manuscript with a standard textbook treatment.
- It does not treat search-result snippets as mathematical verification.
- It does not guarantee that copied figures are suitable for public distribution.
- It does not silently collapse genuinely ambiguous or novel mathematics into a guess; the active project must record candidates, evidence, and independent checks in its autonomous recovery log.

## Privacy and Public Release

The reusable skill should not contain course titles, personal names, institutions, private paths, manuscript-specific notation, or unresolved issues from a private project. Keep those details in the active project, not in the skill package.

Before publishing a repository:

- scan the package for private names and absolute paths;
- verify that examples are synthetic or authorized;
- audit figure licenses and attribution;
- confirm that no source manuscript or derived private content is bundled;
- add an open-source license chosen by the maintainer.

## Contributing

Contributions should preserve source fidelity, make verification decisions more transparent, and keep project-specific information out of the reusable package. New scripts should be deterministic, read-only by default, dependency-light, and tested on a representative LaTeX project.

## License

Released under the [MIT License](LICENSE).

---

## 简体中文

一个用于将手写或扫描数学资料重建为忠实、经过核验、可用于正式发布的 LaTeX 文档的 Codex Skill。

这不是普通的 OCR 工作流。该 Skill 会保留原稿的数学顺序与意图，显式管理不确定内容，利用权威网络资料核查疑似错误，在长篇手稿中维护统一记号，并在交付前检查完整的 LaTeX 项目。

### 功能

- **忠实重建原稿**——保留定义、例子、证明思路、动机和原稿中有意保留的重复内容。
- **按置信度转录**——区分清晰内容、合理重建和确实无法辨认的手写内容。
- **数学核验**——检查假设、符号、维数、定义域与值域、紧致性、约定和系数环。
- **联网核对错误**——使用权威资料核查疑似 typo、遗漏假设、具名定理和专业性陈述。
- **长篇文稿一致性**——通过逻辑检查点以及记号、术语、标签、图形、编辑决定和疑点登记表保持全局一致。
- **图形处理**——根据项目需要选择原图裁剪、带来源的参考图、TikZ、Mathcha 或其他矢量工具，也可以省略不必要的图。
- **整体质量检查**——检查页码来源、章节引用、标签、LaTeX 环境、未解决标记、编译结果和代表性渲染页面。
- **跨平台结构检查器**——附带不依赖第三方库的只读 Python 脚本。

### 核心原则

原始手稿是首要来源。外部资料用于提供核验证据，而不是作为替换作者讲授方式的模板。

在修改前，该 Skill 会先区分问题类型：

1. 排版或抄写错误；
2. 遗漏的标准假设；
3. 实质性的数学矛盾；
4. 不同或未明确说明的约定。

在原稿或可靠证据解决疑点之前，不确定内容会继续保留为不确定状态。

### 运行要求

- Codex 或其他兼容的 Skill 运行环境；
- 能够读取源 PDF 或页面图片；
- 用于编译的 LaTeX 发行版；
- 在需要联网核验时具备网络访问能力；
- 仅在运行可选结构 QA 脚本时需要 Python 3。

QA 脚本只使用 Python 标准库。

### 安装

#### 项目级安装

将此目录复制到项目的 Skill 目录：

```text
your-project/
└── .agents/
    └── skills/
        └── handwritten-math-notes-to-latex/
```

#### 个人安装

将此目录复制到 Codex 的 Skill 目录：

```text
$CODEX_HOME/skills/handwritten-math-notes-to-latex/
```

如果没有配置 `CODEX_HOME`，请使用你的 Codex 安装环境所支持的 Skill 目录。

### 使用方法

显式调用该 Skill：

```text
$handwritten-math-notes-to-latex
```

示例请求：

```text
请使用 $handwritten-math-notes-to-latex，将这份手写代数讲义转换成模块化的中文 LaTeX 项目。
```

```text
请使用 $handwritten-math-notes-to-latex，继续处理第 81–110 页，并继承现有的记号登记表和章节风格。
```

```text
请使用 $handwritten-math-notes-to-latex，通过权威网络资料调查第 27 页疑似存在的符号错误，记录证据，并且只在证据充分时修改 LaTeX。
```

```text
请使用 $handwritten-math-notes-to-latex，完成最终的一致性和编译审计，不要擅自解决仍然存疑的数学内容。
```

### 工作流

对于长篇资料，该 Skill 使用累积式工作流：

```text
整体侦察
    ↓
选择自然的逻辑检查点
    ↓
转录与重建
    ↓
数学核验与联网核验
    ↓
图形处理
    ↓
跨检查点整合
    ↓
全项目编译与 QA
    ↓
检查点交接或最终审计
```

检查点大小可以配置。分界应跟随完整的数学单元，而不是机械地使用固定页数。

### 联网核验

当原稿和本地上下文无法可靠判断疑似 typo、遗漏假设、定理版本、引用或专业约定时，会启动网络检索。

资料优先级如下：

1. 被引用的原始论文或作者本人提供的版本；
2. 期刊、出版社、大学或作者的官方网站；
3. 标准参考书或权威课程讲义；
4. 明确陈述或使用该结果的同行评审论文。

搜索结果摘要、论坛和非正式帖子可以用来发现线索，但不能单独作为实质性修正的证据。每一项由网络资料支持的修改都应记录来源、稳定链接、相关定理或章节以及实际核验的内容。

完整流程见[数学内容联网核验](references/online-verification.md)。

### 结构 QA

在 Skill 目录中运行附带的只读检查器：

```bash
python scripts/check_latex_project.py /path/to/latex-project
```

如需强制检查连续的源页覆盖：

```bash
python scripts/check_latex_project.py /path/to/latex-project \
  --expected-start 1 \
  --expected-end 250
```

检查器会报告：

- 源页注释和预期范围内的缺页；
- 重复的 LaTeX 标签；
- 缺失的 `\input` 或 `\include` 文件；
- 不匹配的 LaTeX 环境；
- 顺序错误的页码标记；
- `% CHECK:` 和未解决内容标记。

它不能替代 LaTeX 编译、渲染页面检查和数学审阅。

### Skill 结构

```text
handwritten-math-notes-to-latex/
├── SKILL.md
├── README.md
├── LICENSE
├── agents/
│   └── openai.yaml
├── references/
│   ├── figures-and-provenance.md
│   ├── mathematical-verification.md
│   ├── online-verification.md
│   ├── qa-storage-and-delivery.md
│   ├── reconstruction-workflow.md
│   ├── requirements-summary.md
│   └── transcription-and-editing.md
└── scripts/
    └── check_latex_project.py
```

`SKILL.md` 保存路由规则和核心约束。只有在当前任务确实需要时，才会加载 `references/` 中的详细流程。

### 不包含的能力

- 不会静默猜测无法辨认的数学内容。
- 不会用标准教材的写法替换原稿。
- 不会把搜索结果摘要当作数学核验证据。
- 不会保证复制的图形天然适合公开发布。
- 不会把真正含糊或全新的数学内容压成无依据的单一答案；应在当前项目的自主恢复记录中保留候选、证据和独立检验。

### 隐私与公开发布

可复用 Skill 不应包含课程名称、个人姓名、机构、私人路径、某份手稿专用的记号或私人项目中的未解决问题。这些信息应保存在实际项目中，而不是 Skill 包内。

发布仓库前应：

- 扫描 Skill 包中的私人姓名和绝对路径；
- 确认示例是合成内容或已获授权；
- 审计图形的许可证和署名；
- 确认没有打包原始手稿或由私人资料衍生的内容；
- 添加由维护者选择的开源许可证。

### 贡献

贡献内容应维护原稿忠实性，使核验决策更加透明，并确保可复用 Skill 中不出现项目专用信息。新增脚本应尽量确定、默认只读、减少依赖，并在有代表性的 LaTeX 项目上进行测试。

### 许可证

本项目采用 [MIT License](LICENSE) 发布。
