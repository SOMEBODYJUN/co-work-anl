# 一般直接福利与可信阈值换位：本轮 checkpoint

2026-10-24。父身份 R-d3981c0168644971803a9c3380ed687c；分支 direct。
唯一目标始终是 CAG-MODEL 全部输入和全部完整历史纯 SPE 的 `OPT_m <= 2W`。
本轮**没有证明一般 half，也没有得到新的已证一般福利付款不等式**。

先读根 AGENTS 与四入口、model、general_half_proof，后按当前义务阅读：

- 旧 continuation_general/fresh 与 exchange：旧(D)、价格 good 菜单、rook 仅尾 floor 的准确停界；没有重复这些阴性锥。
- round5/menu/pair_attack：PB-extra任意背景版本的完整解析反例，不偷用 extra-one逐人floor。
- root 指定的新 `R-cd789330fc7141299ac491bbb3ffa420/round6/global/credible_adjacent_transposition.md`、mixed独审与second-node修复合同。

## 本轮候选已被反驳

见 [adjacent_threshold_cap.md](adjacent_threshold_cap.md)。原候选C现为 **FALSE**，反例来源为 [normal_form正文](../normal_form/swap_ascent_payment_counterexample.md)，本分支先盲定义级重构见 [独立核对](review_threshold_cap_counterexample.md)。换位缺陷与原实际上升的比值无界，不能用任何通用有限倍数支付。原探索历史保留。

`check_adjacent_threshold_cap.py` 和 `adjacent_threshold_cap_diagnostic.json` 只检验这条明确候选，在五份已存在的输入上使用规范的全SPE集合值递归枚举实际有序路径。共检查160个相邻严格上升，未出现反例。没有保存对偶普遍证书，也不把有限阴性当一般成立证据；按父指令停止扩样。

## 当前接续点

候选C已停止，须换另一条真正能将高阈值成本交回同一q利润的关系。原换位定理只给 `mu_B>alpha`，不蕴含 `mu_B<=beta`，也不蕴含 `mu_B>=tau`。虚拟转账本身不使一个非SPE的交换叶成为SPE。
