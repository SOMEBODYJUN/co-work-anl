---
id: "unrelated-machines/tex-safe-polishing"
kind: "resource"
type_tag: "资料"
title: "TeX 安全润色与受保护内容验证边界"
status: "integrated-resource; source-output-preservation-contract"
truth_status: "source-read-workflow-with-artifact-boundaries; no-new-mathematical-claim"
review_level: "full-21723-byte-read-cross-reference"
scope: "research/weighted_congestion_frontier/upstream/polish_skill/paper-polisher/references/tex_safe_polishing.md"
summary: "完整读取 21,723 字节 TeX-Safe Academic Polishing Guide：区分 source-to-output preservation、术语/符号/数字一致性和技术真值；保护数学区、结构键、注释/代码、数字/单位/符号、引用和资产路径；规定术语/notation/numerical ledgers、FULL MANUSCRIPT completeness gate、local/full/verification/consistency/approved-mapping 五模式及 checker 的语法边界。它不产生 UM 数学结论，也不允许借润色修复可疑数值、扩大 claim 或替代执行/渲染验证。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/weighted_congestion_frontier/upstream/polish_skill/paper-polisher/references/tex_safe_polishing.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/weighted_congestion_frontier/upstream/polish_skill/paper-polisher/references/tex_safe_polishing.md"
source_identity:
  id: "08507e794b6ed17a804f"
  path: "research/weighted_congestion_frontier/upstream/polish_skill/paper-polisher/references/tex_safe_polishing.md"
  inventory_blob: "e356336117e99c0f8b34c9fc3c0dd57c85203b91"
  sha256: "0352d085bba703604ee46a0f18b46117480a93ab262c6554619bee7fa25c5871"
  size_bytes: 21723
  frozen_commits:
    - "68fad804ec5946cb296f77dc5b336308a66abf12"
    - "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/tex-safe-polishing-20261031/original/tex_safe_polishing.md"
related_objects:
  - "archives/unrelated-machines/README.md"
  - "archives/unrelated-machines/prompts/README.md"
  - "archives/unrelated-machines/state/资料/Artifact验证层级、执行渲染与证据新鲜度--资料.md"
  - "archives/unrelated-machines/state/资料/论文论证重构与主张证据对齐--资料.md"
  - "archives/unrelated-machines/state/资料/数学写作反防御功能审计与证据量词边界--资料.md"
  - "archives/unrelated-machines/state/资料/数学写作文类剖面与主张责任边界--资料.md"
  - "archives/unrelated-machines/state/资源/数学写作语料清单与测量边界--资源.md"
  - "archives/weighted-congestion/state/资料/接题来源映射与文献导入的版本边界--资料.md"
  - "archives/weighted-congestion/tools/evidence/frontier-brief-evidence/original/research/weighted_congestion_frontier/SOURCES.md"
  - "archives/weighted-congestion/tools/evidence/restored-upstream-manifest/original/research/weighted_congestion_frontier/upstream/manifest.json"
companion_skill:
  path: "cleanup/workspaces/Boss3/agent-gamma/paper_polisher_skill.md"
  sha256: "5a197dc415ab45d271c9567026499bbf4d2d4b83daac2779df4f09b9adde8e3"
  size_bytes: 13116
---

# 1. 来源身份与总体契约

本条目完整读取 `research/weighted_congestion_frontier/upstream/polish_skill/paper-polisher/references/tex_safe_polishing.md` 的 21,723 字节。冻结 inventory blob 为 `e356336117e99c0f8b34c9fc3c0dd57c85203b91`，SHA-256 为 `0352d085bba703604ee46a0f18b46117480a93ab262c6554619bee7fa25c5871`；该路径在 `legacy-cleanup` 与 `main` 两个冻结提交中均有同一来源记录，原文副本位于 evidence 路径。

