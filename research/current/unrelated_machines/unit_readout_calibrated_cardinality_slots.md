# 单位读出双树的校准计数槽与有界密度次二算法

读取目的：越过半密度三半界后，判断增加clause arity是否真的避开所有已知构造。这里增加一个**行分数任务数的整数预算**，使用经典ST有序槽直接舍入；均匀校准将上一份d≤2A障碍推到更多密度/目标组合，且对每个固定密度上界D给此结构类统一次二算法。不是一般UM-TARGET-v1，也不把标准ST/LP工具称为新算法技术；外审、新颖性和独立论文价值未认证。

## 1. 对象和分数计数证书

完整原模型沿[单位读出森林](unit_readout_pruned_forest_boundary.md)：每变量两棵私有满k叉深h树，k,h≥1；每变量一枚unit selector选两根；每内部edge job仅父端1/k、子端1；每leaf port仅父端1/k或其clause任一unit机器时间1。原资格恰此，不同clause外机互异，无其他jobs/pins。A_c≥0，可将外机数截q_c=min(A_c,d_c)，d_c是实际leaf arity。无job时添dummy。

固定整数1≤r≤k，定义L=k−r+1与C_r=2−r/k。对每枚内部edge/leaf port给有理下传分数t_e∈[0,1]，在父端的分配质量为1−t_e。每selector在两个根的分配质量y_+,y_−≥0，和为1。非根u的incoming质量y_u恰是父edge的t_e。证书要求同一组变量共同满足

    Σ_(e out of u) t_e ≥ r−1+y_u       (每内部机器u),
    Σ_(leaf e of clause c) t_e ≤ A_c  (每clause c).

第二行是unit任务数容量，不能用scalar1/A外端替换。第一行等价

    y_u + Σ_(e out of u)(1−t_e) ≤ L.

它是原机器上的**分数任务数量**，不是处理时间行负载。证书是一个多项式规模的有理线性系统；给任意显式有理见证时舍入按原P加见证总编码长度位多项式。若求证书，可用标准有理LP算法取得多项式位长的解；当前实现不冒称已经集成通用LP求解器。

## 2. 给定证书的完整实际舍入

**UM-UNIT-READOUT-CALIBRATED-SLOT-v1。** 对每个上述显式实例、每个1≤r≤k及每个满足第1节条件的有理证书，可确定性总位多项式输出每原job的具体合法目的地，全部内部机负载≤C_r，所有外unit≤1。这里的“总位”包括给定证书字节；不假定任意外给超长分数免费。此LP仅作充分证书，r>1一般不必要。以下均匀校准给按原P位长可构造的特例。

证明：每内部row先放incoming unit job的质量y_u，随后依固定顺序放k枚小job各质量1−t_e，切成长度1的槽，最后不足1仍算一槽。总长度≤整数L，故槽数≤L。incoming的区间从0开始且长≤1，因此它在本row至多邻首槽；质量0不产生边。一个小job可以分到两个相邻槽，**不能沿用每槽度≤2的半质量论证**。

每clause把ports的外送质量t_e依次切成长度1的槽，每槽映射到一个不同真实unit。只需ceil(Σt_e)≤min(A_c,d_c)台。port对每台本clause unit均有原资格，故所有这些分片合法；其余外机负载将为0。不展开binary A_c个无用unit。

现在每job的全部端质量恰1，每槽质量至多1。任意job子集S的总质量|S|全流入其邻接槽N(S)，每槽容量1，所以|S|≤|N(S)|。一次Hall匹配覆盖全部原jobs；按匹配槽所在真实机器输出整数σ。所有selector、内部edge、leaf port共同匹配一次，非逐机独立挑选。

若incoming选u，它只能占首槽，其他小jobs至多L−1=k−r枚，真实负载≤1+(k−r)/k=C_r。若incoming不在u，至多其原k枚小jobs，总负载≤1；更强槽数界L也足够。每外unit只有一个槽，实际至多一枚unit port，负载≤1。所有inactive树、未选sign及外机均已计费。

有理区间端点的加法/比较和切分按证书总位长多项式。每分片质量≤1，任一job在每端至多跨两槽；槽数和邻接边受显式任务数控制。匹配无需枚举分母数值或源赋值。

### 与仅分数激活条件的区别

不能把第一行减弱成Σout t≥r y_u而保留结论。k4,h1,r2，一变量、两根各四ports，每sign所有四ports同接一个私有clause unit，两个clauses各A1。selector两根各1/2，每port下传1/4满足弱条件和外容量，但真OPT7/4>3/2：选中根最多外送一port，至少三枚1/4留根；一枚外送达到。强计数行在此为1/2+4·3/4=7/2>L3，正确拒绝这份见证。

反过来强LP也一般非必要：k2,h1,r2，一变量四ports全接同clause A2。选择任一sign selector，两个该sign ports外送、另一sign ports内留给真C1。两根的强不等式相加却要求Σleaf t≥2+(y_++y_−)=3>A2，故该LP不可行。4机器5jobs的实际最优值1并不被一个不可行的充分LP反驳。

## 3. 深度校准的显式有理证书

令x_0=1/2，每一sign树的深l下传质量统一为

    x_l = (r−1+x_(l−1))/k,   l=1,...,h.

selector两根各1/2，深l内部edge或leaf的下传为x_l。每内部row的分数数量恰L，因为k x_l=r−1+x_(l−1)。k1必r1，所有x_l=1/2；k>1令a=(r−1)/(k−1)，则

    x_h = a+(1/2−a)/k^h ∈[0,1].

