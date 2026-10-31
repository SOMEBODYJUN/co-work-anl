---
id: "unrelated-machines/problem-driven-literature-review-srlhgmcv"
kind: resource
type_tag: "资料"
title: "问题驱动文献综述 S-R-L-H-G-M-C-V 与引用证据边界"
status: "integrated-writing-and-review-resource"
truth_status: "workflow-reference-not-mathematical-evidence"
review_level: "full-source-read-cross-archive-writing-comparison"
scope: "literature review, related work, research-gap synthesis, citation roles, verification mode, and bounded evidence claims"
source_refs:
  - "clean:03f3dbe19b308eef3845:research/weighted_congestion_frontier/upstream/polish_skill/problem-driven-literature-review/SKILL.md"
  - "local:archives/unrelated-machines/tools/evidence/problem-driven-literature-review-20261031/original/SKILL.md"
  - "local:archives/unrelated-machines/tools/evidence/problem-driven-literature-review-20261031/comparisons/comparison-notes.md"
  - "local:archives/unrelated-machines/state/资料/创新框架候选、缺口与证据反证合同--资料.md"
  - "local:archives/unrelated-machines/state/资料/论文论证重构的主线、证据对齐与结构边界--资料.md"
  - "local:archives/unrelated-machines/state/资料/数学写作文类剖面与主张责任边界--资料.md"
  - "local:archives/unrelated-machines/state/资料/数学写作反防御功能审计与证据量词边界--资料.md"
  - "local:archives/unrelated-machines/state/资料/贡献地图模板与主张证据风险边界--资料.md"
  - "local:archives/unrelated-machines/state/资料/创新性审查技能的比较、风险与证据边界--资料.md"
source_identity:
  inventory_blob: "d38ad2e16af65005abb1a1922c7e986cb096d7e5"
  source_sha256: "16d6b89118cc838a613e08ba0de56361e5a40276343857a0692c67028426d592"
  source_size_bytes: 5574
  frozen_commits:
    - "68fad804ec5946cb296f77dc5b336308a66abf12"
    - "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/problem-driven-literature-review-20261031/original/SKILL.md"
  - "archives/unrelated-machines/tools/evidence/problem-driven-literature-review-20261031/comparisons/comparison-notes.md"
related_objects:
  - "archives/unrelated-machines/state/资料/创新框架候选、缺口与证据反证合同--资料.md"
  - "archives/unrelated-machines/state/资料/论文论证重构的主线、证据对齐与结构边界--资料.md"
  - "archives/unrelated-machines/state/资料/数学写作文类剖面与主张责任边界--资料.md"
  - "archives/unrelated-machines/state/资料/数学写作反防御功能审计与证据量词边界--资料.md"
  - "archives/unrelated-machines/state/资料/贡献地图模板与主张证据风险边界--资料.md"
  - "archives/unrelated-machines/state/资料/创新性审查技能的比较、风险与证据边界--资料.md"
---

# 问题驱动文献综述 S-R-L-H-G-M-C-V 与引用证据边界

## 来源身份、实读范围与处置

