# CHENG-MAO-EXISTENCE-CLOCK：Boss1 独立 3D 只读数学审读

## 可采用结论

**可采用当前 done 包及其完整单 core coverage；没有发现阻断数学问题。** 当前唯一新逻辑边 `cheng-mao-99over26-gap-to-4plus-delta-existence-only` 的准确作用是从 Cheng–Mao 的 99/26 配置 LP 间隙定理，推出对端 4+δ 算法合同中的**数值存在性 contribution**。它不是整条算法合同的蕴含。`accepted / unconditional / implies / contribution` 与已经付清的推导一致；不应改成 `whole_result`，也不能补上反向或同常数多项式时间边。

我实际独立阅读了两个当前 v1 登记记录、共同中文正文全文、正式 task/receipt、edge/support/reading-ledger，以及冻结 28 页 PDF 的全部 1673 行 layout 提取文字；目视 PDF 第 23、24 页。Appendix C 的核心证明链在本次重构核对；不是只复核 SHA 或转述 Boss2 的阅读声明。对端 §3–4、Appendix A/B 本次也实际读到，但没有重新实现或运行算法。共享 clone 全程只读；无 Git、work.py/native、科研程序、LP/local-search 后端运行，无认领或写主覆盖。

## 1. 端点合同与关系作用逐项

| 项目 | 独立结论 |
| --- | --- |
| 核心 | `M-b8540026a0fc4c52b209c4ce7311c25b` v1，proved；存在实际分配使每位玩家获得至少 `(26/99)T*`，局部搜索有限终止，不付相同常数的多项式总时间。 |
| 只读对端 | `M-af5cd39d12c444399b616e0d318c27be` v1，proved；每固定 δ>0 的实际分配值 `T*/(4+δ)`，另有论文特定算法与 `poly(m,n)n^{poly(1/δ)}` 时间、目标搜索合同。 |
| 模型 | 同一有限、非空玩家集合；不可分资源；每资源固有值 `v_r≥0`，玩家估值为 0 或该固有值；每资源至多给一人，效用为资源值之和。阈值方向为 max-min，不是 makespan。非空玩家是通常模型前提，也是 support 明列的前提。 |
| LP 基准 | 同一 `CLP(T)`，玩家覆盖至少 1，资源使用至多 1。整数实际分配是 LP 可行点，故 `T*≥OPT`。有限资源的配置集合只在有限多个子集和处改变，`T*>0` 的最大可行阈值可取到。 |
| 方向 | 仅 core → peer 的数值存在性。边只有一个 source；`premises_mode:all` 不丢联合前提。没有需要另加的开放假设。 |
| whole/contribution | 当前没有 `whole_result`，且明确填写 result/remaining，正确。`remaining` 指本边尚未推出的目标合同部分；不是把已经 proved 的目标定理降格为全局 open。 |
| δ 量词 | 对所有 δ>0，`26/99−1/(4+δ)=(5+26δ)/(99(4+δ))>0`。源分配本身不依赖 δ，实际给出比目标所需更强的 `∃A ∀δ>0` 数值保证；因此没有交换量词错误。算法时间仍只按每固定 δ 解释，不是把 δ 当一般输入后的统一多项式时间。 |
| 零目标 | `T*=0` 时任意合法分配给各玩家非负值，满足目标 0；禁止除以 0 的归一化。empty bundles 也合法；如要求每件资源都分配，可任意分配剩余资源，非负值保证不损害下界。 |
| 可行正输入 | 对任意给定 `T>0` 且 `CLP(T)` 可行，按 `v/T` 归一化，Appendix C 的 no-stuck 证明只需 `CLP(1)` 可行，不需它恰为最优值 1，因此有限返回实际 `26T/99` 分配。 |
| 不可行输入 | 本边没有给不可行 `T` 的可行性判别、失败证书或有界时间返回保证。无 LP oracle 是操作接口结论，不等于算法决定 `CLP(T)` 可行性。|
| 复杂度 | 给定二进制有理输入及给定有理 T，每次 Build/Contract 可多项式位时间实施。调用总数的有限界是指数级上界，不能支付统一多项式总 clock；也不证明超多项式下界。 |
| 未知 `T*` | 在存在性证明中取 `T=T*` 是数学论证，不是免费算法输入。未知目标搜索与截断/验证合同仍须独立支付。 |

