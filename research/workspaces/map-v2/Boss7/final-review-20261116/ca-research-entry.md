# customer-attraction：原题、SUMmin 与完整历史编译的研究入口

Boss7，2026-11-16。本入口实读下列原题、定义、候选、反例及边的数学正文后写成；只写本文件，未执行 Git、sync、队列、公屏或 canonical 写入，未运行旧优化器、策略枚举或证书。以下“完整关系”按目标对象整条陈述判断，`contribution` 只表示其中明确的一部分。

Boss7 首次阅读的历史快照：`research/registry.json` SHA256 `202c608164e5e7f706c6178d16a0f13089c01abf7b7fdc3cc5b091370fb1f4a8`；`map/integration.json` SHA256 `135bdadeca23e9346a77097d2818dd9c005e68f7d906af6b4eae587977b141fb`。Boss3 `boss3-summin-budget-repair-d86bee169e3617da` 已在本快照正式 `done`，收据 `map/receipts/boss3-summin-budget-repair-d86bee169e3617da.json` SHA256 `6367602e636649e5ef1a53f4dcecd7f4362cbabf1cded1bf43c48930a7fbffbd`，新边及证明资产已经落盘；两条新边尚未列入上述 registry 的 `edge_files`，由 Boss 串行整合。本入口不把此前尚无新边的审读快照当作当前交付状态。

Boss5，2026-11-16 本轮最终整合补记：d86 的两条局部贡献、`boss5-summin-all-spe-3b-7383c8bf44f753cc` 的全 SPE 联合贡献，以及 `boss3-uniform-summin-identity-3b-3313f41b4a46c9dc` 的完整候选等价均已 done 并接入本轮图。上述首次阅读 SHA 和当时的“尚未列入”仅保留历史来源；当前关系及剩余义务以本入口下面的更新与 [本轮最终验收](../../Boss5/finalization-20261116/phase3-completion.md) 为准。

## 共同起点：先固定真正要证明的量词

| 实际 object ID | 当前状态 | 必读原文与准确作用 |
| --- | --- | --- |
| `CAG-MODEL` | definition | `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md`：《输入和终局量》《策略、真实续局与全部历史量词》《合法背景和剩余利润》。 |
| `Q-CAG-HALF` v2 | open | `archives/customer-attraction/state/问题/任意人数完整均衡半覆盖--问题.md`：《完整量词和目标》《净遗漏是一般付款的准确对象》。这是 **∀m≥1** 的原题身份。 |
| `customer-attraction/six-providers/exact-six-full-history-half-cover` v1 | open | `archives/customer-attraction/subarchives/six-providers/state/问题/六人完整历史半覆盖目标--问题.md`：《精确定义》《当前可确立的边界》；原根入口 `archives/customer-attraction/subarchives/six-providers/问题--问题.md`。这是 **恰六人** 的独立目标。 |

输入是有限不同单位客户、有限非空的共同**标签**目录及任意覆盖映射；保空覆盖、同覆盖异标签、重复动作、零客户与全部弱平局。完整纯策略为 \(\sigma_i:\mathcal S^{i-1}\to\mathcal S\)，每个有序在轨/离轨历史、每个合法偏离均沿**同一完整 \(\sigma\)** 在改变后的历史真实续行。相同负载的历史不必选相同后继。六人目标是每份这样的 \(\sigma\) 均满足 \(2W(\sigma)\ge\mathrm{OPT}_6\)，其中 \(W=|\cup_iS_i|=\sum_i u_i\)、\(u_i=\sum_{x\in S_i}1/c_x\)、\(\mathrm{OPT}_6=\max_{T\in\mathcal S^6}|\cup_iT_i|\)。不以比率排除零覆盖实例。

