# 显式 XOS、分数 NSW 与福利舍入：三源边界资料

- **稳定归档 ID**：`xos-nsw-welfare-boundary-20261031`
- **角色**：第二阶段 cleaner，Boss2
- **本批来源**：
  - `5f270e7352cf6e1402fd`：显式加权 XOS 确定性 NSW 的 primary-source scope audit；
  - `608c39c70c3acf175aba`：显式 XOS 分数 NSW 与 normalized-menu/repair LP 的完整内部证明规格；
  - `ab17f5480379dea87a0c`：Feige 原刊福利舍入摘要定位记录。
- **证据**：`archives/unrelated-machines/tools/evidence/retired-xos-nsw-boundary-20261031/`
- **状态**：三份来源已全文读取并比较；第一份是文献范围审计，第二份是内部候选数学正文，第三份只支持摘要级事实。没有把内部证明规格或摘要事实升级为外部已认证定理。

## 1. 来源层级与共同问题

三份材料都围绕 XOS（fractionally subadditive）福利/NSW，但证据强度不同。

`5f270...` 的 finding 是一个保守的文献审计：在实际核对的 primary papers 中，没有找到“任意显式、加权 XOS 都有确定性常数 NSW 近似”的现成定理。DLRV 的 subadditive NSW 框架给出随机几何分桶/过滤和常数概率成功；它把候选集合固定后，把剩余随机性集中到每件物品的 round label。这个结构适合尝试 conditional expectation，但把期望势变成可计算的精确决策，仍需另行证明。Feng–Li 的 additive NSW 工作提供了对数 NSW 势和 coarsened DP 的确定性先例，却不是一般 XOS 定理。该审计还把确定性 submodular、binary-XOS 和 utilitarian-XOS 结果列为邻近但不同的范围。

`608c...` 是内部完整证明规格，自己明确称算法未实现、外审和全球新颖性未认证。它的价值是把对象、量词、位长和失败边界写成可检查的数学接口；它不是“已发表外部结论”。`ab17...` 只读取 Feige 原刊 landing page 的标题、摘要和出版信息，支持“fractionally subadditive 福利有 `1−1/e` 标准舍入”这一摘要级事实；没有下载全文，也不支持当前 gated-menu 的精确合同或新的 hardness。

因此本批的正确使用方式是：把 `608c...` 当作候选/内部证明接口，把 `5f270...` 当作外部文献范围和反过度宣称约束，把 `ab17...` 当作已定位的标准福利背景。

## 2. `608c...` 的完整内部数学接口

### 2.1 分数 benchmark 到 singleton rematching

第一组精确 ID 是 `UM-FRACTIONAL-BENCHMARK-REMATCHING-v1`。对象包括有限 agent 集、原物品集、指定的 `n` 个不同物品 `H`、残余物品 `B`、二进制有理目标 `V_i` 和显式正分数配置 benchmark `y`。域是有限、单调、次可加的价值函数；对正 agents 假设每个可行分数配置族 `z` 满足 residual 上界

\[
\sum_{i\in A,T\subseteq B}z_{i,T}\frac{v_i(T)}{V_i}\le c n.
\]

这里 `A={i:V_i>0}`，且非正 agents 在 `B` 上价值为零。对任意行和一、物品列和至多一的正 benchmark，正文证明存在双射 `π:[n]→H`，使

\[
\left(\prod_i[V_i+v_i(\pi(i))]\right)^{1/n}
\ge \frac{\mathcal B_v(y)}{c+1}.
\]

证明的关键是把每个配置的质量送到其 `H` 中 singleton 最大的物品，再用行缺口/列缺口运输补成双随机质量。耦合项的 ratio 被 residual 质量与 `|S∩H|` 分摊，前者由上面的 residual 分数假设控制，后者由 `H` 的列容量总和控制。对 `ln` 应用 Jensen，再用有限支撑的 permutation decomposition 得到某个双射的 log-product 下界。

正文还给出有限位比较：若正有理因子的分子/分母位长至多 `L`，不同完美匹配的乘积差至少 `2^{-2nL-1}` 的对数间隔；因此只需把 `ln` 近似到相应精度，就能通过有理最大权匹配得到真最大乘积。它明确处理零因子、空 `A`、空 `B`、重复配置和零 singleton，不在零上取对数。

