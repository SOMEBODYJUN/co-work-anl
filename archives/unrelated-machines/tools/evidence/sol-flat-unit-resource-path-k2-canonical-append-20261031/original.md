# K2 resource-path canonical §12：实际全文读后复核

审查者：`/root/sol_nsw_independent_attack`。这是已知 Exact 和 Author Proof 后的 informed canonical review，不是新的 blind review。仅审 parent 本次释放的 §12；不为未读的旧 §1–11 或其他 native C2 文本签字。

## 1. 精确输入、阅读顺序与冻结记录

本次 canonical 文件：

`/workspace/scratch/038d9dcc4cac/sol_literal_budget_normalized_menu_k2_canonical_draft_v1.md`

- 实核 SHA-256：`1617f7913a5399ad062ba36506c54cfe3166b269d41f91426bfe432cd91cf10b`。
- 实核 49,782 bytes、536 `splitlines()`、mode `0644`。
- 本次真正显示并逐行读取的新增正文为 **340–439、440–536**，即 §12 header 与 §12.1–12.7 全文。父任务所说 198 行 append 还包括其前的空行 339；我不把该数字误报为 198 行数学正文。
- 只对全文 bytes 做了 hash/长度核验，没有语义阅读或重签旧 1–338 行 prefix。也没有打开 §12 的 review 链接或其他未释放文件。

真实先后为：先只读 20 行 Exact，独立重构并冻结；parent 实际读完该独立记录后释放 179 行 Author Proof；我完整读后另冻记录；本次才读 canonical §12。两个旧记录均未修改，现已重新核 SHA：

| 文件 | 实核 SHA-256 | 实核范围/状态 |
|---|---|---|
| `sol_flat_unit_resource_path_c2_exact.md` | `c2c590f3e916d992e6d591e25ccad0f1c8818586ed8a2b4d0a8fd5a2ab1be0d9` | 3,008 bytes / 20 行；先前实际全文读 |
| `sol_flat_unit_resource_path_c2_independent_exact_first.md` | `6e24cdb2b7dcdcfa98f482e371604728b7994c0cc4da70fa601474fd6c3e8639` | 15,504 bytes / 150 行 / `0444`；仍为原冻结记录 |
| `sol_flat_unit_resource_path_c2_proof.md` | `09d9e2b1d3373d2e17f01fb764fab339bd869da7acfbf9479e8eb90225fdde7e` | 14,827 bytes / 179 行；释放后实际 1–90、91–179 全文读 |
| `sol_flat_unit_resource_path_c2_author_read_after.md` | `6ec5c4ad908f137402034d723baaebc0eda12ab42fb76828496ea13a4a96e091` | 13,942 bytes / 107 行 / `0444`；仍为原冻结记录 |

我的既有背景包括原 ordinary job 的 activation/exports 区别、primitive-SA1、资源 empty 的二阶闭包、全局 M1 与 M2 的区别、给定点投影与存在可行点的区别。那些背景不能替代本次 §12 的具体次数核算。也没有把弱合同或真实分配分布的 PSD 自动当成这里的 K2。

## 2. 对象和合同逐项一致

340–349 行给出新的独立 ID `UM-FLAT-UNIT-RESOURCE-PATH-K2-PRESERVATION-v1`，其域、量词、结论、依赖和限制与已审 Exact/Proof 同对象：非空有限 normalized-flat groups/states，全部二进制有理系数，完整 all-jobs 矩阵，逐个有理 `1 ≤ T < 2`，双向构造已给出的完整有限有理证书。

351–383 行的 K2 保留每个 job 的每个 finite endpoint。Boolean 恒等式乘到 degree 4，job one-hot 恒等式乘到 degree 4；全局 M2 对全部 degree≤2 多项式平方 PSD。每台机器的实际 CONFIG list 同时匹配 first 和 same-machine pair，而不是只有 raw-load 线性约束。物理机 localizer 明确是 `L((T−load_i)q²) ≥ 0`，`q` 可以用全部有限端变量且仅要求 affine。它不是未经证明替换后的 activation localizer。

