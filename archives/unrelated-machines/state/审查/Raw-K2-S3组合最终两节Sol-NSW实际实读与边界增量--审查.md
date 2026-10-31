---
id: "unrelated-machines/raw-k2-sa3-final-sections-read-increment"
kind: "review"
type_tag: "审查"
title: "Raw K2/S3 合并 final §13–14：389 源实读增量"
status: "integrated-increment"
truth_status: "exact-for-listed-source-and-read-scope"
review_level: "full-source-read-cross-object-comparison"
summary: "完整读取 cleanup 源 3895339d864be003e0f4，并重核其所指 canonical final 的新增 §13–14：§13 是 Exact-first 重构后的知情复核，保留 18 机/17 job/34 端跨行负三重矩与 OPT=1；§14 是作者对同点 raw-S3→canonical-SA1 桥的一致性核对，保留 cap1、quality 恒等式、固定次数 LP 和严格量词边界。该源是审查身份与版本范围增量，不另造定理或软件 PASS。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_raw_k2_sa3_combined_final_actual_read.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_raw_k2_sa3_combined_final_actual_read.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/single_outer_shared_selector_rounding_and_hardness_source_boundary.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/single_outer_shared_selector_rounding_and_hardness_source_boundary.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_identity_coupling_raw_k2_sa3_final_v2_targeted_addendum.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_raw_sa3_to_canonical_sa1_exact_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_raw_sa3_to_canonical_sa1_author_proof_v1.md"
legacy_ids:
  - "3895339d864be003e0f4"
  - "UM-RAW-K2-LOCAL-LAW-DIRECT-CANONICAL-PULLBACK-OBSTRUCTION-v1"
  - "UM-RAW-SA3-CANONICAL-SA1-POINT-PULLBACK-v1"
related_objects:
  - "unrelated-machines/sol-general-repair-k2-local-law-canonical-pullback-v1"
  - "unrelated-machines/raw-k2-local-law-canonical-pullback-obstruction"
  - "unrelated-machines/raw-s3-to-canonical-sa1-same-point"
  - "unrelated-machines/raw-s3-author-contract-proof-history"
  - "unrelated-machines/raw-k2-sh3-conditional-flow-two-source-review"
---

# 1. 来源、完整阅读与范围

本增量清洗的唯一源是
`cleanup/workspaces/Boss5/resume-20261031-current/3895339d864be003e0f4.md`，其本地实核为 70 行、8,901 bytes、SHA-256
`5b7f9644ef735350132e803020376181bf0b4c46a2f36fc5d1d64ff2cbc82d47`。
`cleanup/workspaces/Boss5/resume-20261031-current/sources.json` 将它绑定到
`history/source/notes/unrelated_machines/sol_raw_k2_sa3_combined_final_actual_read.md`
的 legacy-cleanup 提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 main 提交
`aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`；这两个冻结路径版本在元数据中是同一源身份。

源声称的 canonical 载体为
`single_outer_flat_with_raw_k2_boundary_and_sa3_repair_final_v1.md`，实核 702 行、48,840 bytes、SHA-256
`404cf16df23cffe7b7c61c498907b744047473cf2d2db4e403630e5b6279edd2`。本轮按源记录逐行读完新增 375–702（§13、§14 与末尾 review link）；旧 1–374 仅以 25,741-byte 前缀 SHA
`8c5fcf273f9cd99a7b31b6b082a0880fc7ce186a0771cf600241eb07cc86e221`
作完整性核对，未把旧两算法、旧程序或旧证明重新签署。链接指向的 review 没有在本轮打开。

审查身份必须作为数学成熟度的一部分保留：§13 的记录者先完成 Exact-first 独立重构、再在作者 Proof 释放后读取最终组合，故是**知情最终复核**；§14 的记录者就是该节作者，只能作一致性/准确性复核，不能独立认证自己的 §14。该身份不同于近邻 d38 源“§13 非 Exact-first”的记录；两源共享同一 canonical SHA 和数学结论，但不能合并成两次独立盲审。

# 2. §13：参数化 raw K2 证书和 direct canonical 障碍

输入量词是二进制有理 `0<c<1`，`T=1+c`，`epsilon=1-c`。普通 unrelated-machines 编译保留一个二态 outer 与四个二态 helper，共十个 indexed states；十个 state-private roots 与八个互异资源组成 18 台物理机器。五枚 unit selector 和十二枚 incidence job 各保留两个 finite endpoint，共 17 jobs、34 endpoints。没有删掉零/恒定端、没有加入 `exports<=activation` guard、没有把 indexed states 合并。

三位 Boolean `b1,b2,b3` 替代全部原端点变量；每个 selector 两端互补，每个 incidence private/resource 两端互补。共同有理 functional 的 cube 矩为

\[
L(1)=1,\qquad L(b_i)=3/10,\qquad L(b_ib_j)=3/80,\qquad L(b_1b_2b_3)=-1/160.
\]

