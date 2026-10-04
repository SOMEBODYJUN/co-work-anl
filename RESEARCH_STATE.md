# 当前研究状态（2026-10-03）

**2026-10-04 条件性算法推进。** [SC-K-INCIDENCE-BOX-DP / SC-K-HEIGHT-TWO-INCIDENCE-2](research/current/multi_facility/bounded_incidence_box.md)精确判定贪心盒内的站纯客户 NE：冻结重客户与单选项客户，对每个已占站列举至多 `2^d` 个入站轻客户子集，将逐名二部关联图宽 `tau` 的分解转成站点约束图宽至多 `d(tau+1)-1`。当 `d,tau` 固定，选择器位长多项式；浅层有向轻图保证盒可行，接 BOX-TO-2 得完整多项式因子 2。此结果只扩展可算子类，不证明一般贪心盒可行或任意输入的目标算法；已给出数学证明，外审与规范实现未完成。

以 [README](README.md) 了解模型与文件地图；逐命题严格条件和五轴审查状态分别见 [现行登记](research/current/claims.md)、[审查表](research/review_status.json)。本页只维护**未来前沿与工作分配**，不替代证明。

## 本轮新闭合的可算范围

[RESET-PACK / DOUBLE-LPT](research/current/multi_facility/polytime_frontier.md#sc-k-reset-pack-interface-reset-based-off-path-completion-beyond-the-box) 把离轨接口从“必须找到站点盒内 NE”放宽到每家在轨至少 $\gamma$ 且原始客户池删席装箱可检查。双 LPT 是一个位长多项式充分测试；三站三角例在轨纯 NE 的 M 总负载 $430>400$，仍能按原池重置给出完整 2 倍续局。另有有向轻权路径算法允许不同边异权；固定占站数与不同权数的类型整数规划精确判别盒 NE，固定总目录与不同权数则有无条件 XP 构造。[精确范围](research/current/multi_facility/type_compression.md)。这些均经内部逆审，尚无规范通用软件、外审及优先权核验。任意参数下的位长多项式因子 2 算法仍开放；下方旧叙述中的“盒内 NE 是唯一瓶颈”已被 RESET-PACK 的充分条件放宽。

[三站任意异轻权链存在性](research/current/multi_facility/three_site_chain_box.md)表明完整上下盒内的势最小点必是客户 NE；整批退回上游客户的交换排除唯一被上盒挡住的返程。这仅给存在性，没有多项式势优化算法。

[四站汇聚路径小类](research/current/multi_facility/converging_path_box.md)在每边恰一轻客户、指定重数顺序及汇聚站初始紧下盒时，以至多七步构造盒内精确 NE；其条件可检查，并未覆盖一般树。

[浅层有向轻客户图的盒 NE 存在性](research/current/multi_facility/height_two_box.md)：贪心首开方向中最长有向路径至多两边时，任意分叉、汇合、异轻权都可用 first-crossing 整池交换证明完整盒内势最小点为 NE。三站链是特例。这是存在性与有限选择器，位长多项式求解仍开放。

[汇聚四站的四步放宽版](research/current/multi_facility/converging_four_moves.md)删除旧小类的 A 紧下盒及 A/C 等重数限制，只保留每边恰一轻客户与贪心开启方向；仍给位长多项式完整 2 倍续局。

## 已有地基

双设施共同目录的黄金比上界、相应六地点锐性、异构双设施的因子 2 分支与短目录单交叠的 \(\rho=2\cos(\pi/7)\) 分支均有现行数学稿；各自审查状态并不相同，均尚无外部同行评审。[完整范围表](research/current/claims.md)防止将实例证书与普遍定理混淆。现有成果的投稿、实现复核和文献归属是交付工作，不占新的数学主攻方向。

## 当前前沿与本轮闭合

**异重轻客户星形分量的位多项式 2 倍算法（2026-10-03）。** [SC-K-STAR-LIGHT-GREEDY-2](research/current/multi_facility/polytime_frontier.md#sc-k-star-light-greedy-2-unequal-light-weights-on-anchored-star-edges)把同重费用流之外的可算范围扩到轻客户交叠图中的锚定星形：中心先开，每名轻客户只可选中心与一片叶；其他轻分量可同重数，重客户可跨分量。各叶按权递减队列，只移动严格改善的队头，并在候选叶中选当前最低单位负载。每名客户处理一次；贪心重数序保持上下盒，最后入叶客户与候选叶负载单调性保证精确 NE；BOX-TO-2 完成全部偏离。一个三站异轻权、不可比选项集实例同时在旧 RANGE、ALL-OR-ONE、NESTED-ANCHOR、UNIFORM-LIGHT 的条件之外。证明已内部独立逆审，有限有理数例只核算该实例；有向路径和双 LPT 后续机制已覆盖部分非星形图；一般图仍开放。

**异重轻客户的精确势障碍（2026-10-03）。** [SC-K-TWO-LIGHT-LOWER-POTENTIAL-NO](research/current/multi_facility/polytime_frontier.md#sc-k-two-light-lower-potential-no-lower-bounded-potential-can-overflow-with-two-weights)给一个显式无限整数族：只有两名不同轻权多选项客户，贪心七设施、四站初态是盒内精确 NE；但对全部站施加下盒后，全局客户势最小值仍唯一选到 L 站越上盒一单位的精确 NE。四态代数证明与独立 Fraction 核对明确了同重运输反路径不能直接照搬。旧势最小反例已有更强的设施收益失败；本族的新价值是将该算法接口障碍隔离到仅两个异重轻客户。**盒内 NE 依然存在，不能据此判定贪心选址或全输入 2 倍算法失败。**

**离轨接口与无锚链形构造（2026-10-03）。** [SC-K-GREEDY-SINGLETON-RESET / SC-K-GREEDY-BOX-TO-2](research/current/multi_facility/polytime_frontier.md#sc-k-greedy-singleton-reset-and-sc-k-greedy-box-to-2)给出一个盒内精确在轨客户 NE 的充分路线：对原 $q=1$ 的设施，偏离后直接回到初始贪心客户分配，原单站客户池每站至多 $2\gamma$、原高重数站可按 $2\gamma$ 装箱，故不需在轨客户的私有储备或原孤儿预算；任意在轨收益 $a\ge\gamma$ 都有位长多项式离轨纯 NE 使偏离者至多 $2\gamma\le2a$。若给出盒内站纯/站内均匀的精确在轨 NE，其余 $q\ge2$ 来源也由盒预算完成全部 2 倍续局。

[SC-K-UNIFORM-LIGHT-FLOW-2](research/current/multi_facility/polytime_frontier.md#sc-k-uniform-light-flow-2-partial-overlaps-without-a-common-anchor)进一步处理任意交叠图和混合重数，只要求所有低于 $\gamma$、可选择多个已占站的客户具有同一权重 $\delta$。冻结其他客户、用每站下界的整数凸费用流最小化精确客户势，初始到终局的同重运输逆路径严格排除上盒溢出；高权客户也保持最优反应。与盒内续局引理合成位长多项式 2 倍完整构造。严格 $(3,2,1)$ 三站链例不属 RANGE、ALL-OR-ONE 或 NESTED-ANCHOR。内部独立逆审与 Fraction 复算通过，尚无外部评审或规范软件；**不同轻权的普遍盒内 NE 存在性与多项式选择仍开放**。

**新增部分交叠条件类（2026-10-03）。** [SC-K-NESTED-ANCHOR-GREEDY-2](research/current/multi_facility/polytime_frontier.md#sc-k-nested-anchor-greedy-2-a-partial-overlap-mixed-component)证明：贪心每个混合重数交叠分量若有首开共同锚站，且多选项客户按权重非增排列时选项集逐步扩张，则受限列表分配可位长多项式构造精确在轨 NE 和完整 2 倍续局。它包含先前 ALL-OR-ONE 类，且一个严格三站整数例有真正的部分交叠，旧 RANGE 证书失败。负载盒只靠共同锚站就能保住；精确 NE 额外依赖选项集的顺序。交换同一例两个共有客户的选项集后，无条件列表法产出非 NE，虽然另有精确 NE。该反例只限定此列表规则。一般三站及以上的部分交叠、非嵌套输入仍开放。新证明经独立内部逆审与精确整数复算，未外审，规范软件尚未实现。

**第二阶段新增推进（2026-10-03）。** [SC-K-ALL-OR-ONE-COMPONENT-GREEDY-2](research/current/multi_facility/polytime_frontier.md#sc-k-all-or-one-component-greedy-2-arbitrarily-many-mixed-multiplicity-sites)把条件性多项式 2 倍算法推到**任意大混合重数交叠分量**：每名客户在该分量内的已占选项要么唯一，要么包括分量所有地点。首开地点初始收下全部共有客户且最终重数最大；把这些客户按权重递减分配到当前单位设施负载最低地点，得到精确客户 NE。首开地点保留的总量、其他站的私有负载储备，分别证明贪心负载区间及单设施源消失的装箱预算。原双地点条件类按作用域包含在新定理内；三地点 $(3,2,1)$ 整数例不满足旧区间证书，却由新算法处理。证明经过独立内部逆审，尚无规范实现和外部评审。

[SC-K-DESCENT-ONLY-TRAP-NO](research/current/multi_facility/polytime_frontier.md#sc-k-descent-only-trap-no-three-site-partial-overlap-needs-an-upward-return)将剩余障碍落在**部分交叠**：六客户、三地点 H--M--L、重数 $(3,2,1)$ 的正整数例中，全部严格向不高重数地点改派的最大路径唯一，却停在非 NE；重 2 客户必须从 L 向 M 返回。返回后有精确 NE，负载区间也未被破坏。因此这只排除“向低重数移动绝不回返”的策略，不是一般 2 倍下界。下一步应设计允许上升回返仍能在输入位长多项式时间终止、保持足够偏离预算的规则，或找出贪心布局的真正全 NE 反例；高效全输入 2 倍构造依然开放。

**本轮新增可计算子类及逆向界（2026-10-03）。**
[SC-K-TWO-SITE-COMPONENT-GREEDY-2](research/current/multi_facility/polytime_frontier.md#sc-k-two-site-component-greedy-2-mixed-multiplicities-in-a-two-site-component)
在贪心已占地点的客户交叠图中，允许每个分量重数一致或仅有两个地点且重数不等。对不等重数双站，按共有客户权重递减逐个检查从高重数向低重数的严格改善；每客户至多一次，得到精确在轨 NE，保持贪心负载区间，并补齐单设施源消失的预算。结合既有同速 Nashification 与离轨修复，形成任意设施数、位长多项式的完整 2 倍**条件算法**。三客户整数例在原重数类区间证书失败时仍由这条算法处理。内部重构通过，尚未外审或实现。

在另一个方向，[SC-K-GREEDY-FIXED-LEXMAX-NO](research/current/multi_facility/polytime_frontier.md#sc-k-greedy-fixed-lexmax-no-the-fixed-layout-lexmax-can-select-the-bad-ne)证明已有坏修复例的固定贪心布局唯一 lexmax 客户分配就是坏 NE；[SC-K-GREEDY-FIXED-POTENTIAL-NO](research/current/multi_facility/polytime_frontier.md#sc-k-greedy-fixed-potential-no-global-customer-potential-minimum-can-also-be-bad)给第二份整数例，解析分类恰两项客户 NE，精确势值 86200 的**全局最小**是坏 NE，偏离倍率在所有混合离轨均衡中为 $215/107>2$，而同布局势值 86264 的另一 NE 保有四预算。这两项排除固定贪心选址后的两种自然“选最好客户状态”原则；未排除其他选择规则、其他选址或混合在轨策略。与本页最上方新进展合并后，最窄前沿是至少三个地点、重数不同且客户覆盖关系部分交叠的分量如何多项式选择合适 NE，或必须更换贪心选址。全输入位长多项式 2 倍算法仍未得到。

**本轮已证阶段进展。** [SC-K-DISTINCT-GREEDY-2](research/current/multi_facility/polytime_frontier.md#sc-k-distinct-greedy-2-factor-two-for-all-distinct-greedy-output) 将贪心全异址输出的旧 3 倍多项式界提升至 **2 倍**：首开最大覆盖权 $R$ 地点最终仍只有一家时，贪心最后得分 $\gamma\ge R/2$；同速客户均衡算法保留所有在轨收益至少 $\gamma$，任意离轨收益至多 $R$。[SC-K-RANGE-GREEDY-2](research/current/multi_facility/polytime_frontier.md#sc-k-range-greedy-2-a-multiplicity-class-range-certificate) 更一般地按最终设施重数分组，若客户跨重数条件成本可由组内初始负载区间上、下界逐项排除，则组内多项式 Nashification 及单设施站客户池证明构造完整 2 倍续局。条件可位多项式检查，允许某些 $w_i<\gamma$ 的客户跨重数，也包含多地点 $q=1$ 与全异址输出。证明经过内部独立逆审；文献算法为已发表输入接口，新推论尚未外审，软件尚未实现。

**明确失效的修复规则。** 两个[六地点整数例](research/current/multi_facility/polytime_frontier.md#sc-k-greedy-repair-order-no-exact-repair-order-can-lose-factor-two)证明：从相同贪心布局出发，某条严格客户改派路径到达真正精确 NE 后，B 设施迁空 G 在**所有混合离轨 NE**中收益强制为 $176$，倍率分别为 $32/15$ 与 $88/43$；后一例的路径每一步都选唯一最重的可改善客户。同一贪心布局存在另一条一步路径，终点 NE 保留全部四预算。因此不能让任意严格修复顺序或“最重客户优先”充当全输入算法；反例不否定贪心布局也不否定普遍 2 倍存在性。

**最窄未决义务。** 范围证书失败时，双地点混合重数分量及任意大“全站共有或单站私有”分量现已覆盖；至少三地点、重数不等且有客户仅覆盖分量**部分**地点的交叠分量仍需位长多项式地选择适当在轨精确客户 NE、改变选址，或构造仅控制偏离者的离轨修复。下降重数路径可能不得不回返；同速分组不能直接处理所有轻跨组客户；固定布局的 lexmax 与全局客户势最小化也各被精确例否定。精确全局字典序选址强 NP 难与这些有限反例均不证明完整 2 倍搜索困难。全输入多项式算法及最优统一常数继续开放。

**本轮全 k 高效构造推进（2026-10-02）：**[精确计算前沿](research/current/multi_facility/polytime_frontier.md)证明一个条件性算法分解。给定原因子 2 证明所需的在轨布局及分配，全部实际偏离客户 NE 可借已发表的受限同速并行机 Nashification，在有理输入位长的多项式时间求出，保留宏原子隔离和偏离者的 2 倍上限。原证明要求的**全局字典序精确选址**由 3-PARTITION 强 NP 完全，不能靠直接实现它得到多项式算法；同一困难族却有易求的精确设施 SPE，所以这不是目标问题的困难性证明。四个转移预算实际上只要求一个多项式邻域的局部最大，形成明确的 PLS 搜索上界；未知的是能否在多项式时间抵达这样的状态或以另一原则直接构造 2 倍证书。完整的高效算法仍开放。

**进一步的预算分离。** SC-K-GREEDY-BUDGET 已用多项式贪心单独构造四个充分预算和正收益；在三地点四客户精确例中，冻结该布局并把客户修到唯一 NE 会破坏一项预算。故下一步不是再加速单独的预算生成或离轨修复，而是构造**同时**满足在轨客户 NE 与可用偏离界的状态，允许联合修改布局与客户分配。该例仅破坏过强的预算接口，不能作为 2 倍目标的反例。

**空地点偏离的精确收缩。** `SC-K-GREEDY-UNOPENED-2` 证明贪心布局上的严格客户地点改派保持所有在轨负载至少为最后插入分数；未开放地点的新增覆盖不超过该分数。即使源地点消失，交给迁入空地点设施的客户总重也至多为其新在轨负载的两倍。旧四客户例破坏的强预算并非该偏离真正需要的上界。当前证明缺口是**存续的占据地点如何装箱**，以及能否在输入位长多项式时间找到适当的在轨精确客户 NE；不要把有限改派终止当作运行时间界。

**旧子类与本轮提升的关系。** 同重数 $q\ge2$ 的 SC-K-EQUAL-MULT-GREEDY-2 与旧全异址 3 倍证明仍然成立；前者现在是重数类区间证书的特例，后者已被同一**全异址输出类**上的 SC-K-DISTINCT-GREEDY-2 严格提升。原非贪心布局的近 3 倍例仅反驳粗负载摘要，不能反驳新贪心得分机制。软件尚未实现，内部证明未外审。

**存续地点的初步瓶颈。** [九顾客五地点整数例](research/current/multi_facility/polytime_frontier.md#sc-k-greedy-static-pack-no-a-surviving-site-obstruction)证明：不等重数贪心布局上沿严格客户改派到某个精确 NE 后，即使偏离设施的原地点**没有消失**，若仍冻结其他客户的地点分配，某个存续地点也无法按 $2a$ 容量或单独宏客户装箱。这只否定固定地点分配的旧修复接口；客户可在存续地点之间重分，实例本身的 2 倍稳定性并未被否定。下一段的强化实例继续检验跨地点重分是否足够。

**更强的全局 cap 障碍。** 给前例加入未开放地点 G 和 G 私有客户，得到[六地点十客户版本](research/current/multi_facility/polytime_frontier.md#sc-k-greedy-cap-infeasible-cross-site-reassignment-need-not-restore-the-cap)。同一可达精确在轨 NE 中，B 一家设施负载 $41/2$；迁 G 后，B/E/G 各被私有 $20$ 占据，共有 $24$ 必去三者之一，故任何纯客户分配都出现普通设施 $44>2a=41$。甚至**允许跨站重分**也不能满足旧 MF-PURE-CAP-POLY 的全局初始条件。但另有精确离轨 NE 让迁入 G 的设施只获 $20$，所以坏的是这个充分证明机制，并不是 2 倍稳定性。主目标现在需要只控制偏离者、允许其他设施安全超载的修复原则，或不同的在轨选址机制。

**仍可复用的贪心信息。** [SC-K-GREEDY-MAX-MULT](research/current/multi_facility/polytime_frontier.md#sc-k-greedy-max-mult-initial-customers-choose-a-maximal-multiplicity-site) 严格证明每名顾客**最初**被分配到其可达已占地点里最终设施重数最大的一个。这从地点首开和末次加座的得分顺序得出，可用于约束不等重数的候选修复策略；严格客户改派未必保持该性质，因此还没有把它转成一般 2 倍算法。

**任意设施数的方向级推进。** [SC-K-2-E](research/current/multi_facility/uniform_two.md)在共同目录、正权原子客户和完整精确续局的模型中，对所有 $k\ge2$ 给出统一因子 2 的**存在性**；因此该精确类的最优倍率不可能随设施数无界增长。字典序最大选址同时产生客户 NE 和逐偏离预算，随后隔离超重原子、以纯改善取得偏离后的精确 NE。完整证明经不同路线内部逆审及定义级精确有限攻击，尚未外审；[范围与方向价值](research/K_FACILITY_AUDIT_2026-10-02.md)不把稳定收益倍率误称覆盖或等待时间保证。最佳统一常数在 $[\varphi,2]$，左端仅用 $k=2$ 的旧同类下界；2 的尖锐性、位长多项式构造和异构目录版本仍未解决。

**A 篇后续本轮成果。** [SC-DIAG-NORMAL / SC-OFFDIAG-FPT](research/current/shared/instance_complexity_barriers.md)证明共同目录的实例最优值和完整精确续局可完全绕开同址客户支持枚举；指数参数从最大**全部布局**交叠降为最大**不同地点**交叠 $\kappa_{\ne}$。新求解器与独立精确对照已通过。进一步在每对不同地点至多一公共客户的子类，[SC-SPARSE-3/4/5](research/current/shared/small_sparse_catalogs.md)把最多 1/2/3/4/5 地点的普遍尖锐倍率依次定为 $1,1,\sqrt2,\sqrt[3]4,\phi$；三、四地点有新固定菜单上界与匹配正有理族，五地点从已发表的六地点下界剪枝。四地点构造和证书已由独立路线交叉攻击，仍无外部审稿和完整优先权核查。单交叠的**计算可解**与五地点已逼近 $\phi$ 的**普遍下界**并不矛盾。

**A 的全局复杂度本轮突破。** [三地点全布局归约](research/current/shared/three_site_exact_hardness.md)证明每个固定有理 $1\le a<\sigma=(1+\sqrt3)/2$ 的同类判定弱 NP 完全；[五地点新归约](research/current/shared/five_site_exact_hardness.md)用中心宏客户、强制桥宏客户和完整守卫链证明每个固定有理 $1<a<\phi$ 的判定即使恰五个共同地点仍**弱 NP 完全**。结合 A 的 $\phi$ 构造，固定倍率的本类存在性判定在内部证明层有完整临界点分类。整数权输入存在伪多项式精确算法，故“弱”是实质限定，NO 间隙并非常数。旧三地点 C 私有权预算在 $a\ge\sigma$ 必为负仍是该模板的严格障碍；新构造改变了覆盖与守卫，**未**把旧三地点命题的作用域升级。两个结果的文献优先权与外部审查尚未完成；[本轮范围和价值审查](research/FIVE_SITE_AUDIT_2026-10-02.md)另记。

**A 的粒度与边界。** [原子—可拆分桥](research/current/shared/atomic_granularity.md)给 $\theta<R_{\max}$ 时的可构造实例保证 $(R_{\max}+\theta)/(R_{\max}-\theta)$，其中 $\theta$ 只计异址共有客户的最大单体权重；固定 $a>1$ 的 NO 输入因此必须含相应宏原子。三地点两种 reach 仍可能没有精确 SPE：[五客户整数反例](research/current/shared/instance_complexity_barriers.md)有 $\alpha^*=14/13$，明确界定了稀疏两 reach 定理的假设。[任意 $k$ 的局部误差引理](research/current/local_and_exact/atomic_wardrop_gap.md)有尖锐常数 $(k-1)\theta/2$，只说明任意 NE 的两设施误差常数不能直接推广到全 $k$；不构成多设施下界。可拆分模型 SPE 已属已知文献，新增粒度界的新颖性仍待核。

1. **多设施共同目录：**全 $k$ 的因子 2 存在性已由内部证明闭合；现行问题是 $[\varphi,2]$ 中的最佳统一常数、是否可位长多项式构造以及字典序选址以外的突破机制。单一三设施数值界不自动确定全 $k$ 尖锐性。详见[任务页](research/questions/three_facilities.md)。
2. **Q-SPARSE 本轮闭合：**[SPARSE-RHO-ALL](research/current/heterogeneous/sparse_unbounded_rho.md) 对双方任意长单交叠目录给出固定完整纯 NE 规则下的普遍 `ρ` 上界；原 HC-RHO 的 2×2 正整数下界属于同类，故最优普遍因子恰为 `ρ`。证明不借未取得的“至多两种重身份”候选，而是用不存在稳定布局的反设、全目录回应的高区下降和首个低区入口处的同一客户身份矛盾。已由多条独立路线审读及精确反例攻击，尚无外部同行评审或文献新颖性核定。[任务页](research/questions/sparse_catalogs.md)与[现行命题](research/current/claims.md)记录范围。

**证明依赖与剩余边界：**[SPARSE-HIGH-ACYCLIC / SPARSE-BALANCED-R](research/current/heterogeneous/sparse_high_reach_barrier.md) 对任意 `r≥1` 仍给“坏环低区必经”的独立条件性结论。新全称证明在 `r=ρ` 排除了首个高→低入口，所以无需控制低区内回返次数。旧长环仍反驳**无条件**固定短核心，但因有好稳定格，不反驳新定理。原“身份至多两种”的缺稿候选不作证明前提；新证明只在一个具体边界格强制两次交叠为**同一客户**。

**阈值以下的新障碍：**[SPARSE-BAD-LONG](research/current/heterogeneous/sparse_bad_long_cycles.md) 对每个固定 `3/2<r<ρ` 给真实没有 `r` 稳定格、却有任意长唯一全目录回应环的正有理族，且高行只用同一重客户身份。这推翻了把旧“无条件长环”简单改成“在无坏倍率稳定格下便有常数精确核心”的补救路线；但严格参数余量在 `ρ` 处消失，不触及已闭合阈值。若未来研究更低因子或精确核心复杂度，应先读此族。

**审查后的新版本：**[SPARSE-BAD-LONG-ALL](research/current/heterogeneous/sparse_bad_long_cycles.md) 用同一可实现 incidence 和明确开参数余量将上段的坏长环结论扩至每个 `1≤r<ρ`；端点 `r=1` 单独由更大倍率的反例推出。原 ID 的量词保持不变；新版本不改变 `r=ρ` 的上界，外部审查与文献新颖性仍待核。

先前多设施 55%、稀疏异构 45% 是两条旗舰命题尚开放时的历史投入建议，现已失效；下一阶段的新数学主攻需另行评估。立方成本的孤立阈值和现有求解器的小幅优化暂不重仓；只有能得到跨成本类复用的稳定性机制或新的全局复杂度分界，才重新排入主线。[路线图](research/ROADMAP.md)记载原判别关口及本轮闭合。

**实例复杂度的新前沿：**[Q-INSTANCE-COMPLEXITY](research/questions/instance_complexity.md) 的固定有理 $1\le a<\phi$ 全局判定现已由三、五地点的内部证明闭合；未来可精确研究恰三/四地点高倍率的细分类、把 $a$ 作为输入的统一复杂度，或与伪多项式算法匹配的更强参数界。不得将弱 NP 完全自动升级为强困难或固定间隙困难。研究题库并不止多设施与稀疏异构两项。

## 下一次有信息量的动作

- 多设施最佳常数分支：继续寻找不同选址机制的 $<2$ 上界或真正全局的 $>\varphi$ 下界；仅改变同一选定布局的续局不能普遍降至 2 以下。它与本轮位长多项式因子 2 构造分支是不同的证明义务。
- 多设施算法当前最值得攻击的是[至少三地点的混合重数部分交叠分量](research/current/multi_facility/polytime_frontier.md)：六客户链已强迫上升重数回返，因此要找可允许回返又保持足够偏离预算的位长多项式客户选择规则，或对贪心布局全部客户 NE 找出真正的 2 倍反例。全站共有或单站私有分量已闭合，固定布局字典序与客户势全局最小化已有有限反例，不宜原样重试。必要时只约束偏离者的离轨收益或换选址原则。另可研究局部搜索的多项式可解性；精确全局字典序优化强 NP 难不代表完整 2 倍搜索困难。
- 实例复杂度：先完成新五地点证明的外部逆审和相关博士论文的逐定理优先权核查，再决定是把其与 A 的尖锐构造合写，还是单列固定地点复杂度稿。下一项新的数学目标须另定精确 Claim；恰三/四地点高倍率分类或随输入变化的 $a$ 是候选，不能说原全局区间仍开放。
- 稀疏异构本轮的后续工作是外部独立审稿、查核文献优先权、规范纯构造实现与证书；数学全类 `ρ` 已由首个低入口矛盾闭合。若研究 `r<ρ` 的坏环核心或附加 incidence 的更小常数，须另定精确 Claim，不能把它们写作 Q-SPARSE 阈值的未解义务。

多设施与其他观察池项目仍待证；Q-SPARSE 的新内部定理须持续接受反例和外部审查。任一仍成立的致命反驳都阻止相应命题的状态提升。

## 论文编排与优先权（本轮验收）

[五路线内部审查与出版评估](research/PUBLICATION_REVIEW.md)是本轮新归约之前的出版评估：当时把共同目录尖锐 `φ` 多项式构造、异构目录尖锐 `2` 与任意长单交叠尖锐 `ρ` 组织为两条主线。新的[五地点全局困难性审查](research/FIVE_SITE_AUDIT_2026-10-02.md)改变了“只有局部复杂度”的旧判断：固定低于 `φ` 的同类判定已有完整内部分类，需重评 A 合写或独立组稿；一般异构 `2` 在命题账本中仍保持内部候选。

定向文献核查尚未取得 Simon Krogmann 2025 年博士论文 *Two-Sided Facility Location Games* 的正文（DOI `10.25932/publishup-69272`）；因此新颖性结论仍有一项具体未完成义务。完成优先权表、论文级证明终审和新英文稿后，`SIAM Journal on Discrete Mathematics` / `Algorithmica` 是有依据的投稿目标，`Mathematics of Operations Research` 是可考虑的冲刺；`SIAM Journal on Computing` 尚不能据此视为稳妥层级。此为条件性选刊判断，不是论文已可投稿或被接收的断言。
