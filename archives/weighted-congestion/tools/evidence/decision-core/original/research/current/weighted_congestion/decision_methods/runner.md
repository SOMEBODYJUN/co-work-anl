# 有限显式加权拥塞博弈：可核证决策器

`decision_runner.py` 将给定小游戏与稳定预算 `alpha` 转为一个明确的优化问题：在全部 `alpha`-PNE 中分别最小化 `sum_i C_i` 和 `sum_i w_i C_i`。它枚举真实资源子集策略的笛卡尔积，逐偏离重算真实负载；不是紧凑输入上的多项式算法，不证明全类稳定阈值或新颖性。

## 输入与运行

只需 Python 3 标准库。从仓库根目录运行：

```sh
python3 tests/audits/weighted_congestion/decision_methods/decision_runner.py examples/weighted_congestion/decision_methods/quadratic_triad.json --alpha 1 --alpha 286/267 --summary
python3 tests/audits/weighted_congestion/decision_methods/decision_runner.py examples/weighted_congestion/decision_methods/heterogeneous_nonlinear.json --alpha 1 --alpha 9/8 --alpha 16/11 --summary --output ../NEW_certificate.json
python3 tests/audits/weighted_congestion/decision_methods/decision_runner_audit.py --output ../NEW_audit.json
```

`--output` 独占创建，拒绝覆盖已有文件。默认 JSON 写 stdout；`--summary` 另在 stderr 给人读结论。状态及策略索引从 0 起，玩家顺序等于输入顺序。最小输入：

```json
{
  "id": "example",
  "resources": {"r": ["0", "1", "2"]},
  "players": [
    {"id": "p", "weight": "3/2", "strategies": [["r"], []]}
  ]
}
```

资源系数依次是常数、一次、二次项。只接受整数或有理数字符串，拒绝 JSON 浮点数、非正权、负系数、未知资源、同策略中的重复资源和重复策略。资源集、玩家集、每人策略族非空；其中一个策略可以是空集，费用可以恒零。所有判断采用 `fractions.Fraction`。

可导入 `Game(raw)` 与 `solve(raw, alphas=[...])`。`game.states()` 枚举动作索引元组；`game.costs(state)` 返回 `(loads, costs)`，成本固定为 **不乘权**的 `C_i=sum_e c_e(x_e)`。`game.players` 含 `Player(id, weight, strategies)`，`game.resources` 为名字到有理系数元组的字典。

## 精确合同与证书

每个状态的最小有限稳定因子为

\[
\alpha(s)=\max\{1,\max_{i,t_i} C_i(s)/C_i(t_i,s_{-i})\}.
\]

`0/0` 对应已满足的比较，贡献 1；当前成本正而偏离成本为 0 时，该状态的因子记为字符串 `"infinity"`，所有有限预算都不稳定。自偏离恒满足，输出保留全部非自偏离。端点采用 `<=`。状态表同时保留全部负载、每人成本、最小因子及每条偏离的当前/偏离成本，所以可以独立重算。

对于每个查询，稳定集合为空时，程序输出**覆盖每个状态**的一条严格违约偏离与正差额；这是给定有限输入在该预算下的完整无解证书。有解时输出稳定集合与两种目标各自的最优状态。全枚举提供最优性：逐态先核验稳定条件，再比较目标。两种目标可能选择不同决策，禁止互换。

前沿对每种目标分别给出最优成本发生严格下降的 `alpha_from_inclusive` 节点；两个节点之间沿用左节点成本。第一个节点以下无稳定状态。它们是给定游戏的完整稳定—效率阶梯，不是全类参数界。

基线包括：

- **固定顺序 best response**：从全 0 动作开始（可用 `--initial` 改），按玩家输入顺序轮流，选择最早的最小成本动作，只在严格改善时移动。环检测用 `(状态, 下一玩家)`，而非只看重复状态；连续整轮无移动才宣布精确 PNE。轨迹循环本身不证明无 PNE，完整无解证书另外提供。`--max-br-turns` 截断时明确输出 `turn_limit`。
- **已知次数阈值 `max(1,d)`**：比较该预算下全枚举得到的最优稳定决策；外部存在性结论的精确版本、模型与来源见[基线比较](baselines.md)。这不是本程序对外部 `d` 近似势的高效实现，也不声称该阈值对每个具体游戏最优。
- **积分势基线 `d+1`**：枚举最小化 `Phi(s)=sum_e sum_k a_e,k x_e(s)^(k+1)/(k+1)`。移除玩家权重 `w_i` 的势降至少是 `w_i C_removed/(d+1)`，加入的势增至多是 `w_i C_added`；公共资源抵消，故全局最小点是 `(d+1)`-PNE。程序另核验所选点真实因子。
- **两种无稳定约束的社会最优**：作为各自效率比的分母。`0/0` 效率比记 1，正数/0 记 `"infinity"`。

