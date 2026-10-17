# 逐机两倍跨度的联合槽舍入与共同见证障碍的正面衔接

本页给一个保留额外矩阵结构的正面接口，**不解决UM-TARGET-v1**。它直接对全部任务联合舍入，不先求大边匹配H，也不要求前篇的(Aδ)共同见证。数学机制来自ST有序单位槽匹配及Verschae–Wiese2010第4节Theorem8的前缀计数论证；下面的逐机尺度和两倍跨度估计是该已知机制的直接推论，未认证全球新颖性或独立论文价值。

## 1. 精确身份：UM-ROW-SPREAD-TWO-ROUND-v1

**Exact Statement / Quantifiers。** 对每个UM-MODEL-v1合法输入P，将每个有零可用边的任务分配到一条零边并删除。若剩余输入的每个非空机器行存在正有理γ_i，使其所有有限处理时间均在[γ_i,2γ_i]，则存在一个确定性算法，在P总二进制位长的多项式时间内输出全部原任务的合法分配σ，并有C_max(σ)≤(3/2)OPT(P)。机器数、任务数、行尺度及有理分母均可变；各行γ_i不要求相同，也不要求整个矩阵共用粗格点。

**Objects / Definitions。** 剩余任务没有零可用边，故所有有限时间为正；γ_i可固定取该剩余行最小有限时间。空行不需γ_i。任务仍不可拆分，输入可含∞，输出必须使用有限边。零任务或全部任务可免费分配时返回零调度。

删除零任务保持OPT精确不变：任意原调度限制到剩余任务给一个不更坏的剩余调度；反向，剩余调度加上全部零成本任务也不增负载。故以下只处理存在正任务的情形。跨度条件在删除后检查，属于明确的额外假设。

## 2. 排序槽保留整数前缀计数

给非负有理x，各任务列和1。对每机器i按p_ij非增序，把正x质量从位置0依次装入单位槽，任务连接与其区间有正交长的槽。若前缀S={j:p_ij>a}满足Σ_{j∈S}x_ij≤k，其中k是非负整数，则S的全部质量位于前k槽。任意覆盖所有任务的槽匹配在i上至多选择k个S任务。等号边界也成立，因为只有正交长才连边。

同理，若总质量Σ_j x_ij≤整数k，则该机总槽数≤k，故总任务数≤k。这些性质对每个覆盖匹配同时成立，不先指定大任务身份；Hall覆盖和位复杂度沿UM-ST-ROUND-v1。

## 3. 显式必要LP与逐机负载界

给精确有理目标T>0。剪去p_ij>T，设置任务列和1、非负、机器分数负载ℓ_i=Σ_j p_ijx_ij≤T。每机器另加两行：

Σ_{j:p_ij>T/2}x_ij≤1，　Σ_{j:p_ij>T/3}x_ij≤2。

若该行T<4γ_i，再加Σ_j x_ij≤floor(T/γ_i)；否则不加总计数行。空行只接受零质量。任何makespan≤T的调度均给这些约束的0/1证书：超过T/2不能有两项，超过T/3不能有三项，每个剩余有限任务至少耗时γ_i。

若LP不可行，正确断言OPT>T；若可行，求一个有理可行x并对**全部剩余任务一起**运行有序槽匹配。令t=T/γ_i，逐机分四段：

| 范围 | 由槽保持得到的结论 | 舍入负载 |
| --- | --- | --- |
| t<2 | 总任务数≤1；各保留时间≤T | L_i≤T |
| 2≤t<3 | 总任务数≤2；至多一个时间>T/2 | L_i≤T+T/2 |
| 3≤t<4 | 总任务数≤3；第一大≤2γ_i≤2T/3，第二大≤T/2，第三大≤T/3 | L_i≤(2/3+1/2+1/3)T=3T/2 |
| t≥4 | 全行最大值M_i≤2γ_i≤T/2；普通加性ST | L_i≤ℓ_i+M_i≤3T/2 |

总数不足时缺失项取0。区间包括t=2、3、4各自所列一侧；阈值前缀使用严格大于，等于T/2、T/3的任务由弱负载界处理。全部机器共享一个覆盖匹配，但每行的计数与负载界对任意覆盖匹配成立，故同时满足。加回零成本任务不改变结果。

## 4. 算法、目标搜索与总位复杂度

算法为：零任务预处理和行跨度检查；目标搜索中解上节显式有理LP；在最小可行目标上取有理x、构造排序槽并求覆盖匹配；加回零任务。一般有理LP的多项式求解在此作为标准工具调用，本文审计没有实现通用LP求解器。

