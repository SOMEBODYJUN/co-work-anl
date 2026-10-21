# 重复首主题、末位例外及五人两主题终局的共同目录闭包界

状态：2026-10-21，Boss10 内部候选；一般 Q-CAG-HALF 仍 OPEN。本文给结构充分条件，不给一般定理或反例。`saturation` 已独立重建主恒等式及系数；`global_proof` 的完整独立攻击另行进行。没有外部审查或新颖性认证。

## 精确 Claim

采用 CAG-MODEL：有限单位客户、有限非空共同目录、每位单位提供者选择一次、任意完整有序历史依赖纯 SPE，允许空主题、同覆盖标签、重复选择及任意平局。

**Claim A（任意人数的重复首主题终局）。** 对任意整数 m≥2，若一份上述完整 SPE 的实际有序路径为 `A^(m−1)B`，其中 A、B 是合法主题且允许相等，则

\[
\operatorname{OPT}_m\le\beta_m W<2W\quad(W>0),
\qquad
\beta_m=\max\left\{2-\frac1m,
\frac{4m^3-3m^2+2m-1}{2m^3-m^2+3m-2}\right\}<2.
\tag{A}
\]

若 W=0，结论为 OPT=0，不形成比值。m=1 时直接由唯一玩家最优性有 OPT=W。

**Claim B（两覆盖主题的末位频次筛选）。** 实际终局只使用覆盖集合 A、B，末位为 B。令 A 出现 k≥1 次、B 出现 l≥1 次，k+l=m；A、B 可交叠且覆盖不同。若

\[
l(2k+1)\ge k^2-1,
\tag{B}
\]

则 OPT_m≤2W。特别地，恰五人的任意完整 SPE 若实际终局只使用至多两个不同的客户覆盖集合，则满足 half：l≥2 时适用 (B)，l=1 时路径必为 A^4B，适用 (A)。目录可以有任意多个不同包含极大主题，不要求整个目录只有两个主题。

m=5、Claim A 的 β_5=217/119；m=2、3 的 β 分别为3/2、5/3。这里只证明给定上界，不声称这些结构常数锐。

## 1. 两个真实末层之间的精确闭包恒等式

固定 Claim A，记三块互不交客户为

\[
a=|A\setminus B|,\qquad b=|B\setminus A|,\qquad c=|A\cap B|,
\qquad W=a+b+c.
\]

在前缀 P=A^(m−2) 后，倒数第二位实际选择 A，末位实际选择 B。其实际收益为

\[
u=\frac a{m-1}+\frac cm,\qquad v=b+\frac cm.
\]

固定**任意一个**合法主题 T。令 R 是给定原完整策略在有序历史 `(P,T)` 的真实末位回复。R 是同一共同目录内的合法主题，故可以在实际末位节点 `(P,A)` 比较它。定义

\[
E_R=|R\setminus A|+\frac{|R\cap A|}{m},
\]

即实际末位节点改选 R 的收益。写

\[
s=|T\setminus(A\cup B)|,\quad
 t_A=|T\cap(A\setminus B)|,\quad
 t_B=|T\cap(B\setminus A)|,\quad
 t_C=|T\cap A\cap B|,
\quad D=m(m-1).
\]

令 U_T、U_R 是偏离分支 `(P,T,R)` 中最后两人的各自收益，令 U_B 是末位在 `(P,T)` 改选 B 的收益。三个真实 SPE 比较分别是

\[
u-U_T\ge0,\qquad U_R-U_B\ge0,\qquad v-E_R\ge0.
\tag{1}
\]

逐客户有以下**精确恒等式**：

\[
\boxed{
\frac{a(m+1)}D+\frac cm
-\left(s+\frac{t_B}2+\frac{t_A}{m-1}+\frac{t_C}m\right)
=(u-U_T)+(U_R-U_B)+(v-E_R)+\frac{|A\setminus R|}D.}
\tag{2}
\]

因此

\[
s+\frac{t_B}2+\frac{t_A}{m-1}+\frac{t_C}m
\le\frac{a(m+1)}{m(m-1)}+\frac cm.
\tag{3}
\]

核对 (2) 可使用

\[
U_R=E_R-\frac{|R\cap T\setminus A|}2
 +\frac{|(R\cap A)\setminus T|}D,
\]

\[
U_B=v-\frac{t_B}2+\frac{c-t_C}D,
\quad
U_T=|T\setminus A|-\frac{|R\cap T\setminus A|}2
 +\frac{|T\cap A|}{m-1}-\frac{|R\cap T\cap A|}D.
\]

相加即得 (2)。每个式子在 m=2 的空前缀仍有效，所有出现的分母均正。

这里的共同目录闭包是关键：离轨最优回复 R 同时也是实际末位节点可以比较的主题。我们没有冻结后继为 B，没有限制相同计数历史使用同一回复，也没有把数值松弛点冒充真实 SPE。

## 2. 从单主题闭包界支付 m 个最优主题

取恰 m 个合法最优主题 T_1,…,T_m，允许重复。它们的并集在上述四块中覆盖量分别记作 X_out、X_A、X_B、X_C。将 (3) 求和。因每个最优并集客户至少出现在一个 T_j 且各权均非负，

