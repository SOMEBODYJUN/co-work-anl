---
id: "unrelated-machines/rooted-dag-transit-route-composition-review"
kind: "review"
type_tag: "审查"
title: "根DAG守恒扩区与路线拼接有限审查"
status: "reviewed-finite-scope-open"
summary: "逐源核对守恒扩区/非单位搜索审计与共同容量路线拼接审计，确认独有证据、依赖关系、量词边界和未实现接口；不将有限运行升级为一般算法或反例。"
legacy_ids:
  - "7434abd5a798786e1550"
  - "384a14e7fa00781e7e4f"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/rooted_dag_transit_branch_audit.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/rooted_dag_transit_branch_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/route_composition_review_audit.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/route_composition_review_audit.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/rooted_dag_congestion_flow.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/rooted_dag_congestion_review.md"
---

# 审查范围与方法

本轮完整读取两个冻结来源 JSON，而不是只看文件名、标题或旧图：7434abd5a798786e1550 的 12,244 字节守恒扩区/非单位分叉审计，以及 384a14e7fa00781e7e4f 的 3,871 字节共同容量路线拼接审查。两者的来源路径、SHA-256、双冻结提交和运行字段均逐项核对。随后读过现有 rooted_dag_congestion_flow 正文、rooted_dag_congestion_review 审查、既有有向需求桥/共同拥塞三源审查、共同容量路线拼接关联入口，并搜索后续正文中关于固定支撑、非单位点、token bridge、forest/menu 拼接和 moments 的引用。

证据副本保存在 [rooted-dag-route](../../../../tools/evidence/private-tree/rooted-dag-route/)；本审查与计算对象都只引用其精确字节，不把本地临时读取记录当成源版本。两份源均在 legacy-cleanup 提交 68fad804ec5946cb296f77dc5b336308a66abf12 与 main 提交 aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c 中存在相同内容。

# 守恒扩区审计的逐点判断

## 已被既有正文正确解释的内容

现有共同拥塞正文已给出新合同的全称前提：非根输入上界 K、k_v>=2K 的高点无条件输出、低点 1<=k_v<=2K-1 的共同守恒、低根输出和零点无输出；它还给出一次拆点整数流提取、固定支撑双向搜索、K 单调性、1/(2K-1) 层宽锐界、只枚举高点的 2^h 参数算法及其复杂度。这些证明不由本批 JSON 重复承担。

7434 的独有贡献是把规范与独立实现的有限覆盖固定下来：规范侧 9,496 全部有序 DAG、63,736 父选择、28,488 full-support K 案例和 4,179 合法提取；随机侧 seed=7,102,026 的 500 个图、13,938 个父选择和 500 个任意根重标号。独立 oracle 给出同样 9,496 个 exact cases、5,350 个 fixed-support cases（695 可行）、504 个 old-to-new 裁流案例、695 个 free-extension 案例，并报告 1,516 个最小值交叉与 1,390 个支撑交叉。这里是有限实现核验的逐点映射，而不是对全体 DAG 的新证明。

## 独有边界与量词修正

单边序列 K=1,...,100 及两个巨大 K 例的 1/(2K-1) 值只说明已记录合同的锐界族确实被程序打到；它不说明一般 root-tree optimization 的 hardness，也不说明 UM-TARGET 的统一常数不存在。unit_merge 与 old_certificate_requires_trimming 证明的是版本接口差异：旧合同的 f 需要裁流/重配后才可能成为新合同，不能把字段名换掉就声称新合同。terminal_root_remote_dead_high 保留了“根终端不等于支撑中所有点免费”的量词；这与正文中根单点提取和固定 W 搜索的区别相容。

huge_nonroot_arbitrary_root、deep_unit_corridor 以及约 10^100 的输入只验证二进制大数和任意根/深走廊边界。它们没有限制 h 无界时的 2^h 代价，也没有提供多项式的支撑选择。源 limits 明确否认 global novelty、polynomial algorithm when h unbounded、UM-TARGET solution 和外部审查认证；审查保留这些否定。

# 路线拼接审计的逐点判断

384a 把 route-composition 接口拆成四个独立有限范围。其 code_sha256 与 forest_two_boundary_menu.py、rooted_dag_token_bridge.py 的 dependency_sha256 已核对；因此“独立审查”只能理解为使用精确代码指纹重算/接口核对，不能称外部同行评审。

- 菜单区有 48 个正单任务、1,885 个组装实例、14,425 个分配和 4 个零目标；scope 只保证单任务两个正端点覆盖及组装恒等，不给菜单核心近似。
- 流区有 1,076 个实例、8,956 个树子集和 1 个根终端；图限 n<=4 拓扑 DAG，非根非汇点需求1、汇点可独立 terminal/deadend、根有四个需求（含102位大数）。m=2,...,8 的 full_ratio=1、frozen_ratio=1/m 是有限 alias fixture，不能写成全输入比例下界。
- bounded_demand 区有 9,176 个实例和 87,776 个树子集，非根正需求仅 {1,K}、K∈{2,3}，汇点还可取0。它是小图标准最大流数量回算，不是一般 scheduling 进展。
- moments 区有 548 个非空 Boolean 支持分布、30 个 rank_zero、1,032 个额外仿射候选、fake PSD rank=2、fake PSD Boolean candidates=0；八个列出的 numbers/delta/s/feasible fixtures 必须按原值保留。源明确没有 moment extractor 和 truth-promise verifier，因此没有可外推的矩提取或真实性检查器。

# 与旧对象的差异、重复处置和开放缺口

既有计算对象和审查已经保留共同拥塞合同及其一般证明；本批不是 duplicate 的空壳，因为它新增了两份证据的完整计数、实现/依赖哈希、旧到新版本裁流边界、巨大需求/随机根 fixtures、路线拼接的 moments 假 PSD 搜索和明确的菜单/流/有界需求适用域。它应作为“有限检查/实现依赖”对象与既有根树流对象相连，而不是再创建一个相同的 UM-DAG-CONGESTION-FLOW-v1 定理。

审查后保持以下量词：

1. 固定 W、K 的证书失败，只否定该合同的给定支撑/拥塞组合，不否定原 DAG，也不构成一般调度 NO 证书。
2. 只枚举高点的 2^h poly(B) 程序在 h 无界时仍是指数；有界 K 或 K=2,3 的实验不改变这一点。
3. alias ratio、single-edge sharp、fake PSD 和随机样本都是有限证据；不升级为 hardness、全局近似下界、外部新颖性或概率定理。
4. route composition 的菜单/森林接口保留 token 任务身份和需求量词，不能直接把它当成根DAG共同流的普遍扩展。

未实现接口仍是：从一般 unrelated-machines 输入找到有用 W 与统一 K；免除高点子集枚举；把路线拼接提升为菜单核心近似；给 moments 提供带 truth promise 的验证器；以及主目标 UM-TARGET-v1。上述缺口与既有正文的 OPEN 标签一致，本批没有产生反例或解决方案。

# 处置与接续

两源均处置为 retained/integrated：数学一般证明继续由既有 rooted_dag_congestion_flow 与其审查承担，7434 和 384a 作为可追溯的有限证据与接口范围层保留。后续第三阶段若建立关系，应使用“有限核验”语义，引用两个 JSON 副本及其 SHA，并同时引用旧正文中对应的共同流合同；不应写成“运行通过所以算法存在”。
