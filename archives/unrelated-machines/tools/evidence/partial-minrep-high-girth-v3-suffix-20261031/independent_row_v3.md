# 正规高围长部分 MinRep：v3 陈述先行独立重构

读取目的：仅据 Exact 重构新的 copy-list 同时性、短周期与保度修复、有限随机位和总位复杂度，不借用作者证明。

## 实际读取与顺序

已实际 SHA 并全文读 `regular_high_girth_partial_minrep_v3_exact_statement.md`，SHA256：

`0e2b614ae0a0af12c592d3b57558e2c3baf13cf4377b90b26769fc6e5d24cc61`。

本文冻结前没有读 root、hardness_route 或 pcsp_occurrence 的本候选推导、证明、审查，也没有询问他们。审查者曾独立重构前一线性度数源 v2 的 heavy-list 引理；下面把该思想重新用于 fiber 平均列表，并单独证明新的高阶 witness 概率。对 PCP 起点仍只作条件使用，不把本文计为亲读外部源定理。

结论：Exact 1–5 均可独立重构，暂未发现 fatal objection。关键是下面的 slot-cap witness 尾界；单标签 Azuma 不足以代替它。

全篇采用 Exact 的 \(N,n,D,Q,g,\rho,G,\ell,\lambda,\tau,\gamma,d,S,B,U,z,t\)。令 \(N'=Nt\)、\(M'=dN'/2=tm_*\)。概率先在理想独立均匀 permutations 模型中证明，再计入有限拒绝采样的 FAIL。

## 1. 固定任意 copy lists 的期望上界

固定所有 copy 顶点的任意列表，总成本至多 \(gN'\)。对每个原顶点 \(u\) 和标签 \(\alpha\)，定义
\[
 s_{u\alpha}=\frac1t\#\{c:\alpha\text{ 在 copy }(u,c)\text{ 的列表中}\},
 \qquad L_u=\sum_\alpha s_{u\alpha}.
\]
于是 \(\sum_uL_u\le gN\)。对每条原 edge type \(e=(u,v)\)，令 \(p_e\) 是独立均匀挑选 \(u,v\) 两个 copies 时其列表覆盖 \(e\) 的概率。

令 \(H=4g/\tau\)。称 \(L_u>H\) 的原顶点为 heavy。其数量至多 \(gN/H\)，原 \(D\)-正则多图中碰到 heavy 点的 edge types 比例至多 \(2g/H=\tau/2\)；平行约束仍逐条计数，因此估计不变。

对两端均 low 的原边，union bound 给
\[
 p_e\le\sum_{\alpha}\!s_{u\alpha}s_{v,\pi_e(\alpha)}.
\]
在每个 \(L_u>0\) 的原点独立按 \(s_{u\alpha}/L_u\) 选一个标签；\(L_u=0\) 的点任取标签。若原游戏 \(\operatorname{val}\le\gamma\)，这个随机原单标签赋值的满足边期望至多 \(\gamma M\)。low–low 边上的上述兼容和至多 \(H^2\) 乘它的单标签满足概率。因此
\[
 \frac1M\sum_e p_e\le\tau/2+\gamma H^2
 =\left(\frac12+\frac{2}{125}\right)\tau
 =\frac{129}{250}\tau<\tau.                       \tag{1}
\]

每 layer 的每个原 edge type 恰有 \(z\) 枚 template 边。其两端由不同原顶点的独立 permutations 映到独立均匀 copies，所以其覆盖边际正是 \(p_e\)。若 \(X\) 是全部 \(d\) layers 的覆盖边数（保留 edge 身份），则
\[
 \mu=\mathbb EX=dz\sum_e p_e\le\tau M'.             \tag{2}
\]
这适用于 copies 任意不同的列表，没有把每个原点的所有 copies 强迫使用同一列表。

## 2. slot-cap witness：全部 copy lists 的高阶尾界

固定同一个列表族，并把每条 template 边的未条件化覆盖边际记为 \(p_e\)，按 layer 和 template occurrence 重复计数，故这些边际的总和为 \(\mu\)。

### 2.1 大覆盖集有半度数 witness

每层的 covered template 边在原左右顶点上形成二部多图，每个原点度数至多 \(t\)。这样的多图可分成两个边组，使每个原点在每组的度数至多 \(\lceil t/2\rceil\)。一个自足理由是：补 dummy 平行边使两侧原顶点都 \(t\)-正则（两侧总缺度相等）；Hall 给完美匹配，逐次删除得到 \(t\) 个匹配；把颜色分成前 \(\lceil t/2\rceil\) 个与其余，再删除 dummy 边即可。

对每层分别作此分组，把全部层的第一组和第二组各合并。两组大小和为 \(X\)，所以若 \(X\ge a\)，至少一组含 \(\lceil a/2\rceil\) 条边。在该组取恰
\[
 m=\lceil a/2\rceil
\]
条边，就得到 witness：对每个 (layer, 原顶点)，用到的 template slots 不超过 \(\lceil t/2\rceil\)。分组只用于存在性，不要求在输出算法中猜测这个 witness。

### 2.2 固定 witness 的联合概率

任取满足上述 slot cap 的 \(m\) 枚 template 边，按固定顺序逐条揭示两端 permutations 的 images。在每个相关 fiber 中，之前已用的 slots 少于 \(\lceil t/2\rceil\)，当前 image 均匀落在至少 \(t/2\) 个尚未使用的 copy 编号中。不同两端属于不同原顶点，故在给定此前具体 images 后仍独立均匀。

即使此前覆盖条件具有正相关，条件可用 copy 对中的兼容对数也至多全 \(t^2\) 对的兼容对数。因此当前边的条件覆盖概率至多 \(4p_e\)。逐条条件化得这个 witness 全覆盖的概率至多 \(4^m\prod_e p_e\)。这里没有把同一 permutation 中的 images 误当独立抽样。

对所有合格 witness 并界，放宽为全部 \(m\)-边子集并用基本对称多项式界：
\[
 \Pr[X\ge a]\le 4^m\!\sum_{|W|=m}\prod_{e\in W}p_e
 \le \frac{(4\mu)^m}{m!}
 \le\left(\frac{4e\mu}{m}\right)^m.                \tag{3}
\]

取 \(a=\rho M'/2\)，则 \(m\ge\rho M'/4\)。由式 (2)，
\[
 \frac{4e\mu}{m}\le\frac{16e\tau}{\rho}
 =\frac{4e}{25g^2}<\frac1{g^2}.
\]
因此
\[
 \Pr[X\ge\rho M'/2]\le g^{-\rho M'/2}.             \tag{4}
\]

### 2.3 对所有 copy lists 同时并界

共有 \(N'Q\) 个顶点标签 token，成本上限为整数 \(gN'\)。因为 \(Q\gamma\ge1\) 特别保证 \(Q>g\)，用生成函数或低成本子集计数，有
\[
 \#\mathrm{lists}\le(eQ/g)^{gN'}\le\exp(gN'\lambda).
\]
后一式由 \(1+\ln Q\le1+\lceil\log_2Q\rceil=\lambda\)。若愿意使用允许重复的序列也须保留足够常数；这里直接用无重复 token 子集。

式 (4) 对每个先固定列表成立；因此任意坏列表存在的概率至多
\[
 \exp\!\left(gN'\lambda-\frac{\rho dN'}4\ln g\right)
 \le \exp(-124gN'\lambda)<10^{-3}.                 \tag{5}
\]
最后用 \(d\ge1000g\lambda/(\rho\ell)\)、\(\ln g\ge\ell\ln2>\ell/2\)。所以以严格大于 \(1-10^{-3}\) 的概率，初始随机多图**所有**成本 \(\le gN'\) copy lists 的覆盖均严格少于 \(\rho M'/2\)。

## 3. 短 simple cycles 的期望

理想随机图有 \(N'\) 个 copy 顶点，每个 layer 是 perfect matching，因此总多图每顶点度为 \(d\)。长度 \(l\) 的定向 walk 可以由起点 copy 和 \(l\) 个 layer 选择唯一确定。

对一组可形成 simple cycle 的起点和 layer word，按 walk 顺序揭示所需 permutations。若提前重复顶点，则不形成所计 simple cycle；否则在最后一步前其余顶点均不同。最后 layer 不同于起点的第一 layer，也不同于倒数第二 layer，否则某个 cycle 顶点会在同一个 matching 内用两条不同边。故起点在最后 layer 的 permutation image 尚未揭示。

每个此前揭示的匹配边，在一个固定原顶点的 fiber 中至多揭示一个 copy image，因为二部边不把一个原顶点接到自身。末步若其 template partner 已揭示，不可能正好给尚未揭示的起点；若未揭示，它在目标 fiber 的剩余至少 \(t-G\) 个 copies 中均匀。故末步闭合概率至多
\[
 (t-G)^{-1}\le2/t,
\]
这里 \(t\ge z\ge2G+1\)。同一 layer 的重复使用不破坏这个估计，因为此前在该原 fiber 最多揭示 \(l-1\le G-1\) 个 images。

总共有至多 \(N'd^l\) 组起点和 layer word。每条 simple cycle 至少被其中一个闭合 walk 计到；对 \(l=2\) 使用两条不同 layer 的平行边，论证相同。所以短周期数 \(X_{\rm cyc}\) 满足
\[
 \mathbb EX_{\rm cyc}\le\sum_{l=2}^G2Nd^l=2NS.
\]
由 Markov，\(\Pr[X_{\rm cyc}>B]\le1/20\)。这一步没有假设原图没有平行 edge types。

## 4. 同 bucket 的保度 switching 总能进行

设当前短周期数至多 \(B\)，选其中一条边 \(e\)。每个 (原 edge type,layer) bucket 始终有恰 \(z\) 条边，且是该 layer perfect matching 的一个子集。

当前属于某条长度 \(\le G\) cycle 的边数至多 \(GB\)。从 \(e\) 的两个端点出发，半径 \(G\) 的球的总顶点数至多
\[
 2\sum_{j=0}^Gd^j\le2U.
\]
同一个 bucket 每个 copy 顶点最多关联一条边，所以因某端点在这些球中而不合格的 bucket 边至多 \(2U\)，特别至多 \(4U\)。由于
\[
 z\ge GB+4U+1,
\]
至少有一条 \(f\) 既不在短周期中，又与 \(e\) 所有端点距离大于 \(G\)。

把 \(e=AB\)、\(f=CD\)（\(A,C\) 在同一原左 fiber、\(B,D\) 在同一原右 fiber）改成 \(AD,CB\)。四端点互异。此交换保持每个 copy 在该 layer 的度数、bucket 大小、原 edge type 及投影。

没有新长度 \(\le G\) 周期：若新周期只用一条新边，其余旧路径连接原 \(e\) 与原 \(f\) 的某个端点对，距离至多 \(G-1\)，违背远离条件。若同时用两条新边，删去这两边后有两条旧路径。若它们跨 \(e,f\) 端点，则仍违背远离；否则其中一条连接 \(C,D\)，其长度至多 \(G-2\)，和旧 \(f\) 一起构成旧短周期，违背 \(f\) 的选择。

因此每次至少消去选中的那个 cycle，且不产生新短周期。当前短周期数永不增加，寻找 \(f\) 的论证可反复使用。总 switching 次数至多初始 \(B\)，最终无长度 \(2\) 到 \(G\) 的周期。二部性排除 loops，\(G\ge2\) 又排除平行边，所以输出 simple、balanced、\(d\)-regular、girth \(>G\)。

任何原 perfect 单标签赋值让同一原点的所有 copies 使用同一个标签；交换始终只连接原同一 edge type 的两端，所以这个赋值在每次 switching 后继续满足所有边。

## 5. 修复对所有列表的统一误差及成功概率

一次 switching 删除两条旧边、加入两条新边。对任何固定 copy lists，覆盖边数增加至多 \(2\)。所以至多 \(B\) 次交换给出对所有列表同时成立的确定上界
\[
 \mathrm{covered}_{\rm final}
 \le\mathrm{covered}_{\rm initial}+2B.
\]
由 \(z\ge8B/(\rho m_*)\)、\(t=Dz\ge z\)，
\[
 2B\le\rho M'/4.
\]
结合式 (5) 的初始同时事件，最终每个成本 \(\le gN'\) 列表族覆盖严格少于 \(3\rho M'/4<\rho M'\)。修复可依赖抽样图本身，因为前置事件已经同时量化全部列表；不需要对修复后的列表再作随机独立性假设。

Fisher–Yates 共有 \(L=dN(t-1)>0\) 个 uniform-integer draws。每次拒绝一次的概率小于 \(1/2\)（二的幂 bound 时为零），耗尽 \(R\) 次的概率小于 \(2^{-R}\le1/(2000L)\)。并界可耦合为所有 draws 的耗尽概率严格小于 \(1/2000\)。条件所有 draws 成功时，各次接受值仍独立均匀，因为其停止成功事件只依赖 bound 和拒绝次数，不偏置接受值。

于是对所有合法输入，FAIL 概率至多 \(1/20+1/2000<0.1\)。在 NO 条件下，再排除式 (5) 的坏同时事件，返回非 FAIL 且满足最终列表 NO 的概率严格大于
\[
 1-1/20-1/2000-1/1000>0.8.
\]
这里可以在理想 uniform permutations 上先证明，再与有限拒绝实现作耦合；不要求周期事件和列表事件独立。

## 6. 固定 G 的总位复杂度

域 \(Q\gamma\ge1\) 给
\[
 10^9g^8/\rho^3\le Q,
\]
特别 \(g\le Q\)、\(1/\rho\le Q\)。因此 \(d\le1000Q^2\lambda+1\) 是显式 Q 大小的多项式，不是对 binary 参数数值任意循环。显式投影表本来含 Q 项，故 Q 已被输入长度控制。原 D 也被显式 edge types 的数量控制，即使有平行约束也逐条列出。

固定 \(G\) 时，\(S,U,B,z,t,N',M'\) 的值均为显式输入长度的多项式，指数可依赖 \(G\)。所有 rational 比较、ceil 和参数计算可用位长多项式的整数运算。Fisher–Yates 及每 draw 至多 \(R\) 次、每次有限比特，给确定的最坏随机位和时间上界。

短 cycle 可按固定长度 \(2,\ldots,G\) 显式枚举，哪怕用 \(O((N')^G)\) 的直接实现仍为固定 G 的多项式。每次寻找同 bucket 的 \(f\) 可枚举 bucket、做有界距离搜索并枚举当前短 cycle；交换至多 B 次，仍为多项式。输出全部投影表也为多项式。没有隐藏无限拒绝采样，也没有把变化的 G 指数称为 uniform poly。

若 \(Q\gamma<1\)，任何非空全投影游戏的随机均匀单标签赋值满足边期望恰 \(1/Q>\gamma\)，所以该域确实没有 \(\operatorname{val}\le\gamma\) 的输入。

## 7. 条件 PCP 传递与状态

若外部 PCP 起点在先固定 \(g,\rho\) 后给 \(Q=\operatorname{poly}_\rho(g)\)，则 \(\lambda/\ell=O_\rho(1)\)，所以 \(d=O_\rho(g)\)。任意事先固定 G 可被同时要求，代价只在多项式的常数和指数内。perfect 完全保留，NO 的正确输出概率大于 \(0.8\)，FAIL 可按声明作为归约 YES 分支处理。排除随机多项式判定所用假设仍是 \(\mathrm{NP}\not\subseteq\mathrm{BPP}\)，不是直接 \(\mathrm{P}\ne\mathrm{NP}\)。

本文没有亲读或升级 PCP/repetition 起点，没有导入 arbitrary lift 的 soundness，也没有提供任何 UM compiler。一般复制的有限 cover 障碍与这里选择随机连接的同时列表事件没有矛盾。

本记录已完成 Exact-only 独立重构；没有发现 fatal objection。后续收到作者证明须另记实际全文读取与 hash，不改写本冻结文件。