本轮同时读取共享工作区的 companion SKILL `cleanup/workspaces/Boss3/agent-gamma/paper_polisher_skill.md`，13,116 字节，SHA-256 为 `5a197dc415ab45d271c9567026499bbf4d2d4b83daac2779df4f09b9adde8e3`。SKILL 规定 paper-polisher 用于 TeX 安全学术润色、翻译、校对、source-to-output 验证、术语/符号/数值一致性及作者批准的 notation mapping；novelty、文献、宽论证重构和实验章节审计应分别交给 idea-novelty-auditor、problem-driven-literature-review、paper-argument-reconstructor 和 experiment-section-auditor。

参考文档的核心是把四件事分开：

1. 候选是否保留了 source 的受保护内容；
2. source 自身的术语是否一致；
3. source 自身的数学符号是否一致；
4. source 自身的数字、单位、方向和符号是否一致。

一次 preservation pass 不回答后三项；source 内部不一致也不授权默默修正。该资料因此是写作/发布工作流，不是 UM 定义、算法、证明、反例或外部文献结论。

# 2. 受保护内容：source 到 output 的精确保真

在 polishing、翻译、普通 prose addition、verification、consistency audit 和 notation normalization 中，以下内容都必须按 source 保留：

* 行内和 display math，包括 `$...$`、`\(...\)`、`\[...\]` 以及命名数学环境；
* figure、table、algorithm、theorem、proof、lemma、definition、remark 环境；
* 结构命令及其参数，如 label、ref/eqref、cite、bibliography key、image path；
* 注释、verbatim/listing、literal 或 code-like source，以及行内/整行注释边界和它们相对于 TeX/数学的顺序；
* 变量和函数记号，除非存在作者批准的精确 substitution mapping；
* 数值、数字 token 顺序、单位、百分比、维度、样本量、参数、表格和图中数值、显著性标记以及正负号/`\pm`；
* 技术含义、条件、假设、算法步骤、证明、实验、baseline、dataset、metric、reported result。

数值规则没有例外：不能为改善语流插入、删除、改变或重排数字，也不能改写注释、literal、URL 或命令参数中的数字。如果数值、单位、符号、引用、作者名次序可疑，必须报告并要求作者在技能外提供新的 approved baseline；不能从表格趋势、邻近值或预期结果推断正确值。

保护规则也禁止把 active prose 移进/移出 comment 或 literal 区域，改变 inline `%` 与整行注释的边界，或把 literal region 移过数学/TeX。自定义或 checker 不认识的 literal macro 需要手工比较。

# 3. Structural keys 与 referenceable objects

如果用户明确要求新增可引用对象，先遵循稿件已有 label convention；没有 convention 时使用 semantic typed prefix：`sec:`、`subsec:`、`fig:`、`tab:`、`eq:`、`alg:`、`thm:`、`app:`。保留已有 underscore convention，不输出 `\label{tab}`、`\ref{fig}`、`\label{tmp}` 等裸占位符。

新增 label、reference、image path、size/crop、table、figure、equation、citation 或其他结构对象，只有在用户明确批准后才可加入；即便使用 `--allow-additions` 也不能把结构新增视为被批准。批准后的对象和资产签名必须作为新 baseline 保护。已有对象引用应检查 exact label，不能把实际 `tab:ablation`、`tab:errors`、`tab:torwic_errors` 替换成通用名字，也不能硬编码生成后的 “Figure 1/Table 1”。caption 描述对象，不重复生成的编号。

这条边界与仓库的 source/evidence 组织直接相关：文件名、stable ID、证据路径和原始 TeX 键属于 provenance，不因“语言润色”而可重命名；新增数学对象应另建正式 state/evidence，而不是从段落中隐式生成。

# 4. Faithful language revision

允许的 prose 变化包括拆分过长句、合并重复表达、加入 source 已暗含的轻过渡、把口语换成正式学术语气、局部显式化逻辑，以及在不移动 protected math、结构键、数字、单位或符号的前提下重排 prose-only 子句/句子。

禁止的变化包括改定义、假设、算法、证明、公式、实验设置、baseline、dataset、metric、数值、单位、符号或结果；增加实验、保证、限制、应用或部署主张；把相关性写成因果；把局部结果扩成一般 superiority；把 heuristic 改成理论 guarantee。

