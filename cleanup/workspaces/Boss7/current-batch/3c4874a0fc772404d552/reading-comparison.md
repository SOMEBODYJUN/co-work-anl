# Boss7 当前批次：3c4874a0fc772404d552 阅读与比较记录

## 实际读取

1. 通过 `python3 work.py clean show 3c4874a0fc772404d552 --out source.json` 导出冻结实际源；逐字段读取 1880 字节 JSON，核对 `p,m,mult,weights,path,utilities,welfare,optimum,portfolio,strategy`。
2. 阅读 `archives/customer-attraction/tools/evidence/R-373d-coupling-credible-20261031/source/fixed_bridge_attack.py`，确认 JSON 是固定策略锥扫描的输出；读懂 `coverage_row`、`payoff_row`、`StrategyCone`、LP 归一化和 `integer_clones` 过程。
3. 阅读冻结依赖 `customer_attraction/model.py`、`certificate.py` 与 `tests_audits/customer_attraction_strategy_lp.py`，确认 `topics=6, players=3`、单位客户在最终被覆盖主题间均分、完整有序历史纯 SPE 验证及整数克隆实例构造。
4. 阅读 `individual_security_failure.json`、`run-manifest.json`、`validation.json` 和 `replay/fixed_bridge_replay.stdout`；后者给出同一 mult=3 数值，并记录两次 fixed-bridge 重放范围。
5. 另用 `clean show` 读取 sibling `7cdb308f85a723cb0b0d` 的 `mult=2` JSON，确认两文件是同一脚本不同乘子输出，字段与目标不同。
6. 阅读既有正式对象 `archives/customer-attraction/state/障碍/R-373d耦合桥与计数MILP有限证书--障碍.md` 及其 R-373d 证据目录，核对本源此前已有数值摘要及其“固定策略/固定路径有限桥筛、不是 half 反例”的范围声明。

## 独有内容与纠正

本源独有的是完整的 mult=3 JSON 版本（63 项客户重数、15 个非零类、策略树 43 个动作、portfolio、路径、收益和最优覆盖值的同一快照）及其 SHA-256。既有对象已有摘要数值，但没有逐源登记本 ID 的源 hash 和源字段核验，因此本次补充版本级证据。

实现语义需要纠正既有摘要中可能出现的“六提供者/三主题”说法：冻结代码的第一个参数是主题数，第二个参数是顺序玩家数；本源是六主题、三玩家。该修正不改变既有数值或固定桥障碍的真值，但阻止把它误接到六提供者主模型。

## 结论层级

- **精确有限证书：** 用冻结依赖重建整数克隆实例，`verify_certificate` 检查 43 个决策历史及所有偏离，收益 $(69/2,73/2,32)$、$W=103$、$OPT=145$ 逐项一致。
- **固定锥桥障碍：** 在指定策略锥、乘子 `mult=3` 和组合 `(1,2,5)` 的归一化 LP 截面上，最大目标为 `-123/206`；这是模板失败的有限证据。
- **不能升级：** 由于只固定一个完整策略树和有限参数，不量化任意 SPE/任意客户分布；且 $2W-OPT=61>0$，不构成六人 half 反例，不否定主目标。

处置建议：`integrated` 到已有 R-373d 障碍对象；JSON 与验证脚本/报告作为独立 evidence 入口保留。不要标 `duplicate`，因为虽然数值摘要已在既有对象中出现，源版本本身的完整重数向量与策略快照是此前对象未登记的独有可复核内容。
