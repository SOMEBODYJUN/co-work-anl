# 统一低泄漏锚定时钟预算的普适次数障碍

## 精确命题身份

**ID/version。** `WC-UNIFORM-CLOCK-BUDGET-BARRIER-v1`。

**中文数学名称。** 统一低泄漏锚定时钟预算的普适次数障碍。

**Exact Statement / Objects / Domain / Quantifiers。** 任取 MODEL 中的有限两动作游戏 G，玩家数 n≥3、正实权 w_i，费用为次数至多整数 p≥0 的非负系数多项式；任取实数 α≥1。假设某个玩家顺序的同序双轮翻位全部为严格 α 改善。按该顺序把玩家标为 0,…,n−1，0 为锚点。记

\[
 R=\frac{\max_i w_i}{\min_i w_i},\quad
 L=\binom{n-1}{2},\quad
 B\ge\max_{s,i} C_i^G(s),\quad
 \eta=\min_{\text{环边 }s\to t\text{，移动者 }i}
       \{C_i^G(s)-\alpha C_i^G(t)\},
\]

\[
 \delta=\max_{1\le i<j\le n-1}
 \left(1-\frac{\min(w_0,w_i,w_j)}{w_0+w_i+w_j}\right).
\]

对每个整数 D≥1，只要它满足现行编译器的**统一低泄漏预算**

\[
 \delta^D\le\frac{\eta}{4\alpha^2BL}, \tag{U}
\]

则令 q=max{p,D} 后有

\[
 R>\alpha,\qquad
 D>(R+1)\ln\frac{4\alpha^2BL}{\eta}
 \ge (R+1)\ln(4\alpha^2L)
 >2(\alpha+1)\ln(2\alpha), \tag{1}
\]

\[
 \boxed{\quad\frac{\alpha\ln q}{q}
       <\frac{\alpha}{\alpha+1}<1.\quad} \tag{2}
\]

事实上式 (2) 对每个实数 q≥D 都成立；因此它也适用于实际输出最高次数 d_out≥D，而不依赖 p 是否虚高。这里 B 可以取严格大于实际最大值的已知统一上界。任意玩家顺序、任意被选为首位的锚点均覆盖。零费用、空动作和保留资源完全采用 MODEL，不作成本比值或 0/0。

**Assumptions / Definitions / Scope / Conclusion。** 双轮环、B、η、δ、L 与[锚定全状态编译器](anchored_cycle_lock.md)相同。(U) 是该编译器使用的保守充分条件；本命题覆盖满足它的全部输入和全部整数 D，不只覆盖公式中最小的 ceil。因而不论怎样随 α 改换输入游戏、权重、锚点或人数，使用 (U) 得到的 q 都不能使 α ln q/q 无界；该预算不能建立唯一题目的严格否定。q 是声明的编译次数 max{p,D}；每个新增正单项式具有次数 D，因此实际输出次数至少 D。

**Dependencies。** `WC-R3-DENSE-LOCAL-v1` 的严格 R 有限改善性质、MODEL 的非负成本及有限状态、锚定编译器参数定义与 (U)、初等对数不等式。编译器的全状态结论可用于解释此障碍，但不是不等式推导中的额外假设；不导入文献的均衡存在定理。

**Evidence / Counterevidence / Objections / Status。** 下文给一般证明，配套独立重构攻击和两份标准库精确审计。Status 为 complete budget-obstruction proof; independently reconstructed and exactly audited; unrefereed。Truth 仅指 (U) 的次数效率；Value 为封闭一条输入调参路线并明确重试条件；Novelty 未认证；Mechanism 为权比有限改善性与最坏三元泄漏的耦合；Ambition 保持全类匹配上界问题 OPEN。实际更小 D、非统一幅度/次数、任意非负多项式时钟、不同触发架构均不由本文否定。

## 一、严格改善环强迫全局权比超过倍率

[资源局部窄权带证明](weight_bands/README.md)的 `WC-R3-DENSE-LOCAL-v1` 不只说明 R-PNE 存在，还给每条严格 R 改善都严格下降的有限实势。核对其适用条件：每个资源的潜在使用者是全体玩家的子集，所以潜在用户权比至多全局 R；所有系数非负；多项式次数、人数及策略数不另受限。恒零费用、空策略和偏离前后保留资源也已由势差恒等式覆盖。

若 α≥R，则任一严格 α 改善满足

\[
 C_i^G(s)>\alpha C_i^G(t)\ge R C_i^G(t),
\]

其中第二步用到目标成本非负。于是整个严格双轮环都严格降同一个有限实势，回到起点不可能。因此

\[
 R>\alpha. \tag{3}
\]

这一步必须用**全边有限改善性**，不能只从 R-PNE 存在推出无环。本文使用的是原证明中明确给出的更强性质。

## 二、任意锚点都无法避开极端权比

