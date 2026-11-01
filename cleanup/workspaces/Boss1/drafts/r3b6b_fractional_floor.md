---
id: cleanup/Boss1/r3b6b-fractional-floor
kind: source-review
status: finite-probe-retained
truth_status: exact-code-read; no-run-result; no-universal-claim
source_id: f34f2dceb0a09e0b629a
source_blob: b8acf293ae69a5f3e3756b28bf34890b716f9b94
source_sha256: f346d8c5e1cb8a72dd2a77ad4df03869dedc4978e52a495af62c431a219bfa8f
source_path: research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/global_proof/search_fractional_floor.py
source_commits: [68fad804ec5946cb296f77dc5b336308a66abf12, aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c]
---

# R-3b6b fractional floor：完整实读与边界

## 1. 源文件和依赖

冻结源只有 31 行（1546 bytes）。它固定 `random.Random(77128912)`，对 `n in [3,4,5,6]`、每个 `n` 的 `trial in range(200)` 做随机输入；输入恒有 `k=6` 个主题。每个非空 mask `1..63` 以独立概率 `.22` 加入一个 `CustomerType`，其 `multiplicity` 均匀取 `1..9`。因此至多 `4*200=800` 个实例，主题数、人数、客户类型支持和重数都被硬编码。

依赖 `global_proof/fractional_explore.py` 的 `benchmark(ins,b)`。该模块构造客户-主题 0/1 矩阵 `C`、重数向量 `w`、背景负载 `z=C@b` 和余下人数 `r=players-sum(b)`，用 SciPy SLSQP 在单纯形上最小化

\[
 -\sum_i w_i\log(1+z_i+(r-1)(Cq)_i),
 \]

然后返回

\[
 m=g(q)\cdot q,
 \qquad
 g_a(q)=\sum_i\frac{w_iC_{ia}}{1+z_i+(r-1)(Cq)_i}.
\]

`opt.success`、`opt.x` 的可行性和 `max(g)-g@q` 误差虽被计算/返回，但 `search_fractional_floor.py` 完全忽略；`m` 不是一个 exact Fraction，也没有严格的最优性或残差证书。这里 `b=(0,…,0)`，所以 `z=0,r=n`。`r==1` 的 exact-looking 分支不会被本源调用（本源只取 `n>=3`）。

历史 commit 中同时存在顶层 `customer_attraction` 包；当前重建工作树没有该包和该 `research/workspaces/...` 路径，故这次审阅没有把冻结脚本当作当前树可直接执行的测试。仓库内可读的规范依赖副本是 `archives/customer-attraction/tools/evidence/fractional-load-boundaries/original/customer_attraction/{model.py,exact.py}`。

## 2. 可以视为 exact 的身份

规范 `Instance.topic_payoffs(counts)` 对终局计数 `c` 逐客户类型 `S` 计算

\[
 u_a(c)=\sum_{S\ni a,\ c(S)>0}\frac{\mathrm{multiplicity}(S)}{c(S)},
 \quad c(S)=\sum_{b\in S}c_b,
\]

并对未占用主题给 0；运算使用 `fractions.Fraction`。`CustomerType` 只允许整数主题索引和正整数重数，`Instance` 检查主题标签、索引和终局长度。

`ExactSPESolver.threshold((0,…,0))` 是规范有限递推的精确根地板。令 `R(k+e_a)` 为从该子状态可由纯 SPE 实现的全部终局计数集合，则代码实现

\[
 F(0)=\max_a\min_{c\in R(e_a)}u_a(c).
\]

`_solve` 对所有计数状态缓存 `R(k)`，终局直接返回单元素集合；非终局先求所有孩子，再按上述地板保留满足 `u_a(c)\ge F(k)` 的终局。它枚举的是纯 SPE 终局计数集合（不是混合均衡，也不是一个输入位复杂度算法）。因此 `floor` 本身是 exact，但它依赖的 `m` 不是。

## 3. 两个搜索分支的真实量词

### 3.1 `FLOOR COUNTER`

脚本若发现

```python
float(floor) < m - 1e-6
```

就写 `fractional_floor_obstruction.json` 并立即退出。语义是：在一个随机抽到的 `n<=6,k=6` 实例上，精确 SPE 根地板低于一次数值分数 benchmark。它至多是候选反例，不能推出

\[
\forall\text{ 共同目录、人数、客户类型}:
F(0)\ge M_{\rm frac}(0)
\]

失败；因为 `m` 可能因 SLSQP 未收敛、边界 KKT、浮点误差或目标解释而偏移。反过来，未触发也只表示这 800 个固定随机样本在 `1e-6` 容差下未击穿。

