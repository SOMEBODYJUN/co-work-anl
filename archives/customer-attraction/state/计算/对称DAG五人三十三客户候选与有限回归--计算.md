---
id: customer-attraction/symmetric-dag-q32-certificate-and-regression
kind: computation
type_tag: 计算
title: 对称DAG五人三十三客户候选与有限回归
status: exact-finite-certificate; regression-reconciled; no-universal-result
truth_status: fixed-input-pure-SPE-certificate-and-finite-equivalence; Q-CAG-HALF-open
summary: 冻结的 q=(3,2,0,0,0,0,0) 五人七主题 JSON 给出一个 33 客户完整有序历史纯 SPE，W=20、OPT=33、固定策略锥精确值 33/20；warm-start 三人三主题烟测给出 W=3、OPT=5、5/3；symmetric_dag.py 的 30 个有限回归与 canonical all-SPE BI 在 8 个可达目标和 22 个不可达目标上逐项一致。三者都不证明普适上界或六人 Q-CAG-HALF。
source_refs:
  - clean:66545ba853e2589f6466
  - clean:0e38ce50d15b625a555a
  - clean:3823d89e058e155758ea
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/credible_search/symmetric_dag.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/credible_search/sym_m5p7_q32_Jout.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/credible_search/symmetric_dag_regression.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/credible_search/warm_start_smoke.json
---

# 对称DAG五人三十三客户候选与有限回归

