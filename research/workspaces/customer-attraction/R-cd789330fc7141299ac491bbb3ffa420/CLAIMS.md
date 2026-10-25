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
| R5-PB-EXTRA-v1 | 任意合法有序背景b、剩r≥2、每个完整纯SPE，前两位最终收益和≥2v_(r+1)(b)。v_k是查询抽样不被静态k−1槽对手观察的max-min。原模型及任意平局不变；若普遍成立则half | 充分归约仅用静态安全值嵌入与OPT_m≤2m v_(m+1)(0)，解析已核；候选任意合法背景版本随后被R5-PB-EXTRA-NO-v1反驳；原条件归约保留。更强2v_r与M_r阈值桥不能混同。有限阴性不作证据。round5/independent/two_block_security_reduction.md |

以上对象、假设和量词未更改Q-CAG-HALF。计算是公式/实现核验，非一般证明；没有成立的总费用结论可升级。


## R5-PB-EXTRA-NO-v1（反驳R5-PB-EXTRA-v1的任意合法背景量词）

- Exact Statement：存在原CAG的有限单位客户、有限非空共同目录、合法有序singleton前缀b、剩r=2475和一份包含全部有序历史的完整纯SPE，使其前两位最终利润和严格小于2v_(r+1)(b)。
- Objects / Domain / Quantifiers：客户、提供者均单位；目录含分段Cartesian regular和每客户singleton；背景通过同一目录合法前缀实现；静态r槽对手不观察查询。
- Assumptions / Definitions：k=3,d=20,q=12,t=10,Q=2063,H=100000,M=10^9；real块q−1名客户背景M、一名M+1，dummy块Hq名背景HM。f(c)=(q−1)/(M+c)+1/(M+c+1)，g(c)=Hq/(HM+c)。所有整数与动作规则见唯一正文。
- Conclusion / Scope：前三人各u=dkf(k)，独立查询保证s=d[f(1+rk/Q)+(k−1)g(r+1)]>u；故PB-extra任意合法背景版本FALSE。其强2v_r版本亦随之失败；不反驳原half、根在轨弱版本或全局m阈值floor。
- Dependencies：全部历史Greedy水位、Fill/Copy/Punish自身IC、singleton严格劣势及BI子树补全；逐客户凸倒数Jensen；(G)(P)(F)及容量严格条件。
- Evidence：自足全历史解析构造；root独立重构/参数Fraction重算；credible独审通过；dynamic先盲重构后对稿审查Greedy/Punish全历史部分通过，静态Jensen由root与credible另审通过。标量检查不替代全树证明。
- Counterevidence / Objections：当前内部攻击未发现fatal。背景已覆盖N，未证根实际到达；不得扩大范围。routing只提供威胁结构启发，未直接导入其PoA结论。
- Status：完整解析反例及内部审查，外审和全球新颖性未认证。原Q-CAG-HALF仍OPEN；R5-PB-EXTRA-v1原陈述不改量词，只将其状态改为refuted。
- Related Files：round5/menu/pair_attack.md、pair_background_scalar_audit.py及JSON；round5/parent/review_pair_counterexample.md、audit_pair_parameters.py及JSON；round5/credible/review_pair_counterexample.md；round5/dynamic/review_pair_counterexample*.md。

广播基础组件后续审查补充：round5/independent/review_broadcast.md先盲重构后对稿；真正非零fresh审计使用非最优比较(D,H,B)，不声称覆盖最优owner初始化。局部负荷递增只对同一客户，单谱系不重叠只指过去差异区间；这些都不推出全树actual券cap1。


## 第六轮一般组件：非福利付款

