# 本桌面精确Claim及状态

## round4 一般接续

- **B10-MIN-PI-NO-v1（独立单位审查通过）**：最小调和最优增量保底已被完整SPE反驳；首位3481、最小增量3709，W10671、OPT12546。见[审查](round4/global/review_min_pi.md)。有限窗口凹性不足；不反驳无限全局凹性、EI或half。
- **B10-ACTIVATION-UNIT-WORLD-v1（全输入合法路由；费用界OPEN）**：激活Beta2、actual I逐角色信用、单一优先级unit源及同world适应取消各有独立重构。未证多query整行或总体费用。
- **B10-NET-DYNAMIC-RANK-v1（精确表示，独立对稿通过）**：actual Hall取消rank/base/greedy、NET全价对偶及FRAC证明库存弱化合法；不推出一般可行。精确对象与审查见[本轮一般稿](round4/GENERAL_PROOF_WORKING.md)。

共同对象一律采用仓库CAG-MODEL：有限单位客户、有限非空共同目录、单位提供者、全部有序历史纯SPE；空主题、重复主题、零客户和任意历史依赖平局不被省略。改变模型的加权实参数只作代数延拓，原单位客户结论取整数参数。无外审或新颖性认证。

## Q-CAG-HALF（原身份不变，OPEN）

对每个实例、任意m>=1和每个上述完整SPE，2W>=OPT_m。所有新结果均不解决或反驳它。

## B10-CYCLIC-TERMINAL-BR-NO-v1（解析障碍，独立内审）

八主题i mod8，连续三标签块各a名客户、对径二标签块各b名客户，a,b正整数。三槽菜单Z_i=(i,i+4,i+1)的根/两尾收益为b/2+2a、b/2+3a、b+2a，末位为真正BR；静态v4=(10b+23a)/16。当9a/2<b<=25a/2时根<v4且全部尾>=v4。故根比较、尾部过线及全部列末位BR不足以推出extra-one。菜单非SPE，第二位真实偏离可盈利。依赖：逐客户均分、离散凸性静态上下界；证据与反对范围见[正文](relay_transport/last_br_threshold_menu_boundary.md)及[独审](credible_shared/review_terminal_br_menu.md)。

## B10-CYCLIC-CREDIBLE-v1（同族完整分类，root独立重构）

同一整数族的所有完整三人SPE中，首位收益最小值为b<=a时2a+b/2，b>a时5a/2+b。两段均严格大于v4；b>a时所有完整SPE均福利最优。全历史达到策略在正文给出。依赖：全部末位BR集合、第二人的真实可信阈值L=b+5a/2、旋转策略；不依赖一般EI。见[完整分类](relay_transport/cyclic_family_complete_spe.md)、[root独立审计](parent/audit_cyclic_credibility.py)。范围是本族，不是固定人数一般定理或无界人数支付。

## B10-MENU-SORT-ODD-NO-v1（无界人数模板障碍，独立重构）

环k客户，主题A_i={i-1,i}；r=2h+1,h>=1，菜单每根A_i后各h个A_(i-1)、A_(i+1)。根u=2/(h+1)，每尾比根多1/[h(h+1)]。对n>=2,k>=max(7,2(n-1))，静态v_n=2-2(n-1)/k；取k增大可使v_n/u趋h+1。即使严格收益排序也不给人数无关乘法近似。菜单末位有盈利偏离，不是SPE。精确静态上下界及证据在[正文](global_mechanism/cycle_threshold_obstruction.md)。

## B10-GAP-SUMMARY-NO-v1（无界人数归纳摘要障碍）

对每个k>=3，r=(k-1)^2+1，r个不交k客户主题。每根a列取a^k加r-k个不同非a主题。所有根收益1；每孩子F_(r-1)-P_tail=(r-1)min u_tail，但父F_r-P_root=k(k-1)>r min u_root，差k-2。任意预先固定深度的真实末尾也能补全。仅否定“孩子gap标量+根最优性(+固定末深)”闭合；这些孩子整体不是SPE。一般GAP-r仍OPEN。见[正文§2](tail_credit/gap_and_deletion_obligations.md)。

## B10-HARD-DELETE-DEFICIT-NO-v1（真实完整SPE信用障碍，独立内审）

