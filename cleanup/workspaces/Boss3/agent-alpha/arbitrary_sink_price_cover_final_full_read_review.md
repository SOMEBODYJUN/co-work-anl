# 价格覆盖与共同占位舍入：最终正文实际完整读后审

审查者：boss9 内部 global_relaxation。最终核读日期：2026-10-19。只写 scratch；未修改 repo，未作 Git 写入，未作对外通信。

## 1. 被审字节与实际阅读顺序

被审文件为：

`/workspace/scratch/014c8decb8a6/co-work-anl-boss9/research/current/unrelated_machines/arbitrary_sink_private_group_price_cover_rounding.md`

本报告绑定的 SHA256 为：

`6c23677ab25afb0db3f0c6ced6b1fb16bb8993a541c875d6b3ee2dfaf3d6e580`

本次先实际调用 sha256sum 核对该值，随后用 cat 完整实际读取当前正文全部 §1–9（143 行），并逐节重新攻击。不是把旧哈希报告改号。此前实际完整读过最初 `07e65d4798eece8159ba9c4cbad6631bf3b2c221013eba97c48e1c3cdd3c7d1f` 版本，提出空模式类可能降秩的陈述漏洞；还实际完整读过 `9fa1bb886e50b9393873366116fe6e58c120ad5e1617eac2d36c3849477c849f` 中间版本。最终稿的满秩前提与 eta 编码长度措辞均已在当前实际字节中核对。

此前 statement-first 独立重构另存 `home_arbitrary_sink_statement_first.md`，其冻结 SHA 为 `a2ec7eb380edfe460532150efe2f4548fd76cf189bc0b31d3a88dccd5cec0d91`。本报告明确是读取作者最终正文之后的实际攻击，不追称盲审。

## 2. 结论与三个 ID

**结论：在当前明确合同域内，三个 ID 的数学证明均通过本次内部读后攻击；无仍 standing 的 fatal 或实质证明反例。** 没有认证全球新颖性、外部同行审查或一般 UM-TARGET-v1 进展超过正文所列范围；也没有实现生产级有理 LP 后端。

| ID | 实际核对结论 |
|---|---|
| UM-UPPER-COLUMN-BUDGET-BASE-ROUNDING-v1 | 当前明确要求非空模式类 homes 仍覆盖全部宏任务，修复了原陈述的秩漏洞。单个平行扩张、投影顶点、单侧非负残差计数与加性 +b 均成立。 |
| UM-ARBITRARY-SINK-PRIVATE-GROUP-PRICE-COVER-v1 | 实际 cover 定价、共同宏匹配、有理 MW 支撑与 +b0 T 舍入相接，输出 home≤(1+tau)T、sink≤(1+eta+b0)T。sound FAIL 仅在所列结构域内主张，正确。 |
| UM-ARBITRARY-SINK-PRIVATE-GROUP-PROMISE-APPROX-v1 | §7 专门修改阈值程序，不再检查当前 T 的宏下界；OPT 处的原最优调度对每个 T≥OPT 提供单宏见证。整数 one-sided 搜索无需接受集合单调，最终 alpha OPT 界成立。 |

## 3. §1–3：满秩修复、平行扩张与 +b

最初版本仅假设 G 本身覆盖 B，而允许 Q_h 为空，却直接称模式拟阵的秩为 |B|。普通平行扩张前删掉所有空模式类会降低秩。最终稿已显式加入 H_Q 仍匹配全部 B，并把模式地集定义为 M 限制到 H_Q 后的平行扩张，故该反例不再适用。主算法一旦记录一份成功宏匹配，其所用 homes 都具有实际记录模式，所以调用首引理时此新前提自动满足，不缩小第二 ID 的输入域。

最终扩展明确包含 u_h=Σ_q x_q 及 0≤u_h≤1。这排除了“直接复制右侧 home 邻接”误把同 home 两个模式同时匹配的错误表示。固定模式 x_q=1 只固定 home occupation；f_bh 保持自由，宏任务身份最后共同重新匹配，未提前冻结某一条匹配边。

