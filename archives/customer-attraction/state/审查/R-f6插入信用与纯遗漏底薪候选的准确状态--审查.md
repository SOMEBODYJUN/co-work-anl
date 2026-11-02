---
id: "customer-attraction/f6-insertion-credit-and-pure-omission-floor-candidate-status"
kind: "review"
type_tag: "审查"
title: "R-f6插入信用与纯遗漏底薪候选的准确状态"
status: "unscaled-single-query-and-pure-omission-strengthenings-refuted-by-mature-other-inputs;optimal-min-fresh-candidate-not-refuted-here"
summary: "重构README、ghost_probe与search_missing_floor的精确量：mF≤W+V就是已被十三人反驳的ENT1；D≤m min u的纯遗漏加强被71客户唯一最优例否定，净缺口仍安全；存在最优min-fresh预算保持不同量词。两探针均无冻结执行报告。"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-f6e401683adb4a76a4bd4d8022713582/README.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-f6e401683adb4a76a4bd4d8022713582/README.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-f6e401683adb4a76a4bd4d8022713582/strategic_tree/ghost_probe.py", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-f6e401683adb4a76a4bd4d8022713582/strategic_tree/ghost_probe.py", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-f6e401683adb4a76a4bd4d8022713582/direct_global/search_missing_floor.py", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-f6e401683adb4a76a4bd4d8022713582/direct_global/search_missing_floor.py"]
---

# R-f6插入信用与纯遗漏底薪候选的准确状态

## 静态插入、自留信用与half的正确充分式

在[单位客户完整历史模型](../定义/共同目录完整历史模型--定义.md)固定m≥1及一份完整纯SPE的实际终局s，实际覆盖集U、负载c_x、W=|U|=Σ_i u_i。定义
\[
 f_c(T)=\sum_{x\in T}\frac1{1+c_x},\quad
 F(c)=\max_{T\in\mathcal S}f_c(T),\quad
 V(c)=\sum_{c_x>0}\frac1{1+c_x}.
\tag{1}
\]
这是对完整m槽终局外再插一个静态查询的价格，不是把在轨某玩家移走，也不是其真实偏离续局收益。设比较m元组T的客户负载为d_x。逐客户
\[
 1_{d_x>0}\le\frac{d_x+c_x}{1+c_x},\qquad
 \sum_x\frac{c_x}{1+c_x}=W-V.
\]
求和得
\[
 |\cup_jT_j|\le\sum_j f_c(T_j)+W-V\le mF+W-V.
\tag{2}
\]
所以原README的候选
\[
 mF\le W+V\tag{ENT1?}
\]
若成立足half；这是一个更强预算，而不是half等价式。它保零客户时加法0≤0，不定义0/0效率比。

较弱的存在量词是：存在某个**覆盖最优**m元组T满足Σ_j f_c(T_j)≤W+V。因目录有限，令
\[
 K_0=\min_{T:\,|\cup_jT_j|=OPT_m}\sum_j f_c(T_j),
\]
则该存在版恰为K0≤W+V，见[成熟自留份额候选](../想法/最优覆盖查询的自留份额预算--想法.md)。对每个给定最优元组均要求该式更强；把最大单query重复m次也未必覆盖最优。三种量词不得互换。

本静态推导没有使用SPE，因此它只说明桥若成立的用途。要证明预算仍须付从完整历史真IC到冻结插入价格的额外义务，不能直接让u_i支付f_c(T)。

## ENT1的一般开放状态应纠正为已被后续完整例否定

原1854B README将mF≤W+V记待攻击，2358B ghost_probe.py正对它作固定策略锥攻击。但[已发表SAIC同一性审查](实际终局插入预算与未缩放税桥的同一性--审查.md)完整追到十三人36客户证书，且本式与其ENT1逐符号相同。该成熟输入的六主题为A,B,T,D,E,P，客户类型A2、B2、T1、TD1、TE1、ADE3、BDE1、P25；m=13，实际路径P十次、A两次、B一次。

已认证完整策略给W33、OPT36；实际负载桶是5客户负载二、3客户负载一、25客户负载十、3客户未覆盖。由这些桶及类型，
\[
 V=\frac5{3}+\frac3{2}+\frac{25}{11}=\frac{359}{66},\quad
 (f(A),f(B),f(T),f(D),f(E),f(P))
 =(5/3,3/2,3,5/2,5/2,25/11).
\]
故F3，
\[
 mF-W-V=39-33-359/66=37/66>0.\tag{3}
\]
同一点若福利归一W1，目标是37/2178；若总客户质量归一1，目标是37/2376。本原ghost LP恰采用**总质量1**，不能借另一个W1程序的数值直接称其本轮输出。

成熟同SHA packet已作完整自动机闭合及112050项含自身IC核；本次只复用充分的资格证明与实际目标绑定，不解压重算、不跑原十三人程序。它不是本source发现的新反例，也不在ghost原m∈{2,3,4,5}范围。half余量2W−OPT=30，故它不反主half；当前六人ENT1限制域也不由这个十三人点判定。重复T十三次只覆盖T，不能将(3)迁移为min-fresh K0候选失败。

