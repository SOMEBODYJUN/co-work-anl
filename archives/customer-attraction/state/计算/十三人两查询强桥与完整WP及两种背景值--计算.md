---
id: customer-attraction/thirteen-provider-pair-bridge-full-WP-and-two-background-values
kind: computation
type_tag: 计算
title: 十三人两查询强桥与完整WP及两种背景值
status: pair-bridge-false; fixed-WP-safe; fixed-minimax-exact; universal-individual-bridges-false; aggregate-path-open
summary: 同SHA完整十三人SPE有pair29/11>根5/2，但完整WP最大1423/605，完整根背景25/11，全部整数十三槽混合9925/4586。保三域、历史63面求值及后续保险反族，不能把逐根失败传到全路径聚合。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c57321db16eb40e9867cee444f322c62/relay/algebra/README.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-c57321db16eb40e9867cee444f322c62/relay/algebra/README.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c57321db16eb40e9867cee444f322c62/relay/algebra/clone_chain_identity_and_boundary.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-c57321db16eb40e9867cee444f322c62/relay/algebra/clone_chain_identity_and_boundary.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c57321db16eb40e9867cee444f322c62/relay/algebra/extra_one_pairwise_counterexample_and_values.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-c57321db16eb40e9867cee444f322c62/relay/algebra/extra_one_pairwise_counterexample_and_values.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c57321db16eb40e9867cee444f322c62/relay/algebra/packet_extra_one_report.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-c57321db16eb40e9867cee444f322c62/relay/algebra/packet_extra_one_report.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c57321db16eb40e9867cee444f322c62/relay/algebra/probe_packet_extra_one.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-c57321db16eb40e9867cee444f322c62/relay/algebra/probe_packet_extra_one.py
---

# 真根叶与三个不同量词

按[完整历史模型](../定义/共同目录完整历史模型--定义.md)，固定完整m人纯SPE σ、actual根利润u。强制合法根行动Q后沿**同一σ**真实完成全m槽叶Z(Q)，不删除根/当前槽。独立额外查询价格
\[
 f_T(Z)=\sum_{x\in T}{1\over1+c_x(Z)},\quad M(T,Q)=f_T(Z(Q)).
\]
下标extra-one指静态额外查询，不增加真实玩家。三个合同分别是：

|量|查询与背景的选择顺序|背景域|
|---|---|---|
|WP(p)=pᵀMp|Q、T从同p独立抽取|真实根菜单，背景分布被绑成同p|
|M_root^full=min_q max_T E_qM(T,Q)|先选q，后取查询|真实根强制行动的完整叶|
|v_(m+1)=min_q max_T E_q f_T(Z)|先选q，后取查询|所有合法**整数m槽**静态背景的混合|

两查询pair只取交叉项；它不等WP。自由整数背景不要求由σ可信产生，但必须由m个合法标签构成；同覆盖异标签仍可不同记忆动作。它也不等允许自由分数边际的δ_(m+1)。有限零客户也合法，此时这些价格为0。

# 同SHA完整十三人策略的输入身份

标签顺序(A,B,T,D,E,P)，13单位提供者，8单位客户类型为A:2、B:2、T:1、TD:1、TE:1、ADE:3、BDE:1、P:25，共36客户。目录共同且非空，类型重数表示不同单位客户。所有客户由至多13个主题覆盖，且六标签已覆盖全部，所以OPT₁₃=36。

旧packet gzip372216B的SHA256为`bad2b15d1abe89d9fa8671df84de8638a4b1ca46279712baa5482abb2bdf18ce`。成熟[同SHA固定证书](../程序/两预算菜单原审计的顶层执行与十三人固定证书--程序.md)已绑定完整自动机及112050项比较；本批复用，不再次运行或逐27243节点手工重认证。27243是自动机node数（18675决策、8568终端），18675×6=112050含self比较；六条真child且深度增加、覆盖全部node使其展开为每份ordered历史的完整策略，不是把同count状态擅自合并。

actual P¹⁰AAB，前12位各5/2、末位3，W33；六根强制行动自身收益均5/2。根完整叶逐行是

|根行动|主题count(A,B,T,D,E,P)|
|---|---|
|A|(2,0,1,0,0,10)|
|B|(1,1,0,0,1,10)|
|T|(1,0,1,0,1,10)|
|D/E|(1,0,0,1,1,10)|
|P|(2,1,0,0,0,10)|

