---
id: customer-attraction/interval-ceiling-comparison-and-efficient-catalog-classes
kind: theorem
type_tag: 定理
title: 区间终局剪枝的上界比较与全效率目录类
status: proved-general-inclusion-and-two-full-parameter-classes;general-half-payment-open
summary: 完整区间上界比即时myopic上界保留更小的SPE终局超集且提高逐节点累计下界，公共核加私有单例和足够多不交最大主题两类都被全深度精确到全效率。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-977d3dbff13346b3b7c0f5a4caa6168e/background/interval_ceiling_relaxation.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-977d3dbff13346b3b7c0f5a4caa6168e/background/minvector_ceiling_compression.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-977d3dbff13346b3b7c0f5a4caa6168e/parent/minvector_independent_review.md
---

# 区间终局剪枝的上界比较与全效率目录类

固定[原共同目录模型](../定义/共同目录完整历史模型--定义.md)：有限单位客户、q个合法主题标签、m名单位提供者与全部有序历史纯SPE，允许重复、空主题、零客户及任意离轨平局。b为一个长度|b|≤m的合法计数前缀，r=m−|b|。终局z中占用主题a的一人收益为U_a(z)；辅助坐标在z_a=0时置0。每次真正查询孩子b+e_a的a坐标时该主题都出现，所以这个约定不把未出现题的虚收益混入当前查询。

## 两种准确递归、坐标压缩与合法范围

对X=M或I，终局H_X(b)={b}、G_X(b)=0。非终局先求所有孩子，令
\[
L_X(b)=\max_a\min_{z\in H_X(b+e_a)}U_a(z),\qquad
H_X(b)=\bigcup_{a\in E_X(b)}H_X(b+e_a),
\]
\[
G_X(b)=L_X(b)+\min_{a\in E_X(b)}G_X(b+e_a).
\]
两者差别只有当前行动的上界：
\[
M_a(b)=\sum_{x\in a}\frac1{1+load_b(x)},\quad
E_M(b)=\{a:M_a(b)\ge L_M(b)\},
\]
\[
Z_a^I(b+e_a)=\max_{z\in H_I(b+e_a)}U_a(z),\quad
E_I(b)=\{a:Z_a^I(b+e_a)\ge L_I(b)\}.
\tag{D}
\]
孩子终局都扩张b+e_a，所以真实终局查询收益≤M_a(b)。取达到max-min的a，得到M_a≥L_M，故E_M非空；I版本用max_child≥min_child同样非空。所有等号保留，递归有定义。

对任意完整有序历史σ同时按剩余人数归纳：每个真实偏离a后的终局在孩子H_X，当前偏离收益≥该孩子最小值；真实最优性给当前最终收益≥L_X，实际行动因此eligible，实际终局归入父H_X。于是两者均保所有纯SPE终局，并沿真实路径给剩余利润P≥G_X。**仅b0时P是根覆盖W**；任何固定非空背景不能用累计剩余利润代全覆盖。

集合并的坐标极值精确分配：令V_j^X(b)=min_(H_X(b))U_j，I版再存Z_j^I=max_(H_I(b))U_j。非终局
\[
L_X(b)=\max_aV_a^X(b+e_a),\quad
V_j^X(b)=\min_{a\in E_X(b)}V_j^X(b+e_a),
\]
I版的Z也在同样eligible孩子上逐坐标取max。故每节点M仅需一个q向量，I仅需两个；计算L/E/G和相应极值与显式集合实现逐节点完全同值。不同坐标极值可来自不同终局，证明只用有限集合并的min/max分配，不要求同时取到、不引入同计数同回复的策略限制。它不恢复H本身，也不代真正BI逐终局筛选。

全部计数态数binom(m+q,q)，终局态数binom(m+q−1,q−1)。忽略单个客户收益与M的计算，节点递推用O(q²)算术操作及O(q)个数；原文没有给精确有理数位复杂度界，总状态数也不因此成为关于一般m/q的多项式。

## 全节点包含与下界比较

对每个合法b都有
\[
\boxed{H_I(b)\subseteq H_M(b),\quad L_I(b)\ge L_M(b),\quad G_I(b)\ge G_M(b).}\tag{C}
\]
终局直接。归纳假设给每个孩子H_I⊆H_M，故每行动的孩子最小值提高，得到L_I≥L_M。若a∈E_I，某孩子z满足U_a(z)≥L_I；而U_a(z)≤M_a(b)，于是M_a(b)≥L_I≥L_M，得a∈E_M。结合孩子包含得父包含。最后
\[
L_I+\min_{a\in E_I}G_I(child_a)
\ge L_M+\min_{a\in E_I}G_M(child_a)
\ge L_M+\min_{a\in E_M}G_M(child_a).
\]
证明不要求两种集合极值由同一终局达到。它仅加强一个合法超集，不是精确纯SPE求解：某高终局使a eligible后，其孩子所有低于L_I的终局也被保留。这个失真由[五环精确例](../反例/五环区间行动放松低于额外分数门槛--反例.md)具体区分；一般充分义务G_I(0)≥OPT_m/2仍需另外证明或反例。

## 公共核加私有单例：全参数精确

