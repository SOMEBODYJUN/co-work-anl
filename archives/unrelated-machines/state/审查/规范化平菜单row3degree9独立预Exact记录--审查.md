---
id: "unrelated-machines/normalized-flat-row3-degree9-independent-preexact-review"
kind: review
type_tag: 审查
title: "规范化平菜单 row≤3/degree≤9 独立预 Exact 记录"
status: independent-preexact-provenance-retained
truth_status: "forward-transfer-reconstructed; formal-v3-theorem-existing; CONFIG-gap-paper-fact-unverified"
review_level: "full-9637-byte-pre-exact-source-read-and-cross-archive-comparison"
scope: "row≤3, item positive support≤9 normalized additive-SC checkpoint before reading the released Exact"
summary: "该 checkpoint 在读取 normalized-menu Exact 前独立闭合 FSLP→tree/port→state-dummy 的正向转移、row≤3/item support≤9 计数和 CONFIG(1) 正向证书，明确真实 OPT≥1 promise 与 general SC gap 尚未解决。现有 v1/v3 定理与 Proof 审查承载正式双向桥；本页保留先验推导、版本顺序和外部 PaperFact 限制。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/row_three_degree_nine_sc_independent_pre_exact_research_v1.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/row_three_degree_nine_sc_independent_pre_exact_research_v1.md"
  - "clean:f4965985e118ff2e0736"
related_objects:
  - "../定理/规范化平菜单的CONFIG与正支撑LP双向保持--定理.md"
  - "../审查/规范化平菜单Exact与Proof版本核验--审查.md"
  - "../审查/归一化菜单福利与配置证书双源审查--审查.md"
  - "../资料/加权菜单Santa值桥与不相关机转换--资料.md"
  - "../资源/Santa-Claus超图匹配与配置LP五分之一界--资源.md"
source_sha256: "b33a165fd22dd77b3ce8c93317a9754c52a60675a2d6366edbd9e99f0668d0f6"
source_size: 9637
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/normalized-flat-row3-independent-preexact/original/row_three_degree_nine_sc_independent_pre_exact_research_v1.md"

# 1. 时间顺序与读取边界

`row_three_degree_nine_sc_independent_pre_exact_research_v1.md` 是 2026-10-18 的独立 pre-Exact checkpoint，大小 9,637 字节，源 SHA-256 为
`b33a165fd22dd77b3ce8c93317a9754c52a60675a2d6366edbd9e99f0668d0f6`。它明确：当时尚未读取 root 提供的 normalized-menu FSLP-preservation Exact、rainbow 策略或其他 agent 推导；先前只知道一个独立 selector-tree/port-path 记录。该稿完成后才允许读取新 Exact，因此其“独立”是历史先验，不能倒写成作者 Proof 或外审。

现有正式对象 `规范化平菜单的CONFIG与正支撑LP双向保持--定理` 及 `规范化平菜单Exact与Proof版本核验--审查` 已整合 v1/v3 Exact/Proof、tree/port-path、state-dummy 和 row≤3/degree≤9 的完整双向结论。本页不再创建同义定理，而是保存 f496 的先行推导和其明确未完成项。

## 2. f496 先行闭合的正向转移

### 2.1 从显式 CONFIG(1) support 到 normalized full-state menu

给普通 additive SC 的显式有理 CONFIG(1) support：每 agent 的每个配置 S 有总值 W_(i,S)>=1，配置概率 lambda_(i,S) 和资源 usage 不超过 1。将配置概率归一化为和 1，并为每个配置建 indexed menu state，保留原资源身份、定义 `p_(i,S,u)=v_(i,u)/W_(i,S)`。得到 state 总质量严格 1、p<=v，且 lambda 给 FSLP 的 resource capacity。

若该 normalized menu 有每组 state 的 pairwise-disjoint partial bundle 质量 c，则原 SC 按同一 items 分配的 utility 至少 c；因此菜单 integral V 不超过原 SC OPT。checkpoint 明确：它只使用显式 support，不能把未知最优 allocation 或 promise OPT>=1 当作 support 选择器。

### 2.2 FSLP

FSLP 变量 lambda_(g,s)>=0，每组和为 1，每资源 u 上所有包含 u 的 state lambda 总和不超过 1。这里容量是正支撑 membership 的 0/1，不按 private weight 计 resource capacity；state 权只保证质量为一。

### 2.3 Tree 正向 lift

对每组按 lambda 选择一片 leaf state：root-to-leaf 路径 internal 选 child-own singleton，末叶选原 state，off-path 顶点选 own singleton。每个 fresh own resource 恰使用一次，原资源 usage 保持旧 lambda；概率由子树前缀和精确计算，多项式位长。K=1 直接原 state、无 own/no new group。该稿只闭合正向 FSLP lift；tree 反向、完整实际值双向和正式证明由后续 v1/v3 Exact/Proof 承担。

### 2.4 Port-path 正向 lift

对资源 u 的 d 个 incident groups，令 a_j 为第 j 组全部含 u states 的 lambda 质量，sum a_j<=1。选 hole 分布 h_j>=a_j、sum h=1；hole h 下 helper r 在 r<h 选左 port，r>=h 选右 port。helper usage 恰为 1-h_j，加旧 usage 后每 port 不超过 1。d=1 无 helper，d=0 保留 unused resource；所有概率由有理前缀和得到。tree 先于 path，目标 row≤3、resource cross-group degree≤3，且既有 selector-tree/path 合同声称 integral V 保持。

