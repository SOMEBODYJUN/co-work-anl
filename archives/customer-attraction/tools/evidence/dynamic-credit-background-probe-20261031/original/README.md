# 背景利润的末位证书与精确余项

2026-10-23。个人探索资产；Q-CAG-HALF 仍 OPEN。

- [terminal_profit_remainder.md](terminal_profit_remainder.md)：任意固定非负整数背景、任意实际终局、仅假设末位最佳回应的精确非负余项分解。它扩展并重组现行 `two_remaining_tax.md` §6 的空背景末位税公式；不宣称新颖性或一般 half 已证明。
- [audit_terminal_profit_remainder.py](audit_terminal_profit_remainder.py)：独立 Fraction 核验逐客户恒等式、边界和 69 客户既有完整 SPE 的标量分解。
- [terminal_profit_remainder_exact.json](terminal_profit_remainder_exact.json)：实际运行输出。

派生候选 `F_r(b)-P <= r min_i u_i` 未得到证明或反例。更强的 `F_r(b)-P <= (r-1) min_i u_i` 在本轮也未证明。已经证明的是把 min 替换为真实末位收益的版本；所以真实最小收益在末位时强版本成立。对恰两人的任意背景，现行两人税定理进一步直接推出 `F_2(b)-P <= min(u_1,u_2)`。

下一步必须使用早期的真实离轨菜单给末位过高收益支付，不能仅凭本页末位余项宣称最小收益迁移。正文写明精确所需支付与一个已知非 SPE 模板上的缺口。