**从原题、定义和障碍独立出发的一组**，可只读本节两原题及下文“聚合末位保底已否，但没有否定 SUMmin”一节的两篇反例正文，先自行推导净遗漏接口：对最优并集 \(O\)、实际并集 \(C\)，\(R=O\setminus C\)、\(G=C\setminus O\)，half 等价于 \(|R|-|G|\le W\)。非零背景下剩余玩家利润为 \(\sum_{x:c_x>0}c_x/(b_x+c_x)\)，不能用完整覆盖代替；只验证实际叶、固定尾、计数统一策略或“存在好 SPE”均未支付原题量词。该组无需先接受 SUMmin 或任何编译候选。另两组若调用现有成果，可沿下面两条具体路线读。

## 路线一：SUMmin 的共同动态预算，再接已完整成立的静态充分链

目标对象是 `customer-attraction/e7-summin-full-common-budget-exact-discount-and-finite-tests` v2（open）。原文 `archives/customer-attraction/state/候选/全槽逐行最小价格的共同预算与有限报告--候选.md`，先读《真完整列、逐行最小与开放付款》《静态充分关系与完整槽数》《原m−1槽账与额外完整槽折扣》。固定同一 \(\sigma\) 及实际叶 \(z\)，在原 actual 前缀强制 \(A\) 后得到 \(Z_i(A)\)：保强制者和全部真实后继，恰有 \(m\) 个竞争槽。置

\[
K_i(T,A)=\sum_{x\in T}\frac1{1+c_x(Z_i(A))},\qquad
R_i(p)=\min_A\mathbb E_{T\sim p}K_i(T,A),\qquad
(U_\sigma):\ \forall p\in\Delta(\mathcal S),\ \sum_iR_i(p)\le W.
\]

**同一混合 \(p\)** 用于全部行；每行的最小动作可依 \(i,p\)，不能依已抽到的 \(T\)。纯 \(p=\delta_T\) 取 \(A=T\) 可逐行由真实 IC 付清，但 \(\min_A\mathbb E_pK\ge\mathbb E_p\min_AK\)，不能据纯点推出混合预算。候选允许某行 \(R_i>u_i\)，不是已否的逐人封顶。

完整条件边（当前 canonical，原字节被 d86 保留）：

- ID：`boss7-summin-conditionally-pays-six-half-3b-3b-17d90d43aa54c665`。
- path：`map/edges/Boss7-summin-six-half-3b-3b-17d90d43aa54c665/summin-conditionally-pays-six-half.json`；`accepted / implies / ALL / conditional / whole_result`。唯一对象源为上述一般 SUMmin 目标，终点为六人原题；没有丢掉另一个开放共同前提。
- 证明定位：同目录 `review.md`《2. 已证明的条件边》；`archives/customer-attraction/state/引理/完整槽末位最小价格的精确折扣与静态充分桥--引理.md`《完整槽的静态比较常数恰按2m计》《从未证全路径预算到half的条件推导》。

\[
M_{\rm path}=\max_p\min_{i,A}\mathbb E_pK_i(T,A)\le W/m
\quad\Longrightarrow\quad
\mathrm{OPT}_m\le2m\,v_{m+1}(0)\le2mM_{\rm path}\le2W.
\]

其中 \(v_{m+1}(0)=\max_p\min_{y\in\mathcal S^m}\mathbb E_pK(T,y)\) 是允许重复的全部合法 m 槽静态背景安全值，背景不观察查询的实际抽样。第一步由 \((U_\sigma)\)，中间静态计数、Jensen、有限 minimax 和菜单包含关系都已证明；置 \(m=6\) 即完整条件性 half。这里是 **m 个比较槽、m 个竞争槽**，系数 \(2m\)，没有 \(2m-1\) 结论。原引理《末位的精确式与一份已付款松弛》给 \(R_m=G_b-\max_A D_b^p(A)\le u_m\)；《早期位置仍缺什么》准确留下早期强制动作改变整份后继的问题。全槽折扣恒等式中的 \(\kappa_i\) 可以为负，不能把同一末位松弛给多个互斥孩子反复支出。

