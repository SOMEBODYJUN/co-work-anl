# 机器固定倍率公共尺寸精确重开：独立审查

## 审查身份与范围

审查对象是 `UM-COMMON-MULTIPLIER-UNKNOWN-B-EXACT-v1`，正文为
`research/current/unrelated_machines/unknown_target_common_multiplier_exact_repair.md`，审计为
`tests/audits/unrelated_machines/unknown_target_common_multiplier_exact_repair.py`。
本审查只覆盖正文声明的冻结核心、资格连通分量、公共尺寸 `q_C` 与机器固定倍率 `a_i`；不把接口失败升级为一般 `FAIL`，也不把它外推成 `UM-TARGET-v1` 算法。

## 独立重构

对一个分量，任务若在机器 `i` 上接收 `t_i` 件，最终负载恰为
`f_i+a_i q_C t_i`。因此任意最优峰值必属于
`{f_i+a_i q_C t: i∈M_C, 0≤t≤|U_C|}`。给定候选 `B`，在先检查 `B≥max_i f_i` 后，机器容量是
`floor((B-f_i)/(a_i q_C))_+`。任务到机器的资格图配合这些整数容量构成二分最大流；满流等价于一个真实不可拆分分配达到 `B`。候选集合有限且上端可行，排序后二分首个满流候选得到精确分量最优值。机器侧不交的分量可取峰值最大者。

## 攻击与修复

1. 若省略冻结核心下界，`f=(2,0)`、一件任务只可去机器2、`q=1`、`B=1` 会产生错误满流；正文保留 `B<max f` 的先行拒绝，消除此漏洞。
2. 若同一分量混有两个任务尺寸，单一整数槽容量不再表示不可拆分总量，问题退化为多尺寸装箱/广义指派；正文没有越过此边界。
3. 若机器倍率不是固定于机器而是随任务变化，按单一参考尺寸取比值会误报容量；正文把该条件作为可验证输入承诺。
4. `q_C=0` 和零处理时间任务先分支处理；空任务以及孤立冻结机器均在峰值合并时保留。

## 复核结果

已运行：

```text
python3 tests/audits/unrelated_machines/unknown_target_common_multiplier_exact_repair.py
python3 -m py_compile tests/audits/unrelated_machines/unknown_target_common_multiplier_exact_repair.py
python3 -m compileall -q tests/audits/unrelated_machines
```

独立脚本用 `Fraction` 穷举 400 个随机小实例，并核对冻结核心 guard 与两个不同 `q` 的不交分量；输出为
`{'random_instances': 400, 'frozen_guard': 'ok', 'disconnected_components': 'ok'}`。
这些是有限核验，不承担全称证明。声明范围内未发现仍成立的致命异议；范围外的混合尺寸、一般核心生成和统一相对保证仍未解决。

**状态：** 受限命题的证明与内部审查完成；实现轴为 `audit_only`；外部评审和新颖性未认证；`UM-TARGET-v1` 仍 OPEN。
