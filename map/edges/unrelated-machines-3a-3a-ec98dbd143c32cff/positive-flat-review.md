# 正 sparse-flat 表示、唯一全矩扩张与原 T 提取的本轮核对

本轮 primary core 是 `M-8a8102ce2db9454ba1ed5eae66e12724` v2（下记 POS），只读比较端是 `M-d2f0e90baf4440cab9efbffecfee709e` v2（下记 EXT）与 `UM-GLOBAL-MOMENT-NEARFLAT-EXTRACTION-v1` v4（下记 NF）。三对象的当前完整合同、正文及必要原 PDF 定理已实读。结论是：POS 的正表示结论与 EXT 的无正性唯一平坦扩张不能混同；在 NF 的原合同及精确 δ=0 子域，POS 的全部假设均已支付，并确实给原阈值 T 的支持调度以及原全空间 HS 规则的支撑计数解释。

该下游作用已由当前 canonical `um-positive-sparse-flat-to-original-t-hs-support-step` 精确覆盖。本轮复用其原文件与 SHA，不复制边、不扩大成 NF 全目标，不把其他包的旧说明文件另列为本包 asset。此外，本轮把 EXT 在 POS 本来的实正子域中推出 POS 整条结论的承重链完整写出，新增一条 accepted/unconditional/whole 边。正性是目标自身已给定的输入条件，既未由唯一性凭空推出，也不是开放前提；不新增对象。

## 1. 两个文献结论的准确区别

原文为 Laurent–Mourrain, *A Sparse Flat Extension Theorem for Moment Matrices*，冻结 PDF SHA256 `a79a6aae70263cdc0b15415f838df666cfb99d6a00ef87bb1dae381493478fad`。实读 Theorem 1.1、1.4、1.5、1.6、§2 的构造及 Theorem 3.2、§3.2 的 localizer 说明；并目视第3、9页核公式与条件。

取有限普通单项式集 C，要求 C connected to 1，且

\[
C^+=C\cup\bigcup_i x_iC,
\qquad \operatorname{rank}H_\Lambda^{C^+}
=\operatorname{rank}H_\Lambda^C=R.
\]

EXT 所对应的 Theorem 1.4/1.5 断言：存在唯一完整序列/泛函，其完整 Hankel 算子扩展给定数据且仍为秩 R。这里的唯一性是“同秩 flat 扩张”的唯一性，定理本身不要求 PSD，也不直接声称正测度。POS 所对应的 Theorem 3.2 在同一结构、Hankel 和秩条件之外要求实数据及截断正性，才给 representing measure。

两层如何衔接也可从原证明直接核对。§2 先选择列基 B⊆C，构造投影 φ:R[x]→Span(B) 及扩张 \(\widetilde\Lambda(f)=\Lambda(\varphi(f))\)。φ 是到商代数的正规形映射，满足 φ(fg)=φ(φ(f)φ(g))；对 u,v∈Span(C⁺)，原 Lemma 2.3 给 Λ(uv)=Λ(φ(uv))。因此在原截断矩 PSD 时，任意多项式 f 都有

\[
\widetilde\Lambda(f^2)
=\Lambda\bigl(\varphi(f)^2\bigr)\ge0.
\]

这一步把截断正性传到唯一完整扩张。再用原 Theorem 1.1（正且有限秩的完整矩）得到恰 R 个互异原子的正表示。不能删去上述正性步骤，单凭唯一全矩扩张就宣称正测度。

本轮新边还给一个不把 Theorem 1.1 当作额外黑箱的完整证明。先固定 POS 所量化的任意实、正、connected-to-1、rank-flat 截断数据。EXT 给实的完整 Hankel 扩张 \(\widetilde\Lambda\)，秩为 R。若 R=0，完整矩阵为零，零测度已经表示全部输入，以下处理 R>0。

从 PSD 的原 C 主矩选独立列基 B⊆C，|B|=R，故其 Gram 主块 G≻0。这里只选线性代数基，不要求 B connected。对任意有限单项式集 F⊇C，完整扩张的秩 R 使 rank M_F=R。将 B 放在前面，写

\[
M_F=\begin{pmatrix}G&U\\U^T&W\end{pmatrix}.
\]

G 可逆，而整块秩与 G 相等，Schur complement 必为 W−UᵀG⁻¹U=0。于是 M_F PSD。任意多项式的有限支撑都可放入这样的 F，所以 \(\widetilde\Lambda(f^2)\ge0\) 对所有 f 成立。这说明仅从正的原主块和 EXT 保持的完整秩，就已经把全矩正性真正支付。

令 K=ker H_{\widetilde\Lambda}，A=R[x]/K。K 是 ideal；全矩 PSD 与 Cauchy–Schwarz 表明 K 恰为平方范数零的多项式，因此

