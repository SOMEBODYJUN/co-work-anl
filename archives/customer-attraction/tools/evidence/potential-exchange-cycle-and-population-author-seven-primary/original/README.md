# 一般势表示：两条精确停界与保留接口

2026-10-23，root 子代理 potential 的个人研究备份。Q-CAG-HALF 仍 OPEN。
这里不是共享命题提升，也没有独立外审或全球新颖性认证。

- [potential_boundaries.md](potential_boundaries.md)：自足的任意人数 M 凹交换障碍、全策略标准形严格改善环，以及任意祖先背景的完全单调交叉差公式。前两项只否定写明的推广；没有构造 SPE 福利反例。
- [audit_potential_boundaries.py](audit_potential_boundaries.py)：定义级 Fraction 核验，不导入规范求解器；检查交换余项、全策略四环和高阶交叉差公式。
- [potential_boundaries_audit.json](potential_boundaries_audit.json)：脚本实际输出。
- [population_deletion_boundary.md](population_deletion_boundary.md)：任意人数的完整SPE联合删除闭包停界；所有m人SPE覆盖最优联合U，但所有较少人数SPE均根选T后选fresh块，必须覆盖U外客户。与已有固定人数联合删除/支持删除反例区别已说明。
- [audit_population_deletion.py](audit_population_deletion.py)、[population_deletion_audit.json](population_deletion_audit.json)：完整显式策略的Fraction审计。
- [security独立内部审查](../security/population_review.md)：先独立重构数学再以另一实现核验，审查通过；回收的较少人数全部历史分类已注明审查者归属。无外审或新颖性认证，Q-CAG-HALF仍OPEN。

路线判断：不继续把终局调和势的 M 凹性，或完整策略空间的 ordinal potential 当一般 half 主线。真正可能继续的势论证必须保留真实子博弈约束与祖先反馈。下文的完全单调交叉差是保留的精确接口，并未给全局债务符号；不以有限样本继续调参。
