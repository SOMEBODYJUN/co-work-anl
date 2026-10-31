---
id: "unrelated-machines/diluted-shared-terminal-row-degree-section13-read-after-20261031"
kind: "review"
type_tag: "审查"
title: "稀释共享终端 row-degree 最终 §13 读后增量"
status: "integrated-section-read-after"
truth_status: "scoped-final-section-read-after-no-global-config-upgrade"
review_level: "clean-show-full-read-of-new-section-cross-archive-comparison"
scope: "diluted shared-terminal raw K2 final v1 new §13 row-degree extension"
source_refs:
  - "source:2e993729e2ea4cf91bc8:history/source/notes/unrelated_machines/sol_general_repair_diluted_row_degree_d_final_section13_post_read_v2.md"
source_sha256: "d4dcc198d7e8777d54fe0c74657998fb943f6fa235f2f5bc8e5aeb4641050c28"
evidence_paths:
  - "../../tools/evidence/diluted-shared-terminal-row-degree-section13-20261031/original/sol_general_repair_diluted_row_degree_d_final_section13_post_read_v2.md"
related_objects:
  - "稀释共享终端rawK2与终端探针共同间隙双源审查--审查.md"
  - "配置保环与高周girth有限审计--审查.md"
  - "私有昂贵叶的工作量与固定凸势近二边界--障碍.md"
---

# 稀释共享终端 row-degree 最终 §13 读后增量

## 1. 实际读取范围和时序

本次完整读取 `history/source/notes/unrelated_machines/sol_general_repair_diluted_row_degree_d_final_section13_post_read_v2.md`。
来源 ID 为 `2e993729e2ea4cf91bc8`，大小 4,712 字节，SHA-256
`d4dcc198d7e8777d54fe0c74657998fb943f6fa235f2f5bc8e5aeb4641050c28`；原文保存在
`tools/evidence/diluted-shared-terminal-row-degree-section13-20261031/`。

该来源只完整读取最终稿新增 §13（最终文件第 246–440 行，约 3,585 tokens），旧前
245 行只截取并做字节/hash 身份检查，未重新读取旧正文。它明示已经先读 Exact、独立
重构、作者 Proof 和旧 read-after，因此本页是最终正文的 proof-aware read-after，不是
新 blind review；旧前缀的语义不因 hash check 被重新认证。

## 2. 新 §13 的数学承重

新对象 `UM-DILUTED-SHARED-TERMINAL-ROW-DEGREE-GAP-v1` 与旧 raw K2 分开，参数固定
`d>=2`、`k>=d`、`D=max(4,d)`，新 `M` 吸收 subset 项；生成时间和位复杂度可依赖
固定 d，不能把二进制 d 当作统一多项式变量。全部原机器、jobs、有限端点表、全局
`M2` 和 affine localizers 保留，真实 OPT 仍由所有完整 assignments 给出

\[
\operatorname{OPT}=2-\frac{\lfloor\sqrt{k}\rfloor}{k}.
\]

row-degree 合同把共同矩阶提高到 `D=max(4,d)`：保留每台机器全部 endpoint 单项式、
总次数至多 d 的矩和所有全输入 affine q 的 load-localizer；它仍没有 joint CONFIG
selector、higher-q/event localizer 或 inactive-home 假设。

## 3. 有限差分和 localizer 的 exact 作用

对每个 `B` 行的具体 subset `S`，源使用

\[
b_S=(-1)^{s-|S|}\binom{k-|S|-1}{s-|S|},\qquad s=d-1,
\]

以及
`f(1,...,1)=sum_{|S|<=s} b_S f(1_S)`，把 H 的整行值改写为合法 CONFIG。`|b_S|`
至多 `A_max=binom(k-1,s)`，增大 `M` 至 `1+120Lk^4+4kZA_max` 后每个配置质量
非负，配置负载不超过 `T=1+s/k`。这保持每台机器总次数至多 d 的 moment 和
原全局 affine localizer，而不是只检查 endpoint diagonal。

固定 B 的 Qnew 系数给出正 slack `||c||^2/(60Lk^4)`，H 的负项至多
`-2||c||^2`；`M-1>=120Lk^4` 后按组件方差分解，所有全输入 affine q 的 localizer
非负。该证明继承旧 raw K2 的共同有限法则逻辑，但新 row-degree 只控制固定 d 的
有限矩层。

## 4. exact boundary: higher degree 和 cross-row events

源明确保留两条不能越过的边界：

1. 对 `A_i` 与 `B_{i,b}` incoming unit 指示，已有
   `F[A_i C_{i,b}(T-load_B)]<0`，所以加入有效的跨行二事件容量条件会切掉当前
   raw 证书；
2. 自然 degree-`(d+1)` mixed term 的 `a/L` 为正，而合法 CONFIG 给零，因此不能
   从当前 degree-d global PSD/矩合同自然推到任意更高阶 load/SOS 通过。

这使当前对象属于“固定 row-degree raw K2 的解析 gap”，不是更强 joint-CONFIG-M2、
高阶事件 localizer 或全局 schedule law 的 gap。已有
《稀释共享终端 raw K2 与终端探针共同间隙双源审查》已承重 raw K2、终端探针和共享小端
的完整对象；本页只加入 §13 版本时序、有限差分、row-degree 量词和跨行负项。

## 5. 软件和证据边界

最终稿记录了四个有限 trade audit：`(d,k)=(2,2),(3,3),(4,4),(4,7)`，分别检查
11、42、163、1471 个 squarefree row monomials。它明确没有枚举 global M2/localizers，
没有认证一般 d；旧 k=2 first/pair 的 50 维 audit 不能升级为新 §13 证据。

本次来源作者没有打开或运行 enhanced audit code、作者 JSON、旧代码或 root replay
scope。正文中出现的代码 SHA、JSON SHA、四例输出和 byte-identical CLI 都是作者/root
的归属说明，不是本审查复验；本页不把有限数量当成一般证明，也不把旧 v1 冻结时的
“未来运行”回写成已完成。

## 6. 处置与接续

本源处置为 **integrated-section-read-after**：原文保存，§13 的 row-degree fixed-d
合同、有限差分 CONFIG、localizer 正 slack、跨行负项和有限 audit 边界写入本增量页。
主数学仍由 raw K2 双源审查承重；本页不新造 source-gap 节点。

第三阶段关系可写为“raw K2 → fixed row-degree §13 extension → cross-row/higher-degree
obstruction”。仍开放一般 CONFIG/SDP 求解、跨行 joint law、higher-event localizer、
一般 UM hardness、全球新颖性和六人 SPE；这些不能由固定 d 的证明或四例 audit 代替。
