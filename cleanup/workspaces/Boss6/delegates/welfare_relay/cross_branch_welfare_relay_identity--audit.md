---
id: cleanup/boss6/delegates/welfare-relay/cross-branch-identity-audit
kind: review
type_tag: 审查
title: 非根跨枝福利中继恒等式的独立清洗审查
status: local-independent-draft; exact-local-identity; half-open
summary: 清楚分开修正版非根恒等式、根特例、调和势删位比较、v1反例、全深度调和支付障碍与有限审计；不把任一本地关系升级为Q-CAG-HALF证明或反例。
source_refs:
  - clean:b243bc081ceffd6be46b:research/workspaces/customer-attraction/R-1740705e79f14baba6326b951a52152f/representation/cross_branch_welfare_relay_identity.md
  - clean:bfd05a8f1186e83d3c86:research/workspaces/customer-attraction/R-cef41b80a6e048b5a395b738d3b0b6e7/harmonic/relay_erratum.md
  - clean:254bc65952df60c93eeb:research/workspaces/customer-attraction/R-cef41b80a6e048b5a395b738d3b0b6e7/exchange/relay_correction_review.md
  - clean:39d6432f7dbc0270bd8f:research/workspaces/customer-attraction/R-2e5a6ea95aff4f4c89f75237a74ba472/relay_credit/full_depth_ledger_and_harmonic_obstruction.md
  - clean:f9696dd81c9a59d41582:research/workspaces/customer-attraction/R-2e5a6ea95aff4f4c89f75237a74ba472/relay_credit/full_depth_ledger_audit.json
  - clean:4a0a90aa4d26e578c914:research/workspaces/customer-attraction/R-2e5a6ea95aff4f4c89f75237a74ba472/relay_credit/audit_full_depth_ledger.py
  - clean:9d0174d0fc1435874500:research/workspaces/customer-attraction/R-1740705e79f14baba6326b951a52152f/route5a/sequential_deviation_share_lemma.md
---

# 清洗范围与来源身份

本稿实读 `clean show b243bc081ceffd6be46b` 的完整 3820B 冻结源。源路径为
`research/workspaces/customer-attraction/R-1740705e79f14baba6326b951a52152f/representation/cross_branch_welfare_relay_identity.md`，冻结提交为 `68fad804ec5946cb296f77dc5b336308a66abf12`，源 SHA-256 为
`9ad5e82e4b600bfae3dbdfac0b54867b0bcff13dd72302c7016b98640b3b5679`。

它明确记录 2026-10-24 勘误：初稿把只在根节点成立的 `ΔW ≤ ΔV` 误称为任意节点式；修订保留旧玩家最终利润项 `P`。本审查也通过 `clean show` 实读了勘误、独立定义级复核、全深度账本、有限审计 JSON/代码和顺序偏离份额账本，因而没有把文件名、摘要或旧图当作数学证据。

## 精确模型与量词

采用 CAG-MODEL：客户集 N 有限；共同主题目录 S ⊆ 2ᴺ 有限且非空；有 m ≥ 1 个单位权提供者，依次观察全部有序历史后各选一次主题。主题可重复，允许空主题、零客户、全部离轨历史和任意历史依赖平局。固定一份完整确定性纯策略 σ，并要求它在每个历史节点满足子博弈完美最优性。

对终局 z = (S₁,…,Sₘ)，令客户负载 cₓ(z) = #{j : x ∈ Sⱼ}，收益 uⱼ(z) = ∑ₓ∈Sⱼ 1/cₓ(z)，福利 W(z) = ∑ⱼuⱼ(z) = |∪ⱼSⱼ|。后一等式是单位客户分账恒等式；不使用静态 PNE、同计数历史同一后继或混合策略。

给定长度 i−1 的任意合法历史 h，当前人是 i，令 A* = σᵢ(h)。每个合法主题 T 定义强制分支 z(T)：在 h 后强制当前人选择 T，之后仍按同一完整 σ 的真实后继执行。故 z(T) 与 z(A*) 位于可能互斥的完整有序子树；后继不能冻结为原路径后缀。

