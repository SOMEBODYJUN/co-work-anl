# 两代理两类物品的公平—分数效率兼容边界：原文排雷与独立探针

## 身份与精确范围

ID：SEL-FAIR-FPO-PROBE-v1。Status：文献反例独立复现及有限观察；没有新一般定理或新颖性升级。Objects：两代理、两类可复制的不可分物品；A,B是非负整数数量，估值分别为(1,a)、(1,b)，a,b为严格正有理数；权重w1,w2严格正。所有物品完整分配，代理1获得(x,y)，代理2获得(A−x,B−y)。

定义：alpha-WEFX采用对于所有i,j及g∈Xj，vi(Xi)/wi ≥ alpha vi(Xj\{g})/wj，alpha∈[0,1]；空对方束时条件为空。fPO指不存在分数分配使双方效用不减且至少一方严格增加。一般算法、零估值、多代理和压缩输入位复杂度均不在本探针结论内。

## Paper Fact 与选题异议

Liu–Zhang，*Revisiting Fair and Efficient Allocations for Bivalued Goods*，arXiv:2604.08345v1，2026-04，§5 Future Directions：提出personalized bivalued goods的WEFX+fPO计算方向。应逐项查其定义，不把未来方向当存在定理。[原文](https://arxiv.org/html/2604.08345v1)。

Davidiuk等，*EFX and PO Allocation Exists for Two Types of Goods*，arXiv:2601.03438v1，2026-01-06，§1 “Example: EFX and fPO are not always compatible”：A=B=2、a=10、b=9。唯一EFX计数分配是双方各(1,1)，但分数分配使代理1得11/10个第二类、代理2得2个第一类和9/10个第二类，可弱改进双方且严格改进一方。因此更一般模型中无条件要求WEFX+fPO不能直接成为肯定存在目标。[原文](https://arxiv.org/html/2601.03438v1)。这是已知反例，非团队原创。

## 独立核验与可回收接口

[程序](../probes/fair_fpo_independent.py)分别实现：

1. 正支持权区间：令r为两代理正社会权重之比。第一类给代理1时需r≥1，给代理2时需r≤1；第二类相应阈值为b/a。检查所有正数量分配产生的上下界有公共点。
2. 分数支配多边形：在[0,A]×[0,B]内加入两效用不减不等式，以Fraction精确枚举边界交点，检查是否存在严格效用改进。算法不调用第一种判定，也不使用浮点求解器。
3. 完整枚举整数计数分配，逐删除物品检查alpha-WEFX因子。探针包括空物品、单类为空、相同估值、分数估值、非均等权重。

[冻结结果](../probes/results/fair_fpo_independent.json)记录256个实例、1600个整数分配的两种fPO判定完全一致。已知反例中，fPO分配可达的最佳公平因子为10/11（代理1获(0,1)）；这是固定实例的精确有限结果。相同估值和空物品边界也通过。程序与结果含Python版本和源码SHA256。

可复跑命令（新结果放scratch，不覆盖冻结件）：

`python3 research/topic_selection/probes/fair_fpo_independent.py > /tmp/fair_fpo_recheck.json`

## Interpretation / 下一精确问题

这是分类/边界题的种子：用支持权阈值确定fPO结构，再问在权重、估值比与数量上何时存在精确WEFX，或者最优近似因子是多少。有限计数枚举本身、已有反例及两代理支持权刻画不自动构成可发表新内容。必须继续核Jin–Tao等personalized bivalued文献和一般公平—效率近似界，再判断扩展到多类型/多代理/更强算法是否有实质差额。当前不锁定为主选题。

Dependencies：正加性估值、完整分配、上述WEFX定义。Evidence：原文反例及两种精确oracle；Counterevidence：对无条件精确WEFX+fPO存在已存在fatal objection；对局部分类的新颖性未核完。Related files：程序、冻结输出、原文链接和本分支候选池（收齐后归并）。
