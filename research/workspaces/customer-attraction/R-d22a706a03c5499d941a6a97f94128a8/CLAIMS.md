# 本桌面的精确 Claim

## Q-CAG-HALF

精确模型、量词和目标均按 [主目标](../../../questions/customer_attraction_half_coverage.md)。本轮状态 **OPEN**；没有一般证明或目标反例。

## B10-UNIQUE-OPTIMUM-OMISSION-OBSTRUCTION-v1

- **Exact Statement / Conclusion：** 存在二人、六个两两不同主题、71名单位客户的合法共同目录游戏及完整历史纯 SPE，其实际覆盖 C 的 W=35；唯一最优无序二主题组合的并集 O 满足 |O|=OPT₂=38，|O∩C|=2，|O\C|=36>35。故“每个实例每个纯 SPE 存在最优 O 使 |O\C|≤W”是假。
- **Objects / Domain / Quantifiers：** 存在性反例，m=2；一般主模型允许的单位客户、共同目录、完整全部有序历史策略。最优组合允许重复；唯一性按无序主题多重集，不排除两个有序排列。
- **Assumptions / Definitions：** [CAG-MODEL](../../../current/customer_attraction/model.md)；不限制通用模型的平局规则。
- **Dependencies：** 仅模型及正文所列14类单位客户与七节点完整策略，不导入静态 Nash 桥或外部定理。
- **Evidence：** 发现者和 root 各自从定义展开71单位客户、Fraction 核验42含自身比较，穷尽21个无序二主题多重集。
- **Counterevidence / Objections：** 尚无成立异议；一般半覆盖在此例余量 2W−OPT₂=32，故本结果不能反驳主目标。真实范围仅所述辅助桥及该唯一最优遗漏集的更强价格预算。
- **Status：** 完整解析有限证书、独立内部重构通过；未外审，未认证新颖性，未整理为共享 canonical。
- **Related Files：** [正文](exchange/unique_optimum_omission_obstruction.md)、[发现者审计](exchange/audit_unique_optimum_omission.py)、[root独立审计](parent/audit_optimal_omission.py)及各自冻结JSON。


## B10-TWO-PLAYER-INTEGER-PUSH-SHARP-v1

- **Exact Statement：** 任意固定合法背景b、恰两剩余人，给定真实末位BR映射ρ，任意目录分布p，B~p，R=ρ(B)，A~p独立。令D=EΣ_{x∈B}1/(b_x+1_B+1_R)，C=EΣ_{x∈A}1/(b_x+1_B+1_R+1)，p_x=P(x∈B)。则D−C≥Σ_x p_x²/((b_x+2)(b_x+3))≥0。
- **Objects / Domain / Quantifiers：** 所有有限共同目录/单位客户/有序固定前缀/任意p与末位平局；恰两人局部比较。证明亦允许非负实背景作为纯代数扩展，不改变主游戏模型。
- **Assumptions / Dependencies：** 仅末位对每个首主题的真实最佳回复，不需要首人遵循最优行动；原完整SPE是足够条件。
- **Conclusion / Scope：** 两人完整终局整数静态推送带sharp曲率余量。单客户目录{∅,{x}}、末位总选{x}取等。无一般人数结论。
- **Evidence：** 发现者、root和另一研究员各自重建原始BR行及精确余量；独审先于阅读发现稿。
- **Counterevidence / Objections：** r=3的D≥C已被下条完整SPE反例否定，故归纳不可直接沿用。
- **Status：** 解析证明与独立内部审查通过；外审/新颖性未认证，个人资产。
- **Related Files：** [正文](induction/two_player_full_terminal_pushforward.md)、[独审](independent_pushforward/two_player_pushforward_review.md)。

## B10-THREE-PLAYER-INTEGER-PUSH-AVERAGE-NO-v1

