---
id: customer-attraction/adm-discovery-menu-contract-and-two-exact-saved-points
kind: program
type_tag: 程序
title: ADM探针的完整终局菜单与两保存点精确证书
status: source-contract-preserved; two-finite-primal-dual-certificates-verified-locally
summary: 完整读取ADM浮点发现器与两保存记录，保真实尾菜单、筛选与四次旧检查的范围；新有理重构确认两有限值47/24和53/17，均未反驳ADM。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round3_general/menu/probe_adm.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round3_general/menu/adm_discovery.json
source_ids: [2b863e40a0d9b68eadad, d624353ed020110fb523]
review_status: whole-source-reading-and-informed-exact-reconstruction; no-original-main-run
---

# 模型、菜单与发现器真正优化的量

有限单位客户、有限非空共同标签目录、m名单位提供者；客户在终局覆盖者间均分。标签允许空覆盖、同覆盖和重复选择，完整纯策略允许区分全部有序历史，任意平局保留。原输入用重数表示互异单位客户，没有改变提供者权重。

固定一条可由完整纯SPE支持的实际有序路径z=(a₁,…,a_m)，其终局收益u_i、覆盖福利W。h_i为第i位以前的实际前缀。对每个位置i和强制动作A，取从h_i+A开始的**全部**完整尾SPE终局，而非原策略的一个指定孩子；仅保留强制者最终收益不超过u_i的那些终局。并为D。A=a_i时亦保全部合格替代尾，实际动作列不缩为原叶。

对完整m槽终局计数c和额外静态查询T，定义

\[
k_T(c)=\sum_{x\in T}\frac1{1+n_x(c)},\qquad
V(D)=\max_{p\in\Delta(\mathcal T)}\min_{c\in D}\sum_Tp_Tk_T(c).
\]

发现器求此有限max-min问题，报告gap=V(D)−W/m。正gap才是这个实际路径、完整ADM并集的付款违规；文件名中的“failure/counterexample”是输入的历史名称，不代表本ADM命题失败。D只按终局计数去重合法，因为收益和k均只依计数；这不要求策略本身为计数策略。

# 原程序逐段合同和有限筛选

`ins`按客户型重数、额外查询的1+n分母计算所有k_T；`adm`依实际有序前缀逐位、逐强制动作调用`ExactSPESolver.outcomes`，用强制者真实终局收益作弱cap，合并D。其SciPy变量是主题概率及自由标量γ，约束Kp≥γ、p≥0、Σp=1，目标最大化γ。浮点优化用于发现，原代码自身没有有理原始/对偶接受步骤。

`check`先只筛选`max_T k_T(z)>W/m+1e-8`的根SPE终局，再按此差降序取前`limit`项；每项打乱可支持的有序路径，只取前`max(1,limit//2)`条。返回每输入已查路径中**最大**gap，不是全实例搜索最小值。若gap>1e-7便早停。

`main`默认seed=7351、limit=8、random=0；先扫描示例目录且只保人数/标签数均不超过8的输入。只有示例扫描未早停，才进入要求的random次随机输入：4/5/6标签、3/4/5/6人、指定离散客户重数分布。随机次数、输入类和阈值都不是一般数学假设。报告按gap降序最多留12条；`checked`累加实际被检查的路径数量，不等于留下的记录数。

本保存JSON的`checked=4`、`records=2`。本批没有取得这四次逐调用日志，也没有将原示例库、原`model/exact`实现全量加载或执行，故不补造遗漏两次的输入身份，不称原main复现。程序按原相对位置`parents[6]`定位仓库及导入`customer_attraction.model/exact`；原件搬进证据目录后不可直接当自足入口执行。

# 新的有限有理证书

新[标准库核验器](../../tools/evidence/adm-saved-points-20261102/verify_adm_saved_points.py)只读完整保存JSON，先核其冻结SHA；不导入原发现器、模型、求解器或SciPy。它对两个**指定有限输入**按定义重构全部可信终局计数和D，再对显示的有理p、对偶菜单分布逐条作Fraction比较。它知道原报告，是知情重构，不是盲审或新颖性认证。

递推的正确性：设E(c)为有前缀计数c时全部可由完整尾SPE实现的终局计数。终局时E(c)={c}。对每个合法A令E_A=E(c+e_A)，以及

\[
\ell_A=\min_{y\in E_A}u_A(y),\qquad M=\max_A\ell_A.
\]

选A、选定y∈E_A能成为当前节点完整SPE，当且仅当u_A(y)≥M。必要性由每条偏离至少面对其最小可信收益；充分性保选中孩子y，其他动作各独立贴一个达到\ell的完整SPE。所以下层递推并集恰为E(c)，无严格平局筛除。有相同计数的不同有序历史面对同构续局，但旁枝可独立贴不同策略；按计数缓存不合并它们的策略选择。对保存路径还逐前缀检查同一终局支持条件，才构造D。

| 保存输入 | m | 根可实现计数数 | D计数数 | 有理查询p | V(D) | W/m | gap |
|---|---:|---:|---:|---|---:|---:|---:|
| coverage_opportunity_failure | 3 | 8 | 10 | (1/2,1/4,1/4,0,0) | 47/24 | 8/3 | −17/24 |
| residual_counterexample | 2 | 8 | 10 | (0,5/17,5/17,7/34,7/34) | 53/17 | 9/2 | −47/34 |

原始下界由对所有十行Kp≥V且至少一行取等给出。以下菜单计数c及概率λ给精确上界：对所有五查询，Σ_cλ_ck_T(c)≤V。任意p的最小菜单值不超过此λ加权平均，再不超过V；因此两侧确实夹出最优值，不只是验证一个查询的收益。

| 输入 | 对偶菜单计数，按主题0…4 | 对应λ | 五查询对偶上界向量 |
|---|---|---|---|
| 第一例 | (1,0,0,1,1)；(1,0,1,0,1)；(1,1,0,0,1)；(1,1,0,1,0) | (1/6,11/28,17/84,5/21) | (47/24,47/24,47/24,47/24,107/56) |
| 第二例 | (0,0,0,1,1)；(0,0,1,0,1)；(0,1,0,1,0) | (1/17,8/17,8/17) | (50/17,53/17,53/17,53/17,53/17) |

全部菜单计数、10×5精确核、原始十行值和证书均在[精确报告](../../tools/evidence/adm-saved-points-20261102/exact_saved_points.json)。有理p从浮点记录提出后由精确双边不等式认证；float接近性只核旧字段一致，不承担最优性。

# 真实运行、复用与接续

原发现器0次运行、0浮点LP、0原四次检查重演。新checker首版提取对偶时忽略零概率查询也可能对应紧不等式，第一例提取失败；诊断再次调用两记录后，修正为同时枚举这些可能紧约束，最终完整入口成功。首版失败与诊断没有改原输入或冒记PASS，见[证据说明](../../tools/evidence/adm-saved-points-20261102/README.md)。新双边有理证书不依赖这段搜索历史。

与[共享前缀cap回收](../引理/共享实际前缀的cap回收与最坏福利提升--引理.md)的D定义兼容，因实际行动替代尾没有删除。与[自洽池根稿接口](../资源/删当前自洽池与完整端点cap回收的根稿接口--资源.md)中的m−1竞争负载不同，本程序查询保完整m槽再加静态一槽。

两有限负gap只说明这两个指定D支付；不证明一般ADM、不否定任意别的路径违规，也不构成六人half结果。若接续一般攻击，应保存完整输入、实际路径及完整菜单，并提供同样可核的原始/对偶或正gap证据；本批不继续重复这两已精确解决的有限菜单。
