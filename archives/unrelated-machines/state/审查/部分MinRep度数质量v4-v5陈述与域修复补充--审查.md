---
id: "unrelated-machines/partial-minrep-degree-mass-v4-v5-source-review"
kind: "review"
type_tag: "审查"
title: "部分 Min-Rep 度数质量 v4–v5 陈述与域修复补充"
status: "integrated-with-versioned-domain-boundary"
truth_status: "source-statements-and-independent-nonempty-domain-reconstruction; no-UM-compiler"
review_level: "four-source-full-read-and-cross-source-comparison"
summary: "完整读取 v4 Exact、v4 非空域独立重构、v5 Exact 与 v5 域修复回执。v4 字面对象域未排除空字母表，故只能在通常非空投影游戏子域内承重；v5 显式修复后，度数质量复制、异长置换尾界、高围长修复、FAIL/位复杂度和 exact-k-to-1 PCP 接口恢复为同一条件源合同。"
scope: "任意有限二部投影多重图的 degree-mass copy regularization；v4/v5 版本和 exact-first 审查边界"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/partial_minrep_degree_mass_v4_original_exact_source.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/partial_minrep_degree_mass_v4_original_exact_source.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/partial_minrep_degree_mass_v4_nonempty_independent_pcsp_source.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/partial_minrep_degree_mass_v4_nonempty_independent_pcsp_source.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/partial_minrep_degree_mass_v5_exact_source.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/partial_minrep_degree_mass_v5_exact_source.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/partial_minrep_degree_mass_v5_domain_review_pcsp_source.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/partial_minrep_degree_mass_v5_domain_review_pcsp_source.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/partial_minrep_degree_mass_v5_frozen_proof_source.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/partial_minrep_degree_mass_v5_frozen_proof_source.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/partial_minrep_degree_mass_v5_independent_row_source.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/partial_minrep_degree_mass_v5_independent_row_source.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/partial_minrep_degree_mass_v5_read_after_pcsp_source.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/partial_minrep_degree_mass_v5_read_after_pcsp_source.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/partial_minrep_degree_mass_v5_read_after_row_source.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/partial_minrep_degree_mass_v5_read_after_row_source.md"
legacy_ids:
  - "UM-PARTIAL-MINREP-DEGREE-MASS-REGULARIZATION-v4"
  - "UM-PARTIAL-MINREP-DEGREE-MASS-REGULARIZATION-v5"
  - "UM-PARTIAL-MINREP-DEGREE-MASS-REGULARIZATION-v4-NONEMPTY-EXACT-REVIEW"
---

## 实读范围、版本身份与处置

本批逐字读取四份冻结 Markdown 源，并核对 `clean list --owner self --full` 给出的源提交、路径和 SHA-256。四份分别是：v4 的原始 Exact 陈述（source ID `97b32ad1c635021aee3d`，SHA `45c1d754332fc556066b994bffbda407bd2d619a05a77a539969f5ef2dc66b38`）、对 v4 非空子域的 Exact-first 独立重构（`35ab9d0f521fdd19c51a`，SHA `36950255eaf5df611e01440082a13fec02a353841d408a876741e982f14fbe63`）、v5 的域修复回执（`7bc07357865efe0408bc`，SHA `cb9baf54a78c86ffb2fb344934f4f23a1583a90725436b51dc7523048d398f11`）和 v5 修复后的 Exact 陈述（`8e9c1811b83618923578`，SHA `86dcd98daaa2cc479260e444f47f4e9eb3d8ae56936b220f0a1d18e82863d693`）。`97b...` 与 `8e9...` 是 statement-only 合同；`35ab...` 是只读 Exact 后的独立重构，明确没有读作者 v4 proof；`7bc...` 只比较 v4/v5 并记录另一审查者转述的形式域异议，未把该转述冒称本次独立发现。

这四份源的数学主体与已有《部分MinRep费用桥与pDM阈值双源审查》相同的 v5 对象相接，但本批唯一需要保留的版本信息是：v4 的字面域若只写“有限、Q=max≥2”而不写两侧字母表非空，则允许空 `Σ_A` 或 `Σ_B`；此时全投影和单标签 `val` 可能不再良定义。v4 的 exact-first 推导实际从头到尾使用通常的非空域，因此只能承重“v4 限制到两侧非空”这一子域。v5 把 `1≤|Σ_A|,|Σ_B|` 写进 Exact，且只改变这一域条件；参数、概率合同、修复和复杂度均未改。故 v4 与 v5 不能以同一无版本标签合并。

## v4/v5 的共同数学合同（v5 为字面接受版本）

固定 `G≥2`。输入为任意有限非空二部投影多重图 `Π=(A,B,E)`，删去孤点后 `N₀=|A|+|B|`、`M₀=|E|≥1`；两侧不要求同样大小、正规或有界最大度。每条原边 `e=(a,b)` 带显式全投影 `π_e:Σ_A→Σ_B`，允许平行 edge type；`val` 是单标签赋值满足的原边比例，列表成本是所有真实列表长度之和，边被 covered 当且仅当两端列表中有一对满足投影。v5 明确两侧字母表非空，`Q=max(|Σ_A|,|Σ_B|)≥2`；没有把它们强行识别为共同字母表。