\[
X_{out}+\frac{X_B}2+\frac{X_A}{m-1}+\frac{X_C}m
\le\frac{a(m+1)}{m-1}+c.
\]

再用 X_A≤a、X_B≤b、X_C≤c，得到

\[
\operatorname{OPT}_m\le
P:=\frac{2m-1}{m-1}a+\frac b2+
\left(2-\frac1m\right)c.
\tag{4}
\]

另一条界只用实际末位 B 在 A^(m−1) 后的最优性：任意 T 满足

\[
|T\setminus A|+\frac{|T\cap A|}m\le v.
\]

将 m 个最优主题求和，使用最优并集在 A 内的覆盖至多 |A|，给出

\[
\operatorname{OPT}_m\le m v+\frac{m-1}m|A|
=L:=\frac{m-1}ma+mb+
\left(2-\frac1m\right)c.
\tag{5}
\]

所以 OPT≤min(P,L)。令

\[
D_m=2m^3-m^2+3m-2,
\quad \lambda_m=\frac{2(m-1)(m^2-m-1)}{D_m}.
\]

对每个 m≥2，有 0<λ_m<1，因为分子正且

\[
D_m-2(m-1)(m^2-m-1)=3m^2+m-4>0.
\]

直接代数给

\[
\lambda_m P+(1-\lambda_m)L
=\gamma_m(a+b)+\left(2-\frac1m\right)c,
\quad
\gamma_m=\frac{4m^3-3m^2+2m-1}{D_m}.
\tag{6}
\]

其中

\[
2-\gamma_m=\frac{m^2+4m-3}{D_m}>0,
\]

从而 (A) 成立。此凸合仅用于统一常数；min(P,L) 本身是更细的可检查证书。

## 3. 两主题末位频次筛选

现在允许任意两主题排列，末位 B，频次 A:k、B:l。仍令 a,b,c 为三块大小。

取**最后一次**实际 A 的节点。此前恰有 k−1 个 A，以及某个 l_0 个 B。其余人数含当前共 l+1−l_0。该玩家若真实偏离 B，则每个 B\A 客户最终负载至多 l+1；每个公共客户最终负载至多 m。因此真实偏离收益至少 b/(l+1)+c/m。实际 A 玩家收益是 a/k+c/m，故

\[
(l+1)a\ge kb.
\tag{7}
\]

最后一位的真实最优性及相同逐客户税比较给

\[
\operatorname{OPT}_m\le
\frac{k}{k+1}a+\frac{m+l-1}{l}b+
\left(2-\frac1m\right)c.
\tag{8}
\]

右端减2W为

\[
-\frac{k+2}{k+1}a+\frac{k-1}{l}b-\frac cm.
\]

利用 (7)，其上界不超过零的充分条件恰为

\[
\frac{k(k+2)}{(k+1)(l+1)}\ge\frac{k-1}{l}
\iff l(2k+1)\ge k^2-1.
\]

m=5 时逐项为 (k,l)=(3,2),(2,3),(1,4)，均成立；(4,1) 由 Claim A 覆盖。若只有一个覆盖集合，则可以取 A=B 用 Claim A（或直接用既有 all-big 末位证明）。如果一些不同标签覆盖相同客户，将实际标签按客户覆盖合并作此计数即可；收益与上述真实偏离下界只使用集合，不要求策略本身合并或匿名。

## 4. 来源关系、适用范围与仍缺什么

(2) 是既有 `research/current/customer_attraction/two_remaining_tax.md` §2 的精确三行恒等式，在比较第二主题 S=B 时**保留**其中非负的重叠项 g(T,B)，再按 A、B 三块展开。这里的用途是把单个两人子局比较转成 m 个最优主题的共同支付，并与另一条末位界交叉。不是首次建立末两人三节点比较。

`terminal_geometry/terminal_load_rank.md` 给末位负载尾和、最优覆盖秩及末位信用；`last_theme_containment.md` 给末位主题重复频次充分条件。它们与这里使用相同实际终局几何，但没有这里的 (P,T)→R→(P,A) 真实回复闭包链。本文不声称全球新颖性，且此处仍只是个人工作区结构资产。

五人一般目标若有反例，本文把其实际终局进一步限制为至少三个不同客户覆盖集合。这个终局支持数条件与既有“目录至少七个极大覆盖”的条件不同：目录仍可任意复杂。任意 m 的一般两主题终局并未由本文完全覆盖；例如大 m、小 l 且不属于 A^(m−1)B 的排列仍可能落在 (B) 之外。一般无界终局支持数的承重问题仍然开放。

`audit_two_theme_terminal.py` / `two_theme_terminal_audit.json` 精确核对：16种 A/B/T/R 客户会员模式的 (2)，多个 m 的凸合有理恒等式、符号多项式系数、m=1/2及零/重复覆盖边界，和指定合法输入的完整有序历史 SPE。有限计算只审核公式、代码与证书；全量结构结论依赖正文解析证明。