- **Exact Statement：** 存在34单位客户、七主题（其中一个空主题）、三人完整历史纯SPE及p，使上述r人完整终局推送定义中D=29/30<C=41/40，D−C=−7/120。
- **Objects / Domain / Quantifiers：** 存在性反例，原共同目录单位模型；全部57有序决策历史。p(X2)=1/10、p(∅)=9/10。
- **Assumptions / Dependencies：** 既有34客户个体安全值反例的非空策略部分；增加空主题并显式补完所有含空历史。详见正文完整规则。
- **Scope / Conclusion：** 否定任意r的平均D≥C强推送桥。实际根u=29/3，u−C=1037/120>0，W32、OPT34；不否定弱C≤u、extra-one、真正安全聚合或half。
- **Evidence：** 发现者与root独立单位客户Fraction核验57节点399含自身比较、完整D/C及OPT。
- **Counterevidence / Objections：** 无成立异议；不能用这个强桥失败推断弱桥失败。两块复制的另一个暂报弱桥阳性因额外插入分母算错已撤销。
- **Status：** 完整有限解析证书、独立内部重构通过；外审/新颖性未认证。
- **Related Files：** [正文](representation/terminal_pushforward_D_lt_C.md)、[root审计](parent/audit_integer_push_34.py)及冻结JSON。

## B10-RECIPROCAL-ISOLATION-SHARP-v1

- **Exact Statement：** 任意k≥1，N由两两不交X_i,Y_i,D组成，目录含C_i=X_i、A_i=X_i∪Y_i、B_i⊆X_i∪Y_i∪D及D，允许其他任意主题。完整SPE实际C₁…C_k,D；每个实际i节点改A_i后末选B_i、改B_i后末选A_i，两分支中间行动均避开X_i∪Y_i∪D。则2(k+1)OPT_{k+1}≤(3k+2)W。
- **Objects / Domain / Quantifiers：** 任意k与有限局部池、任意额外目录、所有满足两条真实偏离续局条件的完整SPE；不是所有SPE的普遍界。
- **Definitions / Dependencies：** x_i=|X_i|，y_i=|Y_i|，d=|D|；依真实当前/末位比较x_i≥v_i≥d≥x_i/2+y_i。锐性依既有全人数无拥挤族的完整SPE存在证明。
- **Scope / Conclusion：** 指定惩罚架构的精确有限k上限，原族逐k取等；不能只改局部重叠、遗漏/公共池放大到half反例。
- **Evidence：** 发现者、root及先盲重构的独立研究员均核对解析证明；k=1界5/4，d=0强制全零，正整数取等需d偶数。
- **Counterevidence / Objections：** 不排除多个后继覆盖同局部池、跨组惩罚或D被中间覆盖等逃逸结构。
- **Status：** 解析证明和独立内部审查通过；外审/新颖性未认证。
- **Related Files：** [正文](counterexample/reciprocal_isolation_barrier.md)、[独审](independent_no_go/reciprocal_isolation_review.md)、[逃逸义务](counterexample/breaking_isolation_notes.md)。

## B10-PURE-FULL-ROOT-MENU-NO-v1

- **Exact Statement / Quantifiers：** 存在八人、八主题、32名单位客户的共同目录游戏和完整有序历史纯SPE，实际根u=13/4；每个强制根行动B的完整八槽终局Z(B)均有合法额外查询A满足sum_(x in A)1/(1+c_x(Z(B)))=37/10>u。
- **Objects / Domain / Assumptions / Definitions：** CAG-MODEL；额外查询不删除原根，分母加一。DAG在每步覆盖所有合法动作，不限制原问题历史量词。
- **Scope / Conclusion：** 否定纯完整根菜单阻断；W=OPT8=32，同一菜单的独立混合值851/280<u。
- **Dependencies：** 显式两块客户、完整DAG、有限精确比较及深度归纳；不调用一般直和。
- **Evidence：** 发现者、root及另一研究员分别核验/重构；root审计13872节点、6435叶、59496含自身比较，混合原始/对偶有理匹配。
- **Counterevidence / Objections：** 暂无成立异议；不能据此反驳混合菜单、自由整数背景extra-one或half；旧插入分母误判已撤销。
- **Status：** 精确有限证书，独立内部重构；个人资产，未外审，未认证新颖性。
- **Related Files：** [正文](counterexample/pure_full_root_menu_obstruction.md)、[root核验](parent/verify_two_block_dag.py)、[独立结果](parent/two_block_dag_independent_audit.json)。

