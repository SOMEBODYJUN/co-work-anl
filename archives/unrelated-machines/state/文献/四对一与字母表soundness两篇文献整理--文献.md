# 四对一完美完整性与字母表—soundness 交易：两篇 PCP 文献整理

- **稳定归档 ID**：`literature-four-to-one-alphabet-soundness-20261031`
- **清洗角色**：第二阶段 cleaner，Boss2
- **实读来源**：
  - `1c704ec240f8eb0a6970`：Yumou Fei、Dor Minzer、Shuo Wang，*On the Hardness of 4-to-1 Games with Perfect Completeness*，ECCC Report 179，Revision 2（2026）。
  - `e1a3fa6c3f6a01e00e37`：Dor Minzer、Kai Zhe Zheng，*Near Optimal Alphabet-Soundness Tradeoff PCPs*，ECCC Report 27，Revision 1（2024 版文稿，来源目录按 2026 批次冻结）。
- **证据目录**：`archives/unrelated-machines/tools/evidence/retired-literature-four-to-one-20261031/`
- **阅读方式**：用 `clean show --out` 导出冻结二进制，保留 PDF；对两份 PDF 执行 `pdftotext -layout`，全文分别 7514、6503 行，阅读定义、主定理、证明概览、参数条件、关键 soundness/decoding 引理、应用推论、附录和作者明确写出的限制。`validate_sources.py` 对二进制 SHA-256、文本存在性和行数执行 PASS。

## 1. 先固定对象与量词

两篇论文研究的是 PCP/2-Prover-1-Round projection game 的值，不是 unrelated-machines 的排程可行域。统一的 2-Prover-1-Round 实例是二部图 `G=(L∪R,E)`、左右字母表和每条边的投影约束；策略给每个问题一个标签，`val(Ψ)` 是满足边的最大比例。凡是文中写成 “NP-hard to distinguish” 的结论，量词均是：给定任意固定误差参数，存在足够大的字母表或内部维度，使相应承诺问题在多项式或准多项式（论文特别说明时）归约下困难。不能把这些量词改写成对任意固定六人实例的算法下界。

Fei–Minzer–Wang 还使用 `d-to-d'` 约束：左字母表分成大小为 `d` 的块、右字母表分成大小为 `d'` 的对应块，允许关系是对应块的笛卡尔积。`d=4,d'=1` 就是 4-to-1；论文先构造稍弱的 sub-4-to-1 版本，再在附录 B 把它精确化为 4-to-1。Minzer–Zheng 只要求投影映射，核心参数是字母表大小 `R`（或二的幂 `q`）与值的 soundness。

## 2. Fei–Minzer–Wang：完美完整性的 exact 4-to-1

### 2.1 主定理与可直接引用的结论

论文的摘要和定理 1.6 给出：对任意 `ε>0`，存在正整数 `r`，使得给定左右字母表大小至多 `r` 的 4-to-1 game，区分

- **YES**：`val(Ψ)=1`；
- **NO**：`val(Ψ)≤ε`

是 NP-hard。这里完美完整性是结论的一部分，不能以 “接近 1 的完整性” 替代。定理 3.3 的 sub-4-to-1 版本先给出相同的 1 对 `ε` gap，附录 B 再证明每条 sub-4-to-1 关系可转换为 exact 4-to-1 而不破坏承诺。定理 1.2 复述基础 `GapLC_r(1,ε)`，用来说明其贡献是在严格的 4-to-1 结构下保留 perfect completeness。

由已知的 d-to-1 与图问题组合，论文明确得到：

1. **图着色**（Corollary 1.7）：对每个整数 `k≥3`，NP-hard 区分“图是 3-colorable”和“图不是 k-colorable”。这改善了此前只到 `k=5` 或 yes-case 允许少量错误的结果。
2. **8-color/独立集**（Corollary 1.9）：对任意 `δ>0`，NP-hard 区分“图 8-colorable”和“最大独立集比例小于 `δ`”。
3. **3-一致超图**（Corollary 1.10）：NP-hard 区分“2-colorable”和“没有比例至少 `δ` 的独立集”。
4. **低秩矩阵补全**（Corollaries 1.11、1.12，经 HMRW14 组合）：分别得到 `(k,3,0,c)` 及 `(k,8,ε,c)` completion 的 NP-hard 区间，其中参数 `k,c,ε` 按论文的明确范围取值。

这些推论是从 PCP 到图/矩阵问题的外部归约结果；正文没有把它们转译成排程配置、客户目录或 SPE。

### 2.2 三层构造：外层、middle、内层各自解决什么