对 +b 逐项重新检查：删去0并收缩1后，剩余所有 x_e∈(0,1)，秩 r=x(E) 为整数。紧秩集合并交封闭；最大紧链的每个非空块有正整数 x 质量，所以块数 t≤r。所有紧秩方程由这些块指标张成，基多面体的最小面维数 d=n−t≥n−r=Σ_e(1−x_e)。若交切点为 x 投影的顶点，保留资源行数 k≥d。因此

`Σ_z Σ_e a_ze(1−x_e) ≤ b Σ_e(1−x_e) ≤ bk`。

至少一保留行的未来上增 residual 不超过 b。该行删除时其已固定贡献加当前分数贡献仍≤原预算；任意未来0/1补全相对该点的上增至多此 residual。因此最终只付一次 +b。其他零元永久删除，固定支持不会重新开启，后续收缩不引入额外收费。空资源集时投影本来是整数基多面体；b=0、秩0也都覆盖。

秩一各列落独有资源的族给必要增量 b(1−1/k)，所以系数1在 supremum 意义下锐。该例只校准一般显式菜单接口，未被不当扩大为实际任务域的最优近似常数。

§3 的外部定理归属不承重本次数学判断，因为 §2 自足证明成立。本审未重新核验所引各篇原文的定理编号，不把本报告当作这些文献出处的独立认证。

## 4. §4–5：真实覆盖、定价与任务身份

覆盖需求 D_h=(W_h−tau T)_+ 精确按真实 a_j 定义；没有 home 权舍入误差。D_h>0 的 inclusion-minimal cover 中每个 a_j>0，且删去任意一件后总权<D_h，所以总权<D_h+delta T≤(1−tau+delta)T。任意逐件合法 sink 去向满足总出口≤rho 倍 home 总权，从而一列的 l1≤b0 T。D_h=0 使用空出口模式，不能额外任意选择昂贵出口。

真实 T 调度的每个 occupied home 至多一 macro；其私有留量<T/2≤tau T。只保留达到 D_h 的最小出口子集，其他任务回各自唯一 home，home 留量仍≤tau T，逐 sink 负载只减。empty home 全部私有任务回 home 时 W_h≤T。这是一个共同匹配与模式见证，不是把不同 home 的不相容最优值拼起来。

FPTAS 的成本舍入检查通过：把零成本项单列，覆盖不足则扣除它们的真实覆盖量；枚举最优解最大正成本 C，s=epsilon C/q，d_j=floor(c_j/s)≤q/epsilon。逐件层 DP 按整数成本记录最大真实覆盖量，覆盖权本身不舍入，且回溯不重复任务。正确猜测下可行解真实成本≤c*+epsilon C≤(1+epsilon)c*；再删除冗余只减成本。零需求/零成本/零 a 的分支不会出现 C=0 或 q=0 的除法。

每 home 的定价成本只依该 home，不依 macro 身份，所以可以用一次最小成本完整宏匹配共同选 occupied homes。相对真实 T 共同见证，各 home 误差都乘在同一价格总成本上；不发生按 home 累加额外 eta T。若价格成本>(1+epsilon)T 才 FAIL，原 OPT≤T 时不可能触发。可用 min-cost flow 直接实现；若采用文中可选 dummy 补完，dummy 边须计零成本，不能把 occupied home 成本也收在 dummy 上。

最终每个 home 最多选一个模式；不同 J_h 不交。模式中每私有任务只去一个记录 sink，未出口的留 home；未选 home 的全部私有任务留 home。宏任务由最终匹配各安排一次。因此所有原任务恰一次，且全部端点合法。

## 5. §6：按实际参数重推 1+eta MW

已按最终正文参数重新推算，而非复用早期1+2eta规格。设 epsilon=gamma=eta/4，R=max(1,|H|b0)，K=|Z|≥1，N=ceil(16RK/eta²)。每个实际方案逐 sink 的 ell_z≤|H|b0 T≤RT，因此 g_z=ell_z/(RT)∈[0,1]。

