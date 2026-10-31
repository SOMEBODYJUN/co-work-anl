---
id: "unrelated-machines/shared-ud-tiny-home-v4-potential-rounding"
kind: "algorithm-review"
type_tag: "资料"
title: "shared-UD tiny-home v4 势函数与完整回填"
status: "proved-under-k1-k2-typed-scope"
summary: "v4/v4b 在单 state outer、互异 homes、own-unit helpers、B-only fallback、ε=15/16 exact-threshold leaves 且 k≥2 ν≤1/(16384k²)（k=1解除ν约束）域中，给出 profile fractional potential、stable matroid updates、FW、prefix-flow 和完整原 jobs 回填，保证实际 19/10 分支或 sound baseline。仍不扩 multi-outer、home overlap、general UM 或 true hardness。"
source_refs:
  - "clean:21215d01058e9a688caa"
  - "clean:fa6e0b78d63a7f8dc785"
  - "clean:b9f329c0d9ac6fe95d5b"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_true_hardness_shared_ud_tiny_home_k2_v4_exact_first_attack.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_true_hardness_shared_ud_tiny_home_k2_v4b_author_read_after.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_true_hardness_shared_ud_tiny_home_v4_canonical_actual_read.md"
---

# 来源身份和输入域

三份来源分别是 v4 Exact-first、v4b 作者 read-after、canonical actual-read。对象为 single-state outers、全局互异 homes、每个 home 一个 own-unit helper、helper fallback 全部在 B、额外 leaves 也仅在 B；固定 epsilon=15/16、exact-threshold leaves；k≥2 要求 ν=max home weight≤1/(16384k²)，k=1 无 ν 约束。zero incidences、duplicate states、unused resources 和所有原 jobs 保留。

| clean ID | 原路径 | SHA-256 | 大小 | 实读性质 |
|---|---|---|---:|---|
| `21215d01058e9a688caa` | `history/source/notes/unrelated_machines/sol_true_hardness_shared_ud_tiny_home_k2_v4_exact_first_attack.md` | `69036ac605760a193093869fc2af26b6fed35d76ed1c49f776185d17e9089f10` | 12,401 B | Exact-first 独立算法重构 |
| `fa6e0b78d63a7f8dc785` | `history/source/notes/unrelated_machines/sol_true_hardness_shared_ud_tiny_home_k2_v4b_author_read_after.md` | `4d2d398ea494e66f5397d5c4f0e527282fc6515e03a46d257353c4cc4ea4fba4` | 10,463 B | v4b 作者完整 read-after |
| `b9f329c0d9ac6fe95d5b` | `history/source/notes/unrelated_machines/sol_true_hardness_shared_ud_tiny_home_v4_canonical_actual_read.md` | `c0168657da6cee7ea8b42a5be96fb19a5e41d40f52258b2078fdff67d625df9d` | 3,291 B | canonical 新增段 actual-read，确认量词/软件边界 |

证据原件、manifest 在 `archives/unrelated-machines/tools/evidence/shared-ud-tiny-home-v4-20261031/`，回执草稿在 `cleanup/workspaces/Boss2/shared-ud-tiny-home-v4-receipts-20261031.json`。

# 1. 值身份、叶 matroid 和 baseline

原 normalized menu 的最大最小 integral allocation value 为 V，完整 ordinary matrix 满足 `OPT=2−V`：selected state 的 bundle 正质量 incidence 导出，其他 payload 留 private；反向 C<2 时 resource unit capacity 给 selected-state bundles 互不相交且 value≥2−C。无 full leaf matching 时，任何 value≥ε allocation 都给每叶一枚 H_l resource，故 V<ε，baseline C≤2 满足 19/10 ratio。

若 leaf—B 资格图有 full matching，定义 vacancy matroid A（删去资源后仍能匹配全部 leaves）及 dual M。helper fallback incidence 取 M 的平行扩张，独立性就是资源不重复且剩余 B 仍能给所有 leaves 完整 matching。matching oracle 只做普通 bipartite matching，不藏 profile optimization。

# 2. k1 greedy 与 k≥2 stable profile

k=1：按固定 helper 顺序在 fallback states+empty 上做 submodular greedy，f(O)≤2f(G)。若 welfare W<1/4，则 actual V<ε，baseline sound；W≥1/4 时 Good threshold 1/10 给 outer home mass≥1/6，直接回填。

k≥2：维护每 helper 一个原 fallback state 和当前 M-independent incidence set I。对 fixed positive h_i，weighted matroid greedy 给每个候选 state 的最大 independent set与增益 δ_j≥0。次模性和删/加 basis 的 stable exchange 给

`sum_i h_i L_i* ≤ 2 sum_i h_i L_i + sum_j δ_j`。

若 V>18/19，分析真实 allocation 提取同一共同参考 bundles I*，所有 outer weighted welfare `L_i*>324/361`。势函数为

`Phi(L)=sum_i[-(3/10−L_i)_+² + b L_i]`，`b=1/(50k)`。

每次真实候选 Φ 增益>1/(100N) 才采用；梯度 2-Lipschitz。nu≤1/(16384k²) 和同-outer loss 误差给 `sum_jδ_j` 上界；合并停止不等式与 reference 下界，若某 L_i<19/100 即矛盾。k=1 无二次误差，直接得到 L_1>19/100。作者和独立稿均逐式支付 same-outer helper 挤出，不把 fractional profile optimum 偷换成 actual schedule。

# 3. FW、prefix-flow 和 19/10 实际回填

作者 v4b 的 profile backend 用 FW 近似每个 fixed profile 的 concave potential，步数 O(k/ξ)，matching linear oracle 每轮有 rational bit bound；stable optimal face coupling 只作存在证明。终止时 no candidate gain 反证 actual V≤18/19，故 baseline sound。

LP/FW 成功时，outer claims 聚合到最大 resource coefficient `a_iu`，按资源排序做 prefix lower-bound circulation。原 fractional flow 给 circulation 可行，整数性一次性产生所有 outer claims 与 leaves 的同一完整 matching；每 outer loss≤ν，故 weighted welfare>19/100。Good helpers threshold=1/10，outer 收相应 homes，未选 helpers 回 own homes，叶用剩余 B matching 与原 attaining states，所有 groups quality≥1/10。

完整 ordinary 输出保留所有原 selectors、selected incidences、unselected state payload、duplicate states、zero jobs 和 unused resources；selected roots load≤19/10，unselected roots≤1，resources≤1。若 baseline 则所有 incidence 留 private，峰≤2；unit selectors 给 OPT≥1。因此 typed 域内确定性 19/10 合同成立。

# 4. 计算和范围

Potential range、每步增量阈值、候选 state 数、matching 次数和有理运算位长均显式 polynomial；k1/k2 分支均 worst-case deterministic。canonical actual-read 确认 vacancy rank 是叶数、不是 |B|，以及软件只有限核 exchange lemma，未运行 FW/profile search/tiny instance/prefix flow/all jobs。

本记录不证明：multi-state outer、home overlap、无 home auxiliary groups、general leaves/non-UD extras、一般 UM、source hardness、全球新颖性或端到端实现。它与 raw SH3/NSW/one-outer Exact 分开，不能把 typed shared-UD 结果静默扩域。

# 本轮处置

三源完整实读，比较 Exact-first、v4b proof、canonical新增段；原件和 manifest 在 evidence，正文归档为资料，回执草稿单列，暂不 checkpoint/done。
