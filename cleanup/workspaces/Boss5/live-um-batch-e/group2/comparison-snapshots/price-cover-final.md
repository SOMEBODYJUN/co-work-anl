# 任意汇点逐件资格的价格覆盖与共同占位舍入

本文只给唯一 home 私有分组下的正面算法。它取消固定汇点数、同组共同资格和接收时间下包络；没有从一般矩阵生成该分组或承诺，`UM-TARGET-v1` 仍 OPEN。加权拟阵单侧舍入是旧工具的自足重构，不能据此认证新颖性。

## 1. 精确身份与适用范围

### UM-UPPER-COLUMN-BUDGET-BASE-ROUNDING-v1

给显式二分图 G=(B,H;E)，存在覆盖 B 的匹配。令 M 为 H 上的横截拟阵。对每个 h 给有限的 occupied 模式集合 Q_h，可以为空；另要求非空模式类的 homes 集合 H_Q={h:Q_h非空} 仍可在 G 中匹配全部 B。模式集合 Q 是 M 先限制到 H_Q 后的平行扩张地集：I 独立当且仅当每个 home 至多选一个模式，且这些不同 homes 在 G 中可匹配。其基大小为 |B|。注意：直接复制 G 的 home 邻接而不保 home 容量，会允许同 home 多选，不是这个拟阵。

给非负有理矩阵 A=(a_zq)、有理预算 c_z、常数预算量 b>=0，满足每列 sum_z a_zq<=b；再给一个可核查的有理分数基 x，Ax<=c。存在确定性算法，按这些显式数据总位长的多项式时间输出实际基 I 和覆盖 B 的宏匹配，使每行

`sum_(q in I) a_zq <= c_z+b`。

资源行数、模式数和 |B| 均可增长。只给上界，不承诺下界、保持任意成本或严格最优负载。所有模式均为显式实际对象。b=0、秩零、空资源集均包括。对一般菜单接口，加性系数 1 是 supremum 意义下锐的，见 §3。

### UM-ARBITRARY-SINK-PRIVATE-GROUP-PRICE-COVER-v1

显式给定不交机器集 H、Z，宏任务 B 和不交私有组 J_h，构成全部任务。每个私有任务 j 在其唯一 home h 有有限时间 a_j>=0，可另在任意逐件子集 E_j⊆Z 运行；无其它有限端。宏任务只在 H 运行。所有数据遵循一般有理输入模型，每件任务至少一个有限端。

对 T>0，给有理参数 rho>=1、delta>=0、tau∈[1/2,1)、eta∈(0,1]，令

`b0=rho(1-tau+delta)`，要求 `b0<=1`。

合同假设：W_h=sum_(j in J_h) a_j<=T，a_j<=delta T；每个合法 sink 边 p_zj<=rho a_j；每条有限宏边 p_hb>T/2。宏边可以大于 T，算法先剪去它们。不存在私有任务的强制 sink 端；home 始终有限。Z、H、资格和有理分母均不固定。

有一个确定性算法，运行时间 poly(L,1/eta)，其中 L 包括 P、分组及所有有理参数的总位长，返回 FAIL 或全部真实任务的分配。每个成功输出逐机满足

`L_h <= (1+tau)T`，`L_z <= [1+eta+b0]T`。

若 OPT(P)<=T，则必成功；因此本合同域内 FAIL 蕴含 OPT(P)>T。成功不是精确 T 可行性证书。T=0 单独逐件检查零边，空任务输出空分配。若固定 rho、delta、eta 且 rho delta+eta<1，选择

`tau=[rho(1+delta)+eta]/(1+rho)`

便有 tau∈[1/2,1)、b0=tau-eta<1，实际系数为

`alpha=2-[1-rho delta-eta]/(1+rho)<2`。

### UM-ARBITRARY-SINK-PRIVATE-GROUP-PROMISE-APPROX-v1

另一个身份不输入 T。静态对象与 sink 上界 p_zj<=rho a_j 不变；固定 rho>=1、delta>=0、eta∈(0,1] 且 rho delta+eta<1，tau 按上式选择。承诺仅在真实 OPT 处成立：W_h<=OPT，a_j<=delta OPT，所有有限宏边>OPT/2。则有确定性总位多项式算法输出完整实际分配，Cmax<=alpha OPT。不能免费验证这一含 OPT 的承诺，也没有从一般 P 提取它的算法。可变精度时复杂度为 poly(L,1/eta)，不声称对 eta 的二进制编码长度为多项式。

## 2. 单侧列预算舍入的自足证明

平行扩张基多面体有显式匹配扩展：u_h=sum_(q in Q_h)x_q，0<=u_h<=1；f_bh>=0，sum_h f_bh=1，sum_b f_bh=u_h。只列 G 中合法边。它的 x 投影是基多面体：先分解 u 为 home 基，再按 x_q/u_h 条件选该 home 模式。后者仅证明凸包身份，算法不需枚举分解。固定某模式为 1 不固定该 home 的宏身份，f 保持共同可调，最终重新匹配。