总权上界为

`log W_(N+1) ≤ log K + gamma N(1+epsilon)/R`。

任意单坐标权的下界为

`log w_(N+1,z) ≥ gamma(1−gamma) Σ_t g_(t,z)`，

使用 log(1+gamma g)≥gamma g−gamma²g²≥gamma(1−gamma)g。故

`avg ell_z/T ≤ [1+epsilon+R log K/(gamma N)]/(1−gamma)`。

由 N 的实际值及 log K≤K，误差项≤eta/4；于是上界≤(1+eta/2)/(1−eta/4)≤1+eta。最后一步余量是 eta(1−eta)/4≥0，eta=1 也包括。K=1 不需非零对数；K=0 已在除法前分支处理。

每轮保留的是一份真实全局宏匹配与完整私有方案；按1/N平均同时平均 occupied copies 和 macro flow，而非分别给每行一份不同 witness。故得到的 x 确在同一平行扩张基多面体，H_Q 满秩前提自动成立，且 Ax≤(1+eta)T。加性舍入再给 +b0 T，home 峰值则由宏≤T和私有留量≤tau T给出。

## 6. 总位复杂度与精度措辞

最终 eta 措辞已实际核对为“不声称对 eta 的二进制编码长度为多项式”，准确地区分 poly(L,1/eta) 与 poly(L,log(1/eta))。在固定 eta 下为通常输入位多项式；变量 eta 的反精度依赖没有隐藏。

本次核对的关键位长点：

1. b0≤1 给 R≤max(1,|H|)，故 N 不依 rho 的数值大小循环；即使 rho 编码很大，只需精确有理乘除和比较。
2. cover DP 的状态数依 q 和1/epsilon，极小价格、极大分母、极小 a_j 均不按其数值扩表。真实权是至多输入项数的子集和，位长多项式。
3. 每个 MW 乘子由原输入子集和及参数形成，N次有理乘积的分子分母位长是 O(N poly(L,log N))；价格归一化与 min-cost matching 数据仍多项式。
4. 记录的菜单数≤N|H|；每个菜单是实际任务子集与 sink 端列表。显式 A、x、macro flow 和回溯信息都为多项式大小。
5. 每轮 IR 用投影 lex LP；每次只永久保留0/1固定，临时 lex 等式下一轮释放。临时各坐标最优值来自同一当前多面体的最优面，可以由该当前扩展多面体的某个原顶点实现，因此受其统一 Cramer 位长界控制，不会因 lex 次数递归膨胀。最终匹配是普通整数二分匹配。
6. 未知 OPT 的分母乘积 D 位长≤输入分母总位长；DC 和 D OPT 是整数，U=DC的位长多项式。二分只做 O(log(U+1)) 次调用，不按D或U数值扫描。

文中“所有后续 LP 是原有理矩阵删行并加0/1等式”应按每轮主多面体理解：临时 lex 子 LP 还含当前轮较早坐标的有理最优值等式。上一段给出为何这些临时 RHS 也有统一多项式界。该措辞可将来补一句更清楚，但不构成当前数学或位复杂度 fatal。

## 7. §7：取消当前宏下界检查后的完整性与搜索

这是实际读后审的重点。修改程序只剪 p_hb>T，不再要求 p_hb>T/2。对任意成功运行，最终每选中 home 仍只接一个 macro，且该端≤T，私有留量≤tau T，所以成功输出界从来不需要当前 T 的宏下界。

对任意 T≥OPT，在 promise 内原最优调度的每个 macro端>OPT/2，故最优调度每 home 至多一 macro；其 occupied home 私有留量<OPT/2≤tau T。原宏端≤OPT≤T，未被剪掉；W_h≤OPT≤T、a_j≤delta OPT≤delta T，前置检查全过。对该最优调度的出口做精确 D_h 最小覆盖，便提供各次价格查询所需的共同见证。因此修改程序在每个 T≥OPT 都成功，所有 FAIL 确实只有 T<OPT。

