---
id: weighted-congestion/asymmetric-matroid-perfect-candidate-boundaries
kind: resource
type_tag: 资料
title: 非对称拟阵纯精炼均衡候选与证明承重边界
status: candidate-open; proof-skeleton-only; finite-audit-linked
summary: 冻结选题稿提出 AP-01 共同相对内部边际与 AP-02 任意非对称仿射延迟两个 normal-form 纯 trembling-hand perfect equilibrium 算法候选，并给出扰动消元、有效延迟和 slot 拟阵交的证明骨架；这些不是已认证定理。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/independent_review/research/topic_selection/candidates/atomic_potential.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/independent_review/research/topic_selection/candidates/atomic_potential.md
related_objects:
  - weighted-congestion/two-weight-potential-and-asymmetric-perfect-target-ledger
  - weighted-congestion/atomic-tremble-audit-and-local-obstruction
  - customer-attraction/peer-topic-comparison-and-priority-boundaries
---

# 非对称拟阵纯精炼均衡候选与证明承重边界

## 来源身份、完整性和状态

冻结源 ID `74df7115598c27c71941`，路径为
`history/retired_topic_selection/independent_review/research/topic_selection/candidates/atomic_potential.md`，源 SHA-256 为
`28f5bfae4853bc5fd20526d400a84335a85023fbe940473b31eced505d4cd598`，大小 18,809 字节；`legacy-cleanup` 提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `main` 提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 记录相同冻结内容。本文件已完整读取 `clean show` 返回的全文。它是退役选题研究稿：有明确模型、来源索引、证明草图、反例边界和有限核查计划，但没有经过独立证明、文献穷尽核验、代码复杂度审计或外部新颖性审查。因此不应勾为 theorem，也不应把它写成已解决的非对称拟阵开放题。

## 候选主线和精确量词

源稿的主线不是加权拥塞档案中现有的有限双权近似势。它研究有限无权玩家 (i=1,ldots,n)，每名玩家的策略集合是共同有限地面 (E) 上某个拟阵 (M_i) 的全部基 \(\mathcal B_i\)，允许不同拟阵、不同秩、loops/coloops。给定每资源非负有理非减延迟表 (d_e(1),\ldots,d_e(n))，玩家成本是其基所含资源的延迟之和。目标是从显式策略/独立性 oracle 输入中，以位多项式时间输出一个原始 normal-form 的**纯 trembling-hand perfect equilibrium**。这不同于只输出 PNE、只分析某个固定扰动、SPE、混合 NE，或声称存在一个未打印的全支持分布。

源稿区分两个候选：

* **AP-01（共同相对内部边际）**：任意非减延迟；要求各基多面体 (P_i=\operatorname{conv}\{1_B:B\in\mathcal B_i\}) 有共同的有理相对内部点 (p\in\bigcap_i\operatorname{ri}(P_i))。这是受限结构候选，不代表任意非对称拟阵。
* **AP-02（任意非对称仿射）**：允许任意 (p_i\in\operatorname{ri}(P_i))，延迟为 (d_e(k)=a_e k+b_e)，(a_e,b_e\ge0) 有理；不要求共同内点、共同秩或共同策略集。该候选把身份差异压到个人资源常数中。

AP-03 至 AP-10 是未承重的后备方向（全部非减延迟、加权聚合、优先级、需求偏序、近似势、平滑和相关噪声等），不应与 AP-01/AP-02 合并为一个结论。源稿还明确排除已被后续统一模型覆盖的旧优先级题和把一般近似均衡鸿沟包装成短期目标。

## AP-01 的证明骨架（候选，不是证明）

**内部点构造。** 对任意基 (B\in\mathcal B_i)，把 (B) 与全部合法单交换基 (B-e+f) 的指示向量取平均，候选得到 (p_i\in\operatorname{ri}(P_i))；rank 0 或唯一基退化为单点。需要补上的关键是：这些邻顶点的平均确实落在相对内部，且从该点可构造给每个基正概率的全支持分布 (q_i)；“小支持平均”本身不是全支持分布。该凸几何断言在源稿中只是草图，不能直接当标准定理使用。

**自己的扰动项消去。** 对纯核心 (B_i)，取 (x_i^\varepsilon=(1-\varepsilon)\delta_{B_i}+\varepsilon q_i)，其中 (q_i) 全支持。固定对手混合后，玩家自己的 (q_i) 项与比较的候选纯核无关；对任意纯核 (S,T)，有
\[
 C_i(x_i^\varepsilon(T),x_{-i}^\varepsilon)-C_i(x_i^\varepsilon(S),x_{-i}^\varepsilon)
 =(1-\varepsilon)\sum_e(1_{e\in T}-1_{e\in S})
 \mathbb E[d_e(1+K_{-i,e})].
\]
这里仍须明确使用“不同玩家的混合相互独立”，而不是错误地假设同一玩家的资源选择独立。

**共同内点的有效延迟。** 对名义使用资源 (e) 的玩家，若每个其他玩家边际都为同一 (p_e)，可把其余使用者写为独立 Bernoulli，得到
\[
 \widetilde d_e^\varepsilon(k)=
 \mathbb E[d_e(1+\operatorname{Bin}(k-1,1-\varepsilon+\varepsilon p_e)
 +\operatorname{Bin}(n-k,\varepsilon p_e))].
\]
源稿声称可由 (1-\varepsilon+\varepsilon p_e\ge\varepsilon p_e) 的耦合保持 (k\mapsto\widetilde d_e^\varepsilon(k)) 非减，且其为有理 epsilon 多项式。要补出的是对每个 (e) 和每个 (k) 的精确卷积算法与编码界。