算法保留未删资源预算，固定 x=0 的删元及 x=1 的收缩。每轮以逐 x 坐标精确 lex LP 取得 **x 投影** 的顶点；不能以扩展流的任意顶点代替。lex 等式只在本轮取点时使用，下一轮全部释放，只保留真正 0/1 的固定。若已整数则输出，否则删去 0、收缩 1，以下剩余坐标均严格在 (0,1)。资源行的固定贡献从预算扣除。

设剩余地集大小 n，剩余基秩 r=sum_e x_e 为整数。紧秩集合 x(S)=r_M(S) 对并、交封闭。取极大紧集链

`empty=S_0 ⊊ S_1 ⊊ ... ⊊ S_t=E`。

若另一紧集 V 切开某块 S_i\S_(i-1)，则 S_(i-1) union (V intersection S_i) 是严格居中的紧集，矛盾。故所有紧秩行在这 t 个块指示向量张成空间内，且链行独立。每块的 x 质量是正整数 r_M(S_i)-r_M(S_(i-1))，于是 t<=r。原基多面体最小面维数 d=n-t>=n-r=sum_e(1-x_e)。若当前有 k 条资源行，而 x 是交切投影顶点，则 d<=k，否则有非零双向面方向消掉全部紧资源行。因此

`sum_e(1-x_e) <= d <= k`。

每条保留行的未来上增包络为 e_z=sum_e a_ze(1-x_e)。由非负性和列预算，sum_z e_z<=b sum_e(1-x_e)<=bk。因此有一条保留行 e_z<=b，可删除它。未来任意 0/1 补全相对删行时的当前负载，上增至多 e_z；删行当时满足该预算，故最终不超过原 c_z+b。永久的 0/1 固定不会重新打开已删元，且不会额外再收费。重复至多 |Q| 次固定和 |Z| 次删行；资源行耗尽后基顶点整数。

LP 扩展、临时 lex 优化和最终整数匹配均为多项式规模。所有后续 LP 是原有理矩阵删行并加 0/1 等式；新坐标值受这些矩阵行列式的统一多项式位长界约束，不因 lex 次数反复膨胀。总 LP 次数多项式。固定支持的流具有整数 0/1 可行解，恢复实际宏匹配。此为数学算法；下面的顶点枚举审计不冒充生产 LP 后端。

## 3. 舍入误差的范围与文献扣除

秩一、k 个模式、k 个资源，列 q 为 b 倍第 q 个单位向量，x_q=1/k，c_z=b/k。任一整数基在某行超出预算 b(1-1/k)。所以统一加性 c b（c<1）不可能对这个显式菜单域成立。它不证明实际任务允许更多模式时仍需这一误差，也不是近似困难性。

本引理是标准 upper-only degree-bounded matroid 计数的直接有理加权推论。Király–Lau–Singh 的 Theorem 2 给 0/1 上界版本；Bérczi–Berger–Mnich–Vincze, arXiv:1911.09890v2，Theorem 2（印2/PDF3）已给整数 multiplicities 的上界误差 Delta-1，Delta 为最大列总重。对 A,c 清共同分母即可推出本 +b 界；§2仅自足重构所需证明。Bérczi–Liu–Reis–Tarnawski, arXiv:2608.13983v1 §5 Theorem 10 是相关的双侧加权 discrepancy 结果。本文不以此声称新的舍入原理。新接口须按 §4–7 的实际结构和生成算法评估，全球新颖性/独立论文价值未认证。

## 4. 原矩阵怎样产生小出口实际模式

empty home 不接宏，全部私有任务在 home，负载 W_h<=T，出口向量恒零。occupied home 只要求其私有留量<=tau T，再加真实宏时间<=T，给最终 (1+tau)T。

occupied 的精确覆盖需求为 D_h=(W_h-tau T)_+。只允许有 sink 端的任务参加覆盖。若其 a_j 总和不足 D_h，就禁止该 home 被占用；若 D_h=0，模式为无出口。取任一覆盖集合 X 并删冗余，至 inclusion-minimal。D_h>0 时，每个被选元素 a_j>0，且删除任一元素后覆盖不足，所以

`D_h <= sum_(j in X) a_j < D_h+delta T`。

为每件 X 选择一个实际合法 sink。该模式的实际总出口量满足

`sum_z w_z <= rho sum_(j in X)a_j <= b0 T`。

从一份真实 T 调度出发，每个 home 至多一宏。该 occupied 组的实际 home 留量<T/2<=tau T；其出口集合可删到上述极小覆盖。删除出口就是把任务搬回自己的 home，留量仍<=tau T，各 sink 负载逐坐标不增。empty 组直接全部回 home。因此真实 T 调度提供一个共同宏匹配和低总出口模式见证，但算法从不需要给定该调度。

