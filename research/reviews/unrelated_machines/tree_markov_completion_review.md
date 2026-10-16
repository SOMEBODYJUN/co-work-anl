# 五机生成树再耦合反例的冻结独立审查

基准main：`8701a61b677f1b319053dfa82e7e12ebd7870e64`。
Claim：`UM-TREE-MARKOV-COMPLETION-NO-v1`。
所审正文 `research/current/unrelated_machines/tree_markov_completion.md` 的SHA256为
`73628429e0c9773a3cfc083a8b3d87ef3b20004a583df6f5dce2492309a31817`。
主代码 `tests/audits/unrelated_machines/tree_markov_completion.py` 的SHA256为
`981a354cfb9a41c939a967df8767a3f988d2d13cc732ceaeae802588ea6d72fb`。

内部研究员coupled_relaxation从“真实分布→树边pair→再耦合→固定树任务”接口独立
构造此例。主研究者随后只给local_barrier完整输入和精确待攻击陈述，未先给证明；
该研究员独立重建四态与最优补全，再读冻结全文及主代码。实际内部审查不等于外审。

## 实际覆盖

- 配置A/B是完整合法T=1调度；任务c单项下界与这两个调度证明OPT=1。
- 源D是真实全局分布，所以任意阶overlap数据都可相容；失效发生在丢弃非树相关性。
- path Markov分解的中间机器3恒空，确使左右分支独立；四态各1/4。
- 坏态冻结负载为(1,1/2,0,1/2,1)，c只能去两端，最优补全严格等于2。
- 限定量词是给定F、任一正概率态、冻结树任务。好态选择、换树、移动树任务和
  使用原D均未被排除。本例移动a到2即可修复，正文保留该事实。
- 至多4机器的连通树为star或double-star；一个顶点/中央树边覆盖全部树边。
  其fullstate/pair在D中出现，已决定全部树任务方向，原D状态提供补全。
  不将该边界推广到断开森林或所有算法。

未发现仍成立的fatal objection；未要求进一步数学修补。
两位研究员的独立性限于本组内部任务重构，不宣称外部匿名评审或全球新颖性。

## 可复现核验

主程序逐一构造32个完整整数分配、四个Markov支持态及每态两种c补全；
另独立复算所有单机和四个树边pair边际，检查保持完整配置状态。
Python3.12.14，Fraction/整数，无随机或浮点误差；退出码0。
冻结结果为 `evidence/runs/unrelated_machines/tree_markov_completion_audit.json`，
含完整输入、源分布、pair数据、四态和最优补全。

独立实现 `tests/audits/unrelated_machines/independent_tree_markov_completion.py`
不导入主实现，使用逐条件扩展生成状态，另按树边检查方向恰一端，
运行结果在 `evidence/runs/unrelated_machines/independent_tree_markov_completion_audit.json`。
它也检查32个全分配、四态权重、全单机/pair边际及坏补全质量1/4。
两个精确程序的实际输入均在源码与结果中完整保存，不需外部数据或seed。

核验只覆盖这个明确有限实例。普遍的至多4机器正面边界来自正文的覆盖顶点/中央边
论证，未通过有限测试自动升级。主目标仍OPEN，本反例不足以独立证明论文价值。
