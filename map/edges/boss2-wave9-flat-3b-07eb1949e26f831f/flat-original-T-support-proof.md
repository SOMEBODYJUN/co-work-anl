# 正 sparse-flat 表示到原 T 调度的精确平坦步骤

本比较只把 `M-8a8102ce2db9454ba1ed5eae66e12724` v2 的正 sparse-flat 表示定理应用于 `UM-GLOBAL-MOMENT-NEARFLAT-EXTRACTION-v1` v4 的 δ=0 普通子域。该子域内的推导全部闭合，关系为 accepted、unconditional、step；δ=0 是可精确检验的输入限制，不是等待证明的开放前提。本页不支持 δ>0 的定量 NF 定理整体，不产生一个新的 PREFIX law 边，也不声称一般调度输入上的矩证书生成。

## 1. 固定输入与两端点的合同

保持 NF 目标既定域：给定原 unrelated-machines 实例的合法端集合 E，n,d≥1，目标 T>0，剪去 p_e>T 后每个任务 j 的 E_j 非空，所有保留端满足 0≤p_e≤T；0<η≤1。给定同一份显式有理 degree≤4 矩 y，y_∅=1。变量 x_e 对应原任务的原合法端；重复幂按 x_e²=x_e 合并，含同任务不同端的单项式值为0。每任务的 one-hot 恒等式乘以任意兼容 degree≤3 单项式后成立。兼容 degree≤2 单项式索引的 M₂(y) PSD；每机器 i 的 affine 负载 localizer

\[
L(g_iq^2)\ge0\quad\text{对每个 affine }q,
\qquad g_i=T-\sum_{e\text{ 在机器 }i}p_ex_e
\]

成立。这里只需弱 C2-load(T) 合同，不添加逐条目非负或 prefix-count localizer。

设 V₂ 是共同 M₂ 的零范数商 Hilbert 空间，V₁ 是其中常数与一次单项式生成的子空间，R=dim V₁=rank M₁。由 y_∅=1，R≥1。Π:V₂→V₁ 为正交投影，X_e[q]=[x_eq]，A_e=ΠX_e，B_e=(I−Π)X_e。NF 原正文§3在以上合同内证明 X_e 良定，A_e 自伴且 0≤A_e≤I，并有

\[
X_e^*X_e=A_e,\qquad D_e=A_e-A_e^2=B_e^*B_e\succeq0.
\]

本页额外固定可检验的子域 δ=Σ_e tr D_e=0。它自动满足 NF 数值阈值；以下论证直接工作在这个精确子域，不调用任何正 δ 的扰动估计。

## 2. 从 reduced 输入到普通 Hankel，及 δ=0 的精确意义

在普通交换多项式环 R[x_e:e∈E] 的 degree≤4 部分定义 \(\widehat L\)：把每个单项式的重复幂合并；若出现同任务不同端则值置0；其余读取相应 y_S，再线性延拓。普通单项式乘积有唯一的上述归约，所以这给出真正满足 Hankel 一致性的普通矩数据，而不只是一个缺失平方行的 reduced 表。

取普通单项式集 C={1}∪{x_e:e∈E}。C connected to 1；其 border closure C⁺ 恰为所有普通 degree≤2 单项式。C⁺ 中 x_e² 的行等于 x_e 行；同任务两个不同端的行全0；其余行正是原 reduced M₂ 的行。更精确地，若 F 把普通 coefficient vectors 归约为兼容 coefficient vectors，则

\[
M_{C^+}(\widehat L)=F^TM_2(y)F.
\]

F 满射且包含各 reduced 单项式对应列，故普通矩 PSD，与 reduced M₂ 同秩；其 C 主子矩即 M₁。

每个 D_e=B_e*B_e PSD。迹和 δ=0 强制每个 B_e=0，而非仅强制 B_e[1]=0。因此对所有 e,f，[x_ex_f]=X_e[x_f] 属于 V₁；这些二次向量连同一次与常数张成 V₂，故 V₂=V₁。反向若 rank M₂=rank M₁，则 V₂=V₁、Π=I，所有 B_e=0。因此

\[
\delta=0\quad\Longleftrightarrow\quad
V_2=V_1\quad\Longleftrightarrow\quad
\operatorname{rank}M_{C^+}=\operatorname{rank}M_C=R.
\]

这准确支付 M8a 的 connected-to-1、实数据、PSD 和 rank-flat 输入合同。这里 C 的连通性显式成立；算法后来选取的独立列基 b 只用于线性代数，不需要声称任意 b 也 connected to 1。