本页是三个已认领冻结源的独立对象。三份文件由 `work.py clean show` 对应的冻结行核对，随后从 `/workspace/scratch/3b26e30034a3/tmp/claimed/` 读取；字节数和 SHA-256 与 `cleanup/inventory.jsonl` 完全相同。两个冻结提交 `68fad804ec5946cb296f77dc5b336308a66abf12`（legacy-cleanup）和 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`（main）中的同路径是同一字节版本，不能算两次独立数学证据。

| clean ID | 原始路径（可直接查看冻结版本） | 字节数 | SHA-256 |
| --- | --- | ---: | --- |
| `66545ba853e2589f6466` | [sym_m5p7_q32_Jout.json](https://github.com/SOMEBODYJUN/co-work-anl/blob/68fad804ec5946cb296f77dc5b336308a66abf12/research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/credible_search/sym_m5p7_q32_Jout.json) | 383448 | `d69e034266cf14279ce3de3ed9ebfadd9bb0ae79df9d35a89ad5fddbe5b32fe9` |
| `0e38ce50d15b625a555a` | [symmetric_dag_regression.json](https://github.com/SOMEBODYJUN/co-work-anl/blob/68fad804ec5946cb296f77dc5b336308a66abf12/research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/credible_search/symmetric_dag_regression.json) | 7020 | `dac211bcb43f5a50cab1ed5469bad3703fd5d8dadf5383794ddc58528c836f43` |
| `3823d89e058e155758ea` | [warm_start_smoke.json](https://github.com/SOMEBODYJUN/co-work-anl/blob/68fad804ec5946cb296f77dc5b336308a66abf12/research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/credible_search/warm_start_smoke.json) | 4057 | `1aec58db1e52d7b73b0c1d9bf8df002b874dc85875f65d4c0ea6f9b96f938c6d` |

程序定义保存在 [symmetric_dag.py](https://github.com/SOMEBODYJUN/co-work-anl/blob/68fad804ec5946cb296f77dc5b336308a66abf12/research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/credible_search/symmetric_dag.py)。其完整历史证书审计、依赖边界和早先二十个来源的比较已经整理在 [R275 可信搜索对称DAG与共同次模投影增量](../审查/R275可信搜索对称DAG与共同次模投影增量--审查.md) 以及 [R275 证据包](../../tools/evidence/R275-credible-search-20261031/README.md)。本页补上那两页没有逐字段展开的三份 JSON：q32 候选的具体克隆、对偶支持和策略规模；回归中每种 `kind` 的输入及逐案结果；warm-start 的完整三人实例和对称重优化值。

## 模型、量词和对称商

有 p 个共同主题、m 个依次行动的单位权提供者。客户类型是非空 B⊆[p]，重数 r_B∈ℤ_{≥0}。若终局计数为 c=(c₀,…,cₚ₋₁)，覆盖 B 的客户在 B 中的 c(B)=Σ_{b∈B}c_b 个最终提供者之间均分，因此 c_a>0 时提供者 a 的真实终局收益为

\[
u_a(c)=\sum_{B\ni a}\frac{r_B}{c(B)}.
\]

社会福利是被至少一个终局主题覆盖的客户总数

\[
W(c)=\sum_{B:\,c(B)>0}r_B,
\]

而 OPT 是在 m 个单位提供者的静态计数 c 上最大化 W(c) 的值。完整有序历史纯 SPE 给每一个历史 h∈[p]^{<m} 指定动作，并且指定所有离轨历史的续局；验证必须检查每个历史的真实单步偏离。JSON 的 `exact_candidate` 只在抽取到的完整策略锥上给出精确对偶，不把该锥外的输入或策略一并最优化。

`SymmetricDAG(p,d,m)` 只假设客户输入对后 p−d 个标签置换不变。它**不**强迫纯策略等变。实现中：

* 前缀计数 k 的尾部按 `ck(k)` 排序；
* 终局对 (k,c) 按尾部的 (k_b,c_b) **同时**排序，形成 outcome pair；
* 标记行动的三元组 (k,c,a) 按 (k_b,c_b,1[b=a]) 同时排序，形成实现/惩罚变量；
* 展开时每一个实际有序孩子都使用相应轨道代表，因此没有把轨道大小错误地乘进二元变量，也没有把不同动作选择器当成同一个计数策略。

MILP 使用 y_{k,c} 表示可保留的 outcome pair，z_{k,c,a} 表示在该节点实现 (c) 的动作，x_{k,c,a} 表示对应偏离的惩罚续局，t_k 表示节点阈值。根目标 q 的正福利被归一化到 (W(q)=1)；所有根 SPE 的传播收益都不超过 1，所以该归一化下的 big-M 约束有效。(W(q)=0) 的目标被明确排除，不能把除零状态当作“不可达的数学反例”。浮点 MILP 只用于产生候选，候选随后恢复整数客户重数、展开全部历史并以定义级 `verify_certificate` 检查。

## q32：五人、七主题、33 客户的完整候选

### 浮点搜索层

`sym_m5p7_q32_Jout.json` 的范围是 `symmetric input class; unrestricted ordered-history pure SPE witnesses`，且 `universal_claim_proved=false`。参数为

\[
p=7, d=2, m=5, q=(3,2,0,0,0,0,0), J=(2,3,4,5,6).
\]

后五个主题只是输入商的交换标签；策略仍允许依赖完整有序历史。MILP 的维数和运行事实是：

| 字段 | 值 |
| --- | ---: |
| customer orbits | 23 |
| prefix orbits | 96 |
| variables | 2520 |
| binary variables | 2446 |
| constraints/rows | 4475 |
| HiGHS status | 1，30.021936586 秒到时限 |
| floating value | 1.200000000000045 |
| `floating_bound_not_a_certificate` | `true` |

`status=1` 的到时限 incumbent 不是最优性证明；其浮点目标也不等于后续固定策略锥重优化的精确值。

### 整数恢复后的输入和福利

精确候选的非零 bit-mask 克隆为

\[
4↦3, 8↦3, 16↦3, 32↦3, 63↦5, 64↦1, 67↦15.
\]

主题编号从 0 开始，故对应客户目录是

| 客户支持 B | 重数 r_B |
| --- | ---: |
| ({2}) | 3 |
| ({3}) | 3 |
| ({4}) | 3 |
| ({5}) | 3 |
| ({0,1,2,3,4,5}) | 5 |
| ({6}) | 1 |
| ({0,1,6}) | 15 |

总客户数为 4×3+5+1+15=33。源 JSON 的 `instance` 与上表逐项相同。给定终局 q=(3,2,0,0,0,0,0)，覆盖 {0,1,2,3,4,5} 上的前五类客户，福利为

\[
W(q)=3+3+3+3+5+15=20.
\]

主题 6 的单例客户没有被覆盖。静态最优福利由同一恢复实例的精确求解器计算为 OPT=33，因此

\[
\frac{\operatorname{OPT}}{W(q)}=\frac{33}{20}=1.65<2.
\]

这不是六人目标的反例；它只是一个五人、七主题的有限低福利完整 SPE。

### 完整策略和定义级证书

`exact_candidate.strategy.actions` 有 2801 个动作条目，正好是完整五步有序树的节点数

\[
1+7+7^2+7^3+7^4=2801.
\]

根动作是主题 0；第一层历史 (0,1) 的动作是 0，历史 (2,3,4,5,6) 的动作是 1。其余 2779 个历史动作以及离轨续局均原样保存在上述 JSON；本页不以短表替代这份完整策略。终局计数为 `[3,2,0,0,0,0,0]`。定义级检查报告：

* `certified=true`，`canonical_definition_verified=true`；
* `nodes=2801`，`deviation_checks=16806`，即对完整策略树逐节点检查所有真实单步偏离；
* `welfare=20`，`optimal_welfare=33`；
* `exact_dual_bound="33/20"`、`dual_optimal=true`；
* 13 个非零对偶行（索引从程序的零起始行号计）为
  [
  (60,17/90),(62,17/90),(164,59/45),(165,194/45),(166,3/2),
  (167,15/8),(200,1),(230,1),(237,7),(246,3),
  (1046,1),(1052,104/45),(1055,203/360).
  ]

对偶值证明的是该**抽取策略的固定整数客户锥**上比较组合 J=(2,3,4,5,6) 的精确值 33/20，并不是所有五人输入、所有策略或所有六人输入的全局上界。JSON 没有 `exact_symmetric_candidate` 字段；即使克隆表显示后五个单例重数相同，也不能把此字段缺失的候选宣称为程序重新求出的对称重优化结果。

## warm-start smoke：三人三主题的已知 5/3 点

`warm_start_smoke.json` 同样声明 `universal_claim_proved=false`，但它是一个可快速闭合的三人控制例：

\[
p=3, d=1, m=3, q=(3,0,0), J=(0,1,2).
\]

客户目录为 3×{0}、1×{1}、1×{2}，共 5 个单位客户。所有 13 个完整历史节点的动作都选主题 0，终局福利 W=3，静态最优福利 OPT=5，故精确值为 5/3。exact candidate 和 exact symmetric candidate 都是同一策略、同一克隆和同一实例；对称重优化保留的非零轨道值为

\[
((0,1),1/3),\qquad ((1,0),1),
\]

其余轨道值为零。两个精确候选均 `certified=true`、`canonical_definition_verified=true`、`exact_dual_bound=5/3`、`dual_optimal=true`；对偶支持分别为 `[0,1]` 行系数 1（未加对称投影）以及 `((0,1),1/3),((1,0),1)`（对称重优化）。完整历史为 1+3+3²=13 个节点，`deviation_checks=26`。

MILP 仅用了 112 个变量、100 个二元变量、186 行、13 个前缀轨道和 5 个客户轨道；HiGHS status 7 (`kOptimal`) 在 0.003731667 秒结束。`warm_start.provided=true`、seed objective 为 5/3。该 seed 是代码注释所说的已知 all-big lower-bound family 的数值起点，不增加新的数学下界，也不能把 smoke 例推广到任意输入。

## symmetric_dag_regression：30 个固定输入的全 SPE BI 对照

回归 JSON 的 scope 是 `finite fixed-input regression against canonical all-SPE BI`。程序对 (p,d,m)=(3,1,3) 和 (4,2,3) 建立对称 DAG；对每个 `kind` 生成固定整数克隆，遍历所有只在前 d 个主题上有根计数的 q，并令 `verify_fixed` 用 `ExactSPESolver(inst).outcomes()` 判断 canonical 可达性。若 DAG 找到证书，代码立即用 `verify_certificate(...).assert_valid()` 检查；然后断言 `(found is not None) == canonical`。因此这里的“回归通过”是有限输入上的表示一致性，不是全域定理。

`kind` 的输入生成也在源程序中固定，不能把数字标签当成未定义黑箱。令 `rkeys` 按 ((I,j)) 排序，其中 I⊆[d]，j 是后块中被客户支持的主题数。对轨道索引 i，`kind=0,1,2` 使用

\[
r_{I,j}=1+((7i+3\,\text{kind})\bmod4).
\]

特殊三类为：

* `kind=3`：只有 (I=[d])、(j=p-d) 的全主题客户轨道取 1，其余取 0；
* `kind=4`：(r_{(1,0)}=m)，(r_{(0,1)}=1)，其余为 0；
* `kind=5`：(r_{(1,0)}=m-1)，(r_{(0,1)}=1)，(r_{(2,0)}=1)（若该轨道存在），其余为 0。

所有 q 都是 q₀ 在前 d 个坐标上的组成，后坐标为零。逐类结果如下；“历史数”是 JSON 的 `verified_full_histories` 总和，m=3,p=3 时每个完整树有 13 节点，m=3,p=4 时有 21 节点。

| p,d,m | kind | q 的个数 | canonical 可达 | MILP status 分布 | 已核验完整历史 |
| --- | ---: | ---: | ---: | --- | ---: |
| 3,1,3 | 0 | 1 | 0 | `2`×1 | 0 |
| 3,1,3 | 1 | 1 | 0 | `2`×1 | 0 |
| 3,1,3 | 2 | 1 | 0 | `2`×1 | 0 |
| 3,1,3 | 3 | 1 | 1 | `0`×1 | 13 |
| 3,1,3 | 4 | 1 | 1 | `0`×1 | 13 |
| 3,1,3 | 5 | 1 | 0 | `2`×1 | 0 |
| 4,2,3 | 0 | 4 | 0 | `2`×4 | 0 |
| 4,2,3 | 1 | 4 | 0 | `2`×4 | 0 |
| 4,2,3 | 2 | 4 | 0 | `2`×4 | 0 |
| 4,2,3 | 3 | 4 | 4 | `0`×4 | 84 |
| 4,2,3 | 4 | 4 | 1 | `excluded_by_zero_W_normalization`×1，`2`×2，`0`×1 | 21 |
| 4,2,3 | 5 | 4 | 1 | `0`×1，`2`×3 | 21 |

在 p=4,d=2 的四个根中，`kind=4` 只有 q=(3,0,0,0) 可达；q=(0,3,0,0) 的 (W(q)=0) 被显式标记为 `excluded_by_zero_W_normalization`，另两个根为 status 2。`kind=5` 只有 q=(2,1,0,0) 可达。总计 30 个 cases，其中 8 个可达、22 个不可达、152 个完整历史节点被精确策略展开。可达和不可达均由 canonical all-SPE BI 同步确认；status 2 只是在这组有限固定输入中没有 DAG 证书，不能解释为普适“所有输入不可达”。

## 与既有对象的关系和本页独有内容

已有 [R275 可信搜索对称DAG与共同次模投影增量](../审查/R275可信搜索对称DAG与共同次模投影增量--审查.md) 已保留这一研究批次的高层结论：对称输入并不等于等变策略；浮点 MILP、整数恢复和完整历史检查必须分层；已有 9/5、1791/1000、897/500 及 warm-start 的有限点都小于 2；30 项回归为 8/22；它们不推出六人 Q-CAG-HALF。 [对称输入终局见证商的作者版本与有限候选](../资源/对称输入终局见证商的作者版本与有限候选--资源.md) 则解释同时轨道商、S_s 客户重数参数化、(W=0) 分支和当时缺失八个 JSON 的历史状态。[完整有序策略的定义级均分证书审计](../算法/完整有序策略的定义级均分证书审计--算法.md) 给出逐节点真实收益和均分实现的通用检查接口，[终局见证DAG的完整历史可实现性](../等价/终局见证DAG的完整历史可实现性--等价.md) 给出 y,z,x,t 见证的有限历史等价。

本页相对这些对象新增并唯一保留：

1. q32 原始 383448 B 的客户克隆到客户支持的逐项映射、W=20, OPT=33、13 个非零对偶支持和 2801/16806 的完整证书规模；
2. 回归源代码中 `kind=0,…,5` 的实际克隆生成式，以及 30 案逐类 status、可达根和 152 历史节点的完整表；
3. warm-start 三人五客户实例的 exact candidate 与 exact symmetric candidate 同策略事实、对称轨道值和 seed/HiGHS 元数据。

这三项不能用已有审查页的一句“有限证书”替代，因为它们决定了哪些客户目录、哪些量词和哪些失败机制确实被检查。

## 证据边界和接续用途

q32 是一个真实完整有序历史纯 SPE，其 ratio 33/20<2，所以它既不是 half 反例，也不是 OPT/W≤2 的证明。它只说明在该固定输入和该抽取策略锥内有精确证书；浮点 MILP 到时限说明联合候选搜索的计算瓶颈仍存在。warm-start 只把已知 5/3 点作为数值起始解；其 5 客户、3 人规模与主问题的六人量词不同。回归只覆盖 (p,d,m)=(3,1,3),(4,2,3) 的 30 个固定实例，不能外推到 p=7,m=5 的全部对称输入，更不能外推到六人。

后续若要把 q32 或同族点用于主问题，必须保留完整 JSON 策略、恢复客户目录、对所有离轨历史重算真实均分收益，并单独证明候选输入的静态 OPT；不能把 33/20 的固定锥对偶值写成全局最优或一般福利常数。当前六人 Q-CAG-HALF 仍 OPEN，现有五人完整证书和此处的五人候选不能按人数拼接成六人结论。
