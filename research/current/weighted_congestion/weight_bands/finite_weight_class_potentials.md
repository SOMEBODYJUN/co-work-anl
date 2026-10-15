# 有限权类别的三角排序混合势：隐式次数界与背景吸收

作者为 boss4 内部研究者，主研究者逐式重算；独立重构瓶颈及冻结攻击范围由配套审查分别记录。
本稿给出有限权类别的完整一般证明，并统一两权专用的最优混合参数。
它把显式 B 包络保留为推论，主陈述使用新的三角排序 A 机制；两权命题 `WC-TWO-WEIGHT-ORDER-BLEND-v1` 身份不变。
此处“最优”只指两权稿所用两个边际包络的参数平衡，不声称存在阈值最优。

## 精确身份与全部范围

**ID/version：WC-WEIGHT-CLASS-TRIANGULAR-POTENTIAL-v1。中文名称：有限权类别三角排序混合势。**

**Objects / Domain。** [MODEL](../../../weighted_congestion_frontier/MODEL.md) 的有限加权原子拥塞博弈：正实玩家权、有限非空
资源集、任意非空有限资源子集策略族、允许空策略；费用是非负实系数、次数至多
整数 d 的多项式。成本不乘权重，偏离费用按偏离后真实负载计算。

**Definitions。** 固定整数 `d>=2,k>=1`，令 `A_{d,k}` 是方程

\[
 A=\sum_{j=0}^{k-1}\left(\frac{d-1}{A}\right)^j
\tag{1}
\]

在 `[1,d)` 中的唯一根。`k=1` 时根为 1。另定义可显式核对的上界

\[
 B_{d,k}=\frac{d-1}{d^{1/k}-1}
        =\sum_{j=0}^{k-1}d^{j/k}.
\tag{2}
\]

**Exact Statement / Quantifiers / Conclusion。** 对每个 `d>=2,k>=1`，每个玩家
权重至多取 k 个不同值的 MODEL 博弈均存在 `A_{d,k}`-PNE。若实际不同权值数
恰为 k，下面显式定义的资源可加势在每个严格 `A_{d,k}` 改善下严格下降，其
每个单边局部最小点均是 `A_{d,k}`-PNE。人数、类别人数、权比、费用系数、
资源及策略数不出现在倍率中。对任意实权/实系数只主张有限存在，不主张多项式
时间或实数输入可计算性。

**Additional exact conclusions。** `1<=A_{d,k}<=B_{d,k}`、`A_{d,k}<d`，
`A_{d,k}` 随 k 非减。每个固定 k 有 `A_{d,k}~d^{1-1/k}`（k=1 时均为 1）。
对于每个 `d>=16`，若 `k<=ln d/ln ln d`，则存在 `(2d/ln d)`-PNE。
这些都保留类别数限制，不是 MODEL 全类的匹配上界。

**Dependencies。** 仅凸排序交换、单项式导数估计、正系数混合、有限状态最小化。
没有导入外部均衡存在定理。

**Evidence / Status。** 完整 authored proof 在下文；有限 Fraction 核验另列。
独立审查从精确命题重构瓶颈后攻击冻结稿；另一份审查明确属于知悉构造后的攻击。两者真实范围分别记录。未外审，未认证全球新颖性。

**Counterevidence / Objections / Scope。** k 是全游戏的权类别数，不能用每个
资源各自的种类数替换。共同玩家乘子必须在全部资源一致。k 可任意大，而固定 d
时 `A_{d,k}` 趋近 d；因此本定理没有绕过任意多尺度的局部势障碍。它没有给出
任意多权类别的全类 `O(d/ln d)` 存在证明或否定证明。

**Related Files。** [两权专稿](two_weight_order_blend.md)保持原身份；本稿规范审计、独立审查和冻结证据见末节。

## 1. 根的存在、比较与基本量词

对 `x>0` 令 `f_k(x)=sum_{j=0}^{k-1}((d-1)/x)^j-x`。它连续严格递减，
`f_k(1)>=0`；又

\[
 \sum_{j=0}^{k-1}\left(\frac{d-1}{d}\right)^j
 <\sum_{j=0}^{\infty}\left(\frac{d-1}{d}\right)^j=d,
\]

故 `f_k(d)<0`。唯一根因此位于 `[1,d)`。增加 k 给 f 加一正项，故根非减，
这使“至多 k”由实际类别数版本推出。

令 `q=d^{1/k}>1`，则 `B=B_{d,k}=sum_{j=0}^{k-1}q^j=(d-1)/(q-1)`。
反算 `(d-1)/B=q-1`，于是