文中没有对所有全局 quartic literals 额外作非负假设，没有共同实际 schedule law，也没有将 CONFIG 权重作为新的全局随机变量。只给定有限有理证书的转换；没有声称任意实 SDP feasible 就存在有理证书。

D_+ 正邻居只按 **distinct original groups** 列一次。同组多个 indexed states 的所有正 incidence 共用该组 own port。零 incidence 仍是独立原 job，保留 private 0 和 unit resource 端：有 own port 就路由该处，否则固定 fallback port；`d=0` 保留旧资源。它没有把 zero eligibility 算作 positive degree，也没有合并不同旧资源 tags。

## 3. 次数、null 与正向构造

387–411 行的 null 引理确由 M2 的 Cauchy–Schwarz 给出：若 degree≤2 的 `r` 有 `L(r²)=0`，则可乘任何 degree≤2 多项式。在 Boolean reductions 后，`xy`、`x(1−y)` 的平方等于自身，允许由 pair expectation 零得到 degree-four radical。

同 job 不同端的冗余 one-hot pair 约束可推出：one-hot 乘某端给交叉期望和零；各交叉项是 Boolean 二次项的平方期望，非负；逐项零后用 null 引理。不存在把仅有一阶 one-hot 当作所有高阶恒等式的跳步。

Unit CONFIG 在 `T<2` 迫同机 distinct jobs 的 pair 零，故 `K²−K` 可乘任意 degree≤2 multiplier 消去。`0≤LK≤1` 分别由 Boolean PSD 和 `L((1−K)²)≥0`。式 (12.6) 的差值恰为 `(K²−K)q²`，总次数至多 4；右侧第二项是 degree≤2 多项式的平方。因而可重建 unit resource 对所有全局 affine `q` 的物理 load localizer。

415–440 行的 `O_i` 包含 routed 到该 port 的 **全部原资源端指标**，所以 inactive exports 和零 incidence 没被漏出 `K=ΣO_i`。固定 slack port `f` 后 `H_i=O_i+1[i=f](1−K)`。其 Boolean defects、跨 `H` products 和 `O_i(1−K)` 都由旧 unit-clique radical 和 Boolean identities 线性组合得到，没有免费增加新随机 hole。

新叶 `L_j=Σ_{i>j}H_i`、`R_j=1−L_j` 与各 incidence head 逐项相等，private 端取补。所有新增 finite 变量都是旧全局变量的 affine forms。四次以内的完整 monomial 表用仿射 pullback 定义，所有 Boolean/job 恒等式及 M2 因此确实继承，原 joint moments≤4 原样保留。这里正向选取 canonical 的新叶值并不要求任意反向证书也具这种等式。

442–456 行的所有机器均有证书：旧 private lists 照抄；叶 root 的 selector 与其 private incidence 是互补，load 恒 1；非固定 ports load 恒 1；固定 port load `K`。Leaf weights 与 port singleton weights 非负，可由 affine Boolean PSD 及 unit-clique upper bound 核得，空配置补足至 1。旧 original moment entry 未改，原 root list 的 first/pair 一致性因此未改。任意新增 affine `q` pullback 后仍是旧全局 affine，故旧 roots/fixed port 的 localizer 真能继承。

## 4. 任意 raw 反向证书：degree 4 已付清

460–481 行只用新叶两 unit private roots 的 CONFIG 得 `X(1−F)` null，**未假设 inactive incidence 不 export**。同 port 的 `EF` 为 unit-resource null。

- (12.11)：先用 `X(1−F)` 乘 `E`，再用 `EF` 乘 `X`，得到 `L(EX)=0`。`EX` Boolean 后成为二次 null。
- (12.12)：依次用 `X(1−F)` 乘 `Y`、`Y(1−G)` 乘 `XF`、`FG` 乘 `XY`。所有乘子次数≤2，最高乘积次数为 4；从 `L(XY)=0` 再取得 `XY` null。

483–498 行的 `H_i=L_{i−1}−L_i` 不是先验非负随机事件。以 `L_0=1,L_d=0`，其 defect 经 Boolean reduction 为 `2 L_i(1−L_{i−1})`，该项已由同 port 相邻 leaf state selectors 的 null 消去。边界 defect 恒零。

