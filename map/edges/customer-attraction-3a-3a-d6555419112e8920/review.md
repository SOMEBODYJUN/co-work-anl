# d655 当前 18 核心数学审查

本轮是正式 fresh worker 的实际阅读，不把 Root 预研当作已完成 primary 覆盖。当前任务 owner Boss6，request `ea3e0804a1f447bfb0c90a64e3f8448e`，definition pin `fa4503f777bef11f854015e9dd0de094d0ecdd60a0331bc144da3a6e18ac53b6`。18 core、11 read 的全部 29 对象记录及各引用完整文件 SHA 均核对一致。每份核心完整数学陈述、模型、量词、条件、scope、objections 和承重正文均已直接实读；ME/EX 等对象以其精确登记章节为正文单位。大型原始报告的实际选读字段与只核字节范围分别记录于 reading-ledger，未声称重读所有大策略表。

所有 Python 均用 `-B`。本轮没有运行旧 LP、SPE/IC、DP、随机生成器或有限数学证书程序。精确数字和成熟执行按已发表正文及各自原证据合同复用；文件和 pin 检查、只读 edge_bindings 不充作科学执行。所有新写入仅在指定 staging，clone 只读；Git、队列、源修改、registry、canonical 与发布全部由 Root 串行组织。

## 新关系与数学实质

**区间包含 + 十客户有限表 → 同游戏所有 SPE 全效率，whole。** 一般 H_I 保留全部完整 SPE 终局；在十客户四标签游戏，前缀 0 的第二行动收益区间为 `[2,5/2]、{1}、{3}、{7/2}`，只行动 3 eligible，真实末位在 03 选 2 得 3，对其余 0/1/3 得 2/1/2。故根 0 可完成 032。其余根孩子的排序终局为 123、023、023，根四收益 7/2、2、3、7/2，H_I 根仅保多重集 023。一般包含性与该精确表共同迫所有 SPE 覆盖 10=OPT。根菜单的 W7 分支 003 仍因倒二改 2 后唯一末回复 3、收益 3>2 而不可信，不能转作真 SPE 反例。超边保两个共同来源 ALL；不把 H_I 当一般精确 BI。

**BALANCE → AFC 精确未付义务，step。** 固定 p 时，各位置 q_i 各自归一且独立于本次查询，有 min_q Θ=Σ_i H_i(p)。逐列势抵消于是给

`W−Σ_i H_i(p)=max_q[E(p,q)+R(p,q)]`。

所以一般 AFC 精确等价于每 p 存在 q_i 使 E+R≥0；有限双线性 minimax 又等价于同一组 q_i 同时封顶全部纯 T。推导没有证明这个存在性。SPE 只使 E≥0；36 客户最优菜单的 E=64/15、R=−46/15，合计 6/5。不能删掉负跨势项，也不能把可观察本次 T 的选列混成共同 q。

**36 客户精确 164/5 → AFC 定量固定实例，step。** 18 真删槽列仅有 34/01/02/04/03 五种静态背景，但保全部原位置、强制动作和叶身份。p*=(0,2/5,2/5,0,0,1/5) 给 H1=H2=52/5、H3=12。q1=(2/5,0,0,3/5,0,0)、q2=(1/5,4/5,0,0,0,0)、q3=e0 的六纯查询封顶值为 `(401/15,164/5,164/5,419/15,158/5,164/5)`，匹配证明全 p 最优恰 164/5、最坏余额 6/5。这保留精确优化值和 18 列的独有作用，不重复固定分组全非负 CAG 锥共同 Q 的粗 W 封顶路线；p* 不是声称真正静态 v3 的安全最优分布。坏 p 的自由最小列和 65/2 与自身同 law 推送 69/2 严格区分。

**CAEXACT → individual probe 的全 SPE 逐人量词，step。** 全集 R(0) 的必要充分性给：每完整 SPE 的终局都在其中，且每个保留计数可由某份完整有序历史 SPE 实现。因此 `v(I)=min_{c∈R(0),a:c_a>0}φ_a(c)` 恰为固定输入所有完整 SPE 及全部实际玩家的最低收益；排除缺席主题的软件零值后，弱逐人阈值等价正确。指定 argmin 顺序仍须逐前缀目标筛选；原稀疏 13/8 条日志、192/1500 计划次数、FATAL 可 exit0、无完整动作图等边界不由该算法语义补认证。

**CAEXACT → 九人 low-tail 量词，step。** 对给定目标 q，路径转移必须同时满足 q∈R(b+e_a) 与 U_a(q)≥M(b)。必要性来自真实偏离，充分性在不同有序孩子分别拼子 SPE；同计数仅缓存集合，不统一原策略平局。因而成熟双实现按这条精确转移得到的 20 根计数、18 最差目标、每目标 1440 路径，确可量化所有最差 SPE，而非一份选择器。25920 条路径都六叶先行，尾利润 100,120,120，分别给 960/1005>946；pair_min_cost 仍是较小成本 960。原数据归原双实现证据，本轮未重算大 DP、未物化全部策略树。实际价格 B(120)=135 与 half 余量 926 保持独立。

