# 原子博弈、公平分配与广义指派的近期文献排雷

用途：在扩充候选池前，固定会改变选题判断的原始来源与核查层级。核查日期2026-10-20；boss6（发布身份R-933d363a9e0e431aab148ceeef444958）接续已有选题分支。本文不是新数学定理，也不把最新预印本的声称自动升级为经过独立审查的事实。

## 已核实的题源与覆盖警报

| 原始来源与位置 | 实际读取与准确结论 | 对选题的作用 |
| --- | --- | --- |
| [Cookson–Shah, Constrained Fair Allocations via Partition Matroid Reductions, 2608.31121v1](https://arxiv.org/html/2608.31121v1)，§5、Appendix B Def.13–14/Lem.11–12 | 已读原文相关定义、讨论与约化：四代理laminar问题被压到两种有限key matroid的EF1加指定有序无嫉妒问题；作者明确表示未完成。三代理laminar与任意代理transversal存在性已在本论文解决 | A类明确问题，值得实际试攻；不是因为有限物品就能枚举全部实值估值，尚须全量词证书。原有三代理/transversal存在题退出前排 |
| [Afshinmehr et al., EFX Allocations Exist on Multi-Graphs, 2606.18665v1](https://arxiv.org/abs/2606.18665)，摘要 | 原始摘要声称cancelable多重图估值下存在并可多项式计算EFX。本轮尚未独立复核全部证明 | 不能再直接推多重图additive EFX存在性；可以研究不同输出限制，但必须证明与新定理有真实差额 |
| [Garg–Murhekar, Existence of 2-EFX Allocations of Chores, AAAI2026](https://ojs.aaai.org/index.php/AAAI/article/view/38738)，摘要 | 官方会议页面陈述所有additive chores有2-EFX，并说明起点用Mahara的EF1+PO存在性 | 旧4-EFX不能作为当前最优前沿；2-EFX的计算与存在、效率要求分别核查，不能互换 |
| [Nguyen–Elbassioni–Rothe, Improving the Bounds on Approximating Weighted Maximin Share for Chores, 2610.15520v1](https://arxiv.org/abs/2610.15520)，摘要 | 新预印本声称二进制有理输入可多项式得到4.12424-WMMS，且存在严格正、共同排序成本族使最优因子趋e。本轮未独立审完证明 | WMMS旧[2,12]区间已出现新的覆盖声称，不能据旧区间选题；研究局部类之前先检查新上下界实例是否落入该类 |
| [Liu–Zhang, Revisiting Fair and Efficient Allocations for Bivalued Goods, 2604.08345v1](https://arxiv.org/html/2604.08345v1)，摘要及Future Directions | 原文声称修复旧算法不终止问题，并给共同bivalued设定的WEFX+fPO算法；其personalized扩展措辞必须与已知不可兼容反例核对 | 结合[已有精确复现](fair_fpo_compatibility_boundary.md)，无条件personalized肯定存在目标被阻断，不能仅凭未来方向一节把它列成开放猜想 |
| [Viswanathan, Improved Hardness Results for Nash Social Welfare, Budgeted Allocation and GAP via the Unique Games Conjecture, 2605.27098v2](https://arxiv.org/abs/2605.27098)，摘要 | 原始摘要明确UGC假设，给MaxGAP更强近似困难性声称；不是MinGAP容量扩张结果，也不是无条件不可能性 | GAP候选先统一max/min、比值方向、硬容量与资源增强语义。旧下界不能未经查新继续用作现状 |

## 可立即进入试攻的准确有限核

ID：SEL-LAMINAR4-KEY-v1。来源身份A：上表Cookson–Shah §5及Appendix B；不是团队声称新提出。

- Objects/Domain：四代理，共同laminar独立集约束，非负实值可加估值。两种ground set分别按(3,3,2)或(3,3,3,3)分组；每组每人至多一件；每人总件数分别至多2或3；全部物品分完。
- Quantifiers：对每一组估值、每个预先指定代理次序，是否总存在合法完整分配，同时EF1，并且次序靠前的代理不嫉妒靠后的代理？每种key分别回答。
- Conclusion sought：完整存在证明/算法，或精确反例。若两个核均成功，才依原文约化追到一般四代理laminar；单个核的失败不否定普通EF1存在。
- Dependencies：原文key定义、可行性保持约化、有序无嫉妒拼接接口。
- Evidence：原作者明确尝试；本轮已开始精确有限探针。尚无一般新证明。
- Strongest objection：估值连续无界；原文已指出三代理的top-k分离充分条件在四代理上失败，不能重复证明该条件总能满足。
- Status：probe。Novelty：问题非新；解决结果及新颖性未获得。
- Next discriminator：在真实EF1与ordered条件上构造全估值的有限线性/逻辑证书，或找到有理反例；不是只试随机整数估值。

## 如何使用本记录

先排除已被覆盖的原题，再评价自然限制后的差额。摘要层覆盖警报应促使精读，不能代替对新论文证明的审查。六条线仍独立扩充候选；上述第一项不自动成为唯一主攻。按[类型化价值判据](../VALUE_CRITERIA.md)比较完整成果包，有限实验只记Observation。
