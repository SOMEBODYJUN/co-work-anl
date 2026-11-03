---
id: "unrelated-machines/paper-polisher-skill"
kind: resource
type_tag: "资料"
title: "TeX 安全润色、符号保全与源到输出审计"
status: "integrated-tex-preservation-resource"
summary: "paper-polisher 技能规定在中英文 TeX 学术稿件润色、翻译、校对、验证和授权符号归一化时保护所有数学、数值、结构键、引用和技术含义；对完整稿件默认执行术语、记号、数值一致性审计，并把源到输出保全与源内一致性分开报告。"
truth_status: "workflow-reference-not-mathematical-evidence"
review_level: "full-skill-read-related-genre-argument-anti-defensive-and-tex-evidence-comparison"
scope: "TeX-safe polishing/translation, preservation, terminology/notation/numerical consistency and source-to-output verification"
source_refs:
  - "clean:a384c9cdb4e4cf198fd7:research/weighted_congestion_frontier/upstream/polish_skill/paper-polisher/SKILL.md"
  - "local:archives/unrelated-machines/state/资料/论文论证重构的主线、证据对齐与结构边界--资料.md"
  - "local:archives/unrelated-machines/state/资料/创新性审查技能的比较、风险与证据边界--资料.md"
  - "local:archives/unrelated-machines/state/资料/数学写作反防御功能审计与证据量词边界--资料.md"
  - "local:archives/unrelated-machines/state/资料/Artifact验证层级、执行渲染与证据新鲜度--资料.md"
  - "local:archives/unrelated-machines/tools/evidence/genre-profiles-20261031/comparisons/comparison-notes.md"
  - "local:archives/weighted-congestion/tools/evidence/linear-article-assets/self-check.json"
source_identity:
  inventory_blob: "e67765b31e10ddd0ab4f83b5af504c0c2059af84"
  source_sha256: "5a197dc415ab45d271c9567026499bbf4f2d4b83daac2779df4f09b9adde8e3e"
  source_size_bytes: 19890
  frozen_commits:
    - "68fad804ec5946cb296f77dc5b336308a66abf12"
    - "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/paper-polisher-20261031/original/paper_polisher_skill.md"
related_objects:
  - "archives/unrelated-machines/state/资料/论文论证重构的主线、证据对齐与结构边界--资料.md"
  - "archives/unrelated-machines/state/资料/创新性审查技能的比较、风险与证据边界--资料.md"
  - "archives/unrelated-machines/state/资料/数学写作反防御功能审计与证据量词边界--资料.md"
  - "archives/unrelated-machines/state/资料/Artifact验证层级、执行渲染与证据新鲜度--资料.md"
---

# TeX 安全润色、符号保全与源到输出审计

## 来源身份与处置

本对象完整实读上游 `research/weighted_congestion_frontier/upstream/polish_skill/paper-polisher/SKILL.md` 的 19,890 字节（216 行）。clean source ID 为 `a384c9cdb4e4cf198fd7`，inventory blob 为 `e67765b31e10ddd0ab4f83b5af504c0c2059af84`，原文 SHA-256 为 `5a197dc415ab45d271c9567026499bbf4f2d4b83daac2779df4f09b9adde8e3e`；冻结索引同时列出 `legacy-cleanup` 与 `main`。完整原字节保存在 [paper_polisher_skill.md 原文证据](../../tools/evidence/paper-polisher-20261031/original/paper_polisher_skill.md)。

处置为 `integrated` 资料资源。该技能是 TeX 保护、语言润色和一致性审计的工程合同，不是数学命题、证明、算法、实验结果或外部新颖性认证。它的独有内容是：把默认润色、比较验证、只做一致性审计和授权记号归一化分成模式；对结构键、数学区、数值/单位/符号、评论和代码样式实行不可变保护；用完整稿件门槛和确定性 `TERM-*`/`SYM-*`/`NUM-*` findings 记录覆盖与结果；对 preservation checker 的局限和 `NOT ASSESSED` 边界明确止损。

## 适用范围与任务分流

技能用于中英文 TeX 学术稿件的安全润色、翻译、校对、source-to-output 验证、术语/记号/数值审查和作者明确授权的记号规范化。完整稿件、长章节、验证、跨节一致性、归一化或严格 style-guide 工作要先读相应 `tex_safe_polishing` 参考；中文流程需要时读中文 companion，不为重复上下文同时加载两份。

