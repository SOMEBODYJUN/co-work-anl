# 两尺寸背包：固定激活概率均匀化与拆分方向的真实障碍

**SEL-KNAPSACK-FIXED-X-OBSTRUCTION-v1**。状态：完整局部反例证明、Fraction证书；新颖性未确认。来源为Sergeev的背包相关间隙研究启发的C类工具问题。它不反驳一般背包CRS猜想，也不反驳同时改变激活概率的全局极值归约。

## 1. 对象与近年基线

物品独立激活，概率为固定向量x；尺寸s，权重w非负。自然LP只要求Σs_i x_i≤1。记独立激活集合为R，目标ratio为

\[
\rho_x(w)=\frac{\mathbb E[\max\{\sum_{i\in I}w_i:I\subseteq R,\sum_{i\in I}s_i\le1\}]}{\sum_i x_iw_i}.
\]

仅在分母正时定义。自然LP域不能换成整数可行集凸包而不另立版本。

Paper Fact：Ma–MacRury–Stein, *Forward-backward Contention Resolution Schemes for Fair Rationing*, [arXiv:2502.09521v1](https://arxiv.org/html/2502.09521v1)，Theorem1.4已经给knapsack的1/3-selectable FB-CRS。其随机尺寸模型取尺寸s_i的概率x_i、否则∞就包含上述自然LP激活。因此“超过2020文献的.279”不是当前可立的普通CRS差额。不从该定理自动添加monotonicity。

## 2. 五物品精确反例

两件大物品尺寸a=7/10，三件小物品尺寸b=2/5。可行非空选择是一件大物品，或至多两件小物品；两类不能混选。取

\[
x=(3/5,13/50,17/100,17/50,23/50),\qquad
w=(2,2,1,1,2).
\]

自然LP消耗为99/100。逐个枚举全部32个独立激活集合，以有理概率计算最大可行权值，得

\[
\rho_x(w)=117253/187500.
\]

对任意选择的零权sub-support，如果同尺寸类的所有正权重统一，则其最小ratio为

\[
52726561/84062500,
\]

由(2,2,1,1,1)达到。两者严格差为237199/126093750>0。

### 为什么有限四种权重比已覆盖连续的类内统一向量

固定任意sub-support。设大物品正权为u、小物品正权为v。若v>0，利用齐次性令v=1，记r=u/v。每个激活集合的最优值为max(r·1_{至少一个大物品激活}, min(2,激活小物品数))。所以期望分子在r的区间[0,1]、[1,2]、[2,∞)内仿射；分母在这些区间也仿射且为正。仿射函数之比的导数符号固定，因此每段最小值出现在端点或无穷远极限。只需检查r=0,1,2,∞，对应代码的(u,v)=(0,1),(1,1),(2,1),(1,0)。所有32个sub-support同时枚举，零分母跳过。因此上述最小值不是只检查四个随意权向量的观察，而是全连续类内统一权重族的证书。

**Conclusion**：固定x时，“最坏权重总可在每个尺寸类内统一”这一承重引理为假。没有证明最优相关间隙的全局极值必须非统一，因为全局归约可能同时改变x。

## 3. 保持期望成本的Bernoulli拆分不总降低ratio

仍取a=7/10,b=2/5。一个大物品确定激活，两个小物品各以1/10激活，所有权重1。期望最优值为1+1/100=1.01，分母为6/5，期望尺寸消耗39/50。

将其中一个小物品拆成两个同尺寸同权重、各以1/20独立激活的物品。分母和期望消耗不变，但现在三个小物品至少两个激活的概率为

\[
1/10\cdot1/20+1/10\cdot1/20+1/20\cdot1/20
-2(1/10\cdot1/20\cdot1/20)=3/250.
\]

新期望为1.012，严格上升。于是“任意拆分总使ratio下降，最终Poisson最坏”的逐步证明方向不成立。没有排除另有可行的全局Poisson极值比较。

## 4. 证据、运行与回收

- [精确证书程序](../probes/gap_tools/exact_uniformization_counterexample.py)与[冻结结果](../probes/gap_tools/exact_uniformization_counterexample.json)：无seed，Python Fraction，32种激活×全部sub-support×4个完整极值断点。
- [探索LP](../probes/gap_tools/two_class_attack.py)与[冻结输出](../probes/gap_tools/two_class_attack.json)：seed20261020，SciPy/HiGHS浮点；60个fixed-x最坏权重LP，不能代替一般定理。

原研究脚本会写入同目录JSON；重现时复制到临时目录运行，保持已冻结证据不被覆盖。具体命令及hash见[实验清单](../probes/round2_manifest.json)。

回收的是一个精确方法边界与极值搜索oracle。只有找到新的全局不变量、允许改变x的严谨变换或自然受限类的完整锐界时才值得重开；不能继续沿本节已经反驳的固定x引理推进。
