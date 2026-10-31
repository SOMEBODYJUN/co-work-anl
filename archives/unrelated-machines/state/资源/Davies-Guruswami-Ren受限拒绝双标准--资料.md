---
id: "unrelated-machines/davies-guruswami-ren-constrained-rejections-v1"
kind: "resource"
type_tag: "资料"
title: "Davies–Guruswami–Ren：受限拒绝下的 Makespan、Santa Claus 与 Set Packing 双标准"
status: "retained-literature-source-read"
summary: "完整读取 Davies、Guruswami、Ren 的 arXiv:2511.00184v1（2025-10-31，18页）：(0.6533,3/2)-bicriteria Makespan 随机算法、受限拒绝 Santa Claus 的常数硬度、以及 (1-delta,epsilon)/(1-delta,1-epsilon)-bicriteria Set Packing 的算法与硬度。保留证明量词、失败机制和开放问题，不把文献结果升级为本仓库一般 R||Cmax 近二困难性或六人 SPE 结论。"
truth_status: "published-source theorem statements and proofs read; cited prior-work claims and novelty remain literature-level"
review_level: "full-18-page-PDF-export-and-layout-text-read; repository-cross-comparison; no external peer-review or novelty certification"
scope: "bicriteria unrelated-machine Makespan, Santa Claus with constrained rejections, bicriteria Set Packing"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/literature/unrelated_machines/davies_guruswami_ren_2025_constrained_rejections_v1.pdf"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/literature/unrelated_machines/davies_guruswami_ren_2025_constrained_rejections_v1.pdf"
source_inventory_id: "8f135f38c32ed1b60e40"
source_blob: "f38e6417ce32221c0af3d809199e06ea09f99c45"
source_sha256: "56c4706a59c8ee18a05e72a0fe01e772b3e849600ccb3d11859029a31b776ed0"
source_size_bytes: 577724
source_pdf_pages: 18
arxiv_identifier: "2511.00184v1"
paper_date: "2025-10-31"
legacy_ids:
  - "DGR-CONSTRAINED-REJECTIONS-2025-V1"
  - "UM-LITERATURE-BICRITERIA-REJECTIONS-DGR"
---

# 1. 实读范围与仓库定位

冻结源 8f135f38c32ed1b60e40 的路径是 history/source/literature/unrelated_machines/davies_guruswami_ren_2025_constrained_rejections_v1.pdf。本轮用 clean show --out 导出原始 PDF，核对文件大小 577724 字节和 SHA-256 56c4706a59c8ee18a05e72a0fe01e772b3e849600ccb3d11859029a31b776ed0；PDF 元数据给出 18 页。随后用 Poppler pdftotext -layout 读取全部正文、定理、算法、证明、结论和参考文献，不以摘要或旧索引代替全文。

这是一篇关于“允许固定比例拒绝”的双标准研究。它把普通 Makespan 的“全部作业都安排”改成在给定最优 makespan 阈值 T 下安排至少 alpha n 个作业，并把 Santa Claus 的“所有代理达到 T”改成至少 alpha n 个代理达到 beta T。第三个中间问题是 Set Packing：在已知存在把全集分割的 m 个集合时，允许从选中的每个集合取一个较小子集，并要求这些子集两两不交。

本页补上仓库已有 unrelated-machines 文献页没有的双标准来源。现有不相关机器与两个调度松弛、Santa Claus 配置 LP、Bamas 的 Santa Claus/Matroid 归约和广义指派资料可作背景，但它们不包含本篇的 0.6533 常数或 Set Packing 归约。本文不改变仓库的主问题边界：它没有给出一般 R||Cmax 的 (2-epsilon) 不可能性，没有把配置 LP gap 转成整数 hardness，也没有讨论当前六人、六提供者、有限目录的纯 SPE 覆盖目标。

# 2. 三个双标准模型

## 2.1 Unrelated Machines Makespan

机器集合为 M，作业集合为 J，处理时间 p(i,j) 非负；不可用边写作无穷。令 T 是把全部 n=|J| 个作业安排完的真实最优 makespan。对 0 <= alpha <= 1 <= beta <= 2，(alpha,beta)-bicriteria Makespan 的目标是在最大负载不超过 beta T 的条件下安排 alpha n 个作业。Theorem 1 专门给出 (0.6533,1.5) 点；这里的 T 是全部作业的最优值，不是先删作业后得到的更小最优值。

