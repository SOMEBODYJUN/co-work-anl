---
id: "unrelated-machines/conditional-leaf-hall-v2-path-projection-qt-read-after-20261031"
kind: review
type_tag: 审查
title: "条件叶 Hall v2 路径投影与 Q_t 家族五源读后"
status: integrated-source-read-scoped
truth_status: "restricted-relaxation-projection-and-explicit-family-obstruction"
review_level: "full-source-read-with-author-proof-comparison-no-independent-reconstruction"
scope: "conditional leaf Hall v2, adjacent path projection, and Q_t family; no actual-YES hardness or generic UM result"
summary: "Exact-only v2 与作者证明共同给出指定 core/leaf 分区下 R1-R2 的必要性、路径提升投影恒等式和 Q_t 的 V=1/t 家族；本页保留其前提、证明来源和未外推边界，不把作者稿当独立审查。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_general_repair_conditional_hall_exact_v2.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_general_repair_conditional_hall_exact_v2.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_general_repair_conditional_hall_proof.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_general_repair_conditional_hall_proof.md"
source_ids:
  - "ab22bc6b9a4c44ffd915"
  - "4e43084dee453f78f3cb"
source_sha256:
  - "828c6a178729bf4ce03855ef8e1f53d9efaf85fb9aaa680a6cd4c5a0e012bb4f"
  - "357c762c9481183dd3f0f5fdf9631beddad931bb80977e753287d6bf662d73e6"
evidence_paths:
  - "../../tools/evidence/conditional-leaf-hall-v2-20261031/source/ab22bc6b9a4c44ffd915.md"
  - "../../tools/evidence/conditional-leaf-hall-v2-20261031/source/4e43084dee453f78f3cb.md"
related_objects:
  - "条件叶Hall投影与一致边际四源证明读后--审查.md"
  - "一致条件叶边际仍无福利下界--障碍.md"
---

# 阅读范围与身份

本页逐字读取两个冻结来源。`ab22bc6b9a4c44ffd915` 是 v2 Exact-only 规格（12,455
字节），明确只给定义和定理陈述；`4e43084dee453f78f3cb` 是相同 v2 的作者证明稿
（13,006 字节），补充证明路线但明示不是独立 Exact-first 重构。两路径在
`legacy-cleanup` 与 `main` 的文件版本相同，原字节和 SHA 保存在 evidence 目录。
因此“通过”只表示本次来源级数学比较未发现内部矛盾；不把作者证明算作第二张盲审票。

# 1. 模型、普通矩阵与值恒等式

菜单有有限资源集 (U)、非空组集 (G)，每组显式 indexed states (S_g)，每个状态
系数 (p_{gsu}ge0) 总和为 1；零系数、重复状态、unused resources 和显式零 incidence
均保留。对不交 bundles 定义

\[
v_g(B)=\max_{s\in S_g}\sum_{u\in B}p_{gsu},\qquad
V(Q)=\max_{(B_g)\text{ disjoint}}\min_g v_g(B_g).
\]

完整 ordinary flat 矩阵保留所有原 incidence jobs：状态私有根端时间为 (p_{gsu})，
资源机端为 1，selector 为 unit job；未选状态的 jobs、zero jobs 和 unused data 不因
选状态而删除。来源的双向调度读法给出

\[
\operatorname{OPT}(P(Q))=2-V(Q).
\]

一方向把达到 (V) 的 bundle 导出到资源机，其他 jobs 留在私有根；反方向从峰值
(C<2) 的完整调度读取每组选中根的正导出，资源机至多接一个 unit job，得到价值至少
(2-C) 的不交 bundles。(C=2) 用全私有端点闭合；这只是该 flat 矩阵的值恒等式，
不是一般 UM 结论。

# 2. 阈值叶、R1--R2 与其实际范围

给定二进制 (arepsilon\in(0,1])，令

\[
H_g(\varepsilon)=\{u:\max_s p_{gsu}\ge\varepsilon\},\quad
b_g(\varepsilon)=\max_s\sum_{u\notin H_g}p_{gsu}.
\]

当 (b_g<\varepsilon) 时，价值至少 (arepsilon) 等价于命中 (H_g)；这给出精确
threshold-unit-demand 分类。指定一组 core (C) 和 leaf (L)，core 状态有
(lambda_{cs})、(z_{csu})（(0\le z\lelambda)），并要求

\[
\sum_u p_{csu}z_{csu}\ge\varepsilon\lambda_{cs}.
\]