### 2.2 显式有理 XOS 的确定性分数 NSW 规格

第二个精确 ID 是 `UM-EXPLICIT-XOS-DETERMINISTIC-FRACTIONAL-NSW-v1`。价值函数以有限 clause 表显式给出：

\[
v_i(T)=\max_s\sum_{j\in T}p_{i,s,j},\qquad p_{i,s,j}\in\mathbb Q_{\ge0}.
\]

允许零 clause、重复 indexed clause、unused item 和零系数；不要求全局 normalization、公共网格或最小正系数。该范围是显式有理 XOS，不是 weighted-agent、一般 subadditive 或 oracle-only XOS。

内部规格声称对每个正分数 benchmark `y`，输出真实不交 allocation，并达到

\[
\mathsf{NSW}_v\ge \mathcal B_v(y)/1125000.
\]

证明分成六层：

1. 在全部原物品上找正 singleton 最大乘积匹配；若 Hall 失败，则正 benchmark 也不可能存在，退化分支返回全空。
2. 对 residual `B` 做固定 lift，把显式 XOS clause 转成有理 polytope；用 clause 的 attaining state 保证 utility image 与实际 XOS 价值一致。
3. 用对数势和有限精度有理 LP，寻找满足 residual 质量的向量；规格给出固定步长、Hessian 余项和多项式轮数界。
4. 在支持集合内用确定性福利舍入和精确有限 CDF，把 fractional utility 变成 actual bundles；每一步保留物品不相交。
5. 用候选局部相对网格、逆矩和 deterministic mask 支付低质量项；该层是内部算法规格，不能引用外部 DLRV 随机过滤来代替。
6. 对任意比较排列 `π` 做 rematching，包括 cycles、零 residual 和 self-loop，最后在 `H` 上求真实最大乘积匹配。

文档还给出 bit-polynomial 说明：所有值、系数、LP、匹配、CDF 和 DP 状态都按二进制有理数处理，不按原始数值或最小正系数倒数展开；但它明确没有实现代码或软件审计。因此在清洗分类上，它是“完整内部候选证明 + 未实现”，不是已验证算法交付。

### 2.3 normalized-menu 的几乎所有组与 repair LP 边界

同一内部正文的第三个精确 ID `UM-NORMALIZED-MENU-ALMOST-ALL-AND-REPAIR-LP-BARRIER-v1`，把每个 clause 的系数归一到总量一，使用 unit-FSLP：每个 group 选择 state 的质量为 `λ_{g,s}`，每个资源的总 incidence 不超过一。若 FSLP 可行，则存在 benchmark 一，原 utility 的 unweighted log-CONFIG optimum 为零，且内部确定性 finder 让 NSW 至少 `1/3000000`，从而对固定 `η` 得到少于 `η n` 个组低于 `q_η=2^{-24⌈1/η⌉}` 的数量界。

repair 构造向每个原 group 增加同一批 `D` 个共享 singleton resources 和对应 alternatives。若原问题有至少 `n−D` 个 unit-quality groups，则增强问题有全体 unit allocation；反过来，去掉 repair items 后仍是原 allocation，至多 `D` 个组可被 repair 资源抬高。因此在显式 promise

\[
0\le a_{rep}<\gamma,\quad D\le a_{rep}n,\quad
0<\eta<\gamma-a_{rep},\quad \delta_q\le c_\eta
\]

下，增强问题的 unit-FSLP 可行性可作为 YES/NO 的有理 LP 检验。该证明保留全部原 groups、states、resources 和 jobs，不新增 agents，也不把 repair item 多次复用。

最后，内部 schedule 接口把每个 state 一个 private root、每个资源一个 resource machine、每个 incidence job 明确放置；选中 state 的 root load 为 `2-r_g`，resource machine 负载至多一，所以全矩阵 makespan 至多二，且低质量 group 数受 `q_η` 约束。文档明确说这不是所有机器 makespan `2−ε`、不是一般 UM solver，也没有给出从 NP-complete language 到该 promise gap 的 Karp reduction。

## 3. `5f270...` 的外部范围审计