**这条路线真正未付的是**：一般实例、每份完整 \(\sigma\)、同一任意混合 \(p\) 的总预算；六人子域若单独付清也足以使用同一链。五份保存 \(p\) 的精确负余量、固定策略浮点客户锥及三尾子博弈都不是该全称证明。证据边界可读候选页《2617B原质量探针与本次五存p绑定》《4350B固定策略客户锥：三个不同目标》及 `archives/customer-attraction/state/程序/五人全槽行最小价格与三尾混合整数探针--程序.md`《2. 行最小搜索的完整合同》《4. 三尾 MILP 的较强任意背景问题》。当前五人 half 的别证也不能反推更强 SUMmin。

### 同一预算的另一写法与精确早期缺口

`customer-attraction/uniform-universal-time-full-prefix-menu-and-covariance-budget`（open）的均匀时间候选，与上面的 SUMmin 是同一全称预算。新边 `boss3-uniform-summin-full-budget-equivalence-3313f41b4a46c9dc`，文件 `map/edges/boss3-uniform-summin-identity-3b-3313f41b4a46c9dc/uniform-summin-equivalence.json`，为 **accepted / equivalent_to / ALL / conditional / whole_result**。固定同一原实例、完整 \(\sigma\)、actual 前缀、完整 m 槽及同一合法 p，对每个先固定的 A 有

\[
\mathbb E_{T\sim p}K_i(T,A)
=\sum_x\frac{q_x}{1+c_x(Z_i(A))},\qquad q_x=\Pr_p[x\in T].
\]

只交换有限和，然后在同一原标签目录取 min，得到逐行 \(R_i(p)=\psi_i(p)\)。两个方向保全部 m≥1、原输入和完整历史量词；空覆盖、零客户、重复行动、同覆盖异标签、历史依赖平局及零概率标签也保留。两预算都仍 open，完整等价不为其中任何一个提供初始证明；指定均匀位置权重也不等于“存在某份通用位置权重”。

两篇正文的 L 重名，使用时先作下表对应。这里另用 \(\tau\) 表示无 q 权自税；新边作者把同一量记 s，把本表 \(\Delta\) 记 τ。 对 A∼p，令 I_x=1[x∈A]、c_x=c_x(Z_i(A))；I_x=0 时带 I_x 的除式取0，I_x=1 则 c_x≥1。C_full 是独立 A,T 的完整列均价，C_old 只静态删强制槽而保真实后继；D_i 为强制者真实收益均值，κ_i=D_i−C_old，e_i=u_i−D_i≥0。

| 实际数学量 | 对应正文记号与用途 |
| --- | --- |
| \(\Delta_i=C_i^{old}-C_i^{full}=\sum_xq_x\mathbb E[I_x/(c_x(c_x+1))]\) | SUMmin 的 L、末两位资源的 R；删除强制槽到完整槽的查询折扣。 |
| \(G_i=C_i^{full}-R_i\ge0\) | 均匀时间的 L、末两位资源的 G；同一完整菜单重选防御列的收益。 |
| \(\tau_i=\sum_x\mathbb E[I_x/(c_x(c_x+1))]\) | 协方差自税，无额外 q 权重，一般不等于 \(\Delta_i\)。 |
| \(L_{BR}\) | 倒二的真实末位最佳回复比较松弛；不等于前两项。 |

准确总账是 \(\kappa_i+\Delta_i=\sum_x\mathrm{Cov}_p(I_x,(1+c_x)^{-1})+\tau_i\)。令 \(H_i=C_i^{full}-u_i\)，现役 `ca-r34-tail-reserves-pay-two-prefix-positions` 仍只为局部贡献；它与逐行身份给出 m≥2 的精确剩余：

\[
\sum_iR_i-W=\sum_{i\le m-2}H_i
-\bigl(e_{m-1}+L_{BR}+V+Q+e_m+V_m\bigr)-\sum_iG_i.
\]

因此六人路线尚须对全部原实例、完整 \(\sigma\) 和同一 p 证明前四行 H 的和不超过右侧全部储备。末两位已付不等于前四行已付；只比较末行实际列与平均列这两个选项时，可得储备为 \(\max(V_m,R_{actual})\)，不能将二者相加；完整菜单还可能提供更大储备。另一个 PF 候选的全行 Jensen 余量与 \(\sum_iG_i\) 没有已证一般顺序，不能互换付款。精确双向式、边界及符号字典在同目录 `pointwise-equivalence-audit.json` 和 `tail-route-audit.json`。

