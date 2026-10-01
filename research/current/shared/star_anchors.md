# 星心、首边与双锚：共享目录全局闭环的重建

本文重写共享目录黄金比主稿 §§9–10、12–13 所需的 G2/G3 分支。它以[模型](model.md)、[固定菜单](algorithm.md)和[证明工作稿](proof.md)的局部引理为基础，但把本分支实际用到的量词和不等式写在这里。主稿 §11/附录 A–B 的强弦 C、§§5–8 的重顾客结构分别是本分支的**前提**，不能由下面的闭环运算反过来证明；G1/L1/L2 的独立 Markdown 转写另行完成。

## 1. 反证框架与可调用的见证

设 $S$ 是两个设施共同的完整有限目录，$T\subseteq S$ 是固定菜单最小收益回应 $b$ 的一个有限环。对于任一 $s\in S$，$R_s$ 是覆盖重量，$u(t,s)$ 是预先固定的菜单 $F(t,s)$ 中设施 $t$ 收益的最小值，$d(s)=\max_{t\in S}u(t,s)$，$b(s)$ 取此最大值。以下所有 $d$ **都在完整 $S$ 上最大化**，虽然本节的地点和闭环限于 $T$。记

\[
q=\phi^{-1},\quad a=1-q=q^2,\quad c=\phi/2,\qquad
\max_{s\in T}d(s)=1.
\]

反设不存在满足配额 $L_s\ge qd(t),L_t\ge qd(s)$ 的环上位置对及其菜单见证。于是对于 $s\in T$ 及回应边 $s\to t=b(s)$：

\[
d(s)>cR_s,\quad R_s<2q,\quad
R:=\max_{s\in T}R_s\in[1,2q),\qquad
P\ge d(s)>cR_s,\quad Q<qd(t)\le q. \tag{1}
\]

最后两个条件逐一应用于**每个固定菜单成员**：$P$、$Q$ 分别是响应、原设施负载。若 $R_v\ge q$，纯 P 种子及其受保护修复，必要时加上严格支配证明，给出 $d(v)\le R_v$。反过来，若 $d(v)>R_v$，其回应边的所有顾客 NE 唯一，原设施收益 $R_v$，并有

\[
d(b(v))>\phi R_v. \tag{2}
\]

这里 (2) 是返回规则；其“全部 NE 唯一”已经由共同顾客的严格支配单独证明，不能仅从一个 P 成员推断。沿环可见的顾客权重都严格小于 $q$；“大顾客”指权重 $>q/2$。从重顾客结构结论使用：每处至多两个大顾客；大顾客对族若非空则是星形，且同一对不能占据一条 $b$ 边的两端。以下在调用该结构时逐项点明。

### 两种常用的局部操作

若 $s,t$ 都包含权重 $H$ 的顾客 $h$、$R_s\le R_t$，把 $h$ 放在 $s$，其余共同顾客放在 $t$。设其余共同总重为 $\sigma$，初始负载

\[
U_s=R_s-\sigma\ge H,\qquad V_t=R_t-H. \tag{3}
\]

$h$ 稳定：转往 $t$ 的成本至少 $V_t+H=R_t\ge R_s\ge U_s$。如果 $V_t\le U_s$，其他共同顾客在低侧 $t$，该 **P singleton** 种子已是 NE；若 $V_t>U_s$，低侧只有共同顾客 $h$，且 $V_t-U_s\le R-2H<H$，故满足 P 修复守卫，终态两负载均不小于 $U_s$，响应方终态负载不超过原 $V_t$。特别地，在 $H>aR$、$K=R-H<q$ 时，

\[
u(t,s)\le R_t-H\le K. \tag{4}
\]

