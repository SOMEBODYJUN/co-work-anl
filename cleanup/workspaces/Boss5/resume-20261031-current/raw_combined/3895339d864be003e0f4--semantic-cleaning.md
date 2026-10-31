---
id: "unrelated-machines/raw-k2-sa3-combined-final-sol-nsw-read-boundary"
kind: "review"
type_tag: "审查"
title: "Raw K2/S3组合最终两节：Sol-NSW实际实读与角色边界增量"
status: "integrated-increment"
truth_status: "exact-family-narrow-obstruction-and-conditional-point-bridge"
review_level: "full-source-review-and-related-material-comparison"
summary: "完整读取 Boss5 源3895339d864be003e0f4：记录者对最终 canonical §13 做 Exact-first 独立重构后的知情实读，对 §14 只作作者一致性复核；保留 18机/17job/34端的跨行负三重矩障碍、一般 raw-S3 到 canonical-SA1 同点桥、v1/v2 量词边界以及软件/旧前缀不认证范围。"
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
---

# 处置对象和精确阅读范围

这是对 cleanup 源 `3895339d864be003e0f4` 的自足语义增量，不是把清洗记录伪装成第三个数学证明。源文件本身为 70 行、8,901 bytes，SHA-256 `5b7f9644ef735350132e803020376181bf0b4c46a2f36fc5d1d64ff2cbc82d47`；本地副本与其一致。它所审的 canonical 原件为
`single_outer_flat_with_raw_k2_boundary_and_sa3_repair_final_v1.md`，48,840 bytes、702 行、SHA-256
`404cf16df23cffe7b7c61c498907b744047473cf2d2db4e403630e5b6279edd2`。

源记录明确区分阅读范围：新 canonical 原件第 375--702 行（§13、§14 和最后 review link）逐行读完；旧 1--374 行仅做 25,741 bytes 前缀 hash `8c5fcf273f9cd99a7b31b6b082a0880fc7ce186a0771cf600241eb07cc86e221` 对照，未重签旧两算法或旧程序。本文因此不会把“新两节实读”升级为旧前缀的重新审查，也不把未打开的 linked review 当作已认证对象。

`3895339d864be003e0f4` 的记录者身份是：§13 先做 Exact-first 独立重构、待作者 Proof 释放后再读最终组合；§14 为作者本人，只能作一致性/准确性复核，不能独立认证自己的 §14。这个角色分工是本源的独有审查事实。它与 `d38bc86e1cf24e270a1a`（Sol-identity coupling 的知情 final read）共享同一个 canonical SHA 和 §13--14 数学，但 d38 没有把 §13 叫作 Exact-first；两源不能合并成两次独立盲审。两源均只对列明新增范围负责。

# §13：完整 raw K2 local-law 的指定 canonical 拉回障碍

固定参数为二进制有理 `0<c<1`、`T=1+c`、`epsilon=1-c`。普通 unrelated-machines 菜单有一个二态 outer `M`、四个二态 helper，共 10 个 indexed states；资源 `u,v,r,s,w_u,w_v,w_r,w_s` 互异，10 个 state-private roots 也互异。完整 compiler 保留五个 unit selector、12 个 incidence job、全部两个 finite endpoint，得到 18 台机器、17 个作业和 34 个 finite endpoints；没有删除零/恒定端、没有加 export≤activation guard，也没有把 selector 或 incidence 合并。

三位 Boolean 变量 `b1,b2,b3` 给出全部端点的 affine literals。代表性端为：`M/0` selector `b1`，其 `u` resource head `b2`、`v` head `1`；`M/1` selector `1-b1`，其 `r` head `1`、`s` head `1-b3`；`H_s/0` selector `b3`。每 incidence 的 private/resource 两端互补，每组两个 selector 端互补。因此每个原 Boolean、job one-hot 与 degree≤4 的乘子恒等式在同一三位商代数成立。

共同 functional `L` 由
\[
L(1)=1,\quad L(b_i)=3/10,\quad L(b_ib_j)=3/80,\quad L(b_1b_2b_3)=-1/160
\]
给出，重复位按 Boolean 约化。其 signed cube weights 是 000 和三个 singleton 各 `35/160`，三个 doubleton 各 `7/160`，111 为 `-1/160`。对任意三位 degree≤2 多项式，三阶差分恒等式和 weighted Cauchy 常数
`4(160/35)+3(160/7)=608/7` 给出
\[
L(q^2)\ge(16/35)S\ge0,
\]
其中 `S` 是七个正权 cube 点的加权平方和。故 global `M2` 对完整 34 端点的 596 个 square-free degree≤2 monomials 均成立；这不等于全局 triple-literal 非负。

