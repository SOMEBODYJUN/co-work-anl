# 有界配置任务数的槽包络严格离二：陈述先行的独立重构

Internal independent statement-first review, 2026-10-18. The author algorithm/proof notes have not been read. Scope: supplied feasible equal-coverage CONFIG(T) point with at most K positive jobs in every positive-weight configuration. No global novelty claim, no external review, no repository edits. This result does not establish UM-TARGET-v1.

## Verdict and stronger independently reconstructed statement

The proposed bound with D_K=(K+1)! K^K is valid. In fact, for K>=2 the following stronger bound follows from the configuration marginals alone:

    every row's full standard ST slot envelope <= (2-K^(-(K-1))) T.

For K=1 the envelope is at most T. Every covering matching respects the envelope, so the same bounds hold for every covering matching. The result does not assert sharpness of the displayed K-dependent bound.

Only positive-weight source configurations need the cardinality bound. The union of their eligible jobs may have arbitrary size. Zero-eligible jobs may be assigned to a zero edge globally and removed as in the proposed statement.

## Definitions and boundary cases

Take T>0 and scale processing times by T. Fix one row. All its remaining finite positive processing times are denoted p_j. A supplied configuration distribution y_C has sum_C y_C=1, each supported C has |C|<=K and sum_{j in C}p_j<=1, and x_j=sum_{C contains j}y_C. Empty configurations are allowed.

Order the positive-x jobs by nonincreasing p_j, with arbitrary fixed ties. Put their x_j-length intervals consecutively from 0. Make unit slots and join a job to a slot precisely when their intervals have strictly positive intersection. Let rho=sum_j x_j<=K, and q=ceil(rho). If rho=0 the envelope is zero. Otherwise q<=K. Let a_s be the largest processing time adjacent to slot s, s=1,...,q. Then the full envelope is sum_s a_s. Supported jobs have p_j<=1, hence a_1<=1. If q=1 the proof is complete.

At T=0 every positive job would make CONFIG infeasible; after zero-job removal only the empty case remains. No division by zero is needed.

## 1. Strict threshold-prefix inequalities

For each s=2,...,q,

    sum_{j:p_j>=a_s} x_j > s-1.                 (1)

Indeed, take the earliest job in the row order which intersects slot s. Its right endpoint is strictly larger than s-1, and all jobs through that job have size at least a_s. This proves (1), including equal sizes and integer slot boundaries. The positive-intersection convention is essential for the strict inequality.

Write d=q-1 and b_t=a_(t+1), t=1,...,d, so b_1>=...>=b_d>0.

## 2. Compress each source configuration into at most d types

For each job j of a supported source configuration, if p_j<b_d, discard it. Otherwise assign it to the smallest index t for which p_j>=b_t. Let c_t be its type counts. Then

    c in Z_+^d, sum_t c_t<=K, c dot b<=1.

Ties assign to the earliest equal threshold. Thus, for every t, the prefix c_1+...+c_t is exactly the number of original configuration jobs with p_j>=b_t. The induced distribution on the finite set S of count vectors consequently has prefix means

    H_t = E[c_1+...+c_t] > t,    t=1,...,d.    (2)

No source job identities are merged in the actual rounding algorithm; this compression is used only to prove a one-row numerical bound.

## 3. A fixed integer polytope has objective strictly below one

Keep this induced distribution and its count-vector support S fixed. Consider the d-dimensional polytope

    P_S = {z_1>=...>=z_d>=0 : c dot z<=1 for every c in S}.

The actual threshold vector b belongs to P_S. Since H_1>1 and c_1 is integral, some c in S has c_1>=2. Its inequality and z>=0 imply z_1<=1/2. Hence P_S is closed and bounded. It is nonempty and full-dimensional: sufficiently small strictly decreasing positive z satisfies every nonzero configuration inequality strictly.

For z in P_S, summation by parts gives

    E[c dot z]
      = sum_{t=1}^{d-1} (z_t-z_(t+1)) H_t + z_d H_d,

while

    sum_t z_t
      = sum_{t=1}^{d-1} (z_t-z_(t+1)) t + z_d d.

All coefficients are nonnegative. If z is nonzero at least one coefficient is positive; (2) then yields

    sum_t z_t < E[c dot z] <=1.                (3)

For z=0 its objective is also strictly below one. Compactness therefore ensures a maximizing vertex z* with sum_t z*_t<1.