为精确二分，只将全体剩余正有限时间的有理gcd d用于目标格点。可将全部分母乘积D作共同分母，将整数Dp_ij求gcd再除D。D的位长至多输入分母位数之和，分子、gcd和d的位长多项式；d不参与近似余量。令U=Σ_j min_i p_ij，逐任务选最短机器给makespan≤U的实际调度。U/d为正整数，其二进制位长多项式；OPT也属于d的非负整数倍。

在k∈[0,U/d]上二分T=kd的最小LP可行目标。T=0时正任务使LP不可行。可行性单调：目标增加时保留边扩大、负载上界增大、两个大任务前缀缩小；γ_i固定，总计数floor(T/γ_i)不减，到T≥4γ_i时删除该约束。已有x仍可行。上端T=U由实际调度保证可行；最小可行目标T_*≤OPT，因为OPT格点的最优整数调度给证书。

二分调用次数O(log(U/d+1))，为输入位长多项式；每次LP有O(mn)变量与O(m+n)行，系数和floor的位长多项式，非空有多项式位长有理基本可行解。排序槽至多mn个，每正x区间至多触及两槽；精确比较、槽构造和增广匹配的总位复杂度均多项式。输出n个机器编号，编码多项式。最终负载≤3T_*/2≤3OPT/2，没有固定m、伪多项式时间扫描或指数配置oracle。

## 5. 与半单位困难性的准确关系及实际实例

前篇UM-JOINT-HALF-PROMISE-NO-v1排除的是(Aδ)共同见证的保证构造（固定δ<1/2，条件P≠NP）。半单位归约所有行均落在某个[γ_i,2γ_i]中，因此本页3/2算法适用。两者相容：算法不要求输出该见证，允许实际调度使用1与1/2的叠加负载3/2，也没有预先冻结H。不能由精确中间接口困难推出实际近似调度困难。

一个具体输入从q=2、A={(0,0,0),(0,1,1),(1,0,1),(1,1,0)}得到。任意两个三元组均不能覆盖三个坐标，故没有完美3DM。采用前篇的逐x源/双关联任务构造，此处省略无作用的闲置机器，得到十机十四任务的合法输入；统一加闲置机器的版本等价。

每激活任务在R_x分配2/3，在两个含x的S_a各分配1/6；每关联任务在S_a及其元素机器各分配1/2。每机器分数负载恰1，并满足本页LP：R_x总质量2，S_a总质量3/2且时间1质量1/2，元素机总质量1且时间1质量1。实际排序槽匹配输出makespan3/2；独立完整分配回溯无makespan1调度。全small调度又给3/2上界，故OPT=3/2。该有限实例展示联合舍入的接口，不是一般证明的替代。

## 6. 来源、证据与剩余关键义务

**Paper Fact。** Verschae–Wiese arXiv:1011.4957v1 Theorem8（PDF第9页、印刷第8页）对共同全局区间[γ,3γ]给11/6配置间隙界；紧随证明的说明指出把三个计数行直接加到LST即可形成对应算法。这里重新证明的是逐机尺度、跨度2的显式LP推论，不把它改称原文定理。ST来源、版本和字节哈希见literature_manifest.json。

[独立审查](../../reviews/unrelated_machines/joint_slot_prefix_review.md)记录先按Exact Claim与指定前缀机制重构，再审冻结证明。代码为[局部前缀槽包络审计](../../../tests/audits/unrelated_machines/row_spread_prefix.py)及[实际半单位联合舍入](../../../tests/audits/unrelated_machines/half_unit_joint_slot.py)，[冻结结果](../../../evidence/runs/unrelated_machines/joint_slot_prefix_audit.json)保存参数、版本、代码hash、实际证书和限制。局部有限检查不等于求过所有全局LP；具体分配回溯不等于多项式选择算法。

Truth：本页受限类构造有完整证明；Value/Mechanism：给出绕过新中间接口障碍的实际联合舍入方式；Novelty：已知机制直接推论，未认证；Ambition：仍欠一般输入。真正未解义务是如何对行内任意尺度混合保留这种统一舍入余量。一般M_i/γ_i可无界；简单丢弃或量化tiny任务会改变覆盖和累计容量。需要新的跨尺度联合计数、交换或容量机制及总位多项式证明，不能把额外跨度假设隐藏进UM-TARGET-v1。

## 7. 新域：共同b、每行至多两枚非unit正资格的实际三半锐界

旧UM-ROW-SPREAD-TWO-ROUND-v1及第1–6节量词不变；以下是不同域的新身份，不互相升级。


