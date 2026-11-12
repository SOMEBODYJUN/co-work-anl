# connected 稀疏索引、connected 列基与正表示的三层比较

本包 primary 是 `M-d2f0e90baf4440cab9efbffecfee709e` v2（EXT），共享比较端是 `M-eeb1beecbe7345c29aae65f41841b671` v2（BORDER）与 `M-8a8102ce2db9454ba1ed5eae66e12724` v2（POS）。三份完整当前合同与实际登记记录逐项一致。本轮只复用已经 canonical 的 `um-5c01b2-commuting-border-basis-connected-column-flat-extension`，其完整文件 SHA256 为 `7107cb24a26f8f84a0b4949a21c8606b55935096668c8f210c971289477372b3`；不复制同一条件贡献边。

实际结论如下。BORDER 在额外存在 connected-to-1 满秩列基 B 的分支中，支付 EXT 的全局商基与正规形构造；这仍是对一般 EXT 的局部贡献，不能把本分支的完整证明等同于目标全量词的完整支持。完整次数层由原 Proposition 3.1 支付额外 B 条件。一般稀疏 C 不保证这种 B，原 §2 用 C 的前缀归纳和 Hankel 核结构绕过这一条件。最后，EXT 不要求正性；POS 在自身实正子域中另支付正性保持及有限秩正表示。本轮已实读正在发布的 EXT→POS whole 证明，确认它与前述入边承担不同步骤；未把该尚未 canonical 的文件列成本包复用资产。

## 1. 原合同及实际读取

共同来源是 Laurent–Mourrain, *A Sparse Flat Extension Theorem for Moment Matrices*。冻结 PDF SHA256 为 `a79a6aae70263cdc0b15415f838df666cfb99d6a00ef87bb1dae381493478fad`；共同中文正文 SHA256 为 `0b07529b7a2db2b592942290f8a9d8a3c030387c348afd5c772e0dbc1d00f254`。本轮直接由冻结 PDF 提取并读取全文，其中初次工具输出遗漏的 p.5–6 又单独完整读取；精核 pp.5–8 的 Theorem 1.6、(2.1)–(2.8)、Lemmas 2.1–2.3、全局构造和唯一性，及 p.9 的 Proposition 3.1、列基反例、Theorem 3.2。按 pdf skill 目视 p.5 与 p.9，公式、矩阵及实际条件与提取文本相符。没有把旧包的阅读声明当作本轮实读。

设 K 为域，C 为有限普通单项式集，1∈C，且 C connected to 1；令

\[
C^+=C\cup\bigcup_i x_iC,\qquad
V=\operatorname{Span}(C^+),\qquad
\Lambda\in\operatorname{Span}(C^+\!\cdot C^+)^*.
\]

数据须有 Hankel 一致性，即矩阵条目只依赖单项式乘积，并满足

\[
\operatorname{rank}H^{C^+}_\Lambda
=\operatorname{rank}H^C_\Lambda=r.
\]

EXT 的原结论是唯一完整同秩 Hankel 扩张：存在唯一完整泛函或完整矩序列，保持全部 C⁺·C⁺ 数据且全矩秩为 r。它量化任意满足这些条件的 C，不只量化完整次数层，不要求 PSD。唯一性只针对同秩 flat 扩张；不能自行扩大为任意高秩完整扩张的唯一性。

BORDER 的实际输入是某个有限单项式集 B、它的 border rewriting family F 以及依 F 定义的变量乘法矩阵 χᵢ；Theorem 1.6 要求实际 B connected to 1。其结论为：χᵢ 两两交换，当且仅当 B 是 K[x]/(F) 的基。这个 B 条件不是较大索引集 C 的连通性。

POS 保留 EXT 的结构和 rank-flat 条件，另要求实数据及截断正性。其结论是在 Rⁿ 上存在有限正原子表示，表示全部原数据。半代数支撑需要另外核对应 localizer；普通实正表示本身不需要 localizer。

## 2. flat Hankel 先支付哪些局部代数事实

记 N=ker H^{C⁺}_Λ。由 flat 性，C 的列已经张成 C⁺ 的列空间，故对 p∈V，

\[
p\in N\iff \Lambda(ap)=0\quad(\forall a\in C).
\tag{A}
\]

因此有原 (2.2) 的截断核闭合：若 p∈N 且 xᵢp∈V，则 xᵢp∈N。确实，对 a∈C，有 xᵢa∈C⁺，所以 Λ(a xᵢp)=Λ((xᵢa)p)=0，再用 (A)。该论证只在乘积实际落于原定义域时使用，不把截断核预先当作全环理想。

