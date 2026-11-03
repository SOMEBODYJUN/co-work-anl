---
id: customer-attraction/dynamic-credit-probe-floor
kind: computation
type_tag: 计算
status: finite-fixed-policy-probe-integrated
truth_status: finite-floating-diagnostic; no-universal-floor-result
source_identity:
  inventory_blob: "9dcbfb94ab6dd0cdadcb5bbed3ed0467211344c8"
  source_sha256: "9f8b0ecd1c1054ebd0998f1a8278ce7f2faf2b84c7d0a339b8be2d4bade90d30"
  source_size_bytes: 1457
source_refs:
  - clean:ed4a82e6bbff2de36018:research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/dynamic_credit/probe_floor.py
---

# 动态信用固定策略 floor LP 探针

脚本固定 `m=3,k=6` 和一份确定性 `sigma`，枚举有限历史/偏离及所有重复比较 profile，以浮点 LP 检查 floor。运行输出 `best floor violation=-0.2619342072718278 (1,2,5)`、`minrow=0`、`first=102/311`，未发现正 violation。

这只是一个 hard-coded policy 的有限浮点诊断；负 score 不是普遍 lower bound，脚本不覆盖其他 policy、输入或完整 SPE。与动态一步 probe/弱匹配审计对照，不能升级 Q-CAG-HALF 或 unrelated-machines 结论。
