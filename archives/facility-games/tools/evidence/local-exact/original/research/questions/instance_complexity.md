# Q-INSTANCE-COMPLEXITY：共同目录双设施实例最优倍率的计算边界

**状态：固定有理 $1\le a<\phi$ 的全局判定已有完整内部弱 NP 完全性证明；$a\ge\phi$ 由 SC-PHI-A 普遍可构造。** 数学范围沿用[规范模型](../current/model.md)：两家带标签设施、同一有限非空目录 $S$、有限正有理原子客户、显式覆盖、强制服务、线性实现负载成本、每个布局可独立指定精确独立混合客户 NE。前者由三地点 $a=1$ 和[五地点 $1<a<\phi$ 归约](../current/shared/five_site_exact_hardness.md)合并得到，均未获外部审稿和完整优先权核定。

令 $\mathcal N(s,t)$ 为布局的全部精确客户 NE，$m_1(s,t)=\min_{e\in\mathcal N(s,t)}L_1(e)$，$m_2$ 同理；$D_1(t)=\max_{r\in S}m_1(r,t)$、$D_2(s)=\max_{r\in S}m_2(s,r)$。定义

$$\alpha^*(I)=\min_{(s,t)\in S^2}\min_{e\in\mathcal N(s,t)}\inf\{\alpha\ge1:D_1(t)\le\alpha L_1(e),\ D_2(s)\le\alpha L_2(e)\}.$$

当在轨收益为零而对应威胁为正时内层值为 $+\infty$；二者均零时该坐标不给约束。这个量是**允许完整精确续局选择的实例最优倍率**，不是固定菜单或单张达到证书的值。

## 可判别目标与已知边界

1. 原问题——对每个事先固定的**有理** $\alpha\in[(1+\sqrt3)/2,\phi)$ 判定 $\alpha^*(I)\le\alpha$——已由五地点新归约在内部证明层闭合为弱 NP 完全。恰三或四地点的同段分类、或把 $\alpha$ 作为输入时的统一复杂度，是不同的新问题；固定 $\alpha$ 的预处理不能默默当作输入均匀的多项式算法。
2. 若研究输出 $\alpha^*(I)$，明确是精确分数、代数数还是仅作比较 oracle，并证明所需位复杂度。局部两设施支持区间给有理端点，不能因此省略全局取极小的证明。
3. 原参数 $\kappa=\max_{s,t\in S}|C_s\cap C_t|$ 的指数依赖已由[同址正规形](../current/shared/instance_complexity_barriers.md)改为仅对 $\kappa_{\ne}=\max_{s\ne t}|C_s\cap C_t|$ 指数。[三地点归约](../current/shared/three_site_exact_hardness.md)和[五地点归约](../current/shared/five_site_exact_hardness.md)都有无界异址交叠；二者均显式守卫全布局，不能只引用局部 `LOCAL-HARD`。更细的参数下界仍开放。

按[现行登记](../current/claims.md)，SC-PHI-A 多项式时间输出一个 $\phi$ 达到证书；EXACT-KAPPA 在指数参数时间内求实例最优。原论文对更广的一般设施数输入给出低于 $\phi$ 的 NP 完全性；它的设施数/目录范围不能直接推出此处两设施共同目录的困难性。只改程序常数、添加无最优性语义的证书或增加有限求解样本，都不达到本题门槛。

**本轮已知边界：**固定有理 $\alpha$ 的肯定实例有多项式位长的在轨及逐偏离 NE 证书，故本类 $\mathrm{DEC}_\alpha\in\mathrm{NP}$；原论文对更广输入也指出邻近布局证书的 NP 成员性，不把它包装为新结论。$\alpha^*$ 是可达的有理数。三地点正整数归约对 $1\le\alpha<\sigma$ 给匹配 NP 困难，五地点正整数归约对每个固定有理 $1<\alpha<\phi$ 给匹配困难，整数权又有伪多项式算法。至多两个共同地点必有精确 SPE；异址单交叠且至多两种 reach 也必有精确 SPE，但[五客户例](../current/shared/instance_complexity_barriers.md#4-两种-reach-并不足以去掉单交叠假设)说明不能删去交叠条件。[小目录阈值阶梯](../current/shared/small_sparse_catalogs.md)对异址单交叠给最多三、四、五地点分别 $\sqrt2,\sqrt[3]4,\phi$ 的尖锐普遍因子。

**已经履行的归约义务：**五地点证明对固定 $1<\alpha<\phi$ 控制全部 25 个带标签布局、八个在轨偏离和所有合法精确客户 NE。三地点旧守卫在 $\alpha\ge\sigma$ 的负私有预算仍是其作用域内的障碍；五地点证明改变了覆盖身份并保留宏客户，使 [原子粒度界](../current/shared/atomic_granularity.md) 的必要条件不构成反例。固定 $a>1$ 的 NO 实例须含异址宏原子，这一限制仍可用于攻击未来归约。

**下一阶段：**对新五地点证明进行外部独立审稿与逐定理优先权核查；数学新题须重新固定精确范围，例如恰三/四地点高倍率判定、随输入变化的 $a$、或与伪多项式算法配套的参数近似。此前旧三地点公式的失败机制仍载于[失败路线](../../FAILED_ROUTES.md)，不应重复微调。