\[
\langle[p],[q]\rangle=\widetilde\Lambda(pq)
\]

在 A 上是正定内积。dim A=rank H=R。各变量的乘法算子 Mᵢ:[p]↦[xᵢp] 良定、自伴且两两交换。有限维实谱定理给同时正交分解 A=⊕ₛEₛ，其中 Eₛ 对应互异实 joint eigenvalue zₛ∈Rᵈ。

v=[1] 是循环向量，因为所有 [p]=p(M)v 张成整个商代数。投影到 Eₛ 后，p(M)v 在该空间的投影总是 p(zₛ)Pₛv。循环性强制 Eₛ=span(Pₛv)，所以每个 Eₛ 一维且 Pₛv≠0；从而恰有 R 个互异 zₛ。令 wₛ=‖Pₛv‖²>0，则对任意多项式 p，

\[
\widetilde\Lambda(p)
=\langle v,p(M)v\rangle
=\sum_{s=1}^{R}w_sp(z_s).
\]

故正有限原子测度 \(\mu=\sum_sw_s\delta_{z_s}\) 表示完整扩张，也表示全部原 C⁺·C⁺ 数据。这完整推出 POS 的原句，包括未归一化数据及 R=0 边界。不需要 localizer 即可表示在 Rᵈ；若要支撑在另给半代数集合上，仍须目标本来要求的相应 localizer 核对。本边不提供原子计算算法，也不声称任意表示测度的唯一性；这里的同时对角化只用于存在性证明，不是 NF 的有理实现。

一个归一化的精确界限例：一变量、C={1,x}、C⁺={1,x,x²}，取 y₀=1，yₖ=−1（1≤k≤4）。则

\[
M_C=\begin{pmatrix}1&-1\\-1&-1\end{pmatrix},\qquad
M_{C^+}=\begin{pmatrix}1&-1&-1\\-1&-1&-1\\-1&-1&-1\end{pmatrix}
\]

都秩2，C connected。EXT 给唯一同秩完整扩张；它正是有符号泛函 2 ev₀−ev₁ 的全矩序列。然而 Λ(x²)=−1，连平方正性都不满足，因此无非负表示测度。这个例子只说明“删除正性后的推论”错误，不反驳 EXT 或 POS 的原陈述，也不另建反例节点。

## 2. connected-to-1 与列基不是同一个条件

原第3–4页的 C={1,x³} 例说明，仅有1、PSD及同秩仍不足。选其参数 a=0,b=1，则按索引 (1,x³,x,x⁴) 的 C⁺ 矩为

\[
\begin{pmatrix}
1&0&1&0\\0&1&0&1\\1&0&1&0\\0&1&0&1
\end{pmatrix}\succeq0,
\qquad \operatorname{rank}M_C=\operatorname{rank}M_{C^+}=2.
\]

但 C 不 connected。原文的核递归条件排除其同秩全扩张；正测度也不可能，因为 y₀=y₁=y₂=1 强制 x=1 几乎处处，却有 y₃=0。

另一方面，C connected 不保证任意满秩列基 B⊆C 也 connected，甚至一般不保证存在这种 B。原第9页给 C={1,x₁,x₁x₂}、秩2的例；可取含1的列基 {1,x₁x₂}，它不 connected。Theorem 1.6 以 B connected 为前提，不能凭 C connected 就直接套用。一般 EXT 使用 §2 的核、φ 与次数归纳解决这件事。本轮不把某个有理消元所得列基的连通性当作免费假设。

## 3. NF 原输入如何真正支付 POS 的全部假设

保持 NF v4 的原合同：n,d≥1，T>0，0<η≤1；原合法端先剪枝到 0≤pₑ≤T，每个任务 Eⱼ 非空；给定同一显式有理 degree≤4 的 normalized Boolean/one-hot `C2-load(T)` 矩 y。M₂ PSD，逐任务守恒成立到 degree4；每机原负载 localizer 对所有 affine q 有

\[
L(g_iq^2)\ge0,
\qquad g_i=T-\sum_{e\text{ 在 }i}p_ex_e.
\]

不要求逐个四阶条目非负，不加入 prefix-count localizer。所有任务、端及机器共享同一 y，不能换成逐机边际。

把 reduced 表提升到普通 R[xₑ] 的次数≤4泛函 \(\widehat L\)：重复变量幂按 Boolean 合并，含同任务不同端的项置0，其余读 y。归约由普通单项式唯一决定，故乘积相同的普通 Hankel 条目确实一致。

取 C={1}∪{xₑ}。此 C 显然 connected，C⁺是所有普通次数≤2单项式。令 F 是普通系数到 compatible reduced 系数的归约映射，则

\[
M_{C^+}(\widehat L)=F^TM_2(y)F.
\]

