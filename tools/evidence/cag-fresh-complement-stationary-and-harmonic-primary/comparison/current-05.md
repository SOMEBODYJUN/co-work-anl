---
id: "customer-attraction/stationary-query-and-replicated-menu-finite-evidence-contracts"
kind: "resource"
type_tag: "资源"
title: "平稳查询与复制菜单的有限证据合同"
status: "complete-source-review; conditional-matrix-and-local-proof-preserved; full-cuts-source-report-only"
summary: "明确6286核的平稳/查询手算与原全IC审计边界，保条件复制矩阵的meta-NE、六向量有限分类及整数缩放/编码范围；局部last-low与14类遗漏已覆盖者精确duplicate，0新数学程序。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/round5_audit/stationary_column_candidate_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/round5_audit/stationary_column_candidate_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/round5_mixed/replicated_menu_minimax.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/round5_mixed/replicated_menu_minimax.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/round5_credible/last_low_cut_and_three_block_failure.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/round5_credible/last_low_cut_and_three_block_failure.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/round5_mixed/three_block_last_low_witness.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/round5_mixed/three_block_last_low_witness.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/exchange/unique_optimum_omission_obstruction.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/exchange/unique_optimum_omission_obstruction.md"
---

# 平稳查询与复制菜单的有限证据合同

## 来源与共同模型

本批五稿4495/6490/6701/3104/5359B，共26149B，均GS实际全文读，HF核同SHA逐项比较。有限单位客户、共同有限非空目录、单位提供者、全部有序历史纯SPE，保空主题、重复和任意离轨平局。原码、完整动作JSON或全部数值报告不能由一篇MD的“独立审计通过”代读。

本页补自足的平稳/查询复核、条件矩阵meta-Nash与有限分类/程序范围，既有完整数学见[真实分支账本](../资源/真实分支十项合同与菜单可实现性账本--资源.md)。没有新增实例或另冠同一个定理。

## 6286客户：固定槽核可以手算，完整SPE审计不代跑

该三人、六主题例的21类单位客户、43节点完整规则、六根真实列及所有数值已保在现账本。原策略形式与旧348客户例相同但重数不同；发现输入文件名`stationary_348_diagnostic.json`中的348不表示本输入仍348客户。独审称只读取其中query2条目的mask/重数，以及`high_insertion_2cycle_348_exact.json`的完整动作表；这是当时独立性的来源说明，不是HF新读取那两份JSON。

六个强制根列为
\[
Z_0=(0,3,4),\ Z_1=(1,3,4),\ Z_2=(2,3,4),\quad
Z_3=(3,0,1),\ Z_4=(4,0,1),\ Z_5=(5,0,1).
\]
P_BA=count_A(Z_B)/3，是source到均匀**完整三槽**的核。由这六列直接解pP=p：只有列2会流入标签2，故p_2=p_2/3=0；同理p_5=0。其余方程为2p_0=2p_1=p_3+p_4、2p_3=2p_4=p_0+p_1，归一化给
\[
p=(1,1,0,1,1,0)/4.
\]
这是当前对给定菜单的解析重建；后续发现稿b97b201c7a5d2373db80也明写这个解法。源独审的rank(Pᵀ−I)=5为另一有限核验报告，不必借未读报告才能解该核；但此手算没有核原43节点的全部激励。

查询2涉及的七种mask为4:550、12:229、13:99、29:396、36:380、44:237、46:132。对四个正概率列0/1/3/4独立查询，各型的平均倒数分别1、5/8、5/12、5/16、1、5/8、5/12。因此直接有
\[
(Kp)_2=550+380+(229+237)\frac58+(99+132)\frac5{12}+396\frac5{16}
=\frac{5765}4.
\]
actual列Z0中root0收益也可逐型核：
\[
361+\frac{587}2+\frac{99}2+\frac{396}3+360+99+\frac{132}2+\frac{99}2
=\frac{2821}2.
\]
故查询超该实际根123/4。以上是给定输入/菜单的手算，0代码执行，不是重新认证完整SPE。全部258含自身/215真偏离、最小松弛0、其他根收益、OPT_3=5189等仍按原作者单位审计MD证据身份保存；actualW4514且half余3839，不由这个例否定half。

