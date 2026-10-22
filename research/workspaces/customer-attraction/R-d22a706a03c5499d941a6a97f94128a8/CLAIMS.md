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