## 5. 一次价格查询的实际覆盖与宏匹配

给任意非负有理价格 pi_z，sum_z pi_z=1。对可出口任务令 c_j=min_(z in E_j) pi_z p_zj，按固定编号选实现的真实 sink；无出口端的任务不能参加 cover。

对每个 home 的 D_h，用乘性 (1+epsilon) 最小覆盖 FPTAS（epsilon=eta/4），保持真实覆盖 a 不舍入，输出实际集合；然后删冗余，成本不增，且满足 §4 的列预算。保零成本构造如下：先取零成本物品，若覆盖成功即得零成本解；否则减去这些覆盖量。对每个正成本 C 猜测它是最优解中最大成本，只保 c_j<=C，设 s=epsilon C/q，整数成本 floor(c_j/s)，按整数成本保存最大真实覆盖量及不复用任务的回溯。正确猜测的真实成本<=c*+epsilon C<=(1+epsilon)c*。状态总数 O(q^2/epsilon)，所有正成本猜测给 O(q^4/epsilon) 次更新。很小的正价格、大分母和零覆盖量不扩大状态数；最后删除冗余也删除零 a 项。该原语复用已有 shared_sink_joint_macro_assignment.md §3 的证明，不建立免费精确背包 oracle。

给每个可占用 home 上述近似真实出口成本；全部兼容宏边使用同一 home 成本。最小成本覆盖宏任务的二分匹配（可用 dummy 补完）共同选择占位 homes。不存在匹配则 FAIL。未占用组全回 home。记录所得全局实际方案的 sink 向量 ell，并直接计算价格成本 pi·ell。若它>(1+epsilon)T，返回 FAIL。

若 OPT<=T，§4 的真实见证对这些价格成本<=T。各组 FPTAS 误差乘在同一共同价格总成本上，最小成本宏匹配不会更差，故 pi·ell<=(1+epsilon)T；所有 FAIL 均不发生。每轮每个 sink 的负载还至多 |H|b0 T。精确有理 min-cost flow/匹配为位多项式；宏身份始终共同选择，不预先冻结。

## 6. 有理乘法权重产生多项式显式支撑

设 K=|Z|>=1，R=max(1,|H|b0)<=max(1,|H|)，gamma=eta/4，取

`N=ceil(16 R K/eta^2)`。

初始 w_z=1。第 t 轮 pi_z=w_z/sum w，调用 §5；若没有 FAIL，按实际输出更新

`w_z <- w_z [1+gamma ell_z/(RT)]`。

令 g_z=ell_z/(RT)∈[0,1]。由 log(1+u)<=u 和 log(1+u)>=u-u^2>=gamma(1-gamma)g（u=gamma g），得到每个资源的均值负载

`avg ell_z/T <= [1+epsilon+R log K/(gamma N)]/(1-gamma)`

`<= [1+eta/2]/[1-eta/4] <= 1+eta`。

其中 log K<=K，最后一步的交叉相乘余量为 eta(1-eta)/4>=0。不需要算对数，N 的选取完全有理。K=1 也成立。w 和价格始终正，但实际成本可因零处理时间为零，已由 §5 处理。

保留这 N 份真实全局方案，每次占用 home 时记录其实际模式；empty 不建变量。按频率 1/N 平均，并平均宏匹配流，得到显式模式平行扩张基的分数点 x；每个资源 Ax<=(1+eta)T，每列总量<=b0 T。所有模式和任务回溯均实际存在，最多 N|H| 个模式，未枚举指数 Pareto 表。

调用 §2，逐 sink 最终负载<=(1+eta+b0)T。对 selected homes 恢复宏匹配和一个模式，未选 homes 全部私有任务回 home。每个原任务恰执行一次，所有端点合法，全部机器同时满足 §1。没有保持逐件边际、逐机计数或任何给定初始槽。

N=poly(L,1/eta)，因为 b0<=1，故即使 rho 的数值很大也不按 rho 数值循环。实际负载是原输入子集和，统一分母位长多项式；w 的每个乘子含这些子集和及输入参数，N 次乘积位长 O(N poly(L,log N))，不是指数位数。每轮价格、成本、cover DP、匹配和实际方案位长均多项式。所有回溯任务编码 O(N|J|log|M|)，下一步 LP 数据同样多项式。算法的所有循环次数和位长均已控制。

K=0 时禁止 D_h>0 的 occupied home，再找宏匹配，成功后所有任务在 H；真实 T 调度必给这样的匹配。无宏任务直接全部私有任务回 home，不运行 MW。空组、空任务、零 a、零 sink 时间、无出口端、单端任务、大分母均覆盖。T=0 在任何除法前做完整零边检查；OPT=0 也可在正 T 时提前返回零调度。

