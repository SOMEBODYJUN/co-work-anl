# 全树收益图的类型核、映射环流与真实额外线性空间

研究备份，2026-10-21。目标仍为一般 `Q-CAG-HALF`，**未证明半覆盖**。
以下 1--3 为自含代数/锥证明，4 为从定义完整精确核验的合法例。第4节已由同伴从完整 policy 独立重建全部120行、SCC及秩并通过；见 `../direct_global/audit_extra_lineality.py` 和 `../direct_global/extra_lineality_independent_audit.json`。1--3节的普遍证明未另作独立审查；无外审或新颖性认证。
本页接续 `R-7e9f44beea424d469713364afe7dd180/full_tree_dual/outcome_payoff_graph.md`，不修改该页结论。
Möbius 技术与现行 `research/current/customer_attraction/mobius_compiler.md` 的调和势反演有共同基础；这里计算的是固定总人数、允许重复行动的全部**收益顶点**的精确空间，不声称新颖性。

## 1. 全收益顶点的精确空间与全部通用类型核

固定人数 m>=1、主题标签 p>=1。类型 B 为 [p] 的非空子集，记 x_a(B)=1_{a in B}。
收益顶点 v=(q,a) 满足 sum q=m、q_a>0，收益型向量

\[
F_{q,a}(B)=\frac{x_a(B)}{q(B)}.
\]

分子为零时整项取零。令 d=min(m,p)，并令 V_d 为无常数项、次数至多 d 的 Boolean 多线性多项式空间。
则

\[
\operatorname{span}\{F_{q,a}\}=V_d,
\quad D:=\dim V_d=\sum_{k=1}^{d}\binom pk,
\tag{1}
\]

\[
\operatorname{span}\{F_v-F_u\}
=\{f\in V_d:f([p])=0\},\qquad \dim=D-1.
\tag{2}
\]

**证明。** F_{q,a} 只依赖 q 的支持 T，且 |T|<=m，故属于 V_d。
反向对每个非空 T、|T|<=d 取支撑恰为 T 的正整数 q，总和 m，并取 a in T。
F 的单项式 x_T 系数为

\[
\begin{aligned}
c_T&=\sum_{U\subseteq T\setminus\{a\}}
 \frac{(-1)^{|T|-1-|U|}}{q_a+\sum_{b\in U}q_b}\\
&=\int_0^1 t^{q_a-1}\prod_{b\in T\setminus\{a\}}(t^{q_b}-1)\,dt\ne0.
\end{aligned}
\tag{3}
\]

在 0<t<1 内被积函数的符号恒为 (-1)^{|T|-1}。按 |T| 递增消去低次单项式，得到所有 x_T，证明 (1)。
每个 F_v([p])=1/m，故所有顶点差落在式 (2) 右边。
固定任一顶点 F0，记 H=span{F_v-F0}。span{F_v}=span(F0,H)，而 H 在 [p] 处为零、F0([p])=1/m非零。因此 dim H=D-1，等于 V_d 内该评价核的维数；已有包含关系立即给 (2)。

若 L:e_v -> F_v 为完整顶点类型映射，顶点数

\[
V=p\binom{m+p-2}{p-1},
\]

因此全部通用核恰有维数 V-D。任何 z in ker L 都满足 sum_v z_v=0（在全类型处评价），故该核已经位于抽象零总质量空间。
这说明固定 m 的收益和任意至多 m 个主题的覆盖都只依赖截断交集矩

\[
M_T=\sum_{B\supseteq T}w_B,\qquad 1\le |T|\le m.
\tag{4}
\]

可行矩仍必须来自 w_B>=0，不能将 M_T 当任意非负数；高阶矩压缩不是去掉共同目录可实现性的许可。覆盖 1_{B cap J != empty} 的次数是 |J|<=m，因此也在同一空间。式 (1)--(4) 不是半覆盖预算。

## 2. 映射环流精确给出 SCC 以外的行锥线性空间

固定完整有序历史策略 sigma，保留其全部真实行和真实收益图 D。
令 A 的第 e 列为该真实行 Gamma_e=F_{head(e)}-F_{tail(e)}，故 A=L partial，partial 为抽象 incidence 映射。
行锥 K=A R_+^E。定义

\[
I_* =\{e:\exists t\ge0,\ At=0,\ t_e>0\}.
\tag{5}
\]

则有精确等式

\[
\boxed{\operatorname{lin}(K)=\operatorname{span}\{\Gamma_e:e\in I_*\}.}
\tag{6}
\]

**证明。** 若 At=0 且 t_e>0，

\[
-\Gamma_e=\sum_{f\ne e}(t_f/t_e)\Gamma_f\in K,
\]

所以每个被支持的真实行都双向可用。
反向，任意 z in lin(K) 可写 z=A lambda、-z=A mu，lambda,mu>=0；t=lambda+mu 满足 (5)，且 lambda 支持于 I_*，故 z 位于右侧 span。
有限 E 下可把各 e 的见证 t 相加，得到一条同时支持全部 I_* 的非负映射环流；系数有理时可取有理见证。

