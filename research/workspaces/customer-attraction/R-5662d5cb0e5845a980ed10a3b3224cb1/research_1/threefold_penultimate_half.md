# 六人、倒二主题逐客户三重早期覆盖的半覆盖证书

暂定 Claim：`CA-M6-POINTWISE-THREEFOLD-PENULTIMATE-HALF-v1`。
状态：自足真实行推导和完整局部系数域 Fraction 核验；未作独立外审。它是结构性特例，不是 Q-CAG-HALF-6 的无条件解答。

## 精确命题

采用 CAG-MODEL，恰六名玩家。固定任意一份定义于全部有序历史的纯 SPE。实际终局记为 `(E_1,E_2,E_3,E_4,A,B)`。假设

\[
\tag{P3}\forall x\in A,\qquad\sum_{i=1}^4\mathbf1_{E_i}(x)\ge3.
\]

则 `2W≥OPT_6`。目录任意有限非空，空主题、重复主题、零客户和任意历史依赖平局均保留。

(P3) 是逐客户量词；并不要求存在某一个 `E_i` 包含整个 A。它与旧“至少两名早期实际主题完整包含 A”的条件不可比。例：四个 A 客户各被恰一个不同早期主题遗漏时满足 (P3)，但没有任何早期主题包含 A；反之 A 仅被固定两个早期主题包含时可以只有二重覆盖。

## 从同一份完整策略获得的非负行

任取六个合法比较主题 `T_1,...,T_6`，O 为其并集大小。固定真实前缀 `(E_1,...,E_4)`；强制倒二玩家选 `T_i` 后，R_i 是沿原策略的真实末位回复。写

\[
U_p(X,Y)=\sum_{x\in X}\frac1{p_x+1+\mathbf1_Y(x)},
\quad p_x=\sum_{j=1}^4\mathbf1_{E_j}(x).
\]

以下三条都是非负真实 IC 的和：

\[
\begin{aligned}
S&=\sum_i[u_5-U_p(T_i,R_i)],\\
Z&=\sum_i[u_6-U_p(R_i,A)],\\
V&=\sum_{i\ne j}[U_p(R_i,T_i)-U_p(R_j,T_i)].
\end{aligned}
\]

S 使用原倒二源的偏离比较。Z 使用实际末位在实际前缀后的 R_i 查询。V 使用各强制分支的真实末位回复对其他合法 R_j 的查询；被强制选 T_i 的倒二者从未被误当该分支最优者。令

\[
G=S+Z/12+V/6\ge0.
\]

对实际早期位置 i=1,...,4，令 `q_i(x)=Σ_{j<i}1_{E_j}(x)`。该玩家在真实实际前缀强制改选 A 后，每个 A 客户终局负载至多 `q_i(x)+7-i`，因为还剩 7-i 名玩家，包括该偏离者。原完整 SPE 因此给出有序前缀安全行

\[
H_i=u_i-\sum_{x\in A}\frac1{q_i(x)+7-i}\ge0.
\]

这里全部后继沿原策略行走，未冻结任何后继。最后，实际末位对 A 的精确查询给

\[
L=u_6-U_p(A,A)\ge0.
\]

## 逐客户证书

客户位记为 `e=(e_1,...,e_4)`、`a=1_A`、`b=1_B`。令 `p=Σe_i`、`c=p+a+b`、`w=1_{c>0}`、`d=Σ_i1_{T_i}`、`ell=Σ_i1_{R_i}`、`o=1_{d>0}`。零分子份额定义为零。直接展开 S/Z/V 并消去同索引重叠 `Σ_i1_{T_i∩R_i}` 得

\[
G_x=\frac{6a}{c}+\frac{b}{2c}-\frac d{p+1}
-\frac{\ell}{12(p+a+1)}+\frac{d\ell}{6(p+1)(p+2)}.
\]

另有

\[
H_{i,x}=\frac{e_i}{c}-\frac a{\sum_{j<i}e_j+7-i},\qquad
L_x=\frac b c-\frac a{p+a+1}.
\]

取

\[
(\lambda_1,\lambda_2,\lambda_3,\lambda_4)
=(1/3,1/2,1/2,2/3),\qquad\mu=3/2.
\]

在满足 `a=0` 或 `p≥3` 的全部位型，以及独立扩大的 `d,ell∈{0,...,6}` 上，

\[
Q_x=2w-o-G_x-\sum_i\lambda_iH_{i,x}-\mu L_x\ge0.
\]

因此

\[
2W-O=G+\sum_i\lambda_iH_i+\mu L+\sum_xQ_x\ge0.
\]

取最大比较六元组即得结论，不除以 W。

## 完整域及可复现证据

`replay_threefold_penultimate.py` 直接用 Fraction 重构上述系数，不导入发现 LP。域为：a=0 时四早期位任意；a=1 时四早期位之和至少三；b 任意；d,ell 各独立取 0,...,6。总数 `(16+5)*2*49=2058`；最小 Q=0，负状态为零。每名真实客户必落在该扩大域，故任意非负整数客户重数求和合法。隐藏比较/回复会员的相互相关性仅被放松，没有假设最小赋值可来自某份新 SPE。

运行：

```sh
python research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_1/replay_threefold_penultimate.py
```

输出为 `threefold_penultimate_exact.json`，还保存全部 64 个实际会员模式的最坏余项 rho。

## 无条件带缺陷版本及准确边界

上述真实行在每个六人实例仍然合法。令

\[
\rho(e,a,b)=\min_{0\le d,\ell\le6}Q(e,a,b,d,\ell).
\]

无条件有 `2W−OPT_6≥Σ_x rho(e(x),a(x),b(x))`。因此该实际会员几何的总 rho 非负亦足以推出 half。这里 rho 的定义已经把比较主题和回复会员完全取最坏；不需要知道哪组比较主题最优。证据 JSON 保存了完整 rho 表。

对 a=1，按 p=0,1,2,3,4 再对其余实际位取最小，360rho 依次至少为 `−1079,−299,−93,2,42`；a=0 时 rho≥0。若 n_k 是 A 中被恰 k 名早期玩家覆盖的客户数，则条件

`2n_3+42n_4≥1079n_0+299n_1+93n_2`

也足以给 half。这只是同一证书的定量容错版本，不是主目标已证。

指定行锥的探索边界：将 (P3) 放宽为逐客户 p≥2，在已测试的固定 G、全部有序前缀安全实际主题查询及比较主题求和、实际末位精确查询等非负行系统中，浮点 LP 不可行；另有包含 S/Z/V、强末两人比较及回复对全部实际主题查询的扩大系统也不可行。这里只报告所列模板的计算发现，没有提供该不可行性的精确 Farkas 证书，故更不声称 p≥2 命题或原 Q-CAG-HALF-6 为假。探索脚本 `simple_search.py`、`terminal_rich.py` 与本定理的 Fraction 核验分开。
