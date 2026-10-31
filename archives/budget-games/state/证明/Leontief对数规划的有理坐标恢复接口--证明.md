---
id: budget-games/leontief-log-program-polybit-rational-coordinate-recovery
kind: proof
type_tag: 证明
title: Leontief对数规划的有理坐标恢复接口
status: proved-interface-with-standard-weak-optimization-backend; known-backup
summary: 明确KKT、分母界、内球与oracle、曲率精度和有理恢复；导入标准位多项式弱凸优化工具，不把有理坐标误作有理目标值。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/notes/leontief_fisher_known_interface.md#5
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/multi_lane/research/topic_selection/notes/leontief_fisher_known_interface.md
---

# Leontief对数规划的有理坐标恢复接口

本页完整展开主源的四项备线义务。模型、删退化输入及临界支持引理同[精确Fisher对应](../等价/Leontief贡献矩阵与线性Fisher支出的精确对应--等价.md)。取$n,m\ge1$、$b_i>0,\sum b_i=1$，每行列非空；把每行估值正比例归一为$\sum_jv_{ij}=1$，不改变偏好或NE，只改变报告的效用单位。所有输入二进制有理。

## 对数规划、KKT与唯一性

考虑凸可行域上的凹最大化

$$\max\sum_i b_i\log u_i,\qquad
 \delta\ge0,\ \sum_j\delta_j=1,\quad \delta_j\ge v_{ij}u_i,\quad u_i>0.\tag{P}$$

均匀$\delta$、充分小的正$u$给Slater点。正最优存在：可行域的闭包有界（$u_i\le1$），而任一$u_i\downarrow0$使目标趋负无穷。

约束$\delta_j-v_{ij}u_i$的乘子为$\lambda_{ij}\ge0$，总量乘子为$\tau$。最优正$u$及每列非空使$\delta_j>0$，KKT为

$$\frac{b_i}{u_i}=\sum_j\lambda_{ij}v_{ij},\quad
 \sum_i\lambda_{ij}=\tau,\quad
 \lambda_{ij}(\delta_j-v_{ij}u_i)=0.$$

第一式乘$u_i$、求和并用互补松弛，得$1=\sum_{ij}\lambda_{ij}\delta_j=\tau$。令$X_{ij}=\lambda_{ij}\delta_j$，则行和$b_i$、列和$\delta_j$，正支出只在临界边，所以是NE。反之任一NE，置$u_i=U_i(\delta)$、$\lambda_{ij}=X_{ij}/\delta_j$，临界支持保证上述各式，因而是(P)最优。没有把只给总量的优化解直接充当贡献矩阵。

NE单人按$v_i$比例分配给$u_i\ge b_i$；又$\sum_j\delta_j\ge u_i\sum_jv_{ij}=u_i$，故$u_i\le1$。严格凹的$\sum b_i\log u_i$使所有最优$u$一致为$u^*$。令$M_j=\max_i v_{ij}u_i^*$，可行性给$\sum M_j\le1$；若严格小于一，所有$u_i$同比增大可改善目标，矛盾。因此$\sum M_j=1$且唯一最优总量$\delta_j^*=M_j$。

## 显式有理坐标分母界

只为存在性证明，固定真实临界边集$T_i$。在变量$(u,\delta,X)$中加入：
$\delta_j\ge v_{ij}u_i$、各真实临界等式、非临界支出$X_{ij}=0$、行和$b_i$、列和$\delta_j$以及所有变量$0\le\cdot\le1$。该有界有理多面体非空，且任一可行点都给NE，其$u$必为$u^*$。即使某点多出临界边也不破坏支持条件。

令$d_0=n+m+nm$，$Q$为所有**归一化后**估值与预算分母的乘积。乘$Q$后上述系数和右端绝对值至多$Q$。任一基本可行解的独立整数子矩阵阶不超过$d_0$；Hadamard及Cramer给每个坐标的分母至多

$$D=(d_0Q)^{d_0}.$$

因此$u_i^*$均有此界，$\log D=\operatorname{poly}(n,m,L)$。计算这个界只需输入，**不枚举未知临界集**；固定临界集仅证明存在短表示，不是算法先知步骤。一般“log目标+线性约束”本身并不保证有理最优。

## 弱优化的几何和oracle合同

