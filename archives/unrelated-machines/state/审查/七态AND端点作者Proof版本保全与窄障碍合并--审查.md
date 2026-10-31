---
id: "unrelated-machines/seven-state-and-gate-localizer-author-proof-v1"
kind: "review"
type_tag: "审查"
title: "七态 AND 端点作者 Proof 版本保全与窄障碍合并"
status: "retained-and-integrated"
truth_status: "author-proof-read-and-cross-compared"
review_level: "full-source-read-and-cross-object-comparison"
summary: "完整读取作者 Proof 版本并保存冻结字节。其逐式证明与既有 Exact-first、作者 read-after 对象一致，新增内容仅是 Proof 版本的推导次序和物理读法；因此合并到既有 faithful-AND 二次 localizer 窄障碍，不升级为一般 unrelated-machines 不可能性。"
scope: "正偶 d,s；七态 P；新增 degree-one Z 的 faithful AND Z=CY_i；共同 M3、base≤5、原 v 负载与全部 degree-two load localizer 的窄合同"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_seven_state_and_gate_localizer_obstruction_author_proof_v1.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_seven_state_and_gate_localizer_obstruction_author_proof_v1.md"
related_objects:
  - "unrelated-machines/seven-state-and-gate-localizer-exact-first-20261031"
  - "unrelated-machines/seven-state-and-gate-localizer-exact-v1-review"
  - "unrelated-machines/seven-state-and-gate-localizer-author-read-after-20261031"
  - "unrelated-machines/seven-state-star-global-quadratic-local"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/seven-state-gate-localizer-author-proof-v1/original/sol_seven_state_and_gate_localizer_obstruction_author_proof_v1.md"
---

# 来源身份与字节保全

本次完整读取 clean source `35c3d73eecc8a450aedb`，路径为
`history/source/notes/unrelated_machines/sol_seven_state_and_gate_localizer_obstruction_author_proof_v1.md`，冻结 blob
`89a46a6fc91fa4774ff399938309934b7c6a4bec`，大小 3,766 bytes，源 SHA-256
`6869558f8f155de15bc65f305ce0a3c5d42d76e84a936eb4fdfd5b7c90f29d75`。原文已逐字保存到
`archives/unrelated-machines/tools/evidence/seven-state-gate-localizer-author-proof-v1/original/`。

文件标题为“七态原星的 AND 端点压缩：作者证明与次数核对”，ClaimVersion 为
`UM-SEVEN-STATE-STAR-AND-GATE-LOCALIZER-OBSTRUCTION-v1`。它明确把 Proof 与 Exact-only 分开冻结，并声明未运行程序。本页不是新的 Exact-first blind review；作者 Proof 的读后结论与已有
`七态AND端点二次localizer作者read-after审查--审查.md` 及 Exact-first 独立重构逐式一致。

# 1. 作者 Proof 的完整数学内容

取正偶数 `d,s`，满足 `2≤s≤d/2`，置

\[
\eta=s/d,qquad h=s/2,qquad T=1+\eta,qquad p=\eta^3/1000,
\]
\[
u_0=4p(1-\eta),qquad e=4/5-p-u_0.
\]

于是 `0<η≤1/2`、`1≤h≤d/4`、`p>0`、`e>0.79`。七态原星中 v 行的负载保持

\[
\operatorname{load}_v=C+H/d,qquad g=T-C-H/d.
\]

固定 `i∈[d]`，令 `Z` 为新增 degree-one 原 endpoint（或明确声明的 degree-one Boolean 坐标），并要求忠实关系

\[
G=Z-CY_i,qquad \widehat L(G^2)=0.
\]

`G` 的次数为二，是共同 `M3` 的零向量。作者 Proof 的关键是次数顺序：取

\[
q=Z(H-h),qquad Q=g(H-h)^2,quad \deg Q\le3.
\]

先用 `Z²=Z` 的 Boolean 等式（乘以次数三的 `Q`，总次数五），再用 `G` 与次数三 `Q` 的 PSD 正交性，得到

\[
\begin{aligned}
\widehat L(gq^2)
 &=\widehat L(gZ^2(H-h)^2)\\
 &=\widehat L(QZ)\\
 &=\widehat L(QCY_i).
\end{aligned}
\]

