---
id: "unrelated-machines/type-profile-affine-line-review"
kind: "review"
type_tag: "审查"
title: "类型压缩与仿射并行线双源审查"
status: "integrated-with-scope-boundaries"
truth_status: "scoped-general-proofs; finite evidence and literature reread; no-general-UM-hardness"
review_level: "full-source-read-and-cross-archive-comparison"
scope: "single-threshold type-profile compression/rank matching and arbitrary weighted affine-line half-retention"
source_refs:
  - "source:af0562c14e7407309d73:research/current/unrelated_machines/type_profile_compression_and_matching_rank_bridge.md"
  - "source:cc3fc3849a2e96e053fb:research/current/unrelated_machines/weighted_affine_parallel_relation_reweighting_obstruction.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/type_profile_compression_and_rank_bridge_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/weighted_affine_parallel_relation_reweighting_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:tests/audits/unrelated_machines/santa_block_type_profiles.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:tests/audits/unrelated_machines/type_matching_rank_bridge.py"
legacy_ids:
  - "UM-SC-BLOCK-TYPE-PROFILE-RECONSTRUCTION-v1"
  - "UM-NORMALIZED-TYPE-MATCHING-RANK-VALUE-IDENTITY-v1"
  - "UM-WEIGHTED-AFFINE-LINE-PARALLEL-RELATIONS-HALF-ESCAPE-v1"
---

# 1. 实读范围与处置

本批完整读取 `clean show` 的两个当前 canonical 正文、inventory 指纹、所链接的既有审查、分块/类型匹配审计和仿射线相关审查。当前源 `af0562c14e7407309d73` 的路径为 `research/current/unrelated_machines/type_profile_compression_and_matching_rank_bridge.md`，SHA-256 为 `4ebdbc1d9e4fd41e9d4736b839ea50361e2777b2f2e4aab187e2d36fd604a7dd`；`cc3fc3849a2e96e053fb` 的路径为 `research/current/unrelated_machines/weighted_affine_parallel_relation_reweighting_obstruction.md`。两者均来自冻结提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`。本页不把外部论文摘要当本源证明：文献只作为已读背景，分块与 rank 论证的数学边界按 canonical 正文逐式核对。

两个来源都在普通 unrelated-machines 中保留全部原 jobs 并做显式位复杂度核算，但对象不同。类型源把单阈值 Santa Claus 的离散 value-type profile 压缩为多项式数量的计数菜单，再给每个 profile 一个真实 UM 编译；仿射线源在有限域并行仿射关系上允许任意 state-dependent 权，证明仍能确定性取得一半质量，但明确拒绝把该容易判的关系族当作一般低值困难性源。两源均处置为 `integrated`，并保留其“结构域内正面结论/反例范围”而不制造一般 UM 结论。

# 2. 单阈值类型 profile：分块压缩与真实 rank 编译

## 2.1 Exact A 的定义域、量词与压缩结论

稳定身份为 `UM-SC-BLOCK-TYPE-PROFILE-RECONSTRUCTION-v1`。输入显式二进制有理估值矩阵 `v`，玩家数 `m>=1`、资源数 `n>=0`，固定正有理 `epsilon`。资源可闲置，玩家值是所取资源价值和，目标是最大化最小玩家值。算法输出截断/量化矩阵 `v'`、公共正类型调色板和每玩家的整数 count-profile 集 `C_i`。`epsilon` 固定时，类型数 `t=O_epsilon(log(n+1))`，profile 数 `|C_i| <= binom(H+t,t)=(n+1)^{O_epsilon(1)}`；不声称对 `bit(epsilon)` 统一多项式。

