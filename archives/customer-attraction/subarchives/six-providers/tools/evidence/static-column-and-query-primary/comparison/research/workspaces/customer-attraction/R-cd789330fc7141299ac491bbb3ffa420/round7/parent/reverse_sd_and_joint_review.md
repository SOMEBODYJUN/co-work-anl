# 共同列界与保留 B 正项的反向 SD 核

2026-10-24，Boss10/root。原一般模型、任意人数/目录、每份全历史纯 SPE；Q-CAG-HALF **OPEN**。root 收到 COLUMN/ROW 精确陈述后独立按客户计数重构，再推导本页反向核。coupling 独立复核见[§6](../coupling/static_denominator_and_query_projection_review.md)，global 亦另行重构。无外审或新颖性认证；来源为本轮 [SD](../global/static_denominator_off_ic.md)、[固定 B 共同运输](../coupling/fixed_parent_static_column_capacity.md)与 [prefix 回推](../credible/joint_prefix_claim_pushback.md)。

## 1. root 对两种共同容量的独立核对

固定 Z、B，记 S_i=Z_i，C 为 Z 覆盖。SD 第一类正价为

    q^B_il=Σ_{x∈S_i∩(B_l\S_l), i≠l}1/[c_Z(x)d_i(x)],
    d_i(x)=c_B(x)+1−1_(x∈B_i)。

正支持保证 c_Z,c_B≥1，且 d_i≥c_B。对每个 l,x，发送者 i 数不超过 c_Z(x)，故 Σ_i q^B_il(x)≤1/c_B(x)。更精确的支持是 x∈(C∩B_l)\S_l。因此

    Σ_i q^B_il ≤ u_l(B; (C∩B_l)\S_l)。          (COLUMN)

对固定 i,x∈S_i，正接收角色数为 |cover_B(x)\cover_Z(x)|。若 B_i 覆盖 x，i 是共同角色不在正接收集合；否则 d_i=c_B+1。两种情况都给接收数≤d_i−1。因此

    P^B_i:=Σ_l q^B_il ≤ u_i(Z)。                 (ROW)

这两个界针对同一个矩阵同时成立。输入行系数 β_i≤L 时，全部正 B 税共同使用上述受限父利润，列系数≤L。它们不占 fresh 利润或 B_l∩S_l 的交集利润；这些不交支持上的既有客户密度也≤L时，可以共同放入同一父角色利润。**完整利润重采不保持这个支持条件。**

另对同一子叶 W 与 parent B（在 i 前前缀相同），prefix 回推中的每个 past j 的退款 N_j 安全；Σ_(j<i)q_jl=Σ_{x∈B_l\W_l,b_x>0}b_x/(c_Bc_W)≤u_l(B)，b_x≤c_W。输出 κ∞≤输入 λ∞。这是一份 W 的共同列界；多个互斥 W 或已有 parent suffix claims 不能免费叠加。

## 2. 新推导：保留全部第一类正价，再剪第二类

在一个真正 natural context (g,i)，沿用 SD 的

    B=finish(g), W=finish(g,S_i), v=u_i(B),
    ell=v−u_i(W)≥0,
    u_i=v+P_B+P_W−N_B−N_W−ell。

ROW 给 r=u_i−P_B≥0。令 F=ell+N_B+N_W≥0，则

    r=v+P_W−F，    (r−v)_+≤P_W。

可以保留原全部第一类 B 正边，并从原 W 正边中任取总价 (r−v)_+ 的分数子容量。其余负项与被删 W 正边按同一标量账取消，得到精确非负分裂

    u_i = P_B + min(v,r) + (r−v)_+。             (REVERSE-SD)

含义是：一单位 actual 行的利润资金可送往三类 off-history 利润目标：原 B 正价、当前真 prescribed B 利润中的 min(v,r)，以及 W 的真未来 context 中所选正价。当前完整 B 利润系数 min(v,r)/v≤1（v=0 时零量）。不同 W 目标仍是原正边子容量。这里不需要误设 F≤v；当 F>v 时，取消 W 正价正好使当前金额保持非负。

它和先把所有 P_B+P_W 混在一起作最大取消不同：本版本刻意保留第一类矩阵，因此保留已证共同 ROW/COLUMN。推导实质使用原 off-history IC 的 ell≥0；没有按客户改权调用 IC。

## 3. 方向、域与全局缺项

本核的方向是 **actual u 输入 → off-history 利润金额**。此前 SAFE 核的主要方向相反。不能因为存在这个守恒反向核就说任何 fresh/OPT 来源已在 actual W 内获得资金。

B 正边的合法域以 [SD 正文](../global/static_denominator_off_ic.md)为准：最后强制位置以后的角色是真 prescribed context；等于最后强制位置者是真 query；更早者含未来强制动作。后者可用 [query 投影](../coupling/static_denominator_and_query_projection_review.md)或同一子枝 [prefix 回推](../credible/joint_prefix_claim_pushback.md)修复，但需要合计全部系数。不能购买 fake past IC。

即使每个部分都合法，仍未解决以下事项：当前 B 项与 COLUMN 在父角色的新 C 客户支持上可能重用；多个 W_i 的独占未来利润仍未共同映回父 B；反向核、正向 SAFE 与投影可形成循环；没有证明有限总系数、所需源的可达资金支配或 actual cap2。PRICE/HIT 也不能不经重证穿过新的 current-natural 投影层。

## 4. 精确实现审计

[root 独立脚本](audit_joint_payments.py)展开旧 348 个单位客户，从不变完整策略独立重放 43 个有序节点、258 项含自身 IC、258 个 parent/child 对，核 prefix 退款和共同列界、SD 两步恒等式、固定 B 正价列界，以及全部 648 个 synthetic 叶/角色投影。非零 prefix 列224、非零静态税列101；[冻结结果](joint_payments_independent.json)明确只作实现及代数核验，不是一般福利证据。

反向核的一般证明由 §2 承担；当前独立解析审查已通过，数值不替代证明。未扩固定人数研究，未发现原目标反例。