置$b_{\min}=\min_i b_i$、$a=b_{\min}/(2m)$，限制$a\le u_i\le1$不排除最优。消去$\delta_m=1-\sum_{j<m}\delta_j$，得紧有理凸体$K\subset\mathbb R^{n+m-1}$。中心取$u_i=3/(4m),\delta_j=1/m$，可取内球半径

$$r=\frac1{16m(n+m)},\qquad R=n+m$$

为外球半径。中心每条$\delta_j-v_{ij}u_i$间隔至少$1/(4m)$；非消去列扰动至多$2r$，消去列至多$mr$，均小于间隔。$u$上下界、$\delta$非负亦留余量；$m=1$时没有$\delta$自由坐标，同界仍有效。

令$f=-\sum_i b_i\log u_i$。线性约束可精确有理分离，$\nabla_i f=-b_i/u_i$可精确计算；在$K$上$\|\nabla f\|_2\le\|\nabla f\|_1\le1/a$。值oracle也有位多项式实现：对正有理$t$写$t=2^ks$、$1\le s<2$，令$z=(s-1)/(s+1)\in[0,1/3)$，则

$$\log s=2\sum_{\ell\ge0}\frac{z^{2\ell+1}}{2\ell+1}.$$

尾项几何衰减；同法近似$\log2$，再算$k\log2+\log s$，可在$\operatorname{poly}(\text{输入位长},\log(1/\eta))$时间给误差$\eta$的有理值。无须精确比较大分母指数的加权乘积。

此处**导入**标准有限精度有理弱凸优化定理：给上述线性分离、次梯度、近似值oracle、内外球与Lipschitz界，能在输入位长及$\log(1/\varepsilon)$的多项式时间返回可行$\hat z$使$f(\hat z)-f^*\le\varepsilon$。可用有截断位长控制的ellipsoid实现；本页没有交付该实现或重证通用定理。仅写实数运算次数不够。它亦不是直接调用Jiang要求“最优YES或严格分离全部minimizers”的exact oracle；两种合同不能互换。

## 从目标误差恢复精确坐标

在$u_i\le1$上，$u$方向Hessian为$\operatorname{diag}(b_i/u_i^2)\succeq b_{\min}I$。最优点对可行方向的一阶项非负，故任一可行$\hat z=(\hat u,\hat\delta)$满足

$$f(\hat z)-f^*\ge\frac{b_{\min}}2\|\hat u-u^*\|_2^2.$$

取$\varepsilon=b_{\min}/(100D^4)$，得到

$$\|\hat u-u^*\|_2\le\frac{\sqrt{1/50}}{D^2}<\frac1{3D^2}.$$

分母不超过$D$的不同有理数距离至少$1/D^2$，所以每个坐标在此精度下唯一恢复。连分数判据$|x-p/q|<1/(2q^2)$保证真值为收敛分数；枚举多项式长度收敛分数，筛分母$\le D$及上述邻域即可精确恢复。$\log(1/\varepsilon)$为多项式，不能换成时间依赖$1/\varepsilon$的算法。

计算$\delta_j^*=\max_i v_{ij}u_i^*$，用精确等式找临界边；在其二分图做行供给$b_i$、列需求$\delta_j^*$的有理可行流，KKT保证流存在。容量及输出均短，得到实际$X$。归一化前的效用按行估值缩放还原，贡献矩阵不变。

## 为什么不能二分到“精确目标值”

两人预算各$1/2$，估值$v_1=(1,0),v_2=(2,2)$，NE总量$(1/2,1/2)$，原效用为$(1/2,1/4)$，加权几何平均$1/(2\sqrt2)$无有理编码。$u,\delta$有理不推出幂乘积目标有理。因此主源指出2509.08767v3 Thm5.3末段以目标编码长度支持二分有限命中的表述缺口；此例只反驳该推理步骤，不反驳NE存在、坐标有理或算法结论。

本页通过**坐标**分母界、曲率与弱优化绕过该问题。更短的同矩阵Fisher转移已经覆盖当前实例，因此此备线属于标准理性恢复范式的具体重构，非另一个新算法或新的凸优化工具。文献的实际读取范围与外部算法导入见[覆盖核查](../文献/Leontief精确接口的Fisher覆盖与凸优化来源--文献.md)，[原件和逐节去向](../../../../tools/evidence/cloning-leontief-potential/README.md)另存。
