# 核心—私有资源全层配额障碍的独立审查

审查对象：`research/current/unrelated_machines/cross_layer_quota_matching_near_two_obstruction.md` 及其 Fraction 审计。审查先独立重构闭式配额，再核对桥梁任务的实际负载；本页只确认所声明范围，不把该族升级为一般复杂度下界。

## 重构与核验

令 c=K-s。当 t≤s 时，各变量取私有资源；当 t>s 时每个变量至少占用 t-s 个共同资源，因此 nu_t=min(q,floor(c/(t-s)))。参数 q≥ceil(cK/s) 给出 c/q≤s/K，而 t=s 达到 s/K，故全层值恰为 b*=s/K。这一步不需要假设不同层的领取可以嵌套。

桥梁矩阵中，根任务固定负载1；全部 a_i,b_i 外送后，每个 e_i 留下 c 个 1/K 任务，负载 1+c/K=2-s/K。需求树桥梁的反向解码只对 C<2 使用，足以给出任意更好调度的下界；显式构造给出上界。小实例直接枚举 (K,s)=(2,1),(3,2),(4,3) 时分别得到 3/2,4/3,5/4，与公式一致。

审计 `cross_layer_quota_matching.py` 使用 `Fraction`：小集合代表系统全枚举35个参数组合，闭式与负载检查覆盖 K=2,...,100 的4950个组合，并核对三组实际桥梁样本。运行属于 `checks`，不替代一般证明。

## 异议与边界

“低层全匹配不能区分”只适用于只观察某一低层的 decoder；任意全层 decoder 在 s+1 层仍受 nu_(s+1)≤c 的容量切面限制。该族资源结构显式可识别，YES 对照也显式可解，因此不能推出 P≠NP 下的近二困难性。它没有源相关接线、任意低负载调度的源解码或统一位复杂度归约。

审查结论：在所声明的核心—私有集合系统、需求树桥梁和实际不可拆任务范围内，命题与审计无 standing fatal；状态为 `complete stated-scope obstruction; independently reconstructed and exactly audited; external review and novelty unverified`。`UM-TARGET-v1` 仍 OPEN。
