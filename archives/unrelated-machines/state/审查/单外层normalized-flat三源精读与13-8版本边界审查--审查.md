---
id: "unrelated-machines/one-outer-normalized-flat-three-source-review-20261031"
kind: "review"
type_tag: "审查"
title: "单外层 normalized-flat 三源精读与 13/8 版本边界审查"
status: "complete-source-read-version-separated-integrated"
truth_status: "typed-one-outer-epsilon-and-13-8-scoped-results-no-general-UM"
review_level: "clean-show-full-read-cross-object-comparison"
scope: "one_outer_full_primitive_sa1_rounding_exact_v1、one_outer_normalized_flat_13_8_approximation_exact_v2、one_outer_normalized_flat_13_8_author_proof_v2"
summary: "v1 source 是给定 primitive-SA1 可行点下的 epsilon²/4 结构性舍入陈述；v2 Exact 取消 supplied point 假设，提出显式 typed one-outer normalized-flat Q 上 13/8 算法合同；v2 Proof 用 11 次 rational threshold LP、CDF-max welfare rounding、完整 P_gate 值恒等和固定 margin 完成证明。三源均严格限制在单 outer、互异 home、shared fallback typed 域，不扩展一般 UM-TARGET。"
source_refs:
  - "source:0f20dfac4647048db69c:history/source/notes/unrelated_machines/one_outer_full_primitive_sa1_rounding_exact_v1.md"
  - "source:3858f37087ca3c8a80f0:history/source/notes/unrelated_machines/one_outer_normalized_flat_13_8_approximation_exact_v2.md"
  - "source:47c955a8da722b2e7a1c:history/source/notes/unrelated_machines/one_outer_normalized_flat_13_8_author_proof_v2.md"
related_objects:
  - "../审查/单层平方根配额与单外层选择器双源审查--审查.md"
  - "../审查/多outer双资源后端与tiny-home算法边界有限审查--审查.md"
  - "../审查/归一化门控菜单v2三源精读与13-8算法版本审查--审查.md"
  - "../计算/配置激活与有限覆盖增量审计--计算.md"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/one-outer-v1-v2-sources-20261031/"
---

# 1. 来源身份与全量阅读

三份来源均 `clean claim` 后 `clean show` 导出并逐全文读取；两冻结提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 内容一致。

| ID | 路径 | blob | 字节 | SHA-256 |
|---|---|---|---:|---|
| `0f20dfac4647048db69c` | `one_outer_full_primitive_sa1_rounding_exact_v1.md` | `54dfd679e6cbf78764e50164437b7757cef2a7fc` | 3,283 | `7364055e2c13a8962b5a022f959721014fb6219465dbe0340676521ac9437eac` |
| `3858f37087ca3c8a80f0` | `one_outer_normalized_flat_13_8_approximation_exact_v2.md` | `e4c6f716fc106ee73f48dfbcae1920d0b27c2ad6` | 3,532 | `81b1c6e81d6472aeb55563a6916b8a9a0710cde6718a0c97f80939756a7fdc69` |
| `47c955a8da722b2e7a1c` | `one_outer_normalized_flat_13_8_author_proof_v2.md` | `c15db9a23cc30f5f2473f7ef44f123eb3455091c` | 9,575 | `2a6af63654c9ec36a3a83da47b4cdb95065aa298012369cf7c87dbfa5f226eaf` |

证据目录保留三份 source bytes 和 manifest。现行 `单层平方根配额与单外层选择器双源审查--审查.md` 已整合同一对象，但本批新增 history/source provenance、v1/v2 量词对照和作者 Proof 的逐式来源。

# 2. v1：给定 primitive-SA1 点的 epsilon²/4 陈述

`full_primitive_v1.md` 定义单 outer `M`、每个 indexed state 的互异 home、每个 home 的 singleton helper，以及与 homes 不交的 shared fallback 资源 (B)。普通 normalized-flat UM 矩阵保留全部 selector、每个 state-resource incidence、零 incidence、重复索引、未选 state jobs 和 unused resources。

对每个 rational (0<\epsilon\le1)，primitive SA1 系统包含每组状态分区、box/gate、资源容量和每状态质量 (\ge\epsilon A) 的 rows，并将每一行乘同一原始 (A/Z) primitive 及其 complement；使用一个共同有理二阶数组，但不要求 PSD 或真实 joint law。

v1 的 scoped 结论是：**给定**可行共同 primitive-SA1 点，可确定性总位多项式构造不交 all-group allocation 和完整 schedule，满足

\[
V\ge\epsilon^2/4,
\qquad
C_{\max}\le2-\epsilon^2/4.
\]

它不提供可行点搜索，不解决多个 outer、无 own home 的 helper、一般 multicore menus 或一般 UM。该源与 v2 的区别是关键：v1 的可行点是输入，v2 必须从 Q 自行构造和解 LP。

# 3. v2 Exact：typed Q-only 的 13/8 算法合同

`normalized_flat_exact_v2.md` 保留相同单 outer、互异 home、shared fallback 结构，但将结论加强为：对每个显式 typed normalized-flat Q，仅输入 Q，本身不输入 OPT、福利分配、primitive-SA1 点、oracle 或精度参数，存在单一确定性总位多项式算法输出全部 original jobs 的 assignment，使

\[
C_{\max}\le(13/8)\operatorname{OPT}(P(Q)).
\]

输入允许 zero、duplicate indexed states、unused resources；完整矩阵需保留所有原 jobs。该版本不负责从任意 ordinary matrix 识别 typed presentation，也不扩到多个 outer、无独立 home 的 helper、隐式深树或一般 UM。

