# 两权类别的双排序混合势：平方根次数存在界

本稿由 boss4 内部研究者推导，主研究者逐式重算；独立审查者先从精确命题重构，再攻击冻结稿。
本稿由精确模型独立推导，未作全球新颖性声明。一般证明与有限计算分开。

## 精确命题身份

**ID/version：WC-TWO-WEIGHT-ORDER-BLEND-v1。中文名称：两权类别双排序混合势。**

**Exact Statement / Objects / Domain / Quantifiers。** 对每个整数 `d>=2`，
对 [MODEL](../../../weighted_congestion_frontier/MODEL.md) 中每个有限加权原子拥塞博弈 G，若存在两个实数 `a>=b>0`，
使所有玩家权重都属于 `{a,b}`，则 G 存在

\[
 A_d=\frac{1+\sqrt{4d-3}}2
\]

近似纯 Nash 均衡。下文显式资源可加势的每个单边局部最小点都是
`A_d`-PNE，且每个严格 `A_d` 改善都使势严格下降。
两类别中人数任意、权比任意、每类可以仅有一人；不要求两类都非空。
不同玩家策略族可不同，策略可以是任意资源子集并可为空；费用系数为任意
非负实数，允许零费用、常数项及混合次数。玩家成本不乘其权重。
`A_d` 不依赖人数、权比、资源数、策略数或费用系数。

**Definitions。**
令 `m_e(s)`、`n_e(s)` 为资源 e 当前的 a 权、b 权用户数（`a=b` 时任意固定
一种分组即可，亦可直接使用下述一权精确势）。对每个费用多项式 c，定义

\[
 D_c(m,n)=a\sum_{j=1}^{m}c(ja)
       +b\sum_{k=1}^{n}c(ma+kb),
\tag{1}
\]

\[
 U_c(m,n)=b\sum_{k=1}^{n}c(kb)
       +a\sum_{j=1}^{m}c(nb+ja).
\tag{2}
\]

空和为零；D 是按权非增排序的加权右端点离散积分，U 是按权非减排序的积分。
令

\[
 \lambda_d=\frac{1+\sqrt{4d-3}}{2(d-1)}>0,
 \qquad F_c=D_c+\lambda_d U_c,
 \qquad \Phi(s)=\sum_e F_{c_e}(m_e(s),n_e(s)).
\tag{3}
\]

**Assumptions / Scope。** `d>=2` 的主式用于全次数至多 d 的两权类别子类，
并不假设单项式、单资源策略或同构策略。`d=0,1` 的精确 PNE 单独证明。
该结论不是任意多权类别的全类 `O(d/ln d)` 上界。

**Conclusion。** 因 `A_d^2-A_d=d-1`，有 `A_d=O(sqrt(d))=o(d/ln d)`。
这里后者只是两权类别的渐近比较；不改变主问题全类量词。
不作多项式时间计算均衡的断言。

**Dependencies。** 仅费用非减性、凸性、逐单项式导数估计、有限状态势下降。
没有导入外部存在定理。

**Evidence。** 下文完整一般证明；配套 `verify_order_blend.py` 使用 Fraction
穷举其明示有限参数的资源插入边及有理混合参数。计算不替代证明。

**Counterevidence / Objections。** 任意多权类别下的局部势线性障碍不适用于
本命题的两权范围；不得把本结论外推到所有权重。两类顺序的末类边际恒等式
是承重结构，在三类中没有同时保留。

**Status。** 完整一般证明；内部独立重构与冻结攻击见配套审查。未外审；
新颖性未评估。Truth：所述子类存在性；Value：稠密两权 cohort 的跨尺度接口；
Mechanism：两个排序势的互补精确边际；Ambition：全类目标仍开放。

## 1. 凸排序交换

对任意非减凸费用 c，考虑某排列前缀负载 x，两个相邻权重 `a>=b>0`，
共同终点 `z=x+a+b`。把重权排前、轻权排后的积分贡献减去反向排列贡献，得

