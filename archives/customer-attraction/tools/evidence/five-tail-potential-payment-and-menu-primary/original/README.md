# HALF(5)：五人完整历史 SPE 的半覆盖

研究存档 `customer-attraction`。本轮用户明确指定五名提供者，单位客户数、共同目录大小均任意，全部离轨有序历史和任意历史依赖平局保留。目标 `OPT_5<=2W` 仍 **OPEN**；没有五人证明或目标反例。

这是环境恢复后程序生成的本 clone 身份；先前 Boss10 的数学资产保持原位，不覆盖其身份文件。恢复基线 `ff6a0ccab4ae6eb865d6960a6e7468615159645a`。先读[模型](../../../current/customer_attraction/model.md)、[前沿](../../../customer_attraction/RESEARCH_STATE.md)，本轮直接接续[原五人稿](../R-cd789330fc7141299ac491bbb3ffa420/round13/PROOF_WORKING.md)。

## 本轮可复用内容

| 文件 | 数学内容、真实状态与读取条件 |
| --- | --- |
| [five_payment_interface.md](five_payment_interface.md) | 已知末位、倒二查询行和末二势损失的消元推论：`P+Gamma<=(49W-13OPT_5)/36`。独立内部代数核查通过；由此识别更弱充分候选 `P+Gamma>=23OPT_5/72`，该下界仍 OPEN。它不把两单点实例对 `3u_5` 的反证错误扩大到旧 `3v_5` 候选。 |
| [five_potential/payment_interface_review.md](five_potential/payment_interface_review.md) | 不依赖新代码的独立重构、常数、零客户边界和必要等号条件；只有组件审查，没有证明候选下界。 |
| [terminal_menu_envelope.md](terminal_menu_envelope.md) | 真实末两人三组 IC 的参数化消元包络，五人域的20个精确断点完整保留全参数族。已独立核对节点、符号与参数量词；[17,920个逐类型精确恒等式检查](audit_terminal_menu_envelope.json)是全类型代数 QA，不是有限游戏搜索或 half 证明。 |
| [five_tree/README.md](five_tree/README.md) | 最优根查询族末位与另一真实末位菜单的跨族比较；保留同一客户/同一索引的相关性。新行是旧末位最佳回复的应用；模板分离、有限语义回放和全域定价须分别读取，不能当作完整 SPE 或 HALF(5) 证明。 |

## 当前真正缺口

仍需完整的真实早期子树给出共同预算，或一份可逐历史重放的真正五人反例。单尾税界、局部安全保底、逐节点密度以及必要条件的坏点都不提供这个全局付款。原 `P+Gamma>=3v_5` 与本轮更弱接口均未证；只有 `3u_5` 加强已被旧完整 SPE 反驳。

研究过程中六名指定 `gpt-6.1-sol ultra` 子代理与父方承担不同方向；该记录不承诺 turn 结束后后台常驻。内部重构、外部独立审查与新颖性认证分别标记，本轮没有外审或新颖性认证。