- **B10-SAFE-ACTUAL-ROW-NET-v1**：全客户context的N+e在[0,u_i]，可在βu_i当前整行统一退款；past正券原actual标签保留。credible发现，root/shared独立重构。净券非负，cap未证。[正文](round6/credible/safe_coupon_netting.md)。
- **B10-PROFIT-CLIP-v1**：删原正边总c≤min(P,N+e)并将当前净支付增c合法；最大剪枝当前min(v,u_i)、外送(v−u_i)+，κ=h/max(v,u_i)。新正load≤旧gross，未必≤旧net。credible提出，shared/mixed/root重构；无费用改善或cap结论。
- **B10-FRESH-PROFIT-NORMALIZATION-v1**：仅fresh利润nu归一化，正后继nu>0，sub-Markov角色DAG闭合；nu−P=d_F−N=u_i−Y−N−e>0可安全净成actual整行券，无past或正off-C迁移。relay发现，credible/root重构；beta可能增，旧SOURCE/HIT不自动继承，未用ell及未付容量。[正文](round6/relay/fresh_profit_normalization.md)。
- **B10-CREDIBLE-ADJACENT-TRANSPOSITION-v1**：一般背景、固定AB尾SPE，收益(alpha,beta)。AB可实现iff alpha≥mu、beta≥mu_A；BA iff beta≥mu、alpha≥mu_B。增序且alpha≥mu_B可保终局负载换位，严格祖先完成叶/IC保持；lex最大固定half坏计数的相邻升序必被mu_B>alpha阻断。global提出，mixed/root重构；未付阈值障碍，不保菜单坏性。[正文](round6/global/credible_adjacent_transposition.md)。

以上对原全部输入有效，但均为结构/表示组件；主目标OPEN。定义级回归不提升一般福利证据，无外审/新颖性认证。[root审查](round6/parent/review_general_components.md)。

- **B10-ALL-CONTEXT-COUPON-ROLE-HIT-v1**：SAFE净券图、fresh变体、CLIP子核及各自合法OPT-owner初始化，对任意k角色集K有A(K)≤M(K)+k/(k+1)M(K外)。跨全部context/客户，但只约束角色终端质量，不是actual钱包上界。relay提出，credible/root独立重构；root的uniform-subset行表示与角色价层积分为派生工具。见[派生稿](round6/parent/role_price_envelope.md)，原HIT正文在round6/relay。主目标仍OPEN。

## 第七轮精确身份（均非一般福利结论）

- **B10-FRESH-SOURCE-ORDER-v1**：固定合法全客户 SAFE/CLIP 图、任意有限 actual-prefix fresh 源，源 owner k 的最终实际角色 j≥k；以 h_k(K)=|K∩[k,m]| 得 A(K)≤M(K)+Σ_(k∉K)h_k/(1+h_k)M_k，含前缀 cut 与非增价格推论。全 O 初始化不适用。已有 causal interval/HIT 的综合，不认领新机制；coupling证明，root/credible 独立重构通过。[正文](round7/coupling/fresh_source_order_and_suffix_hits.md)。
- **B10-JOINT-PREFIX-PUSHBACK-v1**：任意两个合法完整叶 B/W 在 i 前行动相同，对同一 W 的全部 prefix 完整利润系数 λ_j∈[0,L]，存在明确非负矩阵将 Σ_(j<i)λ_jp_j(W) 精确写成 Σ_lκ_lp_l(B)，且 κ_l∈[0,L]；矩阵各列和≤1。零利润取零系数。只针对一份 W；已有 suffix 或多个 W 的 claim 不免费叠加。credible证明，coupling/independent/root分别重构通过；§3非减价格与后缀利润推论由金额只前送及列界直接推出。[正文](round7/credible/joint_prefix_claim_pushback.md)。
- **B10-FIXED-PARENT-SD-TRANSPORT-v1**：任意参考完整叶 Z、另一固定叶 B，S_i=Z_i，d_i=c_B+1−1_Bi。q^B_il=Σ_(x∈S_i∩(B_l\S_l),i≠l)1/(c_Z d_i) 的同一矩阵满足 Σ_l q^B_il≤u_i(Z)，Σ_i q^B_il≤u_l(B;(C_Z∩B_l)\S_l)。行系数≤L 时共同列系数≤L，可与不交客户支持的既有密度合并；不含 direct B 或未来 W 响应项。coupling提出，root/independent独立重构通过。[正文](round7/coupling/fixed_parent_static_column_capacity.md)。
- **B10-REVERSE-SD-KEEP-B-v1**：固定 reference Z 与真 natural context，SD 有 u_i=v+P_B+P_W−N_B−N_W−ell，ell≥0。ROW 给 r=u_i−P_B≥0，可保留全部 B 正边，当前送 min(v,r)≤v，仅 W 正边保留总额(r−v)_+≤P_W，精确非负守恒。方向 actual→off 利润；B 目标域须按 last-forced/query/prescribed 分类合法化。没有 PRICE/HIT、循环吸收或 actual cap。root推导，coupling/global独立解析确认。[正文及root核查](round7/parent/reverse_sd_and_joint_review.md)。

