# 度数质量复制正规化 v4：Exact-first 独立重构

审查者：内部子研究者 pcsp_occurrence。实际只读 `degree_mass_copy_regularization_v4_exact_statement.md`，读前、读后 SHA256 均为 `45c1d754332fc556066b994bffbda407bd2d619a05a77a539969f5ef2dc66b38`。未读作者的 v4 proof，未向作者询问证明，未读取或交换其他审查者的本次证明。本稿先冻结，再申请作者 proof 进行读后攻击。

先验披露：此前我已审 v3 的 Exact 及冻结 proof，知道 permutation 的点态 e^j 比较、factorial-moment 上尾、fresh-image 短环计数和同 type/layer repair。以下不是对这些旧引理的无先验发现；v4 的非正规质量归一化、异长 fiber 的 cycle 求和、typed alphabet 和 equal-fiber/PCP 接口是在只看新 Exact 后独立重构。

结论：按投影游戏的通常定义（两侧字母表均非空），新合同没有 standing fatal；精确第1–4项和第5项的条件数学可由下述推导闭合。本次没有运行算法软件、有限实验，亦未以本审查认证新颖性或 UM compiler。文末有非致命的对象域明确化建议。

## 1. exact balance、degree 和输出预算

删除孤点后，每个原 v 的 degree d_v≥1，t_v=d_v z。因为 Σ_{v∈A}d_v=Σ_{v∈B}d_v=M₀，输出两侧均有 M₀z 个 copies，N′=2M₀z。

每层的 slots 按原边逐 type 配对，故是左右全部 slots 的 perfect matching；各 v 的不同长度 permutation 仅重命名其自身 slots，不改变 matching 性质。因此每个 copy 每层恰有一条边，总 degree 恰为 d；M′=dM₀z=dN′/2。每个(type,layer) bucket 恰有 z 条边，平行原约束的不同 type 不合并。

无论原 degree、两侧原点数及 alphabet 大小如何不平衡，这些恒等式都精确成立。输出 cost 计算在所有真实 copies 上，不能用原 N₀ 代替 N′，也无需把原 lists 强行要求成某种 degree-weighted budget。

## 2. degree-mass 对 arbitrary copy lists 的精确归一化

固定一份输出 copy lists ψ，总 cost≤gN′，同一原点不同 copies 完全允许不同。记原 v 的 heavy copies 数 h_v，heavy 指 list 长度>H=4g/τ；总 heavy 数 h≤gN′/H。

对原类型 e=(a,b)，p_e 是独立均匀选择 a、b 各一个 copy 后 lists 覆盖 e 的概率。随机选均匀原边，再在两端各均匀抽一个 copy。触及 heavy 端的概率至多

