# 第二源 λ∈[9,16] 段：两个完整23顶点域与230条完整行

Boss1；研究标识 `six-boss1-20261111`。**0 优化器、0 全局 LP 输入或候选点读取。** λ 段、两个单缺帽面及其几何猜想由 Main 提出；本包从原模型、实际预算和全部真实局部状态独立重建，得到两个完整域与全部原尺度行。这个新族独立冻结，**不加入当前3056计划**。

## 1. 模型、来源与结论范围

采用[共同目录完整历史模型](../../../../archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md)：有限单位客户、有限非空共同标签目录、恰六名单位权提供者，以及任意给定的完整有序历史纯 SPE。允许重复标签选择、空覆盖、同覆盖异标签、查询菜单中的重复索引标签、任意重叠，以及全部弱最优回复。相同负载的不同有序历史可以有不同续局；本证明始终沿给定策略在对应偏离历史后的真实续局，不把策略商成负载函数。

令 $A_1,\ldots,A_6$ 为原实际行动，$u_2$ 为原第二源实际收益。固定任意合法目标 $T$，在真实前缀 $(A_1)$ 后强制 $T$，沿原策略完成真实后继 $R_3,R_4,R_5,R_6$。令 $K=\max_{Q\in\mathcal S}|Q|$，选一个达到 $K$ 的合法标签 $C$。另令 $X$ 为任意合法标签；通用行保留八个目标 $A_1,\ldots,A_6,X,C$。

任一客户的原前缀负载是 $p=1_{A_1}\in\{0,1\}$，目标会员位是 $t=1_T$，真实后继会员位是 $r_3,r_4,r_5,z$。取六个任意合法标签组成带索引菜单，重数为 $d$，覆盖并会员为 $o=1_{d>0}$。覆盖并只用于逐客户投影，不被当成合法行动。

只读取了原定义、[冻结六均值最小帽证明](../source2_minimal_cap_safe/proof.md)、[冻结 ordered 最小帽证明](../ordered_minimal_cap/proof.md)及这两包的 `coordinate_contract.json`。五个准确来源均在 [source_pins.json](source_pins.json) 固定 SHA256，并于生成器和独立检查器首末核验。没有读取其他包的数值工件、全局输入、候选点或最优面。

这里的“完整参数域”指：在指定研究窗口 $9\le\lambda\le16$ 内，指定真实预算、指定坐标最小帽及指定锚的所有非负余项条件的完整域。它不表示任意钱包的最优域，也不声称局部必要状态都能同时嵌入某个完整 SPE。

## 2. 两套权重与从真实预算重建的成本

取 $q_0\in\{1/6,1/5\}$、内部 SAFE 权 $\tau_3,\tau_4,\tau_5\ge0$，定义

\[
a=\lambda+\tau_3+\tau_4+\tau_5,
\qquad
\beta_j=\frac{q_0}{2}+\tau_j+
\sum_{\ell>j}\frac{q_0\tau_\ell}{(7-\ell)(8-\ell)},
\qquad B=\sum_{j=3}^5\beta_j,\quad S=1+B.
\tag{1}
\]

三帽的交叉项分别为

\[
C_3=\frac{q_0}{12}\tau_4+\frac{q_0}{6}\tau_5,
\qquad C_4=\frac{q_0}{6}\tau_5,\qquad C_5=0.
\]

源 IC 付款权为 $a$；三中间大小帽权为 $\beta_j$；末大小帽与末 BR 平均权均为1；内部 SAFE 平均权为 $\tau_j$。内部 SAFE 保留真实节点的实际收益 $v_j$。在该节点真改一个合法查询后沿它自己的真实续局，后面至多还有 $6-j$ 名覆盖者，所以该客户的查询收益至少为

\[
\frac{1_{Q}}{p+t+\sum_{h<j}r_h+7-j}.
\]

这是对真实偏离收益的下界，不冻结偏离后的尾。末 BR 查询收益则准确为 $1_Q/(p+t+r_3+r_4+r_5+1)$。设所用查询平均的会员均值为 $q$，将这些非负预算相加，得到