因此 paper-polisher 只能改表达，不能修复数学。若段落结构有更深 gap，应先交给 argument-reconstructor；若 claim 可能超出文献或结果，应先交给 novelty/literature 审计。修辞上的“更强”如果改变了 claim strength，就是禁止的技术改变。

# 5. 术语、数学记号和数字三本 ledger

## 5.1 Terminology ledger

术语密集的 section 或全稿应建立：实体/概念、canonical term/family、定义位置、使用位置、允许的上下文形式、保留/避免范围。必须双向检查：同一实体是否被多个词表达而没有显式区别；同一术语是否在重叠范围指不同实体。

不能为了风格多样随意替换技术词；例如 `open-vocabulary/open-set/open-world` 或 `risk-aware/safety-aware/uncertainty-aware` 只有在 manuscript definitions 支持时才能区分。发现项用 `TERM-*`，推荐词在未获 author approval 前只是 provisional。

## 5.2 Mathematical notation ledger

记号应视作“数学实体 ↔ 渲染符号”的双向映射，ledger 至少包含：实体、symbol、定义/使用位置、scope、type/dimensions、frame、显式 alias。检查同一实体是否用多个 symbol，以及同一 symbol 是否表示多个实体；同时检查大小写、字体、粗体、accent、prime、上下标，因为它们可能编码身份而非样式。

局部 dummy variable、loop/sum index、明确 alias、非重叠时间步或 frame 坐标的复用不自动构成冲突；有充分证据时报告 `ISSUE REPORTED`，实体或意图不明确时报告 `AUTHOR DECISION REQUIRED`，canonical choice 放在独立字段。不要擅自选择新符号。

若用户批准 exact mapping，先记录 finding、实体、旧/新 symbol、scope、alias/exclusion。只改映射范围内的 TeX-visible 定义和使用，保持数字、单位、维度、符号和结构键不变；每项标为 `AUTHORIZED CHANGE`，任何 unmapped difference 都报告。图中的不可编辑文字无法同步时，报告 normalization incomplete。

## 5.3 Numerical ledger

重要数量应记录 quantity/fact、value、unit、sign/direction、condition/experiment、locations、related table/figure。比较前先匹配 metric、dataset、split、condition、aggregation、rounding；同一条件下 table/prose/figure 不一致是 `NUM-* ISSUE REPORTED`，若是否同一量不能从稿件确定则 `AUTHOR DECISION REQUIRED`。

数值审计是 source-internal：它发现冲突，但不能让 paper-polisher 自动修正。即便 91.2% 与 92.1% 显然冲突，也只能报告、要求作者在技能外改 source 并提供新 baseline。它与 source-to-output preservation 分开，不能把“看起来错”作为编辑许可。

# 6. Full-manuscript coverage gate

只有满足以下条件，才能报告 `Coverage: FULL MANUSCRIPT`：

1. 找到 authoritative root TeX，并按文档顺序解析可静态解析的 `\input`、`\include`、`\subfile`、`\import` 等；
2. 记录 missing/conditional/macro-generated/generated/cyclic includes，以及 notation-bearing appendix/supplement；
3. 检查 notation-producing macros 和 custom math environments，不能只依赖 preservation script；
4. 检查 prose、equation、algorithm、caption、table 和 supplied figure asset 中的记号与数字；不可查看的相关资产使 coverage 变为 partial；
5. 所有 finding 使用 root-relative file:line，且确认没有跳过 requested scope。

完整文件上传本身不等于 FULL MANUSCRIPT。对 pasted text 要以 section/equation/table/algorithm label 或稳定摘录定位。若 figure 的 embedded label 无 editable source，只能报告未完成 normalization。

# 7. 句子结构与 dash policy

在不改变技术词和 protected token order 的情况下，避免机械重复的开头、subject-predicate 框架、clause order、voice、transition、result template 和段落开头；有意 parallelism 用于对比/枚举时保留。

