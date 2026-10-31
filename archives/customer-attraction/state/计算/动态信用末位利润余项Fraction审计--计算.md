---
id: "customer-attraction/dynamic-credit-terminal-profit-remainder-audit"
kind: computation
type_tag: 计算
title: "动态信用末位利润余项 Fraction 审计"
status: "finite-exact-audit-passed"
truth_status: "finite-regression-evidence; companion-general-identity-not-reproved"
review_level: "full-2589-byte-read-and-execution"
scope: "R-12bf dynamic_credit/background_probe/audit_terminal_profit_remainder.py"
summary: "Fraction 脚本核验末位余项局部恒等式 4394 次，并重算 69 客户标量样例；输出明确 full_SPE_reaudit=false，早期信用桥仍开放。"
source_refs:
  - "clean:df15c429ac7f43dd83a8:research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/dynamic_credit/background_probe/audit_terminal_profit_remainder.py"
  - "local:archives/customer-attraction/state/引理/任意背景的末位利润精确余项分解--引理.md"
  - "local:archives/customer-attraction/state/引理/背景新增覆盖余额与首步分解--引理.md"
source_identity:
  inventory_blob: "a03ad82f8199ba768c88a906bc34d93ac6c5d68a"
  source_sha256: "09c206124cfe699d1ee3f9368274be934a441ba499e991851f1e9baed6f9766c"
  source_size_bytes: 2589
  frozen_commits:
    - "68fad804ec5946cb296f77dc5b336308a66abf12"
    - "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/dynamic-credit-terminal-remainder-20261031/original/audit_terminal_profit_remainder.py"
  - "archives/customer-attraction/tools/evidence/dynamic-credit-terminal-remainder-20261031/replay/audit.stdout.txt"
  - "archives/customer-attraction/tools/evidence/dynamic-credit-terminal-remainder-20261031/comparisons/comparison-notes.md"
---

# 动态信用末位利润余项 Fraction 审计

## 身份、运行与处置

完整实读 `dynamic_credit/background_probe/audit_terminal_profit_remainder.py`（2589 B，SHA-256 `09c206124cfe699d1ee3f9368274be934a441ba499e991851f1e9baed6f9766c`，source ID `df15c429ac7f43dd83a8`，blob `a03ad82f8199ba768c88a906bc34d93ac6c5d68a`）。原程序和 stdout 分别保存在 evidence `original/` 和 `replay/`。

程序使用 Fraction 检查 `b,e,d=0..12`、`l∈{0,1}` 共 4394 个局部恒等式，再重算 69 客户标量样例。实际输出记录 `P=48`、末位 `v=18`、比较利润 `R=69`、`L=51/2`、`K=15/2`、`J=0`、总余项 33，且 `full_SPE_reaudit=false`。处置为 integrated 计算对象；本批未把 companion note 中的普遍代数证明重新冒称为程序证明。

## 核验内容与边界

脚本的 `terms(b,e,l,d)` 计算局部 `k,j` 余项并检查 `j,k≥0`、恒等式残差等于零。69 客户例固定 `actual=(0,0,0,5)`、`compare=(0,1,2,3)`，核验实际末位动作是终端最大回应，并比较 `p+3v-R=L+K+J=33`。这些是精确有限算术事实。

它不检查完整 69 客户 SPE 树，也不检查 companion note 的所有历史量词；输出明确声明该例 `full_SPE_reaudit=false`。它还不支付早期玩家与不同真实分支之间的共同信用，因此不能从末位余项自动推出一般 Q-CAG-HALF。

## 与既有对象的关系

既有 `任意背景的末位利润精确余项分解--引理` 承担一般恒等式和条件 `F_r(b)-P≤(r-1)v`；本程序是其局部和标量审计。`背景新增覆盖余额与首步分解--引理` 研究另一种覆盖余额望远镜，不能和末位余项混作同一动态付款。两者共同的开放点是：末位余项如何支付早期真实偏离和跨分支信用。

本批执行通过不是新定理，未迁移到 unrelated-machines；后续若要升级应保存 companion proof、完整 SPE 证书、输入清单和跨节点支付论证。