给 binary `g≥2`、`0<ρ≤1`，令
\[
\ell=\lfloor\log_2g\rfloor,\quad \lambda=1+\lceil\log_2Q\rceil,\quad
\tau=\rho/(100g^2),\quad \gamma=\rho^3/(10^9g^8),\quad
d=\left\lceil\frac{1000g\lambda}{\rho\ell}\right\rceil,
\]
并要求 `Qγ≥1`；`G` 固定，不能把其变参时的指数依赖藏进“统一多项式”。令
\[
S=\sum_{j=2}^Gd^j,\quad B_0=40N_0S,\quad
U=\sum_{j=0}^{G+1}d^j,\quad m_*=dM_0,
\]
\[
z=\left\lceil\max\{2G+1,\;GB_0+4U+1,\;8B_0/(\rho m_*)\}\right\rceil.
\]
每个原点 `v` 建 `t_v=deg_Π(v)z` 个 copies 和 slots；每个 incident type 分成 `z` 个 slots，在每个 layer 中按 type 两端 slotwise 配成 matching。独立建立 `d` 层，每层每个原点抽一份长度 `t_v` 的均匀 permutation。于是
\[
N'=\sum_vt_v=2M_0z,\qquad M'=dM_0z=dN'/2,
\]
且每个 `(type,layer)` bucket 恰有 `z` 条边。原度数不平衡被 `t_v=deg(v)z` 精确支付：从原边均匀抽端点 copy 时，某端 heavy copy 的质量按 `deg(v)/t_v=1/z` 抵消，不能改成原点均匀抽样。

对任意总成本 `≤gN'` 的 copy lists，heavy copies 数由阈值 `H=4g/τ` 控制；light lists 逐原点抽 copy 与标签，NO 条件 `val(Π)≤γ` 给出平均模板覆盖边际小于 `τ`。变长 permutation 在 `j` 个不同 slots 上相对独立抽样的点态密度至多 `e^j`，从而 factorial moments/Chernoff 一次性控制所有 lists，而非逐列表重新消耗概率。精确写法是：若 `m̄` 为模板边覆盖边际和，则 `E(1+s)^Z≤exp(e²m̄s)`，并在 `a=ρM'/2` 下以 `m̄/a<1/(50g²)` 得到坏列表事件的指数上界；统一计数用两侧 typed alphabets 的 bit positions `L≤QN'`，不新增 labels，也不把不同 alphabet 合成一个。

短环部分先计长度 `2..G` 的 simple cycles（平行边算 2-cycle，单边往返不算）。超过 `B_0` 直接 `FAIL`；否则每次在同一 `(type,layer)` bucket 选两端离当前短环两端均超过 `G` 且不在任何短环中的干净边 `f`，以 `ab,cd→ad,cb` 换边。以每个原始起点 `v` 求和，闭合概率至多 `1/(t_v-G)`，且 `t_v≥z≥2G+1`，所以 `E X≤2N_0S`、`Pr[X>B_0]≤1/20`；这一步不需要原 max-degree 常数界。每次换边不生成新短环，最多 `B_0` 次结束；固定任意列表，覆盖数至多增加 `2B_0`，而 `z≥8B_0/(ρm_*)` 使最终仍小于 `ρM'`。输出为 simple、balanced、exact d-regular、girth>`G` 的 source，保留原 edge type、投影表、surjectivity/equal-fiber 属性；不能将投影关系反向误称全函数。

Fisher–Yates 每个均匀整数 draw 用公平拒绝采样，draw 数 `K_0=d∑_v(t_v-1)>0`，耗尽上限 `R=ceil(log₂(2000K_0))` 即 `FAIL`。固定 `G` 时，枚举短环、BFS、字典序 repair 和随机位数关于显式输入及 `binary g,ρ` 总位长多项式；`Qγ≥1` 是参数编码域的一部分。所有域内输入的 `FAIL` 概率小于 `.1`；NO 侧还扣除列表坏事件后，返回非 FAIL 且对所有 cheap lists 同时 sound 的概率至少 `.8`。这不是“所有非 FAIL seed 必然 sound”，`FAIL` 也不是伪造的高围长实例。

## exact-k-to-1 PCP 接口和范围

若另有固定误差、完美完备、常数字母表、exact `k`-to-1（固定 `k`）投影 PCP，可先把误差压到 `γ` 再接 v5，得到 simple、balanced、constant exact-degree、固定高围长的随机 source family，并保持每条投影 exact `k` fibers。同步复制字母表 `(α,s)↦(π_e(α),s)` 可把 `Q` 提到 `Qγ≥1`，value 与 fibers 均保持；clone 后必须按新 `Q` 重算 `λ,d`，不能沿用旧参数。若 `Q=poly_ρ(g)` 才能推出 `d=O_ρ(g)`；一般 fixed-error PCP 不自动提供该 alphabet 定量。把随机 source 与确定性 promise 判别器串联至多得到 `NP⊆BPP` 型后果；不能由此声称 `P≠NP`、确定性 UM 归约、或一般近二 hardness。

