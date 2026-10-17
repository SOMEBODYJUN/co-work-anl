# 部分 Min-Rep 源的线性度数与真实调度费用义务

精确身份：`UM-PARTIAL-MINREP-SPARSIFICATION-BRIDGE-v2` 与 `UM-PARTIAL-MINREP-REGULAR-HIGH-GIRTH-SOURCE-v3`，分别量化原顶点删边和新增复制顶点的正规高围长构造。读取目的：核对一个完美完备、部分覆盖 soundness 的源构造，并据此计算实际 UM 编译器需要支付的费用。结论只到源和条件费用桥；没有构造 UM 困难性归约。早期 v1 只在 scratch 中冻结，参数较弱，不是另一份现行资产。

## 对象、量词与精确结论

输入为显式、无权、两侧各 n≥1 个顶点的 D-regular 二部投影游戏 Π，N=2n，D≥1。公共字母表 Σ 大小 Q≥2；每条约束 e=(a,b) 给定全映射 π_e:Σ→Σ。允许平行约束，逐条计数、独立采样。val(Π) 是单标签赋值满足的约束比例。多标签赋值 ψ 的列表可空，cost(ψ)=Σ_v|ψ(v)|；边被覆盖当且仅当存在 α∈ψ(a)、β∈ψ(b) 满足 π_e(α)=β。

对每个二进制整数 g≥2、二进制有理数 0<ρ≤1，定义

\[
\ell=\lfloor\log_2g\rfloor,\quad
\lambda=1+\lceil\log_2Q\rceil,\quad
\tau=\frac{\rho}{100g^2},\quad
\gamma=\frac{\rho^3}{10^9g^8},\quad
\mu=\left\lceil\frac{1000g\lambda}{\rho\ell}\right\rceil,
\quad\Delta=1000\mu.
\]

存在如下统一随机位多项式删边算法，保持顶点、字母表及剩余约束的投影：

1. 每个随机种子的输出最大度数均≤Δ。若 val(Π)=1，每个种子均保留 cost=N 的满足全部剩余约束的 singleton 赋值，空边集也按此解释。
2. 若 val(Π)≤γ，以至少 0.9 的概率，输出边集非空，且**每个** cost≤gN 的多标签赋值覆盖比例严格小于ρ。
3. 其时间、输出和随机位数按显式输入及 g、ρ 的总二进制长度为多项式，不按 μ、g 或 1/ρ 的数值循环。
4. 对每个先固定的 g、ρ，由完美完备的常数误差 Label-Cover PCP 和投影平行重复得到 Q≤poly_ρ(g) 的源，再接本删边算法，因而 Δ=O_ρ(g)。这是随机归约下的部分 Min-Rep promise：YES singleton cost N 覆盖全部边；NO 任意 cost≤gN 列表覆盖严格少于ρ比例。一个正确的确定性多项式 promise 判别器将推出 NP⊆BPP；采用的否定假设可为 NP⊄BPP，不能直接改写成仅 P≠NP。

还对任意非空、平衡但不必 regular 的全投影游戏证明：若同一 NO 覆盖禁令成立，则 M>(g−1/2)N/ρ，故最大度数>(2g−1)/ρ。固定ρ时 O(g) 的**阶**不可改进；未声称常数锐或同时字母表最优。

## 原图的廉价列表覆盖率

固定 cost≤gN 的列表族，令 H=4g/τ。长度>H 的顶点至多 gN/H 个；其关联边占比至多 2g/H=τ/2，重复计关联边只使上界更大。若该列表族覆盖至少τ比例原边，则至少τ/2比例被覆盖边的两端列表均非空且长度≤H。逐点独立从非空列表均匀选标签，空列表处任取标签；每条这样的边被满足的概率至少 H^−2。因此某个单标签赋值的 value 至少

\[
\frac{\tau}{2H^2}=\frac{\tau^3}{32g^2}
=\frac{\rho^3}{32\cdot10^6g^8}>\gamma,
\]

与 NO 前提矛盾。故每个廉价列表族在原图的覆盖率严格小于τ。H 无须整数，这里未按测试样本推量词。

廉价列表族的总数 K 可用生成函数控制。取 x=1/Q，有

\[
KQ^{-gN}\le(1+1/Q)^{NQ}\le e^N,
\qquad K\le\exp(gN\lambda).
\]

此界在 gN>NQ 时也成立；实际算法不枚举这些列表。

## 采样、高度删边与同一个总边数事件

若 D<2μ，原图即为输出，以上原图覆盖界给确定性 soundness。否则取最小 s 使 2^sμ≥D，每条原边用 s 个独立公平位以概率 p=2^−s 保留。由最小性 pD∈(μ/2,μ]。记中间边数 Y、其均值 H₀=pDN/2>μN/4。

