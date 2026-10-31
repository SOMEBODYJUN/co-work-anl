---
id: "unrelated-machines/normalized-xos-threshold-size-independent-exact-review"
kind: review
type_tag: 审查
title: "归一化 XOS 阈值规模独立 Exact 审查续页"
status: independent-review-retained-as-version-provenance
truth_status: "independent-v1-proof-reconstruction; existing-obstruction-targeted; no-new-general-impossibility"
review_level: "full-8463-byte-source-read-and-existing-obstruction-comparison"
scope: "UM-NORMALIZED-XOS-THRESHOLD-MENU-SIZE-OBSTRUCTION-v1 independent Exact-only review"
summary: "独立审查逐步重构同一资源宇宙中归一化非负 XOS 菜单的 support-cover 计数下界，确认 K >= binom(2t,t)/binom(2t-r,t-r) >= 2^r 及 d=0/t=1/整数端点；现有障碍对象已整合该结论和作者/canonical 版本，本页保留独立先验、proof 细节和可选 r_* 强化，不创建第二个定理。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/normalized_xos_menu_threshold_size_exact_v1_independent_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/normalized_xos_menu_threshold_size_exact_v1_independent_review.md"
  - "clean:822bd98ce829c6df1695"
related_objects:
  - "../障碍/归一化XOS菜单阈值规模下界--障碍.md"
  - "../定理/分数重匹配与归一化XOS稳健缺口边界--定理.md"
  - "../审查/Santa受限桥与归一化菜单双源审查--审查.md"
source_sha256: "6d9c8d6627b4686606ae0d2e4535268d79a710478adae30f7bff3af79dbd407d"
source_size: 8463
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/normalized-xos-threshold-independent-review/original/normalized_xos_menu_threshold_size_exact_v1_independent_review.md"

# 1. 来源身份和审查边界

`normalized_xos_menu_threshold_size_exact_v1_independent_review.md` 是
`UM-NORMALIZED-XOS-THRESHOLD-MENU-SIZE-OBSTRUCTION-v1` 的 Exact-only 独立重构，大小 8,463 字节，源 SHA-256 为
`6d9c8d6627b4686606ae0d2e4535268d79a710478adae30f7bff3af79dbd407d`。原字节已复制至 evidence 目录并核得同一 SHA。审查稿明确只读取指定 v1 Exact，不读取作者 Proof、其他 agent 推导、repo 文件或 Work/Git，也没有软件运行、外审或新颖性认证。

现有 `归一化XOS菜单阈值规模下界--障碍` 已保存同一对象的 v1 Exact、作者 Proof v2 read-after 和 canonical §4–6 read-after；该对象承载正式规模障碍。本页不重复登记数学定理，而是把独立审查者的证明路径、端点核对和 proof-before-author 先验作为版本 provenance，并把其额外的 `r_*` 支撑观察标成可选强化。

## 2. 独立重构的精确模型

资源宇宙 U 有 2t 个资源，固定有理 0<eta<1、d=floor(eta t)、r=d+1。显式 XOS 菜单有 K 个 indexed additive clauses；每 clause 系数非负有理，整个 U 上总量恰为 1，允许零系数和重复 indexed clauses。要求同时满足：

* 每个 t-subset T 的 XOS 值恰为 1；
* 每个大小至多 d 的 subset B 的 XOS 值不超过 eta。

审查稿严格保留全体 t-subsets 和全体 small subsets 的量词，不将它们缩为 reachable bundles、实际 allocation 或抽样集合。它还保留“归一化是 clause 级总量为 1”的前提，不把额外资源、玩家、全局耦合或隐式表示放进同一接口。

## 3. 逐步 proof reconstruction

### Support 必须包含在 unit t-set 中

对 clause s 令 `A_s={u:w_(s,u)>0}`。由于系数非负且 clause 总和为 1，若某 t-set T 的值 f(T)=1，则取到最大值的 clause 必须在 T 上收集全部质量，故 `A_s subseteq T`；反向若 `A_s subseteq T`，该 clause 在 T 上值就是 1。因而 unit t-sets 正好是至少包含一个 clause 正 support 的集合。

### tiny 阈值强制 support >= r

若某 support 大小 m_s<=d，则它本身是 small 集合但该 clause 值为 1>eta，矛盾。归一化还保证 support 非空；因此每个 unit-witness clause 的 support 至少 r=d+1。d=0 时仍只用 support 非空得到 r=1，不伪造空集大小至多零的 clause。

### Covering-family 计数

若 r<=m_s<=t，一个 clause support 覆盖的 t-sets 数为

