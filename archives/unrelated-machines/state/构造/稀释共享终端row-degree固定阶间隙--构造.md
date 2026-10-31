---
id: "unrelated-machines/diluted-shared-terminal-fixed-row-degree-gap"
kind: construction
type_tag: 构造
title: "稀释共享终端固定 row-degree 间隙"
status: proved-in-stated-fixed-degree-raw-contract
truth_status: exact-optimum-and-explicit-interpolation-certificate-with-author-proof
review_status: source-exact-and-author-proof-read; fixed-d scope only
summary: "固定 d≥2、k≥d 时，把共享终端 raw K2 的逐机 CONFIG 矩提升到同机 degree d；有限差分插值给合法配置和全局 affine-localizer，缩放后 gap 趋 2。多项式位复杂度依赖固定 d，且不含更高阶事件 localizer。"
legacy_ids:
  - SCRATCH-UM-DILUTED-SHARED-TERMINAL-ROW-DEGREE-d-v1
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_diluted_shared_terminal_row_degree_d_exact_only.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_diluted_shared_terminal_row_degree_d_author_proof.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_diluted_shared_terminal_row_degree_d_exact_only.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_diluted_shared_terminal_row_degree_d_author_proof.md"
evidence_paths:
  - "../../tools/evidence/diluted-shared-terminal-row-degree-20261031/manifest.json"
  - "../../tools/evidence/diluted-shared-terminal-row-degree-20261031/original/sol_diluted_shared_terminal_row_degree_d_exact_only.md"
  - "../../tools/evidence/diluted-shared-terminal-row-degree-20261031/original/sol_diluted_shared_terminal_row_degree_d_author_proof.md"
related_objects:
  - "稀释共享终端raw-K2锐二倍间隙--构造.md"
  - "稀释共享终端row-degree最终section13读后增量--审查.md"
---

本对象是固定阶 (d) 的独立增强，不能把 raw K2 的 degree-4 first/pair 配置自动改称本定理。两份冻结原件 SHA-256 为 exact `e23ae495b4a997f081e0de06323e5dd9563c98d3828b78804ddc7670b16c9f6a`、proof `7fb8ae7e6635853417963a5ff379406cbc3a0abf347a73015ebc79c1a207c407`；副本见证据 manifest。Proof 是作者 proof/read-after，本页保存其固定-d 量词和边界。

# 1. 输入与增强合同

固定整数 (dge2)，(kge d)，令 (s=d-1)、
[
Z=\sum_{u=0}^{s}\binom ku,quad A_{\max}=\binom{k-1}{s},quad L=2k^2,
quad M=1+120Lk^4+4kZA_{\max},quad T=1+s/k.
]
普通矩阵与前一对象相同（(U_i,B_{i,b},Z_{i,t},h,f,e) 的资格和处理时间不变），故完整真实调度仍有
(\operatorname{OPT}=2-\lfloor\sqrt{k}\rfloor/k)。

共同 functional (F) 定义到 (D=\max(4,d))，布尔/互斥/one-hot 方程乘到相应次数，(M_2) 仍只要求 degree 2 PSD。每台机器的合法 CONFIG 分布必须匹配 (F) 在该机所有 endpoint 单项式的总次数至多 (d)，包括 mixed incoming/home monomial；同时仍要求任意全输入 affine (q) 的 (F[(T-\operatorname{load}_v)q^2]\ge0)。这里没有 joint CONFIG-selector M2、higher-degree q/event localizer、export-activation 或 inactive-home 条件。复杂度只对固定 (d) 多项式，不能令二进制编码的 (d) 自由增长。

# 2. 完整法则和合法背景

均匀选择 (I)，选中组件采用 (H)：随机注入把所有 (f) 分到不同 (B)，所有 (e) 留 home。未选组件用 (Q_{new}=(Q_{old}+R_{fill})/2)。(Q_{old}) 是全 home、单 (f)+双射终端、单 (e) 导出三种法则；(R_{fill}) 先随机 (B)，再随机 (|S|le s) 的子集 (S)，公平选择有/无一件 incoming (f)，在该 (B) 留恰 (S) 的 home (e)，其余 (e) 通过均匀注入送到不同终端。

每个样本是完整 assignment。(Q_{old}) 负载至多 1，(R_{fill}) 负载至多 (T)，(H) 只有 (B) 行可超载；有限概率法则同时给出所有次数的 PSD 扩展，取 degree (D) 即得所需 (F)。

# 3. 有限差分插值与逐机 CONFIG