## 3. 正表示测度、Boolean 合法性与恰 R 个原子

应用 M8a 正 sparse-flat 表示定理，得到表示全部普通 degree≤4 数据的有限正原子测度。先写成

\[
\mu=\sum_{s=1}^{N}w_s\delta_{z_s},\qquad
w_s>0,\quad z_s\in\mathbb R^d\text{ 互异},\quad
\sum_s w_s=\widehat L(1)=1.
\]

此处只使用 M8a 本身的正有限表示结论；无需把另一个代数扩展对象作为额外前提。Laurent–Mourrain 原 PDF 的 Theorem 3.2 给正表示，Theorem 1.1 解释平坦扩展的原子数。下面也在本子域直接证明 N=R，避免把任意表示的原子数当作免费假设。

对每端 h_e=x_e²−x_e，Boolean 归约给 \(\widehat L(h_e^2)=0\)，而 h_e² 的普通次数为4。因此

\[
\sum_s w_s(z_{s,e}^2-z_{s,e})^2=0
\]

强制每个 z_{s,e}∈{0,1}。对每任务 a_j=Σ_{e∈E_j}x_e−1，one-hot 及同任务互斥给 \(\widehat L(a_j^2)=0\)：平方项的期望和为1，交叉项为0，一次项的和为1。因此每个原子满足 Σ_{e∈E_j}z_{s,e}=1，恰选该原任务的一个原合法端。没有改变任务、机器或端身份。

在 L²(μ) 中，M₁、M₂ 的秩分别是 affine functions 和 degree≤2 functions 的评价像维数。它们都等于 R，所以每个 degree≤2 function 在 μ 支撑上等于一个 affine function。于是每个坐标乘法 z_e 都保持 affine 评价空间：乘 affine 得 degree≤2，再用上述相等降回 affine。常数1也在此空间，反复乘坐标表明所有多项式在支撑上的评价都在其中。

不同的有限 Boolean 原子可由多项式隔离，例如

\[
f_s(x)=\prod_{e:z_{s,e}=1}x_e
\prod_{e:z_{s,e}=0}(1-x_e)
\]

在支撑上的评价恰为第 s 个单位向量。这里只把 f_s 当作 L²(μ) 中的函数，不要求它的高次矩已输入或另外可计算。故 affine 评价空间已经是全部 R^N，N=R。这证明该测度恰有 R 个正权互异合法原调度原子。

## 4. affine 单原子插值让原 localizer 逐原子生效

令 E_val 为 (d+1)×R 的评价矩阵，其第 s 列为 (1,z_{s,e})_e。由正表示，

\[
M_1=E_{\rm val}\operatorname{diag}(w_s)E_{\rm val}^T.
\]

rank M₁=R，w_s>0，故 E_val 列满秩。评价映射从 affine polynomials 到 R^R 满射。因此每个 s 都有 affine q_s，使 q_s(z_t)=1 当 t=s，其他 t 为0。

原 g_i 为一次，q_s² 为二次，故 deg(g_iq_s²)≤3，完整处于给定 degree4 数据和原 affine localizer 的范围内。对每一机器 i，

\[
0\le\widehat L(g_iq_s^2)
=w_s\left(T-\sum_{e\text{ 在 }i}p_ez_{s,e}\right).
\]

正权 w_s>0 给每个原子同时满足所有机器 load_i(z_s)≤T。故这是真正原 T 的支持，而非增广目标的支持。一般低阶伪矩没有这里的 affine 插值满射；仅有一些 localizer 不能直接跳到逐原子容量。

该平坦支撑论证本身即使保留长端也成立，长端会被支持约束排除；本边仍保持 NF 已剪枝的目标合同，不借此扩张其正 δ 强式范围。

## 5. L² 评价下的原压缩乘法与 HS 支持计数

映射

\[
U:[q]\longmapsto (\sqrt{w_s}\,q(z_s))_{s=1}^{R}
\]

由 V₁ 到 R^R 为等距同构。flat 给 X_e(V₁)⊆V₁，故 A_e=X_e 在这个表示中就是 diag(z_{s,e})。于是所有 A_e 两两交换，且为0/1正交投影；同任务的投影两两正交且和为I。平方根只用于数学解释，算法不计算它。

对相容前缀 S，令 K_S 为所选 A_e 的乘积。它是满足该前缀的原子坐标上的正交投影。因此

\[
h(K_S)=\|K_S\|_{G\text{-HS}}^2
=\operatorname{tr}(K_S)=\operatorname{rank}(K_S)
=\#\{s:z_s\text{ 满足 }S\}.
\]