\n## 作者冻结证明与两份读后回执\n\n随后完整读取 v5 root 冻结证明（`0537b6c8c8983c81d23b`，SHA `e2e60ca49cb6fcaf14a865a83c1d537d3213eb01a8d60c1e1f6baa1054b86c29`）以及其后的独立行审查、PCSP 读后攻击和 row 读后回执（分别为 `70d3776e1e8877da619d` / `fab9db01a1e7b483d6e0659ab98c869ea3153697a41c5c376837f86cd9b5ddfd`、`1782a07760ed5677c083` / `5f3f086ed5a838fa8d30e97abe24f759bc526efc2b9c712503a213da5d010811`、`d6e9f035165c7e7677b4` / `f873d271dad2dc4341bc538f201c1c5bf1efacfc0b01b0956a7d7c51b92839a6`）。这些源逐段与本批 Exact-first 推导比较，未发现 v5 非空 typed 域内的新致命问题。\n\n* 证明的质量归一化常数正确：在固定一侧，每个 copy 被均匀原边抽到的概率为 `deg(v)/(M₀t_v)=1/(M₀z)=2/N′`；左右 heavy 质量合计至多 `2g/H=τ/2`。这一步严格使用真实 copy 总预算 `gN′`，不能改写成原点未加权预算。\n* variable-fiber permutation 的点态密度上界 `t_v^r/(t_v)_r≤e^r` 与 with-replacement 参照完全兼容；任意 `k` 条模板边只占 `2k` 个不同 `(permutation,slot)`，factorial moment、生成函数计数和全部列表同时 Chernoff 尾界仍成立。\n* 短环闭合按起始原点 `v` 分组，分母 `t_v−G`，求和 `t_v/(t_v−G)≤2` 得 `E X≤2N₀S`；不允许用最小 fiber 或 `N′` 粗乘。repair 只在同一 `(type,layer)` bucket 交换，保持投影类型与 exact-fiber 属性；每次任意列表覆盖数至多增加 2，`M′=zm_*` 负责支付 `2B₀/M′≤ρ/4`。\n* Fisher–Yates draw 数恰为 `K₀=d∑_v(t_v−1)`，截断拒绝采样给 `<.1` 的总 FAIL；条件于成功的 permutation 仍精确均匀。固定 `G`、`Qγ≥1` 和显式 alphabet/投影表共同支付位复杂度。作者没有把“所有非 FAIL 都 sound”或“source 本身是 UM 矩阵”写成结论。\n* 同步标签 clone `(α,s)↦(π_e(α),s)` 是真实 alphabet 扩张：丢掉 `s` 给 `val_new≤val_old`，统一 `s` 给反向不等式，故 value 和 exact `k` fibers 保持；后续 `Q,λ,d` 必须按新 alphabet 重算。读后审查保留 fixed-parameter PCP 接口、`Q=poly_ρ(g)` 才推出 `d=O_ρ(g)`，以及随机判别器至多导出 `NP⊆BPP`。\n\n这四份 proof/read-after 源的独有内容是证明版本顺序、作者 proof 与独立 Exact-first 对照、以及 formal objection 只归于 v4→v5 域修复；它们不提供代码、有限实验、外部新颖性或真实 UM compiler。当前 v5 可标为“源级符号证明+独立读后无新增致命异议”，而 v4 仍只能保留非空子域版本。\n\n## 与既有对象的比较和接续

已有《部分MinRep费用桥与pDM阈值双源审查》已承载 v2 的随机删边、v3 的正规/简单/高围长和 v5 的 degree-mass typed 复制，并明确真实 UM compiler、费用常数 `F`、同一原点列表一致性和低负载 decoder 仍缺。本页不新造第二个 v5 定理，而是补充四份历史 source 的版本证据与域边界；第三阶段应把 v4→v5 作为“域修复”关系，把 v4 Exact-only 与 v4 nonempty reconstruction 标为 statement/independent-reconstruction，而不是把二者当两份证明。

与《坐标切片投影源编译--反例》相比，v4/v5 是一般 typed projection source 的随机正规化，坐标切片对象是另一种私有分叉树调度编译失败；不能用坐标切片反例替代这里的列表尾界，也不能把本源的高围长输出当作 UM 调度。与《稀疏CSP与平坦矩阵两篇文献整理》相比，本源的 repair 是自足的 typed matching construction；文献中的关系结构 homomorphism/稀疏化不能自动认证本算法的 arbitrary-list soundness。

本批仍没有代码、有限实验、作者 proof 读后攻击或外部新颖性认证。独有处置为：v4 exact statement 保留历史陈述与 proof-absent 边界；35ab 的独立重构只接受非空子域；v5 exact 与 domain-review 记录正式 objection 已被修复，作为当前接受字面版本。UM-TARGET-v1 仍 OPEN；必须另造真实位多项式 UM 编译器、完整低负载 decoder、费用支付和复杂度归约，才能从本 source 合同得到调度 hardness。
