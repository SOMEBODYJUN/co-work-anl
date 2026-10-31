---
id: customer-attraction/cartesian-bank-full-root-menu-low-value-symmetric-nash-failure
kind: counterexample
related_result: customer-attraction/cartesian-bank-individual-fractional-floor-counterfamily
type_tag: 反例
title: 笛卡尔银行完整根菜单的低值自洽分布失败
status: NQ-Mfull-and-all-p-WP-refuted-for-general-model; exact-bank-menu-proved
summary: 完整根列保留r槽，Jensen给任意列混合最大查询≥r质量B_r；银行四人u4/3<B4=19/14否定Mfull及低值对称Nash，精确菜单值/全部对称NE值59/36，half仍成立。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round3/mixed/self_consistent_query.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round3/mixed/README.md
---

# 笛卡尔银行完整根菜单的低值自洽分布失败

## 三个量词及原源的历史状态

有限单位客户、有限非空共同目录，保空主题、重复、零客户、完整有序历史和平局。固定任意合法前缀h，其背景b，剩r≥1人及同一完整纯SPE σ。强制根行动A后真实完整剩余列为$Z(A)=(A,Y_A)$，**含根共r槽**，尾r−1槽。当前强制收益与根收益为
\[
 d_A=\sum_{x\in A}\frac1{b_x+c_x(Z(A))},\qquad u=\max_A d_A.
\]
完整根查询矩阵
\[
 K_{T,A}=\sum_{x\in T}\frac1{b_x+1+c_x(Z(A))} \tag{K}
\]
把T当额外静态query，原根A仍在列中；不是删根矩阵。每个K分母≥1。

2551B主源把K看成有限对称两人博弈：行收益$K_{T,A}$、列收益$K_{A,T}$。其候选及两相关桥必须分开：

| 名称 | 精确量词 |
|---|---|
| NQ | 存在此对称博弈的**对称Nash** p，$Kp\le\lambda\mathbf1$、support取等、$\lambda=p^\top Kp\le u$ |
| Mfull | 存在**任意列分布**Q，使$\max_T(KQ)_T\le u$，不要求Q是NE |
| 本源全p-WP | 对**每个**p都有$p^\top Kp\le u$，不是仅比平均强制收益$\mathbb E d_A$ |

NQ⇒Mfull；全p-WP结合对称NE存在⇒NQ。原主源与2827B README当时将它们写为OPEN，且明确固定点不支付尾部联合遗憾。**本批与后续已证银行族比较后，三个一般全称桥均已否定；不能沿用原OPEN作当前状态。** 下文是真正零背景根、完整原SPE反例，不仅任意非法背景菜单。没有否定half。

## 固定点存在与原未付恒等式仍正确

为自足保留原候选论证，任意有限实矩阵K均有对称NE。置$v(p)=p^\top Kp$、$g_i(p)=((Kp)_i-v(p))_+$，连续自映射$F_i(p)=(p_i+g_i)/(1+\sum_jg_j)$在单纯形有Brouwer固定点。若固定点总增益G>0，则$g_i=p_iG$，所有正p_i的收益差严格正，违背$\sum_ip_i[(Kp)_i-v]=0$；所以G0，$Kp\le v\mathbf1$且正support取等。此存在性从未提供值≤原u。

定义$\Phi_b(Y)=\sum_x\sum_{j=1}^{c_x(Y)}1/(b_x+j)$、$F_A=\Phi_b(Y_A)$，以及
\[
 R_{T,A}=\Phi_{b+\mathbf1_T}(Y_A)-\Phi_{b+\mathbf1_T}(Y_T),
\quad\delta_{T,A}=\sum_{x\in T\cap A}\frac1{(b_x+1+c_x(Y_A))(b_x+2+c_x(Y_A))}\ge0.
\]
先写插入T的势差$\Phi_b(T+Y)-\Phi_b(Y)=\Phi_b(T)+\Phi_{b+\mathbf1_T}(Y)-\Phi_b(Y)$，再比较$Y_A,Y_T$，额外保留根A造成重叠税δ，逐客户得
\[
 K_{T,A}=d_T+F_T-F_A+R_{T,A}-\delta_{T,A}.
\]
任意p同分布独立取A,T后F差相消：
\[
 p^\top Kp=\mathbb E_pd_T+\mathbb E R-\mathbb E\delta.
\]
在对称NE上λ≤u等价于$\mathbb ER\le[u-\mathbb Ed]+\mathbb E\delta$。R是**真实后缀联合替换势遗憾**；后继各自最佳回复不共同最大化Φ，不能把R置非正。r1时尾空、R0，任意p都值≤u；一般候选虽因此有正确边界，下面完整SPE仍反驳它。