F 满射：每个 reduced 单项式本身就是一个普通单项式。平方行复制一次行，同任务冲突行全0。因此普通提升矩 PSD，且与 reduced M₂ 同秩；C 主子矩正是 M₁。

在共同 Gram 商空间中，V₁⊆V₂，Π 投影到 V₁，Xₑ[q]=[xₑq]，Aₑ=ΠXₑ，Bₑ=(I−Π)Xₑ。NF 原证明在上述弱合同内给

\[
D_e=A_e-A_e^2=B_e^*B_e\succeq0,
\qquad \delta=\sum_e\operatorname{tr}_{V_1}D_e.
\]

现在限制精确可检验的子域 δ=0。各 Dₑ PSD，迹和0强制每个 Bₑ=0；因此所有 [xₑx_f]=Xₑ[x_f] 都在 V₁，V₂=V₁。反向若秩相等，则 V₂=V₁，所有 Bₑ=0。故

\[
\delta=0\iff \operatorname{rank}M_2=\operatorname{rank}M_1
\iff \operatorname{rank}M_{C^+}=\operatorname{rank}M_C=R.
\]

y∅=1 排除 R=0。这精确支付 POS 的普通 Hankel、实域、PSD、connected-to-1、秩不增所有前提。这里 δ=0 是本已证明步骤的输入子域限制，没有未付的开放数学前提。常数向量上的缺陷为0不能替代全 V₁ 迹：原正文指出合法非平坦矩也可在该向量上缺陷为0。

## 4. 正表示何以给原任务、恰 R 原子及原 T 容量

POS 给有限正表示

\[
\mu=\sum_{s=1}^{N}w_s\delta_{z_s},
\quad w_s>0,\quad\sum_sw_s=1,
\]

先合并重复原子。Boolean 归约给 \(\widehat L((x_e^2-x_e)^2)=0\)，该式次数4；正性使每个原子 zₛ,ₑ∈{0,1}。one-hot/同任务互斥给 \(\widehat L((\sum_{e\in E_j}x_e-1)^2)=0\)，故每个原子每个原任务恰选一个原合法端。

在 L²(μ) 中，M₁、M₂ 的秩分别是 affine 与二次多项式的评价空间维数。同秩使两空间相等；于是每个坐标乘法保持 affine 评价空间。该空间含1，故反复乘坐标后包含一切多项式评价。有限互异 Boolean 原子可由其0/1坐标乘积指示多项式逐个隔离，因此 affine 评价空间就是 Rᴺ，N=R。这里只使用高次多项式作为支撑上的函数，不调用不存在的高阶输入矩。

于是每个原子 s 都有 affine qₛ 满足 qₛ(zₜ)=1 当 t=s，否则为0。对每机，gᵢqₛ² 的次数≤3，处于给定四阶数据及原 affine localizer 范围内。因此

\[
0\le\widehat L(g_iq_s^2)
=w_s\bigl(T-\operatorname{load}_i(z_s)\bigr).
\]

正权使每个原子同时满足所有机器 loadᵢ≤T。由此所得确是原 T 支撑。localizer 在非平坦一般矩上的逐原子推断不能省去这里的 affine 隔离依据；也不能把线性负载 localizer 擅自代入高次完整调度指示函数。

## 5. 原全空间 HS 规则数支撑，不数概率质量

数学等距同构

\[
U:[q]\longmapsto(\sqrt{w_s}q(z_s))_{s=1}^{R}
\]

把 Aₑ 变为 diag(zₛ,ₑ)。故各 Aₑ 是交换的0/1正交投影，每任务投影正交分割 I。任何选端前缀的乘积 K 都是 joint projection，并有

\[
\|K\|_{G\text{-HS}}^2
=\operatorname{tr}K
=\#\{s:z_s\text{ 满足该前缀}\}.
\]

孩子分数是相应的支持原子数，各合法孩子分割父支持。初始为正整数 R；每轮选最大孩子，至少保持1。全部原任务处理完后，完整指派至多对应一个互异 Boolean 原子，故最终 count=1，输出必在 μ 的原 T 支撑上。该论证允许任意预定任务顺序及固定输入顺序破平局。

同一前缀的测度质量却是

\[
\|Kv_0\|_G^2
=\sum_{s\text{ 相容}}w_s,
\qquad v_0=[1].
\]

两者通常不同。已实读的 canonical 三原子例取两任务、两机器、全部 p=0、T=1，原子 (0,0)、(0,1)、(1,0) 的权分别为1/100、1/100、49/50。第一任务的两孩子 HS²为(2,1)，质量为(1/50,49/50)：HS 会选支撑较多的低质量孩子，仍有真实支撑。该例已有精确有理证据，本轮不重复计算或另造资产。

