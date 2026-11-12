# Boss1：positive-flat 独立 3D 数学审读

审读结论：当前 `um-connected-flat-extension-to-positive-atomic-representation` 的 accepted / unconditional / whole 分类成立，整条 EXT→POS 证明闭合。复用的 `um-positive-sparse-flat-to-original-t-hs-support-step` 也成立，但只承担 NF 原合同的 δ=0 contribution；它不支持正 δ 的整个 NF 定量目标。本次未发现需要撤回、降级或修改这两条边的数学问题。

本报告是独立实质审读，不认领、改写或发布任务。沿用 Boss1，源 clone 全程只读；没有 Git、native queue、edge-bind、科学程序重跑、认证文件读取或 spawn。精确文件 SHA、当前 definition/receipt/asset/endpoint pins、逐文件真实阅读范围和只读完整性结果均在同目录 `refs.json`。

## 1. 当前范围与身份

任务为 `unrelated-machines-3a-3a-ec98dbd143c32cff`，当前本地 task state 为 done，owner 为 Boss2。definition pin 为 `990c1ec6633f8bc55654a8653d66b9767d38cfff0109bab78f534f9a2cb81d61`。当前 definition 实际只有一个核心 POS，另有两个 read 端点 EXT/NF。Root 已确认初始派工提到“第三个 isolated 核心”是别包范围混入；本包没有这样的核心，不补造 isolated 处置。

| 简称 | 对象 | 版本 | 当前 registration pin |
| --- | --- | ---: | --- |
| POS | `M-8a8102ce2db9454ba1ed5eae66e12724` | 2 | `8c985cebfde20d2b788e4610e314e7fbdc6ca3525041db765165988c455715b9` |
| EXT | `M-d2f0e90baf4440cab9efbffecfee709e` | 2 | `a066527acf0feec7455d375787e9a60dbe8603fa27a7b32090db79d1c5d54fad` |
| NF | `UM-GLOBAL-MOMENT-NEARFLAT-EXTRACTION-v1` | 4 | `3260dbb3dde9aa8112807f49374bf24da0c0af502b5285cbafbbf6a2655d8b2e` |

三份完整对象记录均从当前 registry 读取，并独立按仓库 canonical JSON 公式计算 pin，与 task input_pins、边 endpoint_pins 一致。task embedded receipt 与外置 receipt 全结构相等；外置 receipt SHA 为 `0a0877a37034a6e9d0ea7bd60e56e4ec54150498f1934bf177a7a019af6fa542`。integration 中该 task receipt 的内容 pin 也一致。

当前 new whole 边 SHA 为 `92808da420d0b13d4b053629927be4aa1bc0e2c461b5c3e266eae4aae578398c`；共享 contribution 边 SHA 为 `9861647925a6cc723294921f0a19b26131fbea401c8e370b5cc81a4eba26cc35`。receipt 四个 assets 的原始字节 SHA 均吻合；两条边的端点 pins、全部 evidence SHA/pins、review_digest 均按只读公式吻合。含 section 的 evidence 标题都精确且唯一。这些只证明版本绑定，数学结论来自下文实读推导。

## 2. 原 PDF 与目标合同的区别

实际从冻结 Laurent–Mourrain 原 PDF 直接提取并读取 pp1–10，精读 Theorem 1.1、1.4、1.5、1.6、§2 全证明、Theorem 3.2 和 §3.2 localizer 讨论，并新渲染目视 p3/p9。PDF SHA 为 `a79a6aae70263cdc0b15415f838df666cfb99d6a00ef87bb1dae381493478fad`。这不是沿用旧 worker 的已读声明。

Theorem 1.4/1.5 的输入是有限 connected-to-1 普通单项式集 C、其 C⁺，以及 rank H_C⁺ = rank H_C 的 Hankel 数据。它给保持原 C⁺·C⁺ 数据的唯一完整同秩扩张，不要求 PSD。Theorem 3.2 则另要求实正数据后才给表示测度。当前边在 POS 原来量化的实 PSD 子域应用 EXT，正性是目标自带输入限制；不是从无正性 EXT 凭空推正性，也不是尚待证明的开放前提。因此此处 unconditional 的使用准确。

原 §2 明确不要求所选列基 B connected，且 p9 给出 connected 的 C 未必有 connected 满秩列基的例子。当前证明使用任意独立 Gram 主块，避开了误用 Theorem 1.6 的风险。新边不仅引用 Theorem 1.1，还把从全矩正性到有限原子表示的完整有限维论证写出，不存在未列出的黑箱数学对象前提。

## 3. whole 证明的独立逐步核验

固定 POS 所允许的任意实数据 Λ，C 含 1 且 connected to 1，M_C⁺ PSD，rank M_C⁺ = rank M_C = R。EXT 给实完整 Hankel 泛函 Λ̃，保持全部原数据，完整秩仍为 R。

1. **R=0。** 完整 Hankel 矩阵秩零，全部条目为零。每个单项式矩都出现在常数行，故 Λ̃=0；零测度表示完整及原截断数据。这覆盖未归一化的零输入，不能强迫它有正权原子。

