# 后部源 λ 锚族：连续付款与 ordered 最弱重数的独立解析审查

**结论：通过。** 对源 $i=3,4,5$、$q_0\in\{1/6,1/5\}$、$0\le\lambda\le25$，指定完整零查询余项域上的解析付款、正查询锚、ordered 的 $d=1$ 唯一最弱结论和 C-only 自由等式符号均成立。第五源低 λ 段确实不能使用 $W>Z$，但其准确重数包络是严格凹二次式，足以在整个连续区间证明同一结论。本审查未发现需要修改的数学公式。

本次只读原模型、三份获准冻结证明，以及本包的 `inputs.json`、`parameter_domains.json`、`analytic_state_checks.json`。只写本文件；0 优化器。没有读取全局 LP 输入、候选点、最优面或其他新包。独立核对没有导入生成器或项目 Python 模块。

## 1. 模型与真实预算

采用[共同目录完整历史模型](../../../../archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md)的全部量词：六人、有限单位客户、有限非空共同标签目录、任意给定完整有序历史纯 SPE。空覆盖、同覆盖异标签、重复标签、任意弱平局及离轨节点全部保留。相同负载的不同有序历史不合并续局。

固定原实际第 $i$ 源历史，强制合法标签 $T$，沿给定策略的真实后继完成。记

\[
J=\{i+1,\ldots,5\},\qquad m=5-i,\qquad D=p+7-i,
\]

\[
a=\lambda+\sum_{j\in J}\tau_j,
\qquad
\beta_j=\frac{q_0}{2}+\tau_j+
\sum_{\ell>j}\frac{q_0\tau_\ell}{(7-\ell)(8-\ell)},
\qquad B=\sum_j\beta_j,\quad S=1+B.
\]

其中 $\tau_j\ge0$、$\lambda\ge0$，故全部真实付款权非负。内部源收益始终是该偏离分支自身的收益。内部 SAFE 是在其真实节点改选一个合法查询，再沿该查询历史的真实续局；使用后面至多 $6-j$ 名覆盖者得到收益下界。

逐客户取原前缀负载 $p$、目标会员 $t$、中间会员 $r_j$、末会员 $z$，令 $L=p+t+\sum_jr_j+z$。源 IC、各大小帽、末 BR 均值及内部 SAFE 均值相加，成本必须为

\[
\begin{aligned}
\Psi(p,t,q;r,z)={}&
\frac{at-z-\sum_j\tau_jr_j}{L}
+\sum_j\beta_jr_j+z\\
&+\frac{q}{p+t+\sum_jr_j+1}
+\sum_j\frac{\tau_jq}{p+t+\sum_{h<j}r_h+7-j}.
\end{aligned}
\tag{A1}
\]

$L=0$ 时首项按照零实际份额取零；此时相应首分子也为零。查询分母始终为正。总真实付款 $P$ 满足

\[
P=a u_i+S K-\sum_x\Psi_x\ge0.
\tag{A2}
\]

这与[六均值冻结证明](../all_source_minimal_cap_safe/proof.md)、[ordered 冻结证明](../ordered_minimal_cap/proof.md)及[第二源窗口证明](../source2_lambda_strip/proof.md)的真实预算口径一致。

## 2. 零目标会员：整个非负 τ 象限上的准确锚与最小帽

在 $t=0$ 时，零尾成本为

\[
0\quad(q=0),\qquad
Z(p)=q_0\left[\frac1{p+1}+\sum_j\frac{\tau_j}{p+7-j}\right]
\quad(q=q_0).
\]

令 $k=\sum_jr_j$、$k_{<j}=\sum_{h<j}r_h$，此时 $L=p+k+z$。把 (A1) 减去 $Z(p)$ 后得到准确恒等式

\[
\begin{aligned}
\Psi(p,0,q_0;r,z)-Z(p)={}&
q_0k\left[\frac12-\frac1{(p+1)(p+k+1)}\right]\\
&+\sum_jq_0\tau_jk_{<j}
\left[\frac1{(7-j)(8-j)}
-\frac1{(p+7-j)(p+k_{<j}+7-j)}\right]\\
&+\left(z+\sum_j\tau_jr_j\right)\left(1-\frac1L\right).
\end{aligned}
\tag{A3}
\]

最后一项在 $L=0$ 时按零理解。第一项在 $k=0$ 时为零；$k\ge1$ 时其分母乘积至少为 $k+1\ge2$。第二项在 $k_{<j}=0$ 时为零；否则分母乘积至少为 $(7-j)(8-j)$。最后一项有非零会员时 $L\ge1$。所以各项非负，零尾准确达到下界。

当 $q=0$ 时，直接保留帽的非负常数、非负交叉项及最后一项即可。因此在整个非负 τ 象限，不依赖 λ 域的任何顶点，

\[
\boxed{m_0(p,0)=0,\qquad m_0(p,q_0)=Z(p).}
\tag{A4}
\]

