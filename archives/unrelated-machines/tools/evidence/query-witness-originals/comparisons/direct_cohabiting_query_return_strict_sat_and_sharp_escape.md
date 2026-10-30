# 直接共居查询—返回的严格SAT合同与三半锐逃逸

读取目的：检验一种允许同机异权、企图以共居负载锁住query/return身份的真实归约。这里严格端确实保SAT，但任意正异权参数仍存在全部任务的三半调度；固定半权时该失败阈值精确。它不同于[逐机统一时间的局部交换](machine_uniform_query_return_index_exchange.md)，也不把一个strict NP困难桥冒称接近2的困难性。

## 1. 完整原矩阵与两个Claim的共同域

源为显式有限CNF，每个clause有至少2枚实际文字occurrences，重复文字、变量及clauses允许，每枚occurrence只属于一个clause。只保出现的变量，将各自occurrences排成环并显式补dummy至环长至少3。记总索引数N、真实occurrences数L、clauses数m。最少padding时N≤L+2v；额外更长dummy表按实际N计。空公式单列为一台idle机器、零任务，OPT=0，不使用下文的非空下界。

非空时每索引有两台不同原机器M_i,C_i，两件不同原任务q_i,b_i；每clause另有一件u_c。令i⁺为变量环后继，正文字s_i=0、负文字s_i=1，dummy的s任取；pin(i)=M_i当s_i=0，否则M_(i⁺)。给有理1/2<ρ<1，每真实i给正有理x_i,y_i且x_i+y_i≤1；dummy固定x_i=1。全部且仅以下端有限，其余∞：

| 原任务 | 有限原端与真实时间 |
| --- | --- |
| q_i | M_i:ρ，M_(i⁺):1，C_i:x_i |
| b_i | pin(i):ρ，C_i:1 |
| u_c | 对其每个真实i∈c，C_i:y_i |

全部2N+m件原任务均须执行；没有预载、额外状态或实际virtual执行端。原机数2N，finite条目5N+L，dense条目2N(2N+m)。这改变了旧[保护环的公共子句机](near_unit_implication_pcsp_and_physical_copy_obligation.md)以及旧D/h pair-sensor的实际矩阵，不回改旧Claim。

## 2. 任意异权的严格合同及全公式失败

**ID / Version：`UM-WEIGHTED-DIRECT-COHABITING-QUERY-RETURN-ALL-FORMULA-FAILURE-v1`。**

**Objects / Domain / Quantifiers / Assumptions / Definitions。** 对§1每个完整输入、全部合法正异权、任意显式环排序及dummy polarity，strict表示完整实际峰≤1。边界出口或返回均由原任务实际目的地读取，无免费同编号假设。

**Exact Statement / Conclusion。** strict可行当且仅当源SAT；给满足赋值能构造strict调度，给任意strict调度能解码满足赋值。另一方面，**不求源赋值或未知strict见证**，可确定性总位多项式输出全部原任务的共同实际调度，峰≤3/2，包括所有UNSAT公式。

严格正向：置每变量方向z=0表示True、z=1表示False。每clause选一满足occurrence i，令q_i→C_i、b_i→pin(i)、u_c→C_i；其余q_i沿方向z取M_i或M_(i⁺)，b_i留C_i，含全部dummy。每环每台M恰一件，时间ρ或1；选中C的两原任务合x_i+y_i≤1，其余C仅b_i。不同clauses所选索引互异，因此所有机器同时≤1。

严格反向：任意实际峰≤1时每M至多一件q/b，因为所有这类时间>1/2。令E={i:q_i在C_i}，R={i:b_i在pin(i)}。正x_i使q_i与unit b_i不能共居C_i，故E⊆R。M端原任务数为N−|E|+|R|≤N，所以E=R且每M恰一件。u_c的正y_i又排斥unit b_i，故其实际C_i必有同编号q_i。每索引恰一件有效环任务（未导出时q_i，导出时b_i）。写其方向z_i为0或1，M_i件数给(1−z_i)+z_(i⁻)=1，遂整条变量环方向相同。返回b_i方向固定为s_i，每个u_c因此给出一个真文字。扫描实际分配即可解码SAT；额外合法exports、returns和dummy均已计入。

## 3. 一个共同匹配给全部异权公式三半调度

把有某个y_i≤1/2的clause称baseline，固定其中一个这样的t(c)；其余active clauses的所有y_i>1/2，故其全部x_i<1/2。设active数h。

只作分析的二部图：左侧全部q_i,b_i及active u_c，右侧全部M_i,C_i及每active clause一个标签V_c，两侧均2N+h。图边为q_i→M_i,M_(i⁺)，active i还可→V_c；b_i→pin(i),C_i；active u_c→自身clause的各C_i。**图中没有q_i→C_i边。** Baseline u只暂不入图，随后全部恢复。