复用旧13人、6主题、36单位客户完整SPE。对每个0<ε<=1/24，t=5/2+ε；全部真实根收益5/2<t，每个真实tail平均>=t。实际根P后删除低于t的11名尾部，根收益返还Γ=45/2而低尾总亏空11ε。因此对任意固定有限K不存在普遍Γ<=K sum(t-u)_+；同理任何在零亏空向量连续且取零的纯亏空函数都失败。t自由是承重；不反驳t绑定安全值的不同合同、分数删除或一般half。来源、守恒公式、完整DAG证据和[独审](global_mechanism/tail_credit_independent_review.md)见[正文§3–4](tail_credit/gap_and_deletion_obligations.md)。

## B10-SHARED-NEAR-TWO-v1（完整SPE压力族，独立内审）

任意m>=2,a>=1；A有ma+1客户含不同x,y，m-1个不交A外块Q_j各a客户，目录A、Q_j+x、Q_j+y。全历史恒A为SPE，W=ma+1，OPT=(2m-1)a+1；全部遗漏恰属两个极大主题，最优并集覆盖全部客户。固定m比率趋2-1/m，m无界可趋2。依赖恒A判据，已知根饱和机制明确复用，不认领新半覆盖定理。[正文](credible_shared/shared_omission_near_two.md)、[独审](mixed_menus/review_shared_family.md)。

## B10-MAX-STANDALONE-HUB-NO-v1（完整SPE规则反例，独立内审）

偶k>=12，M=C(k,k/2)，半子集核心客户与每外围M/2-1私有客户组成hub族。hub是唯一最大单独收益主题，但每个hub根末BR给3M/4<lambda3。真正两人完整SPE根选外围，末位不同外围。否定最大单独收益选择规则；不否定extra-one、Mfull或原q平均真实偏离（后者本族大于lambda3）。[正文](mixed_menus/max_standalone_hub_boundary.md)、[独审](shared_seats/hub_family_independent_review.md)。

## 候选（未提升）

- **EI**：任意合法背景b、剩r人，每份完整后缀SPE首位u>=v_(r+1)(b)。合法背景嵌入及最小r归约正确；任意菜单替代已经失败。
- **GAP-r**：同背景最优剩余利润F_r(b)与真实剩余利润P满足F_r-P<=r min u；r<=2成立，一般OPEN。上述伪菜单不反驳它。
- **P-seat-v2**：平行遗漏块每块可由合法主题实现，每主题U截面为空或恰一整块；容量阈值R>=r是否给所有后继收益>=z。r<=2已重构，一般OPEN。v1漏可实现性，r1可假，已留修订记录。

## 接续阶段精确身份

- **CA-FRACTIONAL-TAIL-WATERFILL-v1（共享已整理，核心独立内审）**：任意有限终局、背景、根、尾与t≥0，存在同一辅助分数尾权重，原高尾保1、覆盖支撑不变、正权unit密度过线；同一全客户H≤Σ(t−u_j)_+同时控制全部Q/J查询。精确守恒保留背景返还；不声称SPE继承或半覆盖。
- **B10-ENDOGENOUS-WATERFILL-SHARP-v1（完整解析族，独立内审）**：固定53客户四人完整SPE加c共同客户，真实静态v4=t0+c/4，t0=28481/2924；唯一低尾亏空D=647/8772，低尾水位根返还Γ/D趋1。原根收益始终高于阈值；不主张在最小反例类锐。
- **B10-HIGH-TAIL-FIXED-CREDIBILITY-NO-v1（精确真实SPE阻断，独立内审）**：同一族中原高尾必须保持1且查询信用≤D时，不能同时保持原完整策略，也不能让原实际叶来自任意重新选择续局的加权SPE。窄合同是承重；允许高尾同步缩权已有所有c的正修复。
- **B10-UNIFORM-CONTRACTION-INTERFACE-v1（新解析充分接口，独立内审通过）**：固定保留根背景及全目录共同核心，若同一原尾SPE在全部有序历史规定行动均避开非核心背景，则任意共同正权λ≤1保留整棵尾SPE。额外S≤a*条件给实际叶水位H≤D。条件未证明普遍，不自动让所有离轨叶同时过线。