准确的新边数值证明只有两步：当 `T*>0`，源定理所给同一实际分配各玩家值至少 `26T*/99 > T*/(4+δ)`；当 `T*=0`，非负性支付零界。它完全不依赖 Appendix C 是否快、是否已知精确 T*，所以 `unconditional` 正确。核心 theorem 本身作为 proved source 是边的逻辑输入，不是额外未付条件。

反方向，4+δ 的保证严格低于 `T*/4`；即使结合实例有限性把 δ↓0 的数值存在性极限整理到 `T*/4`，仍没有达到 `26T*/99>T*/4`，不能反推源定理。未建立某个参数替换的证明，并不等于反驳对端或给出算法不可能性。

## 2. Appendix C 完整核心承重链

### 2.1 定义、实际分配与可实施选边

C.1 与 §2 定义相容：fat 资源值至少 λ，thin 资源值小于 λ，λ=26/99。维持 fat 图的最大匹配 M 与互不共资源的 λ-minimal thin edges E，且每个玩家至多被 M∪E 覆盖一次。根 dummy `(p0,∅)` 属于栈 `B1`，不属于真实 E。

Build 可以先在 `G_M` 求从 blocker 玩家出发的可达玩家，再对每个可达玩家扫描未被栈覆盖的可用 thin 资源。总值至少 λ 时，从全部可用资源反复删除冗余即可得到 λ-minimal edge；这不需要 subset-sum 优化、配置枚举或 LP 解。相交测试扫描 E 即可得到全部 blockers。零值资源可先删除，因它们不需要出现在 minimal edge 中。

Contract 选择最早 unblocked edge a*，选能到达其玩家的最小 blocker 层 t。Lemma 28 保证路径存在且 t 在 a* 旧层之前。路径翻转重新安排 fat matching，并以 a* 的实际资源替代 bt；a* 已无 E blocker，不会造成资源冲突。非平凡路径只改变端点 fat 覆盖，内部玩家继续覆盖；零长路径也允许，故同一玩家直接换 thin edge 的情形合法。t=1 时根玩家覆盖增加一人；t>1 时原已覆盖玩家不丢失。

Lemma 28 的归纳成立：Build 不变旧匹配与旧层；Contract 的最小 t 保证所有较早根集出发的旧证路径与翻转路径不相交，否则拼接到 a* 得到更早 t 的矛盾。删除高层后保留层的可达性因此不变。

### 2.2 Claim 30 对全部配置可行

卡死时令 P+ 为从全部 blocker 玩家在 `G_M` 可达的玩家，`R_f+` 为可达 fat 资源；可达玩家和可达 fat 资源的单价均为 `1−21λ/26=3λ`。栈覆盖的 thin 资源用 support 所列三段 f(v)，其余价格为 0。

逐段可直接核：f 连续、非减、`0≤f≤λ`；当 `0<v<3λ/4`，`f(v)/v≥6/5`。两个接点分别为 `f(λ/2)=3λ/5` 和 `f(3λ/4)=λ`。零资源价格 0。

对 `p∉P+` 约束平凡。对 `p∈P+` 的任意配置 C：有 fat 资源时，该资源从 p 可续达；如果是匹配资源进入 p，则 p 的唯一入边要求可达路径先经过该资源，仍可达，足付 3λ。全 thin 时，没有 addable edge 意味着 `v[C\R(Σ)]<λ`，故栈内总值大于 `(73/26)λ`。按高区间 `[3λ/4,λ)` 的项数 k 分类：