\[
P=a u_2+SK-\sum_x\Psi_x\ge0,
\]

其中逐客户成本必须是

\[
\boxed{
\begin{aligned}
\Psi(p,t,q;r,z)={}&
\frac{at-z-\sum_j\tau_jr_j}{p+t+\sum_jr_j+z}
+\sum_j\beta_jr_j+z\\
&+\frac{q}{p+t+\sum_jr_j+1}
+\sum_j\frac{\tau_jq}{p+t+\sum_{h<j}r_h+7-j}.
\end{aligned}}
\tag{2}
\]

总负载为零时首分子也为零，首项按零份额取零；其余分母始终为正。本包生成器和字面检查器都从源份额、各中间实际份额、末实际份额、各大小帽及各查询独立重建(2)。

## 3. $t=0$：坐标最小帽与任意非负 τ 的准确锚

零尾在 $q=0$ 成本为0，在 $q=q_0$ 成本为

\[
Z(p)=q_0\left[\frac1{p+1}
+\sum_{j=3}^5\frac{\tau_j}{p+7-j}\right].
\tag{3}
\]

这两个值在整个非负 $\tau$ 象限都是准确最小值。令 $k=r_3+r_4+r_5$、$R_{<j}=\sum_{h<j}r_h$、$L=p+k+z$。帽的自身 $\tau$ 项与实际中间份额相减，留下

\[
\sum_j\tau_jr_j(1-1/L)\ge0.
\]

有会员时 $L\ge1$；无会员的零负载边界直接按零份额处理。交叉帽逐项支付内部查询相对零尾的损失，因为 $R_{<j}\ge1$ 时

\[
\frac{q_0\tau_jR_{<j}}{(7-j)(8-j)}
\ge
\frac{q_0\tau_jR_{<j}}
{(p+7-j)(p+R_{<j}+7-j)}.
\]

$R_{<j}=0$ 时两边都为零。常数帽支付末查询损失，因为 $k\ge1$ 时

\[
\frac{q_0k}{2}\ge\frac{q_0k}{k+1}
\ge\frac{q_0k}{(p+1)(p+k+1)}.
\]

剩下的末位项为 $z(1-1/L)\ge0$。故

\[
\boxed{m_0(p,0)=0,\qquad m_0(p,q_0)=Z(p).}
\tag{4}
\]

反向必要性由 $p=t=z=0,q=q_0$、唯一中间会员 $r_j=1$ 给出。暂把帽视为自由变量，该状态减零尾锚准确等于

\[
\beta_j-\frac{q_0}{2}-\tau_j
-\sum_{\ell>j}\frac{q_0\tau_\ell}{(7-\ell)(8-\ell)}.
\tag{5}
\]

所以(1)确是保持这个指定锚及预算形式时的坐标最小帽。两套帽的全部6个自由帽必要式，以及128个 $t=0,q\in\{0,q_0\}$ 仿射余项，均逐系数核验；这些结论不依赖参数域的顶点检查。

## 4. $t=1,q=0$：完整域及全部多缺态

记 $D=p+5\in\{5,6\}$。本段锚统一为三个中间会员全1、末位0，其成本是

\[
\boxed{W(p)=B+\frac{\lambda}{D-1}=B+\frac{\lambda}{p+4}.}
\tag{6}
\]

设缺失中间会员集为 $M\subseteq\{3,4,5\}$、$k=|M|$、$U=\sum_{j\in M}\tau_j$。直接由(2)减(6)，得全部32个真实零查询余项

\[
\boxed{\rho_{D,M,z}
=\frac{\lambda+U-z}{D-1-k+z}+z
-\sum_{j\in M}\beta_j-\frac{\lambda}{D-1}.}
\tag{7}
\]

令

\[
A_j=\frac{\lambda}{20}+\frac{\tau_j}{4}-\beta_j,
\qquad B_j=\frac34+\frac{\tau_j}{4}-\beta_j.
\tag{8}
\]

这里 $B_j$ 是面松弛，区别于总帽 $B=\sum\beta_j$。完整参数域为