若 $s\to t$ 两端含 $h$ 且 $d(s)>q$，(4) 先给 $R_t<R_s$。任何 P 纯成员均须把 $h$ 送往 $t$：否则 $P\le R_t-H\le K<q<d(s)$。若还送去别的共同顾客，以这两位逐人的纯 NE 条件得 $2P\le R_s+Q\le2R_s-H$，从而 $P\le R_s-H/2<cR_s<d(s)$，也不可能。所以只有 $h$ 向前。写其余共同重 $\sigma$、$\Delta=R_s-R_t>0$。由原纯成员 $P=R_t-\sigma\ge d(s)>q$ 可知 $\sigma<R_t-q\le R-q<H$。若 $\sigma\ge\Delta$，把 $h$ 放在 $s$、其他共同顾客放在 $t$，就是一个**已均衡的 P singleton 种子**，响应收益 $R_t-H\le K<q$：$h$ 留在 $s$ 的条件 $R_s-\sigma\le R_t$ 正是 $\sigma\ge\Delta$；其余人留在较低负载 $t$，因为 $R_t-H<R_s-\sigma$（由 $\sigma<H$）。所以 $\sigma<\Delta$。此时 $h$ 对任何其余人的选择都严格偏好 $t$，因为它在 $s$ 的最小成本 $R_s-\sigma>R_t$；给定此决定，所有其余共同顾客严格偏好 $s$，因为其在 $s$ 的最大负载 $R_s-H\le K<q$，而在 $t$ 的最小负载 $R_t-\sigma\ge d(s)>q$。**这一次**才可将所有（包括混合）真实 NE 与菜单最小值识别：

\[
d(s)=R_t-\sigma,\quad Q=R_s-H,\quad 0\le\sigma<R_s-R_t. \tag{5}
\]

该论证用的是 P 的非空性、坏环约束和严格支配，绝没有在别处默认 $d$ 是所有顾客 NE 的最小值。

### 双锚覆盖引理

若 $X\to Y$ 已有 (5)，记

\[
x=R_X>y=R_Y,\quad \delta=d(X)=y-\sigma,\quad
\varepsilon=d(Y),\quad B=\phi(y-H),
\]

且

\[
\delta>B,\quad\varepsilon>B,\quad\delta>\phi H,\quad\varepsilon\le y, \tag{6}
\]

则不存在包含 $h$ 的 $t\in T$ 满足 $B<R_t\le y$、$d(t)\le B$。证明对每个锚 $i=X,Y$，将 $h$ 放在 $t$、其他共同顾客放在 $i$，记它们的重量为 $\sigma_{it}$。若某一个 $\sigma_{it}\le R_t-qd(i)$，则

\[
U_t=R_t-\sigma_{it}\ge qd(i),\quad V_i=R_i-H\ge y-H=qB\ge qd(t). \tag{7}
\]

因 $R_t\le y\le R_i$，$h$ 稳定。若 $V_i\le U_t$，这是 P singleton 的精确 NE；若 $V_i>U_t$，低侧 $t$ 只有 $h$，并有 $V_i-U_t\le R-2H<H$（利用 $H>aR\Rightarrow R<3H$），因此 P 修复适用。终态两侧均不低于 $U_t$；这里 $U_t\ge qd(i)>qB\ge qd(t)$，故仍满足双配额，矛盾。无见证因此迫使两锚同时满足

\[
\sigma_{Xt}>R_t-q\delta,\qquad\sigma_{Yt}>R_t-q\varepsilon. \tag{8}
\]

两集合在 $t\setminus\{h\}$ 内的交集属于 $X\cap Y$ 中非 $h$ 顾客，重量至多 $\sigma$；容斥给

\[
2R_t-q(\delta+\varepsilon)<\sigma_{Xt}+\sigma_{Yt}
\le R_t-H+\sigma,
\]

故 $R_t<L:=q(\delta+\varepsilon)-H+\sigma$。又 $y=\delta+\sigma$、$\varepsilon\le y$，

\[
B-L=\delta-q\varepsilon+q\sigma-qH
\ge a\delta-qH>0,
\]

因为 $\delta>\phi H=H/q$。这与 $R_t>B$ 矛盾。这个证明**不需要** $\varepsilon\le\delta$，后文将分别验证 (6)。

## 2. 中心引理：没有高覆盖的非 $h$ 点则环不可能存在

**假设。** 一个可见顾客 $h$ 的重量满足

\[
H>aR,\qquad H<q,\qquad K=R-H<q, \tag{9}
\]

且 $T$ 内一切不含 $h$ 的位置 $v$ 均有 $R_v\le\phi H$。这里 $H>aR$ 给 $R<3H$、$\phi H>q$；$H<q$ 给 $\phi H<1\le R$。断言这样的坏环不可能存在。