对每个原资源子集 A，只要 `val_i(A)>=1`，就存在 A' subseteq A，按类型完整匹配一个 `c in C_i`，且 `v'_i(A') >= gamma=1/(1+epsilon)`。分别应用于一份不交的 SC YES 分配仍保持不交，因此舍下值可以由显式 profiles 表示；任意 `v'` 的实际分配在原 v 下不降。算法不判定 OPT>=1、不读取未知最优解，也不免费选择一个共同 profile。

构造取 `delta=epsilon/(4(1+epsilon))`、`tau=delta/n`，先 cap 到 1，删 tiny 值，再按 `(1+delta)^{-k}` 向下舍入。块长
\[
b_k=max\{1,\lfloor\delta/(t a_k)\rfloor\},\qquad H=\lceil4t/\delta\rceil
\]
保证每个完整块价值至少 `delta/(2t)`。从任意 cap 总值在 `[1,2)` 的集合按 type 每类截取 `b_k floor(d_k/b_k)` 件，逐类损失总计至多 `delta`，块数小于 H；枚举受总块预算、type 可用数、Exact 价值过滤的 profile，而不是枚举无界计数直积。几何舍入和 tiny 删除合并给 `v'(A') >= 1-3delta > 1/(1+epsilon)`，位长和前缀 DFS 均按固定 epsilon 的输入位长多项式。

## 2.2 原文 cutoff 的实质边界

正文实读并保留一个明确纠错：原文 Appendix B 印 20–21 的 tiny cutoff `1/((1+eta)n)` 与“删除只损失因子”的字面推断有反例（一位玩家，101 项资源，100 件 `9/1000` 和一件 `1/10`）。将 cutoff 改为 `eta/((1+eta)n)`，或 canonical 构造采用 `tau=delta/n`，可支付加性损失；向下舍入后低于 cutoff 的正值也要求 grid 保留到最小 `a_K<=tau`。该反例只修正特定步骤，不推出原主定理整体错误；原文 PDF/HTML 和后续结论被分开引用。

## 2.3 Exact B：归一化 type matching 的真实值恒等式

稳定身份为 `UM-NORMALIZED-TYPE-MATCHING-RANK-VALUE-IDENTITY-v1`。输入非空玩家/资源集、显式非负有理类型矩阵和每玩家非空 indexed profile 菜单 `C_i`。profile 的 type counts 受资源数、可用同值资源数约束，归一化值
\[
f_{ic}(B)=\frac1{W(c)}\sum_v v\min\{c(v),|\{j\in B:v'_{ij}=v\}|\},quad F_i(B)=\max_c f_{ic}(B).
\]
定义 `V=max_{B_i disjoint} min_i F_i(B_i)`。每个固定 profile 的 `f_ic` 是 weighted partition-matroid rank；max over profiles 的 `F_i` 不必次模。

普通 UM 编译为：每个 `(i,c)` 一台 private `Q_ic`，每个实际资源一台 `R_j`，每玩家一枚 selector 只在自己 profiles 的 private 机上耗时 1；每个 positive type 复制 `c(v)` 枚 token job，private 端时间 `v/W(c)`，在该 type 可用的所有 `R_j` 上时间 1。未选 profile 的所有 token 仍留 private，不能从矩阵中删除 job。若给定不交 B_i，选一个达到 F_i(B_i) 的 profile，外送匹配的 tokens，其他 tokens 留 private，峰值恰 `2-min_i F_i(B_i)`；反向任何峰 C<2 的 schedule 中每台资源机至多接一个 unit token，selector 所在 profile 的实际外送资源给出不交 B_i 和 `F_i(B_i)>=2-C`。因此
\[
OPT_{UM}=2-V.
\]
这是真实全部 jobs 的两向证明，适用于 V=0、OPT=2、重复 indexed profiles 和未选菜单；复杂度按显式菜单长度而不是隐式数值复制收费。

## 2.4 非次模和接续限制

一位玩家的四个资源值 `1/4,1/2,1/2,3/4` 与所有总值至少 1 的 profiles 给出 `F(A)=F(B)=3/5`、`F(A cup B)=1`、`F(A cap B)=1/4` 的违反次模反例。故不能直接把 `max_profile` 当作一个次模 oracle；固定 profile 的 matroid rank 不足以处理 max。若要求把每个 profile 展开为同一资源宇宙上的显式 additive norm-one 菜单，仓库已有规模障碍，本源不重复建立新的 XOS claim。

Exact A 与 Exact B 可以在 SC YES/NO 承诺下组合：SC YES 时 `V=1`，且 `V<=OPT_SC/gamma`；这只传递另行给定的源 gap，不提供任意小 `zeta` 的困难性归约。空 `C_i` 的 YES 前提不成立，可单独输出固定 OPT=2 的退化 UM 分支；不能把空菜单送入 Exact B。BLMRS 外部文献的复杂度/近似结论只作背景，本文没有重构其全部算法、matroid 变体或一般 UM 反向等价。

# 3. 仿射并行线：任意状态权仍有一半可保留

## 3.1 定义域和真实 UM 编译

稳定身份为 `UM-WEIGHTED-AFFINE-LINE-PARALLEL-RELATIONS-HALF-ESCAPE-v1`。取素数 `R>=2`、`k>=2`、域 `F_R`，有 R 个 constraints `j`，每个允许表
\[
A_j=\{a\in F_R^k:\sum_i a_i=j\}.
\]
变量 tag 资源宇宙为 `U=disjoint_union_i ({x_i} times F_R^2)`；state `a` 含每个 tag 上 R 点的仿射线，允许权 `w_(j,a,u)>=0`，每个 state 总和为 1，可任意依赖 j、a、tag、cell，允许零权。

普通 UM 编译为每 state 一台 private 机、每资源一点一台 resource 机；每组一个 selector 在本组 private 机上耗时 1；每个 incidence job 只有自己的 private 端（耗时 w）或对应 resource 端（耗时 1）。不合并 tags、不删除未选 state 或零 private job，故是完整原模型。

结论量词是：对所有这些完整显式权表，存在每组一个 affine state `a(j)=cj+d`（`sum c=1`、`sum d=0`），以及全局不交实际 partial subsets，各组质量至少 1/2；可确定性总位多项式输出这些集合和全部原 jobs 的实际 `Cmax<=3/2` 调度。它不输入 source witness、OPT 或分数 oracle；源关系 value 恰为 `1/R`，是易判族，不能冒称 NP-hard image 或一般低值 NO soundness。

## 3.2 条件平均和唯一例外回填

先在 `C={c:sum c_i=1}` 与 `D_0={d:sum d_i=0}` 上均匀取 c,d。固定一个完整 state `a` 后，映射 `(c,d) -> (c,cj+d)` 是双射到 `C x A_j`，所以条件于该组 state，c 仍均匀；每个坐标 `c_i` 的概率为 `1/R`。固定 c,d 后，同一 tag 的已选 lines 平行或只在一个点 `P_i` 相交。删去所有共点 H 后，各组原质量损失 `L_j` 的条件期望至多 `1/R`，全组总期望至多 1，于是存在候选 `(c,d)` 总损失<=1。

至多一个组的损失可超过 `1/2`。若无例外，所有删点后的 subsets 两两不交且各质量>=1/2；若有唯一例外 h，则给 h 回填完整 line set，其它组仍删 H，交点只由 h 占用，不破坏全局不交。枚举 `R^(2k-2)` 个 `(c,d)` 候选并精确比较，候选总数是显式输入状态表 `R^k` 的多项式，因此给定全权表时是确定性总位多项式算法。

每个选中 state 的保留 incidence jobs 导出到相应 resources，其余 jobs 留 private；资源机至多接一 unit，selected private load 为 `2 - mass <=3/2`，未选 private load 为 1。所有原 jobs 恰一次，含零私有时间和未选 state，故完整 schedule 峰至多 3/2；selector 给 OPT>=1。

## 3.3 否定范围、反例和有限证据

singleton 关系 `A'_j={(j,0,...,0)}` 可以把总权放在一个共同点，最多一组获得该点，V=0，实际 OPT=2；k=1 本身也落在该反例。因此任意关系、k=1 或仅仅“给每 incidence 重新赋权”并不能自动得到半保留/低值 soundness。主仿射族的 source value=1/R 来自显式可判关系；存在另一个避开此族的 hard image、改变关系或资源接口仍未排除。

