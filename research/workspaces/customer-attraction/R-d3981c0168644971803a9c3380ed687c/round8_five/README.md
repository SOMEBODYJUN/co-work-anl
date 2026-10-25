# HALF(5)：五名提供者的接续

用户本轮明确要求六名 gpt-6.1-sol ultra 集中攻 n=5；这里 n 指提供者数 m=5，
客户数与目录大小任意，原模型全部历史、平局、空主题、重复及零客户不变。
这次范围改变不改写一般 Q-CAG-HALF。**HALF(5) 和一般目标仍 OPEN。**
本目录是个人研究备份，不是共享 canonical 结论或外审认证。
连续推导与真正未付款见[主工作稿](PROOF_WORKING.md)。

## 当前可接续的信息

| 对象 | 精确范围与用途 |
| --- | --- |
| [共用加权最大主题后的 hinge 族](root/shared_maximum_hinge_review.md) | 任意第三位真实历史、任意两份五主题菜单；从旧 BNS 与一个共同目录最大值消元。完整参数族仅13个断点，作者与父方独立解析核对。已精确切掉旧5421行联合松弛点，但尚无二倍付款 |
| [H 后真实两后继的七行投影](certificate/trueH_seven_rows.md) | 144隐藏状态完整有理系数证书，父方独立复算整表；只用原IC、两种最大性和末二税，保留真实Q,R。任意真实第三节点均适用，不继承祖先收益cap |
| [实际第三源的13原行投影](certificate/actual13_projection.md) | 6750行63有理原子点满足全部旧行却严格违反新投影；父方独立原式重算和tree语义审查通过。全部原支持只用真实IC/目录cap/末二税，max8可严格压为outer2定价；单条面尚未付二 |
| [有金额的覆盖重置](direct/weighted_maximum_coverage_transfer.md) | `|U_H minus U_source|<=24(V_H-K)`；完整共同账户恒等式及[独立审查](tree/coverage_reset_independent_review.md)。仍缺互斥source的总额付款 |
| [实际并集钱包](root/actual_union_wallet_review.md) | 对每个合法 C 有 `4W-5u1-4|C|+|A1|>=0`；父方独立64状态恒等式检查。是既有实际 IC 的显式后果，不扩大原有 LP 锥 |
| [末二最大势分支信用](tail/maximizing_pair_ic_credit.md) | 旧 Gamma2 可扩成 `K=Gamma2+epsilon*<=u4/2`，并有 delta*>=v5；`前三利润+K>=3v5` 仍是开放充分桥 |
| [末位份额与填充的精确失败](tree/terminal_share_and_padding.md) | 明确五人10客户完整 SPE 否定 W>=3u5（一般版本已有旧反例）；任意三人尾前添DD的通用提升亦失败。两者都不是 HALF(5) 反例 |
| [最大主题根来源审计](maxroot/independent_review.md) | 对同行192状态证书的节点适用性与精确系数独立核查。没有把辅助根关系当作新福利界 |

## 正在研究的付款

maxroot 与 certificate 正将实际第三源的同一个H,Q,R显式保留，接入该分支全部747原行，
而不为多条投影各自任意选择H。当前受限候选尚待全类型定价。直接推导继续保留相邻同计数历史的旧角色返还；
反例构造转向“最优五主题内单会员、其他目录主题共享”的遗漏与保险张力。
受限 LP 浮点值、精确松弛点和有限无反例均不是目标结论。

六名实际分支为 direct、maxroot、tail、tree、certificate、counter；父方同时推导
及独立定义级核验。研究状态以各文件的准确声明为准；未得到外审或新颖性认证。

## 证据

父方 [64状态实际钱包审计](root/audit_actual_union_wallet.py)、
[完整 hinge 系数投影](root/audit_shared_maximum_hinge.py)、
[10单位客户全树回放](root/audit_five_terminal_share.py)均通过。
其余实现、精确原始点和审查在对应分支目录。阶段运行仍在推进；本地图不承诺
任何 turn 结束后的后台计算。

[二值背景四尾重权](root/binary_four_tail.md)是为主付款做的一次辅助检验，已独审。
其新系数及自己的余项未切当前点，已停止该付款入口；不把它作为HALF5成果或另开四人项目。
