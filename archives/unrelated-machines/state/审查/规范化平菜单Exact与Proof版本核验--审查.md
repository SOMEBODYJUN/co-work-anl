---
id: "unrelated-machines/normalized-menu-exact-proof-version-audit"
kind: "review"
type_tag: "审查"
title: "规范化平菜单 Exact v1/v2/v3 与 Proof v1/v3 的版本核验"
status: "internally-reviewed"
summary: "逐篇读取五份 Exact/Proof 冻结源，记录v1到v3的新增承重内容、Proof步骤、版本依赖和未完成外推；不把过程版本重复计为多个定理。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/normalized_menu_full_support_lp_preservation_exact_v1.md#全文"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/normalized_menu_full_support_lp_preservation_exact_v2.md#全文"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/normalized_menu_full_support_lp_preservation_exact_v3.md#全文"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/normalized_menu_full_support_lp_preservation_proof_v1.md#全文"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/normalized_menu_full_support_lp_preservation_proof_v3.md#全文"
---

# 规范化平菜单 Exact v1/v2/v3 与 Proof v1/v3 的版本核验

## 实际读取与稳定身份

本批逐篇读取五份冻结源，而不是只看文件名或前一批审查摘要。冻结树记录的内容 SHA-256 为：

| 源 | SHA-256 | 本版独有承重内容 |
|---|---|---|
| Exact v1 | `9fd644392d624431050d0d1489bea4464284a1594f7868bf4a3667641233a763` | normalized menu、FSLP、tree/port-path、state-dummy SC、row≤3/degree≤9 与 (Q_D) |
| Exact v2 | `0176af114d1323cb963c98481533a41d35d50d6bd5f81c5dd10094ffd27c9c8b` | 通用有限 additive SC 的 unit-helper 路径；actual/CONFIG 正阈值域；最终 degree≤3 |
| Exact v3 | `6a31b2699304f18847d1226305fa72c8f56998a2930f846a3467ca45309194bf` | restricted-flat UM machine CONFIG(1) 与 FSLP 的精确桥，并将 v2 路径并入成熟合同 |
| Proof v1 | `7f8bd074a0f137dd4c75260fd7c8bd4023bcd24d5bd96042b56b46c552e47740` | v1 的 tree、port-path、state-dummy、实际值与 (Q_D) 的逐步证明；未证明 flat CONFIG 桥 |
| Proof v3 | `fb652fd0a1fd71d01ec6297fd86dfb56bbaf06fa55b1acbb8440ca06e103c930` | 自足证明 flat CONFIG 桥、SC path 及 v3 合成；明确未制作独立 v2 Proof |

五份源均注明作者 rainbow、日期 2026-10-18，并保留外部 scratch 生成历史。当前正文把 v3 作为稳定统一对象，把 v1/v2 作为保留版本和新增内容来源；不因版本数量增加而复制定理或提升外审状态。

## Exact 三版本的对象演进

### v1：正支撑分数合同与 degree≤9 像

Exact v1 规定每个 group 有非空 indexed states，每个 state 的非负二进制有理权总和为一，资源标签在 state 内互异；零项、重复 indexed states、unused resources 允许。FSLP 只按 (p>0) 的正支撑指示计容量，零权原 UM jobs 仍留在完整实际矩阵。

它冻结了 binary selector-tree (T) 和 menu-level port-path (D)，并以 (N=D\circ T) 得到每 group 至多三 states、每 resource 至多跨三 groups。给定显式有理 FSLP 证书，T、D、N 可双向转换。state-dummy SC 每 state 一个 agent、每 group (K-1) 个 unit dummy；v1 声称 FSLP 与 SC CONFIG(1) 等价，SC CONFIG 最高阈值不超过一，实际值桥仍是另一个合同。