对固定廉价列表族，记其被采样的覆盖边数 X，EX<τH₀。稀少覆盖事件的 Chernoff 上尾给

\[
\Pr[X\ge\rho H_0/2]
\le\left(\frac{e}{50g^2}\right)^{\rho H_0/2}
\le\exp(-\rho H_0\ln g).
\]

实数阈值对整数随机变量同样适用，零均值时坏事件概率为零。又 ln g≥ℓ ln2>ℓ/2，因此 ρH₀ ln g>125gNλ。对全部廉价列表做 union bound，任何列表越界的概率小于 exp(−124gNλ)<0.001。

另一次共同事件为 Y≥3H₀/4，其失败概率≤exp(−H₀/32)<0.001。这里 H₀>250gλN/(ρℓ)≥1000。**总边数事件只控制一次，不对所有列表重复 union**。原覆盖极稀所产生的 ln g 上尾增益，正好抵去列表计数的对数因子。

根据中间图度数一次性标记所有 degree>Δ 的点，删除它们的全部关联边。条件于某条边已被采样，其某端中间度数的条件期望≤1+μ≤2μ；Markov 给该端被标记概率≤0.002，两端合计≤0.004。若 Z 为实际删除的边数，则 EZ≤0.004H₀，再由 Markov 得 Pr[Z>H₀/4]≤0.016。平行约束使用独立随机位，结论不变。

三类坏事件总概率<0.018。在补集上最终 M′=Y−Z≥H₀/2>0，每个廉价列表覆盖的最终边数≤X<ρH₀/2≤ρM′。度数上界对每个种子成立；YES 的原满足赋值在任何删边后仍满足全部剩余约束。

## 总位复杂度与完美完备起点

μ、Δ 可以数值很大，但固定次幂及有理运算只产生输入位长多项式的整数。D<2μ 时立即返回原图；否则 μ≤D/2，s=O(log D)，只按显式约束表用 O(|E|log D) 个随机位采样，计中间度数后扫描删边。不存在按 μ、g、1/ρ 的数值展开。

外部 Paper Fact 的准确用途如下。Moshkovitz 最终版 Theorem 2.1 在固定 ε₀∈(0,1/4) 给完美完备、双正规、常数字母表与常数度数的投影源；同页前置 PCP 定义明确 YES 可满足全部约束。Dinur–Steurer 作者原稿 Theorem 1.1 对 val(G)≤v 给

\[
\operatorname{val}(G^{\otimes k})
\le\left(\frac{2\sqrt v}{1+v}\right)^{k/2}.
\]

取 k=O(log(1/γ))，完备性和双正规性由显式直积保留，字母表为 poly(1/γ)。也可直接用 Moshkovitz 最终 Theorem 2.3；没有导入 PGC。对固定ρ，γ=ρ³/(10⁹g⁸) 使 Q≤C_ρg^c，c 与g无关。

双正规度数为 d_A,d_B 时，每个左点复制 d_A 份、右点复制 d_B 份，每条旧边连接其全部 copy-pairs 并保持投影。新两侧均有旧 |E| 个点，degree=d_Ad_B。旧赋值复制证明 value 不减；从任意 copy 赋值在每个旧点独立抽一个 copy，其原赋值期望 value 等于新 value，证明 value 不增。显式 blowup 至多原边数三次方。不同侧字母表可嵌入公共大小 max(2,Q_A,Q_B) 的字母表：左新增符号先 retract 至旧标签，右新增符号不在任何投影像中；替换右 dummy 不减满足数，故 value 恰保留。

λ/ℓ=O_ρ(1)，所以 Δ=O_ρ(g)。PCP 链先固定 g、ρ 再归约 SAT，指数允许依赖固定参数；没有宣称当二进制 g 随 SAT 长度增长时整条 PCP 链仍统一多项式。删边算法本身则满足上一节的统一位复杂度。

YES 每个种子属于 YES promise，NO 至少 0.9 概率属于 NO promise。与确定性 promise 判别器复合给 SAT 的单侧随机多项式算法，足以推出 NP⊆BPP。这与声称确定性 NP-hard 归约不同。

## 正规、简单和固定高围长的加强

本节另立精确身份 `UM-PARTIAL-MINREP-REGULAR-HIGH-GIRTH-SOURCE-v3`。v2 在原顶点上删边，保证最大度数；本节采用随机复制连线及同类型交换，得到恰 regular、simple 和固定高围长的输出。两者没有相互替代相应算法的输入域或输出合同。

