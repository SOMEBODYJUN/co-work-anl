# 实分析 12 · Littlewood 三定律、Lusin 与可测性

黑字依原件保留命题、记号、估计、旁注及原错误。蓝色块标出补证、释义与订正。红字标出三处原稿明画的待填线，补全紧接待填位置。页次及低置信字形详见原件观察与恢复报告。

## 目录

1. [Littlewood 三定律与开区间近似](#1-littlewood-三定律与开区间近似)
2. [开覆盖、闭覆盖与连续性](#2-开覆盖闭覆盖与连续性)
3. [Egorov 一致收敛工具](#3-egorov-一致收敛工具)
4. [Lusin 定理的各种情形](#4-lusin-定理的各种情形)
   1. 有限测度的简单函数
   2. 公共闭集、有界化与一致极限
   3. 有限测度的 Egorov 路线
   4. 无限测度的环带路线
5. [正规空间、Tietze 延拓与 Urysohn 分隔](#5-正规空间tietze-延拓与-urysohn-分隔)
6. [Lusin 逆命题与可测性的三种刻画](#6-lusin-逆命题与可测性的三种刻画)
   1. Lusin 逆命题
   2. 可测性、简单函数逐点逼近和连续函数几乎处处逼近
   3. Borel–Cantelli 与逐点最终恒等

## 1. Littlewood 三定律与开区间近似

原稿第 1 页的顺序如下。

1. 每一个可测集几乎是有限个开区间并。
2. 每一个可测函数几乎连续。
3. 每个可测收敛函数列几乎一致收敛。

> [!info] 释义
> 第一条的“几乎”以对称差的测度任意小来度量，这里相应集合的测度有限。第二条指在遗漏任意小测度的闭子集上，限制函数连续。第三条指在有限测度的定义域内，删去任意小测度的集合后取得一致收敛，所给可测函数列原先几乎处处收敛。

**例题。** 设 $E\in\mathcal M$ 且 $m(E)<+\infty$。对每个 $\varepsilon>0$，存在开区间 $I_1,\ldots,I_n$，使
$$
m\left(E\triangle\bigcup_{i=1}^{n}I_i\right)<\varepsilon.
$$

> [!info] 补证
> 按 Lebesgue 外测度的开区间覆盖取可数族 $I_1,I_2,\ldots$，覆盖 $E$，且
> $$
> \sum_{j=1}^\infty |I_j|<m(E)+\frac{\varepsilon}{2}.
> $$
> 记 $O=\bigcup_{j\ge1}I_j$。由 $E\subset O$ 及有限性，
> $$
> m(O\setminus E)=m(O)-m(E)\le\sum_{j\ge1}|I_j|-m(E)<\frac{\varepsilon}{2}.
> $$
> 取 $n$ 使 $\sum_{j>n}|I_j|<\varepsilon/2$，置 $U=\bigcup_{j=1}^n I_j$。集合 $E\setminus U$ 被尾部区间覆盖，$U\setminus E$ 含于 $O\setminus E$。两部分不交，因此
> $$
> m(E\triangle U)=m(E\setminus U)+m(U\setminus E)<\frac{\varepsilon}{2}+\frac{\varepsilon}{2}=\varepsilon.
> $$
> 如定义外测度时使用闭区间，可逐项略微扩大为开区间，将扩大长度的总和先控制在所留预算内。

## 2. 开覆盖、闭覆盖与连续性

原稿第 1 页的 Lemma 设 $f:X\to Y$，且 $X$ 有一个开覆盖 $X=\bigcup_{i\in I}X_i$。若对各 $\alpha$ 有 $f_\alpha:X_\alpha\to Y$ 连续，则 $f:X\to Y$ 连续。原稿在引理中换用了指标 $i$ 和 $\alpha$。

取开集 $U$，原稿写出
$$
f^{-1}(U)=\bigcup_\alpha\bigl(f^{-1}(U)\cap X_\alpha\bigr)
=\bigcup_\alpha(f|_{X_\alpha})^{-1}(U).
$$
原稿随即写“注意 $f|_{X_\alpha}$ 连续”并把 $\tau_{X_\alpha}$ 与 $C\cap X_\alpha$、$C\in\tau_X$ 并记。因为 $X_\alpha$ 本身属于 $\tau_X$，$C\cap X_\alpha$ 是 $X$ 中开集。

> [!info] 记号与补证
> 两处指标可以统一为 $\alpha\in\Lambda$，$f_\alpha=f|_{X_\alpha}$。若从一族局部映射出发，须在每个交集 $X_\alpha\cap X_\beta$ 上取值一致，以定义这一个 $f$。
>
> 子空间拓扑应写为 $\tau_{X_\alpha}=\{C\cap X_\alpha:C\in\tau_X\}$。给定 $Y$ 中开集 $U$，限制映射的原像是 $X_\alpha$ 的开集，因而等于 $C_\alpha\cap X_\alpha$，其中 $C_\alpha$ 在 $X$ 中开。开覆盖中的 $X_\alpha$ 也在 $X$ 中开，故这些交集和它们的并都在 $X$ 中开。这样对每个 $U\in\tau_Y$ 都有 $f^{-1}(U)\in\tau_X$。从全局连续反推各限制连续时，同一取交式直接给出相对开性。

原稿还把开覆盖换成局部有限闭覆盖。给定 $x\in X$，存在邻域 $U$，它只与有限个 $X_\alpha$ 相交。页末有“可测也类似，要求可取〔一个〕覆盖”的短句，括出的连接字形据上下文读。

> [!info] 补证 · 闭覆盖的粘合
> 设 $\{X_\alpha\}$ 是 $X$ 的局部有限闭覆盖，每个 $f|_{X_\alpha}$ 连续。对任意闭集 $D\subset Y$，令 $D_\alpha=(f|_{X_\alpha})^{-1}(D)$。$D_\alpha$ 在 $X_\alpha$ 中闭，而 $X_\alpha$ 在 $X$ 中闭，故 $D_\alpha$ 在 $X$ 中闭。给定 $x\notin\bigcup_\alpha D_\alpha$，取开邻域 $U$，使它仅与有限个 $X_\alpha$ 相交。从 $U$ 中删去这些片上的有限个闭集 $D_\alpha$，便得到 $x$ 的开邻域，且与整个 $\bigcup_\alpha D_\alpha$ 不交。于是 $f^{-1}(D)=\bigcup_\alpha D_\alpha$ 在 $X$ 中闭，$f$ 连续。有限闭覆盖自动局部有限。
>
> 局部有限条件保证闭集并仍闭。若在 $\mathbb R$ 用所有单点作闭覆盖，任意函数的每个限制都连续，其中包含在 $0$ 处跃迁的函数。

> [!info] 补证 · 可测覆盖
> 若 $X$ 由可数个可测子集 $X_j$ 覆盖，各 $f|_{X_j}$ 相对于相应的子空间 $\sigma$-代数可测，则对目标任一可测集 $D$ 有 $f^{-1}(D)=\bigcup_j(f^{-1}(D)\cap X_j)$。每项相对可测，且 $X_j$ 可测，故各项及其可数并在 $X$ 中可测。

## 3. Egorov 一致收敛工具

原稿第 3 页提醒 Egorov 要求 $m(E)<+\infty$。第 4 页用 $G_\delta\subset E$ 表示要删掉的一部分，在 $E\setminus G_\delta$ 上写 $\varphi_k$ 一致趋于 $f$。

> [!info] 补证 · Egorov 定理
> 设 $E$ 可测且 $m(E)<+\infty$，$u_k,u$ 是 $E$ 上的可测实函数，$u_k\to u$ 几乎处处。对 $\eta>0$ 取例外集 $G$，使 $m(G)<\eta$ 且 $u_k$ 在 $E\setminus G$ 上一致趋于 $u$。
>
> 对每个整数 $r\ge1$，置
> $$
> W_{r,N}=\bigcup_{k\ge N}\{x\in E:|u_k(x)-u(x)|\ge 1/r\}.
> $$
> 当 $N$ 增大时，$W_{r,N}$ 递减。其交是误差至少 $1/r$ 无穷次发生的点集，测度为 0。由 $m(W_{r,1})\le m(E)<+\infty$ 与测度的上连续性，选 $N_r$ 使 $m(W_{r,N_r})<\eta\,2^{-r}$。令 $G=\bigcup_{r\ge1}W_{r,N_r}$，则 $m(G)<\eta$，严格号来自首项已严格小于其预算。给定 $\epsilon>0$，取 $r$ 使 $1/r<\epsilon$。当 $k\ge N_r$ 时，所有 $x\in E\setminus G$ 同时满足 $|u_k(x)-u(x)|<1/r$，于是收敛一致。
>
> 有限测度的作用在上连续性。取 $u_k=\mathbf1_{[k,\infty)}$ 于 $[0,\infty)$，它逐点趋于 $0$；在删去任一有限测度集后的集合上，每个 $u_k$ 仍取得 $1$。

## 4. Lusin 定理的各种情形

**Lusin 定理。** 设 $f$ 是 $E$ 上 a.e. 有限的 Lebesgue 可测函数。对任意 $\delta>0$，存在闭集 $F_\delta\subset E$，满足 $m(E\setminus F_\delta)<\delta$ 且 $f|_{F_\delta}\in C(F_\delta)$。

> [!info] 适用范围与内正规性
> 这里 $E$ 是 $\mathbb R^n$ 中的 Lebesgue 可测集，闭集是在 $\mathbb R^n$ 中闭。若 $f$ 可取 $\pm\infty$，先删除零测集 $N=\{x\in E:|f(x)|=\infty\}$，下文在 $E\setminus N$ 工作，闭集 $F_\delta$ 仍闭于 $\mathbb R^n$，且补回 $N$ 不改变误差测度。
>
> 对有限测度可测集 $A$ 和 $\eta>0$，可取紧 $K\subset A$ 使 $m(A\setminus K)<\eta$。取大闭盒 $Q$ 使 $m(A\setminus Q)<\eta/2$。按外测度的开盒覆盖取开集 $O\supset Q\setminus A$ 使 $m(O\setminus(Q\setminus A))<\eta/2$。令 $K=Q\setminus O$，则 $K$ 紧且 $K\subset A$，遗漏部分满足
> $$
> m(A\setminus K)\le m(A\setminus Q)+m(O\setminus(Q\setminus A))<\eta.
> $$

### 4.1 有限测度的简单函数

原稿写“开始，闭集构造 $F_\delta$ 的表达式”。对 $f\in S(E)$，选用 $E_1,\ldots,E_\ell\in\mathcal M$，写 $f=\sum_{i=1}^\ell c_i\chi_{E_i}$。原稿在这行的覆盖式右侧写成 $\bigcup_i X_i$ 式样。由 Lebesgue 测度内正规性取闭集 $F_{i,\delta}\subset E_i$，满足 $m(E_i\setminus F_{i,\delta})<\delta/\ell$。令 $F_\delta=\bigcup_{i=1}^{\ell}F_{i,\delta}$。原稿的测度链为
$$
m(E\setminus F_\delta)=m\left(E\setminus\bigcup_i F_{i,\delta}\right)
=m\left(\bigcup_{i=1}^{\ell}(E\setminus F_{i,\delta})\right)
=\sum_i m(E\setminus F_{i,\delta})<\delta.
$$

> [!info] 订正与补证
> 取 $E_i=\{x\in E:f(x)=c_i\}$ 为不同函数值的层集，则 $E=\bigcup_i E_i$，各层可测且两两不交。按内正规性分配 $\delta/\ell$ 得上述 $F_{i,\delta}$，其有限并在 $\mathbb R^n$ 中闭，且各块上 $f=c_i$ 连续。应用有限闭覆盖的粘合，得到 $f|_{F_\delta}$ 连续。
>
> 原链中的 $E$ 与 $\bigcup$ 不能一同用在差集展开。De Morgan 律给 $E\setminus\bigcup_i F_{i,\delta}=\bigcap_i(E\setminus F_{i,\delta})$，或按两两不交值层写为
> $$
> E\setminus F_\delta=\bigcup_{i=1}^{\ell}(E_i\setminus F_{i,\delta}),
> \qquad m(E\setminus F_\delta)=\sum_{i=1}^{\ell}m(E_i\setminus F_{i,\delta})<\delta .
> $$
> 例如取 $E=[0,1]\cup[2,3]$，$F_{1,\delta}=[0,1]$、$F_{2,\delta}=[2,3]$。真实补集为空，原链却会把整个 $E$ 计入并集。

### 4.2 公共闭集、有界化与一致极限

一般情形 $f\in\mathcal M(E)$，原稿第 2 页末取 $\{\varphi_k\}\subset S(E)$，$\varphi_k(x)\to f(x)$，$x\in E$。第 3 页初由第 (1) 步，给定 $\delta>0$，逐个 $k\in\mathbb N^*$ 取闭集 $F_k\subset E$，使 $m(E\setminus F_k)<\delta/2^k$。首行闭包含左边原有 $F_\delta$ 形，与误差行的 $F_k$ 并见。第二行写 $\varphi_k\in C(F_k)$。令 $F_\delta=\bigcap_{k=1}^{\infty}F_k$，原稿把 $m(E\setminus F_\delta)$ 展开为各补集之并的测度，再以 $\sum_k\delta/2^k$ 估计。接着重复写“$\varphi_k$ 在 $F_k$ 上连续。$\varphi_k$ 在 $\cap F_k$ 上连续，$f$ 还一致收敛”。

原稿随后记 $f$ a.e. 有限、$m(E(|f|=+\infty))=0$，令
$$
g(x)=\frac{f(x)}{1+|f(x)|}.
$$
则 $g$ 有界，原稿两行逆式为
$$
|f(x)|=\frac{|g(x)|}{1-|g(x)|},\qquad
f(x)=\frac{g(x)}{1-g(x)}.
$$
旁边再记 $g(x)$ 有界。

> [!info] 订正与补证 · 有界化路线
> $\varphi_k\in C(F_k)$ 表示限制 $\varphi_k|_{F_k}\in C(F_k)$。固定 $\delta$ 后，各 $F_k$ 随 $k$ 各自选取，$F_\delta$ 表示最后的共同闭集。由 $F_\delta\subset F_k$，每个 $\varphi_k|_{F_\delta}$ 连续，而且
> $$
> m(E\setminus F_\delta)
> =m\left(\bigcup_{k\ge1}(E\setminus F_k)\right)
> \le \sum_{k\ge1}m(E\setminus F_k)<\delta.
> $$
> 最后一号可从首项严格和其余项的弱上界得到。无穷交中每个 $F_k$ 本身闭。
>
> 逐点收敛本身尚不足以使公共闭集上的极限连续。设 $E=[2,3]\cup\{0\}\cup\{1/j:j\ge1\}$，在每个有限孤立点集 $\{1,\ldots,1/k\}$ 上取 $1$、其余取 $0$。每个这样的简单函数在闭集 $E$ 上连续，逐点极限在 $0$ 不连续。其一致误差至少在 $1/(k+1)$ 处等于 $1$。
>
> 先证有界的情形。对有界可测实函数 $u$ 取 $\psi_k=2^{-k}\lfloor 2^k u\rfloor$。它是有限值简单函数，且对所有 $x$ 有 $0\le u(x)-\psi_k(x)<2^{-k}$。把上述闭集交的构造用于 $\psi_k$，它们在 $F_\delta$ 上一致趋于 $u|_{F_\delta}$，故后者连续。
>
> 对一般实值 $f$，应用有界情形于 $g=T\circ f$，其中 $T(t)=t/(1+|t|)$ 连续，且 $|T(t)|<1$。$T$ 的连续逆为 $T^{-1}(s)=s/(1-|s|)$，$s\in(-1,1)$。原稿的第二行漏掉分母绝对值，例如 $f=-2$ 时 $g=-2/3$，用 $1-g$ 会给 $-2/5$。现在 $g|_{F_\delta}$ 连续且逐点值域在 $(-1,1)$，复合 $T^{-1}$ 得 $f|_{F_\delta}$ 连续。

### 4.3 有限测度的 Egorov 路线

原稿第 3 页下写“或用 Egorov 定理”。先设 $m(E)<+\infty$，$\exists\varphi_k\to f$。对每个 $\delta>0$ 取闭 $F_\delta\subset E$，$m(E\setminus F_\delta)$ <span style="color:#c62828">〔原待填〕</span>。

> [!info] 补全第一处待填
> 前一步共同闭集的构造把预算换成 $\delta/3$，得到 $m(E\setminus F_\delta)<\delta/3$，且每个 $\varphi_k|_{F_\delta}$ 已连续。这条路线可使用任何逐点逼近的可测简单函数列。

第 4 页续写用 Egorov 取 $G_\delta\subset E$，$m(E\setminus G_\delta)$ <span style="color:#c62828">〔原待填〕</span>，$\varphi_k$ 在 $E\setminus G_\delta$ 上一致趋于 $f$。

> [!info] 补全第二处待填
> 按后续公式取 $G_\delta$ 为例外集，Egorov 给 $m(G_\delta)<\delta/3$。沿用原式左侧可填 $m(E\setminus G_\delta)>m(E)-\delta/3$。有限测度下两式等价。

原稿考虑 $F_\delta\cap(E\setminus G_\delta)$。由可测集的内正规性，取闭集 $H_\delta\subset E\setminus G_\delta$，并写 $m((E\setminus G_\delta)\setminus H_\delta)<$ <span style="color:#c62828">〔原待填〕</span>。

> [!info] 补全第三处待填
> 取 $\delta/3$。因为 $E\setminus G_\delta$ 可测且有限测度，内正规性确实可给闭 $H_\delta$ 及这个界。

原稿令 $\widehat F_\delta=F_\delta\cap H_\delta$，对
$$
m\bigl((E\setminus F_\delta)\cup(E\setminus H_\delta)\bigr)
<m(E\setminus F_\delta)+m(E\setminus H_\delta)
$$
作估计，并写
$$
E\setminus H_\delta
=\bigl((E\setminus G_\delta)\setminus H_\delta\bigr)\cup(G_\delta\setminus H_\delta).
$$

> [!info] 订正与补证
> 原稿的并集测度步骤可用 $\le$。例如两个补集恰好不交时等号成立。又因 $H_\delta\cap G_\delta=\varnothing$，上式的第二项就是 $G_\delta$。对闭集 $\widehat F_\delta$，
> $$
> \begin{aligned}
> m(E\setminus\widehat F_\delta)
> &\le m(E\setminus F_\delta)+m(E\setminus H_\delta)\\
> &=m(E\setminus F_\delta)+m((E\setminus G_\delta)\setminus H_\delta)+m(G_\delta)\\
> &<\delta .
> \end{aligned}
> $$
> $\widehat F_\delta\subset F_\delta$ 使每个 $\varphi_k$ 的限制连续，$\widehat F_\delta\subset E\setminus G_\delta$ 使收敛一致。连续函数的一致极限仍连续，故 $f|_{\widehat F_\delta}$ 连续。

### 4.4 无限测度的环带路线

原稿第 4 页下另设 $m(E)=+\infty$，令
$$
A_k=B(0,k)\setminus B(0,k-1),\qquad
E=\bigcup_{k=1}^\infty(A_k\cap E).
$$
在 $A_k\cap E$ 上取一个闭集。原稿最后一行写“需要用局部有限性”。

> [!info] 补证
> 约定 $B(0,k)$ 是开球，$B(0,0)=\varnothing$。每个 $E_k=A_k\cap E$ 可测且有限测度。用有限测度情形给 $E_k$ 取闭的 $K_k\subset E_k$，使 $m(E_k\setminus K_k)<\delta 2^{-k}$ 且 $f|_{K_k}$ 连续。给定 $x\in\mathbb R^n$，一个有界邻域只和有限个环带相交，所以也只和有限个 $K_k$ 相交。这些闭集的并 $K=\bigcup_k K_k$ 在 $\mathbb R^n$ 中闭，它们在 $K$ 中是局部有限闭覆盖，故由第 2 节知 $f|_K$ 连续。
> $$
> m(E\setminus K)
> =m\left(\bigcup_{k\ge1}(E_k\setminus K_k)\right)
> \le\sum_{k\ge1}m(E_k\setminus K_k)<\delta .
> $$
> 这样得到无限测度定义域上的 Lusin 结论。各环带的局部有限性保证闭性与粘合，误差的可求和性保证全局预算。

## 5. 正规空间、Tietze 延拓与 Urysohn 分隔

原稿第 5 页写设 $(X,\tau)$，下述等价。

1. $X$ 正规。
2. 对每个闭集 $E\subset X$，若 $f\in C(F)$，则存在 $F\in C(X)$，使 $F|_E=f$。（Tietze）
3. 对不交闭集 $A,B\subset X$，存在连续函数 $f$，满足 $f|_A=0$、$f|_B=1$。（Urysohn）箭头从 $X$ 指向一段区间，原写右端括号近于圆括形。

Remark 提到外测度 $m^*(A\cup B)$ 与“$A$ 和 $B$ 可被可测集分〔隔〕”。右端只见至“分”，末字据语义读取。下一行另写 $C=A\cup B$。

> [!info] 订正与命题
> (2) 的条件应是 $f\in C(E)$，其值在闭集 $E$ 上给定。原稿此处的括号内字面为 $F$。结论中的 $F$ 是 $f$ 的实值连续延拓。
>
> (3) 的余域为 $[0,1]$，两个常值要求分别使用端点 $0$ 和 $1$。采用正规空间包含 $T_1$ 的定义时，在 $T_1$ 空间内陈述等价即可。

> [!info] 补证 · 正规性推出 Urysohn 分隔
> 若闭集 $D$ 被开集 $O$ 包含，由正规性分开 $D$ 与 $X\setminus O$，可取开集 $V$ 使 $D\subset V\subset\overline V\subset O$。令 $U_1=X\setminus B$，先取 $U_0$ 使 $A\subset U_0\subset\overline{U_0}\subset U_1$。在已构造的相邻二进有理数 $r<s$ 之间，对闭 $\overline U_r$ 和开 $U_s$ 再用缩小邻域的性质，构造中点的 $U_{(r+s)/2}$。逐级得到全体二进有理标号 $D_2\subset [0,1]$ 上的开集，且 $r<s$ 时 $\overline U_r\subset U_s$。
>
> 定义 $u(x)=\inf\{r\in D_2:x\in U_r\}$，空集合取 $1$，所以 $0\le u\le1$。$A$ 上 $u=0$，$B$ 上 $u=1$。对 $0<a\le1$，$\{u<a\}=\bigcup_{r<a}U_r$。对 $0\le a<1$，
> $$
> \{u>a\}=\bigcup_{\substack{r\in D_2\\r>a}}(X\setminus\overline U_r).
> $$
> 若点在右侧，则它不属于任一 $s<r$ 的 $U_s$，故 $u\ge r>a$。若 $u>a$，选 $a<r<s<u$ 的二进有理数，点在 $U_s$ 外，于是也在 $\overline U_r$ 外。端点之外的水平集为全空间或空集。上述上下水平集均开，$u$ 连续。

> [!info] 补证 · Urysohn 分隔推出 Tietze 延拓
> 先设 $f:E\to\mathbb R$ 连续且 $|f|\le a$，其中 $a>0$。给任一连续剩余量 $r$ 满足 $|r|\le b$，取两块闭集 $\{x\in E:r(x)\le-b/3\}$ 与 $\{x\in E:r(x)\ge b/3\}$。它们因 $E$ 闭而都是 $X$ 的闭集。Urysohn 函数 $u$ 在两块上分别取 $0$、$1$，设 $h=(2u-1)b/3$，则 $|h|\le b/3$ 且 $|r(x)-h(x)|\le 2b/3$ 对所有 $x\in E$ 成立。在两块上分别用 $h=-b/3,b/3$ 检验，中间用 $|r|<b/3$ 即得。
>
> 从 $r_0=f$ 开始递推。第 $j$ 次取 $b_j=a(2/3)^j$，得到 $h_j$ 并令 $r_{j+1}=r_j-h_j|_E$。于是 $\sup_X|h_j|\le b_j/3$，$\sup_E|r_{j+1}|\le b_{j+1}$。级数 $\sum_{j=0}^\infty h_j$ 在 $X$ 上一致收敛，和函数 $H$ 连续且 $|H|\le a$。在 $E$ 上余量趋零，所以 $H|_E=f$。
>
> 对无界的连续 $f$，先令 $q=f/(1+|f|)$，把其有界延拓记为 $Q:X\to[-1,1]$。闭集 $D=Q^{-1}(\{-1,1\})$ 与 $E$ 不交。Urysohn 给连续 $v:X\to[0,1]$，其在 $E$ 上为 $1$，在 $D$ 上为 $0$。因此 $|vQ|<1$ 在 $X$ 上逐点成立，且 $(vQ)|_E=q$。令 $F=vQ/(1-|vQ|)$，就是所需实值连续延拓。

> [!info] 补证 · 反向两支与 $C=A\cup B$
> 由 (2) 得 (3) 时，在 $C=A\cup B$ 上令 $a|_A=0$、$a|_B=1$，有限闭覆盖粘合给 $a\in C(C)$。应用 (2) 延拓到 $X$，再复合连续截断 $t\mapsto\max(0,\min(t,1))$，得到 (3)。
>
> 由 (3) 得正规性时，$f^{-1}([0,1/3))$ 和 $f^{-1}((2/3,1])$ 是包含 $A,B$ 的不交开邻域，区间开性取 $[0,1]$ 的相对拓扑。$\mathbb R^n$ 正规，因为不交非空闭集 $A,B$ 由连续函数
> $$
> x\longmapsto \frac{d(x,A)}{d(x,A)+d(x,B)}
> $$
> 分隔。距离函数是 $1$-Lipschitz，分母在任一点为正。若一块为空，用相应常数函数即可。

> [!info] 释义 · Remark 中的可测分隔
> 设 $A,B\subset\mathbb R^n$，若有 Lebesgue 可测集 $D$ 使 $A\subset D$、$B\subset D^c$，把 Carathéodory 等式用于 $A\cup B$，即得
> $$
> m^*(A\cup B)=m^*((A\cup B)\cap D)+m^*((A\cup B)\setminus D)=m^*(A)+m^*(B).
> $$
> 在上述 Urysohn 情形可取 $D=f^{-1}([0,1/2))$，它是 Borel 集。原稿的 $C=A\cup B$ 则可作为先定义分段函数的闭域。

## 6. Lusin 逆命题与可测性的三种刻画

### 6.1 Lusin 逆命题

原稿第 5 页页首写“Lusin 逆定理也成立”。

> [!info] 补证
> 设 $E\subset\mathbb R^n$ 可测，且对每个 $\delta>0$ 都有一个在 $\mathbb R^n$ 中闭的 $F_\delta\subset E$，满足 $m(E\setminus F_\delta)<\delta$，且 $f|_{F_\delta}$ 连续。取 $\delta=2^{-j}$，令 $F=\bigcup_{j\ge1}F_{2^{-j}}$。因 $E\setminus F\subset E\setminus F_{2^{-j}}$ 对各 $j$ 都成立，故 $m(E\setminus F)=0$。
>
> 对每个开集 $V\subset\mathbb R$，在 $F_{2^{-n}}$ 上的原像为该闭子空间中的开集，故在 $\mathbb R^n$ 中 Borel。它们的可数并是 $f$ 在 $F$ 上的原像，在 $E\setminus F$ 上的剩余部分是零测集的子集，因 Lebesgue 测度完备而可测。因此 $f$ 在 $E$ 上可测。如果允许 $f$ 在零测补集取扩展实值，同样用超水平集判别。

### 6.2 可测性、简单函数逐点逼近和连续函数几乎处处逼近

原稿第 5 页下的定理设 $f$ 为 $E$ 上几乎处处有限的函数，$E\in\mathcal M$。三条为

1. $f$ 可测。
2. 存在 $\{\varphi_k\}\subset S(E)$，$\varphi_k\to f$ 逐点。
3. 存在 $\{\varphi_k\}\subset C(\mathbb R^n)$，$\varphi_k\xrightarrow{\mathrm{a.e.}}f$。

> [!info] 补证 · 简单函数的等价
> 由 (1) 得 (2)。将 $f$ 截断到 $[-k,k]$ 得 $f^{(k)}=\max(-k,\min(k,f))$，再取 $\varphi_k=2^{-k}\lfloor 2^kf^{(k)}\rfloor$。每个函数为可测简单函数，$0\le f^{(k)}(x)-\varphi_k(x)<2^{-k}$，且 $f^{(k)}(x)\to f(x)$，于是所需逐点收敛成立。若允许零测点取 $\pm\infty$，在那里有 $\varphi_k(x)=\pm k$，故逐点收敛在扩展实数意义下依然成立。
>
> 由 (2) 得 (1)。若 $\varphi_k$ 逐点趋于 $f$，则对每个 $a\in\mathbb R$，
> $$
> \{x\in E:f(x)>a\}
> =
> \bigcup_{\substack{q\in\mathbb Q\\q>a}}\bigcup_{N=1}^\infty
> \bigcap_{k\ge N}\{x\in E:\varphi_k(x)>q\}.
> $$
> 右侧各项可测。若 $f(x)>a$，可在两值之间取 $q$，从某项起 $\varphi_k(x)>q$；反之，有这样的 $q$ 时 $f(x)\ge q>a$。

> [!info] 补证 · 由 (3) 得 (1)
> 每个全空间连续函数限制到 $E$ 可测。可令 $u=\liminf_k \varphi_k|_E$，它是可测扩展实函数，因为可数上确界和下确界保持可测性。$u=f$ 在 $E$ 上几乎处处成立，两者的任一超水平集的对称差是零测集的子集。Lebesgue 测度完备，故 $f$ 可测。

### 6.3 Borel–Cantelli 与逐点最终恒等

原稿第 6 页专证 $(1)\Rightarrow(3)$。先写 $\exists g\in C(\mathbb R^n)$，$g|_{F_\delta}=f$。随后对每个 $k\in\mathbb N^*$ 写 $\exists F_k$ 闭 $\subset E$，$g_k\in C(\mathbb R^n)$，同一行的限制原式仍写 $g|_{F_k}=f$，并有
$$
m(E\setminus F_k)<\frac1{2^k}.
$$

> [!info] 补证与订正
> 对给定 $\delta>0$，Lusin 给闭 $F_\delta\subset E$ 及连续 $f|_{F_\delta}$，后者由 Tietze 延拓为 $g\in C(\mathbb R^n)$，在 $F_\delta$ 上与 $f$ 相等。令 $\delta=2^{-k}$，逐项得到 $F_k$ 和 $g_k$，第 $k$ 项的限制式应为 $g_k|_{F_k}=f|_{F_k}$。

其下写“由 Borel–Cantelli”，$m(\limsup_{n\to\infty}E_n)=0$。旁写“考虑 $E\{g_k\ne f\}\subset E\setminus F_k$”。再写
$$
m\left(\limsup_{k\to\infty}E(g_k\ne f)\right)=0,\qquad
m\left(\bigcap_{n=1}^\infty\bigcup_{k\ge n}E(g_k\ne f)\right)=0.
$$
下一行把几乎每个点写入好集
$$
\text{（几乎任意） }x\in\bigcup_{n=1}^\infty\bigcap_{k\ge n}E(f=g_k).
$$
末写存在 $N(x)$，使 $k>N(x)$ 时 $f=g_k$ 恒等。

> [!info] 释义与补证
> 这里 $E(P)=\{x\in E:P(x)\}$。令 $D_k=E(g_k\ne f)$，则 $D_k\subset E\setminus F_k$，由小测度预算可求和可知
> $$
> m\left(\bigcup_{k\ge n}D_k\right)
> \le\sum_{k\ge n}m(E\setminus F_k)
> \le\sum_{k\ge n}2^{-k}\longrightarrow0.
> $$
> $\limsup D_k=\bigcap_{n=1}^\infty\bigcup_{k\ge n}D_k$ 含于每个尾并，因此测度为 $0$。用 $E_k=E\setminus F_k$ 代替 $D_k$，同一估计也给 $m(\limsup E_k)=0$。
>
> 在 $E$ 内取相对补集，De Morgan 律给
> $$
> E\setminus\limsup D_k=\bigcup_{n=1}^\infty\bigcap_{k\ge n}E(f=g_k).
> $$
> 对每个在此并集中的 $x$，有一个依赖于 $x$ 的指标 $N(x)$，使所有 $k\ge N(x)$ 均有 $g_k(x)=f(x)$，于是 $g_k(x)\to f(x)$。这证明整列全空间连续函数限制到 $E$ 后几乎处处收敛，且几乎每一点从某项起取值完全相同。

原稿第 7 物理页为空白。
