# 重新选题：boss37本轮完成的实际前沿

更新时间2026-10-20。沿用research/or-topic-battle-20261020、topics/or-optimization-board及or-optimization-selection，未创建分支。actor固定R-cc0ca968777e443ea4d5031f3e9c4883。旧UM-TARGET-v1正反面仍OPEN，退出本轮默认主攻。

## 广度、实际团队与保存内容

本轮两批共六名gpt-6.1-sol ultra全部完成，均收到完整用户指导。环境总并发4含root，即3子槽，未声称六人同时工作。最终包括14条原子、6条Nash、20条公平、19条GAP，共59条候选记录；[完整索引](CANDIDATE_INDEX.md)和[候选池](candidate_pool.json)明确含淘汰/合并/已闭合子题，不是59个已认证开放题。

## 当前排序及实际数学增量

1. **先推进近二值图的公平参数算法**。FA17 simple min-charity有3^k poly完整证明，支持非负二进制删除cost；FA01的fixed-heavy unit-forest残差有binary-bit阈值DP及2^k受限推论。普通内部包平分有k=1反例。一般multigraph原A题仍未解。两小结果可能过短，需查新与实质扩张。
2. **保留资源轮廓的LP子模分类**。GA01已形成二维全b,w iff（非零列≤2射线）、任意维两射线充分性及二维三列禁形；高维不称iff，未得GAP近似算法。具体新颖性未确认。
3. **保留克隆不变性分类**。NA03已有active-cell 2^R poly识别、一般R的coNP包含、m2全正/m3失败及精确Farkas证书。旧coordinate-minimization/active-face理论需继续排覆盖，不能把KKT当新工具。
4. **原子势降级但保存**。64/59全人数type-scaled势及根式混合族优化成立；37/33不再可包装新最佳界，单{1,3}curl由HKM2011覆盖；势终止不等于poly步数。
5. **重大查重反转**。NA02虽被AAMAS2026仍列weighted Leontief open，本轮独立Fisher归约后找到Brandt NE=Lindahl + Tao–Zheng2025 duality + Orlin2010 exact算法直接覆盖，已淘汰新算法主目标。数学成立与新颖性通过严格分开。
6. **工具失败已存档**。背包fixed-x类内统一与任意Bernoulli拆分被精确反例否定；EC25基线1/3。配置支持已有确定性(1−1/e)/2旧工具组合基线；普通改常数不够立题。三值chores仅已知反例与有限邻域观察。

各项完整证明、来源、代码和冻结输出从[BATTLE](BATTLE.md)进入；[root独立复核](notes/round2_independent_root_review.md)列明证据与范围。没有将未查新候选升级成可靠新一般定理，没有对外宣布解决作者开放题。

## 本轮核验与接续

整数/Fraction实验与浮点探索分开记录；已闭合数学不靠继续加样本维持信心。原文卡区分完整阅读、只读定理、摘要警报与未完成覆盖。接续围绕前三个成果包的真实差额，保留FA03/FA11/NA05等备选；新反驳可直接改变排序，不需Route Card或开工审批。

首次45记录与安全并存合并已由work.py确认pushed于78361f3b1bb6c1aa885b4c68487492473f8bd53a。最终59记录的远端提交以本轮下一checkpoint回执为准，不预填未发生commit。结构检查只认证路由、字段和引用，不认证定理和新颖性。

## 旧资产与其他Work

等长theta、拟阵交换、四代理laminar、personalized EFX补全等既有同行资产保留原身份，未因本轮新排序删除或升级。其他Work的阶段记录如下，运行状态只代表各自发稿时刻。

## 同步保留的其他Work阶段记录

以下原样保留其他Work已保存的数学进展；其中运行状态只代表其发稿时刻，不替代本轮实际团队回执。

# 选题前沿

## boss0本轮实际接续（2026-10-20）

从既有2f5cf533恢复，沿用research/or-topic-battle-20261020与topics/or-optimization-board；未创建远端分支。发布身份R-889894680a2d4194b47020bdb5c477bf。六个全新gpt-6.1-sol / ultra研究员均实际启动，逐字指导已放进BOSS_START单一可复制块，且六人确认全文读取。六线为atomic PNE、Nash结构/动态、goods、chores/约束、GAP舍入、GAP结构。已在公屏告知重新选题；以下旧running文字仅是历史快照，不表示旧线程本轮仍运行。

第一批已形成[四代理laminar关键核探针](notes/boss0_laminar_key_probe.md)：独立枚举可行分配并逐项反算；有限输入都找到ordered EF1见证，同时排除顺序最大化效用的朴素算法。仍是原A类问题的有限Observation，不升级存在性。六线正在按类型化价值标准广搜、去重并交叉battle；未确定唯一主定理。下一义务是收到全部实物候选卡后形成规范候选池与比较，避免只有运行状态。

## boss6本轮接续（2026-10-20）

已从既有research/or-topic-battle-20261020恢复，未创建远端分支；save与topics/or-optimization-board保持不变。发布身份R-933d363a9e0e431aab148ceeef444958。六路已通知重新选题：原子结构、Nash算法、goods、chores、GAP、跨界反方。实际配置为三个新建gpt-6.1-sol ultra及三个复用gpt-6.1-sol max线程；后者的推理档位工具不支持在followup修改，不将它们冒记为ultra。全部收到当前指导，并要求全文读取含用户完整原话的BOSS_START。

首先保存的[原始来源排雷](notes/source_frontier_checks.md)给出覆盖层级与四代理laminar有限核的精确身份。候选池尚未收齐，当前不指定唯一主定理。chores线出现同密度budget-EFX的降序贪心证明候选，已交goods线盲攻；需完成自足正文、精确核验与查新，不能把简单地基当完整选题。

