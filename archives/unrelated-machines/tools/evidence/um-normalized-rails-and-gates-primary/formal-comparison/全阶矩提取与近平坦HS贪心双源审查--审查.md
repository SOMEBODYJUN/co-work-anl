---
id: unrelated-machines/full-degree-moment-and-nearflat-hs-review
kind: review
title: 全阶矩提取与近平坦HS贪心双源审查
status: complete-source-read-integrated
scope: "full-degree moment/localizer decoding bridge and explicit near-flat global-moment HS extraction/gap"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/full_degree_moment_localizer_decoding_bridge.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/full_degree_moment_localizer_decoding_bridge.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/global_assignment_moment_rounding.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/global_assignment_moment_rounding.md
source_ids:
  - 8d5ac47aad7decd3c239
  - 43aee4f76d83e01522ad
inventory_sha256:
  8d5ac47aad7decd3c239: 32b6374633176fd2e1d3d7534a1b4aaec5066b99f38d2353ff91e51ae3860108
  43aee4f76d83e01522ad: c49e7d8dd13757f16ce6bd451c32999966739bed9be5c40d0bade4fce63cb1f0
---

# 阅读范围和对象区分

本批完整读取两个当前正文，并回读《近平坦 HS 矩提取与负接口有限审计》、C2/weak-H2 配置对象和相关证据路由。两源都处理 unrelated-machines 的全局 assignment moments，但承担不同数学任务：第一源给出一个不追求多项式规模的“全阶共同矩 + 每机局部化器必含真实整数调度”逻辑终点；第二源在给定四阶共同矩的前提下，提出可验证的近平坦缺陷条件和 HS 贪心提取器，并以一个大缺陷真实矩给出全空间 HS 规则的精确二倍反例。两者都没有从普通实例生成所需矩证书，也没有解决 `UM-TARGET-v1` 或六人 SPE。

稳定身份为 `UM-FULL-DEGREE-MOMENT-DECODING-v1`、`UM-GLOBAL-MOMENT-NEARFLAT-EXTRACTION-v1` 与 `UM-GLOBAL-MOMENT-HS-GREEDY-GAP-v1`。正文中的证明、条件算法、有限审计和拒绝边界分开处置。

# 一、全阶共同矩到整数调度的闭合桥

## 1. 精确合同

设合法 unrelated-machines 实例的有限边为 (E)，任务数为 (n)，每条边变量 (x_e)。assignment ideal (I) 包含布尔关系、同一任务不同端的互斥关系和每任务端点和为 1。给定有理 (T\ge0) 与定义在次数至多 (2n+1) 商空间上的有理线性泛函 (L)，要求：

1. 对次数至多 (n) 的 (q)，(L(q^2)\ge0)；
2. 对每台机器 (i)，(K_i=T-\sum_{e=(i,j)}p_ex_e)，并对同样次数的 (q) 有 (L(K_iq^2)\ge0)；
3. (L) 尊重 (I) 的恒等式。

量词是任意合法 (P,T) 和任意满足这些条件的 (L)。结论是存在真实不可拆分整数调度 (sigma) 使所有机器负载不超过 (T)。该桥不提供寻找 (L) 的算法，也不把其编码规模压缩成多项式。

## 2. 原子权和筛除超载

对每个合法调度 (sigma) 定义
\[
m_\sigma=\prod_{j=1}^n x_{e_j(\sigma)}.
\]
assignment ideal 给出
\[
\sum_{\sigma\text{合法}}m_\sigma
=\prod_{j=1}^n\left(\sum_{e\in E_j}x_e\right)=1.
\]
由幂等性和平方正性，(w_\sigma=L(m_\sigma)\ge0)，且 (sum_sigma w_sigma=1)，所以至少有一个正权原子。对机器 (i)，在商环中
\[
K_i m_\sigma^2=(T-L_i(\sigma))m_\sigma.
\]
因为 (m_sigma) 的次数恰为 (n)，可代入局部化器条件，得到
\[
0\le L(K_im_\sigma^2)=(T-L_i(\sigma))w_\sigma.
\]
任何正权 (sigma) 因而都满足所有 (L_i(\sigma)\le T)。这同时覆盖 (T=0)、零处理时间和空任务的逻辑边界；空任务的原子是 1，直接得到空调度。

核心用途是准确指出“共同矩到整数调度”的承重义务：必须有足以表达完整任务原子 (m_sigma) 的阶数和同一全局 (L)，而逐机配置边际或固定阶局部化器一般不能直接代入该原子。

