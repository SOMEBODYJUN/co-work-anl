# 旧完整 SPE 的有限匹配预算探针

本页是 `R-059140e622784d85a4e3a4dd6554f506` 批次中 `cross_tree/pivot_probe.json` 与生成脚本的独立计算记录。完整结论和量词限制见《动态可信门槛与剥离递归缺口：有限反例及精确重置项》；这里单独留下可复现的有限表格，避免把 JSON 当作定理。

- 范围：old complete SPEs；候选 beta-packing 与 fixed legal owners；不是所有实例或所有可行付款规则。
- 精确算术：源脚本使用 `Fraction`；输出为 `computed`。
- 结果：`portfolio_matching_failure` 的 role/action 为 `2/11`，`cap2=13/11`；`root_tax_failure` 为 `1,1,2`；`individual_security_failure` 为 `1,49/67,1696/1015`；`eight_cce_welfare_gap` 为 `3/2,1,2`；`coverage_opportunity_failure` 为 `1,1,2`；`prefix_balance_failure` 为 `51221/76055,748568/1323357,14807/8323`。

这些只是有限候选路线的障碍证据，不能推导主目标反例。原 JSON、脚本、哈希和冻结 commit 见 `archives/customer-attraction/tools/evidence/R-059140e622784d85a4e3a4dd6554f506/`。
