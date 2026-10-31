# LST 2025 仿射线源：uniform 菜单编译的实际三二上界合同

候选 ID：`UM-LST2025-AFFINE-LINE-SOURCE-UNIFORM-COMPILATION-OBSTRUCTION-v1`。

Exact-first scratch freeze，2026-10-18。本文件只陈述精确合同，不附证明。所需数学是既有 pair-overlap/Hall 计数对一个实际 primary source 的应用；不主张新 Hall 定理、新近似算法框架或数学新颖性。没有改 repo、Git 或 Work。

## 1. 已实际读取的 primary 与其准确证据域

Euiwoong Lee, Ola Svensson, Theophile Thiery, *Asymptotically Optimal Hardness for k-Set Packing and k-Matroid Intersection*，arXiv:2409.17831v1；STOC 2025，DOI `10.1145/3717823.3718142`。

- Primary full PDF：<https://arxiv.org/pdf/2409.17831>
- Primary abstract：<https://arxiv.org/abs/2409.17831>
- 实际读取位置：§2 Definition 2.1；§3 Theorem 3.1、Claim 3.3 及完整构造/对应证明；§4 Theorem 4.1。
- 没有把 PDF 下载到本地，故没有本地 raw PDF 路径或 hash 可交付。

论文 §3 使用 prime R、alphabet `[R]`、变量 constraint-degree 至多 R，并把 constraint 的允许 tuple 编译成 kR 元 set。其 affine-line gadget 用 label 作 slope、变量的 constraint incidence index 作 intercept。§4 的已证 hardness 是：固定 `k>=4, epsilon>0`，充分大的 prime R 上，YES value 至少 `1-epsilon`，NO value 至多 `k(1+epsilon)/((k-3)R)`，除非 `NP subseteq BPP`。不是 perfect-completeness promise，也不是 partial-set tiny-retention hardness。

以下使用该 source 的明确表示形式另定义 grouped 菜单和普通 UM compiler。group 是一项 constraint；state 是该 constraint 的一个允许 tuple，不把每个 tuple 当作独立 group。

## 2. 完整 grouped line 输入

取任意 prime `R>=2`，采用论文的域 `F_R=Z/RZ`。有限变量集合 X，有限非空的 indexed constraints 集 G。每项 constraint g 涉及一个由 **k 个不同变量**组成的有序 tuple `X_g=(x_1,...,x_k)`，其中整数 `k>=1` 对所有 g 固定。变量不得在同一 constraint 内重复。论文的 k-partite 特例满足这一条件；这里不要求全局 k-partiteness。

对每个变量 x，令

\[
G(x)=\{g:x\in X_g\},\qquad d_x=|G(x)|\le R,
\]

并固定一个注入

\[
j_x:G(x)\hookrightarrow F_R.
\]

它可由编号 `1,...,d_x` 在 F_R 中取值获得；当 `d_x=R` 时编号 R 对应域元素 0。degree 按含 x 的 indexed constraints 计，不是某个 constraint 里重复变量的个数，也不是所有 allowed states 的数目。

每 g 有显式允许 tuple 集 `A_g subseteq F_R^k`。**本编译合同要求每个 A_g 非空。** 每个 state s 就是该允许 tuple，给 x_i 的 label 记作 `s(x_i)`。允许不同 indexed constraints 使用同样的变量 tuple 或同样的允许 tuple 表；它们的 incidence indices 仍须按 indexed constraints 区分。

变量资源宇宙互相带 tag：

\[
U_x=\{x\}\times F_R^2,\qquad U=\biguplus_{x\in X}U_x.
\]

定义每个变量 incidence/label 的 line

\[
E_{x,g,a}=\{(x,z,az+j_x(g)):z\in F_R\}.
\]

定义 state 的资源 **集合**

\[
S_{g,s}=\biguplus_{x\in X_g}E_{x,g,s(x)}.
\]

域加乘在 F_R 中进行；变量 tag 为身份的一部分，不跨变量合并资源。同一 state 对每个变量恰用一条 line、对每个资源恰有一个 incidence。

每条 line 有 R 个不同资源；每个 state 恰有 `kR` 个不同资源。两个不同 constraint 在同一变量上的 line intercept 不同，因此它们不会是同一条 line；若 slope 相同则不交，若 slope 不同则恰交一个资源。

## 3. 待独立核对的 source-specific allocation 合同

**对每个上述显式 grouped 输入、每个任意完整 state 选择 `s(g) in A_g`，都存在 pairwise-disjoint subsets**

\[
\tag{A}
B_g\subseteq S_{g,s(g)},\qquad
|B_g|=\left\lceil\frac{kR}{2}\right\rceil\quad(g\in G).
\]

