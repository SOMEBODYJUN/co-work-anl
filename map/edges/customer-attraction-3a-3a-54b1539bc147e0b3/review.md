# Boss3 fresh Solver：单玩家边界修订与14核心复核

任务 `boss3-single-player-boundary-repair-671659461d75219b`（stage 3A，owner observed `Boss2`）替代 `boss4-source-clarification-repair-repair-eb9c65b4dae79501`。本轮按 ordered passes 完成：

1. **身份与版本 pass**：读当前任务、前一任务/receipt、旧六条边、旧 read-ledger/review、registry 与 AGENTS；核对 18 个输入 pin。唯一变化是 `CA-DISJOINT-MAXIMA-2M1` 从旧 pin `d0ea4ff6…` 更新到当前 registry v6 pin `94b1a0b0…`，正文由旧 SHA `73ee40eb…` 变为当前 `0c003387…`。其余 17 个对象 pin 和 34 个未变历史来源均一致。
2. **正文 pass**：完整读当前不交极大正文（269 行）、共同目录模型、奇偶迁移、最优遗漏证书、唯一最优反例、同枝审计/引理、自由源审计/引理；按顺序读静态安全正文第1、4—6、8节。
3. **关系 pass**：复核旧六条边的 source/target、ALL 前提、量词、真实后继与证据；证明链保留为 3 条 whole logical relations、1 条 logical contribution、2 条有限/context checks。
4. **边界 pass**：重新检查 m=1、共同核 C、极大残余覆盖、实际前缀 L、signed→uniform、有限审计与来源未评估状态；只做最小边界修正，不扩张开放结论。
5. **交付 pass**：写入本任务六条替代边、coverage 草稿、read-ledger、review 与 receipt；未改队列状态、未执行 Git commit/push。

## 当前 v6 的最小数学修订

当前正文仍证明：在共同核 `K`、`C=|K|` 且不同包含极大残余覆盖两两不交时，每个完整纯 SPE 的每个有序历史均选极大花瓣；极大花瓣计数为 singleton PNE；
\[
\operatorname{OPT}_m\le C+(2-1/m)(W-C)\le(2-1/m)W.
\]
阈值席位引理、单资源严格降低、严格子花瓣动态删除以及 DM 福利/锐性推导均未改变。`m=1` 的正确边界是：任意有限目录由唯一提供者选真实最大覆盖主题，故 `W=OPT_1`；“只有一个覆盖集合”只属于 `m=1` 的特定锐性构造，不是一般一人目录假设。该最小修正已反映在当前 edge 条件与 endpoint pin。

由 DM 与同一目录静态锐等式 `OPT_n=(2n-1)v_n` 只能得到总福利贡献
\[W\ge [nOPT_n+(n-1)C]/(2n-1)=nv_n+(n-1)C/(2n-1)\ge nv_n,\]
不能推出任意实际 SPE 前缀嵌入 S2 唯一负载 `L`。只有在同一完整 SPE 的实际前 `n-1` 个动作确实产生 `L` 时，静态唯一负载边才给末位 `v_n`、各前缀 `g=v_n`、每位收入至少 `v_n` 及 `W\ge nv_n`。

## 14 个核心对象的处置

