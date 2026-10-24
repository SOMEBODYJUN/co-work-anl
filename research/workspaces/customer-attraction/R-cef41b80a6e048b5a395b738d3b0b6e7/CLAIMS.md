# 本轮精确身份与状态

日期 2026-10-24。只记录本轮实际触及的对象，未建立新的共享福利 Claim。

## Q-CAG-HALF：原目标

- Objects/domain：任意有限单位客户 N、有限非空共同目录 S⊆2^N、任意整数 m≥1。
- Quantifiers/assumptions：每个定义在全部有序历史上的纯 SPE；允许任意历史平局、重复、空题及零客户。
- Conclusion：2W≥OPT_m。
- Status：OPEN；本轮没有一般证明、真正目标反例或新增原目标已证范围。
- Evidence/dependencies：模型和共享一般稿；本轮没有提升其真值。

## 既有 FTA（本轮曾记 AP-extra）：仍 OPEN

对全部原模型输入、完整策略和每个目录查询分布 p，令 A,B 独立 p，Z_i(B) 是在实际 i 前缀强制 B 后沿同一完整策略所得完整 m 槽叶，C_i⁺=E e_(Z_i(B))(A)。结论为 Σ_i C_i⁺≤W。

来源、定义、恒等式、充分性和 copositive 接口都已有于 R-486bb9adb8cd4d9a940dbf3b1ab0b1de/security/full_terminal_debt.md。本轮仅独立重构，不能视为新 Claim。固定策略锥无分离不支持一般真值。仍缺跨深度真实后继 IC 对共同 H/δ 信用的支付。

## PAIR-AP：FALSE，既有全路径反例已恢复

同一 Z_i，要求对全部 A,B 有 Σ_i[e_(Z_i(B))(A)+e_(Z_i(A))(B)]≤2W。245 单位客户、六主题、四人完整 SPE 的旧证书给 365>360；本轮已独立重放全部历史及动作。它只是 FTA 的更强充分条件，不反驳 FTA。精确输入、来源、两点余量与审查在 [independent/old_crosscap_replay_review.md](independent/old_crosscap_replay_review.md)。

## 非根 relay：初稿 R1 FALSE，R1-v2 是正确修复

- Objects：任意完整 SPE、任意有序历史 h、当前实际行动 A*、强制 T 后沿同一策略的完整叶。
- Definitions：V 为后继最终利润和，P 为早期最终利润和，Γ=u_current(actual)-u_current(deviation)≥0。
- Exact statement：ΔW=ΔV+ΔP−Γ≤ΔV+ΔP。
- Scope：全部原模型节点；只有根 P=0 或另证 ΔP≤0 时才可推旧 ΔW≤ΔV。
- Status：正确恒等式的来源已有 full-depth 账本；本轮纠正错误范围，不认领新机制。原无旧玩家项的通用 R1 已由两人三客户完整 SPE 反驳。
- Evidence/review：harmonic 自足反证，父方独立 Fraction 全历史回放，exchange 另作独立审查（以实际审查文件为准）。无外审或新颖性认证。
- Related files：[harmonic/relay_erratum.md](harmonic/relay_erratum.md)、[GENERAL_WORKING.md](GENERAL_WORKING.md)、已修旧稿及本题 RESEARCH_STATE。
