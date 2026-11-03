---
id: customer-attraction/true-source-AP-menu-cartesian-sums-and-pricing-closure-review
kind: review
type_tag: 审查
title: 真实源AP菜单的笛卡尔求和与定价闭包
status: analytic-AP-and-stated-menu-closure-reconstructed;no-oracle-rerun-or-half-certificate
truth_status: genuine-source-necessary-rows-valid;specified-histogram-extension-separable
review_level: primary-review-and-three-dependencies-fully-read;inherited-two-pricing-sources-compared
scope: 五单位提供者、有限共同目录和单位客户、同一完整有序历史纯SPE；七个真实非末优化节点与指定同族菜单行
summary: 自足证明M5任意主题AP、七真实源与笛卡尔菜单行，重构根J×T的7125式及单族二次计数定价；固定行族闭包、浮点发现、全型有理证书及全树补全分开。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round13/adversary/menu_ap_source_and_pricing_review.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/background_near_saturation.md#任意主题-c-的线性背景行
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round13/certificate/menu_ap_pricing.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round13/certificate/audit_menu_ap.py
---

# 真实源AP菜单的笛卡尔求和与定价闭包

4484B原独审全文及5606B背景近饱和证明、9062B菜单定价、4695B核验器均已全文读。本页保存自足数学与实现合同，没有运行原全oracle、认证全型最优或由此证明五人half。[五人half](../定理/五人半覆盖--定理.md)已另证，局部行族未完成付款与旧稿主目标OPEN不能混同。

## 1. 任意真实节点和任意合法锚主题的AP

固定[原完整历史模型](../定义/共同目录完整历史模型--定义.md)的一份五人纯SPE σ。任一真实决策历史h的旧负载为$p_x$、剩$k\ge2$人，当前规定行动者的最终利润为v。客户单位价值、共同目录有限非空；空主题、重复/同覆盖标签、零客户和所有离轨平局保留。因为过去只有$5-k$位，$p_x+k\le5$。

任取合法主题C、D，不要求C加权最大，置
\[
w_x=1/(p_x+k),\quad s=\sum_Cw_x,\quad e=v-s,
\]
\[
F(C,D)=\sum_{C\cap D}1/(p_x+k)+\sum_{D\setminus C}1/(p_x+1).
\]
则
\[
\boxed{e\ge0,\qquad F(C,D)\le s+[4(k-1)+k^2/2]e.}\tag{AP5}
\]
这是[已有加权背景AP](../引理/任意背景加权近饱和交换与统一锚主题上界--引理.md)取共同上界M5的版本，不新增AP新颖性或逐列可变M。

### 同一C偏离分支上的完整证明

当前强制C后沿同一σ的改变历史得到后继$A_2,\ldots,A_k=L$，令$q_x$为这k人对客户的总覆盖数，偏离者收益$v_C=\sum_C1/(p_x+q_x)$。最坏分母与当前IC给$s\le v_C\le v$。定义
\[
d=\sum_C\frac{k-q_x}{p_x+k}
=\sum_{j=2}^k\sum_{C\setminus A_j}w_x,
\quad d_L=\sum_{C\setminus L}w_x.
\]
当$k-q_x>0$，$p_x+q_x\le4$，故$v_C-s\ge d/4$，从而$d\le4e$。当前偏离任意合法B的最终分母至多$p_x+k$，所以$\sum_Bw_x\le v=s+e$；于是
\[
\sum_{B\setminus C}w_x\le\sum_{C\setminus B}w_x+e.\tag{1}
\]
中间$k-2$位在C外的w-incidence至多$d-d_L+(k-2)e$。真实末位L利润$t_L$与$v_C$在交集上相消；L外于C的每项至多$1/(p_x+1)\le kw_x$；C外于L的损失因$q_x\le k-1$及$p_x+k\le5$至少$5w_x/4$。用(1)于L得
\[
t_L-v_C\le(k-5/4)d_L+ke.\tag{2}
\]
在这个真实末位历史改选D。D∩C每客户至少得w；对D∖C，中间覆盖数为整数$0\le z\le k-2$，有
\[
\frac1{p+z+1}\ge\frac1{p+1}-\frac z{(p+1)(p+2)}
\ge\frac1{p+1}-\frac k2\frac z{p+k}.\tag{3}
\]
第一差精确为$z(z-1)/[(p+1)(p+2)(p+z+1)]\ge0$；第二步等价于$p[kp+3k-2]\ge0$。这里保留整数性，没有误用于连续0<z<1。D的真实偏离收益至少$F-(k/2)[d-d_L+(k-2)e]$。末位最佳回复结合(2)给
\[
F\le v_C+(k/2)d+(k/2-5/4)d_L+(k^2/2)e.\tag{4}
\]
k≥3时$d_L$系数非负，代$d_L\le d\le4e$及$v_C\le s+e$得AP5。k2时该系数负，不能照用这一粗化；但此时没有中间后继，d=d_L，直接合并(4)再用$d\le4e$得$F\le s+6e$，仍是AP5。证明不除e或主题大小，C空、零客户亦成立。没有冻结actual后缀或把被强制C当作该分支优化者。

## 2. 七个真实源与三个索引回复族

旧十固定位为`ABCDEUVWXY`。actual路径ABCDE；第二位强制E后的真实路径AEUVW；第三位强制E后的真实路径ABEXY。可用AP源恰为

|路径|零基位置i|规定优化行动|余k|
|---|---|---|---|
|actual|0,1,2,3|A,B,C,D|5,4,3,2|
|second|2,3|U,V|3,2|
|third|3|X|2|

