---
id: "unrelated-machines/token-label-lift-v1-exact-first-and-author-read-after-review"
kind: "review"
type_tag: "审查"
title: "Token-label lift v1 Exact-first 与作者读后两源审查"
status: "given-point-moment-boundary-read"
summary: "Exact-first 独立稿与作者 Proof read-after 对照确认：一般 M1 的 token-label 平均/contrast 分解成立；指定 aggregate degree-4 M2 点的 Schur quotient 正定且 rank 55，但 formal lift 有 Q²=-1/150，任意保留完整 aggregate functional 的原 token M2 extension 必须满足的 affine-context block 在半符号方向为负。结论限于给定矩点与必要条件，不是 native scheduling gap、generic SDP 失败或一般 UM hardness。"
source_refs:
  - "clean:0a497ae30880f9b08b66"
  - "clean:87e962ba1c44ce4fbee7"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_true_hardness_token_label_lift_exact_first_attack.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_true_hardness_token_label_lift_author_read_after_v1.md"
---

# 来源身份、读序与精确范围

本批两份记录的读序不能抹平。`0a497ae30880f9b08b66` 是 Exact-first 独立攻击：先只读 Exact 的陈述，自行推导一般 M1 PSD、aggregate M2 Schur、formal kernel 负平方和原 token extension 的必要条件；它没有读作者 Proof 或作者代码。`87e962ba1c44ce4fbee7` 是随后作者 Proof v1 的实际 read-after：逐节对照独立稿，补充作者更大 210 函数空间 Schur、整体 context Gram 的量词、ordinary 13-machine witness 和软件/SH3 边界；它明确没有重跑作者 code/audit。

| clean ID | 原路径 | SHA-256 | 读域 |
|---|---|---|---|
| `0a497ae30880f9b08b66` | `history/source/notes/unrelated_machines/sol_true_hardness_token_label_lift_exact_first_attack.md` | `091585c4b21b13eb8487435d094fa6b0d8905655c88a7232faa4a39d32d1b9d0` | Exact-first 自行证明/攻击 |
| `87e962ba1c44ce4fbee7` | `history/source/notes/unrelated_machines/sol_true_hardness_token_label_lift_author_read_after_v1.md` | `6836e703ef5084e67c8655aedae6397f5aad575df44ecfdb51961e553196187e` | 作者 Proof 读后比较 |

原件导出和 manifest 在 `archives/unrelated-machines/tools/evidence/token-label-lift-v1-two-sources-20261031/`，receipt 草稿在 `cleanup/workspaces/Boss2/token-label-lift-v1-two-source-receipts-20261031.json`。源内提到的作者 Exact/Proof SHA 是 provenance 元数据；本轮 clean sources 是上表两份，不把元数据指针冒充第三份已独立 clean show 的作者原文。

# 1. 一般 M1：标签平均与 contrast 块

设一组有 `k≥2` 个原 token、`r` 个 head 请求、`h=k−r` 个 home 标签。匿名变量为 `A` 与 `X_i`，一阶/二阶矩记 `a=L(A)`、`p_i=L(X_i)`、`M_{ij}=L(X_iX_j)`。Boolean ideal 和共同 M2 PSD 给出 `p_i≥0`、`M_{ij}≥0`，而 aggregate 方程给出 `Σ_i p_i=ra`、`Σ_jM_{ij}=rp_i`、`M_{ii}=p_i`。

Formal lift 把原 token 通过下降阶乘系数平均分配到不同 head/home 标签；任意 lifted linear polynomial 在每组拆成 token 平均项和零和 contrasts。token-permutation 对称性使 contrasts 与 context、其它组、平均项的二阶交叉消失；平均项的平方正好是 aggregate/context 线性多项式的平方，因此非负。独立稿的 contrast 块为

`k(k−1)(D−O)=[[hr a, −h pᵀ], [−h p, k diag(p)−M]]`,

其二次型是 `h Σ_i p_i(u−v_i)^2 + Σ_{i<j} M_ij(v_i−v_j)^2≥0`。作者 Proof 用类别计数 `n_0=k−rA,n_w=X_w` 的 weighted-category Laplacian 写同一块；两种证明相容。`k=1` 单独用线性替换，不除以 `k−1`；`r=0`、`r=k` 使相应对比块退化为零，均在范围内。

这只是 M1 保持/contrast PSD 的条件结论；它没有推出 lifted M2 PSD，也没有给出任意 native machine row 的完整 CONFIG。恢复真实 row law 还需 incoming activity、destination pair-zero 等额外身份。

# 2. 指定 aggregate M2：Schur 正性不等于原身份可提升

Exact 点使用 210 个 four-subsets 上的 signed `β`：10 个纯半集权 `1/8`、100 个 2+2 半集权 `−1/400`，总权 1。`β` 不是概率 law；它与 uniform `ν` 组合满足指定 Boolean/full-row aggregate moments，但跨半 `L(YX_iX_j)` 可为负，不能被解释成完整 true joint distribution。

独立稿在 45 个 pair monomial 与 10 个 `YX_i` 基上写 `G=[[A,δC],[δCᵀ,δD]]`，其中

