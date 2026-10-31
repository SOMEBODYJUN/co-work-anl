---
id: "unrelated-machines/raw-s3-to-canonical-sa1-same-point"
kind: "bridge"
type_tag: "资料"
title: "raw S3 到 canonical plain-SA1 的同点提取"
status: "proved-under-explicit-s3-contract-with-fixed-lp-boundary"
summary: "在显式 normalized-flat 菜单、同一 degree≤4 有理 functional L、Boolean/cover 等式乘子、每 box/物理 slack/unit-cap 行至多三个 raw-literal 乘子均非负的完整 S3 合同下，指定 pullback A_s=a_s、Z_e=a_sE_e 保持 canonical plain-SA1、resource/gate/quality rows；同点 raw M2 可选地给 canonical M1。固定次数 rational-LP 与输出位长多项式。该桥不把 raw K2、CONFIG 或实际共同 schedule 自动升级为 S3。"
source_refs:
  - "clean:8eb4c167d32fbb5529e7"
  - "clean:1dcf604fc03919848b61"
  - "clean:d760f7cca827d40995da"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_identity_coupling_raw_sa3_canonical_sa1_exact_reconstruction.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_identity_coupling_raw_sa3_canonical_sa1_author_proof_read_after.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_identity_coupling_raw_k2_sa3_final_v2_targeted_addendum.md"
---

# 来源身份和合同范围

三份来源共同审查 raw S3 到 canonical plain-SA1 的同点 pullback。Exact-only 独立重构、作者 Proof read-after 与 v2 triple 量词定向补记均完整读取。结论是一个**条件性桥**：给定完整 S3 functional 合同，可按指定公式把 raw moments 提取为 canonical entries；合同本身比 raw K2 强，不能从 raw K2、普通 CONFIG 或实际 schedule 自动得到。

| clean ID | 原路径 | SHA-256 | 大小 | 实读性质 | 本页处置 |
|---|---|---|---:|---|---|
| `8eb4c167d32fbb5529e7` | `history/source/notes/unrelated_machines/sol_identity_coupling_raw_sa3_canonical_sa1_exact_reconstruction.md` | `5ee6c219ebde7bd459ba1f5afa24442cb8111de21d3bbfd1fea9bbcdc664746e` | 11,264 B | Exact-first 独立重构 A/B/C、次数账、LP 复杂度 | 保存自足代数与量词 |
| `1dcf604fc03919848b61` | `history/source/notes/unrelated_machines/sol_identity_coupling_raw_sa3_canonical_sa1_author_proof_read_after.md` | `173148aa4baeac7d9fb66c6e4bad76c935999a9599d85473b56c9e0c9bcaa8b3` | 6,273 B | 作者 Proof 全文 read-after；逐节对照 S3 付款 | 保存证明一致性和 PSD/LP 边界 |
| `d760f7cca827d40995da` | `history/source/notes/unrelated_machines/sol_identity_coupling_raw_k2_sa3_final_v2_targeted_addendum.md` | `558c93fd068e01d8183a40bcf58096c9d3727a9dd8a9d6fc116d4cae3560cc5d` | 1,937 B | v1/v2 final 唯一 triple 量词 diff 定向实读 | 保存“全部 global triples 非负”精确范围，不扩成任意单 triple |

原件、manifest 在 `archives/unrelated-machines/tools/evidence/raw-s3-to-canonical-sa1-20261031/`，回执草稿在 `cleanup/workspaces/Boss2/raw-s3-to-canonical-sa1-receipts-20261031.json`。

# 1. raw S3 输入和 pullback 定义

Domain 是完整显式 normalized-flat menu：每 indexed state 系数非负且总和一；zero incidences、duplicate indexed states、unused resources 和未选 state jobs 全保留。普通 P 每组一个 unit selector、每 state 独立 private root、每枚 incidence 一个不可拆原 job，private 时间为原系数、resource 端时间为一。

同一共同有理 functional L 满足：degree≤4；所有原 Boolean identity 乘 degree≤2 monomial、每原 job cover equality 乘 degree≤3 monomial、每原 box/physical slack/unit-cap-1 行乘任意至多三个 raw literals 均有非负 L 值。等式乘子可有符号，但由逐 monomial 合同线性推出。给定有理 1≤T<2，epsilon=2−T。

对 state s selector raw variable a_s、incidence e 的 resource-head raw variable E_e，指定 pullback

`A_s := a_s`，
`Z_e := a_(s(e)) E_e`。

canonical primitive 补的 pullback 是

`1−a_s`，
`1−a_s E_e = (1−a_s)+a_s(1−E_e)`。

因此每项至多两个 raw literals；再乘一个 canonical primitive/complement 后，至多四个 raw literals，恰落在 S3 合同支付范围内。

# 2. A：实际 makespan 必要性与 sound FAIL

任意完整实际 schedule 峰值≤T<2 可取其 Dirac functional：每 job 恰选一个合法端，Boolean/cover 等式逐点成立，physical slack 非负；每 resource unit-head 端耗时一，故 T<2 使每 resource 至多一枚 unit job，unit-cap-1 行及其任意 raw-literal 乘子非负。private coefficient 为零的 incidence job 仍有 resource 端 unit 成本，不能漏掉。

反向不作声称，但 S3 不可行即可排除实际 makespan≤T。这是对全部普通合法 schedules 的必要性，不是只对某个 selector 选择或 canonical schedule。

# 3. B：Boolean、boxes、gates、组和 resource rows