等价 signed-cube 权为 000 与三个 singleton 各 `35/160`、三个 doubleton 各 `7/160`、111 为 `-1/160`。因此原 Boolean、one-hot 和 degree-4 内允许的 job-cover 等式都在同一张全局表中成立；没有按机器拼接不同矩。

## 2.1 全局 M2、raw localizers 和逐行 law

任何原 degree≤2 多项式拉回都落在七维基
`(1,b1,b2,b3,b1b2,b1b3,b2b3)`。源中的全参数证明使用三阶差分和正权七点平方和 `S`：weighted-Cauchy 常数为
`4(160/35)+3(160/7)=608/7`，故

\[
L(q^2)\ge (16/35)S\ge0
\]

对全部 raw quadratic squares 成立。这个 M2 不要求三次 literal 非负，故不排除 `L(b1b2b3)<0`。

两条 outer private raw slack 为 `(1-b1)+c b2` 与 `b1+c(1-b3)`；其余 raw physical slack 为常数 `c` 或 `c` 加一个 literal。对任意 raw-affine `q` 和任意 literal `l`，`lq` 的次数至多二且
`L(l q^2)=L((lq)^2)>=0`，所以全部 raw affine load localizers 对参数域成立。

每台机器的端点至多依赖两位，取相应 two-bit marginal
`P(00),P(10),P(01),P(11)=(35,21,21,3)/80`
可给出完整的 row CONFIG membership law；两台 outer row 的非空配置均有 load 至多 `T`，其他行只依赖一位或常数。这里的“完整”是每行内部的 membership law，不是把不同机器 law 拼成一份 global schedule law。

## 2.2 实际调度与负值的精确量词

选择 `M/0,H_u/1,H_v/1,H_r/0,H_s/0`，把选中 incidence 导出到互异 unit resources，其他 incidence 留在 private roots。17 个原 job 均执行一次，峰值为 1；unit selector 给下界，所以该实例的真实 `OPT=1`。

指定 direct canonical extraction 为 selector 端与 resource-export 端的乘积：

\[
A_{M0}=b_1,\qquad Z_{M0u}=b_1b_2,\qquad Z_{M0v}=b_1,\qquad A_{Hs0}=b_3.
\]

于是 canonical claim 行乘 `A_Hs0` 的同点值为
`L(Z_M0u A_Hs0)=-1/160<0`；state-0 activation-quality pullback 为 `c b1 b2`，再乘 `A_Hs0` 得 `-c/160<0`。三个因子来自三台不同物理机器，故各行完整 local law 仍无法支付跨行三重矩。结论只是否定**这个给定 L、这个 extraction、这个同点**的 plain primitive-SA1 pullback；它不否定换一个 SA1 点、改 extraction、重新求解、实际调度或一般 UM。

另一个可复核边界是：raw slack `h' = c b1b2` 等于 `A_M0` 乘原 raw slack。取 raw-affine `q=b3` 时 `L(h' q^2)=-c/160`，总 raw 次数为 4；这仍不能升级为“所有 canonical-affine square 都负”，后者含 canonical quadratic claim，平方可能需要 degree 6。若额外要求**所有** global triple literals 非负，本点会被排除；v2 补记不能改写成“任意一条不相关 triple 非负即可排除”。

# 3. §14：raw S3 到 canonical plain-SA1 的条件桥

该节正式对象是 `UM-RAW-SA3-CANONICAL-SA1-POINT-PULLBACK-v1`。它的量词是任意显式 normalized-flat 菜单、任意有理 `1<=T<2`、`epsilon=2-T`，以及同一点给定的共同有理 raw degree≤4 functional `L`。所有 groups/states、zero incidences、duplicate indexed states、unused resources、原 selectors 与 private/resource finite endpoints 均保留。

S3 合同同时支付：

* 每个 raw Boolean identity 乘 degree≤2 monomial；
* 每个原 job cover identity 乘 degree≤3 monomial；
* 每个 raw box、physical load slack 和每个 resource 的 **unit-cap1** 行乘任意长度≤3 raw-literal product，均非负。

指定
`A_s=a_s`、`Z_e=a_(s(e))E_e`。所有 canonical degree≤2 entries 只用 raw degree≤4。补项的正展开
`1-aE=(1-a)+a(1-E)`
使 boxes、gates 和 resource 补项至多四个 raw literals；resource 还必须用

\[
1-\sum_e a_{s(e)}E_e
=\left(1-\sum_e E_e\right)+\sum_e(1-a_{s(e)})E_e,
\]

其中第一项明确付款给 cap1 行，不能用 `T-sum E` 偷换。

令原 state-private slack 为
`h_s=T-a_s-sum_{e in s}p_eD_e`，canonical quality pullback 为
`q_s=sum_{e in s}p_e a_s E_e-(2-T)a_s`。由 `sum p_e=1`、Boolean identity 与原 job cover identity 有精确恒等式

