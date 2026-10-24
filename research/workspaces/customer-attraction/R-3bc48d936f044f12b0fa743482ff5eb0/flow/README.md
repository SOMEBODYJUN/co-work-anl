# flow：同一角色共同预算的来源回撤

一般 Q-CAG-HALF 仍 OPEN。本目录只研究任意人数、任意共同目录、每份完整历史纯 SPE 的一般组件。

- [来源回撤与共享容量](origin_retraction_shared_capacity.md)：证明任意来源标记 R-flow 的精确回撤公式、最大回撤贪心及失败时的非负价格 cut。允许初始化 current 使用同一角色剩余第二份预算，不把每个 context 各付一次 u。该固定路由修复族可精确判定，但未证所有 SPE 必有成功修复；m=5 代入仍有四条未付容量条件。
- `audit_origin_retraction.py` 与 `origin_retraction_exact_audit.json`：定义级有理检查。重放既有真实完整 SPE 与零/空/全主题、五人 all-big 边界，检查同一次库存和金额回撤；不作通用成功或新特殊定理的证据。

下一步：用真正 off-history IC 限制 greedy 首次失败的 CUT，或允许重选最优 T、初始坐标分割及 common 边同时修复。当前没有证明该 CUT 对所有原输入非负。
