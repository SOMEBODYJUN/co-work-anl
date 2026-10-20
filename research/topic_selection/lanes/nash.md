> 当前统一编号NA01–NA06。N7并入AT03，不另计；NA02已有明确Fisher覆盖而淘汰。最终判断见[候选比较](../BATTLE.md)。

# Nash/动态/选择：第二轮独立候选卡 v1

2026-10-20。重新选题；不是旧UM主目标。这里给7个有不同承重结构的候选。A=作者原文明确开放问题，B=作者明确建议方向，C=我们派生的精确限制/idea。**作者提出一个宽方向，不表示下面限制题是作者原题。** 不给成功概率或虚假精确评分。网页核查截至本日期，未检索到覆盖不等于确认开放。

## N1 / PS-CAC-v1：cactus上的随机best response

**精确问题（C，附着A）**：无权player-specific singleton congestion game；每个玩家只能选两个资源，以资源为顶点、玩家为边得到简单cactus图；每条资源上的每名玩家成本关于人数严格增加、无平局。每步在当前不满意玩家中均匀选一人作best response。是否存在对所有初态/成本序均成立的n^{O(1)}期望到达NE界？先只看两个环共享一个顶点，其余任意挂树。这里n=玩家数；需明确计数的是实际改善步，而非抽到满意玩家的空步。

**原始文献与位置**：Ackermann–Röglin, *On the Convergence Time of the Best Response Dynamics in Player-specific Congestion Games*, arXiv:0805.1130，§1 Conjecture1、§3 trees、§4 circles、§5 branching-token construction。原文Conjecture1是一般游戏存在superpolynomial随机收敛例的A，cactus版本是C。

**Paper Fact/已覆盖**：树上任意BR序列O(n²)；单环上随机BR期望O(n²)。一般存在短BR路径不意味着随机路径短。原文§5说明token数在分叉图可增长，但没有完成其猜想的严格下界。已查2024–2026及cactus/随机BR关键词，没有找到一手后续判定；**一般猜想的最新状态尚未穷尽核实**。

**工具内化/toy**：单环中overload/underload token像随机游走并消灭；共享割点可能复制/吸收token，破坏“token数单调”。先精确建figure-eight有限Markov链，分析一个割点出入的regeneration cycle，不能只跑平均步数。

**最低完整成果**：两个环+任意挂树的统一多项式界，或同一自然图类的显式superpolynomial下界及可核验机制。单个六玩家循环或Monte Carlo增长不是完整成果。主目标cactus全类；伸展以cycle rank参数给FPT期望界或阈值。

**最强objection**：旧§5的复制gadget可能已经是cactus，读图/严格图类核查可能直接改变题目；若只需逐块套单环游走，成果也可能太直接。下一动作先把§5图的每条边列出，核查是否有共享两顶点/多条独立路径，随后才设计算法。

**当前裁决**：可立即判别但不宜默认主攻。训练价值：随机过程、吸收链与离散动态。

来源：https://arxiv.org/pdf/0805.1130

## N2 / BA-WL-v1：weighted Leontief的binary-bit多项式精确NE

**精确问题（A）**：预算b_i为正有理数、总和1，二进制输入；每人utility `u_i(delta)=min_{x:v_ix>0} delta_x/v_ix`，v_ix非负有理且每人至少一项正。输出精确有理NE profile，时间多项式于全部输入位长，不能按共同分母D复制D个玩家。

**原始文献与位置**：Becker–Fries–Greger–Segal-Halevi, *Efficiently Computing Equilibria in Budget-Aggregation Games*, arXiv:2509.08767v3（2026-02-24），§5 Theorem5.3为equal budgets的poly；§8 Theorem8.3为cloning的pseudo-poly，紧随其后的明确open question是weighted尤其Leontief能否poly。这是A；**equal-budget Leontief已经解决，不能重列为题目**。

**机制与toy**：NE由每人只向critical projects支出刻画；固定critical sets后是有理LP，因此即使预算有不同位长，存在多项式位长证书。难处是找到critical sets，而非存在性。equal-budget证明用几何平均产品level set的强分离；不同有理指数直接清分母会产生巨大次数。