独审的其他query向量和纯列cap已完整在现账本。五个纯列0/1/2/3/5安全，故自由mixed在这个例甚至不必混；唯一stationary p不是meta最佳回复，因为transient query2价格高于其self平均C(p,p)=185785/192。单独“有stationary p”和“有对称meta-NE p”不能拼成同一个p；对固定这个P,K，甚至不存在同时stationary和meta-NE的p。此精确固定核合同的否定不排内生改变核的另一构造，也不说明一般stationary self strong-push已失败。

## 平稳预算的完整定义及两个不同核/输入

[完整槽恒等式](../引理/完整槽插入税与跨角色价格恒等式--引理.md)HF已全文实读。Q是完整r槽的列分布，n_x为一列负载，n'_x是独立同分布副本。零负载的下列分子项取0，定义
\[
\bar U_Q=\frac1r\mathbb E_Q\sum_x\frac{n_x}{b_x+n_x},\qquad
T_Q=\frac1r\mathbb E_Q\sum_x\frac{n_x}{(b_x+n_x)(b_x+1+n_x)},
\]
\[
\Gamma_Q=\frac1{2r}\sum_x\mathbb E\frac{(n_x-n'_x)^2}{(b_x+1+n_x)(b_x+1+n'_x)}\ge0.
\]
从列中均匀抽槽得到主题边际q_Q，再独立重抽竞争列，其额外查询价格为Ubar−T+Gamma。pP=p时q_Q=p，故C(p,p)=Ubar_p−T_p+Gamma_p。6286例原独审报告Ubar9149/6,T98063/144,Gamma71303/576，D2821/2；于是D−Ubar=−343/3而D−C=85031/192>0。平稳没有角色平均收益可交换性，Gamma也不支付外部query2。

零背景rUbar是**混合列的期望覆盖**，不是一个actual列的W；有过去时它只是剩余玩家总利润。不能把上面9149/6代成4514/3。该例的固定完整槽核与此前DY1274客户真实尾槽例不是同输入/同查询背景。对同一个策略r>1虽有P_full=(I+(r−1)P_tail)/r、两核stationary集合相同，仍不能将r槽查询分母换成r−1槽，或把两份客户重数/数值相混。

## 条件复制矩阵：meta-Nash也是条件对象

每个16客户块四主题A/B/C/D，类型A:2,BD:4,AC:6,CD:3,ABCD:1。n不交块、4n人；q0=(2,1,1,0)，qA=(2,0,1,1)，qB=(1,1,1,1)，qC=(1,0,2,1)，qD=(1,0,1,2)。条件菜单R_n要求根T_j后本块qT、其他全q0，含root共4n槽；必须由**同一**完整SPE同时实现，不能假设一般直和。

现账本保完整单块查询矩阵L及异块h，n≥3的精确minimax是M_n=37/10−17/(12n)。补清原稿的meta-NE：Q均匀各D列时，四query价依次
\[
71/30+5/(6n),\quad 11/5-2/(3n),\quad16/5-1/(4n),\quad M_n.
\]
n≥3时D为最大，支持内D全取等，所以在行玩家收益K_AB、列玩家收益K_BA的对称两人游戏中，p=Q=uniform(D_j)确为对称meta-Nash，尽管K本身不必对称。此游戏描述的是插入矩阵，不是原顺序子博弈。对任何其余对称meta-NE p，value=max_A(Kp)_A≥min_Q max_A(KQ)_A=M_n；因而若R4真实现，**所有**此类meta-NE值都>u13/4，而不只某个坏p。

R4条件值803/240、gap23/240；R3值581/180<u。n1纯A安全cap16/5，n2值851/280；不能将n≥3的D最大公式机械代到n2。若R4实现，均匀D也使pᵀKp=M4>u，反弱WP；但自由静态每块qB把全查询压到16/5<u，actualW=OPT64，因此不是half反例。