- k≥3：三项各价 λ，足付 3λ。
- k=0：价格大于 `(6/5)(73/26)λ=(219/65)λ>3λ`。
- k=1：余项总值大于 `(47/26)λ`，余价格大于 `(141/65)λ`；再加一项 λ，得 `(206/65)λ>3λ`。
- k=2：两项先付 2λ，余项总值大于 `(21/26)λ`。逐项缩小至总值 `c=21λ/26` 不增加价格。将两个小于 λ/2 的项合并或挪至 λ/2，可减少小项数、保总和且不增价格，最终恰余两项：小项 `c−a` 与大项 `a∈[λ/2,3λ/4)`。不能剩一个项，因为总和 c>3λ/4；不能有两个大项，因为 c<λ。令 `g(v)=3λv/(2λ+v)`、`h(v)=3λv/(3λ−v)`。固定和、`ab>cd` 的分式比较支付跨界合并。`g(c−a)+h(a)` 导数为正，其符号为 `q(t)=3(73/26−t)^2−2(3−t)^2`，t=a/λ。`q'(t)=2t−63/13<0`，且 `q(3/4)=6969/2704>0`，故全区间为正。最小在 a=λ/2，`g(4λ/13)+h(λ/2)=2λ/5+3λ/5=λ`，总价格至少 3λ。

因此是全玩家、全配置的对偶可行性，没有以有限样本检查替代量词。

### 2.3 Claim 32、逐 tuple 半收费与严格余量

对栈中每条真实 λ-minimal thin edge e，最小值资源 r0 给出 `Σ_e f≤3λ/2+f(r0)/2`。当最小项至少 λ/2，minimal 性迫使正好两项，使用 `f≤λ`；当最小项小于 λ/2 且最小、最大两项已达到 λ，同样只能两项；其余情形 `v_min<λ−v_max`，逐段得 `f(v)/v≤3λ/(2λ+v_min)`，再乘 minimal 性的 `v[e]<λ+v_min` 即得界。边界 `v=3λ/4` 也按连续接点成立，没有隐藏未付的单点情形。

f 非减，故 r0 可换成 e 中任一共享资源 s 而不减右界。每个 tuple `(ai,Bi)` 中 E blockers 彼此不共资源，资源最多出现在 candidate 与一条 blocker 两条边中。共用资源各付一半，每条边选一共享资源 s，所收不超过 `Σ_e f−f(s)/2≤3λ/2`。因此 tuple 总价不超过 `(3λ/2)(|Bi|+1)≤3λ|Bi|`。各 tuple 资源并集不交：新 candidate 避开全部旧栈资源，E blockers 本身不交，旧 blocker 不再能阻挡新 candidate。dummy 根资源为空，得到 thin 总价 `≤3λ(|B_≤ℓ|−1)`。

可达 fat 资源必须被 M 匹配，否则从 M 未匹配的 blocker 根出现增广路，违背最大匹配。将每可达 fat 资源付给其匹配玩家给出到 P+ 的单射，全部 blocker 玩家均未被 M 匹配、收不到此收费，故 `|P+|−|R_f+|≥|B_≤ℓ|`。于是总对偶余量至少

`(1−21λ/26)|B_≤ℓ|−3λ(|B_≤ℓ|−1)=3λ>0`。

这与 `CLP(1)` 可行时的弱对偶直接矛盾，所以 no-stuck 成立。这里只用可行性；并不读取最优 LP 解，也不使用目标最大性。给定任意可行正 T 的缩放扩展由此严格成立。

### 2.4 有限签名与总时间界

每次 Build 在原 ∞ 处增加有限坐标；每次非终止 Contract 保留较早坐标、把保留末层 blockers 数至少减 1，字典序严格下降。Contract 循环结束前最多只有当前末层可能为 0。其余非根坐标至少 1，根为 1；E 中 blockers 不重复，当前根尚未覆盖，故含 dummy 的总 blocker 计数至多 n，栈长至多 n+1。