\[
\boxed{\tau_j\ge0,\quad9\le\lambda\le16,\quad A_j\ge0,\quad B_j\ge0\quad(j=3,4,5).}
\tag{9}
\]

等价地，两组帽面正是

\[
\boxed{\frac34\tau_j+C_j\le\frac\lambda{20}-\frac{q_0}{2},
\qquad
\frac34\tau_j+C_j\le\frac34-\frac{q_0}{2}.}
\tag{10}
\]

### 4.1 必要性与研究窗口的区别

| 条件 | 准确真实状态余项 |
|---|---|
| $A_j\ge0$ | $D=6,M=\{j\},z=0$ 时 $\rho=A_j$ |
| $B_j\ge0$ | $D=5,M=\{j\},z=1$ 时 $\rho=B_j$ |
| $\lambda\le16$ | $D=5,M=\varnothing,z=1$ 时 $\rho=(16-\lambda)/20$ |
| $\tau_j\ge0$ | 内部真实 SAFE 权的非负选择条件 |
| $\lambda\ge9$ | 本次指定研究窗口下界；不由本段隐藏态推出 |

独立检查器从这些真实状态的仿射系数恢复法向和右端。没有把窗口下界或局部必要性见证误称为 SPE 定理的必要条件。

### 4.2 所有多缺态的准确付款身份

令 $A_M=\sum_{j\in M}A_j$、$B_M=\sum_{j\in M}B_j$。所有32个余项按缺失数归入以下身份；包内保留每个具体 $M$，不合并或删除状态。

| $k,z$ | $D=5$ | $D=6$ |
|---|---|---|
| (0,0) | (0) | (0) |
| (0,1) | $(16-\lambda)/20$ | $(25-\lambda)/30$ |
| (1,0) | $A_j+\lambda/30+\tau_j/12$ | $A_j$ |
| (1,1) | $B_j$ | $B_j+(1-\tau_j)/20$ |
| (2,0) | $A_M+3\lambda/20+U/4$ | $A_M+\lambda/30+U/12$ |
| (2,1) | $A_M+2/3-\lambda/60+U/12$ | 见下一式 |
| (3,0) | $A_M+3\lambda/5+3U/4$ | $A_M+3\lambda/20+U/4$ |
| (3,1) | $A_M+\lambda/10+1/2+U/4$ | $A_M+2/3-\lambda/60+U/12$ |

唯一需要切换非负分解的是 $D=6,k=2,z=1$：

\[
\rho=
\begin{cases}
A_M+3/4-\lambda/20,&9\le\lambda\le15,\\
B_M+\lambda/20-3/4,&15\le\lambda\le16.
\end{cases}
\tag{11}
\]

两式本身都是恒等式，只是分别在对应半段逐项非负。由 $B_j\ge0$ 和交叉项非负，

\[
0\le\tau_j\le1-\frac{2q_0}{3}<1.
\]

又 $2/3-\lambda/60\ge2/5$，所以表中全部余项非负。**不需要额外双缺或三缺面。** 生成器逐仿射系数核验表中每一身份；独立字面程序另用真实成本检查全部 $46\times32=1472$ 个端点余项。

域有界且为4维：$\tau_j\le8/9$（六均值）或 (13/15)（ordered），$\lambda\in[9,16]$；$(\tau_3,\tau_4,\tau_5,\lambda)=(1/100,1/100,1/100,10)$ 是严格内点。源 IC 权 $a\ge9$，三帽均为正，所有真实付款合法。

## 5. $t=1$ 的全部正查询：锚的两个不同分母

锚尾 (1110) 的源实际收益分母是 $D-1=p+4$，但其末查询分母是

\[
p+1+3+1=D,
\]

每个内部查询分母也是

\[
p+1+(j-3)+7-j=D.
\]

任意其他尾的这些查询分母都不大于 $D$，且查询权非负，因此其查询斜率至少为 $(1+\sum\tau_j)/D$。尾 (1110) 同时达到最小零查询成本和最小斜率，故对任意 $q\ge0$，