定义

    V(T) = ∑ℓ>i uℓ(z(T))
    P(T) = ∑j<i uⱼ(z(T))
    W(z(T)) = P(T) + uᵢ(z(T)) + V(T)
    Γ(T) = uᵢ(z(A*)) − uᵢ(z(T)) ≥ 0

Γ(T) ≥ 0 是固定历史下真实一步偏离的 SPE 余量；它不是静态费用，也不是另一个历史的行。上述量词是：对任意有限 N、S、m，任意完整纯 SPE σ，任意合法 h、任意 T。

## 修正版恒等式（可证明的局部引理）

直接相减两枝的总利润守恒式得到

    ΔW = ΔV + ΔP − Γ,
    ΔX = X(T) − X(A*).

因此总是

    ΔW ≤ ΔV + ΔP.                              (R1-v2)

这是非根节点的正确式。过去提供者的行动在比较中固定，但其最终利润因未来负载变化而不固定。更精确地，旧的无 P 版本 ΔW ≤ ΔV 对这一个固定比较成立，当且仅当 ΔP ≤ Γ；ΔP ≤ 0 只是一个充分条件。根节点没有过去提供者，P(T) = P(A*) = 0，所以根上才自动恢复 ΔW ≤ ΔV。

旧玩家项还能逐客户写成真实有符号返还。令 bₓ 是 h 中的负载，令 nₓ(T)、nₓ(A*) 是两枝从当前人起的后续负载，则

    ΔP = ∑(x : bₓ>0) bₓ [ 1/(bₓ+nₓ(T)) − 1/(bₓ+nₓ(A*)) ].

释放旧客户上的拥挤会使该项为正；因此不能把它当作免费非负信用，也不能仅凭 SPE 假定其不正。

若改定义固定背景 h 下活跃玩家总利润 Rₕ(z) = W(z) − P(z) = uᵢ(z)+V(z)，则 ΔRₕ = ΔV − Γ ≤ ΔV 在任意节点都成立，但 Rₕ 不是目标覆盖福利 W。这只修复一个替代量，不闭合半覆盖。

## 调和势式 R2 的精确范围

令 Rosenthal 调和势 Φ(z) = ∑ₓ H_{cₓ(z)}，并令 z⁻ⁱ 表示从终局中删去当前提供者 i 的行动、保留该枝真实后继及所有已行动提供者的行动。逐枝恒等式

    uᵢ(z) = Φ(z) − Φ(z⁻ⁱ)

把 SPE 比较等价为

    Φ(z(T)) − Φ(z(A*))
      ≤ Φ(z(T)⁻ⁱ) − Φ(z(A*)⁻ⁱ).                 (R2)

R2 在任意节点成立；但删除当前人的势仍包含旧玩家和该枝后继，不能称作“仅后继势”。因此 R2 是删位势的 IC 比较，不是没有 P 项的福利式，也不能与错误的 v1 R1 互相替代。

## v1 错误的完整 SPE 见证

两位提供者、客户 a、b、c，目录含 A={a,b} 与 T={c}。策略在根选 A，在历史 (A) 和 (T) 后的末位都选 A。

在 (A) 后末位选 A 与 T 都给末位收益 1；在 (T) 后末位选 A 给 2，选 T 给 1/2，所以所有三个决策节点、所有合法动作比较都满足纯 SPE。于历史 h=(A) 比较规定 A 与强制 T：

    z(A)=(A,A), z(T)=(A,T)
    ΔW = 3−2 = 1,  ΔV = 0,  ΔP = 2−1 = 1,  Γ = 0.

旧 v1 会得到 1 ≤ 0，严格错误；R1-v2 取等。该实例实际 W=2、OPT₂=3，所以它是 v1 的定义级反例，不是 Q-CAG-HALF 反例。

## 与已读相关来源的比较

