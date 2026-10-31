# R29 fixed-tail bridge and direct-floor probe evidence

本证据包保存本批四个冻结源的原件、实际运行输出和独立字段检查。四源来自同一 R29 `general_proof/potential_attack` 路径，在两个冻结提交中内容相同；本批仍按四个源版本分别登记。

## 源与完整哈希

| clean id | source path | bytes | SHA-256 | 作用 |
|---|---|---:|---|---|
| `236119a64f2b157f723b` | `.../audit_tail_pne_bridge.json` | 2051 | `4a208a4cd9aa0856e4c894cab1050aeecd077497b8215d77c56c2907b6da1631` | 54 单位客户固定旧主题的冻结输出 |
| `de55dd3e248ed5f3d5cb` | `.../audit_tail_pne_bridge.py` | 3027 | `b1b104006d53ab0a73b05ed52144f52703a663b30fd4b7a5b54118c8a9725f92` | 独立 `Fraction` 尾局审计程序 |
| `4f9af5314afa8ff2e005` | `.../probe_direct_floor.py` | 2809 | `d1cce9460be05890190b5d63c99fa7cda3e61f31512b3bb0886bf280ccf78879` | 两个固定策略锥的浮点直接门槛探针 |
| `f452da595a7ff80736af` | `.../probe_observer_pne.py` | 1437 | `63ff62374859673d131ebf488d6d6202959283b9c7d90de468008217d84a1f1f` | 随机固定目录搜索静态尾 PNE 桥反例 |

源 JSON 与 `audit_tail_pne_bridge.py` 重放输出逐字节相同。重放不调用父方代码、canonical solver 或存储证书；`probe_direct_floor.py` 只依赖 numpy/scipy 的 LP 求解器，`probe_observer_pne.py` 只依赖 Python 标准库。

## 重放

```text
audit_tail_pne_bridge.py: exit 0, stderr empty, output byte-identical
probe_direct_floor.py: exit 0, stderr empty
probe_observer_pne.py: exit 0, stderr empty
verify_r29_general_tail_floor.py: PASS
```

`probe_direct_floor.py` 的两行原始输出是：

```text
{'m': 4, 'path': (0, 0, 0, 5), 'comparison': (0, 1, 2, 3), 'max_comparison_over_root': 7.0, 'direct_threshold': 8}
{'m': 3, 'path': (0, 3, 4), 'comparison': (1, 2, 5), 'max_comparison_over_root': 4.205623901581722, 'direct_threshold': 6}
```

它们都低于各自的 `2m` 门槛，因此是有限阴性探针，不是直接门槛反例。

`probe_observer_pne.py` 在固定 seed 492 的第 125 次随机样本找到与尾桥审计相同的 14 类重数。它报告 `k=6`、根主题 `1`、候选尾 `(0,1)`、候选根收益 `44/3`、所有静态尾 PNE 的最小旧玩家收益 `21`，尾 PNE 恰为 `(2,5)` 与 `(5,2)`，第一尾续局门槛为 `53/3`。

## 范围

54 客户结果只证明固定旧主题和两名顺序尾玩家的局部尾子局；它没有构造完整根策略，也没有检查固定旧主题在根节点的 IC。两份直接地板输出只覆盖各自硬编码的完整策略映射与有限比较支持。所有结果都不能升级为一般 SPE、整数客户恢复或六人 half 结论。
