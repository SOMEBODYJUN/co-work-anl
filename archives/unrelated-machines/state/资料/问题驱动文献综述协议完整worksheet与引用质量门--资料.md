---
id: "unrelated-machines/literature-review-protocol-srlhgmcv"
kind: "resource"
type_tag: "资料"
title: "问题驱动文献综述协议：完整 Worksheet、引用角色与质量门"
status: "integrated-resource; full-protocol-read"
truth_status: "source-read-writing-protocol; no-search-or-mathematical-claim"
review_level: "full-14796-byte-read-cross-archive-comparison"
scope: "research/weighted_congestion_frontier/upstream/polish_skill/problem-driven-literature-review/references/literature_review_protocol.md"
summary: "完整读取 14,796 字节 Problem-Driven Literature Review Protocol：在写 prose 前填 S-R-L-H-G-M-C-V worksheet，用五步段落模板把 requirement、existing capability、hidden assumption、boundary、bridge 串起来；以 claim-first 选择引用并赋予 FND/SUR/REP/SOTA/COMP/BOUND/BENCH/THEO/APP/ADJ 角色；按 seed/backward/forward/requirement 检索；运行 direct-competitor、negative-claim、review-experiment、citation-integrity、metadata 五类质量门，并用 BibTeX checker 复核元数据。协议本身未执行搜索、Crossref 或引用核验，不产生 UM 数学结论或外部优先权。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/weighted_congestion_frontier/upstream/polish_skill/problem-driven-literature-review/references/literature_review_protocol.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/weighted_congestion_frontier/upstream/polish_skill/problem-driven-literature-review/references/literature_review_protocol.md"
source_identity:
  id: "ad8ddf8cdd1a700ec049"
  path: "research/weighted_congestion_frontier/upstream/polish_skill/problem-driven-literature-review/references/literature_review_protocol.md"
  inventory_blob: "2972c5bd49e44fc37ae902b72975dce89968d2a7"
  sha256: "f3c66ab4d820c5598951d344e5729f22b042e784253c5049ff9564b7f969fb33"
  size_bytes: 14796
  frozen_commits:
    - "68fad804ec5946cb296f77dc5b336308a66abf12"
    - "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/literature-review-protocol-20261031/original/literature_review_protocol.md"
  - "archives/unrelated-machines/tools/evidence/literature-review-protocol-20261031/comparisons/comparison-notes.md"
related_objects:
  - "archives/unrelated-machines/state/资料/问题驱动文献综述S-R-L-H-G-M-C-V与引用证据边界--资料.md"
  - "archives/unrelated-machines/state/资料/论文论证重构与主张证据对齐--资料.md"
  - "archives/unrelated-machines/state/资料/贡献地图模板与主张证据风险边界--资料.md"
  - "archives/unrelated-machines/state/资料/科研想法新颖性风险审计与优先权边界--资料.md"
  - "archives/unrelated-machines/state/资料/数学写作反防御功能审计与证据量词边界--资料.md"
  - "archives/unrelated-machines/state/资料/数学写作文类剖面与主张责任边界--资料.md"
  - "archives/unrelated-machines/state/资料/TeX安全润色与受保护内容验证边界--资料.md"
  - "archives/unrelated-machines/state/资源/BibTeX引用元数据检查器解析、规则与Crossref边界--资源.md"
  - "archives/unrelated-machines/README.md"
  - "archives/unrelated-machines/prompts/README.md"
companion_skill:
  path: "cleanup/workspaces/Boss3/root/literature_review_skill.md"
  sha256: "16d6b89118cc838a613e08ba0de56361e5a40276343857a0692c67028426d592"
  size_bytes: 5574
---

# 1. 来源身份与协议职责

本条目完整读取 `research/weighted_congestion_frontier/upstream/polish_skill/problem-driven-literature-review/references/literature_review_protocol.md` 的 14,796 字节。冻结 inventory blob 为 `2972c5bd49e44fc37ae902b72975dce89968d2a7`，SHA-256 为 `f3c66ab4d820c5598951d344e5729f22b042e784253c5049ff9564b7f969fb33`；该路径在 `legacy-cleanup` 和 `main` 两个冻结提交中均有来源记录，原文和 comparison notes 位于本条目的 evidence 路径。

协议是 `problem-driven-literature-review/SKILL.md` 的完整参考。SKILL 已登记核心 S-R-L-H-G-M-C-V、工具分流和 verification mode；本源新增完整 worksheet、五步段落模板、reference-role 分类、seed/backward/forward/requirement 检索、BibTeX metadata checker 用法、五类质量门和按贡献类型的例子。它只规定怎样组织和核查文献综述，不执行搜索、Crossref、程序、定理证明或外部优先权认证。

