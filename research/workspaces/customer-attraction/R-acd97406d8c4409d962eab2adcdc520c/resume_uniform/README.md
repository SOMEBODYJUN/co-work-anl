# 真实在轨偏离的均匀组合接口：续研探针

目标仍是原全历史纯 SPE 的 Q-CAG-HALF，一般情形 **OPEN**。
这里攻击现行 `research/current/customer_attraction/global_new_uniform_portfolio_two.md`
式 (6)：固定任意 m 个比较主题 T_j，是否总有

`m |∪T_j| ≤ (m−1)W + Σ_i Σ_j V_ij`，

其中 V_ij 是玩家 i 在原实际前缀选择 T_j 后，执行原完整策略得到的真实收益。
该接口仍未证明；若成立，它给更强的 `(2−1/m)W≥OPT_m`。
有限未分离不是本接口成立的证据升级，也不改变一般半覆盖的状态。

## 可复现材料

- `probe.py`：读取现有单位客户输入及完整策略，先用规范逐历史核验器确认 SPE，
  再重放每个实际前缀的每个真实偏离。比较元组可按非空支持 J 枚举：在 J 中每题
  出现一次，其余位置用 J 内 Σ_i V_i,a 最小的主题补齐。这精确最小化给定支持的
  接口余量，故不漏掉重复比较主题；代码用 Fraction 计算。
- `existing_results.json`：现有十七个可读取例子的精确计算。没有负余量。
  来源是明确列出的完整策略或规范全集 solver 构造的一棵策略，不是全实例搜索。
- `cone_probe.py`：复用 `tests/audits/customer_attraction_strategy_lp.py` 的
  完整策略锥，在全部非空客户类型上最小化接口余量，保持全部真实有序历史约束。
  浮点 LP 仅用于发现；若有严格负候选，必须重建有理点并逐历史核验。
- `cone_results.json`：旧冻结样本的七十个四人五主题完整锥，每锥七十个比较
  多重集。浮点最优均未产生负候选；没有恢复全部精确对偶，故不称这些锥的定理。
- `m5p7_cone_result.json`：本轮研究员产生的一棵五人七主题完整锥，全部四百六十二
  个比较多重集未分离；同样只是有限发现过程。

从仓库根执行：

```sh
PYTHONPATH=. python research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/resume_uniform/probe.py
PYTHONPATH=. python research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/resume_uniform/cone_probe.py
```

支持枚举另用六个边界实例核对了十二个完整 SPE 终局，和全部有序比较元组枚举
得到完全相同的 Fraction 余量。实例包含零客户、单人、空主题、重复覆盖和不交主题。
这只验证探针实现；没有把有限核对当作一般数学证明。

下一步要解决的是跨分支支付本身，而不是继续把未分离计数当作进展。
若新策略锥产生负点，先判定它是否只是该更强接口反例，再单独核验半覆盖目标。