## 4. Integer determinants make the strict gap uniform

A vertex uses d linearly independent active constraints. Their coefficients are integers and their right-hand sides are either 0 or 1. A configuration row has Euclidean norm at most sum_t c_t<=K; an order row has norm sqrt(2)<=K for K>=2; the terminal nonnegativity row has norm 1.

Let Q>=1 be the absolute determinant of the active d-by-d matrix. Hadamard's inequality gives

    Q <= K^d.

Cramer's rule gives sum_t z*_t=N/Q for an integer N. Since this rational number is strictly below 1,

    sum_t b_t <= sum_t z*_t <=1-1/Q <=1-K^(-d).

Adding a_1<=1 yields

    envelope <=2-K^(-d) <=2-K^(-(K-1)).        (4)

This is stronger than 2-1/D_K because D_K=(K+1)!K^K>=K^(K-1). For K=1, q<=1 and the earlier direct bound is T.

All rows satisfy (4) simultaneously. Every integral covering matching uses at most one job from each slot, so its row load is at most the envelope even when one job appears in several slot neighborhoods. Hall existence follows from the given x's job coverage and slot capacities, as in standard ST matching.

## 5. Exact low-K examples and actual full-instance matchings

The row examples below attain the listed envelope; they are not merely bounds on a surrogate. Add a distinct unit job B with small positive singleton configuration weight eta=1/100. Multiply the listed other configuration weights by 1-eta. For every job j, add a private machine on which only j is eligible, with size 1. Its configuration distribution is singleton {j} of weight 1-x_j and empty of weight x_j. This makes every job's global coverage exactly 1. Every source configuration contains at most K jobs.

The all-private schedule has makespan 1, and B has size 1 on every eligible machine, so the full ordinary-UM instance has OPT=1. For the central row, choose the job attaining each slot maximum; in these examples those jobs are distinct. Match all other jobs to their own private slot. This is a genuine covering matching with row load equal to the full envelope.

| K | Lower nonunit levels | Configuration count vectors and original weights | Envelope |
|---|---|---|---|
| 1 | none | singleton only | 1 |
| 2 | 1/2 | (2), weight 1 | 3/2 |
| 3 | 1/2, 1/3 | (2,0), weight 2/3; (0,3), weight 1/3 | 11/6 |
| 4 | 3/8, 1/3, 1/4 | (2,0,1), weight 5/9; (0,3,0), weight 1/3; (0,0,4), weight 1/9 | 47/24 |

For K=2 and K=3 the envelopes are sharp: (1) implies that some configuration contains at least s jobs of size at least a_s, so a_s<=1/s. Thus the bounds 1+1/2 and 1+1/2+1/3 hold for q<=2 and q<=3, respectively, and the table attains them.

For K=4, the original prefix means are 10/9,19/9,28/9; mixing the unit singleton with any eta in (0,1/19) preserves the strict thresholds. Exact arrangement-vertex enumeration found 47/24 as the largest candidate, but this note does not promote that computation into an independently reviewed sharp-K4 theorem. The explicit lower example is fully verified using rational arithmetic.

Exact full-instance and matching audit: bounded_k_slot_envelope_certificates.py. Exploratory exact-vertex/LP search: bounded_k_slot_envelope_search.py. The latter uses floating LP to locate weights, then verifies the returned rational certificate exactly; it is not the basis of the general proof.

## 6. Algorithmic wrapper and scope

For fixed K, all job subsets of size at most K can be explicitly enumerated for each row in O(m n^K) configurations. At a given rational T, retain those with load at most T, solve the equal-coverage rational LP, and perform ST slot matching. The bit complexity is polynomial in the explicit input for fixed K. The general proof does not require solving the small auxiliary proof polytope P_S.

If a separate input promise says some optimal schedule uses at most K positive jobs per machine, then the bounded-cardinality CONFIG LP is feasible at T=OPT. Its first feasible threshold T* is at most OPT, and the rounding gives the displayed K-dependent approximation relative to ordinary OPT. One can search the sorted set of all row subset sums with at most K jobs; it has polynomial size for fixed K and polynomial bit length.

Without that promise, the first feasible bounded-cardinality threshold can exceed ordinary OPT or fail to exist (for example n>Km). Thus this is not a uniform epsilon improvement for unrestricted UM, nor may K grow with the input while keeping the same fixed polynomial running-time claim.