| 来源 | 实读内容与独有作用 | 语义处置 |
|---|---|---|
| `bfd05a8f1186e83d3c86` 勘误 | 逐式指出非根漏掉 P，给出同一两人三客户完整 SPE 反证；确认根特例及 R2 保留旧玩家 | 纠错与反例证据；不能把 v1 留作通用引理 |
| `254bc65952df60c93eeb` 独立复核 | 从收益守恒独立重构 ΔW=ΔP+ΔV−Γ，给出 ΔP≤Γ 的充要条件、活跃利润 Rₕ 和链接边界 | 定义级内部复核通过；无外审/新颖性认证 |
| `39d6432f7dbc0270bd8f` 全深度账本 | 任意深度三笔钱 T、O、Γ，全前缀望远镜，互斥分支错误计源，及 all-big/sharp 族的 m(Hₘ−1) 费用障碍 | 独有的全深度支付障碍；源文自称工作备份、未独立审查，保留为障碍而非定理升级 |
| `f9696dd81c9a59d41582` 有理审计 JSON | m=2..6 全历史 10213 个节点、60276 个动作比较；m=2..7 共 5912 个最优排列；公式检查至 m=80；任意策略代数 60 例/5678 边，含空主题和零客户但明确不声称 SPE | 有限回归证据；不能替代全称证明 |
| `4a0a90aa4d26e578c914` 审计代码 | 独立标准库 Fraction，重算收益、Γ、尾项、旧项及恒等式；未导入现有 SPE 求解器 | 可复现实验入口；运行范围按 JSON，不能扩成一般搜索 |
| `9d0174d0fc1435874500` 顺序偏离份额账本 | L1–L4 控制实际路径单个偏离者的未覆盖客户份额，保留真实后继；明确最坏分母聚合不足、跨枝信用未闭合及旧算术跳步修正 | 与 R1-v2 互补的局部引理；不提供共同跨枝支付 |

我把 `clean show 4a0a90aa4d26e578c914` 导出的标准库 Fraction 审计脚本在本地临时文件中重放；输出 `all_exact_checks_passed`，并复现 JSON 的 10213 个全历史节点、60276 个动作比较、5912 个最优排列、m≤80 公式检查和 60 例/5678 边任意策略代数范围。临时脚本和输出已删除；这次重放只确认冻结有限证据，没有扩大其数学量词。

当前清洗快照的治理记录还把 `CA-CROSS-BRANCH-RELAY-v1` 标为 FALSE，把 `CA-CROSS-BRANCH-RELAY-v2` 保留为精确节点式；当前 Q-CAG-HALF 量词仍是任意有限共同目录、任意人数、任意完整历史纯 SPE，状态 OPEN。该治理记录不是本源的证明替代，但与上述实读范围一致。

## 结论、分类与推荐去向

1. **证明/引理（局部）**：R1-v2 的 ΔW=ΔV+ΔP−Γ、根 P=0 特例、ΔP≤Γ 的固定比较条件，以及 R2，均由收益守恒、SPE 一步最优性和势分解直接证明。量词为任意有限 CAG-MODEL、任意完整纯 SPE、任意节点/动作比较。
2. **反例/纠错（v1）**：两人三客户的完整 SPE 反驳无条件非根 ΔW≤ΔV。它只否定 v1 接口，不否定半覆盖目标。
3. **障碍（支付模板）**：全深度账本的互斥子树重复计费和 sharp 族 m(Hₘ−1) 费用，排除“沿一条最优前缀把所有真实后继/旧返还统一由实际 W 支付”的充分模板；不排除任何带共同实际 source 的新流，也不构造低福利 SPE。
4. **有限证据**：JSON/代码只支持列明的有限回归和代数一致性；含空主题、零客户的任意策略样本不宣称 SPE。
5. **未闭合义务**：若要推出 2W≥OPTₘ，还需在互斥真实后继子树间建立共同支付/边平衡，并逐枝结算有符号 ΔP 与返还；不能把 ΔP 丢掉，不能把 R2 当纯后继福利式，也不能把 L1–L4 的单枝份额直接求和。

推荐保留原冻结源，另在正式存档拆为两个对象：

- `archives/customer-attraction/state/引理/非根跨枝福利中继恒等式--引理.md`：仅承载模型、量词、R1-v2、根特例、R2 和 Rₕ 说明；
- `archives/customer-attraction/state/障碍/跨枝共同付款与调和全深度支付障碍--障碍.md`：承载 v1 两人三客户反例、全深度账本/有限审计范围及未付义务。

本文件是 Boss6 delegate 的独立工作区审查稿，不修改上述 canonical 路径，不执行 Git、clean done 或远端声明。