## 7. 未知 OPT 的 one-sided 搜索

对 §1 的未知 OPT promise，使用同一阈值程序，但 **不检查** 宏边是否>当前 T/2。只剪掉宏时间>T；检查 W_h<=T、a_j<=delta T；随后照 §4–6 运行。任何成功输出仍满足 alpha T，因为只用到实际宏时间<=T。宏任务数大于 |H| 或其它不存在匹配的分支可返回 FAIL。

在 promise 内，对任何 T>=OPT，原最优调度每 home 至多一宏，私有留量<OPT/2<=tau T；原私有总量和尺寸承诺也保证两项检查通过。因此 §4–6 的完整性仍成立，故每次 FAIL 都有 T<OPT。这里没有偷偷假设在较大 T 上仍满足宏下界；原最优调度本身提供所需的单宏见证。

先逐件检查零边，若全部有零端，直接输出零调度。否则 OPT>0。令 D 为输入全部有限处理时间分母的乘积，bit(D)为输入位长的线性上界；任意实际 makespan 在 1/D 网格。任选合法调度的值 C，令整数 U=DC>=D OPT。运行阈值 U/D 必成功，保存其调度。设 lo=0、hi=U，反复在 mid=floor((lo+hi)/2) 查询；成功更新 hi 并保存输出，FAIL 更新 lo。接受集合不必单调；不变式是 lo<D OPT 且 hi 保存成功。终止 hi=lo+1<=D OPT，返回调度负载<=alpha hi/D<=alpha OPT。O(log(U+1)) 次查询，每个阈值位长多项式。delta=0 用直接乘法比较，不除以 delta。

## 8. 与现有接口的关系和未解决义务

固定 sink 数占位方法使用高维 DP 和 heavy 枚举；这里由真实价格查询生成有限支撑，sink 数进入多项式次数而不进入指数。weighted/distorted_group_joint_slot_rounding 要求同组共同接收资格或上下包络；这里允许任意 E_j 和只有上界 p_zj<=rho a_j。异质宏 arbitrary-tiny 接口要求 |B|=|H|；这里宏数量任意但保留唯一 home 与 W_h<=T。三者范围不能互相静默改写。

主目标缺口仍是从任意 P 产生共同角色、home 分组、可接收边及统一 rho、delta 余量。只看单件 tiny 不控制整组出口；选择最快端为 home 也不保 W_h<=T。知道真实最优调度后能删边得到有利结构，不等于能位多项式生成它。本算法不把该生成器当 oracle，不把结构 promise 改成 UM-TARGET-v1 的全部输入域。

Truth：上述一般证明与实际读后审分开登记。Value/Mechanism：原矩阵→覆盖价格查询→poly实际菜单→同一宏占位基→全 sink 实际整数输出。Novelty：旧 cover、匹配、MW 和单侧拟阵工具的结构性组合，未认证全球新颖或独立成文价值。Ambition：取消两个真实接口限制，仍非一般调度突破。

## 9. 审查、实现和有限证据

首轮冻结全文审查发现并修复了空模式类可能降低拟阵秩的陈述漏洞；首引理现明确要求 H_Q 仍覆盖全部 B。该要求由主算法成功积累的共同匹配见证自动满足，不改变结构算法域。实际冻结审查见 [price_cover_joint_rounding_review.md](../../reviews/unrelated_machines/price_cover_joint_rounding_review.md)。数学算法具有完整位复杂度规格；没有集成生产级有理 LP 求解后端。小规模顶点枚举、子集/匹配枚举、原矩阵 oracle 和 MW 回放仅为有限审计，不能冒充多项式实现或一般证明。


精确复现入口：

- [列预算舍入审计](../../../tests/audits/unrelated_machines/upper_column_budget_base_audit.py)与[有限顶点核心](../../../tests/audits/unrelated_machines/occupation_vertex_audit_core.py)：独立枚举基、全部紧秩子集及实际宏排列匹配，含缺 home 容量的负控制；[冻结结果](../../../evidence/runs/unrelated_machines/upper_column_budget_base_audit.json)。
- [独立价格覆盖与 MW 审计](../../../tests/audits/unrelated_machines/arbitrary_sink_price_cover_mw_audit.py)：不调用已有覆盖实现，比较原矩阵全部实际分配、子集最优覆盖、完整/前缀 MW；[完整输入](../../../examples/unrelated_machines/arbitrary_sink_price_cover_mw_cases.json)与[冻结结果](../../../evidence/runs/unrelated_machines/arbitrary_sink_price_cover_mw_audit.json)。

重跑输出到 scratch，新建结果；默认不改写冻结证据。以上有限审计分别覆盖舍入后端和原输入菜单生成，不等于完整生产级 LP 软件已实现。