\[
 f_k(B)=\sum_{j=0}^{k-1}(q-1)^j-\sum_{j=0}^{k-1}q^j\le0.
\tag{3}
\]

严格递减性给出 `A_{d,k}<=B_{d,k}`。

## 2. 任意固定排序的边际上界

资源费用为 c。对任意当前用户排列，定义其加权右端点积分：每名用户以自身权
乘以加入后该前缀负载的费用，再求和。插入正权 w 的用户，插入前缀负载为 X，
其后用户权依次 `v_1,...,v_m`。令

\[
 Y=X+w+\sum_jv_j>0,\qquad z_j=X+w+\sum_{l\le j}v_l\le Y.
\]

新旧积分之差是

\[
 \Delta P=w c(X+w)+\sum_{j=1}^m v_j[c(z_j)-c(z_j-w)]\ge0.
\tag{4}
\]

若 `c(x)=x^p,1<=p<=d`，差项不超过 `p w z_j^{p-1}`。以
`u=(X+w)/Y∈(0,1]` 记，得到

\[
 \Delta P\le wY^p[u^p+p(1-u)]\le p wY^p\le d wY^p.
\tag{5}
\]

第二步用 `u^p<=u`。常数项 p=0 的边际恰为 w；非负线性组合遂给出

\[
 0\le\Delta P\le d w c(Y)
\tag{6}
\]

对允许的所有 c 成立，包括零费用。

## 3. 轻重后缀的互补比较

对凸 c，两相邻权 `a>=b>0`，共同终点 z，重后轻与轻后重的积分之差为

\[
 a c(z-b)+b c(z)-b c(z-a)-a c(z)
 =ab\left(\frac{c(z)-c(z-a)}a
          -\frac{c(z)-c(z-b)}b\right)\le0.
\tag{7}
\]

末端相同的短区间割线斜率较大。后续负载不变，故可依次交换 mover 与其后用户：

* 后缀每个用户的权均不超过 mover 的 w，则把 mover 移到最后只会增大积分，
  因而 `Delta P<=w c(Y)`。
* 后缀每个用户的权均不小于 mover 的 w，则移到最后只会减小积分，
  因而 `Delta P>=w c(Y)`。
* 后缀为空，边际恰为 `w c(Y)`。

非负系数多项式均凸且非减。相同权的交换为等号，类别内部具体次序无影响。

## 4. 三角排序与共同乘子

将实际权值记为 `a_1>...>a_k>0`。对每个 `r=1,...,k`，定义类型排列

\[
 \pi_r=(k,k-1,\ldots,r+1,1,2,\ldots,r).
\tag{8}
\]

即先把比 r 轻的类别按权非减排入，再把类别 1 到 r 按权非增排入。
空区段略去。令 `P_{r,c}(n_1,...,n_k)` 为按该排列、各类内部逐名加入用户的
加权右端点积分。形式上，若 `L_{r,g}=sum_{h先于g} n_h a_h`，则

\[
 P_{r,c}(n)=\sum_{g\text{按}\pi_r\text{排列}}
     a_g\sum_{j=1}^{n_g}c(L_{r,g}+j a_g).
\tag{9}
\]

类型 i 的新用户在该类型末端插入，插入后总负载为 Y。
若 `r<i`，类型 i 位于升序前区，全部后缀用户均比它重（或同权），所以第3节
给下界 1、第2节给上界 d。若 `r=i`，该类型位于整个排列最后，边际精确。
若 `r>i`，类型 i 位于降序后区，其后均比它轻，所以下界 0、上界 1。
概括为

\[
\begin{array}{c|c}
 r<i & a_i c(Y)\le\Delta_iP_{r,c}\le d a_i c(Y)\\
 r=i & \Delta_iP_{r,c}=a_i c(Y)\\
 r>i & 0\le\Delta_iP_{r,c}\le a_i c(Y).
\end{array}
\tag{10}
\]

任何类型当前无人时，这些用户后缀陈述仍有效；插入者自身保证 Y>0。

令 `A=A_{d,k}`、`t=(d-1)/A>0`，定义

\[
 \lambda_r=\frac{t^{r-1}}A>0,\quad
 S_i=\sum_{r=1}^{i}\lambda_r,\quad S_0=0,\quad
 F_c(n)=\sum_{r=1}^k\lambda_rP_{r,c}(n).
\tag{11}
\]

根方程(1)恰好保证 `sum_r lambda_r=1`。从式(10)

\[
 S_i a_i c(Y)\le\Delta_iF_c
 \le[1+(d-1)S_{i-1}]a_i c(Y).
\tag{12}
\]

逐式反算其上系数：

\[
 1+(d-1)S_{i-1}
 =1+t\sum_{j=0}^{i-2}t^j
 =\sum_{j=0}^{i-1}t^j=A S_i.
\tag{13}
\]