**最低完整成果**：任意二进制预算的算法及完整bit complexity，或固定两种/常数种budget数值的真正poly算法（指数不能依赖其分母数值）。主目标原A；伸展组合/强多项式算法。固定预算分母是常数的情形已被cloning直接覆盖，不能作保底贡献。

**本轮试攻（尚非证明）**：考虑weighted log-Nash凸规划 `max sum_i b_i log u_i`。梯度b_i/u_i有理；若先用一般凸优化把目标逼近到2^{-poly}，再用强凹性和最优utility的多项式位长做有理重构，也许可绕开“巨大指数精确乘积比较”。应详细证明：(i)正utility下界与有界domain；(ii)强凹常数只造成poly的log条件数；(iii)近似优化的bit复杂度；(iv)唯一utility重构后通过LP恢复delta/profile。**未核验Jain框架/现有市场算法是否已直接给出，因此不能称已解原A。**

**最强objection**：这可能是标准凸规划+rational recovery的直接推论，作者/后续已处理；若确实只需两页现成定理，作为20天项目可能太小。另一方面，若需精确比较指数乘积而没有可用距离界，就会卡在隐藏算术复杂度。下一动作是把前述四项写成完整位长引理，不能继续只写“用ellipsoid”。

**当前裁决**：原题真实、范围具体，优先做完整证明核查；与均衡势数值不同，不靠一般PPAD大题下注。优化理论训练价值高。

**最终同日覆盖淘汰更新**：本卡上面的优先建议已失效。独立核到Tao–Zheng arXiv2511.04572v2/STOC2026 §3 Theorem2及Leontief dual-linear公式；结合Brandt等NE↔Lindahl和Orlin2010 exact linear Fisher，weighted问题已有直接理论覆盖。Fisher归约的零价、same-v、binary-bit和actual spending profile接口均通过独立攻击。**不再主张其为可做的新公开问题。** 见 `FINAL_SOURCE_AND_INTERFACE_AUDIT.md`§4；保留原卡作为审查轨迹。

来源：https://arxiv.org/html/2509.08767v3 （§5、§8）

## N3 / BA-CLONE-v1：polyhedral concave utility的cloning不变性分类

**精确问题（C，源A）**：给有限非负有理矩阵A，utility `u(delta)=min_r a_r·delta`。对所有预算、所有将一个u玩家拆为相同u的有限clones、所有外部玩家策略环境，是否cloned game的任一NE合并clones后仍为NE？寻找必要充分的active-gradient/最小禁形刻画及有效识别。明确“任意外部环境”可等价固定外部总分配；与是否存在某个可合并的NE是不同量词。

**来源位置**：同一Becker等v3 §8 Lemma8.2后明确问其cloning lemma适用于哪些utility的分类；这是一般A，我们polyhedral限制是C。

**实际试攻**：`CLONING_AND_SEPARABLE_TOYS.md`已完成3资源、2线性分支、两个预算1/4 clones的精确凹且单调反例。原NE效用5/4，合并为预算1/2玩家后可增至3/2。`cloning_certificate.py/json`用Fraction作10302个网格策略核验；全连续策略最优性由正文的线性上界证明。另已证明所有在当前总分配可微的凹utility保持cloning，靠共享gradient的KKT。

**机制**：不同clones可分别被不同active subgradient锁住，合并后跨支持的协调方向却改善。这解释Leontief的特殊结构，而不仅是列出一个人为反例。分类应考察active faces的normal cone是否存在一个公共supporting gradient能同时认证所有clone支持。

**最低完整成果**：R=2、m任意的必要充分分类+polytime识别+规范最小反例；若只给上面反例和可微lemma，**不足独立成稿**。主目标有限R全分类或参数算法；伸展将分类用于不用cloning的weighted NE计算。

**最强objection**：normal-cone条件可能只是重新表述定义；必须消去量词，输出可读的矩阵结构或有限禁形。另需查pseudo-concavity、aggregative game合并/coalitional deviations文献，不可因源论文没写便认新。

**当前裁决**：本轮最有信息量的分类toy之一，值得短期查重/两分支刻画；符合“分类优势由孔洞/禁形解释”的用户指导。

