---
id: "customer-attraction/frozen-assignment-intersection-transport-and-true-query-gap"
kind: "lemma"
type_tag: "引理"
title: "冻结指派的交集运输与真实查询差额"
status: "fixed-matrix-assignment-and-gap-identities-proved; strong-FOMA-refuted; weak-budget-unpaid"
summary: "冻结成本只有实际交集bonus随排列变化，精确指派原始/对偶及循环条件成立；真实查询GAP保全部未来响应，fresh列常数不产生负环，普遍K≤W已被旧52/1953否定。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round7/transport/frozen_optimal_assignment_working.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round7/transport/frozen_optimal_assignment_working.md"
---

# 冻结指派的交集运输与真实查询差额

## 同一静态矩阵，先不要求比较最优

采用[有限单位客户共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)，任意m≥1，保空主题、重复、零客户、任意有序离轨平局。固定实际有序叶Z=(S₁,…,S_m)、覆盖C、负载cₓ、福利W。任取合法m个**索引**比较主题Tⱼ，并集O；代数部分不需SPE，也不需T最优。定义冻结删位查询
\[
d_{ij}=\sum_{x\in T_j}\frac1{c_x+1-\mathbf1_{x\in S_i}},
\qquad K(T;Z)=\min_{\pi\in\mathrm{Sym}(m)}\sum_i d_{i,\pi(i)}.
\]
它冻结其它actual行动，不能用早期SPE IC直接断dᵢⱼ≤uᵢ。只在最后讨论FOMA时取|O|=OPT_m。

写dₓ为比较出现次数，tₓ为配给同时实际覆盖x的角色的位置数。[既成客户恒等式](冻结指派的客户恒等式与最优比较量词--引理.md)已自足证明
\[
\sum_i d_{i,\pi(i)}
=\sum_{c_x=0}d_x+
\sum_{c_x>0}\left[\frac{d_x}{c_x+1}+\frac{t_x}{c_x(c_x+1)}\right].
\]
因此下面运输分解是该身份的固定矩阵表达，不重授另一普遍覆盖定理。

## BONUS：只有实际交集随指派变化

置
\[
\beta_j=\sum_{x\in T_j}\frac1{c_x+1},\qquad
H_{ij}=\sum_{x\in S_i\cap T_j}\frac1{c_x(c_x+1)}.
\]
H中客户实际c≥1，无零分母；β含fresh和实际覆盖客户。直接通分得
\[
\boxed{d_{ij}=\beta_j+H_{ij},\qquad
K(T;Z)=\sum_j\beta_j+\min_\pi\sum_iH_{i,\pi(i)}.} \tag{BONUS}
\]
列常数β只加一次，排列只改变实际交集C∩O的非负bonus。fresh客户x∈O\C对H全部为0；它在所出现比较槽贡献的是所有行相同的列常数，不会因换角色产生冻结成本改进。

最小bonus恰为有限二分完美指派的原始/对偶共同值：
\[
\min_{\substack{p_{ij}\ge0\\\sum_jp_{ij}=1\\\sum_ip_{ij}=1}}
\sum_{ij}H_{ij}p_{ij}
=\max_{\substack{a_i+b_j\le H_{ij}}}
\left(\sum_i a_i+\sum_jb_j\right). \tag{ASSIGN}
\]
a,b为自由符号势，不能额外要求非负。左边等于最佳纯排列，理由可直接给出：双随机p的正支持满足Hall条件，因为任意行集的总质量等于行数，至多流入其邻列各1；故有一份全正支持上的完美匹配。令ε为匹配边上p的最小正值。ε=1时p本身就是该排列；ε<1时沿匹配减ε，再将剩余除以1−ε，得到p是该排列与另一个双随机点的凸组合。至少一条正边消失，有限递归即分解成置换凸组合。线性目标取最小必可在一排列达到。右式则是这个有限可行有界指派LP的标准强对偶；逐边势aᵢ+bⱼ≤Hᵢⱼ也直接给所有排列的下界。

重复比较主题只是若干索引列相同，以上仍按m列计算。枚举不同标签排列时，每个不同排列恰对应同样数量的索引排列，因此对不同排列均匀平均与对m!索引排列均匀平均一致；不能因重复槽删除玩家或漏掉其覆盖重数。

## 均匀平均和最优匹配的区别

均匀索引排列使每(i,j)概率1/m，并有
\[
\boxed{\mathbb E_\pi\sum_i d_{i,\pi(i)}
=\sum_{c_x=0}d_x+\frac{m+1}{m}\sum_{c_x>0}\frac{d_x}{c_x+1}.} \tag{MEAN}
\]
因为ΣᵢHᵢⱼ对每个实际覆盖客户把其c个actual coverer加齐，恰为该列的Σ1/(c+1)。最小值总不超过均值，均匀预算是更强要求。