NF 指定的孩子分数 \(\|A_eK_S\|_{G\text{-HS}}^2\) 就是满足 S 及 e 的支撑原子数，是非负整数。每个未分配任务的合法孩子把父支持准确分割，因此其分数和等于父 count。初始 h(I)=R>0，每步最大孩子分数至少1；固定输入顺序的任意平局规则都保持正整数 count。全部 n 个任务处理完后，完整指派至多对应一个互异 Boolean 原子，故最终 count=1。原全空间 HS 算法输出的正是 μ 支撑中的某一个原 T 可行原调度。

测度的前缀概率质量是另一个量：v₀=[1] 时

\[
\|K_Sv_0\|_G^2=\sum_{s:z_s\text{ 满足 }S}w_s.
\]

一般并不等于 h(K_S)，最大 HS 孩子也不必有最大概率质量。该 distinction 不影响支撑非空证明。

## 6. 一个完全有理的 count 与 mass 分离例

取两任务、两机器，四个原合法端的处理时间都为0，T=1。三个支持原子（元组依次给任务0、任务1的机器）及权为

| 原子 | 权 |
|---|---:|
| (0,0) | 1/100 |
| (0,1) | 1/100 |
| (1,0) | 98/100 |

写 a=x_(machine0,job0)、b=x_(machine0,job1)。基 (1,a,b) 的评价矩阵可逆，G 的行列式为49/500000>0，M₁、M₂ 秩均3，δ=0。它是原 C2-load 的真实平坦证书。

先处理任务0：机器0孩子的 HS²=2，概率质量1/50；机器1孩子的 HS²=1，概率质量49/50。原 HS 必选机器0这个低概率分支，仍保留两个真实支持原子。下一任务两孩子 count 都是1；按机器0先行破平局输出 (0,0)，其正权为1/100。随附 JSON 保存全部9个 reduced 矩值、G、四个有理 A_e 和精确核验；这是有限说明例，不代替上面的全称证明。

## 7. 不用谱 oracle 的有理提取与总位复杂度

用精确有理 Schur/LDL 或秩消元在 M₁ 中选单项式独立基 b，包含常数1可优先选取。G=L(bbᵀ) 为正定有理矩阵，H_e=L(bbᵀx_e)，并定义

\[
A_e=G^{-1}H_e,\qquad Z^\dagger=G^{-1}Z^TG,
\qquad\|Z\|_{G\text{-HS}}^2=\operatorname{tr}(Z^\dagger Z).
\]

G、H_e、A_e 及全部比较分数都是有理数。输入校验、秩、逆矩阵和迹的计算均为精确有理线性代数；处理零 pivot 时须同时检查剩余零对角块无非零条目，不能把非PSD的零对角块误收。rank0 被 y_∅=1 排除。一般正 sparse-flat 的实原子坐标未必有理，本 Boolean 子域已证明原子坐标为0/1。

若只需一个调度，直接实现上一节的原 HS 最大分支即可，最多 d 个候选 R×R 矩阵乘积，R≤d+1。若需恢复完整测度，从有理 v₀=[1] 开始，按任务把每个现有非零 u 分成所有 A_eu，丢弃 G 范数平方0的孩子。不同孩子及不同父节点的非零向量互相正交；每层至多 R 个。最后每条分支对应一个支持原子 s，其权为 \(w_s=\|u_s\|_G^2>0\)，是有理数，权和为1。这个分裂只用有理投影，不求一般特征值、特征向量或 G 的平方根，不接收造矩时的原子作为 oracle。

全部输入矩可以重构：每个 ordinary degree≤4 单项式拆成两个 degree≤2 单项式 m₁,m₂；其矩值是 V₂=V₁ 中 [m₁]、[m₂] 的内积，等于 Σ_s w_s m₁(z_s)m₂(z_s)，与原 y 一致。此完整 law 和矩重构结论在既有 NF→PREFIX 边已经存在，本节只把有理实现同本页的源定理应用对齐，不新建该终点关系。

设 B_in 为显式 (P,T,η,y) 的总输入位长。矩阵阶、条目数及校验式数均为 B_in 的多项式。消元/行列式界使 G⁻¹、A_e 的条目位长为多项式。取所有固定 A_e 条目分母乘积 Q 作共同分母，则任意至多 n 步乘积的分母可取 Q^n，分子位长至多 O(n(log Q+log R+max log(1+|Q A_e[a,b]|)))。n,R 和 log Q 都是输入位长多项式；加上 G 范数、迹及最多 R 个分支仍为总位多项式。没有按1/δ、1/T、1/min_s w_s 或条件数迭代的隐藏循环。