证明把有限边按 T/2 分成大边 E_L={T/2 < p(i,j) <= T} 与小边 E_S={0 <= p(i,j) <= T/2}。m* 是大边二分图上的最大匹配大小。因真实 T-可行完整调度在每台机器上至多放一条大边，删除所有大边后仍有至少 n-m* 个作业可由小边安排在 T 内。

## 2.2 Santa Claus

代理集合为 A，物品集合为 I，p(i,j) 是代理 i 获得物品 j 的非负价值，每项物品最多给一名代理。令 T 是所有 n 个代理都能得到的最小总价值的最优值。对 0 <= alpha,beta <= 1，(alpha,beta)-bicriteria Santa Claus 要求至少 alpha n 个代理得到总价值至少 beta T。文中研究的是允许 1-alpha 比例代理得到零价值，仍要求高福利的硬度。

## 2.3 Bicriteria Set Packing

给定全集 U 上的集合族 S，并承诺族中存在 m 个集合把 U 分割。目标是找 m'=alpha m 个集合 S_i，并为每个选子集 A_i subseteq S_i，满足 |A_i| >= beta |S_i| 且所有 A_i 两两不交。承诺中的分割是输入保证，不是算法需要先找到的证书。

# 3. Makespan 的 (0.6533,1.5) 算法

Theorem 1 的准确结论是：存在多项式时间随机算法；给定全部作业的最优 makespan T，算法期望在 makespan 3T/2 内安排
(6e-5)/(6e+1) * n > 0.6533 n > (1-1/e+0.02)n
个作业。论文把这一点作为从 beta=1 的 Maximum General Assignment 结果向 beta=3/2 的改进。

算法最终取两种候选调度中作业数较大的一个。

第一种候选在 E_L 上求最大匹配，得到 m* 个作业、makespan 至多 T 的确定性调度。真实完整 T-调度的大边部分本身是匹配，因此删掉它后仍有至少 n-m* 个作业只用小边且可在 T 内完成。

第二种候选先做只用小边的贪心，再对剩余作业做配置 LP 随机舍入。配置 LP 对每台机器 i 使用所有处理时间总和不超过 T 的作业子集 C 作为配置，变量 y(i,C) 满足每台机器选一个配置、每个作业被所有机器配置总覆盖为一。真实完整调度给出整数可行解。每台机器独立按 y(i,C) 采样一个配置，同一作业若被多机采样只保留一次。对每个作业 j，
Pr[j 被覆盖] = 1 - product_i (1 - sum_{C contains j} y(i,C)) >= 1 - 1/e，
故期望覆盖至少 (1-1/e)n 个作业，且机器负载不超过 T。这个组件是文献引用的早期 Maximum General Assignment 舍入事实；本轮没有重做其完整历史优先权。

小边贪心从任意当前完成时间向量 c_i <= T 出发，反复选可放置的最小处理时间边，把作业放入机器列表，直到无可行边；随后每台机器按处理时间排序，只取负载至多 T/2 的前缀。Proposition 1 的量词是：若从 c 出发可继续安排 S，则该循环至少把 |S|/2 个作业加入列表。证明用交换：若最小边不在固定最大可安排集 S，其所在机器上必有 S 中另一个可替代作业，且最小边不长于该边；替换后继续归纳。代入 n-m* 个小边作业，列表总长度至少 (n-m*)/2。由于每台列表总处理时间至多 T 且每条边不超过 T/2，最短前缀至少保留列表长度的三分之一，故算法在 T/2 内确定性安排至少 (n-m*)/6 个作业。

于是两候选的期望保证为
max{ m*, (n-m*)/6 + (1-1/e)(n-(n-m*)/6) }。
两条直线相交处给出 m*=(6e-5)/(6e+1)n，得到 Theorem 1。论文明确指出 T/2 截断是脆弱接口：降低小边阈值会失去每台机器至多一条非小边的计数，细分更多层也没有在该分析中形成更好的平滑 trade-off。这是算法障碍说明，不是任意细分算法都失败的下界。