**v1后实质升级（同日）**：`CLONING_AND_SEPARABLE_TOYS.md`§5已给严格等预算clones的universal quantifier，以及 `2^R poly(m,R,input bits)` 有效识别定理：active cells枚举+共享gradient LP；R=2识别因此已完成，不再把它列作未解主目标。另得m=2总保持、m=3有反例的dimension边界。下一价值门应是一般R的tight complexity/可读结构或由分类导出新均衡算法，并查重coalitional local maxima/clone aggregation invariance。

来源：https://arxiv.org/html/2509.08767v3 （§8末）

## N4 / BA-ORDGRAD-v1：非binary可分偏好的log-gradient凸势分类

**精确问题（C，源B）**：玩家预算任意、`u_i(delta)=sum_x v_ix f_i(delta_x)`，v_ix>0。刻画哪些自然的player-specific递增凹f_i族，使NE等价于一个全局凹规划，且给输入表示与近似NE计算的bit保证；首先研究 `f'_i(t)=a_i g(t)^{b_i}`，a_i,b_i>0、g递减。

**来源**：同一Becker等v3 §9建议把binary symmetric separable utilities扩为nonbinary valuations。这是B；本精确积分接口是C。

**本轮实证/证明**：共同f_i=f的正valuations子类，已在 `CLONING_AND_SEPARABLE_TOYS.md`证明NE恰为

`max P=sum_x integral_0^{delta_x} log f'(s)ds +sum_ix x_ix log v_ix`

的global maximizers；P凹，aggregate唯一。关键不是“存在势”这个名词，而是原utility坐标边际与P坐标边际为严格单调的log变换，simplex KKT完全相同。player-specific log derivatives可用正仿射变换统一时也有同一接口。

**最低完整成果**：一个严格更广且可识别的f_i分类，带算法及结构之外的最小坏例。共同f子类的上述两段KKT证明是地基，**不能单独称足够论文**。主目标最大可积/ordinal-gradient类；伸展允许不同项目函数f_ix并刻画四格curl/图环兼容性。

**最强objection**：可能完全是已知ordinal potential/regular potential或Fisher市场的标准重写。必须先比Jensen的aggregative potential框架及公共品市场论文，不可把相同凸规划换名。oracle、log系数和精确求解也不能被隐藏。

**当前裁决**：高优先查重，若被覆盖就保留为排除非binary方向“表面空白”的工具，不默认主项目。

来源：https://arxiv.org/html/2509.08767v3 （§6、§9）

## N5 / BA-L1-SELECT-v1：非凸均衡集合上的Pareto/社会成本选择

**精确问题（C，源B）**：有理peaks p_i∈simplex与有理预算b_i，utility为负l1 distance。在所有NE profiles中，最小化加权社会disutility `sum_i a_i ||delta-p_i||_1`；或者判定是否有NE达到阈值K。先正权a_i=1、equal budgets，目标是在全m类证明poly算法或NP-hard，再给一个自然结构的精确算法。

**来源位置**：Becker等v3 §7 Lemma7.1为“只向不过供项目支出”的NE刻画；Proposition7.3给equilibrium distributions非凸例；Theorem7.4给任意NE的O(mn log n)算法；§9明确建议按Pareto efficiency等条件select equilibria。这是B，具体社会l1最优是C。

**已覆盖/最小toy**：任意NE已poly，不可重复。作者Example7.2的两个NE中点并非NE，故直接凸组合/convex feasibility会输出错误。固定m可枚举每个delta_x相对所有peaks的threshold cells，再用流/LP处理支出支持与分段线性目标，给(n+1)^{O(m)}时间；这个简单XP本身不是贡献。

**最低完整成果**：选择问题的tight复杂性+一个有内容的参数/近似边界，如project–agent approval/threshold graph的树结构，或hardness已经发生在每项目只有3个不同peak值。主目标精确selection；伸展Pareto maximal NE的高效输出和PoA。

**最强objection**：若选择Pareto最大只需优化任意正linear utility组合，可能标准凸分析直接解；但这里equilibriumset非凸，必须验证。也可能公共品fair mixing已有完整选择理论覆盖。下一动作：写阈值cell的精确flow模型，独立穷举3–4项目小例，检验作者的顺序greedy是否能实现全部最优selection，随后才做归约。