对每个 (|S|le s) 定义
[
b_S=(-1)^{s-|S|}\binom{k-|S|-1}{s-|S|},\qquad |b_S|le A_{\max}.
]
任意 degree-(s) 多项式满足
[
f(1,\ldots,1)=\sum_{|S|\le s}b_S f(1_S),
]
且 (sum b_S=1)。固定 (B) 行的 endpoint 多项式在 unit-clique/Boolean 关系下写为
(p(R,Y)=p_0(Y)+\sum_jR_jp_j(Y))，其中 \(\deg p_j\le d-1=s)。因此 H 的整行值可由 (C_{j,S})（incoming (j)+home 集合 (S)）和 (C_{0,S})（无 unit、home 集合 (S)）插值：
[
p(C_{j,\rm all})=p(C_{0,\rm all})+
\sum_{|S|\le s}b_S[p(C_{j,S})-p(C_{0,S})].
]

令 \(\rho_Q) 为 (Q_{new}) 下的真实 B-row 分布，配置分布定义为
[
\rho_{CFG}=(1-a)\rho_Q+a\delta_{C_{0,all}}
+\frac aL\sum_{j,S}b_S\delta_{C_{j,S}}
-\frac{ak}{L}\sum_Sb_S\delta_{C_{0,S}},qquad a=1/M.
]
所有配置负载不超过 (T)：(C_{j,S}) 负载 (1+|S|/kle1+s/k)，无 unit 状态负载至多 1。(R_{fill}) 背景分别以至少 (1/(4LkZ))、(1/(4LZ)) 质量提供 (C_{j,S})、(C_{0,S})；(M-1ge4kZA_{max}) 吸收全部负修正，故合并相同状态后是真正概率分布。插值恒等式保证它匹配每个 B-row degree≤d 单项式；纯 home 边际甚至在所有次数保持。U 与终端取真实 row marginal，逐点已合法。

# 4. 全局 affine localizer

对固定 B 写 (g=T-\operatorname{load}_B)。在 (Q_{old}) 下 (g\ge s/k\ge1/k)，而 (R_{fill}) 下 (g\ge0)，故
(\mathbb E_{Q_{new}}[gq^2]\ge\frac1{2k}\mathbb E_{Q_{old}}[q^2])。与 raw K2 相同的 three-state square estimate 给
(\mathbb E_{Q_{old}}q^2\ge\|c\|^2/(30Lk^3))，从而 Qnew 给正 slack \(\|c\|^2/(60Lk^4))。在 H 下 (g=s/k-1\{B\text{ 被注入选中}\})，\(\mu=\mathbb E_Hg=(s-1/2)/k\ge1/(2k))，且完成平方得 \(\mathbb E_H[gq^2]\ge-2\|c\|^2\)。条件于 selector 后组件独立，其他组件方差项乘正的 \(\mathbb E[g\mid I=h]\)；平均得到
[
F[gq^2]\ge\left(\frac{1-a}{60Lk^4}-2a\right)\|c\|^2\ge0
]
由 (M-1ge120Lk^4)。U/终端 localizer 点态成立，且不产生随 M 增长的维度因子。

# 5. 固定-d 复杂度、缩放与精确边界

固定 (d) 时 (Z,A_{max},M) 都是 (k) 的多项式，row CONFIG 列表和 degree-(D) 矩表也有多项式大小；Rfill 的 queried-head 概率用有限子集和与 falling factorial 直接生成，无需枚举指数支持。该结论不是 variable-d uniform algorithm 或一般 exact SDP solver。

缩放所有 processing times (k/(k+s)) 到目标 1，证书仍可行，真实 OPT 为
[
\frac{2-\lfloor\sqrt{k}\rfloor/k}{1+s/k}\to2quad(k\to\infty, d\text{ 固定}).
]
任意首阶 CONFIG 仍给标准 2-slot 上界，故固定-d raw 合同在此域的 gap supremum 为 2。

该有限法则的自然 degree-((d+1)) mixed monomial（一个 incoming (R_j) 与任意 (d) 个不同 home (Y)）在 (F) 中为 (a/L>0)，而任何负载不超过 (T) 的 CONFIG（至多 (s=d-1) 个 home 与 unit 同行）给零；这是本证书越过下一阶时的明确失败，不是对所有更强证书的不可能性证明。跨行 product event 也失败：
(F[A_iC_{i,b}(T-\operatorname{load}_B)]=a(k/L)(T-2)<0)。因此不能把固定-d row contract 提升为高阶 SOS、joint CONFIG-M2、cross-row localizer、canonical C2/S3、hardness 或六人 SPE 结论。