作者自己写的 manuscript prose 不用 em dash 或 en dash；按角色改为 apposition、content clause、relative clause、colon、semicolon、parentheses、conjunction 或 separate sentence。不要把 prose dash 与 lexical hyphen、URL/DOI/filename/citation key、数学 minus、signed value 混同：`risk-aware`、`$a-b$`、`$-1$`、`-3.2 dB` 和 `mean \pm std` 在 source 中应原样保留。

该规则是风格限制，不是数学修改；若 dash 位于受保护 literal、key 或数学中，保留 source。

# 8. 五种工作模式

## 8.1 Local polishing

识别局部修辞作用；保护 TeX、math、keys、numbers、units、signs 和 facts；润色客观学术英语；检查可见术语、符号、数字一致性；局部范围即使 clean，也报告 `Coverage: PARTIAL`。

## 8.2 Full-manuscript polishing

先过 completeness gate；建立 terminology、notation、numerical、structural ledgers；逐节润色并维护 protected-token order；运行三项 source-internal consistency audits、全稿 style/claim-boundary/dash checks 和 strict source comparison；返回一份 authoritative TeX 与 review report。除非用户明确要求，不另生成可编辑 Markdown 版本。

## 8.3 Verification

需要 original 和 candidate 才能作 comparative preservation 判断；若 original 不在，所有比较字段标 `NOT ASSESSED`，只做 candidate intrinsic checks。不得改写 candidate；分别报告 candidate-introduced deviations 与 source-internal TERM/SYM/NUM findings。

## 8.4 Consistency-only audit

仅建立用户要求的 ledger；不重写 source；分开给 terminology/notation/numerical 的 Coverage 和 Result，并报告 finding 与 author question。

## 8.5 Approved notation normalization

必须先有 exact approved mapping；否则停在 audit mode。只作 mapped substitutions，报告每项 `AUTHORIZED CHANGE` 和 unresolved macro/custom environment/generated file/figure asset；验证所有差异后返回一份 authoritative normalized TeX，不额外生成竞争改写。不要用 `--allow-additions` 为 symbol change 开例外。

如果同时要 normalization 和 prose polishing，先完成并批准 normalization，再以新 baseline 做单独 prose pass；不能把两种差异混成 mapping-only validation。

# 9. Preservation checker 与证据层级

单文件严格比较：

```bash
python3 paper-polisher/scripts/check_preservation.py original.tex candidate.tex
```

仅普通 prose additions 可用 `--allow-additions`，但它仍不允许 structural key、image asset、math region、numeric token、unit 或 sign 的新增、删除、改变或重排。多文件 manuscript 传 authoritative root 并用 `--project`；project mode 沿当前/旧 import-directory context 跟随静态 include。missing、dynamic 或 cyclic include 会失败，并且也是 semantic coverage gap。

`--approved-symbol-map` 只作全局 normalization mapping，必须 shell-safe 转义反斜杠；非 math prose 和 unmapped math token 必须不变，numeric/currency/percentage/unit/sign 永不被授权。映射含 excluded/intentional reuse 时，改用 location-aware authorization ledger 和 author-approved baseline。

checker pass 只建立支持语法的 source-to-output preservation；它不理解任意 user macro、custom environment、figure embedded text 或所有自然语言数值/单位。它的 numeric scan 是 syntactic coverage，不是全语义 unit lexer；手工比较未识别形式，仍需 semantic quantity-to-unit audit。不要把 checker 通过写成数学正确、执行成功或渲染成功。

这与本仓库的[Artifact 验证层级、执行渲染与证据新鲜度](Artifact验证层级、执行渲染与证据新鲜度--资料.md)互补：

| 层级 | 可说什么 |
| --- | --- |
| Text-bound | 源正文、公式、记号、内部链接在文本层一致或发现问题 |
| Source-bound | 指定引用/定理位置与支配来源一致或冲突 |
| Execution-bound | 新鲜代码运行、seed/tolerance/dependencies、输出/命令可复核 |
| Render-bound | 导出 HTML/PDF/notebook 的可见页面按描述渲染 |