这比限制 T<2p_min 更直接，并没有偷偷假设当前较大 T 上所有宏端仍>T/2。也不需要最优调度作为输入，只在完整性证明中使用它的存在。

零端检查失败后 OPT>0；在1/D整数格上 lo=0<D OPT，hi=U保存成功。任一次 FAIL 都能安全更新 lo；任一次 SUCCESS 即使发生在T<OPT，也已有实际 alpha T 输出，可更新hi。终止 hi=lo+1且D OPT整数，所以hi≤D OPT；返回的已保存实际调度≤alpha hi/D≤alpha OPT。接受集合可在OPT以下任意非单调，推导仍成立。

独立精确回归 `unknown_opt_modified_threshold_audit.py` 使用两 home、无 sink、一个宏端为3/4和2、各home私有权1/4，rho=1、delta=1/2、eta=1/4、tau=7/8。真实 OPT=1，初始上界9/4的选中宏端3/4不满足当前宏下界，却正确成功；二分又在T=3/4<OPT成功，最终返回实际峰1而仍守alpha OPT。此外穷尽3066个“OPT以上全成功、OPT以下任意接受模式”的整数搜索模式，全部维持该不变式。该有限回归不是一般证明的替代。

## 8. 零、空、无 sink 与边界

| 分支 | 实际核对 |
|---|---|
| T=0 | 在任何1/T、MW归一化前逐件查零端；全有零端则真实零调度，否则OPT>0。 |
| OPT=0、空任务 | 直接零分配；空任务匹配/分组均可空，不调用MW。 |
| 无宏 | 全部私有任务留各自home，W_h≤T；未知OPT promise下峰≤OPT。 |
| 无sink | D_h>0的home不能occupied，D_h=0模式零；真实T/最优见证保证若应成功就有完整宏匹配。 |
| a_j=0、delta=0 | 有限sink时间也0；零覆盖任务可删除。delta=0分支只做a_j≤delta T乘法比较，没有除delta。 |
| 零sink时间或零价格成本 | 独立零成本cover分支保可行与回溯；MW权始终正，不强迫实际成本正。 |
| b=0、秩0、空资源 | 单拟阵引理均成立；没有除资源数0的问题。 |
| tau=1/2、eta=1 | 给定T的严格宏下界足以单宏；MW最后不等式含eta=1。近似系数小于2另需rho delta+eta<1。 |
| 大rho、大分母、任意资格 | b0≤1控制循环；其余仅有理位长成本。不存在共同资格或下包络的隐含使用。 |

## 9. 有限证据、未覆盖项与真实修复建议

本审实际检查过 canonical `upper_column_budget_base_audit.json`：187例、283次face检查、1062个vertex candidates、380个整数选择、96次删行、27例原预算下无整数选择；报告明确是指数有限枚举，不冒称生产后端。还实际读取 `arbitrary_sink_price_cover_mw_audit.py` 的最终参数与MW记录逻辑，确为epsilon=gamma=eta/4、N=ceil(16RK/eta²)，并区分完整N与小eta严格前缀。root说明该脚本的新参数结果由其独立复跑、后续绑定；本报告不把未亲跑的新全N结果冒称本人的运行。

本人的先前 Fraction 审计已通过600个cover/枚举对照和60个小partition-base精确顶点舍入；本次额外实际运行 §7 专门回归，并把结果保存为：

`/workspace/scratch/014c8decb8a6/global_relaxation/unknown_opt_modified_threshold_audit.json`。

**仍 standing 的实质数学 objections：无。** 最初满秩域漏洞已在最终正文修复；eta措辞已修。真实范围仍仅是结构输入算法与包含OPT的结构promise算法，未关闭一般分组生成、真实统一全输入次二或困难性义务。

非阻断的实现/文字建议：定义 §5 的 q 为该次cover物品数；可选dummy补完须用零dummy成本；如进一步展开位复杂度，可加入 §6 上述临时lex最优面/Cramer一句。它们不要求改动现有冻结数学结论。没有其它声称已完成而实际未读的审查。