PI已被下述完整SPE反例否定；混合弱推送、全树水位信用仍为OPEN候选，不从有限回归推断成立。新颖性、外审及一般主目标未认证/未闭合。

- **B10-VARIATIONAL-WATERFILL-v1（任意人数解析规范化，独立重构）**：t>0时最大化原支撑上的Σlog(L*/L1)+t(n−M)，有全盒KKT、原高尾保1、支撑不变、唯一客户负载与总质量、M(t)非增；同一H≤D，零权尾满足重入密度≤t，且max{H,根加背景返还}+最优势增F*+tM≤tn。主证明及审查见round2/shared与tail，状态细节以实际审查稿为准。个别负载、根信用不必随t单调；跨原叶重置的基线债务尚无总预算。
- **B10-UNIFORM-REGRET-REFUND-v1（全树解析账，独立重构）**：任意固定背景b、同一完整原单位n尾SPE及统一正质量λ≤1，新质量利润失真k_i精确非负且Σ_i k_i=背景返还；任何固定h后一直跟原σ的规定路径，全部新单步regret之和≤该同终局返还。规定边有可递推剩余税状态；反复改枝的跨终局费用没有这个免费界。unit密度regret须再除λ。

- **B10-POTENTIAL-NEXT-INCREMENT-NO-v1（完整SPE反例，独立盲审）**：三个单位玩家、六主题、430单位客户，完整43历史纯SPE实际(0,3,4)、收益(91,91,83)，W265、OPT3=324；最优调和势P1=144、P2=246、P3=329、P4=873/2，所以首位91< P4−P3=215/2。全部56/126计数与全部258含自身比较已独审，实际及六个真实根终局均达P3；全部36插入核项≤90<91，故WP在此例严格成立，较弱EI/Main均未被反驳。只否定新PI候选，序列不凹是准确失败机制。
- **B10-VARIATIONAL-SWITCH-H-ONLY-NO-v1（复用旧真实SPE的接口停界，root独立核）**：旧34客户三人完整SPE，t=真实v3=2411/246，六根强制收益≤29/3<t而所有tail≥67/6>t。每根VAR均原权1、H=F*=Γ=0，但同多重集虚拟换根严格增VAR，真实子树债务为正。故仅用ΣH支付该Debt不可能；t并非extra-one阈值，W32>3t，不反驳聚合安全值、WP或half。
- **B10-ROOT-ONLY-PRIVATE-BOUNDARY-v1（复用旧席位谱的范围延伸）**：所有正深度子局SPE且实际遗漏只在q≤m−1个全局私有块时，最后q个正深度玩家支付全部遗漏；53支架七根均有q≤2且OPT=N，故OPT≤2W−u1−u2，任意保留正深度SPE的非负兴趣类型重数均无法突破3Delta保险门槛。未运行重数锥，不宣称新一般半覆盖类。

## 一般-only接续轮

- **B10-OPTIMAL-REPLACEMENT-KERNELS-v1（全输入交换代数；独立内部解析审查通过）**：任意m≥1、任意最优m槽元组T和任意合法m槽profile B，独立Bernoulli逐槽替换给(BER)；对dp/p积分给O外H_c与O内无同槽交叠客户的Beta(a,c+1)预算。均匀配对系数C(m−a,c)/C(m,c)；固定一个相同T_j槽后可用m−1槽锚定版本。普遍性由随机替槽及最优性证明；有限Fraction审计只核实现。未给真实跨子树总支付、half或新颖性认证。
- **B10-REAL-DEVIATION-GAP-MATCH（旧弱匹配义务的本轮展开，OPEN）**：对实际路径和某个OPT元组，期望存在排列使Σ_i d_i(Tπi)≥OPT−W；CAP恒等式将其化为一次捕获流/已覆盖收益/重复比较与G共同预算。未证明此全称候选；不是对已失败遗漏匹配的修复证明。


