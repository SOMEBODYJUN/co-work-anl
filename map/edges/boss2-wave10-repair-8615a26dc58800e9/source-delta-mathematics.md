# 零 incidence 勘误后的门控值桥定向复核

本页属于 `boss2-wave10-repair-8615a26dc58800e9`，身份 Boss2。正式任务当前为 claimed/Boss2，认领 request 为 `8d6e4deb34494a129a7b7332856173d3`；定义 pin 为 `2a167f9a7bde3aab346b3b2d2e408882d876cefc1b79546760d78ea73019c33b`。本文只形成数学交付；原生绑定、检查、Git 推送和 done 留给 Boss 统一执行。

## 本次源差分及逐 job 覆盖

唯一源差分在《归一化菜单福利与配置证书双源审查》的“二、完整归一化菜单的配置证书桥 / 1. FSLP 与完整 flat machine CONFIG(1)”：互补 private 配置由“所有 positive incidence”补明为“全部 incidence jobs（含零 jobs）”。当前全文 SHA 为 `33bd31b883b26f49508808dd7175cd104f391b86642bff90ea2bce7f1142097b`。将该唯一句逆替换，精确恢复旧全文 SHA `63629abaa5cd2bcc0e42ff051936b91882ea63c711dfdac231f238763b682255`，因此本轮没有未解释的第二处源差分。

对每个 state 的 private，以 λ 取 selector 加全部零 private-time jobs，以 1−λ 取全部 incidence。正 incidence 在 private 得 1−λ，在其命名资源 singleton 得 λ，覆盖恰一；零 incidence 同时属于两个 private 配置，覆盖 λ+(1−λ)=1，增加负载为零。每组 selector 的总覆盖为 Σ_s λ_gs=1。资源 singleton 只对正 support 计 λ，剩余空配置合法，容量仍是 Σ_{g,s:u∈P_gs} λ_gs≤1。零 incidence 没有给资源机增添质量。

主正文《规范化平菜单的 CONFIG(1) 与正支撑 FSLP 双向保持》的“1. 平坦不相关机与 FSLP 的双向证书”原来已正确写“全部 I_gsu”，当前 SHA `8bfbaa80b98546b6d1320e9760bb9491165e26a6cef1b6cd35eb86116c822f66`。反向 CONFIG→FSLP 仍只使用 positive incidence 与 unit selector 不能同处 private 的排斥；零 job 不提供该排斥。此次修订只修复审查摘要中的逐 job 覆盖，未改变主证明、模型、陈述、量词或结论。

受影响边引用的是源文件的“**一、归一化门控菜单的精确实际值**”；该章节内容没有改变，但引用 SHA 绑定全文字节，仍须更新。WELFARE 与 13/8 两端点当前分别为版本 6、pins `db1912d2262298cc45f879dfb52c315f6d5e10c3da4571a4756f4577f6dc0876` 和 `94dffb9efd7fe5c0c5f91d33d7c8da06be50b259084298ec14fedcf1bf765be2`。

## 无 FSLP 的完整 P_gate 值桥

域为非空有限组 G、n=|G|≥1、非空显式 indexed states、每 state 非负二进制有理权重和恰一、state 内资源标签互异。bundles 全局两两不交，资源可闲置。零 incidence、重复 indexed states、全部未选 states 的 jobs 和 unused 机器均保留；未列的零系数不凭空造物理 job。R、X_g、M_gs、Q_u 四类机器互异。root pin 只在 R 时间一；connector 在 R 时间 1/n、在自身 gate 时间一；selector 在自身 gate 或本组 private 时间一；每个 listed incidence 在自身 private 时间 p_gsu、在其资源机时间一。

令 β*=max({0}∪{min(|H|/n,min_{g∈H}v_g(B_g)): H 非空，B_g 全局不交})。有限显式组合域上最大值取到，但定义不提供搜索 oracle。对任意给出的平衡见证 b>0，取各组达到 bundle 价值的 state，并按下表完整执行原 jobs。

| 原 jobs | H 内 | H 外 |
| --- | --- | --- |
| root pin | 始终在 R | 始终在 R |
| connector | 自身 gate X_g | R |
| selector | attaining private M_gs | 自身 gate X_g |
| incidence | 仅选中 state 且在本组 bundle 上的正项去 Q_u；其余全部回自身 private | 全部回自身 private |

R 的负载为 2−|H|/n≤2−b；选中 private 的负载为 2−v_g(B_g)≤2−b；每个 gate 恰一枚 unit job；其余 private 负载≤1；资源因 bundles 不交至多一枚 unit job。因此实际完整峰 C≤2−b。b=0 单独使用 pin 与全部 connector 留根、全部 selector 去 gate、全部 incidence 留 private 的峰二基线。这里“其余全部留 private”仅可指 incidence，不能指全部 jobs。