ID `UM-TWO-SMALL-INCIDENCE-SHARP-APPROXIMATION-v2`。root已据hardness_route的阈值合同自行提出全类算法及下界；作者不是盲审。冻结Exact-only来源不含证明，下文给完整证明。旧threshold v1来源不倒改，不升级一般UM目标。

输入是完整普通UM：m≥1，n≥0，finite p_ij为binary非负有理，其余∞，每job至少一条finite边；另给binary有理b>0，所有finite p_ij≤b。对每个machine i，其全部job资格中满足0<p_ij<b的不同job数至多2。时间恰b的unit资格数量无限制；一个job可有任意多个small端与unit端，不假设每job只有一个small或资格≤3，不限制共享/环或机器时间行和。时间0资格不限数。复杂度按完整P和b的总编码长度，输出全部原job的一个finite端。

精确结论：

1. 存在确定性总位多项式算法，对上述所有输入输出具体合法σ，Cmax(σ)≤(3/2)OPT(P)。OPT=0、所有/部分job有zero端、n0、单机、没有实际b端和binary极端尺度均覆盖。不依赖randomexpectation、估值或固定机器数。
2. 对每个给定binary有理0≤T<b，存在确定性位多项式精确可行性判定，OPT≤T当且仅当返回完整C≤T的真实σ；失败可证OPT>T。可按显式输入位长多项式求出最优值在[0,b)内是否存在，并在存在时输出exactOPT调度。
3. 对每个给定有理T=b+a，0≤a<b，存在确定性总位多项式程序，若OPT≤T则输出完整C≤3b/2+a≤(3/2)T调度；否则允许返回FAIL，但任意FAIL均保证OPT>T。此项程序成功时也满足该负载界，不用YES witness，不隐含调用OPT oracle。并非声称若OPT>T程序一定FAIL。
4. 因子3/2在复杂性意义下sharp：对每个固定ρ<3/2，本结构类不存在保证ρ的确定性位多项式近似算法，除非P=NP。困难性已在b=1、所有finite时间仅1/2或1、每job最多两种时间（端数仍可多）、无zero资格的更窄子类成立。给出从显式非空perfect3DM的确定性位多项式归约，YES OPT≤1、NO OPT≥3/2，且所有机器仍至多两条positive small资格。退化无可用triple的源可用合法常量NO实例处理。

这是结构类的实际算法与匹配复杂性下界，不是一般UM统一离二算法，也不证明一般UM反面。证明/构造、bit复杂度及外部标准3DM源须独立核；代码实现、有限运行、新颖性与独立论文价值未认证。若日后扩到三条small行或其它times另立版本。


Objects/Domain/Definitions/Assumptions见精确陈述；Dependencies为UM-MODEL-v1、UM-ST-ROUND-v1、标准有理LP/整数流、Karp3DM和下述PSM2018框架。Scope为完整受限类实际算法及条件锐下界；证明完成/双陈述先行与双读后内审；无standing fatal；外审未记录/新颖性未认证。


绑定Exact SHA `051148816053f0c150ee70c9efa1b3f7cb76ecc46b999d793155b4070e3cd065`，ID `UM-TWO-SMALL-INCIDENCE-SHARP-APPROXIMATION-v2`。root先据hardness_route的阈值陈述独立推出以下slot证明、OPT全区间包装和3DM下界；尚未读该作者的slot proof。之后其找到Page–Solis-Oba–Maack2018相关flow-plan论文，root已见该prior摘要，非零信息盲审、不认证原创。给shared/literal的只有本Exact，本文在未收到其本次推导前冻结，之后才交读后攻击。

### 7.1. 零、空与所有OPT<b的精确解

凡某job有零端，任选该零端直接安排并从剩余求解子问题移除。可在任何调度上把它改到此零端，原其它负载只减，故最优值恰等于剩余实例最优值；最后加回这些job不增任何负载。每machine的positive small资格数不增加。若无剩余jobs，返回完整zero调度，OPT0，包含原n0。

固定0≤T<b。所有unit端b不可能用于C≤T调度；small端p>T也删除。每machine剩至多两枚eligible jobs。若有两枚且处理时间和≤T，给该machine整数容量2；其余非空行容量1，空行容量0。建job→machine资格图，job需求1、machine上述容量，求一次整数b-matching/flow。它覆盖全部jobs iff存在实际C≤T调度：任何合法调度按容量可行；反向每行至多两候选，容量2只在两者之和≤T时允许，否则至多一个且该端已≤T。按matched端分配给完整σ。失败的Hall/mincut证书说明OPT>T。

