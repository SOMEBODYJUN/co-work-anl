---
id: "unrelated-machines/prefix-atomic-finite-precision-gram-boundary-20261031"
kind: "review"
type_tag: "审查"
title: "有限精度前缀原子解码与 Gram 满行秩边界冻结审查"
status: "integrated-finite-precision-boundary"
truth_status: "sharp-prefix-decoder-with-relative-localizer-and-full-row-rank-condition"
review_level: "full-source-read-independent-reconstruction-and-gram-attack"
summary: "完整读取 UM-PREFIX-ATOMIC-FINITE-PRECISION-v1 审查。给定同一守恒前缀 law、误差 alpha 的最大估计查询，输出叶质量下界为 max(0,[1−2alpha(N−1)]/N)，并有等号构造；配合真实全叶负载 localizer、共同分母 Q 和 alpha/tau 取值可恢复精确负载。绝对 localizer 会被零任务指数稀释；Gram PSD 反推原子约束必须有满行秩，低秩常数基有两原子反例。结论是 promise decoder 与线性代数边界，不是一般 oracle 生成器或 UM hardness。"
source_refs:
  - "source:5f0ef9a295ae78b8e680:research/reviews/unrelated_machines/prefix_atomic_finite_precision_review.md"
legacy_ids:
  - "UM-PREFIX-ATOMIC-FINITE-PRECISION-v1"
related_objects:
  - "unrelated-machines/succinct-prefix-atomic-decoding-bridge"
  - "unrelated-machines/full-degree-moment-localizer-decoding-bridge"
---

# 1. 来源与独立顺序

`clean show` 导出的来源 `5f0ef9a295ae78b8e680` 位于
`research/reviews/unrelated_machines/prefix_atomic_finite_precision_review.md`，14,827 bytes，SHA-256 为
`2aace0a62dc3edc320bb5a9c50d7de578b9a953cd0763cc388c86919d1cb1e3f`。本页逐段读取并保存原文到
`archives/unrelated-machines/tools/evidence/prefix-atomic-finite-precision-20261031/original/`。

来源记录先只收精确陈述，独立推导和 Fraction 审计在读 canonical 前完成；随后再读最终 `succinct_prefix_atomic_decoding_bridge.md` 的新增有限精度 §1–6、原精确定义及 `full_degree_moment_localizer_decoding_bridge.md`。独立脚本、root 重跑和作者侧脚本均被区分；所有 audit 都是有限证据，不是一般 proof 或全承诺验证器。

# 2. 守恒前缀 law 与 sharp 质量下界

固定 n 件 job，第 j 件有 `d_j≥1` 个显式有限端，`N=∏_j d_j`（空积为 1）。完整合法 assignments 是叶，非负前缀 law `π` 满足 root=1、每父值等于全部孩子值之和。对同一 `π` 的查询前缀，oracle 返回 `hatπ(v)` 且误差不超过 `α`；每层查全部孩子、取最大估计、平局按固定次序。

对每个固定分支向量和 `α≥0`，输出叶 `σ` 的真实质量满足精确最坏界
\[
\pi(\sigma)\ge b:=\max\left(0,\frac{1-2\alpha(N-1)}N\right).
\]
`N=1` 时唯一叶质量恒为 1，涵盖 `n=0` 和所有 `d_j=1`。

若父真实质量为 `x`，选中孩子真实质量为 `y`、孩子数为 `d`，其它孩子真实质量至多 `y+2α`，故
\[
y\ge\frac{x-2\alpha(d-1)}d.
\]
令 `D_j=∏_{h≤j}d_h`、`q_j` 为所选前缀质量，乘以 `D_j` 后望远镜得到
\[
D_jq_j\ge1-2α(D_j-1).
\]
再用非负性截断。

当 `N>1` 且 `α≤1/[2(N-1)]`，沿固定平局分支令
\[
q_j=(1+2α)/D_j-2α,
\]
其它兄弟取 `q_j+2α=(1+2α)/D_j`，查询估计均置为 `q_j+α`，便得到精确等号；`d_j=1` 没有兄弟仍成立。`α` 超过临界值时沿用临界零叶例，输出恰为 0。若要求唯一最大值，通常只能称下确界；确定性、历史依赖的平局规则仍可先固定路径再布置特殊叶。

# 3. 真实负载、共同分母与精确恢复

对同一 `π` 的每个完整叶和机器 i，若真实 localizer 满足
\[
(T-L_i(σ))\pi(σ)\ge-τ,
\]
且解码保证 `b>0`，则真实负载
\[
L_i(σ)\le T+τ/b.
\]
分母不能使用 `hatπ`。

