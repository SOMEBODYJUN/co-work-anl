# 归一化菜单的Santa Claus精确值桥与状态数量锐界

读取目的：给反面归约一个可逐原任务检验的数值合同，并检查从一般加性源逐玩家归一化的显式规模。这两项是标准selector思想和自足覆盖计数的准确结构结论，不是新近二困难性或一般Santa Claus算法。第一项保持最优值和给定分配的解码；第二项只排除一个明示的逐玩家转换接口。

## 1. 归一化完整菜单与精确值桥

**ID / Version：`UM-WEIGHTED-MENU-STATE-DUMMY-SC-VALUE-BRIDGE-v1`。**

**Objects / Domain / Definitions / Assumptions。** 有限非空groups G；每组g有K_g≥1个显式indexed states。每state有distinct资源集S_gs及二进制非负有理p_gsu，总量**恰1**。每state独立private机M_gs，每resource一R_u；每组一selector只能在本组任意state机耗时1，每(g,s,u)一job只能在M_gs耗时p_gsu或R_u耗时1，其余∞，无其它jobs/资格/约束。所有states的原jobs都在P内，允许零项及重复indexed states，无resource跨组度或菜单大小限制。

令a_gs(B)=Σ_{u∈B∩S_gs}p_gsu、f_g(B)=max_s a_gs(B)，并令

\[
 V=\max_{B_g\text{ pairwise disjoint}}\min_g f_g(B_g),\quad 0\le V\le1. \tag{1}
\]

**Quantifiers / Exact Statement / Conclusion。** 对每个上述P可确定性位多项式构造显式非负加性Santa Claus实例SC(P)，满足

\[
 \mathrm{OPT}_{SC}=V,\qquad
 \mathrm{OPT}_{UM}(P)=2-V=2-\mathrm{OPT}_{SC}. \tag{2}
\]

不输入OPT，不声称可poly优化任一边；以下给定allocation或schedule的转换是结论的一部分。包括V0、V1、K1及UMOPT2端点。每给定有理t∈[0,1]，SC存在所有agent效用≥t的实际分配 iff P存在峰≤2−t的完整实际调度，t不是构造时猜测的未知最优值。

**构造。** 每indexed state建立一名agent b_gs；每原resource一枚real item u，对该agent价值p_gsu（缺失/零项为0）。每组再添K_g−1枚不同dummy items，各对自己组的全部K_g名state agents价值1、外组价值0。每item不可拆、至多一个owner，可闲置；非负价值下强制全分配也不改变最优值。未把每条state-incidence job复制成独立real item。

**Dependencies。** 只依上述完整矩阵、norm1/非负及item不可拆；无外部hardness、SC近似后端或配置LP前提。standard state-selector装置本身不主张新颖。

## 2. 全部给定分配的转换与值恒等式证明

**资源bundles到SC。** 给不交B_g，扫描菜单各选达到f_g(B_g)的state，把B_g real items给它；其余K_g−1 agents各得一枚不同的本组dummy。所选者得f_g(B_g)≤1，其余得≥1，故SC min≥min_g f_g(B_g)，特别OPT_SC≥V。

**SC到一个state/组。** 给任意SC分配，实际min效用t≥0。每组K_g名agent只有K_g−1枚own dummy，必有至少一名没拿本组任何dummy；外组dummy对它值0，所以它收到的real bundle B_g满足a_gs(B_g)≥t，且≤1。所选agents不同、real items不可共享，故B_g跨组不交。于是V≥t，对最优SC分配得到V≥OPT_SC，也顺带证任何分配的min≤1。不拼接同一组多个state agents的bundle；K1时唯一agent自动dummy-free。

**资源bundles到完整UM。** 每selector放所选原state；只将该state在B_g内的原incidence jobs导出到R_u（零private job也可留根），全部其它原incidence——含每个未选state——均留自己的private根。资源至多一unit、未选根负载1、选根负载2−a_gs(B_g)。从SC上述dummy-free decoder可得实际峰≤2−t；所有原jobs各一次、资格和p不变，输出并非只报效用值。