SD/query-projection 是合法表示，完整说明在 global/coupling；COMMON-CAP 的 per-client 交集运输只付同一 B/W 的共同覆盖部分。所有本轮 finite audits 只核定义和明确候选，不证明上述一般定理或 half；一般关系由解析证明承担。内审通过不等于外审，新颖性未认证。主目标始终 OPEN。

- **B10-OPT-COORDINATE-INIT-v1**：每个原实例/完整SPE实际叶B、每个比较m元组T，对 x∈T_i 的份额p_ix=1/cT(x)存在显式非负分解p_ix=P^B_ix+c_ix+Σ_j>i a_ijx，保留原future正边容量；current_i=Σc_ix=min(r_i,u_i)≤u_i，r_ix=p_ix−P^B_ix≥0，future总额(r_i−u_i)_+；所有实际B列Σ_iP^B_i,l≤u_l(B;(O∩B_l)\T_l)。关键一步Σ(r_ix−P^W_ix)_+≤u_i(W_i)≤u_i只在求和后用一次wholeIC，无客户重权。root推导，global/coupling按陈述独立重构通过。库存标签不要求被当前付款actual角色覆盖；与actual客户券不同。[正文](round7/parent/optimal_coordinate_initialization.md)。
- **B10-OPT-COORDINATE-RESIDUAL-v1**（OPEN充分候选，非上述引理结论）：每个原实例与完整SPE是否存在最优T及允许的坐标剪枝/SAFE或CLIP选择，使仅future源的终端金额Aout_l≤2u_l−current_l−Bcol_l对全部角色同时成立。右边已证非负；若此候选成立则half。没有声称任意固定T/路由满足。真future初始化及严格角色DAG合法，剩余共同容量仍未证。

## 第八轮已恢复的旧反例：状态纠正

强FOMA-EXISTS与FOMA-ALL均 refuted，旧精确身份 B10-STATIC-OPTIMAL-ASSIGNMENT-NO-v1，来源 R-a0bb57fa24044a8794bc7991918a19c6/static_matching/optimal_static_matching_counterexample.md。第七轮漏读旧资产、标为OPEN是本桌面状态错误。root独立代码与新冻结重放在round8/parent，确认52单位客户、m4、actual3322、W47、OPT52唯一支持0145，24匹配最小48。同行R-105的新1953客户证明是另一条独立分离，本桌面未冒称其完整复审。弱K≤(1+1/m)W与原目标仍OPEN。静态公式不因候选失败而失效。

## 第八轮：来源保持密度与一般支付接口

- **B10-COORDINATE-INIT-DENSITY-v1**：原round7任意比较元组T初始化可将每条future子容量进一步裁为min(1/cT,1/d_ix)/cWi，而保留同一current_i=min(r_i,u_i)、future_i=(r_i−u_i)+与全部H不变。逐客户(r−qhat)+≤1/cWi，求和后只用一次wholeIC；每个初始目标密度≤p_ix。inventory证明，independent/root分别重构通过。[正文](round8/inventory/source_preserving_density_envelope.md)。
- **B10-SOURCE-PRESERVING-DENSITY-ONE-v1**：采用上述初始化及保持同客户的正coverer-difference核，所有非actual natural context的f_tx=cVt(x)h_tx≤p_kx+Σ_(i<k)a_ix≤1，k为history首实际分歧位置。全部父节点为同一角色k、同源同客户质量是角色反链，所以允许真实合流。actual-prefix目标只作终端，不纳入密度声明。全图不重采客户，L_s≤D_s≤u_i及非负退款只用一次完整IC。一般角色汇总cap未证。inventory证明，independent按合同盲重构后对稿、root另核通过；无外审/新颖性认证。
- **B10-COMMON-COVERER-CHOICE-v1**：先用同行I互补付款，R-only流中保留全部新coverer正边h/cA，允许每个共同future coverer增加[0,h/cA]子边；所有选择均保持库存、密度≤1、wholeIC及future DAG。原current只下降；新future密度贡献≤父h，反链证明保持。全共同角点为旧round3均分flow，不认领新核。root提出，inventory/residual及independent分别确认。[root重构](round8/parent/density_reconstruction_and_common_edges.md)。

