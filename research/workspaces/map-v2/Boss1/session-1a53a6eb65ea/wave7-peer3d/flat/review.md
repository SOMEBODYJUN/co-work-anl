# Boss1：M8a→NF 当前平坦步骤 3D 数学核验

结论：本轮可接纳当前 done 包作为 **accepted / unconditional / contribution-step**。在以下实读边界内，没有发现阻塞数学问题；这不是 M8a 或 NF 的新 3A 主覆盖，也不把 NF 整条定量结论提升为来自 M8a 的无条件整结果。

## 冻结与回执

- Clone：`/workspace/scratch/1a53a6eb65ea/co-work-anl-boss1`。
- 冻结 SHA：`90e4ff1723256c59b1e87706b172c13fd67a2f6a`；结束前直接读取 HEAD/ref 仍为同一 SHA。
- Task：`boss2-wave9-flat-3b-07eb1949e26f831f`；本地正式 task 快照 state=done、owner=Boss2，done request=`786f8a07d03e4752aaee5b1296e6b2f3`。本审查未查询或改动 native queue。
- Task definition pin：`331782b11fe1dbb54944748b7b62091001c6c500fbd68beb8598083ee6d2da7a`。
- Receipt 原字节 SHA：`379f034eeb503c9b33d31ee20f536446d15a6b388c146ff1de0afdc4b69fdb11`。
- `rr.pin(task.receipt)`：`a5ae8d4c2c507275e4af5966e98ee4ad60e43e3d83a8fd94b8cd3619407bbe8b`；使用当前 tools/research_runtime.py 的 canonical JSON 算法独立计算。Receipt 文件 JSON 与 task.receipt 完全相同。

| 输入对象 | 当前版本 | input pin = 当前 registration pin |
|---|---:|---|
| M-8a8102ce2db9454ba1ed5eae66e12724 | 2 | `8c985cebfde20d2b788e4610e314e7fbdc6ca3525041db765165988c455715b9` |
| UM-GLOBAL-MOMENT-NEARFLAT-EXTRACTION-v1 | 4 | `3260dbb3dde9aa8112807f49374bf24da0c0af502b5285cbafbbf6a2655d8b2e` |
| UM-PREFIX-ATOMIC-DECODING-v1（只读） | 4 | `8a54b4990271f92b3532688d041d6e81792fa3cc5a4fe8db671c45d50864f528` |

| 交付资产 | SHA256 |
|---|---|
| positive-flat-to-original-T-HS-step.json | `9861647925a6cc723294921f0a19b26131fbea401c8e370b5cc81a4eba26cc35` |
| flat-original-T-support-proof.md | `a4b8f522304ce5a703f1fa807b3309c49e8d3e9dd9eaa75b39dbe7351bd0467f` |
| count-versus-mass-witness.json | `48678946f48b8a6af8e31de39edd30a9956f01cb49554aa2846adb63207c6f10` |

三资产、当前三对象全部登记 refs、边 evidence（去重共 21 个引用文件）均核过原字节 SHA。完整路径和逐项内容阅读状态见同目录 review.json；“核 SHA”不冒称阅读内容。

## 独立数学判定

1. **普通 Hankel lift 通过。** 在普通多项式环 degree≤4 上先做 Boolean/同任务冲突归约，定义的是按普通单项式乘积一致的线性泛函。C={1,x_e} 确实 connected to 1，C+ 是全部普通 degree≤2 单项式。平方行复制一次行，冲突二次行全零；普通矩为满射 F 的 pullback `FᵀM₂F`，故 PSD 且与 reduced M₂ 同秩。这里没有把后选独立基 b 误当 connected basis。
2. **δ=0⇔rank-flat 通过。** 每个 D_e=B_e*B_e PSD；迹和为零杀掉各个完整 B_e，而不只常数方向。因此所有二次向量进入 V₁，V₂=V₁。反向由 V₂=V₁ 立即给 B_e=0。归一化排除 R=0。
3. **正表示与合法原子通过。** 在上述精确合同上复用当前 M8a 的正有限表示定理。degree4 的 `(x_e²−x_e)²` 零平方、degree2 的 `(Σ_{e∈E_j}x_e−1)²` 零平方配合正权，逐原子强制 Boolean 和每原任务恰选一个原合法端，没有换模型或端身份。
4. **恰 R 个原子与 affine localizer 通过。** flat 使 affine 与 quadratic 评价像同为 R 维；于是 affine 评价空间含常数并对每个坐标乘法封闭，因而含支撑上的所有多项式评价。有限互异 Boolean 原子的单点指示评价遂在其中，故 N=R。评价矩阵列满秩，存在 affine q_s 隔离第 s 个原子。原负载 g_i 一次，`g_i q_s²` 次数≤3；原弱 affine localizer 因而给 `w_s(T−load_i(z_s))≥0`，正权推出每原子所有机器原 T 可行。这一步不需要强 helper 的 entry-wise 或 prefix-count 额外条件。
5. **HS 是 count 通过。** 加权 L² 评价等距同构把 A_e 化为 diagonal 0/1 projections；前缀 K 是 joint-support projection。其 G-HS²=rank K=相容支持原子个数。合法孩子精确分割 count；初始 R>0，每步最大分支保正整数，完整任务后恰为1。概率质量为 `||K v₀||_G²=Σ相容w_s`，与 HS count 一般不同。
6. **有理提取与总位复杂度通过。** G/H_e/A_e、有理 G-adjoint、score 比较均可精确计算。按任务对 v₀ 分裂为 A_eu；各层最多 R 个正交非零分支，最后正有理权是 G 范数平方，且重构全部四阶矩。固定矩阵的共同分母 Q 让至多 n 步乘积的分母取 Q^n，分子位长随 n、logR 和固定条目位长多项式增长；加上至多 R 分支及 d 个端，总位时间关于显式 (P,T,η,y) 长度为多项式。这里不按逆最小原子权、1/δ 或条件数循环，也不需要谱或开平方 oracle。
7. **短例独立复算通过。** 新写的 inline Fraction 小计算从显示的三个原子重建全部9个 reduced 矩、G、四个 A_e；与 witness 逐项一致，并验证投影和首轮 HS=(2,1)、次轮=(1,1)。首轮 mass=(1/50,49/50)，精确展示 count/mass 分离。未运行历史科学审计脚本。