审查范围明确没有软件/有限实验/外部同行评审认证；算法是有限域候选枚举和精确有理累加的数学规格。其复杂度是按完整显式 state 表长度多项式，不是 succinct `poly(k,log R)`。原 source 还强调给定 full-set packing 时归一化权自动保留 YES，但这不替代 NO 的全 partial decoder。

# 4. 双源比较、关系图与开放义务

两源共同保留“完整原 jobs、显式位复杂度、逐对象实际构造”的严谨性；但 type source 是菜单/profile 压缩和 rank 编译，affine source 是仿射关系中任意权的半保留。它们不能互换 soundness：type source 只在 SC YES/给定 profiles 的结构域传递质量，affine source 的低值是容易判关系族，均没有一般 NP-hardness。

与既有 Santa/normalized menu 审查的关系：本批新增可复用的分块 profile 数量和 cutoff 修复，以及 `OPT=2-V` 的全部任务双向编译；保留 max-profile 非次模反例和 explicit menu size 障碍。与 uniform affine-line、tuple-group 和 line-set packing 审查的关系：本批新增任意 state-dependent 权仍可半保留的条件平均，保留 singleton 关系 V=0/OPT=2 作为不可外推边界；不重复声称任意关系、低值 source 或困难性。

第三阶段可记录两条条件边：

- `固定 epsilon 的 type compression -> 多项式 profile menu -> normalized rank matching -> 真实 UM OPT=2-V`；边上标注 `max profile 非次模，全球 disjoint choice 未解决`。
- `并行仿射关系 + 任意完整 state weights -> 条件 affine average -> half-retention / Cmax<=3/2`；边上标注 `关系 value=1/R、易判族，不能作一般 soundness`。

未闭义务是：给生成 profile 菜单的全局不交选择提供算法或可用 soundness；在真实 YES/NO 源中建立低值并行仿射关系而不落入 singleton 反例；处理多外层、全资源容量和一般 normalized menu 的复杂度；以及把这些结构域结论与 UM-TARGET-v1 的六人 SPE 模型保持独立。两源均没有一般 UM 近似比、NP-hardness 或主目标结论。

逐源处置：

- `af0562c14e7407309d73`：`integrated`。Exact A 分块压缩、cutoff 纠错、Exact B 的 rank 恒等式、非次模反例、空菜单分支和位复杂度边界写入第 2、4 节。
- `cc3fc3849a2e96e053fb`：`integrated`。仿射线完整权域、条件平均、唯一例外回填、确定性枚举、singleton 反例和 source value 限制写入第 3、4 节。

两源均为全文件实读，相关审查/程序/证据已比较，独有内容去向和不混量词的理由已明确。