它不主导以下任务：

- novelty、contribution defensibility、危险 baseline、reviewer attack 由 `idea-novelty-auditor` 负责；
- literature review、gap framing、引用选择和 citation-role assignment 由 `problem-driven-literature-review` 负责；
- broad storyline、引言结构和 experiment-to-claim redesign 由 `paper-argument-reconstructor` 负责。

若请求把这些任务和润色混在一起，必须先完成上游推理，再做最后的 faithful language/consistency pass；各自 artifact 和报告分开，除非明确要求合并。

## 模式选择和优先级

用户明确要求的动作先于输入稿件由谁产生。若同时要求 notation normalization 与 prose polishing，先执行并批准精确符号映射，把归一化 TeX 作为新 baseline，再按 baseline 做润色；不能把语言和符号改动合并成一次无法解释的比较。

### Default Polishing Mode

润色或翻译供给文本，同时保护全部 protected elements。完整稿件还要默认执行术语、记号和源内数值一致性审计，并报告源级问题，不能静默修正。

### Verification Mode

比较 candidate 和 original 时必须同时提供两者，才能判断 TeX、数学、数值、单位、符号、引文、技术含义或 claim strength。若 original 不可用，只检查 candidate 自身，并将每项源比较写为 `NOT ASSESSED`，不能从 candidate 单独推断保全。验证模式不得重写或修复 candidate，即使发现硬规则违反；逐位置报告 deviation，并分开标注 candidate 引入的问题与源稿原有冲突。

### Consistency Audit Mode

若用户只要求术语、变量、记号、符号或数字一致性，禁止重写稿件；只在可用范围报告 `TERM-*`、`SYM-*`、`NUM-*` findings，并保留 source text、symbols、values、units、signs 不变。

### Approved Notation Normalization Mode

只在用户明确要求规范化并批准精确 symbol mapping 时启用。映射必须说明数学实体、旧/新符号、范围/位置及有意 aliases/exclusions。只能执行批准替换；未映射的数学、结构、文本和数字差异都算 error。数字、单位、百分比、维度、样本量、顺序、正负或 plus-minus 符号永不因 mapping 被改变。若符号落在不可编辑 figure、generated file、custom environment 或未解析 macro 中，报告 unresolved location，不能声称 complete normalization。`--allow-additions` 不能授权符号变化。

## 共享覆盖和结果协议

每次术语、记号和数值审计都要分别报告 coverage 与 result：

- `Coverage: FULL MANUSCRIPT` 仅在完整稿件门槛通过后使用；
- `Coverage: PARTIAL` 表示只审计所声明的 local 或可解析范围；
- `Result: PASS` 表示当前范围没有冲突或未解歧义；
- `Result: ISSUE REPORTED` 表示有清楚的不一致，且没有 finding 还需要作者决定；
- `Result: AUTHOR DECISION REQUIRED` 表示存在稿件本身无法解决的可能冲突；已确认的冲突仍单独标 `ISSUE REPORTED`；
- `Result: NOT ASSESSED` 只表示某项比较完全无法执行，不能因为 coverage partial 就滥用。

Finding ID 按 root-relative file 和 source order 确定：`TERM-001`、`SYM-001`、`NUM-001`。每项给出精确 file/line；若没有文件，则用 section、equation、table、algorithm、caption 或 quoted-text 稳定锚点。冲突的确定性与修复权限分开：即便作者还需决定替换 term/symbol/value，已证实冲突仍是 `ISSUE REPORTED`。

## 完整稿件覆盖门槛

只有满足下列五项才能声称 FULL MANUSCRIPT：

1. 识别 authoritative root TeX，并按 document order 解析所有静态可达 `\\input`、`\\include`、`\\subfile`、`\\import` 和等价 include；
2. 记录缺失、条件、动态、生成或循环 include，以及 notation-bearing appendix/supplement；
3. 检查 user macro 和 custom math environment，不依赖 preservation script 自动理解它们；
4. 检查正文、公式、algorithm、caption、table 和 figure asset 中的记号/数值。若 figure 有相关嵌入文字却无法读，coverage 只能 partial；
5. 保留 root-relative 文件/行位置并确认没有跳过请求范围。

