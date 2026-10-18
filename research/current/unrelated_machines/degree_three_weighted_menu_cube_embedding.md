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

## 6. 任意资源跨组度的真实路径降度

**ID / Version：`UM-FLAT-MENU-RESOURCE-DEGREE-THREE-PATH-REDUCTION-v1`。**

**Objects / Domain / Definitions / Quantifiers / Assumptions。** 源P是§1同一完整显式flat weighted-menu ordinary UM，但**去掉资源跨组≤3的条件**；其余非空groups/menus、state distinct资源、private质量≤1、selector1/resource1、全部原jobs、0时间/空state/unused资源等完全保留。令Γ(u)为全部菜单中使用u的旧groups（零private项仍计），d_u=|Γ(u)|，L为原incidence数，K为原最大菜单数。group与resource均显式，不是一般UM的免费flat分解。

**Exact Statement / Conclusion。** 有确定性位多项式构造D(P)，仍为同一flat域，resource跨全部菜单至多3组、每组state数≤max{K,2}，所有旧state质量原样保持。对任意源完整实际σ且峰C<2，可构造目标完整σ'≤C，所有旧job身份及private/外送决定保留；对任意目标完整实际τ'且峰C<2，可按全部旧jobs投影成源实际τ≤C，含任意partial exports及未选state jobs。并有

\[
 \mathrm{OPT}(D(P))=\mathrm{OPT}(P). \tag{3}
\]

当所有原states归一化W=1时，目标亦归一化，§1–4所用one-state partial resource allocation的最大共同导出值V同样精确保持，包括V0。归约不输入OPT、目标阈值或源assignment；给定assignment的转换才读取它。**不声称保group interaction M**，也不把helpers换成其它未述mixed角色。

**完整构造。** 对d=d_u≥1，列Γ(u)为g_1,…,g_d，用d个ports z_{u,1},…,z_{u,d}替换u；旧group g_j的所有state incidences在u上的外端统一改到z_{u,j}，仍time1，旧private机、job身份、p及selector的全部资格不变。对j=1,…,d−1加一个helper group H_{u,j}，恰两个states：singleton z_{u,j}权1，singleton z_{u,j+1}权1。按真实flat规则各自生成两台private机、一枚unit selector、两枚private1/resource1 incidence jobs，其余∞。d1无helper；d0旧resource明确保留为unused机器。

每port只属于一个旧group及至多两个相邻helpers，资源跨组度≤3；旧K_g不变，helpers K2/质量1。因此W≤1或W1均保持，未引入抽象matroid边或免费容量。

**正向全jobs证明。** 源C<2且C≥1，每旧R_u至多一枚unit外送job，连未选state及private0原jobs也计。若这枚job来自g_a，取port a为空位；否则任取a。让helper H_j选左port j（j<a），选右port j+1（j≥a），这匹配恰所有ports除a。每helper所选state的incidence导出，selector留选根，另一state incidence留自己的private机，三件真实helper jobs全部恰一次，各新机负载≤1≤C。旧private选择不动，唯一旧外送到本group的空port，所有旧/新jobs实际峰≤C。

**任意目标的逆向证明。** 给目标C<2，每helper实际selector所在state的private1 incidence必导出，否则两unit共根负载2。d−1枚被迫外送的helper jobs必占d−1个不同ports；任意未选helper incidence若也导出，只会多占，不能释放这些已占端。故路径至多一枚**旧**job可外送。删全部helper jobs/private机，将每旧外送port合回R_u，private端旧jobs不动；每R_u至多一unit，其余旧负载不增，给合法完整源调度≤C。没有假设helper使用预设matching、每helper只导出一job或旧state全量导出。

**OPT2边界。** 两边全private基线都≤2，selector使OPT≥1；最优完整assignments有限，达到。若源OPT<2，正向再逆向给相等；若源OPT2而目标<2，逆向矛盾。由此式(3)包括2端点。对任意给定C≥2的单份调度，也可直接输出另一边全private≤2，不声称保持这份调度的private/外送决定。

**归一化partial value。** 对每v∈(0,1]，给源一个state/组及不交导出子集质量≥v。每u按其旧领取group留下port空位（未领取任留一个），helpers按上述路径各领取自己的singleton、质量1≥v，旧state及领取子集权不变。反向任意目标正值allocation中每helper都必须领取完整singleton资源，所以d−1ports被占；旧groups至多领取一个port，合回u仍不交，旧group仍同一个原state的同一partial subset。两向对每正v成立，有限最大值及0≤V≤1给V0也保持；这不是只对full-state YES的decoder。