## B10-MIXED-FULL-ROOT-MENU-v1

- **Exact Statement：** 对每个合法有序前缀b、每个剩r≥1、每份完整纯SPE，令Z(B)为强制当前根B后同一策略的完整r槽终局，u=max_B sum_(x in B)1/(b_x+c_x(Z(B)))。存在独立列分布Q，使对每个合法查询A，E_Q sum_(x in A)1/(b_x+c_x(Z(B))+1)≤u。
- **Objects / Domain / Quantifiers：** 所有有限单位客户共同目录、任意总人数、全部历史和平局；Q依节点、实例、策略，但不观察查询抽样。
- **Definitions / Scope / Conclusion：** 列含根，恰r竞争槽；强于自由r槽背景extra-one，弱于纯列。逐实际节点成立足以推出half。
- **Dependencies：** 有限minmax、静态OPT_m≤2m v_(m+1)(0)；真实多后继比较仍未证明。
- **Evidence：** r≤2解析成立；八人纯列反例混合值低于u仅是实例核对。
- **Counterevidence / Objections：** r≥3有D(p)<C(p)、势排序失败与高插入二环，均不自动否定本候选。
- **Status：** OPEN。
- **Related Files：** [混合义务](induction/full_root_menu_mixed_obligations.md)、[接口](tree/full_terminal_menu_interface.md)、[联合势身份](tree/full_terminal_reply_column_identity.md)。

## B10-PROFIT-BELLMAN-LOCAL-NO-v1

- **Exact Statement：** 对每个整数n≥4，采用CA-PREFIX-BALANCE-NO的同一原始单位客户族与完整SPE，定义F_r(b)=max_(r主题Z) sum_x c_x(Z)/(b_x+c_x(Z))，零分子项为0。则F_(n−1)(1_A)=2(n−1)(n−2)+(7n−13)/6，而实际首位u1=n−1/n，F_n(0)=OPT_n=2n²−2n−2。
- **Objects / Domain / Quantifiers：** 该显式共同目录无限族；所有n≥4。一般拟议台阶欲量化所有合法背景与SPE，反例取空根实际首行动。
- **Assumptions / Definitions / Dependencies：** CAG-MODEL、既有完整全历史SPE族合法性；新F是背景剩余利润，非总覆盖补全。精确优化由整数槽消元证明。
- **Scope / Conclusion：** 2u1+Ftail−OPT=(23−5n)/6−2/n<0对每个n≥5；任何固定α<17/6最终也违反αu1+Ftail≥OPT。只反驳该局部充分归纳，不反驳F_r≤2P或Q-CAG-HALF。
- **Evidence：** 发现者与root各自从原始客户类型解析求最优值；独立实现各枚举n4..8共15501计数候选。原SPE全历史证明沿既有资产引用。
- **Counterevidence / Objections：** 暂无成立异议；全局2W−OPT=2(n−1)>0，尾部额外裕量能支付首步债，不可忽略。
- **Status：** 个人完整证明、独立内部解析复核；未外审、未认证新颖性、未提升共享canonical。
- **Related Files：** [自足正文](round5_induction/profit_bellman_counterfamily.md)、[root审查](parent/profit_bellman_family_independent_review.md)、[独立回归](parent/profit_bellman_family_independent_audit.json)。

## B10-PROFIT-BELLMAN-ANY-FIXED-NO-v1

