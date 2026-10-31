---
id: "unrelated-machines/bamas-lindermayr-megow-rohwedder-schloeter-2023-santa-claus-makespan-matroids"
kind: "resource"
type_tag: "资源"
title: "Santa Claus meets Makespan and Matroids: Algorithms and Reductions"
status: "retained-literature"
truth_status: "literature-summary; not a theorem of this archive"
review_level: "full-pdf-text-read-and-cross-archive-comparison"
summary: "完整阅读 arXiv:2307.08453v1 作者版，保存 Santa Claus、unrelated-machine makespan、资源/作业拟阵推广之间的定义、近似归约、局部搜索算法和明确缺口；文献结论与本存档有限审计及一般命题保持分离。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/literature/unrelated_machines/bamas_et_al_2023_santa_claus_makespan_matroids_v1.pdf"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/literature/unrelated_machines/bamas_et_al_2023_santa_claus_makespan_matroids_v1.pdf"
source_ids:
  - "d23c74e5058f74aeed0d"
source_sha256: "fc907ac5159b3b20ae8498052c161f7aaf8d64114db84d7ef1947d6f1c6d4183"
source_blob: "246ae9e96acf19a68e8f5c3f57147629192140cb"
source_size_bytes: 512937
bibliographic:
  authors: "Étienne Bamas; Alexander Lindermayr; Nicole Megow; Lars Rohwedder; Jens Schlöter"
  version: "arXiv:2307.08453v1 [cs.DS], 2023-07-17"
  pages: 37
reading_evidence:
  extraction: "pdftotext -layout; 1975 text lines; definitions, Theorems 1-4, 7-9, 10-16, 21-23, Lemmas 11-14 and 24-37 read"
  local_export: "/workspace/scratch/3566036a3e78/bamas2023.pdf"
---

# 阅读范围和文献身份

这是冻结在 history/source/literature/unrelated_machines 的作者版 PDF，不是本仓库的证明稿。clean show 返回的 legacy-cleanup 与 main 两个提交具有同一 blob、SHA-256 和 512937 字节大小。已用 Poppler pdftotext -layout 导出 37 页全文，阅读摘要、引言、模型定义、归约、局部搜索、附录关键引理/定理和结论。外部引用只按作者版陈述记录，没有把它们当作本批独立核验。

文献研究两个目标：

- Santa Claus（max-min fair allocation）：有限玩家和资源，资源 j 对玩家 i 有非负值 v_ij，每项资源分给一个玩家，最大化最小玩家总值。
- unrelated parallel-machine Makespan：有限机器和作业，处理时间 p_ij 为非负数，不可用端点相当于无穷，每作业分给一台机器，最小化最大机器负载。

restricted 特例把每项资源或作业的非零值压成一个公共值。文献再为每项资源或作业附加整数 polymatroid，并要求选择一个 basis，形成 resource-matroid Santa Claus 和 job-matroid Makespan。rank-one uniform matroid 情形恢复传统 restricted assignment。

# 可直接引用的文献结论

## 1. 一般 Santa Claus 到 Makespan

Theorem 1 的量词是：对任意 alpha >= 2，若存在多项式时间 (2 - 1/alpha)-近似的 unrelated Makespan 算法，则对任意 epsilon > 0 存在多项式时间 (alpha + epsilon)-近似的 Santa Claus 算法。

证明分两层。第一层（Lemma 11）对值类型做舍入，使每个玩家只需多项式数量的配置，损失至多 1+epsilon。配置是按值类型计数的多重集，不是完整全局分配。第二层（Lemma 12-14）把配置编译成 Makespan gadget：每个玩家/配置有 configuration-machine 和 selection job，每个资源有 resource-machine，配置 job 在自己的 configuration-machine 上编码其值，在相容的 resource-machine 上耗时 1。makespan 不超过 2 - 1/alpha 时，离开 player-machine 的配置 jobs 总大小至少 1/alpha，且每个 resource-machine 至多接一件，于是解码为每位玩家至少 1/alpha 的资源值。

这个方向只说明调度优于 2 的算法会带来 Santa Claus 的常数近似；没有给出 Santa Claus 一般常数近似已经存在，也没有把 gadget 自动变成当前存档的算法。

## 2. 两值一般模型等价

Theorem 2：对任意 alpha >= 2，存在两值 Santa Claus 的 alpha-近似算法，当且仅当存在两值 Makespan 的 (2 - 1/alpha)-近似算法。两值是 v_ij 属于 {0,u,w} 与 p_ij 属于 {u,w,无穷} 的模型，w >= u。两值时每位玩家的相关配置只有多项式数量，因此正向归约不再损失额外的 1+epsilon；反向归约保持两种作业大小。该等价不应推广到任意多值 restricted assignment 或任意 matroid 实例。

## 3. 两值资源/作业拟阵双向归约

Definition 7 和 8 将每个资源/作业的分配改成从给定 polymatroid basis 取一个整数向量 x_j。resource-matroid Santa Claus 最大化 min_i sum_j v_j x_j(i)；job-matroid Makespan 最小化 max_i sum_j p_j x_j(i)。