T∈[0,b)时可行性只在有限阈值集改变：0、所有small资格值q、每行两small值之和q+q′（只收<b的值）。每行最多两small资格，所以此集O(m)，真实编码位长受输入控制；若一个job没有small端，所有这些阈值匹配都自动失败。对排序去重后的阈值作单调查找；若某阈值可行，最小者就是OPT<b的精确值，返回其真实调度。若全失败，则OPT≥b。无需按b的数值循环，没有OPT oracle。T0、singlejob/singlemachine均同式。

### 7.2. b≤T<2b的精确配置LP可显式列出

写T=b+a、0≤a<b。在此范围每machine配置至多一个unit job，其余至多它的两枚small资格任务。每行枚举small子集S（至多4个），以及“无unit”或每一个实际unit资格job j，保留总时长≤T的真实配置。变量总数≤Σ_i4(1+|U_i|)，是完整输入的多项式；unit job即使在别机有small资格，也仍逐原job身份计覆盖。每machine配置权重和1，每原job覆盖恰1，非负，得到真正普通CONFIG(T)而非只必要的load松弛。

若整数C≤T调度存在，它直接给可行点；LP infeasible因此可报告FAIL、保证OPT>T。反之可行时用标准确定性有理LP方法选bit长多项式的一份有理点，求原assignment marginals x_ij，每job和1，所有端合法。设每machine Q_i=Σ_jx_ij；因每配置最多3jobs，Q_i≤3。下面构造把该分数点变成实际低负载σ，不冒称LP feasible⇒OPT≤T。

### 7.3. 有序槽匹配，保原unit身份

每machine按processing time非增排序其x_ij>0资格（ties按原jobID），在长度Q_i线上顺序放宽度x_ij的job片段；切成ceil(Q_i)个长度≤1的槽。每job与所有有正片段交叠的槽相连。原片段给job需求1、slot容量1的分数matching，因此Hall条件成立，整数二分matching可覆盖全部jobs。把matched槽还原为原machine，得到完整真实σ，job不会重复，所有端finite。

零概率资格忽略。单位端时间b大于所有small端，且CONFIG(T<2b)的unit总边际≤1，因此所有unit片段均在第1槽中；每machine最多round到一个unit job。这不合并真实unit jobs或额外复制容量。每row至多3slots，图与有理比较均为总位多项式。

### 7.4. 逐行完整负载上界3b/2+a

先看Q_i>2的行。因为Q_i是配置中job数量的期望、每配置最多3job，此时至少一个正权配置含3job。这只能是一枚unit和该行的两枚small jobs p,q，故b+p+q≤T，即p+q≤a。最终这行最多一unit及原两small，因此不论具体matching，负载≤b+p+q≤T≤3b/2+a。

现在Q_i≤2，所以最多round到2jobs。定义big关联为unit端，加上所有small端p>b/2+a。在任一CONFIG(T)中这些big关联至多一个：unit加这样的small已超过T；两枚这样的small之和>b+2a≥b+a=T；两unit也超过T。因此big总边际≤1。它们在排序中先于其它small（unit先于全部small），故全在第1槽；最终至多一个big。

若行含一个big，另一个job必small且p≤min(b,b/2+a)，行负载≤b+(b/2+a)=3b/2+a。若不含big，两个job都是small，各≤min(b,b/2+a)，其总量也≤3b/2+a：a≤b/2时，2(b/2+a)=b+2a≤3b/2+a；a≥b/2时，2b≤3b/2+a。只有0/1job时更显然。Q_i恰2、恰整数的槽边界都按半开片段，不产生第三槽。

故全machine同时C≤3b/2+a≤(3/2)(b+a)。若LP infeasible则FAIL，若可行则明确输出全部原jobs调度；其输入无需YES witness。所有资格可任意共享、每job可多small、多unit，证明只用每行positive small资格最多2与common最大b。

### 7.5. 包装成所有OPT的三半算法

先第7.1节精确查OPT<b；成功则已最优。否则OPT≥b。

对T∈[b,2b)的CONFIG(T)，所有配置负载只能是unit位0/1加本行small子集之和。收集全部落在[b,2b)的b及q、q+q′、b+q、b+q+q′等真实配置阈值，至多O(m)个、bit长多项式。排序后求最小LP可行阈值τ（单调二分亦可）。若存在，调用第7.2–7.4节输出≤(3/2)τ。若OPT<2b，其真实整数配置保证τ≤OPT；若OPT≥2b，则τ<2b≤OPT。故此分支总≤1.5OPT。

