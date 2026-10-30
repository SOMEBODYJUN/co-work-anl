---
id: "unrelated-machines/normalized-menu-welfare-ce-backend-finite-review"
kind: "review"
type_tag: "审查"
title: "归一化菜单福利与 CE 后端有限审查"
status: "finite-exact-audit-with-proof-scope"
truth_status: "finite implementation audit only; the universal welfare proof remains separately scoped"
review_level: "full-json-read-and-scope-comparison"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/normalized_menu_partial_quota_welfare.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/normalized_menu_partial_quota_welfare.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/multi_outer_request_winner_pair_backend_audit.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/multi_outer_request_winner_pair_backend_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/multi_outer_request_winner_pair_backend_root_replay_scope.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/multi_outer_request_winner_pair_backend_root_replay_scope.json"
evidence:
  solver_sha256: "ee41f5fd20993dff6ecdf7103d5930793654201557b83c293f9b929e3d971e53"
  replay_code_sha256: "460679c82477934bcfdc3ad326f39dd0d0dd0baf7fa4fd75d02df015c7f6b2f0"
---

# 归一化部分配额福利审计

`normalized_menu_partial_quota_welfare.json` 的程序和输出全部使用 `fractions.Fraction`。它保留重复 indexed states、零权重、零激活行、未用资源、大二进制分母和极小 `q`，并在无随机抽样的有限域中枚举 5,696 个候选，拒绝 2,168 个超容量项，接受 3,536 个，访问 86,912 个 joint actions 和 42,418 个正概率前缀；边界 fixture 为 8 个，非法输入拒绝 19 个。

审计域固定为 1–3 个资源、1–2 个组、每组两个状态，状态是 `{0,1/2,1}` 上的所有有序 pair（保留重复），`theta∈{1,1/3,1/2,5/6}`，`delta=3/8`，并以全部正概率 joint actions 作为 oracle。它验证实现的容量、CDF、潜势和 attaining-state 处理与有限精确 oracle 一致；它没有实现 LP 求解器、一般 unrelated-machines 调度器或复杂度归约。

现有归一化菜单正文/审查给出更一般的福利计数证明（例如在明确 `q>0` 和 `δ+(1−δ)β<1−1/e` 域内的条件结论）。本 JSON 只能作为程序和列明有限输入的复现证据，不能把有限枚举升级为普遍福利下界，也不能把 `q=0` 的理论分支写成当前软件合同。

# 多外层请求 pair backend

`multi_outer_request_winner_pair_backend_audit.json` 只有两个“两资源、三 helper、两 outer、均匀请求率”的有限 CE 例：分别遍历 2,048 与 2,916 个 brute outcomes，精确计算均值、seconds、初始/终止潜势和 11 步 conditional-expectation 后端。第二例允许实际 outer value 为零，因此不是正值定理的输入。审计明确 `whole_scheduling_algorithm_checked=false`、`small_weight_class_instantiated=false`。

配套 `root_replay_scope.json` 的程序和 stdout 字节与作者输出相同，Fraction 精度、无随机 seed；但 root 只读并共同开发分母/请求 coin caveat，不是独立审查者。范围仍只有这两个例子，没有 tiny-domain/LP/MW/一般调度实现。它可作为 CE 后端回归和字节一致性证据，不是全局 welfare 或调度证明。

## 处置与接续

两类来源都 integrated 到本审查：归一化菜单的有限 solver 证据与 pair backend 的有限 CE 回放保持不同对象和量词。后续扩展必须补上完整输入域、正值/零值分支、全局概率相容性和实际调度接口；不得因 exact JSON、11 步 CE 或作者 stdout 相同而声称算法已在一般模型闭合。