# 4. 受限拒绝 Santa Claus 的硬度

Theorem 2：存在普适常数 delta,epsilon>0，给定一个所有 n 个代理都能得到总价值至少 T 的 Santa Claus 实例，若要找到至少 (1-delta)n 个代理得到至少 (1-epsilon)T，则是 NP-hard。

证明从 Theorem 4 的 Set Packing 硬度出发。设输入有 n 个集合，且存在 m=alpha n 个集合分割全集；NO 情形下不能找到 beta n 个 epsilon-almost-disjoint 集合，其中 alpha>beta>0，每个集合只可删除至多 epsilon 比例元素。建立 n 个代理：每个集合对应一个代理；物品包含全集元素对应的正常物品，以及 (1-alpha)n 个 dummy 物品。集合 S_i 的代理对其中每个正常元素的价值为 T/|S_i|，对不属于集合的正常物品价值为零；任一代理拿到 dummy 时价值为 T。

完整性：分割中的 alpha n 个代理各拿其集合元素，剩余 (1-alpha)n 个代理各拿一个 dummy，所有代理达到 T。可靠性方向：若有 (1-delta)n=(1-alpha+beta)n 个代理达到 (1-epsilon)T，至多 (1-alpha)n 个可由 dummy 满足，故至少 beta n 个代理只依靠正常物品达到该价值。每个此类代理得到的正常物品子集是其集合至少 1-epsilon 的比例，物品不重复分配，所以得到 Set Packing 的 NO 矛盾。参数关系是 delta=alpha-beta。

这是假设全体可达 T 的承诺问题上的双标准硬度，不是普通 Santa Claus 的任意实例近似比，也不是 R||Cmax 的硬度。

# 5. Bicriteria Set Packing 的算法

Theorem 3：对任意 delta>0，存在 epsilon>0 和多项式时间随机算法；若输入集合族存在 m 个集合分割全集，则期望找到 (1-delta)m 个集合及其两两不交子集，每个子集至少占原集合 epsilon 比例。

作者取 D=40/delta，C=400/delta^2，epsilon=delta^2/800，按集合大小分为小集合 |S|<=C 与大集合 |S|>C。小集合阶段在集合节点与元素节点之间建单位容量网络：源到集合容量一，元素到汇点容量一，集合与其元素之间容量一。最大流饱和的集合各取一个元素；因 epsilon<1/C，每个小集合取一个元素即满足比例。

大集合阶段解 fractional packing LP
max sum_S x_S subject to sum_{S contains u} x_S <= 1 for each u, 0<=x_S<=1。
有 m 个分割集合，所以 LP 最优值至少 m。独立按 x_S 采样集合。令 T 为被至少 D 个采样集合覆盖的元素；保留采样集合中 |S intersect T|<0.1|S| 的集合 B；将每个非热门元素随机分配给包含它的 B 中某集合；若集合收集到至少 epsilon |S intersect T| 个元素，保留之为 C。

每个元素的采样覆盖期望不超过一，Chernoff 界给 Pr[u in T] <= delta/20。Markov 界给采样集合因热门元素比例过大而被删的概率至多 delta/2，因此 E|B| >= (1-delta/2)E|A|。对 B 中固定集合，非热门元素覆盖次数至多 D，单个元素分配到该集合的概率至少 1/D；|S|>C 和第二次 Chernoff 界给收集不足概率至多 delta/2。故
E|C| >= (1-delta/2)^2 sum_S x_S >= (1-delta)m，
且每个保留集合取得至少 epsilon |S intersect T| >= 0.9 epsilon |S| 个元素。算法保证是期望意义；多项式时间表述依赖固定 delta 后的常数 C,D。

# 6. Bicriteria Set Packing 的硬度

Theorem 4：存在普适 epsilon>0 及 alpha>beta>0，给定集合族中存在 m=alpha n 个集合分割全集，若要找 beta n 个集合及其每个至少保留 1-epsilon 比例的两两不交子集，则 NP-hard。