## 路线二：完整历史编译，精确识别反例的范围并支付指定输入族

这条路线有完整的策略迁移和解析子类预算；它把辅助势的可信结构变成合法客户实例，供研究者检验共同付款机制。设标签数为 \(d\)（源文用字母 p 表示标签数，此处与混合分布 p 区分）。

| 关系、实际 edge ID/path | ALL、作用范围与证据 |
| --- | --- |
| `ca-de845-mobius-inversion-with-positive-bias-compiles-full-history`；`map/edges/customer-attraction-3a-3a-de845558940d83ed/mobius-inversion-with-positive-bias-compiles-full-history.json` | `accepted / transfers / ALL / unconditional / whole_result`：`CA-MOBIUS-BOOLEAN` ⇒ `CA-MOBIUS-FULL-HISTORY-EMBED`。任意归零有理势 F、d≥n≥1，清分母反演整数 x，M=Σ\|x_B\|、K=4M+1、r_B=x_B+K；每份原完整 SPE 在每个有序历史均 fresh，每份辅助 SPE 有完整原扩展，限制投影恰为辅助 SPE 全集，非双射。 |
| `boss7-ca-756cb8-mobius-embed-all-n-aggregate`；`map/edges/customer-attraction-3a-3a-756cb80a6af99d8e/mobius-embed-all-n-aggregate.json` | `accepted / implies / ALL / unconditional / contribution`：**{`CA-MOBIUS-BOOLEAN`, `CA-MOBIUS-FULL-HISTORY-EMBED`}** ⇒ `CA-AGGREGATE-LAST-FLOOR-NO`。联合给每 n≥3 的 2n 标签、K=6M+4 正整数反族及完整 SPE，W=nθ_n−1、2W>OPT；没有提供目标合并陈述中独立的 36 客户实例，故不是 whole。 |
| `cag-609ace-fresh-embedding-pays-bias-barrier`；`map/edges/customer-attraction-3a-3a-609ace1518772a58/fresh-embedding-pays-bias-barrier.json` | `accepted / implies / ALL / unconditional / whole_result`：`CA-MOBIUS-FULL-HISTORY-EMBED` ⇒ `CA-MOBIUS-BIAS-BARRIER`，限定充分偏置 K=4M+1。所有编译根 W≥KC−M、OPT≤KC+M、2W−OPT≥KC−3M>0，C=2^d−2^(d−n)。保策略结构不保福利比。 |

证据正文依序为 `archives/customer-attraction/state/定理/子集调和势的Möbius反演--定理.md`《从子集势到真正的边际收益对象》；`archives/customer-attraction/state/定理/无重复辅助博弈的完整历史编译--定理.md`《所有重复历史上的严格支配证明》《无重复子树的等价及重复子树的扩展》；`archives/customer-attraction/state/反例/三人及以上聚合末位保底--反例.md`《从带符号势到合法单位客户的精确接口》《最坏末位背景：为什么重复历史不会降低θ_n》；`archives/customer-attraction/state/障碍/均匀客户偏置的福利与比较边界--障碍.md`《充分偏置必然使编译根远离half反例》。

M1 唯一确定 signed 类型及重复计数的调和扩张，不能任意补填重复收益。M2 的承重点是每个真实孩子 SPE 后继下 fresh−old 偏置差≥1/2，signed 差≥−2M，故充分 K 严格排除 old，再把全部重复离轨子树补齐；只把 r_B 加到正数不够。它是**完整历史**迁移，不能只验证根路径；它也明确没有把 signed 低福利比迁移成原 half 反例。

### 聚合末位保底已否，但没有否定 SUMmin

\[
\theta_n=\min_{B\in\mathcal S^{n-1}}\max_A
\sum_{x\in A}\frac1{1+h_B(x)}
\]

