# 运筹学与优化理论：从论文机制到可完成的研究选题

本分支的任务是重新选题并做判别性试攻。优先级：扎实可完成的数学贡献、清楚的论文叙事、研究生方向匹配；作者名气和问题年龄只是背景。原 UM-TARGET-v1 与其反面仍 OPEN，本分支不继续默认主攻。

## 用户当前指定范围

优先研究原子博弈、Nash均衡、近似公平分配和广义指派近似算法。六路分工见[当前前沿](RESEARCH_STATE.md)，原论文类型、工具本质、玩具模型、自然扩类和禁形/孔洞边界仍按同一标准比较。之前凸序、theta相关间隙等候选按原状态保留，暂不占本轮前排；不是数学否定。

## Research Goal

从高质量原始论文出发，广搜多个问题、提取工具与视角、形成精确候选、通过交叉 battle 和玩具模型选择值得投入的研究目标。用户预算为连续20天、每天12小时的 gpt-6.1-sol ultra 使用意愿；预算不构成可解性或发表保证。

## Mathematical Objects / Definition Map

尚未统一数学模型；每个候选独立固定对象、定义域、量词、假设及输出。A=作者明确开放问题，B=作者建议方向，C=本团队从论文机制派生的问题；C不能改称作者原题。论文类型分别记录问题、工具、视角、组合、分类，可多选。

论文原命题 → 工具接口与关键假设 → 最小toy → 候选精确版本 → 实验/证明义务 → 可完成成果包。任何跨箭头都要说明新增假设，实验不是证明。

## Claim Map / Dependency / Known Results

本分支的文献命题与新候选见 [CLAIMS](CLAIMS.md)。已有研究不因重新选题被否定，也不因小样本成功得到升级。现有[统一候选池](candidate_pool.json)保存45张原子/公平/GAP卡；[BATTLE](BATTLE.md)记录具体覆盖、反击与优先级变化。完整论文机制见[原子](lanes/atomic.md)、[公平](lanes/fair.md)、[GAP](lanes/gap.md)。

## Research Frontier / Open Problems

当前障碍是选题校准：旧文open可能已解决；小切口可能仅为已知定理直接推论；过度扩类可能重新变成巨大开放题。只有同时说明切入口与完整成果形态，才列前排。

## Next Actions

六线独立广搜 → 对前列原文和后续工作核查 → 跨线battle → 实际toy/有限枚举 → 选择试攻目标与备选。探索立即开始；battle是选题比较，不是开工审批。

## File Map

| 完整仓库路径 | 数学/操作资产与何时使用 |
| --- | --- |
| research/topic_selection/BOSS_START.md | 可复制完整研究提示词，含用户完整指导、论文内化历程、选题与直接研究、分支公屏及checkpoint命令；新对话首先读取 |
| research/topic_selection/RUNBOOK.md | 分支、身份、公屏、同步、恢复和保存的准确操作合同；启动或共享失败时读 |
| research/topic_selection/RESEARCH_STATE.md | 本分支当前前沿、候选试攻状态、尚未闭合义务与下一行动 |
| research/topic_selection/CLAIMS.md | 区分文献事实/派生问题/观察/可靠新结果的精确身份入口 |
| research/topic_selection/FAILED_ROUTES.md | 已解旧问题、被覆盖变体、不值得投入路线及原因；选题前去重 |
| research/topic_selection/branch_manifest.json | 独立研究分支、公屏、save、入口及基线SHA |

旧研究地图保留在父分支快照及原目录；本分支不复制旧正文。根 research/active_research.json 仍是旧main工具默认兼容合同，本分支显式参数和 branch_manifest.json 优先。

## 首轮可接续数学资产

- [原子博弈、公平分配与GAP的近期文献排雷及四代理有限核](notes/source_frontier_checks.md)：区分原文明确问题、摘要覆盖警报与既有反例；查新后才进入候选比较。

- [等长theta图相关间隙的有限公式与证明候选](notes/combinatorial_equal_theta_correlation.md)：论文建议方向派生，含支持约化纠错、双水平最坏边缘结构、完整草案及查新义务。
- [独立逐子集与联合分布LP探针](probes/equal_theta_independent.py)及[冻结输出](probes/results/equal_theta_independent_20261020.json)：用于交叉核查公式与边界，不认证一般证明或新颖性。

- [公平与分数效率的兼容边界](notes/fair_fpo_compatibility_boundary.md)：已知两代理反例的两种精确oracle复现，先排除一般兼容目标，再检查分类题的实质差额；不是原创新定理。

选题价值的类型化判据见[按论文贡献类型评价选题价值与可完成性](VALUE_CRITERIA.md)。本轮接续分支为 `research/or-topic-battle-20261020`，从已保存的 `1c3c22a9` 恢复；独立公屏继续使用 `topics/or-optimization-board`。

- [三类chores反例的精确复现与邻域边界](notes/chores_trivalued_exact_boundary.md)：排除过时的一般肯定存在目标，显示固定反例的近似障碍与参数非单调性；仅有限精确观察。

- [公共基交换图围长距离与原子博弈接口](notes/matroid_exchange_distance_and_girth.md)：原文明确猜想驱动的证明候选，含独立抽象拟阵穷举；还缺全球查新与应用价值核验。

- [四代理laminar关键核：精确枚举与顺序贪心障碍](notes/boss0_laminar_key_probe.md)：沿用作者A类问题，新增真实可行分配oracle、独立标签枚举和边界输入；保存有限证据与补偿交换义务，不宣称一般定理。

- [个性化双值EFX的单调补全障碍](notes/personalized_bivalued_monotone_completion_obstruction.md)：连续参数族否定任意公平起点的效用单调补全；含独立全分配核查，保留普通PO存在题的准确边界。