本页归入 `archives/unrelated-machines/state/资料/`。对 UM 的使用方式是把已读取的定义域、量词、文献路线、隐藏假设、结构缺口和证据层级放回正式对象；不能从协议的“缺口”语言创建新的定理、hardness、算法或开放问题。

# 2. Infer Before Asking 与最小 Worksheet

在写或改综述前先保守推断以下变量：目标 venue/venue family、paper type（method/theory/benchmark/system/application/survey）、main contribution type（algorithm/controller/framework/protocol/dataset/metric/theorem/system implementation）、target audience、review length，以及已有 validation（theorem/simulation/ablation/benchmark/real-system/case study）。只有缺失信息会实质改变结构、语气、引用策略或 claim strength 时，最多问一个紧凑澄清问题；默认先行动，不把常规假设转成审批。

在 prose 之前必须填写最小 S-R-L-H-G-M-C-V worksheet：

| 项目 | 必须写明 |
| --- | --- |
| Target scenario S | 目标任务、环境和约束 |
| Key requirements R | 可信方案必须满足的 3–5 个要求 |
| Literature routes L | 哪些功能路线解决哪些要求 |
| Hidden assumptions H | 每条路线成立所需的 support、oracle、数据、测量、可实现性等 |
| Structural gap G | 为什么现有路线不能共同满足 R |
| Missing object M | 缺失的是表示、机制、接口、理论、指标、基准还是框架 |
| Contributions C | 每项贡献填补 G 的哪一部分 |
| Validation V | 哪个 theorem、experiment、ablation、benchmark 或 audit 承担每条 claim |

G 和 M 必须分开。G 是联合缺失的能力，M 是承载该能力的具体对象。未命名 M 的 gap 仍是宣传句；命名 M 也不自动证明其存在或可行。

# 3. 五步段落模板与结构缺口

每个相关工作段落通常完成五步：

1. **Requirement**：一个可部署/可信方案必须满足 X 并保持 Y；
2. **Existing capability**：既有方法 A 有效处理 X；
3. **Hidden assumption**：其有效性依赖 H；
4. **Boundary**：在目标场景中 H 因何变得限制性；
5. **Bridge**：这推动一种能提供所需能力的机制/表示/框架。

这五步是推理骨架，不是机械复制的句子模板。综述结尾不能只是列“方法 A 有问题、方法 B 很慢、方法 C 没有理论保证”；应说明既有研究分别推进了哪些路线，但在目标场景下对 X/Y/Z 的隔离处理或隐含假设造成 R1/R2/R3 的持续权衡，最后点名 M。

结构 gap 必须是对“路线—假设—要求”的关系判断，不是模糊的“还需要更多研究”。对 UM，可以写某路线提供配置可行性但没有完整整数 schedule，某路线有必要 flow 但没有 shared ownership decoder，或某有限 audit 只能支持特定输入族；必须把这些关系绑定到来源和证据范围。

# 4. Contribution mapping

贡献不能是模块列表。每项贡献都应回答：如果没有它，哪个 gap component 仍未闭合？建议使用：

| Gap component | Contribution | Validation |
| --- | --- | --- |
| G1 | C1 | theorem / experiment / ablation |
| G2 | C2 | baseline comparison / benchmark |
| G3 | C3 | robustness / runtime / real-world test |

句式为“为处理某 gap component，提出某 contribution，使某 capability 成为可能”。对于 UM，C 需要注明是定义、定理、条件桥、反例、障碍、有限 exact audit、文献基线还是实现接口；V 需要说明是证明、程序重放、冻结证据还是 source-bound 文献对照。不能把一个支持必要条件的 V 写成充分性。

这与贡献地图资源相邻但不相同：贡献地图提供 `primary_claim`/`secondary_claims`/`non_claims`/`risks`/`reviewer_objections` 字段；本协议额外要求每个综述句把 gap、文献路线、隐藏假设和引用角色连接起来。

# 5. Claim-first 引用选择和 reference roles

不要先堆一批论文再拼综述。先写需要支撑的 claim，再为每条 claim 找来源：

| Claim 类型 | 应找的来源 |
| --- | --- |
| Problem importance | survey / application / deployment paper |
| A route is effective | representative method paper |
| A route has a limitation | limitation / failure / comparative paper |
| Current state of the art | recent high-quality paper |
| Direct competition | closest related method |
| Benchmark validity | dataset / benchmark / metric paper |
| Theory legitimacy | foundational theory / authoritative source |

每个引用还要赋予角色：`FND` foundational theory/basic definition、`SUR` survey、`REP` representative method、`SOTA` recent strong method、`COMP` direct competitor、`BOUND` boundary/failure、`BENCH` dataset/metric/evaluation、`THEO` theorem/proof tool、`APP` application/deployment、`ADJ` adjacent-field inspiration。没有清楚角色的引用应删除或降为待核候选。