两条强制E槽及所有末位被排除；不能用它们强制动作的收益当当前规定最优收益。若标签/历史重合，仍来自同一σ，不能为同一个有序节点指定两份不同回复。

固定五个合法比较索引$T_i$，可重复，是否最优不影响AP必要性。三个真实族为
\[
AB_i=(A,B,T_i,R_i,S_i),\quad AE_i=(A,E,T_i,R'_i,S'_i),
\quad S_i^{branch}=(A,T_i,U_i,V_i,W_i).
\]
AB/AE取两最终回复菜单，Sbranch取三回复菜单。代码名mX/mY与mU/mV/mW是**索引菜单**，不可与十固定位X/Y/U/V/W的单个标签混淆。每项都是同目录合法主题，故可在任意上述源作C或D；重复项仍按索引重数求和。

## 3. 单对行、笛卡尔求和及根7125式

设$a_k=8(k-1)+k^2$。单客户C/D会员位c,d与该源当前利润贡献$v_x$给加倍AP行
\[
a_kv_x-\frac{(a_k-2)c+2cd}{p_x+k}-\frac{2d(1-c)}{p_x+1}.\tag{5}
\]
只有跨全部客户的总行保证非负，逐客户系数允许正负。长度$n_C,n_D$两合法菜单独立扫全部$n_Cn_D$对，客户会员次数为c,d，精确求和为
\[
\boxed{n_Cn_Da_kv_x-\frac{(a_k-2)n_Dc}{p_x+k}
-\frac{2n_Cd}{p_x+1}
+2\left(\frac1{p_x+1}-\frac1{p_x+k}\right)cd.}\tag{CART}
\]
其依据是$\sum_{i,j}c_id_j=(\sum_ic_i)(\sum_jd_j)=cd$。同名列表也扫全部笛卡尔积，i=j包含在内，无须未记录的索引配对。

根k5/p0/a57，单对总行是$57u_1-11|C|-2|D|+(8/5)|C\cap D|\ge0$。取C为Sbranch五个末回复$W_i$（原独审另记$J_i$），D为五个$T_j$。令$J_x=\sum_i1_{W_i}(x)$、$t_x=\sum_j1_{T_j}(x)$。25行求和再乘5恰得
\[
\boxed{7125u_1-275\sum_xJ_x-50\sum_xt_x+8\sum_xJ_xt_x\ge0.}\tag{ROOT-JT}
\]
这不是只扫i≠j，亦不容逐客户选择有利配对；重复菜单、空题和相同T均按合法行重复计数。

## 4. 所写AP集合的单族定价闭包

原子记录十固定位、共同比较次数t、AB/AE各8格三元直方图及Sbranch16格四元直方图，均含5个索引。固定十位与t后，菜单计数是其同族完整直方图的线性函数。CART只含常数/c/d/cd；菜单一端来自一个族、另一端为固定位/比较列表/同族菜单时，新增目标只依该族。

源码menu_specs恰限这些组合，没有新增跨族C×D：AB/AE每族每源48规格，Sbranch每源75，乘7共1197菜单行；每源100固定标签对加1个opt×opt，另707固定行；连旧717，理论2621行。这是从规格列表推得的计数，非本次实际初始化日志。

family_score把新项化成常数、单计数、同族两计数乘积，变量名排序合并相同单项式，平方保重复变量。缓存key保旧key及全部新单项式系数；常数在缓存取回后另加，无需把它错误地说成直方图score缓存的一部分。旧菜单$(\ell,h)$不出现在新项，原仿射四角最大化因此保持。

707固定行只依十位/t，正确追加base张量；ec/hc追加零，因为新行不含旧$(\ell,h)$。oldids追加其固定列索引，旧crossweights仍来自原`lam[557:717]`，不能按扩展后的末160列误切到AP。wrapper显式调用BaseUniverse.price并先设旧crossweights/清cache，避开CrossUniverse.price原来的尾160切片合同。

全文读了既有15042B full_pricing与6342B cross_pair_pricing的常数、family_score/price和完整运行尾段，没有import或执行。新代数确认附加项不引入跨族乘积；不是仅凭源码阅读重新认证全部旧oracle、旧行缩放或全型最优。跨族C×D一般会引入两个独立直方图的乘积，不能免费沿当前三族可加式处理。

## 5. 原有限核验与没有完成的全树付款

audit_menu_ap.py设计为：规范ExactSPESolver生成四个小输入的完整五人策略，再逐历史检查所有行动；从同一动作函数抽actual/second/third及三回复族。逐客户算压缩CART，另独立扫所有合法主题对AP5，逐行断言值相同且非负。四输入含单空题、含空题小目录、大题单例和重叠目录。

该源码仍导规范solver和menu_ap_pricing/旧oracle依赖，不能称零依赖独立发现器。main旁写audit_menu_ap.json，并打印去掉cases的摘要。本批未执行它或读取其冻结输出绑定新运行，没有重跑全型定价。

闭包只针对所写必要行族。索引相等模式、同主题/同历史一致性和所有真实后继最优性没有被直方图自动补全。二以上有理primal仅否该必要行模板足够，不构成坏SPE；普遍上界需非负有理dual及整个允许原子域上的精确余项，float CG与有限回放本身不承担。AP合法性、特定定价闭包与一般half分开保存。

原件及0-run边界见[审查证据](../../tools/evidence/tail-potential-and-static-matching-primary/a4-review/README.md)。另一主源README的候选时态/匹配与S5独有内容见[对抗分支资源](../资源/第十三轮对抗分支的匹配反例与索引对称化边界--资源.md)。