对active i∈c取θ_i=1/k_c≤1/2，其余θ_i=0。给b_i在pin,C质量θ_i,1−θ_i，active u_c在C_i质量θ_i；q_i先各给两M端1/2，再从其pin端扣θ_i、给V_c加θ_i。各job质量1；每M被扣的q质量由同编号b补回；每active C的b+u质量1，其余C的b质量1；每V收质量1。这是全图同一份fractional perfect matching，普通Hall/整数匹配给一个共同perfect matching。

Baseline/dummy C只有b邻居，故所有这些b都留C、q都在环内。每active V恰选一q_j，每active u占一C_r并迫该b_r返回pin；其它该clause的b留C。所有M恰一件，所有返回pins互异。允许j≠r，这正是弱端失去的索引合同。

将匹配中q_j→V_c改成同一原q_j→自身C_j，所有其它匹配原任务保原端与真实时间；把全部baseline u_c加回C_(t(c))。Virtual标签不出现在最终分配。逐机实际负载为：

| 原机器 | 全部任务的共同负载 |
| --- | --- |
| 每M_i | 匹配的一件q或b，≤1 |
| baseline C_i | b_i=1，选中时再加自身clause的u，≤3/2；无q导出 |
| dummy C_i | 仅b_i=1 |
| active C_i且b_i留此 | 1，或1+x_i<3/2；此机没有u |
| active C_i且b_i返回 | 原u的y_i，可能另加q_i的x_i，总≤1 |

每occurrence仅属一clause，故不会另加其它u。全部2N+m原任务一次，所有原资格合法，同一分配峰≤3/2。Baseline和active可任意混合，不依赖源可满足性。

**Scope / Dependencies / Evidence / Counterevidence / Status / Related Files。** 依赖§1实际矩阵、k_c≥2、正x,y、和≤1及标准匹配；不纳unit/empty clauses，不把其它同机异权接口都排除。Baseline比较、图构造/匹配、全任务恢复及有理负载回算均按显式总编码长度多项式，不按分母或1/x复制。匹配技巧是已有技术，本增量为此具体改动矩阵及任意异权全公式失败，非新匹配定理。作者Exact先冻，typed仅读Exact独立重构后才读作者Proof；root实际通读并独核。作者一次向reviewer简述策略发生在独立记录已冻结之后，原记录如实保存。见[实际限定范围审查](../../reviews/unrelated_machines/weighted_direct_cohabiting_query_return_review.md)。数学完整，无standing fatal；implementation none、外审/全球新颖性未认证。不能从strict SAT推出near2困难性。

## 4. 固定半权的精确三半阈值

**ID / Version：`UM-DIRECT-COHABITING-SAT-COMPILER-SHARP-THREE-HALVES-v1`。**

**Objects / Domain / Quantifiers / Assumptions / Definitions。** §1同一完整P，固定全部真实x_i=y_i=1/2、dummy x_i=1，且3/4<ρ<1，域内全部公式。该新Claim改变参数与结论，另立ID；不把§3的异权匹配作为本节必需前提。

**Exact Statement / Conclusion。** 非空SAT实例actual OPT=1，非空UNSAT实例actual OPT=3/2；任意完整峰<3/2实际调度可确定性总位多项式解码SAT。空公式仍OPT=0。

所有公式的三半上界直接给全任务：q_i→M_i，b_i→C_i，每u_c任取自己一个真实C_i。每M仅q时间ρ，每C有b及至多一u，负载1或3/2，dummy仅b。不求源解。

任意完整C<3/2中，每M至多一q/b，因为2ρ>3/2；每C至多一q/b，因为真实q_i+b_i为1/2+1=3/2，dummy为2。全部2N件q/b只在这2N台机执行，因此每机恰有一件。每C于是恰在q_i与b_i中选一个，同编号q外送当且仅当b返回。每u_c=1/2又不能与b_i=1共居，必读到该同编号q。有效环任务及方向计数与§2相同，给共同变量赋值，故UNSAT不可能有C<3/2。结合上界得UNSAT exact OPT=3/2。

SAT的unit完整调度按§2直接给出。非空OPT≥1另证：若C<1，则它也<3/2，上述计数迫每C恰有一q/b；任取clause的u所在C，若有b则负载≥3/2，若有真实q则负载1，两者矛盾。故非空SAT exact OPT=1。此下界没有从“某任务有一个可选unit端”错误推出OPT≥1。

**Scope / Dependencies / Evidence / Counterevidence / Status / Related Files。** 固定3/2 gap的具体锐界，不排所有小ε改善。给实际分配的decoder只扫描原身份与环方向，不搜索SAT或丢弃任务；ρ的二进制位长与dense输出均计入。root先冻陈述和作者证明；general仅读完整矩阵Exact及新陈述独立重构后才实际读root证明，见[审查](../../reviews/unrelated_machines/direct_cohabiting_sharp_three_halves_review.md)。ρ=4/5、源(x∨x)∧(¬x∨¬x)的8机10任务24finite实例，root与general分别从原资格枚举全部5184分配，最优15/10；仅为有限checks，解析计数承担全公式证明。全部证书及audit-only核验另登记；没有general生产求解器、外审或全球新颖性认证，无standing fatal。UM-TARGET-v1仍OPEN。