v1 的 (Q_D) 族有 main state 权 (1/D)、helper 二选 (g_{a,j}/A_a)，满足实际值 (1/D) 及 FSLP 可行；经 N 与 state-dummy 得 row≤3、item 正度≤9 的 CONFIG=1/actual=1/D 间隙。v1 明确它不是 actual-OPT≥1 promise 的反例，也不含一般 UM hardness 或 near-two 结论。

### v2：通用 SC unit-helper 路径与 degree≤3

v2 保留 v1 所有对象和 exact contract，新增适用于任意非空 old agents、有限（可空）items、非负二进制有理 additive values 的 (P_{SC})。对 item (u) 的正 owner (i_1,\ldots,i_d) 建 d 个 owner copies，加入 d−1 个相邻 unit helper agents；d=0 保留 unused item，d=1 无 helper。

实际 allocation 正向只对目标 (0<v\le1) 保证：old owner 取自己的 copy，按 hole 让 helper 取其它相邻 copy；逆向对任意 (v>0) 成立，即使 helper 同时取两份 copy 也只能加强占用计数。因此 old OPT≤1 时 actual optimum 相等，old OPT>1 不作保持声明，old OPT=0 单独以正阈值/空端点处理。

有限 SC CONFIG 的正向量词是 (0<t\le1)，逆向是任意 (t>0)。逆向只需 helper 配置非空，不把双 copy 偷剪成 singleton；若 old 最高有限阈值≤1，则新旧最高阈值相等，阈值零用 empty configurations 另证。每 old agent rowtotal 不变、helper rowtotal=2、每个新 item 正度≤3。v2 还明确 BCG2009 的相邻 dummy 是已知装置，不会把一般高 rowtotal SC 自动归约到 row≤3。

### v3：restricted-flat machine CONFIG(1) 桥

v3 在 v1 的严格 normalized 域中补上完整 flat UM 的新对象。每 state 有 selector (J_g)、private machine (M_{gs})、incidence jobs (I_{gsu})；正关联的 resource endpoint 时间为一、private 时间为正，零 private incidence 仍是原 job。新 Exact 声明：完整 restricted-flat UM machine CONFIG(1) 可行，当且仅当 FSLP 可行；给任一显式有限有理证书可确定性总位多项式互转。它只覆盖阈值一和这类两端结构，不外推一般 UM、任意阈值、给定证书全部边际或未知指数配置表。

v3 同时把 v2 的 (P_{SC}) 合入成熟组合 (J(Q)=P_{SC}(SC(N(Q))))。由于 N 后 old SC row≤3 且 actual/CONFIG 最高值≤1，最终 row≤3、item 正度≤3。v3 的剩余问题仍是 actual OPT≥1 promise 下寻找固定正常数 minutility 的确定性位多项式算法；CONFIG 障碍不解决该 promise。

## Proof v1：已直接核对的证明链

Proof v1 的正向 tree 令 (x_v) 为子树叶的旧 λ 总和；root child 概率为子树和，非 root internal/leaf 的 own 概率为 (1-x_v)，child/旧 state 概率为相应 (x)。每个 fresh own resource 的两端边缘和为一，旧正资源用量保持原 λ。

其 tree 反向从 root 发送一单位 flow；非 root 的 own-resource 容量给出 parent-child flow 加 own 概率不超过一，因此非 own 分支概率至少可承接 incoming flow。逐层分配到 leaves，得到叶质量总和一且每叶不超过目标旧 state 概率；直接取叶流作为旧 λ，原资源行不增。它显式处理 K=1 和 off-path 质量，不假设只有一条活路径。

Proof v1 的 port-path 正向用 hole 分布 π 控制每个 helper 两端 singleton 概率，helper 在 port i 的边际是 (1-π_i)，与旧正支撑 (x_i\leπ_i) 相加不超过一。逆向把 d 个 port 容量相加，d−1 个 helper 各贡献总 singleton 质量一，得到 Σx_i≤1；d=0/1 和 zero membership 单列。

