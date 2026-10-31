# R-2e5 full-tree-duality evidence

本证据包保存四份已领取来源的完整原件、当前隔离重放和独立字段检查。两类数学对象分别归入既有“固定终局资料包的共同客户粘合缺口”和“实际遗漏客户删除与可信根门槛的无界敏感性”正文。

## 来源与 SHA-256

| clean id | path | bytes | SHA-256 | 处置 |
|---|---|---:|---|---|
| `6be56f17c0ebb348caed` | `full_tree_duality/audit_omitted_deletion.py` | 4553 | `7a32c282f80320f22d9323276a3b664103ce89e5e2af284891a41e991a71846f` | 独立有理数重放 |
| `3f758046862511d94bfe` | `full_tree_duality/global_customer_gluing_verification.json` | 538 | `f3694c27451d1fe2f796cc438181d5e616f335aa5d73bca86a8cb3cdeab18491` | 冻结输出完整读取，与生成 stdout 逐字节相同 |
| `8943f6a7cc92cabb38c1` | `full_tree_duality/omitted_deletion_independent_audit.json` | 40974 | `26ea8648c6b8ab6c8a41d95b9d257f639a9b541b512cb8ad41e93874421ca4c5` | 冻结输出完整读取，与本次重放除 source 路径外字段一致 |
| `ffb30cb52627f7a937b2` | `full_tree_duality/verify_global_customer_gluing.py` | 4945 | `d7ddc1bcb63060ee588429d103ff512aac72186a0d49cc9c661c8085ef31f717` | 独立标准库 Fraction 重放 |

重放所需 `omitted_deletion/reduced.json` 的 SHA-256 为 `6323f6d761c537aaeee50b17a6ae3ffa8f53d36b2c7879de40856fedd4162fe5`；它是此前已保全的原始输入，随本批 replay 副本保存。

## global gluing 有符号资料回归

`verify_global_customer_gluing.py` 独立构造 (m=2,k=4) 的 (X/Y) signed 客户表：9 个主题、45 个终局计数、81 个 payoff vertices、990 个两终局显式共同非负实现、729 个 sharp dilution 比较、10 个有序历史和90项含自身 SPE 图比较。所有 Fraction 断言通过，hypermetric 值为 `-8`，根计数为 `[1,1,0,0,0,0,0,0,0]`，root signed coverage 为 8。冻结 JSON 与本次 stdout 逐字节相同。

该对象支持的是表示障碍：固定大小终局资料包可各自有共同非负实现，但全目录共同非负客户表示被二阶整数 hypermetric 行分离。signed 表含负单例，不是合法 CAG 客户输入，因此不构成六人 half 反例；正文保留一般 (m,L,k) 的解析证明与这个有限回归的层级。

## omitted deletion 独立审计

`audit_omitted_deletion.py` 从同一 `reduced.json` 运行完整逆向归纳，源 JSON 的 `target=[2,1,0,0,2]`。原客户 36 人时目标可实现、根有两个结果；删除一个 `topics=[3]` 的客户后变成35人，目标不可实现、根只保留 `[2,1,1,0,1]`。重放 exit 0、stderr 为空，独立 verifier 返回 `PASS`。

冻结独立审计与新布局运行的唯一差异是报告中的 `source` 路径；`target`、原/删后根结果、252 状态、严格排除树和所有精确收益字段一致。该审计确认遗漏删除闭包失败，保持“不是 half 覆盖结论”的范围。
