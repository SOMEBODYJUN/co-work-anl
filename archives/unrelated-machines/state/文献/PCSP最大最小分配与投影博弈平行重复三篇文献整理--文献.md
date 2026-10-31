# PCSP、最大最小分配与投影博弈平行重复：三篇文献整理

- **稳定对象**：promise-CSP 的抽象代数、不可分物品 MaxMin allocation、投影博弈平行重复。
- **处理身份**：Boss2 / cleaner；三份冻结来源逐篇完整读取，二进制先用 `clean show --out` 导出，再用 `pdftotext -layout` 提取全文；提取文本和原 PDF 副本保存在 `tools/evidence/retired-literature-pcsp-20261031/`。
- **性质**：这是文献数学正文和适用边界整理，不把文献定理改写成当前六人 SPE 模型，也不把其复杂度/近似结论误报成新的仓库结果。

## 来源、稳定 ID 与证据

|稳定 ID|冻结来源|SHA-256|大小|全文证据|
|---|---|---|---:|---|
|`3f2b93ba359d4487b122`|`history/source/literature/unrelated_machines/barto_bulin_krokhin_oprsal_2019_algebraic_pcsp_v3.pdf`|`9c2c8d16c804c440cb7bbd15d8be68fce8b212722f5db284a4633b7d92bc1394`|794958|`algebraic_pcsp.pdf` + `algebraic_pcsp.txt`|
|`670daf7cbfc0c2948c1a`|`history/source/literature/unrelated_machines/bateni_charikar_guruswami_2009_maxmin.pdf`|`7f7b21ff08b37e8489e9f60527e9aa9458dc5cf4cd6cc6804869665c24d51f7f`|451682|`maxmin.pdf` + `maxmin.txt`|
|`0eaaaf4db05d1be24e86`|`history/source/literature/unrelated_machines/dinur_steurer_2014_parallel_repetition_author.pdf`|`7a7d2fcb62e173dabed10d69faa1e522055a811a228b707ab94f3e88b28dfdd5`|272532|`parallel_repetition.pdf` + `parallel_repetition.txt`|

`source-manifest.json` 固定了来源、导出方式、文本范围；`validate_sources.py` 对三个 PDF 的 SHA、文本存在性和非空全文做 PASS 核验。三份正文均从摘要、引言、定义、主要证明/算法、限制和结论读到参考文献，未只依赖旧摘要。

## 1. Barto–Bulín–Krokhin–Opršal：Algebraic Approach to Promise CSP

### 模型与核心定义

PCSP 模板是有限结构对 `(A,B)`，严格实例要求映射到 `A`，放宽实例允许映射到 `B`。普通 CSP 是 `A=B` 的特例；近似图着色是 `(K_k,K_c)` 的典型实例。来源把从严格域到放宽域、保持关系的多元函数称为 polymorphism；这些函数不能像普通 CSP 的多项式那样任意复合，因此作者把可复用的结构换成 **minor identities** 及其无交左右符号的 **bipartite minor conditions**。

一条 minor identity 是
\[
 f(x_1,\ldots,x_n)\approx g(x_{\pi(1)},\ldots,x_{\pi(m)}),
\]
其中 `π:[m]→[n]`；一个有限 identity 系统在相应 polymorphism 集合中可满足，就给出该集合的抽象对称性约束。所有 polymorphism 按取 minor 的操作组成 minion。来源反复区分：具体函数、满足的 minor 条件、minion homomorphism，以及由关系结构诱导的 PCSP 归约，不能把其中任一层直接替换成另一层。

### 主要结论

1. **代数归约**：来源的 Theorem 3.1 给出以 minion/多项式保持映射为条件的 log-space 归约方向；若后一 PCSP 的 polymorphism 满足前一方所有相关 bipartite minor condition，则相应复杂度可归约。Theorem 3.12 将任意固定 PCSP 与一个“给 projections/dictators 可满足、给该 PCSP 的 polymorphism 不可满足”的 minor-condition 判定问题联系起来，因而把 PCSP 的复杂度解释成抽象 minor 条件的可满足性。
2. **关系构造**：free structures、pp-constructions 和相应 minion homomorphism 结果给出另一条等价描述。Theorem 4.12/Corollary 9.5 把关系侧的构造与 minor 条件保留连接起来；这些是归约和比较工具，不是对当前仓库对象的均衡存在性结论。
3. **PCP 硬度**：来源用 Label Cover、Gap Label Cover 和 multilayered Label Cover 把 minor-condition gap 放大。对没有非平凡、低至三元 bipartite minor condition 的模板，Corollary 5.3 给出 NP-hardness；Theorem 5.23 复述 `PCSP(H2,Hk)` 对所有 `k≥2` 的 NP-hardness。近似图着色部分给出 `k`-可着色图不能在无额外假设下有效着成任意 `2k−1` 色的相应硬度陈述。
4. **可处理性侧**：local consistency、LP relaxation、affine Diophantine relaxation 章节把特定 minor 结构与算法联系起来；来源强调可处理 PCSP 还可通过 homomorphic sandwich `A→D→B` 且 `CSP(D)` 可处理来获得。它没有给出 PCSP 的一般 P/NP dichotomy。

