# 一般半覆盖：全树运输与跨实例产品判别

研究存档 `customer-attraction`；程序身份 `R-4243b113e6fc4c25a197dec299f08049`，本对话独立 main clone。唯一目标仍为 Q-CAG-HALF；全部有序历史与任意平局量词保留，一般仍 OPEN。

## 已改变的认识

[PRODUCT-MENU-TIME-v1](parent/product_menu_time_obligation.md) 给一个全局等价归约：自由完整实际前缀菜单若对所有实例支付 W/m，固定 m 下必须存在跨全部实例/SPE/查询通用的时间权重。有限不相容可由整数产品转换为该辅助桥的合法完整 SPE 反例。独立定义级审查通过；没有证明通用权重存在或不存在，不解决 half。

[BANK-PATH-CAPACITY-v1](global_induction/bank_joint_deviation_budget.md) 给完整产品目录任意跨坐标历史依赖 SPE 的银行补贴容量：保持当前银行动作时，全部实际节点主菜单盈利之和，至多逐银行客户的精确时间谱；每客户最多 1−c_x/m，递增嵌套银行路径的容量恰为零。全历史满足相应包含条件时，主坐标诱导策略保留完整 SPE。这不排除离轨激活的银行，也没有把互斥子树信用支付回根。

两组自足解析证明均经独立内部重构，另实现的完整策略审计及 root 重放通过。外审和新颖性未认证。六分支均已完成本轮交接，无后台常驻研究承诺。

## 文件地图与接续

| 路径 | 内容及用途 |
| --- | --- |
| [CLAIMS.md](CLAIMS.md) | 主目标及产品归约的精确对象、量词、依赖、审查与局限 |
| [RESEARCH_STATE.md](RESEARCH_STATE.md) | 当前新增认识、未解义务与下一次有信息价值的行动 |
| [parent/product_menu_time_obligation.md](parent/product_menu_time_obligation.md) | 同步位置产品公式与全实例通用时间混合的完整证明 |
| [independent_attack/product_menu_separation_review.md](independent_attack/product_menu_separation_review.md) | 独立定义级重构，检查全历史、查询边际、有限有理分离及零客户 |
| [representation/menu_separation_small_support.md](representation/menu_separation_small_support.md) | 独立证明不相容见证至多 m 种实例查询对；总整数复制数不可偷换成 m |
| [counterexample/product_menu_review.md](counterexample/product_menu_review.md) | 另实现审计273历史、4368比较、768核项和12组关联查询；精确原始/对偶值277/54 |
| [global_induction/bank_joint_deviation_budget.md](global_induction/bank_joint_deviation_budget.md) | 真实联合偏离银行预算、时间谱、额外税与全历史主投影充分条件 |
| [tree_dual/bank_budget_independent_review.md](tree_dual/bank_budget_independent_review.md) | 独立银行推导和审查；含非零前缀版及互斥子树的未解支付 |
| [global_induction/audit_bank_budget.py](global_induction/audit_bank_budget.py)、[证据](global_induction/bank_budget_audit.json) | 固定seed 37个小产品、7447决策节点、66597含自身比较及414主投影比较的精确实现检查 |
| [parent/probe_common_time.py](parent/probe_common_time.py) | 固定规范证书语料的一次切割平面诊断；不是一般证明 |
| [parent/common_time_diagnostic.json](parent/common_time_diagnostic.json) | 实际参数、接纳/跳过语料和有限阴性结果，禁止据此升级真值 |
| tree_dual/、global_induction/、transport/、representation/、counterexample/ | 六分支中相应五路的当前推导/查重/边界；以各自 README 实际内容和状态为准 |
| independent_attack/ | 第六分支的独立攻击与产品归约审查 |
| [FAILED_ROUTES.md](FAILED_ROUTES.md) | 本轮撤回、查重、恒等表示与真正承重义务的区别 |

## 研究原则

不重复固定人数乘子调优。已失败加强命题与主目标严格分开；归约、完整证明、内部审查、外审及新颖性分别标记。个人备份不是共享 canonical 入库。root 统一 checkpoint，只有实际 status=pushed 才报告远端保存。