**鲜源同次 F-BUDGET → Q-CAG-HALF，accepted conditional whole。** 前提明确为：每个 m、每个输入、每份完整 σ，都存在同一个最优 O、一次合法仅 C 外鲜源分配和由此重新计算的同一 ν 流，M=OPT−W 且 BF≤W。源 current 精确式和 INIT-MASS 为

`A_i=θ_i(u_i−Y_i^src−e_i^src)`，`M=Σ_i A_i+Σ_t b_t`。

同一 ν 图的 F-LEDGER 为

`Σ_t b_t=Σ_t β_t(u_role(t)−Y_t−N_t−e_t)`。

所以 BF−M=Σ_i θ_i e_i^src+Σ_t β_t e_t≥0，进而 M≤BF≤W，OPT≤2W。推导完整，故不是 proposed；开放的是全称共同选择和费用上界，不能逐 source/context 换点。源量≤1、θ≤1、真实 query、ν 正分母、future DAG 都保留。未除 W，零客户、空覆盖、重复和同覆盖异标签均含。不存在把原更强 |O\C|≤W 偷换进目标的步骤。

## 已有 canonical 的精确复用

两条两人税边、ME 到八统计行边、平稳成员矩到 −4/3 协方差见证边已逐字节核 SHA 及当前 endpoint/evidence/review bindings。完整路径与 SHA 在 manifest/receipt 列出，不复制同证明关系。

两人税根锐性实读包括两个完整 SPE 端点、客户不交和标签 Cartesian 产品、单位复制与每个有理 I/W 的显式参数；非零背景仍只比较剩余利润。普通税与实际末位 BR 的最小值推新生重叠界，不把两个加权式作全域支配。

ME/MM 实读完整登记静态章节，EX1/2/3 的承重替槽证明，以及八行原代码与成熟形式基报告职责。取 k1/Y空并对六比较槽求和，actual 各六倍、B/C 各族求和，统一系数为 `6·1[d=1]−r_F·1[d=1]−6r_F·1[d=0]`；R/Z 不影响系数、辅助列零。比较元组真最优不可省。独立均匀抽槽不产生互斥真叶之间的共同付款。

平稳核是包含原根的全槽 P，m≥2 时与仅后继 K 同平稳集。36 客户的唯一 p=(1/4,1/4,0,1/4,1/4,0) 仍满足每客成员矩，而收益差为 10−34/3=−4/3。不能从 E X=E C/m 给比值或协方差符号，也未与 22 客户另一静态 cap 混用。

互惠两当前 v2 正文已完整实读：复制数 r 对应前缀后 r+1 个位置、|H|+r+1=m；R(b) 读取 H+b^r 的真实末节点。固定前缀核对称/真 BR 单调，加上把本步回复移入前缀的 δ 转移和逐客调和望远镜，可得跨前缀阶梯整条结论。r1 端点债是 signed，不误用非负债；r2 同前缀 cohort 一次支付不推广到 r>2。本轮接续已全文实读并核已发布 DD45 payload，路径为 `map/edges/customer-attraction-3a-3a-dd45d4a4c0eb661e/reciprocal-kernel-pays-harmonic-staircase.json`，SHA `a69f98930f361e6e5100ec21e7296549be65bd55f0b66c1ba114a2a40818bac1`，当前 bindings 一致。正式 registry canonical gate 已由 Root 在 commit `02e79ef113022e28a647b8b51bed1c7db4794bb4` 确认并推送；现在按该原 SHA 接入最终收据。

## 各核心覆盖的实际决定