**先排除低 $d$ 的含 $h$ 位置。** 若含 $h$ 的 $u$ 有 $d(u)\le H$，由 $d(u)>cR_u$ 可得 $R_u<2qH<\phi H$。取任意 $R_t>\phi H$ 的位置，则按假设 $t$ 含 $h$ 且 $R_t>R_u$。若 $d(t)\le\phi H$，按 (3) 把 $h$ 放 $u$，其余共同顾客放 $t$，得到 $U_u\ge H\ge qd(t)$ 与 $V_t=R_t-H>qH\ge qd(u)$。若无修复已是 P 成员；若需修复，低侧只有 $h$，守卫是 $V_t-U_u\le R-2H<H$，两终态负载至少 $U_u\ge H\ge qd(t),qd(u)$。两种都给双配额。因此坏环上所有 $R_t>\phi H$ 必有 $d(t)>\phi H$。这类位置非空，因为 $R\ge1>\phi H$；它们在 $b$ 下封闭，因为 $R_{b(t)}\ge d(t)>\phi H$。封闭集合中都含 $h$，而 $d(t)>\phi H>q>K$ 使 (4) 排除任何不降覆盖重的回应边：每条边严格下降。有限封闭图不可能如此。于是

\[
h\in C_u\Longrightarrow d(u)>H. \tag{10}
\]

**离开 $h$ 的返回增益。** 若 $u\to v$ 中 $u$ 含 $h$、$v$ 不含，原设施每个菜单成员负载至少 $H$；由 (1) 得 $d(v)>\phi H\ge R_v$。返回规则 (2) 作用于 $v$，其下一位置 $w=b(v)$ 满足 $R_w\ge d(v)>\phi H$，故含 $h$，并且由于 $R_v\ge d(u)>H$，

\[
d(w)>\phi R_v\ge\phi d(u)>\phi H. \tag{11}
\]

**选最大中心。** 在环上含 $h$ 的位置中取使 $d$ 最大的 $X$，写 $\delta=d(X)$。最大覆盖位置含 $h$，故 $\delta>cR$。若环有离开 $h$ 的边，(11) 给 $\delta>\phi H$；若没有离开边，则整个环含 $h$，最大 $d$ 是 $1>\phi H$。总之 $\delta>\phi H>q$。$Y=b(X)$ 必含 $h$：若不含，(11) 会给某个含 $h$ 的 $d(w)>\phi\delta>\delta$。于是 (5) 适用，取 $x=R_X>y=R_Y$、$\sigma$、$\varepsilon=d(Y)$、$B=\phi(y-H)$。边条件 (1) 施于唯一 P/真实 NE，得到

\[
\varepsilon>\phi(x-H)>\phi(y-H)=B. \tag{12}
\]

又 $\varepsilon\le\delta$ 因 $X$ 在含 $h$ 点中最大；结合 (12)，$x<H+q\delta$。因 $y<x$，$B<\phi(q\delta)=\delta$。余下 $B>K$ 分两类：

* 若 $H\le R/2$，由 $y\ge\delta>cR$ 得 $B>\phi(cR-H)$，因此
  \[
  B-K>(\phi c-1)R-qH=q(R/2-H)\ge0.
  \]
* 若 $H\ge R/2$，由 $y\ge\delta>\phi H$ 得 $B>\phi(\phi H-H)=H\ge K$。

还需 (6) 中 $\varepsilon\le y$：$y\ge\delta>\phi H>q$，故覆盖界 $d(Y)\le R_Y=y$ 适用。双锚覆盖引理的四个条件现已全部核对。

**关闭环。** 从 $Y$ 反复走 $b$。只要含 $h$ 的当前点 $s$ 有 $d(s)>B>K$，下一点若也含 $h$，(4) 迫使 $R_{b(s)}<R_s$；若下一点首次成为含 $h$ 且 $d\le B$，它由前点 $R_t\ge d(s)>B$，同时由单调下降有 $R_t\le y$，双锚引理排除。因环有限，路径不能一直含 $h$、$d>B$ 且覆盖重严格下降，于是必须出现离开 $h$ 的边 $u\to v$，出发点仍有 $d(u)>B$。返回 (11) 给新的含 $h$ 点 $w$ 满足 $d(w)>\phi d(u)>\phi B$。另一方面由 $\delta=y-\sigma$ 直接计算

\[
\phi B-\delta=\phi(\delta-\phi H)+\phi^2\sigma>0,
\]

所以 $d(w)>\delta$，违背最大中心的定义。中心引理得证。