## 实际结果

既有 `WC-R1-INTEGER-TRIAD-v1` 例由仓库 `tests/audits/weighted_congestion/quadratic_triad/verify.py` 的六个真实资源逐字转换，权重为 `(16,2,5)`，次数 2，8 状态、24 非自偏离。此处只复用有限例，不主张新构造。

| 稳定预算起点（包含端点） | 最优 `sum C_i` | 最优 `sum w_i C_i` | 所选动作 |
|---|---:|---:|---|
| `286/267` | `5321` | `44058` | `(0,1,0)` |
| `963/898` | `5216` | `42628` | `(0,1,1)` |
| `1507/1403` | `5156` | `41818` | `(0,0,1)` |

`alpha=1` 及 `21/20` 均无解，各有完整 8 状态出口证书；最小可行预算正好 `286/267`，端点有两个稳定状态。固定顺序 BR 从全 0 出发，8 次轮转后检测到长度 6 的状态—阶段环。次数基线预算 2 已可选社会最优；积分势最小点选择第一行，其成本比为 `5321/5156`、`3147/2987`。

异权非线性 fixture 权重为 `(1,2,3/2)`，同为 8 状态、24 非自偏离，展示两目标的区别：

| 条件/目标 | 动作 | `sum C_i` | `sum w_i C_i` | 所需真实因子 |
|---|---|---:|---:|---|
| 精确 PNE | `(1,1,0)` | `32` | `91/2` | `1` |
| 加权社会最优 | `(0,1,0)` | `32` | `89/2` | `9/8` |
| 不加权社会最优 | `(1,0,0)` | `31` | `99/2` | `16/11` |

其固定顺序 BR 收敛到精确 PNE；它给出可运行基线，而优化器在允许放松稳定预算后选出更符合指定社会目标的决策。另附零成本、含空策略、单玩家三个边界 fixture。

## 规模、审计及局限

状态数 `P=product_i |S_i|`，非自偏离数 `D=P sum_i(|S_i|-1)`。程序在枚举前先检验 `--max-states`（默认 100000）与 `--max-deviations`（默认 2000000）；超限退出码 2、`capacity_error`、`nonexistence_certified=false`，**绝不称无解**。不保证该默认上限内每个高次数/大位长输入都能快速处理；有理算术位长、资源数与输出证书体积仍可能很大。前沿排序 `O(P log P)`，状态—偏离证书体积至少 `O(P+D)`；所有费用计算还依赖显式资源关联及多项式长度。

`decision_runner_audit.py` 的单人成本 oracle 独立按冻结其他玩家重算，不调用 runner 的负载/多项式函数。它逐态逐偏离核对输出，核查每个无解出口、每个预算的最优性、每个因子层级的前沿、两类基线、BR 环的阶段、容量报错及输出拒绝覆盖；再对固定 seed 的 40 个游戏及其 7 倍费用副本作同样核验。实际随机原例覆盖 168 状态、522 偏离，倍乘副本再覆盖同样数量。

[冻结审计](../../../../evidence/runs/weighted_congestion/decision_methods/decision_runner_audit.json) 记录源码/fixture SHA256、Python 版本、seed 与五个完整 fixture 运行证书。这里是作者实现审计，不冒称外部独立审查。有限测试不能代替全实参数或无限游戏族的数学证明，程序也没有紧凑输入可扩展性结论。

正式程序：[decision_runner.py](../../../../tests/audits/weighted_congestion/decision_methods/decision_runner.py)；[独立成本oracle审计](../../../../tests/audits/weighted_congestion/decision_methods/decision_runner_audit.py)；[输入样例目录](../../../../examples/weighted_congestion/decision_methods/)；通用选择问题的精确身份是 `WC-EXPLICIT-STABILITY-COST-FRONTIER-v1`，见[质量正文](decision_quality.md)。
