# 部分 Min-Rep 源的线性度数与真实调度费用义务

精确身份：`UM-PARTIAL-MINREP-SPARSIFICATION-BRIDGE-v2` 与 `UM-PARTIAL-MINREP-REGULAR-HIGH-GIRTH-SOURCE-v3`，以及 `UM-PARTIAL-MINREP-DEGREE-MASS-REGULARIZATION-v5`；分别量化原顶点删边、等份复制正规源及任意原degree/typed域的质量复制。读取目的：核对一个完美完备、部分覆盖 soundness 的源构造，并据此计算实际 UM 编译器需要支付的费用。结论只到源和条件费用桥；没有构造 UM 困难性归约。早期 v1 只在 scratch 中冻结，参数较弱，不是另一份现行资产。

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

## 任意不正规 typed 源的度数质量复制

精确身份 `UM-PARTIAL-MINREP-DEGREE-MASS-REGULARIZATION-v5`。这项加强不要求原图 regular、两侧等大或原最大degree有常数界；两个字母表保留各自的真实类型。v4漏写非空字母表会使val不良定，故其字面全域不获接受；本节只登记显式修复后的v5，不倒改旧冻结记录。

固定整数 G≥2。输入任意非空、有限、显式无权二部multigraph Π=(A,B,E)，M₀=|E|≥1。先删孤点，令N₀=|A|+|B|。左右字母表Σ_A、Σ_B均非空、明确列举，Q=max(|Σ_A|,|Σ_B|)≥2；每条edge type e给显式全投影π_e:Σ_A→Σ_B。平行约束逐type计。列表可空，cost逐实际标签符号计。给binary整数g≥2和binary有理0<ρ≤1，沿用ℓ、λ、τ、γ、d的公式，但此处λ由typed域的最大大小Q计算，并要求Qγ≥1。

设

\[
S=\sum_{j=2}^{G}d^j,\qquad B_0=40N_0S,\qquad
U=\sum_{j=0}^{G+1}d^j,\qquad m_*=dM_0,
\]
\[
z=\left\lceil\max\left\{2G+1,\ GB_0+4U+1,
\frac{8B_0}{\rho m_*}\right\}\right\rceil.
\]

每个原v建立t_v=deg_Π(v)z个copies及同数slots。按v的incident原edge types分成每组z个，同type两端按局部序号配对成template。独立建立d层，每个原v、每层抽一份uniform[t_v] permutation重命名到其copies。每层为左右全部slots的perfect matching，每个(type,layer)bucket总有z条matching边。

因为左右Σ_vdeg(v)均为M₀，输出每侧恰M₀z个copies，

\[
N'=2M_0z,\qquad M'=dM_0z=dN'/2.
\]

因此全部copies的degree恰为d。与v3一样，保留type/layer标记，采用same-type/layer有限换边修短cycle。每条边继承原π_e，不合并左右alphabet、不构造反向全函数，不改变任何原边的surjectivity或equal-fiber属性。

精确合同为：每个seed返回FAIL或simple、balanced、exact d-regular、girth>G的显式游戏。全部域内输入FAIL概率<0.1；若原val=1，任一非FAIL输出复制原labels即全满足。若原val≤γ，至少0.8概率返回非FAIL输出，并对**所有**cost≤gN′的真实copy lists同时有covered<ρM′。同一原点copies可取完全不同的lists；不要求原点成本按degree加权。对固定G，最坏时间、输出规模和硬随机位数均为总显式输入及binary g、ρ长度的多项式。

### 质量归一化为何不需要原regularity

固定cost≤gN′的copy lists，令H=4g/τ，并令h_v为原v的heavy copies数，heavy指list长度>H；总h≤gN′/H。对原edge e=(a,b)，p_e为独立均匀抽其两端copies时lists覆盖的概率。随机均匀抽一条原edge，再抽两端copies，触及heavy的概率至多