## 7. Primary-source comparison

Page--Solis-Oba--Maack, COCOA2018 accepted author PDF:
https://drpage.pagewizardgames.com/COCOA2018_dpage_solis_maack_accepted.pdf .
Definition in Section 1, PDF p.2, bounds |J_i|, the total number of eligible jobs on a machine. Theorem 2, PDF p.11, gives ratios 1,3/2,5/3 for eligibility bounds 2,3,4. This differs from a support-configuration cardinality bound: a machine here may have arbitrarily many distinct eligible jobs while each source configuration contains at most K.

Its related-work discussion, PDF p.4, cites Saha--Srinivasan (ICS2010), *A new approximation technique for resource-allocation problems*, for a 2-approximation with machine cardinality capacities. That citation warrants follow-up before a novelty claim; it is not evidence that the present determinant bound was already proved there. No such novelty claim is made.

Verschae--Wiese's familiar 11/6 bounded processing-time-spread result uses the same threshold-prefix ancestry. The present proof handles arbitrary size spread under a different bounded-configuration-cardinality hypothesis. Standard ST matching and integer-polytope determinant bounds remain known ingredients.


---

# 有界配置槽余量：冻结独立重构后的规范全文实读审查

Date: 2026-10-18. Reviewer: literature_new_bridge, internal boss4 researcher.

## Independence and exact reviewed bytes

The statement-first independent draft remains unchanged:

- /workspace/scratch/6bd6916818c5/bounded_k_slot_envelope_statement_first_review.md
- SHA256: 69a4a75069a8ffcb5eb05607c182685344ed9da9dc8b22de575e3d2c8ce09f84

That draft was frozen before reading the author's proof notes or the canonical proof. It independently reconstructed the stronger bound 2-K^(-(K-1)) and gave the low-K examples. This separate append records a later actual full read of the canonical text and is proof-aware, not a second blind review.

Actually read in full and hashed before and after the checks:

| File under /workspace/scratch/6bd6916818c5/co-work-anl-boss4/ | SHA256 |
|---|---|
| research/current/unrelated_machines/bounded_configuration_cardinality_slot_margin.md | 8f32aa1662305c493a28418f646ac320bb82257833faa320c572b6f88b26a345 |
| tests/audits/unrelated_machines/bounded_configuration_cardinality_slots.py | bd3ca0fe16d8473ced1aa4005ecca3f9957347656013c821d7930b8c4e4a4b4f |
| evidence/runs/unrelated_machines/bounded_configuration_cardinality_audit.json | b2c3a0694d2956a7c95b679d10eab6bacd84bd9fc4b9795fd8d4b3763b9a4505 |

No shared files were edited.

## Actual mathematical review verdict

No fatal or material defect found in the precise statements, full proof, approximation wrapper, or example table at the above hash.

The following obligations were checked against the full text, not merely its outline:

1. Removing globally zero-eligible jobs preserves OPT and all other configuration marginals; merging duplicate residual configurations preserves row normalization. Feasible T=0 becomes empty after this preprocessing.
2. Every positive-weight residual configuration has cardinality at most K, so the positive row mass and slot count are at most K. Empty rows and the one-slot case are separated before using d=q-1.
3. Positive slot intersection yields strict threshold-prefix mass >s-1, including equal processing times and exact integer boundaries. Earliest admissible threshold assignment keeps prefix counts exact when threshold values coincide.
4. The auxiliary polytope keeps the induced count support and its distribution fixed. H_1>1 gives a count vector with c_1>=2 and hence compactness. Abel summation is strict for every nonzero ordered nonnegative vector; the zero vector's objective is also below one.
5. A maximizing vertex has d independent integer active constraints, with right-hand sides 0 or 1. Configuration rows have norm at most K and order/nonnegativity rows have smaller norms. The determinant argument yields the stated uniform gap with the correct inequality direction.
6. The same global covering matching simultaneously realizes all row bounds; the type compression is only a numerical proof device. No independent per-row matching is substituted for the actual global output.
7. The unknown-OPT wrapper enumerates only cardinality-at-most-K subsets and their exact rational sums. Under the separately stated optimal-cardinality promise, feasibility at OPT ensures T*<=OPT. Fixed-K column count, threshold count, and encoding lengths are polynomial. No ordinary-OPT claim is made without the promise.
8. The table's K2 and K3 sharpness follows from the harmonic threshold count bound plus actual matching examples. K4 is accurately labeled only as the explicit lower example 47/24. Page's total eligibility bound is correctly distinguished; no global novelty or unrestricted-UM theorem is asserted.