完整文件上传不自动等于完整 analytical coverage。任何动态 include、缺源图、未解析 macro、条件 appendix 或未读 supplement 都必须在报告中写成 coverage gap。

## 不可协商的保护规则

技能将以下内容视为 protected source：TeX structures、environments、citations、labels、references、bibliography keys、function/module/dataset/metric names 和技术含义；`\\label`、`\\ref`、`\\eqref`、`\\includegraphics`、citation command、`\\bibitem`、BibTeX key 等结构命令的参数不能 rename、merge、delete、reorder 或 normalize。`comment`、`verbatim`、listing、inline literal 和 code-like source 也逐字保护，不能把 inline comment 改成整行 comment、把 prose 移入/移出 protected region，或跨数学/TeX 结构移动。

每个原始数学区域及 document order 必须保留，唯一例外是批准 mapping 中的精确替换。每一个数字、单位、百分比、维度、参数、样本量、table/figure value、significance marker、数字 token 顺序以及正负/plus-minus 符号都必须保留，包括 identifier、comment、literal、URL 和 protected command 参数中的数字。技能没有“数字校正例外”，`--allow-additions` 也不能放松此规则。

源到输出保全与源内一致性是两项独立检查。源中已有 term/symbol/value/unit/sign 冲突是 finding，不是编辑许可；不能修正可疑数字，必须报告 `NUM-*` 并要求作者在技能外修改 source，交回新的 author-approved baseline。不能改变数学定义、定理条件、proof logic、algorithm steps、实验设置、reported results、baselines 或 datasets；不能为文体变化任意替换技术术语；不能凭空增加 claim、experiment、guarantee、deployment value、limitation 或 conclusion。

此外，作者新写的 manuscript prose 不使用 dash punctuation；保护 lexical hyphen、数学 minus、signed value、keys、URLs、DOI、filename 和 bibliography metadata 原样不动。这是文字风格规则，不得被误读为可改数学减号或受保护标识符。

## 审计工作流和 preservation checker

工作流先按用户意图选择模式并固定 scope，完整稿件先过 coverage gate，然后建立三本 ledger：

- **术语 ledger：** entity、canonical term、允许的上下文形式、定义和位置；
- **记号 ledger：** 数学实体、symbol、定义/使用、scope、type/dimensions、frame 和 aliases；
- **数值 ledger：** measured/configured quantity、value、unit、sign、condition、source location 与 prose/table/figure 对应。

润色模式只在 protected math 和 numerical-token order 固定后改 prose；随后做 entity↔term/symbol 和 quantity/condition↔value/unit/sign 的双向 consistency check，再做 sentence architecture、dash-free prose、objective tone 和 claim boundary 检查。original/candidate 都存在时运行 preservation checker；多文件 manuscript 使用 `--project` 遍历静态 include；不规则 macro、figure asset 或 custom environment 仍需人工比较。

单文件严格比较命令是：

```bash
python3 paper-polisher/scripts/check_preservation.py original.tex candidate.tex
```

允许用户明确授权普通 prose addition 时才可加 `--allow-additions`，但该选项仍不允许新增/删除/改变/重排 structural keys、math regions、numbers、units 或 signs。完整项目使用：

```bash
python3 paper-polisher/scripts/check_preservation.py original/main.tex candidate/main.tex --project
```

经用户批准的全局 symbol mapping 可重复使用 `--approved-symbol-map`，需用 shell 单引号保护 TeX backslash；该 flag 只做 math-token substitution，不授权 prose、数字、货币、百分比、单位、sign 或有排除位置的实体映射。无法解析的动态/cyclic/missing include 会使比较失败，同时也是完整稿件 coverage gap。

Checker 不能证明语义源内一致性，也可能不理解任意 user macro、custom environment、figure asset 或自然语言数字/单位。其数字扫描对支持的 decimal、English textual、contextual Roman、Unicode numeric、significance marker、currency、common unit 和 unit-like compounds 是 fail-closed，但不是 global semantic lexer；无法识别的表达式和歧义 glyph 必须人工检查并另做 semantic numerical audit。

## 输出格式与当前存档的证据边界

