---
id: "customer-attraction/harmonic-payoff-cap-for-any-actual-player"
kind: "lemma"
type_tag: "引理"
title: "任一实际玩家的调和福利支付界"
status: "analytic-proposition-with-finite-corroboration"
truth_status: "general derivation read; not a Q-CAG-HALF proof"
review_level: "full-3913-byte-read-and-related-harmonic-material-comparison"
scope: "CAG-MODEL complete ordered-history pure SPE; arbitrary actual player j"
source_refs:
  - "clean:4e13b559d21301fae696:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/counterexample/mechanism_scan/harmonic_payoff_cap.md"
  - "clean:b9d80e2f19a93e649701:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/counterexample/mechanism_scan/harmonic_payoff_cap_audit.json"
  - "local:archives/customer-attraction/state/引理/同一实际福利对末对钱包的调和复制付款--引理.md"
  - "local:archives/customer-attraction/state/反例/三人调和势最优增量的完整策略证书--反例.md"
  - "local:archives/customer-attraction/state/障碍/调和势链未来回应项--障碍.md"
source_identity:
  inventory_blob: "36c82f77f5fc1c694163631b7037cd5538488deb"
  source_sha256: "e73c8f0da0a6ae86f3c5c207a2a12c165c7ec60f288b9e7307d20290040ed56c"
  source_size_bytes: 3913
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R-18-harmonic-counterexample-20261031/original/harmonic_payoff_cap.md"
  - "archives/customer-attraction/tools/evidence/R-18-harmonic-counterexample-20261031/comparisons/4e13b559d21301fae696.md"

# 任一实际玩家的调和福利支付界

## 命题和逐人系数

完整实读 3,913 字节个人工作稿。它在 CAG-MODEL 的共同有限目录、任意完整有序历史纯 SPE、重复/空主题、零客户及历史依赖平局全部保留的量词下，令实际终局收益为 `u_i`、福利 `W=sum_i u_i`、`H_m=sum_{r=1}^m1/r`，提出
\[
 W\ge H_m u_j\quad\text{对每个实际玩家 }j.
\]
更细的逐位置界为：若 `i<j`，`u_i\ge u_j/r_i`；若 `i>j`，`u_i\ge u_j/(r_i+1)`，其中 `r_i=m-i+1`。求和恰给 `H_m`。

## 证明的实际后继使用

在玩家 `i` 的真实历史，令 `b_i(x)` 为过去负载、`c_x` 为实际终局负载。允许 `i` 偏离到实际主题 `S_j`，再沿同一完整策略继续；无论后继如何回复，`S_j` 中客户的最终负载至多 `b_i(x)+r_i`，所以 SPE IC 给
\[
 u_i\ge\sum_{x\in S_j}\frac1{b_i(x)+r_i}.
\]
当 `i<j` 时 `b_i(x)\le c_x-1`，故 `b_i+r_i\le r_i c_x`；当 `i>j` 时 `b_i(x)\le c_x`，故 `b_i+r_i\le(r_i+1)c_x`。将 `S_j` 上逐客户份额与 `u_j` 比较即得两段系数。证明不冻结偏离后继、不合并同计数历史，也不要求匿名策略。

## 含义和严格性

它给出半覆盖反例的必要约束 `u_m\le W/H_m`，可作为策略锥快速筛选，但不是新的离轨最优性行。稿件还指出 `m>=3,u_m>0` 时 `W>H_m u_m`：若全等号，根位置的逐客户等号迫使末位主题客户各负载一且与早期主题不交；随后末位偏离到 `S_{m-1}` 会严格改善，矛盾。`m=2` 存在 `(1,2)` 福利 3、恰等 `H_2u_2` 的路径，因此严格性不能统一下调常数。

## 与现有调和对象的关系

已归档的调和末对钱包引理用不同的 `C'` 末对钱包支付 `(2H_m+1)C'\le W`，并明确早期冻结税仍未支付。本源按任一实际玩家给出更简单的调和福利必要界；它不构造实际全局付款。三人调和势最优增量完整证书反驳的是“下一调和势增量由根收益支付”的另一量词，而不是本命题；调和势链未来回应项障碍也只排除特定重置付款路线。

对象处置为 integrated 引理组件。伴随有限 audit 的作用是核对代数，不将本命题升级为 `2W\ge OPT`、弱 CCE 桥、策略锥反例或 unrelated-machines 结论。