状态：六线广搜与首轮精读正在进行，尚未选定最终数学主目标。

当前优先方向为原子博弈、Nash均衡、近似公平分配、广义指派近似算法。本次恢复自2ff22b9；六个gpt-6.1-sol / ultra已实际启动，并完整读取含用户全部本轮原话的共同指导。当前六线为：

- atomic_pne：近似纯均衡、势函数和结构扩类；
- nash_dynamics：player-specific singleton均衡选择、随机动态和结构化Nash比较；
- fair_goods：goods侧WEFX/MMS与公平—效率边界；
- fair_chores：chores/mixed及冲突/类别约束；
- gap_rounding：MaxGAP、成本保持依赖舍入与hard-budget公平；
- gap_structure：多资源MinGAP、结构参数和容量扩张。

前一轮六线名称只作当时分工，不视为已保存候选。当前跨线battle已启动；以实际卡片、原文和精确实验为准，不用公屏口头计数替代资产。此前连续优化候选保留，暂不主攻。

首个新范围内可恢复试攻是[公平—分数效率兼容探针](notes/fair_fpo_compatibility_boundary.md)：已知两代理两物品类型反例由两种独立Fraction oracle复现。不是新反例或新定理；作用是排除未经核实的一般兼容目标，检验参数分类是否还有值得研究的差额。

需要减少的不确定性：原文是否明确提出；最新是否已解；候选是否只是直接推论；最小toy能否暴露核心机制；小结果能否扩成完整而不虚构价值的成果包。

下一行动：收齐独立卡片，交叉battle，核验前排来源与实际实验。不要把paper count、打分或通过软件检查称为数学进展。

## 首个实质试攻：CS-THETA-EXACT-v1

[等长多路theta图相关间隙](notes/combinatorial_equal_theta_correlation.md)已有覆盖所有整数路径数和共同长度的有限有理公式及证明草案。核心是原文Thm4.3的支持紧性、删除桥、路径内AM–GM及两坐标平方差凸性；全base约化曾遗漏restrictions，已由交叉攻击修正。状态是证明候选，新颖性和后置全面审查未完成。

[root独立探针](probes/equal_theta_independent.py)使用union-find逐子集秩、Fraction精确期望、所有rank不等式及全联合分布LP，与路径公式分开重构；[冻结输出](probes/results/equal_theta_independent_20261020.json)保存正常/零/自由拟阵/非法图边界与环境。有限核查不证明全公式。

六路仍在扩充不同论文族并写候选卡；不要将该首个可推导细胞直接变成唯一主目标。下一义务是跨线比较完整成果包，核验更一般series-extension覆盖，再决定投入。

## 本轮恢复后已核实的保存缺口

远端基线528c8d6含theta候选和探针，尚无完整候选池与六线比较正文。历史口头的“共同最坏分布”“幂网络误差界”不足以恢复精确身份，须重查原文，不能臆补。此前轮的六个研究员状态不随会话恢复；本轮六个gpt-6.1-sol ultra研究员已重新实际启动，分别完整读取用户指导，正在及时写lanes/。先行随机鲁棒卡已发现固定均值W∞球凸序极值被Gerhold–Gülüm Prop.3.2覆盖；W1及历史标签仍待独立核验。

即时动作：逐批保存稳定候选卡；对前排做原文与后续核查，收到具体跨线异议后更新排序。旧题、旧口头候选数和模型赞同不作为本轮已保存成果。

## 本轮实际接续（2026-10-20）

从远端1c3c22a9保留全部已有资产，在用户授权的新分支research/or-topic-battle-20261020继续。新启动六个gpt-6.1-sol / ultra：atomic_pne、nash_structure、fair_goods、fair_chores、gap_rounding、gap_structure，均须全文读取含用户指导的BOSS_START。旧会话的running文字不是本轮运行证据。新增VALUE_CRITERIA将idea类型与价值判据对应；候选仍在核验，不提升定理状态。

## boss32本轮阶段：从公开问题到具体交换引理

六个新gpt-6.1-sol ultra已实际启动，逐条读取完整用户选题指导；接入既有research/or-topic-battle-20261020及topics/or-optimization-board，未创建远端分支。首个可接续增量是[rank-girth交换距离证明候选](notes/matroid_exchange_distance_and_girth.md)：前向距离层秩下降、另一研究者statement-first反向BFS独立重构，以及root全抽象n≤5审计分别支持同一合同。尚不认证新颖性或已完成PoA新结果，继续广搜与battle，不因先得到小引理就自动锁唯一主目标。

查重已实际改变排序：ICAPL2025建议的strongly base-orderable hard-cost+Chernoff扩展，须先核SOSA2026 face-preserving框架及swap rounding的组合覆盖；不能忽略新工具而重复造定理。四代理laminar两key核继续攻击，但所有连续估值量词仍未闭合。

## boss41第一批可接续试攻

已接入既有research/or-topic-battle-20261020，不创建新远端分支；发布身份R-6632b20bf45d4fa6ba30666e1ca8c1df。本轮实际运行六个gpt-6.1-sol ultra子研究员，全部逐字收到用户当前完整指导。六路为原子拥塞、Nash结构动态、goods、chores约束、GAP、优化结构桥梁。

首份稳定资产[个性化双值单调补全障碍](notes/personalized_bivalued_monotone_completion_obstruction.md)否定一条强证明路线；root未调用scout核心，独立Fraction枚举基例全243分配、参数与退化边界。它不否定EFX+普通PO存在性，也未认证新颖性或独立论文价值。六路候选池与跨线battle正在落盘；不靠运行状态替代下一批实体卡片。
