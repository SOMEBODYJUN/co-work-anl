---
id: "customer-attraction/r171-signed-delta-residual-independent-review"
kind: "review"
type_tag: "审查"
title: "R-171 有符号 delta 余项与 tau 支付独立复核"
status: "analytic-identities-checked-global-payment-open"
truth_status: "conditional analytic review; no general payment certificate"
review_level: "full-5833-byte-read-and-parameter-range-check"
scope: "Signed-delta review of source §§5/6; scalar residual, S/Z normalization, terminal credit, cross-player obligation"
source_refs:
  - "clean:b8790423236c5c1b29da:research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/continuation/independent/signed_delta_residual_review.md"
  - "local:archives/customer-attraction/state/障碍/R-171有符号delta选择性预算独立复核--障碍.md"
  - "local:archives/customer-attraction/state/审查/R171独立接续工作区与稀疏租金弱CCE边界--审查.md"
source_identity:
  inventory_blob: "d175722b25a1db44d69958aaa703cf9102d6d17d"
  source_sha256: "77faf9edb822c5c6e4f1aaa546862b8ae2320e6b89e6df8f56c5c90ee7c52bd9"
  source_size_bytes: 5833
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R-171-independent-20261031/original/signed_delta_residual_review.md"
  - "archives/customer-attraction/tools/evidence/R-171-independent-20261031/comparisons/b8790423236c5c1b29da.md"

# R-171 有符号 delta 余项与 tau 支付独立复核

## 复核范围

完整实读 5833 字节解析复核。原文明确只审查 `../prices/signed_delta_selection_boundaries.md` 第 5、6 节，没有读取作者审计实现，也没有重跑其 13 人自动机或 2002 个最优组合枚举。本文因此把解析资产与已归档的 `R-171有符号delta选择性预算独立复核` 分开：后者是具体父方数值的选择性预算障碍，本页只检查公式在声明参数范围内的代数方向。

## 标量余项加强

令
\[
 A=d+a+1,\quad D=(d+1)(d+2),\quad
 R(u,e)=q\min(1,u)-\frac{u}{d+1}-\frac{\eta e}{A}+\frac{ue}{D}.
\]
在 \(d\ge0\)、\(a\in\{0,1\}\)、\(\eta\ge0\)、\(q,e\in[0,1]\)、\(u\ge0\) 下，复核用 \(u=0,1\) 端点和 \(e=0,1\) 端点得到
\[
 R(u,e)\le (q-t)_+\min(1,u)-\frac{(u-1)_+}{d+2},\qquad
t=\min\{(d+1)^{-1},(d+2)^{-1}+\eta/A\}.
\]
这里 `eta>=0` 控制零端点，`e<=1` 控制 `u>=1` 段斜率；不需要额外偷偷假设 `eta<=1` 或 `tau=1`。当 `q=1` 时，复核保留未覆盖客户信用和重复覆盖信用，这些项组成文中的 `E_i(z)`。

## S/Z 归一化、末位信用和总式

对同一组合 \(z\) 令 `tau=sum z_T>=1`、`mu=z/tau`。文中逐字核对
\[
 S=\tau u_i-\sum_Tz_TD_i(T)=\tau s_i(\mu),\qquad
 Z=\tau w-\sum_Tz_TU_{(d_i)}(R_{i,T},S_i)=\tau z_i(\mu).
\]
代入 \(\eta=1/2\) 后，覆盖式中 `S` 的信用系数是 `tau`，而 `Z` 的归一化系数是 **1/2**，不能误写成 `tau/2`。跨玩家相加并记
\[
 C_G=\tau\sum_{i=1}^m s_i(\mu)+\frac12\sum_{i<m}z_i(\mu),\quad
 E=\sum_iE_i(z),
\]
得到充分支付义务
\[
 \tau\sum_{i<m}\delta_i(\mu)-C_G-E
 \le (m-\tau+\tfrac12)W+\frac w2.
\]
舍掉非负 `E` 就得到作者的较弱式；当 `tau=m`、再舍掉信用时才回到 `(W+w)/2` 型预算。复核还展开了末位逐客户恒等式，确认 `p=0` 时仍由 `(u-1)_+` 正确处理，实际份额松弛 `F_i,F_m` 可保留为额外非负量。

## 结论边界

这些是带量词的解析恒等式与充分式检查，未证明存在一个最优组合 `z` 满足该支付义务，也未支付 signed-δ、skip-premium 或跨全树真实偏离。它没有复核 13 人数值、没有认证一般 Q-CAG-HALF、SPE、hardness 或新颖性。与父方已归档的数值障碍相比，本页提供的是可拼接的局部公式，不是障碍的撤销。对象处置为 integrated 审查记录，且不迁移到 unrelated-machines。
