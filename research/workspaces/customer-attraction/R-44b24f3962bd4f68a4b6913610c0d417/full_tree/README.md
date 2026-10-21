# 全树支付与客户交集矩

本目录维护两组自包含数学资产；原一般 Q-CAG-HALF 仍 OPEN。正文均按 CAG-MODEL 的全部有序历史纯 SPE，尚无外审或新颖性认证。独立内审以审查者实际回执为准。

- `truncated_intersection_moments.md`：固定 m,p 的全部终局收益行精确张成 ≤m 阶无常数 Boolean 多项式空间，秩 `Σ_{s≤min(m,p)} C(p,s)`；全部有序历史博弈只依赖这些交集矩；给非负有理客户类型压缩，m≥2保两两不同覆盖，以及奇偶核与合法矩边界。`audit_truncated_moments.py`、`truncated_moments_audit.json` 为标准库 Fraction 有限实现审计。
- `count_lattice_circulation.md`：势端点配平的普遍真实行零循环机制；十五单位客户、三个不同主题、三人完整 SPE 严格扩大收益图 SCC 像空间。根偏离行负向能由三个真实行非负支付。`audit_lattice_circulation.py`、`lattice_circulation_audit.json` 独立展开全部单位客户和有序历史、检查 SCC 与四行相消。
- `probe_extra_lineality.py`、`probe_distinct_lineality.py`：仅候选发现过程，后者 seed840013 在 trial29 找到上述合法实例。它们使用规范 solver、同行图工具和浮点 LP；正式数学证据由独立审计及自包含证明承担。前者的两主题候选强迫同覆盖，不用于原目录不同覆盖结论。

当前关键缺口：额外有符号空间不自动控制一般福利目标 `2c−o` 的余项。下一步应允许计数势端点循环共同重选早期支付，再研究未被循环支付的真实跨分支总预算；不能固定旧乘子后默认一切误差都可消去。低阶矩压缩同样不把合法矩锥变成独立非负坐标。
