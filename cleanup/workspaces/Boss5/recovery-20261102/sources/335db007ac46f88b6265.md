# 连续分数背景候选的解析核查

2026-10-24。内部子任务，未独立审查；不修改共享 Claim。Q-CAG-HALF 仍 OPEN。

本分支在读过根入口、模型、现行前沿与失败范围后，尝试用连续分数背景弱化完整菜单 / extra-slot 个体保底。候选是任意合法背景 b、剩 r 人的首位利润至少

\[
f_r(b)=\min_{q\in\Delta(\mathcal S)}\max_{T\in\mathcal S}
\sum_{x\in T}\frac1{1+b_x+r\sum_{A\ni x}q_A}.
\]

这严格放松了整数静态背景和背景随机化的 reciprocal 平均；但任意背景版本仍被既有 PB-extra 构造直接否定。新核查只把该构造 §6 的 Jensen 论证准确扩到连续分数负载，不认领新实例、新策略或主线进展。

- [分数背景弱化仍受已有 PB-extra 分离的推论](fractional_background_floor_corollary.md)：自足定义、严格蕴含、分数 Jensen 扩展及来源。
- [空根分数容量的非线性静态对偶与未付义务](root_fractional_capacity_notes.md)：精确静态表示，不计作一般付款进展；记录根聚合候选仍缺什么。

根在轨的全局 m 槽弱版、聚合付款及一般 half 均未由此判定。没有新的一般正向支付关系；不把已有势恒等式重新命名为进展。
