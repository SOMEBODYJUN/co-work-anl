# 三组资源加权菜单的三坐标表示：零格权精确保留真实OPT

读取目的：区分“固定几何维数”与“有限组间交互”。以下显式表示仍包含完整的资源跨组度三加权菜单类；它转移已有的实际源承诺，却不产生近二困难性源。允许零cell权和各indexed state自己的cost table是准确对象的一部分。

## 1. 精确对象与结论

**ID / Version：`UM-DEGREE-THREE-WEIGHTED-MENU-CUBE-EMBEDDING-v1`。**

**Objects / Domain / Definitions / Quantifiers。** 输入P为完整flat weighted-menu ordinary UM：有限非空groups G，每组非空显式indexed states A_g；每state有distinct资源集合S_gs，及二进制有理p_gsu≥0，总量W_gs≤1。每state独立private机器M_gs；每resource一机器R_u；每组一selector只能在自己的state机器耗时1；每(g,s,u)一独立job只能在M_gs耗时p_gsu或R_u耗时1，其余∞。没有其它jobs、预载、资格或约束。空state、重复indexed states、p=0和unused资源均允许。

写U_g=⋃_s S_gs、q_g=|U_g|、K_g=|A_g|、S=Σ_gK_g。只要求每resource跨全部菜单至多3个groups；不限制K_g、q_g、组交互度M。M是完整U_g交集图的最大度，含只由零权incidences产生的membership。

目标C(P)是同样完整UM格式的weighted grouped coordinate slices：每variable x有独立tagged cube {x}×[3]^3全部27资源；它出现在至多3组，给这些组互异index j_x(g)∈[3]。每组变量集非空；每indexed state对每变量选一个coordinate label ℓ∈[3]，包含完整9格slice {z:z_ℓ=j_x(g)}，每格一独立incidence job，private权非负、resource端1；每state总private≤1，一个unit selector选态。

目标明确允许**零cell权、不同indexed states拥有同一个label vector而cost table不同**。原state身份由其indexed private机器/jobs保留，不假设label vector唯一决定它。不属于全cell正权或label唯一定价的更窄模型。

**Exact Statement / Assumptions / Conclusion。** 对每个上述P，有确定性位多项式显式构造C(P)，保持原K_g、W_gs和交互图、每个原job身份及其全部原有限端时间（incidence jobs恰有两端），并满足：任意完整P调度可扩展为峰完全相同的完整C(P)调度；任意完整C(P)调度可投影为峰不增的完整P调度。因此

\[
 \mathrm{OPT}(C(P))=\mathrm{OPT}(P). \tag{1}
\]

两向映射也位多项式，不需最优见证或阈值假设。所有实际makespan YES/NO承诺精确转移；不声称转移其它费用/拒绝数等未声明目标。G非空保证两者OPT≥1，空组输入不在本ID域内。

**Dependencies / Scope。** 自足显式构造；不调用文献hardness源或SC近似算法，不将配置间隙当实际困难性。

## 2. 固定active格与完整构造

对每个原resource u建立variable x_u及其全部27资源，即使u未被使用也保留。将{g:u∈U_g}按输入顺序赋互异indices j_{x_u}(g)。固定

\[
 z^*=(1,2,3).
\]

每g的每个state对每u∈U_g都取label ℓ=j_{x_u}(g)。因为z^*_i=i，z*属于所有这些slices；每slice恰9个互异cells。

保留每个原indexed state、private机和selector。把原R_u识别为active资源(x_u,z*)；对实际存在的原incidence I_gsu，把它识别为该state中x_u的active-cell job，原private权p、外端1完全不变。若u未在原S_gs出现，则该state的active-cell job是新加的private0 job；其余8格也全为新加private0/resource1 jobs。原p=0 job仍有自己的原job身份，不能只按“权为零”删除。

若U_g为空，为它单独添只属于g的dummy变量y_g，index和label均1；每state该slice九枚job的private权全0，完整27资源仍显式列出。故目标每组变量集非空，不增加组交互。新dummy tags与全部x_u tags互异。

