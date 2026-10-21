# direct_global 工作区

当前目标：一般 Q-CAG-HALF 的全局证明，允许全部历史依赖平局。一般目标仍 OPEN。

- `background_near_saturation_independent_review.md`：独立逐客户审查同伴的 BNS/AP；未发现致命异议，并证明 M 可缩小到比较主题 C 上的背景最大负载。
- `benchmark_deviation_obstruction_independent_review.md`：独立重建全部有序历史比较，确认遗漏单个R查询即会导致无界模板障碍；记录一个可修复self-action文字缺漏。
- `static_matching_counterexample_independent_review.md`、`static_matching_independent_audit.py/.json`：独立展开52个单位客户，完整核验259节点1554偏离、1296有序终局与24最优匹配，确认辅助静态匹配桥失败。
- `markov_probe.py`：有限探索工具，检验三人全历史终局多重集是否均可由按计数选择的 SPE 实现。四主题随机 10000 例未找到分离；该证据不证明一般等价，当前未形成猜想或可用桥。

下一步：继续寻找真正跨分支交换；先检验按计数的终局实现是否可严格证明或被精确反例否定。它与“固定原策略必须同计数同回复”的已失败断言不同，但未证时不能限制主定理量词。