对 distinct `i,j`，`L((H_iH_j)²)=L(H_iH_j)` 的第一次 reduction 以 `H_j²` 乘 `H_i` 的 degree-2 defect，第二次以 `H_i` 乘 `H_j` 的 defect；均在 degree 4 内。左侧由 M2 非负，故每个 pair expectation 非负。`ΣH_i=1` 与各 Boolean defect 给所有跨 pair 期望总和零，于是逐项零，且 quadratic `H_iH_j` 是 null。没有借用任意 quartic literal 非负性。

500–513 行对旧 job head `E` 的支撑性也只在有限次数下推出：`L(EH_i)=LE`；`q=E(1−H_i)` 有期望零，且 Boolean reduction 给 `L(q²−q)=L(E(H_i²−H_i))=0`，所以 `q` null。不同 ports 的旧 `E,F` 用 `q_E` 乘 `F`、`q_F` 乘 `EH_i`、`H_iH_j` 乘 `EF`，得到 (12.15)。每个 multiplier 都≤2、总次数≤4。同 port pair 由 unit CONFIG，`d=1` 直接用唯一 port，`d=0` 原证书未动。

因此反向没有假设叶只输出一个 head，也没有把 state-selector differences 解释为免费全局 events。原零 incidence、同组多 states 共 port、inactive original exports 均被这一推导覆盖。

## 5. 限制、所有旧 moments、数量和位长

517–521 行的 principal restriction 保留每个原 job 的全部有限端变量，仅把资源端物理名改回旧资源。全部旧 degree≤4 joint moments、Boolean/one-hot identities、M2 和 private-root CONFIG lists 因此确实保留。旧 unit resource list 用各旧 head first moment 给 singleton 和 empty 重建；不必保留事先指定的 list 分解。旧 roots 的 global-affine localizers 由 restriction 继承，旧 unit resources 由 (12.6) 重建。

525–534 行的计数核对通过：令 `L_+=Σ max(d_u−1,0)`，新增每叶 2 roots、1 selector、2 incidence jobs，finite endpoints 为 2+2+2=6。故全矩阵机器数 `S+2L_++m_+`、jobs 数 `n+I+3L_+`、finite endpoints 数 `S+2I+6L_+`，正邻居数和 `L_+` 均≤`I_+`。原零 jobs 被 `I` 正确计入；unused resources 被 `m_+` 的 `d=0` 项正确保留。

Moment table degree 固定为 4，所以仿射替换展开只读多项式多个已给条目，系数为长度多项式有界的整数。有理加减、求和分母总位长至多为所有输入分母位长的多项式；没有按 `1/probability` 展开。新 singleton/empty lists 大小多项式。转换不需求任何未知 CONFIG/SDP oracle，也不作 general exact SDP feasibility/finder 断言。

`1≤T<2` 的两端用途与已审 Exact 相同：`T<2` 给 unit pair exclusion；`T≥1` 给 singleton 合法及 (12.6) 第一系数非负。`T<1` 时保留的 original unit selector 在所有 finite endpoints 都不属于任何合法 CONFIG，其 first marginals 为零又 one-hot 总和 1，故双方都不可行。没有 `T≥2` 保持结论。

## 6. 来源角色与结论

§12.347 明确不主张 path 思想新颖性，这与本次已实际读到的 Bateni–Charikar–Guruswami STOC’09 Theorem 3 一致。真实 primary 阅读范围和仅限 topology 的来源结论，另冻在 `sol_bcg2009_degree_path_primary_target_read.md`；该来源不被充作 degree-four certificate preservation 的现成证明。

**审查结论：本次实际读取的 §12/12.1–12.7 与已审 Exact/Author Proof 同对象、同量词、同次数合同，未发现站得住的 fatal。PASS 仅限上述 raw K2 有限有理证书双向转换。** 不追认旧 prefix 的任何结论，不把 native canonical C2、primitive-SA1、M1 或 bare load-only C2 当作同一系统，不升级旧 gap、software 或来源结论。

这是数学规格及数学变换证明；本 ID 的软件实现、checker、SDP finder、数值实验均为 **none**。没有为形式而写镜像测试。全球新颖性没有认证；一般 UM 的 `UM-TARGET-v1` 仍 OPEN。
