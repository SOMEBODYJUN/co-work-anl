# 顺序客户吸引博弈：共同目录的半覆盖猜想

**活跃目标：** [Q-CAG-HALF](../../questions/customer_attraction_half_coverage.md)：
任意人数、任意有限共同主题目录，全部有序历史依赖的纯 SPE 都覆盖最优的一半。
这个目标尚未证明，也没有在本轮获得目标反例。

本分支使用 [CAG-MODEL](model.md)：客户价值固定均分，没有客户侧优化。
它与仓库原来的主动原子客户设施模型独立。不能借用原模型的因子 2 存在性，
也不能把静态 CAG 的 Nash 结论自动用于顺序 SPE。

## 定义和依赖地图

`CAG-MODEL` → `CA-EXACT-PURE-SPE-ALL` → 有限实例的全部终局及完整有序历史证书。
最后这一步是算法正确性，不是 `Q-CAG-HALF` 的普遍福利证明。

`CA-SPE-NON-PNE` 排除静态 Nash 的直接导入。
`CA-HISTORY-TIES` 排除未经证明的匿名平局与收益次序简化。
`CA-RESIDUAL-NO` 排除逐人遗漏收益保证及其平均化替代。
这些失败证书限制相应证明路线，不反驳主目标。

## 文件地图

| 路径 | 数学资产与何时使用 |
| --- | --- |
| `research/current/customer_attraction/model.md` | 定义单位客户均分、完整历史 SPE 和最优覆盖；任何证明或实验先核对量词。 |
| `research/questions/customer_attraction_half_coverage.md` | 主目标、已知文献边界、当前收费义务；继续研究时先读。 |
| `research/current/customer_attraction/exact_solver.md` | 集合值逆向归纳的必要性、充分性及全历史证书重构；修改枚举器时必须重读。 |
| `research/current/customer_attraction/literature.md` | 一手文献模型条件及不可直接导入的桥梁；静态/顺序、共同/异目录不能混淆。 |
| `research/current/customer_attraction/continuation_lemmas.md` | 已确认小反例、收益保证和失败机制；攻 residual 或匿名平局路线前必读。 |
| `customer_attraction/` | 本模型唯一规范有限精确实现；返回全部纯 SPE 终局，不声称多项式时间或普遍福利。 |
| `tests/test_customer_attraction.py` | 独立完整有序策略枚举 oracle、定义级证书检查和边界回归。 |
| `tests/audits/customer_attraction_search.py` | LCM 缩放整数的独立有限攻击，固定种子及重数参数；新的搜索不能冒充证明。 |
| `evidence/runs/2026-10-09/customer_attraction_search.json` | 冻结的有限搜索范围和摘要；零反例只对所列输入成立。 |
| `history/source/notes/customer_attraction/origin_2026-10-09.md` | 原始目标、核对位置和恢复基线；不保存聊天或认证信息。 |

## 复现入口

从仓库根运行：

```sh
python3 -m unittest tests.test_customer_attraction -v
python3 tests/audits/customer_attraction_continuations.py
python3 -m customer_attraction examples/customer_attraction/residual_counterexample.json --verify evidence/certificates/customer_attraction/residual_counterexample.json
```

完整策略随历史树增长，有限求解器不是计算复杂度突破。直接有理数反例证明
和算法正确性的完整归纳已经写出；主目标的全部人数论证仍缺，外部同行评审未记录。
