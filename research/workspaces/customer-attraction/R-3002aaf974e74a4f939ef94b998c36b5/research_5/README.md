# 3889旧关系加入五条根行：精确共同可行边界

状态：可复现的精确必要条件点，**不是实例、不是SPE、不是六人目标反例、不是最优值认证**。research_5准备了集成代码后因平台用量限制停止；主方执行完成发现、精确恢复与核验。

输入是 `R-c4f1ef099fad483c9f81283b61eb0b53/six_astra/attractive_nested_exact.json` 中16个hist类型支撑，原生成器 `attractive_nested.build(histcols)` 的3889条关系，加本轮 `research_4` 四条已独立内审的根行和联合QL/QD根行，共3894行1905列。五份精确证书的SHA、a、beta及唯一来源全部绑定在 `root_rows_joint_point.json`。不修改任何旧冻结输入。

运行 `python <本目录>/integrate_root_rows.py`，浮点只发现支撑，`cl.exact_point`恢复有理权，继而完整Fraction逐行核验。结果 `O=1`，

`W=11563846740120540563650285979166203/24234087715908087797320314905948740≈0.4771727690<1/2`。

所有3894关系精确非负，最小0。五个根行的精确余量在JSON，联合QL/QD行取等。父方另写 `../audit_augmented_point.py`，调用原3889行生成器重放旧关系，并独立从hist实际会员计算r、K、O及五条证书a/beta，复核新行；输出 `../augmented_point_audit.json`。它不导入本目录集成代码，但不声称独立字面重建全部旧行。

旧3889点确被新根行切掉，重优化后这个新点仍存在，所以切一点不能当共同主预算已闭合。16hist是限制支撑：可行坏点足以给指定行族的边界，但若此支撑不可行则不能推出全域half。隐藏变量的联合实现条件沿旧正交叠/共同阈值证明；未添加Z→Z或全部真实早期索引关系。

复现：从仓库根运行 `python research/workspaces/customer-attraction/R-3002aaf974e74a4f939ef94b998c36b5/research_5/integrate_root_rows.py --verify research/workspaces/customer-attraction/R-3002aaf974e74a4f939ef94b998c36b5/research_5/root_rows_joint_point.json`。父方复核用 `python research/workspaces/customer-attraction/R-3002aaf974e74a4f939ef94b998c36b5/audit_augmented_point.py`。