Theorem 3：对任意 alpha >= 2，两值 restricted resource-matroid Santa Claus 有多项式时间 alpha-近似，当且仅当两值 restricted job-matroid Makespan 有多项式时间 (2 - 1/alpha)-近似。归约使用 polymatroid duality；Lemma 15、16 分别给出两方向。Proposition 9 说明同值项可先合并到一个 polymatroid，再用 polymatroid intersection 分解回原项。

## 4. resource-matroid Santa Claus 局部搜索

Theorem 4：对任意 epsilon > 0，restricted resource-matroid Santa Claus 有多项式时间 (8 + epsilon)-近似；两值时为 (4 + epsilon)-近似。

算法先约化为阈值子程序：给定 matroid M、polymatroid P 和 b，寻找 I_M 与 y，使每个元素要么在 I_M 中、要么 y(i) >= b；失败时给出排除更强值 alpha b 的证书，alpha = 4 + O(epsilon)。核心是 matroid 与 polymatroid 多重集合之间的递归交换：构造可加入集合 A、相关集合 C，追踪阻塞集合 B，并用 contraction 递归释放阻塞元素。

论文明确指出配置 LP 在该推广中不是充分的不可行证书：有实例的配置 LP 值为 m 而整数最优至多 1；简单的 r(X)+f(X)/b < |X| 也不能排除假解。该局部搜索只针对文献引入的资源拟阵模型，不是本仓库 CAG/SPE 客户模型。

## 5. 舍入接口

Theorem 21：给定值 T 的可行 resource-matroid assignment LP 分数解，可在多项式时间舍入为整数分配，最小玩家值至少 T - max_j v_j。证明在二部图上构造 polymatroid intersection，并沿资源顺序传递每个玩家的分数余量。

Theorem 23：给定值 T 的 job-matroid Makespan assignment LP 分数解，可舍入为 makespan 至多 T + max_j p_j，从而得到至多 2 OPT 的整数解。该证明使用相同的 polymatroid-intersection 整数性。

Lemma 22 把一般两值 resource-matroid 实例约化到一个无穷值 matroid 加一个单位 polymatroid 的规范子程序；重资源先整数处理、轻资源分数处理，再用 Theorem 21 舍入，可得到一般资源拟阵 Santa Claus 的 2 alpha 版本（在其外部算法假设下）。

# 与仓库正文的比较、用途和边界

## 保留的独有内容

1. 明确的配置选择 gadget：把“每个玩家选一个配置”编译成机器/作业，使 makespan 低于 2 的解能反解码为 Santa Claus 福利。
2. 资源/作业拟阵定义、polymatroid duality 归约和 local-search 证书框架，可作为第三阶段的文献来源或方法启发边。
3. Theorem 21/23 的 T 加减最大单项值舍入接口，可用于比较 assignment-LP 审计；它不能替代当前正文对具体支撑、配置合同或有限 Fraction 运行的精确分析。

## 不能从文献推出的内容

- 文献不研究有限客户目录、六位提供者、完整有序历史、纯 SPE 或覆盖主题人数至少最大主题一半；这些对象继续留在 customer-attraction 存档。
- resource/job matroid 是对每个资源/作业的 basis 选择，不能写成当前普通矩阵的隐藏通用约束；rank-one uniform matroid 只是 restricted assignment 特例。
- Theorem 1 是单向蕴含；Theorem 2/3 的等价只在明确两值和拟阵域内成立。文献没有给出任意多值 Makespan 到 Santa Claus 的反向归约，也没有一般 restricted assignment 的优于 2 算法。
- (8+epsilon)、(4+epsilon) 是算法近似保证，不是本仓库任何矩阵、合同或 SPE 的实际 makespan 证书。附录 LP 舍入不是全仓算法的外部验证。
- 本次未重新核验文献引用的所有外部论文、复杂度下界或历史最佳比较；这些保持为作者版陈述。

# 全仓比较和后续接续

已检索 archives/unrelated-machines 及 cleanup 清单中的 2307.08453、Santa Claus meets Makespan、resource-matroid SantaClaus 和 job-matroid Makespan。已有《极小超载星容量耦合与最小工作面支撑障碍有限审查》只抽取 Lemma 12-14 作为配置 gadget 背景；本页补齐整篇 PDF 的模型、Theorems 1-4、Definitions 7-8、Proposition 9、Theorems 21/23 和局部搜索证书边界，两者不是重复对象。其他正文引用的 Bamas 2024/2025 版本保持独立，本页只绑定 2023 版 d23c74e...。

第三阶段可建立以下关系，但不要造推导边：

- 与极小超载星容量耦合与最小工作面支撑障碍有限审查：文献来源/方法启发；后者的星族、GPC2 pair coupling 和 assignment-LP 支撑障碍仍由仓库自身证明或有限审计承担。
- 与完整菜单的资源度三路径归约：两者都把配置/资源机器编译为普通 unrelated-machine 任务，但文献 gadget 与本仓库显式 flat 菜单归约的量词不同。
- 与逐资源正权畸变与 kappa 边界：文献 resource-matroid/Santa Claus 接口可作背景；该定理依赖完整 flat 菜单、private 权和外部 restricted-Santa 算法契约，适用域不同。
- 与不相关机器与两个调度松弛定义：提供 makespan 与 assignment-LP 的术语背景；不替换该定义。

若需复核证明细节，应重新导出同一 SHA 的 PDF，不能依赖本地临时文本。
