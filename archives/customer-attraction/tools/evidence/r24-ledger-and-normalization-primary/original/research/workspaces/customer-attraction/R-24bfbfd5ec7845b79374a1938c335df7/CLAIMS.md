# 本工作区的精确身份

所有条目使用仓库 CAG-MODEL；Q-CAG-HALF 一般量词与 OPEN 状态不变。
这里是个人研究备份，不自动成为共享 canonical record；外审、新颖性分别未认证。

## B3-TAIL-MIN-NORMALIZATION-NO-v1

- **Objects/domain:** 任意原模型实例、m>=2、全部完整有序历史纯 SPE；theta_m 对全部 m-1 长历史取末位最佳回复的最小值。
- **Exact statement:** 若存在福利 W0<m theta_m 的 SPE，则每个福利不超过 W0 的 SPE 的全部全局最低收益位置都在末两位之前。任何具有末两位全局最低收益者的 SPE 福利至少 m theta_m；原终局行动多重集不能通过重排实现这种 SPE。
- **Assumptions/definitions:** 不增加目录或人数上界；重复、空主题、任意平局均允许。W 是完整根福利，不是尾部剩余利润。
- **Conclusion/scope:** 否定特定福利不增的端点归一化，不否定半覆盖。m=2 时前提不可能成立。
- **Dependencies:** CA-LAST-TWO-FLOOR、客户均分的福利恒等式、同终局多重集收益的置换不变性。
- **Evidence:** 自足解析证明和下述36客户见证。
- **Counterevidence/objections:** 未见未解决致命异议；未声明所有实例均满足前提。
- **Status:** 作者及主代理解析核对，定义级独立核验通过；未正式共享入库。
- **Related files:** `normalization/tail_minimum_obstruction.md`、`normalization/audit_tail_minimum.py`、`.json`。

## B3-TAIL-MIN-RELOCATION-GAP-36-v1

- **Objects/domain:** 原有36单位客户、六个不同主题、三提供者的 aggregate-theta 实例；不更改原实例或其 Claim 身份。
- **Exact statement:** 全部 SPE 福利集合恰为 {34,36}；最差 SPE 福利34，而含末两位全局最低收益者的 SPE 最低福利36，故最小加法代价恰2。
- **Assumptions/definitions:** 全部有序历史纯 SPE 和任意历史依赖平局；不是固定某一计数选择器的结果。
- **Dependencies:** 该实例的逐客户收益表；完整离轨最优性；上面的阈值障碍。
- **Evidence:** 自足分类证明；两棵完整策略的单位客户 Fraction 回放；集合值逆向归纳检查全部有序 SPE 终局。
- **Counterevidence/objections:** 无目标反例；OPT_3=36，始终满足 half。无最小客户数、新颖性或外审声明。
- **Status:** 定义级核验通过；主代理核对正文。个人资产。
- **Related files:** 同上；原输入 `examples/customer_attraction/aggregate_theta_failure.json`。

## B3-ORBIT-OVERLAP-PRICE-v1

- **Objects/domain:** 原模型有限客户与共同目录；另有一个保关联、对主题传递的有限自同构群。任意 m>=1 的终局，不需 SPE。
- **Exact statement:** 设客户轨道 O 中客户喜欢主题的比例 p_O，若实际玩家 i 对每个轨道满足 `sum_{j!=i}|S_i intersect S_j intersect O| <= (m-1)p_O^2|O|`，则任意非负主题权重 z、总重 tau 都有 `sum_x min(1,sum_{T contains x}z_T) <= (tau+m-1)u_i`。若该玩家是实际收益最小者，推出 `OPT_m <= (2-1/m)W`。
- **Scope:** 轨道交叠条件承重；不宣称一般 CAG 实例具有此条件。重复行动只在确实满足该条件时覆盖。
- **Dependencies:** 有限群平均、截断覆盖的凹性、逐轨道 reciprocal Jensen 与显式一变量不等式。
- **Evidence:** 自足全参数解析证明；独立攻击正在进行。
- **Counterevidence/objections:** 一般早期最低收益玩家不自动满足轨道条件；没有因此支付一般半覆盖。
- **Status:** 完整解析稿；等待独立数学审查，未进入共享 canonical。
- **Related files:** `symmetry/orbit_overlap_price_certificate.md`。