r=0 时 C⁺ 主矩阵全零，零完整泛函是唯一秩0扩张。以下取 r>0。此时 1∉N：否则沿 C⁺ 中的逐变量前缀反复使用截断核闭合，会把每个 C⁺ 单项式放入 N，与 r>0 矛盾。C 的类张成 V/N，故可从 C 选一个含1的列基 B，|B|=r；商上的非退化对称双线性型使对应主块 H^B_Λ 非退化。这里保证的是“可含1”，没有保证 B connected。

令 W=Span(B)，则 V=W⊕N。记沿 N 到 W 的投影为 π，设 f(p)=p−π(p)，并取

\[
F=\{m-\pi(m):m\in\partial B\},\qquad
\chi_i(b)=\pi(x_i b)\quad(b\in B).
\]

因为 B⊆C，所以 xᵢb∈C⁺，这些定义确实可由原数据给出。若 xᵢb∈B，则 χᵢ(b)=xᵢb，因而它们正是 F 所定义的 border 乘法算子。

原 Lemma 2.1 证明所有 χᵢ 交换，无需 B 连通，也无需正性。展开 χᵢχⱼ(b)−χⱼχᵢ(b)，其中可能超出 V 的最高项 xᵢxⱼb 相消；余下的关键项是

\[
x_i f(x_j b)-x_j f(x_i b)\in V.
\]

它与任何 a∈C 配对为零，因为 axᵢ、axⱼ∈C⁺，且 f(xⱼb)、f(xᵢb)∈N。由 (A) 它在 N 中；其他项本已是 F 中元素的线性组合。因此整个交换子既在 W 又在 N，只能为0。这里使用了截断 Hankel 配对及 flat 核；不能把任意一组非连通 B 上的 border prebasis 都自动赋予这些性质。

## 3. connected 满秩 B 分支实际完成的贡献

若额外确有 B⊆C connected to 1、|B|=rank H^B_Λ=r，则上一节的 χ 交换可以直接调用 BORDER，得到 B 为 K[x]/(F) 的真实基。商的正规形为

\[
\varphi(p)=p(\chi)1.
\]

沿 C 的前缀与截断核闭合，可核 φ 在 V 上就是 π。随后在 W 上使用非退化对称型 ⟨u,v⟩=Λ(uv)，各 χᵢ 对此型自伴；于是正规形完整保持所有原乘积配对，而不仅是单个 C⁺ 索引。定义 Λ̃(p)=Λ(φ(p))，得到保持全部 C⁺·C⁺ 数据的完整泛函，秩恰为 r。border 关系 F 落入任意另一秩 r 完整扩张的核，商正规形强制另一扩张与 Λ̃ 相同。

这些正是现有 canonical 条件贡献边完整写明并已支付的内容。就这个加强子域而言，存在性、数据一致性、秩及唯一性都已闭合；就原 EXT 的“任意 connected 稀疏 C”而言，它仍只是 contribution-step，因为额外的 B 存在条件没有免费获得。

完整次数层 C=Mₙ,ₜ₋₁ 为什么可进入该分支？原 Proposition 3.1 用次数相容的单项式序，在 C 中贪心选择最大独立列集 B，证明 B division-closed，因此 connected to 1。其承重点也可从局部核看清：若某个前驱 m 已由较小列线性表示，则关系 m−Σc_b b 在截断核；若 xᵢm∈C，所有 xᵢb 仍在完整次数层中，截断核闭合使 xᵢm 被更早列表示。所以贪心保留 xᵢm 时必须保留其前驱。完整次数层支付了这些被乘单项式仍在 C 中的条件；一般稀疏 C 不能复用这一支付。

原 §3.1 给出精确分离：C={1,x₁,x₁x₂} 本身 connected。a≠1 时

\[
H^C_\Lambda=
\begin{pmatrix}1&1&1\\1&1&1\\1&1&a\end{pmatrix},
\qquad \operatorname{rank}H^{C^+}_\Lambda
=\operatorname{rank}H^C_\Lambda=2.
\]

C 内只有两组满秩列基 {1,x₁x₂}、{x₁,x₁x₂}。第一组虽含1，却没有通往 x₁x₂ 的 B 内前缀；第二组连1都没有。两者均非 connected。因此本例否定的是“C connected 保证存在 connected 满秩 B”这一额外主张，不否定 BORDER，也不否定 EXT。共同正文当前版本已经准确区分“含1”与“connected”；本轮没有发现新的源修订义务。

