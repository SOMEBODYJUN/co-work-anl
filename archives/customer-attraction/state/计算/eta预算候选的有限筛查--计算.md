---
id: "customer-attraction/eta-budget-candidate-finite-screen"
kind: "computation"
type_tag: "计算"
title: "eta 预算候选的有限筛查"
status: "finite-screen-read-with-no-counterexample-and-no-proof"
truth_status: "candidate-unresolved"
review_level: "full-source-read-and-output-comparison"
summary: "完整读取 R-3bc48 的 eta_budget_attack.json、test_eta_budget.py 与 workspace.json。测试攻击候选不等式 sum_i min_menu eta_i/r_i <= 2W-OPT；seed=723、1000 次有限随机搜索未发现正 excess，但最佳记录是全零权重的平凡样例，不能支持候选，更不能证明六人 Q-CAG-HALF。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3bc48d936f044f12b0fa743482ff5eb0/optimal_gap/eta_budget_attack.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3bc48d936f044f12b0fa743482ff5eb0/optimal_gap/test_eta_budget.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3bc48d936f044f12b0fa743482ff5eb0/workspace.json"
---

# eta 预算候选的有限筛查

## 来源与研究身份

本对象完整读取 R-3bc48 子目录的三个来源：一个 JSON 输出、一个 Python 筛查程序和一个 workspace 元数据文件。workspace 记录存档 `customer-attraction`、actor `R-3bc48d936f044f12b0fa743482ff5eb0` 及实例标识；它不提供数学证明。JSON 将候选状态明确写为 `finite tests only`，因此本对象保留为有限计算证据，不升级为定理或反例。

## 被攻击的候选不等式

程序针对候选

\[
 \sum_i \frac{\min_{A\in\text{menu}_i}\eta_i(A)}{r_i}
 \;\le\; 2W-OPT,
\]

其中 `r_i` 是剩余提供者数，`W` 是生成终局的客户福利，`OPT` 是在同一客户权重和主题目录上的最大覆盖福利，`eta_i` 是一个保持剩余最优覆盖的动作所产生的局部预算项。程序在每个阶段只从保持当前 `F(r,P)` 最大值的动作中取最小 `eta/r`，然后把这些局部值相加；`excess = eta_sum - (2W-OPT)` 若为正则构成候选反例。

## 程序实际做法

`test_eta_budget.py` 使用标准库 `Fraction` 计算整数/有理量，同时以 `random.Random(seed)` 生成有限输入。每次 `evaluate(m,p,weights,rng)`：

1. 令 `L=lcm(1,…,m)`，把每个客户类型的覆盖编码为主题位掩码；`size(U)` 给出被主题集合覆盖的客户权重。
2. 递归求 `F(k,P)`，即在已有覆盖 `P` 下用 `k` 个剩余动作可达到的最大覆盖权重；`OPT=F(m,0)`。
3. 递归 `solve(c)`，在计数前缀 `c` 下把下一位动作选为终局效用最大的主题。并列由随机数打破，记录 `policy`；这是一条有限策略生成规则，不是对所有完整 SPE 的枚举。
4. 沿生成路径逐位计算剩余步数 `r`、当前覆盖 `P`、动作 `A`、总终局效用 `d`，以及新覆盖量 `M,t`，使用

   \[
   \eta=r d-M-(r-1)t.
   \]

   对保持 `F(r,P)` 最大的候选动作断言 `eta>=0`，选最小 `eta/r` 并累计。

程序默认 `m∈{2,3,4,5}`、`p∈{3,4,5,6}`，权重数组长度为 `2^p`，每个类型以约 0.35 的概率获得整数权重 `1..30`，否则为零。主循环固定 `seed=723`、`trials=1000`；一旦发现 `excess>0` 就写 counterexample 并停止，否则写 best 记录。

## 冻结输出的实际含义

JSON 输出没有发现 counterexample，写入：

```text
candidate: sum_i min_menu eta_i/r_i <= 2W-OPT
status: finite tests only
seed: 723
trials: 1000
```

`best` 是第 6 次试验的四人三主题实例，但其八类客户权重全部为零，故 `W=0`、`OPT=0`、`eta_sum=0`、`excess=0`。这只是搜索排序下的平凡最佳记录；它没有测试出严格正权客户的边界，也不能作为候选成立的支持证据。输出保存了每一剩余步的 `r`、选择动作、`min_eta_over_r`、菜单极小动作和完整策略表，便于复核该特定零权输入。

## 与既有对象的关系和缺口

本源与[动态局部门槛的独立见证锥与人口预算](../资料/动态局部门槛的独立见证锥与人口预算--资料.md)的 TB/POP 预算讨论属于同一研究家族，但候选项、局部 `eta` 定义和有限生成路径不同。既有对象明确区分完整局部 SPE、独立 witness 与人口预算；本批没有证明其候选预算，也没有发现严格负点或六人 half 反例。

复用该筛查时必须保留以下边界：随机搜索只覆盖 1000 个小参数实例；并列动作使用随机 tie-break；策略由单一路径递归生成，而不是完整历史纯 SPE 的全量搜索；零权最佳记录不能替代正权输入。任何候选升级都需要正权、有理化的严格正 `excess`，并独立核对完整有序历史、真实 `OPT`、`2W-OPT` 与所有客户 IC。当前来源处置为 `integrated` 到本计算对象，状态保持 `candidate-unresolved`。