抽象图环流要求 partial t=0，只能支持 SCC 内边；这里仅要求

\[
partial t\in\ker L.
\tag{7}
\]

所以映射核允许非零抽象净流量，使不同 SCC 的映射边仍能形成精确的正环流。
对完整 H_*:=lin(K) 再取商，剩余锥才必为 pointed；仅对 SCC 像空间取商不保证此事。
式 (1)--(3) 给 (7) 的全部通用核，不需猜测额外 payoff identities。

这是一种完整锥的精确规范化，**不是**一般 half 的构造：仍须联合选取非负跨商边流、H_* 方向和逐类型非负余项以支付 2c-o。

## 3. 可行正客户向量给 lineality 的可核验上界

若 w 满足全部真实 SPE 行 Gamma_e w>=0，则任意 z in lin(K) 的两向非负表示相加可知，所有被使用的行都满足 Gamma_e w=0。
所以

\[
\operatorname{lin}(K)\subseteq
\operatorname{span}\{\Gamma_e:\Gamma_e w=0\}.
\tag{8}
\]

这给一个无需数值 cone membership 的精确上界。若另给足够多线性独立的行及其真实非负反向证书，便能认证全部 lineality 秩。

## 4. 全部类型严格正、目录主题不同的真实 SPE：SCC 像秩 1，完整像锥 lineality 秩 2

m=4，目录 A,B,C。类型顺序 `(A,B,AB,C,AC,BC,ABC)`，质量

\[
w=(3,4,3,4,3,4,3).
\tag{9}
\]

这是 24 个不同单位客户；全部类型严格正，三个主题两两不同，模型没有 signed 客户或加权提供者。
完整策略如下。根选 B；第一主题为 A,B,C 时第二主题分别为 B,A,A。
第三位表行是第一主题、列是第二主题：

| 第一/第二 | A | B | C |
|---|---|---|---|
| A | B | C | B |
| B | C | C | A |
| C | B | A | B |

末位表行是第一主题、列是第二和第三主题的有序对子：

| 第一 / 后两位 | AA | AB | AC | BA | BB | BC | CA | CB | CC |
|---|---|---|---|---|---|---|---|---|---|
| A | C | C | B | C | C | B | B | C | B |
| B | C | C | C | C | C | A | C | A | A |
| C | B | C | B | B | A | A | B | A | B |

从定义核验全部 40 个有序决策历史、120 个行动比较，最小 slack=0，全部非负。实际路径 BACC，收益

\[
(91/12,25/4,61/12,61/12),\qquad W=OPT_4=24.
\tag{10}
\]

这只是表示障碍例，福利已最优，**不是 half 反例**。
真实收益图只有一个非平凡 SCC，由

\[
((1,1,2),C),\quad ((1,2,1),B)
\]

组成，其像方向可取

\[
s=\Gamma_{BA,B}=(0,-1/2,-1/3,1/2,1/3,0,0).
\]

其反向为真实行 Gamma_{ABC,C}=-s；所以 SCC 像空间秩恰为 1。
另取两条真实行

\[
r=\Gamma_{AA,C}=(0,1,1/3,-1,-1/3,0,0),
\]

\[
t=\Gamma_{AAA,B}=(0,-1,-1/4,1,1/4,0,0).
\]

它们满足逐类型有理恒等式

\[
\boxed{r+(2/5)s+(4/5)t=0.}
\tag{11}
\]

因而 -r=(2/5)s+(4/5)t 是全部系数非负、全部行真实的反向支付。
r 与 s 线性独立；r 的两个端点 ((2,1,1),C) 与 ((2,1,1),B) 位于不同 SCC。
由此完整映射行锥 lineality 至少有秩 2。
在 (9) 处全部零 slack 行的精确秩恰为 2；式 (8) 给反向上界，因此完整秩**恰为 2**。

直观代数是，r,s,t 仅在 B-C 和 AB-AC 两个反对称方向有分量，但分母 3、2、4 给出三个不同斜率；正组合 (11) 在类型映射后闭合，抽象顶点净流量仍不为零。

## 5. 保存与下一步

- `extra_lineality_exact.json`：完整 policy（按深度、每层有序历史字典序）与行反向证书。
- `audit_full_tree.py`：独立定义级 Fraction 核验，不导入规范 solver 或 LP。
- `full_tree_audit.json`：120 行、SCC、全部 lineality 秩上/下界、11 组 rank 边界的精确结果。
- `explore.py`：探索用浮点 LP；仅生成候选，不承重上述证明。

运行 `python3 .../audit_full_tree.py`。人数1、主题1、重复计数、m>p 均有边界回归；零客户令全部不等式为0，空主题是某标签所有所属正类型质量为0，以上表示仍有效。

下一步仍是一般 half：映射环流应与非负福利余项一起选择，不能先把 SCC-DAG 视作 pointed 后强行取拓扑势。可探索 full-map polar 的暴露面与根覆盖的统一预算；本页尚无该预算。