## 3. 规模和开放边界

合法调度数可达 (m^n)，逐个保存原子权或完整次数 (2n) 矩阵通常指数大。次数 (2r) 的共同矩只能把局部化测试中的 (q) 提到次数 (r)，当 (r) 固定或 (o(n)) 时不能直接实现上述筛除。该观察是信息规模边界，不是所有低阶松弛的统一 gap 定理：额外跨机器约束可能改变结论。

任意真实 (T)-可行调度分布都能产生一个满足条件的 (L)，但其支撑可能指数大；证书存在、证书可验证、证书可多项式解码是三个不同问题。该桥比当前 C2-load、弱 H2 和单机 CONFIG 投影强得多，但没有从原输入构造这种全阶 (L) 的流程。

# 二、近平坦四阶矩的条件提取与 HS 贪心

## 4. 四阶共同矩合同

第二正文接收剪去 (p_{ij}>T) 端后的显式四阶 `C2-load(T)` 有理矩 (y)：任务守恒、全局 (M_2\succeq0)、逐机次数一负载局部化器 (K_i\succeq0)，不要求所有四阶条目逐项非负，也不要求 prefix-count localizer。令 (R=\operatorname{rank}M_1\ge1)，由 M1/M2 构造压缩算子 (A_e)、缺陷 (D_e=A_e-A_e^2\succeq0)，并令
\[
\delta_e=\operatorname{tr}D_e,\qquad \delta=\sum_e\delta_e.
\]
近平坦承诺为（对 (n\ge1)）
\[
\delta\le\min\left\{\frac1{64ndR},\frac\eta{16}\right\},
\]
其中 (d) 是保留端数，(eta\in(0,1])。这是给定证书的可验证充分条件，不是原模型的新承诺，也不是证书生成器。

## 5. 共同压缩算子与近幂等

在 M2 定义的商 Hilbert 空间中，(Pi) 投影到常数和一次单项式空间，(X_e:q\mapsto x_eq)，(A_e=\Pi X_e)。四阶交换性和 assignment ideal 给出
\[
X_e^*X_e=A_e,\quad D_e=A_e-A_e^2=B_e^*B_e,
\]
以及
\[
\|D_e\|\le\delta_e,qquad
\|[A_e,A_f]\|\le2\sqrt{\delta_e\delta_f}.
\]
任务守恒和机器局部化器分别成为
\[
\sum_{e\in E_j}A_e=I,qquad
\sum_{e\text{ at }i}p_eA_e\preceq TI.
\]
不能只用常数向量上的缺陷：所有合法四阶矩都可能在该向量上缺陷为零，真正需要的是整个 V1 上的迹缺陷。

固定任务顺序，令 (K_0=I)，每步在候选端中最大化
\[
\operatorname{score}_e=\|A_eK\|_{HS}^2,
\]
选中端后左乘更新 (K\leftarrow A_eK)。通过至多一次交换每对因子和 (A_e^2-A_e=-D_e)，任意前缀满足
\[
\|K_t^2-K_t\|\\le\left(\sum_{s\le t}\sqrt{\delta_{e_s}}\right)^2\le n\sum_{s\le t}\delta_{e_s}\le n\delta.
\]
近平坦阈值使前缀范数不会塌缩，最大 HS 分支保持 (|K_t|\ge1-2n\delta)，最终 (|K|_{HS}^2\ge(31/32)^2)。这一步依赖整体乘积近幂等，不能把每步正分支的质量简单相乘。

## 6. 从选端 loss 到真实共同负载

令 (h=\|K\|_{HS}^2)，(\rho=KK^*/h) 为迹一的有理密度。对选中端 (e)，正文以晚因子交换和缺陷估计
\[
\gamma_e=\|(I-A_e)K\|,qquad
\gamma_e^2\le(8n+2)\delta\delta_e,
\]
进而得到选择损失
\[
\ell_e=1-\operatorname{tr}(\rho A_e)<3\delta_e.
\]
同一 (\rho) 同时作用于所有机器；由 (\sum_ep_eA_e\preceq TI)，最终真实调度 (sigma) 满足
\[
L_i(\sigma)\le T+3\sum_{e\text{ selected at }i}p_e\delta_e\le(1+3\delta)T\le(1+\eta)T.
\]
这是真实任务标签输出，不是把 (\rho) 当作实际调度分布。有限端先剪枝到 (p_e\le T) 才能使用 ((1+3delta)T) 的强式；未剪枝版本只保留由 (\ell_e)\le3delta) 推出的 ((1-3delta)^{-1}T) 型保证，两个范围不能混用。