以上解决客户身份能否合法穿过未来IC的支持问题，不解决同角色所有contexts的总付款。原fullSAFE/CLIP受限RESIDUAL-CAP没有因此被证明，也不能把新客户核称旧核的删边。

- **B10-TERMINAL-FROZEN-WALLET-v1**：任意实际末两位p,m、此前背景b，A=B_p，a=u_p，v=u_m，L_A=Σ_A1/(b_x+2)，C'_p=min(a,v)−L_A≥0且≤min(a,v)/2。对任意给这两位分配的目录主题，末两行冻结成本总额≤a+v+C'_p；自足精确恒等式另保真末位BR和根IC非负credits，早期总税未付。matching推导，root独立以w(P)−γ(P∩Q)重构CROSS与钱包；独立固定证书代码核全部IC/等式。复用两人共同目录对称交集机制，无外审/新颖性认证。[正文](round8/matching/terminal_frozen_regret_wallet.md)。

query凸包付款、全选择族LP/价格DP及sibling Hessian只按各自正文标为接口/精确身份；尚无新的一般福利付款。有限阴性或纯policy几何例不作SPE/half反例。

- **B10-SOURCE-PRESERVING-PAYMENT-CERTIFICATE-v1**（条件充分接口）：固定原实例、完整SPE与任意比较T，round8/residual/linear_joint_payment_certificate.md的INIT/I-PAY/R-FLOW/ROLE有限线性系统任一可行点都给同一份|O|库存的合法actual两预算付款，故|O|≤2W。数据取同一σ全部有序history，不重命名旧query叶；source current可非极大，共同future用edge z变量保持线性。对最优T的一般存在可行性仍OPEN，未称原目标等价。root提出合成，residual独立展开，root另核质量与域；无外审/新颖性认领。

independent v2/v3在同一固定packet改变已证允许的初始化/共同边选项，激活interlayer但未出现merger。没有从有限通过提升一般role cap；f≤1及wholeIC由解析证明承担。

- **B10-MULTIQUERY-SOURCE-DENSITY-v1**（独立辅助身份）：固定任意完整纯policy及actual叶、有限actual-prefix query sources（同owner可多query），每客户Σp≤1、初始future总量≤p、每初始future边≤p/c_W。则同客户difference/common边家族所有非actual targets密度≤1。actual-prefix/past出口仅终止；不证明初始资金。图/密度不需SPE，wholeIC付款才需原IC。root提出合同，residual证明于primal§4，inventory/independent分别审查通过，不改变Q-CAG-HALF。

共同付款primal双独审见round8/inventory/payment_primal_review.md、round8/independent/linear_joint_payment_review.md；一般ROLE可行性仍OPEN。


## 第九轮精确身份（个人资产，非共享canonical提升）

