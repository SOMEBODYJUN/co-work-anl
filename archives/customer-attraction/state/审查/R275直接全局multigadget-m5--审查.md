---
id: "customer-attraction/R275-direct-global-multigadget-m5"
kind: "review"
type_tag: "审查"
title: "R275 直接全局 multigadget-m5 完整策略证书"
status: "finite-full-history-spe-reverified"
truth_status: "exact-finite-certificate; no-universal-half-theorem"
summary: "冻结 multigadget_m5.json 给出一个 14 主题、5 玩家实例及完整有序历史策略；独立定义级核验检查 41371 个决策历史和 537823 个偏离，证书有效且无激励违反。实际福利 21，实例最优福利 22。"
source_refs:
  - "clean:69ab06bd6874fafc0051:research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/direct_global/multigadget_m5.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/direct_global/multigadget_m5.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-27557809587746a46867c9eb07/direct_global/multigadget_m5.json"
  - "local:archives/customer-attraction/tools/evidence/R275-direct-m5-agent/verification.json"
  - "local:archives/customer-attraction/tools/evidence/R275-direct-m5-agent/verify_certificate.py"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R275-direct-m5-agent/multigadget_m5.json"
  - "archives/customer-attraction/tools/evidence/R275-direct-m5-agent/verification.json"
  - "archives/customer-attraction/tools/evidence/R275-direct-m5-agent/verify_certificate.py"
---

# 来源身份和模型

冻结源 `69ab06bd6874fafc0051` 是 `direct_global/multigadget_m5.json`，源记录大小 1,701,078 字节，SHA-256 为 `82a019ae9164dd2c24416d35408341f1bcad6cd41e93e4c3157f77091de331d6`。JSON 只有 `instance` 与 `certificate` 两个顶层对象：它不是搜索日志，而是一个实例和完整策略证书的封装。

实例有 14 个主题、12 类客户、总客户重数 26、5 名单位权提供者。客户类型包括八个二主题类型、两个单主题类型，以及两个包含 9 个主题的较大类型；所有重数均为正整数。终局客户在被选主题之间均分，福利是被覆盖客户重数之和。

# 完整证书和独立核验

`terminal_counts=(1,1,1,1,0,0,0,0,0,0,0,0,1,0)`，总数为 5。`actions` 有 41,371 条记录，恰好等于 14^0+14^1+14^2+14^3+14^4，即每个长度小于 5 的有序历史都有动作，包含离轨历史。

我用仓库已有的 `Instance`/`StrategyCertificate` 定义级核验器，将源 JSON 转成有限客户模型并逐分支计算。核验结果：

- `valid=true`，无错误、无偏离违反；
- 检查 41,371 个决策历史；
- 检查 537,823 个替代动作；
- 证书声明的终局计数与策略根路径一致。

因此该文件支持一个有限输入上的完整纯 SPE 证书。这里的“完整”是对这个 14 主题、5 人实例的全有序历史树，不是对所有实例的算法或定理声明。

# 实际路径和福利

从根开始的实际路径为 `(0,1,2,3,12)`，五位提供者收益为 `(4,4,4,4,5)`，总终局福利为 `W=21`。同一实例的穷举覆盖最优值为 `OPT=22`，故 `OPT/W=22/21`；它接近效率一，但不是半覆盖反例，也没有显示通用下界达到或超过某个新常数。

`verification.json` 保存了终局计数、路径、福利、最优值、历史与偏离计数。该有限证书可作为 direct_global 多 gadget 路线的可复核正实例，并可与其他 m 值候选比较；本源没有给出 m=3、m=4 或任意 m 的递推关系。

# 边界与接续

这份证书保留了完整量词（固定实例、所有有序历史、所有单步替代），所以可用于检查客户均分、平局和离轨动作的实现。它不证明六人 Q-CAG-HALF-6 的半覆盖命题，也不把 `W=21` 或 `OPT=22` 外推为任意 multigadget 家族结论。若继续研究，应把 m=3/m=4/m=5 的实例参数和核验输出放在同一显式模型下比较，先确认是否存在可证明的递推，再讨论半覆盖桥。
