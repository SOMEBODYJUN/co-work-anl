# Round 5：两块菜单不能直接扩展成三块

对象始终是 CAG-MODEL：有限单位客户、共同目录、完整有序历史、任意平局纯 SPE。
一般 Q-CAG-HALF 仍 OPEN。本目录仅保存个人探索与精确有限证据，不提升共享 Claim。

- [last_low_cut_and_three_block_failure.md](last_low_cut_and_three_block_failure.md)：通用的最后低收益行动截断引理，以及三块菜单的有限完整排除。四个指定根子树目标全部不可实现；不是 half 反例，也不是任意块数定理。
- [block_menu_probe.cpp](block_menu_probe.cpp)：不导入规范求解器的整数集合 BI。输入参数 `2`、`3`；每块五个原始客户类型直接写入收益公式，计算全部历史依赖纯 SPE 终局集合，并诊断目标盒截面。
- [block_menu_n2_probe.json](block_menu_n2_probe.json)：两块回归，与旧证书的 12,870 状态、6,435 终局、16,852 保留 outcomes 完全吻合，四根目标全部可实现。
- [block_menu_n3_probe.json](block_menu_n3_probe.json)：三块 2,704,156 状态、1,352,078 终局、3,207,136 保留 outcomes；四根目标全部不可实现，全部最后低收益截面严格阻断。另保存 root 指定的 `p=uniform D` 替代菜单诊断，B、D 列不能过阈值。

下一步应证明或攻击真实子博弈的模块容量/最后低收益截断机制；不要盲目计算四块、更改组参数，或把条件插入矩阵误称为可实现策略。当前最精确的一般候选是：本例任意 `n` 块、`4n` 人时，根终局恰是单块六种根终局的乘积，并且至多一个块取 `q0=(2,1,1,0)`。仅 `n=1,2,3` 已由有限证据确认，任意 `n` 尚无证明。

2026-10-23。没有修改共享文件、没有 git 操作、没有读凭据。