Exact v2 仍把可用 primitive-SA1 作为算法内部可选工具：每个阈值 (\epsilon) 的 rows 与原 (A/Z) primitive 的 complements 组成显式有理 LP；点不是输入，需算法自行求解。Exact 文件本身不含 proof、threshold recipe 或实现。

# 4. Author Proof v2：完整 13/8 推导

## 4.1 P_gate 值恒等

给定 outer typed menu 的不交 allocation，定义最大最小 bundle quality (V)。完整普通矩阵的精确值桥为

\[
1\le\operatorname{OPT}(P(Q))=2-V\le2.
\]

正向把 selected state 的 allocated positive incidences 导出 resource machines，未选 state jobs 留 private；反向若 (C<2)，每个 resource 至多承载一个 unit incidence，selector/selected-private 负载恢复不交 bundle，得到质量至少 (2-C)。该 identity 计入所有原 jobs，不能用 relaxation 或删 job 代替。

## 4.2 Primitive-SA1 阈值 LP 与同一矩行条件化

对阈值 (\epsilon) 求 plain common primitive-SA1 LP。若 (V\ge\epsilon)，真实 allocation 的 Dirac state/claim 点给可行证书，因此 LP FAIL soundly 推出 (V<\epsilon)。算法不把 LP feasible 当实际 allocation。

singleton helper 的 own-state (A) 与 claim (Z) 由共同二阶数组给 (\mu_A=\mu_Z=Y_{AZ})，再由 gate rows 得 (Y_{AF}=Y_{ZF})。选一个有正 outer marginal 的状态并条件化，得到同一个矩行中的 fallback state/claim marginals：

\[
\sum_jw_jb_j\ge\epsilon,
\quad f_j\ge b_j,
\quad \sum_up_{jsu}\zeta_{jsu}\ge\epsilon\alpha_{js},
\quad \sum_{j,s}\zeta_{jsu}\le1.
\]

这是一份共同 fractional packing；不能把每个 helper 单独找的 fallback 点直接相加。

## 4.3 CDF-max welfare rounding 和有理去随机化

每 helper 按 conditional state marginals 选 fallback state，按 claim/state ratio 请求资源；每个资源交给 (w_jp_{jsu}) 最高的 helper。对 score level (d) 定义 (\beta_j(d))，资源容量给 (\sum_j\beta_j(d)\le1)。跨 helper 独立性给

\[
\Pr(\max\text{ score}\ge d)
\ge1-e^{-t(d)}
\ge(1-1/e)t(d),
\]

因而 weighted welfare (W>5\epsilon^2/8)。有限原始 score levels 上逐个 helper state、再逐个 selected-state claim coin 做精确条件期望去随机化；每一步选最大条件期望，不使用无理数比较，空算法选项不成为物理 state。

## 4.4 固定 rational margin

置

\[
a=13/8,\quad b=10/8,\quad d=1/256,
\quad q=a\epsilon-b+d.
\]

若 (q>0)，则

\[
\frac58\epsilon^2>2q-q^2.
\]

若 Good helper 的 home 权总和不超过 q，则 (W\le2q-q^2) 矛盾；故 Good 权 (>q)，恢复 all original jobs 得 (C\le2-q)。

## 4.5 11 次阈值二分、失败分支和位复杂度

算法固定做 11 次 rational LP：([l,h]=[0,1])，测试 (\epsilon=(l+h)/2)，可行抬高 l 并保留点，不可行降低 h。最终 (h-l=1/2048)。若 (q\le0)，使用 (C\le2) baseline，并由 (V<10/13) 证明 (2<(13/8)(2-V))；若 (q>0)，用 (l) 证书得到 (C<(13/8)\operatorname{OPT})。

所有 LP、conditioning、CDF products 和原 jobs 回填按显式 state/claim 数及输入有理位长计算，循环次数固定 11，不按 denominator、accuracy 或 tiny marginal 迭代。零 incidence、duplicate state、unused resources、未选 outer-state payload 全部保留。

# 5. 与既有对象的关系和边界

既有 `单层平方根配额与单外层选择器双源审查--审查.md` 已整合 v1 supplied-point、v2 typed-Q 13/8、CDF backend、11 次二分和近二源排除。本批三源的独有内容是：

| 来源 | 独有内容 | 处置 |
|---|---|---|
| `0f20dfac4647048db69c` | primitive-SA1 给定点下 (\epsilon^2/4) 舍入合同及 full physical domain | integrated-supplied-point-epsilon2-4 |
| `3858f37087ca3c8a80f0` | Q-only v2 Exact 输入/输出量词、11次LP所需算法接口的陈述 | integrated-exact-v2-statement |
| `47c955a8da722b2e7a1c` | Author Proof v2 的 P_gate identity、CDF-max、固定 q、失败分支和位复杂度 | integrated-author-proof-v2 |

该 typed one-outer 算法不能迁移到一般 normalized multicore、多个 outer groups、没有 distinct own homes 的 helper、隐式 exponential menu 或任意 ordinary matrix。它也不改变已有一般 UM-TARGET-v1 和 CAG 六人 SPE 目标的开放状态。

# 6. 处置与真实运行边界

三源已完整实读、比较并保全。Author Proof 明确这是 typed special-case proof，不是一般 UM 算法或 novelty claim。当前 checkout 没有 canonical one-outer 生产实现，本批没有重跑 LP、CDF backend、11 次二分或完整 scheduler；既有 finite audits 只承担其声明范围。父 Boss 在 checkpoint/pushed 后逐源 done；本批未执行 clean done、commit 或 push。