## 6. 有理分裂与总位复杂度

在 M₁ 中选有理独立列基 b。其用途仅是坐标运算，无须声称 b connected。设

\[
G=L(bb^T),\quad H_e=L(bb^Tx_e),\quad
A_e=G^{-1}H_e,\quad Z^\dagger=G^{-1}Z^TG.
\]

G 正定；所有算子、迹及 HS 分数都用有理数精确计算。只取一调度时运行原 HS 规则即可。要恢复全部正权原子时，从 v₀ 出发，按任务将每个非零分支 u 分成所有 Aₑu，删除 G 范数0的分支。不同分支正交，每层至多 R 个；完成后每支为一个原子，权 \(\|u_s\|_G^2>0\)，是有理数，权和为1，并重构输入四阶矩。无需计算上面的平方根、一般特征值或无理特征向量。

精确有理消元的行列式界控制 G⁻¹ 与各固定 Aₑ 的位长。取固定算子条目的共同分母 Q，每个长度≤n的乘积可用分母 Qⁿ；分子位长随 n、log R 及固定算子位长多项式增长。每层至多 R 支、各候选总数为输入规模多项式，故按显式 (P,T,η,y) 的总编码长度计为位多项式。没有按1/min wₛ、1/δ、1/T或条件数运行的隐含循环。

## 7. 与完整 NF、矩寻找及既有 canonical 的边界

POS 在本比较中只支付 NF 的精确平坦步骤。δ>0 时不存在上述精确 joint projection/count 结构；完整 NF 的交换子误差、任意前缀近幂等、不塌缩下界、selected-loss 和共同密度矩阵证明由 NF 自身正文另行支付。本页不把这些已另证的部分说成本条经典正表示迁移的结论，也不把它们记成本条关系尚未证明的前提。

NF v4 的原合同要求 pₑ≤T，才有强式 (1+3δ)T；未剪枝时只能保原文的 T/(1−3δ) 弱式，不能互换。δₑ=0 时 loss=0，严格 <3δₑ 只适用于 δₑ>0；当前合同和主审查已修正该边界。T=0、n=0 可在外层处理，但本页保持 NF 核心 n,d≥1、T>0 合同，不宣称所有大缺陷零目标矩自动被核心接受。

给定有理共同矩的校验、提取与从普通 (P,T) 寻找矩是不同问题。POS/EXT 都不是 SDP 点或 NF 证书生成器；本页不提供生成算法，不给可靠 FAIL 语义，NF 拒绝不能推出 OPT>T。NF 正文的原 T 普适小缺陷生成障碍另依赖半单位3DM归约，不是本轮新增结果，也不在此重证。

写新边前，当前 registry 的2262条 canonical 边只作精确端点扫描：POS 唯一 incident 边就是上述 accepted step，没有 EXT→POS 同问题边；EXT 的另一条入边属于 connected column basis 的不同问题，本页不读其对端对象、不扩张比较。既有 NF→PREFIX 文件只用于确认原 canonical 已明确区分 HS count 与常数向量权，以及正 δ 的 T′ law；其 PREFIX 端点不是本任务新覆盖或前提，不据此制造额外 read-add 或新边。

最终复用的原边文件 SHA256 为 `9861647925a6cc723294921f0a19b26131fbea401c8e370b5cc81a4eba26cc35`，源/目标 pins 与本轮 POS v2/NF v4 完全一致。它的 `contribution` 已准确标为 δ=0 的已闭合算法步骤，`remaining` 保留全 NF 范围与矩寻找边界。本轮新增 `um-connected-flat-extension-to-positive-atomic-representation`，以 EXT 为源、POS 为目标，§1 的 Schur/正商代数证明覆盖 POS 整条正表示结论。本轮 primary-core 覆盖为 linked；两个比较都记在收据 `comparison_dispositions`，任务没有 formal follow-up，故 `closed_overlaps=[]`。

## 8. 本轮实读与操作界限

本轮实际读取：AGENTS.md、prompts/03-map-worker.md、IMPLEMENTATION.md 第三阶段及收据接口；当前 task 与父 Boss 提供的完整三对象合同导出；共享文献页全文（承重为§2）；原 PDF 必要定理和证明、原 NF 正文全文、当前主审查全文、共同有理 Gram 资源全文；既有 canonical step 全文及其 proof、三原子证据全文；NF→PREFIX canonical 文件全文仅作上述去重。

本轮没有把旧包记录的“已读全部 refs”继承成本轮实读范围，也没有重跑历史科学计算。只写本 task 的 write_paths；没有执行 Git、work.py、native 队列、全局 registry/coverage/integration 或 spawn。原 PDF 目视截图为临时阅读产物，交付前移除。父 Boss 负责最终 native 检查、保存与队列动作。
