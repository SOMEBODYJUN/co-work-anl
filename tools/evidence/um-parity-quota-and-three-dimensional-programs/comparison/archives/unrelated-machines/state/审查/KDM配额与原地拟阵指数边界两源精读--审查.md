---
id: "unrelated-machines/kdm-quota-and-on-site-matroid-exponential-two-source-review"
kind: "review"
type_tag: "审查"
title: "KDM 配额与原地拟阵指数边界两源精读"
status: "restricted-quota-and-representation-boundary"
summary: "高维 KDM 配额源确认需求树的直接 packing 恒等式、公共/私有资源低配额逃逸和 LST 事实不自动给 UM hardness；原地拟阵源证明同一基集上表示所有容量族的拟阵数量至少 ceil(C(k,r)/C(k-r-1,r))，并在完整读后核对覆盖设计、严格阈值、固定辅助收缩和 audit。两者均不升级一般 UM-TARGET。"
source_refs:
  - "clean:879441ebddc3ee11cc6a"
  - "clean:006c7de2e930e45bfaf8"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/kdm_high_dimensional_quota_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/knapsack_matroid_exponential_review.md"
---

# 来源与读域

`879441ebddc3ee11cc6a`（SHA `b5fc3538dca8062cdc36a075b3e62f80b746a30ba3a12f7444e26a90512b5ac5`）审高维 KDM quota/需求树源、LST paper facts 和条件 hardness 量词；`006c7de2e930e45bfaf8`（SHA `66915ca7a772061521147b4c0018fe209cb18f0588f9b9c4a8ac917d041a190c`）先独立重构原地拟阵指数表示下界，再读作者冻结正文、代码与 canonical 第9节并重跑 Fraction audit。两源均 clean show 全文实读，证据/manifest 在 `archives/unrelated-machines/tools/evidence/quota-matroid-20261031/`，receipt 草稿在 `cleanup/workspaces/Boss2/quota-matroid-receipts-20261031.json`。

# 1. 高维 KDM quota 恒等式与边界

对根需求 q、超边节点需求 K、资源终端 DAG，评分 b 的树选取 s 条超边，每条至少 `ceil(Kb)` 资源。资源单父条件给 t-packing；反向由 t-packing 构造需求树，因此

`b*=max_t min(ν_t/q, t/K)`。

公共/私有资源族中可出现 `ν_K=1` 而 `ν_t=q`（`t<K`），故完整 matching 比例与需求树值可分离。两标签资源的低配额引理在 `2t≤K` 时阻止单层共享/私有 selector 强制唯一标签：若两差集都够大取差集，否则差集等势且交集足够分两份。该逃逸是接口障碍，未提供全局 decoder。

审查核对 LST Theorem 3.1 的 CSP→KDM 最大匹配保真、Theorem 4.1/4.3 的随机稀疏化假设；它们没有 KDM→Santa 或 KDM→R||Cmax 的完整归约。已有“低于2 makespan算法蕴含 Santa 算法”是算法性蕴含，不能反向写作 hardness。

读后追加发现旧条件反面存在明确异议：`q=10,K=5,delta=1/5,gamma=4/5`、每组唯一标签是同一五资源束时，八组取一资源不可能，但需求树值仅 `b*=1/5<delta`；正确阈值至少涉及 `max(delta,gamma)`，例如增加 `gamma≤delta` 才可能恢复旧式条件。另，固定 `rho<2` 本身不足以否定 UM-TARGET；需要对每个固定 ε 给出绝对 `(2−ε)(1+η)<β` 区分与可靠 NO decoder。故 KDM 旧条件不能登记为完成 hardness。

# 2. 原地拟阵指数表示下界

原地基集 `E=A∪{h}`，`|A|=k`，tiny 元素权 `1/k`，h 权 `1−r/k`，`1≤r<k/2`。可行族 `I={S:w(S)≤1}`。若 q 个同一基集拟阵均包含 I，且共同独立集都满足严格 `w(S)<2−2r/k`，则

`q ≥ ceil( C(k,r) / C(k−r−1,r) ) ≥ exp(r(r+1)/k)`。

证明：A 在每拟阵中独立，故每个拟阵至多一个含 h 的回路 `h∪D`；否则 circuit elimination 产生 A 内回路。所有 `|R|≤r` 的 `{h}∪R` 可行，故 `|D|≥r+1`。每个边界坏集 `{h}∪S`、`|S|=k−r`、权恰 `2−2r/k` 必被某回路覆盖；一个 `D` 覆盖至多 `C(k−r−1,r)` 个 S，计数得比值。对数乘积和 `−log(1−u)≥u` 给指数下界。

固定 `B<2` 时取 `r=floor(αk)`、`α<min(1/2,(2−B)/2)`，严格共同上界 ≤B 触发该计数；显式输入长度 `Θ(k log k)`，因此拟阵数量超任意固定位长多项式。若 B<1，连权1的 A 都不可行，合同本身不可能。等号阈值不能沿用同一坏集层；辅助元素、扩展基集、投影、并集和 signed/动态规则均超出原地声明。

# 3. 作者读后与 audit 范围

完整读后核对最小测试数为覆盖设计数 `C(k,k−r−1,r)`：任意回路补集扩成 block 不减 witness，反向每 block 用 `U_{r+1,r+2}` 加自由元素实现。网格阈值在 `[w0−1/k,w0)` 内保持同一最小数；端点 `k=2r+1` 分母为1、列出全部 `r+1`-sets 的回路拟阵使下界取等。固定独立私有辅助 `U` 且接受条件为 `U∪S` 在同一 transversal matroid 中独立时，接受族正是 contraction `(N/U)|_E`；共享/动态辅助被明确排除。

本轮重跑 `audit_matroid_capacity.py` 的 `run()`，与冻结 JSON 返回对象精确相等：16 组参数、2674 回路、109351 回路-witness 检查通过；端点 augmentation 仅 `k=3,5` 穷举，来源没有把此范围夸大为全部端点。canonical 第9节也实际全文读并复跑，确认仅该节在本轮覆盖，未把整文件 hash 当作第1–8节复审。

# 4. 关系、用途与未解边界

两源都展示“受限接口内部的精确数量/配额边界”，但身份不同：KDM 是需求树/资源配额与条件 hardness，原地拟阵是静态表示数量下界。它们不提供一般 UM 的近二 hardness，也不限制引入辅助空间、扩展 gadget、物理 decoder 或不同算法路线。拟阵计数不依赖 P≠NP；KDM 条件反面需要修正阈值和绝对量词后才可继续。

处置为 `restricted-quota-and-representation-boundary`。引用时必须保留 strict `<` 阈值、原地同基集、非空/端点限制、KDM `max(delta,gamma)` 修正及 LST 事实的导入性质；有限 audit 不能替代普遍证明，亦无实现、外审或新颖性认证。
