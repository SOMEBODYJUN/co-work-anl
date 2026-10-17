# 双 small 行三半合同：修文后最终字节核对

本次是读后最终修文核对，不是盲审。旧最终组合回执 SHA `553f5b4465cda9e582993fffc5098e577901d6d05222442f8c8efcdabe82ffc0` 保持原字节。

实际读取修文后的正文和审查页，SHA256 与 root 提供值均一致：

- `research/current/unrelated_machines/joint_slot_prefix_rounding.md`：`ab1a6cd8c7c3b5cceabc7a4a103d77180ee0465f722dddbeb277400cc2533be4`。
- `research/reviews/unrelated_machines/joint_slot_prefix_review.md`：`988d78681ac0b88761800d44624c6f91d5ebdd988ea841aaa4e3664f8e669e1e`。

三类非 fatal 修文均已实际核清：冻结 Exact-only 来源与本节完整证明的层次分开；§7.5 内部链接为7.1、7.2–7.4（含后段“结合7.1”）；Karp 读取来源明确为原文重印 PDF。

不仅按字面观察，还对新全文执行只读反向替换：仅还原这些导航／来源词句便精确恢复上一实读正文 SHA `3d0c4d42a6ee171ba7717dc94fb314c1daa03f56420a2acbc5bacd72dbde2981` 和上一实读审查页 SHA `e00b3a02681083b7bc7ca0e6350ff956f8f5648200ce10edb81d87e21a5a46a0`。因此修文没有带入其它未审数学变化。

正文 §7 前旧 v1 前缀、恢复旧单一末尾换行后，仍精确得到 `8b1abf7a149759cb2f9c7424c380181442990e0f7ee913273a1c1091526f3e00`；旧 v1 的历史 hash 与对象身份未改。

最终 §7 仍无 fatal objection：完整结构域、全 OPT 实际σ算法、严格阈值保证、同域三半困难性、PSM common-b 的局部分支适配及已发表方法扣除均保持前次已核内容。没有新增 Claim、任意不同 big 时间推广或一般 UM 升级。

root 在本次回告中确认自己也已全文实际读取本 §7；审查页另保留其读审查／读代码／真实运行的来源记录。本审查者本次没有重跑 finite 审计，没有把 root 的运行计为本人运行，也没有追加新实现认证。

结论：上述新 SHA 可作为已核最终字节保存。新颖性、外审、独立论文价值和一般 UM 正反面状态均未改变。
