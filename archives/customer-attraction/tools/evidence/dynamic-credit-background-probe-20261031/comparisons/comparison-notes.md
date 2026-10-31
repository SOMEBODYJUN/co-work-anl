# dynamic-credit/background_probe 三源比较记录

本批三个来源均完整实读：

| ID | 文件 | 字节 | SHA-256 | 作用 |
|---|---|---:|---|---|
| `6bacca03ff57d72f3a8d` | `dynamic_credit_background_readme.md` | 1,250 | `acb242fbf35e4bbce6453d98bcf3b259e852e60cb11bbc6774fbca29748dd2a4` | 个人探索入口、来源关系、开放义务和处置边界 |
| `a329e42732730bc0f9d6` | `terminal_profit_remainder.md` | 6,149 | `1e51e92b46123aea00720a6a1c6ed9346079a7d18a21651a9642fc078769ce76` | 一般非负整数背景下的 (L+K+J) 精确分解、条件界和 69 客户标量例 |
| `af18a968e70a74bbba3c` | `terminal_profit_remainder_exact.json` | 639 | `1ebce91bd28bd28e6bfab1f8bb498f1f875e96cd51792c78a24514dc1585c7dc` | 4,394 次局部恒等式检查及 69 客户样例输出；明确非普遍证明、未重审完整 SPE |

## 与现有 dynamic-credit 对象的关系

现有 `dynamic-query-credit-primary` 的 `dynamic_query_credit.md` 给出每个实际节点的静态非负信用 (L_i) 和自适应罚项 (Q_i)，并明确 `Q_i` 的合计阈值仍是 HALF?/SHARP? 未证；全局 direct-cover README 也把弱匹配、弱平均和旧强平均分开。本批 terminal remainder 针对的是**固定背景、任意比较组合、只用实际末位最佳回应**的末位节点，把整体差额精确拆成 `L(T)+K+J(T)`。它不计算跨玩家的 (Q_i)，不把多条互斥真实分支合成一个钱包，也不提供早期支付。

现有 `末位收益与前缀税的根诊断` 在空背景下给 `OPT_m≤m v+τ`；本批把该末位 BR 机制推广到任意固定非负整数背景，并保留 `K`（末位未覆盖的早期客户差额）和 `J`（比较重复/遗漏的边界）两个非负余项。现有 `固定背景两人税界` 对恰两人给更强的独立恒等式，因此本批的 `r=2` min-payoff 特例是已有两人结果的推论，而非新的任意人数递推。

## 与 direct-cover/早期真实支付的关系

`customer-attraction-direct-cover` README 已将弱匹配、弱平均和旧强平均分别列为不同充分接口，并保留 BAAF/actual-prefix relay 对“单一入场者标量比例”的反例。本批 README 明确要求下一步读取真实早期离轨菜单来支付末位过高时留下的信用，不能仅凭终端余项把 `v` 替换成全体 `min_i u_i`。因此本批支持的是终端证书和缺口定位，不能闭合 Q-CAG-HALF。

## 计算与真实性边界

JSON 是来源随附的实际输出记录；本轮只读取并复制它，没有重新运行缺失的 `audit_terminal_profit_remainder.py`，也没有重审 69 客户完整 SPE。`local_identity_exact_checks=4394` 只支持脚本声称覆盖的局部恒等式检查；`full_SPE_reaudit=false` 保留了完整策略合法性并未由该 JSON 重审的边界。该 JSON 不能升级为一般半覆盖、完整 SPE 全类证书、外部新颖性或跨模型结论。