两条 outer private 的 raw slack 是
\[
(1-b_1)+cb_2,\qquad b_1+c(1-b_3),
\]
其余机器为常数 `c` 或 `c` 加一个 literal。对每个原全局 affine `q` 和任一 literal `l`，`lq` 的次数至多二，且 `L(lq^2)=L((lq)^2)\ge0`；所以全部物理 raw-load localizer 对所有 `0<c<1` 成立。每台机器端只依赖最多两位，使用对应真实 two-bit marginal
`(35,21,21,3)/80`，可给出完整合法 CONFIG law，并与该行全部 membership moments 一致。各行 law 不拼成共同 global schedule law。

实际 schedule 选择 `M/0,H_u/1,H_v/1,H_r/0,H_s/0`，选中 incidence export 到互异 unit resources，其他 incidence 留在 private；17 个 job 的峰值为 1，unit selector 给下界，故 `OPT=1`。指定 direct canonical extraction 为 selector 端乘 resource-export 端：
\[
A_{M0}=b_1,\quad Z_{M0u}=b_1b_2,\quad Z_{M0v}=b_1,\quad A_{H_s0}=b_3.
\]
于是 canonical claim 行乘 `A_{H_s0}` 的同点值是
\[
L(Z_{M0u}A_{H_s0})=-1/160<0.
\]
state-0 activation quality 的 pullback 为 `h'=cb_1b_2`，其乘 `A_{H_s0}` 的值为 `-c/160<0`。三个因子来自三台不同物理机器；每行的完整 local law 因而无法支付这个跨行 triple。这里失败的是指定、同一点的 direct pullback，不是原实例不可排程、不是 `OPT>1`、不是 SA1 对所有点不可行。

`h'` 同时等于 `A_{M0}` 乘原 raw slack。取 raw-affine `q=b3` 时 `L(h'q^2)=-c/160`，总原次数为 4；这只证明 raw slack 的 affine localizer 不能自动转成 activation slack 的同类 localizer。不能把任意 canonical affine 测试免费降成 raw affine：canonical claim 已含 raw quadratic，平方测试可能要 degree 6。若额外要求所有 global triple literal 的期望均非负，因本点 `L(b1b2b3)<0` 会被排除；不能改写成“任意一条不相关 triple 非负就排除”。

# §14：完整 raw S3 到 canonical plain-SA1 的同点桥

源 §14 的正式身份是 `UM-RAW-SA3-CANONICAL-SA1-POINT-PULLBACK-v1`。输入是任意显式 normalized-flat 菜单：有限非空 groups/states、每 state incidence 系数总和一、全部 selectors/incidences/zero entries/重复 states/unused resources 和 finite endpoints 均保留。阈值为有理 `1≤T<2`，`epsilon=2-T`。给定共同有限有理 raw degree≤4 functional `L`，要求每个原 Boolean 乘子（degree≤2）、job one-hot 乘子（degree≤3），以及每个原 box、physical load slack、**unit-resource cap1** 行乘全部长度≤3 raw literals 都付款。

对 state selector `a_s` 和 incidence resource head `E_e` 指定
\[
A_s=a_s,\qquad Z_e=a_sE_e.
\]
所有 canonical degree≤2 entries 只需 raw degree≤4。补项使用
`1-a_sE_e=(1-a_s)+a_s(1-E_e)`，所以长度≤4 的 raw cylinders 都可由 box+至多三个 literal 付款。Resource identity 为
\[
1-\sum_{e:u(e)=u}a_{s(e)}E_e
=(1-\sum_{e:u(e)=u}E_e)+\sum_e(1-a_{s(e)})E_e,
\]
第一项必须用 cap1 行，不能以 `T-ΣE` 偷换。

