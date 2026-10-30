# 显式 XOS 的分数 NSW、几乎所有组质量与共享修复 LP 边界

下文 §F 原高/低比例解读有实质错误，已明确撤回并更正；A、B及C–D原精确结论保留。数学证明及实际独立重构、作者读后与最终正文审查的次序和范围见[审查记录](../../reviews/unrelated_machines/explicit_xos_fractional_nsw_and_normalized_robust_gap_boundary_review.md)。原 A–F 的算法为数学规格，未实现；新增 F2 的给定见证构造另有软件及单独审查。外审与全球新颖性未认证。正文对应冻结 Exact v5 `3160d7f7dc3265c7753ba558bb6cd21fe58fc5e2ea84562d2558ee852701154e`、作者 Proof v5 `2989351ca6ab45779fecb3c4a4ccefbae2044cdcce7ad3f3fab0d0e2ce55a1af`。

本页证明：一般单调次可加的分数 benchmark 匹配；任意有限显式非负二进制有理 XOS 的确定性无权 NSW；原归一化菜单的几乎所有组常数质量、同组 singleton REPAIR 的 LP promise decider，以及保留全部原 jobs 的普通 flat-UM 排程。后者只保证全矩阵 makespan 至多二和接近二的 selected-root 计数。

## 共用记号与有限位计算

实际 allocation 指原物品上的两两不交子集，允许余物不分配。写 \(v_i(j)=v_i(\{j\})\)。有限分数配置族的每行质量为一、每个原物品总边际至多一。正 benchmark 要求每个正质量配置的实际价值严格正，定义

\[
\mathcal B_v(y)=
\exp\left(\frac1n\sum_{i,S}y_{i,S}\ln v_i(S)\right)>0 .
\tag{0.1}
\]

重复子集可保留为不同条目；它们不产生新的原物品容量。所有概率、系数、目标和中间有理数均按二进制分子/分母存储，除法不表示按倒数数值展开。下文使用标准确定性有理 LP 和二分图匹配算法及精确有理算术；所需日志精度在此给出，不假定精确超越数比较。

**有限位引理：真最大乘积匹配。** 对每条正因子边 \(f_e=P_e/Q_e\)，设分子分母至多 \(2^L\)，匹配包含 \(n\) 条边。两个不同匹配乘积 \(A/B>C/D\) 的分子分母各至多 \(2^{nL}\)，故

\[
\ln(A/B)-\ln(C/D)
\ge\ln(1+2^{-2nL})\ge 2^{-2nL-1}=:G .
\tag{0.2}
\]

先删除零因子边并测试是否存在覆盖全部 agents 的匹配。若存在，将每边 \(\ln f_e\) 近似到绝对误差 \(G/(4n)\)，再对有理近似权求真最大权匹配。每个匹配总误差至多 \(G/4\)，不同真乘积的顺序严格保持，因而所得是真最大乘积匹配；相等乘积用固定确定性 tie rule。

日志近似亦有显式算法。对正有理 \(x=2^e z\)、\(1\le z<2\)，令 \(t=(z-1)/(z+1)\in[0,1/3)\)。截断

\[
\ln z=2\sum_{k\ge0}\frac{t^{2k+1}}{2k+1}
\]

的前 \(N\) 项，余项不超过 \(9^{-N}\)；用 \(t=1/3\) 同样近似 \(\ln2\)。总误差至多 \((|e|+1)9^{-N}\)，而 \(|e|\) 受 \(x\) 的分子分母位长控制。指定绝对误差 \(\alpha>0\) 只需在实际输入位长和 \(\log(1+1/\alpha)\) 上多项式次有理运算及多项式位长。于是 (0.2) 所需精度仅 \(O(nL+\log n)\) bits；矩形初始匹配、A 的匹配和最终 bundle-plus-singleton 匹配都适用。

## 精确 ID：UM-FRACTIONAL-BENCHMARK-REMATCHING-v1

- **Objects：** \(n\ge1\) agents，有限原物品集 \(U\)，指定的 \(n\) 个不同物品 \(H\subseteq U\)，残余 \(B=U\setminus H\)；二进制有理目标 \(V_i\ge0\)、\(c\ge1\)；有限显式有理正配置 benchmark \(y\)。
- **Domain：** \(v_i:2^U\to\mathbb Q_{\ge0}\) 有限、单调、次可加且 \(v_i(\varnothing)=0\)。这部分不要求 XOS。可用 value queries；复杂度计入实际输入及被查询有理值的位长。
- **Quantifiers：** 令 \(A=\{i:V_i>0\}\)，要求 \(i\notin A\Rightarrow v_i(B)=0\)。对 \(A\) 在 \(B\) 上的**每一个可行分数配置族** \(z\)，假设
  \[
  \sum_{i\in A,T\subseteq B}z_{i,T}\frac{v_i(T)}{V_i}\le cn .
  \tag{A.1}
  \]
  较强上界 \(c|A|\) 也足够；\(A=\varnothing\) 时条件空。
- **Dependencies：** 本页的分数运输/Jensen/匹配证明与有限位引理。应用于下一 ID 时，(A.1) 由其固定 lift 后端以 \(c=2\) 对全部分数族提供；A 的语义定理自身不依赖该后端。
- **Limitations：** 不声称验证全局假设 (A.1)、求出 \(V_i\) 或求解一般指数规模 log-CONFIG；不能把 (A.1) 偷换成仅对 integral allocations 的上界。

**Exact。** 对每个满足上述条件、行和一且原物品列至多一的正 \(y\)，存在双射 \(\pi:[n]\to H\) 使

\[
\left(\prod_i[V_i+v_i(\pi(i))]\right)^{1/n}
\ge\frac{\mathcal B_v(y)}{c+1}.
\tag{A.2}
\]

所有左因子均正。确定性算法只用给定 \(V_i\) 和 \(H\) 上 \(n^2\) 个 singleton 值，以总 bit-polynomial 时间返回真最大乘积匹配，故无需表示一般无理 benchmark。对任何有理 \(\epsilon>0\) 放宽为额外 \(1+\epsilon\) 损失也成立。

**证明。** 写 \(a_{ih}=v_i(h)\)、\(f_{ih}=V_i+a_{ih}\)。每个正条目 \((i,S)\) 若 \(S\cap H\ne\varnothing\)，将其质量送往其中 singleton 最大的 \(h\)。每行和、每列和至多一，因为所选 \(h\) 是该原配置内的真实物品。行缺口恰是 \(H\)-empty 配置的质量；若 \(i\notin A\)，这些配置位于 \(B\)，不可能有正价值，故只有 \(A\) 的行有缺口。将总量相同的行缺口和列缺口以非负运输填满，必要时拆分配置质量，得

\[
\sum_h\widetilde y_{i,S,h}=y_{i,S},\qquad
q_{ih}=\sum_S\widetilde y_{i,S,h},\qquad
\sum_hq_{ih}=\sum_iq_{ih}=1.
\tag{A.3}
\]

所有用到的 \(f_{ih}>0\)：\(A\) 内由 \(V_i>0\)；\(A\) 外若代表 singleton 为零，则次可加性及 \(v_i(B)=0\) 会推出 \(v_i(S)=0\)，矛盾。

对耦合条目设 \(T=S\cap B\)、\(k=|S\cap H|\)。若 \(i\in A\)，由代表的最大性及次可加性，

\[
\frac{v_i(S)}{f_{ih}}
\le\frac{v_i(T)}{V_i}+k.
\]

\(k=0\) 时只用 \(f_{ih}\ge V_i\)；\(i\notin A\) 时 \(k>0\)，ratio 至多 \(k\)。将 \(A\) 的 \(y\) 投影到 \(B\)，仍是行和一、列至多一的分数族，故残余项总和由 (A.1) 控为 \(cn\)；同时

\[
\sum_{i,S}y_{i,S}|S\cap H|\le |H|=n.
\]

