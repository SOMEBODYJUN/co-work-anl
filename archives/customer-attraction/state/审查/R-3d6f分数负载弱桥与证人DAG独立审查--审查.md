---
id: customer-attraction/r3d6f-fractional-weak-bridge-and-witness-dag-review
kind: review
type_tag: 审查
title: R-3d6f 分数负载弱桥与证人 DAG 的独立审查
status: exact-family-and-finite-audit-reviewed
truth_status: auxiliary-weak-bridge-refuted; Q-CAG-HALF-unaffected
review_level: independent-unit-audit-and-source-comparison
scope: four-topic fractional actual-load family, finite m=2..7 replays, and outcome-DAG witness equivalence
summary: Independent standard-library audits reconstruct a complete pure SPE family with m²+1 customers, W=m² and OPT=m²+1, refuting the fixed actual-load weak bridge for every m≥4. The exact m4 audit gives W=16, OPT=17 and weak-bridge gap 11/26. A separate outcome-DAG review proves finite witness constraints equivalent to full-history SPE realizability for a fixed root outcome, while floating MILP optima remain uncertified.
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3d6f7a072d5e489eb5a0bdc4d32bb769/independent_audit/audit_fractional_family.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3d6f7a072d5e489eb5a0bdc4d32bb769/independent_audit/audit_fractional_weak.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3d6f7a072d5e489eb5a0bdc4d32bb769/independent_audit/fractional_family_audit.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3d6f7a072d5e489eb5a0bdc4d32bb769/independent_audit/fractional_family_review.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3d6f7a072d5e489eb5a0bdc4d32bb769/independent_audit/fractional_weak_m4_audit.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3d6f7a072d5e489eb5a0bdc4d32bb769/independent_audit/fractional_weak_review.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3d6f7a072d5e489eb5a0bdc4d32bb769/independent_audit/outcome_dag_review.md
---

# R-3d6f 分数负载弱桥与证人 DAG 的独立审查

## 四主题完整 SPE 族

独立脚本只用 `fractions.Fraction` 和标准库，展开四类单位客户：\(m-1\) 个只喜欢 A，1 个只喜欢 Q，1 个喜欢 A,D，\(m(m-1)\) 个喜欢 B,Q,D。总数为 \(m^2+1\)。全历史策略由两个资源奖金子博弈的有限逆向归纳 \(\beta(r,q,e)\) 生成：全 B 历史在末位选 A，其余历史按 \(\beta\) 选 Q/D。审查逐一核对全部有序历史、所有动作和真实后继，未把计数策略当作一般 SPE 假设。

对每个整数 \(m=2,\ldots,7\)，`audit_fractional_family.py` 的报告给
\[
W=m^2,\qquad \operatorname{OPT}_m=m^2+1,
\]
并逐历史最小 SPE slack 为0。固定实际终局的 \(\alpha=(m-1)/m\) 查询值中，最大值 \(M\) 使
\[
\left(m-	frac12\right)M-W
=\frac{m^3-4m^2+3m-1}{2(m^2-m+1)}.
\]
因此对所有 \(m\ge4\) 该固定实际缩放负载弱桥严格失败。它不是 Q-CAG-HALF 反例：\(2W-\operatorname{OPT}=m^2-1>0\)。真正静态安全值可取合法 B 重复列作上界，因而该失败只针对实际缩放接口。

## 独立 m=4 定义级审计

`audit_fractional_weak.py` 不导入 CAG 模型、规范求解器或发现器。它把 17 名单位客户逐个展开，要求动作映射恰覆盖 \(1+4+16+64=85\) 个有序决策节点，并对每节点四个动作沿同一完整策略重算分数收益。全部255项非自身比较通过，最小 slack 为0；策略路径为 \((B,B,B,A)\)，玩家收益全4，\(W=16\)、\(\operatorname{OPT}_4=17\)。查询值
\[
(g(A),g(B),g(Q),g(D))=(16/7,48/13,61/13,388/91),
\]
所以 \(M=61/13\)，弱桥差
\[
(4-	frac12)M-W=11/26>0.
\]
审计另核零客户边界、缺少一个历史节点会被拒绝，以及全部256个比较主题元组的逐客户覆盖代数。它明确说明辅助桥失败不转化为half失败。

## 证人 DAG 的独立范围

`outcome_dag_review.md` 审查固定根终局证人集 \(Y(k)\) 的必要/充分约束：每个目标叶选择一个可行动作保持到子证人集；每个偏离动作选一个惩罚证人并以共同阈值比较收益；同计数不同有序历史在展开时保持独立。按剩余人数归纳，这些约束可逐有序历史展开为完整纯 SPE；反向从完整 SPE 终局集合选择最小收益惩罚证人即得约束。这个等价性只针对固定 \((p,m)\)、客户重数和根终局证人，不认证 MILP 浮点全局最优。

独立 `fractional_family_review.md` 将该族与既有“实际均匀缩放负载的弱付款桥”及“分数负载四主题族的全历史核验”逐项比较。它确认无限族解析最优性来自 \(\beta\) 的两资源逆向归纳，有限 JSON 只承担实现回归；不把有限 m=2..7 输出冒充一般证明，也不把 R-3d6f 的证人 DAG 审查改成 half 定理。

## 处置边界

这七源新增的是独立定义级重放、精确公式回归和 witness-DAG 量词审查；主反例和计算对象仍保留原稳定身份。该对象不重复声称 13 人精确税桥反例，也不把真实静态安全值聚合桥一起否定。后续若使用 DAG 编译器，必须分别给出整数客户输入、完整历史策略和 exact dual/optimality 证据，不能只凭浮点 MILP 或候选证人集升级结论。