原incidences在目标中单射：不同(g,s,u)映射到不同state、variable或job，未合并任何任务。额外jobs只添private0，总private质量仍逐state恰W_gs。各state可同label vector而异cost，正是域内明示的indexed-state含义。

## 3. 任意完整调度的双向还原

**扩展。** 给任意P调度，按上述机器和job映射保持其执行端。每额外job放自己的indexed private机，耗时0，包括selector所在state及全部未选states的额外jobs。原private及active资源负载逐项不变，其余新资源空载，全部目标jobs恰一次，峰完全相同。

**投影。** 给任意C(P)调度，不要求额外jobs已留private，也不要求峰<2。依显式身份删所有额外jobs和非原机器像；原unused R_u的active机器像仍保留。每个原selector只可能在自己的原state；每个原incidence只有原private像及原active资源像两个有限端，没有获得另外8格的资格。按逆映射逐job返回原端，所有原jobs仍各一次、合法且耗时不变；删除jobs只会减负载。因此峰不增。两向立即证明式(1)，包括OPT=2和任意严格/非严格阈值。

## 4. 全菜单交互、正support及显式大小

两组若共享原u，则其x_u slices都包含active格，在目标完整资源并集上仍相交；若不共享原u，则variable tags不交，dummy各组独有，也不相交。故完整group interaction graph**精确相同**，M不变。任何目标resource属于单一cube，其incident groups至多该variable的3组，dummy至多1、unused cube为0，所以目标资源跨组度≤3。

使峰≤1当且仅当可每组选一个state，其正private权support跨组不交：必要性来自selector1强迫该state所有p>0 jobs导出，resource单位容量；充分性将这些正jobs导出，其余各state全部jobs留自己的private≤1，选态零jobs与selector共居。目标正support恰为原positive incidences在active格的像，因而保持此unit可行性。完整几何slices还可在零权格相交，不能由几何交集免费推出额外一致性。

令e=#{g:q_g=0}、q'_g=max(1,q_g)。目标资源机恰27(|U|+e)、private机S、selectors |G|、incidence jobs恰

\[
 9\sum_gK_gq'_g. \tag{2}
\]

K_gq_g不一定与原incidence数线性，因为原state可能缺该group并集内很多资源；但Σ_gK_gq'_g≤S max(1,|U|)，且e≤|G|≤S，故显式规模仍多项式。并未生成3^{q_g}全局label states。若原输入是dense矩阵，目标最多

\[
 (|G|+9\sum_gK_gq'_g)\big(S+27(|U|+e)\big)
\]

项，也总位多项式。有限时间仅复制原二进制有理数或写0、1，余项∞；indices/tags/逐原job映射位长多项式，不按分母或处理时间数值复制。

## 5. 与交互正界的组成及其严格限制

[有限交互算法](weighted_menu_bounded_group_interaction_rounding.md)的v2定理应用于该目标，取Δ=3，因子为2−1/(M+5)。固定M仍有本结构类的统一改善；本嵌入允许M随q_g增长，因此固定d=Q=3本身没有消掉剩余全局耦合。它也说明Q2的degree2算法不能直接覆盖所有Q3带零权菜单。

一个真正的近二反面源仍须先在本flat菜单域证明YES OPT≤1、NO OPT≥2−δ，NO覆盖所有选态及部分导出。式(1)只负责传递这个已证明的源gap，不提供它。若对所有格加正扰动，原本可留private的零jobs在unit阈值下会被迫导出，几何交集可能立刻破坏YES；本结果不支持这种替换。若label vector唯一决定cost/原state，本构造亦未证明可嵌入。

**Evidence / Counterevidence / Objections / Status / Related Files。** 自足构造及两向全部原job证明完成；Exact-only独立重构、实际作者Proof读后及最终正文核对另见[审查](../../reviews/unrelated_machines/degree_three_weighted_menu_cube_embedding_review.md)。无standing fatal；外审、新颖性未认证。没有软件实现或有限实验声明。与已有uniform cube的绝对三半界不矛盾：这里允许任意state权表及零格。一般UM-TARGET-v1的存在或反面仍未解决。
