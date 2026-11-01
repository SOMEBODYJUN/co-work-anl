# R-3002 八源：根行分离与联合必要行审计

本批八个源均由 Boss2 `clean show` 全文导出并按冻结 SHA/字节数核对。四个 Python 审计程序已 `py_compile`；独立 `Fraction`/整数满立方验证保存在 `replay/`，总验证见 `validation.json`。

`baseline_exact_primal.json` 与 `audit_baseline_point.py` 给出 36 个客户类型、235 条旧根行的精确必要条件点：`K=1`、`O=21/5`，所有旧行松弛非负，而 QL 标量余量为负 `-3697209993063870745398581491/36084325959030869305950000000000`。这只分离指定旧行系统，不能解释为游戏或 SPE 反例。

`audit_root_rows.py` 对五个 root requery 证书逐个重建系数并穷举完整 membership cube；每个证书最小整数残差为 0、唯一零类型，且在旧 exact point 上分离余量均为负。`audit_requery_merged.py` 对其中四个证书合并重复路径玩家收益后再次满立方检查，非零类型最小残差分别为 210、120、190、180。它们都是局部必要行证书。

`augmented_point_audit.json` 记录旧 canonical generator 的 3889 行重放及五条新 root 行，五条精确 slack 均非负（末项为 0），W 为 `11563846740120540563650285979166203/24234087715908087797320314905948740`；其状态明确是“3894 条必要关系的可行点”，不是 SPE 或目标反例。本批尝试重新运行该旧生成器，但完整冻结的 `six_maxroot/query_closure/general_payment` 依赖树不在八源内；错误原文保存在 `replay/augmented_point_audit.stderr`，没有把未重跑写成已验证。

正式对象仅记录这些精确处置与接续边界。后续若要推进六人半覆盖问题，应把根行关系与真实完整历史纯 SPE 条件、任意平局、空/重复主题和零客户情况分开重新证明；本批没有全称定理。