The canonical implementation is deliberately a finite certificate audit, not a generic configuration-LP solver. Its documented limitation is accurate. The mathematical algorithm may invoke standard deterministic rational LP algorithms; the absence of their integration is not hidden.

## Actual verification performed

Reran the canonical audit into a new scratch file, without overwriting frozen evidence. The JSON objects and the bytes match the frozen JSON exactly. Scratch rerun:

- /workspace/scratch/6bd6916818c5/bounded_configuration_cardinality_canonical_rerun.json
- SHA256 b2c3a0694d2956a7c95b679d10eab6bacd84bd9fc4b9795fd8d4b3763b9a4505

Wrote a separate exact Fraction boundary checker that does not import the canonical code. It validates source configuration feasibility, exact global coverage, zero-job deletion and configuration merging, constructs the full slot graph, and exhaustively enumerates all covering matchings on its small instances.

| Independent case | Covering matchings checked | Maximum makespan / T |
|---|---:|---:|
| Empty jobs, T=0, K=1 | 1 | zero |
| K=1 with equal-size ties | 2 | 1 |
| All-zero T=0; original configuration has two jobs before deletion | 1 | zero |
| Zero-edge job originally partly assigned on a positive edge; duplicate residual configurations merge | 1 | 1 |
| K=1, large processing-time and weight denominators | 2 | 1 |
| K=2, tiny positive interval and exact integer boundary | 6 | 3/2 |
| Canonical K2 data, reconstructed as full central/private point | 6 | 3/2 |
| Canonical K3 data, reconstructed as full central/private point | 34 | 11/6 |
| Canonical K4 data, reconstructed as full central/private point | 201 | 47/24 |

The large-denominator test uses T=(2^91+17)/(2^127-1), weights 1/(2^149+37), and processing-time perturbations with denominator 2^173+23. The near-boundary K2 test additionally uses singleton mass 1/(2^191+51), retains all strictly positive intersections exactly, and attains 3T/2. No floats, sampling, or tolerance is used in this checker.

Independent checker:

- /workspace/scratch/6bd6916818c5/bounded_k_slot_boundary_independent.py
- SHA256 80ab6048d79df687cf06672cf37b443a5b3ae2761e4feb9f2e475b5db0b3242b

Frozen scratch output:

- /workspace/scratch/6bd6916818c5/bounded_k_slot_boundary_independent.json
- SHA256 824faa4af886c0ed8adcadbe4001de6899518b0cc404065967be5263a2130e99

These are finite implementation checks supporting the explicit cases, separate from the general proof. They do not establish K4 sharpness, global novelty, an implemented generic LP solver, or the unrestricted UM target.


---

# 有界配置任务数槽余量的证明知情最终审查

## 独立性时间顺序与实际范围

审查者最先提出较弱的固定 `K` 分母界 `ε_K=1/[(K+1)!K^K]`，并将完整候选冻结在 `bounded_cardinality_slot_margin.md`，SHA-256 为 `abd995b13928f0ee64ccd1f7c1ffdacbea2f68c27639edc80b27fd432d48acab`。该稿没有进入 canonical，不能把它写成已经登记的旧定理。

另一位研究者只收到原先较弱的精确声明，未读取本审查者证明，独立重构并改进为 `ε_K=K^{-(K-1)}`。随后 root 把更强证明的整数类型多面体、Abel严格不等式及行列式思路发给本审查者；本审查者已据该思路做过证明知情核对。因此，**本文件是原较弱候选作者的证明知情实际读后审查，不是更强定理的盲审或独立声明先行重构。** 独立重构者的原始冻结审查另存，不能与本次时间顺序混淆。

本次已实际全文读取如下 canonical 正文、审计代码和冻结记录：

