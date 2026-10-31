---
id: "unrelated-machines/tex-safe-polishing-zh-reference"
kind: resource
type_tag: "资料"
title: "中文 TeX 安全润色、结构键与一致性审计指南"
status: "integrated-zh-tex-preservation-resource"
summary: "中文 TeX-Safe companion 把 paper-polisher 的 source-to-output 保全、结构 key、术语/记号/数值 ledger、全文覆盖门槛、五种模式和 preservation checker 解释成中文流程，并以 examples 固定不能猜修数字、引用、资产和数学边界。"
truth_status: "workflow-reference-not-mathematical-evidence"
review_level: "full-source-read-cross-language-and-evidence-comparison"
scope: "Chinese-facing TeX-safe polishing, preservation, terminology/notation/numerical consistency and checker workflow"
source_refs:
  - "clean:eeea779c1adaeba50eb9:research/weighted_congestion_frontier/upstream/polish_skill/paper-polisher/references/tex_safe_polishing_zh.md"
  - "local:archives/unrelated-machines/state/资料/TeX安全润色、符号保全与源到输出审计--资料.md"
  - "local:archives/unrelated-machines/tools/evidence/tex-safe-polishing-zh-20261031/comparisons/comparison-notes.md"
  - "local:archives/unrelated-machines/state/资料/Artifact验证层级、执行渲染与证据新鲜度--资料.md"
  - "local:archives/unrelated-machines/state/资料/论文论证重构的主线、证据对齐与结构边界--资料.md"
  - "local:archives/unrelated-machines/state/资料/数学写作反防御功能审计与证据量词边界--资料.md"
  - "local:archives/unrelated-machines/tools/evidence/genre-profiles-20261031/comparisons/comparison-notes.md"
  - "local:archives/weighted-congestion/tools/evidence/linear-article-assets/self-check.json"
source_identity:
  inventory_blob: "1ed0763b4ebdb651a98f9f0c630b21529092fe14"
  source_sha256: "615388149cd14b9d464044eb97cea64017f847a18d3f92c6454f0a6edb7b0f1c"
  source_size_bytes: 19517
  frozen_commits:
    - "68fad804ec5946cb296f77dc5b336308a66abf12"
    - "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/tex-safe-polishing-zh-20261031/original/tex_safe_polishing_zh.md"
  - "archives/unrelated-machines/tools/evidence/tex-safe-polishing-zh-20261031/comparisons/comparison-notes.md"
related_objects:
  - "archives/unrelated-machines/state/资料/TeX安全润色、符号保全与源到输出审计--资料.md"
  - "archives/unrelated-machines/state/资料/Artifact验证层级、执行渲染与证据新鲜度--资料.md"
  - "archives/unrelated-machines/state/资料/论文论证重构的主线、证据对齐与结构边界--资料.md"
  - "archives/unrelated-machines/state/资料/数学写作反防御功能审计与证据量词边界--资料.md"
---

# 中文 TeX 安全润色、结构键与一致性审计指南

## 来源身份与处置

本对象完整实读上游 `research/weighted_congestion_frontier/upstream/polish_skill/paper-polisher/references/tex_safe_polishing_zh.md` 的 19,517 字节、374 行。clean source ID 为 `eeea779c1adaeba50eb9`，inventory blob 为 `1ed0763b4ebdb651a98f9f0c630b21529092fe14`，原文 SHA-256 为 `615388149cd14b9d464044eb97cea64017f847a18d3f92c6454f0a6edb7b0f1c`；冻结索引同时列出 `legacy-cleanup` 和 `main`。原字节保存在 [tex_safe_polishing_zh.md 原文证据](../../tools/evidence/tex-safe-polishing-zh-20261031/original/tex_safe_polishing_zh.md)，逐项比较写入 [比较记录](../../tools/evidence/tex-safe-polishing-zh-20261031/comparisons/comparison-notes.md)。