论文把 perfect completeness 的困难拆成三个互相耦合的对象。

**外层 PCP。** 从二次方程系统 `3QSF_2` 出发。定理 2.4 的强 soundness 不是“任意单个向量不能满足很多式子”，而是：对每个固定 `r`，存在 `ε>0`，使得在 NO 情形下任取 `r` 个向量 `x^(1),…,x^(r)`，它们的联合（superposition）至多满足 `1−ε` 比例的方程。这个条件允许后续把答案视作低秩矩阵，同时阻断“用少数多个向量叠加骗过二次测试”的策略。外层采用带 advice 的 smooth parallel repetition，既压低值又保留 covering property。

**Middle PCP。** 直接把二次方程编码成二次 Grassmann 答案会破坏 covering property：Bob 只在变量子集上回答，向全空间补零得到的矩阵在未出现的行列上总为零，而典型全空间矩阵没有这种结构。论文试过稀疏 expander 或高维 expander 的 clique 局部 tensor test，但发现局部 rank-1 约束不够，作弊者可以在邻域内保持 rank-1、其余部分任意。最终把 tensor/low-rank 检查单独放进 middle PCP，并引入 **lazy parallel repetition**，在维持 soundness 的同时给下一层留出可用的 covering 质量。

**内层 PCP。** 使用标准 Grassmann encoding 与 Golowich 的 low-rank Grassmann 变体的混合图。内层的 Grassmann agreement test 不是传统纠错意义上的全局解码 soundness，而是论文所需的 non-standard soundness：若局部表在足够多 Grassmann 子空间上相容，就能在较低维的 zoom-out 子空间上解码线性函数。低秩版本配合 middle PCP 才能同时处理 exact 4-to-1 与 perfect completeness。

### 2.3 参数化 soundness 链

定理 3.3/定理 1.6 的证明在 Condition 3.12 下分成 Game1a、Game1b、Game2a、Game2b、Game3 五步。参数包括有限域维度、重复次数 `k`、Grassmann 维度 `ℓ1,ℓ2`、advice 维数、平滑参数和误差序列 `τ_i`；这些参数必须按条件式顺序选取，不能独立地把某个维度缩小。

核心桥梁是 Lemma 6.1：当外层 smooth game 的值低于 `q^{-ζ(δ)·ℓ^2}` 时，组合后的 PCP 值至多 `64 q^{-2(1-1000δ)ℓ}`（论文在式中取 `k=q^{2(1+c)ℓ}`、`β=q^{-2(1+2c/3)ℓ}` 的相容参数）。证明走逆命题：若 Alice/Bob 表的组合测试通过率高于该界，则经过 clique-consistency、zoom-in/zoom-out、Grassmann 线性测试和 list decoding，可解码出外层策略，从而与外层 soundness 矛盾。

Lemma 6.64 是最终 decoding 的关键形态：许多 Bob-packet 与 zoom-out 线性函数形成 sunflower 后，先在公共大空间上做 Grassmann 线性测试，得到一个全局线性函数，再用 list-decoding 证明它必须与某个 Bob 函数完全一致。论文明确指出这里需要把局部“与 `f_i` 有明显 agreement”提升成一个全局函数；单纯的二次损失会落到随机函数阈值以下，所以必须用更强的、与 agreement 同阶的解码论证。

### 2.4 论文内的失败机制与边界

- **二次 Grassmann 的覆盖失败**：Bob 侧投影补零造成全零行/列，不能近似覆盖 Alice 的典型矩阵；因此不能直接把二次检查塞进传统 Grassmann 内层。
- **稀疏 expander 的局部低秩不足**：局部 tensor test 允许“邻域内 rank-1、其余任意”的 cheating strategy；论文没有把该尝试当作完成的证明。
- **内层 soundness 的类型**：需要的是 non-standard、带 `Q⊆L⊆W` 条件的局部表解码，不是任意噪声模型下的传统低度测试定理。
- **参数与完美完整性不可分离**：若把 quadratic outer、middle lazy repetition 或 low-rank Grassmann 任一层换回普通线性/普通重复，原证明的 covering 或 exact 4-to-1 性质会失效。
- **应用边界**：图着色、独立集、超图和矩阵补全的推论依赖各自已知的组合归约；论文没有证明与 unrelated-machines、客户价值或 Nash/SPE 的直接等价性。

## 3. Minzer–Zheng：近最优字母表—soundness 交易

### 3.1 主定理与量词

定理 1.3：对任意 `ε,τ>0`，当 `R` 足够大时，给定字母表大小为 `R` 的 2-Prover-1-Round projection game，NP-hard 区分