| 资产 | SHA-256 | 实际覆盖 |
| --- | --- | --- |
| `research/current/unrelated_machines/bounded_configuration_cardinality_slot_margin.md` | `8f32aa1662305c493a28418f646ac320bb82257833faa320c572b6f88b26a345` | 第1–6节全部文字与公式，包括小K实例和未知OPT算法 |
| `tests/audits/unrelated_machines/bounded_configuration_cardinality_slots.py` | `bd3ca0fe16d8473ced1aa4005ecca3f9957347656013c821d7930b8c4e4a4b4f` | 全部代码、构造、槽边、匹配、源哈希及元数据 |
| `evidence/runs/unrelated_machines/bounded_configuration_cardinality_audit.json` | `b2c3a0694d2956a7c95b679d10eab6bacd84bd9fc4b9795fd8d4b3763b9a4505` | K=2、3、4全部证书和输出元数据 |

**实际读后结论：该冻结版本无承重数学异议。** 本结论不包含外部同行评审、全球新颖性认证、一般UM近似结论或未实现的通用LP软件。

## 更强余量的逐项核对

1. **输入与零边。** 有零端的任务可独立移到零端并删除，非负性保证OPT精确保留；从原配置中删掉这些任务仍保持其余任务覆盖、配置归一化及容量。`T=0` 下可行点使每个原任务有零端，预处理后为空。剩余有限端均正，所以正槽最大值严格正。无任务、空行和单槽行都按正文处理。
2. **槽数与严格前缀。** 配置平均任务数 `u≤K` 给 `q=ceil(u)≤K`。第s槽有严格正交长，故大小至少该槽最大值 `a_s` 的任务质量严格超过 `s−1`。同值任务合成同一大小前缀仍成立；恰整数端点不连零交长边，不能把严格号误写成由零边产生。
3. **类别与重复阈值。** 去掉首槽、设 `b_t=a_{t+1}`。每个配置任务归到满足 `p_j≥b_t` 的最小下标，并忽略 `p_j<b_d` 的任务，则前t类恰为 `p_j≥b_t` 的任务集。重复阈值必须归入最早类别，正文已明确。计数非负整数、总数≤K，且替换为所属阈值不会增处理时间，故 `c·b≤1`。
4. **多面体紧性与严格目标。** `H_1>1` 使某支持类型 `c_1≥2`；所有坐标非负，因此其容量行给 `z_1≤1/2`，结合排序，整个多面体有界。对任意非零有序非负向量z，至少一个Abel系数严格正，每个前缀均值 `H_t>t`，故 `E(c·z)>Σz`。可行性又给 `E(c·z)≤1`，所以全部非零可行目标严格小于1，零目标也小于1。
5. **整数行列式的统一差距。** 最大值在顶点达到。取d条独立活约束，类型行的二范数≤K；排序行范数 `sqrt(2)≤K`（本段K≥2）；非负行范数1。Hadamard给整数行列式 `1≤D≤K^d`。右端只有0、1，所以顶点目标是 `N/D`；严格小于1迫使 `N≤D−1`。因此尾槽和≤`1−K^{-d}≤1−K^{-(K-1)}`，加首槽≤1即得正文界。这里并没有对原有理时间作网格舍入，也没有把本地新计数分布拼成全局调度。
6. **实际同一匹配。** 全局任务—槽分数匹配来自原始共同x，Hall覆盖不依赖证明中Q的优化。每个真实槽任务大小≤该槽最大值，所以同一覆盖匹配同时兑现全部行上界。正文正确声称任意覆盖匹配，而不是免费生成一份最优调度分解。

## 小K锐性与完整有限实例

由前缀均值严格超过 `s−1`，某个真实配置至少有s枚大小≥`a_s`的任务，故 `a_s≤1/s`。这给K=2的3/2、K=3的11/6包络上界；K=1则精确为1。

正文及代码的K=2、3实例确实有对应的完整普通UM坏匹配，分别达到3/2、11/6。K=4的配置计数层 `(2,0,1),(0,3,0),(0,0,4)` 在大小 `(3/8,1/3,1/4)` 下均负载1，D0在两个配置中保持同一原任务。以小正权unit配置混合后，中心四槽最大值为 `1,3/8,1/3,1/4`，且可选择不同原任务，实际值47/24。没有把K4有限下界升级为一般锐界。

对每个中心任务j，私有机配置可显式取singleton `{j}` 权重 `1−x_j` 与空配置权重 `x_j`。二者非负且归一化，任务总覆盖 `x_j+(1−x_j)=1`；私有机时间1使这些配置均在T=1可行。未选中心任务全部匹配各自私有槽，中心所选任务匹配其实际正交槽边，所以是完整合法ST覆盖。全部任务放私有机给上界1，而unit任务B所有可用端均时间1给下界1，因此普通OPT恰1。