独立两块稿90b16a6fa71daf25a8fc本批首次实际全文读：其最优列Q(C_j)=1/14,Q(D_j)=3/7不仅给KQ最大851/280，支持C/D均达到该值，故Q自己也为对称meta-NE。匹配零和行对偶p(C_j)=2/7,p(D_j)=3/14是**不同**分布；不能把匹配行对偶与这个meta-NE混成一个p。原独审报告独立整数BI用LCM840枚举12870计数前缀/6435终局、重造13872节点DAG再由单位审计核7437决策节点/59496比较；还报告B根另一候选(2,1,0,1)|q0不可实现。这里新读的是4023B独审数学文本，不是其代码/DAG/两份结果；HD先前未取得该review的历史事实不覆写成当时已读。

早期纠错f325ca53c510560b1607与独立接口681138cd2e959bc26dcb也全文比过：qD中旧D收益13/4，完整四槽后额外D为137/60；两块uniform-D的C359/120，比u低31/120。原规范BI记录(q0,q0)不在root可实现集，早期尚未独立压缩证书；后来的独立两块报告另保其后时点。旧“弱/extra-one/FM仍OPEN”是当时状态；现在零根银行族已独立反一般合同，不可由本例未反驳推出当前真值仍OPEN。

## 六个单块终局及三块有限分类

6701B稿的单块根可实现集合明确为
\[
\mathcal Q=\{(1,0,1,2),(1,0,2,1),(1,1,2,0),
(2,0,0,2),(2,0,1,1),(2,1,1,0)\}.
\]
最后一项是q0。原报告称n=1,2,3的root终局恰为Q^n中至多一个q0，其数6/35/200=5^n+n5^(n−1)。依据为每个枚举终局逐块属于Q、无两个q0，且枚举总数等于所有这些组合数，故**在这三个n**两有限集合相等。任意n仍猜想；此处没有把计数公式当任意n可信嫁接定理。

集合值逆归纳的逻辑已在[可信菜单算法](../算法/可信续局菜单与完整策略重构--算法.md)完整解释，HF实际全文核过。对计数前缀s，R(s)是所有完整历史纯SPE可实现终局，F(s)=max_a min_(z∈R(s+e_a))U_a(z)。root实际行动a与真实终局z满足U_a(z)≥F(s)，故
\[
R(s)=\bigcup_a\{z\in R(s+e_a):U_a(z)\ge F(s)\}.
\]
反向由选中孩子用z、每个其他有序孩子独立选最坏子SPE拼合，证明充分；不是仅保必要IC的松弛。计数缓存保的是**所有终局集**，不同有序历史仍可选择不同可信目标。枚举终局全集不枚举每一完整动作图，有限采样更不等于穷尽所有策略，也无多项式运行时保证。

## 原程序的整数域与审查覆盖

| 作者原有限报告 | 准确范围及尚未覆盖的认证 |
| --- | --- |
| 三块12人收益缩放LCM(1,…,12)=27720 | 普通玩家分母≤12，可用整数比较无浮点容差；这是原MD说明，HF本地helper未得到C++ blob，未读源码或新编译。 |
| 三块额外查询缩放LCM(1,…,13)=360360 | 插入查询额外+1，不能用原12人分母代替；原指定查询p=uniformD诊断独立于root列抽样。 |
| 2704156计数状态、1352078终局、3207136保留outcomes | 是单份C++的状态/终局集合记录，不是完整有序策略数、独立实现数或当前新run。 |
| 四根A/B/C/D指定目标均不可实现；last-low截面192/384/192/192，全截面最小F=37/10>13/4 | 该全部截面结果只有一个实现。B截面含额外不相容root前缀，检查更大集合仍全严格阻断不会削弱所需相容子集结论。未独立逐截面重算。 |
| 两块回归和程序范围 | 原文称n2复现旧三个状态计数/四类可实现根，不能替代n3独立审核；C++刻意拒绝n>3以防四位计数编码越界。未读代码不把此描述当当前实际parser测试。 |
| 最小门槛代表与另一独立局部稿 | 只独立解析一个余3人代表，不覆盖全部截面或任意n；区别见下一节。 |