坐标取 `{0,…,n}`，长度至多 n+1，全部签名数不超过 `Σ_{k=1}^{n+1}(n+1)^k≤(n+1)^(n+2)`。该保守界覆盖 n=1、dummy 不在 E、以及 Build 后/Contract 中瞬时末层 0 的细节。它与严格下降足够证明有限终止，每轮覆盖一个新玩家，至多 n 轮得到实际全分配。它完全不等于多项式总 clock，也不构成任何超多项式运行下界。

给定有理 T，单调用只有图搜索、子集与匹配更改、资源扫描、精确有理求和/阈值比较，未生成新资源权重。表示位长由输入与 T 的位长多项式控制；也可清分母比较，因此单调用 polynomial-bit 的论断成立。有限调用数乘单调用多项式只给有限/指数级总上界。

## 3. 对端算法证明与精确 remaining

§3–4、Appendix A/B 的路径/批量更新链确是另一合同：多条 node-disjoint 路径；canonical decomposition；unblocked λ-minimal I 与 blocked `(1+γ)λ`-minimal A_i；inactive resources 与 limited blocking；lazy `|I_i|>μ|B_i|` 的批量 Collapse。附录 A 的最大路径数可多项式求，附录 B 支付 canonical 与不变量，不是给 Appendix C 增加 LP oracle。

主文取 `β=γ²`、`μ=γ³`。Claim 16 需要

`λ < R(γ)=(1−3γ³)/(4+10γ+4γ²+3γ³−γ⁴)`。

对所用小正 γ，分母正且 `4(1−3γ³)−(4+10γ+4γ²+3γ³−γ⁴)=γ⁴−15γ³−4γ²−10γ<0`，故 `R(γ)<1/4<26/99`。不能把 Appendix C 的 λ 放入本证明。γ→0 的极限仅为 1/4；直接取 γ=β=μ=0 又丢失正几何层增长 `h=γ³/(1+γ)` 与正比例坍塌。形式上将 `1/(4+δ)=26/99` 解得 δ=−5/26，也不满足目标正 δ。

Lemma 17 的层增长和 Lemma 18 的带权签名计数才支付 `n^{poly(1/δ)}` 调用数。Appendix C 没有该计数，强数值对偶分析不会自动使它得到主文时间界。因此当前 edge.remaining 完整且不过度：目标特定 Build/Collapse、canonical/lazy/limited-blocking 不变量、几何层增长、固定 δ 统一多项式总位 clock、未知 T* 搜索均仍由目标自己的成熟证明承担。目标是 proved，不表示这些都由本边重新推出。

## 4. 两处 source 误植与现行登记影响

PDF p23 与 p24 已独立渲染目视核实，不是 pdftotext 的 OCR 错误：

1. p23 Case 2.2 已有余价格 `>141λ/65`，下一行错误排成 `>151λ/65+λ`。使用正确且足够的 `141λ/65+λ=206λ/65>3λ` 即可。较强错界不被本边、support 或当前中文合同采用。
2. p24 `a+b=c<λ/2` 的首个 `g(c)` 分式漏乘 c。按此前定义应为 `3λc/(2λ+c)`，恰与下一项 `3λ(a+b)/(2λ+a+b)` 相等，合并不增价格仍成立。

二者都有局部直接的正确替换，不影响 Claim 30、Theorem 2 或数值边。当前中文正文/注册陈述没有把这两个错误中间式当结论；support 明确记录正确式。无需修改冻结 PDF、源正文或提升两个对象版本。

PDF p27 的 `n^n` 粗计数把 dummy 写成 E 子集并略过零末层细节；support 的 `(n+1)^(n+2)` 是稳健有限替代，不是时间改进。中文正文只把 `n^n` 写作粗量级并明确有限、非多项式；核心注册合同只需有限终止，因此不存在需要源修订的结论冲突。后续复用应沿本包明确计数，而不要将原字面 `n^n` 作为精确小 n 的运行上界。

