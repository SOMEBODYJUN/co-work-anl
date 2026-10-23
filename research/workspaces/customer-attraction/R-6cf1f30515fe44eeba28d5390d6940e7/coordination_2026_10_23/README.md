# 2026-10-23：一般候选的跨组核验与转送

恢复快照main `f6c744d7710f1981184c78ad74fc841bf682c1b3`。一般Q-CAG-HALF仍OPEN。本目录是Boss2协调核对与可复现诊断，未提升共享canonical，不声称外审或新颖性。通知和本人回复从[协调记录](../coordination_status.md)及[回执](../communication_receipts.json)读取；内部核对不代替同行本人回答。

| 文件 | 精确用途与读取条件 |
| --- | --- |
| [背景F递推](background_recurrence_review.md) | 重构Boss5旧全人数完整SPE族，否定固定首步系数和有界前缀欠债；Boss3新状态只有README，未据名称认定其重复旧桥 |
| [安全值平台](safe_value_review.md) | 重构Boss5公屏130–131：五环v7=v6(eA)=3/5及局部漂移−1/10；一般singleton整数/分数门槛不比较；不否定真实extra-one |
| [精确安全核验](audit_safe_values.py)、[结果](safe_value_audit.json) | 从单位客户定义独立复算五环462区间状态与静态原始/对偶，不导入原求解器；解析一般结论由正文证明 |
| [区间总预算](interval_total_review.md) | 校准GI、真实WP与自由Q的对象和强弱；累计债务只需支付OPT/2−根静态余量，无需强求累计非负 |
| [四组资产核对](quiet_bosses_review.md) | Boss1/4/8/9的已推送一般工作与身份依据；保护价格旧OPEN已被匹配证书否定，同支持/双支持耦合各有指定模板障碍 |
| [独立策略检查](strategy_review.md) | 单核完整净债是路由不变量，须新增真实中继约束；不同对象的失败不能互相代用，协调不形成审批循环 |

| [整合核BR信用边界](signed_kernel_review.md) | 新精确接口障碍CA-COORD-NOBR-MERGE-NO-v1：八人完整SPE W10、OPT16，任意先压缩路线首步BR slack41/8超过总余量4，因此丢全部BR信用的式(13)无可付路线；保留信用的总账与half仍开放 |
| [独立核验](kernel_debt_independent_review.md)、[脚本](audit_kernel_debt_independent.py) | 独立重放m5全部有序历史及m8全部11440计数状态/102960比较；五人只否定固定pivot标准路线，八人覆盖任意换pivot，不能混同 |
| [构造与导出](audit_merge_br_credit.py) | 明确诊断同一一般预算，精确逆推+导出策略后单独重放；仅m5/m8两次定向判别，不做人数调参 |
| [八人完整策略](merge_br_credit_m8_certificate.json)、[独审结果](kernel_debt_m8_independent_audit.json) | 直接恢复所有历史的合法计数策略；逐节点Fraction偏离核验及首步解析路由障碍 |
| [五人策略](merge_br_credit_certificate.json)、[独审结果](kernel_debt_independent_audit.json) | 保留路线量词的校准：固定pivot双写失败，允许切换pivot则有可付路线，不得将五人结果夸成全路由反例 |

新增结果的有限证书只证明指定实例的完整SPE身份；对其全部现行压缩路线的否定由首步解析下界承担。它不构成Q-CAG-HALF反例。实现环境Python 3.12.14，标准库、Fraction、无随机seed/浮点误差。内部独立复核已发生，无外审或新颖性认证。
