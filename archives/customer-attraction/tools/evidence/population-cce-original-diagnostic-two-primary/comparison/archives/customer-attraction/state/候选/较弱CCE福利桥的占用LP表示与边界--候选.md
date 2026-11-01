---
id: "customer-attraction/weak-cce-occupancy-bridge-candidate"
kind: "candidate"
type_tag: "候选"
title: "较弱 CCE 福利桥的占用 LP 表示与边界"
status: "exact-occupancy-reduction-with-open-bridge"
truth_status: "finite LP equivalence and family checks; bridge neither proved nor refuted"
review_level: "full-5075-byte-read-and-related-static-CCE-comparison"
scope: "Static CCE occupancy reduction for finite common-directory CAG model"
source_refs:
  - "clean:152335e7b6c56c7da922:research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/independent/weak_cce_occupancy.md"
  - "local:archives/customer-attraction/state/计算/R171弱CCE Boss2 独立逐人审计--计算.md"
  - "local:archives/customer-attraction/state/计算/静态CCE福利分离的初次策略锥证据--计算.md"
  - "local:archives/customer-attraction/state/反例/三人顺序SPE低于全部静态CCE福利--反例.md"
  - "local:archives/customer-attraction/state/定理/静态独立同分布安全基准--定理.md"
source_identity:
  inventory_blob: "d11af32ba70323464daaa736f080bd3c34d93be4"
  source_sha256: "48411e66ef69c04da6df6dd857c404f036cff99a645e65445d93577b3eacd363"
  source_size_bytes: 5075
evidence_paths:
  - "archives/customer-attraction/tools/evidence/weak-cce-occupancy-20261031/original/weak_cce_occupancy.md"
  - "archives/customer-attraction/tools/evidence/weak-cce-occupancy-20261031/comparisons/152335e7b6c56c7da922.md"

# 较弱 CCE 福利桥的占用 LP 表示与边界

## 待检验桥和模型量词

完整实读 5,075 字节原文。令
\[
 C_m=\min_{\rho\in\mathrm{static\ CCE}}\mathbb E_\rho W,
\]
候选桥是
\[
 W(\mathrm{SPE})\ge\left(1-\frac1{2m}\right)C_m.\tag{WC}
\]
已有静态安全值界 `C_m\ge m v_m\ge m OPT_m/(2m-1)` 若成立，即可由 (WC) 推出 `W\ge OPT_m/2`。原文明确这是充分桥，不声称等价性、`C_m` 总取下界或弱桥成立；对称 iid Nash 分布只是 CCE 的子类，因此 `C_m\le Z_m`。

## 占用计数的精确降维

对静态终局 `s` 和客户 `x` 的负载 `c_x`，把所有 `m` 位玩家单独改为固定主题 `T`，客户 `x\in T` 的查询收益总和为
\[
 b_m(0)=m,\qquad b_m(c)=\frac{m+1}{c+1}\quad(1\le c\le m).
\]
定义
\[
 H_T(s)=\sum_{x\in T}b_m(c_x(s)).
\]
任意静态 CCE 的个体约束相加得到 `E H_T\le E W`。反向地，如果终局分布满足全部聚合约束，将其按玩家置换均匀对称化后，福利和每个 `H_T` 不变；每位玩家对 `T` 的偏离损失为 `(E W-E H_T)/m\ge0`，所以对称化分布是 CCE。该双向论证给出精确有限 LP：令 `q` 枚举允许重复的 `m` 主题无序计数终局，
\[
 C_m=\min\sum_q\rho_qW(q),
\quad \sum_q\rho_q[H_T(q)-W(q)]\le0,
\quad \rho\ge0,\ \sum_q\rho_q=1.
\]
它允许任意相关、原本不对称的 CCE；不是只检验 iid 的放松。空主题、重复主题、零客户的边界仍在域内。

## 对偶与量词障碍

有限 LP 对偶可写为
\[
 C_m=\max_{y_T\ge0}\min_q\left[(1-\tau)W(q)+\sum_Ty_TH_T(q)\right],
\qquad \tau=\sum_Ty_T.
\]
若 `a_x=sum_{T\ni x}y_T`，内层逐客户分解为
\[
 \sum_x\big[(1-\tau)1_{c_x>0}+a_xb_m(c_x)\big].
\]
`1-tau` 必须保留符号：`tau` 可小于或大于 1，不能把离轨高福利一律当正成本，也不能预设 `tau\ge1`。要证明 (WC)，仍需对每个非负 `y` 方向构造一个合法 `q`，其对偶值受给定 SPE 福利控制；原文没有完成此构造。

## 已核对边界族

旧八客户、十三客户三人完整 SPE 例的静态 CCE 福利分别 `544/87`、`2785/297`，两例否定强桥 `W\ge C_m`，但仍满足 (WC) 的正余量；不能因此反驳弱桥。另有无拥挤 `m=k+1` 族，主题 `A_i=X_i+{a_i}`, `B_i=X_i+{b}`, `C_i=X_i`, `D={b,d}`，SPE 实际 `C_1,...,C_k,D` 的 `W=2m`、`OPT=3m-1`。取 `P0` 与 `P1` 混合，`p=2/(3k)`，并在玩家排列上均匀化，得到
\[
 \mathbb EW=2m+\frac23,
\]
且所有固定查询的 `H_T` 不超过该值；这给合法 CCE 上界 `C_m\le W+2/3`，足以验证该族满足 (WC)，但没有声称这是最小 CCE 福利。

## 与其他对象的关系和处置

R-171 Boss2 脚本是另一条弱 iid 家族的有限逐人 Fraction 审计；本源提供一般占用 LP 与对偶量词，二者不能互相替代。已有 iid 静态安全定理证明的是静态基准 `Z_n` 与 `v_n` 的关系，不证明顺序 SPE 向 `C_m` 的动态支付。已归档强 CCE 反例也不否定 (WC)。

本对象处置为 integrated 的候选/桥接口：占用降维和有限族检查可复用，但一般证明仍开放，不把旧摘要、有限 CCE 上界或 LP 表示升级为 Q-CAG-HALF 定理，也不迁移到 unrelated-machines。
