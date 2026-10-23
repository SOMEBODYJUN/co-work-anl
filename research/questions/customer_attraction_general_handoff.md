# 一般半覆盖：真实分支的共同支付与候选安全值接口

研究存档：customer-attraction；目标身份：Q-CAG-HALF。

本页是 **Q-CAG-HALF** 的短数学义务，不是角色提示词、路线审批或指定方法。[一般目标](customer_attraction_half_coverage.md)仍 OPEN；任意人数、任意有限共同目录、每个完整历史依赖纯 SPE 的量词不变。旧两份长提示词移入[历史原件](../../history/research_operations/customer_attraction_general_handoff_2026_10_10.md)，其中相对链接按原 research/questions 目录解释。

## 当前研究范围

主人最新决定：只研究任意人数和一般共同目录，所有数学领域与方法开放。停止特例规模、结构子类、局部常数和逐n算法项目。有限实例只检验一个明确一般候选；失败推导、无反例、超时均不能说明原目标不成立或不可证明。下面的接口是可替换的搜索种子，不能形成方法白名单或开工审批。

## 直接目标：控制真实离轨分支的总覆盖

固定任意完整形式策略 \(\sigma\) 及任意 \(m\) 个合法比较主题 \(T_1,\ldots,T_m\)。令 \(w\ge0\) 为客户兴趣类型重数，\(\Gamma_{h,a}\) 为每个有序历史 \(h\) 的原行动收益减去改选 \(a\) 后沿原 \(\sigma\) 续局所得收益的逐类型系数。于是 \(\Gamma w\ge0\) 恰好表达全部真实 SPE 偏离约束。令 \(c\) 为实际根覆盖系数，\(o\) 为比较主题并集系数。

一种充分的完整形式证明是：对每个上述 \(\sigma,T_1,\ldots,T_m\)，构造

\[
2c-o=\Gamma^\mathsf T\lambda+r,\qquad \lambda\ge0,\quad r\ge0.
\]

与 \(w\) 相乘即得 \(2W\ge|\bigcup_iT_i|\)，再取最优比较元组。存在这样的证书仍待证明；不能循环用待证半覆盖和 Farkas 引理宣称它存在。还可自由使用不同的不变量、归约、交换、表示或直接覆盖证明。

[完整策略锥](../current/customer_attraction/strategy_cone.md)给有限证书合同；[末回复运输](../current/customer_attraction/terminal_reply_transport.md)和[平局商空间](../current/customer_attraction/terminal_tie_quotient.md)提供给定证书的提升。真实末层行可重构，早期误差仍须共同支付；固定早期乘子提升已失败，不能把这个限制扩大成一般不可能。

## 可选充分桥：聚合静态安全值

对固定前缀客户负载 \(b\)、剩余人数 \(r\)，定义

\[
v_r(b)=\max_{p\in\Delta(\mathcal S)}
\min_{B\in\mathcal S^{r-1}}\sum_{a\in\mathcal S}p_a
\sum_{x\in a}\frac1{b_x+1+\operatorname{load}_B(x)}.
\]

静态竞争组合 \(B\) **不观察查询抽样** \(a\)。[已证安全值下界](../current/customer_attraction/oblivious_security.md)为
\(v_m(0)\ge\operatorname{OPT}_m/(2m-1)\)。因此

\[
W\ge(m-\tfrac12)v_m(0)
\]

足以推出半覆盖。这是可能比主目标更强、也可能为假的候选桥，不是必须沿用的路线。更强的 \(W\ge m v_m(0)\) 也仍开放；逐人 \(u_i\ge v_m(0)\) 已被完整 SPE 否定。

[安全值链](../current/customer_attraction/security_chain_and_local_boundary.md)给真实路径上的精确恒等式
\(\sum_{i<m}D_i=W-mv_m(0)\)，但没有给需要的总债务下界。局部 \(D_i\ge0\)、弱局部 iid 漂移、节点内先平均全部偏离和规定静态核均有明确障碍。允许局部亏损、共同选取各历史乘子；一般聚合桥没有因此被否定。

## 已经排除的重复动作与证据边界

- 三/四人一般界、至多六极大半覆盖、指定完整策略锥已有资产，按原范围引用；不再继续特殊人数/目录的常数优化或逐规模补齐。
- 半覆盖的反例需要完整合法策略和所有真实历史的最优性；模板分离向量、松弛 LP 点、一个坏菜单或辅助桥反例都不够。
- [失败记录](../customer_attraction/FAILED_ROUTES.md)只限制写明的机制。新方法可直接尝试，探索不等审核；成熟结果按实际证明和攻击更新状态。