\[
q_s-a_sh_s=(a_s^2-a_s)+\sum_{e\in s}p_ea_s(D_e+E_e-1).
\]

对任意 canonical multiplier `W`（空、primitive 或 complement），最后的 `a_s pullback(W)` 至多三个 raw literals，正好落入 S3 physical-slack localizer；Boolean defect 和 job-cover 项分别用其规定次数支付。因此在完整 S3 合同下，canonical boxes、gates、resource rows 与 quality rows 全部成立。

若同一点另给 raw M2，则 canonical affine test 的 pullback 仅为 raw quadratic，得到可选 canonical M1；S3 自身不含 M2、CONFIG law 或 global schedule law。真实 makespan≤T 的完整 schedule 的 Dirac table 满足 S3（`T<2` 强制 unit resource 至多一个 unit job），所以 S3 infeasible 是 sound FAIL；S3 feasible 只给 relaxation point，不给实际 schedule。固定次数 rational LP 的 moment 数、literal constraints、系数位长和 vertex/Cramer/Hadamard 输出位长均多项式；§14 没有实现、checker 或 run。

# 4. 交叉比较、独有内容和成熟度

本轮全文比较了以下正式对象的完整正文：

1. `sol-general-repair-k2-local-law-canonical-pullback-v1`：18 机全参数族、M2/raw localizer、逐行 full law、`OPT=1` 和 `-1/160,-c/160`；
2. `raw-k2-local-law-canonical-pullback-obstruction`：固定 `c=3/4` 的有限 audit、72 个 local checks、三点参数回归和软件边界；
3. `raw-s3-to-canonical-sa1-same-point` 与 `raw-s3-author-contract-proof-history`：S3 输入、cap1/quality identity、sound FAIL、LP 位长和作者来源次序；
4. `raw-k2-sh3-conditional-flow-two-source-review`：K2 给定点 non-extension、S3 point pullback 与 SH3 flow/decoder 未解边界；
5. `single-layer-quota-single-outer-selector-review`：同一 canonical 载体中 typed 13/8 算法、raw K2 障碍、S3 桥三者的模型和量词分隔；
6. d38 raw_identity staging/report、receipt 和 final-sections review：同一 canonical SHA 的近邻读者记录及其不同角色声明。

交叉结果是：389 的数学主线与既有十八机 K2 对象和 S3 资料桥重合，不应伪造新定理或新 software evidence。389 的不可丢失新增是来源级审查身份和边界：§13 为 Exact-first 之后的知情复核；§14 为作者自文一致性复核；前缀 374 不重签；`h'=c b1b2`、`q=b3` 的 degree-4 负 localizer 与可能需要 degree-6 的 canonical-affine square 分层；未读 linked review、未运行 Fraction audit/root replay、未认证 §13 程序以及不升级一般 schedule/SA1/硬度结论。

成熟度应分开记录：

* **已支持（精确、给定范围）：** 参数化 18m/17j/34e raw K2 证书的 M2、raw affine localizers、逐行完整 membership law、实际 `OPT=1` witness、direct pullback 的两项负式；以及给定完整 S3 contract 的同点 pullback identities、sound FAIL 和固定次数 LP 位长。
* **有限或条件：** 旧 audit 的 c=3/4、三点回归、代码输出和固定规模运行；它们不能替代全参数符号推导，也不能从未运行状态升级软件 PASS。S3 结论是给定 functional 的条件桥，不是从 raw K2 自动得到 S3。
* **仍开放：** 全局联合 schedule law、所有 canonical extraction/所有 SA1 点、实际 schedule 由 S3 可行点反推、一般 UM 近二 gap、hardness、全局 triple positivity 和外部新颖性。

# 5. 正式路径建议和处置

本增量建议作为 provenance/scope review，接续而不替换既有对象：

* §13 身份、跨行负式和旧前缀/软件边界，挂到 `archives/unrelated-machines/state/审查/K2局部行律拉回障碍--审查.md` 及 `Sol通用repair-k2全局local-law与canonical-pullback三源审查--审查.md`；
* §14 的 cap1、quality identity、S3-only 和 LP 位长边界，挂到 `archives/unrelated-machines/state/资料/rawS3到canonicalSA1同点提取--资料.md` 及 `完整原端三次条件的作者合同与拉回证明--审查.md`；
* v2 的唯一量词修正（所有 global triples，而非任意单 triple）与载体/角色差异，可在 `单层平方根配额与单外层选择器双源审查--审查.md` 留增量引用；
* 与 d38 建立“近邻 provenance/角色比较”边，不把两源计作两次独立盲审。

该文件只在 retry 工作区提供自足增量；不修改共享正文、Git、认领、认证或原件，也不创建不存在的超边。额外原件需求为“无”：继续检查所需 canonical 载体、Exact/Proof、v2 补记和现有 evidence 均已在仓库可读路径中。
