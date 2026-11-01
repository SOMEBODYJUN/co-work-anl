# R-373d：耦合桥、签名图恒等式与计数 MILP 有限证书

## 范围与边界

本对象整理 R-373daba10913464c93771a808d88fce3 下八个冻结源：三份 coupling/签名图材料、四份 credible/计数 MILP 材料和固定桥攻击脚本。源、clean-show、依赖副本、重放及验证器位于 `archives/customer-attraction/tools/evidence/R-373d-coupling-credible-20261031/`。它们是有限实验、定义级恒等式、有限桥障碍和固定策略证书；没有一个结果被提升为当前六人六提供者 CAG-HALF 全称结论。

## 签名图审计

`audit_signed_graph_menus.py` 用 Fraction 逐项审计 cut、direct/formula、envelope、deficit 和 odd-cycle 量。固定 seed 重放通过：1,200 个随机定义案例、150 个 half-density sharp 案例、135 个 clique sharp 案例；K5 为 `joint_deficit=2`、最佳 scalar odd-cycle packing (5/3)。源 JSON 与重放逐字段一致。这支持一个局部代数账本，但没有客户类型、终局均分、完整 ordered-history 策略或 SPE 约束，因此不是一般 half 证明。

## 静态桥有限反例

`pair_interest_static_bridge_failure.json` 明确标注 `exact finite bridge counterexample, not half counterexample`：4 个玩家、5 个主题、13 个类型，根 `[2,4,0,3]`，目标计数 `[1,0,1,1,1]`。将 provider 0 移到 1 的静态项由 (10) 变为 (21/2)，并完成 780 条 ordered-history 检查。它只反驳该实例的一条静态桥传递，不能替代覆盖值或半覆盖结论。

## 三个计数 MILP 候选

`count_milp.py` 是浮点 MILP 候选发生器；三个源均为 HiGHS `status=1` time limit，`floating_only=true`，所以 objective 不是全局最优证明。独立 Fraction `StrategyCertificate` verifier 对提取策略树全部通过：

| 源 | 参数/路径 | 精确目标 | (W) | OPT | 历史数 |
|---|---|---:|---:|---:|---:|
| `count_milp_4_0-0-0-1-1.json` | (p=4,m=5), ((0,0,0,1,1)) | (-4/5) | 5 | 6 | 341 |
| `count_milp_4_0-1-1-1-1.json` | (p=4,m=5), ((0,1,1,1,1)) | (-1) | 1 | 1 | 341 |
| `count_milp_5_0-1-1-1_mult3.json` | (p=5,m=4), mult=3, ((0,1,1,1)) | (-1/4) | 4 | 6 | 156 |

这些是固定策略的完整纯 SPE 证书；第一、三行仍满足 (2W>OPT)，第二行为零损失。保留 time-limit 元数据，不能把候选发生器的搜索状态写成最优性证明。

## 固定 bridge attack

`fixed_bridge_attack.py` 在 (p=6,m=3) 的固定 strategy cone 内扫描 mult=2、3。Fraction 恢复并验证的重放为：

* mult=2：路径 ((0,3,4))，portfolio ((1,2,4))，objective (-6/23)，收益 (48,48,42)，(W=138)，OPT=198；
* mult=3：路径 ((0,3,4))，portfolio ((1,2,5))，objective (-123/206)，收益 (69/2,73/2,32)，(W=103)，OPT=145。

这是固定策略/固定路径的有限桥屏幕，不是所有 SPE 的搜索，也不是六人六提供者 half 反例。

## 缺口与接续

签名图账本缺少从 edge state 到客户类型和完整历史的统一构造；静态桥只说明 bridge 变量变化；MILP 策略虽通过定义级 verifier，但 search `status=1`；fixed bridge 依赖 6-provider/3-topic 证书。后续若要推进主问题，必须重新定义终局客户价值均分，覆盖所有 ordered histories、任意平局、空/重复主题和零客户，并把候选、完整证明、条件结论、有限实验、障碍和原模型反例分开标注。
