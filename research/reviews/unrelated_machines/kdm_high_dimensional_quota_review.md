# 高维匹配来源与部分配额障碍的独立审查

## 审查对象

审查 `research/current/unrelated_machines/kdm_high_dimensional_quota_obstruction.md` 的四项：LST 论文事实、直接超边需求树公式、公共/私有资源的低配额引理，以及对 `UM-TARGET-v1` 的逻辑状态。

## 先陈述重构

对根需求 `q`、超边节点需求 `K`、资源终端的 DAG，评分为 `b` 的树选取 `s` 条超边，且每条至少 `ceil(Kb)` 个资源；由资源单父条件得到一层 `t`-packing。反向从 `t`-packing 构造树，故

`b*=max_t min(nu_t/q,t/K)`。

这个上下界不使用计算假设，也不把 `nu_t` 当作可计算 oracle。公共资源加私有资源的族中，`nu_K=1` 而 `nu_t=q`（`t<K`），所以完整匹配比例与需求树值可完全分离。

## 独立攻击

审查者重构 LST Theorem 3.1 的确定性 CSP→KDM 最大匹配保真，以及 Theorem 4.1/4.3 的 `NP⊄BPP` 随机稀疏化假设。它们没有提供 KDM→Santa 或 KDM→`R||Cmax` 归约；已有 Bamas 方向也是“低于2的 makespan 算法蕴含 Santa 算法”的算法性蕴含，不能反向当作 hardness。

对两标签资源集合 `A,B`，当 `2t≤K` 时分别取不交 `t`-子集的集合论证明成立。若两差集都够大，直接取差集；否则两差集等势且交集足够分成两份。故单层共享/私有选择器无法在低配额时强制唯一标签。

## 结论

正文的 Paper Fact、部分配额恒等式和低配额逃逸均无尚成立 fatal。当前精确边界是：高维匹配给出了一个很强的候选源问题，但要用于主目标仍需跨层一致性 gadget，以及从任意低负载实际调度解码完整 KDM 匹配。`UM-TARGET-v1` 仍 OPEN；本页不能报告条件 hardness 已完成。

有限 `Fraction` 程序只核公共/私有族和双标签子集构造，不承担一般公式之外的数值证据。