## 4. 一般稀疏 C 的 kernel 归纳如何真正补齐

一般稀疏 C 可以保留第2节任意含1的非退化列基 B，而不直接调用要求 B connected 的 BORDER。由 χ 交换仍可定义 φ(p)=p(χ)1，并有

\[
\varphi(pq)=p(\chi)\varphi(q),
\]

故 ker φ 是理想。接下来两项归纳才是一般 EXT 超过现有条件分支的承重部分。

第一项是原 Lemma 2.2：φ(m)=π(m) 对所有 m∈C⁺ 成立。m=1 时显然。非恒定 m 可沿 C 的连通前缀写为 m=xᵢm₁，m₁∈C 且次数更小。由归纳 φ(m₁)=π(m₁)，所以

\[
\varphi(m)=\chi_i\pi(m_1)=\pi(x_i\pi(m_1)).
\]

另一方面 m₁−π(m₁)∈N，且
xᵢ(m₁−π(m₁))=m−xᵢπ(m₁)∈V；截断核闭合给该差在 N 中。两式推出 π(m)=π(xᵢπ(m₁))=φ(m)。这个归纳使用 C 的前缀，不要求 B 的前缀。

特别地，φ(b)=b 对 b∈B 成立。每个 F 中关系因而属于 ker φ。B 含1使 border 消去足以张成 K[x]/(F)；φ|W=id 又保证 B 在商中独立。因此 B 确实成为商基，即使它不 connected。这里商基合法性来自“特殊 Hankel 核 + C 前缀归纳”，并没有删去一般 BORDER 的 B 条件。

第二项是原 Lemma 2.3：必须核全部乘积数据

\[
\Lambda(pq)=\Lambda(\varphi(pq))\quad(p,q\in V),
\tag{B}
\]

而不能只说 φ 在 V 上为 π 后就跳到扩张。局部核先给
Λ(pq)=Λ(pφ(q))=Λ(φ(p)φ(q))。原证明再沿 m∈C⁺ 的次数归纳，证明对所有 b∈B 有 Λ(mb)=Λ(φ(mb))：若 m=xᵢm₁，先把 xᵢb 换成 φ(xᵢb)=χᵢb，再对 m₁ 与 χᵢb 的 B 展开使用归纳。最后对 q 的 φ(q)∈W 作线性展开，结合 φ(pφ(q))=φ(pq)，便得到 (B)。该步骤完整保持原 C⁺·C⁺ 数据的 Hankel 一致性。

现在定义 Λ̃(p)=Λ(φ(p))。(B) 使它确为原截断泛函的扩张。若 κ∈N，则 φ(κ)=0，故对任意 p，Λ̃(pκ)=Λ(p(χ)φ(κ))=0，即 N⊆ker H_Λ̃。F⊆N 且 B 张成 K[x]/(F)，给 rank H_Λ̃≤r；原非退化 B 主块又给 rank H_Λ̃≥r。因此秩恰 r。进一步 (N)=ker H_Λ̃，φ 是沿这个全局理想到 W 的正规形。

最后，若 Λ′ 是另一完整秩 r 扩张，B 的 r 个独立列张成其全列空间。任意 κ∈N 与 B 配对为零，因而与每个完整列配对为零，故 N⊆ker H_Λ′。全 Hankel 核为理想，所以 (N)⊆ker H_Λ′。对所有 p 有

\[
\Lambda'(p)=\Lambda'(\varphi(p))
=\Lambda(\varphi(p))=\widetilde\Lambda(p).
\]

这补齐一般 EXT 的完整唯一性。原目标本身已有这份完整证明；本轮将其与 BORDER 的适用条件逐步对齐，没有新增一个把 BORDER 单独升级为一般 EXT 全证的边，也没有将原文已证明的一般分支错记成开放数学问题。

## 5. 正性在哪一步另付，EXT→POS 为何是另一条 whole

EXT 的代数构造不需要实数域或 PSD。若进入 POS 自身给定的实 PSD 子域，正性从截断数据传到完整扩张仍须实际证明。按 §2 正规形可直接核

\[
\widetilde\Lambda(p^2)
=\Lambda(\varphi(p)^2)\ge0,
\]

其中 φ(p)∈W⊆V；等式使用商正规形和 (B)。这支付全矩正性，再结合有限秩实正表示得到 POS。

本轮也实读了另一包正在发布的 `um-connected-flat-extension-to-positive-atomic-representation` 全文及其新 support 的对应证明。它完全不要求 connected 列基，使用 EXT 的存在和完整秩，选任意独立 Gram 基 B⊆C，令 G=H^B_Λ≻0。任意包含 C 的有限完整主块都秩 r，写为