Canonical 二阶 entries 直接读取 raw monomial：

`F(A_s)=L(a_s)`，`F(Z_e)=L(a_sE_e)`，

以及 `F(A_sA_t)`、`F(A_sZ_e)`、`F(Z_eZ_f)` 的相应 raw 表项，最高 degree 四。F(1)=1 且表对称。

Z_e 的 Boolean identity 由

`(aE)^2−aE=(a²−a)E² + a(E²−E)`

支付；selector group equality `H_g=sum_s a_s−1=0` 乘任意 canonical primitive/complement 时，pullback 次数至多二，落在原 cover equality 的次数三预算。

Boxes：每个 canonical positive primitive 或 complement 的 pullback 是非负 raw-literal 组合；再乘 box 行 primitive/complement，每项至多四 literals，直接由一个 raw box 行取一个 literal 作 box、其余作乘子支付。

Gates：`A_s−Z_e` 拉回为 `a_s(1−E_e)`，与任意 W 的 pullback 相乘仍至多四 literals，故 gate 的空、primitive、complement 乘子全部成立。

Resource row：原 unit-cap 行记

`C_u = 1 − sum_(e:u(e)=u) E_e`。

canonical resource slack 有恒等式

`1 − sum_e a_(s(e))E_e = C_u + sum_e (1−a_(s(e)))E_e`。

第一项乘任意 W 时使用 raw cap-1 localizer；补项每项至多四 literals，由 boxes 支付。没有把 cap1 替换成 T−sum E，也没有按 state/group 更换 moment 表。

# 4. Quality rows：S3 第三个 raw literal 的真实使用

state s 的 raw root slack 和 canonical quality pullback 分别为

`h_s = T − a_s − sum_(e in s) p_e b_e`，
`q_s = sum_(e in s) p_e a_s E_e − epsilon a_s`。

利用 `T+epsilon=2`、state 系数总和一和 incidence cover `b_e+E_e−1=0`，有普通多项式恒等式

`q_s − a_s h_s = (a_s²−a_s) + sum_(e in s) p_e a_s(b_e+E_e−1)`。

对任意 canonical multiplier W，第一项用 Boolean identity 预算，第二项用原 cover equality 预算；随后 `a_s * pullback(W)` 每项至多三个 raw literals，正好由 physical slack 的 S3 localizers 支付。W=Z_f 时出现 `h_s a_s a_(s(f)) E_f`，W=1−Z_f 时出现 `h_s a_s(1−a_(s(f)))` 和 `h_s a_s a_(s(f))(1−E_f)`，都未超过 degree 四。因而 canonical quality rows 的空、primitive、complement 乘子全部非负。

若只有 raw K2 一阶/二阶 localizer，这一步无法免费替代；它明确需要“原 slack 行乘至多三个 raw literals”的 S3 合同。

# 5. C：可选同点 raw M2 到 canonical M1

若同一点另有 raw M2：对任意 canonical affine polynomial

`ell=c0+sum_s c_s A_s + sum_e d_e Z_e`，

其 raw pullback 是 degree≤2 polynomial `ell~`，故

`F(ell²)=L(ell~²)>=0`。

这给 canonical M1 PSD，是给定有限有理证书的代数保持，不是从 S3 自动找到 PSD 点，也不是把任意实 PSD feasible point 替成有理 point。raw K2/SA3 与这一可选 PSD 层必须分开记录。

# 6. 固定次数 rational LP、提取和总位成本

原变量数 N 下，degree≤4 可交换 monomial 表为 O((N+1)^4)；每原 affine 行乘至多三个 raw literals 的数量为 O(R(N+1)^3)。每个 literal product 最多展开八项，系数是输入 binary rationals 的固定次和积，bit length 保持多项式。

若 S3 rational LP 可行，有限有界 polytope 有 rational vertex；选活跃独立行、清分母即可得到 polynomial-bit rational certificate，普通 rational LP 算法可输出 feasible point 或 infeasible。该结论只针对显式固定次数 S3，不提供 CONFIG separation、exact SDP finder 或指数 schedule enumeration。

Canonical primitive 数 O(N)，一/二阶输出表 O(N²) entries，均直接查询给定 raw monomial entries；重复索引保留原表示。无需 epsilon^-1、L(a_s)^-1 或最小概率倒数循环。

# 7. triple 量词澄清与和 raw K2 的边界

v2 定向补记只修改最终文稿中的一句量词：如果**要求所有 global triple literal 的期望非负**，则含 `L(b1b2b3)<0` 的特定证书会被排除；不能把它写成“任意一个 global triple 非负都排除”。本补记没有改变 S3 合同、raw K2 负式、matrix 或算法。

因此本桥的正确接续方式是：先明确给定同一 L 是否满足完整 S3（三 literal localizers、quality slack 与 unit-cap），再应用上述 pullback；不能从 raw K2 family 的 first/pair/affine rows 直接跳到 canonical SA1，也不能用 ordinary actual schedule 替代 S3 moments。

# 8. 本轮实际处置

三源均完整实读并比较 A/B/C 的定义域、literal 次数、quality 恒等式、resource decomposition、固定次数 LP/vertex 位长和 triple 量词。没有代码运行或实际 SDP/CONFIG 求解；原件和 manifest 在 evidence，正文归档为资料桥，回执草稿单列。它不证明一般 normalized Q 的 S3 可行性、不输出真实共同 schedule law、不完成一般 UM 舍入或 hardness。
