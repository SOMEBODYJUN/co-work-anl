# 共享选址集合：研究对象与可检验条件

本分支研究两个设施共同拥有同一有限选址集合时，如何选择顾客续局，使设施的单边改善至多为黄金比。本文从博弈对象重新建立记号；定理、证明和算法分别见 [theorems.md](theorems.md)、[proof.md](proof.md)、[algorithm.md](algorithm.md)。这里的定义本身不依赖黄金比存在性猜想。

## 1. 输入、时序与量词

顾客集合 $I$ 有限，每名顾客 $i$ 的原子权重为 $w_i>0$。物理位置集合 $S\ne\varnothing$ 有限，每个位置给定覆盖集合 $C_s\subseteq I$，其覆盖重量为 $R_s=\sum_{i\in C_s}w_i$。两个设施同时选址，行动集合均为 $S$。布局是有标签的有序对 $(s,t)$，允许 $s=t$；同址的两个设施仍是不同玩家。

布局确定后，未被覆盖的顾客不参与；仅被一个设施覆盖的顾客必须使用它；共同覆盖的顾客必须选其中一个，没有退出选项。顾客的成本是所选设施上**实现的总重量**的期望，包括自己的重量。设施收益是所服务顾客重量的期望。顾客可独立混合，不能将不同顾客捆绑为相关行动或可分流质量。

一个完整续局规则 $\sigma$ 为每个有标签布局选定一个精确顾客 Nash 均衡。研究结论的量词是：

\[
\forall\text{合法输入}\quad\exists(s,t),\ \exists\sigma\quad
\text{顾客逐个子博弈精确最优，设施改善比受限}.
\]

它不要求任意续局选择都稳定。正实数权重用于存在性；算法的输入必须是显式覆盖列表和二进制编码的正有理数权重。

## 2. 一个布局上的精确均衡方程

令 $A=w(C_s\setminus C_t)$、$B=w(C_t\setminus C_s)$，共同顾客为 $1,\ldots,k$，总重 $W=\sum_iw_i$。顾客 $i$ 选择设施 1 的概率为 $p_i$。定义

\[
x=A+\sum_iw_ip_i,\quad y=B+\sum_iw_i(1-p_i),\quad
V=A+B+W,\quad \Delta=x-y.
\]

顾客选择 1 与选择 2 的条件成本分别为

\[
A+w_i+\sum_{j\ne i}w_jp_j,\qquad
B+w_i+\sum_{j\ne i}w_j(1-p_j).
\]

两者相减是 $\Delta+w_i(1-2p_i)$，故精确 NE **等价于**

\[
p_i=1\Rightarrow\Delta\le w_i,\quad
p_i=0\Rightarrow\Delta\ge-w_i,\quad
0<p_i<1\Rightarrow\Delta=w_i(2p_i-1). \tag{NE}
\]

独立性使条件期望由其他人的边际概率决定；没有用“以期望负载代替随机成本”的近似。端点概率只需单边不等式。

另一套便于证明的坐标是 $c_i=w_i(2p_i-1)$。于是 $\Delta=A-B+\sum_i c_i$，纯行动对应 $c_i=\pm w_i$，真混合对应 $c_i=\Delta$。若指定 $m\ge2$ 名混合顾客，其余两侧纯质量为 $P_A,P_B$，则

\[
(m-1)\Delta=-(A-B)-P_A+P_B.
\]

只有一个混合顾客时分母消失，可能留下一个闭区间；不能把所有支持类型都当作唯一点。

## 3. 设施稳定性与菜单充分条件

给定路径上布局 $(s,t)$ 和收益 $(x,y)$，α-SPE 要求 α≥1，且

\[
L_1(\sigma(r,t))\le\alpha x\ (r\ne s),\qquad
L_2(\sigma(s,r))\le\alpha y\ (r\ne t).
\]

若 $x=0$，第一组要求所有实际偏离收益为零；不能用浮点除零或忽略该组。两组偏离布局不相交，因为共同的有序对只能是被排除的 $(s,t)$。

设每个无序物理对预先构造非空有限菜单 $F(s,t)\subseteq\mathrm{NE}(s,t)$，反向标签使用同一菜单的反射 $p\mapsto1-p$。令

\[
u(s,t)=\min_{e\in F(s,t)}L_s(e),\qquad d(t)=\max_{r\in S}u(r,t).
\]

取 $q=(\sqrt5-1)/2$。若菜单成员满足

\[
x\ge qd(t),\qquad y\ge qd(s), \tag{Q}
\]

则在每个实际偏离布局选择最小化偏离者收益的菜单成员，并在其余布局指定任一精确纯 NE，即得 φ-SPE，φ=1/q。这是直接证明的**充分条件**。

若 $m(s,t)$ 是所有实际顾客 NE 中的最低收益，则 $m(s,t)\le u(s,t)$。菜单内最小值没有被证明等于真实最小值；使用菜单不求解一般局部最低收益问题。即使只分析一个响应环，$d(t)$ 的最大化也始终覆盖整个 $S$。

## 来源与本次重写范围

定义与公式核对：[MODEL.md M1–M4](../../../history/curation-2026-10-01/MODEL.md)、[主稿 §§1–2](../../../history/source/manuscripts/shared_phi/main.tex)；实现核对：[shared_phi.py 的 `parsed`、`exact_ne`、`verify`](../../../facility_spe/shared_phi.py)。这些路径是来源定位，不替代上面的定义或推导。
