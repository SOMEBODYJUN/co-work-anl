# 个性化双值物品的公平分配不能逐效用单调补全

用途：否定一种看似自然的证明路线，校准 EFX 与普通 Pareto 效率兼容问题的选题；不把方法反例当作兼容性不存在或独立论文成果。

## 精确身份

- ID/version：`SEL-PB-EFX-MONOTONE-COMPLETION-OBSTRUCTION-v1`。
- Origin：C，团队在阅读 Jin–Tao 后攻击的强路线；不是作者公开问题本身。
- Objects / Domain：三代理、五件不可分 goods，严格正可加估值；每个代理有自己的两个值。完整分配，每件物品归一人，普通整数 PO。
- Definitions：EFX 指任意代理 i,j 与任意 g∈X_j，均有 v_i(X_i)≥v_i(X_j\{g})。Y 严格 Pareto 支配 X 指每人效用不降且至少一人严格上升。
- Exact Statement / Quantifiers：对所有有理 a,b,c 满足 3/2<a≤2、b≥2、c>2，并且 a<2 或 b>2，下述 X 是 EFX、不是 PO，且不存在 EFX 分配 Y 严格 Pareto 支配 X。
- Scope / Conclusion：否定“任意 EFX 分配均可在不降低任何人效用的条件下补全到 EFX+PO”。不否定每个实例存在某个 EFX+PO，也不否定允许暂时降效用或改变起点的方法。
- Dependencies：下述直接计数与 EFX 定义；无外部黑盒。
- Evidence：作者线给出参数族证明草案；root 不导入作者 oracle，以 Fraction 独立穷举基例全部完整分配及参数/边界/退化输入。
- Counterevidence / Objections：此路线比真正存在问题强，故反例的独立价值有限。全球新颖性未确认。基例实际上有 EFX+PO 分配。
- Status：范围明确的证明草案与独立有限核验；未进入 current 可靠新定理层，不宣称新颖或足以独立成稿。
- Related Files：[独立审计](../probes/personalized_efx_completion_independent.py)、[冻结证据](../probes/results/personalized_efx_completion_independent_20261020.json)。

## 与原论文的关系

[Jin–Tao, On Pareto-Optimal and Fair Allocations with Personalized Bi-Valued Utilities, arXiv:2507.18251v2, 2025-10-17](https://arxiv.org/html/2507.18251v2)，§3、§5：原文给整数比率的 PO 验证/补全工具，并明确提出 EFX 与普通 PO 是否总兼容。原文已说明 MNW 与 Fisher/fPO 的自然方法会失败。本文攻击的是另一条更强的桥：先随便取 EFX，再只走效用不降的路径到 PO。

## 构造与完整论证

估值矩阵为

| 代理 | 物品1 | 物品2 | 物品3 | 物品4 | 物品5 |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | a | a |
| 2 | 1 | 1 | b | 1 | 1 |
| 3 | 1 | 1 | c | c | c |

取 X_1={4,5}、X_2={1,2}、X_3={3}，自身效用为 (2a,2,c)。每个对比包至多两件：代理1删除后所见最多1；代理2删除后所见最多1；代理3看代理1删除后为 c，看代理2删除后为1。因此 X 是 EFX。

设 Y 弱支配 X 且至少一人严格改进。所有代理须非空，所以代理1至多拿三件，至少拿两件。

如果代理1只拿两件，由 a>1，达到2a的唯一可能是仍拿{4,5}。代理3需效用至少 c>2，所以在剩余三件{1,2,3}中必须拿3；代理2需效用至少2，必须拿1和2。故只能回到 X，没有严格改进。

因此代理1拿三件，其他两人各一件。由2a>3，代理1至少拿4或5；代理3因 c>2 必须拿3/4/5的一件；代理2因目标2，只能拿3（b≥2）。所以代理3拿4或5，代理1必拿1、2及另一件高值物品。只剩两个可能的支配者：

Y=({1,2,4},{3},{5})，或交换4、5。

其效用是 (a+2,b,c)，由 a≤2、b≥2 且至少一处严格，确实严格支配 X。但代理3看代理1的包，删去物品1后还有效用 c+1>c，因此两个 Y 都不满足 EFX。这穷尽了全部支配者。

## 实际独立核验与边界

基例 a=2,b=3,c=4：root 穷举243个完整分配，X效用(4,2,4)，恰有两个严格支配者，效用均(4,3,4)，都违反EFX；整个实例有21个EFX与13个EFX+PO分配。数值已由独立 Python 回算，不能据此否定原作者存在问题。

独立审计另核参数网格、等号边界和空物品/零值/大分母输入。3/2<a 的作用是排除代理1拿三个低值物品；c>2 的作用是强制代理3拿高值物品；a<2或b>2用于严格改进。边界不属于声称范围，即使某些边界也失败，不能省掉证明中的假设。

复现命令：`python3 research/topic_selection/probes/personalized_efx_completion_independent.py --output /tmp/efx_completion_rerun.json`；必须给临时输出路径，不覆盖冻结证据。冻结文件与程序 SHA 在阶段保存回执核对。

## Honest salvage 与下一判别

失败类型是强路线命题为假。已排除效用逐点不降的任意 EFX 补全合同；保留了稀疏小参数族与精确 Pareto/公平独立 oracle。只有在限制起点、允许暂时效用回退或引入可证明全局势时重开。真正主选题仍应比较：个性化比率的结构界、两类物品加一个新类型、四代理 laminar 有限核等；不能因这条容易反驳的强猜想就默认新论文方向成立。