引用句必须能回答该来源支持定义、能力、限制、比较、历史事实还是优先权。只有主题相近不代表支持当前句；摘要、二手综述或搜索结果不能替代直接来源，除非综述明确把它们标成 source-bound 和未核边界。

# 6. 检索流程与元数据检查

协议给出的简化检索流程是：

1. 从 seed papers 开始：最近竞争者、经典理论、最新 survey 和 benchmark；
2. backward trace，检查 seed 的引用；
3. forward trace，检查近期引用 seed 的工作；
4. 按 requirement 搜索，不只按方法名搜。例如同时搜索“real-time constrained control under uncertainty”“executable multimodal evaluation”“online calibration uncertainty downstream fusion”；
5. 直接搜索 reviewer 会想到的 direct competitors；
6. 只有确认来源确实支撑具体 claim 后才引用。

元数据方面，Google Scholar BibTeX 只能作初始导出，常见错误包括把 conference 当 article、缺 DOI、作者被写成 `et al.`、大小写保护丢失、作者分隔符不符合 BibTeX、venue 字段放错等。协议建议运行：

```bash
python3 problem-driven-literature-review/scripts/check_references.py references.bib
python3 problem-driven-literature-review/scripts/check_references.py references.bib --strict
python3 problem-driven-literature-review/scripts/check_references.py references.bib --online --title-search --strict
```

项目有 method/proper noun 时，增加 `--protected-title-term` 或 UTF-8 `--protected-title-terms-file`。若脚本报警，不能静默标准化；应对照出版社页、DOI landing page、Crossref、DBLP、PubMed、arXiv、IEEE/ACM/Elsevier/Springer 或目标期刊样式，并将未核 entries 保持 candidate 状态。

当前仓库的 `BibTeX引用元数据检查器解析、规则与 Crossref 边界` 资源已完整记录该脚本的 parser、required fields、duplicate key/DOI、title/author/page/year/DOI/venue hygiene、退出码和 Crossref 限制。它属于静态 metadata gate，不做 direct-competitor coverage、negative-claim hygiene、S-R-L-H-G-M-C-V 或“这条文献是否真的支撑当前句”的语义判断；本协议也没有在本轮执行脚本或发起在线请求。

# 7. 五类质量门

## 7.1 Direct-Competitor Rule

综述不能回避 reviewer 自然会想到的方法。每个直接竞争者至少写：解决什么、为何是强 baseline、为何在目标场景仍不足、是否有实验比较；没有比较时说明原因，而不是不提它。

## 7.2 Negative-Claim Hygiene

避免 `No existing work ...`、`Existing methods cannot ...`、`All previous studies ignore ...`。在检索有限时改写为“Few studies jointly consider ...”“This remains underexplored under ...”“Existing methods typically address X or Y, but not their coupling under Z ...”，并保留检索范围、时间、数据库/来源及未覆盖对象。

## 7.3 Review-Experiment Alignment

综述批评某个性质，论文就应测试、证明、讨论或明确限定它：

| 综述批评 | 预期验证 |
| --- | --- |
| Computationally heavy | runtime / complexity |
| Unsafe | safety margin / violation / proof |
| Overly conservative | detour / energy / activation frequency |
| Not robust | noise / disturbance / domain shift |
| Not executable | execution success / downstream acceptance |
| Not auditable | intermediate inspection / failure attribution |
| Calibration insufficient | parameter error / uncertainty / downstream result |

对 UM，类似地，称某桥“只能必要性”就需要把 decoder 缺口或反例写进 V；称某算法“位多项式”就需保存输入编码、运行和输出位长证据。

## 7.4 Citation Integrity

禁止发明 references、年份、题名、DOI、dataset、model name 或结论；快速变化领域要核近期模型、benchmark 和版本；每条引用必须支持句子中的具体 claim。reference metadata 要先检查，不能把 Google Scholar 手工格式当事实。

## 7.5 Reference Metadata Integrity

结构、重复、必填字段、DOI/year/URL、author separators、title capitalization 和 venue field 等由 checker 发出 issue；有争议时回到 publisher/DOI/Crossref 等来源。通过 checker 只能说明元数据满足当前规则，不说明论文内容、优先权或数学正确。

# 8. 按贡献类型组织综述

协议给出四类例子，强调类别由 output objective 和 contribution type 决定，不由应用名词机械决定：

