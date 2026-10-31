---
id: "unrelated-machines/seven-state-and-gate-localizer-author-read-after-20261031"
kind: "review"
type_tag: "审查"
title: "七态 AND endpoint 与二次 localizer 作者 read-after 审查"
status: "integrated-narrow-obstruction"
truth_status: "author-read-after-consistent-with-exact-first"
review_level: "full-source-read-and-cross-object-comparison"
summary: "作者 Proof read-after 逐式确认七态原星中的 degree-two null vector、degree-three 支付、次数四 Boolean 约化及指定二次 localizer 的负值。该页只保留忠实 AND 端点与基础五阶矩合同同时保留时的窄障碍，不升级为一般非线性 owner 定理、一般 unrelated-machines gap 或 hardness。"
source_refs:
  - "source:7ccd86160f25544a1e74:history/source/notes/unrelated_machines/sol_seven_state_and_gate_localizer_obstruction_author_read_after.md"
legacy_ids:
  - "UM-SEVEN-STATE-AND-LOCALIZER-AUTHOR-READ-AFTER-v1"
related_objects:
  - "unrelated-machines/seven-state-star-global-quadratic-audit-scope-review"
  - "unrelated-machines/seven-state-affine-boolean-owner-boundary-author-proof-v1"
---

# 1. 来源身份与 read-after 时序

`clean show` 导出的来源 `7ccd86160f25544a1e74` 为
`history/source/notes/unrelated_machines/sol_seven_state_and_gate_localizer_obstruction_author_read_after.md`，2,158 bytes，SHA-256 `8fbf850ba8c91df530c2c55f28e990a230b87749e091700b2b91e554a5777cbb`。本页逐字读取并保存原文到
`archives/unrelated-machines/tools/evidence/seven-state-gate-localizer-author-read-after-20261031/original/`。

该文本明确是在 root 先完整阅读旧 Exact-first 后才读取作者 Proof 的 read-after；作者 Proof 原对象为 3,766 bytes、SHA-256 `6869558f8f155de15bc65f305ce0a3c5d42d76e84a936eb4fdfd5b7c90f29d75` 的 `sol_seven_state_and_gate_localizer_obstruction_author_proof_v1.md`。因此本页不是新的 blind review，也不把作者说明之外的软件结果写成已运行证据。

# 2. 固定七态背景与窄合同

对象是七态原星的固定参数背景：旧 Exact-first 已定义共同 M3、原 Boolean/one-hot identities、物理 `v` 负载和 degree-two null 关系。作者读后结论只针对一个真实新增 endpoint 被忠实写成

\[
X=C(1-Y_i)
\]

之类的 AND 依赖，并同时保留基础的 fifth moments、原 `v` load、全局 quadratic load 检验以及指定的二次 localizer。它不涉及非仿射或近似 AND、深层 shared-owner/common-law、改变基础矩或一般 schedule solver。

# 3. Degree-two null、degree-three 支付与负 localizer

令 `D=Z-CY_i`。作者逐式核对：`D` 是共同 M3 中的 degree-two null vector；先取 degree-three multiplier

\[
Q=g(H-h)^2
\]

支付 Boolean 约化 `Z^2\to Z`，总次数为五；再用 `D` 与 `Q` 的正交关系把该项消去，最后才在 base≤5 的真实 `P` 期望上取值。这个次序避免把 base-4 当作 base-5，也没有把记号多项式误当作新增 degree-one endpoint 或把 null 关系乘到超过合同的次数。

在七态期望中，唯一留下负项的是 `(C,H)=(1,d)` slice，精确值为

\[
-p(1-\eta)(d-h)^2<0.
\]

新增 job 的两个 private unit 端点都是真实原端点；每个 sample 仍完整执行，`v` 负载保持原值。因而这是指定 faithful-AND + fifth-moment + quadratic-load 接口的直接负 localizer，而不是删除端点或改变普通 eligibility 逻辑得到的伪反例。普通 eligibility 没有被偷偷当成 AND 约束。

# 4. 真实范围、已有对象与缺口

作者 read-after 与 Exact-first 顺序一致，未发现 standing fatal；它只禁止“忠实 AND 关系、基础 fifth moments、原 `v` 负载和全局 quadratic load 检验同时保留”的这一个接口族。它没有证明：

* 一般非线性依赖、近似 AND、不同基础矩或改变 extraction 后仍然失败；
* 所有物理 owner 的总 degree、深层 shared-owner/common-law 或多背景耦合的 impossibility；
* 一般 unrelated-machines 算法、near-two gap、SDP finder、source decoder、hardness 或新颖性。

该页与七态全局二次审计/root replay 的关系是分层的：有限 JSON 只核其明列的有限 PSD、秩、assignment 和输出字节范围；本页保留作者的代数推导与负 localizer 身份，不能把有限软件审计替代成任意参数的程序证明。与 affine Boolean owner boundary 作者 Proof 相邻但独立：前者分类 affine endpoints 与 unit-owner 边界，当前页研究忠实 AND 端点的更高次数 localizer 障碍。

# 5. 接续用途

若第三阶段要把该对象接入更强 SA3→canonical-SA1 桥，必须显式写出是否允许跨行 degree-3/5 moments、是否加入对 AND 端点的额外 consistency rows，以及是否改变 `v` load。只有在同一窄合同下，`-p(1-\eta)(d-h)^2` 才能作为负值证据；任何扩域或不同取点都应新建对象并重新证明量词。当前来源没有新软件运行，正式结论保持为七态 faithful-AND 二次 localizer 的范围性障碍。