反向对任意完整实际调度 C<2，取 connector 真正在 gate 的组 H。R 负载恰 2−|H|/n，故 |H|/n≥2−C>0。H 中 selector 不能与 gate connector 同处，只能去某个本组 private；该 state 本来的 incidence 总质量一，加 selector 一，迫使至少 2−C 正质量导出。每个 Q_u 在 C<2 时至多接一枚 unit incidence，因而这些真实导出 bundles 全局不交。于是 β*≥2−C；未选 state 的其它导出项可以忽略而不破坏不交。C≥2 时只用 β*≥0。前向、反向和 root pin 合成

\[
\operatorname{OPT}(P_{gate})=2-\beta^*\in[1,2].
\]

整个值桥和给定见证的总位多项式回填均不要求 unit-FSLP。它也不把 flat 全组 max-min V 换成部分选组 β*：两组仅有同一个单位资源时，flat V=0、实际值二，而 gated β*=1/2、实际值 3/2。

## 从福利到平衡见证，再到实际峰

为避免混淆，以下用 **W** 表示总福利，用 **v=βhat** 表示输出的平衡质量。W≥(5/8)L 本身不能直接写成实际峰≤2−W；必须完成排序提取这一步。

目标 v2 自己求解一般福利 LP：Σ_s z_gs=1、0≤x_gsu≤z_gs、Σ_{g,s}x_gsu≤1，最大化 L=Σp_gsu x_gsu。该 LP 总可行（选任意实际 state、令 x=0），且 W*≤L≤n。真实 allocation 取 attaining state 后可嵌入 LP。算法输入只有菜单，必须实际求得 LP 解，不能把一份给定 unit-FSLP 或存在性证书当成搜索结果。

按 z 抽 state，再以 x/z 提议正 incidence，初始每资源每个正 tail level 的跨组提议概率和≤1。独立乘积及有限 levels 尾和给期望福利≥(1−1/e)L。逐组固定 state、再逐 coin 固定分支时，每一步枚举正概率分支并取精确有理条件期望最大者；概率零/一直接取唯一合法分支，避免 0/0。条件化后提议概率和可超过一，必须重算有限有理乘积，不能再套初始容量不等式。最终资源赢家产生全局不交 bundles，按菜单重选 attaining state 不减价值，得到

\[
W=\sum_g r_g\ge(1-1/e)L\ge\tfrac58L.
\]

排序 r_(1)≥⋯≥r_(n)，扫描 v=max_k min(k/n,r_(k))，实际输出达到该最大值的前 k 组及其原 bundles 和 attaining states。这是明示可回填见证：组比例和每个选中组质量均≥v，因此前节给完整实际调度 **C≤2−v**。令 h=#{g:r_g>v}，若 h>nv，第 h 项会使 min(h/n,r_(h))>v，矛盾；故 h≤nv。由 0≤r_g≤1，

\[
W\le h+(n-h)v\le n(2v-v^2).
\]

β* 的 attaining witness 至少有 nβ* 个组、各有价值≥β*，故 W*≥n(β*)²。结合 LP 与福利界，得到 2v−v²≥(5/8)(β*)²，即

\[
C\le2-v\le1+\sqrt{1-\tfrac58(\beta^*)^2}.
\]

对 β∈[0,1]，D=(13/8)(2−β)−1=(18−13β)/8>0，且

\[
D^2-(1-\tfrac58\beta^2)
=\frac{209\beta^2-468\beta+260}{64}\ge\frac1{64}.
\]

分子在该区间导数 418β−468<0，最小值在一。于是 C≤(13/8)(2−β*)=(13/8)OPT。平方根和 e 只用于分析；算法比较有理数。显式 LP 变量数、levels、states、coins 和直接重算乘积次数均多项式；有理分母位长按输入分母位长之和及多项式次乘积控制，不依赖最小正概率的倒数。该数学总位多项式规格与现有有限浮点提案/Fraction 认证软件的生产实现范围分开。

本段核清了目标正文已支付的完整算法步骤，但本条 `um-normalized-welfare-to-general-ratio-value-bridge` **仍仅交值分母和回填的 STEP**。源的 unit-FSLP 福利/绝对峰 13/8 子定理不能单独推出任意 norm1 类的整条比例算法。一般 LP、两阶段条件期望及其位复杂度、福利界、排序两式和二次比较仍是这条边的 `contribution.remaining`，由目标自己的成熟证明支付，不能据此把本边升级为 whole。

## 其余十一核心覆盖及实际剩余边界

以下各项继承前任 `boss2-6405-source-repair-b61b3ed236a4a90b` 收据的实际已付比较。本次读取全部旧 coverage、四条旧边和旧数学说明，核当前十五个对象记录及 pins、全部 declared refs 的字节；没有把这些历史证明或旧程序记作本次 fresh 全文重读/重跑。