| 核心 | 实际比较与结论 |
| --- | --- |
| M7cb 背景新生重叠税 | linked：复用普通税+真实末位 BR→背景界及背景→根锐界；整数背景、剩余利润和完整端点齐备。 |
| M9a 根重叠锐性 | linked：复用背景专门化+两完整端点+不交 Cartesian 产品+复制，所有有理比例均取等。 |
| Md782 十客户所有 SPE | linked：HI 一般包含与同输入有限表 ALL 给 whole 全效率和实际 032。 |
| root-menu 压缩障碍 | linked：为同一实例 HI 表提供共同来源；压缩菜单的倒二致命偏离独立保真。 |
| free-column BALANCE | linked：AFC 义务等价重写，E+R 合计；R 不单独非负。 |
| 36 free-column exact | linked：164/5 匹配全查询证书给 AFC 固定实例定量贡献，不外推一般预算。 |
| M229 ME/MM | linked：复用已有八统计行特化；静态抽槽与动态共同付款分开。 |
| closeout9d18 双诊断 | isolated-after-review：固定 σ 全历史 floor 与 all-subgame overlay 是不同输入；六行和十九行报告、Q 泛用 guard 缺口、本实际域合法性、一个 query 不精确归一以及两微负 float 均保。没有把保存字段或浮点 gap 变成新 SPE/一般 PF 证明，当前包无精确相应目标关系。 |
| stationary covariance | linked：复用实际 P 的唯一平稳分布及负协方差步；不保证符号。 |
| individual probe | linked：CAEXACT 支付其全部完整 SPE 的最低占用收益量词；稀疏旧日志保有限历史身份。 |
| shared-only floor failure | isolated-after-review：18 客户/七极大/六人恒 0 在所有有序历史合法，u=2、W12、OPT18；六共享行均 −6B_t，而正确 total mixed 行≥5/12。它只否源选择性删私有支付行，当前包没有等同被否行的独立目标；不否 F-BUDGET、正确 mixed 或 half。 |
| four-provider structured optimum | isolated-after-review：固定策略全 63 类型锥的 9 项原始点、7 IC+4 pack 对偶与全 63 余项证 3/2；其相对私有块含 B 客户，不能当全目录私有或未覆盖量。点上 δ1=1/2、块比3/2，不是同量。ME 静态替槽不能替固定锥全部 IC/对偶，未造同数值关系。 |
| F-BUDGET | linked：对 Q 的 conditional whole 已完整合成；BF≤W 的同次全称存在性仍 open。 |
| M534 m5 mask28 | isolated-after-review：同完整动作表全部规定核心 alias，C/(g+r)≥C/m，私有偏离≤q 给真全历史解析认证。decimal/new q1/5 合法；exactbinary q>1/5，根差 −1/90071992547409920。不是 m6/m8 或其它 m5 原输入，未因相似模式强连。 |
| M045 curvature | isolated-after-review：一般 p* 最坏背景的一槽替换逐客给 α 加权二阶差；不是无 α 一阶 δ+。与大主题族的全部最坏真实源精确比过，必要行满足而无ρ债仍正，没有反驳正确曲率，也没有由必要行推出整个族。 |
| nine low-tail selector | linked：CAEXACT 支付成熟有限分类的全部最差 SPE/可实现路径量词步骤；数据与原执行仍归原作者。 |
| Ma232 reciprocal staircase | linked：数学比较完成，按 DD45 当前 v2 已正式发布的 whole canonical 精确路径/SHA 复用。 |
| M1d m6 mask134 | isolated-after-review：三版本 q≤1/6 都全历史 SPE；仅新1/6 清分母为11客户、W6/OPT11。原 decimal/binary 精确大整数各不同；相似 core-only 证明不产生新迁移，未新枚举1287表。 |

## 两个 declared follow-up 已闭合

individualprobe/CAEXACT 由上述新量词贡献落实；没有未付的新比较需要另发 3B。

curvature/bigtheme 已直接比完：D=2L+m+1、α_B=(m+1)/D、α_S=2/D。在 q=mB 的 B→S 交换，曲率左右均 1/D；在 q=(m−1)B+S 的 S→B 交换也均 1/D。所有真实源都是静态纯最坏背景、静态 regret 为零；但 Eδ+ 在 mB/B 和 mixed/S 两类都严格正，而 Eδ+−ρ=−1/D。由必要二阶行跳到无ρ一阶债非正的加强明确失败，正确的带α曲率与含ρ预算没有失败。m 背景槽对应 v_(m+1)，不混 SSR 的 m−1 槽。该对已完成数学处置，closed_overlaps 只含这两个 declared follow-up；互惠 in-packet 不填 closed。

## 开放边界与交付

一般 AFC 的共同 q 存在性、F-BUDGET 的同次共同费用存在性、互惠阶梯终点与调和租金的共同 actual 钱包都仍开放。固定锥、有限精确值、局部静态交换、原负浮点与完整 SPE 反例各保自身范围。没有新节点需求，也没有源更正需求。

最终 manifest 列新文件逐字 SHA，canonical 复用另列；收据不自列，manifest 不 hash 自己或收据，避免环。Root 原生 edge-bind/check 后若字节变化，只需更新受影响边及 manifest/receipt SHA。

## Round51 同批接续核读

当前 request/definition 保持不变；在 HEAD `d78c5663460515016d7774551ddd7ff68c4a47c4` 重新核对全部 29 对象 pins 及所有引用完整文件 SHA 均一致。互惠已发布 payload 已由本 worker 全文实读，核对同 m、真实末节点、δ 转移、T0/r1 和调和租金，数学与 scope 无修改；观察当时尚未进入 registry；现已由 Root 推送 commit `02e79ef113022e28a647b8b51bed1c7db4794bb4` 完成正式 canonical gate，按原字节复用。

Root 提供的 fresh 独立数学交叉审阅已全文读取：六条新关系及四条旧 canonical 审阅 PASS，无数学 blocker，12 linked/6 isolated 的数学决定获确认。独立审阅的阅读量和成熟原运行身份没有计作本 worker 的新增阅读或执行；本轮只承接其无改动审阅结论。所有数学 edge 文件字节保持原样，0 科学重跑、0 clone/Git/队列/source/registry 写入。
