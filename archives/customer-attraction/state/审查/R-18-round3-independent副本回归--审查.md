# R-18 round3 independent：副本回归审查

处置源 `035cea698bf9b90abbd0`（JSON）和 `b90d3ca90da77066bf31`（独立审计脚本），原文与回放在 `archives/customer-attraction/tools/evidence/R-18-round3-independent-20261031/`。源 SHA-256 为 `74c0d6835c4e19f0397a4612decc00f3e1023cafd624792410d71f66660e7cc4` 与 `47921e48308658669cac4aec67faf824358c503a7bd0c9024a0a039557fd61ae`。

独立脚本不导入作者审计、模型、solver 或 verifier；它显式遍历规范/BI 模式且一旦进入 BI 永不返回。实际运行退出码 0：k=1 有 4 个有序节点、12 个动作比较、路径 `(1,0)`、总遗憾 `1/2`；k=2 有 259 个节点、1554 个比较、路径 `(1,4,0,3)`、总遗憾 `1`，每位实际收益均为 2。JSON 与 stdout 逐字段一致。

这批独立实现加强了“静态总正遗憾副本族”的有限核验，但范围仍是 k=1,2 的完整有序树；任意 k 的归纳来自正文，且该族 W=OPT 全覆盖，不是 Q-CAG-HALF 反例。处置为 integrated（脚本）与 retained（输出），供第三阶段作为独立交叉核验。