本对象完整实读 clean source `03f3dbe19b308eef3845` 对应的上游 `problem-driven-literature-review/SKILL.md`，导出文件为 5574 字节，SHA-256 为 `16d6b89118cc838a613e08ba0de56361e5a40276343857a0692c67028426d592`，inventory blob 为 `d38ad2e16af65005abb1a1922c7e986cb096d7e5`。原字节保存在 [SKILL.md 原文证据](../../tools/evidence/problem-driven-literature-review-20261031/original/SKILL.md)，逐项比较记录保存在 [comparison-notes.md](../../tools/evidence/problem-driven-literature-review-20261031/comparisons/comparison-notes.md)。冻结索引中记录的基线提交为 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`。

处置为 `integrated` 资料资源。源文件是文献综述和相关工作写作/审查合同，不是 unrelated-machines 的定义、算法、证明、反例、近似比、复杂度或外部优先权证据。源文件要求另读 `references/literature_review_protocol.md` 才能得到完整 worksheet、段落模板、reference-role 表、元数据检查、质量门槛和按贡献类型的示例；该 companion 未在本 claim 中认领或实读，因此本页只登记技能正文提供的规则，并把 companion 留作后续来源，不能把未读内容写成已验证的协议细节。

## 核心链条：S-R-L-H-G-M-C-V

源文件把文献综述定义为证明目标论文为什么有必要，而不是按方法名堆引用。最小论证链是：

```text
S requires R.
Literature L solves parts of R under H.
H breaks under S, producing gap G.
We propose C to close G and validate it by V.
```

这里的八个字母具有不同责任：

| 符号 | 责任 | 写作时必须回答 |
| --- | --- | --- |
| S | 场景（Scenario） | 目标任务、环境、约束和输入域是什么？ |
| R | 要求（Requirements） | 一个可信方案必须满足哪些性质、输出和资源边界？ |
| L | 文献路线（Literature lines） | 既有工作按什么功能路线解决 R 的哪些部分？ |
| H | 隐含假设（Hidden assumptions） | 每条路线要成功，必须假设哪些支持、数据、oracle、可实现性或测量条件？ |
| G | 结构缺口（Structural gap） | 为什么现有路线不能同时满足 R？缺的是哪项联合能力？ |
| M | 缺失对象（Missing object） | 哪个具体表示、机制、接口、理论、指标、基准或框架能承载缺口？ |
| C | 贡献（Contributions） | 每项贡献填补 G 的哪一部分，作用范围是什么？ |
| V | 验证（Validation） | 哪个定理、证明、反例、消融、实验、基准或审计承担每条主张？ |

G 与 M 必须分开。G 是“联合缺失的能力”，例如无法同时处理共同容量、真实整数输出和 sound failure；M 是提供这项能力的具体对象，例如某种 decoder、接口、证明桥或受限基准。只写“现有工作有 gap”而不命名 M，会把动机变成宣传句，无法接到贡献和验证。反过来，给出一个对象名称也不能自动证明 G 存在。

## 适用范围与验证模式

该技能用于 literature review、related work、introduction background、research-gap synthesis、reference selection 和 citation-role assignment，优先按问题和功能组织，而不是按年代或方法名称平铺。它与相邻技能的分工是：新颖性风险、危险 baseline 与贡献可防守性归 `idea-novelty-auditor`；稿件故事线、章节结构和贡献—证据重构归 `paper-argument-reconstructor`；TeX 安全润色归 `paper-polisher`。这些分工避免用一份综述技能替代新颖性审查、论证重构或源到输出保真检查。

源文件有 default mode 与 verification mode。若输入段落是本技能自己起草，可以按 S-R-L-H-G-M-C-V 组织和改写；若另一工具或技能已经起草 related work/background，则必须进入 verification mode：不覆盖其措辞，检查 citation integrity、reference metadata、direct-competitor coverage、negative-claim hygiene，以及命名的 structural gap 是否由引用和比较真正支持；只报告偏差，在硬规则被破坏时才原位收紧一处。这个边界对当前清洗尤其重要：保留已有正文和失败信息，不能把更漂亮的综述重写成未经证据支持的更强优先权主张。

## 从问题到文献路线的工作步骤

源文件给出的顺序可以落成以下可审计工作流：

1. 先确定 venue、paper type、贡献类型、读者和已有验证；只有这些会改变结构时才问一个澄清问题。
2. 在写 prose 前填最小 S-R-L-H-G-M-C-V worksheet，先把对象、量词和验证层级写清。
3. 按功能路线和隐含假设组织文献，例如“解决哪项共同约束”“依赖什么 support/oracle”“输出是否可解码”，不要做方法名时间线。
4. 把多条局限压缩成一个结构缺口 G，同时命名具体缺失对象 M；不能用“还需要更多研究”代替。
5. 把每项贡献 C 映射到 G 的一部分，把每条 claim 映射到验证 V。贡献如果没有对应 gap，验证如果没有对应 claim，都应标记风险。
6. 采用 claim-first reference selection：先写要证明的文献事实或比较主张，再找来源；每个引用都记录其 role，而不是只放一个 BibTeX key。
7. BibTeX 若由 Google Scholar、别的工具或手工复制而来，必须运行 `scripts/check_references.py`；能够联网时加 `--online` 做 DOI/Crossref 检查，需要警告阻断时加 `--strict`。Google Scholar 导出只能是草稿，不能当权威元数据。
8. 运行 direct-competitor coverage、negative-claim hygiene、review-experiment alignment、citation integrity、reference metadata integrity 五类质量门槛；任何未覆盖直接竞争者、无人承重的负面断言或与实验不对齐的综述句都要标出。

## 引用、负面断言与来源角色

该源的独有增量不是“多列几篇论文”，而是把引用当作主张的证据接口。一个文献句应至少能回答：它支持的是定义、能力、限制、比较、历史事实还是优先权？其元数据是否经过 DOI、出版社、Crossref、DBLP、PubMed、arXiv 或目标期刊样式核对？来源是否直接覆盖目标句，而不是只在摘要或二手综述中相似？

“没有人做过”“首次解决”一类负面或优先权句不能凭空写。若无法核验近期文献，应搜索或要求用户提供参考集合，并把句子收紧为有边界的观察，例如“在所检查的路线和输入假设下，未找到同时满足 R 的实例”。这类收紧仍需保留检索范围、时间点、数据库/来源和未覆盖对象；不能把“未找到”升格为全体文献的不存在定理。

综述与实验必须互相对齐：如果相关工作句声称某路线在某失败机制下受限，实验或反例应能展示这个机制；如果贡献把某缺口说成已关闭，至少应有定理、可复现程序、有限 exact audit 或其他相称证据。source-bound 文献核对只能支持“源文确实如此说”或“元数据通过某检查”，不能升级为 unrelated-machines 的数学结论。

## 对 unrelated-machines 清洗的适配

在当前 unrelated-machines 目标上，综述页面必须把以下内容写在同一证据边界内：

- 场景 S：二进制非负有理 processing times、`∞` 禁边、空任务、零处理时间、完整整数 schedule 和任意合法 tie；若目标是六提供者的有限单位客户模型，则保持其独立身份，不把客户覆盖模型的结论迁移进机器调度。
- 要求 R：除了近似比，还要说明逐机可行性、共同容量状态、真实可执行输出、失败证书、decoder、位复杂度和输入总位长中哪些是硬要求。
- 文献路线 L：LST/ST、configuration LP、support/home/sink、局部矩或有限 probe 等分别覆盖哪些部分；每条路线的支持范围和可行输出不能被综述摘要替代。
- 隐含假设 H：是否有共同容量、给定 support/oracle、可用 decoder、无限精度、外部 solver、受限资格、完整历史或只读摘要；假设破坏时要记录失败机制。
- 缺口 G：例如能证明局部 feasibility 却不能给完整整数 schedule，或有限 audit 能发现一个障碍却不能支持一般 hardness；缺口必须是结构关系，不是模糊的“算法还不够好”。
- 缺失对象 M：可能是 sound decoder、统一余量桥、可组合配置接口、能保持位复杂度的认证过程或可比较 benchmark。它必须由后续 claim 和 V 承重，不能只放在 related work 里。
- 贡献 C 与验证 V：定理/证明、条件桥、有限 exact audit、最小反例、障碍、原始文献核对和程序 replay 分别是什么层级；不能把旧图、摘要、一次运行或引用列表当成一般性结论。

对 `UM-TARGET-v1` 的写作示例只能作为结构适配。即使综述指出共同状态、真实输出或位复杂度的缺口，也不能由这份资料推出一般 `(2-\varepsilon)` 算法、hardness、优先权或开放问题已解。任何受限结论必须把输入族、量词、证据来源和失败边界写在主张附近。

## 与已有清洗对象的比较、去重与接续

与“创新框架候选、缺口与证据反证合同”相比，本页增加了文献路线 L、隐含假设 H、引用 role、direct-competitor coverage 和 review-experiment alignment；创新 framing 更强调候选主张的 falsifier，而本页更强调用来源支持每个文献事实。两者都要求 G 具体可定位，不能用宣传性 gap。

与“论文论证重构的主线、证据对齐与结构边界”相比，本页专注 related work/background 的来源选择和比较结构；论证重构则把真实需求、技术瓶颈、机制、证据和含义串成整篇稿件。综述输出可以给重构提供 L/H/G/M，但不能替代章节级 claim-to-evidence 表。

与“数学写作反防御功能审计”相比，本页在引用句和负面断言层面前置证据检查；反防御审计仍负责句子级 Keep/Rewrite/Compress/Delete/Flag，并保护定义域、量词、必要否定和失败条件。与“数学写作文类剖面”相比，本页不决定一个对象是定理、反例、障碍或有限实验；它只保证综述没有把这些类型混写。

与“贡献地图模板”和“创新性审查技能”相比，本页提供 claim-first references 与 direct competitors 的文献闭环；贡献地图继续记录每个贡献的唯一承重义务，创新性审查继续处理直接/相邻/危险工作和 reviewer attack。来源角色、写作结构和数学 truth status 必须保持分层。

后续接续应先认领并实读 `references/literature_review_protocol.md`，再为具体 UM 对象填写 S-R-L-H-G-M-C-V worksheet。若没有实际参考集、搜索结果或原始文献，不应补写外部比较；若只有源文和摘要，状态保持 source-bound。任何新增文献综述都应在 evidence 中保留原文和检索边界，在 receipt 中说明哪些句子实际核对、哪些直接竞争者仍未覆盖、哪些主张仍需验证。

## 明确缺口与停止条件

本资料未执行 `check_references.py`，未访问 DOI/Crossref，也未声称完成最新文献检索。它没有编译 TeX、运行算法、生成 schedule、证明近似比或验证任何外部 priority。若后续工作无法取得完整 protocol、可靠元数据或直接竞争者来源，应登记 `blocked`/`needs-source`，而不是用假想引用填空。综述清洗完成只表示这一来源的工作流边界已准确归档；开放数学问题和未证实候选仍需各自的证明、反例、实验或原始来源。