因此，只要每clause满足d_c x_h≤A_c，就有完整实际C≤2−r/k调度，**所有wiring**均覆盖。计算分母的位长O(1+h log k)，非空显式树/完整叶路径已含这些长度；空变量先输出0，不能为不存在的树计算巨大k^h。

这是真比半密度更宽的证书，仍是ST工具推论。例如k4,h3,r2时x_h=43/128，因此d_c·43≤128A_c就足够普适三半，不只d≤2A。没有声称此密度条件必要，也没有由固定部件推出一般UM近二困难性。

### 受限的严格YES必要性

k>1，另假设每clause有a d_c≤A_c。若原实例有实际C≤1，selector所选sign整棵树的所有jobs必须下传；令s∈{0,1}是某sign根是否被selector选中，t_c为clause中这些被选sign的leaf数，必t_c≤A_c。把该sign深l分数改为a+(s−a)/k^l，根incoming取s，则所有row不等式取等，clause总分数为

    a d_c(1−1/k^h)+t_c/k^h ≤ A_c.

所以在这个额外密度域内，数学上LP不可行能证明OPT>1。此处并未说所有OPT>1都拒绝、未把数值求解失败当数学不可行，也未将该一次阈值推导冒称一般unknown-OPT搜索。前述4机5job非必要例违反额外a d≤A，二者没有冲突。

## 4. 固定密度上界类的统一次二算法

**UM-UNIT-READOUT-BOUNDED-DENSITY-SUBTWO-v1。** 对每个固定有理常数D≥2，在第1节模型内、所有clause满足d_c≤D A_c的结构类，有确定性总位多项式算法输出完整合法σ，

    C_max(σ) ≤ (2−1/(4D)) OPT.

算法不用未知OPT、源赋值或通用LP求解器；D可以作为显式有理输入，运行时间仍按其位长多项式，但只有D固定时该系数是类上统一常数。1/(4D)是一个方便的显式保证，不声称该类最优常数。

先处理无变量：此时无原jobs，输出空σ、负载0=OPT，不展开k,h或A数值。

若k≥D，则k≥2，取

    r = 1+floor((k−1)/(2D)).

有1≤r≤k，a=(r−1)/(k−1)≤1/(2D)，N=k^h≥k。于是

    x_h = a(1−1/N)+1/(2N)
        ≤1/(2D)+1/(2k) ≤1/D.

由d_c≤D A_c，第3节显式证书可行，舍入实际C≤2−r/k。因为1+floor z>z，

    r/k > (k−1)/(2Dk) ≥1/(4D).

非空实例每selector有时间1，故OPT≥1，得到所需比例。

若k<D，求一个普通容量匹配：左为变量，右为clauses，变量可连到其任一sign中存在原leaf path的clause；每变量需匹配一枚实际叶，clause容量A_c（可截至变量数/arity）。成功时为每变量取所配leaf的唯一root路径，只沿该sign该路径下传，其余所有jobs父置。每active机负载1+(k−1)/k=2−1/k，inactive机1，每clause实际选叶≤A_c、注入不同units，全部合法。此时2−1/k<2−1/D<2−1/(4D)，又OPT≥1。

若匹配失败，则任何C<2实际调度都会沿每selector选轨提取至少一条root到leaf的实际下传路径，叶继承外unit注入；不同变量树私有，这会给上述容量匹配，矛盾。故OPT≥2。将所有非selector jobs放parent，selector任放一根，负载恰2（根selector1+全部outgoing1；其他internal为1；unit0），所以OPT=2并已输出最优。k1同样覆盖：成功实际1，失败真OPT2。

整个算法的有理整数运算、分数槽、路径与容量匹配均按显式P和D的总位长多项式；A0在密度条件下只能d0，直接旁路。这里没有处理一般输入的无穷资格或零时间矩阵，因为这只是明确定义的正时间树结构类；空任务边界已给。一般UM目标仍包含这些额外对象并保持OPEN。

## 5. 来源扣除、证据与近二归约仍缺的内容

本页比裸配置T多使用：固定唯一incoming/统一small时间结构、可实际构造的整数行分数任务数预算L，以及外端共同unit资格。标准ST在这些明确证书上给实际C_r；没有证明一般矩阵可产生这样的结构或预算。双树配置gap趋2的封闭族不违反结果，其有效clause密度可随k增长，D不是固定常数。

与最近经典结果对照：已登记的Verschae–Wiese原文§4、Theorem7（PDF第9页/印8）对一般输入给2−gcd(p)/max(p)保证；本页非空时间集{1/k,1}只代入出2−1/k，所以不能把有界k改善称为新增机制。该已有因子在k增长时趋2，本页固定D结论仍允许k和h无界；其新增限定结构内容是可构造的校准基数证书和密度如何给统一余量，而非新的通用ST舍入工具。此比较不认证全球新颖性。

固定D类已有严格次二算法，因此一个要对任意小ε证明近二困难性的归约，不能只把所有输出困在同一固定D类。D随目标ε变化并非被禁止；这时还须实际保持非空YES并排除所有低负载mandatory森林。超半密度、不平衡源、常量及dummy的共同容量不能只靠源PCSP分类补齐。未证明UM-TARGET-v1的反面。

两项正式Claim的Objects、Domain、Quantifiers、Assumptions、Definitions、Scope、Conclusion及Dependencies如各节；Evidence为原P/完整σ/实际负载审计，Counterevidence为§2的非必要与弱条件反例。实际实现、冻结数学审查及软件范围见[审查](../../reviews/unrelated_machines/unit_readout_calibrated_cardinality_slots_review.md)。Status：限定范围自足证明、内部先陈述独立重构及最终全文攻击；无外审、全球新颖性或独立论文价值认证。所有旧冻结结果保持原字节。