指定真实子树替代诊断只取p=uniformD,u13/4：A/B/C/D在root自身≤u下可选60/39/35/35终局，最大p插入101/30、283/90、197/60、551/180；B/D不足，不能产这套指定p的mixed反例。最大目标qT|qE|q0，qE=(1,1,2,0)，D插入16/5比q0少1/2。这些最大/可实现性仍是单C++报告，本批未读原5925B报告所有字段；不由诊断失败证一般FM或排所有p。

## last-low的量词与局部729稿的duplicate去向

目标z，L={a:z_a>0,U_a(z)≤u}。若每个与指定root前缀相容、s≤z且Σ_(a∈L)(z_a−s_a)=1的非终端截面都有F(s)>u，取真实路径最后一个L行动便矛盾。因此不可实现。该一般引理不自动给三块全截面门槛，更不证明任意n。

3104B局部稿729c23b4e89e761e0043的全部实质证明已在现账本完整：合法前缀ACD|AAB|AAB尚余3人；只要当前规定D0，其最终13/4，改D1后任意真两人SPE新增只可能{C1,C2},{C1,D2},{C2,D2}，该偏离者最坏37/10>13/4。其余两人首C1可保37/10，非C1/C2/D2即时≤13/4，首C2/首D2的末位BR也已穷尽。该证明不排先C1/C2的其他排序，不能替代全部截面。原`verify_last_low_witness.py`称展开48单位客户、每首动作枚举12末动作、用Fraction且不导solver；HF本地blob未取到，不冒实际代码读/执行。数学文本证明完整，原实现边界另记，故该主稿按准确目标duplicate。

## 14类遗漏原稿：另一个完整duplicate身份

5359B aa188e3cd37022c8cb39的14兴趣类型与D22回复(B,R,R,R,S,R)在现账本有独立原件身份；当前[唯一最优遗漏族](../反例/唯一最优组合的全遗漏支付--反例.md)用12类型和(B,S,R,S,S,R)，[两输入等价](../等价/两份最优遗漏输入的二人收益等价--等价.md)已保共同大小/两两交集及三人不等价。B/Q处R-S是合法平局差，不能据“同证书”称客户表/selector/字节全同。

全部7节点/42比较/21对覆盖已按这些明确定义表完整覆盖；TQ唯一OPT38，actualAB为W35，交集2/遗漏36/实际独有33，half余32。保护价格B_D(16)=4>3是另由本例遗漏集每主题至多18、总36和T/Q各权1达到证明，不能仅以一般两两交集相同就断言所有高阶保护价格相同。原发现/父审计不新读或运行、原优化线索不认证最小性。此源全部独有数学与历史去向已保，准确duplicate，不新造一个二人反例。

## 实际读取、缺失边界与接续

[五主源](../../../../tools/evidence/stationary-query-and-replicated-menu-audits/source-manifest.json)保GS首读与HF同字节复用；[五份相关及下一批预读原件](../../../../tools/evidence/stationary-query-and-replicated-menu-audits/related-and-next-prework-source-manifest.json)HF实际全文首次读，尚不对它们写primary receipt。三种单块/多块/局部/平稳/遗漏输入和矩阵的域不互换。

两次安全本地helper共9个ID尝试，5份MD齐、4程序/报告本地缺blob；缺失不重试/不network。它们是3ea438c35454a47d226d、b94a4e2caf2abbfd0854、53a06d4d1ae0ca89c85e、e37e092b132faffbe938，原manifest保留，不宣称全局或别缓存永久不存在。当前新增的是给定六列的平稳解、query2七型和root0八型手算及文本证明比较；新数学**程序**、原CLI、LP/BI/随机/旧成功重跑全0。来源历史独审不新增外审或新颖性、canonical实现认证，不导第三阶段图。