\[
\boxed{m_1(p,q)=W(p)+\frac{1+\sum_j\tau_j}{p+5}\,q.}
\tag{12}
\]

这一步不能把查询分母替换成新的源收益分母 $p+4$。两域的64个查询斜率差均已从真实查询重建，并逐常数及 $\tau$ 系数核验非负。

## 6. 两个23顶点域的完整几何

令

\[
\alpha(\lambda)=\min(\lambda/20,3/4)-q_0/2.
\]

固定 $\lambda$ 的全部8个截面角可由 $\varepsilon\in\{0,1\}^3$ 递推：

\[
\begin{aligned}
\tau_5&=\varepsilon_5\frac{4\alpha}{3},\\
\tau_4&=\varepsilon_4\frac43\left(\alpha-\frac{q_0}{6}\tau_5\right),\\
\tau_3&=\varepsilon_3\frac43\left(\alpha-\frac{q_0}{12}\tau_4-\frac{q_0}{6}\tau_5\right).
\end{aligned}
\tag{13}
\]

每个坐标上界严格正，所以截面角每坐标恰选下界或上界。四维域的全部顶点是：$\lambda=9$ 的8角、$\lambda=16$ 的8角，以及 $\lambda=15$ 的7个非零角。零角在 $\lambda=15$ 位于一条直边内部，不是顶点。

| 查询基准 | 全部面 | 全部四面交点组合 | $\lambda=9$ | $\lambda=15$ | $\lambda=16$ | 全部顶点 |
|---|---:|---:|---:|---:|---:|---:|
| $q_0=1/6$ | 11 | 330 | 8 | 7 | 8 | 23 |
| $q_0=1/5$ | 11 | 330 | 8 | 7 | 8 | 23 |

生成器枚举所有四面交点；独立检查器从包围盒 $[0,1]^3\times[9,16]$ 出发，仅沿共享活跃法向秩为3的**真边**逐面裁切，并另用(13)独立构造角集。三种方法给出完全相同的两个23顶点集合。

每个 $\tau_j=0$ 面含11顶点；两个 $\lambda$ 端面和六个帽面各含8顶点。22个面的顶点仿射秩全部为3，所以均不可约。检查器还核验 [necessary_facet_witnesses.json](necessary_facet_witnesses.json) 中的具体有理点：每点只违反指定一面而满足其他10面；若该面来自真实状态，其对应 $\rho<0$。全部具体坐标见 [endpoint_table.md](endpoint_table.md)，几何摘要见 [geometry.md](geometry.md)。

## 7. 纯六均值：184条通用行与23条 C-only 行

取 $q_0=1/6$。每个真实末 BR 与内部 SAFE 都使用六个合法查询的等权平均，实际会员均值为 $d/6$。用 $d\ge o$ 弱化到 $o/6$ 的准确差为

\[
\Delta_x=\frac{d_x-o_x}{6}\left[
\frac1{p+t+r_3+r_4+r_5+1}
+\sum_j\frac{\tau_j}{p+t+\sum_{h<j}r_h+7-j}\right]\ge0.
\tag{14}
\]

由(4)、(12)，弱化成本的准确最小值统一为

\[
\boxed{
m=t\left(B+\frac\lambda{p+4}\right)
+\frac{o}{6(p+1+4t)}
+\sum_j\frac{\tau_jo}{6[p+(j-2)t+7-j]}.
}
\tag{15}
\]

因此对任意合法 $T$，有通用真实行

\[
\boxed{
a u_2+SK\ge
B|T|+\lambda\sum_x\frac{t_x}{p_x+4}
+M(T,O)+\sum_j\tau_jN_j(T,O),
}
\tag{16}
\]

其中 $M=\sum_xo_x/[6(p_x+1+4t_x)]$、$N_j=\sum_xo_x/\{6[p_x+(j-2)t_x+7-j]\}$。这些查询分母是从新锚重新推导得到，恰好仍与此前六均值最小帽的 $M,N$ 形式一致。