该审计把 DLRV 框架定位为最接近的 primary precedent：随机 geometric item labels、固定 candidate set、constant-probability filtering。它核对了 DLRV 章节、Algorithm 1、Lemmas 4–6、Theorem 10/11，并搜索 `determin`/`derandom` 词干；没有找到论文自身已经声明的显式 XOS conditional-expectation oracle。

它还核对了 Feng–Li additive NSW 的两个可复用思想：

- 直接维护可计算的 logarithmic NSW potential，以不降低势的 rotation 操作取代随机选择；
- 围绕猜测的最大 item value 做 coarsening，再用 dynamic programming 处理 logarithmic configuration separation。

这两个思想是“证明路线的先例”，不是把 DLRV 的 XOS geometric filter 自动变成确定性算法的黑箱。审计特别列出三个不能扩大范围的邻域：submodular 的确定性常数近似、binary-XOS 的常数结果、XOS utilitarian welfare 的 deterministic factor-2。它们都不能直接证明一般显式 weighted-XOS NSW。

安全表述应是：“在显式 clause 表和有理运算模型下，若下述 conditional-expectation/DP 实现和势函数不降证明成立，则它是 DLRV 框架的表示特定 derandomization。”不能写成 demand-oracle、任意 subadditive、一般 weighted XOS 或首个 deterministic XOS 定理。

## 4. `ab17...` 的摘要级事实

Feige 原刊摘要只支持：fractionally subadditive valuations 的社会福利有 `1−1/e` 近似舍入背景。它没有提供当前部分激活菜单的 `H_{3/8}>2q/5` 合同，也没有陈述 NSW、repair LP、六人 SPE 或当前普通 flat-UM schedule。这个来源应保留为“标准 welfare rounding 的原刊定位”，不能当作当前证明的关键步骤。

## 5. 与已归档 NSW 文献及当前模型的关系

这三源与仓库已归档的 DLRV/subadditive NSW 文献属于相邻证据链。`5f270...` 说明外部 DLRV 仍是随机 framework；`608c...` 试图在显式 XOS 下补上分数 benchmark、确定性舍入和归一化菜单后果；`ab17...` 只补标准 welfare 的历史归属。三者不应被计作三个相互独立的 NSW 定理。

对当前六人 SPE/共同目录模型，适用关系仍是方法接口而非主线结论：

- XOS clause 表和有限 LP 可以启发如何记录一个有限历史下的候选质量/覆盖量；
- singleton rematching 与 repair 证明提醒必须保留原物品、原 jobs、共享资源的容量约束；
- deterministic log-potential 只能说明一种可能的算法组织，不能替代纯 SPE 的逐偏离检验；
- “几乎所有组质量”也不等于每份完整历史的主题覆盖至少一半，尤其不能忽略空主题、零客户、重复主题、离轨历史和任意平局；
- 内部规格所称 `2` 的 makespan 上界是完整 ordinary schedule 的接口，不能改写成当前六提供者价值均分的均衡收益。

因此本批分类为：

- **外部已知背景**：Feige 摘要的 `1−1/e` 福利舍入；DLRV/Feng–Li 在 `5f270...` 中的范围审计。
- **完整内部候选证明**：`608c...` 的三个精确 ID；保留其量词、位长、退化分支和未实现状态。
- **条件结论**：若显式 XOS 输入、LP promise 和 repair slack 全部满足，可使用该内部规格的接口。
- **障碍**：oracle-only、weighted/general-subadditive、全体组 minimum quality、近二主线与 SPE 均未由这些来源解决。
- **未解决**：没有从本批得到六人纯 SPE 半最大主题覆盖定理，也没有得到当前模型的 hardness。

## 6. 去向

全文源副本、manifest、SHA/行数校验和 PASS 的 `validation.json` 位于 `archives/unrelated-machines/tools/evidence/retired-xos-nsw-boundary-20261031/`。正文仅作为资料归档，不把内部 Proof v5 当作外部发表结果；第三阶段 mapper 可登记：

- `5f270...` → `DLRV randomized NSW / conditional-expectation gap / explicit-XOS scope`；
- `608c...` → `fractional benchmark rematching / explicit rational XOS / normalized-menu repair LP / schedule ≤2 interface`；
- `ab17...` → `Feige standard XOS welfare rounding (abstract only)`；
- 三者 → 当前 SPE 模型仅有 `methodological interface`，需要另外的历史—策略—偏离关系证据。