`A=(1/14)I+(1/35)RᵀR+(1/210)J`, `A⁻¹=14I−(4/3)RᵀR+(1/4)J`。

`A` 的谱为 `4/5,3/10,1/14`；`D−δCᵀA⁻¹C` 在常数、半符号、半内 contrast 三个对称子空间的特征值分别为 `3767/3125, 37/20, 4547/100000`，全正。因此 aggregate 67×67 M2 PSD 且 rank=55（12 条 Boolean/row null relations）。作者 Proof read-after 使用更大的 210-dimensional four-subset 函数空间，Schur 三类特征值为 `10729/10000,59/40,2687/160000`，也全正；数值不同来自 Schur 空间不同，不是冲突。

聚合 M2 通过不能自动恢复原 token/head 身份，也不能当作完整原作业 CONFIG 或 native scheduling relaxation witness。

# 3. Formal lift 负平方与所有原身份 extension 的必要阻碍

在 `k=r=4,h=0,A=1`、保留 context `Y` 的点上，令 `s=(1,1,1,1,1,−1,−1,−1,−1,−1)`，`Q=Y Σ_i s_i(x_{1,i}−x_{2,i})`。由 `E_β(Σ_i s_iX_i)^2=20` 直接展开 formal uniform lift 得

`L'(Q²)=2δ−(8/3)δ=−(2/3)δ=−1/150`。

`Q` 为 degree two，所以这是 lifted M2 的真实负 Gram 范数；它精确否定该 uniform kernel 的 M2 正性。

更强的 given-point 结论不依赖 uniform kernel。若某 `Lhat` 保留完整 aggregate moments、原 one-hot/Boolean 与共同 M2，令 `P_a=Y Σ_i v_i x_{a,i}`，共同 M2 给出

`k Σ_a Lhat(P_a²)−Lhat((Σ_aP_a)²)=Σ_{a<b}Lhat((P_a−P_b)²)≥0`。

同 token cross-head 的零范数和 aggregate 守恒把左侧化成 `vᵀ[k diag_i L(YX_i)−(L(YX_iX_j))]v`。本点 `L(YX_i)=δ·2/5`，且 `D` 的半符号特征值为 2；`k=4` 时该 block 半符号方向值 `−2δ/5`，quadratic 为 `−4δ=−1/25<0`。因此**任何**保持此完整 aggregate functional 的原 token M2 extension 都不存在。作者 read-after 用 S4 平均法得到同一必要约束；它确认“uniform kernel 失败”不能缩写成“所有 extension 失败”，真正量词是 given-point necessary block。

# 4. 全局 affine-context K 与 ordinary witness

作者读后进一步把任意全局 affine contexts `z_0=1,z_1,…,z_s`（可含本组原 label）作为整体指标 `(i,l)×(j,t)`，必要矩阵为

`K_(i,l),(j,t)=k·1_(i=j)L(X_i z_l z_t)−L(X_iX_j z_l z_t) ⪰0`。

令 `t_i=Σ_l c_(i,l)z_l`、`B=Σ_iX_it_i`、`q_a=Σ_ix_(a,i)t_i−B/k`，则 `cᵀKc=kΣ_aL(q_a²)≥0`。`k=1` 时 K 由原 ideal 恒为零。单个不同 context 的 cross-block 未必 PSD；安全命题是整体 K 及其主子矩阵。对 bad aggregate point，取 `t_i=s_iY` 得 `cᵀKc=−1/25`，故该 given point 不能有原身份 extension；K 不是 sufficient criterion。

为分离矩非扩展与实际调度值，作者读后给 13-machine、6-job、48 finite-end ordinary witness：root job 留在唯一 root 端，四个 `f` jobs 分到四个不同 `z`，`y` 去 `y_0`，峰值为 1；root job 强迫 `OPT≥1`，故 actual OPT=1。它不是 native integrality gap、SH3 source reduction 或 near-two hardness。

# 5. 关系、缺口与处置

仓库已有 `Token-label桥canonical-v2新增全局语境块与读域审查`、`原任务标签提升的一阶PSD与全语境容量块`，它们整理 canonical v2 §7 的 affine-context K、旧 prefix 仅 hash 的读域，以及 raw SH3/ordinary scheduling 分界。本批独有去向是为 clean IDs `0a497…`、`87e962…` 保留 Exact-first→author-read-after 时序、原字节 SHA，以及独立 45-basis Schur 与作者 210-basis Schur 的差异；既有对象作为相关背景，不被本批重复取代。

不能由本批推出：旧 native-cycle prefix 已被本轮重新全文审查；所有 aggregate functional/所有 growing depth 都不可延拓；K 是充分条件；generic exact SDP finder、shared integer forest decoder、source-to-UM reduction、一般 UM near-two 正反结论或新颖性认证。作者 code/audit 未在本轮读取或重跑，作者 read-after 中提到的程序 SHA 只作 provenance 记录。

处置为 `given-point-moment-boundary-read`：两源已完整实读与比较，原件和 manifest 在 evidence，receipt 草稿单列。引用时须保留 `Q²=−1/150` 与 necessary K 负方向的不同量词、整体 context K 而非单独 cross-block、ordinary OPT=1 witness 的有限范围，以及 raw SH3/一般 UM 未完成义务。
