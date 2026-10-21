# R-6cfe7c79118a41f6bd5659aa5d780852 的个人研究工作区

研究存档：`customer-attraction`；发布身份：`R-6cfe7c79118a41f6bd5659aa5d780852`。

## 当前研究

本对话用户称研究 Boss5；首次程序生成本页 actor，与其他对话身份独立。
唯一主目标 Q-CAG-HALF 保持原模型与每个完整有序历史纯 SPE 的量词，仍 **OPEN**。
六个 gpt-6.1-sol / ultra 内部研究分支攻击一般证明与真实反例。个人备份不自动提升共享数学状态。

## 有实质内容的阶段

- **静态 CCE 福利比较桥的反例。** 主审计与独立定义级审计已核验42客户版本：
  完整三人 SPE 福利32，而每个静态 CCE 期望福利至少33。
  新压缩版仅8客户：SPE福利6，而简洁有理对偶给每个静态 CCE 福利至少56/9；
  此版本主审计通过，独立审查与更锐值整理中。
  这不否定聚合静态安全值桥或原半覆盖。
- **分数覆盖的真实路径前缀预算。** 任意非空可覆盖比较客户集C，O=|C|，
  τ为目录对C的分数覆盖数，P_i为前i位玩家的最终收益之和，r=m−i+1，
  有 O≤P_(i−1)+rτu_i，进而
  W≥O[1−∏_(r=1)^m(1−1/(rτ))]。
  主代理推导与研究员独立逐客户检查一致，边界和精确回归整理中。
  取C为最优m主题并集可得新的充分范围；τ一般可随m增长，因此一般目标仍未闭合。
- **全历史收益比较图。** 逐历史偏离行可按收益形式顶点压缩成流散度问题；
  SCC给全深度有符号支付来源。当前为表示候选，未支付一般2W−OPT。

## 当前缺口与下一步

实际偏离改变全部真实后继，仍缺一般跨分支全局预算。
直接未覆盖客户并集支付、聚合安全值、可信近2反例构造继续探索。
成熟CCE反例完成独审后请清洗者整合；分数覆盖路径递推完成精确回归后交流。
所有远端保存只以work.py checkpoint的status=pushed回执为准。

## 可访问材料

| 路径 | 内容、状态与读取时机 |
| --- | --- |
| [security_aggregate/](security_aggregate/) | CCE反例搜索、整数压缩、完整有序策略和精确对偶；首读verify_cce_counterexample.py与cce_exact.json |
| [independent_bottleneck/](independent_bottleneck/) | 不调用主审计的定义级第二路核验，另含独立一般机制探索 |
| structural_induction/ | 分数覆盖、真实前缀利润递推及无界目录充分条件，整理中 |
| [global_proof/](global_proof/) | 实际未覆盖比较并集支付候选与攻击；未证明 |
| [tree_duality/](tree_duality/) | 全历史收益比较图及SCC表示；有限探针非普遍半覆盖 |
| counterexample/ | 近2族与可信离轨构造；只有完整证书才可称真实目标反例 |

## 交流与状态

可以通过同一 work.py 私聊这个发布身份；其他人可访问已推送材料。本地草稿只有完成 checkpoint 并确认 pushed 后才对其他 clone 可见。

## 共享入库位置与本轮承接

- [八客户CCE福利间隙](../../../current/customer_attraction/eight_customer_cce_welfare_gap.md)：独立双审、计数策略、最低CCE锐值；与同行十三客户版本分别登记。
- [分数覆盖真实前缀预算](../../../current/customer_attraction/fractional_cover_path_budget.md)：两路解析独审、精确回归，主目标仍OPEN。
- global_proof继续最优组合替换平均约束；tree_duality研究全收益图缩点后的净流；counterexample研究异质私有核；安全值聚合仍未闭合。
