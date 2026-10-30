---
id: "unrelated-machines/multirow-shared-escape-hall-finite-review"
kind: "review"
type_tag: "审查"
title: "多行共享逃逸与 Hall 边界有限审查"
status: "finite-exact-boundary-audit"
truth_status: "finite Hall certificates and endpoint obstructions; no general constrained-extension solver"
review_level: "full-json-read"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/multirow_count_extension_audit.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/multirow_count_extension_audit.json"
evidence:
  base_commit: "957f04bcdc4dfd0723c8211559ced4c0be988127"
  audit_sha256: "1e2dec124bd2df625d8e4660722ca7218e87b2a6c32d75e76aaffe4bb5d97170"
---

# 多行配置延伸的实际内容

`multirow_count_extension_audit.json` 记录一个精确整数负载单位为 `1/k`、处理时间用 `Fraction` 的多行真实负载审计。它研究紧凑共享逃逸延伸中的容量/Hall端点，不是一个通用配置 LP 或调度算法。

在 `k=2`，审计穷举最多 4 个 `U` 中心的全部中心子集 163 个、所有合格 `v` 与配置 50,319 个、任务分配 2,012,760 个；所有其它行由计数上界覆盖。结构化 `k=3` 查询检查 12 个边界中心、30 个配置查询和 3,780 个任务分配，在 13 个受保护中心处出现尖锐失败；强制配置 `z=empty` 时，Hall 任务数 18 而邻居数 17，匹配秩恰为 17，缺口来自一个真实负载 1 中心不能接 `X`：其 `k` 个 `Z` 与 `k` 个 `Y` 需要 `2k>k+1` 个局部单位槽。

审计还保留 5 个受保护中心的同型必要证书（8 个任务、7 个邻居），说明该端点是由容量计数直接推出的障碍。结果只证明必要 Hall 条件失败，不是对所有配置或所有调度的全枚举；不同查询之间的分布也不自动相容。

## 与既有对象的关系和范围

该有限记录应连接到相关紧凑容量一星/共享资源对象，作为其多行延伸的端点审查。它不能被改写为 LST、配置 LP、条件分布或一般 `UM-TARGET-v1` 的反例；审计明确没有通用 constrained-extension solver、没有新的近似算法、没有复杂度或新颖性结论。后续若要推广，必须先证明所有多行查询共用同一个全局分布，并给出匹配/配置合同，而不能把各次 Hall 必要条件拼成充分条件。