处置为 `integrated` 资料资源。它是 English paper-polisher SKILL 的中文 companion，增加的是中文说明、示例、步骤和 author-facing 解释，而不是新的 TeX 权限、数学事实或外部新颖性结论。英文 SKILL 的模式和 protected source 规则优先；中文 companion 不能用翻译自由度放宽数值、结构 key、公式、引用、单位、sign、asset 或技术含义的保全。

## 核心目标：四个问题分开回答

指南要求在不改变技术事实的前提下，把中文或英文 TeX 文稿处理为正式、客观、克制的工程期刊英文，并把四个检查问题分开：

1. candidate 是否保留 original 的受保护内容；
2. original 内部术语是否一致；
3. original 内部数学记号是否一致；
4. 同一数值事实、单位和正负号是否在各处一致。

source-to-output preservation 通过不代表 source 内部语义一致；source 内部不一致也不授权自动修稿。这一分层与当前 cleanup 的 `read_note`/`comparison_note`/`decision_note` 纪律一致：文件哈希、结构检查、数学阅读和执行/渲染验证属于不同证据层。

## 原稿到输出稿的逐字节保全

以下内容在润色、翻译、普通正文新增、检验、一致性审计和记号统一中都必须原样保留：

- `$...$`、`\\(...)`、`\\[...]` 及命名数学环境中的全部公式；
- figure、table、algorithm、theorem、proof、lemma、definition、remark 环境；
- label、reference、citation、BibTeX key、图片路径等结构命令及参数；
- comment、verbatim、listing、inline literal 和 code-like 源码，包括注释是行内还是整行以及它们相对于数学/TeX 结构的顺序；
- 变量与函数记号，除非作者确认了精确 symbol mapping；
- 所有数值、数值 token 顺序、单位、百分比、维度、样本量、参数、表格值、图中数值、显著性标记以及正号、负号和 `\\pm`；
- 技术含义、条件、假设、算法、证明步骤、实验、baseline、数据集、指标和结果。

数字硬保护覆盖 identifier、注释、literal 示例、URL 和受保护 command 参数中的数字。任何为改善语序而新增、删除、修改或调换数字都是禁止的。可疑数字、单位、正负号、引用或作者姓名顺序只报告，要求作者在 paper-polisher 之外修改后提供新 baseline，不能依据表格趋势、单位换算或预期结果猜修。

保全检查器也把可识别 comment/literal/code 区域当作 exact source：不能把正文变成 comment、把文字移进/移出 literal、把行内 `%` 变成整行注释，或让这些区域跨过公式/TeX 结构。自定义或未识别 literal macro 仍须人工对照。

## 结构性 key 与可引用对象

用户明确要求新增可引用对象时，先沿用既有 label 风格；没有规范时按对象使用 typed prefix：`sec:`、`subsec:`、`fig:`、`tab:`、`eq:`、`alg:`、`thm:`、`app:`。既有下划线风格继续保留，不能输出 `\\label{tab}`、`\\ref{fig}`、`\\label{tmp}` 等裸占位 key。

新增 label、reference、图片路径/尺寸/裁剪、table、figure、equation、citation 或其他结构对象不能靠 `--allow-additions` 放行；先由用户确认修改后的 TeX，形成新 baseline。引用已有对象要先定位 exact label；不能把 `tab:ablation` 改写成泛化 label、硬编码 `Figure 1`，也不能在 caption 重复 LaTeX 自动编号。图片新增时，label 与 asset signature 同样受保护；未经授权不得简化路径、替换文件或改图像参数。

## 忠实语言修改和术语 ledger

允许的正文修改是拆长句、合并重复、增加 source 已隐含的轻连接、把口语改为正式学术表达和局部明确逻辑，前提是公式、key、数字、单位、sign 顺序及技术事实不变。禁止改定义、假设、算法、证明、公式、实验设置、baseline、数据集、指标、数值、单位、符号或结果；禁止把相关写成因果、局部写成全面优越性、启发式写成理论保证，或新增实验/限制/部署价值。

