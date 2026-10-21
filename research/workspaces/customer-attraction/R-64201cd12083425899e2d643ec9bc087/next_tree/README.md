# 全深度树表示与离轨秩边界

本轮仅个人checkpoint；一般Q-CAG-HALF仍OPEN。

- `fixed_rank_proof.md`：从旧程序独立补全任意固定k截断障碍的自足证明；形式策略非SPE。
- `payoff_state_flow.py`：保留全部有序历史生成真实行，再按收益状态(q,a)压缩端点；可加
  自拥挤单调弧，或用`--potential`投影到Φ(q)-Φ(q-e_a)的势节点超边。是探索接口，
  不是普遍可行性定理。Fraction输出只有exact_ok=true时才已精确核验。
- `cyclic_nonpotential_obstruction.py`：n=2、5主题抽象循环收益精确否定只含真实行和
  自拥挤弧的全称流定理。不是客户吸引实例；违反exact-potential循环可积性。
- `anonymous_attack.py`：更宽匿名自拥挤收益类的有限攻击，不把该类当成CAG。

当前实质进展：固定秩障碍已经补全；纯payoff-state流缺少势可积性，有明确有限阻碍。
下一步在势节点超边表示中保留全部深度，检验/证明任意形式策略的投影流是否可行；
尤其区分一般单调DR势、自拥挤DR势、实际非负客户harmonic核三类。