- **Exact Statement / Quantifiers：** 对每个有限实数α，存在整数n≥2、有限单位客户共同目录和完整全有序历史纯SPE，使F_n(0)−F_(n−1)(1_A)>αu1；这里F_r(b)=max_(r主题Z) sum_x c_x(Z)/(b_x+c_x(Z))，零分子项为0。
- **Objects / Domain / Assumptions / Definitions：** n名单位玩家；互不交A（n客户）、B1,...,B_(n−1)（各1客户）；全部历史策略均选A，保留任意原模型平局。
- **Conclusion / Scope：** u1=1，F_n(0)=OPT=2n−1，Ftail=2n−h_n，h_n=min_(1≤j≤n整数)(j+n/j)≥2√n。台阶损失h_n−1无界。因此不存在任何通用固定局部乘数。只反驳此局部充分归纳，不反驳F_r≤2P或half。
- **Dependencies：** 均分定义、全部历史下A收益≥1而任何B偏离≤1、剩余槽按A次数及不同singleton规范化；无外部定理导入。
- **Evidence：** 发现者与root各自独立解析全历史策略与精确F最优值；root另以不导入solver的实现核n2..8。
- **Counterevidence / Objections：** 暂无成立异议；W=n且2W−OPT=1。真实tail裕量h_n−2支付根系数二债h_n−3。不能把有限阴性或该例当一般half证明。
- **Status：** 完整任意n证明、独立内部解析复核；未外审、未认证新颖性、未提升共享canonical。实例族已有，新内容仅局部利润归纳的精确无界障碍。
- **Related Files：** round5_induction/README.md、[root独立正文](parent/profit_bellman_unbounded_independent_review.md)、[独立代码](parent/audit_profit_bellman_unbounded.py)、[冻结结果](parent/profit_bellman_unbounded_independent_audit.json)。

## B10-MONOCHROME-SATURATED-QUERY-v1

- **Exact Statement / Quantifiers：** 固定CAG-MODEL任意合法有序背景b、任意r≥1、任意完整纯SPE，若实际剩余路径为A B^r，并且u_A=q(B)，其中q(T)=sum_(x in T)1/(b_x+1+r 1_B(x))，则每个合法T均有q(T)≤u_A。
- **Objects / Domain / Assumptions / Definitions：** 有限单位客户共同目录、任意原总人数、全部有序历史、任意平局；允许空B与零客户。饱和假设是精确等式，不能换成近似等式。
- **Scope / Conclusion：** 一般背景的全查询预算，强于仅q(T)≤u_A+tau_A的VA端点。空背景实际A B^(m−1)且u_A=|B|/m时有OPT_m≤(2−1/m)|B|；不声称扩大已知福利范围。
- **Dependencies：** 根真实改B偏离、逐客户最坏拥挤保底取等刚性、原实际末位B的BR、改B真实枝末位BR。根枝取等迫使所有后继含B；原末位排除严格超集，故真实枝全B。
- **Evidence：** 研究员与root独立解析重构，含空/零边界。
- **Counterevidence / Objections：** 暂无成立异议；M=u_A−q(B)>0的稳定支付未证，不能由连续性填补。
- **Status：** 个人完整解析证明及独立内部审查；未外审/新颖性认证；主目标与一般VA仍OPEN。
- **Related Files：** [正文及M>0精确剩余税](round5_global/monochrome_dominance_and_va_localization.md)。

## B10-OVERLAP-ONLY-ADDITIVE-CREDIT-NO-v1

- **Exact Statement / Quantifiers：** 不存在一族实例无关函数f_r(b,c)，满足所有非负整数负载上f_r(0,c)=f_r(b,0)=0，且C_r=sum_x f_r(b_x,c_x)在每个原模型完整SPE节点同时给F_r(b)≤2P+C_r以及Δ_h+C_child−C_h≤2u_h。
- **Objects / Domain / Assumptions / Definitions：** F为同背景剩余最优利润，P为真实tail总利润，c为真实剩余玩家负载；Δ=F_r−F_(r−1)(b+1_A)。f可负、依r，但不依实例/主题/策略的其他信息。
- **Scope / Conclusion：** 仅否定所写可加信用及充分递推合同；不否定含独占项、实例信息、非可加信用或其他一般证明。
- **Dependencies：** 本轮all-big与旧交叠族的完整SPE及精确F值；两族在同一r=n−1对同一f(1,r)施加不相容上下界，n≥16。
- **Evidence：** 研究员与root分别解析得到冲突；不靠有限搜索。
- **Counterevidence / Objections：** 暂无成立异议；实例无关和两条消失条件均承重，不可省略。
- **Status：** 个人完整解析证明、独立内部复核；未外审、新颖性未认证。
- **Related Files：** [精确合同](round5_induction/credit_state_obligations.md)、[root独立复核](parent/profit_bellman_unbounded_independent_review.md)。