是 **n−1 个纯背景槽后最佳回复（背景允许重复）**；不是 SUMmin 的完整 n 槽额外查询价，也不是混合安全值 \(v_n\)。`CA-AGGREGATE-LAST-FLOOR-NO` v2（proved）的量词是 **∀n≥3，∃合法输入及至少一份完整 SPE**，使 \(W=n\theta_n-1\)；不能由该存在量词外推所有 SPE。两组势、整数反演、K=6M+4、重复背景拆分与福利界在上一表所指反例正文有自足证明。

**背景槽数不能省略。** 另一个现役开放对象 `M-8f66f1abb0374762883f01d13235901c` 要求 m 人实际游戏的 W≥mθ_(m+1)，其中 θ_(m+1) 对**恰 m 个**可重复纯背景槽取最小。它不是上面已否的 m−1 槽 W≥mθ_m；多一个背景槽使门槛不增，前者不会由后者的反例自动被否定。源为 `archives/customer-attraction/state/资源/额外槽饱和势与真实偏离分支覆盖上界--资源.md` 的“纯额外槽静态计数成立”；现役 `cag-609ace-mixed-extra-slot-pays-pure-static-comparison` 只支付 OPT_m≤2mθ_(m+1) 的静态贡献，保动态付款 remaining。该纯 θ 亦不等于混合安全值 v 或受限真实菜单值。

独立固定源 `customer-attraction/three-player-aggregate-last-floor-counterexample` v1（当前 registry 为 finite）：`archives/customer-attraction/state/反例/三人聚合末位保底--反例.md`《被否定的命题及原模型输入》《终局算术与全部历史策略》《θ_3、真正安全值及失败范围》。六标签 X/Y 各三，九个跨组 pair 各一客户、九个“两 X 两 Y”类型各三客户；完整 43 节点策略 actual z=(0,3,4)、u=(10,12,12)、W=34、θ_3=12、OPT_3=36、v_3=10。它否定 W≥3θ_3，且严格满足 half；不是一般 n 正偏置族的一个小参数点。原输入为 `archives/customer-attraction/tools/evidence/aggregate-security/original/examples/customer_attraction/aggregate_theta_failure.json`，完整证书为 `archives/customer-attraction/tools/evidence/aggregate-security/original/evidence/certificates/customer_attraction/aggregate_theta_failure.json`。

Boss3 d86 的两条**独立局部贡献**已正式整合，不能串成一般 SUMmin 的 whole：

| 当前交付 edge ID/path | 精确结论与条件 |
| --- | --- |
| `boss3-three-player-36-summin-contribution-d86bee169e3617da`；`map/edges/boss3-summin-budget-repair-d86bee169e3617da/three-player-36-summin-contribution.json` | `accepted / implies / ALL / conditional / contribution`，36 源 ⇒ SUMmin。固定上述输入及原指定完整 σ，∀同一 p，ΣR_i(p)≤57/2<34；源当前 finite，故保 conditional，固定 σ 的全 p 推导本身完整。 |
| `boss3-all-n-counterexample-summin-contribution-d86bee169e3617da`；`map/edges/boss3-summin-budget-repair-d86bee169e3617da/all-n-counterexample-summin-contribution.json` | `accepted / implies / ALL / unconditional / contribution`，`CA-AGGREGATE-LAST-FLOOR-NO` ⇒ SUMmin。每 n≥3，**仅源指定 fresh 辅助策略的任意完整原 SPE 扩展 σ**，∀同一 p，ΣR_i(p)≤nKβ_n<W=KC+n−1；β_n=(2^(2n)−2^(n−1))/(n+1)、C=2^(2n)−2^n。不是同输入全部 SPE 的现行边。 |

