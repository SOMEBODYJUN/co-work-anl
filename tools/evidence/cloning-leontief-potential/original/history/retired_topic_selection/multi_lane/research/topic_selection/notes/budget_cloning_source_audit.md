# 克隆不变性：版本变更与坐标优化理论的覆盖边界

日期2026-10-20。对应[几何判别](budget_cloning_and_concave_geometry.md)和[coNP证书](budget_cloning_complexity_certificate.md)。

## 2. 原论文v1曾有更强且错误的cloning断言，现行v3已修订

**原始源一：** Becker–Fries–Greger–Segal-Halevi, arXiv:2509.08767v1，2025-09-10，§8 Condition(2)、Lemma8.2及其证明。

- Condition(2)要求从delta到严格更好delta'的任意内部线段点也严格更好；原文明确concavity蕴含它。
- v1 Lemma8.2据此声称一般cloning保持。
- 证明中先把改善移动缩至总L1距离≤2/D，再断言可由一个clone完成。这一步不成立：总移动小不保证所需移出资金都在同一clone的support中。

本轮三项目反例的u是凹且单调，outside线性utility也是凹。目标预算1/2拆成两个1/4 clones，outside预算1/2也可拆成两个1/4 clones。因此它**确实反驳v1 Lemma8.2的一般范围**，而不仅是反驳研究者自造强猜想。

**现行源二：** 同论文v3，2026-02-24，§8 Lemma8.2已改为linear、Leontief、binary symmetric separable strict concave/convex及l1等特定classes，用各class的forbidden-support结构重证；§8末提出一般utility分类问题。我们的反例**没有反驳现行v3**。文本修订本身不能证明作者不知道/知道哪一个反例，也不能把已撤回v1当当前公开定理覆盖。

准确链接：

- https://arxiv.org/html/2509.08767v1 （§8，Condition(2)，Lemma8.2 proof，尤其由L1小移动推出单clone可执行的一步）
- https://arxiv.org/html/2509.08767v3 （§8，Lemma8.2 proof及末尾开放方向）

## 3. 对cloning矩阵判别最接近的既有理论核查

### 3.1 Tseng2001：机制明确属于已知coordinatewise/global gap

P. Tseng, *Convergence of a Block Coordinate Descent Method for Nondifferentiable Minimization*, JOTA109(3):475–494, 2001。

已读原文§1及§3：期刊p476明确说明凸但不可微时coordinate descent会卡在非stationary点；p479定义coordinatewise minimum及regularity（equations(4),(5)）；Lemma3.1给smooth coupled term+separable nonsmooth terms的regularity充分条件。

将同utility clones的共同目标写为

`F((x_a))=−u(r+sum_a x_a)+sum_a indicator_{b_a simplex}(x_a)`，

cloned NE就是coordinatewise minima，合并最优就是full minimizer（simplexes的Minkowski sum为总预算simplex）。因此“不可微时不同blocks的subgradient不一致、光滑时共享gradient恢复全局最优”的**机制不是新发现**。本轮可微lemma和反例的核心优化现象必须以此降级。

尚未在已读位置看到：对输入u=min_R linear、所有r/预算/clone数的量词消除，active-cell识别、按R的2^R算法或该矩阵语言coNP归属。不能把“没有在这些页看到”写成新颖性确认。

作者存档全文：
https://www.mit.edu/~dimitrib/PTseng/papers/archive/bcr_jota.pdf

### 3.2 Dlask2020 / Dlask–Werner2021：active-face/cone识别方法同样有成熟源头

T. Dlask, *On Coordinate-Wise Minimization Applied to General Convex Optimization Problems*, KES/Procedia Computer Science176:1328–1337, 2020。已读Theorems1/2及Conclusion：对polyhedral constraints、convex differentiable objective，利用每个active constraint subset的feasible-direction cone，给更新方向族保证全局最优的必要充分条件；Theorems4/5处理box以及box+one equality。

T. Dlask and T. Werner, *Classes of Linear Programs Solvable by Coordinate-Wise Minimization*, 2021作者版本。已读Introduction、Theorem1、§3.2 Proposition1/2及§5边界：nonoptimal coordinatewise minima是基本现象；对2-in-row/bipartite-acyclic等矩阵类给全局最优保证，并用complementary slackness/constraint propagation解释。

这些论文没有在所读定理中直接陈述本矩阵universal cloning语言，但说明本轮active-cell枚举和共同最优性LP属于标准polyhedral优化工具链。**即使我们的具体识别定理未被逐字写过，也不能据此认定它足以独立成稿。** 须继续检查能否由其一般active-face判别一行推出；本次没有完成所有后续引用追踪。

原始作者PDF：

- https://cmp.felk.cvut.cz/~dlaskto2/papers/Dlask-KES2020.pdf
- https://cmp.felk.cvut.cz/~dlaskto2/papers/Dlask-Werner-AMAI-2021.pdf

### 3.3 Coalition stability不能混同存在性与“每个NE都保持合并”

Brandt–Greger–Segal-Halevi–Suksompong, *Coordinating Charitable Donations with Leontief Preferences*, arXiv:2305.10286v4，2025-10-10，§4.1 Lemma1和Corollary1（PDF p10）已有Leontief NE对所有coalitions的稳定性。因此Leontief这一个positive class已经远强于cloning保持，不能再算本轮新类。

Kukushkin, *Strong equilibrium in games with common and complementary local utilities*, MPRA55499（2014预印本；2017期刊题名含Nash），§2模型、§3–6的acyclicity/existence及minimum aggregation边界已定位。其“在结构假设下存在strong equilibria”不自动说明每一个NE都是strong，也不直接给本输入A上的universal识别。因此该类文章相关，但不能不核量词便当覆盖或不覆盖。本文未逐行重构其全部定理证明。

- https://arxiv.org/pdf/2305.10286 （§4.1 Lemma1/Cor1）
- https://mpra.ub.uni-muenchen.de/55499/1/MPRA_paper_55499.pdf

### 3.4 本次搜索的诚实结论

cloning/merging/aggregation/concave nonsmooth/coalition关键词检索未找到直接陈述本有限矩阵判别及FPT/coNP上界的一手来源。但最主要机制和generic active-face工具明显已有成熟理论。检索不充分不能当新颖性证书；应把N3保留为“已具完整小算法/证书，须进一步找结构或复杂性差额”的候选。