## 3. 非退化星形：先识别星心，再调用中心引理

假设重顾客对族有至少两个不同成员，G1 的结构结论给唯一共同星心 $h$，并排除三角对族。若某点不含 $h$、覆盖重 $\ge q$，大顾客对避让引理迫使它分别与两个不同星边相交，即含这两个叶子；这形成已排除的三角对。因此

\[
h\notin C_s\Longrightarrow R_s<q. \tag{13}
\]

**这里先调用与星形无关的最大覆盖首边计算。** 取 $A_0\in T$ 满足 $R_{A_0}=R\ge1$，$A_1=b(A_0)$。若 $R_{A_1}=R$，E 等覆盖半分成员有 $P=Q$，而 (1) 给 $P>cR\ge c>q>Q$，不可能；故 $R_1<R$。任取 P 纯成员：若无共同顾客前往 $A_1$，原设施 $Q=R\ge1>q$。若至少两名，逐个纯 NE 条件及送出总重 $R-Q$ 给 $2P\le R+Q<R+q$，与 $2P>\phi R$ 合起来得 $R<1$。所以恰有一人 $g$ 前进，记其权重 $G$，于是

\[
G=R-Q>R-q\ge aR>q/2,\quad G<q,\quad
K_g=R-G<q. \tag{14}
\]

$G<q$ 来自整个环的可见原子界。其余共同重 $\sigma_0$ 满足 $P=R_1-\sigma_0>cR>q$，故 $\sigma_0<R_1-q\le R-q<G$。若 $\sigma_0\ge R-R_1$，反向 singleton（$g$ 留在 $A_0$，其余共同者到 $A_1$）已是 P 中的 NE，响应收益 $R_1-G\le R-G=K_g<q$，违反 (1)。所以 $\sigma_0<R-R_1$；如 (5) 的严格支配论证，全部真实 NE 只有 $g$ 向前，且

\[
d(A_0)=R_1-\sigma_0>cR,\qquad
d(A_1)>\phi(R-G). \tag{15}
\]

特别地 $R_1\ge d(A_0)>cR>q$。由 (13) 两端含星心 $h$。此外

\[
\sigma_0=R_1-d(A_0)<R-cR=(a/2)R<aq=q^3<q/2.
\]

若 $g\ne h$，星心重量 $H>q/2$ 属于首边其他共同者总重 $\sigma_0$，矛盾。因此 $g=h$，(14) 变成 $H>aR,H<q,K<q$，且由 $H>aR$ 有 $\phi H>q$。利用 (13)，所有不含星心的位置 $R_s<q<\phi H$；第 2 节中心引理排除非退化星形。依赖顺序是**首边 (14)–(15) → 星心识别 → 中心引理**，不是引用后面的空对/单对锚点结论。

## 4. 空对族或唯一一对：建立 $h$-only 锚

由上一节排除非退化星形；本节独立假设重顾客对族为空，或只有一对 $\{h,j\}$。仍用第 3 节不依赖星形的首边 $A_0\to A_1$，并将它唯一送出的顾客称为 $h$；已有 (14)–(15)，故 (9) 成立。若有唯一一对，$A_0$ 必与该对相交：否则大对避让给 $R=R_{A_0}<qd(\text{对位置})\le q$，与 $R\ge1$ 矛盾。又 $h$ 在 $A_0$ 且本身是大顾客；若不属于唯一一对，它与 $A_0$ 中的对成员构成第二个大顾客对，矛盾。所以 $h$ 属于唯一一对。这里的“$h$-only”指某位置的大顾客集合恰为 $\{h\}$，**并不**限制小顾客人数。

若 $A_0$ 是 $h$-only，则选 $Z=A_0$；否则它含唯一对，而 $A_1$ 也含 $h$、且按 G1 不允许同一大对占据 $b$ 边两端，于是 $A_1$ 是 $h$-only，选 $Z=A_1$。两种都有

\[
R_Z>cR. \tag{16}
\]

事实上 $A_1$ 含 $h$ 是首边严格支配结论的必要前提，已由 $h$ 在边上共同覆盖得到；在空对族 $A_0$ 自然 $h$-only。

### 若 $H\ge R/2$：一根锚已经足够