## 保留完整r列的Jensen下界

令$\mathcal K_r=r\operatorname{conv}\{\mathbf1_A:A\text{合法}\}$，$d_x=b_x+1$，定义
\[
 B_r(b)=\min_{z\in\mathcal K_r}\max_T\sum_{x\in T}\frac1{d_x+z_x}.
\]
这是**r槽自由分数背景**，旧记号$t_{r+1}$，不是r−1槽。对任何列分布Q，均值负载$\bar z_x=\mathbb E_Q c_x(Z(A))\in\mathcal K_r$，因为每个Z(A)由r个合法主题组成。$s\mapsto1/(d_x+s)$凸，Jensen方向是
\[
 (KQ)_T=\sum_{x\in T}\mathbb E_Q\frac1{d_x+c_x(Z(A))}
 \ \ge\ \sum_{x\in T}\frac1{d_x+\bar z_x}.
\]
逐行后取最大、再用B的最小化，得
\[
 \boxed{\max_T(KQ)_T\ge B_r(b)\quad\text{对每个Q}.}\tag{JENSEN}
\]
没有把平均倒数误写成倒数平均，也未将根删去。若一份完整SPE有$u<B_r$，Mfull即无任何Q；对每个对称NE p，$\lambda=\max_T(Kp)_T\ge B_r>u$，所以NQ更无低值NE。NE存在使全p-WP亦失败。无需求解器、有限Nash扫描或重跑已有银行程序。

## 真正完整SPE的银行输入与根收益

对任意m≥2，有m个经济singleton$e_0,\ldots,e_{m-1}$，m−1个互不交的2客户银行块$B_0,\ldots,B_{m-2}$；目录含全部Cartesian主题$(a,b)=\{e_a\}\cup B_b$。每位在终局利润$1/n_a+2/n_b$，总客户3m−2。完整策略按全部已观察有序历史更新模式：

| 模式 | 指定行动及更新 |
|---|---|
| 根 | 指定(0,0)；任一实际根行动(a,b)都将此真行动作为锚进入BASE |
| BASE非末位 | 经济复制根a、银行最小未用；若不等规定联合动作，新银行则转PUNISH并固定此次银行为过去目标，旧银行则转EXIT |
| BASE末位 | 经济最小未用、银行复制根b |
| PUNISH非末位 | 两坐标各最小未用；若实际银行新则继续且**目标不更新**，旧则转EXIT |
| PUNISH末位 | 经济最小未用、银行复制固定过去目标 |
| EXIT | 两坐标各最小未用，永久EXIT |

EXIT发生过银行重复，故余r人至少r个银行未用，指定者经济/银行皆独享得3，达到上界。PUNISH的银行在末位前不重复，固定目标在过去；非末位指定者不会被末位复制，得3最优，末位面对所有银行各一旧用户、取新经济加银行得2最优。BASE非末位得$2+1/(m-1)>2$；任何改变经济/银行或同时改两坐标的联合偏离，新银行会被PUNISH末位复制，旧银行已有共享，经济至多1，总收益≤2。BASE末位得2最优。根任一行动都重锚同型BASE，故每个根分支真实当前收益
\[
 u=d_A=1+1/(m-1).
\]
这些情况及不变量涵盖全部再次偏离、有序历史和平局，是真正完整SPE，不是静态伪菜单。每个根完整列经济a被m−1人覆盖、另最小未用经济$f(a)$一人覆盖，银行b两人、其余各一人。

一般实际路径$(0,0),(0,1),\ldots,(0,m-2),(1,0)$只覆盖两个经济客户与全部银行，W=2m；另选m个互异经济坐标并让m−1银行至少各出现一次即可覆盖全体3m−2客户，故OPT=3m−2，仍过half。已证[银行反族](笛卡尔银行目录的逐人分数门槛反族--反例.md)还给均匀边际/均匀query Jensen双边式
\[
 B_m(0)=\frac m{m+m}+\frac{2(m-1)}{m-1+m}=\frac32-\frac1{2m-1}>u\quad(m\ge4).
\]
这里上界取所有主题均匀背景，经济均值负载1、银行客户均值负载m/(m−1)，每query恰为显示值。下界取所有query均匀：每经济客户权1/m、每银行单位客户权1/(m−1)，任何z的经济总负载m、银行单位总负载2m，分组Jensen分别给1/2与2(m−1)/(2m−1)。故B确为等号，不是只给一个不足反驳的上界。