可以使用一个整数 capacitated bipartite matching/flow 确定性构造这些 subsets。最终 B_g 是自由的全局 partial subsets；不要求它是变量-wise、line-wise 或 coordinatewise product，也不要求选中 states 可由一个一致的全局 CSP assignment 产生。

“任意完整选择”是本合同核心：不论 source YES/NO，也不论这些 local tuples 在共享变量上的 labels 是否冲突，均有(A)。因此不能把 source 对**整条 lines／整个 sets**的匹配一致性结论，未经另证延伸到 tiny partial allocations。

本合同不声称 ceiling 配额在每个实例上最优，也不声称不能领取更多。它只给一个源特定的统一 constructive lower bound。

## 4. 完整普通 UM compiler 及实际负载合同

构造原 ordinary unrelated-machines 实例 P，所有对象保留 indexed 身份：

- 每 `(g,s)` 一台 private machine `M_gs`；
- 每 `u in U` 一台 resource machine `R_u`；private/resource 的标签互不相同；
- 每 g 一件 selector `J_g`，仅能在本组所有 `M_gs` 上执行，时间为 1；
- 每 `(g,s,u)`、`u in S_gs` 一件不同 incidence job `I_gsu`，仅能在自身 `M_gs` 上用普通有理时间 `1/(kR)`，或在 `R_u` 上用时间 1。

其余时间均为 infinity。没有额外 jobs、预载、物理一致性约束、拒绝或不同机器身份的合并。所有未选 indexed states 的全部 incidence jobs 也在 P 中并必须执行。每 state 的 private 总质量恰为 1。

**实际调度合同：** 对每个这样的 P，不输入 source witness 或 OPT，任取每组一个允许 state，再用(A)的 allocation，即可构造全部原 jobs 的合法调度，满足

\[
\tag{B}
C_{\max}\le 2-\frac{\lceil kR/2\rceil}{kR}\le\frac32.
\]

具体原任务输出要求：把每 J_g 放在所选 state；只把所选 states 中对应 B_g 的 jobs 导出；所有其余 jobs，包括所有未选 states 的全部 jobs，留在自己的 private machine。所有 resource loads 至多 1，未选 private loads 为 1，选中 private loads 为 `2-|B_g|/(kR)`。

selector 强制 `OPT(P)>=1`。如果存在一项全局 CSP assignment 满足全部 constraints，则选择其所有 local tuples 时全部 S_gs 互不相交，得到 `OPT(P)=1`。但 source §4 的 YES promise 仅为 `value>=1-epsilon`，不能免费当作这个 stronger premise。

式(B)是该具体 uniform compiler 所有输入上的 absolute bound，并且自然给其至多 3/2 的 actual approximation bound。它不代表原 set packing 或 k-CSP 变容易，也不是对任意真实 source compiler 的普适归约不可能性。改变权重、资源映射、额外 jobs 或其它物理结构后必须另行分析。

## 5. 空 allowed tuple 集及 degree 的接口边界

论文 Definition 2.1 允许 constraint 是任意 relation，未在定义处统一保证每个 relation 非空。若某 `A_g` 为空，source set packing 可没有该 constraint 的任何 set；但本 grouped-selector compiler 若仍保留 J_g，就会让该 job 无 eligible state machine，实例不可行。

因此不能把原始 source 的空 relation 静默编译成该普通 P；本合同明确只对所有 A_g 非空的菜单输入负责。若另一个 reduction 删除这些 constraints、增加 dummy state 或重新编码，必须对其 completeness/soundness 和实际 jobs 另给合同，不能引用本页掩盖空菜单。非空显式菜单时无需寻找全局满足 assignment，任取 local state 即可启动(B)。

## 6. 显式位复杂度与证据状态

设 `v=|X|`、`m=|G|`、`a=sum_g |A_g|`。资源 `vR^2`；private machines a；incidence jobs `L=kR a`；selectors m；有限资格条目 `2L+a`。dense P 则有 `(vR^2+a)(m+L)` 项。时间 `1/(kR)` 和域元素/身份可用 `O(log(kR)+log(v+m+a+1))` 量级位编码。

归约及 matching 输出按上述完整显式总位长多项式计；不声称 polynomial in `log R` 的 succinct 编译。固定 source 的 k,R 时，这是普通 source input 大小上的多项式编译；论文 Theorem 3.1 自己也给以 `R^k` 计费的运行时间界。

第3节的 allocation 可由显式组—资源图的整数 flow 恢复，每组需求至多 kR；无需按更大隐藏数值复制。最终输出每一原 job 的合法 machine identifier。此页不附实施或数值实验，不把旧 Hall/pair-overlap 事实包装成新数学主定理。

本 Exact 尚待独立核对和 root 对 primary 的亲读。它不声称本源满足 perfect YES1，不提供任何 normalized tiny-hardness 源，不把 `NP not subseteq BPP` 改成只需 `P!=NP`，也不写入 repo。