右端仅含 `C,Y` 且次数至多五，因此在 base≤5 匹配合同下可换成真实七态 law `P` 的期望。`C=0` 类别被因子消去；`C=1,H=0` 类因 `Y_i=0` 消去；`C=1,H=h` 类因 `(H-h)^2=0` 消去。唯一留下的是 `(C,H)=(1,d)`，其概率为 `p`、`g=η-1`、`Y_i=1`，所以

\[
\widehat L(gq^2)=p(\eta-1)(d-h)^2
 =-p(1-\eta)(d-h)^2<0.
\]

严格性对全部合法边界成立，包括 `d=4,s=2,h=1`；不需要 `h≥2`。因此若 v 行要求对全部全局次数不超过二的 `q` 都有非负二次负载局部化，该合同发生矛盾。

# 2. 物理读法与条件边界

作者 Proof 还给出一个合法的 ordinary-UM 读法：在基础普通星外新增一枚 unit job `K`，它仅能在两个新的 private 机器 `a,b` 上以处理时间一执行。保留原 assignment law `P`，当 `CY_i=1` 时把 `K` 放在 `a`，否则放在 `b`；令 `Z` 为其真实原端点指示。每个样本仍完整执行所有原 jobs，新机器负载至多一，`G=0` 点态成立，且所有 Boolean/one-hot 与共同矩来自真实 assignment law。

这说明忠实 AND 可以具有原 job 语义，但不是 ordinary UM eligibility 逻辑自动强制的 AND。新增 job 的物理读法没有产生 near-two gap：原星仍存在峰值一的完整调度，`K` 也可放在任一 private 端。负值只排除同时保留以下接口的候选：

1. 原七态基础 `P` 的 base≤5 矩匹配；
2. 新 endpoint 的 degree-one Boolean/one-hot 等式；
3. 忠实 `Z=CY_i` Gram 零关系；
4. 原 v 负载公式 `C+H/d`；
5. v 行全部 degree-two 全局负载 localizer 非负。

若改变基础第五次矩、只给一阶边际、把 `CY_i` 误当 degree-one、改变原 v 负载、采用近似或其他非线性 AND、或改变 localizer 次数，作者 Proof 不能直接套用。

# 3. 与既有对象的比较和去重判断

* **Exact-first 独立重构：** 先行独立页已从 Exact-only 重新推导相同的 `G`、`Q` 和负值；它保留未读作者 Proof 的时序。当前来源不是 Exact-first 的新独立证据。
* **Exact 量词与障碍审查：** 既有页记录了 statement-only Exact 的 degree-one `Z`、base≤5、次数五 localizer 和普通 job 读法；作者 Proof 的逐式推导与其完全吻合。
* **作者 read-after：** 既有页是在读取 Exact-first 后再读作者 Proof 的 read-after；它已经记录作者 Proof 的 3,766 bytes、同一 hash、同一负值和窄范围。当前来源的独有内容是直接作者 Proof 字节和“先 Boolean、再 M3 正交”的证明顺序，故保留为证据并合并到同一对象链，不另立一般定理。
* **七态原星全局二次负载局部核：** 原星的正向对象不含新 faithful AND endpoint；本来源不否定原始真实 assignment law，也不把两个对象合并为“所有延拓失败”。
* **Affine Boolean owner：** affine owner 使用 base≤4 与 affine candidates；本来源使用 base≤5、degree-one `Z=CY_i` 和 degree-five localizer，必须保持独立身份。

# 4. 结论级别与接续

本来源应处置为 `retained`/`integrated`（原字节保全，数学内容合并到已有 faithful-AND 窄障碍链），而不是 `duplicate` 后删除：作者 Proof 与 Exact、作者 read-after 的来源角色和阅读时序不同，且 Proof 版本提供明确的次数核对。它也不应被标为 `needs-decision`，因为条件、证明和缺口均已完整读取并与既有对象交叉核对。

安全可引用的结论是：在上述正偶参数和五项接口前提下，`q=Z(H-h)` 给出精确负值 `-p(1-η)(d-h)^2`，所以这些条件不能同时与 v 行全部二次 localizer 非负共存。

不得从本来源推出一般非线性 extension 不可能、所有 shared-owner/common-law 都失败、near-two gap、SDP finder、调度算法、hardness、source decoder 或外部新颖性。后续若扩展基础矩、接线、支持或 localizer，必须另建对象并重新证明量词。