**总位复杂度。** Σ_u d_u≤L，helper数h=Σ(d_u−1)_+≤L；有用port≤L，再加至多|U|个保留unused旧resource。每helper恰增2 private机、3 jobs、6 finite资格。若旧private数a、group数n，目标机器≤a+|U|+3L，jobs≤n+4L，dense条目乘积仍多项式。所有新时间为1，原p逐job复制，其余未列资格仍为∞；membership去重、孔位与路径匹配、全job投影按显式L扫描，不按分母或阈值倒数展开。

**最接近结果与准确扣除。** 已存[BCG2009原作者PDF](../../../history/source/literature/unrelated_machines/bateni_charikar_guruswami_2009_maxmin.pdf)（SHA7f7b21ff08b37e8489e9f60527e9aa9458dc5cf4cd6cc6804869665c24d51f7f）§2.2 Theorem2.4/Fig2、PDF及印8–9，已明确使用d个item copies与d−1个相邻dummy players的同一路径装置，dummy取值∞；其脚注也提及MinMax版本。root本次实际读这些原文位置，不把装置或degree-three思想当原创。本页保留的是该标准技巧在明示flat ordinary UM矩阵中的物理helper实现、全原jobs/任意partial exports/OPT2与V0端点及位复杂度的自足合同，视作直接重构；没有新的SC降度或近二hardness声明。

**Dependencies / Evidence / Counterevidence / Objections / Status / Related Files。** 自足单位路径匹配与完整矩阵域；typed先冻Exact，rainbow只据Exact独立重构先冻，root亦只据陈述独立核，再分别实际读作者Proof及最终稿范围，详见[路径归约审查](../../reviews/unrelated_machines/flat_menu_resource_degree_three_path_reduction_review.md)。无standing fatal；标准matching路径技巧不主张全球新颖，未实现软件、未外审。原§1–5的三坐标嵌入及其原冻结审查保留，不能把本追加当旧Claim换域。

## 7. 组成后真正剩余的源条件

先用§6降度，再用§1–5的zero-cell cube表示，**任意**显式flat weighted-menu源都可位多项式嵌入d=Q3，精确保实际OPT、保归一化，目标最大菜单数≤max{K,2}。它允许增加真实helper groups/jobs；不保原组数或M，也不要求全cell正权、label唯一定价或one-heavy/two-diffuse型。

因此本路线的源无需先做到资源跨组≤3；近二hardness仍缺norm1、显式小表示、所有partial exports都可解码的实际gap。仅证明一个已有源的资源度很大不再是致命缺口，直接把general additive行归一化则仍受[同宇宙菜单数障碍](normalized_weighted_menu_santa_value_and_size.md)的严格接口限制。整个组成不是一般UM到flat的归约，更不是已有的近二反面证明。

## 8. 任意归一化菜单的三态、资源度三正规形

**ID / Version：`UM-NORMALIZED-FLAT-MENU-THREE-STATE-DEGREE-THREE-NORMAL-FORM-v1`。**

**Objects / Domain / Definitions / Quantifiers / Assumptions。** 源P为§6任意K/任意资源跨组度的完整flat域，另要求每原state的非负private质量**恰1**；原group非空、menus显式非空、state内资源互异，全部原incidence及selector仍是实际不可拆jobs。可有零项、重复states和unused资源，无其它jobs。令n=|G|、S=ΣK_g、I为原incidence数。V为每group选一个state及该state的partial子集、跨groups不交的最大共同private质量。

**Exact Statement / Conclusion。** 有确定性总位多项式映射P↦P*，输出同一normalized flat ordinary UM类，且每group至多3states、每resource跨全部states至多3groups。任意实际C<2调度在两向均可转为另一边全部原jobs完整调度、峰不增，任意正阈值v的one-state partial allocation也两向可转；于是

\[
 \mathrm{OPT}(P^*)=\mathrm{OPT}(P),\qquad V(P^*)=V(P), \tag{4}
\]

包括OPT2、V0端点。不输入OPT/源YES证书，不制造源gap；允许增加真实group/selector/单例job，不保原group数、M或one-heavy/two-diffuse型。

**第一步：真实binary selector树。** 对每原g，取叶恰为它K_g个indexed states的显式满二叉树，K1即单叶。每树顶点v建一个新group Q_v，每group**恰一枚**selector；每state独立private机与其全部incidence jobs。每非root v有一个fresh own-resource a_v，树/旧资源namespace不交。菜单如下：

| 树顶点 | 完整state菜单，singleton权均1 |
| --- | --- |
| internal root | 两个states，分别用左child的own-resource、右child的own-resource |
| 非root internal | own singleton，以及左child、右child的own singletons，共3states |
| 非root leaf，对应原s | own singleton，以及原S_gs/原p state，共2states |
| root即单叶 | 只有原state，无own state/resource |

原state private机及全部incidence jobs在对应leaf沿用原身份、时间与两个有限端；原selector J_g用作root selector，其资格改到root states。每非root新group另增一枚unit selector。所有新singleton incidences是独立真实jobs，不免费当OR约束。每state质量1。