术语密集章节建立表格：对象/概念、canonical term/family、定义位置、使用位置、允许上下文和保留/避免范围。双向检查同一对象是否被多个术语表示、同一术语是否表示多个对象。不得为词汇变化替换 canonical technical term；`open-vocabulary`、`open-set`、`open-world` 与 `risk-aware`、`safety-aware`、`uncertainty-aware` 等不等价词须依据定义区分。Finding 采用 `TERM-*`，未获作者确认的推荐词只能是 provisional。

## 数学记号 ledger 与授权 mapping

记号是数学实体与显示符号的双向映射。ledger 至少记录实体、symbol、定义/使用位置、作用域、type/dimensions、坐标系和 aliases。检查 object→symbol 是否多符号，symbol→object 是否多实体，并结合大小写、字体、字重、重音、撇号、上下标、类型、维度、坐标系、单位和公式依赖判断。

局部哑变量、循环/求和下标、明示别名、不重叠时间步或坐标系的合法复用不自动构成冲突；有证据的冲突标 `ISSUE REPORTED`，对象或原意不明确才标 `AUTHOR DECISION REQUIRED`，canonical choice 不可擅自决定。

授权 mapping 必须先记录数学对象、旧/新 symbol、包含位置/作用域、aliases/exclusions，再只处理 mapping 中的替换，所有 mapping 外差异均失败或报告。要同步公式、正文、算法、caption、表格、附录中的可见用法，保持数字、单位、维度、sign、key、无关公式不变；每项列 `AUTHORIZED CHANGE`。图中文字无 editable source 时，明确 normalization incomplete；先确认 mapping-only baseline，再做独立 prose polish，不得把 additions-aware 检查当成记号授权。

## 原稿内部数值 ledger

重要事实记录 quantity、value、unit、sign/direction、condition/experiment、位置和对应表格/图片。比较前匹配 metric、dataset、split、condition、aggregation、rounding。检查摘要/正文/结论/附录、方法/实验设置、正文/表格/caption/figure、样本数、数据划分、epoch、维度、阈值、超参数、原值、百分比、增量、置信区间、不确定性、显著性、单位前缀和方向。

同一条件的 91.2% 与 92.1% 属于 `NUM-* ISSUE REPORTED`；条件无法确认是否同一量时才用 `AUTHOR DECISION REQUIRED`。数值审计发现冲突却不授予自动修改权；即便值明显异常，也要外部修正并提供 author-approved baseline。

## 全文覆盖、句式和破折号

只有通过 completeness gate 才可称 `Coverage: FULL MANUSCRIPT`：从 authoritative root 按文档顺序解析静态 `\\input`、`\\include`、`\\subfile`、`\\import` 及项目等价 include；记录缺失、条件、宏生成、生成或循环 include 以及 notation-bearing appendix/supplement；检查 notation-producing macro、custom math environment、正文/公式/算法/caption/table/figure asset 的记号和数字；所有 finding 具 root-relative file:line。缺 macro、动态路径、缺图或未读 supplement 就是 partial coverage。

句式应避免相邻句、段首和同类章节机械重复，但不能换 canonical term 或移动 protected token。作者 prose 不用破折号，改用同位语、从句、冒号、分号、括号、连词或独立句；lexical hyphen、TeX key、URL/DOI、filename/citation key、数学减号、signed value 和 `\\pm` 必须保留。

## 五种模式流程

