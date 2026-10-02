# Q-INSTANCE-COMPLEXITY：共同目录双设施实例最优倍率的计算边界

**状态：固定有理 $1\le a<(1+\sqrt3)/2$ 已弱 NP 完全；更高但低于 $\phi$ 的全局判定仍开放。** 数学范围沿用[规范模型](../current/model.md)：两家带标签设施、同一有限非空目录 $S$、有限正有理原子客户、显式覆盖、强制服务、线性实现负载成本、每个布局可独立指定精确独立混合客户 NE。

令 $\mathcal N(s,t)$ 为布局的全部精确客户 NE，$m_1(s,t)=\min_{e\in\mathcal N(s,t)}L_1(e)$，$m_2$ 同理；$D_1(t)=\max_{r\in S}m_1(r,t)$、$D_2(s)=\max_{r\in S}m_2(s,r)$。定义

$$\alpha^*(I)=\min_{(s,t)\in S^2}\min_{e\in\mathcal N(s,t)}\inf\{\alpha\ge1:D_1(t)\le\alpha L_1(e),\ D_2(s)\le\alpha L_2(e)\}.$$

当在轨收益为零而对应威胁为正时内层值为 $+\infty$；二者均零时该坐标不给约束。这个量是**允许完整精确续局选择的实例最优倍率**，不是固定菜单或单张达到证书的值。

## 可判别目标与已知边界

1. 对一个事先固定的**有理** $\alpha\in[(1+\sqrt3)/2,\phi)$，判定是否 $\alpha^*(I)\le\alpha$ 的复杂度是什么？低于该区间已有全局弱 NP 完全性；端点本身未解决。不要将固定 $\alpha$ 的归约误写成把 $\alpha$ 作为输入时仍统一多项式。
2. 若研究输出 $\alpha^*(I)$，明确是精确分数、代数数还是仅作比较 oracle，并证明所需位复杂度。局部两设施支持区间给有理端点，不能因此省略全局取极小的证明。
3. 原参数 $\kappa=\max_{s,t\in S}|C_s\cap C_t|$ 的指数依赖已由[同址正规形](../current/shared/instance_complexity_barriers.md)改为仅对 $\kappa_{\ne}=\max_{s\ne t}|C_s\cap C_t|$ 指数。新[三地点归约](../current/shared/three_site_exact_hardness.md)有无界异址交叠，恰需此参数增长；它显式守卫全布局，而不能只引用局部 `LOCAL-HARD`。更高倍率的参数下界仍开放。

按[现行登记](../current/claims.md)，SC-PHI-A 多项式时间输出一个 $\phi$ 达到证书；EXACT-KAPPA 在指数参数时间内求实例最优。原论文对更广的一般设施数输入给出低于 $\phi$ 的 NP 完全性；它的设施数/目录范围不能直接推出此处两设施共同目录的困难性。只改程序常数、添加无最优性语义的证书或增加有限求解样本，都不达到本题门槛。

**本轮已知边界：**固定有理 $\alpha$ 的肯定实例有多项式位长的在轨及逐偏离 NE 证书，故本类 $\mathrm{DEC}_\alpha\in\mathrm{NP}$；原论文对更广输入也指出邻近布局证书的 NP 成员性，不把它包装为新结论。$\alpha^*$ 是可达的有理数。三地点正整数归约对每个固定有理 $1\le\alpha<(1+\sqrt3)/2$ 给匹配 NP 困难，整数权又有伪多项式算法。至多两个共同地点必有精确 SPE；异址单交叠且至多两种 reach 也必有精确 SPE，但[五客户例](../current/shared/instance_complexity_barriers.md#4-两种-reach-并不足以去掉单交叠假设)说明不能删去交叠条件。[小目录阈值阶梯](../current/shared/small_sparse_catalogs.md)对异址单交叠给最多三、四、五地点分别 $\sqrt2,\sqrt[3]4,\phi$ 的尖锐普遍因子。

**下一道归约义务：**在固定 $\alpha\ge(1+\sqrt3)/2$ 仍控制**所有**候选在轨布局、对半同址及竞争异址逃逸。已有单硬边、AB/AC 各一名共有客户的三地点守卫在该阈值上 C 的私有权预算必为负；这只是覆盖模板的严格失败，不排除多重守卫或更多地点。固定 $a>1$ 的 NO 实例还须含有异址单体重 $w_i>(a-1)R_{\max}/(a+1)$，见[原子粒度界](../current/shared/atomic_granularity.md)。

**止损条件：**本轮的成功守卫已证明低倍率区间的全局困难性；其更高倍率参数预算由[失败路线](../../FAILED_ROUTES.md)精确排除。只有改变覆盖身份、客户结构、地点数或找到全局判定不变量，才值得继续冲击 $[(1+\sqrt3)/2,\phi)$；重复微调同一三地点公式已无信息价值。