### 证明结构与边界

- 证明的“完整性”通常来自严格实例映射保持；真正困难的是 Gap Label Cover 的 soundness、minor 条件不满足时的排除和 PCP/parallel-repetition 参数。
- `Pol(A,B)` 的具体函数值不能只用低维抽样替代；低 arity（三元条件足够产生某些硬度结论）是来源中的定量假设。
- 结论只对有限固定模板成立，且复杂度归约受输入编码和关系结构限制。来源结论明确保留 Boolean PCSP、图同态等更广分类问题的开放状态，也没有声称所有硬度都能脱离 PCP/parallel repetition。
- 对当前仓库的用途是：提供“抽象 minor 条件—PCSP 复杂度—Gap Label Cover”的来源链；它不提供有限单位客户、共同目录或 SPE 的 payoff 论证。该文档因此把它归入 unrelated-machines 的文献资料层。

## 2. Bateni–Charikar–Guruswami：MaxMin allocation via MaxMinDegree Arborescences

### 模型

有 `n` 个玩家、`m` 个不可分物品，玩家 `i` 对物品 `j` 的非负价值为 `p_ij`，分配价值是所获物品价值和，目标最大化所有玩家所得总价值的最小值。对偶目标是 unrelated parallel machines 的 makespan。来源用 `DegreeTwo`/`DegreeThree` 表示每件物品正价值涉及的玩家数上限，用 `InfDegreeOne`/`InfDegreeTwo` 表示无限价值边的玩家数上限；`NoInfCycle` 排除只由无限边组成的环。

### 完整结论

1. **Degree reduction**（Theorem 2.4）：任意 MaxMin1 实例可通过链式虚拟玩家/物品 gadget 变成大小至多 `mn` 的 `DegreeThree` 实例；每个高阶物品的副本中只有一个副本可服务原玩家。该等价保持多项式规模，但额外玩家会影响精确近似比的常数解释。
2. **DegreeTwo**：来源给出对称或非对称价值均适用的 4-approximation。核心步骤是求 M-LP、把小物品变量整理成 0 或 `1/2`、旋转大边消除环、对树组件使用 LP-Round，再处理每棵树的剩余大物品；令 `λ=4` 得到至少 `OPT/4`。Theorem 3.1 通过每个文字至多出现两次的 3SAT 构造，证明 DegreeTwo 即使对称也不能在 `P≠NP` 下优于因子 2；可满足时目标值 2，不可满足时至多 1。
3. **LP 与有限 gap**：来源的新 M-LP 比 configuration LP 更易写，能力相当；在 `InfDegreeOne` 上，M-LP/configuration LP 存在 `Ω(n^{1/6})` 的积分间隙（`InfDegreeTwo` 有相应 `Ω(n^{1/4})` 构造）。因此“LP 可行”不能直接当成整数分配证明。
4. **InfDegreeOne/Two 与新图问题**：定义 `MaxMinDegree Arborescence`，在有向图中找包含全部 source、arborescence 内非 sink 出度至少 `M` 的森林，最大化 `M`。依赖图把玩家和零/一价值物品作为顶点，边表示单位小物品关系；该问题是 InfDegreeOne 算法的技术核心。lift-and-project / Sherali–Adams `t` 轮和依赖舍入给出 `m^ε` 时间 `m^{O(1/ε)}` 的近似，并在拟多项式时间得到 polylog 近似；来源把 integrality gap 量化到 `max{polylog(m),m^{O(1/t)}}` 级别。
5. **硬度和延伸**：InfDegreeOne 也有因子 2 硬度（且可与 DegreeTwo 相交）；NoInfCycle 和 InfDegreeTwo 需要处理无限组件、反应链和随机删点后的完美匹配。来源没有完成一般 DegreeThree 的直接同样算法，而是把“无限环如何消除”明确列为障碍。

### 失败机制与硬度边界

Section 7 的 duplication gadget 说明，若用“三个显著物品复制可用性”的套路做硬度，DegreeTwo 算法和已有近似结果会把可得因子限制在 2 附近（作者明确指出该方法不能给出超过 2 的新硬度，较宽松地也给出 4 级障碍）。因此更强 hardness 需要离开该 gadget 路线。来源结尾把改进近似比/运行时间、MaxMinDegree Arborescence 的更精确复杂度、以及 Sherali–Adams 的 tight gap 列为开放方向。