共同承重点可直接复用：每行取实际动作 \(S_i\)，则 \(Z_i(S_i)=z\)，故对同一 p 有 \(\sum_iR_i(p)\le m\mathbb E_pK(T,z)\)。36 例六查询价为 \((20/3,35/4,35/4,22/3,22/3,19/2)\)，给 \(3\max K=57/2\)。d86 指定策略族对未用查询 signed 边际为 \(F(Z\cup\{a\})-F(Z)=0\)，已用查询价严格更小，因此 \(\max_aK(a,z)=K\beta_n\)；\(\delta_n=C-n\beta_n>n\) 保证严格裕量 \(K\delta_n+n-1\)。这个最大价等号不是 \(\max_p\sum_iR_i\) 的最优值声明。完整证明定位在 d86 同目录 `comparison-review.json` 的 `shared_row_argument`、`three_player_36_proof`、`all_n_positive_compilation_proof`；一般族另有 `all-n-budget-proof.json` 的 `analytic_budget_proof` 与 `tightening_discovered_in_this_reconstruction`。

**这条路线真正留下的义务**：充分偏置已保证其根严格 half，继续用相同充分偏置无法把 signed 福利坏点变成原题反例；其他合法化机制若用于反例，须另证全部原历史 IC 与实际福利失真。若用于正面付款，上述实际动作列目前只在明确输入族被证明足够小，仍需一般输入、一般完整 σ 的共同金额。不能再把已否 W≥nθ_n 当作一般引理，亦不能由反例族满足 SUMmin 推出一般 SUMmin。

### 原正编译族的全部完整 SPE 已支付

新边 `boss5-all-spe-summin-budget-7383c8bf44f753cc`，文件 `map/edges/boss5-summin-all-spe-3b-7383c8bf44f753cc/all-spe-summin-budget.json`，为 **accepted / implies / ALL / unconditional / contribution**，共同前提为 **{`CA-AGGREGATE-LAST-FLOOR-NO`, `CA-MOBIUS-FULL-HISTORY-EMBED`}**。对每个 n≥3，它把完全相同原输入 \(K=6M+4\) 的策略量词扩大到**每份完整原纯 SPE**；旧 d86 指定策略边和资产保持原样。

M2 的实际严格比较在较大 K 上为 \(K/2-2M=M+2>0\)，逆向归纳覆盖所有有序历史，包括此前已经重复的离轨历史。比较两个孩子时只分别置换均匀偏置，signed 两个真实终局不置换。因此每份 \(\sigma\) 的 actual n 标签互异，不能再假定都等于旧展示路径。任意这样的集合 Z 都有

\[
W\ge KC+n-1,\qquad
\max_a Q_a(z)=K\beta_n-F(Z),\qquad F(Z)\in\{0,1\}.
\]

未用查询的 signed 价由 Boolean 势差给 \(-F(Z)\)；已用查询产生重复计数，只用 signed 绝对值界，不能套 Boolean 势差。于是每份完整 \(\sigma\)、每个同一合法 p 都满足

\[
\sum_iR_i(p)\le n\mathbb E_pQ_T(z)
\le n[K\beta_n-F(Z)]\le nK\beta_n<W,
\]

统一余量至少 \(K(C-n\beta_n)+n-1>0\)。两份独立解析附件为 `full-history-parameter-proof.json` 与 `all-spe-query-budget-proof.json`；较粗的 \(W\ge KC-M\)、\(\sum R_i\le n(K\beta_n+M)\) 也独立闭合。该结果只支付这个明确原输入族的全部策略，不支付其它输入、其它 F/K 或 36 客户的任意其它 SPE，更不把一般 SUMmin 或六人 half 标成 proved。

## 使用本入口时的最后边界

一般 SUMmin、无条件六人 half 和任意人数 Q-CAG-HALF 都保持 open。完整的条件 whole 边可以复用，不等于其开放前提已付；具体反族的全 p 解析预算可以复用，不等于一般目标 whole。以上三组是阅读与数学入口，不是新建研究任务或声称关闭原题。Boss7 原 `cag-joint-review.md`、`summin-36-budget-review.md`、`summin-alln-budget-review.md` 可辅助交叉核对；本入口关于当前关系的结论以列出的实际边、原定义和精确量词为准。
