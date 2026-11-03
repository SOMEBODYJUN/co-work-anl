---
id: "customer-attraction/direct-cover-weak-matching-lp-diagnostic"
kind: computation
type_tag: 计算
title: "直接覆盖弱匹配 LP 诊断入口与有限锥边界"
status: "source-read-diagnostic-only-not-executed"
truth_status: "finite-exploratory-LP-tool; no-universal-bridge-result"
review_level: "full-5104-byte-read; direct-cover-and-weak-matching-comparison"
scope: "R-12bf direct_cover/lp_weak_matching.py; random finite strategy-cone LP diagnostic"
summary: "脚本随机生成 k-topic 客户重数，构造真实偏离/覆盖约束并用 scipy linprog 检查 match、strong_average 或 average bridge；它是有限诊断入口，不是求解器或一般证明。本批未运行。"
source_refs:
  - "clean:72e45e29364108da001a:research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/direct_cover/lp_weak_matching.py"
  - "local:archives/customer-attraction/state/审查/customer-attraction直接覆盖分支README、义务分层与前缀障碍路由--审查.md"
  - "local:archives/customer-attraction/state/计算/弱匹配与分区查询的精确核验--计算.md"
  - "local:archives/customer-attraction/state/候选/真实前缀均匀组合接口--候选.md"
source_identity:
  inventory_blob: "e3360bfa0728a02f1de5146f8c8207b04137ae4f"
  source_sha256: "1dd36dfc20d6bceb04b07b312282da3b370be2424782647b9a675fb4c740a4fd"
  source_size_bytes: 5104
  frozen_commits:
    - "68fad804ec5946cb296f77dc5b336308a66abf12"
    - "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/direct-cover-weak-matching-lp-20261031/original/lp_weak_matching.py"
  - "archives/customer-attraction/tools/evidence/direct-cover-weak-matching-lp-20261031/comparisons/comparison-notes.md"
related_objects:
  - "archives/customer-attraction/state/审查/customer-attraction直接覆盖分支README、义务分层与前缀障碍路由--审查.md"
  - "archives/customer-attraction/state/计算/弱匹配与分区查询的精确核验--计算.md"
  - "archives/customer-attraction/state/候选/真实前缀均匀组合接口--候选.md"
---

# 直接覆盖弱匹配 LP 诊断入口与有限锥边界

## 身份与处置

本源是 `R-12bf6a96d24c48eca828620d6642e203/direct_cover/lp_weak_matching.py`，clean source ID `72e45e29364108da001a`，大小 5104 字节，SHA-256 `1dd36dfc20d6bceb04b07b312282da3b370be2424782647b9a675fb4c740a4fd`，inventory blob `e3360bfa0728a02f1de5146f8c8207b04137ae4f`。完整原文保存在 [脚本 evidence](../../tools/evidence/direct-cover-weak-matching-lp-20261031/original/lp_weak_matching.py)。

处置为 `integrated` 的计算入口对象，但状态为“诊断专用、未执行”。脚本文件头已经写明 `Find a bridge counterexample in fixed complete strategy cones; diagnostic only.`；本批实读代码、依赖和输出边界，没有运行随机 LP，因此不生成新的数值结果。

## 代码实际做什么

默认 `search(k=6,m=4,steps=50,seed=20261023,kind="solver",bridge="match",min_depth=0)`。每个 step：

1. 在全部非空 k-topic masks 上随机生成客户重数；一部分步骤偏向小支持或稀疏输入；
2. `kind="solver"` 时构造 `customer_attraction.model.Instance`，用 `ExactSPESolver` 随机抽取 worst outcome 和 continuation certificate；另一种 kind 直接为每个历史选择 utility 最大的动作并随机处理 ties；
3. 用 `utility`、`cover`、完整 histories 和 profiles 构造实际偏离行；对每个随机比较目标添加覆盖约束；
4. 在 `bridge="match"` 时加入 target 主题排列的匹配约束，在 `strong_average` 或其他模式时加入平均形式目标；
5. 用 `scipy.optimize.linprog` 在非负客户分布及辅助变量上寻找最小目标值；发现负值时再将浮点量近似为 Fraction，重建 Instance 和 StrategyCertificate，调用 `verify_certificate` 和 `check_weak_matching.evaluate`，通过后写出 `weak_matching_lp_candidate.json`。

代码同时保存 `best` 浮点目标、随机种子、step、target profile、候选实例和证书。它依赖 NumPy、SciPy、canonical customer-attraction model/exact/certificate、`check_weak_matching` 等外部模块，并非独立可移植证明器。

## 诊断边界

该程序只能探索有限的随机客户重数、固定 `k,m`、固定 step/seed、有限 strategy cone 和所选 bridge 约束。即便 `verify_certificate` 通过，也只得到某一份完整策略和某一输入的有限候选；浮点 LP 的负值还需要有理恢复、全历史 SPE 校验和语义核对。若搜索没有负值，更不能推出 bridge 对所有实例成立。

与已归档 `customer-attraction直接覆盖分支README、义务分层与前缀障碍路由` 相比，本脚本是其 `lp_weak_matching.py` 指针的原始实现；README 已停止少量 m=4/k=6、m=5/k=7 的同类随机扫描，明说不能代替 weak matching、weak/strong average 或 Q-CAG-HALF 证明。与 `弱匹配与分区查询的精确核验--计算` 相比，本脚本没有继承其有理恒等式、固定 52 客户策略或 1302 组合 Fraction 复核；它是另一条随机固定锥诊断路线。

## 接续和不迁移边界

若未来确需执行，应在隔离目录固定 Python/NumPy/SciPy/canonical source 版本，保存完整 argv/cwd/seed、原始 stdout/stderr、LP 结果、证书哈希和有限 scope。任何候选都要和 direct-cover 的真实偏离、弱匹配量词及已有障碍逐项比较。本对象不迁移到 unrelated-machines 调度，也不生成一般 half、hardness 或 algorithm 结论。