假设某不含 $h$ 的 $t$ 有 $r=R_t>\phi H$。令 $z=R_Z$、共同重量 $C=w(C_Z\cap C_t)$。由于 $Z$ 为 $h$-only，所有共同者均小，且

\[
r>\phi H\ge cz,\qquad z>cR\ge cr,\qquad
C\le z-H\le H<qr,\quad C\le z/2<qz. \tag{17}
\]

这里 $r>\phi H\ge qR\ge q$；$z>cR>q$。最重共同顾客 $\le q/2<az\le a\max(r,z)$，因为 $z>cR\ge c$、$ac=q/2$。所以 **C 固定菜单成员**的三个实际条件均成立：两覆盖之比严格高于 $c$，$C<q\min(r,z)$，最大原子 $\le a\max(r,z)$。C 给高覆盖位置负载至少 $q$ 倍低覆盖、低覆盖位置负载至少 $q$ 倍高覆盖。两位置覆盖均 $>q$，由 $d(v)\le R_v$ 把覆盖配额逐项升级为 (1) 的 $d$ 配额，构成坏环禁止的见证。故所有不含 $h$ 的点 $R_t\le\phi H$；第 2 节中心引理矛盾。于是以下只需 $H<R/2$。

### 若 $H<R/2$：选相邻的双锚

由 (15)，$d(A_1)>\phi K>\phi R/2=cR>q$。若 $A_1$ 已为 $h$-only，选 $X=A_0,Y=A_1$；(5) 保证首边为唯一 $h$ 运输。若 $A_1$ 含唯一大对，$A_0$ 必是 $h$-only。令 $A_2=b(A_1)$。如 $A_2$ 不含 $h$，则 $R_2\ge d(A_1)>\phi K>cR$，与 $A_0$ 构成 C 弦：两者实际覆盖都 $>cR$ 且都 $\le R$，故两覆盖之比严格 $>c$；共同重量 $C\le R-H=K<qR_2$，这里用 $R_2>\phi K$，另由 $H>aR$ 得 $K=R-H<qR$。故 $C<q\min(R,R_2)$。$A_0$ 是 $h$-only，所有共同原子 $\le q/2<aR=a\max(R,R_2)$（$R\ge1$）。两覆盖 $>q$，C 见证与覆盖界 $d\le R$ 遂给双 $d$ 配额，矛盾。因此 $A_2$ 含 $h$；G1 禁止 $A_1,A_2$ 同大对，$A_2$ 为 $h$-only。$d(A_1)>q$ 使 (5) 适用于 $A_1\to A_2$，选 $X=A_1,Y=A_2$。

两种选择统一得到

\[
x=R_X>y=R_Y>cR,\quad
\delta=d(X)=y-\sigma>cR>\phi H,
\quad \varepsilon=d(Y),\quad0\le\sigma<x-y, \tag{18}
\]

且 $Y$ 为 $h$-only，$y>\phi K$。前一选择用 $y=R_1\ge d(A_0)>cR$、$y\ge d(A_1)>\phi K$；后一选择用 $y=R_2\ge d(A_1)>\phi K>cR$、$\delta=d(A_1)>\phi K>cR$。$cR>\phi H$ 来自 $H<R/2$。后一选择需要 $d(A_1)\le R_1$ 才给 $R_1>cR$：此时 $R_1\ge d(A_0)>cR>q$，所以覆盖界确实适用。

## 5. 双锚四条件及最终两支

由 (18) 的唯一运输，边 $X\to Y$ 的原设施负载 $x-H$；(1) 给

\[
\varepsilon>\phi(x-H)>\phi(y-H)=B. \tag{19}
\]

因 $y>cR>q$，覆盖界给 $\varepsilon\le y$，并由 (19) 得 $x<H+qy$。用 $\sigma<x-y$ 推出

\[
\delta=y-\sigma>2y-x>(2-q)y-H>B,
\]

末个严格差是 $q(H-ay)>0$，因为 $H>aR\ge ay$。再由 $y>\phi K$：

\[
B-K>\phi(R-2H)>0, \tag{20}
\]

计算为 $B-K>\phi(\phi K-H)-K=\phi(K-H)$；$H<R/2$。于是 (6) 的 $\delta>B,\varepsilon>B,\delta>\phi H,\varepsilon\le y$ 均已确认，另有 $B>K$。本节的每个 C 调用继续使用真实覆盖重量，不把 $B$ 或 $d$ 误当成 C 的输入。

