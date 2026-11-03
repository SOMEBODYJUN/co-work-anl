# 全树对偶与旧人银行势：本轮草稿

2026-10-25。作者为父方分配的 tree_dual 子研究员。本目录仅为个人草稿，不修改共享 canonical，不执行 git 或网络操作。

- [旧人银行势及单步失败](credible_bank_potential_attempt.md)：定义真正全历史 SPE 的旧人收入下包络，给出其能望远镜推出任意路径 exact-M 累计候选的精确单步义务；末一步可证明，但旧四人根税反例已经严格否定一般单步义务。附一个自然覆盖修正的解析反例。
- [单步失败原始 JSON](credible_bank_edge_counterexample.json)：原合法输入、各相关状态的完整 SPE 终局全集、最小旧人收入终局、最优补全及来源 SHA256。有限核验只审计所列反例；正文同时给解析计算。
- [复现脚本](reproduce_credible_bank_edge.py)：直接读旧输入并调用规范 ExactSPESolver，重建 JSON，断言两条 `19>18`；默认 stdout，不改写冻结文件。加 `--check-reference` 可核对保存的全部字段和来源 SHA。

Q-CAG-HALF、全 2 统一缺陷价格和 exact-M 任意路径 half 均仍 OPEN。本轮没有新增全树通用付款，没有一般证明或主目标反例。以下候选的失败只限定各自明示形式。
