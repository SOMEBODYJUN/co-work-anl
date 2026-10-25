# Round 2：全槽 SUMmin 与精确有限层 DR 边界

当前原 Q-CAG-HALF、CAG-SUMmin-full 和 m 槽真正安全值聚合接口均仍 OPEN。本目录没有原模型的一般新福利界或目标反例，没有修改共享资产、git操作或外发。

## 已完成的精确辅助边界

[自足整数证书](dr_fullslot_boundary.md)给出共同四动作、三位玩家的有限相关层匿名势反例。势定义在0至m+1=4层，单调、含重复方向DR、精确边际效用、非负；同一完整有序历史纯SPE的实际总边际效用8，而全部12个实际full菜单的uniform独立query均为11/4。因此全槽SUMmin为33/4，严格超过8。

这排除只依赖相关有限层单调DR与匿名边际势的普遍SUMmin-full推广。它不是CAG，违反调和重复恒等式且三阶差为−5；没有声称无限域扩展，任何探索中的浮点feasibility状态不作数学断言。父方独立定义级重构尚待回报。

精确资产：

- [dr_counterexample_exact.json](dr_counterexample_exact.json)：70个整数势值、21节点完整有序策略。
- [audit_general_dr.py](audit_general_dr.py)：只读上述精确输入，以Fraction核全部140单调边、150局部DR方格（含重复）、84条SPE比较及12个完整菜单。
- [dr_counterexample_audit.json](dr_counterexample_audit.json)：精确输出，SUMmin gap=1/4。
- [probe_general_dr.py](probe_general_dr.py)、[probe_general_dr_float.json](probe_general_dr_float.json)：发现用MILP与浮点原输出；其最优性不用于结论。
- [probe_quadratic_dr.py](probe_quadratic_dr.py)：一次先行的二次负交互势定向检错，浮点最优0；不作一般证据，未继续阴性扩样。

## 回到原 CAG 的准确断点

本轮没有得到适用于所有原输入的新共同付款。对原1/c核重算可得任意完整m槽z的Euler/删除恒等式

    (m+1) G_p(z) = Σ_(j=1)^m G_p(z删j) + E_(T~p)|T\U(z)|.

逐客户核对：c=0时右侧是(m+1)q_x；c>0时右侧为q_x[1+(m−c)/(c+1)]=(m+1)q_x/(c+1)。这只是已知全槽折扣的另一准确表示，不记为新增付款关系。它显示泛势版本的末项是总边际效用增量，CAG把它绑定为真实非负新增覆盖；尚未把不同实际菜单分支共同支付到原实际W。

真正下一步仍是直接利用1/c核、非负相容客户类型或覆盖守恒证明CAG-SUMmin-full，或构造原类严格反例。原候选来源为R-e7c3c9a51d38458aa551eec469e04cf2/global/及父方既存接续；本目录不认候选首次。没有再开固定人数或结构专项。

按同一一般机制代m=5，SUMmin-full若成立只条件性给v_6≤W/5及OPT_5≤10v_6≤2W。没有该付款证明就没有无条件一般五人half；泛DR辅助反例也不能判原CAG机制为假。
