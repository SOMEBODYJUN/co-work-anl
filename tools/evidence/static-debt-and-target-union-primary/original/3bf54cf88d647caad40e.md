# 全历史半覆盖反例扫描与 extra-one 障碍

状态：**观察/候选边界，非主命题反例；未外审。** 这是本轮 Boss22 子分支对 Q-CAG-HALF 的独立攻击。主目标量词保持任意有限共同目录、任意人数、全部有序历史纯 SPE。

## 有限精确扫描

复用仓库的 `tests/audits/customer_attraction_search.py` 作为全历史集合递归（不是固定 Markov 策略）：在 `--skip-tiny --random-per-size 2000 --extended --confirm` 下，扫描 23,875 个整数单位客户实例，包含 `k=3..7`、`m=3..8`、随机关联密度 0.09/0.2/0.5、singleton/pair/(k−1)-mask 和 large-vs-disjoint-small 结构。每阶段最差可实现纯 SPE 终局均用规范 Fraction solver 交叉核验；全部样本都满足 `2W≥OPT_m`。最低记录比率为 `W/OPT=5/9`（经典大主题+互斥小主题族，仍有 `2W≥OPT`）。

这只是有限观察，不是一般证明；没有把无反例提升为真值。扫描脚本另有 `search_f_static_security.py`：用 `scipy.optimize.linprog` 计算 `v_{m+1}(0)` 的静态不观察查询安全值，并从 exact SPE 根子集取最小首位收益。对 2,000 个 `k∈{3,4}, m∈{3,4}` 随机实例未发现 `u_1<v_{m+1}(0)`。该脚本为探索性浮点筛选，不能作为精确证书。

## 已知的精确障碍（边界，不是半覆盖反例）

1. **真实菜单不够支付静态安全值。** `research/current/customer_attraction/continuation_security_barriers.md` 的 36 客户、三人完整 SPE 给 `u_1=10`，根真实后继菜单的混合零和值 `z_1=11`，而 unrestricted static safety value `v_3=10`。任意 n≥3 的 Möbius 编译族给 `z_1=u_1+1/2`。因此把对偶限制在真实根后继菜单上是严格错误的；安全值对偶需要菜单外竞争组合，必须另证跨分支支付。

2. **extra-one 首位候选仍未被反驳。** 若最小剩余人数 `r` 反例满足 `u<v_{r+1}(b)`, 则对每个强制根行动 `A`，沿同一完整 SPE 的真实分支 `z^A` 有 `d_A≤u`; 最小性把每个后继收益推到 `≥v_{r+1}(b)`, 并给每个后继主题 `B` 根外折扣
   `outside_A(B)≥v_{r+1}(b)-d_A`.
   这是跨分支共同信用的准确义务；至多两主题时这些式子直接矛盾，但三主题以上尚未闭合。

3. **有限背景嵌入不是 max/min 可交换。** `research/workspaces/customer-attraction/R-4ffa8b85fa8847e09e45dcafc8e1326f/audit/minimum_spe_value_embedding_counterexample.md` 的两不交主题五客户实例（两人）精确给 `M_2(0)=3` 但固定前缀 A 后 `M_1(1_A)=2`。这只否定把“首位最差 SPE 值”按固定背景直接嵌入的加强，不能否定静态 `v_r` 或原目标。

下一步若继续，必须处理 `outside` 信用如何在不同根分支合并而不重复收费，或构造完整三主题以上 F_r 反例；重复真实菜单阴性或固定安全值重命名没有信息价值。