2. **独立列基与正定主块。** R>0 时，从原 PSD 的 M_C 选 R 个独立列 B⊆C。以 Gram 表示看，这 R 个向量独立，所以对应主块 G=M_B 正定。选 B 只为线性代数，不需要连通性，也无需把所有 B 强制含 1。

3. **任意有限主矩的 Schur 补。** 任意有限普通单项式集 F⊇C，完整秩上界给 rank M_F≤R，而包含 rank R 的 G 给 rank M_F≥R。把 B 排在前面后，M_F=[[G,U],[Uᵀ,W]]。可逆块消元给 rank M_F=R+rank(W−UᵀG⁻¹U)，故该 Schur 补为零。于是 M_F 是 G 的合同扩张，确为 PSD。该推理不预设整个 M_F 已正。

4. **全多项式正性。** 对任意多项式 p，取 F 含其有限单项式支撑及 C；上一步给 Λ̃(p²)≥0。由此全局正性已真正支付，不仅是某些有限阶或稀疏平方的正性。

5. **Hankel 核是 ideal。** K=ker H_Λ̃ 定义为对所有 q 都有 Λ̃(pq)=0 的 p。若 p∈K，则对任意 r,q，Λ̃((rp)q)=Λ̃(p(rq))=0，所以 rp∈K。这里使用完整 Hankel 泛函，不能把一般截断核直接当完整 ideal。

6. **正商与维数。** 全矩 PSD 的 Cauchy–Schwarz 给 |Λ̃(pq)|²≤Λ̃(p²)Λ̃(q²)。因此 Λ̃(p²)=0 当且仅当 p∈K。内积 ⟨[p],[q]⟩=Λ̃(pq) 在 A=ℝ[x]/K 上良定且正定。线性映射 H 的核商维数等于其 rank，故 dim A=R。

7. **真实、交换、自伴的乘法。** K 为 ideal 保证 M_i[p]=[x_i p] 良定；Hankel 乘积给 ⟨M_i[p],[q]⟩=Λ̃(x_i pq)=⟨[p],M_i[q]⟩；交换多项式环保证 M_iM_j=M_jM_i。故它们是在同一 R 维实正内积空间上的交换自伴算子，可以同时正交谱分解，joint eigenvalues 均在 ℝ^d。

8. **循环常数排除重谱维数和零权。** v=[1] 循环，因为 [p]=p(M)v 张成 A。合并相同 joint eigenvalue 后，记联合谱空间为 E_s，谱投影为 P_s，joint value 为 z_s。投影 p(M)v 恒为 p(z_s)P_sv，所以循环性使 E_s=span(P_sv)。每个 E_s 非零，故 P_sv≠0 且 dim E_s=1。于是恰有 R 个互异实 z_s，不能留下高维联合谱空间或零质量谱点。

9. **正权与完整表示。** 令 w_s=‖P_sv‖²>0，则 Λ̃(p)=⟨v,p(M)v⟩=Σ_s w_s p(z_s)。μ=Σ_s w_s δ_z_s 为恰 R 个互异实原子的正有限测度。权和为 Λ̃(1)=Λ(1)，不要求归一化。

10. **原数据保留。** EXT 的扩张在整个 Span(C⁺·C⁺) 与 Λ 相同；上一步表示完整 Λ̃，所以自动表示全部原截断数据，并非只表示 C·C 或所选 B 块。

以上证明对 POS 的整个原输入域逐份成立，所以应保 whole_result，不能降成仅“存在同秩扩张”的 contribution。没有发现循环证明、隐含 connected 列基、遗漏 R0 或虚假的全矩正性步骤。

## 4. 反例与边界的准确使用

正文的 2 ev₀−ev₁ 例归一化且 connected/rank-flat，但 Λ(x²)=−1，说明删除 PSD 后不能得到非负表示。它不反驳 EXT 原定理，也不反驳 POS 原定理。

C={1,x³}、a=0,b=1 的例中，局部 PSD 同秩成立，但 C 不 connected；若存在正测度，y₀=y₁=y₂=1 会使 x=1 几乎处处，与 y₃=0 冲突。该例准确说明不能删除 C 的连通性。p9 的非 connected 列基例属于更一般无正性域，用于说明 C 与 B 的条件不同；当前边并未声称其一定是正输入。

新 whole 边没有支付 Boolean/one-hot、半代数支撑或调度容量；没有给一般实原子的有理算法；没有推出正 δ NF 估计、矩生成器或可靠 FAIL；也没有宣称所有表示测度的唯一性。原完整扩张的同秩唯一性仍可保留为 EXT 的源结论，但本边的正表示证明不需要扩大唯一性范围。

## 5. 共享 POS→NF contribution 的独立核验

本次完整读共享边及 companion proof、三原子 witness、NF 当前完整合同、主审查、原数学证明和有理 Gram 资源。另读各有限审计/实现说明以核范围，没有重跑任何旧科学程序或把有限 PASS 当全称证明。