## 与 canonical NF→PREFIX 的精确区别

既有 canonical 边：`map/edges/unrelated-machines-3a-3a-6992d380256546e6/um-nearflat-hs-pruned-support-to-common-prefix-law.json`，SHA=`576e3c28bee648bf224c66ac4059633c7f6a4d812f7d6918ba604886cf765493`。已完整读其 JSON，以及当前 PREFIX v4 record 与 body§3。

| 项目 | 当前新边 | 已有 canonical 边 |
|---|---|---|
| 起终点 | M8a 正 sparse-flat 表示 → NF 的 δ0算法步骤 | NF → PREFIX 共同守恒 law 接口 |
| δ范围 | 可精确检查的 δ=0 子域 | NF 数值阈值内的 δ≥0 |
| 新边直接补的承重 | ordinary lift；正表示；affine 原子隔离与原 T；HS=count；有理实现 | 枚举/剪枝保留叶构造共同 law；对任意相容部分指派可查询 |
| 正δ权与阈值 | 不支付 | 完整保留叶的 h 权归一，真实 T′=(1+3δ)T；h 前缀本身通常不守恒 |
| flat概率权 | 支撑与算法解释使用 count；真正概率为 v₀ 权 | 已用 `||Pσv₀||²` 正权，原 T 且重构四阶矩 |

新边既无 whole_result，又明确 contribution.remaining 保留整个 NF 的正δ commutator/近幂等/不塌缩/selected-loss 定量部分；它的 unconditional 是该已付数据子域上的闭合迁移，不声称 M8a 单独证明 NF 整条。没有新增 PREFIX 边，也没有把 HS h 当作精确概率 law。两核心 linked 用于本次3B比较成立，不代替各自原3A主覆盖。

## 当前承重源与真实阅读边界

- 已读仓内 AGENTS.md、prompts/03-map.md、prompts/03-map-worker.md，以及 IMPLEMENTATION 中实际阶段、边/收据、step/whole 与绑定合同。
- 三个当前对象完整 record、当前 task 的身份/版本/输入与交付字段、完整 receipt，以及新 edge、176行完整 proof、完整 witness 均已读。
- M8a body 的指定文献§2（41–59行）完整读。**本轮未重新读 Laurent 原 PDF 或其定理证明**；复用当前已登记成熟 theorem 的精确 connected-to-1、ordinary Hankel、positive、rank-flat 合同，再独立支付本实例的全部假设。
- NF v4 当前主审查指定§二（67–134行）完整读；其承重原证明 `global_assignment_moment_rounding.md` 222行全文完整读；共同 rational Gram/flat 原子资源73行、独立HS/强helper资源57行、六输入证书页46行均全文读。
- PREFIX v4 body§3（85–136行）完整读；canonical NF→PREFIX JSON 完整读。未重复读其全部历史 evidence 内容，也未复核通用生成/精度扩展的所有旧原件。
- 当前登记的其它 freeze/finite fixture/未归档审查内容只核精确 SHA，不冒称本轮全文读。数学结论依据新 proof 全文、当前承重定义/证明及上列成熟 theorem 合同；不依据旧程序 PASS。

已知源边界：原 NF source§6 仍显示最后的严格 `<3δ_e`，δ_e=0 时不能照字面使用。当前 NF v4 body 已明确 `≤3δ_e` 且 δ_e=0 时 loss=0；新 proof§8 也明确沿修正合同。本轮以当前登记主正文的修正合同为准，不把该旧严格号扩张到零缺陷。这不是当前新 edge 的未付前提。

普通实例如何生成适用共同矩、可靠失败语义、正δ一般原 T 支撑以及新困难性结论均未由此边支付，本轮也不声称重新审完这些其它义务。

本轮只写 clone 外本目录。启动时仅用只读 rev-parse/status 冻结状态；未执行 Git 写、native queue/work.py、clone 写入、凭据读取或历史科学程序。最终结论没有随 pending 清理目标缩小。