**完整UM到SC。** 给实际峰C<2的任意P调度，取每selector真实所在state；该state实际导出的资源B_g跨组不交，因为每resource最多一unit。其归一化private负载恰2−a_gs(B_g)≤C，故a≥2−C。按第一段给real items与dummy，得到SC min≥2−C。无需先把未选state规范化；它们占用的资源可忽略，取出的B_g仍不交。若C≥2，不可断言资源独占，但目标max(0,2−C)=0由任意非负SC分配满足即可。

这证明每UM调度C≥2−V：C<2用上一段，C≥2用V≥0。反向按达到V的bundles实际构造≤2−V，得式(2)，没有在C=2误用独占。对t>0，峰≤2−t严格小于2可逆提取；t0两边由全private≤2和SC非负分配平凡成立。若需非抢占起止时刻，各机按固定顺序串行，精确有理部分和给位多项式时刻表。

## 3. 归一化、degree、位复杂度与反面源义务

记n=|G|、S=ΣK_g、m=|U|、I=Σ|S_gs|。SC恰S agents、m real items、S−n dummy；real估值显式条目≤I，dummy正值条目恰ΣK_g(K_g−1)≤S²，dense矩阵S(m+S−n)项。时间仅复制原有理或写0/1；找dummy-free agent、扫描给定bundle选态及还原全部n+I原jobs都是总位多项式，没有数值复制或隐式state枚举。

每SC agent的**real-row总量1，完整row总量K_g**，不能冒称完整SC行也归一化为1。原resource跨组小不代表SC item正值agent少：同组许多states都可正值，dummy还连K_g agents；不能免费调用degree2 SC后端。只对明确给定的共同单位T>0整体缩放SC所有值，式(2)变UMOPT=2−OPT_SC/T，不提供任意外部SC的最优值归一化。

若原菜单仅W≤1，可先用[每state独占bonus归一化](weighted_menu_bounded_group_interaction_rounding.md)精确保UMOPT，再在**增广资源上重定义V**；不能保留旧未增广V照写2−V。例如原零工作state的V0而UMOPT1，已直接否定这种偷换。

任意固定δ∈(0,1)，在本构造像类中

\[
 UM:\ YES\ OPT\le1,\ NO\ OPT>2-\delta
 \quad\Longleftrightarrow\quad
 SC:\ YES\ OPT=1,\ NO\ OPT<\delta. \tag{3}
\]

弱NO界也按式(2)同步改成弱值界。固定1-versus-1/2 SC源只给UM 1-versus-3/2，不排除所有常数ε。一般additive源、聚合福利、正值可行性或列所有可行bundles，都未自动满足本normalized image的全选态/部分导出NO合同。资源跨组≤3的输入可再接[零格三坐标精确表示](degree_three_weighted_menu_cube_embedding.md)，但它只传gap，不制造gap。

**Evidence / Counterevidence / Status / Related Files。** Exact-first独立完整重构、作者Proof实际读后及本正文实读范围见[值桥审查](../../reviews/unrelated_machines/normalized_weighted_menu_santa_value_bridge_review.md)。证明完成，未实现软件，无有限枚举声明，外审/全球新颖性未认证；无standing fatal。式(3)是源义务而不是源困难性定理，UM-TARGET-v1正反面未解。

## 4. 同资源宇宙的逐玩家菜单规模：精确陈述

**ID / Version：`UM-NORMALIZED-XOS-THRESHOLD-MENU-SIZE-OBSTRUCTION-v2`。** v1的较弱2^{⌊ηt⌋+1}下界来源不覆盖；本v2同对象强化最小规模及锐端点，不改全局归约的范围。

**Objects / Domain / Quantifiers / Definitions / Assumptions。** 固定有理η∈(0,1)，整数t≥1，U为2t个不同资源；d=⌊ηt⌋，k=max{1,⌈d/η⌉}，故0≤d<t、1≤k≤t。显式K≥1个indexed非负有理additive clauses w_s，逐clause全U总量恰1，允许零系数、重复states。f(B)=max_sΣ_{u∈B}w_su，要求对**全部**|T|=t有f(T)=1，对全部|B|≤d有f(B)≤η。

令K_min为满足上述要求的最小clause数；令Θ(2t,t,k)为最小family F⊆binom(U,k)的大小，使每个t-subset都**包含**某个F∈family。方向是大集合含一个指定小集合，不混同相反的覆盖定义。Θ只是有限组合量，不输入或调用求它的算法。