### 对当前对象的处置

这是不可分分配/调度的历史文献。它的 `OPT/4`、因子 2 hardness、积分间隙和 arborescence 结论都依赖 additive utility、二部图、指定 `Degree/InfDegree` 类和复杂度假设；不能移植成当前六人有限单位客户、目录覆盖或 SPE 的福利保证。证据中的全文文本保留了 LP 约束、树组件舍入、gadget 和 Section 7 的失败边界，便于第三阶段只提取“可比较的有限分配结构”。

## 3. Dinur–Steurer：Analytical Approach to Parallel Repetition

### 游戏与算子

一轮两玩家游戏由二部问题图、字母表和边约束给出，`val(G)` 是最大满足约束比例；投影博弈要求 Bob 的每个答案至多对应 Alice 的一个可接受答案。`G^{⊗k}` 独立抽 `k` 条边并要求每个坐标满足约束。作者把游戏 lift 成 label-extended graph 和线性算子，定义 collision value `||G||`，并使用
\[
  \operatorname{val}(G)\le \lVert G\rVert\le \sqrt{\operatorname{val}(G)}.
\]

关键技术参数是乘法控制量 `val_+(G)`（以及 expanding 情况下的 `λ_+(G)`），使任意投影博弈 `H` 满足
\[
 \lVert G\otimes H\rVert\le \operatorname{val}_+(G)\lVert H\rVert.
\]
Theorem 1.8 的核心算子不等式是
\[
 \lVert G\otimes H\rVert\le \phi(\lVert G\rVert)\lVert H\rVert,
 \qquad \phi(x)=\frac{2x}{1+x}.
\]
来源通过 collision value 而非普通 `val` 直接相乘；文中还明确提醒普通值的同型乘法不等式一般为假。

### 主要定量结论

- Theorem 1.1：若投影博弈 `val(G)≤ρ`，则
  \[
  \operatorname{val}(G^{\otimes k})
  \le \left(\frac{2\sqrt{ρ}}{1+ρ}\right)^{k/2}.
  \]
  由此得到高值情形 `val(G)≤1−ε` 时的指数衰减 `≤(1−ε^2/16)^k`，以及小值情形的 `≤(4ρ)^{k/4}`。
- Theorem 1.7（少量重复）：当 `val(G)=1−ε` 且 `k` 远小于 `1/ε^2` 时，`val(G^{⊗k})≤1−Ω(√k·ε)`。来源把它与 odd-cycle XOR 的 tight 行为比较，而不是声称 strong parallel repetition 对所有游戏成立。
- 应用到 Label Cover：结合 Moshkovitz–Raz PCP，得到任意常数 `α>0` 的 `(1,ε)` Label Cover 硬度，字母表可控制在 `exp(1/ε^α)`；取 `ε=(log n)^{-c}` 并选 `α<1/c`，得到字母表不超过 `n` 的 NP-hardness。进一步经 agreement-soundness 与 partition-system gadget 得到 set cover 的 `(1−α)ln n` 级 NP-hardness（按文中复杂度假设和参数）。

### 适用边界

- 结论是投影博弈、二玩家和特定值/重复参数的复杂度结果；来源结论明确留下一般非投影游戏、XOR、多人游戏和其他分析框架的开放问题。
- 版本脚注记录早期稿曾错误声称一般约束可约化为投影约束，作者已撤回；本次读取按修订版结论，不把错误版本导入。
- 该文献支持前一篇 PCSP 综述中的 Gap Label Cover soundness 链，但不改变 MaxMin allocation 的 additive utility 模型，也不提供客户目录覆盖或均分 payoff 的直接证书。

## 跨来源比较与第三阶段接续

- 三篇文献都把“有限结构 + 精确量词 + 复杂度/算法边界”写在结果旁边：PCSP 依赖 polymorphism/minor 条件，MaxMin 依赖 additive utility 与 Degree/InfDegree，parallel repetition 依赖 projection game、collision operator 与 `k` 的范围。第三阶段若引用，只应连同这些假设和失败机制。
- 共同可迁移的是“先定义对象和严格量词，再给有限证明/算法，最后标出未覆盖的全称命题”的写法；不迁移其复杂度结论为当前六人 SPE 定理。
- 当前六人 SPE 的主题覆盖目标与三篇来源没有同一 payoff 或目录模型，故本批三源均归入 unrelated-machines 的 `文献` 类型；来源独有内容全部留在本正文与 evidence，不合并为现有客户吸引、facility 或 fair-allocation 的定理。
