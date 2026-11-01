---
id: "customer-attraction/frequency-two-client-quadratic-fresh-safety-boundary"
kind: "candidate"
type_tag: "候选"
title: "频率二客户编译与二次 fresh 安全边界"
status: "restricted-representation-candidate"
truth_status: "conditional-candidate-with-finite-regression; fresh-floor-open"
summary: "在对称有理二次 fresh 辅助博弈与频率二客户 CAG 的受限编译中，记录高私有偏置、重复 old 前缀排除、theta 迁移和有限回归安全边界；不证明 fresh 逐人保底，也不构成六人半覆盖反例。"
source_refs:
  - "clean:9323c104d32cc08cc3c3"
related_objects:
  - "customer-attraction/symmetric-quadratic-fresh-individual-floor-candidate"
  - "customer-attraction/general-half"
evidence_refs:
  - "../../tools/evidence/r3d6f-quadratic-graph-compiler-20261101/README.md"
---

## 受限对象

源文件的承重范围是给定人数、对称有理二次参数与全部有序历史量词下的频率二客户编译：高私有偏置排除旧行动，fresh 辅助 SPE 的合法路径映射到 CAG，且在 distinct 终局中满足
\[
u_a=B+v_a,\qquad \theta_{CAG}=B+\theta_{fresh}.
\]
这是一项表示候选，不是无条件定理；fresh 辅助博弈的逐人静态保底 `theta_fresh` 仍开放。

编译器代码将有理系数转换为整数单位客户并执行有限 ExactSPESolver/证书比较。其高私有偏置给出 `OPT<2W` 的安全边界，因此该路线不能直接制造六人 Q-CAG-HALF 反例，也不能替代完整历史、重复前缀和离轨动作的逐式证明。

## 有限证据与边界

独立审计源 `79d1d48e3736cc7459d5`（SHA-256 `faae2d4c12b407eb8ce73e90123b4c965a1498c4f8827c635f532268a1ff9d2a`）报告 2288 个输入、4041 条有序路径、8861 个末前缀、13566 个子博弈和 23523 个证书历史通过。这只支持列明有限域的一致性；不证明任意有理系数、任意人数、fresh 保底猜想或一般 Q-CAG-HALF。

后续接续应分别读取 fresh 候选、编译器代码和审计 JSON，保留候选、有限回归与一般开放问题的层级。
