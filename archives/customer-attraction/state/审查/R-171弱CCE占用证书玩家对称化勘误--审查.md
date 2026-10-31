---
id: "customer-attraction/r171-weak-cce-occupancy-player-symmetrization-review"
kind: "review"
type_tag: "审查"
title: "R-171 弱 CCE 占用证书的玩家对称化勘误"
status: "finite-exact-audit-corrected-by-player-symmetrization"
truth_status: "aggregate-slack-certificate; symmetrized-CCE-witness; general-bridge-open"
review_level: "full-source-read-and-Fraction-quantity-audit"
scope: "Boss2 weak CCE three-state family and 57-case exact audit"
summary: "冻结报告的 Fraction 算术保持有效，但原有序混合只证明聚合偏离损失非负，不能直接称逐玩家 CCE。对玩家位置均匀对称化后得到同福利 CCE；花瓣标签对称不能替代玩家对称。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/continuation/independent/weak_cce_boss2_audit.json#source"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/continuation/independent/audit_weak_cce_boss2.py#source"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/continuation/independent/weak_cce_boss2_family.md#source"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R-171-independent-20261031/original/weak_cce_boss2_audit.json"
  - "archives/customer-attraction/tools/evidence/R-171-independent-20261031/original/audit_weak_cce_boss2.py"
  - "archives/customer-attraction/tools/evidence/R-171-independent-20261031/replay/weak_cce_boss2_audit.json"
related_objects:
  - "archives/customer-attraction/state/计算/R171弱CCE Boss2 独立逐人审计--计算.md"
  - "archives/customer-attraction/state/候选/较弱CCE福利桥的占用LP表示与边界--候选.md"
  - "archives/customer-attraction/state/反例/三人顺序SPE低于全部静态CCE福利--反例.md"
---

# 1. 量词修正

共同目录静态 CCE 的约束是：对每个终局分布 `\\mu`、每个玩家 `i` 和每个固定主题 `T`，

\\[
\\Delta_i^T(\\mu)=\\mathbb E_{s\\sim\\mu}[u_i(s)-u_i(T,s_{-i})]\\ge 0.
\\]

冻结程序输出的却是

\\[
A_T(\\mu)=\\sum_{i=1}^m\\Delta_i^T(\\mu)
 =\\mathbb E_\\mu\\left[W(s)-\\sum_i u_i(T,s_{-i})\\right].
\\]

`A_T\\ge0` 是必要的聚合约束；对玩家标签不对称的分布，它不蕴含每个 `\\Delta_i^T\\ge0`。因此报告中的 `status=passed` 和所有 `aggregate_slack` 非负，只能称为聚合审计，不能把原固定槽位支持直接称为 CCE。

# 2. 冻结范围与精确证据

源 `e659ae7cc2fe2ecebd70` 是 15,580 字节、SHA-256 `573b9a60f68308d65b31645d91c563d19698075770d7ccd95bc7d4c95e3adad9` 的报告；程序源 `6678221a19976d2929df` 是 2,760 字节、SHA-256 `b4ca4d0a38816d7a1eda83645aa85c6d91adc8125f910c5252711120b2ec41fe` 的 Fraction 审计。它检查 `m=2..12,K=2..6` 的 55 组及 `(53,53),(100,100)` 两组，共 57 组，并保留三状态族的有理权重与聚合 slack；它不求最小 CCE 福利，也不证明一般目录桥。

目录族有核心块 `A`（两客户）、块 `B`（`2(m-1)` 客户）和花瓣客户；主题为 `C=A`、`B`、`P_j=A\\cup\\{c_j\\}`。三状态固定槽位支持为 `P_0=(C,B,\\ldots,B)`、`P_1=(P_j,B,\\ldots,B)`、`P_2=(C,C,B,\\ldots,B)`，福利分别 `2m,2m+1,2m`。报告中的有限核验保持这些数值。

# 3. 三人两花瓣的失败与修复

在 `(m,K)=(3,2)`，冻结权重给出

\\[
\\mu=\\tfrac7{24}[C,B,B]+\\tfrac38[C,C,B]
 +\\tfrac16[P_1,B,B]+\\tfrac16[P_2,B,B].
\\]

逐玩家精确偏离损失为：

| `T` | `\\Delta_1^T` | `\\Delta_2^T` | `\\Delta_3^T` | `A_T` |
|---|---:|---:|---:|---:|
| `B` | `3/8` | `-3/8` | `0` | `0` |
| `C` | `1/3` | `5/8` | `15/8` | `17/6` |
| `P_1` | `-2/3` | `-7/24` | `23/24` | `0` |
| `P_2` | `-2/3` | `-7/24` | `23/24` | `0` |

所以原有序分布不是 CCE，尽管所有 `A_T` 都非负。这个修正是量词修正，不是对 Fraction 算术的否定。

令 `\\Pi` 在玩家位置的对称群 `S_m` 上均匀取值，并令 `\\bar\\mu` 为 `\\mu` 的玩家置换平均。由于客户吸引博弈对玩家标签对称，福利和每个聚合量 `A_T` 不变，而

\\[
\\Delta_i^T(\\bar\\mu)=\\frac1m A_T(\\mu)
\\qquad (i=1,\\ldots,m).
\\]

因此对称化后的分布才是 CCE，且期望福利保持 `2m+p_1`。花瓣标签的置换只处理主题同构，不能替代玩家位置的对称化；若目录没有花瓣同构，仍需逐个合法主题检查 `A_T`。

静态 PNE 单点 `P_1B^{m-1}` 则可直接逐玩家核验，因此它的 CCE 身份不依赖上述修复。两类证书必须分开。

# 4. 与占用 LP 和既有 CCE 反例的关系

对终局 `s` 和固定主题 `T`，令 `H_T(s)=\\sum_i u_i(T,s_{-i})`。客户负载为 `c` 时，该客户对 `H_T` 的贡献为 `m`（`c=0`）或 `(m+1)/(c+1)`（`c>0`）。所以 `A_T=W-H_T`，对任意 CCE 求和得到 `\\mathbb E H_T\\le\\mathbb E W`。

反向表示必须先做玩家对称化：若分布满足所有聚合约束，置换平均保持 `W` 与 `H_T`，并把每个玩家损失变成 `A_T/m`。这使按主题计数的有限 LP 精确刻画 CCE 的最小福利，但不意味着每个未对称原始分布都满足逐玩家约束。既有八客户和十三客户的静态 CCE 锐反例仍有效；它们有完整个体原始/对偶证书，本勘误不削弱也不扩大其量词。

弱 iid 福利桥、真实顺序后继的安全值、聚合 POOL 和六人 Q-CAG-HALF 仍保持独立身份与开放状态。有限 57 组核验只支持修正后的玩家对称 CCE 见证族，不是一般共同目录定理。

# 5. 处置

该报告、审计程序和已有 replay 均保留原字节。源版本语义处置为 `integrated`：报告接入本页和 R-171-independent 证据目录；原有 `R171弱CCE Boss2 独立逐人审计` 继续承载 Fraction 族校准。不得把 `aggregate_slack` 改名为逐玩家 slack，也不得将原固定槽位混合称 CCE。若后续扩展程序，应显式输出玩家置换或直接验证每个 `\\Delta_i^T`。
