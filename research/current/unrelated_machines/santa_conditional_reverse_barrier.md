# Santa Claus 无常数近似假设下的条件反面界

本文把当前最强的“证明不存在”技术路线写成精确条件命题。它是已有 Makespan→Santa Claus 归约和 LST 困难性的直接逻辑合成，不是新的无条件硬度结果；`UM-TARGET-v1` 仍 OPEN。

## 条件命题

定义假设 **SCHA**（Santa Claus Hardness Assumption）：对每个固定常数 (c\ge1)，在 (P\ne NP) 下，一般无额外限制的 Santa Claus/最大最小分配问题不存在确定性多项式时间 (c)-近似算法。这个假设目前没有被证明；它严格强于已知的固定因子困难性。

**UM-SANTA-NO-CONSTANT-CONDITIONAL-v1。** 若 (P\ne NP) 且 SCHA 成立，则不存在任何统一 (arepsilon\in(0,1)) 和确定性位多项式算法，对所有一般不相关机器输入满足
\[
C_{\max}\le(2-\varepsilon)\operatorname{OPT}.
\]

**证明。** 若 (arepsilon>1/2)，目标比率 (2-arepsilon<3/2)，直接违反 LST 的 (P\ne NP) 下界。若 (arepsilon\le1/2)，置 (alpha=1/arepsilon\ge2)，则 (2-arepsilon=2-1/\alpha)。BLMRS 的 Theorem 1（已有原文登记）说明：任何该比率的 Makespan 算法都会给出 Santa Claus 的 ((\alpha+\eta))-近似（任意固定 (eta>0)），与 SCHA 矛盾。两种情形覆盖全部 (arepsilon)。

该证明的量词是：对任意给定的统一 (arepsilon)，反设存在对应算法，再选择固定 (alpha=1/arepsilon)；因此没有把 (arepsilon) 偷换成输入参数，也没有使用准多项式过程。

## 为什么这还不是主目标反面

SCHA 是未解决的强假设。当前公开结果只给一般 Santa Claus 的固定因子困难性和 (n^\delta) 型近似上界；它们没有证明“无任何常数近似”。同样，配置 LP 或 Sherali–Adams 的积分间隙是松弛/舍入障碍，不是所有算法的复杂度下界。故本页只能作为**条件反面路线**：若未来证明 SCHA（或直接构造每个固定 (arepsilon) 的实际 OPT gap），即可立即得到主目标不存在；现阶段不能把它写成 `UM-TARGET-v1` 的无条件否定。

## 认知层和下一义务

- **Paper Fact：** BLMRS 的方向是“若 Makespan 优于2，则 Santa Claus 有相应常数近似”；它不是 Santa Claus 的无常数困难性证明。
- **Interpretation：** 要从该桥真正否定主目标，最短缺口是证明一般 Santa Claus 无任何常数近似，或绕开 Santa 直接给出实际整数 (1) 对 (2-arepsilon) 的归约。
- **Objection：** 已知 Santa 的 factor-2 困难性不能推出 SCHA；对 (alpha=2) 的 BLMRS 转换甚至只给 (2+eta) 近似。
- **Status：** 条件命题证明闭合；条件假设未证，外审/新颖性未认证。

相关来源已在 `research/unrelated_machines/LITERATURE.md` 与 `literature_manifest.json` 登记；本页不新增或改写原始文献字节。
