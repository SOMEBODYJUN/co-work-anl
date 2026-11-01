---
id: "customer-attraction/Ra0-background-near-saturation-audit-v2"
kind: "review"
type_tag: "审查"
title: "Ra0 背景近饱和审计 v2 脚本"
status: "finite-audit-script-read; syntax-validated"
truth_status: "finite-certificate-audit-framework; no-universal-lemma"
summary: "冻结 v2 脚本用 Fraction 在指定完整纯 SPE 证书上逐有序节点核验 BNS/AP 中间不等式、任意主题查询和实际后继边界；脚本明确不推出普遍引理或 Q-CAG-HALF。"
source_refs:
  - "clean:cbd7d354e0b358cc2510:research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/background_near_saturation_audit_v2.py"
  - "local:archives/customer-attraction/tools/evidence/Ra0-py2-agent/manifest.json"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/Ra0-py2-agent/background_near_saturation_audit_v2.py"
  - "archives/customer-attraction/tools/evidence/Ra0-py2-agent/manifest.json"
---

## 来源和范围

主源为冻结的 `background_near_saturation_audit_v2.py`，6584 字节，SHA-256 为 `f1ce76100f0a5a733c3eb1dbbaca2da68b08980e89110e6389c253e61a927bdd`。文件头已经限定：这是对指定有限完整纯 SPE 证书的精确审计，不限制策略为按计数的 Markov 形式，也不证明普遍引理或 Q-CAG-HALF。该副本通过 `py_compile`；本轮没有伪造其外部 `nonpne_best.json` 输入，因此没有把未执行的生成流程冒称复现。

## 审计的实际对象

`audit(inst, cert, name)` 先调用 `verify_certificate`，要求完整有序历史的策略证书和所有偏离通过定义级检查。对每个历史 `h` 及动作 `a`，仅在剩余人数 `k≥2` 时计算背景负载 `b`、权重 `w_j=1/(b_j+k)`、每主题大小 `s_C`、最大值 `K`、当前行动收益 `u` 和 `delta=u-K`，并断言 `delta≥0`。

随后它枚举任意主题对 `(C,D)`，检查 v2 的主题特定 `M_C` 系数不等式；再沿给定证书的真实后继分支，计算 `v`、末位主题 `L`、尾部差额 `d,d_L`，核对 `K≤v≤u`、`d≤(M−1)delta`、`t−v` 的尾部界、`d_L≤d`，以及 `k=2` 时的等号。对于 `delta=0` 的饱和分支，脚本额外检查所有真实尾部主题与最大主题 C 的客户支持一致。最后把实际末步偏离收益与中间行比较，记录最小 slack 和饱和分支数。

`generate()` 构造零客户、共同重复客户、大私有客户和四组稀疏随机实例，并从精确 SPE 求解器挑选目标终局、随机选择可行动作和后继继续生成证书；还尝试加载另一个工作区的 `nonpne_best.json` 作为已有实例。生成结果的 `scope` 字段明确只覆盖这些指定有限证书。

## 可复用结论和边界

v2 的新增检查点是把主题最大负载 M 收紧到比较主题 C，并同时核对任意 `(C,D)` 行、真实后继行、直接末步偏离和 `delta=0` 的支持饱和条件。它适合做有限回归和中间式审计，能够发现实现、量词或系数错误；但脚本本身不证明任意目录、人数、客户重数或所有完整历史的 BNS/AP 引理，也不推出半覆盖结果。

本轮没有执行 `generate()`，因为其外部 `nonpne_best.json` 路径不在当前可用输入中；因此不报告脚本的汇总计数、随机实例结果或运行时间。后续若要复现，应先恢复同一冻结依赖和 `customer_attraction` ExactSPESolver，再逐行保存证书哈希、历史/偏离计数及最小 slack。