**partial allocation正向。** 给每原group一个state及导出子集质量≥v>0，在树中选到该leaf的路径。root及路径上internal选下一个child的singleton并领取它；路径终leaf选原state并领取原子集。其余树顶点一律选own singleton并领取它。每own-resource恰由parent路径job或自身off-path job使用，互不冲突，质量均1≥v；原资源子集仍跨groups不交。K1直接保原state/subset。

**任意partial allocation逆向。** root所选singleton要正值必须领取child own-resource，故该child不能以own singleton取得正值，必须选child分支或在leaf选原state。沿实际所选singleton逐层到某个实际选择原state的leaf，取得原同一state的原partial子集质量≥v。未选分支可以自行激活，不影响从root取出这一条路径；只取一leaf/原group，原资源互不相交从全目标allocation继承。K1的root本来就是原state。故正阈值两向等价，有限最大值与非负性给V0也保持。

**实际完整调度正向。** 给原σ峰C<2，取J_g实际所在的原state s，选到它的路径如上。K_g=1时该树所有旧jobs原位不动；以下root移动只用于K_g>1。将原J_g移到树root的相应singleton private机；每非root路径internal的selector选child state，路径leaf的selector选原M_gs；off-path顶点selector选own state。所有已选singleton incidences外送其own-resource，未选singleton incidences留自己private，全部新机负载≤1≤C。所有原incidence jobs保留σ的原private/外送目的地，不只保selected state；原M_gs处新leaf selector替代移走的原J_g，负载相同。其它原private没有新增selector，仍≤1≤C，旧resource负载不变。全部原/新增jobs各一次，峰≤C。

**任意实际目标调度逆向。** 对树中实际selector选择，所选singleton job若留private会与unit selector成负载2，故C<2强迫外送。root占child own-resource后，child若选own state，其singleton也被迫外送同一resource，负载2矛盾。因此沿真实singleton选择到一个实际选原state的leaf。将原root-selector J_g移回该leaf的原M_gs，替代其将被删除的leaf selector；保留全部原incidence的实际目的地，删其它新增selectors/singleton jobs/own-resources。被选原M_gs的selector负载相同，其余原private只减负载，旧resource仅删除aux后不增，输出全部源原jobs的合法σ≤C。未预设一条正规路径、未忽略未选原state的实际exports。K1无需移动。

**第二步及端点。** 在以上三态中间实例的**全部资源**上执行§6真实port-path归约；先三态、后降度，因为拆旧states成leaf可能先增资源跨组度。path helpers仅2states，所以最终仍≤3；其actual C<2和partial正值双向接上前一步，资源度≤3。两边all-private≤2及C<2两向排矛盾，得actualOPT2也相等；V0由正阈值同理。每原job最终都经实际中间矩阵还原，不用式OPT=2−V替代全任务证明。

**规模 / Dependencies。** 第一部恰2S−n groups、5S−4n states、2S−2n个fresh own-resources；保全部I原incidences，再加4S−4n枚singleton incidences。公式含K1（单组贡献1group/1state/0新资源）。每组一selector，第一部jobs恰I+6S−5n。之后path helper数≤第一部incidence数，总机器/jobs及dense乘积均多项式；每个时间为原有理或1，∞未述端禁止，不按数值/分母复制。数学依赖完整normalized flat域及§6路径降度，不借SC行归一化或配置LP。

**Evidence / Counterevidence / Objections / Status / Related Files。** typed先冻新Exact，general仅据该Exact及明确path Exact依赖独立构证先冻，然后才实际读作者Proof与本追加正文；root亦仅读Exact独立核partial链与逐原job替换，后亲读源与审查，见[三态正规形审查](../../reviews/unrelated_machines/normalized_flat_menu_three_state_degree_three_normal_form_review.md)。证明完整，无standing fatal；selector/matching树直接重构，全球新颖性未认证、实现none、未外审。这里没有把任意未归一化Santa Claus行Σp>1偷偷转入域。

## 9. 对反面源搜索的准确更新

任意显式normalized flat菜单的真实near2 gap，若另行证明，均可先变成(K≤3、Δ≤3)，再嵌入d=Q3零格cube；因此K或resource度无界不是本源域固有的归约缺口。full cell权表/zero许可、归一化和所有partial exports的源NO依旧承重。新normal form的internal可以三heavy singletons，mixed leaf可own-heavy/原state二选一，不得擅自等同更窄的one-heavy/two-diffuse或固定角色类。

本表示不解决主目标：尚无本文提供的normalized YES V1/NO任意小V的复杂度源，也没有从一般UM到flat的免费转换。它把后续源工作集中到可实际解码的全局一致性，未用新对象替换UM-TARGET-v1。