- **B10-HARMONIC-TERMINAL-WALLET-v1**：任意m≥2、任意共同目录、每份完整纯SPE，按实际末对定义C′=min(u_(m−1),u_m)−Σ_(x∈B_(m−1))1/(k_x+2)，有(2H_m+1)C′≤W。完整解析证明、menu/credible/root独立重构及旧packet实现核对。只支付末对一项，早期冻结差未付；无外审/新颖性认证。正文[round9](round9/exchange/harmonic_terminal_wallet.md)。
- **B10-VARIABLE-COORDINATE-OWNERSHIP-v1**：固定T，full-O坐标付款证书可把p_ix变为支持T_i且逐客户和1的变量，H/r及全部边界线性；p_ix k_ix≤1区域每点均可初始化。扩大证书仍只有ROLE可行⇒half。R任意owner分割早有旧来源，不认领首次。正文[所有权](round9/payment/roleobstruction/fractional_ownership_extension.md)。
- **B10-ALL-FUTURE-COVERER-PAYMENT-v1**：原R-only自然图上全部真实future coverer边可取0≤z≤h/c_A、L=h−Σz、0≤L≤c_Vh/c_A；全图密度/一次wholeIC/质量守恒同时保持，含旧正边与NET、可把必要净流改送共同coverer。局部允许域可严格扩大，不声称新SPE可付范围。root证明、menu/payment独立重构及menu事后全文核查。正文[边族](round9/parent/all_future_coverer_payment_family.md)。
- **B10-SOURCE-PRESERVING-ROW-CLIP-v1**：上述edge caps及同客户守恒可配单contextΣ_xL_tx≤u_i（或β_*u_i）；uniform可行后在整行退款内取消同客户边，密度保持。旧scalarCLIP在客户保留边界上的合成表示；不同context总和仍未付；不将可分客户DP迁移到此联合行。正文同上§6；无新颖性声明。
- **B10-OPTIMAL-EXCHANGE-CURVE-v1**：最优T与任意合法m槽S逐客户负载(k,c)，对每t∈[0,1]有Σ_E[1−(1−t)^c]≤Σ_OPT t^k(1−t)^c binom(m−c,k)/binom(m,k)，及固定槽数/调和积分式。完整静态证明，exchange/root独立核；不使用SPE、不支付遗漏、无half界。正文[交换曲线](round9/global/optimal_exchange_curve.md)。
- **B10-ARBITRARY-BACKGROUND-PUSHFORWARD-NO-v1**：任意合法背景全称版本WP、SELF及完整真实菜单Mfull≤u均已被旧round5 PB构造否定；此是旧证据直接后果，非新游戏。空背景SELF另早有旧34客户反例，本轮单位客户独立重放；空背景弱WP/自由Mfull及actual-prefix专用桥仍OPEN。正文[域纠正](round9/parent/background_pushforward_status_correction.md)、[旧SELF恢复](round9/credible/root_covariance_and_background_domains.md)。

Q-CAG-HALF仍OPEN；扩张ROLE、弱K≤(1+1/m)W、根实际全路径聚合支付均未证。本轮所有新项没有外审和新颖性认证。


## 第十轮精确状态：原目标仍OPEN

- **B10-STRONG-ADJACENT-WALLET-NO-v1（proved counterexample, internally checked）**：原模型完整SPE不保证Σ_i max_T u_i(T,Z_−i)−W≤C_adj，亦不保证每个最优指派可由同一C_adj支付。10单位客户m3实例W9、OPT10、冻结regret2、C_adj1；全部21有序历史已分别独立核查。先有巨大m5原型，后有exchange独立紧凑构造，均保留原证据。[自足正文](round10/exchange/compact_adjacent_wallet_counterexample.md)。这是辅助桥反例，非HALF反例。
- **B10-OPTIMAL-ADJACENT-WALLET-NO-v1（complete analytic family, internally checked）**：每m≥2有单位客户共同目录完整SPE，W=m²、OPT=m²+m−1，唯一最优支持，C_adj1，所有最优元组/排列的最小冻结Q满足Q−W=(m−4)/2。故存在最优元组+指派的C_adj桥从m≥7起失败；任意固定α倍同样失败。tree/netglobal盲合同独立推导通过；有限count-prefixQA只核实现，不证明全m。[正文](round10/parent/optimal_assignment_adjacent_wallet_counterfamily.md)。不否定较宽旧弱K≤(1+1/m)W或half；m5单族过线不能作一般定理。
- **B10-ALPHA-ONE-ACTUAL-TAX-RECOVERY-v1（old evidence consequence）**：旧13人实例同一actual表给α1实际负载银行与common-query frozen总价两桥均正差37/66；已核准确槽数/实际c分布。是旧refined-tax后果，不认领新反例。[算术与原来源](round10/security/old13_alpha_one_tax_arithmetic.md)。只否定全部查询加强，真正安全最优查询/有利最优指派仍未被该证据否定。

本轮静态终端吸收、arrival rent、退款重组只是准确等式/组件，未给早期共同付款；不提升Q-CAG-HALF或一般五人half状态。所有新项外审/新颖性未认证。

- **B10-ROOT-STANDALONE-ROW-HELPER-NO-v1（exact complete-SPE counterexample, internally checked）**：即使q=m，root query row≥O−max|S|也不普遍成立。m6、10单位客户、6不交主题大小(3,3,1,1,1,1)，完整BI策略W6、OPT10、root row6、maxsize3。root/direct两套独立实现核全部9331有序节点/55986含自身IC，净ROW及HALF均未失败。也否定W≥OPT−max|S|的简单加性加强。[原始定义/证据](round10/parent/root_standalone_row_helper_counterexample.md)。有限完整证书用于反驳全称加强，不作一般正面证据。无新游戏结构新颖性声明。