**Exact Statement / Conclusion。** 对全部所列参数，

\[
 K_{\min}=\Theta(2t,t,k),\qquad
 K\ge\frac{\binom{2t}{t}}{\binom{2t-k}{t-k}}. \tag{4}
\]

任意满足域的菜单可不增K改成在k子集均匀权1/k的菜单；反向任何达到Θ的family给合法菜单。两个达到的锐端点为

\[
 d=0:\ K_{\min}=t+1;\qquad
 \eta t\in\mathbb Z_{\ge1}:\ K_{\min}=\binom{2t}{t}. \tag{5}
\]

固定η，令c=⌈1/η⌉−1。当d≥1，另有

\[
 K\ge\frac{\binom{2t}{t}}{(2t)^c}
 \ge\frac{4^t}{(2t+1)(2t)^c}. \tag{6}
\]

式(4)比值不声称全部参数达到；式(5)给真正相等及构造。不含软件、有限测试或hardness假设。

## 5. support计数、正规化与锐界的自足证明

令某clause正support大小h≥1。若d≥1而h≤d，取该support作B就有f(B)≥1>η，矛盾。故h>d；其最大d项和至少d/h，被low条件约束为≤η，于是h≥⌈d/η⌉=k。d0时直接有h≥1=k。

每个unit T上有限max由某clause取得1；非负norm1迫该clause**整个正support**含于T。对每clause任取其support的k子集F_s，换为在F_s上均匀权1/k。原被覆盖的T仍包含F_s，故全部unit保住；小B的新值≤d/k≤η（d0值0），因此low也保住。去重后family大小≤K，覆盖全部t集。反向任何Θ-family用这些均匀clauses实现，仍同时满足两阈值，得到K_min=Θ。

每固定k集被恰binom(2t−k,t−k)个t集包含，覆盖计数立刻给式(4)。d0时k1，若只选≤t个singletons，未选资源至少t个可组成无覆盖T；选t+1个singletons后未选只有t−1个，每T必命中，给第一个锐端点。ηt为正整数时k=t，每个T只能包含其自身的指定t集，必须列全部binom(2t,t)个；它们的均匀权clause在任意至多d项上的和至多d/t=η，取support内d项达到，故确实满足，给第二个锐端点。固定约分η=A/B，取t为B的任意正倍数便有该锐等号。

当d≥1，写θ=ηt−d∈[0,1)，则l=t−k=⌊θ/η⌋≤c，且0≤l≤t−1。因此binom(2t−k,t−k)=binom(t+l,l)≤(2t)^c。中央二项式是(1+1)^{2t}中最大项，至少4^t/(2t+1)，证明式(6)。零系数不在support；重复clauses只浪费覆盖。若外部表示多列冗余全零clause，可先删掉，它不能取得unit值1，上述下界由非零norm1部分承担。

## 6. 对源归约的准确否定范围

一名普通additive玩家对2t个资源各值1/t，全部t集原值1，至多d项原值≤η，显式源长度O(t log(t+1))。若逐玩家转换要在**同一U**上用非负norm1 explicitXOS同时保这些全部subset阈值，则固定η下式(6)已迫超多项式输出；当ηt整齐时精确需中央二项式那么多states。即使所有系数只取统一数值1/k，每个indexed support仍需显式列出。

这不是2^{Ω(源总位长)}的声称，η随输入变时c也不再常数；不是一般求Θ的复杂度结论。允许辅助resources/players、全局耦合、只对可达分配保真、unit completeness损失、未归一化clauses或另证可处理的隐式表示，都不在本障碍范围内。它排除了式(3)源义务的一种未经证明的shortcut，未证明不存在任何满足该源义务的归约。

**Dependencies / Evidence / Counterevidence / Objections / Status / Related Files。** 依非负norm1有限显式max、全部subset阈值及本文计数；无外部SC困难性或实验前提。Exact-first独立重构、作者Proof读后及最终正文实际范围见[规模锐界审查](../../reviews/unrelated_machines/normalized_xos_menu_threshold_size_review.md)。证明完整，明确锐端点，外审/全球新颖性未认证；无standing fatal及软件声明。一般UM正反面仍未解。
