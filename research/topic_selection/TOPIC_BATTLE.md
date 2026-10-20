# 运筹与优化选题比较：公开缺口、可攻接口与反方意见

研究日期：2026-10-20。六条 `gpt-6.1-sol/ultra` 子线收到完整用户指导后广搜并相互攻击。本文是 boss4 的选题判断，不是新颖性认证、录用预测或二十天可解承诺。完整候选和已淘汰题见各子线报告，跨线复核同题不重复计算数学成果。

**boss4本轮判断：最值得先投入承重证明的是两种容量 BMKP，其次是四人 laminar EF1 的有限瓶颈与三人 copies SD-EF1。** 这是基于原文入口清楚、可单独验证的关键义务以及本轮实际推导的判断；不是根据问题听起来宏大或样本通过率排序。低秩 chores 是值得保持的第四条。原子博弈保留小策略 PNE 分类，但尚不足以把经典复杂度边界当成短周期题；Nash 线发现的小加强经独立反方后已主动降级。

## 比较短名单

| 候选 | 精确入口与文章类型 | 值得做的结果 | 本轮实际进展 | 最危险的义务/停止条件 |
| --- | --- | --- | --- | --- |
| **GA-03 两种容量 BMKP** | Chen 等 ICALP26 §7 明问常数种容量能否 `(2/3−ε)`；问题突破＋配置舍入工具 | 两种容量 `{1,C}`、共同非负利润/正重量、硬容量不超载，所有固定 ε 的总位多项式真实分配 | 已形成联合类型、全局critical选择、短包嵌套匹配和独立小物品舍入的算法候选 | 按原文完整重建 profile 结构，逐条核假设与预算；需实际算法级重放，当前仍候选 |
| **FG01 四人 laminar EF1** | Cookson–Shah 2026 §5/Appendix B；结构归约＋有限基例 | 解开 K8、K12 的指定 ordered no-envy＋EF1，即可接四人共同laminar全类 | 原文归约/失败工具已读，数值枚举有证人；已复现 top-i 分散条件的反例 | K8虽物品少但估值连续，排名不够；作者已试过计算辅助。只增加随机样本则停止 |
| **FG02 三人 copies SD-EF1** | Cookson–Ebadian–Shah AAAI25 §3.3.2 明确问题；分类边界＋工具迁移 | 每类型副本等值、每人至多一件同类型、完整分配；先三人任意类型数 | 化为三序前缀的带正负三色平衡；有限域独立穷举一致 | 逐人误差1只给pair误差2，不能偷换；必须有保持全部前缀的共同交换或最小反例 |
| **FC-01 rank≤2 chores EFX** | Lin–Liu–Tao–Zhou 2026 §4 binary-submodular余留；分类＋组合编码 | 三平行类/loops的自然扩大，或最小sharp obstruction | 两平行类无loops得到完整EF构造草稿，有独立Hall攻击与实现核查 | 两类小引理单独成文体量不足；三类与loops各破坏原证明不同步骤，不能机械扩类 |
| **AG-01 小策略 PNE** | Bilò 等 AAMAS25 §6 p350 明确问题；复杂度分类 | 单位玩家、非减延迟、每动作≤2资源的PNE复杂度；先自然受限子域 | 精确转写局部二次势，查清global NP-hard不等于local PLS-hard | 经典归约的最大策略长度仍需精读核对；若重现著名PLS硬核，则不作二十天首押 |
| **NASH-02 随机反馈 RM+** | Anagnostides 等 ICLR26 §5 明确下一步；工具主导 | 真实 ε-NE、总样本计费、处理clipping与无偏噪声相关性的新记账 | 单玩家精确反例已否定“无偏⇒真势期望上升” | 若只是通用SGD/置信区间的改名则价值不足，必须和现成优化界比较 |

