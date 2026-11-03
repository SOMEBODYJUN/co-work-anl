---
id: "unrelated-machines/shared-ud-optimal-exchange-two-source-review"
kind: "review"
type_tag: "审查"
title: "共享UD最优交换有限网络双源审查"
status: "finite-exact-evidence-integrated"
truth_status: "finite integral-network coupling only; no asymptotic, k>=2, or end-to-end algorithm claim"
review_level: "full-json-read-code-read-and-prior-proof-comparison"
scope: "shared-UD optimal-vector exchange, heterogeneous lambda cases, root replay provenance, and exact small-network enumeration"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/shared_ud_optimal_exchange_root_replay_scope.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/shared_ud_optimal_exchange_root_replay_scope.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/shared_ud_optimal_exchange_small_network_audit.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/shared_ud_optimal_exchange_small_network_audit.json"
---

# 读取范围与对象

本审查逐字读取两个冻结 JSON，并继续读取其规范程序 `tests/audits/unrelated_machines/shared_ud_optimal_exchange_small_network_audit.py`（inventory code SHA `823132666e9442093aec2a2506644d3835e4622b996d4f4da302e391101864ec`）。库存稳定 ID 为 `08a34146d494774f899f`（root replay scope，文件 SHA `1c0a21c5425cc6bd723ff41e6be8914c7159eeaba4b823017e002799e3e74adc`）和 `5155d8c9c4bad4f82a5e`（small-network audit，文件 SHA `474aea7b8ce9359ddecf429c455aa807ff375e96fafb5a73ab36820d726c2600`）。两个 commit 绑定的是同一路径版本；不把 legacy/main 记成两次数学实验。

程序的模块 docstring 已明确写出：它审计 weighted profile-exchange coupling，不是算法；直接枚举原始 resource ownership 与 leaf matchability，不使用 matroid exchange、potential formula 或证明中的 coupling construction；小实例不推出 19/10 或渐近结论。这些限制构成正文的量词边界。

## 有限交换性质

程序对 240 个 case 做直接穷举。每个 case 取 `n=4` 或 5 个资源、1 或 2 个 leaves、3 个 helper menus；owner 向量固定为 `(0,0,1)`，home weights 为 `(2/5,3/5,1)`。对每个 menu 的两种状态，按 `Fraction` 生成归一化资源向量；对外层权重 lambda 交替使用等权和两组异质权重 `(1/17,91/17)`、`(27/5,2/9)`。每个 case 改变一个 profile 坐标，分别计算旧/新 profile 下所有可行原始 ownership 的最优加权向量集合。

对每个旧最优向量 `x`，程序寻找新最优向量 `y`，要求
`||y-x||_∞ <= lambda_owner * home_weight`、
`||y-x||_1 <= 2 * lambda_owner * home_weight`，并断言 `sum(y-x)` 恰好等于新旧最优目标值之差。这个结论是“存在一个受单 helper 贡献界控制的最优向量交换”，不是给定任意 tie-breaking 的唯一交换，也不是一个已证明的全局 potential 下降。

冻结输出报告：

- `cases=240`；
- `feasible_original_resource_ownerships=26674`；
- `all_old_optimal_outer_vectors_checked=242`；
- `heterogeneous_lambda_cases=160`；
- `changed_helper_has_other_same_outer_helper_cases=160`；
- `passed=true`。

这些数量说明程序实际覆盖了异质 lambda 和同一 outer 的其它 helper 仍可变化的情形。它仍然只覆盖 4/5-resource、3-helper、1/2-leaf 的有限积分网络，不能外推到任意 `k>=2`、任意菜单状态数量、任意叶超图或共享 home 的完整域。

## root replay 证据与软件边界

`shared_ud_optimal_exchange_root_replay_scope.json` 记录作者 actor、日期、规范 code SHA、实际 argv/cwd、fresh stdout 路径和 stdout SHA。root replay 的 stdout 与作者输出逐字相同（`author_stdout_byte_identical=true`），退出码 0，seed `31082026`，精度为 `fractions.Fraction` 加 exhaustive original integral ownership sets。该包装的独有内容是复现 provenance，不是新数学对象；它确认小网络 audit 的输出可由指定程序与指定命令重放。

root replay 同时明确 `not_checked`：渐近定理、`k>=2` tiny 输入域、k=1 greedy、potential profile search、Frank–Wolfe、common prefix circulation、full original job output 和 end-to-end algorithm implementation。故不能因为 stdout 字节相同，就把有限交换引理升级为完整 19/10 近似算法或目标问题的 hardness/algorithm 结论。

## 与既有共享UD正文比较

1. 与已有《共享UD叶与k²-home算法》及《O(1/k)-home实际分配算法》：那些正文包含 potential、相对曲率、共同叶 matching、prefix-flow 和实际 allocation 的条件证明；本批程序明确不实现这些构造，因此只能作为“局部最优向量交换边界”的有限回归，不能代签证明中的关键 coupling。
2. 与已有 shared-UD exchange/rounding 讨论：本批把 `L∞/L1` 换界和异质 lambda 的存在性写成可重放的 exact finite contract，补上同 outer helper 变化的计数；它不修复全状态 profile 选择、共同叶容量或原始 job 输出的缺口。
3. 与旧图、摘要和未完成工作区：旧材料只作为线索。完成依据是本次实际读取 JSON、程序正文和 source SHA；没有把旧图直接导入成数学结论。

## 处置与后续接口

**固定有限结论：** 对列出的 240 个随机种子固定 case，所有被枚举的旧最优加权向量都存在满足指定 `L∞/L1` 界的新最优向量，目标差等式精确成立；root replay 与作者 stdout 字节一致。

**有限实验/程序证据：** `seed=31082026`、26674 个可行 ownership、242 个旧最优向量、160 异质 lambda case 和 160 个同-outer helper 变化计数。它适合作为交换核回归和后续 coupling 实现的单元级证据。

**障碍：** 尚未验证任意 profile 的最优面结构、全 k² tiny 域、Frank–Wolfe 或整数 prefix-flow，也未运行完整原始 job 输出。将来若接续，需给出目标量词、共同叶容量、实际 selector/incidence 回填和分母/位复杂度；不能仅扩大随机 case 数量来替代这些证明。