State-dummy 正向：agent 以 λ 取完整正 real support，其余概率平均分给 (K-1) 个 dummy；每个 dummy 总占用恰一。逆向把含本组 dummy 的配置剪成一个 dummy，不含 dummy 的阈值一配置必须含全 real support，得到 real 配置概率总和至少一，再向下削减成 FSLP。目标阈值大于一时每 agent 都需 dummy，K 个需求超过 K−1 容量。实际值桥独立处理至少一名 agent 未拿 dummy 的 pigeonhole。

最后，Proof v1 逐项核对 (Q_D)：main 每 state 以 (1/D)，helper 以 (1-1/D) 选 (g)、以 (1/D) 选 (A)，每资源边际恰一；实际 main 在一行至多拿一个 (g)，故 (V=1/D)，并给出等号 allocation。它还给出 T/D/SC 计数与 bit-length 约束，明确不把标准 LP 可行性升级为实际 allocation 或一般 solver。

## Proof v3：新增 flat CONFIG 桥与 v2 路径

Proof v3 的 flat CONFIG 正向在每个 private machine 给两类配置：

- 以 λ 取 selector 与全部 zero-private jobs，负载一；
- 以 (1-λ) 取全部 incidence jobs，负载为 state 权总和一。

每个正 incidence 的 private coverage 是 (1-λ)，再在其 unit resource machine 上以 λ 取 singleton；zero incidence 在 private 两类配置中都已覆盖一，unused resource 用 empty 配置。selector 跨 states 恰覆盖一，所有原 job 身份（含未选 state 和 zero job）保留，支持大小多项式。

反向对任意有限 CONFIG(1) 证书，令 λ⁰ 为 private selector 边缘。每 group Σλ⁰≥1。正 private incidence 不能与 unit selector 共存，故其 private coverage α≤1−λ⁰，唯一 resource 端 coverage 至少 λ⁰；resource 端所有原 job 时间为一，单配置至多一件，故正支撑 λ⁰ 总和≤1。按组向下削减到和一，得到 FSLP。若证书只要求 coverage≥1，Proof v3 还说明逐 job 剪掉多余覆盖，必要时在一个配置处分割一次，保机器负载且有限支持多项式。

Proof v3 重复但自足地给出 tree flow、port-path hole、state-dummy reverse 与 (P_{SC}) 的 actual/CONFIG 正阈值双向。SC path 反向的承重是：每 helper 正配置至少占一枚相邻 copy，即使同时占两枚；d−1 个 helper 占据至少 d−1 个不同 copy，剩余 old copies 边际总和不超过一。t>1 时不能剪 helper 为 singleton，证明只使用非空下界。oldOPT/old最高阈值不超过一时得到相等；t=0 另以 empty configuration 处理。

## 证据级别、范围与未完成项

这五份源分别是 Exact statement 和作者 Proof；Proof v1/v3 不是独立外审。前一批四份 statement-first/author read-after/final scope 审查记录已分别归档，最终 verdict “VALID/no fatal” 仍是内部审查结论。本文直接读取了五份源的全文，但没有运行代码、有限枚举或外部同行评议；BCG 归属只按源内叙述保留，不作本批文献新颖性认证。

Proof v3 未制作独立 v2 Proof，v2 的新增路径最终由 v3 Proof 重述。v1/v2 过程 Exact 保留其历史 SHA 与独有增量，不是额外重复定理。任何后续引用必须同时给出：FSLP 正支撑域、阈值一、oldOPT/old-threshold≤1 的 SC path 条件、zero/unused/duplicate 边界、以及 actual-OPT≥1 promise 尚未解决的限制。

## 用途与接续

该审查对象供第三阶段建立跨版本与证明依赖关系：v1 Exact/Proof 提供旧合同与 gap；v2 Exact 提供通用 SC 路径；v3 Exact/Proof 提供 flat CONFIG 桥并统一成熟对象。若需要直接核验 canonical scratch 中另列的原稿或代码，必须另行取得对应冻结文件；本批已提供的五份 Exact/Proof 本身足以支撑这里列出的版本差异与证明步骤。