- **B10-OWNER-EXCHANGE-POTENTIAL-v1（全部输入解析；独立重构通过）**：任意OPT元组T及分析分割Q_i⊆T_i并O，Φ_Q=ΣoutsideH_c−Σowner未cover 1/(c+1)≤0，F_Q=OPT+Φ_Q单调次模且0≤F_Q≤OPT。原单位收益精确拆成formal F边际ℓ和非负error e；同叶Σℓ=G+κ、Σe=I−κ，e是非owner插入势边际。实际-prefix matching查询每客户Σe≤(a−1)/2；最优前缀首次owner选择给≤H_a−1。分析Q不作为行动，无SPE继承或half结论。见round3/shared与relay。
- **B10-OWNER-HYBRID-TRANSPORT-v1（全部输入解析；独立对稿核查通过）**：任意合法B，全部角色子集hybrid割给A/B两份可选有理maxflow：outside原利润经O真实份额到真遗漏，outside调和份额经owner-error到missing-owner价格。actual A给G单位合法γ取消；可预先在每owner取消至多其actual G利润的R库存再补足。固定合法OPT前缀anchors可避开其全部覆盖，并为真实未来角色的联合捕获/transport提供同一whole-IC钱包。一般散布anchors仅给静态财务容量，不自动购买过去IC。不同叶兼容及动态NET未证明。
- **B10-CAPTURE-HIT-AND-SOURCE-NET-v1（全部输入一般组件；独立重构核对）**：actual-prefix递增角色均分吸收对单个遗漏客户守恒，非owner单行到达≤ρ/2；多角色集只控制曾命中。上述同一γ可使所有owner初始source费用同时≤η_i=u_i(I)+γ_i，总η=W；之后的捕获重置到达费用仍未付。HIT、源预算或协方差界均不升级为NET可行性或half定理。

- **B10-RANKWISE-COUPON-PROJECTION-v1（独立重构通过）**：逐world随机winner Hall-A/B送满G；joint正query可保留B送R路径再增广A，完整SPE下E K_R<=E K_joint−κ^-，κ^-只计owner未覆盖I的query概率。随机域与固定均值Gamma不同，不保旧delta/SOURCE，不能用随机收入代原IC。未证任一总价界；正文见round4/mixed/rankwise_joint_hall.md及round4/credible/adaptive_hall_projection.md。

## 第五轮精确身份（个人内部记录）

| 身份 | Exact statement、对象/定义/量词、假设与结论范围 | 依赖、证据、异议与状态、文件 |
|---|---|---|
| R5-IN-DIAG-v1 | 任意原CAG、任意完整有序历史纯SPE、固定ρ∈[0,1]^R。当前吸收f_q/c_q，captured总量f_q(c_q−1)/c_q只送父真叶future coverer，则全父子Σ f_g/c_B=M−H，K_in=M−H+T+COV−L，变量按正文；空源/空主题保留 | 依赖源守恒与完整actual/offhistory IC；解析和独立Fraction审查通过；T+COV−L无共同界；内部已核的精确表示，非half，外审/新颖性未认证。round5/rank/incoming_density_diagonal_ledger.md及dynamic两份审稿 |
| R5-BROADCAST-ELIM-v1 | 任意原完整σ与actual叶、任意正利润natural context，按两个真实completion的coverer差取q±。future送真实context，past送actual (j,x)券。任意非负利润注入经β=h/v递推，Σb=Σβ[J+L+P_past]=Σβ[u_actual+P_past−N_all−e]；fresh子集行质量≤k/(k+1)。零利润不接正输入，零客户/空主题按空和 | 依赖逐客户差、有限严格角色DAG及actual IC；基础核不需ell。root解析审查和独立单位回归通过，盲审范围以其实际文件为准；全树券cap1未证，负N/e不可假配actual退券。非福利定理，外审/新颖性未认证。round5/credible/all_fresh_submarkov_elimination.md、parent/review_broadcast.md、parent/audit_broadcast.py及JSON |
| R5-PB-EXTRA-v1 | 任意合法有序背景b、剩r≥2、每个完整纯SPE，前两位最终收益和≥2v_(r+1)(b)。v_k是查询抽样不被静态k−1槽对手观察的max-min。原模型及任意平局不变；若普遍成立则half | 充分归约仅用静态安全值嵌入与OPT_m≤2m v_(m+1)(0)，解析已核；候选本身OPEN，真实第二位跨主题改枝费用未付。更强2v_r与M_r阈值桥不能混同。有限阴性不作证据。round5/independent/two_block_security_reduction.md |

以上对象、假设和量词未更改Q-CAG-HALF。计算是公式/实现核验，非一般证明；没有成立的总费用结论可升级。