固定整数 G≥2。沿用本文显式平衡 D-regular 全投影游戏的对象域及 g、ρ、Q、ℓ、λ、τ、γ，另外要求 Qγ≥1。G 是预先固定的常数，不将 binary G 变参数时的指数依赖隐藏成统一多项式。原平行约束仍允许，并作为不同 edge types。

设

\[
 d=\left\lceil\frac{1000g\lambda}{\rho\ell}\right\rceil,
 \quad S=\sum_{j=2}^{G}d^j,
 \quad B=40NS,
 \quad U=\sum_{j=0}^{G+1}d^j,
 \quad m_*=dN/2,
\]
\[
 z=\left\lceil\max\left\{2G+1,\ GB+4U+1,
             \frac{8B}{\rho m_*}\right\}\right\rceil,
 \qquad t=Dz.
\]

存在有硬随机位上界的随机算法，返回 FAIL 或一个投影游戏，顶点数 N′=Nt，边数 M′=dtN/2，字母表不变。其精确合同为：

1. 每个非 FAIL 输出均为显式、平衡、simple、d-regular、girth>G 的游戏；各边继承某个原 edge type 的投影。若原游戏 perfect-complete，把同一原标签复制到其全部 copies 便满足输出全部边。
2. 对所有域内输入，FAIL 概率<0.1。若原 val≤γ，以至少0.8概率得到非 FAIL 输出，并且每一份 cost≤gN′ 的 copy lists 覆盖严格少于ρM′条边；同一原 vertex 的不同 copies 可以使用完全不同的 lists。
3. 对固定 G，最坏时间、输出和随机位数关于完整显式输入及 binary g、ρ 的总位长为多项式；不声称当 G 变化时指数独立于 G。

### 模板、随机层及修复

每个原顶点建立 t 个 slots，按 D 个 incident edge types 分成每组 z 个。同一原 edge type 两端的组按局部序号一一配对，得到跨左右全部 slots 的一个 perfect matching。独立建立 d 层；每个原 vertex、每层抽一份独立 uniform [t] permutation，把 slots 重命名到该原点的 t 个 copy 编号。层并图保留 layer/type 标记，因此每个 copy 在每层恰有一条边，degree 恰为 d，每个(type,layer) bucket 恰有 z 条边。

采用 Fisher–Yates 抽 permutation。每个 uniform 整数 draw 用相应 range 的 ceil-log2 位拒绝采样，至多

\[
 R=\left\lceil\log_2(2000dN(t-1))\right\rceil
\]

次，任一耗尽即 FAIL。实际共有 dN 份 permutations、dN(t−1) 个整数 draws；由此 sampling FAIL≤1/2000。各 draw 的 range 预定且使用独立 bit blocks，所以条件于全部成功，它们仍为独立 uniform draws，得到证明所需的精确 permutation 分布。

枚举并计数长度2至 G 的 simple cycles，parallel 两边算长度2 cycle，单边往返不计。若数量 X>B，返回 FAIL。否则反复选一条短 cycle 的边 e，从同一 original type、同一 layer 的 bucket 中找边 f，使 f 不在任何当前短 cycle，且 f 两端均距 e 两端>G。设 e=(a,b)、f=(c,d)，用 (a,d)、(c,b) 替换二者，继承原 type 和 layer。

候选 f 始终存在：短 cycle vertices 至多 GB 个；e 两端半径 G balls 至多2Σ_{j=0}^Gd^j个 vertices。bucket 是 matching，触及这些禁点的 bucket 边数≤GB+2Σd^j<z。交换保持所有层为 perfect matching，并保持全部 bucket 大小及投影类型。只含一条新边的短 cycle 会给 e/f 端点间的旧短 path；含两条新边的短 cycle 要么也给这样的跨端点 path，要么给 f 两端间一条旧 path，与旧 f 拼成短 cycle。这分别违反远距和 f 非短 cycle 边。因此不产生新短 cycles，至少毁掉所选 cycle，至多 B 次终止。无长度2 cycle 意味着输出 simple。

### arbitrary copy lists 的同时 soundness

固定任意 cost≤gNt 的 copy lists。对原类型 e，记 p_e 为独立均匀选其两端各一个 copy 后 lists 覆盖该投影的概率。取 H=4g/τ。长度>H 的 heavy copies 总数≤gNt/H；D-regularity 使随机原边端点及 copy 的边际均匀，因此触及 heavy 端的概率≤2g/H=τ/2。逐原 vertex 独立抽一个 copy，再从其非空 list 均匀取标签，空 list 任取。其随机单标签赋值的平均 value≤γ；light-covered 边被满足概率至少 H^(−2)。故