帽的必要性也来自一个真实局部状态。把帽暂作自由变量，取 $p=t=z=0$、$q=q_0$，只让中间 $j$ 覆盖。其对零尾锚的准确余项为

\[
\beta_j-\frac{q_0}{2}-\tau_j
-\sum_{\ell>j}\frac{q_0\tau_\ell}{(7-\ell)(8-\ell)}.
\tag{A5}
\]

所以指定帽在这个真实预算形式和零尾锚内逐坐标最小。这个必要性不涉及任意钱包方法的最优性，也不把局部必要状态声称为可同时实现的完整 SPE。

## 3. 正目标会员：两个末位锚与真正的查询分母

全部中间覆盖时，实际源收益分母为 $D-1+z$。去掉公共帽 $B$ 后，两个末位状态成本分别为

\[
g_0(\lambda,D)=\frac\lambda{D-1},\qquad
g_1(\lambda,D)=1+\frac{\lambda-1}{D}.
\]

两者差是

\[
g_0-g_1=\frac{\lambda-(D-1)^2}{D(D-1)}.
\tag{A6}
\]

故 $\lambda<(D-1)^2$ 使用末位 0，$\lambda>(D-1)^2$ 使用末位 1，切点上两者都达到。定义

\[
w_\lambda(D)=\min(g_0,g_1),\qquad W(p)=B+w_\lambda(D).
\]

对任意缺失集 $M\subseteq J$，(A1) 的 $t=1,q=0$ 成本减去此锚，准确为

\[
\rho_{p,M,z}=
\frac{\lambda+\sum_{j\in M}\tau_j-z}{D-1-|M|+z}
+z-\sum_{j\in M}\beta_j-w_\lambda(D).
\tag{A7}
\]

分母至少为 $p+1>0$。完整域保留全部这些余项非负，因此零查询最小值准确是 $W(p)$。这一步不要求真实续局采用锚态。

两种全中间锚的末查询分母均为

\[
p+1+m+1=D,
\]

每个内部查询分母也均为

\[
p+1+(j-i-1)+7-j=D.
\]

末位 $z$ 不进入这些查询分母。任意其他尾态的查询分母都不超过 $D$，权重非负，所以其查询斜率至少为 $(1+\sum_j\tau_j)/D$。最低零查询成本与最低查询斜率由同一个全中间锚同时达到。由此对**所有 $q\ge0$**，

\[
\boxed{m_1(p,q)=W(p)+\frac{1+\sum_j\tau_j}{D}q.}
\tag{A8}
\]

源实际收益分母 $D-1+z$ 与查询分母 $D$ 必须分别保留。切点两种锚均保留；若其他尾态也达到，非严格余项定义同样保留它们。

## 4. Ordered 第三、第四源：连续域上的严格重数比较

同六标签菜单保留索引。外层强制索引 $k$ 后，内五查询只删除该索引；相同标签的其他索引仍保留。因此真实条件均值为

\[
q=\frac{d-t}{5}.
\tag{A9}
\]

令 $q_0=1/5$。第三、第四源有至少一个中间源。在实际 $D=6$、单缺中间 $j$、末位 0 状态，因 $\lambda\le25$，$D=6$ 的锚可取末位 0，余项为

\[
\frac\lambda{20}+\frac{\tau_j}{4}-\beta_j
=\frac\lambda{20}-\frac1{10}-\frac34\tau_j
-\sum_{\ell>j}\frac{\tau_\ell}{5(7-\ell)(8-\ell)}\ge0.
\tag{A10}
\]

因此整个完整域自动满足 $\lambda\ge2$，不是根据顶点观察外推。结合 $D\le6$，

\[
\frac\lambda{D-1}\ge\frac25,
\qquad 1+\frac{\lambda-1}{D}\ge\frac76,
\qquad w_\lambda(D)\ge\frac25.
\]

同时

\[
B\ge\frac m{10}+\sum_j\tau_j,
\qquad Z(p)\le\frac15+\frac1{10}\sum_j\tau_j.
\]

所以审查目标中的界准确成立：

\[
\boxed{W(p)-Z(p)\ge\frac15+\frac m{10}
+\frac9{10}\sum_j\tau_j>0.}
\tag{A11}
\]

固定尾的查询成本非减，故准确最小值 $m_0,m_1$ 也非减。只使用实际存在的条件，定义

\[
f(p,d)=\frac{(6-d)m_0(p,d/5)+d\,m_1(p,(d-1)/5)}6.
\tag{A12}
\]

$d=0$ 仅计算第一项，$d=6$ 仅计算第二项，不计算不存在的 $-1/5$ 或 $6/5$ 条件。由 (A4)、(A8)，

\[
f(p,1)=\frac{5Z(p)+W(p)}6=G(p).
\]

对 $d=2,\ldots,6$，单调性与 (A11) 给出

