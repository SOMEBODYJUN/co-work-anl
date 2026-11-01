# R-2fc round3_security 六源清洗

六个源均在认领后执行 `clean show` 并返回 0。它们属于一个较大的 support-budget DR 探索类，源文件自己反复写明 `EXPLORATORY_LARGER_MODEL_NOT_CAG` 或 “never CAG evidence”。原始输出、冻结 blob/大小/SHA 在 `source-manifest.json`；`support_budget_probe.py` 的 py_compile 和两种策略 smoke 输出保存在 `replay/`。

`support_budget_probe.py` 用掩码 support value (W) 定义递归 (|q|\Phi(q)=W(\operatorname{supp}q)+\sum_aq_a\Phi(q-e_a))，施加单调/DR/交替约束、一个固定策略的完整有序历史比较，并以浮点 LP 迭代寻找预算下界。它处理的是 support-budget DR 游戏，不是共同目录 CAG；没有客户类型、终局客户均分或合法 CAG 的 SPE 语义。

五份 JSON 报告给出有限参数记录：

- `rank_seed_n4k6.json`：(n=4,k=6)、100 trials、submod policy，`best=0`。
- `support_submod_alternating_n4k6.json`：(n=4,k=6)、50 trials、submod+alternating，`best=0`。
- `support_submod_groups_n3k6.json`：(n=3,k=6)、1 trial、groups，`best=0`。
- `support_submod_n5k6.json`：(n=5,k=6)、30 trials、submod，`best=0`。
- `support_groups_n3k6.json`：(n=3,k=6)、1 trial、groups，出现浮点 `best=-0.006552668982782672` 的 LP witness，包含 fractional `p`, `W`, policy 和 root；它仍被标为较大模型探索，不能解释为 CAG 客户实例、纯 SPE 证书或半覆盖反例。

验证清单 `validation.json` 确认五份 JSON 的状态标签、源 SHA/大小、脚本编译和 1-trial smoke 均通过。该批只保留较大 support-budget 模型的探索边界；没有把负 witness 迁移到 Q-CAG-HALF，也没有把四个 no-hit 报告升级为普遍定理。