1. **局部润色：** 判断修辞功能，保护 TeX/math/key/number/unit/sign/fact，做客观英文，局部检查，结果为 `Coverage: PARTIAL`。
2. **全文润色：** 过完整性门槛，建立术语/记号/数值/结构清单，分章润色，做三项源内审计、全稿 claim-boundary/句式/破折号检查和严格 source comparison；只返回一个 authoritative TeX，除非用户要求才给 Markdown。
3. **检验：** original 与 candidate 都存在才比较；缺 original 时所有 comparative fields 为 `NOT ASSESSED`，只做 candidate intrinsic checks；分开 candidate deviation 与 TERM/SYM/NUM source findings；只报告不修改 candidate。
4. **仅一致性审计：** 过 completeness gate，建立所需 ledger，分术语/记号/数值输出 Coverage/Result、finding 和 author question，不改 source。
5. **已确认记号统一：** 必须有 exact approved mapping，只执行 mapping 内替换并记录 `AUTHORIZED CHANGE`、unresolved macro/asset；验证全部差异，返回唯一 authoritative normalized TeX，不生成竞争改写。

## 保全检查器与自动扫描边界

单文件：

```bash
python3 paper-polisher/scripts/check_preservation.py original.tex candidate.tex
```

仅用户授权普通正文新增可加 `--allow-additions`；它仍不允许结构 key、图片 asset、数学区域、数值 token、单位或正负号新增、删除、改变或调序。多文件项目：

```bash
python3 paper-polisher/scripts/check_preservation.py original/main.tex candidate/main.tex --project
```

Project mode 递归解析 `\\input`、`\\include`、`\\subfile`、`\\subfileinclude`、`\\import`、`\\subimport`、`\\inputfrom`、`\\subinputfrom`、`\\includefrom` 和 `\\subincludefrom`，保留 import directory context；缺失、动态、循环 include 既令检查失败，也必须作为 coverage gap。approved symbol map 仅当全局适用时使用，TeX backslash 用 shell 单引号保护；不得与 `--allow-additions` 组合。

自动数字扫描只覆盖可识别的十进制、英文数字、上下文罗马数字、Unicode 数值，以及支持锚点/TeX 连接/括号/提示语境中的 sign、显著性、货币、常见单位和 unit-like compounds。这不是全局语义单位词法器。无法识别的表达式、独立歧义 glyph、custom macro、figure asset 和语义数量都要人工复核；脚本通过不能替代 preservation、coverage 或 quantity-to-unit semantic audit。

## 输出与证据边界

指南的 finding 状态沿用 English SKILL：`PASS`、`ISSUE REPORTED`、`AUTHOR DECISION REQUIRED`、`NOT ASSESSED`；模板中斜线分隔选项不得原样输出。符号示例显示 `SYM-001` 的对象、位置、依据、canonical choice 和仅报告处理；数值示例显示 `NUM-001` 的条件匹配、冲突位置、外部修正要求；缺 original 的 verification 示例明确 candidate 可用但 comparative preservation、technical fidelity 和 numerical preservation 为 `NOT ASSESSED`。

这与 Artifact verification 资料相容：本指南/保全脚本属于语法或 source-bound 证据；fresh execution、输出/seed/依赖才是 Execution-bound；导出并检查可见 PDF/HTML/notebook 才是 Render-bound。已有 weighted-congestion build/pdf/replay/self-check 只提供可复核的分层证据样例，本批没有执行其程序、编译新 TeX 或验证所有 figure/macro。

## 对 UM 存档的适配与未覆盖项

转用于 unrelated-machines 正文或审查页时，只能保留真实输入域、量词、假设、证明/反例、有限 audit scope、模型名、数值、证据等级和 source/output freshness。不能把“只证明必要条件”“有限枚举”“给定 support/oracle”“未完成 decoder”润色成一般算法或 hardness；若稿件把文献、执行回放和 PDF 渲染混成一个 `validated`，应报告 claim-boundary finding，而不是用语言掩盖层级错误。

本资料不创建 theorem、algorithm、gap、hardness、complexity、counterexample、experiment result 或 priority claim；本批未运行 checker、未编译新稿、未检查完整论文 figure/macro、未执行外部文献核验。以后若要改数字、单位、sign、结构 key、citation、asset 或 theorem condition，须在技能外取得新 author-approved baseline；任何 source/output/preview 变化都要绑定新路径、时间戳或 SHA，不覆盖历史证据。