令 $\eta_x=\Psi(p,t,o/6;r,z)-m_x\ge0$，则(16)左减右准确等于

\[
R_{\rm general}=P+\sum_x\Delta_x+\sum_x\eta_x.
\tag{17}
\]

对 $T=C$，使用真实大小等式 $E_C=|C|-K=0$，得到

\[
\boxed{a u_2+K\ge\lambda\sum_x\frac{c_x}{p_x+4}
+M(C,O)+\sum_j\tau_jN_j(C,O).}
\tag{18}
\]

完整自由等式付款关系为

\[
\boxed{R_{\rm C\text{-}only}=P+\sum_x\Delta_x+\sum_x\eta_x+B E_C,
\qquad R_{\rm general}(T=C)=R_{\rm C\text{-}only}-(S-1)E_C.}
\tag{19}
\]

这里自由等式乘子为 $B=S-1$；本段它为正，但其合法性来自等式而非符号要求。独立 $K$ 列在通用行是 $S$，在 C-only 行准确为1。不能把 C-only 行的 $C$ 直接改名为任意 $T$。23顶点逐一保留八目标通用行，共184条；另外保留23条 C-only，彼此不作行剪枝。

## 8. Ordered 五条件查询：23条行与 $d=1$ 唯一最弱

取 $q_0=1/5$。固定同一六标签菜单 $Q_1,\ldots,Q_6$。外层在原实际第二源历史分别强制 $Q_k$，沿同一给定策略的真实后继，六索引等权平均。每个分支的末 BR 和内部 SAFE 只用同一菜单的五个索引 $\ell\ne k$，故客户实际条件均值准确为

\[
q=\frac{d-t}{5}.
\tag{20}
\]

排除的是索引；如果两个索引标签相同，另一个索引仍保留。同标签的同一实际历史遵守同一策略续局。逐分支应用普遍下界再求平均，不要求这些续局可独立选取。

设 $m_t(p,q)$ 是16个真实尾态上的准确最小值。每个固定尾的查询斜率为正，所以 $m_t$ 非减；不预设 $t=0,q>1/5$ 的最小尾保持零尾。重数 $d$ 的准确外平均包络为

\[
f(p,d)=\frac{(6-d)m_0(p,d/5)+d\,m_1(p,(d-1)/5)}6.
\tag{21}
\]

只计算实际存在的项：$d=0$ 只有 $t=0,q=0$；$d=6$ 只有 $t=1,q=1$，不构造不存在的 (-1/5) 或 (6/5) 条件。

当 $d=1$，

\[
\boxed{G(p)=f(p,1)=\frac{5Z(p)+W(p)}6
=\frac16\left[B+\frac\lambda{p+4}
+\frac1{p+1}+\sum_j\frac{\tau_j}{p+7-j}\right].}
\tag{22}
\]

整个连续参数域上的准确差为

\[
\begin{aligned}
W(0)-Z(0)&=\frac1{10}+\frac\lambda4
+\frac{19}{20}(\tau_3+\tau_4)+\frac{29}{30}\tau_5,\\
W(1)-Z(1)&=\frac15+\frac\lambda5
+\frac{24}{25}\tau_3+\frac{29}{30}\tau_4+\tau_5.
\end{aligned}
\]

所以

\[
\boxed{W-Z\ge2+\frac{19}{20}\sum_j\tau_j>0.}
\tag{23}
\]

准确最小值2在 $p=1,\lambda=9,\tau=0$ 取得。由单调性，对每个 $d\ge2$，包含 $d=6$，

\[
f(p,d)-f(p,1)\ge\frac{d-1}{6}(W-Z)>0.
\tag{24}
\]

因此 $d=1$ 在整个连续域是唯一最弱正重数，$d=0$ 给0。最终行是

\[
\boxed{a u_2+SK\ge\sum_xo_xG(p_x).}
\tag{25}
\]

其付款身份为