**分支一：$H\ge y/2$。** 若不含 $h$ 的 $t$ 有 $r_t>\phi H$，以 $h$-only 的 $Y$ 重用 (17)：$r_t>\phi H\ge cy$、$y>cR\ge c r_t$；$C(Y,t)\le y-H\le H<q r_t$ 且 $C(Y,t)\le y/2<qy$。共同顾客都小于等于 $q/2<ay$，两覆盖均 $>q$（$r_t>\phi H>q$）。故 C 在 $(Y,t)$ 的实际覆盖门槛成立，覆盖配额转为 $d$ 配额，矛盾。于是所有不含 $h$ 的点 $R_t\le\phi H$，第 2 节中心引理排除本支。

**分支二：$H<y/2$。** 首先

\[
B=\phi(y-H)>cy>c^2R>q. \tag{21}
\]

最后一步利用 $R\ge1$ 及 $c^2>q$。若某个不含 $h$ 的 $t$ 有 $r_t>B$，则真实覆盖满足

\[
r_t>cy,\quad y>cR\ge c r_t,\quad
C(Y,t)\le y-H<qy,
\quad C(Y,t)\le y-H<q r_t. \tag{22}
\]

末个严格不等式来自 $r_t>\phi(y-H)$，前一个来自 $H>aR\ge ay$，即 $y-H<qy$。$Y$ 为 $h$-only，所有共同原子 $\le q/2<ay\le a\max(y,r_t)$；由 (21)，$r_t,y>q$。因此固定 C 成员的**实际覆盖**三条件均满足，给双覆盖配额；再由两边各自的 $d(v)\le R_v$ 换成双 $d$ 配额。坏环反设迫使

\[
h\notin C_t\Longrightarrow R_t\le B. \tag{23}
\]

从 $Y$ 开始沿 $b$ 行走，$d(Y)=\varepsilon>B$。只要当前 $s$ 有 $d(s)>B$，则下一点 $t=b(s)$ 满足 $R_t\ge d(s)>B$，由 (23) 必含 $h$。当前 $s$ 也含 $h$，且 $d(s)>B>K$，所以 (4) 排除 $R_t\ge R_s$；覆盖重严格下降。若永远 $d>B$，有限环上不可能永远严格下降。首次 $d(t)\le B$ 的 $t$ 仍由前点给 $R_t>B$，又由严格下降给 $R_t\le y$，且含 $h$，这正违反第 1 节双锚覆盖引理。因此空对族、单对族也不允许坏环。

## 6. 依赖、量词及重写边界

| 证明位置 | 实际固定菜单见证 | 需要另行已证的前提 |
|---|---|---|
| (3)–(4)、中心引理的低 $d$ 点、双锚覆盖 | P singleton，若修复则初始低侧仅有 $h$ 且初始差 $<H$ | 受保护修复性质及 (1) |
| (5)、首边 (14)–(15) | P 的一个纯成员及反向 singleton；最后用严格支配覆盖全部 NE | P 非空、坏环对每个菜单成员成立 |
| 等覆盖首边排除 | E 半分 | 两端真实覆盖相同、(1) |
| (17)、双锚选择 $A_0,A_2$、最终两支 | C 强弦；均先核真实覆盖比、共同总重、最大共同原子，再用 $R_v>q\Rightarrow d(v)\le R_v$ | 任意共同顾客人数的强弦证明及算法（L1/L2） |
| 星心识别、$h$-only 选择 | 本身不增加新的 NE 成员 | 大对避让、三角排除、同对回应边禁令（G1） |

因此 G2/G3 在本文件有自含的**条件性全分支闭环重写**：给定 G1 的结构结论与 L1/L2 的 C 引理，非退化星形、空对族和单对族均矛盾。它不宣称已重写或审毕那些外部前提，也不宣称通过外部同行评审。所有坏环地点限于 $T$，所有 $d(s)$ 始终以完整 $S$ 为域；C 的输入只有两点实际覆盖和共同顾客权重。

来源：[原集成主稿 §§2–13](../../../history/source/manuscripts/shared_phi/main.tex)；[工作稿的 G2/G3 接口](proof.md)。本文件把关键循环的依赖顺序、两个锚的门槛和两个 $H/y$ 分支重新逐式展开，不以原稿链接代替当前论证。