论文从每个变量出现次数为五、每个子句恰有三个文字的 3-CNF 硬度出发，经 q-CSP 到 Set Packing 的标准超图构造。对变量 x 使用 Feige 超立方分割系统 V(x)=[d]^Sigma，其中 |Sigma|=2、d=5；第 i 个标签匹配由 e(i,j)={a: a_i=j} 构成。不同匹配中的两条超边交集为各自大小的 1/d=1/5。每个 CSP 子句和一个满足该子句的赋值对应一个集合，该集合是相关变量 gadget 超边的并。

固定参数是 q=3、|Sigma|=2、d=5、每子句有 eta=7 个满足赋值，故 |S|=7m，每个集合大小 k=q d^(|Sigma|-1)=15，全集大小 15m。完整 CSP 赋值给出 m 个互不相交集合，因此 alpha=1/7。若两个集合对应不一致的变量赋值，它们在相应 gadget 至少共享 gamma^q 比例元素，其中 gamma=1/5；取 epsilon<gamma/(2q)=1/30，则要使集合 almost-disjoint，只能在每个变量固定同一标签，从而对应全局 CSP 赋值。NO 情况下任意赋值最多满足 1-epsilon_0 比例子句，所以 almost-disjoint 集合数至多 beta n，其中 beta=(1-epsilon_0)/7。这里只给固定常数参数的 NP-hardness，不能外推为所有 epsilon 或所有集合大小的普遍阈值。

# 7. 文献关系、结论等级与不迁移范围

与仓库已有对象的关系如下。

- 与广义指派的费用保持与加性负载舍入：都涉及 unrelated-machine assignment 与 configuration/LST 传统，但该页处理费用/负载同时约束；本源研究允许拒绝的作业比例和 makespan 比例，算法接口不同。
- 与 SantaClaus 调度与受限指派配置界、Bamas 升投影 MMDA 与 SantaClaus：共享 Santa Claus、配置 LP 和受限指派术语；本源新增代理拒绝比例的硬度及其 Set Packing 中间归约，不替代配置 LP gap 或 Matroid 归约。
- 与广义指派的 1-1/e 覆盖：本源明确把该比例作为算法 2 的配置 LP 舍入组件；本轮核对了其在三段组合中的使用，但没有重新证明历史优先权。
- 与仓库中 R||Cmax 有限审计和菜单构造：那些是本地矩阵、有限枚举或特定接口证书；本源是外部文献算法/复杂度结论，不能把其双标准点直接贴到任何本地输入。
- 与当前六人 SPE：本源的 alpha,beta 是调度/分配保证参数，与六提供者依完整有序历史选目录客户子集、终局客户在覆盖者间均分的量词完全不同，不建立任何覆盖人数下界。

正式等级分开记录：

1. 已读文献定理/证明：Theorem 1 的 (0.6533,1.5) Makespan 算法；Theorem 2 的 Santa Claus 常数硬度；Theorem 3 的 (1-delta,epsilon) Set Packing 随机算法；Theorem 4 的 (1-delta,1-epsilon) Set Packing 硬度；相应定义、算法和主要证明。
2. 历史依赖/引用性结论：1-1/e Maximum General Assignment、LST 经典下界、Feige 3-SAT、Set Packing 既有近似/硬度、Golovin 的 Santa Claus 算法均按本文引用定位，没有在本轮独立重做外部论文的优先权或复杂度证明。
3. 作者开放方向：在 beta=1 附近提高作业比例是否需要 makespan 跃迁；接近 (1,2) 时拒绝少量作业能否达到 (2-delta)T；Santa Claus 中算法的 epsilon 与硬度的 1-epsilon 间隙；Set Packing 中 epsilon 接近 1/2 的阈值。
4. 不迁移：本页没有证明一般 R||Cmax 不存在 (2-delta) 算法，没有给出普通 Makespan 的新 NP-hardness 归约，没有把 bicriteria 参数当作当前六人纯 SPE 覆盖比例，也没有做新的随机实验或 LP 运行。

后续第三阶段若建关系，应把本页作为“外部来源 → 双标准调度/分配对象”的文献节点，分别连到仓库已有 Makespan、Santa Claus、Set Packing 对象；不能用一个 derives 边把四个文献定理合并成仓库内统一定理。