因此每个类型 i 的玩家具有跨全部资源一致的正乘子 `h_i=S_i a_i`，并满足

\[
 h_i c_e(Y)\le\Delta_iF_{c_e}\le A h_i c_e(Y).
\tag{14}
\]

这些数只依 d、k 和该玩家的权类别；费用、多资源策略及各资源的当前用户数均
不改变 h。资源局部类别数不足以定义这里的全局 i，故不在量词范围内。

## 5. 任意偏离、零成本及次数端点

定义 `Phi(s)=sum_e F_{c_e}(n_e(s))`。在偏离 `s'=(t_i,s_-i)` 中，保留资源
的用户集和负载不变；删去资源的势减少至少是 h_i 乘旧费用；新加入资源的势
增加至多 A h_i 乘偏离后真实费用。设保留资源成本为 `C_H>=0`，则

\[
 \Phi(s')-\Phi(s)
 \le h_i[A C_i(s')-C_i(s)-(A-1)C_H]
 \le h_i[A C_i(s')-C_i(s)].
\tag{15}
\]

每个严格 A 改善严格降势。状态空间有限非空，全局最小点存在；任何单边局部
最小点满足全部弱近似均衡不等式，全部严格 A 改善路径终止。

空旧策略、新策略、缺席类别和全零费用都已包含；正成本偏离到零成本时式(15)
严格负，没有除任何玩家成本。相同权值先合成一类；若 k=1，式(1)根为 1，
资源势就是同权标准离散积分，结论精确。k=2 时式(1)给
`A^2-A=d-1`，得到原两权稿 `(1+sqrt(4d-3))/2` 的同一存在界，原 ID 不变。

d=0 时各玩家独立选最低常数费用策略得到精确 PNE。
d=1 时全类资源仿射势

\[
 \frac{\ell_e}{2}\left(x_e(s)^2+\sum_{i:e\in s_i}w_i^2\right)+\beta_e x_e(s)
\]

的插入边际恰为 `w_i c_e(Y)`，也得到精确 PNE；不需要在本文 d>=2 参数中
代入 d=1。单个玩家或某资源只有一类用户同样被直接覆盖。

## 6. 显式目标量级子类与权类别必要条件

式(3)给 `A<=B`。固定 k>=2 时 `B=O_k(d^{1-1/k})`，而根方程中末项给
`A^k>=(d-1)^{k-1}`。从上界知 `t=(d-1)/A` 趋于无穷，因此
`A/t^{k-1}=sum_{j=0}^{k-1}t^{j-(k-1)}` 趋于 1，得出所述渐近等价。

若 `d>=16`、`k<=ln d/ln ln d`，则 `ln d>2` 且
`d^{1/k}>=ln d`。于是

\[
 A_{d,k}\le B_{d,k}\le\frac d{\ln d-1}\le\frac{2d}{\ln d}.
\tag{16}
\]

因此这一**类别受限子类**满足显式 `C=2,d0=16` 的目标倍率。

一项只用较粗 B 式的严格必要条件是：若 degree<=d 的某游戏没有 alpha-PNE，
`alpha>=1`，则实际权类别数满足

\[
 k>\frac{\ln d}{\ln(1+(d-1)/\alpha)}.
\tag{17}
\]

否则 B<=alpha，已给出 alpha-PNE，矛盾。它是全局类别数的限制，不断言某坏
状态同时活跃这么多类别。目标 `alpha=C d/ln d` 时右边渐近 `ln d/ln ln d`。
该结论不是新非存在族，也不限制类别数没有统一上界的全模型。

## 7. 固定玩家背景的精确吸收

**明确推论 WC-WEIGHT-CLASS-FIXED-BACKGROUND-v1。** 对每个 d>=2 和 MODEL
游戏，把策略族恰为单元素的玩家称为固定玩家，其余称为可动玩家。若可动玩家
的不同权值至多 k>=1，则即使固定玩家的权类别任意，原游戏仍有 `A_{d,k}`-PNE。
若没有可动玩家，唯一状态为精确 PNE。固定玩家唯一策略可以是任意资源子集，
包括空集；本推论不要求可动玩家有严格有利偏离。

**证明。** 固定玩家在资源 e 上形成固定背景负载 `B_e>=0`。删去这些玩家，
把剩余资源费用改为 `c'_e(x)=c_e(B_e+x)`。若
`c_e(x)=sum_{j=0}^d a_{e,j}x^j`，则

\[
 c'_e(x)=\sum_{r=0}^d
   \left[\sum_{j=r}^d a_{e,j}\binom jr B_e^{j-r}\right]x^r,
\tag{18}
\]

仍为非负系数、次数至多 d 的费用。可动玩家全部状态和真实偏离费用逐一相同。
若可动玩家非空，应用主定理；恢复固定玩家后其偏离约束是自偏离等式，其他玩家
的全部约束不变。若为空则全部约束显然满足。未假定固定背景可由零权替代。

## 8. 近似有限权簇的单向取整

**明确推论 WC-WEIGHT-CLASS-CLUSTER-ROUNDING-v1。** 对每个 d>=2、k>=1、
每个实数 R>=1 和 MODEL 游戏，允许任意固定玩家。若存在 k 个正代表权
`v_1,...,v_k` 及对每个可动玩家 i 的固定标签 tau(i)，使

\[
 v_{\tau(i)}\le w_i\le R v_{\tau(i)},
\tag{19}
\]

则原游戏存在 `R^d A_{d,k}`-PNE。代表权不必全部被使用；可合并重复代表权。
该推论只限制可动玩家权，固定玩家不取整。

**证明。** 保持所有策略、费用和固定玩家，把每个可动玩家权向下改为代表权。
记任意相同状态（包括每个真实偏离后状态）下的原负载和取整负载为 x、x'。
固定背景非负，所以 `x'<=x<=R x'`。非负系数次数至多 d 给

\[
 c_e(x')\le c_e(x)\le R^d c_e(x'),
 \qquad C'_i(s)\le C_i(s)\le R^d C'_i(s).
\tag{20}
\]

包括 x'=0、常数、零费用：若 x'=0，则 x=0，直接比较多项式即可。
取整游戏由第7节有 `A_{d,k}`-PNE s，且对每个偏离

\[
 C_i(s)\le R^d C'_i(s)
 \le R^d A_{d,k}C'_i(t_i,s_-i)
 \le R^d A_{d,k}C_i(t_i,s_-i).
\tag{21}
\]

固定玩家约束仍然恒真。无可动玩家时结论精确。
特别地 R=exp(1/d) 时损失恰为 e；若同时 d>=16 和
`k<=ln d/ln ln d`，则该明确子类有 `(2e d/ln d)`-PNE。
本推论没有给出任意权谱可用这么少窄簇覆盖的断言。

## 9. 来源、审查合同与剩余义务

排序离散积分已有文献来源。本次读取 Caragiannis--Fanelli, ICALP 2019,
pp.133:3--4 对 Hansknecht 等排序势的回顾：
<https://drops.dagstuhl.de/storage/00lipics/lipics-vol132-icalp2019/LIPIcs.ICALP.2019.133/LIPIcs.ICALP.2019.133.pdf>。
该来源不用于导入本文三角混合定理；未完成权类别相关文献的穷尽优先权核查。

独立攻击应绑定本文 hash，并核对根的全部量词、式(4)--(15)的后缀顺序、类别
缺席、零/常数费用、任意保留资源、式(18)的非负系数以及式(20)在零负载的
边界。旧 B 草稿的先独立重构不计为对本文新 A 机制的先独立重构。

Truth、Value、Novelty、Mechanism、Ambition 分开：本文是经过内部独立攻击的一般子类
证明，有明确复用接口；不因有限核验、入 main 或推送而升级为全类结论。
全类仍缺对无界不同权类别数的均衡选择机制，或一族超目标的全状态非存在构造。

## 10. 正式审查与复现入口

- [先独立重构瓶颈后冻结攻击](../../../reviews/weighted_congestion/weight_types/finite_weight_classes_reconstruction_review.md)。
- [知悉新构造后的另一份独立攻击](../../../reviews/weighted_congestion/weight_types/finite_weight_classes_informed_review.md)。
- 作者精确核验：`tests/audits/weighted_congestion/weight_types/verify_triangular_classes.py --output NEW_PATH`。
- 独立核验：`tests/audits/weighted_congestion/weight_types/independent_triangular_classes.py`，仅stdout。
- 冻结运行：`evidence/runs/weighted_congestion/weight_types/triangular_classes.json` 与 `independent_triangular_classes.json`。

式(17)结合固定背景吸收，还可把 k 计为可动玩家的实际权类别数；非存在时可动集必非空。它仍不是某单个坏状态活跃类别的下界。

为说明固定 d、k→∞时的精确边界，令单调根极限L≤d。若L≤d−1，根右侧的k项和无界，矛盾；否则(d−1)/L<1，几何和极限给L=1/[1−(d−1)/L]，故L=d。

Status：complete structural proof; independently reconstructed and exactly audited; unrefereed。上述审查分别记录实际重构范围；有限核验不承担任意实参数、任意类别数的一般证明。
