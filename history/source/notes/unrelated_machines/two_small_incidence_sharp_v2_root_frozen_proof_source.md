# 双small资格行的全类三半算法与匹配下界：root冻结证明

绑定Exact SHA `051148816053f0c150ee70c9efa1b3f7cb76ecc46b999d793155b4070e3cd065`，ID `UM-TWO-SMALL-INCIDENCE-SHARP-APPROXIMATION-v2`。root先据hardness_route的阈值陈述独立推出以下slot证明、OPT全区间包装和3DM下界；尚未读该作者的slot proof。之后其找到Page–Solis-Oba–Maack2018相关flow-plan论文，root已见该prior摘要，非零信息盲审、不认证原创。给shared/literal的只有本Exact，本文在未收到其本次推导前冻结，之后才交读后攻击。

## 1. 零、空与所有OPT<b的精确解

凡某job有零端，任选该零端直接安排并从剩余求解子问题移除。可在任何调度上把它改到此零端，原其它负载只减，故最优值恰等于剩余实例最优值；最后加回这些job不增任何负载。每machine的positive small资格数不增加。若无剩余jobs，返回完整zero调度，OPT0，包含原n0。

固定0≤T<b。所有unit端b不可能用于C≤T调度；small端p>T也删除。每machine剩至多两枚eligible jobs。若有两枚且处理时间和≤T，给该machine整数容量2；其余非空行容量1，空行容量0。建job→machine资格图，job需求1、machine上述容量，求一次整数b-matching/flow。它覆盖全部jobs iff存在实际C≤T调度：任何合法调度按容量可行；反向每行至多两候选，容量2只在两者之和≤T时允许，否则至多一个且该端已≤T。按matched端分配给完整σ。失败的Hall/mincut证书说明OPT>T。

T∈[0,b)时可行性只在有限阈值集改变：0、所有small资格值q、每行两small值之和q+q′（只收<b的值）。每行最多两small资格，所以此集O(m)，真实编码位长受输入控制；若一个job没有small端，所有这些阈值匹配都自动失败。对排序去重后的阈值作单调查找；若某阈值可行，最小者就是OPT<b的精确值，返回其真实调度。若全失败，则OPT≥b。无需按b的数值循环，没有OPT oracle。T0、singlejob/singlemachine均同式。

## 2. b≤T<2b的精确配置LP可显式列出

写T=b+a、0≤a<b。在此范围每machine配置至多一个unit job，其余至多它的两枚small资格任务。每行枚举small子集S（至多4个），以及“无unit”或每一个实际unit资格job j，保留总时长≤T的真实配置。变量总数≤Σ_i4(1+|U_i|)，是完整输入的多项式；unit job即使在别机有small资格，也仍逐原job身份计覆盖。每machine配置权重和1，每原job覆盖恰1，非负，得到真正普通CONFIG(T)而非只必要的load松弛。

若整数C≤T调度存在，它直接给可行点；LP infeasible因此可报告FAIL、保证OPT>T。反之可行时用标准确定性有理LP方法选bit长多项式的一份有理点，求原assignment marginals x_ij，每job和1，所有端合法。设每machine Q_i=Σ_jx_ij；因每配置最多3jobs，Q_i≤3。下面构造把该分数点变成实际低负载σ，不冒称LP feasible⇒OPT≤T。

## 3. 有序槽匹配，保原unit身份

每machine按processing time非增排序其x_ij>0资格（ties按原jobID），在长度Q_i线上顺序放宽度x_ij的job片段；切成ceil(Q_i)个长度≤1的槽。每job与所有有正片段交叠的槽相连。原片段给job需求1、slot容量1的分数matching，因此Hall条件成立，整数二分matching可覆盖全部jobs。把matched槽还原为原machine，得到完整真实σ，job不会重复，所有端finite。

零概率资格忽略。单位端时间b大于所有small端，且CONFIG(T<2b)的unit总边际≤1，因此所有unit片段均在第1槽中；每machine最多round到一个unit job。这不合并真实unit jobs或额外复制容量。每row至多3slots，图与有理比较均为总位多项式。

## 4. 逐行完整负载上界3b/2+a

先看Q_i>2的行。因为Q_i是配置中job数量的期望、每配置最多3job，此时至少一个正权配置含3job。这只能是一枚unit和该行的两枚small jobs p,q，故b+p+q≤T，即p+q≤a。最终这行最多一unit及原两small，因此不论具体matching，负载≤b+p+q≤T≤3b/2+a。

现在Q_i≤2，所以最多round到2jobs。定义big关联为unit端，加上所有small端p>b/2+a。在任一CONFIG(T)中这些big关联至多一个：unit加这样的small已超过T；两枚这样的small之和>b+2a≥b+a=T；两unit也超过T。因此big总边际≤1。它们在排序中先于其它small（unit先于全部small），故全在第1槽；最终至多一个big。