若这些阈值均infeasible，则任何T∈[b,2b)都不可行，结合第7.1节可知OPT≥2b。求普通assignment loadLP的最小目标L：Σ_i x_ij=1、Σ_jp_ij x_ij≤L，每job仅finite端。它总可行有有限有理最优点，且L≤OPT。令target τ=max(2b,L)≤OPT；用相同有序槽匹配对其fractional point舍入。标准load估计在此自足可证：slot k≥2选中job的时间≤前一完整slot k−1任一片段的时间，故≤其加权平均；把各k的前一槽积分相加≤原fractional load≤τ。第1槽若选中job再加至多b。因此每row实际≤τ+b≤1.5τ≤1.5OPT。

此大目标分支slot数至多n+m，标准matching仍位多项式。所有LP、有限阈值、有理排序和matching均deterministic，总编码长多项式；不按binary处理时间数值展开。没有要求输入实际包含一个b端；b即使松上界也不破任何不等式。最后加回zero jobs，保持相同负载。

### 7.6. 同结构类的3/2困难性

导入标准非空perfect3DM：互异坐标集A,B,C同大小q≥1，显式triples E⊆A×B×C。若某A点无triple，可直接输出合法常量NO：一machine、两unit jobs、b1、OPT2、small资格0。通常困难族可先排除此情况。

对每a∈A建一个unit selector，它仅可在所有含该a的triple状态根machine M_e执行，time1。每个triple e=(a,b,c)有独立根M_e及两枚不同leaf jobs：各在M_e时间1/2，分别在共同resource B_b与C_c时间1，其余∞。没有其他jobs/端。机器为全部M_e及B/C resources，所有finite时间仅1/2或1。每M_e正small资格恰2，其它machine为0；unit资格数量任意，属于Exact类，所有job合法。

若perfect3DM存在，把各a的selector放所选triple根，并把该根两leaf外送相应B/C，所有未选根两leaf父置。选中根负载1，未选根两small总1，每resource接至多1unit，得到实际C1。q非空使selector下界1，故YES其实OPT1。

反之若有实际C<3/2，每a的selector所在根不能再留任何small1/2，因此该根两leaf必须都外送；每resource不容两unit。各a所选triples于B/C均互异，共q个，正是perfect3DM。因此NO的全部合法调度C≥3/2。输出size按q+|E|多项式（dense P仍多项式），所有数位常数。

任何固定ρ<1.5的近似算法会在YES输出C≤ρ<1.5，在NO无法输出这种合法调度；精确回算load即可判perfect3DM，故除非P=NP不存在这样的位多项式算法。该下界只给结构类三半sharp，不排一般UM的所有2−ε，也不借配置gap作hardness。

### 7.7. 已发表框架的实际扣除

Paper Fact：Page–Solis-Oba–Maack COCOA2018 accepted author稿，摘要、§6/Fig.5/Theorem2，PDF8–11已实际核读。原定理对每机器全部资格至多2/3/4给exact/3/2/5/3；其正整数模型并非本无限unit/任意有理/zero域的字面陈述。本处为直接machine-plan推广，不能自称新算法框架。

Fig.5保留每个真实job节点，用容量1的big-buffer进入machine。对b≤T<2b按p>T/2分类：threshold-small≤1时允许一个big及该small，负载≤b+T/2。threshold-small恰2时，它们就是本行两枚非unit资格，故所有big恰为共同b；若b加两small总和≤T，允许big-buffer1及总数3，否则big-buffer1及总数2。所有实际T调度嵌入，任意满流负载≤max(T,b+T/2)≤3b/2+a。若原small升级为threshold-big，则threshold-small≤1已覆盖。没有把原unit jobs合成一个全局代理；任一job可跨行具有不同角色。该适配严格限common-b，不推广到任意不同big时间加两threshold-small。

低/大OPT分支、zero删除、binary总位复杂度与同域3DM下界由上文自足证明。ordered slots、标准有理LP、整数matching、Karp3DM及已发表machine-plan均明确扣除。root先推导不认证新颖性；此资产为精确结构合同/既有方法推广，外审、新颖性及论文价值未认证。独立flow审计原型不实现通用CONFIG-LP生产求解器。一般UM-TARGET-v1正反面仍OPEN。

Related Files：[实际审查](../../reviews/unrelated_machines/joint_slot_prefix_review.md)、[独立流审计](../../../tests/audits/unrelated_machines/two_small_incidence_flow_audit.py)、[root真实重跑冻结输出](../../../evidence/runs/unrelated_machines/two_small_incidence_flow_audit.json)。六份原字节源见source_crosswalk。有限测试仅checks，不是普遍证明。
