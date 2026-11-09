# 474257b8-resource-integration：resource 两个已完成 3A 批的数学集成意见

审读身份：Boss5。本文件仅记录本次 3D 的实质数学比较；没有修改边、收据、登记总表、覆盖表或集成表，没有执行 Git、同步、checkpoint 或队列写入。

## 可接范围与作用类型

本次核对 `resource-3a-3a-6690dabdf05908fb` 与 `resource-3a-3a-7b3c562d1a327a4d` 的全部四条边。结论是：三条可按完整目标接入，一条可按已成立的局部贡献接入；没有需要开放前提才能成立的条件关系，也没有发现须把现有 accepted 改为 proposed 的承重缺步。三个开放算法/概率对象的 `isolated-after-review` 是本次有限比较的准确处置，不能解释为其与任何其他对象都没有潜在关系。

| 边 | 精确可接结果 | 对整条目标的作用 |
| --- | --- | --- |
| `resource-c01-price-split-implies-convex-homogeneous-cost` | `C01-v3.L1` 推出第一象限任意凸锥上有限凸一次齐次成本的子模格不等式，连同非负线性价格 LP 的实现成本特例 | 完整：`M-2811342f46434965bf98081115bedcde`，`unconditional` 相对于已列出的模型假设成立 |
| `resource-c01-price-split-implies-full-two-ray-sufficiency` | 同一互补分裂用于原 d 维对偶，推出任意维数、所有非负容量与利润的两射线归一、单调、子模充分性 | 完整：`SEL-RESOURCE-LP-SUBMODULAR-v3`，没有使用高维价格可逆性 |
| `resource-v2-three-ray-certificate-specializes-to-axial-obstruction` | v2 三射线证书取中列 `(1,1)`、两端 `(1,0),(0,1)`、α=λ=μ=1，得到四个指定最优值与缺口 1 | 完整：`SEL-VECTOR-LP-SUBMODULAR-OBSTRUCTION-v1`；当前总图已有同证书的两段证明链，本边是直接捷径 |
| `resource-v3-sufficiency-specializes-to-v2-sufficient-clause` | v3 限制到 d=2，得到 v2 的“至多两条非零列射线 ⇒ 对所有 b,w 子模” | 仅局部贡献；必须保留现有 `contribution.result/remaining`，不能当作 v2 完整 iff 的独立支持 |

当前两个任务文件的 `state` 均为 `done`，四条收据资产的实际 SHA256 均与收据一致，四条边所引证明正文的实际 SHA256 均一致。八个收据输入 pin 与本地当前 coverage 对应的 object_pin 一致；本次实读的登记对象均为 version 1，陈述与边所使用的版本一致。C01 的只读 show 还返回 `binding_status: current`。数学核对以正文逐式推导为依据，这些字节核对仅确认所读证据与交付资产相符。

## 共同模型、量词与联合前提

启用 LP 固定有限 d,n≥1、非负实矩阵 A，定义

\[
\varphi_{b,w}(S)=\max\{w^\top x:Ax\le b,\quad 0\le x_i\le \mathbf1_{i\in S}\},\qquad b,w\ge0.
\]

变量可分数取用，每件启用物品有上界 1；矩阵列的射线以严格正比例判同，零列独立贡献模函数。v2 的必要性量化所有容量和所有利润；固定一个容量下子模不能反推出两射线。v3 的结论对任意维数成立，但只给充分性。资源容量为零、矩阵零行和方向中的零坐标均允许。

C01 的共同承重假设是两个价格坐标非负。成本对象另需 K⊆R²₊ 为凸锥，c:K→R 有限、凸、一次正齐次，并包括 c(0)=0。LP 成本特例中的 P 是由非负 2×d 有限矩阵给出的**线性**价格映射，b≥0；不能把“非负价格映射”扩读为任意非线性映射。全维 LP 边另需有限 LP 强对偶及最优达到、每列只依赖两价格中的一个、hinge 的递减性。这些均在正文已经支付，属于明确模型内的标准事实，不是未登记的开放研究假设。

两条 C01 出边可各自使用同一已证分裂引理；成本对象不是全维充分性证明必须额外接入的 ALL 前提。反过来，C01 加全维充分性不会支付三射线必要半边。不同结论共享价格分裂，不应因此合并模型、制造定义 hub，或把彼此当作循环证明。

## C01 互补分裂与凸齐次成本：完整性核对