## 5. 全部 core coverage、formal receipt 与当前冻结状态

该 task 仅有 1 个 core，与 1 个只读 peer；coverage 恰有核心一项，无漏核心。已实读比较包含完整模型、两个定理合同、C.1/C.2 全证明链、反向为什么不能推出及主文 clock 为什么不迁移。因此 `linked` 可采用；这是负责核心的完整本次比较覆盖，不是声称解决源端点的同常数多项式时间问题，也不是声称不存在其它可比较对象。

当前任务 state=done、owner=Boss2；definition_pin、两个 input pins、正式 receipt 与 task 内嵌 receipt 全部一致。资产为 1 边 + support + ledger，逐字节 SHA 全部匹配。边的 endpoint_pins、evidence_pins、review_digest 与当前记录/文字一致。该边已在 registry canonical edge_files，integration 的 receipt/edge/object 语义 pin 以及 coverage 当前核心记录均匹配。24 项独立 JSON/字节核验全部通过；详细可机器检查证据见 refs.json。未调用 native checker，故不冒称重跑了 Boss2 的原生检查。

正式 receipt 的 `request_id` 指此前 read-add 请求，task 当前 `request_id` 指 done 请求；两者均在 task.requests 对应历史动作，无需强求相同。receipt 中 worker not-run 字段为原 worker 的来源记录，后续 root_mathematical_review.native_validation 明列 Boss2 接回后的 bind/check；不把先后两个主体混作矛盾。`all_three_edges_checked` 是 Boss2 的批内说明，此 task 可采用逻辑资产仍只有所列一条边，本审不认证额外未列资产。

`follow_up_tasks` 对应正式已发布 `boss2-wave17-santa-ga05-3c-2c145fadd5b8270e`，本快照状态 claimed/Boss2，题目精确承接统一总 clock 与未知目标编译。它没有被本包当作 proved 前提或已完成成果；其 pending 不阻断本包已经完整的 contribution/核心覆盖。本审只核该 follow-up 的正式范围/状态，没有把 GA-05 数学端点纳入本包实读覆盖。

主要冻结值：

| 项 | SHA / pin |
| --- | --- |
| definition pin | `1db265df4107f1cdda3131555f5e0a760642d5730c0f3a824af4adca1a175fde` |
| core registration pin | `94f3d06211128043b9b86c0d8c73049abf17e2551c7a14a47f99729d2f89e31e` |
| peer registration pin | `62077266d7b015a7d2ec0e854f173491f1d776d5d2dc840b88fb799d756ae49b` |
| task file | `3d780236d3bf4bac5c274f0cc9b565b9efe55978928132c05ee5926b223bac6d` |
| receipt file | `33cf0edb5ed04474a8fd07d6610e9cf1bdf1acaf3ccae92ec388079e0a538ae7` |
| edge file | `f558d05e00707f798578e495bf931e4c5a895c234293e4fd496816c058e889f1` |
| support file | `3b676dce201acc54e4373c88fd30a8f22f13f1c40fa46501638f1008faf04c48` |
| reading ledger | `a5a9574b00f2fc92738ba974e01d2a94981ad0ed2df92be0ace215290901f867` |
| Chinese source | `fa7375b5a1a8a5719b539df0192242461e713e6673735813a9f612dae7d1b574` |
| frozen PDF | `ea99b29b0b05694d16fcf18b63fddcd9dc798aa6ef476ac0b78033c8eaf90e7a` |

本审没有主库修改建议；Root 可在保持上述 exact contribution/remaining 的前提下采用当前包。若集成时任一数学文字、端点版本或证据字节已变，按 refs.json 定向核变化即可，不将此快照自动背书给新版本。