`binom(2t-m_s, t-m_s) <= binom(2t-r, t-r)`.

若 m_s>t，该 clause 覆盖零个 unit t-sets。所有 `binom(2t,t)` 个 t-sets 必须被某个 clause support 覆盖，故并集上界给出

`K >= binom(2t,t) / binom(2t-r,t-r)`.

该比值只是下界，不声称每组参数均达到；重复 supports、overlap、重复 indexed clauses 和全零 clause 都不能改善覆盖上界。反向给定 r-subset covering family，在每 support 上均匀放 1/r 的 clause，即构造满足 unit/tiny 条件的归一化菜单；因此最小菜单数可等价为该 covering-family 问题，但不把 covering oracle 误称为短输入算法。

### 指数因子

对 1<=r<=t，

`binom(2t,t) / binom(2t-r,t-r) = product_(j=0)^(r-1) (2t-j)/(t-j) >= 2^r`.

每因子不等式只用 j>=0，无需 Stirling、概率独立性或枚举全部 subsets。固定 eta 时 r>=floor(eta t)+1，故资源数 2t 增长时 clauses 指数增长；审查稿明确这不是对逐项输入 bitlength 的 `2^(Omega(L))` 断言。

## 4. 端点、可行性和输入规模核对

独立审查额外逐项确认：

* t=1 时 d=0、r=1，两个 singleton clauses 足够且 K>=2 正确；
* d=0 时最小有效 K 是 t+1（singleton clauses 命中所有 t-sets），Exact 的比值下界可以松但不错误；
* r=t 时每个 t-set 只能由自身 support 覆盖，K>=binom(2t,t)；
* 全体 t-sets 各列一个均匀 1/t clause，构成非空可行菜单，证明条件族不 vacuous；
* 添加全零 clause 不提高非负 XOS 值，不能降低有效 indexed clauses 数；
* 原加性玩家 2t 个资源、每项 1/t 的短输入长度为 O(t log(t+1))，但显式归一化 clauses 仍需指数输出；固定 eta 时这是显式输出规模障碍，不是所有变化 eta 或隐式表示的统一不可能性。

## 5. 可选 r_* 强化（保留为审查观察）

独立稿在主 PASS 之外给出支持集的简单强化：令

`r_* = max{1, ceil(d/eta)}`.

当 d>0，取任一 clause 的 d 个最大正系数；它们质量至少 d/m_s，而 tiny 条件使这和不超过 eta，因此 m_s>=ceil(d/eta)。d=0 仍用 support 非空。于是同一 covering count 给

`K >= binom(2t,t) / binom(2t-r_*, t-r_*)`.

固定 eta 时 t-r_* 为常数，审查稿指出可得到约 `4^t / poly_eta(t)` 的强化。现有障碍对象的 canonical §3 已有相同的 k=ceil(d/eta) 精度修正和余数分析；故本页把 r_* 视为独立 reviewer 的重构增量和 provenance，而不是另一个正式 Exact 或新的 hardness claim。

## 6. 与现有对象的分工和禁止外推

现有障碍对象已完整保存 v1 Exact、作者 Proof v2 和 canonical §4–6 的模型、证明、版本修正及 scope：它是正式的 normalized XOS menu-size obstruction。本独立审查的作用是确认 v1 结论可在不读取作者 Proof 的情况下逐步重构，并把 d=0/t=1/整数组合数/输出规模边界写清楚。

与 `分数重匹配与归一化XOS稳健缺口边界` 的关系仅是相邻接口：后者研究给定显式 clause list 的 fractional rematching、unit-FSLP 和未实现 deterministic rounding；本障碍研究的是从短逐玩家加性描述直接生成同宇宙、全 unit/tiny 保真的显式 clause list。它不能反向否定显式 XOS 算法。

本来源和既有障碍均不推出：

* 一般 Santa Claus 或 unrelated-machines 的 NP-hardness/近二下界；
* normalized YES/NO source 的全局归约；
* 允许额外资源/玩家、reachable-only 保真、放宽 unit sets、未归一化 clauses 或隐式可计算表示时的菜单规模下界；
* canonical source §1–3 SC value bridge 的结论，本来源同样没有读取它。

## 7. 处置

处置为 `integrated` 的独立审查 provenance：保留原字节和独立 proof reconstruction，链接现有 `归一化XOS菜单阈值规模下界--障碍` 作为唯一正式数学对象；r_* 只作可选强化观察，不新建 theorem 或 hardness object。第三阶段可建立“independent exact review / confirms support-count boundary”边，不能建立一般不可能性或外审边。