令 m=min_i w_i、M=max_i w_i=Rm。锚定三元族必含一个同时包含全局最小权和最大权玩家的三元：若锚点不是这两名玩家，就取它们与锚点；若锚点是其中一名，n≥3 允许补任意第三名。由 (3)，R>1，极小和极大玩家可取为不同玩家。

该三元第三个权重至少 m。因此三元总重 W≥M+2m，三元最小权恰为 m，给

\[
 \delta\ge1-\frac{m}{W}
 \ge1-\frac{m}{M+2m}
 =\frac{R+1}{R+2}. \tag{4}
\]

不要求极端权重有多名玩家重复出现。正权及有限非空三元族也给 0<δ<1。

## 三、预算联立得到次数下界

严格环及非负成本给 0<η≤B，特别地 B>0；n≥3 给 L≥1。令 A=4α²BL/η≥4。对 (U) 取对数，方向为

\[
 D\ge\frac{\ln A}{\ln(1/\delta)}.
\]

由 (4) 以及对 x>0 的严格不等式 ln(1+x)<x，

\[
 \ln(1/\delta)
 \le\ln\left(1+\frac1{R+1}\right)
 <\frac1{R+1}.
\]

分子 ln A>0，因此

\[
 D>(R+1)\ln A
 \ge(R+1)\ln(4\alpha^2L)
 >2(\alpha+1)\ln(2\alpha).
\]

最后一步使用 R>α、L≥1 和 ln(2α)>0。这证明 (1)，且不依赖任何浮点 ceil。

## 四、对全部实数倍率的归一化上界

设 t=2(α+1)ln(2α)。对 α≥1，ln 2>1/2 给 t>α+1。函数 α−ln(2α) 在 [1,∞) 非减，且在 1 为 1−ln2>0，所以

\[
 \ln(2\alpha)<\alpha,\qquad
 t<2\alpha(\alpha+1)\le4\alpha^2.
\]

于是

\[
 (\alpha+1)\ln t
 <2(\alpha+1)\ln(2\alpha)=t.
\]

函数 f(x)=x−(α+1)ln x 在 x>α+1 严格递增。由 q≥D>t>α+1，

\[
 q-(\alpha+1)\ln q>t-(\alpha+1)\ln t>0.
\]

除以正 q，再乘 α/(α+1)，得到 (2)。该证明直接包括 α=1，无需假定 α 很大或借助 x>e 的分段单调性。

若某族满足 (U)，则在每个输出次数 q 上 α<q/ln q；特别地这些无 α-PNE 实例不能仅凭其 α 非存在证书，给出无 (Cq/ln q)-PNE 的实例，C≥1。没有较小倍率均衡不蕴含没有较大倍率均衡。

## 五、失败机制与可重试条件

尝试机制是把近 p 改善环送入现行统一低漏编译器，再以编译后的次数 q 声称超出 q/ln q 的全状态非存在。其失败发生在联合参数约束：大的 α 强制 R>α，而同一个 R 迫使某锚定三元的 δ 接近 1；即使 η=B、L=1 的最理想预算也已要求 D>2(α+1)ln(2α)。单独改善 B/η、减少人数、换锚点或挑选别的输入环无法解除这个约束。

可回收资产为 (3)、无需重复极值的 (4)，及直接对全部 α≥1 的 (2)。本文不判定原游戏或实际输出的最优近似均衡倍率；也不证明 (U) 必要。下一次值得重试时，必须使用实际新旧时钟差、逐三元不同预算、别的时钟费用/拓扑，或新的全状态机制。不能仅再次优化本预算中的输入环。

## 六、核验合同与文件

- [独立重构与冻结攻击](../../reviews/weighted_congestion/ordinal_potentials/uniform_clock_budget_barrier_review.md)：审查者先只据精确候选重构，再阅读所列 SHA256 正文；覆盖 (3) 的全模型适用、任意锚点、全部实数 α 和上述范围限制。
- `tests/audits/weighted_congestion/cyclic_clone/verify_uniform_clock_budget.py` 与 `evidence/runs/weighted_congestion/cyclic_clone/uniform_clock_budget.json`：Fraction 直接算锚定 δ、逐幂二分最小预算 D、有理级数含余项包住 ln、复算真实三玩家输入；非随机。
- `tests/audits/weighted_congestion/cyclic_clone/independent_uniform_clock_budget.py` 与 `evidence/runs/weighted_congestion/cyclic_clone/independent_uniform_clock_budget.json`：独立参数枚举与有理对数包络；不把仅有 α<R 的抽象参数冒充真实输入游戏。

从仓库根运行两份脚本；它们输出 JSON 到 stdout 或显式独占新输出路径，不覆盖冻结记录。Python 版本、代码 SHA256、输入列表、精度和有限覆盖范围均写入实际 JSON。有限算术核验不替代第一至四节的一般证明。