## 8. 与现行 canonical 边的精确去重与剩余范围

实读既有 accepted `um-nearflat-hs-pruned-support-to-common-prefix-law`，文件 SHA256 `576e3c28bee648bf224c66ac4059633c7f6a4d812f7d6918ba604886cf765493`。它以 NF 为源、PREFIX 为目标：正 δ 下给剪枝保留叶的 T′=(1+3δ)T law；δ=0 下已给 commuting joint projections、v₀ 正权、原 T law 与四阶矩重构。

本页源为通用正 sparse-flat 表示 M8a，终点为 NF 的一个已证明算法子步骤。新增可复用作用是普通 Hankel lift 的完整核对、用 affine 单原子插值支付原 localizer 的逐原子原 T 支持，以及 HS² 精确等于支撑原子计数的谱解释和有理实现。这不是再造 NF→PREFIX 的另一条 law 边。PREFIX 只作只读去重比较，follow-up 在该精确比较范围关闭；不抢 M8a 或 NF 原3A内部主覆盖。

已正式 read-add 的 `UM-PREFIX-ATOMIC-DECODING-v1` v4 要求同一归一非负 law 对任意相容部分指派守恒、每个完整原子逐机局部化，以及按位多项式查询。其 body§3、完整 canonical 原正文与全部登记 evidence 已实读并核 SHA。平坦测度可取 π(S)=Σ_{s 满足S}w_s，准确满足这些要求；这里的 π 是权重和，而 h(K_S) 是计数。既有 canonical NF→PREFIX 边已经负责该端点关系，故本包不再发布到 PREFIX 的新边，也不把正 δ 的 h 误当精确守恒概率。

本边剩余（相对于整个 NF 目标）为 δ>0 的 noncommutative commutator、任意前缀 near-idempotence、最大分支的定量下界及 selected loss 的定量估计。这些已有 NF 自身正文证明；它们不由本条经典正表示迁移支付，也不是本条关系的开放数学前提。普通实例的证书生成和失败语义仍是另一个问题，本页没有解决或新增其困难性证明。

T=0 的同一 flat 支撑论证也给0负载，n=0 可直接取空分配 Dirac；这些只是边界说明，不把核心 NF API 改写成对所有大缺陷零目标输入都接受。原 source§6 的严格号最后一步只在 δ_e>0 成立，δ_e=0 时 loss=0；现 NF v4 与主审查已经明确修正，本页沿该已修正合同。

## 9. 实读证据与检查界限

- 已核 actualtask claimed/Boss2、当前 registry 的 M8a v2/NF v4 与精确 pins；读 AGENTS.md、IMPLEMENTATION.md 的实际阶段/边/收据合同及 prompts/03-map-worker.md。
- M8a 共同文献页指定§2完整实读；Laurent–Mourrain 原 PDF SHA256 `a79a6aae70263cdc0b15415f838df666cfb99d6a00ef87bb1dae381493478fad` 的12页全文实际抽读，并目视第3、9、10页，核 C connected、普通 Hankel、Theorem 3.2 与 localizer 应用的次数。
- NF 主审查指定§二、完整原证明、冻结增量、共同 rational Gram 资源、独立 HS 资源、有限审查、六输入证书页、未归档配置审查全文及指定§6均已完整实读并逐文件核 SHA。有限21/6 fixtures 和强 helper 的额外条件只作为证据范围，未重跑旧科学程序，也未拿运行 PASS 代替证明。
- 当前任务 read-add 后仍 claimed/Boss2，request `6041ec5adede4a97b96140f436045e3b`，definition canonical SHA256 `331782b11fe1dbb54944748b7b62091001c6c500fbd68beb8598083ee6d2da7a`。PREFIX v4 pin `8a54b4990271f92b3532688d041d6e81792fa3cc5a4fe8db671c45d50864f528` 的完整 record、body§3与五个去重后 evidence 文件均已实读核字节；不扩大到它们提及而本任务未需的外部算法。
- 既有3D审查 SHA256 `e4910f2d56f9d8a8570b2448a198888ebce8f01eee988be7fd62015eca752a70` 与外部数学草稿仅用于定位和复核。本页重新核 source 合同，承重论证全部写在正文中；没有借用未加入任务的 Md2 对象。
- 随附 count/mass 例只作当前短有理算术核验。作者没有执行 Git、native queue、registry、全局 projection 或 token 读取；发布、绑定及队列交付由父 Boss 串行办理。
