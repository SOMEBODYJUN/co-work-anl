---
id: "unrelated-machines/check-references-script"
kind: resource
type_tag: "资源"
title: "BibTeX 引用元数据检查器解析、规则与 Crossref 边界"
status: "integrated-verification-resource"
truth_status: "static-reference-checker-not-citation-support"
review_level: "full-source-read-cross-archive-comparison"
scope: "BibTeX parsing, required metadata validation, title/author/venue hygiene, duplicate detection, and optional Crossref verification"
source_refs:
  - "clean:2cfb83687a887020e1f9:research/weighted_congestion_frontier/upstream/polish_skill/problem-driven-literature-review/scripts/check_references.py"
  - "local:archives/unrelated-machines/tools/evidence/check-references-script-20261031/original/check_references.py"
  - "local:archives/unrelated-machines/tools/evidence/check-references-script-20261031/comparisons/comparison-notes.md"
  - "local:archives/unrelated-machines/state/资料/问题驱动文献综述S-R-L-H-G-M-C-V与引用证据边界--资料.md"
  - "local:archives/unrelated-machines/state/资料/创新框架候选、缺口与证据反证合同--资料.md"
  - "local:archives/unrelated-machines/state/资料/TeX安全润色、符号保全与源到输出审计--资料.md"
  - "local:archives/unrelated-machines/state/资料/Artifact验证层级、执行渲染与证据新鲜度--资料.md"
source_identity:
  inventory_blob: "3765d1a7d2b7e45cacd3b6f65e3ccf6dead56afa"
  source_sha256: "728411eaf64ed7e7bb33953e6a98cd0f45435fbea994d7349d1bb7727aa11192"
  source_size_bytes: 37262
  source_line_count: 997
  frozen_commits:
    - "68fad804ec5946cb296f77dc5b336308a66abf12"
    - "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/check-references-script-20261031/original/check_references.py"
  - "archives/unrelated-machines/tools/evidence/check-references-script-20261031/comparisons/comparison-notes.md"
related_objects:
  - "archives/unrelated-machines/state/资料/问题驱动文献综述S-R-L-H-G-M-C-V与引用证据边界--资料.md"
  - "archives/unrelated-machines/state/资料/创新框架候选、缺口与证据反证合同--资料.md"
  - "archives/unrelated-machines/state/资料/TeX安全润色、符号保全与源到输出审计--资料.md"
  - "archives/unrelated-machines/state/资料/Artifact验证层级、执行渲染与证据新鲜度--资料.md"
---

# BibTeX 引用元数据检查器解析、规则与 Crossref 边界

## 来源身份与处置

本对象完整实读 clean source `2cfb83687a887020e1f9` 对应的上游 `problem-driven-literature-review/scripts/check_references.py`：997 行、37,262 字节，inventory blob 为 `3765d1a7d2b7e45cacd3b6f65e3ccf6dead56afa`，SHA-256 为 `728411eaf64ed7e7bb33953e6a98cd0f45435fbea994d7349d1bb7727aa11192`。原字节保存在 [check_references.py 原文证据](../../tools/evidence/check-references-script-20261031/original/check_references.py)，比较记录在 [comparison-notes.md](../../tools/evidence/check-references-script-20261031/comparisons/comparison-notes.md)。冻结索引记录 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`。

处置为 `integrated` 资源。脚本检查 BibTeX 结构和元数据卫生，能为引用流程提供可重复的静态警报；它不能证明某文献支持某一数学句子、直接竞争者覆盖完整、负面优先权断言成立，也不能把 Crossref 返回自动变成原始论文证据。未在本次清洗中发起 Crossref 网络请求，也未把任何在线结果登记为新鲜证据。

## 数据模型与解析器

脚本定义不可变 `Field`、`Entry`、`Issue` 数据类。`Field` 保留字段名、原始值、去包装后的值和行号；`Entry` 保留 entry type、key、字段字典和起始行；`Issue` 记录 `ERROR`/`WARN`、代码、key、行号、消息和可选 hint。`BibTeXParseError` 带索引，使未闭合分隔符能映射回源行。

解析器不是简单按逗号切字符串。`find_matching_delimiter` 处理 `{}` 或 `()` 嵌套和引号/转义；`split_top_level_once` 只在顶层切开 key 与 fields；`parse_value` 支持 brace、quoted、裸值和 `#` 拼接；`plain_text` 去除 TeX 包装以便比较，但字段同时保留 raw 供保护和格式诊断。`@comment`、`@preamble`、`@string` 被跳过，其他 entry 按 entry type、key 和字段解析；缺 key、缺等号、未闭合值和缺 entry body 会产生 parse issue 而不静默吞掉。

这种解析保留了行号和原始包装，适合在引用稿件中定位问题；但它仍是一个有限 BibTeX 方言解析器，不能保证所有 biblatex 宏、非标准 bst/bbx、复杂宏展开或编译器特有语义都被理解。解析 PASS 只表示该输入通过当前 parser/validator 的规则，不表示 LaTeX 编译或目标期刊样式一定接受。

## entry type 与必填字段

`KNOWN_ENTRY_TYPES` 覆盖常见 article、book、inproceedings、conference、incollection、inbook、phdthesis、mastersthesis、techreport、manual、proceedings、unpublished、online、misc 等；未知类型发 `unknown-type` 警告并给出使用标准类型或确认目标 bst/bbx 的提示。`REQUIRED_FIELDS` 以“至少一个字段组”为单位：article 要 author/title/journal/year-or-date，book 允许 author 或 editor 并要 publisher，inproceedings/conference 要 booktitle，学位论文要 school，online 要 url-or-doi 和 year/date/urldate 之一，manual/proceedings/unpublished/misc 也有各自最低集合。

