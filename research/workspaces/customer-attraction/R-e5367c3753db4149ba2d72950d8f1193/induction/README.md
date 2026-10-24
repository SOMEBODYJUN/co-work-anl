# 一般归纳分支：退款势与一个被否定的 reset 合同

主文件 [refund_potential_contract.md](refund_potential_contract.md)。Q-CAG-HALF 与 BG-HALF 均仍 OPEN。

本轮实际产出：

- 任意合法背景、任意固定删除位置的全历史关系 `g−ΔH=ε_actual−ε_deviation−Γ`，其中 `H=P_deleted−lost_coverage=全部 surviving incumbents 退款`，`ε_i=H−R_i>=0`；未来 reserve 精确为 `(n−1)H+I_fixed`。更小的共同终局税 `M=max_active R_i` 给 reserve `nM−H+I_fixed`，并且 M 在要求所有 reserve 非负的共同标量税类中逐叶最小。这明确携带每次改枝的新余额，但不构成较小原 CAG SPE。
- 独立完整核验35客户三人反例，否定 `max_T u_i(postdelete forced T)<=u_i(actual)+u_last(actual)`；根为24>13+9。实际退款势 H=0 仍有正 regret11，说明不能把实际 H 当唯一钱包。不是 half 反例。
- [audit_refund_potential.py](audit_refund_potential.py) / [refund_potential_audit.json](refund_potential_audit.json)：定义级 Fraction 审计 RP/RES、全部删除位置和完整反例。
- `check_last_deletion.py`、`last_deletion_diagnostic.json`、`attack_last_delete_one.py`、`last_delete_one_attack_report.json` 保留先前七个旧输入/完整策略锥的定向诊断。有限阴性没有证明候选，已由明确反例覆盖；不继续扩大扫描。

下一步：把真实全树约束用于支付 RP 的 signed reset 和 incumbent reserve；没有这一步不能宣称 half 正向闭合。来源与准确局限见主文件。无 git 提交、无 board 发送，由父研究者整合。