令原 state-private slack 为 `h_s`，quality pullback 为
`q_s=Σ_{e∈s}p_ea_sE_e-(2-T)a_s`。由 job identity、`Σp_e=1` 和 Boolean identity，差值
\[
q_s-a_sh_s=(a_s^2-a_s)+\sum_{e\in s}p_ea_s(D_e+E_e-1)
\]
在 `L` 下为零。任意 canonical multiplier `W∈{1,V,1-V}` 的拉回最多再添三 raw literals，正好由 physical slack 的三-literal lifts 付款。因此完整 canonical plain-SA1 的 boxes、gates、resource 和 quality rows 均成立。若同一点另给 raw M2，则 affine canonical test 的 raw pullback 只有 degree≤2，可选得到 canonical M1；S3 本身不含 M2、CONFIG 或全局 schedule law。

真实 makespan≤T 的完整 schedule 的 Dirac 表是 S3 可行点，因为 `T<2` 使每 unit resource 至多接一个 unit job，故 cap1 也逐点成立；所以 S3 不可行推出真实 threshold-T 不可行。S3 可行只给 relaxation point，不能反向给 actual schedule。固定 degree rational LP 的 moment 数为 `O(N^4)`，约束和系数位长多项式；vertex/Cramer/Hadamard 给有理 witness 位长界。§14 无软件、checker 或 run，不能由 §13 的固定族 audit 补签。

# 来源比较、独有内容和去向

本源与现有正式资料/审查的交集是上述 §13 数学、§14 S3 桥及 v2 triple 量词纠正；这些内容已分别存在于以下对象中，故不另造重复定理：

- `archives/unrelated-machines/state/审查/K2局部行律拉回障碍--审查.md`：固定 c 的 audit、18m/17j/34端 local-law 障碍、OPT=1 和有限程序边界。
- `archives/unrelated-machines/state/资料/rawS3到canonicalSA1同点提取--资料.md`：S3 输入、同点 pullback、quality/resource identities、sound FAIL 与位长。
- `archives/unrelated-machines/state/审查/完整原端三次条件的作者合同与拉回证明--审查.md`：作者 Exact/Proof 合同的逐项来源和证明义务。
- `archives/unrelated-machines/state/审查/单层平方根配额与单外层选择器双源审查--审查.md`：同一 canonical 载体中 typed 13/8、§13 障碍和 §14 桥的模型边界。

本源的真正新增是可复核的审查身份/次序和范围分层：§13 是 Sol-NSW 在独立重构之后的知情复核；§14 是同一记录者作为作者的非独立一致性复核；旧前缀、未读 linked review、程序和全局新颖性都明确排除。其 unique 内容建议作为上述三个审查对象的增量段落登记，而不是提升为单独数学 theorem。与 d38 源重合的矩阵、PSD、local-law、negative values、S3 identities 和 v2 one-line diff，只保留一次对象边；d38 的角色差异另作审查元数据，不作为独立数学证据。

建议正式整合路径（由 Boss 串行检查关系后写入）：

1. §13 的身份与 negative `-1/160,-c/160` 范围，增量挂到 `K2局部行律拉回障碍--审查.md` 和 `Raw-K2与SH3条件流两源精读--审查.md`；保留“给定点 direct pullback”边界。
2. §14 的 cap1/quality identity/S3-only 边界，增量挂到 `rawS3到canonicalSA1同点提取--资料.md` 与 `完整原端三次条件的作者合同与拉回证明--审查.md`；保留 `S3↛CONFIG/M2` 和“可行只给 relaxation”边界。
3. v2 唯一 diff（全部 global triple 非负量词）挂到 `单层平方根配额与单外层选择器双源审查--审查.md` 及 raw K2/S3 review；不得将它写成任意单 triple 约束。
4. 本源原始 389 文件和 404cf/d2b004 source evidence 作为审查 provenance 留在 cleanup/evidence 路径；不修改共享正文，不增加不真实超边，不把 §13 审查当 software PASS。

# 最终决定

对 Boss5 清洗，本源的 disposition 为 `integrated-increment`：它的数学主张和证据已由现行对象承载，但本源增加不可丢失的审查角色、实际阅读区间、旧前缀不重签、§14 作者非独立认证以及 v1/v2 量词边界。没有额外原件需求；继续工作所需的 canonical v2、两份 Exact/Proof、审查文件和有限 audit evidence 均已在仓库可读路径中。一般 UM 目标、全局 schedule law、全局 triple 非负、所有 canonical extraction 失败和外部新颖性均保持 OPEN。
