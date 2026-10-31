# 全深度树表示与离轨秩边界

本轮仅个人checkpoint；一般Q-CAG-HALF仍OPEN。

- `fixed_rank_proof.md`：从旧程序独立补全任意固定k截断障碍的自足证明；形式策略非SPE。
- `payoff_state_flow.py`：保留全部有序历史生成真实行，再按收益状态(q,a)压缩端点；可加
  自拥挤单调弧，或用`--potential`投影到Φ(q)-Φ(q-e_a)的势节点超边。是探索接口，
  不是普遍可行性定理。Fraction输出只有exact_ok=true时才已精确核验。
- `cyclic_nonpotential_obstruction.py`：n=2、5主题抽象循环收益精确否定只含真实行和
  自拥挤弧的全称流定理。不是客户吸引实例；违反exact-potential循环可积性。
- `anonymous_attack.py`：更宽匿名自拥挤收益类的有限攻击，不把该类当成CAG。
- `potential_attack.py` 与 `capped_attack.json`、`quadratic_attack.json`：直接从更宽单调DR
  势生成策略的5000+5000有限抽样；未发现桥反例，不是一般结论。相邻工作区随后用势锥LP
  找到严格反例，故这些阴性样本已不承担正向证据。
- `audit_potential_candidate_independent.py`、`potential_candidate_independent_audit.json`：
  独立逐定义核验相邻弱势反例，精确gap=-189；未使用发现实现。
- `shifted_potential_dilution_audit.py`、`shifted_potential_dilution_audit.json`：公共线性势
  平移K=17601同时修复全部2520条终局sharp稀释，而gap不变；仍有明确同支持效率违规。
- `audit_strong_potential_candidate.py`、`strong_potential_independent_audit.json`：独立核验
  相邻强势点的DR、自拥挤、全层一步sharp、纯harmonic轨迹、全部SPE及21背景；gap=-567。
  9个同支持效率冲突及二支持身份违规排除共同signed客户表示。
- `potential_flow_boundary.md`：上述边界的自足短稿，包括公共平移引理与Φ空间全层效率E
  恢复common signed Shapley覆盖矩的递推接口。明确引用Boss9已完成的共同客户表示，
  不把旧全图/稀释障碍重新声称为新结果。
- `global_submodular_lift_review.md`：独立逐式审查相邻单调次模C的全域Shapley势提升，
  并接入已有TC-DIL-1，确认其自动满足全部sharp。没有聚合安全或half结论。

当前实质进展：固定秩障碍已经补全；纯payoff-state流缺少势可积性；一般有限域单调DR
自拥挤势加全深度真实行，即使补终局sharp或纯harmonic/全层一步sharp，仍不能普遍给
聚合安全桥。这些失败都发生在共同signed客户耦合之前，不能声称高阶非负核必需。
下一步必须先保留全层支持效率E恢复同一Shapley覆盖矩，再区分次模、局部交替与真正
非负客户实现；不要再扫描已被强点击穿的松散势类或重复无信息的阴性样本。