## 3. State-dummy SC forward bridge

每个 flat group g 有 K_g<=3 states，建 K_g 名 state-agents，每个原 resource 是普通 item，agent(g,s) 对原 state 项取 p_(g,s,u)。再建 K_g-1 枚只对该组 agents value=1 的 private dummy items。每个 state-agent row total 为 `1+(K_g-1)=K_g<=3`；原 item 正 support 不超过 3 groups*3 states=9，dummy support 不超过 3。

给 FSLP lambda：state-agent 以 lambda 取完整原 state support，其余概率均匀分给 dummy singleton；每 agent 配置概率和一、每 dummy 使用恰一、旧 item usage 仍由 FSLP 控制，构造 SC CONFIG(1)。K=1 不做除零。

给任意目标 allocation：每组只有 K_g-1 dummy，至少一名 state-agent 未拿 dummy，其效用来自原 state resource bundle；抽出每组该 agent 及其原 bundle，得到 flat one-state disjoint partial allocation，质量不低于目标 min。反向 flat 分配给选中 agent，其余 agents 各拿一个 dummy。该桥保存实际 integral V，而不是把 fractional CONFIG 当 actual allocation。

结合 selector-tree/port-path 的正向 lift，得到 row≤3/item support≤9 的普通 SC 像；checkpoint 只认证正向和给定证书的转换，不声称对 general SC promise 已有 constant algorithm。

## 4. CONFIG 障碍和 Q_D 族边界

f496 先行稿指出：若导入一般 SC CONFIG LP 的无界 integrality-gap PaperFact，则上述 forward transfer 可把 CONFIG(1) 可行但 actual V 任意小的实例带入 row≤3/support≤9 子类，排除“CONFIG LP(1) 本身足够 round 固定 c>0”的合同。但该稿只直接核到 Bansal–Sviridenko *The Santa Claus Problem* 的摘要/作者页（general arbitrary valuations 的 Omega(sqrt(m)) gap）；ACM 全文请求返回 403，未读 gap construction/proof。因此这一应用只记录为外部依赖，不能把它写成仓库内部已证明的显式 gap family。

它还记录自足 Q_D pattern：一个 main group 有 D 个 state，每 state 在 D 个 g_(a,j) 上权 1/D；D² helpers 各有 g_(a,j) 或 A_a 的 unit singleton。任意正 main bundle 在同一 row 至多取一个 g，实际 V=1/D；FSLP main lambda=1/D、helper home/parking lambda=(1-1/D,1/D) 可行。经 N/tree、state-dummy 及 SC path，得到 row≤3、最终 item positive degree≤3（中间 state-dummy image≤9）、CONFIG=1/actual=1/D，规模按显式 D 多项式。

Q_D 是 CONFIG obstruction，实际值低于一；它不满足 actual OPT>=1 promise，不能写成 near-two hardness 或一般 SC/UM impossibility。现有 `规范化平菜单的CONFIG与正支撑LP双向保持` 正式定理已承载该族和 scope；本 pre-Exact 仅保留先行发现顺序。

## 5. 与正式 Exact/Proof、文献和未完成项的关系

现有 `规范化平菜单Exact与Proof版本核验` 把 f496 之后的版本分为：v1 normalized menu/FSLP/tree/path/state-dummy/Q_D；v2 general SC unit-helper path；v3 restricted-flat machine CONFIG(1)↔FSLP 和成熟组合。Proof v3 已补齐 flat CONFIG 反向、SC path 正阈值双向和 t=0 empty 分支；f496 的正向推导是其历史先验，不替代 v3 Proof。

`加权菜单Santa值桥与不相关机转换`、`归一化菜单福利与配置证书双源审查` 记录 normalized flat menu 到 Santa/UM 的值桥及完整原 jobs；`Santa-Claus超图匹配与配置LP五分之一界` 是外部 Haxell/AFS 资源说明。它们共同要求显式 state support、零项/unused/duplicate 边界、阈值一和 all-original-jobs 回填；不把外部 PaperFact 变成一般算法。

f496 明确未完成：

* 真正 `OPT>=1` promise 下固定正常数 minutility 的 deterministic bit-poly 算法；
* 一般 SC CONFIG gap 的仓库内部自足显式 family 或复杂性证明；
* 将给定 fractional support 当作未知 optimum/support solver；
* 任何 general UM near-two hardness、P!=NP 结论、生产代码或新颖性认证。

它还记录 BCG2009 PDF 的 degree-three path 归约与 Bamas 2025 restricted-assignment阅读：这些 primary 只作模型边界，不能直接解决 arbitrary row/support SC。该 checkpoint 没有小样本枚举或软件优化实验。

## 6. 处置

处置为 `integrated` 的 independent pre-Exact provenance：原字节 evidence 保留，f496 的 FSLP/tree/path/state-dummy 正向推导、row≤3/support≤9 计数、Q_D CONFIG 障碍和外部 PaperFact 限制写入本页并链接正式 v1/v3 定理。第三阶段可建立“先行独立重构→后续 Exact/Proof”边；不建立第二定理，不把 CONFIG 障碍当 actual OPT>=1 promise 反例，也不把 Bansal–Sviridenko 摘要升级为仓库内部 gap 证明。
