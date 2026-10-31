# R-31bbb：终局税桥与弱匹配锥的有限屏幕

## 范围与资料身份

本对象处置 R-31bbb6cfd6594bc8bb076db7b2950993/terminal_tax、weak_matching 以及工作区元数据的六个冻结源。逐源 `clean show` 输出、SHA/大小、依赖和重放位于 `archives/customer-attraction/tools/evidence/R-31bbb-tail-20261031/`；`validation.json` 的独立断言通过。

六个源分别是：

* `874d2e5005dc4b2b770a`：`terminal_tax/named_run.json`；
* `4789e4082bbf9cfe27ca`：`terminal_tax/probe.py`；
* `6ffc4dceb4d6d84bae0b`：`weak_matching/addition_m4p6_seed10211.json`；
* `4c4118f59f0c8493e2f0`：`weak_matching/markov_cone.py`；
* `1101265dd6065cf6fbcd`：`weak_matching/portfolio_addition_cone.py`；
* `884171b4b9d5dc1039b2`：`workspace.json`。

`workspace.json` 只有 schema/save/actor/instance 的 provenance 字段；它被保留到 source-manifest 并在正文中说明，没有数学断言。

所有程序都把 LP 结果定位为“counterexample discovery only”或“finite complete-policy cone attack”。它们在每个 ordered history 使用完整 continuation policy 的行，但权重和分离器由浮点 SciPy/HiGHS 求出。没有正 gap 候选经过有理恢复，因此本批属于有限实验屏幕与障碍记录。

## 终局税桥（terminal_tax）

`probe.py` 检验的桥形是
\[
  \operatorname{OPT}\le W+\sum_x\frac{c_x}{c_x+1},
\]
其中 `c_x` 是终局中覆盖客户类型的计数。`matrix` 用整数 `lcm(1,\ldots,m)` 缩放 ordered-history deviation rows，`attack` 对每个大小为 \(\min(m,p)\) 的目标 support 解一个 full-policy cone LP；正 gap 才会进一步尝试 Fraction 恢复、exact `StrategyCone.verify` 和 integer-clone audit。

`named_run.json` 给出 17 个已有证书策略的有限浮点结果。独立重放使用同一 canonical package、`customer_attraction_strategy_lp.py` 和冻结证书集合；当前证书目录多了两个可读文件，所以重放有 19 行，但原 17 个 `label` 逐项匹配、gap 和状态完全相同。所有 17 行状态均为 `finite_floating_cone_result_only`，gap 均小于 0；最接近零的是 `root_tax_failure.json` 的约 \(-0.05\)，对应 4 人 6 主题、259 ordered nodes。没有触发 `exact_full_policy_auxiliary_bridge_counterexample`。

这组数据支持的事实是：在这些固定完整策略与目标 support 组合上，浮点锥没有发现负向终局税桥分离器。它不能量化为所有客户盒、所有平局或六提供者模型的定理；`named_run` 的 `scope` 已明确写出 finite complete-policy cone attack。

## 弱匹配与 addition 屏幕

`addition_m4p6_seed10211.json` 是 `portfolio_addition_cone.py` 的 200-game 冻结结果：`status=no_floating_separator_in_finite_sample`，`games_processed=200`，`policy_target_pairs=1663`，`largest_gap=-0.02702702702702703=-1/37`，`candidate=null`。复跑使用 `--topics 6 --players 4 --seed 10211 --mode portfolio`，除输出路径和新增的 `mode` 字段外，五个数值字段完全一致。

`portfolio_addition_cone.py` 对 ExactSPESolver 产生的每个完整策略证书，比较所有支持大小 `1..min(m,p)` 的 portfolio 与目标最优 support，并把终局 `covered-addition` 行加入 LP；代码注释明确严格唯一只是为了把所有最优 portfolio 计入，正 gap 仍需精确审计。一次单局 smoke 的最大 gap 为 \(-0.1\)，200 局重放给出上面的 \(-1/37\)，均无候选。

`markov_cone.py` 是另一条计数状态 Markov 搜索。它在 count state 比较所有 action children 的真实终局 policy state，并把每个 count policy lift 到 ordered histories；代码同时声明一般定理不限制于 Markov。固定 seed 10214 的两局 smoke 处理 32 个 policy/target pairs，`largest_gap=-0.026845637583892745`，无 candidate。这个读数只能作为小样本屏幕，不能把 Markov 子类无命中升级成全策略结论。

## 证据、复现与缺口

证据包包含：

* `source/` 的六份原始冻结文件和 `clean-show/` 六份服务端指纹；
* `dependencies/customer_attraction/`、`dependencies/tests/audits/customer_attraction_strategy_lp.py` 与完整证书 JSON，供终局税 named replay 使用；
* `replay/terminal_named_smoke.json`、`replay/markov_smoke.json`、`replay/portfolio_smoke.json` 和 `replay/portfolio_200_replay.json` 及 stdout/stderr；
* `source-manifest.json`、`run-manifest.json`、`validate_r31tail.py` 与 `validation.json`。

验证器检查六个冻结 SHA/大小、17 个 named 结果逐标签匹配、Markov smoke 无 candidate、portfolio 一局及 200 局结果、以及 workspace actor/save。所有 Python 源与依赖通过 `py_compile`。

后续若要推进这些方向，应把浮点负 gap 转成可复核的有理不等式：先从各策略的 LP 权重恢复 Fraction，逐 ordered history 检查 SPE deviation rows，再精确计算终局客户值与目标 OPT。若出现正 gap，必须保存第一条失败类型、完整动作树、整数 clones 和 verifier；当前没有这类候选。还需将 Markov 限制、portfolio 严格唯一条件、空/重复主题、零客户与任意 tie-break 回接到六人六提供者主模型，不能直接把辅助桥读数当作 half 覆盖结论。