正文 [P] 第三节的交叉情形为 z=(p,q)、z′=(r,s)，p<r、q>s，且坐标均非负。令

\[
D=rq-ps=r(q-s)+s(r-p)>0,\qquad
\lambda=\frac{s(r-p)}D,\quad
\mu=\frac{p(q-s)}D.
\]

有 D−s(r−p)=r(q−s)≥0、D−p(q−s)=q(r−p)≥0，因此 λ,μ∈[0,1]。直接展开得 λp+μr=p、λq+μs=s，故

\[
z\wedge z'=\lambda z+\mu z',\qquad
z\vee z'=(1-\lambda)z+(1-\mu)z'.
\]

可比点选 `(λ,μ)=(1,0)` 或 `(0,1)`。p=0、s=0 以及两者同时为零均不导致除零；同时为零时 D=rq>0、λ=μ=0，min 为零，max 为两原向量之和。没有引入严格正价格或可微性的隐藏条件。

K 是凸锥，所以这两个非负线性组合仍在 K；这一步给出目标中的 min/max 封闭性。有限凸一次齐次性对 α,β≥0 给出

\[
c(\alpha z+\beta z')\le\alpha c(z)+\beta c(z'),
\]

α+β>0 时由凸性与一次齐次性推出，α=β=0 时由 c(0)=0 支付。分别代入互补两组系数再相加，立即得到