母论文原文：[BMKP](https://drops.dagstuhl.de/storage/00lipics/lipics-vol374-icalp2026/html/LIPIcs.ICALP.2026.60/LIPIcs.ICALP.2026.60.html)；[laminar](https://arxiv.org/html/2608.31121v1)；[copies](https://www.cs.toronto.edu/~nisarg/papers/constrained-fair-efficient.pdf)；[binary-marginal chores](https://arxiv.org/html/2608.10572v1)；[小策略拥塞](https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p343.pdf)；[RM+](https://arxiv.org/html/2510.17067v2)。原文位置与最近邻详见子线，不以此链接清单替代精读。

## 为什么把 BMKP 放在第一位

这不是重启一般不相关机的二壁垒。这里物品利润和重量不随背包改变，只有两种容量；原作者已解决相同容量，并明确留下常数种容量。新问题保留全机/全背包共同供给的实质困难，同时有具体可检验的桥。

本轮推进的是一条算法候选：对未知好解按容量使用有限profile；将两套物品标签取联合类型；同类型在所有long bins共同选最重critical物品，用轻物品换回原short/unused位置；short仅用未占用expensive池，借嵌套资格的固定基数最大权匹配；cheap池独立以LP补全。精确的版本、假设和当前缺口见 [候选正文](generalized_assignment/TWO_CAPACITY_LEMMA.md) 与 [独立反方](cross_field_battle/bmkp_algorithm_review.md)。

这条线经历了实际修正：利润必须cap以使类型数仅依ε；short singleton的预处理不能沿用相同容量的免费greedy；LP必须允许unused；OPT搜索不能假设成功谓词单调。我们还发现原文Lemma22字面“所有物品完整覆盖且容量不增”的合同不可直接使用，已用允许discard的独立BFS舍入草稿替换：每个背包损失至多四件小物品的利润上界。**这不等于推翻母论文总定理，也不等于算法候选已经完成验证。**

仍需将母Lemma8的全部前提、heavy-cheap删除及隐含精度重标、昂贵项数规范化和枚举命中性写成同一完整证明，并对算法本身做小规模精确重放。未完成这些步骤前，不对外称“解开ICALP公开问题”。若这些接口失败，保存真实反例和可复用的联合canonical/匹配/舍入模块，重新比较其他候选。

## 为什么保留两个 goods 题并行 battle

FG01有非常清楚的有限瓶颈：问题突破可以直接接到四人laminar全类。它的缺点同样清楚——有限物品不等于有限估值；真实任务是线性不等式区域的全域覆盖或有理反例。K8应先于K12验证，不能因样本有很多证人就直接外推。

FG02更适合先做完全序数化攻击：三人每种非全体副本数量只有两种，分数均分点只是起点，真正关键是有符号前缀的共同交换。其价值判据是跨越一般partition matroid已知反例，在等值副本类给结构定理或最小障碍。有限穷举本身不够，但纯离散表示使反例/归纳策略都更容易审查。

## 本轮主动降级和淘汰

- **AG-04 的玩家交互树保证均衡**：两玩家、每人两策略已出现改进环；树条件不够。不要把同一无均衡机制换参数再当新研究。
- **AG-03 有限网格最优势**：cubic有限LP候选在格外已失败。它只是合成方法的探索证据，尚无无限人数域证书。
- **NASH-04 稀疏重复平方**：代数与局部图证通过，独立审查把路径宽降到精确3，也修正了闭球和收益归一化语义。但原构造已有常数路径宽，真正新增主要是去掉高程度apex，论文价值近remark级，已撤出主押。下一题须自然正类或sharp边界，而不是包装小加强。
- **GA-01 成本保留Chernoff舍入**：查到2026框架可能通过自洽误差区域直接导出，已降为LIKELY_STANDARD_COROLLARY_PENDING_CHECK；没有为了每线凑两个主押而保留。详细推导和条件见[核查记录](generalized_assignment/COST_CHERNOFF_COROLLARY_CHECK.md)。
- 多个旧公平分配/均衡公开题已经有近期论文宣称解决或反例，逐题见报告。预印本的“作者宣称”、已发表定理、本组复核和撤回原因保持分层；不把撤稿自动当数学错误，也不把预印本自动升级成已核真理。
- 精确配额的双值chores MMS、restricted additive的简单效率因子等，可由流或短推论得到，留作工具，不用来凑主选题。

## 六线文件入口与读取条件

| 入口 | 内容与用途 |
| --- | --- |
| [原子博弈报告](atomic_games/candidate_report.md) / [JSON](atomic_games/candidates.json) | 小策略复杂度、拟阵动态、有限权重势、收费；读AG01/03的原文模型与反证 |
| [Nash报告](nash_equilibria/candidate_report.md) / [JSON](nash_equilibria/candidates.json) | RM+、Minty、稀疏精度、低秩枚举与样本复杂性；含降级理由 |
| [goods报告](fair_goods/candidate_report.md) / [JSON](fair_goods/candidates.json) | laminar key、副本、EF1+fPO、MMS与已解决旧题 |
| [chores报告](fair_chores/candidate_report.md) / [JSON](fair_chores/candidates.json) | rank2、混合图、配额三值与双值前沿；有完整局部证明草稿 |
| [广义指派报告](generalized_assignment/candidate_report.md) / [JSON](generalized_assignment/candidates.json) | matroid rounding、BMKP、Santa、GAP与新算法候选；先查严格预算合同 |
| [跨领域反方](cross_field_battle/candidate_report.md) / [JSON](cross_field_battle/candidates.json) | 同题独立重构与淘汰，重复条目是复核而非新增问题 |
| [局部秩成本证明](fair_chores/rank2_two_classes_lemma.md) | EF/EFX的准确范围、Hall翻转、算法及loops/三类失败点 |
| [Nash独立审查](fair_goods/nash_sparse_potential_review.md) | 代数/图宽核验、闭球反例与最强论文价值反方 |
| [核验与复现](VERIFICATION.md) | 实际脚本、冻结输出、算术、seed、范围及工程检查 |

## 当前决策及信息边界

优先审完 BMKP 的完整共同构造，保留 FG01-K8 与 FG02-三人作为两个可证伪对照；rank2 chores有可用新引理，后续投入取决于能否跨过一个真实分类边界。原子博弈与Nash保留成熟论文的精确入口，但不给它们虚构短周期成功率。

这已经改变了研究策略：每个课题必须尽早交出承重引理、反例或可审算法，而不是不断累计局部障碍；优先级随真实证据变化。旧UM-TARGET-v1及其否定仍OPEN，其长期资产仍在main和对应专题，本轮没有声称解决它们。


## 同行加入后的共同前沿

保存期间boss17在同一分支提交了不同短名单，已保留其[完整比较](peer_topic_comparison.md)和[AP-01/02原子精炼候选](candidates/atomic_potential.md)。其优先方向是非对称affine拟阵拥塞的normal-form纯perfect equilibrium算法、以及共同相对内部资源边际的非线性扩类；另有star mSOAC等入口。它们有同行推导和算术核查，仍是候选，boss4没有把本轮六线已经完成的独立审查范围扩写到这些新增稿。

双方优先级不必强行一致。boss4先审BMKP共同构造，boss17先攻原子精炼；下一轮应比较承重接口闭合、新颖性与自然扩类的实际进展。45条记录仅指boss4六线的结构化候选，不含同行另列候选。共同分支保存不表示任何一方结果已升级为定理。