- **YES**：`val(Ψ)≥1−τ`；
- **NO**：`val(Ψ)≤R^{-(1−ε)}`（正文排版写作 `1/R^{1−ε}`）。

随机赋值的基线约为 `1/R`，因此这是接近信息论极限的 alphabet-to-soundness 交易，但完整性仍是 imperfect（`1−τ`），没有给出 Fei–Minzer–Wang 那样的 perfect completeness。论文也说明构造在实例大小与字母表之间保持足够好的关系，且经轻微修改可以得到二部 biregular、bounded-degree 版本（定理 7.2）。

论文的关键技术性新引理是 Lemma 1.7：若一个线性表在许多 codimension-`r` 的 zoom-out 子空间 `W_i` 上分别与线性函数 `f_i` 有至少 `ε'` 的 agreement，且数量达到 `q^{Cℓ_1}`，当 `ε'≥q^{-(1−δ)ℓ_1}` 时，可找到更低 codimension 的 zoom-out `W` 和线性函数 `f`，其 agreement 仍为 `Ω(ε')`。它避免了早期解码引理的平方损失 `Ω(ε'^12)`，因为在本文参数区间那种平方损失低于随机线性函数阈值而失去意义。

### 3.2 组合结构与证明依赖

论文从 Gap3Lin 开始，构造带 advice 的 smooth variable-versus-equation game，再做平滑并行重复。内层用 subspace-vs-subspace/Grassmann 低度测试；证明大幅使用 Grassmann graph 上的 global hypercontractivity、低度/线性测试、list decoding 与覆盖性质。证明的流程是：

1. 外层提供低值和 covering property；
2. 内层在 zoom-in 子空间上得到局部线性一致性；
3. 若很多 Bob zoom-out 都成功，Lemma 1.7 把它们压缩成低 codimension 的全局解码；
4. 全局解码与外层低值冲突，得到定理 1.3。

论文在 Theorem 7.2 中把图变换为 `(d_1,d_2)`-regular bipartite 2-CSP，并保留 `val≥1−φ` 对 `val≤R^{-(1−ε)}` 的 gap。该版本是把 alphabet/soundness 交易接到有限度优化问题时的接口，而非一个新的 unrelated-machines 定理。

### 3.3 三个应用及其限制

- **Boolean Quadratic Programming（定理 1.4）**：经 ABHKS 归约，在准多项式归约下，NP-hard 逼近因子 `(log n)^{1−o(1)}`；构造需要实例大小、字母表和 soundness 同时满足，不能只引用定理 1.3 的值 gap。
- **有界度 2-CSP（定理 1.5）**：对足够大的 `d`，在随机归约下，最大度 `d` 的 2-CSP 在因子约 `(1/2−η)d` 内逼近是 NP-hard。独立集/无爪图推论还需要 Lee–Manurangsi 与 DFRR 的额外归约。
- **连通性问题（定理 1.6）**：结合 Laekhanukit、Manurangsi 的归约，得到 Rooted-k-Connectivity、Vertex-Connectivity Survivable Network Design、Vertex-Connectivity k-Route Cut 的幂次 hardness；随机归约的复杂性假设需保留，不能简化为确定性 NP-hard。

论文明确写出 **滑尺猜想边界**：covering property 似乎把 soundness 限制在至多关于实例大小的逆对数；作者不知道如何达到小于 inverse-polylog 的 soundness，因而该技术对 polynomial-size、constant-query、polynomial alphabet、inverse-polynomial soundness 的 sliding-scale conjecture 没有结论。这是方法的真实障碍，而不是未完成的排版细节。

## 4. 两篇论文的关系、相同点和不可替代差异

| 维度 | Fei–Minzer–Wang | Minzer–Zheng |
|---|---|---|
| 核心目标 | exact 4-to-1，`val=1` 对 `val≤ε` | projection game，`val≥1−τ` 对 `val≤R^{-(1−ε)}` |
| 完整性 | 完美 | 不完美（接近 1） |
| 主障碍 | 二次方程、covering、exact d-to-1 的三层兼容 | 在极低 soundness 下保持 covering 与近最优字母表交易 |
| 内层 | standard + low-rank Grassmann，middle PCP 做 tensor/低秩 | Grassmann/subspace low-degree test 与 global hypercontractivity |
| 关键解码 | Lemma 6.64：sunflower、线性测试、list decoding | Lemma 1.7：许多 zoom-outs 的近无损降 codimension 解码 |
| 主要外部应用 | 3-coloring、独立集、超图、矩阵补全 | Quadratic Programming、bounded-degree 2-CSP、连通性 |
| 明确限制 | 局部低秩 cheating、参数条件、非一般排程结论 | covering 限制 inverse-polylog，不能推出 sliding-scale |