## AP-02 的候选势和边界

取任意 (p_i\in\operatorname{ri}(P_i))，记 (P_e=\sum_jp_{j,e})。对仿射延迟，源稿给出
\[
 \widetilde d_{i,e}^\varepsilon(k)
 =a_e(1-\varepsilon)k+b_e
 +\varepsilon a_e(1+P_e-p_{i,e}).
\]
于是身份依赖只出现在不随 (k) 变化的个人资源常数；候选固定纯核心的势为
\[
 \Phi^\varepsilon(B)=\sum_e a_e(1-\varepsilon)\frac{k_e(k_e+1)}2
 +\sum_i\sum_{e\in B_i}
   [b_e+\varepsilon a_e(1+P_e-p_{i,e})].
\]
这个公式解释为什么 AP-02 比 AP-01 的共同内点要求更宽，但它仍是候选：必须核对所有玩家的独立全支持扰动、纯核心选择与势的精确战略等价，并证明所取核心在一段统一的充分小 epsilon 区间内稳定。次数二以上一般延迟会出现名义使用者身份的高阶交互，不能沿用该 affine 公式；这是源稿明确的自然边界。

源稿给了一个非对称 rank-2 例：(E=\{a,b,c,d\})，(M_1) 排除基 (ab)，(M_2) 排除基 (ac)，并列出共同内点候选
(p=(1/5,11/20,11/20,7/10))。它还给出 (M_1) 排除 (ab)、(M_2) 排除 (cd) 时共同相对内部交为空的边界例。两例是机制说明，不是算法正确性或交点识别的证明。

## 组合优化候选和真正的未完成义务

对公共非减有效延迟和个人线性项，源稿把固定核心优化写成地面元素 ((i,e,k))（(k=1,\ldots,n)）上的加权拟阵交：每个玩家的基拟阵复制为并直和；每个资源的 slot (k) 形成容量一的分组拟阵。若能严谨证明最优解占用资源的前 (k_e) 个 slot，目标势可由一个加权拟阵交最小解表示。源稿还提出将有理多项式的系数清分母并以足够大的整数基数编码，以稳定比较形式无穷小 epsilon。

这一步是核心未完成部分：需要核对加权拟阵交输入规模、独立性 oracle 调用、负权/零权处理、系数位长和同一核心在所有足够小 epsilon 下的稳定性。最后一步才可把固定核心对 (x_{-i}^\varepsilon) 的最佳回应取极限，得到原 normal-form 的纯 perfect equilibrium。单个有限 epsilon 的实验、有限 profiles 或“势会下降”都不足以完成 perfect 证明。

## 已有有限证据和原子审计的边界

该源稿引用的 `atomic_tremble_audit.py/json` 已由另一来源独立归档于[原子扰动审计与单交换局部障碍](../审查/原子扰动审计与单交换局部障碍--审查.md)：Fraction 精确核查 3 玩家、4 资源、125 个固定 profile，\(\varepsilon\in\{1/10,1/100\}\)，共 3,750 条 payoff-difference 与 3,000 条不等边际 affine 关系。它还给出 (U(2,4)) 的单交换局部反例：成本 `[2,2,1,1]` 下基 `{a,b}` 的所有单交换成本仍为 2，而全局基 `{c,d}` 成本为 1。该证据只否定“单交换局部最优自动等于全局最优”的未加条件说法；不证明 AP-01/AP-02，也不产生无 PNE 或复杂度下界。

因此本源相对于已有审计的独有内容是：AP-01/AP-02 的完整模型边界、AP-L1/L2/L3 证明路线、共同内点/非对称 affine 的两个实例、AP-03 至 AP-10 的候选淘汰理由，以及把有限审计明确降格为验证接口。有限审计的原字节和脚本不应再次复制成另一个证据对象。

## 全仓关系和接续用途

* [有限双权近似势与非对称精炼目标的不同合同](有限双权近似势与非对称精炼目标的不同合同--资料.md) 已保存同一非对称精炼目标的量词合同，但没有本源的 AP-L1/L2/L3 公式；两者应通过“候选目标—证明义务”关系连接，不合并为一个已证定理。
* [原子扰动审计与单交换局部障碍](../原子扰动审计与单交换局部障碍--审查.md) 已保存本源引用的 Fraction 审计和 U(2,4) 障碍；本源只应链接该证据，不重复入库。
* [同行选题比较与候选优先级边界](../../../customer-attraction/state/资料/同行选题比较与候选优先级边界--资料.md) 保留 AP-01/AP-02 的同行优先级与新颖性边界。该对象不等于本源的证明草稿，也不应把“第一梯队”写成数学结论。
* [原子拥塞重选题与失败路线审查](../原子拥塞重选题与失败路线--审查.md) 处理 AG-01/AG-03 等另一批选题及两玩家 toy 反例，不能与 AP-01/AP-02 的拟阵精炼模型混写。

本对象适合归档为 `state/资料` 或 `state/审查` 的候选资料，保留 `status: candidate-open; proof-skeleton-only; finite-audit-linked`。来源处置建议为 `integrated`：独有证明骨架和范围边界进入本对象；重复的有限核查引用既有对象。只有在补完多项式编码、统一小 epsilon 区间、拟阵交正确性和最新文献查重后，才可另写 `state/定理`。