“锐”在此针对完整槽包络和**任意匹配**保证的最坏允许输出。正文已正确说明：这些例子存在更好的完整匹配/调度，并未证明最佳槽匹配、整个算法或配置LP自身有对应近似困难性。

## 未知OPT算法与失败语义

对固定K，显式列出每行大小≤K的全部有限端任务子集，配置数和子集负载候选数均为 `O(mn^K)`。每个配置总负载是输入有理数之和，位长多项式；配置集只在候选子集和断点处改变。若承诺某个普通OPT调度每机≤K个无零边任务，其所有实际行配置必在所列集合内，因此候选集含OPT（非空正实例），且截断CONFIG(OPT)可行。第一个可行目标 `T*≤OPT`，随后的实际ST输出满足所列比例。

此证明不需要一个免费OPT oracle，不需要中间输出集合单调；使用的只是截断LP可行性随阈值单调。显式LP与有理匹配的位复杂度按固定K成立，K无界时没有统一多项式声明。所有候选均不接受只能排除K基数有界调度；正文没有把它误写成无承诺输入上的 `OPT>T`。

把K限制为固定值的义务仍承重。仅限制“大件数”、并把tiny工作量另收费会产生配置相关的有理剩余容量，不能直接沿用统一整数右端1的本证明。主目标仍OPEN。

## 实际重跑与额外独立核对

本次实际重新执行 canonical 脚本，并把其完整JSON对象与冻结记录作精确相等比较，连同 `source_sha256`、命令、Python3.12.14和算术元数据均一致；另核当前脚本哈希等于记录的源哈希。

还写了不调用作者槽构造函数的短独立 `Fraction` 核对：从冻结的配置、边际和所选任务重建各中心行的排序区间；显式构造每个私有机的空/singleton配置；逐任务核总覆盖1、逐配置核归一化及负载≤1；逐个中心匹配边核严格正交长；对其余任务用私有机重算完整调度负载。三组均分别得到3/2、11/6、47/24。

这些有限核对只覆盖给定低K完整证书，不实现通用配置LP，不证明所有K上的一般界或任何K4最优性。普遍结论来自上述严格前缀、整数类型多面体及行列式证明。没有发现尚未解决的承重异议。


## 规范独立审计的可恢复路径（主研究者实际核对）

原独立审计未调用主审计核心。入库时唯一行为外改动是把冻结输入的scratch绝对路径
改为相对脚本所在仓库的路径，以便环境重置后重跑。主研究者实际通读完整代码并重跑，
输出的六个边界与三组全部覆盖匹配核对通过。
规范代码：tests/audits/unrelated_machines/bounded_configuration_cardinality_independent.py，SHA256 04b5db9779a66fab10c39492dbea2ae4ffcf2ef7612e1a3c6914b4f40dd39d29。
冻结结果：evidence/runs/unrelated_machines/bounded_configuration_cardinality_independent.json，SHA256 b02f458ecab334f0aa963ca0f29caddc2167b5ad077d75eb10a4f924f938646c。
此记录不倒改此前独立声明重构及原始实际读稿的时间顺序。


## K5扩展的实际独立核对

boss14主研究者先由计数超平面枚举发现K5候选，再由另一子代理收到显式五层配置后，
独立展开全部15任务16机的原矩阵、CONFIG与有序槽。此审计知道候选数据，不称盲审。
主研究者实际读完整代码，并另用不调用其构造核心的Fraction程序从JSON重建每机配置归一化、
每任务覆盖、两份完整匹配的槽注入及正交长、所有机器负载，结果一致。
这验证正文§4.1下例，未新增一般K上界或主目标结论。

- 扩展正文 SHA256：`14c1b00b50a8b87f9aa30e5bbe77300516943a60e68073b123582e074ffe79f4`。
- 独立展开代码 SHA256：`450d41b4e7dbe1289a6c02e31c87703114a92a371087906c168b02fb23bc8972`。
- 新冻结证据 SHA256：`e335e6db53e109cd0a09a121e9390418d2f79fb49ec3f7b9895c3082e4a20d2c`。

实际坏匹配287/144、好匹配1，单位任务下界使OPT1；阶乘候选差1/720由Fraction反算。
旧K2–4冻结记录与审查原字节均保留，仅追加本扩展记录。