Consistency-only audit 报告 audited scope/coverage gaps、分别的 TERM/SYM/NUM coverage/result、finding 位置/证据/建议映射，并明确没有改 source。Verification 报告 original 是否可用、comparison coverage、candidate introduced deviations、source-internal findings、未评估项以及 candidate 未被修改。Approved normalization 输出 authoritative normalized TeX、逐项 `AUTHORIZED CHANGE`、unresolved locations 和 unexpected-difference report，不生成第二份重写稿。

重大章节/完整稿件的 Default Polishing 输出 authoritative TeX、source preservation/technical fidelity/numerical-token preservation/terminology/notation/numerical/citation/sentence structure/claim boundary/output completeness 的 concise report；Markdown reading version 只有用户明确要求才生成，TeX artifact 才是权威版本。每个 comparative field 选择 `PASS`、`ISSUE REPORTED` 或 `NOT ASSESSED`；citation/bibliography 还可 `NOT PRESENT`，intrinsic style/output completeness 只能 `PASS` 或 `ISSUE REPORTED`。不得把 angle-bracket placeholder 原样输出。

这套边界与本仓库已有 artifact verification 资料一致：source 阅读或静态检查最多是 Text/Source-bound；只有新鲜执行及输出/seed/依赖才能叫 Execution-bound；只有导出并检查可见 HTML/PDF/notebook 才叫 Render-bound。`archives/weighted-congestion/tools/evidence/linear-article-assets/` 中现成的 `build`、`pdf-reading`、`replay-comparison`、`self-check` 和 `provenance` 文件展示了源码、编译结果、PDF 抽取、页面重渲染和数值回放可以分层保存，但这些现成证据不把本技能自身变成对所有稿件都已执行。

## 与相邻资料的去重和 UM 适配

| 相邻资料 | 主要职责 | paper-polisher 的边界 |
| --- | --- | --- |
| 创新性审查技能 | 比较直接/相邻/经典/危险工作、reviewer attack、novelty risk | 不重新判断 novelty，只在上游边界确定后忠实保持 claim |
| 创新框架候选 | 主张、重要性、已有覆盖、gap、证据、falsifier | 不把候选改写成更强贡献；保留 scope 和 non-claims |
| 论文论证重构 | 需求→瓶颈→能力→机制→证据的章节和段落主线 | 不进行 broad storyline redesign；只做 final faithful language/consistency pass |
| 反防御功能审计 | Keep/Rewrite/Compress/Delete/Flag 句子功能、否定和量词保护 | 可执行同一证据保护，但不能删除 TeX/math/number protected source |
| Artifact 验证资料 | Text/Source/Execution/Render 层级和 freshness/hash | 为 TeX 源到输出及静态/可视检查给出操作细节，不把 checker 通过写成数学正确 |
| genre profiles / linear-article evidence | 文类、编译、PDF 和回放证据 | 只借验证分层；不把已有论文构建状态迁移到新稿件 |

转用于 UM 正文或审查页时，润色只能保持真实对象的输入域、量词、假设、证明/反例、有限 audit scope、模型名称、数值和证据等级；不能把“仅必要条件”“有限枚举”“给定 support/oracle”“未完成 decoder”改写成一般算法或 hardness。若原稿把 source-bound 文献、execution-bound replay 与 render-bound PDF 混成一个“validated”，应报告 claim-boundary finding，不能靠句子美化掩盖层级错误。

## 处置与未覆盖项

本资料保留为 TeX 论文、PDF/HTML 预览和数学审查页的安全编辑合同。它支持受保护内容清单、四种模式、完整覆盖门槛、术语/记号/数值 ledger、preservation checker 和确定性 findings；不产生新的 theorem、algorithm、gap、hardness、complexity、counterexample、experiment result 或 priority claim，也没有在本批运行 checker、编译所有现成论文或读上游参考文献全文。

以后若要修改数字、单位、sign、结构键、citation、figure asset 或 theorem condition，必须在技能外取得作者批准的新 baseline；若要给出 novelty、literature、storyline 或实验充分性结论，先调用对应资源并把结果分开登记。任何 source/output/preview 新鲜度变化都要绑定新的路径、时间戳或 SHA，不应覆盖历史证据。
