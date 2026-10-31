---
id: "unrelated-machines/unitforest-leaf-hall-threshold-two-source-review"
kind: "review"
type_tag: "审查"
title: "单位森林与叶 Hall 阈值两源精读"
status: "typed-forest-and-marginal-projection-read"
summary: "两份 review 确认 unit-readout 的 mandatory pruned-forest IFF、半密度全深度 3/2 实际 assignment、精确叶 hitting q^h/最大 r-free 补集，以及 threshold leaf Hall 的共同叶边际运输。全部依赖显式完整树、唯一 incoming、unit-slot/叶域与指定 partition；不升级一般 UM。"
source_refs:
  - "clean:1478744b5a736559f7df"
  - "clean:67caa876d911ca47b51e"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/unit_readout_pruned_forest_boundary_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/threshold_leaf_hall_consistent_marginals_path_projection_review.md"
---

# 读域

`1478744b5a736559f7df`（SHA `805ca7add480936faa8071eda372bf046b7108e9b0f4422dad76768be78e1dfe`）审 unit-readout 三合同：一般 arity、half-density 3/2、叶 hitting q^h/最大 r-free；`67caa876d911ca47b51e`（SHA `caa8284fdda6656f1612c7781f5b69f9858ff58f4f05b07b5d9ab1bfd8d82242`）审 threshold leaf Hall、consistent marginals 和 path projection。两源均 clean show 全文实读，证据/manifest 在 `archives/unrelated-machines/tools/evidence/unitforest-threshold-hall-20261031/`，receipt 草稿在 `cleanup/workspaces/Boss2/unitforest-threshold-hall-receipts-20261031.json`。

# 1. Mandatory pruned-forest IFF 与半密度合同

显式完整 k-叉树、每内部点唯一 incoming unit、每条原 job 仅 parent/child 或所属 clause unit 资格。实际 `C<2` assignment 中 active 内部已有 unit1，留父 small 数≤`floor(k(C−1))`，故至少 `r=ceil(k(2−C))` 条原下传；递归选这些已下传 child 得 mandatory r-pruned forest。反向给 forest 用原边/slot 注入，active 负载 `1+(k−r)/k≤C`，inactive 全 parent 负载1，所有原 jobs/未选轨/重复 branches均计入。

额外 half-density `d_c≤2A_c` 时，一次共同 Hall matching 先于 forest 剪枝覆盖全部 jobs：incoming 半片占首槽，small 半片两两成槽，clause ports 分到 `ceil(d_c/2)` 个真实 units；active 内机≤`1+floor(k/2)/k`，无 incoming 机≤1，外 unit≤1。k1、A0、空变量和边界均旁路；这是给定 typed domain 的实际 C1+/3/2 contract，不是一般 UM。

# 2. 精确叶 hitting 与 dummy 逃逸

令 `q=k−r+1`。叶集合 H 命中每个完整深 h 的 r-pruned subtree，当且仅当补集 D 不含 r-pruned subtree。good 递归：叶 good 若 blue，内部 good 若至少 r 个 good child。根 good 提取纯 blue r-subtree；根 bad 至少 q 个 bad child，递归提取纯 red q-subtree。故最小 hitting 数恰 `q^h`，最大 r-free 补集恰 `k^h−q^h`；r=1/r=k/h=1/k=1 边界均正确。显式树后序 DP+固定 child extraction 为 O(|V|)，但不对仅二进制 k,h 压缩树承诺 poly 输出。

若真实 occurrence 叶集合 `R` 满足 `|R|<q^h`，dummy 补集必含完整 r-pruned subtree；等号不能如此，t-pruned blocker 给锐界。该结论只处理叶树集合，不保证 dummy 外部资源容量、跨 rail 联合 packing 或物理调度 decoder。

# 3. Threshold leaf Hall 与 consistent marginals

threshold unit-demand 的严格 `b<epsilon` 判别、指定 partition 投影和新 `D_+` 只列 positive neighbors；共同叶边际运输只共享同一套 leaf-edge marginals，不共享所有 core-state 或完整 matching law。弱合同可用单 matching，强化 `(MC)` 一般需混合；zero lambda、beta=1、非邻居、zero jobs及 conditional rows均需显式保留。`q_t` 含 unit core 系数，parking tail 为一，不是趋零伪尾。

canonical threshold正文给出 `V=1/t`、ordinary `OPT=2−1/t`、t=2 的 180-machine/201-job fixture；有限软件重放核指定矩阵、边际等式和混合片段，不提供 exact SDP oracle 或一般调度 finder。路径投影只证明共同叶边际，不能把“共享边际”误写成共同完整 leaf matching law，也不能将原 partition 变化后的等式静默复用。

# 4. 关系与未解边界

unitforest IFF/half-density 是实际 assignment/mandatory forest 的 typed 合同；leaf hitting 是组合树的纯 set 计数；threshold Hall 是指定 partition 下的 marginal projection。三者不可合并成一般 source hardness、真实 shared ownership decoder 或 near-two gap。外部经典 majority/BCG 等仅作模型背景，未认证全球新颖性/外审；一般 UM-TARGET 仍 open。

处置为 `typed-forest-and-marginal-projection-read`。后续引用需注明 explicit full tree、unique incoming、unit slots、half-density/partition、共同边际而非共同 law、dummy outside capacity 未证明及显式输入复杂度。
