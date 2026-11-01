# Boss3：一般半覆盖的继续攻击

研究存档 `customer-attraction`；程序身份 `R-24bfbfd5ec7845b79374a1938c335df7`。
本工作区属于用户所称 Boss3 的本次独立 clone，首次身份由程序生成。

## Exact target and status

Q-CAG-HALF 保持原来的有限单位客户、任意有限非空共同目录、任意人数、全部有序历史纯 SPE、任意历史依赖平局、重复/空主题和零客户量词。目标为每个 SPE 的 `2W>=OPT_m`。**一般目标仍 OPEN**；下面的结构结论和失败推论都不改变它。

本轮六名实际 `gpt-6.1-sol` / `ultra` 内部研究员分别攻击背景归纳、共同价格预算、可信反例、新表示、势与负载预算、独立对抗审查。主代理汇总、核对并 checkpoint，不另为内部研究员建立远端身份。

## 新增可接续资产

| 文件 | 内容、准确范围与下一次读取条件 |
| --- | --- |
| [CLAIMS.md](CLAIMS.md) | 本工作区精确身份和状态；没有把个人备份自动升级为 canonical。 |
| [normalization/tail_minimum_obstruction.md](normalization/tail_minimum_obstruction.md) | 从已证末两人保底推出：即使只取最差 SPE，也不能福利不增地把最低收益玩家移到末两位；既有 36 客户实例的最差福利恰34、端点最低收益 SPE 的最小福利恰36。用于排除端点归一化这条证明简化。 |
| [normalization/audit_tail_minimum.py](normalization/audit_tail_minimum.py)、[报告](normalization/audit_tail_minimum.json) | 独立展开36单位客户，核验两棵完整43节点策略、全部末前缀和全部可实现有序终局；有限核验不替代一般阈值证明。 |
| [symmetry/orbit_overlap_price_certificate.md](symmetry/orbit_overlap_price_certificate.md) | 主题传递自同构群下的逐客户轨道交叠条件，推出任意质量分数查询的价格证书；两等大可交换组中的少数组玩家满足此条件。解析稿，独立审查正在进行。 |

## 当前真正缺口

`B(v)=max_{z>=0}[sum_x min(1,sum_{T contains x}z_T)-v sum_T z_T]`。
已证末位和倒二价格端点；任意较早最低收益玩家的共同价格预算尚未闭合。
一般背景版本可把最小剩余人数的反例化为第一名剩余玩家严格低于全部后继，但严格最低者这一情形仍无有效 Bellman 不等式。
独立策略锥实验尚未发现真正的目标反例，不把这一点当作一般真值证据。

对称类的新推导说明一种跨客户共同支付；一般目录并不具有这些自同构。继续研究须处理更早真实离轨续局，或构造经过全部历史精确回放的反例。局部结果、失败整理与有限搜索均不是主目标的终点。

## 保存与接续

根 `work.py`，存档及角色由本 clone 绑定；凭据在仓库外。
仅 `checkpoint` 回执 `status=pushed` 才表示远端保存。
本页是个人备份地图；共享正式入库应另做按对象整理、真实审查和适用登记。
