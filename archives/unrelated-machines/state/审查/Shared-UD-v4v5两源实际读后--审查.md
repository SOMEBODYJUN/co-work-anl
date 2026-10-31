---
id: "unrelated-machines/shared-ud-v4-v5-review-two-sources"
kind: "review"
type_tag: "审查"
title: "Shared-UD v4/v5 两源实际读后"
status: "typed-domain-read-with-algorithm-boundaries"
summary: "两份 review 源分别核对 shared-UD 单状态 tiny-home v4 的 k² 曲率/FW 与共同叶 matching、以及 v5 的 O(1/k) 相对曲率实际分配算法。两套算法和读序保持独立，均限于 typed domain：不同 homes、own-unit helpers、shared normalized B fallback、k=1 无 tiny、k≥2 ν 上界；不外推为一般 UM。"
source_refs:
  - "clean:2249ff297d19a6102fb3"
  - "clean:9c81a5cfa8b0a07f0737"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/shared_ud_tiny_home_potential_rounding_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/shared_ud_relative_curvature_rounding_review.md"
---

# 来源与版本范围

`2249ff297d19a6102fb3`（SHA `497389548402aeda76da4aa1eba680cdbed6880ffaf97fa05ab88000ac7ecd13`）只审 shared-UD v4 新增 §12–20；旧 382 行前缀与 v1/v3 原证明只按 hash/关联票，软件仅交换引理有限校准。`9c81a5cfa8b0a07f0737`（SHA `92ec604d08686956a0aa6feef3ea086ecf1881db8d7a6e2bb64cec6bca35654a`）只审 v5 新增 §21–27；旧 v4 不升级，新增 O(1/k) 实际 allocation 与 relative-curvature 后置攻击。两源均 clean show 全文实读，原件/manifest 在 `archives/unrelated-machines/tools/evidence/shared-ud-review-20261031/`，receipt 草稿在 `cleanup/workspaces/Boss2/shared-ud-review-receipts-20261031.json`。

# 1. 共同 typed domain

外层是 k 个 single-state outers，homes 全局互异；每 outer 有 own-unit helpers，B 上任意 normalized fallback，共同一份真实 leaf matching。B-only 叶需满足 ε=15/16 whole-menu threshold-UD；所有原 zero/indexed/inactive jobs、无限资格和大分母都显式编译。k=1 不要求 tiny，k≥2 要求 vacancy/leaf matching 参数 `ν≤1/(16384k²)`（v5 放宽到 `1/(1024k)` 的对应合同，具体常数按版本保留）；域内 OPT≥1，输出是全部原 jobs 的实际 assignment，目标 ratio 19/10。不能改成一般 UM 的 OPT=0 或任意矩阵。

v4 与 v5 都同时保留 profile/潜势算法和 actual-allocation 算法，不能用一套算法的正确性代替另一套：v4 的 primal smooth-deficit + stable optimal-face coupling + k² 曲率 + rational FW + common integer prefix-flow；v5 的单 helper matroid greedy、weighted relative-curvature payments、same-outer impact 控制、共同叶 matching 与全 jobs 回填。

# 2. v4 k² tiny-home 势与 FAIL 量词

v4 的主桥是 `OPT=2−V`，其中 V 为共享叶 matching 值；无全叶 matching 时 actual `V<15/16`。k≥2 的 tiny vacancy 令累计 curvature 可付款，FW 定步有理迭代在固定 optimal face 上逼出 helper/own home 的共同整数 prefix-flow。成功时 Good helpers、own homes 与共同叶 matching 质量至少 1/10，selectors/incidences 全部实际完成；若 `V≤18/19`，基线给 ratio 1.9。主算法的 exact profile optimum 只作分析，不能假设免费 oracle。

v4 的另一 Exact-first 算法以 matroid greedy 候选、weighted-rank comparison `reference≤2current+Σgain`、平方缺口势直接推进各 outer≥19/100；其 FAIL `V≤18/19` 与主 FW/coupling 算法分开审查。k=1 使用 weighted-rank greedy 的 1/2 benchmark，不调用 tiny 条件。

软件范围严格有限：规范交换引理程序只枚举小资源/小 outer 的 ownership，seed 240 例和有限 weight 组合；它不实现 profile 势、FW、prefix-flow 或全原 jobs，不能将软件 PASS 写成 v4 全称算法验证。v4 局限仍是多-state outers、重 homes、任意 non-UD leaves 和一般 UM。

# 3. v5 O(1/k) relative-curvature actual allocation

v5 在同一 typed domain 内把 k≥2 vacancy 条件调整到 `ν≤1/(1024k)` 版本，k=1 仍无 tiny。单 helper 候选用 `I_-j` 加 state 的 matroid greedy；对任意 optimal fractional face，reference/current 比满足 `h·reference≤2h·current+Σδ`，其余 helpers 的 weighted 丢失由新 j 贡献支付。same-outer weighted 影响、所有跨-cap 余项、倒数势 `φ`、终点 S 和等号 FAIL 均被逐项核对；共同叶 matching 保持 all outer 实际资源独立，selectors/incidences 全回填。

若 actual V>18/19 且某 terminal `L_i<19/100`，曲率与 Cauchy 给 reference gap 系数 `9657/36100`，大于误差付款上界 `698/2851`；因此无可付款进展时是 sound FAIL `V≤18/19`，基线 ratio 1.9。固定 `1/(100N)` 步幅与有理 bitset 重算给总迭代次数 `O(k²N)`（k=1 为 `O(N)`），递归分母不增长，输出全 jobs/容量检查按显式 bit length 多项式。该数学合同未配端到端软件执行；v4 交换 audit 不能转作 v5 实现证明。

v5 另有 actual-allocation 独立算法和作者 read-after：它不借 v4 profile/FW oracle，逐 outer 直接构造实际 I、Good helpers/home 和共同叶分配；后置审查逐核 same-outer、跨 cap、O(1/k) payment、终点/FAIL 等号。读后无 standing fatal 只适用于 typed domain。

# 4. 算法身份、依赖与未解范围

两版都基于标准 matroid rank、submodular greedy、basis exchange、flow integrality、FW 有理迭代；这些工具非新颖性认证。可复用增量是：在 shared fallback 和变量 k 下保持同一真实 leaf matching，并把每 outer 的 helper 进展与共同 actual target 绑定；v5 进一步付款相对曲率余项。此类结构仍要求全域 UD、single-state、互异 homes 和 B-only threshold-UD，不能替换多-state/共享 home/任意 non-UD。

来源中 `P≠NP` 仅排 typed-domain 的 fixed γ NP source（YES actualOPT≤1、NO≥2−γ）；不排一般 normalized menu 或一般 UM。没有外审、全球新颖性或独立论文价值认证。v4/v5 都未给一般 UM→Q reduction、跨域 decoder 或主目标统一近二正反结论。

# 5. 与已有 shared-UD 正文和本轮前批关系

本轮此前已实读并归档 shared-UD v4 三份 Exact/Proof/actual-read 来源，以及 relative-curvature O(1/k) 三源 Exact/Proof/独立/作者读后。本两源 review 的独有处置是按 v4/v5 版本只读范围，核对两套算法不得互代、v4/v5 vacancy 常数和 k=1 边界、sound FAIL 的精确量词、有限交换软件不覆盖全算法。它们与既有正文互相支撑但不制造新主命题对象。

处置为 `typed-domain-read-with-algorithm-boundaries`；引用时必须注明 v4 k² 或 v5 O(1/k) 版本、single-state/UD/互异 home/threshold-UD 前提、实际 allocation 与 profile/FW 的身份、软件仅有限校准及一般 UM 未解。