因而总耦合质量为 \(n\) 的正 ratios 满足

\[
\sum_{i,S,h}\widetilde y_{i,S,h}\frac{v_i(S)}{f_{ih}}
\le(c+1)n.
\]

对 \(\ln\) 作 Jensen，

\[
\sum_{i,S}y_{i,S}\ln v_i(S)
\le\sum_{i,h}q_{ih}\ln f_{ih}+n\ln(c+1).
\tag{A.4}
\]

正支撑图满足 Hall：任意行集 \(I\) 的 \(|I|\) 质量只能流向总列容量 \(|N(I)|\)。取正边 perfect matching，减去其最小正条目并对非零余量重标度，逐次消去至少一条正边，得到有限 permutation 分解。至少一个 permutation 的 log product 不小于 \(\sum q\ln f\)，给出 (A.2)。有限位引理计算真最大值即可。空 \(A\)、空 \(B\)、零 singleton、零 \(V_i\) 和重复配置均已包含；没有在零因子上取日志。

## 精确 ID：UM-EXPLICIT-XOS-DETERMINISTIC-FRACTIONAL-NSW-v1

- **Objects：** \(n\ge1\)，显式 \(m\ge0\) 个原物品，非空有限 indexed clause lists，
  \[
  v_i(T)=\max_s\sum_{j\in T}p_{i,s,j},\qquad
  p_{i,s,j}\in\mathbb Q_{\ge0}.
  \tag{B.0}
  \]
- **Domain：** 所有系数均明确以二进制给出；可有零、重复 indexed clauses、零总量 clauses 和未用物品。无全局归一化、公共数值网格、最小正系数或 utility floor 假设；不接受只有 oracle 的输入表示。value、singleton、attaining-clause 均由有限原表直接有理求值。
- **Quantifiers：** 单个确定性输出，对同一原始对象的**每个**有限正分数 benchmark \(y\) 同时成立；算法不以 \(y\) 或实际最优 allocation 为输入。目标仅为无权几何平均。
- **Dependencies：** 上一 ID 的语义匹配接口、标准有理 LP/匹配；DLRV v1 的初始 singleton 匹配、分裂、按满足组迭代和任意比较匹配 rematching 框架。全分数残余 solver、确定性显式 XOS 福利舍入、下述加性逆矩和局部网格 DP 均在页内另证，不把源文的 actual-integral-OPT theorem 当作分数 theorem。
- **Limitations：** 无 weighted-agent、一般 subadditive 后端或 oracle-only XOS 后端结论；算法未实现，无软件执行或测试审计认证。

**Exact。** 总算法输出原物品上的真实不交 allocation，满足

\[
\mathsf{NSW}_v\ge\frac{\mathcal B_v(y)}{1125000}
\quad\text{对每个上述正 }y.
\tag{B.1}
\]

运行时间关于全部显式输入位长及 agent/item/clause 数为多项式，不按原分母、正系数倒数、目标倒数或概率倒数数值展开。以下给出构造及完整承重证明。

### B1. 正 singleton 匹配与所有退化分支

非负 XOS 为单调次可加，且任意正值集合含正 singleton。先在所有原物品 \(U\) 上找覆盖全部 agents 的正 singleton 匹配；若没有，由 Hall 存在 \(|N(I)|<|I|\)。正实际 allocation 会从 \(I\) 的不交正 bundles 各取一个不同正 singleton，矛盾；正分数 benchmark 也会使

\[
|I|\le\sum_{i\in I,S}y_{i,S}|S\cap N(I)|
\le |N(I)|,
\]

矛盾。此分支返回全部空 bundle，实际最优 NSW 为零且不存在所比较的正 benchmark；涵盖 \(m=0\)、\(n>m\)、全零及某 agent 全零。

否则用有限位引理求**全部 \(U\) 上真最大正 singleton product** 的匹配 \(\tau\)，设 \(H=\tau([n])\)、\(B=U\setminus H\)、\(A=\{i:v_i(B)>0\}\)。全 \(U\) 的真最优性用于 B6，不能只在后来固定的 \(H\) 上最优。若 \(A=\varnothing\)，置所有 \(V_i=0\)，省略残余 solver、分裂和 mask，取 \(T_i=\varnothing\) 并直接最终匹配；空 \(B\) 在其中。

### B2. 归一化的固定 lift 与纯有理残余 solver

令 \(a=|A|>0\)，\(W_i=v_i(B)>0\)，并只在算法内部定义

\[
\widehat p_{i,s,j}=p_{i,s,j}/W_i,\quad
\widehat v_i(T)=v_i(T)/W_i\quad(j\in B).
\]

每个归一化 residual clause 总量至多一，至少一个恰为一。有限次有理和、比较、除法仅产生多项式位长，不按 \(1/W_i\) 展开。固定 polytope \(P\) 为

\[
\lambda_{i,s}\ge0,\quad\sum_s\lambda_{i,s}=1,\quad
0\le z_{i,s,j}\le\lambda_{i,s},\quad
\sum_{i\in A,s}z_{i,s,j}\le1\quad(j\in B).
\tag{B.2}
\]

其 utility image \(R\) 为 \(u_i=\sum_{s,j}\widehat p_{i,s,j}z_{i,s,j}\)，满足 \(0\le u_i\le1\)。为每个 agent 选 total-one clause、令其 \(\lambda=1,z_j=1/a\)，得到 \(b_i=1/a\) 的 lift，物品列和一。

任意可行分数 residual 配置族都能 lift 到 \(P\)，且 utility 恰为实际归一化期望：为每个配置选实际 attaining clause，\(\lambda\) 记录分给该 clause 的质量，\(z\) 记录其中包含物品的质量。反向对 rational lift，条件于 \(\lambda>0\) 将 \(z_j/\lambda\) 排序；写 \(b_B=|B|\)，若 \(q_1\ge\cdots\ge q_{b_B}\)、\(q_0=1,q_{b_B+1}=0\)，给前 \(k\) 个物品的 nested subset 质量 \(q_k-q_{k+1}\)，精确实现 marginals。每 clause 至多 \(|B|+1\) 个 subsets。乘回 \(\lambda\) 后列不变，assigned-clause 期望等于 utility，actual XOS 期望至少该 utility。

置

\[
\ell=\frac1{4a},\qquad h=\frac{\ell^2}{2}=\frac1{32a^2},
\qquad R'=b/4+3R/4.
\]

从 \(x=b\) 的 lift 开始，反复在同一 \(P\) 上求

\[
M=\max_{w\in R}\sum_iw_i/x_i
\tag{B.3}
\]

