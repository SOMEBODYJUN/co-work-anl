# R-3b6b `search_maxsize.py` 读源边界（08145efe1e5aefe4cf92）

## 对象与代码路径

冻结源 `research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/global_proof/search_maxsize.py` 是一个有限随机/组合探针，依赖同目录 `fractional_explore.benchmark` 与 `customer_attraction.model.{Instance,CustomerType}`。代码没有通用证明器，也没有 exact SPE solver。

每个 `n` 取 3、4、5；每个 n 做 1000 个 trial；固定 `random.Random(883)`。每个 trial 固定 6 个主题 `k=6`，遍历非空掩码 `mask=1..63`，以概率 .35 保留该客户类型，重数独立均匀取 1..9，构造 `CustomerType(frozenset(topics), multiplicity)`，玩家数为 n。客户可重叠，空客户类型不生成；这是有限随机族而非全体有限实例。

## 搜索的对象、输入输出

`benchmark(ins,(0,)*k)` 给根部基准 `M`。在 `fractional_explore.py` 中，令 `r=n-sum(b)`，`C` 为客户类型×主题的 0/1 关联矩阵，`w` 为客户重数，`z=C b`；当 `r=1` 返回 `max(C.T @ (w/(1+z)))`，当 `r>1` 用 SciPy SLSQP 在主题单纯形上最小化
`-sum(w*log(1+z+(r-1)*(C@q)))`，再返回 `g@q`。因此 `M` 是浮点 fractional-log benchmark 的根值（SLSQP 近似），不是 SPE 阈值或 exact optimum；代码没有检查 `opt.success`/KKT 残差后再接受 `M`。

随后按客户重数计算每个主题的“size”
`size[a] = sum(multiplicity for customer_type if a in customer_type.topics)`，取 `a=max(range(k), key=size)`；并枚举前 n−1 个动作的无序多重组合 `bs in combinations_with_replacement(range(k), n-1)`，把候选终局计数设为 `q=ins.counts(bs+(a,))`。以精确 `Fraction` 的 `ins.topic_payoffs(q)` 计算各主题真实终局付款；若最大-size 主题 `a` 的付款 `< M−1e−6`，同时每个 `b in bs` 的付款 `>= M+1e−6`，便写出 JSON 并立即退出。

唯一可能输出是同目录覆盖写 `maxsize_obstruction.json`，字段为 `instance`（`to_dict()` 的主题/客户重数/人数）、浮点 `M`、`largest` 主题索引、`witness` 前 n−1 动作元组、以及字符串化的 `player_payoffs`；stdout 打印 n/trial/M/q/payoffs。源树没有随该脚本保存 `maxsize_obstruction.json` 或 stdout/stderr/运行清单，故不能声称找到见证；没有输出意味着至多在保存的有限运行（若存在）中未触发条件，不能解释为全称否定。

## 精确性与有限性

终局分摊 `topic_payoffs` 本身按 `Fraction` 精确计算，且 `player_payoffs` 保存精确有理数的字符串；但比较阈值 `M` 来自一次浮点 SLSQP，容差为 `1e−6`。随机实例族、1000×3 个 trial、6 主题、组合式前缀枚举和首个命中即停都给出明确有限范围；未枚举客户类型的全部 2^63−1 重数配置、任意主题数/人数、动作有序历史、任意最大-size 并列选取、或完整纯 SPE 续接。因此该程序不能提供精确反例证书或一般定理。

此外，`a=max(..., key=size)` 对并列最大主题只选 Python `max` 的首个索引；它测试“一个被选出的最大 size 主题在某个终局是否低于 M，而其余动作均高于 M”的局部模式。它不证明所有最大主题都安全，也不检查 `bs+(a,)` 是否为任何 SPE 路径，更不验证 deviating players 对所有后续历史的激励约束。

## 与同目录 fractional 源的关系

- `fractional_explore.py` 定义上述 SLSQP `M`；本源是其下游的 max-size 主题筛选，不是独立 fractional 目标。
- `search_fractional.py` 同样以 `benchmark` 作数值基准，但额外调用 `ExactSPESolver`，检查单主题前缀下的最小可接受付款与一个局部递推差额 `D`；它仍是 100×4、7 主题的浮点有限攻击。`search_maxsize.py` 不调用 `ExactSPESolver`，所以比它更弱。
- `search_fractional_floor.py` 比较 exact 根阈值 `ExactSPESolver.threshold` 与 fractional `M`，并探查“每个动作都有坏终局”的局部条件；同样是随机有限探针。max-size 源只复用 `M` 和 exact 终局付款，不能继承 floor 源的 exact-SPE 量词。

相关工作稿/审查页把这些 fractional-floor、安全动作和最大主题搜索都定位为有限诊断；Q-CAG-HALF（一般共同目录、任意人数、完整有序历史纯 SPE 的 2W≥OPT）仍开放。最大主题/唯一最大主题的其他有理审计属于固定参数、单位客户或特定菜单族，不能把本随机 max-size 扫描升级为一般最大主题付款引理。

## 处置建议

保留源代码作为“有限、数值、局部筛选”证据；把状态标为 `finite_numeric_probe_only`，不要入主定理、反例或 exact certificate。若需继续使用，应保存实际 stdout/stderr、随机种子、Python/SciPy 版本、每个 trial 的计数和 `benchmark` 优化诊断，并把候选 `M` 以有理上下界复核，再对候选终局扩展完整 `ExactSPESolver` 的所有纯 SPE 续接/历史激励。没有这些补件，建议在 Boss1 总结中作为与 `search_fractional*` 并列的阴性/未触发扫描，归档而不作为证明。