令 `Q` 为所有有限 processing times 与 `T` 的正整数分母之积，未约分也可；每个合法叶的 `Q(L_i-T)` 是整数。取
\[
α=1/(4N),\quad b=(N+1)/(2N^2)>1/(2N),\quad τ=1/(4QN)
\]
得到 `τ/b=N/[2Q(N+1)]<1/(2Q)`，因而整数性给出 `L_i≤T`。一般充分条件是 `τ/b<1/Q`；等号不能无条件放宽，因为负载违反 `1/Q`、质量 b 的叶可在 `τ=b/Q` 时通过 localizer。

dyadic oracle 只需精度位 `k_π=ceil(log2(4N))`、`k_loc=ceil(log2(4QN))`；查询数 `∑_j d_j`、精度和工作位长在“oracle 查询时间 poly(input length,k)”承诺下为多项式。给出精度位数不证明存在该 oracle。

边界明确：`n=0/N=1` 直接输出唯一叶；`T=0` 仍由网格迫使负载为 0；只枚举原有限资格，`Q` 不含 infinity；每 job 至少一条有限边，`d_j=0` 必须拒绝，不能令 `N=0`；所有查询与 localizer 必须来自同一非负守恒 `π`。只检查近似 localizer 数值而没有真实残差保证，不能套用该结论。

# 4. 绝对误差的 dilution 与相对 localizer

两台机器 `a,z`、`T=0`，一枚只能在 `a` 执行且耗时 `d>0` 的任务，另有 `k` 枚在两台机器均为 0 的任务。`N=2^k`，所有完整调度都有 `L_a=d`，没有 `T` 调度。均匀守恒 `π` 给每叶 `(T-L_a)π=-d/N`，所以 `τ≥d/N` 会让完全不可行实例满足全部绝对 localizer；实际过载没有改变，只被叶数稀释。若 `d` 的分母整除 `Q`，`d/N≥1/(QN)>1/(4QN)`，不反驳前节安全常数。

改成相对条件
\[
(T-L_i)\pi\ge-Δ\pi
\]
则每个正质量叶直接给 `L_i≤T+Δ`，叶数不再出现；仍需 `Δ<1/Q` 才能用网格恢复精确 T。零质量叶没有负载信息，解码必须保证输出正质量。

# 5. Gram 满行秩的必要条件与精确反例

设支撑数 s、函数数 r，`F∈R^{s×r}` 的行是原子函数值，列为函数值，且 `w_σ>0`。若每个原子系数非负，则
\[
K_i+Δ_iM=F^T\operatorname{diag}((T+Δ_i-L_i(σ))w_σ)F\succeq0.
\]
反向需要 `rank(F)=s`：对每个原子可取 `c_σ` 使 `Fc_σ=e_σ`，二次型给出 `(T+Δ_i-L_i(σ))w_σ≥0`，再除以正权重恢复原子容量界。`M` 可奇异，`F` 不需方阵或可逆。

精确低秩反例：两支撑原子各权 `1/2`，`T=1`，机器 A 负载为 0、2，只保留常数函数 `F=(1,1)^T`。则 `rank(F)=1<2`、`M=[1]`、`K_A=[0]` 在 `Δ=0` 时 PSD，但第二原子真实负载为 2>T；可由两件 job 在 A 各耗 1、B 各耗 0 的两个叶均匀分布实现。改用完整指示基 `F=I_2`，`K_A=diag(1/2,-1/2)` 立即拒绝。

绝对 I 容差也不保持任意基变换：`F=I_2`、`τ=1/2` 时 `K_A\succeq-τI`，改用可逆 `G=diag(1,2)` 得 `G^TK_AG=diag(1/2,-2)`，同一绝对 τ 失败。相对条件连 M 同变换，`K'+ΔM'=G^T(K+ΔM)G`，才保持等价。丢列、截断或低阶投影不能借基变换保留原子结论。

# 6. 原精确桥、高阶矩与证据等级

原精确桥的 `Eval(S)` 可以查询任意相容部分分配；新扩展只沿固定顺序前缀使用该能力，不能倒推免费实现所有任意 S 的查询。证明使用同一 exact law、归一化、非负、守恒和完整原子 localizer。

依赖的高阶文件把 `L` 定义在次数 `≤2n+1`，要求次数 `≤n` 的平方正性及 `K_i q^2` 局部化。前缀指标 `m_S` 满足 `m_S^2=m_S`、次数 `≤2n`，并由 one-hot 理想展开；完整 `m_σ` 次数 n，`K_i m_σ^2` 次数 `≤2n+1`，于是
\[
L(K_i m_σ^2)=(T-L_i(σ))L(m_σ).
\]
这提供 exact law 与零残差条件，但高阶大小可指数大，不自动提供有限精度压缩 oracle；原文件概述中的“次数 2n”必须按精确 §1 的 `2n+1` 理解。

处置为 **integrated**：整合 sharp 前缀质量、网格精确恢复、绝对/相对误差边界、满行秩 Gram 反推和高阶依赖阶数；保留独立 Fraction/Gram 审计与实际 SHA。未把 promise oracle 变成一般生成/验证器、UM 新近似、hardness 或全球新颖性结论。