若行含一个big，另一个job必small且p≤min(b,b/2+a)，行负载≤b+(b/2+a)=3b/2+a。若不含big，两个job都是small，各≤min(b,b/2+a)，其总量也≤3b/2+a：a≤b/2时，2(b/2+a)=b+2a≤3b/2+a；a≥b/2时，2b≤3b/2+a。只有0/1job时更显然。Q_i恰2、恰整数的槽边界都按半开片段，不产生第三槽。

故全machine同时C≤3b/2+a≤(3/2)(b+a)。若LP infeasible则FAIL，若可行则明确输出全部原jobs调度；其输入无需YES witness。所有资格可任意共享、每job可多small、多unit，证明只用每行positive small资格最多2与common最大b。

## 5. 包装成所有OPT的三半算法

先第1节精确查OPT<b；成功则已最优。否则OPT≥b。

对T∈[b,2b)的CONFIG(T)，所有配置负载只能是unit位0/1加本行small子集之和。收集全部落在[b,2b)的b及q、q+q′、b+q、b+q+q′等真实配置阈值，至多O(m)个、bit长多项式。排序后求最小LP可行阈值τ（单调二分亦可）。若存在，调用第2–4节输出≤(3/2)τ。若OPT<2b，其真实整数配置保证τ≤OPT；若OPT≥2b，则τ<2b≤OPT。故此分支总≤1.5OPT。

若这些阈值均infeasible，则任何T∈[b,2b)都不可行，结合第1节可知OPT≥2b。求普通assignment loadLP的最小目标L：Σ_i x_ij=1、Σ_jp_ij x_ij≤L，每job仅finite端。它总可行有有限有理最优点，且L≤OPT。令target τ=max(2b,L)≤OPT；用相同有序槽匹配对其fractional point舍入。标准load估计在此自足可证：slot k≥2选中job的时间≤前一完整slot k−1任一片段的时间，故≤其加权平均；把各k的前一槽积分相加≤原fractional load≤τ。第1槽若选中job再加至多b。因此每row实际≤τ+b≤1.5τ≤1.5OPT。

此大目标分支slot数至多n+m，标准matching仍位多项式。所有LP、有限阈值、有理排序和matching均deterministic，总编码长多项式；不按binary处理时间数值展开。没有要求输入实际包含一个b端；b即使松上界也不破任何不等式。最后加回zero jobs，保持相同负载。

## 6. 同结构类的3/2困难性

导入标准非空perfect3DM：互异坐标集A,B,C同大小q≥1，显式triples E⊆A×B×C。若某A点无triple，可直接输出合法常量NO：一machine、两unit jobs、b1、OPT2、small资格0。通常困难族可先排除此情况。

对每a∈A建一个unit selector，它仅可在所有含该a的triple状态根machine M_e执行，time1。每个triple e=(a,b,c)有独立根M_e及两枚不同leaf jobs：各在M_e时间1/2，分别在共同resource B_b与C_c时间1，其余∞。没有其他jobs/端。机器为全部M_e及B/C resources，所有finite时间仅1/2或1。每M_e正small资格恰2，其它machine为0；unit资格数量任意，属于Exact类，所有job合法。

若perfect3DM存在，把各a的selector放所选triple根，并把该根两leaf外送相应B/C，所有未选根两leaf父置。选中根负载1，未选根两small总1，每resource接至多1unit，得到实际C1。q非空使selector下界1，故YES其实OPT1。

反之若有实际C<3/2，每a的selector所在根不能再留任何small1/2，因此该根两leaf必须都外送；每resource不容两unit。各a所选triples于B/C均互异，共q个，正是perfect3DM。因此NO的全部合法调度C≥3/2。输出size按q+|E|多项式（dense P仍多项式），所有数位常数。

任何固定ρ<1.5的近似算法会在YES输出C≤ρ<1.5，在NO无法输出这种合法调度；精确回算load即可判perfect3DM，故除非P=NP不存在这样的位多项式算法。该下界只给结构类三半sharp，不排一般UM的所有2−ε，也不借配置gap作hardness。

## 7. 已有技术与审核层级

Ordered slots、rational LP及matching框架均是LST/ST经典工具；本页局部cut、最多3slots与完整OPT区间合起来给明确结构合同。Page–Solis-Oba–Maack COCOA2018已对每机全部资格≤3给3/2、≤4给5/3，并有big-buffer machine-plan框架；它很可能已直接导出本common-unit代理扩域，必须按其实际全文扣除，不能自称全新算法机制。root本证明主链在获知该prior之前已自行推导，但这不认证新颖性。作者稿实际适用条件、版本及重叠另行核读。

这是完整数学算法及精确复杂性下界，生产实现/有限运行未做；外审、全球新颖性和独立论文价值未认证。正式目标UM-TARGET-v1在一般模型正反面仍OPEN。