因此(JENSEN)已对所有m≥4否定NQ和Mfull，包含恰六人；这不是相同人数的half反例。

## 四人的精确完整菜单证书

取m=r=4、b0：4经济客户、3银行各2客户，共10客户/12主题。根actual路径$(0,0),(0,1),(0,2),(1,0)$，根经济份额1/3、根银行份额1，故$u=4/3$，W8、OPT10；$B_4=19/14$，严格差1/42。B4竞争质量4，对应静态第五查询槽，不是实际多一位玩家。

取p在9主题$\{1,2,3\}\times\{0,1,2\}$各1/9，其余3个经济0主题概率0。对任一支持根列(a,b)，经济a完整负载3、经济0负载1，其他经济0；银行b完整负载2、其他银行1。故query经济t=1,2,3的期望项$\frac13\frac14+\frac23=3/4$；经济0项1/2。每个query银行期望项$\frac13\frac23+\frac23=8/9$。于是
\[
 (Kp)_{(t,b')}=\begin{cases}59/36,&t=1,2,3,\\25/18,&t=0.\end{cases}
\]
因此p真为对称NE，$\lambda=p^\top Kp=59/36>4/3$，差11/36；它同时是全p-WP明确反例。

还可排除所有低值NE并求Mfull精确值。对任意列分布Q令$q_a$经济边际，银行边际$q_b^B$。经济0 query值$1/2-q_0/4\le1/2$；经济1值$1-3q_1/4-q_0/2$；经济2、3值$1-3q_a/4$。后3个平均为$3/4+q_0/12\ge3/4$，故经济0永不最佳。银行query值$1-q_b^B/3$，最大至少8/9。完整Cartesian query可同时选最佳经济与银行，故任意Q最大行≥59/36；上述p取等，所以$\min_Q\max_T(KQ)_T=59/36$。 同一p作为行分布另给显式对偶证书：$p^\top K[:,A]$在根经济0列为31/18，其余列为59/36，故对任意Q都有$\max_T(KQ)_T\ge p^\top KQ\ge59/36$。

任何对称NE不得用经济0；其它经济如有未用，query该经济值1，高于正用者，故3个都用且等收益强迫各1/3。银行亦全部用且各1/3。联合相关性可任意，只要此两边际；因此**所有**对称NE值均59/36，并非仅某一坏NE。NQ的“至少有一个低值NE”正被否定，而不是误拿一个高值NE反驳存在量词。

在这个显式p，原suffix账也精确失败：每个支持根d=4/3，$\mathbb E\delta=5/36$（经济重合贡献1/36，银行重合贡献1/9）；尾经济a有2人、经济0有1人、每银行有1人。若query经济T与根A不同，$R_{T,A}=2/3$，相同则0，故$\mathbb ER=4/9$。于是$\lambda-u=4/9-5/36=11/36>0$，原child IC全部可信仍不支付联合势遗憾。

[精确矩阵与有理代入](../../tools/evidence/cag-mixed-routing-primary/analytic-bank-menu.json)保12×12 K、p与所有行值。它是上面解析公式的计算展开，不是新SPE穷举、Nash求解器输出或额外原程序run；本批五源均Markdown，原程序执行0。一般银行原run不重复。

## 原源、README与当前用途

2551B原文的K定义、对称Nash量词、NQ⇒Mfull、固定点不支付suffix遗憾及r1边界均正确保存；“一般NQ开放”现由本解析反例更新为否定。2827B README还列策略生成闭包稿：以种子查询支持对全部有序历史的σ行动取闭包，声称保SPE/actual菜单及以OPT种子时W/OPT，同时不保统一大小界。这是准确的**待领原稿导航**，本批没有将未读`strategy_generated_closure.md`当新done或依其声明证明本反例。

README所称已失败的删当前槽全p aggregate桥是另一矩阵；这里K保根，银行完整列证书另外否定保根Mfull/NQ/WP，不能把两种失败混同。它列HIT/FUND/OWNER-ROUTE三个正组件及同一whole-IC耦合缺口仍保真；NQ否定不使这些真组件失效，也不免费证明half。当前五人他证成立，六人half仍需较弱共同支付。

[来源清单](../../tools/evidence/cag-mixed-routing-primary/source-manifest.json)与比较快照保全部原字节；本文新反证是对当前已证银行族和原完整根矩阵的解析比较，非原2026-10-23作者已发现的结论，不冒称盲审或外审。旧正式页的最小状态修正另包供父级串行保存，本stage不覆盖共享正文。