\[
\begin{pmatrix}G&U\\U^T&W\end{pmatrix}.
\]

完整秩 r 强制 Schur 补 W−UᵀG⁻¹U=0，所以所有有限块 PSD，完整 Λ̃ 正。商 A=R[x]/ker H_Λ̃ 具有 r 维正定内积；各变量乘法良定、交换且实自伴。共同正交谱分解中常数 [1] 循环，迫每个 joint eigenspace 为一维且其常数投影非零，故得到 r 个互异实原子及严格正权。r=0 给零测度；无需归一化，权和为 Λ(1)。该证明确实支付 POS 整条正表示结论。

因此两条关系的作用范围不同：BORDER→EXT 的既有边是额外 connected 满秩 B 域中的 conditional contribution-step；EXT→POS 新证明在目标本来自带的实正域中支付整条 POS。后一条不反向消除前一条的 B 缺口，也不把正性变成 EXT 在非正输入上的结论。本包只复用已经 canonical 的前一条；新 whole 的绑定、检查和发布归另一 primary 包，本轮不把它另列共享资产或固定其资产 SHA，不复制边。

归一化的精确分离例为 C={1,x}、Λ=2ev₀−ev₁。y₀=1，yₖ=−1（1≤k≤4），因此

\[
M_C=\begin{pmatrix}1&-1\\-1&-1\end{pmatrix},\qquad
M_{C^+}=\begin{pmatrix}1&-1&-1\\-1&-1&-1\\-1&-1&-1\end{pmatrix}.
\]

两矩都秩2，C connected，EXT 完全适用，并给该有符号泛函的唯一同秩扩张；但 Λ(x²)=−1，无非负表示测度。它只反驳“删除正性也能由唯一扩张推出正表示”的强化，没有反驳 EXT 或 POS 的原陈述。

## 6. 连通性和有理算法的独立边界

原 pp.3–4 的不连通例 C={1,x³} 取 a=0、b=1，按 (1,x³,x,x⁴) 排列的 C⁺ 主矩是

\[
\begin{pmatrix}
1&0&1&0\\0&1&0&1\\1&0&1&0\\0&1&0&1
\end{pmatrix}\succeq0,
\qquad \operatorname{rank}M_C
=\operatorname{rank}M_{C^+}=2.
\]

它虽 PSD 且同秩，却没有同秩完整扩张。原证明用 1−x 的核关系递推，迫矛盾的后续矩；正测度也不可能，因为 y₀=y₁=y₂=1 使 x=1 几乎处处，却给 y₃=0。这里欠的是 C connected，不能拿它反驳保留 connected 假设的 POS。相反，第3节的 C={1,x₁,x₁x₂} 欠的是 connected 列基，C 自身连通，故一般 EXT 仍成立。这是两个不同的失败靶。

若原数据有理且选定非退化主块有理，投影线性方程与 χᵢ 可在 Q 中进行，所有由矩阵整数次幂定义的扩张矩仍有理。这是代数正规形的有理性；它不自动给一般实原子的有理坐标，也不是一份总位复杂度算法证明。例 y₀=1、y₁=0、y₂=2、y₃=0、y₄=4 的 PSD flat 数据有有理乘法矩阵 [[0,2],[1,0]]，正表示原子却在 ±√2。正商代数的同时谱分解在本比较中用于存在性；本包不把它冒充有理提取、矩寻找、任意调度恢复或 localizer 的算法实现。

## 7. 本包交付及比较处置

primary EXT 标为 linked，复用 canonical accepted/conditional contribution-step，保其源、目标当前 pins 与原 SHA。完整次数层怎样进入条件分支、一般稀疏 C 由核归纳另支付什么、实正表示怎样从完整秩继承正性，已分别落在本文第3、4、5节。

当前 task 无 formal follow-up 或 overlap_comparisons；故 `closed_overlaps=[]`，`follow_up_tasks=[]`。两个 read-added 端点的实质比较写在收据 `comparison_dispositions`。未发现需要新增 read-add 的依赖；没有新源错误或未辨身份。EXT 的一般分支已经由其原文证明闭合，不为“BORDER 单独不够”另造未完研究任务。

本轮仅写 task 的 write_paths；未执行 Git、work.py、native 队列、edge-bind、edge-check、全局 registry/coverage/integration 写入或 spawn。没有重跑历史科学计算。PDF 临时图在实读后移除。父 Boss 负责实际发布与最终收据检查；本文不预先声称这些动作已经完成。