\[
\frac1{M_0}\sum_{e=(a,b)}
 \left(\frac{h_a}{t_a}+\frac{h_b}{t_b}\right)
=\frac1{M_0z}\sum_v h_v
=\frac{2h}{N'}\le\frac{2g}{H}=\frac\tau2.
\]

中间等号承重：每 v 的 d_v 个原 incidences 与 t_v=d_vz 精确抵消。不能以原点均匀分布替代；原点按 degree 抽取的不同质量正由 copies 数支付。

逐原 v 独立均匀抽一个 copy，再从其非空 list 均匀选一个标签（空 list 任取其侧的合法标签）。这产生原游戏上的真实随机单标签赋值。NO 前提 val≤γ 使其期望 value≤γ。每个 light-covered 端点对，其兼容标签 pair 被选概率至少1/H²。于是

\[
\frac1{M_0}\sum_e p_e
\le\frac{2g}{H}+\gamma H^2
=\frac\tau2+\frac{16\tau}{1000}<\tau.
\]

这一步只使用 copy-list cost≤gN′，不要求抽代表 copy 后有某个原 cost≤gN₀ 的事件，更不把该随机成本当确定约束。

每原 type 在 d 层共出现 dz 次，因此固定 ψ 的所有模板边覆盖概率边际和 mbar=dzΣ_ep_e<τM′。

## 3. 异长 permutations 的同时 tail

任意长度 t_v 的 uniform permutation，在 j 个不同 slots 的 images 上，相对 j 份独立 uniform [t_v] 值的点态密度≤t_v^j/(t_v)_j≤e^j；该界不依赖长度是否相同。取任意 k 条不同模板边，它们在每份 permutation 内涉及不同 slots，总2k个。不同原 v/layer 的 permutations 独立，所以全 covered 概率≤e^(2k)乘对应 p_e 的积。

with-replacement 参照中所有已选 slots 独立，不同模板边 slots 不交，所以各覆盖事件独立。非单射 images 在真实 permutation 中概率0，不破点态比较。若 Z 是这份 ψ 的 covered 边数，

\[
\mathbb E\binom Zk\le\frac{(e^2\mathrm{mbar})^k}{k!},\qquad
\mathbb E(1+s)^Z\le e^{e^2\mathrm{mbar}s}\quad(s\ge0).
\]

令 a=ρM′/2，由 mbar/a<1/(50g²)，Chernoff 给

\[
\Pr[Z\ge a]\le(e^3\mathrm{mbar}/a)^a
\le(e^3/(50g^2))^{\rho M'/2}
<e^{-\rho M'\ln g}.
\]

零均值时概率0，实数阈值无整数问题。

两侧 typed alphabet 大小可不同。可用 bit positions 总数 L=Σ_v t_v|Σ_{side(v)}|≤QN′ 做统一生成函数计数：

\[
KQ^{-gN'}\le(1+1/Q)^L\le e^{N'},\qquad
K\le e^{gN'\lambda}.
\]

这没有新增任何 labels，只是以上界 Q 计数。M′=dN′/2、ln g≥ℓ/2 和 d 的取值给 ρM′ln g≥250gN′λ。对全部 cost≤gN′ lists 并界，坏概率<exp(−249gN′λ)<0.001。故初始图以该高概率同时让所有 cheap copy lists cover<ρM′/2，允许最终 lists 在看到图后选择。

## 4. 原度数无界仍只需 B₀=40N₀S

cycle 数不能粗略用 N′/z_min 而丢失原质量；可按起始原 v 单独求和。

固定起始原 v 的一个 copy、长度 j≤G 的 layer 序列。实际 simple cycle 的相邻 layers 必不同，包括首末；否则某 copy 在同层用两条边，违反 matching。逐步揭该 walk 的 matching 邻居。一条 matching 查询同时揭两端相应 slots 的 images。条件于 simple prefix，最后当前 copy 与起始 copy 在最后一层的 matching 都未揭：arrival/first layers 不同，且之前未重访这些 copies。

揭当前的 fresh inverse slot 后，若其 template mate 指向别的原 vertex 而非起始 v，则闭合概率0。若 mate 位于起始 v，则其 slot 也 fresh（否则对应 partner 早已揭），起始 copy 编号也仍未使用。故在至少 t_v−G 个未用编号中，闭合概率≤1/(t_v−G)。不需要原类型在此条件下均匀。

起始原 v 有 t_v 个 copy，共至多 d^j 个序列，因此 rooted cycles 多计的上界给

\[
\mathbb EX\le\sum_v\frac{t_v}{t_v-G}\sum_{j=2}^Gd^j
\le2N_0S,
\]

因为 t_v≥z≥2G+1。这正说明 B₀ 不需按 N′ 膨胀，也不需原 max-degree 常数界。原平行 types 只让不同层出现真正 parallel edges；这些长2 cycles 已被计入，单边来回不计。Markov 给 Pr[X>B₀]≤1/20。

## 5. typed bucket repair 和全部 lists 的统一变化

初始 X≤B₀ 时，短 cycle vertices 并集≤GB₀。当前 degree 为 d，e 两端半径 G balls 合计 vertices≤2Σ_{j=0}^Gd^j。指定 bucket 是一份 matching，因此触及这些 vertices 的 bucket 边数≤GB₀+2Σd^j≤GB₀+4U。z≥GB₀+4U+1，故所需 f 存在。禁区基于输出 degree d，不涉及原 degree d_v。

同 original type/layer 换边保持每层 matching、bucket 大小、两侧机器/原类型、两个 typed alphabets 和投影表。远距给四端不同；新短 cycle 含一条新边时违反跨端点远距，含两条时要么仍违反远距，要么与旧 f 组成旧短 cycle（而 f 不在任何短 cycle）。所以不新增短环，并杀掉至少一条旧短环，≤B₀次终止，最终 simple 且 girth>G。

每次更改两条约束，对任何 ψ covered 数至多增加2，确定界同时适用所有 ψ。M′=zm*≥8B₀/ρ，因此最终统一 cover<ρM′/2+2B₀≤3ρM′/4<ρM′。非 FAIL 的 copied 原 perfect assignment 仍逐 edge type 满足，surjectivity 和 equal-fiber 数也只取决于原投影表，不受端点 copies 更换影响。没有把 projection relation 反向当成总函数。

## 6. capped bits、FAIL 和 uniform 位复杂度

由于 M₀≥1、N₀≥2、z≥5，所有 t_v≥5，故 K₀=dΣ_v(t_v−1)>0。实际有 dN₀ 份 permutations；整数 draws 数为给出的 K₀，不是 dN′ 或2dN₀(t−1)同长写法。R=ceil log₂(2000K₀)给 sampling FAIL≤1/2000。各 draw 的 range 由原 degree 和步骤预定、使用独立 bit blocks；条件于所有 draws 成功，接受值仍独立 uniform，概率证明使用的分布精确成立。

因此全部域内输入 FAIL≤.05+.0005<.1；NO 再扣<.001的列表坏事件，得到非 FAIL 且全部 cheap lists sound 的概率>.948，足够0.8。并未声称所有非 FAIL 都 sound。

Qγ≥1 给 Qρ³≥10⁹g⁸，数值 g、1/ρ 和 d 由显式 Q 的固定多项式控制。原点数、M₀及 degrees 显式列举；t_v=d_vz≤M₀z，N′=2M₀z，固定 G 时 S、U、B₀、z 都是显式输入的固定多项式。typed alphabets 明确列出，Q亦支付输入长度，即使某些右 labels 未被任何 edge 的像使用也不影响计费。

随机位硬上界可取 K₀ R ceil(log₂ t_max)，同样多项式；cycle 枚举、确定性字典序找边、BFS和≤B₀步 repair 都是固定 G 的多项式。若 G 变参不再保证指数独立于 G，Exact 已排除。没有在 binary g 或1/ρ 数值巨大且 Q 不支付长度时展开。

## 7. 第5项的条件 PCP 与 exact fibers

若原 π_e exact k-to1，保持表逐 type 继承就保 exact k fibers；simple/exact dregular/girth 都来自上述图结构，不要求 PCP 起点 biregular、constant-degree 或两侧点数相同。

同步 alphabet clone Σ_A×[L]、Σ_B×[L]，新映射 (α,s)↦(π_e(α),s)。每个 (β,s) 的原像数恰为旧 β 的 k，故 fibers和surjectivity原样保留。旧最优标签全用相同 index s=1，证明新 val≥旧 val；任意新赋值投影回旧 labels 满足所有新满足的边，证明旧 val≥新 val。因此 value恰保持，完美完备也保持。取 L=ceil(1/(Qγ))（至少1），新 Q′=LQ≥1/γ，合法域成立；算法参数 λ、d 要由扩充后的 Q′ 重算，不能仍用旧 Q。没有把 retraction padding 的非等纤维版本拿来替换这里的 paired clone。

固定 g、ρ、G 时，已知 fixed-error perfect-complete exact k-to1 PCP 若给常数字母表，则上述 clone 数及 d 仍为固定常数，输出为 constant exact degree、高围长、balanced simple 的随机源。第5项没有声称一般此类 PCP 的 alphabet 随 g 有 polynomial 上界；只有另给 Q=poly_ρ(g) 时才有 d=O_ρ(g)。若需 padding，LQ≤Q+1/γ 对该条件仍是 polynomial_ρ(g)。整个 PCP 链先固定参数再归约 SAT，不将其指数说成对 binary g 统一。

本次条件推导不需要替外部 PCP 定理投票。我此前实际读过新 primary Theorem1.6 的原陈述，但未在本次重审其证明。随机变换与确定性 promise 判别器复合只保证 NP⊆BPP；FAIL按YES处理保逐种子完备性，NO坏事件以概率扣除，不能升级为 P≠NP 下确定性归约。

## 8. 对象域明确化和最终状态

标准“投影游戏”已经包含各侧可取标签，即两侧 alphabet 非空。若要彻底避免把仅有“有限、Q=max≥2”的文字误读为允许空 Σ_A，则建议规范正文显式写1≤|Σ_A|、|Σ_B|。空左 alphabet 时单标签 val 本就不良定；这不是新概率证明反例。其余没有需修改 Exact 才成立的数学项。

最终：仅据 Exact 独立重构闭合，第1–4项及第5项条件数学无 standing fatal；尚未读作者 v4 proof。没有实现、没有有限实验作证，没有 UM compiler、新颖性或主目标真值升级。