**当前裁决**：适合OR优化题风格，真实差额清楚，优先于无结构的一般均衡难题；但尚未有hardness/算法核心。

来源：https://arxiv.org/html/2509.08767v3 （§7、§9）

## N6 / CG-PAIR2T-v1：两类pair-strategy游戏中求任意PNE

**精确问题（C，源A）**：无权拥塞博弈、所有策略均为2资源子集、成本非负非降（先线性有理）。玩家分为两个types，每type共享一个显式列出的pair-strategy family。求任意PNE是否polytime？必须区分global minimum potential与local minimum/NE。先只允许每type策略family是某图的全部edges。

**原始文献/位置**：Bilò–Fanelli–Gourvès–Tsoufis–Vinci, *Minimizing Rosenthal's Potential in Monotone Congestion Games*, arXiv:2408.11489，Table1、Theorem2（symmetric size2 global min可poly），Theorem3（general size2 global min NP-hard）、§6 Conclusion（PDF p13）明确把nondecreasing size2 general任意PNE复杂性列为未来问题A。两type限制为C。

**机制/toy**：一个type的全局势最小化可化为matching；两个type引入资源使用与type配额同时耦合。不能把globalmin NP-hard当作PNE NP-hard，也不能把有exact potential当poly。适合先研究matching构造的augmenting circuits怎样同时尊重两类玩家。

**最低完整成果**：两type类的poly PNE算法及位复杂度，或对同一受限类的PLS-hardness。若只在两type资源不相交/共享公共必选资源上成功，退化为singleton或独立matching，不够。主目标两类pair families；伸展固定t类型参数。

**最强objection**：一般size2原A可能已有2025–2026后续解决，需精查引用；两类globalmin问题可能接近带颜色/配额的exact matching，不能无证断言标准matching可解。也可能某个PLS归约本来只有两类strategy families。下一动作逐行重构Theorem2 matching reduction并保持type标签，找第一处不闭合的配额约束。

**当前裁决**：比一般PPAD问题窄且有源头，完整结果可独立；但需要先完整核查hardness现状，不能仅因题面短推荐。

来源：https://arxiv.org/pdf/2408.11489 （§3、§6）

## N7 / FT-SMOOTH-v1：有限weight近似势到smoothed实际动态

**精确问题（C）**：weights{1,2}、非负二次成本的非零coefficients作bounded-density噪声，策略显式或最短路可BR；在原游戏上按 `(64/59)(1+epsilon)`-improvement运行指定动态，证明expected poly步数并给bit复杂度。尝试允许共同/相关扰动保持单调，或只有一个全局噪声源。

**源论文**：Giannakopoulos, *A Smoothed FPTAS for Equilibria in Congestion Games*, EC2024 / arXiv:2306.10600v3，Theorem1、Lemma1、§3.3.2；原定理处理unweighted exact-potential games，不直接声称weighted。然而其截断倒数分析一旦有polynomial-range近似势通常可直接迁移。

**实际素材**：本轮 `UNIVERSAL_SCALING_ATTACK.md`已给全n近似势64/59，且边际范围有共享type scaling。第一轮已有“边际density即可、不需独立”的union-bound lemma，所以仅把这两条接起来很可能是短推论。

**最低完整成果**：更自然且原框架不能直接覆盖的低维相关噪声模型，或全n最优type-scaled势与锐利动态界的组合。单纯把64/59嵌进原smoothed证明不够独立。

**最强objection/裁决**：直接黑盒推论风险极高；列入降级储备/附属，不作20天主项目。可服务更强势理论的算法落点。

来源：https://arxiv.org/html/2306.10600v3

## 本轮比较结论

不要把7张卡累加成7个研究贡献。已完成的实质增量是：原37/33主候选被自由type scaling严格支配；固定{1,3}势分类被HKM2011 Proposition3.4显著覆盖；cloning的一般凹性猜想有精确反例；非binary共同可分凹utility有直接KKT凸规划，所以不能把“非binary”三个字当新难点。

若只按本轮证据安排下一次研究：先给N2完整位长证明尝试与N3两active branches分类，同时查N4市场/ordinal potential覆盖；N1和N6先完成原图/归约的覆盖检查再投入。N5需要一个selection核心而非更多综述。N7只能作附属。