\[
f(p,d)-f(p,1)\ge\frac{d-1}{6}(W-Z)>0.
\tag{A13}
\]

因此第三、第四源的 $d=1$ 在整个连续域内都是唯一最弱正重数。该结论没有假设 $q>1/5$ 时零尾仍是 $m_0$ 的达到态。

## 5. Ordered 第五源：低 λ 必须单独使用严格凹二次身份

第五源没有中间权或帽，$D=p+2$、$B=0$、$S=1$。由两个真实末位状态直接得到，任意 $q\ge0$ 时

\[
\boxed{m_0(p,q)=\frac q{p+1},\qquad
m_1(p,q)=w_\lambda(p+2)+\frac q{p+2}.}
\tag{A14}
\]

这里 $p=0,\ldots,4$，且 $w_\lambda(p+2)\ge0$。为简记置 $w=w_\lambda(p+2)$。准确外平均是

\[
\boxed{f(p,d)=\frac{dw}{6}
+\frac{d(6-d)}{30(p+1)}
+\frac{d(d-1)}{30(p+2)}.}
\tag{A15}
\]

关于 $d$ 的二次项系数为

\[
-\frac1{30(p+1)(p+2)}<0.
\]

端点准确差为

\[
\boxed{f(p,6)-f(p,1)
=\frac{5w}{6}+\frac{5p+4}{6(p+1)(p+2)}>0.}
\tag{A16}
\]

更直接地，对每个 $d=2,\ldots,6$，有覆盖整个连续 λ 域的恒等式

\[
\boxed{
f(p,d)-f(p,1)
=\frac{d-1}{5}\,[f(p,6)-f(p,1)]
+\frac{(d-1)(6-d)}{30(p+1)(p+2)}>0.}
\tag{A17}
\]

因此第五源同样以 $d=1$ 为唯一最弱正重数，包括 $\lambda=0$、全部锚切点及全部区间边界。

不能把 (A11) 套用于此源。事实上 $0\le\lambda<1/5$ 时，对所有允许 $p$，

\[
W(p)-Z(p)=\frac{\lambda-1/5}{p+1}<0.
\tag{A18}
\]

(A17) 完全避开这个失效条件。查询重数的严格比较也不改变模型中策略最优回复可以弱平局的事实。

## 6. C-only 自由等式：符号确认

对六均值通用行，记左减右为

\[
R_{\mathrm{general},T}
=a u_i+S K-\sum_x\left[t_x(B+w_\lambda(D_x))
+M_x+\sum_j\tau_jN_{j,x}\right].
\]

当 $T=C$、$C$ 为真实最大大小标签时，定义 $E_C=|C|-K=0$。C-only 左减右为

\[
R_C=a u_i+K-\sum_x\left[c_xw_\lambda(D_x)
+M_x+\sum_j\tau_jN_{j,x}\right].
\]

逐项相减给出

\[
\boxed{R_C=R_{\mathrm{general},C}+(S-1)E_C,}
\qquad
\boxed{R_{\mathrm{general},C}=R_C-(S-1)E_C.}
\tag{A19}
\]

所以自由等式乘子是 $+(S-1)$，对应从通用付款得到 C-only 付款；客户 $c$ 列增加 $S-1$，独立 $K$ 列减少 $S-1$，最终恰为 1。第五源 $S-1=0$，C-only 与通用 $T=C$ 行完全相同，其重复来源仍须保留。

## 7. 独立精确核验记录与结论边界

本审查使用仅含 Python 标准库 `Fraction` 的独立临时程序，从个人真实份额、各帽及各真实查询分母分别重建成本，不导入生成器。以零点和每个参数基向量恢复仿射系数，独立检查了 `analytic_state_checks.json` 的全部记录：

| 核验对象 | 精确记录数 | 结果 |
|---|---:|---|
| $t=0,q\in\{0,q_0\}$ 整个非负 τ 象限的余项 | 200 | 系数全相等且非负；λ 系数为零 |
| $t=1$ 任意尾的查询斜率差 | 100 | 系数全相等且非负；λ 系数为零 |
| 自由帽的单中间会员必要式 | 6 | 全部系数准确相等 |
| 第五源全部 $p=0,\ldots,4,d=2,\ldots,6$ 身份 | 25 | 全部准确相等；端点差严格正 |
| **合计** | **331** | **PASS** |

第五源低 λ 的 $W-Z<0$ 另从真实两状态公式直接核对。C-only 符号通过 (A19) 逐项恒等式确认。

本审查证明的是连续解析承重步骤。全 facet/顶点枚举、所有列身份及全部物理最小表的输出完整性由本包另一份完整独立检查器负责。本文件没有将有限端点检查冒充 (A11)、(A13) 或 (A17) 的连续证明，也没有声明局部隐藏态可同时实现为完整 SPE、任意钱包方法最优性、全局福利改进或六人 half 结论。
