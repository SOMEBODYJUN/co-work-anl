---
id: "unrelated-machines/multi-outer-tiny-home-author-proof-v1-read-after-20261031"
kind: "review"
type_tag: "审查"
title: "多 outer tiny-home 作者证明 v1 读后与完整算法范围增量"
status: "integrated-author-proof-read-after"
truth_status: "full-source-read-scoped-19-over-10-proof-with-finite-backend-separated"
review_level: "clean-show-full-read-cross-archive-comparison"
scope: "UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-19-10-APPROX-v1 author proof"
source_refs:
  - "source:e15dcf3e8976443630af:history/source/notes/unrelated_machines/sol_general_repair_multiouter_single_state_tiny_home_19_10_author_proof_v1.md"
source_sha256: "ce05c7d5fb99d78da44a802578ca33c5ba383b15f6fe0c3a64424ff088c00332"
evidence_paths:
  - "../../tools/evidence/multi-outer-tiny-home-author-proof-v1-20261031/original/sol_general_repair_multiouter_single_state_tiny_home_19_10_author_proof_v1.md"
related_objects:
  - "多outer双资源后端与tiny-home算法边界有限审查--审查.md"
  - "归一化门控菜单v2三源精读与13-8算法版本审查--审查.md"
  - "../障碍/私有昂贵叶的工作量与固定凸势近二边界--障碍.md"
---

# 多 outer tiny-home 作者证明 v1 读后与完整算法范围增量

## 1. 来源身份和与 Exact-first 的时序

本次完整读取 `history/source/notes/unrelated_machines/sol_general_repair_multiouter_single_state_tiny_home_19_10_author_proof_v1.md`。
来源 ID 为 `e15dcf3e8976443630af`，大小 17,024 字节，SHA-256
`ce05c7d5fb99d78da44a802578ca33c5ba383b15f6fe0c3a64424ff088c00332`；原文保存在
`tools/evidence/multi-outer-tiny-home-author-proof-v1-20261031/`。
作者稿明示其对应 Exact-only 源的 SHA 为
`38c85ffed433edc9742f2e523ae39c820dc315454262a498ff8386b0b6cc001a`，并说明该稿在
Exact-first 独立重构之前不提供给 reviewer；因此本页是 author-proof read-after，不能
称 statement-first 盲证明，也不把作者身份抹平。

现有《多outer双资源后端与 tiny-home 算法边界有限审查》已承载同一 v1 的规范、
两资源后端和有限重放；本源的独有内容是作者证明的完整承重链：共同 primitive-SA1
可行性、weighted winner oracle、floored rational MW、整块 helper 方差、两资源 CE
平方势，以及所有原 jobs 的 19/10 回填。处置为 **integrated-author-proof-read-after**，
不新建第二个算法对象。

## 2. 定义域和 `OPT=2-V` 桥

输入是多个 single-state outer，每个 helper 有一个 unit home、若干 normalized fallback
states、共享 B 资源；home 权满足
`0<w_j<=delta=1/(4096 k^4)`，每个 outer 的 home 权和为 1，所有 indexed states
和零 incidence jobs 保留。对互不相交的 fallback bundles 定义 group value，`V` 是所有
groups 最小值的最大化。

作者 proof 重复并完整写出：

\[
\operatorname{OPT}(P(Q))=2-V,
\qquad 0\le V\le1,
\qquad 1\le\operatorname{OPT}\le2.
\]

正向从每组 attaining state 的 bundle 外送对应 incidence，全部其余 jobs 留 private，
使选中 private 负载至多 `1+(1-v)`；反向若 `C<2`，每 resource machine 至多一个
unit incidence，从 selector 所在 state 读出互不相交 bundle，值至少 `2-C`。这两个
方向均以完整 selectors、未选 states、零 jobs 为前提；有限输入的离散资源分配保证最大
值达到。若固定 LP 不可行，源给出 `V<15/16`，全-private baseline `C<=2`，故
`C/OPT<32/17<19/10`。

## 3. 固定阈值共同 primitive-SA1 LP

作者 proof 不是 SDP 或 CONFIG oracle，而是固定 `epsilon=15/16` 的有界二阶 rational
SA1 系统：primitive 是每 indexed state 的 A 和每 listed incidence 的 Z；base rows
包括 state partition、boxes、gates `Z<=A`、resource capacities 和
`sum_u pZ>=epsilon A`，并保留每行与同一 primitive 或其 complement 的乘积，使用
`X^2=X`。变量和 row 数关于显式输入二次/多项式，标准确定性有理 LP 给出不可行或
多项式位长的精确可行点。

若 `V>=epsilon`，对每组取达到阈值的 state/bundle，置相应 A/Z 为 1，其余为 0，
故所有 lifted rows 可行；这证明不可行推出 `V<15/16`，而不是把分数 LP 点当成整数
allocation。作者还明确没有 PSD、unit CONFIG、额外 U、精确 SDP 或实际 allocation
oracle。

从共同点的一阶矩提取中，own singleton 的 gate/quality/box rows 给
`E A_j0=E Z_j0`；每 outer 的 fallback mass `f_j` 满足 `f_j>=x_j`，质量约束为