共同点是：都把“高值策略”转成带结构的局部表，再用 covering + Grassmann 解码得到全局对象；共同的负面信息是，覆盖性质是组合归约能否闭合的关键。差异是，Fei–Minzer–Wang 为了 perfect completeness 引入 quadratic outer + middle low-rank 层，不能用 Minzer–Zheng 的 imperfect-completeness 结论直接替换；反向也不能用 Fei 的 4-to-1 结论推出近最优 `R^{-1+o(1)}` soundness。

## 5. 对当前六人 SPE/目录覆盖模型的接续判断

当前主模型是六个单位客户、有限非空共同目录、六个提供者沿完整有序历史各选客户子集，终局客户价值在覆盖者间均分；目标是每份完整历史纯 SPE 的覆盖人数至少达到六个目录主题最大覆盖人数的一半。两篇 PCP 不是该模型的证明，也没有给出客户效用、提供者策略、子博弈完美性、任意平局或空主题处理的定义。因此本文件只建立以下**接口和障碍**：

1. **可作为硬度压力源的抽象**：projection-game 的“局部标签一致性”与目录/历史上的局部选择一致性有形式相似性。若第三阶段要主张某个自动构造或搜索程序对所有完整历史都能高效找到半覆盖 SPE，应先说明其输入如何编码成有限 game，以及归约是否保留共同目录、零客户、离轨历史和任意平局。两篇论文没有完成这一步。
2. **完美完整性警告**：任何把“存在一个全局可行标签”类比为“存在一个完整历史 SPE”的论证，都必须处理 Fei 论文所强调的完美完整性与近完整性的差别。当前模型的“完整历史”与“纯 SPE”是量词要求，不能由高概率或 `1−τ` 近似替代。
3. **覆盖性质警告**：PCP 证明中 covering property 不是字段检查可以代替的假设。当前目标的“覆盖者均分终局客户价值”也需逐历史验证；把目录主题覆盖数或摘要中的最大值直接当作 SPE 的均衡收益，会跳过偏离者的策略可行性。
4. **失败机制的转译**：Fei 论文中的 quadratic-Grassmann 补零、稀疏 expander 局部 rank-1 cheating，是一个有用的反例模板：在当前模型中，局部目录覆盖或单个客户的局部最优不保证全局历史可延拓；必须记录未覆盖主题、离轨历史与所有提供者偏离。
5. **可复用的证明组织**：若以后要把六人模型编码成有限约束系统，可借用两篇论文的“外层承诺—中间保持覆盖—内层解码”分层记录方式；但这是方法借鉴，不是已证的等价变换。第三阶段 mapper 需要新增显式关系证据，不能把本文件直接导入为主线定理。

因此，本批结论在当前工程中的分类是：

- **完整文献结论**：两篇原文的主定理、关键引理、应用范围和作者明确限制，已由全文与证据副本固定。
- **条件结论**：把 PCP game 或其 bounded-degree 2-CSP 作为当前模型的压力测试，需要另行给出编码和效用保持证明。
- **候选接口**：covering/局部到全局解码的证明组织可供 mapper 设计来源关系。
- **障碍/反例模板**：局部 rank-1、补零、近完整性替代完美完整性、inverse-polylog soundness 边界。
- **未解决问题**：没有从任一论文推出六人有限共同目录模型的半最大覆盖 SPE 下界，也没有证明该目标的 NP-hardness 或多项式算法界。

## 6. 去向与交接

两份 PDF、两份完整抽取文本、`source-manifest.json`、`validate_sources.py` 和 PASS 的 `validation.json` 归入 `archives/unrelated-machines/tools/evidence/retired-literature-four-to-one-20261031/`。本正文归入 `archives/unrelated-machines/state/文献/`；没有把原 PDF 的摘要当作已完成数学证明，也没有删除未使用的失败机制。

第三阶段 mapper 应至少登记以下关系：

- `1c704ec240f8eb0a6970` → `exact 4-to-1 / perfect completeness / graph-coloring hardness / low-rank PCP`；
- `e1a3fa6c3f6a01e00e37` → `alphabet-soundness tradeoff / bounded-degree 2-CSP / quadratic programming / covering barrier`；
- 两者共同 → `Grassmann decoding + covering property`，但 completeness 与 soundness 参数不可互换；
- 当前六人 SPE 模型 → 仅 `methodological interface`，关系证据待第三阶段补写，不能标作“已适用”。