\[
 \frac1{|E|}\sum_e p_e
 \le\frac{2g}{H}+\gamma H^2
 =\frac\tau2+\frac{16\tau}{1000}<\tau.
\]

每 type 恰出现 dz 次，故全部模板边的覆盖边际和 mbar<τM′。这里未将各 copy 的 lists 合并成一份原廉价 lists，也未假定抽代表 copy 后的随机成本仍≤gN。

一个 uniform [t] permutation 在 j 个不同 slots 上的联合 images，相对 j 个独立 uniform [t] 值的点态密度至多

\[
 \frac{t^j}{(t)_j}\le e^j.
\]

非单射 tuple 的真实概率为零；对单射 tuple 用 (t)_j≥(t!)^(j/t)≥(t/e)^j。任取 k 条不同模板边，它们在各 vertex/layer 中使用不同 slots，总共2k个，因而其全部 covered 的概率≤e^(2k)乘各边 p_e 的乘积。with-replacement 参照分布下各模板边确实独立，因为 slots 不交；无需声称真实 matching 边的指示变量负相关。

若 Z 为该 lists 的初始 covered 边数，则

\[
 \mathbb E\binom Zk\le\frac{(e^2\mathrm{mbar})^k}{k!},
 \qquad \mathbb E(1+s)^Z\le\exp(e^2\mathrm{mbar}\,s)
 \quad(s\ge0).
\]

Chernoff 给