**普通 Hankel 提升及 δ0。** NF 给 degree≤4 的同一 Boolean/one-hot reduced y。把普通幂归约、同任务冲突置零得到真正 ordinary Hankel 泛函。C={1,x_e} connected，C⁺为普通次数≤2单项式；普通矩是 reduced M₂ 的满射 pullback FᵀM₂F，故 PSD 且同秩，C 主块为 M₁。原证明的 X_e 在零范数商中良定，并有 D_e=B_e*B_e PSD。全 V₁ 上迹和 δ=0 迫所有 B_e=0，故每个二次向量都在 V₁，V₂=V₁。反向也成立。这里不能改成常数向量上的零缺陷。

**原子合法与原 T。** POS 给有限正表示；四次零平方 (x_e²−x_e)² 强制每原子 Boolean，任务 one-hot 的零平方使每原任务恰选一个原端。rank M₂=rank M₁ 使二次评价空间等于 affine 评价空间，故后者对每坐标乘法封闭且含 1，包含所有多项式评价。有限互异 Boolean 原子的指示函数可用多项式隔离，因此 affine 评价空间就是全部 ℝ^N，N=R。每个原子可由 affine q_s 隔离。g_i q_s² 的次数至多 3，落在原四阶输入及 affine load localizer 的实际测试域；于是 0≤L(g_iq_s²)=w_s(T−load_i(z_s))，每原子同时满足所有机器原 T 容量。不存在把低阶 localizer 擅自代入高阶完整调度指示函数的问题。

**HS 是支撑计数。** 加权评价等距同构把 A_e 化为 diag(z_s,e)，全部是交换 0/1 正交投影。前缀 K 是 joint projection，HS²=tr K=rank K，是相容原子数量；各合法孩子分割父支持。初值 R>0，最大孩子保持正整数，全部任务后 count=1，原算法输出原 T 支撑中的一个真实调度。常数向量质量 ‖Kv₀‖²=Σ相容w_s 是另一量。三原子 witness 的首步 count=(2,1)、mass=(1/50,49/50) 清楚区分两者；本轮仅读其精确记录与解释，未重算全部矩阵。

**有理实现。** G、H_e、A_e=G⁻¹H_e、G-adjoint 及 HS 迹均为有理量；Boolean 域原子坐标是 0/1。由 v₀ 按各任务投影分裂，非零分支正交，每层至多 R 条；最终权为有理 G 范数平方。固定矩阵共同分母 Q 的至多 n 步乘积可用 Q^n，分子位长随 n 和矩阵条目位长多项式增长，故是显式输入总位长的多项式，不借一般谱计算、平方根、逆最小权或条件数循环。上述数学存在性谱分解没有被冒充为算法。

该 contribution 的 δ=0 是已指定、可精确检查的输入子域，不是开放前提，故 unconditional 合理。其 contribution.remaining 也准确保留“本经典迁移不支付正 δ NF”的边界。正 δ 的原自足证明可另读，不能由此经典正表示直接取代。当前 NF v4/主审查对 δ_e=0 时 loss=0、以及未剪枝仅有 T/(1−3δ) 弱式的修正与共享边一致。

## 6. 覆盖、版本与可采用结论

POS 当前 linked 覆盖有实际数学依据：new whole 从 EXT 完整支持 POS；共享 step 又解释 POS 对 NF 精确平坦算法步骤的实际作用。该任务没有 formal follow-up 或 isolated 核心，因此 closed_overlaps=[] 与本任务范围相符。

读到的投影快照中，EXT 自身 coverage 仍是 needs-decision / “No completed comparison batch yet”，但已有两条 incident edges。它不是本任务的 core，本报告不凭 incident edge 替另一任务完成主覆盖，也不改投影；可由 Root 在实际 assemble 后按其所属任务检查这一残留。POS 和 NF 的当前 coverage pins 与合同一致。

可联合采用本审读作为本包完整 1-core+2-read 比较范围的独立数学复核：new whole 和复用 contribution 均通过，未付义务限于边本来保留的范围。无需新增逻辑边、反例节点、外部对象前提或 follow-up 任务。

## 7. 本轮真实阅读范围

完整读：AGENTS、IMPLEMENTATION、worker prompt；当前 task/receipt/ledger/new edge/positive-flat-review；三对象完整 registry records；共同中文文献页；共享 POS→NF edge/proof/witness；NF 原证明、主审查、Gram 资源、冻结审查、独立 HS 资源、有限审查及六输入说明页。PDF 直接读 pp1–10 并目视 p3/p9。

定向读：registry 的 canonical edge 路径成员关系，coverage 三记录，integration 本任务 pin；《未归档配置证书批次与量词边界》的开头及精确 §6；NF→PREFIX 的完整 edge JSON仅核既有 flat law/计数质量去重，不新增 PREFIX 覆盖；runtime 仅 pin 与 edge_digest 公式。

未读或未做：未重读各说明页提及的所有 transitive 原代码、大型 JSON、外部 3DM 归约或 PREFIX 全对象；没有任何新全称证明依赖这些未读材料。未运行 fixture、矩阵重算、PSD 审计、旧科学程序或 native 检查。逐文件 hash 与读取范围以 `refs.json` 为准；旧 ledger 的历史“已读”不被继承成本轮实读。