D/E相同终负载仅用于此矩阵求值，不给任意前缀的匿名策略归约。

# 完整矩阵与两查询失败

按客户定义直接计算（行是独立query，列为根行动）：

|T\\Q|A|B|T|D|E|P|
|---|---:|---:|---:|---:|---:|---:|
|A|5/3|2|2|7/4|7/4|5/3|
|B|3|4/3|5/2|7/3|7/3|3/2|
|T|3/2|5/2|4/3|2|2|3|
|D|5/2|7/3|2|19/12|19/12|5/2|
|E|5/2|11/6|11/6|19/12|19/12|5/2|
|P|25/11|25/11|25/11|25/11|25/11|25/11|

Z(P)未覆盖T/TD/TE三客，故M(T,P)=3；Z(T)有十P，故M(P,T)=25/11。其交叉均值29/11=5/2+3/22，直接反驳“任意两查询交叉平均≤真实根利润”。该失败在空前缀的合法完整SPE，未用非单位参与者。

完整p=(T+P)/2的四项均值却为293/132<5/2，不能丢两个对角信用再称WP反例。更一般令D(T)为真实根选择T的收益，则对全部分布p逐项展开
\[
 u-p^TMp=\sum_Tp_T[u-D(T)]+\sum_Tp_T^2[D(T)-M(T,T)]
 +\sum_{T<Q}p_Tp_Q[D(T)+D(Q)-M(T,Q)-M(Q,T)].\tag{CROSS}
\]
首项由根全行IC非负；第二项因在含T的真叶再插入查询分母增加而非负。最后跨项可负，本点即如此；一般copositivity仅重写这笔尚需全树付款的cross债。

# 本矩阵完整WP安全及原63面精确最大值

安全有短解析证书，不依赖重新求值。置H=(M+Mᵀ)/2、K=(5/2)11ᵀ−H。逐读上表可见除TP/PT条目−3/22外皆非负。将两个对角一并取出，相关二次式
\[
 {7\over6}p_T^2-{3\over11}p_Tp_P+{5\over22}p_P^2
\]
的对称矩阵正对角、行列式179/726>0，故非负；其余系数对p≥0非负。因此所有p都有WP(p)≤5/2。

原报告更精细地存**这个有限矩阵**的最大值1423/605，在p_T=12/55、p_P=43/55处取到，距u尚179/1210。该面上直接式为25/11+(8/11)t−(5/3)t²。全局上界的原有限审计遍历63个非空支持I的有理驻点系统H_Ip=λ1、Σp=1。任意全局最大点取其正支持，位于该面相对内部，必满足该系统；原码不要求每个驻点是局部极大，只取全部候选最大，故覆盖全局。全部31个非负唯一解、4个一致奇异面的值与向量均保原JSON：

|支持大小|非负唯一解数|最大保存值|
|---|---:|---:|
|1|6|25/11|
|2|12|1423/605|
|3|6|1912/927|
|4|5|10445/5064|
|5|2|18175313/8812551|
|6|0|无|

四个奇异支持DE/ADE/DEP/ADEP的λ分别19/12、1081/576、12175/5324、−16175/363。原有理高斯消元对每个齐次方向断言λ分量0，故一致仿射解集λ恒定；即使其非负部分为空，把该值纳入只会扩大上界。原63面入口本批0次；这些精细逐面字段是完整实读冻结报告与算法合同，不冒本次独立重算。上段简单PSD证书另自足承担所需WP≤u。

# 完整根菜单25/11的匹配双证

纯query P对每个根叶恒25/11，给M_root^full≥25/11。反向独立背景混合q=(62/77)Z(B)+(15/77)Z(T)，使六纯query价格
\[
 (2,103/66,25/11,524/231,11/6,25/11)
\]
均≤25/11。因此M_root^full=25/11。这里背景仍全部**13**槽，根的那一份保留；不是12个竞争者的删除式，也不是只沿actual叶的单列。

# 全部整数十三槽混合9925/4586

所有整数counts非负、总和13，共C(18,5)=8568列；这是顺序可按终价格取商的**静态**列域，不是对完整策略取商。原匹配query
\[
 p=(200,225,200,75,75,1518)/2293
\]
及下列六背景（公共分母20637）给值t=9925/4586：