\[
 \Pr[Z\ge\rho M'/2]
 \le\left(\frac{e^3}{50g^2}\right)^{\rho M'/2}
 <\exp(-\rho M'\ln g).
\]

mbar=0 时概率为零；阈值不必整数。cost≤gN′ lists 数 K≤exp(gN′λ)，而

\[
 \rho M'\ln g\ge250gN'\lambda.
\]

故任何 cheap copy lists 越界的概率<exp(−249gN′λ)<0.001。这是对全部 copy lists 一次完成的同时性，允许 lists 在看到输出图后选择。

每次 repair 只换两条边，对任意 lists 的 covered 数增加至多2；这个确定界同时适用全部 lists。参数给 M′≥8B/ρ，所以在上述好事件中，全部 repair 后仍 covered<ρM′/2+2B≤3ρM′/4<ρM′。

### 短 cycle 概率和总位复杂度

每层是 matching，任何实际 simple cycle 的相邻 layers 必不同，包括首末。固定起始 copy 及长度 j≤G 的 layer 序列，沿 walk 暴露 matching。若 prefix 为 simple，最后当前 copy 和起始目标 copy 在最后一层的 matching 均未揭过：它们相邻所用层不同，且之前没有重访这两个 copy。揭当前 fresh slot 后，若其 template mate 不在起始原 base vertex，则闭合概率0；否则 mate slot 也 fresh，image 在至少 t−G 个未用编号中均匀，闭合概率≤1/(t−G)。这不需要原 edge type 的条件分布均匀。

于是

\[
 \mathbb E X\le\frac{Nt}{t-G}\sum_{j=2}^{G}d^j
 \le2NS,
 \qquad \Pr[X>B]\le1/20.
\]

rooted walks 多计只加强上界，且不同层的 parallel 2-cycles 已包含。加上 capped sampling，所有输入 FAIL<0.1；NO 再扣同时 lists 坏事件<0.001，成功概率实际上>0.9，故满足保守的0.8合同。

Qγ≥1 意味着 Qρ³≥10⁹g⁸，因而数值 g、1/ρ、d 受显式 Q 的固定多项式控制。Q 由非空显式投影表支付输入长度；固定 G 时 S、B、U、z、t 和 bounded random bits 均为显式输入的多项式。枚举长度≤G的 cycles、BFS 找远距候选、扫描 bucket 及至多 B 次交换也满足总位多项式。G 变参数时该指数依赖 G，不属于本合同。

Qγ<1 不属于算法域，且此时非空全投影游戏 val≤γ 本就不可能，因为任意左标签配均匀随机右标签的期望 value 为1/Q。若固定参数 PCP 起点需进入合法域，可通过左右共同字母表的 retraction/injection 填充到 Q≥1/γ；投影定义为先 retract 左新增符号、再投影至旧右标签的 injection，value 及完美完备性恰保持。由旧 PCP 起点的 Q=poly_ρ(g)，此填充仍保 polynomial alphabet。因此，对每个先固定的 g、ρ、G，可同时得到 d=O_ρ(g)、simple、regular 和 girth>G 的部分 Min-Rep promise。

FAIL 是明确 flag，不是伪造的 girth 游戏。源归约调用者可在 FAIL 分支直接按 YES 处理；若以后有实际 UM 编译器，也可输出合法空任务实例。因此固定参数 PCP 链与该随机变换复合，仅给随机 source reduction；一个确定性 promise 判别器将推出 NP⊆BPP，采用的否定假设可为 NP⊄BPP，不自动改写成 P≠NP 下的确定性 hardness。

本节没有实现生产代码，没有把某个随机 lift 的 soundness 升级为任意 cover 均保持 soundness，也不否定配置有限覆盖整数化障碍。v3 沿用既存源的强错误率及 rare-covered-tail 框架，增加复制 lists 的同时控制、固定高围长 regular 输出和有限 repair。其全球新颖性未认证；高围长本身不是一般 UM 的费用或 source decoder，后文真实 trigger、π 接口、预算 B 和固定费用 F 的义务仍全部保留。UM-TARGET-v1 正反面均保持 OPEN。

## 线性度数的必要性

对任意非空平衡全投影游戏，先在每个左点任选一标签，成本 N/2。任选 t 条不同边，将所选左标签沿这些边的投影加入右列表；增加成本至多 t，覆盖至少这 t 条边。令整数 B=(g−1/2)N。若 ρM≤B，则 t=ceil(ρM)≤min(B,M)，由此得到 cost≤N/2+B=gN、覆盖比例≥ρ 的列表，违反严格 NO 禁令。因此

\[
M>\frac{(g-1/2)N}{\rho},\qquad
\Delta_{\max}\ge\frac{2M}{N}>\frac{2g-1}{\rho}.
\]

孤点、重复右标签或平行约束只使这项便宜构造的成本更低。全投影、平衡与非空是实际使用的前提。

## 费用桥、最近文献和仍缺的实际义务

另设一个尚待构造的实际 UM 编译器。它须给出具体 P、YES 的实际阈值 T 调度，并从每个所需弱阈值下的**完整实际调度** σ 提取覆盖至少ρM条原投影边的列表，满足

\[
\operatorname{cost}(\psi)\le N+B(\sigma)/F,
\quad 0\le B(\sigma)\le cM,
\quad F>0,\quad c\ge0.
\]

若 F≥cΔ/[2(g−1)]，则 M≤ΔN/2 给 cost(ψ)≤gN，与好 NO 源矛盾。固定ρ、c且 Δ=O_ρ(g) 时，只需一个足够大的**固定常数** F。v3 中取 Δ=d，N、M 则使用输出的 N′、M′；相同代数仍只给条件充分式。此处没有实现该费用；degree 必要性也不是对任意 c 排除 F=1 的定理，仍须逐项验证实际编译器给出的 c、F。更长路径、更多复制或 Hamming 距离不自动付费；若同时放大 B 的系数 c，净收益可能消失。

Manurangsi 2019 Lemma 7 已有独立采样、高度 trimming 与同时廉价列表分析，相关源给 O(g log g) 度数及较小多项式字母表。本文沿用其框架，改用更强原 soundness、稀少 **covered** 边上尾及一次共同总边数事件，证明当前较粗 polynomial-alphabet / O(g)-degree 取舍；不是把其 Lemma 7 换符号就当新结果。ECCC TR24-027 的 2026 修订 §7.4/Theorem 7.13 仍给 O(g log g) 度数和接近 g² 的字母表。当前未优化字母表，也未证明优于其连通性应用，更未认证全球新颖性。原文定位见 [文献表](../../unrelated_machines/LITERATURE.md) 与 manifest。

真实调度中的常数比例 trigger、同一源顶点标签的一致性、π_e 接口、无重复计账的 B 和固定费用 F 全部仍缺。两份内部 Exact-first 重构及冻结全文读后攻击见 [审查](../../reviews/unrelated_machines/partial_minrep_linear_degree_source_review.md)；算法未作生产实现，有限测试没有被用作一般证明。UM-TARGET-v1 正反面均保持 OPEN。


v3 的相关原文边界：Kun arXiv:0706.1701v2 Theorem1已有 CSP 的固定高围长等价，Theorem9用 twisted-product 内的同纤维置换修短环；因此这里不把换边或高围长本身称作新机制。Dinitz–Kortsarz–Raz TALG2015 §3/Lemma3.1、Theorem3.2–3.4 以采样和删除短环保 Label-Cover/Min-Rep gap，其输出不保证恰正规。v3 的实际增量在 arbitrary copy lists 的两侧置换同时性、线性阶 degree 与保类型的有限修复之组合；尚未认证全球新颖性。原文、读取范围及无法下载的版本见 manifest。