## 第十一轮：一般共享负载接口及准确停界

原Q-CAG-HALF仍OPEN；本轮无新无条件福利界或目标反例。以下为个人阶段身份，不自动作共享canonical提升；外审、新颖性均未认证。

- **B10-SHARED-CONVEX-MENU-CAP-v1（OPEN充分候选）**：对每份原完整SPE、每个查询p，是否 min_(L∈K)Σρ_x/(1+L_x)≤W/m，其中K=(1/m)Σ_i conv{actual-prefix强制B后删当前槽的真实负载}。凸minimax及既有静态关系给条件OPT≤(2−1/m)W，m5仅条件9W/5。[合同](round11/parent/shared_load_bregman_working.md)、[独审](round11/tree/shared_load_independent_review.md)。
- **B10-SHARED-VARIANCE-BALANCE-v1（全输入凸性/恒等式，内审）**：共享平均负载保留明确非负Jensen余量；最优负载处W−mF=ΣIC−C+D，D≥0，KKT另给非负去相关gap。纯查询可由原IC支付；混合C仍未付。只是表示/充分接口，非新金额。[VAR及纯查询](round11/aggregate/shared_load_components_and_exact_sign_boundary.md)、[root稿](round11/parent/shared_load_bregman_working.md)；tree/aggregate独立检查域与符号。
- **B10-SHARED-SADDLE-ZERO-C-NO-v1（旧完整SPE的新精确后果，内审）**：旧16单位客户m6保险族有唯一全局shared primal最优L*；任意最优saddle查询仅支持nonanchor主题，逐行C在这些主题恒定。因此任意saddle及保持查询边际的角色运输均有C=135/242>0。正确付款仍D=2017/1210、ΣIC=4/5、W−6γ=21/11>0，不否定SHARED或half。[解析与原来源](round11/aggregate/shared_load_components_and_exact_sign_boundary.md)、[独审](round11/matching/insurance_saddle_independent_review.md)、[root单位客户复核](round11/parent/shared_insurance_literal_independent.json)。全历史SPE继承原证明，180菜单审计不是新全树枚举。
- **B10-CROSS-ROLE-OPTIMAL-GATE-v1（静态全输入关系，内审）**：取全局最小冻结成本最优tuple/assignment。对等势最优槽I与actual角色J，若换为B_J净覆盖损失δ0，则Σ_I f_i(T_i)≤Σ_Ju_j−max_配对ΣR_ij，R_ij=Σ_(B_j\B_i)1/[c(c+1)]。只要求覆盖数仍最优，不要求同一最优并集；正δ未付。[证明](round11/matching/cross_role_optimal_exchange.md)、[独审](round11/geometry/matching_displacement_gate_review.md)。旧52/1953有限QA只核定义，不作动态half推进。
- **B10-EXTRA-LOCAL-FRAC-NO-v1（旧PB索引后果）**：任意合法背景的逐步u+(r−1)δ_r(b+S)≥rδ_(r+1)(b)被旧PB同一完整策略严格否定；背景和SPE继承原证明，本轮核新saddle及热负载恢复。该输入总新玩家效用仍超过rδ_(r+1)，聚合与零根目标保留OPEN。[正文](round11/aggregate/extra_fractional_local_plateau.md)、[root标量复核](round11/parent/extra_local_scalar_independent.json)。
- **B10-OPTIMAL-FRESH-RESERVE-v1（OPEN充分候选）**：最优m主题组中是否存在K0=Σ_jΣ_(x∈T_j)1/(1+c_x)≤W+J，J=Σ_actual1/(1+c_x)。静态OPT≤K0+W−J成立；SPE付款未证。区别于已败所有查询max税。有限旧输入/锥未分离不提升真值。[合同](round11/geometry/optimal_fresh_self_reserve_working.md)。

terminal余量、可信endpoint、same-p互补银行和fixed-t切线游戏均保存准确未付项；没有half新界。前缀harmonic kernel已去重至R-7eb旧稿。原净ROW/SUMROW、宽冻结指派、安全聚合及ROLE仍未闭合。见[本轮稿](round11/GENERAL_PROOF_WORKING.md)。

