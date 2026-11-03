---
id: "customer-attraction/dynamic-credit-one-step-closure-probe"
kind: computation
type_tag: 计算
title: "动态信用一步闭合随机 LP 探针"
status: "finite-floating-probe-found-witness"
truth_status: "finite-exploratory-LP-witness; no-SPE-or-universal-claim"
review_level: "full-1447-byte-read-and-execution"
scope: "R-12bf dynamic_credit/one_step_closure_probe.py; r=3,k=4,3000 random response maps"
summary: "随机 LP 探针在 trial 2 找到 gap=1/16 的 scalar one-step closure witness；这是有限浮点搜索，不是 exact JSON、完整 SPE 或原目标反例。"
source_refs:
  - "clean:ac321ae4ebb5862e0dc9:research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/dynamic_credit/one_step_closure_probe.py"
  - "local:archives/customer-attraction/state/反例/动态信用一步闭合标量反例--反例.md"
  - "local:archives/customer-attraction/state/障碍/动态信用一步闭合标量投影障碍--障碍.md"
source_identity:
  inventory_blob: "e2ee024e867f178d5fd2e6cc86f06ac867c92027"
  source_sha256: "8975d63c1fde7d51abfa8690b08ff2a119be44d4492ad5ea12c1242af2e32ba9"
  source_size_bytes: 1447
  frozen_commits:
    - "68fad804ec5946cb296f77dc5b336308a66abf12"
    - "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/dynamic-credit-one-step-probe-20261031/original/one_step_closure_probe.py"
  - "archives/customer-attraction/tools/evidence/dynamic-credit-one-step-probe-20261031/replay/probe.stdout.txt"
  - "archives/customer-attraction/tools/evidence/dynamic-credit-one-step-probe-20261031/comparisons/comparison-notes.md"
---

# 动态信用一步闭合随机 LP 探针

脚本完整实读 1447 B（SHA-256 `8975d63c1fde7d51abfa8690b08ff2a119be44d4492ad5ea12c1242af2e32ba9`，source ID `ac321ae4ebb5862e0dc9`，blob `e2ee024e867f178d5fd2e6cc86f06ac867c92027`）。它固定 r=3、k=4，在非空 mask 上随机生成 response map，使用 Fraction 计算 utility/profit，用 SciPy LP 检查根动作行和两倍尾利润行，并搜索覆盖 gap。

实际执行 3000 次抽样，在 trial 2 找到：

- response `{0:(2,2), 1:(2,3), 2:(1,2), 3:(2,3)}`；
- gap `1/16`；
- 支持权重 `{2:17/40,4:1/40,5:33/40,8:51/80,9:3/20}`；
- `minrow=0`。

这是有限浮点搜索 witness。它没有构造完整策略、验证末位 SPE、恢复 exact rational certificate 或证明所有 response map 失败。与 exact JSON/obstruction note 相比，它是独立随机探针，不能当作同一证书的生成程序；与 `coverage_one_step_probe.py` 相比，约束行不同，也不能合并。未迁移到 unrelated-machines。
