# Boss8：一般完整历史半覆盖

研究存档：`customer-attraction`；本clone发布身份：`R-e6796fb9db2a4ae9994cee93ac9bd152`。

## 精确目标与状态

一般 Q-CAG-HALF 仍 **OPEN**。有限单位客户、有限非空共同主题目录、任意人数、全部有序历史和任意历史依赖平局的纯 SPE，目标为 `2W>=OPT_m`。重复、空主题与零客户不删去。本区是个人备份，不自动成为共享canonical结论。

从main `82da0361e60081fdc2e0440d4788860f8dc44b7e`恢复，先读根四入口、适用AGENTS、RUNBOOK、精确模型与本题前沿。六名指定 `gpt-6.1-sol` / `ultra` 内部研究员已实际运行；主代理汇总、独立审查与checkpoint。旧Boss8的13人36客户自动机继续按原来源复用，不改写其既有Claim。

## 已改变的认识

根响应成员核的stationary分布，即便只要求较弱 `cap<=W/(m-1/2)`，也不能普遍支付。旧13人36客户完整SPE给唯一stationary核 `cap=427/156`，阈值 `66/25`，严格差 `379/3900`。这只否定指定根核；同一根菜单任意混合可以降到 `29/12<W/m`，真正安全值已有 `v_13<=5/2`，半覆盖没有被反驳。

两份独立标准库程序从旧封闭自动机重建全部节点、动作边及真实最优性。主代理审计位于 [root_review/audit_root_stationary.py](root_review/audit_root_stationary.py)，冻结精确输出 [root_review/root_stationary_audit.json](root_review/root_stationary_audit.json)。核验27243个可达节点、93375个非自偏离（含自比较112050），用有理行消元证明stationary唯一。数学范围和发现正文见 `security/`；外审、新颖性未认证。

## 工作地图与下一步

| 目录 | 内容与准确状态 |
| --- | --- |
| security/ | 真正聚合安全值、根菜单与指定stationary核；有限锥LP仅作发现，弱根核已有精确反例 |
| root_review/ | 主代理对弱根核的新独立定义级重建，不导入发现者代码、规范SPE包或LP |
| root_uniform/ | 真偏离均匀接口，补查任意重复比较tuple。固定支持的计数单纯形端点完整覆盖，但仅四个既有策略锥；浮点未发现越界不作一般证据 |
| global/ | 真实末菜单与非均匀早期比较，正在探索全局非负支付 |
| credible/ | 弱逐人桥的完整DAG攻击，以及新多池可信构造。MILP无incumbent/浮点infeasible没有数学真值含义 |
| coupling/ | 共同非负客户与跨人数正项提升，推导进行中；不当作一般half证明 |
| background/ | 合法背景递归与弱逐人保底，尚未闭合 |
| independent/ | 独立全树计数策略锥探索与匿名化量词检查；有限样本不排除完整历史策略 |

继续义务：需要控制一般早期偏离的真实后继分支，而非只修改指定静态核。新正性工具须独立检查，并证明如何进入真实SPE行锥后，才能用于主目标。每段有价值工作及时checkpoint；只有程序回执pushed才报告远端保存。