算法只对给定有理矩做线性代数和 (d) 次矩阵乘法；精确 Schur/LDL 处理零 pivot，行列式界控制逆矩阵位长。它不调用 SDP、特征值分解或真实分布 oracle。NF 失败只能拒绝该充分证书，不能推出 (OPT>T)。

## 7. 平坦极限与可复现边界

(delta=0) 等价于 (\operatorname{rank}M_2=\operatorname{rank}M_1)。此时所有 (A_e) 是两两交换的正交投影，V1 可按有理范数分裂为有限正交分支，给出真实 (T)-可行调度；这是布尔情形的 flat-extension 解释。该经典机制只说明给定平坦矩可提取，不说明矩易找。

已有《近平坦 HS 矩提取与负接口有限审计》对 21 个给定分布/矩案例和 6 个 self-contained fixtures 做了 Fraction 精确核验；通过案例支持阈值常数，large-defect rejection 只表示充分条件不满足。该有限审计与当前正文互补：当前正文给全称 near-flat 推导，旧审查给运行范围、冻结 JSON、独立实现和 rejection 边界。

# 三、全空间 HS 规则的大缺陷二倍反例

## 8. 反例对象和精确输出

第三身份 `UM-GLOBAL-MOMENT-HS-GREEDY-GAP-v1` 固定三台相同机器、一个长度 1 的大任务和八个长度 (1/4) 的小任务，(T=OPT=1)。210 个真实最优调度的均匀分布产生共同四阶矩，(\operatorname{rankM_1=17)。逐任务按固定 big-first 顺序，用全空间 HS 分数选择最大 (\|A_eK\|_{HS}^2)，精确平局取最小机器编号。

首个大任务选择任意机器；第二步在剩余两机间平局；之后差值均严格正，算法输出形状为一个机器负载 1、另一台负载 2、第三台负载 0，真实比率恰为 2。该输出不在 210 个最优分量支持中，说明正压缩算子连乘不等于被选任务事件有共同真实交集。

全空间矩来自真实最优分布，并且每台机器的负载算子在整个 V1 上精确饱和；但缺陷迹为 (delta=66)，远不在 NF 范围内。故该例只反驳无近平坦条件的指定全空间 HS 规则，不反驳近平坦定理、所有任务顺序、所有 moment 方法或一般近二算法。相同证书上的 rank-one state 规则输出最优，只作为范围对照。

## 9. 生成障碍与研究意义

正文还证明：若存在一个对所有 (OPT\le T) 输入都能在总位多项式时间生成满足 (delta\le1/(64ndR)) 的四阶 C2-load 矩，再调用近平坦提取，则半单位 3DM 的 YES/NO（YES 峰值 1、NO 峰值 (3/2)）可被区分。因此在 (P\ne NP) 下，这种原 (T) 上的普遍强近平坦生成器不存在。该推论依赖已登记的 3DM 归约和精确提取保证，不是配置 LP gap，也不排除其它增广容量或统一小于二的算法。

# 四、比较、处置和接续

1. 全阶桥是逻辑终点：完整原子权直接筛掉超载调度，但原子数和矩阶可能指数；近平坦 HS 是输入已给四阶矩时的压缩提取器，靠迹缺陷控制近幂等和 loss。
2. `C2-load` 的单位多切片趋二例说明固定阶、低阶共同矩可能留下 gap；本批补上“若把阶数推到 (2n)，为什么足够”以及“强近平坦四阶证书何时可提取”的精确层次。不能把两个结论合成一个统一阶数算法。
3. 近平坦有限审计的 21/6 cases、独立 Fraction 实现、零 T 和大分母均为证据范围；large-defect 拒绝不能解释为不可行性。全空间 HS 二倍例是原模型整数矩阵加真实分布反例，不能升级为所有矩算法失败。
4. 下一步义务是寻找可构造且位多项式的 moment/near-flat 生成机制，或者给出不要求近平坦的共同容量增广；同时要保持四阶矩的全局同一性，不能把逐机 CONFIG 边际拼成全局分布。
5. 两源均不涉及客户目录、历史 order 或 SPE 均分目标。其数学对象归入 unrelated-machines 的矩/舍入子存档；主目标与六人 SPE 目标保持开放。

两个来源的正文、证明、边界、证据和开放义务均已完整读取并归档；没有把证书存在误写成证书生成，也没有把有限审计或二倍反例扩大为一般 hardness。