要升级为数学反例，至少要保留实例 JSON、以 `Fraction` 重算 `floor`、给 `M_frac` 一个可审计的全局上界/下界（或证明候选 `q` 的 KKT 与精确值），并用完整有序历史的 SPE 证书核验该根地板含义。

### 3.2 `INDUCTION COUNTER`

对每个 `bs in combinations_with_replacement(range(6), n-1)` 和主题 `a`，脚本令 `q=ins.counts(bs+(a,))`，重算终局 `pay=ins.topic_payoffs(q)`，收集满足

\[
 u_a(q)<m-10^{-6},\qquad
 \min_{b\in bs}u_b(q)\ge m+10^{-6}
\]

的一个 `bs`。只有当六个主题都各找到一个 witness 时，才写 `fractional_induction_obstruction.json` 并退出。`witness[a]` 会被后续命中覆盖，文件只保留每个动作最后一个 witness。

这不是 SPE 归纳反例：代码没有要求 `bs` 是某个均衡前缀、`q` 属于 `ExactSPESolver.outcomes()`，也没有要求同一条完整有序策略能同时实现这些终局；它只检查一个静态终局计数向量中的“旧主题 payoff 全部高、新动作 payoff 低”。更没有处理有序历史的续局量词。故即使六个主题全有 witness，也只能否定一个尚未写明的静态 safe-action 充分条件，不能否定 SPE 地板、福利半界或 `Q-CAG-HALF`。

`bs` 为非空（`n>=3`），故 `min(...)` 不会在本源范围内空集报错；重复动作只改变计数，不改变 `topic_payoffs` 的计数语义。

## 4. 全仓相关对象与已知边界

- 同目录 `search_fractional.py` 也调用同一个数值 `benchmark`，但测试的是局部偏离差 `D`；`search_maxsize.py` 测试“最大静态主题”的一个终局 witness。两者同样是有限数值探针，不提供全称证明。
- `R-3b6b.../README.md` 明确写出 Q-CAG-HALF 仍 OPEN，并警告有限搜索不是一般猜想证明器；该工作区的 `boss/`、`counterexample/`、`security_global/`、`strategy_dual/` 材料也没有把本脚本的地板比较升格为定理。
- 仓库已有同主题的处置先例：`archives/customer-attraction/state/障碍/R-2fc分数地板与安全动作有限探针--障碍.md` 将同类固定 seed/trials、数值 SLSQP、精确根阈值材料标为 `finite-probe-retained`，明确 `candidate=null`/未击穿不等于一般地板或 safe-action 引理；若要升级，要求 exact Fraction、完整历史偏离证书和全称量词处理。
- 可保留的解析接口在 `archives/customer-attraction/tools/evidence/fractional-load-boundaries/original/research/current/customer_attraction/fractional_cover_path_budget.md`（真实根路径的 Fraction 前缀支付递推）和 `fractional_tail_waterfill.md`（给定终局的辅助分数水位引理）；二者都明确不自动给出新的单位玩家 SPE。`fractional_actual_load_counterexample.md` 还显示一个粗实际负载桥可被完整 SPE 族击破，所以不应从本探针的数值地板直推福利桥。

## 5. 集成/保留建议

1. 以 `finite-probe-retained / candidate-only` 保留脚本本身，不生成或宣称冻结 obstruction 结果（当前树没有该脚本产生的两个 JSON）。若清理目录需要摘要，说明“未运行/未见结果文件”，不要填入虚构的 counterexample 或 `candidate=null`。
2. 可把 `m` 记为探索记号 `M_frac(b)`，但文档须同时写出它是 SLSQP 候选点的 `g(q)·q`，不是已证明的分数最优值；不得写成对任意目录/人数的 floor lower bound。
3. 若将来发现 `FLOOR COUNTER`，先固定 exact 输入，再独立给数值优化的严格界并调用 `ExactSPESolver.ordered_outcomes`/`certificate` 检查完整有序策略。若将来发现 `INDUCTION COUNTER`，还要把每个 `bs` 绑定到同一历史/同一纯 SPE 证书，明确 safe-action 命题的“对所有历史、所有合法目录、所有续局”量词；否则仍只能是静态候选。
4. 当前最安全的整合是把它作为 fractional-cover/waterfill 研究的启发式搜索入口，和已有精确前缀预算、实际负载桥反例并列；不纳入 Q-CAG-HALF 的 proof graph，也不改变 OPEN 状态。

结论：源代码中 `floor` 的递推计算是 exact，`m` 与两类命中条件属于有限随机+数值实验；文件既没有可直接发布的反例，也没有一般安全动作证明。保留为有限探针并清楚标注量词与失败证书要求。