README另说更强mF≤W被已有两人残余例否定：W9且未覆盖主题含5客户，F≥5使2F≥10>9。此处原转述只作旧入口关系；本轮未重读该残余证书或登记新资产。比起沿用这条导航当新证明，当前ENT1精确状态由上面已全文比较的独立成熟对象承担。

## ghost_probe.py实际构造与缺少的结果

程序scan默认seed67、trials300，每轮p∈{3,4,5,6}、m∈{2,3,4,5}。对每个非空兴趣mask，频率≤2时以0.7概率保留，较密型以0.15保留，重数均匀1…19。用规范ExactSPESolver求**全部**SPE根终局，从中随机一个，再用两个随机选择器构完整σ；不是只取最坏SPE或count统一σ。种子instance用于生成策略，换质量后固定σ，不要求仍为新实例最坏。

build()逐每个有序h/非自身动作重放两真实终局，使用Fraction形成Γ，再转float作LP。对每个单query T最大化
\[
 \sum_Bw_B\left[
 {m1_{T\in B}\over1+c(B)}-
 {1_{c(B)>0}\over1+c(B)}-1_{c(B)>0}\right]
 =m f_c(T)-V-W,
\tag{4}
\]
其中c(B)是实际路径中属于兴趣型B的行动次数。约束w≥0、Γw≥0、Σ_Bw_B=1；非W归一。success且−fun>10^−8即输出并返回首个float候选，没有有理恢复、非负/归一精确检查或完整单位客户独审；导入verify_certificate但源码未调用它。阳性JSON会含trial/k/m/root/T/objective/seed_instance/weights/actions，但这11主源中无这种保存输出。不能宣称实际完成300轮、NO_COUNTEREXAMPLE或有一个正点；本次入口/import/LP/BI全0。

本程序与[朴素前缀幽灵租金核验](../计算/朴素前缀幽灵租金的精确核验--计算.md)的目标不同：后者按前缀累积旧ghost租金，本源是**最终完整负载**的单query插入预算。名称相似不构成同输入或反证迁移，当前状态靠(1)–(4)精确同一性。

## search_missing_floor.py：纯遗漏与净差的分界

1087B程序无main guard，导入即运行seed19024的至多3000轮。固定p6、m3；只允许兴趣频率≤2的客户，各型以0.55概率保留、重数0…11，其余型0。每轮规范ExactSPESolver枚举全部根SPE终局c，并枚举全部最优三主题多重集。对每个c，按占用标签收益取
\[
 u_{min}=\min_{i\,\text{实际玩家}}u_i
         =\min_{a:c_a>0}U_a(c),
\quad D=\max_{O\text{为最优覆盖并集}}|O\setminus U|.
\tag{5}
\]
判FAIL的条件是m u_min<D。这里max取最优比较中最大的**纯遗漏**，不是OPT−W；由于Σc=m3，占用标签非空，min有定义，即使零客户时也只是u_min0。原源码调用ExactSPESolver.outcomes()，因此它不排除非count历史SPE。

若纯遗漏加强D≤m u_min对所有最优并集成立，则令E(O)=|U\setminus O|，有OPT−W=|O\setminus U|−E≤D≤m u_min≤W，足half。但要求付D比付净差更强。该全人数加强已经被[71客户唯一最优遗漏族](../反例/唯一最优组合的全遗漏支付--反例.md)直接否定：取成熟两人六主题族k=3，其完整策略根A、末位回复A→B/B→S/T→R/Q→S/R→S/S→R；actual AB收益16、19，所以m u_min32。唯一最优TQ给
\[
 W=35,\quad OPT_2=38,\quad D=36,\quad E=33.
\]
于是36>32，连存在有利最优比较也无法满足这项纯遗漏付款。该成熟族的七节点完整资格和全部主题对最优性充分复用，本次0重跑；它是原模型内**辅助桥**反例，不是当前原程序实际找到的FAIL，且m2不在固定m3扫描范围。

相反净差D−E=3≤32。这个例子完全不反[逐人净缺口](../程序/逐人覆盖地板与净缺口的完整策略锥探针--程序.md)的OPT−W≤m u_i，也不反B11的同一净差路线。目录六主题不是六名提供者；71客户点half余量32，主六人半覆盖不因此失败。

原程序stdout如发现严格失败会打印完整w/counts/OPT/W/D/u并SystemExit，否则每50轮打印进度，全部完成才打印none。未保存报告或stdout，不能由文件存在断言3000轮已运行/没有失败；本次不导入、不补跑随机搜索。该文件有价值的内容是准确目标、枚举量词与可复用发现接口，原无结果缺口照实保留。

## 来源、证据级别与接续

三primary完整字节与双冻结精确source均在[证据](../../tools/evidence/f6-fixed-count-and-credible-policies-primary/README.md)。本页的(2)、(3)、(5)和36>32是显示的解析推导，0新数学程序调用；本批唯一独立运行只核另四个原分数策略点，没有运行这两个探针。一般ENT1和一般纯遗漏加强当前均假；min-fresh存在最优候选、逐人净差及六人half各保自己的未付义务，不以一个旧导航OPEN状态或不同归一的扫描数字替代结论。
