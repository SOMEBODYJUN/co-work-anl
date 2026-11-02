# 聚合安全值 / 静态 CCE 研究 checkpoint

主目标 Q-CAG-HALF 与聚合安全桥仍 OPEN。本轮得到一个已精确核验且经另一研究员独立核验的新辅助桥反例：三玩家、四主题、八单位客户的完整 SPE 福利为 6，同实例每个静态 CCE 的期望福利至少 544/87，且该下界达到。

首先阅读 `eight_client_cce_bridge_failure.md`；完整有理输出 `eight_client_cce_exact.json`，自含核验器 `verify_eight_client_cce.py`。该页自足证明完整历史 SPE、任意非对称 CCE 的对偶下界和达到的对称分布，也记录真实安全值 44/23，故不误报聚合桥失败。

`search_cce.py` 为发现脚本，固定完整 SPE 锥后交替优化客户质量与静态 CCE 对偶。`cce_best*.json` 是纯数值候选，`cce_integer_candidate.json`、`verify_cce_counterexample.py`、`cce_exact.json` 保存先得到的42客户来源，不应优先于8客户正文。`cce_small_candidate.json` 是整数压缩的发现记录。

下一步：将8客户新反例经主代理按正常流程正式入库；若继续主攻，静态 CCE 福利支付桥已经失败，应转向聚合安全或真实跨分支新对象。没有一般定理或主猜想反例。
