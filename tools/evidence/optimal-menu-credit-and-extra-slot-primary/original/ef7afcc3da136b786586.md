# 真实最优孩子机会损失的精确递推

2026-10-24。目标仍为一般 `Q-CAG-HALF`，状态 OPEN。本文独立从模型重构
Boss21 阶段 1 的最优补全交换，再把新提出的孩子机会损失项写成带全部松弛的
精确关系。下述代数对任意有限共同非空目录、任意人数和每份完整历史纯 SPE
成立，允许重复、空主题、零客户和任意历史平局。没有给出一般 half 闭合。

## 固定真实节点和三个松弛

在任意真实有序历史 h，旧主题并集为 P，旧负载为 b，还剩 r≥1 位玩家。
原 SPE 当前动作 S，最终利润 u。记

\[
 F=F_r(P),\qquad F'=F_{r-1}(P\cup S),\qquad\delta=F-F'.
\]

任取最优补全 `(T_1,…,T_r)`，令 `O=P∪⋃T_j`，其比较私有块

\[
 D_j=T_j\setminus(P\cup\bigcup_{\ell\ne j}T_\ell),
 \qquad e=|S\setminus O|.
\]

强制当前玩家选 T_j，之后沿同一原 SPE。令 Y_j 是该枝真实 r−1 个后继主题
的并集；完整终局覆盖为 `P∪T_j∪Y_j`，当前偏离收益为 d_j。定义

\[
 \rho_j=F-|P\cup T_j\cup Y_j|,\qquad
 \Gamma_j=u-d_j\ge0,
\]

\[
 t_j=|T_j\setminus(P\cup S\cup Y_j)|,
 \quad f_j=|S\setminus(P\cup T_j\cup Y_j)|.
\]

最优补全中含 T_j，所以恰有

\[
 F_{r-1}(P\cup T_j)=F_r(P)=F.
\]

因此 ρ_j 是这个**真实强制孩子**从其自身最优补全到其真实最终覆盖的机会
损失；它不只是一个任意比较差额。所有背景在此等式中保留。

三个非负松弛为

\[
 \varepsilon_j=F'-[F+e-|D_j\setminus S|]\ge0,
\]

\[
 \xi_j=F'-|P\cup S\cup Y_j|\ge0,
\]

\[
 \eta_j=r d_j-|D_j\setminus S|-(r-1)t_j\ge0.
\]

ε 的非负性由用 S 替换 T_j 的最优补全交换给出；ξ 的非负性由真实尾主题
Y_j 也是 S 后的 r−1 个合法补全给出。η 的非负性逐客户证明如下。

`D_j\S` 无旧背景负载，其当前份额至少 `1/r`。其中属于 t_j 的客户当前
独占，除了这 `1/r` 的基线外，还提供 `(r−1)/r`。t_j 中其余客户同样当前
独占；给它们计 `(r−1)/r` 不超过其实际份额 1。其余 T_j 客户的利润非负。
乘 r 即得 η≥0。没有冻结后继，也没有替换旧玩家的跨枝利润。

## 精确关系

同一尾主题 Y_j 中把当前 T_j 换成 S，覆盖差恰为 `t_j−f_j`，所以

\[
 \delta=\rho_j+t_j-f_j-\xi_j.
\]

另一方面，交换松弛定义给

\[
 |D_j\setminus S|=\delta+e+\varepsilon_j.
\]

代入 η，并用 `u=d_j+Γ_j`，得到

\[
\boxed{
\delta-u=\frac{r-1}{r}\rho_j
-\frac{\varepsilon_j+e+\eta_j}{r}
-\frac{r-1}{r}(f_j+\xi_j)-\Gamma_j.}
\tag{R}
\]

这严格推出待核候选

\[
\boxed{\delta-u\le\frac{r-1}{r}\rho_j
 -\frac{\varepsilon_j}{r}-\Gamma_j.}
\]

r=1 时没有尾主题，η 的证明、ξ 的定义和所有系数仍有效，ρ_j=0。
零客户时全部量为零。重复比较主题导致某些 D_j 为空，也无需另设例外。

## 一般递归应保留的状态

记任意节点 h 的真实最终覆盖 W_h、当前及全部后继的最终利润和 V_h，
以及该节点机会损失

\[
 R_h=F_r(P)-W_h.
\]

若 hS 是原规定孩子，则严格有 `R_h=δ+R_{hS}`。若 hT_j 是强制最优孩子，
则上文严格有 `R_{hT_j}=ρ_j`。所以式 (R) 给一个带真孩子的全树递推：

\[
R_h-u=R_{hS}+\frac{r-1}{r}R_{hT_j}
-\frac{\varepsilon_j+e+\eta_j}{r}
-\frac{r-1}{r}(f_j+\xi_j)-\Gamma_j.
\tag{Tree}
\]

但这里 `u` 是 h 的规定真实终局利润。强制孩子的尾利润来自另一真实叶；
不能将它替换为规定孩子的尾利润。取每个实际节点的一条式 (R) 再求和，
还未付款的项是不同强制孩子的机会损失，未被 `(r−1)/r` 系数自动消除。

一个自然的全范围加强是背景子树不变量

\[
 F_r(P)-W_h\le V_h.
\tag{BG?}
\]

等价地，若 `g_h=W_h−|P|` 为实际新增覆盖，则
`F_r(P)−|P|≤g_h+V_h`。空根时 BG? 恰给 half。r=1 可直接由真实当前最优性
证明。这个精确候选已见于旧工作区 `R-2fc8878b4bdd4328bbc1bcf1df8ca831`
的 `RESEARCH_STATE.md` 和 `round3_root/reviewed_obligations.md`，不认领新候选。
它不是一般背景利润比例界，也不是已被否定的总税。

直接假设两个孩子都满足 BG?，只能推出
`R_{hS}≤V_{hS}`、`ρ_j≤V_{hT_j}`。第二项仍位于强制枝；Tree 中没有合法的
`V_{hT_j}→V_{hS}` 转换。因此这一步不是归纳闭合，不能删掉其跨枝债务。

当前继续方向：利用全部最优主题 T_j 的共同合法目录和真实 Γ_j，寻找
多孩子轮换付款，而不是把单个 ρ_j 当作实际尾预算。本文没有采用有限扫描。