TeX checker 主要属于 source-to-output/static preservation；只有当前 source 编译、查看 compiler result、渲染高风险页并检查 glyph、minus、subscript、delimiter、label/link，才达到 Render-bound。源改动而旧 PDF/preview 未重生成时，下游 stale；不能让静态 hash 或旧输出越过新鲜度边界。

# 10. 输出协议与 finding 状态

Consistency report 应分别列：

* audited scope 和 coverage gaps；
* terminology、notation、numerical 各自 Coverage/Result；
* `TERM-*`、`SYM-*`、`NUM-*` 的位置、证据和建议/作者问题；
* source content 未修改声明。

Verification report 应列 original/candidate 是否可用、candidate deviations、source-internal findings、original 不可用时的 `NOT ASSESSED`，并明确 candidate 未修改。

Default polishing 对小段返回 TeX-safe 版本和必要说明；对大 section/full manuscript 返回 authoritative TeX、简洁 review report（preservation、technical/claim fidelity、numeric/token/unit/sign、术语、符号、source-internal numerical、citation/bibliography、sentence/dash/objective tone、output completeness）和 compliance note。Markdown reading version 只有用户明确要求才生成，TeX 仍是 authoritative artifact。

finding 状态必须从协议中选择：`PASS`、`ISSUE REPORTED`、`AUTHOR DECISION REQUIRED`、`NOT ASSESSED`；coverage 使用 `FULL MANUSCRIPT` 或 `PARTIAL`。比较字段在 original 缺失时全部 `NOT ASSESSED`，不要用“partial”代替“not assessed”。finding ID 按 root-relative source order 确定性编号。

# 11. 与现有资料和 UM 归档的分工

* `论文论证重构与主张证据对齐` 负责问题—瓶颈—gap—机制—证据—含义的故事线；paper-polisher 只在该逻辑确定后做 faithful prose/TeX pass。
* `数学写作反防御功能审计` 负责 Keep/Rewrite/Compress/Delete/Flag 和数学否定保护；paper-polisher 不能用语言优化删除必要条件。
* `数学写作文类剖面` 负责不同 genre 的论证依赖；`数学写作语料清单` 只给 corpus-bound 的有限风格测量；两者不改变 TeX 真值。
* `Artifact 验证层级、执行渲染与证据新鲜度` 负责 text/source/execution/render 层级及 source→output→preview freshness；paper-polisher checker 不替代执行/渲染。
* `贡献地图` 和 `科研想法新颖性风险审计` 负责主张、风险、baseline、priority 和 reviewer attack；paper-polisher 不审 novelty 或 literature。
* `archives/unrelated-machines/README.md` 与 `prompts/README.md` 规定正式数学条件以 state 正文为准；TeX 资料不得从 prose 生成新 theorem/algorithm。

对 UM 长篇数学文稿，safe workflow 是：先绑定 source ID/version 和 authoritative root；再用 argument/novelty/literature 资料确定可防守主张；随后建立 terminology/notation/numerical ledger；保留数学区、结构键、数字、符号和证据路径；若发现数值/单位/符号可疑只报告；最后按 checker 与 artifact freshness 层级给出实际覆盖。任何新定理、证明、程序、图或参考文献必须另建 source/evidence，不在 polishing pass 中悄悄增加。

# 12. 处置与边界

本源处置为 `integrated` 资料/资源：原文 evidence 已保全，受保护内容、结构键、faithful language、三本 ledger、full-manuscript gate、dash policy、五种模式、checker 命令、finding protocol 和执行/渲染分层均已归档。

它不创建新的 UM 定理、算法、复杂度、gap、hardness、反例、实验结果、外部优先权或 PDF/HTML 成功结论；不允许用润色掩盖 source 内部矛盾或修正可疑数字。参考文档本身也没有执行 checker、编译 TeX 或渲染 PDF；本次清洗达到的是 source-bound 文本阅读与工作流整理，不是 execution-bound/render-bound 验证。