\[
 a c(z-b)+b c(z)-b c(z-a)-a c(z)
 =ab\left(\frac{c(z)-c(z-a)}a
              -\frac{c(z)-c(z-b)}b\right)\le0.
\tag{4}
\]

末端为 z 的较短区间 `[z-b,z]` 的割线斜率不小于较长区间 `[z-a,z]`
的割线斜率；这是凸性的直接结论。交换不改变后续负载，所以反复交换给出：
在任何有限用户多重集中，D 最小化所有排列的加权离散积分，U 最大化。
所有非负系数多项式均非减且凸，包括常数、仿射及零多项式。

## 2. 四个单资源插入估计

以下每次均在插入后真实总负载 Y 上评价费用；不存在冻结旧负载。

### 重权插入

原来有 m 个重权和 n 个轻权，加入一名重权 a，`Y=(m+1)a+nb`。
由式(2)，U 中重权位于末端，因此

\[
 \Delta_a U=a c(Y).
\tag{5}
\]

D 中自身新贡献为 `a c((m+1)a)`，所有轻权的前缀负载增加 a，所以
`Delta_a D>=0`。把新增重权先放在旧降序排列的最后是一种候选排列，贡献
恰增加 `a c(Y)`；D 是所有排列的最小值。因此

\[
 0\le\Delta_a D\le a c(Y).
\tag{6}
\]

### 轻权插入

原来有 m 个重权和 n 个轻权，加入一名轻权 b，`B=(n+1)b`、`Y=B+ma`。
D 的轻权位于末端，故

\[
 \Delta_b D=b c(Y).
\tag{7}
\]

把新增轻权放在旧升序排列最后是一种候选排列；U 最大化排列积分，故

\[
 \Delta_b U\ge b c(Y).
\tag{8}
\]

上界按费用系数非负逐单项式证明。若 `c(x)=x^k`、`1<=k<=d`，由式(2)

\[
 \Delta_b U=b B^k
   +a\sum_{j=1}^m[(B+ja)^k-(B-b+ja)^k].
\]

每个差由导数积分不超过 `k b(B+ja)^{k-1}`，后者不超过 `k bY^{k-1}`。
于是令 `t=B/Y`（Y>0，`0<t<=1`），有

\[
 \frac{\Delta_b U}{bY^k}
 \le t^k+k(1-t)\le k\le d.
\tag{9}
\]

中间一步用 `t^k<=t` 和 `k>=1`：`t^k+k(1-t)<=k-(k-1)t<=k`。
当 `k=0` 时所有外部差为零，`Delta_b U=b`，也不超过 `d b`。
逐项相加，包括系数为零的项，得到

\[
 b c(Y)\le\Delta_b U\le d b c(Y).
\tag{10}
\]

全程没有除费用；式(9)中单项式的 Y>0 由新加入的正权玩家保证。
零费用由线性组合直接包含。

## 3. 混合与共同玩家乘子

先任取 `lambda>0`，定义 `F=D+lambda U`。式(5)--(10) 给出

\[
 \lambda a c(Y)\le\Delta_aF\le(1+\lambda)a c(Y),
\tag{11}
\]

\[
 (1+\lambda)b c(Y)\le\Delta_bF\le(1+d\lambda)b c(Y).
\tag{12}
\]

因此玩家共同乘子可以取

\[
 h_i=\begin{cases}\lambda a,&i\text{ 属于固定的 a 类},\\
                 (1+\lambda)b,&i\text{ 属于固定的 b 类},
      \end{cases}
\quad
 A(\lambda)=\max\left\{\frac{1+\lambda}{\lambda},
                       \frac{1+d\lambda}{1+\lambda}\right\}.
\tag{13}
\]

这些乘子在全部资源上相同，只依玩家所属类别、两权值及 d；资源系数和用户数
任意变化不影响它们。第一分式递减、第二分式（d>1 时）递增；相等条件是