- **B10-SHARED-HALF-CAP-v1（OPEN、较弱充分候选）**：同一shared minimax值γ是否有W≥(m−1/2)γ。它仅需C≤D+ΣIC+γ/2，已足原half，不要求强SHARED的锐2−1/m。γ/2是目标容许余量，未给资金。m5需(9/2)γ≤W，未无条件成立。原强候选身份保留，不能以此重新命名为已证。

## 第十二轮个人阶段身份

原HALF与m5仍OPEN，无新无条件福利界/目标反例；外审、新颖性未认证。

- **B10-MEAN-CAP-SHADOW-CREDIT-v1**：全行均值cap分析域保留原source，μ_i≥0、η_i自由给G=Σμ_i I_i+ΣE R_i≥Σμ_i I_i。均值cap不是纯重选，无μ_i u_i额外钱包。[正文](round12/tree/mean_cap_credible_shadow_working.md)、[独审](round12/credible/mean_cap_weighted_credit_review.md)。
- **B10-ALIGNED-CREDIBLE-FIXPOINT-v1**：Kakutani给query/background边际、max-price支持和future折扣一致的固定点；非minimax、小γ或原纯SPE，不免费叠global版G。[正文](round12/tree/aligned_credible_menu_fixedpoint.md)、[独审](round12/credible/aligned_fixedpoint_review.md)。
- **B10-FULL-SLOT-NORM-BANK-v1**：full负载/原deleted source有W−mγ+=Σ(1+μ_i)I_i+R+D0−Cov0+m||ρt||²。插入税/曲率抵消成范数项，Cov未付。[正文](round12/aggregate/full_slot_cap_dual_norm_bank.md)、[独审](round12/tree/full_slot_norm_independent_review.md)。
- **B10-CANONICAL-FLOOR-RESET-PRICE-v1**：旧min-pasting给有序FLOOR-IFF。raw均值floor分析域λ_h≥0定价允许reset，source slack非负；固定actual标签须保例外。[域审查](round12/tree/reset_floor_domain_independent_check.md)、[独审](round12/credible/mean_floor_reset_review.md)。
- **B10-UNIFORM-NET-CAP-v1**：B_i=d_i−Σ_future(u−M)，一份总约束ΣE B_i≤W给共同μ、G=μ(I_total+S_total)+R。辅助路径非SPE；真copy消去root/current变化，前缀损失未付。[正文](round12/parent/net_cap_bubble_component.md)。
- **B10-HALF-REDUCED-COST-FLOW-v1**：同row非负行动平衡first-follower流满足μΣθ(d−v)≤½Σθr(source)。还须原source逐原子容量才可用半份R，不控制边正部和，实际Cov流平衡未证。[证明](round12/credible/uniform_copy_swap_component.md)、[独审](round12/tree/uniform_swap_and_raw_flow_independent_review.md)。
- **B10-ACTUAL-PREFIX-BUBBLE-v1**：raw(h_i,A,b_i,Y)真尾SPE可换成下一actual行(h_i,b_i,A,Y)的child SPE，删除query背景/利润相同，净cost差=M(h_i,A)−u_b。真原first-follower强制尾时差=Γ−source slack。下一row cap/原σ一致性与多源容量未保证。[正文及QA](round12/parent/net_cap_bubble_component.md)。tree/credible独立解析通过，有限QA非一般half证据。

同端点真/几何重放的总adaptive work相同，仅真边有原Γ；fixed F/B/r signed工作一次望远镜，不付款任意target余项。[真重放](round12/tree/real_replay_covariance_flow.md)、[几何重放](round12/geometry/conservative_raw_tail_replay.md)。

- **B10-ACTUAL-LOAD-TANGENT-PAY-v1（OPEN充分候选）**：coherent shared KKT下，若C≤D+I+(m−1)/(2m)Σρt²c，则实际银行的KKT上界≤γ/2足half。未有r_beta/reset到该银行的真实映射；不是通用PSD passivity结果。[最后稿](round12/direct/GENERAL_PROOF_WORKING.md)。


最新本对话用户指定五人专项，客户/目录任意；一般目标仍OPEN。见[round13](round13/README.md)及[精确范围](round13/CLAIMS.md)。