| object | state | 已核实结果与边界 |
|---|---|---|
| `CA-DISJOINT-MAXIMA-2M1` | linked | v6 当前正文成立；新边 `b3r1-disjoint-maxima-static-sharp-welfare-contribution` 只贡献 DM→总福利。m=1 边界按上段修订。 |
| `M-7fa6f1e2b320459eac88c1c614c870b3` | isolated-after-review | tau6 13 原子只否定命名 44 行的非负组合；无已证包含桥，不反合法六人 SPE、half 或一般信用。 |
| `customer-attraction/eighteen-topic-materialized-three-player-credibility-diagnostic` | isolated-after-review | CDE/查询尾真实偏离排除保持；计数统一只穷 `Ω_M`，不排 `Ω_H`；五槽并集非 `OPT_3`。 |
| `customer-attraction/closeout-22932a6dc419ad09ee8817f1` | isolated-after-review | 21 个 SPE 与 v2 重入行只给有限/context checks，不推出全参数遗漏耦合。新边 `b3r1-common-credit-audit-checks-sharp-interface` 仅核接口。 |
| `B8-PURE-MENU-CONVEX-CUT-NO-v1` | isolated-after-review | 30 客户纯/混合最小利润差 `1/10`，反“先凸纯菜单再截门槛无损”；不反统一末层、纯 BI 或根 half。 |
| `customer-attraction/three-player-count-uniform-outcome-last-layer-enumeration-and-skip-boundary` | isolated-after-review | 固定全局末层 `f(q)` 后的 `C_a,L_a,M_f` 枚举及 `None=skip` 成立；不给六人一般净化。 |
| `M-acf631e39b224ab3a96014370744b2fa` | linked | signed all-new 表迁移合法 uniform 单位客户，`m≥3` 完整 SPE，`W=OPT_m=2^(2m)-2^m`（可删空类型）。 |
| `customer-attraction/signed-credible-repair-direction-review-and-continuation-chronology` | isolated-after-review | `g_i=M_i-u_i(z)` 是退出缺陷，非 signed 负客户或驻留 Δ；不支付普遍目标族。 |
| `customer-attraction/parity-signed-uniform-all-new-policy` | linked | 同一完整动作表在 uniform 中逐历史保持 BR；不迁移 signed 矩或负类型。新边 `b3r1-signed-policy-transfers-to-uniform`。 |
| `customer-attraction/optimal-omission-unit-and-linear-certificates` | linked (conditional) | `f(k)=f(3)+α(k-3)`、`α≥0,f(3)≥0` 支持全参数遗漏族；来源 truth_status 仍 unassessed，故不升级为 unconditional。 |
| `customer-attraction/full-tail-stationary-additive-defect-sharp-envelope-and-four-label-realization` | isolated-after-review | `L_r(b)` 驻留形式包络与四标签取等不提供实际 `W` 钱包或跨枝支付。 |
| `customer-attraction/common-theme-price-cap-copy-punishment-elimination-redundancy` | isolated-after-review | 非负价消元由原主题帽推出；与 tau6 无证行族包含桥，不反真实后继 BR。 |
| `M-3b33bff2ccf041a9a82eb35664d00a69` | linked (conditional) | S2 唯一 `L` 加实际前缀嵌入条件给完整付款；DM 仅给总福利贡献。新边 `b3r1-static-unique-load-pays-actual-prefix` 与 DM 边并列。 |
| `customer-attraction/r868-parent-path-two-original-exact-audits` | isolated-after-review | 5184/1225 有限审计及自由源恒等式只做 checks；总体 `C-D=-31/24` 补偿正逐客债，不反 Mpath/half。 |

## 六条替代边与数学结果

- `b3r1-disjoint-maxima-static-sharp-welfare-contribution`：`CA-DISJOINT-MAXIMA-2M1` ⇒ `M-3b33…` 的条件总福利贡献；保 `C` 项、n=1 和共同目录边界。
- `b3r1-static-unique-load-pays-actual-prefix`：`M-921…` ⇒ `M-3b33…`，条件是静态锐等式、同一实际前缀负载恰为 `L`、末位为真实 BR。
- `b3r1-signed-policy-transfers-to-uniform`：形式 signed all-new 动作表转为合法 uniform 完整 SPE，保 `m≥3` 与 `2^(2m)-2^m` 覆盖。
- `b3r1-linear-certificates-support-unique-optimal-omission`：在源证书前提与 `truth_status=unassessed` 下条件推出 `N=27k-10,W=13k-4,OPT_2=14k-4,I=2,L=14k-6,E=13k-6`，`L-W=k-2`、`L-E=k`。
- `b3r1-common-credit-audit-checks-sharp-interface`：有限同枝审计核 `E=(Q-R)_+`、`E+G≤1-1/d≤1-1/m` 和容量边界；不升级全局遗漏耦合。
- `b3r1-free-source-audits-check-mismatch-identity`：有限 5184/1225 源/查询域核协方差恒等式与错配项；不升级 Mpath/half。

## 四个 shared/read endpoints

- `M-921cb4daa29e43c6b2816c1ec73720b5`：`linked-conditional`；S2 唯一负载与最坏回复身份只在实际前缀嵌入 `L` 条件下支付目标。
- `customer-attraction/unique-optimal-omission-existence-counterexample-family`：`linked-conditional`；由线性证书边承接，源 truth_status 未评估，保持条件。
- `customer-attraction/same-branch-deletion-refund-and-old-prefix-positive-loss-sharp-common-credit`：`context-linked`；只支撑有限同枝 E/G 审计。
- `customer-attraction/free-complete-menu-source-mismatch-and-conditional-reciprocal-debt`：`context-linked`；只支撑有限 5184/1225 源/查询恒等式。

## Open gaps, follow-up, overlap disposition

未关闭的数学边界保持开放：一般交叠极大目录的 half、实际 SPE 前缀是否总能嵌入静态唯一 `L`、最优遗漏源证书登记状态、同枝/自由源有限 checks 是否能推出全局遗漏耦合，以及 Mpath/half。它们是明确 open，不是身份或来源 needs-decision。

本任务没有可安全派生的具体 follow-up object pair；`follow_up_tasks=[]`。`M-3b33…` 与 `M-921…` 的 S2/实际前缀比较已在本包闭合，记入 `closed_overlaps`，不重复派工。旧六条边被本任务对应六条替代边取代，原 boss4 资产保留为历史，不再作为当前证据。

当前审计脚本路径在 clone 中不存在，故本 fresh worker 未重跑程序；有限数值与既有审计仅按已保存正文/证据复用，不把复用当成本轮新计算。