\[
c(z\wedge z')+c(z\vee z')\le c(z)+c(z').
\]

这里不要求 λ+μ=1，因而不能把分裂误述为两点线段内的通常凸组合；所需的是凸锥与凸齐次函数的次可加性。当前边采用的是正确的非负组合论证。

对 LP 特例 `c_b(z)=min{bᵀy:y≥0,Py=z}`，每个 z∈P(Rᵈ₊) 均可行，目标非负且在任一可行实现上有限，有限维线性规划保证有限最优值达到。y=0 给 c_b(0)=0；最优实现的凸组合给凸性，正缩放与反缩放给齐次性，t=0 单独由零值处理。非唯一实现、折点、零 b 均无影响。[P] 第四节完整支付了目标的一般成本命题及 LP 特例，不需要恢复旧稿光滑 crosspartial 猜想。

## 全维两射线充分性：原对偶之和必须保留

正文 [P] 第一、三节与账本 [L] 的机制一致。原 LP 含零解且可行域紧，完整线性对偶存在最优解；消去上界的非负对偶变量得到

\[
\varphi(S)=\min_{y\ge0}D_S(y),\qquad
D_S(y)=b^\top y+\sum_{i\in S}(w_i-A_i^\top y)_+,
\]

并可取达到最优的 y_S、y_T。达到性来自 LP，不来自“连续函数在无界集合上必达”的错误原则。

把非零列写成 s_i u 或 s_i v，其中 s_i>0、u,v≥0；一射线可令 v=u，零射线情形为纯模函数。对两个原对偶的二维价格 `(uᵀy,vᵀy)` 使用 C01，取

\[
y_\wedge=\lambda y_S+\mu y_T,\qquad
y_\vee=(1-\lambda)y_S+(1-\mu)y_T.
\]

二者非负、分别实现价格 min/max，并且

\[
y_\wedge+y_\vee=y_S+y_T.
\]

因此 bᵀ 成本和严格保持。d>2 时无需、也一般不能把 bᵀy 写成两个价格的固定线性函数；当前边明确使用原 d 维向量和，避开了这个缺口。

每件物品的 hinge 只读取一种价格。交集物品在两个原价格上的 hinge 和与 min/max 处完全相同；S 或 T 独有物品在 max 价格处不增。把 max 用于 union、min 用于 intersection，得到

\[
\varphi(S)+\varphi(T)
\ge D_{S\cup T}(y_\vee)+D_{S\cap T}(y_\wedge)
\ge\varphi(S\cup T)+\varphi(S\cap T).
\]

空启用只有零 x，启用扩大只扩大可行域，所以归一和单调也完整成立。零列剥离后再加回模函数，不影响子模。因而 `C01→v3` 的 whole_result 完整成立；没有遗漏零容量、退化方向或一射线边界。

## 三射线必要性与轴向反例：需要全容量全利润的二维量词

若二维 A 有三条不同非零射线，选两端列 e,f 及中间列 d。d 的两坐标严格正，且 d=λe+μf，λ,μ>0。选择资源坐标顺序使

\[
e_1/d_1>e_2/d_2,\qquad f_2/d_2>f_1/d_1.
\]

取 `w_d=1,w_e=e₁/d₁,w_f=f₂/d₂` 与容量 `b=αd`，其中 `0<α≤min(1,1/λ,1/μ)`。对 S={d,e}，目标正好是第一资源消耗除以 d₁，所以不超过 α；取 x_d=α 达到。T={d,f} 用第二资源同证，交集 {d} 也恰 α。并集取 x_d=0、x_e=αλ、x_f=αμ，容量恰饱和，启用上界因 α 的选择成立，其利润严格大于 α。于是

\[
\varphi(S)+\varphi(T)=2\alpha
<\varphi(S\cap T)+\varphi(S\cup T).
\]

其余物品不启用即可，故构造适用于原矩阵中任意选出的三列。对有理 A，方向比较、二元线性方程及 α 的选择均为固定层数有理运算，可给多项式位长证书。一般三射线构造只需并集的严格大于 α 的可行见证，不必声称一般并集最优值已精确求出。

固定轴向实例中令 d=a=(1,1)、e=b=(1,0)、f=c=(0,1)，λ=μ=α=1，利润均为 1。两 pair 和交集值均为 1；并集在 `(x_a,x_b,x_c)=(0,1,1)` 达到 2。两容量相加给 `2x_a+x_b+x_c≤2`，因此总利润不超过 `2−x_a≤2`，精确最优值为 2。缺口为 `rhs−lhs=1`，与 [V] 的 masks 3、5、1、7 对应值 1、1、1、2 一致。这支付轴向目标的全部四值，没有借用随机 HiGHS 探针。

v3 只在 d=2 支付上述 iff 的充分半边。必要半边仍是本节独立的三射线构造；不能以 `v3→v2` 的 contribution 代替它。高维 `A=I₃` 有三条不同列射线，但

\[
\varphi(S)=\sum_{i\in S}w_i\min(1,b_i)
\]

为模函数。这明确排除把二维必要性或 v2 的 iff 无条件外推到高维。固定 b 的分类、近似子模缺陷估计和新的指派近似算法也没有由本包支付。

## 开放对象的具体未付桥与覆盖处置

`M-8e21b2ce4dec4976a576924f343e8742`（C17）要求在 AW 的既定 k 拟阵交舍入过程中，对归一单调 coverage f、单物品边际≤1，证明以 `F(x)=E f(R(x))` 为尺度的维数无关下尾。启用 LP 的确定性子模性没有给该随机过程的非线性期望保证，更没有 conditional drift、quadratic variation 或适当 variance lemma。固定 modular 下界可显著低于 F(x)，因此不能直接把线性定理的权重向量换成 f。可保留 bounded-overlap 受限族为后续入口；本批没有证明它。使用 conditional 标签也不能掩盖这些论证本身尚缺步骤。`isolated-after-review` 成立，状态保持 open。

`M-ed52023e7ef545d79147e2b65482dd89`（C18）固定 L≥3，独立 batch 各至多两个互斥 alternatives，每产品使用≤L个单位容量资源，要求相对于自然 ex-ante LP 的统一 selectable OCRS 改善或 q=2 的准确 barrier。每 batch 只有两候选不等于全矩阵列只有两射线，也不等于 L-partite。确定性、可分数的启用 LP 结论没有提供在线接受策略、逐产品条件选中概率或 pair-blocker 控制。具体缺口仍是 L=3 的正 blocker 引理或最小 hard LP，以及推广到每固定 L 的量词；排除某个 affine-plane 例子不等于消除全部障碍。`isolated-after-review` 成立，不能从 offline φ 子模造出 OCRS 保证。

`M-caef92af522b43f18a8c58e97acc3d58`（C19）为 rank-one 独立激活、Σx≤1 的循环路线问题：从 r 个切点的 rotations 及 reverse 共≤2r 个 orders 中选择分布，分布可依已知 x、不可依激活 realization，在线 policy 不可看未来。启用值或 offline weighted gap 没有构造这种限支持 order 分布及在线策略，也不证明最优 selectability α_r。r=2 四 orders 的准确算法或 small-LP 对偶障碍仍未付。C18 的 q=2 条件也不是相同路线/激活合同的桥。`isolated-after-review` 成立，问题保持 open。

这三项均为明确的数学未付义务，不是身份或证据来源未辨的 `needs-decision`。本地 current coverage 尚把它们写作“没有完成比较”；本次 done 收据确实已经给出有界比较，集成时可用收据的实际范围与上述缺口取代占位说明。不能把其开放性扩大宣称为全世界的文献未解状态。

## 与所读总图快照的重叠及集成建议

本节“当前”均指本次实读时、根 Boss 本轮 assemble 之前的快照。笔记初稿保存后，根 Boss 通知本轮 assemble 已成功、104 个 effective done、449 个 edge files、repair_tasks 为空；本 worker 没有重新读取或重写该最新集成产物，以下“尚无 pin/占位”只说明本次审读前态，不用于否定新 assemble 状态。

以本次所读 `research/registry.json` 的 canonical `edge_files` 为准，涉及这八个对象的既有逻辑边只有以下两条：

1. `resource-three-ray-transfers-to-exact-vector-defect`：v2 → `M-db748b49766141e79b7ab59a27ad25bb`（ε∈[0,1) 的近共线三列族）。
2. `exact-vector-defect-specializes-to-unit-axes`：该 ε 族 → `SEL-VECTOR-LP-SUBMODULAR-OBSTRUCTION-v1`，取 ε=0。

已实读两条 canonical 边全文、ε族当前登记陈述、[G] §4 和 [R] 的 C01 段。令 e=(1,ε)、f=(ε,1)、d=(1,1)，三射线系数为 λ=μ=1/(1+ε)、α=1；两容量求和补上并集精确上界，值为 2/(1+ε)。ε=0 正是本批新增直接边的 λ=μ=α=1 实例。

因此新增 v2→轴向边与既有两段链数学上重复同一证书，但不是已有 canonical 边的相同 source/target 文件副本。它可作为局部直接导航保留；集成说明应称“同证明的直接特化/传递捷径”，不可把它与经过 ε族的路径计为两份独立证据、两个新反例或新研究进展。原 ε族还保留正消耗、近共线和定量缺口的较广结论，本边不替代其作用。

另外三条新边没有发现当前 canonical 中的同端点重复。`C01→成本` 与 `C01→v3` 共享引理但目标不同，均有实际数学作用；`v3→v2` 是较强维数范围到充分子句的局部特化，应在研究线索/局部贡献投影中保持原有 remaining，不提升为完整支持。

本地 current `map/integration.json` 尚无这两个任务的 task_receipt_pins；resource-activation 的 archive_review 仍含“Await actual cross-batch integration review”和“cross-batch review pending”占位。实际可接内容应包括：互补分裂的两个完整用途、v3/v2 的充分与必要分工、与既有 ε族链的同证书重复，以及 C17–C19 的具体未付桥。本次两批没有新增跨档算法迁移；跨档有效数学仍是既有 resource-activation ↔ bottleneck-knapsack 的同一连续 LP 三射线证书及 ε族/轴向特化，不能把档案标签或同一来源当作 online/OCRS 桥。

两份 done 收据的 review_note 仍保留“仅保存本地草稿”“尚未推送或map done”的旧描述，与当前任务文件的 `state: done` 不一致。这是交付说明文字的时间遗留，不是四条推导的数学反例；本意见没有改写该收据，也不以这段旧话否定已见的 done 状态。

## 可直接采用的 resource-activation 集成段落

**comparison_scope 建议文本：** 实读 C01 互补价格分裂、凸齐次成本接口、全维两射线充分性及二维三射线必要性完整证明；逐项核对两个 resource 3A done 批的四条关系、八个对象陈述和全容量全利润量词。另与既有 v2→近共线 ε族→轴向反例的 3C 链比较资源、利润、变量上界、启用集合及精确缺口，并分别比较 C17 的 AW coverage 下尾、C18 的 q=2 random-element OCRS、C19 的有限 order 支持 rank-one 在线合同。

**outcome 建议文本：** C01 的同一非负互补系数一方面证明第一象限凸锥对 min/max 封闭及有限凸一次齐次成本的子模格不等式，另一方面在原 d 维对偶中保持向量和及 bᵀ 成本和，连同单价格递减 hinge 完整得到全维两射线充分性。二维三射线中间列构造独立支付 v2 的必要半边；v3 在 d=2 只贡献其充分半边，不能作为完整 iff 支持。固定轴向实例的 pair、交集均为 1、并集为 2、缺口为 1；新增 v2→轴向边是既有 ε族链的同证书直接特化，不构成独立新证据。三个开放对象本次仅得到明确模型比较，未从 offline 连续启用值子模性推出在线可选率或随机舍入下尾。

**unresolved 建议条目：** C17 仍欠 AW 非线性期望接口、随机边际的条件漂移/二次变差控制及真实 variance lemma；C18 仍欠 L=3、q=2 下的正 pair-blocker 引理或精确 hard LP，以及各固定 L≥3 的完整量词；C19 仍欠 r=2 四 orders 的准确分布/无未来信息策略或 small-LP 对偶障碍、继而最优 α_r。固定容量分类、高维必要条件及指派算法后果均不由本包推出。上述是已辨清身份的数学 open 义务，不是待补办的集成身份或字节冲突。

**cross_archive_review 可采用的补充句：** 本轮 resource 新接关系主要在同档内；与瓶颈背包档的真实跨档数学保持同一个连续向量 packing 启用 LP 的恒等映射，ε族与轴向特化共用二维三射线证书和容量求和上界。没有建立到 AW、OCRS 或限支持 arrival 在线策略的迁移桥。

## 实际读取的来源与边界

工作约束实读：根 `AGENTS.md`；`research/IMPLEMENTATION.md`（一般接口及第三阶段/定向替代/后续消费段）；`prompts/03-map-worker.md`。

批次与当前图实读：上述两份 `map/receipts/*.json`、对应两个 `research/operations/map-v2/tasks/*.json`、四条本批边全文；`research/registry.json` 中八个目标/依赖对象的完整记录，以及用于比较重复链的 `M-db748b49766141e79b7ab59a27ad25bb` 完整记录；当前 registry 的 edge_files 中涉及这些端点的边；`map/coverage.json` 中八个对象条目；`map/integration.json` 的相关 pins、object_scopes、resource-activation archive_review 及 cross_archive_review；上列两条既有 3C 边全文。

数学正文实读：

- [P] `archives/resource-activation/state/证明/启用值的两价格分裂与二维三射线禁形--证明.md`，全文，包括六节及退化边界。SHA256 `5f9d97e5e6fb490c22d1668b40120cd2ae180c13d766abe9f32ef7dd8f77c7e1`。
- [L] `archives/resource-activation/state/资料/两列射线启用值的二维分类与全维充分性--资料.md`，全文。SHA256 `d14b7729ff08dbd40303cd6fd7dcf83e2ff59b53a53fc964eaf2dae202bfeca4`。
- [S] `archives/resource-activation/state/资料/第二轮GAP候选与CRS边界--资料.md`，精确 C01、C17、C18、C19 各完整节；本意见的算法比较只依这些节与对应登记陈述，不声称完成 C06/C08 的数学核对。SHA256 `3ff76bddbd2b86c4373efbd30f7c9be5758ddfa81198014a5e6dd5edb65c827a`。
- [V] `archives/bottleneck-knapsack/state/审查/向量容量启用值子模性失败三源复现--审查.md`，全文；精确枚举表只作与手证的对照，没有重跑脚本。SHA256 `13b607c971691b207e37569e60887c5055a1b5fe50dd8456311a2ed6256cdb15`。
- [R] `archives/bottleneck-knapsack/state/审查/退役GAP选题底稿与数学边界--审查.md` 的 `C01：两资源启用值的分类` 完整节；仅为参数族和模型边界比较。SHA256（既有引用）`3a6d7787cf22efa03d645baf2719fa84927e55e5777d886bd38c19627913c10e`。
- [G] `research/registration/evidence/register-ab98f323ad-0001-1/gap.md` 的 `4. 已完成：consecutive-ones向量LP的精确反例` 完整节，核轴向与 ε族的手工上下界。SHA256（既有引用）`8e14e6d6525cc353091aa0484c6c72dc447f581d6227d6232fb3f960db06b68e`。

本次未访问 Library 或外部连接，未重跑历史浮点 LP、Fraction 顶点枚举、AW/OCRS 或任何搜索程序。对源代码和空随机搜索输出没有新增实读/运行声明；四值反例由本文写明的有限约束上下界直接闭合。没有发现新的数学阻断项；须保留的实质限制是 v2 必要半边不能由 v3 替代、轴向直接边与既有链同证书，以及三个开放对象的在线/随机过程桥尚未支付。
