# 一般人数：提前末回复的可迭代性边界

一般 half 与六人 half 均 OPEN。没有把五人图机械扩成六人图。

本轮更强的付款边界是 [零源 regret 的正 reset](zero_regret_promotion_reset.md)：7客户、3人、4主题完整 SPE，实际末主题提前后源收益同为2，但势9降至8。现有强 PAIR 新枝独有税恰为1，且沿原主题回放链的全部所用 IC 松弛也为0。因而任何有限倍源 regret 或这些回放松弛均不能支付 reset。完整策略由 [固定逐单位核验](verify_zero_regret_promotion.py) 和 [精确输出](zero_regret_promotion_exact.json) 保存；非 half 反例。

[独立有序树重构](independent_zero_source.py)及[冻结结果](independent_zero_source_exact.json)另建完整策略并重现零松弛、reset=1；内部审查通过，未记录外审。[父方带价叉的独立阅读审查](promoted_fork_independent_review.md)核对了一般 k 的真实节点语义、全部权支出和压缩，不把旧点分离当成当前共同预算。

[末主题提前与尖锐 reset 边界](promotion_reset_boundary.md)重构任意背景末两人有效的势单调关系，指出其回复轨道部分与已有静态运输资产重复；再用完整历史三人 SPE 解析家族否定直接提前到更早源的势单调推广。已有强 PAIR 给出的新枝倒二独有税界，在该家族精确取等号，所以系数 1 不能无条件缩减。任意 k 的真实枝精确账说明未付项是跨互斥枝的有符号删位势 reset；仍须找共同预算。

固定复核为 [verify_promotion_reset.py](verify_promotion_reset.py)，输出 [promotion_reset_exact.json](promotion_reset_exact.json)。它展开单位客户并核对全部有序历史；不使用求解器或随机扫描。基础三主题实例不主张新颖，本页没有新增福利界、目标反例、外审或一般付款。