每个字段都检查空值和 HTML entity；后者是 warning，提示把 `&amp;` 等数据库导出残留换成普通文本或 LaTeX-safe 字符。重复 key 是 error；归一化 DOI 重复也是 error。通过这些规则后，引用集合至少在结构上可被后续 BibTeX 工具消费，但没有验证字段是否真实对应目标论文。

## 标题、作者、页码与 venue 卫生

标题检查有三层：

1. 检查 Google Scholar 风格 `[J]`、`[C]` 等 source-type marker；
2. 识别未用大括号保护的大写 acronym、混合大小写词和 proper-noun-like token；
3. 对默认 `Monte Carlo`、`Reliable-loc` 以及 CLI 追加的 protected terms 检查是否在 brace 范围内。

`unprotected_*` 函数识别单层 brace 包装、嵌套保护范围和 Roman numeral 例外；它不声称能判断所有期刊大小写规则，只给“可能需要保护”的 warning。CLI 可从 UTF-8 文件逐行读取额外 term，也可重复传 `--protected-title-term`，再去重。

作者检查 `et al.`、分号/`&` 分隔、格式化逗号列表，提醒使用 BibTeX 的 `and` 语法并让 bibliography style 负责缩写。页码检查单个 hyphen 而非 `--`。年份从 year/date 中提取四位数字，缺失格式是 error，1800 以前或当前年加一年以后是 suspicious-year warning。DOI 归一化支持 `doi:`、doi.org、ACM DOI URL、URL 编码和尾部标点；裸 DOI 以外的存储形式发 `doi-format` warning，URL 中藏 DOI 但缺 DOI 字段发 `doi-in-url` warning，明显非 http(s) URL 发 `bad-url` warning。

venue 规则把会议样式词和 `journal` 放在 article 中标记为 `conference-as-article`，把 proceedings 中的 journal 标成 `journal-in-proceedings`，把 article 中的 booktitle 标成 `booktitle-in-article`。这些是核对提示而非自动重分类，因为目标出版商和样式可能有正当例外。

## 规则输出与退出码

CLI 读取 BibTeX、TeX 或含 BibTeX entry 的文本文件，默认打印最多 80 条 issue。输出先给 `Reference metadata check: PASS | PASS_WITH_WARNINGS | FAIL`，并报告 entry 数、error 数和 warning 数；随后按 severity、行号、key、code 稳定排序，打印位置和 hint，超出 limit 的部分只计数不展开。

默认模式仅 ERROR 导致非零退出；warning 仍显示但状态为 `PASS_WITH_WARNINGS`。`--strict` 把 warning 也变成失败条件，适合把元数据门槛设为发布阻断。`--online` 启动 Crossref DOI 校验；`--title-search` 只在 `--online` 且无 DOI 时按标题取一个候选。`--mailto` 和 `--timeout` 控制请求身份和超时，`--limit` 控制显示量。输入文件或 protected-term 文件读取失败返回 2；静态检查 error 或 strict warning 返回 1。

## Crossref 在线分支的精确边界

有 DOI 时，脚本请求 `https://api.crossref.org/works/{doi}`，比较标题相似度（低于 0.82 为 `crossref-title` error）、年份（不同为 warning）、第一作者姓氏（不同为 warning）和 venue（相似度低于 0.55 为 warning）。HTTP DOI 解析失败是 error；URL、超时或 JSON 失败是 warning 并继续其他条目。无 DOI 且启用 title search 时，请求 Crossref `query.title` 取一条候选；相似度至少 0.90 且有 DOI 才提示 `missing-doi`，仍要求人工确认。

Crossref 校验是元数据一致性检查，不是内容支持核验。标题相似度阈值、出版年份字段优先级、作者/venue 归一化都可能产生合法版本差异或误报；网络结果有时间性、限流和可用性边界。任何实际运行必须保存脚本版本、日期、请求参数、返回摘要和失败/跳过原因，不能只写“online passed”。当前清洗没有执行这一路径。

## 与问题驱动综述和证据分层的关系

与问题驱动文献综述资料相比，本脚本实现的是引用元数据 integrity gate，是 claim-first reference selection 的工具环节；它不做 direct-competitor coverage、negative-claim hygiene、S-R-L-H-G-M-C-V 结构或 reference role 判断。综述仍需人工确认“这条文献真的覆盖该句”，不能把 parser PASS 当作 citation support。

与 TeX 安全润色资料相比，脚本只处理 BibTeX/文本元数据，不保护稿件中的数学公式、label、数字或 literal；与 Artifact 验证资料相比，它属于静态/source-bound 检查，不能替代 execution/render/freshness。与创新 framing、反防御审计和论证重构相比，它不决定候选 gap、句子功能、贡献范围或数学量词。它也不对 unrelated-machines 的定理、算法、hardness、反例或优先权作任何判断。

## 使用协议、失败处置与缺口

推荐在稿件引用进入正式审查前运行：先无 `--online` 检查结构，再在网络和身份可用时用 `--online --mailto ...` 验 DOI，最后按需要用 `--strict` 阻断 warning。脚本输出应与 BibTeX 源、目标期刊样式和人工核对记录一起归档。若有 unknown type、Crossref 404、title mismatch、缺 metadata 或 DOI 候选，保留 issue 并回到原始出版社/DOI/DBLP/arXiv 等来源，不以“脚本给出 PASS”覆盖问题。

该脚本没有测试源中对所有 biblatex 方言、宏展开、Unicode/非拉丁作者名、版本关系、撤稿状态、引用语义、全文内容或优先权事实的验证；没有运行检索覆盖率、直接竞争者完整性或 claim-to-source 对齐。清洗完成只表示静态 checker 的规则和边界已准确入档；真正的文献事实和数学主张仍需来源级 evidence、比较和适当验证。