\[
 (d-1)\lambda^2=1+\lambda.
\]

正解为式(3)的 `lambda_d`。此时 `A=1+1/lambda_d`，消元得
`A^2-A=d-1`，唯一大于 1 的根即 `A_d`。这同时核对了式(3)的根与混合参数。

## 4. 任意多资源偏离与边界

令 `s'=(t_i,s_-i)`，`D_i=s_i\t_i`、`A_i=t_i\s_i`、`H_i=s_i∩t_i`。
保留资源用户集合和负载均完全不变。删去一资源的势减少量正是对应逆向插入
边际，至少为 `h_i c_e(x_e(s))`；新加入一资源的势增加至多为
`A_d h_i c_e(x_e(s'))`。所以

\[
 \Phi(s')-\Phi(s)
 \le h_i[A_d C_i(s')-C_i(s)-(A_d-1)C_{i,H_i}(s)]
 \le h_i[A_d C_i(s')-C_i(s)].
\tag{14}
\]

若 `C_i(s)>A_d C_i(s')`，正乘子 h_i 使右边严格负。因此每个单边局部最小点
满足全部弱近似均衡不等式。状态集有限非空，所以全局最小点存在；任何严格 `A_d`
改善路径也终止。允许任意正实权、任意实系数时只用有限性，不需计算可表示性。

空旧策略、空新策略、所有费用为零均由式(14)覆盖；正成本偏离到零成本时势
严格减少，没有使用 `0/0`。资源上缺失某一类时公式仍是空和，所有估计成立。
潜在用户只属于一类的资源无须额外处理。

`a=b` 时可直接把所有玩家视为同一类，资源势
`a sum_{j=1}^{|S_e|}c_e(ja)` 的边际为 `a c_e(Y)`，所以存在精确 PNE。
若保留任意双分组，则 D=U 为此势，所给较弱 A_d 结论仍然成立。

`d=0` 时每名玩家独立选择最低常数成本策略，得到精确 PNE。
`d=1` 时 c(x)=ell x+beta，资源势

\[
 \tfrac\ell2\left(x_e(s)^2+\sum_{i:e\in s_i}w_i^2\right)
       +\beta x_e(s)
\]

的插入边际恰为 `w_i c_e(Y)`，不限权种类，给出精确 PNE。
`lambda_d` 的式子不在 d=1 代入。

## 5. 已检查来源与限度

本次有限文献核对读取 Caragiannis--Fanelli, ICALP 2019, pp.133:3--4：
<https://drops.dagstuhl.de/storage/00lipics/lipics-vol132-icalp2019/LIPIcs.ICALP.2019.133/LIPIcs.ICALP.2019.133.pdf>。
该处回顾 Hansknecht 等的按权非减离散积分近似势；这支持排序势本身已有来源，
不把双排序混合及两权范围称为新颖。还检索了 two weights / weight classes /
ascending descending 的原始论文线索，没有完成穷尽优先权审查。

已检查仓库两权仿射工具、有序尾部冻结与窄带势；本命题覆盖任意尾部总重与权比，结论仍只对全局两权类别成立。来源核对不认证优先权；当前全类主问题仍然没有结论。

## 6. 审查与复现

- 独立重构和冻结攻击：[审查记录](../../../reviews/weighted_congestion/weight_types/two_weight_order_blend_review.md)。
- 作者精确核验：`tests/audits/weighted_congestion/weight_types/verify_order_blend.py`。
- 独立真实资源实现：`tests/audits/weighted_congestion/weight_types/independent_order_blend.py`。
- 冻结结果：`evidence/runs/weighted_congestion/weight_types/order_blend.json` 与 `independent_order_blend.json`。

从仓库根运行上述程序并传 `--output NEW_PATH`；均用独占创建避免覆盖冻结证据。正文证明任意实参数命题，有限核验只检查实现及边界。
