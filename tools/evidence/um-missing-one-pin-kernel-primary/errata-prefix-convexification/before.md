---
id: "unrelated-machines/slot-envelope-configuration-identity-20261031"
kind: "review"
type_tag: "审查"
title: "有序槽包络配置身份与凸化边界冻结审查"
status: "integrated-representation-identity"
truth_status: "fixed-threshold-convex-hull-and-configuration-projection"
review_level: "full-source-read-independent-reconstruction-and-canonical-diff"
summary: "完整读取 UM-ST-ENVELOPE-CONFIG-IDENTITY-v1 审查。固定阈值下，前缀任务的有序槽包络 E 等于逐槽最大值之和；floor-shift 原子给出局部凸包的显式有理分解；全局最小包络等于真实 OPT；逐行固定同一 B 后的凸化恰是 CONFIG 的边际投影，并有附带上图凸包身份。结论是表示等价/凸化退化识别，不产生共同状态提取、通用 LP、非凸优化器或 UM-TARGET 结论。"
source_refs:
  - "source:657737ce38b6b4ed6820:research/reviews/unrelated_machines/slot_envelope_identity_review.md"
legacy_ids:
  - "UM-ST-ENVELOPE-CONFIG-IDENTITY-v1"
related_objects:
  - "unrelated-machines/slot-envelope-and-configuration-identity"
  - "unrelated-machines/configuration-lp-two-positive-endpoint-backend"
---

# 1. 来源与冻结范围

`clean show` 导出的来源 `657737ce38b6b4ed6820` 位于
`research/reviews/unrelated_machines/slot_envelope_identity_review.md`，6,094 bytes，SHA-256 为
`887e7321f04cbec31252e924e1e92f9054e9e6186baf33424f455a927e5736bc`。本页完整读取并将原文保存到
`archives/unrelated-machines/tools/evidence/slot-envelope-identity-20261031/original/`。

来源审查先只收到精确陈述，独立重构共同偏移分解和全局量词，区分“固定阈值子水平集凸化”与“整个上图凸化”，之后才读冻结证明。它还核对 canonical `slot_envelope_and_configuration_identity.md` 的 SHA-256 `d0c6ad29748d5c6b834415a77c615d325deaae98803093b9cf78439191a5ad52`；差异只改候选/正式身份措辞、补审查与链接说明，数学陈述、证明、例子、边界和位复杂度未变。canonical 新增链接所指的代码和运行记录本轮没有执行或确认。

# 2. 有序槽包络闭式

前缀任务的区间并集为 `[0,X_t)`，因此正交邻槽正好是前 `ceil(X_t)` 个；整数端点不会多出槽。按非负大小差分分层，逐槽最大值之和为
\[
E=\sum_t(p_t-p_{t+1})\,\lceil X_t\rceil,
\]
并可用同一分部求和得到线性负载及两者差。零质量前缀、零大小和并列大小都不破坏论证。`E` 是逐槽最大值的包络，不是给定全局槽图最佳覆盖匹配的负载。

# 3. 固定阈值局部凸包

对共同阈值 `B`，令
\[
y_t(u)=\lfloor X_t+u\rfloor-\lfloor X_{t-1}+u\rfloor,
\qquad u\in[0,1).
\]
每个 `y_t` 为 0/1，所有前缀计数不超过 `ceil(X_t)`，非负差分收费给出每个原子负载不超过 `E`；对 `u` 积分恢复任务边际 `x`。反向在每个整数配置上 `E` 恰为真实负载，所以固定 `B` 的局部凸包相等。

给定有理输入时，只需对 `0,1` 与所有内部断点 `1-frac(X_t)` 去重排序，再在每个区间取有理中点和区间长度；至多 `d+1` 个正权原子，不需在断点采样或按分母数值枚举。整数前缀无内部断点，`x_t` 为 0/1 给恒定原子，`d=0` 给权重 1 的空配置。前缀、断点、权重、中点和重算负载的总位长受输入总位长多项式控制，`B=0` 也成立。

# 4. 全局最小包络与 CONFIG 投影

全局任务守恒给每任务单位分数匹配、每槽容量至多一，Hall 覆盖匹配存在；匹配在各槽取得任务大小不超过该槽 `q`，因而所有机器满足 `L_i≤E_i`。另一方向取真实最优整数分配，其包络就是实际负载，于是最小包络精确等于 `OPT`，且由整数点取得；不依赖不连续非凸函数的拓扑取极值。

正质量区间长度至多 1，最多跨两个单位槽，总槽数和图边数多项式；确定性覆盖匹配和精确负载重算的位复杂度成立。无可用端任务的 `+∞` 约定、不可用边删除、空任务和 `OPT=0` 边界均已覆盖。剪枝实例 `P^T` 的等价范围只在 `OPT(P)≤T`，不外推到任意扩容 B。

逐行 CONFIG 身份必须先固定同一 `B`，再取每行 `conv S_p(B)`。局部凸包身份说明每行恰为 B 配置的边际凸包；加上每任务边际和为一，得到 CONFIG 的边际投影。空配置补足行权重、向下闭合删除超额覆盖的处理正确。两树 CONFIG 证书给出已知二倍下界，投影后的 `ST` 给二倍上界；这是已有阈值 gap 的复用，不是一般困难性证明。

# 5. 附带上图凸包与最小辨别例

`E≥p·x`，且所有 0/1 顶点取等，所以最大凸下包络为 `p·x`。同一有限顶点分解先给 `(x,p·x)`，再把每个原子高度统一增至 `z-p·x`，直接得到上图凸包等式，无需额外闭包。

这不同于固定 B 的子水平集凸包。`d=1,p=1,B=1/2` 时，固定阈值截面允许 `x≤1/2`，而整个上图凸化只保留 `x=0`；若删去“先固定 B”，CONFIG 身份会失效。手工 `9/10` 包络、`4/5` 均值负载、`7/10,9/10` 两原子及全局二机 `OPT=7/10` 例均与公式一致。

# 6. 处置与剩余义务

处置为 **integrated**：将槽包络闭式、floor-shift 分解、全局 OPT 身份、逐行固定 B 的 CONFIG 投影和上图区别纳入正式正文。剩余承重义务是从一般矩阵高效取得统一共同状态/余量、实际完整输出、sound FAIL 与总位多项式保证；本稿没有实现通用 LP、配置分离 oracle、非凸优化器或一般近似算法，不能据此关闭 `UM-TARGET-v1`。