已证[八客户固定策略](../反例/均匀最优主题排列预算的八客户失败--反例.md)实际011、W6、唯一最优123，矩阵
\[
\begin{pmatrix}4/3&3&3\\2&2&2\\2&2&2\end{pmatrix}
\]
的均值58/9>6，但K=16/3<6。重复非最优222的费用又为7>6，却只覆盖3而非OPT₃8；它既不能反驳最优存在式，也不能与最优均匀失败混作一个量词。

## CYCLE：固定H最优指派的准确信息

将一份最小指派重标为当前Tᵢ配实际角色i，因β列常数不变，对任意角色简单循环i₁,…,i_l（l≥2）有
\[
\boxed{\sum_{r=1}^lH_{i_r,i_r}
\le\sum_{r=1}^lH_{i_r,i_{r+1}}},\quad i_{l+1}=i_1. \tag{CYCLE}
\]
否则只沿此环替换即可降低成本。反过来，对固定H，若全部循环满足它，任意排列分解为不交循环、逐环相加，便不比当前指派便宜。所以这是固定指派最优性的完整矩阵条件，**不含**其值≤W的数值上界，也不使用真实后继IC。

## GAP：真实同策略查询与冻结成本的差

恢复完整SPE σ及其实际Z，仍用上述最小指派的重标Tᵢ。令
\[
Y^i=\operatorname{finish}_\sigma(Z_{<i},T_i),\quad
D_i=u_i(Y^i),\quad e_i=u_i-D_i\ge0.
\]
对x∈Tᵢ，写fᵢ(x)=c_Z(x)+1−1_(x∈Sᵢ)，yᵢ(x)=c_(Yⁱ)(x)。两分母正。真实过去完全相同，所以
\[
\begin{aligned}
E_i&=\sum_{x\in T_i}\left(\frac1{f_i(x)}-\frac1{y_i(x)}\right)\\
&=\sum_{\substack{j>i\\x\in T_i}}
\frac{\mathbf1_{x\in(Y^i)_j}-\mathbf1_{x\in S_j}}{f_i(x)y_i(x)}.
\end{aligned}
\]
因此
\[
\boxed{K(T;Z)-W=\sum_i(E_i-e_i).} \tag{GAP}
\]
E有符号，不能取正后保等式；e才是一条实际前缀对完整Tᵢ query的真IC松弛。末位E0；早期不能把真实Yⁱ尾改回actual尾再保IC。这里的E与[单角色整行信用](单角色动态损失的同客户信用与未付份额--引理.md)的非负静态E不是同一个量，后者汇集全部m个查询，本页只取每角色一个匹配查询。

对于fresh x∈O\C，H全0，但其被分给某Tᵢ时f=1，若真实后继也来覆盖它，E的该项1−1/y>0。故fresh捕获税可以出现在GAP中，却不直接造成CYCLE严格改进。把coupon行过载直接变成负交替环会漏掉这层真实关系。共同first-departure reset分组同样只确定父角色/动作，不给汇集的off-history整行密度bracket≤1。

## 已否强FOMA与仍未证的准确弱化

原8742B稿顶部第八轮纠正已经明确：
\[
\exists\,T\text{最优}:K(T;Z)\le W \quad(\mathrm{FOMA\!-\!EXISTS}),
\]
以及要求每个最优T都成立的FOMA-ALL，**均非一般真命题**。现有[52客户四人完整SPE](../反例/最优组合冻结匹配的一单位缺口--反例.md)有唯一最优0145、W47、所有24匹配最小48；[1953客户三人例](../反例/静态最优主题排列的冻结后缀失败--反例.md)唯一最优125、W1735、K1736。两份现正文已给完整单位输入、全有序策略、唯一最优与全部排列的证明，本次不重复旧成功重演或授新游戏。

所以原后文“若用CYCLE与IC控制ΣE≤Σe便闭合FOMA”只保其历史条件接合。对固定T，GAP使这项控制等价K≤W；若要求普遍存在这种最优T，就是已被否定的FOMA-EXISTS，不能继续称其一般付款只是尚未完成。CYCLE与全树IC都在这些反例中为真，故它们不可能无额外限制普遍推出这条强上界；这不排除交替环用于别的弱化。

仍可准确陈述的弱预算是：存在某个最优T及匹配使K≤(1+1/m)W。它由既成COVER式OPT≤K+(1−1/m)W足以推出half。用本页GAP，固定T的弱预算等价Σ(E−e)≤W/m；本材料和现有固定锥数值均未证明这个存在式。两旧反例的K都小于弱预算，不能由强失败否弱式，更不能与真实改变后缀的净差匹配候选混同。

原有限13目标全部通过强式的报告不含旧52/1953，故与这两反例没有矛盾。其精确实现、24实际JSON闭包及九个浮点诊断的严格唯一性退化在[资源](../资源/冻结指派原审计的十三目标与严格唯一锥范围--资源.md)完整保全。本轮无原import/main、SPE/匹配扫描或新数学checker；通用身份、运输表示与循环条件由上述解析承担，不产生新的福利下界或六人half结论。
