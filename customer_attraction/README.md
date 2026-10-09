# 顺序客户吸引博弈的有限精确求解

本包使用一个新的模型合同：所有单位玩家依次观察完整历史后，从共同有限主题目录中选一个主题；每名单位客户将其一个单位平均分给选到其任一可接受主题的全部玩家。整数客户重数只是同类单位客户的压缩编码。这里没有客户侧 NE，也没有原子负载成本。

`ExactSPESolver.outcomes()` 返回**任意历史依赖纯策略 SPE**能够产生的全部终局主题计数，保留全部无差异选择。它没有固定单一 backward-induction selector，也没有强迫相同计数历史使用同一续局。混合行为策略 SPE 不在本接口内。

```python
from customer_attraction import Instance, ExactSPESolver, verify_certificate

instance = Instance.from_topic_sets([{0}, {0, 1}, {1, 2}], players=3,
                                    labels=("A", "B", "C"))
solver = ExactSPESolver(instance)
all_terminal_counts = solver.outcomes()
certificate = solver.certificate(on_path=(2, 0, 2))
report = verify_certificate(instance, certificate)
report.assert_valid()
```

客户类型接口为 `CustomerType(frozenset({0, 1}), multiplicity=5)`，主题使用从零开始的目录索引；`Instance(topics, customers, players)` 将这些类型组合成实例。客户不喜欢任何主题、主题覆盖为空、不同主题覆盖相同均合法；正玩家数需要非空目录。另支持零玩家边界。

| 接口 | 精确语义 |
| --- | --- |
| `outcomes(prefix_counts=None)` | 给定前缀计数后的全部纯 SPE 可达终局计数 |
| `ordered_outcomes(target_counts=None)` | 全部可由纯 SPE 实现的有序在轨路径迭代器 |
| `certificate(target_counts=None, on_path=None)` | 一个覆盖每个有序决策历史的纯 SPE 策略；可指定终局或完整路径 |
| `certificate(..., action_selector=..., continuation_selector=...)` | 在传入的合法候选中按完整历史自行破除无差异 |
| `verify_certificate(instance, certificate)` | 独立按完整策略树核验所有子博弈的一步偏离，不调用集合递推 |
| `minimum_welfare()`, `worst_outcomes()`, `worst_certificate()` | 本实例最差纯 SPE 的覆盖福利及达到证书 |
| `Instance.optimal_welfare()` | 不加均衡约束的精确最大覆盖福利，有限子集枚举 |
| `inefficiency_ratio()` | `OPT / minimum SPE welfare`；零覆盖实例约定为 1 |

终局收益使用 `Fraction`，福利为单位客户的被覆盖数量。证书 `actions` 以完整历史 tuple 为键；`to_dict()` / `from_dict()` 提供无损 JSON 结构。计数缓存只缓存可实现集合，证书可以让 `(0, 1)` 和 `(1, 0)` 采用不同续局。

实例 JSON 结构为：

```json
{
  "topics": ["A", "B"],
  "customers": [
    {"topics": [0, 1], "multiplicity": 3},
    {"topics": [1], "multiplicity": 1}
  ],
  "players": 2
}
```

```sh
python3 -m customer_attraction instance.json --certificate --output result.json
python3 -m customer_attraction instance.json --verify result.json
python3 -m unittest tests.test_customer_attraction -v
```

输出文件已存在时 CLI 拒绝覆盖。完整证书随有序历史树指数增长；求解是有限精确枚举，没有联合输入位长多项式时间保证。`big_theme_lower_bound(m)` 提供一个大主题和 `m-1` 个独立单例主题的现有下界家族输入；测试检查 `m=1,...,6` 的 all-big SPE 达到与精确最优覆盖。

全集递推和策略证书的完整证明见 [精确算法账户](../research/current/customer_attraction/exact_solver.md)。独立小规模 oracle 直接枚举全部完整有序历史策略，并按逐名单位客户计算实际偏离；有限成功不证明新模型的任何全称福利猜想。
