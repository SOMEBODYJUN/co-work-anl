# menu-parent-batch 六源比较记录

| ID | 文件 | 字节 | SHA-256 | 处置/核心范围 |
|---|---|---:|---|---|
| `f3b5851cc7fb29ce4d0f` | `audit_extra_slot_independent.py` | 3119 | `db1fb3c980ae6985c43177a95bb9d15830b7079b411ff9186eb8a3d5ddeb8d0a` | 独立展开 terminal_pushforward 34 客户证书，Fraction 全历史审计强桥 (D-H=-1,H-G=12,e=1/24)，gap (-1/48)。 |
| `708e078a449b904a88de` | `audit_nonempty_padding.py` | 2586 | `da69294d9c2150ef68cb29e95d833f5b7b13a98dc7c684740180674e289365fc` | 读取同一 34 客户证书，K=67/J=1 私有 padding，Fraction 全历史审计七主题非空、gap (-7/384)、discriminant (K(K-66J))。 |
| `e7f670068a5bcc94f1d6` | `exchange_moments_independent_report.json` | 157 | `37e3a6e92fbeab717c1760d32e7b7042f54d73dc67358d15279ceb8609f77bda` | `PASS`，3,080 exact parameter triples，players 1..20，harmonic/Vandermonde kernels，Fraction only。 |
| `531742debfbd901e38d9` | `exchange_moments_independent_review.md` | 1,838 | `3e76c91a7bf4439205e1bb4e005c4a3af9e93b4abed363ad16f74045a404537c` | 独立重构删除/插入最优和实际槽的 (R_r,H,Hrev,K_m) 恒等式；明确静态最优性、无 SPE/half 结论。 |
| `76b6133ddf55ba4b18f3` | `extra_slot_decorrelation_probe.json` | 17,712 | `9014742460c85e3c2b637fa8ee49d7ff780f95e2757137715c97b0163a3f5814` | `numerical discovery only`，75 次，best ratio=1.0，n=5,k=5，浮点 p/weights/完整 action 字典。 |
| `bf46dd86db65a5613aec` | `extra_slot_decorrelation_probe.py` | 3,194 | `cf7d5d295d6d43738b98e5ebb1c0b56f942e1983c0155ef17cd35239c01e566a` | 与 aggregate probe 同骨架，但加入 diagonal correction `diag` 和 `v`，交替 LP/SLSQP，最多75次随机 discovery。 |

## 去重关系

两份 audit 复核既有 `完整强制终局聚合去相关的非空主题反例` 的同一三人强桥边界，不创建第二反例。34 客户 audit 的 (D-H=-1,H-G=12) 与 (-1/48) 方向对应既有空主题/强制终局证书；非空 padding audit 的 K=67/J=1 与 (-7/384) 对应既有 B9-NONEMPTY-AGG-EXTRASLOT-NO-v1。二者都只否定强 (Sigma G_i^+(p)\le\Sigma D_i(p))，不否定弱 (Sigma G\le W)、自由完整菜单或 Q-CAG-HALF。

exchange review/report 对应既有 `最优覆盖等槽交换的调和矩` 引理：删除最优 r 槽、插入实际 r 槽、Vandermonde/Harmonic 闭式仅用静态 OPT 最优性，不使用 SPE，也不构成 half 或 signed budget。

extra_slot_decorrelation 的 JSON/probe 与此前 aggregate discovery 同属浮点 cone discovery，但目标加入 \(diag\) 和 \(v\) diagonal correction；best ratio=1.0 只反映75次有限探索，不能反驳 exact 强桥反例，也没有完整策略证书。

## 证据边界

两份 audit 依赖同一冻结 `terminal_pushforward_34_D_lt_C_exact.json`，本批未重新执行；现有 exact run/正文承载对应实例，receipt 仅声明源码完整读取与比较。exchange report 是一行 PASS 统计，review 给出解析证明；后者未新增外审。decorrelation JSON/probe 使用浮点 LP/SLSQP、随机有限 trials 和外部 `background_pair_probe.py` 依赖，没有 Fraction/full-SPE exact recheck。六源均不迁移到 unrelated-machines。
