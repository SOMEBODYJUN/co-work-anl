# 正规高围长部分 Min-Rep 源 v3：冻结证明读后攻击

审查者：内部子研究者 pcsp_occurrence。实际读取并攻击作者冻结证明 `regular_high_girth_partial_minrep_v3_root_frozen_proof.md`；读前、读后 SHA256 均为 `f43e32fa61899de87121c161e3ca51ac76dbaa47daccef5fce7a02ba8609e646`。其 Exact 的 SHA256 为 `0e2b614ae0a0af12c592d3b57558e2c3baf13cf4377b90b26769fc6e5d24cc61`。本稿是读后审查，不冒称新盲审；较早真正 Exact-first 的独立重构保留原字节，SHA256 为 `f9c965c6a8b608ba088e135444c4cc8f19c7ed36798b5259c397b84b09b26396`。

结论：在 Exact 全部对象域和量词下，无 standing fatal。作者以 factorial moments 替代我盲稿中的有界度 witness，证明更简且给更强尾界；无需把 matching 边指示变量假设为负相关。短 cycle 的 fresh-image 暴露论证同样有效。没有新软件实现、有限随机实验或新增外部文献审查声明。

## 1. 点态密度与 factorial-moment 承重步骤

固定 copy lists 后，对每个原 edge type e 记 p_e 为独立均匀选择其两端 copies 所得到的覆盖概率。全部模板边的边际之和记为 mbar；作者第1节给 mbar<tau M′。该步骤直接处理各 copies 完全不同的 lists，未把平均 copy lists 偷换成某个成本受限的原 lists。heavy-copy 端概率由 D-regularity 精确控制，随机单标签赋值的抽样在不同原 vertices 间独立，包含 n=1 情形。

对一份 uniform [t] permutation 的 j 个不同 slots，其 images 相对于 j 份独立 uniform [t] 值的密度上界为 t^j/(t)_j。对任何非单射 tuple，真实概率为0；对单射 tuple，该密度为常数。因为 ln t,ln(t−1),...,ln1 递减，前 j 项平均不小于全部 t 项平均，

(t)_j >= (t!)^(j/t) >= (t/e)^j,

故密度至多 e^j，对 j=0,t 两端均成立。无需把 j 限制到 t/2。

任取 k 条不同模板边。每层模板是 perfect matching，所以同一原 vertex/layer 中涉及的 slots 确实不同；总 slots 数恰为2k。所有原 vertex/layer permutations 独立，联合点态密度至多 e^(2k)。在 with-replacement 参照分布中，每个 slot image 独立；不同模板边使用不交 slots，因此其覆盖事件也独立，即便原图有 parallel types。于是

Pr[所选 k 边全 covered] <= e^(2k) product p_e,
E binom(Z,k) <= (e² mbar)^k/k!.

有限随机变量恒等式 E(1+s)^Z=sum_k E binom(Z,k) s^k 对 s>=0 合法，故 <=exp(e² mbar s)。这里不存在由条件 MGF 嵌套导致指数损失的问题。

取 a=rho M′/2。mbar/a<1/(50g²)，所以 e²mbar<a。选择 exp(theta)=a/(e²mbar)，得到

Pr[Z>=a] <= (e³mbar/a)^a <= (e³/(50g²))^a < exp(−rho M′ ln g).

mbar=0 时概率0；a 非整数没有漏洞。e<3 即足以给 e³<50。作者这里比我的 witness 尾界强约一倍，且常数远有余量。

廉价 lists 的生成函数计数、ln g>=ell/2 和 d 的取值给全局坏概率 <exp(−249gN′lambda)<.001。对所有 copy lists 的 union bound 在 repair 前一次完成；后来 lists 可依赖输出图，仍被该同时性覆盖。

## 2. 短 cycles 的 fresh-image 暴露

固定起始 copy vertex 和长度 l 的 layer 序列。相邻 layer 不同（含首末）是实际 simple cycle 的必要条件，因为每层为 matching。若不满足，贡献0；l=2 必须是不同层的两条 parallel edges，单边往返不计 cycle。

沿序列查询实际 matching 邻居时，一次查询同时揭两端 permutation 对应 slots 的 images。故此前已揭过的该层 matching 边，其两 copy 端点均在已经访问的 walk vertices 中。条件于一个 simple prefix，最后当前点的 last-layer incident matching 边未揭：其 arrival layer 不同，且当前 copy 没有在更早访问过。起始目标的 last-layer matching 也未揭，因为首层不同，且起点没有提前重访。