的 basic optimal vertex。若 \(M\le2a\) 停；否则令 \(y=b/4+3w/4\)，以全 lift 的同一凸组合更新 \(x\leftarrow(1-h)x+hy\)。\(R'\subseteq R\)，始终 \(x_i\in[\ell,1]\)。

只作分析而不数值计算 \(F(x)=\sum_i\ln x_i\)。令 \(D=y-x\)；更新条件给出

\[
\nabla F(x)\cdot D
=\tfrac14\sum_i b_i/x_i+\tfrac34M-a>a/2.
\]

线段上 Hessian 对角项为 \(-1/x_i^2\)，且 \(\sum_iD_i^2\le a\)，故

\[
F(x+hD)-F(x)
\ge h\nabla F(x)\cdot D-\frac{h^2a}{2\ell^2}
>\frac1{128a}.
\tag{B.4}
\]

起点 \(F(b)=-a\ln a\)、全过程 \(F\le0\)，\(a\ge2\) 时更新数小于 \(128a^2\ln a<128a^3\)；\(a=1\) 初始 \(M\le1\) 立即停。

**固定顶点位长是关键。** \(P\) 的矩阵只含 \(0,\pm1\)，RHS 只含 \(0,1\)，与当前 objective 无关。设变量数 \(D_P\)，每个顶点由满秩 active 方程确定；Cramer/Hadamard 给出各坐标及其共同 determinant 分母 \(O(D_P\log(D_P+2))\) 位界。可在最优 face 上逐坐标作确定性 lex 优化取原 \(P\) 的顶点，仍只有多项式次 LP。若当前 lift 分母为 \(D_t\)，下一步可用 \(D_t\) 乘一个这种固定界的 vertex 分母和 \(a,4,32a^2\) 的多项式位长因子作为分母；因此位长每次只**加**多项式量。多项式次更新后 lift、由固定 \(\widehat p\) 计算的 \(x\)、其倒数和每次 LP objective 都是多项式位长，不发生 objective-dependent 输出界的递归放大。

由最终 lift 的 threshold 配置重新评价 actual 值，令

\[
\widehat V_i=\sum_Tx_{i,T}\widehat v_i(T)\ge x_i\ge1/(4a),
\quad V_i=W_i\widehat V_i\in(0,W_i],
\quad V_i=0\ (i\notin A).
\tag{B.5}
\]

配置行和一、列至多一，support 和有理位长均多项式。对**任意** feasible fractional residual family，其实际 normalized utility \(u^z\in R\)，故

\[
\sum_{i\in A,T}z_{i,T}\frac{v_i(T)}{V_i}
=\sum_i\frac{u_i^z}{\widehat V_i}
\le\sum_i\frac{u_i^z}{x_i}\le M\le2a.
\tag{B.6}
\]

这给 A 所需 \(c=2\) 的全分数界，不仅是 integral 或本次恢复族的界。

### B3. 支持集合内的确定性福利舍入与精确 CDF

给任意有限 rational feasible 配置族和正实际期望 \(U_i\)，当前 agents 数为 \(q\)。对每个正概率配置固定实际 attaining clause，先在分析中让各 agent 独立抽其配置，并在其中物品上出价 \(p_{i,s,j}/U_i\)，其他出价零。对物品 \(j\) 和 \(t>0\)，记 \(p_i(t)=\Pr(b_{ij}\ge t)\)、\(s(t)=\sum_i p_i(t)\le1\)，最后一步由配置列容量。跨 agents 独立给出

\[
\Pr(\max_i b_{ij}\ge t)
=1-\prod_i(1-p_i(t))
\ge s(t)-s(t)^2/2\ge s(t)/2.
\]

对有限 bid levels 积分/求和，再加总物品，因 attaining clause 在每个配置上总出价恰为 \(v_i(T)/U_i\)，得到

\[
\mathbb E\sum_j\max_i b_{ij}\ge q/2.
\tag{B.7}
\]

逐 agent 固定配置、枚举其所有正概率 choices 并选 proxy 条件期望最大者，父期望是这些子期望的概率平均，因此不降。精确计算是有限 rational CDF：对某物品全部可能 bid levels \(0=t_0<\cdots<t_K\)，

\[
\mathbb E\max_i b_{ij}
=\sum_{\ell=1}^K(t_\ell-t_{\ell-1})
\left[1-\prod_i\Pr(b_{ij}<t_\ell)\right].
\tag{B.8}
\]

已固定 agents 的 CDF 为 \(0/1\)，未固定者为配置概率和；严格 \(<t_\ell\) 正确处理等价 bids。仅有多项式个 levels、choices 和 rational sums/products；直接重算的分母位长由多项式个输入分母位长之和控制。无需枚举联合抽样。全固定后将 positive maximum bid 的物品交给一个最大 bidder，零 bid 物品可不分配。每个实际 bundle 是其所选原 support 配置的子集，original clause lower-bounds actual XOS，故输出不交 bundles 且

\[
\sum_i v_i(S_i)/U_i\ge q/2.
\tag{B.9}
\]

若 \(q=0\) 直接返回。不同物品 bids 的相关性不影响逐物品期望相加。此程序不观察任何 labels；下文保守取 \(d=5/2\)，因为 \(q/2\ge q/d\)。

### B4. 分裂后质量不放大、先固定全部候选

令 \(\nu_i=\max_{j\in B}v_i(j)\)（空集取零）、\(A''=\{i\in A:V_i\ge6\nu_i\}\)。\(i\in A\) 时 \(\nu_i>0\)。对 \(A''\) 的 recovered 配置族，丢弃价值 \(<V_i/3\) 的配置。每个保留的 \(T\) 取 attaining clause，令 \(k=\lfloor3v_i(T)/V_i\rfloor\ge1\)。其 weights 各至多 \(\nu_i\)，总量至少 \(kV_i/3\)。贪心取 \(k-1\) 个不交部分，每部分 clause weight 在

\[
\alpha_i=V_i/3-\nu_i\ge V_i/6
\quad\text{与}\quad V_i/3
\]

之间：累加至首次达到 \(\alpha_i\)，最后一个物品最多增 \(\nu_i\)。每步取走至多 \(V_i/3\)，故有足够剩余；最后部分的 clause weight 至少 \(V_i/3\)。若某部分 actual XOS 值超过 \(V_i\)，逐项删除至不超过；次可加性保证单次损失至多 \(\nu_i\)，首次跨过后仍 \(>V_i-\nu_i\ge\alpha_i\)。最终各部分均满足

\[
V_i/3-\nu_i\le v_i(T')\le V_i.
\tag{B.10}
\]

部分仍是原 \(T\) 的不交子集；可舍掉删除的物品。由 \(v_i(T)\le|T|\nu_i\)，

\[
k\le3|T|\nu_i/V_i\le|T|/2,
\]

没有 tiny coefficient 或 \(1/V_i\) 数值展开。

每部分继承原配置概率。被丢弃的配置贡献至多 \(V_i/3\)，高值部分原期望至少 \(2V_i/3\)。利用 \(\lfloor r\rfloor\ge r/2\ (r\ge1)\)，总继承质量

\[
M_i=\sum_{T\ \mathrm{high}}x_{i,T}
\left\lfloor\frac{3v_i(T)}{V_i}\right\rfloor
\ge\frac3{2V_i}\sum_{T\ \mathrm{high}}x_{i,T}v_i(T)\ge1.
\tag{B.11}
\]

同一原配置的每个物品至多出现在一个部分，继承后其 marginal 不增；再逐行除以 \(M_i\ge1\)，仍不增。所得 \(x'\) 行和一、原物品列至多一，support、系数位长多项式，实际期望 \(V'_i\in[V_i/6,V_i]\)。

置 \(\delta_{\mathrm m}=1/(7d)=2/35\)。对当前 agents 调 B3、用 \(U_i=V'_i\)，所得每个 normalized value 在 \([0,6]\)，总和至少 \(q/d\)。若达到 \(v_i(S_i)\ge\delta_{\mathrm m} V'_i\) 者不足 \(\delta_{\mathrm m} q\)，则总和 \(<6\delta_{\mathrm m} q+\delta_{\mathrm m} q=q/d\)，矛盾。固定这些满足者的实际 \(S_i\) 和轮次 \(t_i\)，将其移出后继续；每轮至少一人，至多 \(L=a_0=|A''|\) 轮。同轮候选两两不交，且

\[
\delta_{\mathrm m} V_i/6\le v_i(S_i)\le V_i.
\tag{B.12}
\]

所有候选、轮次和 attaining clauses 都在任何 label/mask 前确定。按退出轮次排序，rank \(k\) 在退出时仍有至少 \(a_0-k+1\) agents；每轮 population 下降至少 \(\delta_{\mathrm m}\) 比例，故

\[
p_{t_i}:=\delta_{\mathrm m}(1-\delta_{\mathrm m})^{t_i-1}
\ge\delta_{\mathrm m}(a_0-k+1)/a_0.
\tag{B.13}
\]

令每个原残余物品独立具有形式 label \(r_j\in\{0,\ldots,L\}\)，

\[
\Pr(r_j=t)=\delta_{\mathrm m}(1-\delta_{\mathrm m})^{t-1}\ (1\le t\le L),
\qquad \Pr(r_j=0)=(1-\delta_{\mathrm m})^L.
\tag{B.14}
\]

有限分布总质量恰为一；每概率正，位长 \(O(L)\)。这只定义分析和去随机化接口，算法不抽随机 bits。若 \(A''=\varnothing\)，省略 B4–B5，置全部 \(T_i=\varnothing\)。

### B5. 候选局部相对网格、内嵌逆矩与确定性 mask

现设 \(a_0>0\)，故 \(m_B=|B|\ge1\)。每个已固定候选 \(S_i\) 选原 attaining clause，其原系数 \(w_{i,j}\) 满足总和 \(v_i(S_i)\in[\delta_{\mathrm m} V_i/6,V_i]\)、各项 \(\le\nu_i\)。只对这些候选的辅助相对系数定义

\[
Q=210m_B,\qquad
a_{i,j}=\frac1Q\left\lfloor\frac{Qw_{i,j}}{V_i}\right\rfloor,
\qquad\beta_i=\nu_i/V_i>0.
\tag{B.15}
\]

逐项损失 \(<1/Q\)，总损失 \(<m_B/Q=1/210=\delta_{\mathrm m}/12\)，于是

\[
0\le a_{i,j}\le\beta_i,\qquad
\delta_{\mathrm m}/12\le\sum_{j\in S_i}a_{i,j}\le1.
\tag{B.16}
\]

\(h_{i,j}=Qa_{i,j}\) 为非负整数、行总量至多 \(Q\)。\(Q\) 关于显式物品数多项式，而与原分母、utility scale 无关；此 floor 不替换原 valuation、state、item 或 processing time。

**内嵌引理：独立 Bernoulli 的 shifted inverse moment。** 若 \(\beta>0\)、\(a_j\in[0,\beta]\)、独立 Bernoulli \(X_j\) 的 \(M=\sum_j a_j\Pr(X_j=1)>0\)，则

\[
\mathbb E\ln\frac1{\beta+\sum_j a_jX_j}\le\ln\frac1M.
\tag{B.17}
\]

证明：令 \(p_j=\Pr(X_j=1)\)、\(d_j=a_j/\beta\in[0,1]\)、\(Y=\sum_jd_jX_j\)、\(\mu=M/\beta\)。对 \(0<t<1\)，\(d\mapsto t^d\) 的凸性弦界为 \(t^d\le1-d+dt\)。独立性给

\[
\mathbb E t^Y
\le\prod_j[1-p_jd_j(1-t)]\le e^{-\mu(1-t)}.
\]

有限期望与 \(1/(1+Y)=\int_0^1t^Ydt\) 交换，得到

\[
\mathbb E\frac1{\beta+\sum a_jX_j}
\le\frac{1-e^{-\mu}}M<\frac1M;
\]

再对正 inverse variable 用 \(\ln\) 的 Jensen 即得。此引理只用于加性 weights 和单个候选内独立原物品，不声称 correlated-mask 或一般 subadditive concentration；不同 agents 的 masks 相关不影响逐行期望相加。

记

\[
A_i(r)=\sum_{j\in S_i}a_{i,j}\mathbf1[r_j=t_i],\qquad
\Phi(r)=\sum_{i\in A''}-\ln(\beta_i+A_i(r)).
\tag{B.18}
\]

**内嵌引理：有限网格 label DP，势函数总误差一。** 预计算 \(f_i(k)=-\ln(\beta_i+k/Q)\)、\(0\le k\le Q\) 的有理近似，绝对误差

\[
\alpha=\frac1{2a_0m_B}.
\]

共用日志算法保证位复杂度多项式；小 \(\beta_i\) 只增加二进制描述/精度成本，不增加 \(1/\beta_i\) 个状态。

逐原物品固定一个正概率 label。当前 prefix 对 row \(i\) 给定整数 offset；未定候选物品的剩余 weight 分布由

\[
\prod_{j\ \mathrm{undecided},\,j\in S_i}
[(1-p_{t_i})+p_{t_i}z^{h_{i,j}}]
\tag{B.19}
\]

的系数给出，次数至多 \(Q\)，故用 \(Q+1\) 格卷积 DP 精确计算。对概率 \(P_j/D_j\)，若当前分母为 \(D\)、整数分子 \(N_k\)，更新为

\[
N'_k=(D_j-P_j)N_k+P_jN_{k-h_{i,j}},\qquad D'=DD_j.
\tag{B.20}
\]

分子非负且和为分母，位长由实际概率分母位长之和控制；零 weight 合并同格、概率零/一也合法。对下一物品每个正概率 candidate label，加入其实际 offset 后重算剩余 DP，求有理近似条件势；每行概率和一，故 total score 误差至多 \(a_0\alpha=1/(2m_B)\)。取近似最小者，其真子势至多真最小子势加 \(2a_0\alpha=1/m_B\)；父势是真子势的概率平均。因此全部 \(m_B\) 步后

\[
\Phi(r)\le\mathbb E\Phi+1.
\tag{B.21}
\]

prefix 后未定物品仍按原分布独立，不需除以极小 prefix 概率。即使为每物品、每个 \(L+1\) label、每 agent 全部重算，只有 \(O(m_B(L+1)a_0m_BQ)\) 次卷积运算；DP 系数和日志表均 polynomial bit length。\(L\le n\)、\(Q=210m_B\)，故为 total-bit-polynomial 确定性程序，无精确超越比较和随机 bits。

返回 \(T_i=\{j\in S_i:r_j=t_i\}\)，对所有 \(i\notin A''\) 一律置 \(T_i=\varnothing\)（包括 \(A''\ne\varnothing\) 的情形）。若两个 agents 共用一物品，其唯一 label 会使其轮次相同，但同轮候选不交，矛盾，故所有 \(T_i\) 全局不交。原 attaining clause 未改，且 \(w_{i,j}\ge V_ia_{i,j}\)，所以

\[
v_i(T_i)/V_i\ge A_i(r),\qquad v_i(T_i)\le V_i.
\tag{B.22}
\]

由 (B.13)、(B.16)，rank \(k\) 的辅助均值

\[
M_i=p_{t_i}\sum_j a_{i,j}
\ge\frac{\delta_{\mathrm m}^2(a_0-k+1)}{12a_0}>0.
\]

令 \(a=a_0\)，(B.17) 逐行相加及 \(\ln(a!)\ge a\ln a-a\) 给出

\[
\mathbb E\Phi
\le a\ln(12/\delta_{\mathrm m}^2)+a\ln a-\ln(a!)
\le a[\ln(12/\delta_{\mathrm m}^2)+1].
\]

包括 (B.21) 的全部误差后，

\[
\begin{aligned}
\left(\prod_{i\in A''}\frac{V_i}{\nu_i+v_i(T_i)}\right)^{1/a}
&\le\left(\prod_i\frac1{\beta_i+A_i(r)}\right)^{1/a}\\
&\le12e^{1+1/a}/\delta_{\mathrm m}^2
\le12e^2/\delta_{\mathrm m}^2<200/\delta_{\mathrm m}^2\\
&=9800d^2<10000d^2.
\end{aligned}
\tag{B.23}
\]

严格数值余量已有 \(e<3\Rightarrow12e^2<108<200\)，不依赖随机成功事件、未付精度损失或旧 generic-SA 数值尾界。

### B6. 任意比较 \(\pi\) 的 rematching，包括 cycles 和零分支

**Rematching 引理。** 写 singleton \(a_{ih}=v_i(h)\)，\(\tau\) 是全 \(U\) 上正乘积真最大匹配，\(H=\tau([n])\)、\(\nu_i=\max_{j\in B}v_i(j)\)。对任意非负 \(W_i\) 及任意双射 \(\pi:[n]\to H\)，存在双射 \(\rho\) 使

\[
\prod_i\max\{W_i,a_{i\rho(i)}\}
\ge\prod_i\max\{W_i,a_{i\pi(i)},\nu_i\}.
\tag{B.24}
\]

若右 product 为零，\(\rho=\tau\) 的左 product 正，立即成立。否则令

\[
E=\{i:W_i<\max(a_{i\pi(i)},\nu_i)\},\qquad
N=\{i\in E:\nu_i>a_{i\pi(i)}\}.
\]

在 \(E\) 上保留 successor \(i\to\tau^{-1}(\pi(i))\) 且终点仍在 \(E\) 的边。入/出度至多一。令 \(E_\tau\) 为可沿 forward path 到达 \(N\) 者（含 \(N\)），\(E_\pi=E\setminus E_\tau\)。分别给前者 \(\tau\)-item、后者 \(\pi\)-item。若 \(\pi(i)=\tau(k)\)、\(i\in E_\pi,k\in E_\tau\)，则 \(i\to k\) 使 \(i\) 也能到 \(N\)，矛盾，所以可任意补齐 \(E\) 外的双射。

在 \(E_\tau\) 图中删除**每个 \(N\) 顶点**的 outgoing edge。所有余下组件是不交路径，恰止于一个 \(N\)：无 \(N\) 的 cycle 不可能到达 \(N\)，而原 cycle 即使含多个 \(N\) 也被此删除切开。对路径 \(P=(i_1,\ldots,i_r=s)\)、\(s\in N\)，让非终点 agents 改用 \(\pi(i_\ell)=\tau(i_{\ell+1})\)，终点改用某原残余 item attaining \(\nu_s>0\)，其他 agents 保持 \(\tau\)。这是全 \(U\) 上合法正 matching，故

\[
\prod_{i\in P}a_{i\tau(i)}
\ge\nu_s\prod_{i\in P\setminus\{s\}}a_{i\pi(i)}.
\tag{B.25}
\]

各路径分开作反事实比较，再相乘；不同终点可有相同 residual maximizer，因为未同时分配它们。于是 \(E_\tau\) 上得到全部 \(N\) 的 \(\nu\) 和其余的 \(\pi\) 因子，\(E_\pi\) 用 \(\pi\)，\(E\) 外用 \(W_i>0\)，即 (B.24)。这也处理零 \(\pi\)-singletons、零 \(W\)、self-loop 和空 \(B\)；补齐后的某零 singleton 由 \(W_i>0\) 保护，无需在其上取日志。

现在令 \(b_i=v_i(T_i)\)。在 \(H\) 上用原表 factors \(v_i(T_i\cup\{h\})\) 求真最大乘积 \(\sigma\)。其正 perfect matching 存在，因为 \(\tau\) 的每个 singleton 正。最终实际 bundles 不交，且对每个比较 \(\pi\)，由 (B.24)、单调性及最大性，

\[
\prod_i v_i(T_i\cup\{\sigma(i)\})
\ge\prod_i\max\{b_i,a_{i\pi(i)},\nu_i\}.
\tag{B.26}
\]

若比较 product \(\prod_i(V_i+a_{i\pi(i)})=0\)，保证空泛但实际输出仍正。否则置 \(D_i=b_i+\nu_i+a_{i\pi(i)}>0\)。在 \(A''\) 内 \(0<b_i+\nu_i\le2V_i\)，所以

\[
\frac{V_i+a_{i\pi(i)}}{D_i}
\le\frac{2V_i}{b_i+\nu_i}.
\]

\(A\setminus A''\) 内 \(b_i=0,V_i<6\nu_i\)，ratio 至多六；\(A\) 外 \(V_i=b_i=\nu_i=0\)，正比较迫使 singleton 正，ratio 为一。由 (B.23)，

\[
\prod_i\frac{V_i+a_{i\pi(i)}}{D_i}
\le(20000d^2)^{|A''|}6^{n-|A''|}
\le(20000d^2)^n.
\]

\(A''=\varnothing\) 时直接用 outside ratios，不取空集合的 geometric mean。又 \(\max\{b_i,a_{i\pi(i)},\nu_i\}\ge D_i/3\)，故

\[
\mathsf{NSW}_v\ge\frac1{60000d^2}
\left(\prod_i[V_i+v_i(\pi(i))]\right)^{1/n}.
\tag{B.27}
\]

将 B2 的全分数 bound (B.6) 代入 A 的 \(c=2\)，对任意正 \(y\) 得某比较 \(\pi\) 的 target GM 至少 \(\mathcal B_v(y)/3\)。算法不需该 \(\pi\) 或 \(y\)。于是

\[
60000\cdot3\cdot(5/2)^2=1125000
\]

给出 (B.1)。matching 的日志精度已由共用有限位引理完整支付，sum-to-max 的因子三也明确保留。所有 solver、threshold support、split、至多 \(n\) 轮 CDF、局部 \(Q=210m_B\) DP 和最终有理因子匹配都是上述 bit-polynomial 子程序的多项式组合；没有按输入的原始数值网格或极小量倒数展开。

## 精确 ID：UM-NORMALIZED-MENU-ALMOST-ALL-AND-REPAIR-LP-BARRIER-v1

- **Objects：** 同一 \(n\ge1\) 个原 menu groups、\(m\ge1\) 个原 resources、非空有限 indexed states，原系数满足 \(p_{g,s,u}\in\mathbb Q_{\ge0}\)、\(\sum_u p_{g,s,u}=1\)，实际质量为 \(v_g(T)=\max_s\sum_{u\in T}p_{g,s,u}\)。每个输出从一个原 state 和全局不交的原资源子集读取质量。包括下述同组共享 singleton REPAIR 及这些对象的完整 ordinary flat-UM 矩阵。
- **Domain：** 原表明确二进制有理、每 clause 总量一；允许零、unused resources、重复 indexed states。本文所有 cardinality 比例使用同一个原 group 数 \(n\)，不改为 machines/jobs/states/auxiliary agents 数。
- **Quantifiers：** 每个 feasible unit-FSLP 对象有确定性 actual output；对每个固定 rational \(0<\eta<1\) 有下列常数计数保证。REPAIR decider 使用固定 \(0\le a_{\rm rep}<\gamma\le1\)、\(0<\eta<\gamma-a_{\rm rep}\)、\(D\le a_{\rm rep}n\) 及显式小阈值 \(0\le\delta_{\mathrm q}\le c_\eta\)。\(\delta_{\mathrm q}\) 是菜单/源质量阈值，与 B 的 mask 概率 \(\delta_{\mathrm m}=2/35\) 不同。
- **Dependencies：** 前两 ID，正 support 的原 unit-FSLP，普通矩阵的直接 job-by-job 构造；不调用源论文仅相对 integral OPT 的近似定理来推 LP infeasibility。
- **Limitations：** 不保证所有组常数 minimum quality，不给全部原 machines 的 \(2-\epsilon\) makespan，不是 general UM solver、source hardness、其他 dummy/SC bridge 或 universal near-two barrier。NP 结论仅在另有指定 promise-gap Karp reduction 时条件成立；未声称该 reduction 存在。

### C. 原 unit-FSLP、benchmark 一与几乎所有组

原始 utilities 均在 \([0,1]\)。定义 \(P_{g,s}=\{u:p_{g,s,u}>0\}\)，显式 unit-FSLP 是

\[
\lambda_{g,s}\ge0,\quad\sum_s\lambda_{g,s}=1,\qquad
\sum_{g,s:u\in P_{g,s}}\lambda_{g,s}\le1\quad(u\in U).
\tag{C.1}
\]

**Exact。** 若 (C.1) 可行，则有有限正分数 benchmark \(\mathcal B_v(y)=1\)，原 utility 的 unweighted log-CONFIG optimum 为零，item-equality 版本亦为零。确定性 bit-polynomial finder 输出原 indexed states 与真实不交 allocation，使

\[
\mathsf{NSW}_v\ge1/3000000>2^{-24}.
\tag{C.2}
\]

令 \(\rho=2^{24}\)。对每个固定 rational \(0<\eta<1\)，设

\[
K=\lceil1/\eta\rceil,\qquad q_\eta=\rho^{-K},\qquad
c_\eta=q_\eta/2=2^{-24K-1}.
\tag{C.3}
\]

同一个输出满足

\[
\#\{g:v_g(T_g)<q_\eta\}<\eta n,\qquad
\#\{g:v_g(T_g)\le c_\eta\}<\eta n.
\tag{C.4}
\]

故 FSLP 可行不可能同时满足“每个实际 allocation 至少 \(\gamma n\) 组质量 \(\le\delta_{\mathrm q}\)”且 \(\gamma>\eta,\ 0\le\delta_{\mathrm q}\le c_\eta\)。这不是所有正 constants \((\gamma,\delta_{\mathrm q})\) 的禁令。

**证明。** 每个原 state 在自己的正 support 上 clause 值一，actual XOS 至多一，所以 \(v_g(P_{g,s})=1\)。以可行 \(\lambda_{g,s}\) 为这些 supports 的配置质量，行和一，列约束正是 (C.1)，得正 benchmark 一。约束系数是 positive-support indicators，不是处理时间 weights，更不是零 incidence 指示。所有正 log terms \(\le0\)，该 witness 达零，因此 optimum 零。

对 item-equality，只需逐 item 补列缺口。当前列质量 \(c\le1\)，所有 rows 中不含该 item 的配置质量为 \(n-c\ge1-c\)。取其中 \(1-c\) 的质量（必要时拆一条）添该 item，保持行和及其他列不变；原值一由单调性和上界一继续为一。依次处理全部物品得有限 equality witness；未提供一般指数 log-CONFIG 的求解器。

FSLP witness 可给定或用显式有理 LP 找到；它的正 benchmark 保证 B 不走无 positive singleton matching 分支。B 实际给至少 \(1/1125000\)，故 (C.2) 的保守常数成立。若 \(k\ge\eta n\) 个输出值 \(<q_\eta\)，其余至多一，则

\[
\prod_gv_g(T_g)<q_\eta^k=\rho^{-Kk}\le\rho^{-n},
\]

与 (C.2) 的 NSW 严格 \(>\rho^{-1}\) 矛盾。\(k>0\) 保证严格号，无需 \(\eta n\) 整除；\(\le c_\eta\) 严格蕴含 \(<q_\eta\)，处理 equality boundary。fixed \(\eta\) 的阈值是 constants；variable \(\eta\) 的位长及阈值运算关于 \(K\) 和原输入多项式，不声称关于 \(\log(1/\eta)\) 多项式。若 FSLP 不可行，不因此断言某一般 UM 实例不可行。

最终原 state 始终在原 unfloored table 上重新取 attaining index。value 与 attaining-clause 直接遍历有限表；若需 demand，给价格 \(r_u\)，有

\[
\max_T[v_g(T)-\sum_{u\in T}r_u]
=\max_s\sum_u\max\{p_{g,s,u}-r_u,0\},
\]

选 maximizing state 的正 surplus items 即可。无 oracle 黑箱假设。残余 row normalization 与候选 local floor 只用于内部运算，所有原 state/resource/系数始终保持，绝不把 floor 后数值读为 actual quality 或物理 processing time。

### D. 同组共享 singleton REPAIR 的 promise LP test

给原 normalized 对象 \(Q\) 与整数 \(D\ge0\)。创建全局共享的 \(D\) 个不同资源 \(d_1,\ldots,d_D\)；向**每个相同原 group** 添加恰 \(D\) 个 indexed alternatives，第 \(\ell\) 个只有 \(d_\ell\) 上系数一，其余系数零/absent。保留所有旧 states、资源和系数，得 \(Q^+\)，group 数仍 \(n\)。其 utility 为

\[
v_g^+(T)=\max\{v_g(T\cap U),\ \max_\ell\mathbf1[d_\ell\in T]\}.
\tag{D.1}
\]

空 repair list 的第二项视为零。

**Exact 与证明。** 原 allocation 若至少 \(n-D\) 个 groups 质量一，保留它们，将余下至多 \(D\) 个 groups 各给不同 repair resource 和对应 singleton state，便在 \(Q^+\) 全体 unit；涵盖 \(D=0\) 和 \(D\ge n\)。反之任意 augmented allocation 去掉 repair items 后是原实际 allocation。若原每个 allocation 至少 \(\gamma n\) 组质量 \(\le\delta_{\mathrm q}\)，至多 \(D\) 组收到任何 repair item，故依 (D.1) augmented 仍至少 \(\gamma n-D\) 组质量 \(\le\delta_{\mathrm q}\)；没有资源多组复用或新增 agents。

固定 rational \(0\le a_{\rm rep}<\gamma\le1\)，选 fixed rational \(0<\eta<\gamma-a_{\rm rep}\)，固定 \(0\le\delta_{\mathrm q}\le c_\eta\)，并令 \(D\le a_{\rm rep}n\)。在以下 promise 下：

- YES：原 \(Q\) 有 allocation 使至少 \(n-D\) 组 quality one；
- NO：原每个 allocation 至少 \(\gamma n\) 组 quality \(\le\delta_{\mathrm q}\)。

以 \(Q^+\) 的显式 unit-FSLP 可行为 YES 判据，确定性 bit-polynomial 地分离两类。YES 的全体 unit allocation 中，每组 attaining total-one state 的全部 positive support 都在其 bundle 内，否则缺一个正系数便达不到一；取这些不交 supports 的 integral \(\lambda\) 是 LP witness。NO 若 augmented LP 可行，C 给少于 \(\eta n\) 组质量 \(\le c_\eta\)，而 D 的计数迫使至少

\[
\gamma n-D\ge(\gamma-a_{\rm rep})n>\eta n
\]

组质量 \(\le\delta_{\mathrm q}\le c_\eta\)，矛盾。LP 只有明确的 \(0/1\) incidence 约束，直接 rational feasibility 即可；不必运行 NSW finder 或数值判定未知 integral NSW optimum。\(D\le a_{\rm rep}n\) 时新增 \(nD\) states 的显式规模多项式，promise 外任一 LP 结果均可。

固定正 slack \(\gamma-a_{\rm rep}\) 是必要使用的条件；不得转成较大机器/变量数的比例。\(D=0\) 也给原 actual \(V=1\) versus 此 robust NO 的 decider。若某 NP-complete language Karp-reduces 到这个**明确常数及显式表示**的 promise gap，则组合得到 P=NP；本页没有构造或假定这样的 reduction 已存在。其他 shared-dummy 或 state-dummy SC 机制不在此条内。

### E. 每个原 selector 和 incidence job 的完整 ordinary schedule

对 \(Q\) 或 \(Q^+\) 构造普通 flat UM：每个 indexed state 一个不同 private root，每个列出的 resource 一个 resource machine；每 group 只有一个原 unit selector，可在该 group 所有 roots 上以一执行。每个 state-resource incidence 是不同的原 job，在自己的 root 上时间为原 \(p_{g,s,u}\)，在自己的 resource machine 上时间一，其他 endpoints 为 infinity。保留全部 positive incidences 及显式列出的零 incidences、所有未选 states 和 unused machines。

给 C 的输出 bundles \(Z_g\)，选原 attaining state \(s_g\)，记原 quality \(r_g=\sum_{u\in Z_g}p_{g,s_g,u}\)。selector 在 \(s_g\) 的 root 执行；仅将 \(s_g\) 对 allocated positive resources 的 incidence jobs 放到其原 resource machines；该 state 的其余 jobs 留原 root；每个未选 state 的全部 incidence jobs 留自己的 root。每个 selector/incidence identity 恰执行一次，零 job 以零 private time 留 root。

selected root load 为

\[
1+\sum_{u\notin Z_g}p_{g,s_g,u}=2-r_g.
\tag{E.1}
\]

unselected roots load 一；不交 bundles 使每 resource 至多执行一个 unit incidence，load 至多一。因此同一全部原矩阵的完整 actual makespan 至多二；selected root 超过 \(2-q_\eta\) 当且仅当 \(r_g<q_\eta\)，由 C 数量 \(<\eta n\)。没有得到所有 machines 的 makespan 至多 \(2-c_\eta\)。

若存在 actual unit allocation，同一完整构造所有 selected roots load 一，其他 machines 也至多一，故 makespan 一；至少一个原 selector 的任何 finite endpoint 都为一，给 ordinary OPT 至少一，因此 OPT 恰一。D 的 augmented unit-YES 包含所有旧 jobs 和新 repair-state jobs。

设原 indexed-state 数 \(S\)、原显式 incidence 数 \(I\)，机器数 \(S+m\)、jobs 数 \(n+I\)。REPAIR 增加 \(nD\) private roots、\(D\) resources、\(nD\) positive singleton incidence jobs 和 \(nD\) selector endpoints，原 selector identities 仍是同一 \(n\) 个；任何另行显式零 incidence 也计入并保留。稠密矩阵或完整 job assignment 的输出规模关于显式 augmented 输入多项式。内部 normalization/grid 从不替代这些 physical processing times。

### F. 必要数量界、主线参数域与未解义务

unit-FSLP 可行，若每个 allocation 至少 \(\gamma n\) 组质量 \(\le\delta_{\mathrm q}\)、\(0<\delta_{\mathrm q}<1\)，将其作用于 C 的输出，其他值至多一，得到

\[
-\ln\rho\le\ln\mathsf{NSW}_v
\le\gamma\ln\delta_{\mathrm q},
\qquad
\gamma\ln(1/\delta_{\mathrm q})\le\ln\rho.
\tag{F.1}
\]

\(\delta_{\mathrm q}=0,\gamma>0\) 已被正输出直接排除，不在日志式取零。禁区是 C–D 的显式小阈值及固定 fraction/slack，并非任意正 \((\gamma,\delta_{\mathrm q})\)。\(\gamma\) 可依赖选定目标 \(\delta_{\mathrm q}\)，对每个固定目标仍正；本页没有要求 \(\delta_{\mathrm q}\) 随 source size 趋零，故不能推出 \(\gamma\) 随 \(n\) 趋零，也不能推出辅助规模必须随 source size 增长而非仅依赖固定目标参数。

**与需求树主线的条件参数对照。** 设树目标值为 \(b\)、最优值为 \(b^*\)、\(0<\delta_{\mathrm q}<1\)。若某解码在阈值 \(x\ge\delta_{\mathrm q}\) 下从 \(b\ge x\) 抽出至少 \(xn\) 个已达 NO 质量门槛的变量束，而 NO 仅禁至少 \(\gamma n\) 个部分束，则直接取 \(x=\delta_{\mathrm q}\) 调用 NO 需 \(\gamma\le\delta_{\mathrm q}\)；一般取 \(x=\max\{\gamma,\delta_{\mathrm q}\}\) 仅得 \(b^*<\max\{\gamma,\delta_{\mathrm q}\}\)，不能省去 fraction 参数而写成 \(b^*<\delta_{\mathrm q}\)。这是条件解码的量词对照，不将未核验的旧 source/matching 条款当作 theorem 或本页依赖。

**2026-10-18 实质勘误：高组上限与低组下限必须取互补。** 旧 §F 从“本页 C–D 排除的却是”开始的两段误把这里的高质量组上限 \(\gamma_{\rm hi}\) 与 C–D 的低质量组下限 \(\gamma_{\rm lo}\) 当成同一比例；“不覆盖 \(\gamma\le\delta_{\mathrm q}\)”的结论撤回。旧作者 Proof、旧 Exact 与旧审查原件保持原字节；原来 C–D 的低质量定理和 (F.1) 本身不因此被反驳，新适用结论另有精确身份。

若 robust NO 对每个 allocation 要求
\[
\#\{g:r_g\ge\delta_{\mathrm q}\}<\gamma_{\rm hi}n,
\]
则其准确互补为
\[
\#\{g:r_g<\delta_{\mathrm q}\}>(1-\gamma_{\rm hi})n.
\]
因此应以低质量比例 \(1-\gamma_{\rm hi}\) 对照 C，不是以 \(\gamma_{\rm hi}\) 本身。尤其当 \(\delta_{\mathrm q}\le q_\eta\)、\(\gamma_{\rm hi}\le1-\eta\) 时，C.4 的同一输出已直接违反该 robust NO；等号也被严格计数覆盖。高端若用 \(>\delta_{\mathrm q}\)，低端须相应用 \(\le\delta_{\mathrm q}\)，不能无条件交换两种边界。

所以对于本页明确的 norm1 显式菜单，典型 \(\gamma_{\rm hi}\le\delta_{\mathrm q}\) 的充分小常数域恰被排除。这里仅修正集合互补及 C 的直接适用范围，不采用尚未在本页完成审查的门控构造或新算法。原 flat 全组 selector 仍不因此获得统一低于二负载。一般 UM、共享内部、多层或不保正 support LP 的源仍须独立解决，不能把这次范围纠错当作 UM-TARGET-v1 的正反面证明。

## F2. 部分激活菜单的福利计分与高质量组数地板

**ID / Version：`UM-NORMALIZED-MENU-PARTIAL-QUOTA-WELFARE-FLOOR-v1`。**
本节是标准 XOS 福利舍入在当前源合同上的直接推论，不是新的舍入机制或近二困难性。
它允许候选组数大于根的选择需求，补的是“部分激活”的共同计数，不是全组 max-min。
原 A–F 的 v5 冻结审查只覆盖其当时字节；本新增身份单独沿下方审查读取。

**Objects / Domain / Definitions。** 有 n≥1 个原 groups、有限显式资源 U；每组有非空有限 indexed states，
非负二进制有理 p_gsu 满足每个 state 的全 U 总量恰一。允许零项、重复 state、未用资源及整行零激活。
原质量仍为 f_g(B)=max_s Σ_{u∈B}p_gsu∈[0,1]，实际 B_g 跨组两两不交。
给二进制有理 0<q≤n，部分正支撑 LP 为

\[
\lambda_{gs}\ge0,\quad a_g:=\sum_s\lambda_{gs}\le1,\quad
\sum_g a_g=q,\quad
\sum_{g,s:p_{gsu}>0}\lambda_{gs}\le1\quad(u\in U). \tag{F2.1}
\]

正支撑列约束不是加权列负载，也不数零系数；所有原 state 和资源保留。

**Quantifiers / Exact Statement / Conclusion。** 给任意 (F2.1) 的显式有理可行 λ，
可确定性总位多项式输出原资源的不交 bundles 和每组的原 attaining state，使

\[
H:=\#\{g:f_g(B_g)\ge3/8\}>2q/5. \tag{F2.2}
\]

同一机制对任意给定有理 0<δ<1−1/e 给

\[
H_\delta\ge\frac{1-1/e-\delta}{1-\delta}\,q. \tag{F2.3}
\]

算法不用计算 e。q=0 可另返回空 bundles，但不声称 (F2.2) 的严格式。
这是给定 LP 见证的实际构造；通用有理 LP 可先决定见证是否存在，其软件后端未在本页实现。

**独立抽态与福利。** 每组以概率 λ_gs 选择原 state s，以概率 1−a_g 选择 inactive，各组独立。
active 组对 u 出价 p_gsu，inactive 出价零。令 W=Σ_u max_g bid_gu，A 为 active 组数。
对每个 u 和正阈值 t，令 r_g(t)=Pr[bid_gu≥t]、z(t)=Σ_g r_g(t)。由 (F2.1)，0≤z(t)≤1，故

\[
\Pr[\max_g bid_{gu}\ge t]
=1-\prod_g(1-r_g(t))
\ge1-e^{-z(t)}\ge(1-1/e)z(t).
\]

末式为凹函数 1−e^(−z) 在 [0,1] 上的端点弦界。对有限出价层积分或求和，
Σ_u EΣ_g bid_gu=Σ_gs λ_gs Σ_u p_gsu=q，于是 EW≥(1−1/e)q，EA=q。

**必须同时计费激活数。** 对给定 δ 去随机化的目标是

\[
\Phi=W-\delta A,\qquad E\Phi\ge(1-1/e-\delta)q. \tag{F2.4}
\]

不能只最大化 W 再把实际 active 数擅自当作 q。逐组枚举其正概率的 states 和 inactive 选择，
取条件期望 Φ 最大者。父期望是这些子期望的概率平均，所以最终 Φ 不小于 (F2.4)。
把每个正出价资源交给一个最高出价 active 组（固定 tie rule），零出价资源闲置。
每组收到的 chosen-state 质量 w_g≤1；inactive 为零，W=Σ_active w_g。
再遍历原菜单重新选 attaining state，得到 f_g(B_g)≥w_g，且不改变 B 或物品容量。
质量小于 δ 的 active 组对 w_g−δ 贡献非正，其余至多 1−δ，因此

\[
\Phi=\sum_{g\ {\rm active}}(w_g-\delta)
\le(1-\delta)H_\delta.
\]

这同时控制所有高组的不交性，证明 (F2.3)，并未假设实际 A≤q。
取 δ=3/8。级数 e>1+1+1/2+1/6+1/24=65/24>8/3 给 1−1/e>5/8，
故 Φ>q/4、H>(q/4)/(5/8)=2q/5，得到严格 (F2.2)。

**精确条件期望与位复杂度。** 对每个 u，把全部可能正 bids 排成 0=t_0<⋯<t_K。
在任何已固定前缀，

\[
E\max_g bid_{gu}
=\sum_{\ell=1}^K(t_\ell-t_{\ell-1})
\left[1-\prod_g\Pr(bid_{gu}<t_\ell)\right]. \tag{F2.5}
\]

固定组的 CDF 为 0/1；未定组的 CDF 为 inactive 质量加若干原 λ 的和。
EA 为已固定 active 数加未定 a_g 的和。式 (F2.5) 全为精确有理运算，
没有超越数比较，也不按 1/q、1/λ、δ 的倒数或原分母数值枚举。
决策次数 n、每次候选数和 bid levels 均受显式表大小多项式控制；
所有概率乘积至多用每组一次输入分母，直接有限和/积的位长多项式。
前缀固定不对 tiny 事件概率反复做 Bayes 除法，避免隐藏的精度增长。
输出 attaining states、全部 B_g 和原系数质量回算也都是总位多项式。

**准确的源筛选。** 对任意固定 0<β≤3/8，下列 promise 可只用 (F2.1) 的有理 LP 可行性分离：

- YES：存在不交 allocation，使至少 q 个原 groups 质量一；
- NO：每个不交 allocation 中，质量至少 3/8 的 groups 数严格小于 βq。

YES 中每个 unit group 选 attaining norm1 state，其全部正支撑必须在该 bundle 内。
若有 r≥q 个这样的 groups，给这些 states 各质量 q/r，其余零，得到 (F2.1)。
NO 若 LP 可行，则 (F2.2) 给 H>2q/5≥βq，矛盾。故 promise 下 LP 可行为 YES、否则 NO。
一般 δ,β 满足 δ+(1−δ)β<1−1/e 时同理；这里只使用有理参数的充分条件，
不把超越常数比较当作程序步骤，也不声称边界锐。

**Scope / Counterevidence / Dependencies。** 本结论封闭的是显式 norm1 菜单的“选择足够多高组”源合同，
包括候选组数大于 q 的情形。q 是组数基准，不能换成 state/机器/任务数；
β 是 NO 禁止的高组比例，不是本页 C–F 使用的低组比例 γ。
因此它不证明原 γ≤δ 的低组禁区全部不可能，也不推出所有 groups 都有正常数质量。
LP 不可行仅排除该源 YES，不是一般 UM 的可靠 FAIL 或一般 Santa 的新困难性。
共享内部节点、多层依赖、非 norm1 或隐式菜单没有被排除。
证明依赖 norm1、显式表、正支撑共同列容量及上述福利/激活计分，不依赖本页 NSW 的完整 B 定理。

**来源扣除 / Status / Evidence / Related Files。** 福利 (1−1/e) 机制已有：Feige，
[On Maximizing Welfare When Utility Functions Are Subadditive](https://epubs.siam.org/doi/10.1137/070680977)，
原刊摘要明确记录 fractionally subadditive 的此保证；本次只核原刊摘要，不声称读完原证明。
本节给本接口的自足证明及实际确定化，属于标准工具直接推论，未认证新颖性或外审。
[实际审查](../../reviews/unrelated_machines/normalized_menu_partial_quota_welfare_review.md)、
[给定见证的规范构造及独立穷举审计](../../../tests/audits/unrelated_machines/normalized_menu_partial_quota_welfare.py)
和[冻结运行](../../../evidence/runs/unrelated_machines/normalized_menu_partial_quota_welfare.json)
分别记录证明攻击、实现及有限范围；不把计算升格成全称证明。
一般 `UM-TARGET-v1` 和全部 ε 的反面都仍 OPEN。

## 来源分工、复用范围与版本边界

继承框架来自 DLRV，arXiv:2309.04656v1，§2.1–§2.5、Appendix B；[v1 原始 PDF](../../../history/source/literature/unrelated_machines/dobzinski_li_rubinstein_vondrak_2023_subadditive_nsw_v1.pdf)。英文作者稿编写者实际全文读所供 v1 文本，未读 PDF 或额外 paper/source audits；boss11 的原文阅读与选页渲染范围另记于审查记录，不把下载当作全文实读。原作提供 matching/splitting/iteration/rematching 模板；本页不把其 actual-integral-OPT theorem 直接换成分数结论，A 和本页 deterministic fractional guarantee 由上述推导支撑。LP/matching 为标准工具；分数 lift、位长、CDF、局部 floor、inverse moment 与误差一 DP 在页内另证，不由 standalone 引理跳认 NSW 常数。

对象接口：[既有 normalized-menu 配置证书页](normalized_menu_configuration_certificate_preservation.md)（未冒称本作者另行实读）。reviewer 历史及来源账归同 stem review；本稿非 blind。

v1–v4 原件及旧 generic-SA 数值 objections 保留；旧版没有本次完整 NSW 作者 Proof，不得以新 v5 回填“旧 Proof 早已存在”或转旧数值路线为 PASS。v4 的 global-grid statement 范围亦不追溯改写。v5 以 residual exact normalization 和固定候选 local relative grid 去掉 B 的全局数值-grid 输入限制，这是本次另证的域。

原 v5 的复用范围止于三个精确 ID 的对象与量词；新增 F2 单独按其第四 ID 的范围读取。原 v5：A 的一般 SA 语义匹配、B 的显式无权 XOS 分数 NSW、C–F 的原 normalized 同组后果；不扩展至 weighted/general-SA 后端、all-group max-min、general UM、source hardness、主 near-two 命题或全球新颖性，原 v5 也无已实现软件可 audit；F2 的给定见证软件以本节所链独立审查和冻结运行为准。Evidence、Counterevidence、Status 与 Related Files 由本节、各 ID 的定义/限制及所链审查记录共同给出；main/push 不升级数学真值。