\[
\frac1{M_0}\sum_{e=(a,b)}\left(\frac{h_a}{t_a}+\frac{h_b}{t_b}\right)
=\frac{\sum_vh_v}{M_0z}=\frac{2h}{N'}\le\frac{2g}{H}.
\]

deg(v)和t_v=deg(v)z精确抵消。这是度数质量复制相对固定fiber尺寸的新增承重步骤；若仍按每原v相同份数复制，上式一般不成立。

逐原v独立抽一个copy，再在其非空list均匀取typed标签，空list任取合法标签。由val≤γ及light-covered pair至少以1/H²概率满足，

\[
\frac1{M_0}\sum_ep_e\le\frac{2g}{H}+\gamma H^2
=\frac\tau2+\frac{16\tau}{1000}<\tau.
\]

每type在d层共出现dz次，所有模板边覆盖边际和mbar=dzΣ_ep_e<τM′。没有将copy lists合并成一份廉价原lists，也没有把随机代表copy的原成本说成必受gN₀控制。

每份不同长度t_v permutation在j个distinct slots上的点态密度同样≤e^j；因此v3的factorial-moment证明逐对象沿用，总2k slots给e^(2k)。对固定lists仍有

\[
\Pr[Z\ge\rho M'/2]<\exp(-\rho M'\ln g).
\]

typed标签的bit positions总数为Σ_vt_v|Σ_{side(v)}|≤QN′，故全部cheap lists数≤exp(gN′λ)。d的选择给ρM′ln g≥250gN′λ，全列表坏事件<0.001。只用Q上界计数不代表把typed labels识别成相同符号。

### 不同fiber的短cycle、repair与硬位数

固定一个属于原v的起始copy及长度j≤G的layer序列。若实际walk形成simple cycle，相邻layers必不同。最后当前copy与起始copy在最后层均fresh，template mate亦fresh；若mate不属于原v闭合概率为0，否则其image在v的至少t_v−G个未用copy编号中均匀。因此闭合到起始copy概率≤1/(t_v−G)。按起始原v分组求和，得到

\[
\mathbb EX\le\sum_v\frac{t_v}{t_v-G}\sum_{j=2}^{G}d^j
\le2N_0S,
\qquad \Pr[X>B_0]\le1/20,
\]

其中t_v≥z≥2G+1。这里没有用N′乘最小fiber闭合界；B₀只按原非孤点数N₀计费。不同层parallel2-cycles已包含，单边往返不计。

X≤B₀时，短cycle vertices至多GB₀；当前输出degree为d，选中坏边两端的半径G balls至多2Σ_{j=0}^Gd^j个vertices。每bucket是matching，故其触及禁点的边数≤GB₀+2Σd^j<z，所需干净远距f必存在。与v3同一双边交换证明保证不生新短cycles，≤B₀步终止。对所有lists covered统一增量≤2B₀；M′=zm_*≥8B₀/ρ使最终仍covered<3ρM′/4<ρM′。

Fisher–Yates实际整数draws数为

\[
K_0=d\sum_v(t_v-1)>0.
\]

每draw使用至多R=ceil log₂(2000K₀)轮拒绝采样，任一耗尽返回FAIL；sampling FAIL≤1/2000。range预定、bit blocks独立，条件全部成功后仍为精确独立uniform permutations。因此所有输入FAIL≤.0505<.1，NO再扣全lists坏事件<.001，成功概率>.9，满足保守.8合同。

Qγ≥1支付数值g、1/ρ、d；删孤点后N₀≤2M₀、原degree≤M₀，固定G时z及t_v≤M₀z、N′=2M₀z均为显式输入固定多项式。硬随机位、cycle枚举、BFS、扫描bucket及≤B₀次repair同样多项式。G变参的指数依赖、没有Qγ域时的数值展开均不属于合同。此变换未构造任何UM矩阵。

### 保exact k-to1的固定误差PCP应用

若有perfect-complete、任意固定误差、常数字母表的exact k-to1投影PCP（k先固定），先固定g、ρ、G并取误差≤γ，再接本变换。原PCP可以不regular、degree随输入长增长、两侧点数不同；结论给simple、balanced、constant exact degree、固定高girth，同时保exact k fibers的随机source family。

若起点Qγ<1，可在这个**先固定参数的PCP corollary**中显式同步复制alphabet：取足够大的固定整数L，左右新域分别为Σ_A×[L]、Σ_B×[L]，新投影为

\[
\pi'_e(\alpha,s)=(\pi_e(\alpha),s).
\]

每个(α,s)是新source中一个真实标签，列表逐这种pair计cost，π完整读取并保留tag；tag不是隐藏的route alias。所有后续Q′、λ、d由新alphabet实际大小重算。丢tag把新满足边投回旧满足边，给val_new≤val_old；旧最优赋值统一tag给反向≥，故value恰保持。每个(β,s)有原先恰k个preimages，equalfibers和surjectivity均保持。

取L≥1/(Qγ)即可进入Q′γ≥1。参数先固定时L为常数，PCP归约仍多项式。这里没有把域外任意binary g、ρ的小Q输入按巨大L展开，继而冒称该padding也有uniform位多项式保证。主图变换在其Qγ域内的uniform位复杂度与本固定参数预处理不同。

一般fixed-error PCP仅给字母表为某个常数，不自动给Q=poly_ρ(g)。只有另给这个定量alphabet界时，才由λ/ℓ=O_ρ(1)推出d=O_ρ(g)；若还需同步clone，Q′≤Q+1/γ仍保这个多项式界。新exact4-to1 primary theorem可作为本条件应用的外部Paper Fact，原文定位和读取范围单独登记，不用本节内部概率证明替代PCP审查。

FAIL为明确flag，调用者可按YES处理；原perfect标签对每个非FAIL输出均满足。原记录的确定性promise判别器后果NP⊆BPP仍成立；末节另以独立身份提取更强的全种子后果，不能改称P≠NP下确定性hardness。没有真实UMcompiler、没有新颖性认证或生产实现，UM-TARGET-v1保持OPEN。

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


v5的具体Paper Fact应用：Fei–Minzer–Wang ECCC TR26-179 Revision2 Theorem1.6 给任意固定误差下perfect-complete exact4-to1游戏的NP-hardness；Definition1.1中的4-to1确为每个右标签恰4个左原像，允许平行约束。root实际读原PDF对应定义/定理及AppendixB的sub→exact变换，并核119页原字节；不声称完整重审其PCP证明，也不从该定理免费导入常数degree或regularity。v5本身补上所需正规化，因此可接出constant-degree、simple、balanced、固定高girth的exact4随机源；一般字母表随误差的定量增长未由此原文推出poly(g)，所以不自动得到d=O(g)。原文身份、读取范围与局限见manifest。

## 全种子完备源的拒绝种子证书

**UM-PERFECT-COMPLETE-SEED-CERTIFICATE-v1。** 这是从复杂度定义得到的独立推论，不改变以上v2/v3/v5源的身份，也不声称新PCP或物理归约。设固定确定性程序R(Φ,r)在每条计算路径上均有关于公式长度的硬多项式时间及输出长度界，种子r有固定多项式长度；未用位可忽略。R返回FAIL或明确对象域I内的合法显式实例。设D是全输入确定性多项式程序，在source YES上答1、source NO上答0，在promise外可任意答但必须停机。FAIL直接按1处理，记复合结果为D̂(Φ,r)。要求

\[
\Phi\in\mathrm{SAT}\Rightarrow\forall r\quad\widehat D(\Phi,r)=1,
\qquad
\Phi\in\mathrm{UNSAT}\Rightarrow\exists r\quad\widehat D(\Phi,r)=0. \tag{S1}
\]

则UNSAT∈NP，故NP=coNP。若均匀独立公平位采样另满足一个对所有UNSAT输入都成立的固定逆多项式拒绝概率下界，则进一步有

\[
\mathrm{SAT}\in\mathrm{coRP},\qquad
\mathrm{NP}=\mathrm{RP}=\mathrm{coRP}=\mathrm{coNP}. \tag{S2}
\]

**证明。** UNSAT验证器猜测r，重跑R；FAIL拒绝证书，否则当且仅当D输出0时接受证书。(S1)左边排除可满足公式的所有假证书，右边给每个不可满足公式一个证书。验证器无需辨认source好事件或验证source NO承诺；D在promise外的拒绝也不会给SAT假证书。SAT的确定性many-one完全性给coNP⊆NP，取补即得相等。这里只存在输入各自的种子，不存在或寻找一个公共好种子的声明。

设拒绝概率≥1/q(|Φ|)，q为固定整数值、至少1的多项式上界。独立运行q次，全部答1才接受SAT。SAT永不误拒，UNSAT误受概率≤(1−1/q)^q≤e^(−1)<1/2，故SAT∈coRP。RP⊆NP由接受随机位作证书直接成立，取补给coRP⊆coNP；再用NP⊆coRP和取补夹得(S2)。仅有一个好种子可能只有指数小概率，不能免费推出(S2)。均匀性、最坏多项式时间、硬种子长度和同一个逆多项式界都是前提；期望时间须先截断并重核概率，不能未经转换直接调用本引理；随机advice或仅高概率YES完备不属于本合同。

**应用到已有源。** 先固定g、ρ及需要时的G，再接本文已登记的确定性完美完备PCP起点。以下概率均是好NO且非FAIL的无条件联合概率。

| 源身份 | 每个YES种子的行为 | 每个UNSAT输入的好NO概率 | 确定性总promise判别器的后果 |
| --- | --- | --- | --- |
| UM-PARTIAL-MINREP-SPARSIFICATION-BRIDGE-v2 | 每次删边都保singleton覆盖，空边集也是YES | ≥0.9，且输出非空 | (S2) |
| UM-PARTIAL-MINREP-REGULAR-HIGH-GIRTH-SOURCE-v3 | 非FAIL复制原标签全满足；FAIL按YES处理 | ≥0.8 | (S2) |
| UM-PARTIAL-MINREP-DEGREE-MASS-REGULARIZATION-v5 | 非FAIL保原typed标签完备；FAIL按YES处理 | ≥0.8 | (S2) |

原文NP⊆BPP是仍正确的较弱后果；这里提高的是复杂度后果，未更改源的度数、alphabet、概率或费用合同。固定参数的PCP指数可依赖g、ρ、G，不声明它们随公式长增长时整条链仍统一多项式。v2的空边YES必须被D接受；v3/v5的FAIL不提交给D。既有Qγ域、typed非空域及capped sampling硬位界保持。

**条件UM推论。** 对每个先固定整数k≥2，设上述R_k的每个非FAIL输出H还可由一个确定性总位多项式编译器产生合法完整模型(P_H,T_H)，T_H为正有理数，令β_k=2−1/k。必须额外证明：

1. SAT的所有非FAIL种子均有真实整数OPT(P_H)≤T_H。
2. 每个UNSAT至少有一个好、非FAIL种子，其每个真实合法完整分配σ若C_max(σ)<β_kT_H，就能导出违反source NO的见证。因此该种子有OPT(P_H)≥β_kT_H，允许等号。

若UM-TARGET-v1的算法A和常数ε>0存在，选择固定k使1/k<ε，定义

\[
D_A(H)=1\quad\Longleftrightarrow\quad
C_{\max}(A(P_H))<\beta_k T_H. \tag{S3}
\]

SAT时C_max≤(2−ε)OPT≤(2−ε)T_H<β_kT_H；好NO时任何A的合法输出均有C_max≥β_kT_H。故(S1)成立，推出NP=coNP；满足上述第2项**编译后NO/全输出decoder合同**的非FAIL种子有逆多项式概率时才得到(S2)，不能只引用更大source NO事件的概率。证书接受条件是(S3)的补 **≥β_kT_H**，不能误用严格大于而漏掉NO等号。算法只编码整数k和有理阈值，不需要编码或比较未知实ε。精确逐机有理求和与交叉相乘的位长多项式；坏种子也必须输出合法实例并使A停机。空任务/零OPT给负载0，T_H>0保严格YES分离；∞不参加有限负载求和。

本条件推论保留一个实质缺口：本文没有提供编译器或第2项全输出decoder。原费用桥若能从每个低负载σ产生covered≥ρM且cost≤N+B/F≤gN的列表，才可用其严格NO禁令证明第2项。只给某个调度、LP证书、好事件概率或固定ε的一次gap都不够。

在额外物理合同全部成立之后，NP≠coNP已足以否定原目标；有概率下界时也可采用NP⊄coRP，它比NP⊄BPP弱。任何一项都没有被改写成仅P≠NP，主目标及其一般反面仍OPEN。该推论是标准证书/单侧错误机制的自足应用，全球新颖性未认证。独立先陈述重构、最终正文攻击、精确阈值边界核验见[专门审查](../../reviews/unrelated_machines/perfect_complete_seed_certificate_review.md)。