揭当前 copy 的 fresh inverse-permutation slot 后，其 template mate 若指向别的原 base vertex，则闭合概率0。若指向起始 base vertex，mate slot 仍未揭：若曾揭 mate，其匹配 partner slot 也早已揭，矛盾。其 fresh image 在该 permutation 尚未用的 copy 编号中 uniform，目标编号也未用；此前最多 l 个 relevant images，故闭合概率 <=1/(t−G)。这不要求 next type 均匀、不要求原图 simple，也没有把构造误认为保持原每条边各 copy degree 的 D-cover。

因此 E X <= Nt S/(t−G)<=2NS，按 rooted/directed walks 多计仅加强上界。Markov 给 cycle FAIL <=.05。参数 t>=2G+1 已足够本证；无需调用我先前较粗的完整 slot/image 枚举。

## 3. 同 type/layer repair 与同时 soundness

当前所有短 cycles 顶点并集大小 <=GB。一份 bucket 始终为 matching 且大小 z，故触及这些坏 vertices 的 bucket 边数 <=GB。e 两端半径 G balls 合计 vertices <=2 sum_{0..G}d^j；每 vertex 在同 layer 只有一条 bucket 边，触及 balls 的候选数不超过该顶点数。Exact 的4U更保守。因此 z>=GB+4U+1 保证候选 f 存在。

远距保证四端不同并排除新 parallel edges。含一条新边的短 cycle 给旧图跨 e/f 端点的短 path；含两条新边时，删去它们后的两条旧 paths 要么跨 e/f（违背远距），要么分别连接 e 两端和 f 两端，其中后者与旧 f 组成旧短 cycle（违背 f 不在任何短 cycle）。没有新短 cycles，至少杀掉所选旧 cycle，所以 <=B 步终止。

每次只换两条约束，任意 lists 的 covered 数增加至多2。M′=tm_*>=8B/rho，故最终对全部 cheap lists 仍同时 covered<rho M′/2+2B<=3rho M′/4<rho M′。projection types、每层 matching、degree 和 perfect-complete copied assignment 全保持。

## 4. bounded sampling、域条件和解释范围

作者第6节写有2dN份 permutations，是实际 dN 份的保守多计。于是实际 draws 为 dN(t−1)，其原 R 给 sampling FAIL <=1/2000；使用作者多计的 draws 上界则只得到 <=1/1000。两者都有效，前者更强；这是弱化 FAIL 上界，不改变算法或随机分布。各 draw 的 range 预定、使用独立 bit blocks，因此条件于全部 draws 成功，所有接受值仍独立且 uniform，permutations 恰服从概率证明使用的分布。

Qgamma>=1 给数值 g 和 1/rho 为显式 Q 的多项式；Q 由非空显式投影表计入输入长度。固定 G 时 d,S,B,U,z,t 以及 bounded random bits、cycle 枚举和 repair 均为总位多项式；不延伸到 binary G 变化而指数仍统一的合同。regular 的两侧允许原 parallel edge types，输出消除 parallel 2-cycles 后 simple。Qgamma<1 不在主算法域，不能不说明便对它宣称输出。

随机 source corollary 须继续区分固定 g,rho,G 的 PCP 归约与该图变换本身的统一位复杂度；FAIL 可以由调用者按 YES 分支处理，但不是伪造的高围长游戏。NP不包含BPP 是足够的明确假设，本稿不把此归约升级为确定性 NP-hardness 或 UM near2 困难性。高围长/simplicity 源并不解决实际调度的 label fee、trigger 或 π 解码。

## 5. 对本人旧 Exact-first 稿的非致命勘误

旧稿第4节写“z>GB+4U+1”；应改读为“z>=GB+4U+1>GB+4U”。Exact 只保证第一个非严格不等式。排除候选数至多GB+4U，正确的末尾严格不等式仍保证 f 存在，所以不影响接受结论。旧冻结稿原字节保持不改，本稿单独记录此自我勘误。

最终状态：作者 proof 所有承重步骤审查通过，无 standing fatal；不是新颖性认证、不是生产软件验证，UM-TARGET-v1 保持 OPEN。