全局叶流 (y^0) 每个 leaf 行和为 1、每资源列加上 core (z) 不超 1；每个 core-state
还有独立条件叶流 (y^{cs})，其行和为 (lambda_{cs})，列约束只含该 state 的
(z_{csu})，不含其他 core 的用量。来源证明：若 (V(Q)\gearepsilon)，取一组达到值的
state 与不交正 incidence，叶重资源选一份完整匹配，即得 R1--R2。该 LP 是必要多项式
放松，不是充分性、实际 allocation 或一般近似算法。

特别要保留 partition 前提：若自动把所有 threshold-unit-demand 原组移入 (L)，
路径投影的 core 集已改变；来源不允许把“指定的 C/L”静默换成自动分区。

# 3. 相邻路径的精确投影

旧资源 (u) 有 (d) 个不同正 core group 邻居时，改成各组自己的 port
(u_1,\ldots,u_d)，并新增 (d-1) 个相邻两端 leaf。给 old basic point
((\lambda,z))，令每组在 (u) 上的总 core 使用为
(eta_i)，旧列给出 (sum_i\beta_i\le1)。选择一个有理 hole 分布
(pi_i\geeta_i,sum_ipi_i=1)，把每个 leaf 匹配到 hole 左右端的平均；于是全局
叶行恰为 1、每个 port 列为 (1-pi_i)，与 (eta_i) 合计不超 1。对某一 core-state
取其自有 port 为 hole，匹配乘 (lambda_{cs})，条件列只留该状态的 (z)，故无须除以
(lambda)，零 lambda、(d=0,1)、zero/unused 数据均闭合。

反向把一个路径块的 (d-1) 叶行与 (d) 个端口列相加，恢复旧列
(sum_ieta_i\le1)。在同一指定分区下，完整 R1--R2 投影到原 ((\lambda,z)) 的多面体
恰为旧 basic polytope；来源还给出保值方向，故

\[
V(Q^{\rm path})=V(Q),\qquad
\operatorname{OPT}(P(Q^{\rm path}))=\operatorname{OPT}(P(Q)).
\]

这是 fractional projection 与实际 normalized value 的等式，不能改写为 full CONFIG/PSD
合同，也不产生跨 core 条件匹配的共同 joint schedule law。

# 4. (Q_t) 明确族与 gap

取 (t\ge2,D=t^2)。主组 (M) 的每个状态在一行 (D) 个 (g_{a,j}) 上各权
(1/D)；每个 (H_{a,j}) 有 unit home (g_{a,j}) 和在 (t) 个 parking
资源 (A_{a,h}) 上各权 (1/t) 的状态。路径叶只承担新增 ports，core 保持指定分区。
来源给出的 (lambda,z) 与 global/conditional path flows 可行，但实际值为

\[
V(Q_t)=1/t,qquad \operatorname{OPT}(P(Q_t))=2-1/t.
\]

上界：若 (M) 取得 (q) 个 home 资源，至多挤出 (q\) 个 helper，而这些 helper
需要不同 parking resources，故 (q\le t)，主组价值至多 (q/D\le1/t)。取 (q=t)
并让被挤 helper 用互异 parking resources 达到下界。(t=2) 的最小示例为 17 cores、
40 leaves、64 resources、116 states、180 machines、201 jobs，(V=1/2,
OPT=3/2)。来源没有声称在所有 counterexamples 中最小。

固定 (arepsilon>0) 取 (t>1/\varepsilon)，得到该 relaxation 在自己的阈值下可行而
实际 (V<\varepsilon)。这是放松的 integrality/consistency 障碍，不能升级为 actual-YES
hardness、NP-hardness、近二近似下界或六人 half 反例。

# 5. 处置、差异与接续

两源的独有内容为：Exact v2 的完整定义、变量/约束、路径 general projection 与
(Q_t) 精确值；作者稿给出 one-hole matching、全局/条件流的证明细节、完整原 jobs
保留和位复杂度计数。它们共同支持本页的受限结论，但没有独立重构，也没有作者 checker
的独立运行。与已有四源 v3/MC 读后页的关系是版本增量：本页登记 v2 的原始 source
IDs，后页登记后续 MC 一致边际与 t=2 Fraction audit，不能互相替代。

第三阶段可建立 `v2 relaxation → path projection → Q_t obstruction` 关系；仍开放
actual-YES promise、full CONFIG/PSD 等价、一般 UM 算法与 hardness。原 source 的
`UM-TARGET-v1` 明确保持 OPEN。