| 核心 | 保留状态及数学边界 |
| --- | --- |
| ROW-DEGREE / RAW-K2 两核心 | linked；raw→row 只传实际 OPT 与 affine slack。fixed-d 插值只作用 mixed 部分，pure-home 抵消、Rfill、负质量吸收与固定 d 复杂度仍由目标独立支付；d=2 指定 M/Qnew 不等同 raw。 |
| WELFARE | linked；本次重核无 FSLP 值桥、完整 jobs 和零项差分；保同 edge_id、accepted/unconditional/ALL/STEP。 |
| VW Theorem16（M-5b626…） | isolated-after-review；全局潜在 big 资源集合常数不能弱化成某最优解所用大端数。外指技术报告完整算法证明仍缺，维持 unassessed，不造支持。 |
| affine-line review | isolated-after-review；单 primary pairwise、multi-primary all-pair simplex、R-states 单边际三合同分立；没有已付跨模型桥。 |
| OPT-HULL-HIGHER-NC | isolated-after-review；同一固定 x 的完整达到 law 保同组正 cylinder 上界，不含补事件/跨组 NC，不付多数状态内不交束或条件叶 all-core law。前任 k−q 修正及边界保留。 |
| DGR（M-43f278…） | isolated-after-review；允许裁剪且期望选组的 packing，0<δ<1 时保留比例 9δ²/8000；δ≥1/空集合分支保留。不自动给完整集合或全部物理 jobs 的调度。 |
| TERNARY-PALETTE | linked；单 pin 树→palette 只给实际 OPT=2−q/3^k 及路径上界。末层两色、tuple/binary 达到、常量/正高度、G_k 递减与纯收缩由目标独立支付。 |
| conditional-leaf/sink common law | isolated-after-review；各条件 matching mixtures 与相同平均叶边际不提供共同 all-core 逐样本容量 law。抽象 Bernoulli 兼容性警告不是原 UM 的已恢复反例。 |
| FIXED-SINK-MACRO-PROMISE | linked；固定 K/唯一 home 及每有限宏端>OPT/2 承诺内维持 whole。单侧 FAIL 和实际成功见证支持非单调网格搜索；成功不等于 T 可行，承诺不能免费删除。 |
| HEAVY-ALTERNATIVE-FILTER | isolated-after-review；严格>T/2 的匹配界只给安全必要过滤。弱化≥会错删；raw/fixed-d 的 U/B/Z 初始域首轮零删的解析比较继承，不推出接受后调度。 |

任务和直接前任的 definition/context_plan 均无 declared overlap_comparisons / follow-up 对；本次没有复用任何旧 follow-up task，也无新增需要任务化的跨包问题。前任 NC 与两状态多数的 in-packet 比较保留为合同分离：固定边际/同组 NC 与单状态残余束不交互不提供所缺桥。

一般 UM 的 near-two 算法/困难性、真实可靠源的 YES/NO 编译、全部物理 jobs/ports/one-hot 与 decoder、共同 all-core 相关性及更强系统边界仍按各原对象范围保留。给定 T 的分数 CONFIG 证书存在性、证书转换或单侧例程不能免费令 T 等于未知实际 OPT，也不提供整数 perfect completeness。此次勘误不解决这些义务。

## 阅读归属、资产时点和交付边界

本次 fresh 实读：AGENTS、完整 IMPLEMENTATION 与 worker 提示词；当前任务定义和直接前任任务比较范围；前任十一条 coverage、全部交付/阅读/验证字段和四条边；前任 repair_mathematics；本预核报告全文；源纠错 ledger；impact-3d 的本桥 entry 及阅读归属；当前两个门控端点完整 records；FSLP 四源、福利配置双源、gated-v2、八源、比例纠错最终审查全文；主定理“对象、全部条件与精确陈述”和“1. 平坦不相关机与 FSLP 的双向证书”完整章节。其它十三个当前对象 record 的模型、陈述、量词、假设、scope、objections 均读取核对。

本次元数据核：十五 pins；七 prior assets 原字节及其在前任 receipt 的精确成员关系；三条未受影响旧边全部端点及 direct evidence 的当前 SHA；七十条任务 reading refs / 五十二文件的全文 SHA 与唯一标题存在。字节核验只证明引用当前，不能替代数学实读。未重建六份历史 registry records 的全字段旧快照；前任 record contract 与当前的源唯一差分、两端点现行陈述及现行正文一起确定本轮范围。

历史继承：除上述 fresh 范围外，raw/fixed-d、NC、固定 sink、DGR、palette 的底层原证明、其它旧审查、外部 PDF 和历史有限科学运行按前任实际成熟范围使用。未 fresh 重读全部五十二文件，未重跑任何历史科学程序、生产 LP、scheduler 或旧 audit。旧 `repair_mathematics.md`、`repair_audit.py`、`repair_audit.json` 保原路径原 SHA；其中“当前”“本轮”等措辞均指前任 source-repair 的历史时点，不能作为本轮源 SHA 或本轮新运行声明。旧数学说明本已保留全部 incidence，其有效论证可以继续引用。

七份直接前任资产只替换福利桥，其余六份逐项 retained 原 SHA。新边语义已由本次阅读定为 accepted/implies/unconditional/ALL，`contribution.result/remaining` 原义原文保留。旧 `review_digest` 删除，等待 Boss 对最终新文字执行原生 bind/check；本次文件与收据列的是实际原始字节 SHA，不声称已绑定、pushed 或 done。
