# MathLab prompts.py 实读比较记录

- Claim：`f413aad10283f4e6337a`
- 原路径：`research/weighted_congestion_frontier/upstream/mathlab/src/mathlab/prompts.py`
- blob：`b99b90dc5b57d652ecc85fe81916907183032102`
- SHA-256：`74cee56c656a37ad1fe273aedf9ad7676ffbff52374a0a1674000f31fbaf771a`
- 大小：6117 B

## 实际代码内容

文件定义 `BASE`、八种 `ROLE` prompt、`blackboard_digest` 和 `build_instructions`。BASE 强制区分 proof/computation/conjecture/heuristic/failure，要求 shell exact computation、保存有用脚本、禁止有限计算升级定理、优先反驳、PROVISIONAL_PROOF 新鲜 verifier、REFUTED 证据、capability request、消息与 promoted blackboard artifacts、以及简洁 log_progress。

角色分别是 cartographer、director、researcher、experimentalist、falsifier、verifier、synthesizer、framework_engineer；每个角色合同规定其主要动作和禁止事项。`blackboard_digest` 对 claims/tasks/features 只取固定前 60/40/20 项及指定字段，输出 JSON；`build_instructions` 把 BASE、角色、agent/island、项目根、handoff 和 digest 拼成 prompt。

## 与当前清洗流程的关系

当前 Boss3 清洗已经有同方向的硬边界：实际 `clean show` 全文读取、正式正文与 evidence、receipt 字段、checkpoint pushed 后 done、有限实验与定理分离、开放缺口保留。MathLab prompt 中的状态词和 API（`publish`/`review_claim`/`request_capability`/`log_progress`）不在本结果分支实现，也不能替代 `work.py`、Git、board 或 clean receipt。

`blackboard_digest` 的前 N 截断尤其不能被解释成“全黑板已审查”：它是 prompt 输入压缩器，旧 claim/task 可能不在摘要中；当前阶段仍以 clean list、clean show 和实际正文为准。该文件与 ARCHITECTURE 属于同一上游 MathLab 选集，但本 claim 实读的是代码实现，ARCHITECTURE claim 只记录系统级数据流，两者一源一对象，不重复抹平。