\[
\sum_{j:i(j)=i}w_jf_j\ge\epsilon,
\quad
0\le\zeta_{jsu}\le\alpha_{js},
\quad
\sum_up_{jsu}\zeta_{jsu}\ge\epsilon\alpha_{js},
\quad
\sum_{j,s}\zeta_{jsu}\le1.
\]

`alpha=0` 时 gate 强制所有 `zeta=0`，所以没有 0/0；零 incidence 可在 LP 有正 claim
但丢弃只减少资源使用，不改变 quality。

## 4. Weighted winner oracle 与 `1125/2048`

每个 helper 独立选择 fallback state 或 empty，随后只对所选 state 的正 incidences
请求资源。给 outer 权重 `lambda`，资源按实际请求者的
`lambda_i w_j p_jsu` 排序，固定索引打破平局；未请求但 state 已选者不参与 winner。
对阈值 z，helper 的请求概率 `a_j(z)` 跨 helpers 独立且 `sum_j a_j(z)<=1`，因此

\[
1-\prod_j(1-a_j(z))
\ge(1-e^{-1})\sum_ja_j(z)>(5/8)\sum_ja_j(z).
\]

按有限 score levels 积分并使用质量约束，作者得到
`lambda·g(lambda)>= (5/8)epsilon^2=1125/2048`。winner 期望是显式有理：
给定候选 `(j,s)`，其在资源 u 胜出的概率为

\[
\zeta_{jsu}\prod_{h\ne j}
\left(1-\sum_{t:(h,t)\prec(j,s)}\zeta_{htu}\right),
\]

同一 helper 的不同 state 互斥，只乘一次。算法按显式 state/requester 数计算，未枚举
所有 helper profiles；这是 v1 proof 的核心可执行接口。

## 5. Floored rational MW、整块方差和 CE

固定 `theta=1/8`、`eta=1/32`、`N=1024k`，从 `b_i=1` 开始，每轮令
`p_i=b_i/sum b`、`lambda=(7/8)p+1/(8k)`，计算 exact oracle 并更新
`b_i<-b_i(1-eta g_i)`。标准 log inequality 给每个 outer 的平均

\[
\mu_i\ge757/1792>2/5.
\]

每个资源独立均匀抽一个已保存轮次；helper 的整个 state/request profile 作为一个
独立块。条件于 profiles，资源 rule 独立且
`Var(W_i|X)<=delta k`；替换一个 helper 的 profile 对任意 outer 的影响至多 `16kw_j`，
Efron–Stein 给 `Var F_i<=128delta k^3`，合计

\[
\sum_i Var(W_i)\le129\delta k^4\le129/4096<1/25.
\]

固定中心平方势 `Psi=sum_i(W_i-mu_i)^2`。CE 依次固定 helper states、positive request
coins 和 resource rounds；每一步精确选择 conditional `E Psi` 最小的正概率选项。
单/双 resource winner events 足以计算一二阶矩：同一 helper 在两个资源上必须共享同一
selected state，若 requirements 不相容该项为零；这避免了把 shared state 误当成独立
重抽，也避免枚举指数 profile。全部概率和比较为有理，位长随输入与 LP 点多项式增长。

最终 `Psi<1/25` 给 `W_i>1/5`。取 `q=1/10`，以 `Q_j>=q` 的 helpers 为 Good，有
`W_i<=z_i+q(1-z_i)`，故每个 outer 的 Good home weight `z_i>1/9>1/10`。Good
fallback winner bundles 交给 outer，其余 helper 回 own，得到每个 group value 至少
1/10；完整回填所有 jobs 产生 `C_max<=2-1/10=19/10`，而 `OPT>=1`，所以是
19/10 approximation。

## 6. 软件证据与模型边界

现有 two-resource backend 只验证两个固定小例：3 helpers、2 outers、2 states/helper、
2 resources、2 rules，完整枚举 2048/2916 profiles/rules，核对 exact moments、11
步 CE、平方势不增和实际 winner values。第二例可有 outer 最终值 0，因为它没有
`delta` tiny-home 和 `mu_i>2/5` 前提；不能把该有限输出写成 v1 反例。backend 明确
`whole_scheduling_algorithm_checked=false`、`small_weight_class_instantiated=false`。

该证明仍只适用单 state outer、互异 homes、`k^4` tiny home、共享 B fallback 和完整
ordinary jobs。它没有覆盖多 state outer、重合 homes、一般 non-UD group、一般 UM，
也没有证明 source hardness、P≠NP、外部新颖性或六人 SPE。任何后续 k²、相对曲率、
多 outer 变体都必须保持独立 source 身份，不能把本 v1 proof 的 `delta` 和方差界静默
迁移。

## 7. 处置与接续

本源处置为 integrated-author-proof-read-after：原文证据、作者 Proof 的 LP/MW/variance/
CE/Good 回填链均归档；既有 finite backend 审查保留软件运行和 hash，二者不合并为
两份一般证明。第三阶段可建立“Exact → Author Proof → finite backend”关系，但必须
保留作者先读 Exact、未实现 whole scheduler、有限 backend 不覆盖 tiny-home 全域等事实。