|counts(A,B,T,D,E,P)|背景权分子|
|---|---:|
|(0,0,0,1,1,11)|1826|
|(1,0,0,0,1,11)|4326|
|(1,0,0,1,0,11)|5674|
|(1,0,0,1,1,10)|2892|
|(1,1,0,0,1,10)|1348|
|(1,1,1,0,0,10)|4571|

六权正且和20637，每count和13。按上列混合，六纯query价格均t，给上界。query下界对任意c=(a,b,z,d,e,f)精确写为
\[
2293G_p(c)={400\over1+a}+{450\over1+b}+{200\over1+z}
+{275\over1+z+d}+{275\over1+z+e}
+{1050\over1+a+d+e}+{375\over1+b+d+e}+{37950\over1+f}.
\]
成熟同点[8568列固定证书](../程序/两预算菜单原审计的顶层执行与十三人固定证书--程序.md)已保每列G_p≥t及达等，不重扫。原新probe也有同一匹配Fraction合同；其LP只是支持发现，之后有理恢复/全列检查才承担精确证据。综合得到本点
\[
 v_{14}=9925/4586< M_{root}^{full}=25/11< u=5/2,
\quad \max_pWP(p)=1423/605<u.
\]
自由整数静态混合、真根菜单混合和同p二次平均不能按名字合并。

# 旧开放状态的后续修正与仍开放范围

源2026-10-22只说明本点没有反WP/M_root/free桥，其当时一般OPEN是历史。后续[保险族完整根值](../反例/保险族完整根额外槽菜单的精确值与逐位置分离--反例.md)对每m≥2给成熟完整SPE，u1=1+1/(m−1)、W2m、OPT3m−2，并有解析匹配值
\[
 M_{root}^{full}=2-1/m-1/[3(m-1)],\quad
 v_{m+1}=3/2-1/[3(m-1)],\quad
 \delta_{m+1}=3/2-1/(2m-1).
\]
从m4起M_root^full>u1；m4更有δ5=19/14>u1=4/3，所以v5>u1。安全query的下界对所有合法静态列（包含全部真根叶）成立，取背景也用同p，即得该完整SPE某p的WP(p)>u1。因此“每个实例每个实际位置WP≤u_i”“M_i^full≤u_i”“v_(m+1)≤u_i”三种一般逐人桥均已假；不只是pair强化失败。

保险根精确值却始终小于W/m=2。允许在**全部actual位置**自由选完整叶的M_path≤W/m，以及Σ_i min_A E_p f_T(Z_i(A))≤W这类SUMmin-full共同预算，仍不能由逐根失败关闭。也不能把本m13的历史安全点当六人half的新证据。当前模型允许同覆盖不同标签，保险族本身覆盖不同，无借别名绕域。

# 原程序合同、独有内容与接续

7743B probe_packet_extra_one有main guard、固定旧R-171 packet路径，先按node真实children从深到浅重建leaf，全部18675×6 Fraction IC；不使用desired，但不像成熟另实现那样显式断言任意输入的全root-reach/schema，固定原件可信性依同SHA成熟认证。继而算本页完整6×6矩阵、63面有理RREF、全部8568静态列，并两次SciPy linprog发现支持，再按Fraction高斯消元恢复query/value、dual权、检查全部列。它不是纯只读算术入口，执行会重复成熟IC/LP/全列，所以本批0运行、0import/--help。

完整9312B原JSON保source_sha256、全部31驻点/4奇异面/矩阵/两种匹配证书；stdout有意去掉矩阵和逐面大字段，不可称完整报告逐字节重放。原报告所称独立重建是历史执行身份，没有本次argv/exit/环境的新绑定。独有可复用内容是pair与WP分离、对角税/CROSS恒等式、这个有限矩阵全支持求值及完整根25/11双证；同8568静态值/完整SPE可信性则复用成熟成功。

继续构造跨前缀运输时须携带“具体前缀×查询”的联合分布与同一全行权；child-WP只在一个固定前缀和同p上陈述，不能把不同前缀各自的实际A_Q并成无条件scalar再套。当前逐人WP已否，若改做全路径聚合须另写准确量词、保全部对角信用与actual-only预算，不能仅改目标名称。完整原件与0执行账见[证据](../../tools/evidence/real-history-clock-relay-single-kernel-and-packet-primary/README.md)。