\[
R_{\rm ordered}
=\frac16\sum_kP_k
+\frac16\sum_{k,x}\left[\Psi_x^{,k}-m_{t_x^k}\!\left(p_x,\frac{d_x-t_x^k}{5}\right)\right]
+\sum_x[f(p_x,d_x)-o_xG(p_x)].
\tag{26}
\]

每项非负；没有 $C$ 等式，没有覆盖分割或菜单独立假设。

## 9. 完整513列、无损顶点化与独立核验

列0至511保留全部九位 $(a_1,\ldots,a_6,x,o,c)$ 的词典序客户型，列512为独立 $K$。实际源收益份额为 $a_2/\sum_{h=1}^6a_h$，零负载取零。通用行原尺度客户列为 $a a_2/\sum a_h-m(p,t,o)$；C-only 加 $Bc$；ordered 为 $a a_2/\sum a_h-oG(p)$。没有支持缩减、目标删除、零型删除、重复列删除或行剪枝。

| 行族 | 参数域 | 每顶点行数 | 完整 raw 行数 | 独立 $K$ 系数 |
|---|---|---:|---:|---|
| 六均值八合法纯目标 | $q_0=1/6$ 的23顶点 | 8 | 184 | $S$ |
| 六均值 C-only | 同上 | 1 | 23 | 1 |
| 同六菜单 ordered | $q_0=1/5$ 的23顶点 | 1 | 23 | $S$ |
| **合计** | 两个完整域 | — | **230** | 各自保留 |

所有行在对应参数上仿射；有界域由完整顶点凸生成，因此每个连续参数行是同目标顶点行的凸组合，独立 $K$ 列一并保留。这给出指定连续族的无损有限表示。输出保留原尺度，也保存统一正除数25后的系数；25仅为继承的数值除数，源 IC 权始终是变化的 $a=\lambda+\sum\tau$。

两程序的承重核验全部 PASS：

| 检查 | 精确数量 |
|---|---:|
| 原始 $t=1,q=0$ 仿射状态 | 64 |
| 全顶点的零查询余项 | 1472 |
| 任意非负 $\tau$ 的 $t=0$ 仿射余项 | 128 |
| $t=1$ 查询斜率差 | 64 |
| 自由帽最小性必要式 | 6 |
| 全部物理条件最小值表 | 736 |
| 完整真实隐藏尾成本 | 11776 |
| 全部弱平局达到态出现 | 1231；单表最多7个 |
| Ordered 重数外平均 | 322 |
| 全64菜单的 ordered 上下文 | 2944 |
| 实际内五索引均值 | 17664 |
| 逐实际菜单重付全部达到态成本 | 26574 |
| 五索引与分母的独立恒等式 | 2304 |
| 六均值全部菜单弱化上下文 | 4096 |
| 完整原尺度与除25后列重建 | 117990 |
| C-only 自由等式逐列身份 | 11799 |

独立 `check_literal.py` 不导入生成器或任何项目 Python 模块，只读本包 JSON 与五个固定来源。它从真实个人份额及逐索引合法查询重算全部最小值、全部弱平局和所有列，再用不同算法验证几何。全部 Fraction 计算，未调用优化器。

## 10. 工件、复现与冻结边界

```bash
python research/workspaces/six-boss1-20261111/source2_lambda_strip/derive_family.py
python research/workspaces/six-boss1-20261111/source2_lambda_strip/check_literal.py
```

核心工件为 [exact_family.json](exact_family.json)、[parameter_domains.json](parameter_domains.json)、[coordinate_contract.json](coordinate_contract.json)、[row_catalog.json](row_catalog.json)、[literal_checker_output.json](literal_checker_output.json) 与 [full_column_checks.tsv](full_column_checks.tsv)。全部条件表、真实隐藏态、原始半空间、必要面见证和菜单身份都完整保留。最终身份见 `freeze_manifest.json` 与 `SHA256SUMS`。

零客户、全目录空覆盖、$K=0$、$O=0$ 以及全部弱平局由相同齐次预算涵盖。本包只证明并冻结上述指定局部参数族，不产生新全局最优值、不声明完整 SPE 实现、不声明任意钱包最优性，也不据此声称六人 half 问题已解决。
