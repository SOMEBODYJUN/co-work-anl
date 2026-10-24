# 全范围遗漏联合预算分支

2026-10-24。范围始终为任意人数、任意有限共同目录、每个完整有序历史纯 SPE；Q-CAG-HALF 仍 OPEN。只在本目录写作，无共享修改或 git 操作。

当前正向资产是 [实际前缀上的联合客户席位](prefix_coupled_seat_budget.md)：全输入的完整竞争元组受限安全谱 F，以及显式前缀价格谱 G，给每个实际玩家一项下界，求和仅用一份 W。它同时计入私有遗漏、共享遗漏与已覆盖客户，逐位置支配旧固定分母私有谱和直接分母保底的最大值；严格区分例为新谱和127/2、旧最大值和184/3、W95。全文解析证明已完成；induction先只见G陈述盲重构，后读稿核F，解析审查通过（不含其独立重跑数值），见 `../induction/private_offset_spectrum_independent_review.md`。未提升为一般 half。

- `audit_prefix_coupled_seats.py` / `prefix_coupled_seat_audit.json`：Fraction 重算冻结例的 F/G 及旧界，完整证书31历史/124偏离通过。
- `refined_spectrum_complete_strategy.json`：上述严格区分例的完整历史纯 SPE 策略。
- `refined_spectrum_strict_example.json`：输入、实际路径与精细谱严格差。
- `check_refined_spectrum.py` / `refined_spectrum_regression.json`：检验这条精确全输入候选的固定种子有限回归，2288条可实现路径逐位置 u_i≥新谱≥旧两界最大值断言通过；不是普遍证明。

已及时放弃 `m min_i u_i≥|O\C|`：它被仓库已有71客户唯一最优例直接反驳，不再扩样，也不在此复制已有阴性资产。固定规模测试只为本目录明确的一般谱公式作精确回归。

准确剩余缺口：没有证明新谱和≥OPT/2或OPT−W≤新谱和。全部 Q_j 为空时，F/G 都退回已有直接分母保底；全共享遗漏仍需真实后继的额外理性，不能把同叶支配无条件延伸到共享触及。下一步应研究真正净机会缺口及同一份实际信用的跨树支付，而非继续固定规模或受限目录。