任意整数m≥1、K≥0，目录恰m题A₁…A_m，所有题共有K名单位客户，A_j另有一名只喜欢自身的私有单位客户。OPT_m=K+m；固定任一前缀后，公共客户终局始终由全部m人覆盖，每人固定K/m，不能按当前前缀人数高估后再免掉将来的稀释。

**结论。** 对每个合法b、r>0，H_I(b)恰为后r人各选一个以前未用题、且相互不同的终局集，并且
\[
L_I(b)=K/m+1,\qquad G_I(b)=r(K/m+1).
\tag{Core}
\]
对r归纳。前缀最多用|b|种题，所以至少m−|b|=r个fresh题。当前fresh后，孩子归纳只用其余fresh，当前收益恰K/m+1；当前选旧题后，孩子也只用fresh，所以当前收益恰K/m+1/(b_a+1)<K/m+1。于是LI及EI恰如结论，所有这些孩子终局都保留，G递推加r份。终局r0单独H={b}/G0，不定义LI。每种fresh选择均最佳，亦可逐节点补全为完整SPE；所有原SPE由HI包含只能用fresh。

空根得到G_I=W(SPE)=OPT_m=K+m。K0/m1边界均在上述证明中。固定背景若早已重复浪费私有主题，未来r人的利润仍是(Core)，却不能声称此前遗漏私有客户会全部补齐。

**三人三公共客户的放松差可直接核。** m3/K3，主题A/B/C各有1私有。每终局公共份额1；旧H_M在孩子b=e_A保AAB/AAC/ABC，A收益最小3/2；新H_I只保ABC，A收益2。各两动作前缀的末位floor均2；因此

| b | L_M | G_M | L_I | G_I |
|---|---:|---:|---:|---:|
| 空根 | 3/2 | 11/2 | 2 | 6 |
| e_A | 2 | 4 | 2 | 4 |
| 2e_A或e_A+e_B | 2 | 2 | 2 | 2 |

旧e_A处myopic上界M_A=2恰过floor，保第二次A；它真实所有孩子的当前收益却只有3/2<2，新区间max上界恰排该动作。表按三个对称标签及两种末前背景穷尽，不需要用程序PASS替代这个机制。

## 足够多不交最大题：排除全部旧近轨伪策略族

设目录中任意两不同非空主题互不交，最大大小L>0，且至少有m个不同大小L主题。允许更多小题/空题。任意合法b、r>0时
\[
\boxed{E_I(b)=\{\text{fresh且大小L的主题}\},\quad
L_I(b)=L,\quad G_I(b)=rL.}\tag{Disjoint}
\]
前缀至多用m−r个不同最大题，所以至少r个最大题fresh。若当前fresh最大，孩子归纳永不重选它，当前终局收益L；若当前旧题，孩子均fresh最大、不再选该旧题，其当前收益|a|/(b_a+1)≤L/2；若当前fresh小题，收益|a|<L。故LI=L、EI精确如上，子集与G公式随归纳得到。当前动作是空题时收益0同样排除。L0时仅单列GI=OPT0，不能说全零平局只选fresh。

根OPT_m=mL，G_I及所有完整SPE覆盖皆mL；(Disjoint)允许fresh最大题来自任何标签，不仅来自某一预先命名族。

原旧在轨/Hamming/固定末k层伪策略族有m个不交B_j、大小L，另n=m−k个不交A_i，大小L/max(n−i−h+1,1)，其中1≤k<m、0≤h<n、L=lcm(1,…,n−h)。全部宇宙不交，至少m个最大题，所以(Disjoint)对全部参数给G_I=mL=OPT。记d=n−h：d≥2时旧路径首A₁大小L/d<L已在根排除；d1时旧路径本来全效率。某些晚A_i亦大小L，合法fresh最大选择当然包含它们，不能误写只许选B。

原m7/k1/h0例L60、A大小10/12/15/20/30/60，另7个B大小60，总567单位客户；旧路径福利207而OPT420，区间GI420。这里只直接代入全参数定理，不把旧非SPE近轨证书变成原目标反例或声称新跑27132状态。

## 证据及原读取先验

7739B主源与3579B minvector前驱、1722B父方重构均全文比对。父方明确只作一般递推独立数学重构，作者有限实现对照不是父方独立实现；本轮知情读三者，不新增盲审或外审。

原minvector报告552个0/1类型小实例、9132状态/27068坐标、4660非终局对照；interval报告同9132状态、664处严格集合收缩/107处G改善及24处仍大于真BI。原tail-family报告20参数/5860非终局，小参数显式集合对照，再加m7例27132，合32992。这些是原文有限记录，本批未因此自动读或重跑其三原程序/JSON。普遍(C)/(Core)/(Disjoint)和压缩等价性由本文完整归纳承担；旧3025五环成功及另线新C5程序范围也不替这些旧回归生成运行日志。

当前一般六人问题、精确SPE算法复杂度和G_I的普遍half付款都不由这些全效率类自动解决；新目录、更多交叠或有限阴性样本要另负担真实证明。

原件/指纹、逐源比较与准确复用范围见[本批证据](../../../../tools/evidence/interval-comparison-and-exact-floor-primary/README.md)。