* **Method/Algorithm**：task requirements → main routes → assumptions/trade-offs → 方法如何改变 trade-off → experimental/theoretical validation；典型 gap 是 A/B/C 可分别改善但无法在目标场景共同满足 R1/R2/R3。
* **Theory**：已有定理覆盖什么 → 需要哪些假设 → 本文放宽哪项 → 新定理在哪里适用；典型 gap 是 H1/H2 排除了目标系统。
* **Benchmark/Dataset**：既有 benchmark 测什么 → 哪项真实能力未测 → 新 benchmark 如何定义 task/metric/baseline。
* **System/Framework**：真实流程的 breakpoint → upstream 方法解决什么 → downstream 需要什么 → 缺失 interface → 模块边界与验证闭环。
* **Application/Deployment**：场景约束 → 一般方法为何不能直接迁移 → 本文做了哪些适配 → 真实实验如何证明部署价值。

对于 UM，理论对象应围绕模型假设、既有覆盖、放宽条件和适用域；计算/审计对象应围绕输出、证书、位复杂度和有限范围；不要把系统/benchmark 话语迁移成 theorem。

# 9. 最终清单与最短公式

定稿前逐项检查：

* 第一段是否从目标场景和核心冲突开始；
* 是否清楚 3–5 个关键要求；
* 文献类别是否由功能和假设驱动，而非方法名堆叠；
* 每条路线是否写 capability、assumption、boundary；
* 是否有一句综合 structural gap；
* 是否明确 M；
* 每项贡献是否对应 gap component；
* 每个 major claim 是否有 validation 或 discussion；
* direct competitors 是否覆盖；
* 是否避免 `nobody has done this`；
* 每条引用是否有清楚 role；
* 是否无发明、误用或装饰性引用；
* BibTeX/reference list 是否过了 metadata check，尤其是 Google Scholar 导出。

最短版本是：

```text
Define scenario S.
Derive requirements R.
Organize literature L by function and assumptions H.
Compress limitations into structural gap G.
Name the missing object M.
Make contributions C respond to G.
Support each claim with validation V.
```

目标不是证明某个方法天然优越，而是让读者看到：在目标场景下，论文填补的是既有路线留下的具体缺失对象，并且每项主张都有相称验证。

# 10. 与已有资料的去重与 UM 适配

与已归档的 `问题驱动文献综述S-R-L-H-G-M-C-V与引用证据边界--资料.md` 相比，本页首次完整读取 companion protocol；SKILL 页已保存核心原则和工具分流，本页新增 worksheet、五步段落模板、reference-role taxon、retrieval flow、metadata CLI、五类质量门、贡献类型示例和 final checklist。

与 `论文论证重构与主张证据对齐` 相比，本协议专注 related work/background 的来源选择、引用角色、直接竞争者和结构 gap；argument reconstruction 负责整篇稿件的 demand→bottleneck→mechanism→evidence→implication 故事线。与 `科研想法新颖性风险审计` 相比，本协议不做四层 novelty threat 或 reviewer attack，而是把已确认的文献 claim 绑到 source 和 role。与 `贡献地图` 相比，本协议增加 L/H/G/M 和引用闭环；与 `反防御审计`、`genre_profiles`、`TeX-safe polishing` 相比，它不改句子、文类或 TeX protected token，只判断综述证据是否承重。

对不相关机器综述的安全适配必须把 `S` 写成真实输入/场景，`R` 写成近似比、整数 schedule、sound FAIL、decoder、位复杂度等实际要求，`L` 写成 LST/ST、configuration LP、support/home/sink、局部矩等功能路线，`H` 写出共同容量、给定 oracle、无限精度或受限资格等隐藏假设，`G` 写成必要性/充分性、局部/全机、有限/全称之间的结构缺口，`M` 指向 decoder、统一余量桥或可组合接口，`C/V` 绑定正式定理、反例、程序或 source-bound 文献。

本轮没有执行搜索、BibTeX checker、Crossref、DOI 或引用覆盖率检查；没有取得外部论文或证明任何 UM claim。若没有完整参考集和可靠元数据，综述应保持 source-bound、candidate 或 needs-source，不能写“首次”“无人做过”或“已证明开放”。

# 11. 处置

本源处置为 `integrated` 资料资源：原文和 comparison notes 已保存，完整保留 S-R-L-H-G-M-C-V worksheet、五步段落模板、结构 gap/M 区分、claim-first reference roles、检索流程、BibTeX metadata 命令、direct-competitor/negative-claim/review-experiment/citation/metadata 五类质量门、贡献类型例子和最终 checklist。

协议没有执行搜索或引用检查，不创建 theorem、algorithm、gap、hardness、复杂度、实验结果或外部优先权；静态 metadata checker 通过也不等于引用支撑句子。任何当前 UM 文献综述应按该协议新建 evidence 和检索边界，并在 receipt 中写明实际核对的句子、直接竞争者和未覆盖范围。
