# Nash 计算与优化理论：六类候选、近期排雷与三个可核查切口

研究日期：2026-10-20。研究者已完整读取 USER_GUIDANCE.md 和 AGENTS.md；本轮是重新选题，不沿用 UM-TARGET-v1。仅写本目录，未操作 git、公屏或通信账号。

## 结论先行

这条子线不建议攻一般近似 Nash、一般三人精确均衡复杂性或“所有势博弈都快速”。独立审查后，六个异质候选中仅 **NASH-02（随机反馈下 RM+）** 保留为优先评估的主课题预候选，仍有明确的反方理由，不能视为已选定。**NASH-04已降为工具引理，不作为本轮主押候选**：原共享t构造本来就有constant pathwidth，局部化新增主要是去掉高degree apex，容易被视作remark级推论。NASH-01同时RM+的零初始化统一速率列为方法备选；本报告不为凑“前二”强行补一个主押。NASH-03的树宽Minty识别很可能只是现有LP/动态规划的自然推论；NASH-05仍偏大；NASH-06有价值但技术体系较远。

本轮最有用的排雷，不是宣布找到了新开放题，而是发现若干已经改变的边界：

| 旧直觉/旧开放问题 | 2026-10-20 的核实结果 |
|---|---|
| Minty 条件下 VI 能否获得 poly(log(1/ε)) 算法？ | 已被 Anagnostides–Farina–Sandholm–Zhang 解决；最新 v4 是 2026-10-02，FOCS 2026。弱 Minty 的小参数范围也已覆盖。 |
| 同时 RM+ 在势博弈是否收敛？ | ICLR 母文 v2 已覆盖同时更新；不能把 v1 的 alternating 限制当开放题。 |
| alternating RM+ 能否有界 regret？ | 2026-08 的公开稿 2608.17417 宣称已经解决；该稿后来被 arXiv Admin 因作者身份/affiliation 无法核实而撤回。撤回原因不是数学反证，故不能把其结果当已接受定理，也不能忽略其公开优先权风险。 |
| 两队各两人、队内协调/队间零和的 polymatrix NE 复杂性？ | Anagnostides–Panageas–Sandholm–Yan 2026-06 已给 PPAD-complete。 |
| path/star/caterpillar 的精确 graphical / polymatrix NE？ | Lucca–Irfan–Ortiz UAI 2026 已有新正结果，不能重提旧版 caterpillar 问题。 |
| COLT 2025 矩阵博弈 instance-dependent 样本复杂性是否没有新进展？ | Jiang–Zhang 2026 已用 LP resolving 推进，但其关键保证是 Gap(E[输出])，不能误读成 E[Gap(输出)] 或高概率 ε-NE。 |

## 来源与精确定位

只使用论文、作者公开稿或正式会议材料。下列 web ref 是本次检索的返回标识，便于 boss4 再打开核验；URL 是实际引用地址。

| 编号 | 原文、版本与位置 | URL / 本次 web ref |
|---|---|---|
| S1 | Anagnostides, Tewolde, Zhang, Panageas, Conitzer, Sandholm，*Convergence of Regret Matching in Potential Games and Constrained Optimization*，ICLR 2026；arXiv v2 2025-11-17。§2.2 算法；Thm 3.4、Cor 3.5、§3.2；§5 future research。正式作者 PDF §5 p.13。 | https://arxiv.org/html/2510.17067v2 ; https://emanueltewolde.com/files/RM%2BKKTConvergence.pdf ; refs `turn43view0`, `turn46view1`, `turn46view4`, `turn69view1` |
| S2 | Dewasurendra–Jayawardhana，*Self-Bounding Regret Matching+…*，2026-08 v1/v2；官方 v3 2026-09-24 撤回。v1 §2 Lemma 1/Thm 2、§3–4、§5 limitations。 | https://arxiv.org/abs/2608.17417 ; https://arxiv.org/html/2608.17417v1 ; refs `turn60view0`, `turn60view1`, `turn69view0` |
| S3 | Anagnostides, Farina, Sandholm, Zhang，*A Polynomial-Time Algorithm for Variational Inequalities under the Minty Condition*，v4 2026-10-02。Thm 1.5/4.7；§4.3 Thm 4.13；Prop 1.14；§6 complexity。 | https://arxiv.org/html/2504.03432v4 ; https://arxiv.org/abs/2504.03432 ; refs `turn5view0`, `turn8view2`, `turn78view3` |
| S4 | Anagnostides, Balcan, Fragkia, Sandholm, Tewolde, Zhang，*The Complexity of Equilibrium Refinements in Potential Games*，2026-02-11 作者稿。§4.5 Cor 4.9、Thm 4.10；Appendix C.1 Prop C.8/C.9；C.2 Thm C.10/C.11；§6 Question 6.1。 | https://emanueltewolde.com/files/EQRefinementPotential.pdf ; https://arxiv.org/abs/2511.03968 ; refs `turn5view1`, `turn8view4`, `turn101view0`, `turn101view1` |
| S5 | Adsul, Garg, Mehta, Sohoni, von Stengel，*Fast Algorithms for Rank-1 Bimatrix Games*，arXiv 1812.04611v4，正式期刊版本对应稿。§6 全路径；§8 指数多均衡；§10 Conclusions 中明确的 output-efficient / second equilibrium / smoothed-analysis 问题。 | https://arxiv.org/html/1812.04611v4 ; https://arxiv.org/pdf/1812.04611 ; refs `turn71view2`, `turn101view2` |
| S6 | Maiti，COLT 2025 Open Problem，pp.6230–6234；Maiti–Jamieson–Ratliff AISTATS 2023，n×2；Jiang–Zhang 2026，§2 定义、§3 支撑识别、§5 Thm 5.1/Cor 5.2。 | https://proceedings.mlr.press/v291/maiti25b.html ; https://proceedings.mlr.press/v206/maiti23a.html ; https://arxiv.org/html/2602.12513v1 ; refs `turn5view2`, `turn21search1`, `turn71view0`, `turn78view2` |
| S7 | Anagnostides–Panageas–Sandholm–Yan，*The Computational Complexity of Team Zero-Sum Games*，2026-06。摘要已明确 2v2、polymatrix、inverse-poly 精度仍 PPAD-complete。 | https://arxiv.org/abs/2606.16139 ; refs `turn41academia31`, `turn43view2` |
| S8 | Lucca–Irfan–Ortiz，UAI 2026 *Computing Exact Nash Equilibria in Graphical Games: A Geometric Approach to Paths, Stars, and Caterpillars*，正式摘要。全文 PDF reader 遇到 content-type 阻断，未把未读取的定理细节当证据。 | https://proceedings.mlr.press/v337/lucca26a.html ; refs `turn83view0`, `turn85view0` |

文献检索到当前日期；“未找到同定理”不等于新颖性认证。S2 撤回尤其要求进一步作者/数学核验；这里明确保留，而不把搜索摘要当有效定理。

## 候选总表

| ID | 精确切口 | 类型、母机制 | 当前处理 | 致命风险 |
|---|---|---|---|---|
| NASH-01 | 标准零 regret 初始化的同时 RM+，对有理多线性势，能否给参数统一的 O(ε^-2) best-iterate NE 界；先两人3×3及二元稀疏势。 | S1 工具突破；S2 的 forward-gain 自界工具迁移。 | 第三顺位；深挖了一个带大初始化的确定性小核。 | 大初始化结论太直接；零初始化常数可能依赖极小首激活量。S2 存公开优先权风险。 |
| NASH-02 | 有界无偏随机全信息反馈，交替 RM+ 能否以可计算 batch / confidence schedule 达到高概率 ε-NE；先二元二次势。 | S1 §5 明确提出 stochastic/bandit 下一步；噪声下恢复势记账。 | 第一顺位，仍 OPEN。 | 黑箱 batching 只重现通用随机梯度的量级，论文价值不足；固定噪声破坏精确记账。 |
| NASH-03 | 给定 bounded-treewidth polymatrix/局部因子博弈，精确识别 Minty 可行性，输出 anchor 或小支撑 strict aggregate-CCE 证书。 | S3 新视角/工具；把连续全称条件化成 pure-profile LP 分离。 | 低优先级基线；可当子引理。 | 很可能是 S3 Prop1.14 + 标准 bounded-treewidth welfare DP 的直接组合。 |
| NASH-04 | 本地化共享t给最大度6、pathwidth恰3的精度障碍；真正下一题是三次势treewidth≤2/Berge-acyclic等正类。 | S4 分类边界；复制变量 + 重复平方 gadget。 | 已降为工具引理，不作主押；通过独立内部数学审查。 | 原构造已有constant pathwidth；作者明言t只固定ε，局部化近remark级。 |
| NASH-05 | 非退化 rank(A+B)=1；参数 a 的不同值数 k 固定时，能否 output-polynomial 枚举全部孤立 NE或判定第二 NE。 | S5 显式问题的结构化切口；一参数 LP 轨迹与超平面求交。 | 远期备选。 | k=2 可能仍容纳指数轨迹；低秩不限制零和部分，难点未消失。 |
| NASH-06 | 有噪声可自适应查询的3×3零和矩阵，固定置信度下 ε-exploitability NE 的实例依赖最优采样，先 full-support 非退化类。 | S6 公开问题；LP 灵敏度 + information allocation。 | 有价值但跨学习统计体系；需另组主攻。 | 不能把 Gap(E[x]) 与 E Gap(x) 混淆；可能只做出已知 n×2 的重写。 |

## NASH-01 深挖：同时 RM+ 的精确 gap 与 regret-state 记账

**精确模型。** 有 n 个 simplex，X=∏ᵢΔ(mᵢ)，势 Φ 是有理多线性函数，梯度 L-Lipschitz。每步同时观察 uᵢ=∇ᵢΦ(x)，运行

\[
g_i=u_i-\langle x_i,u_i\rangle\mathbf1,\qquad
r'_i=[r_i+g_i]_+,\qquad x'_i=r'_i/\|r'_i\|_1.
\]

零向量时保留原策略。研究真实标准初始化 rᵢ⁰=0 的轨迹，目标是 maxᵢ BRGapᵢ≤ε 的一个实际迭代；不能把平均 CCE 当 NE，也不要求收敛到同一个精确 NE。

**Paper Fact。** S1 v2 已有 simultaneous 的 ε^-4/零初始化一般约束 ε^-8 类保证，§5 留有 regret-growth 问题。S2 v1 公布了更强单步记账及交替方向的 ε^-2，且其 §5 明确不覆盖一般同时更新；S2 官方撤回状态见上，既不能当有效已接受结果，也不能抹去其公开内容。

**我们新 idea。** 先不用 sharp √(m−1) 常数，只用范数凸性重新推导如下小核。它给一个可完成但可能不足以独立成文的正结果。令 q=r'−r、D=⟨x'−x,u⟩、R=||r||₂、s'=||r'||₁，则

\[
2s'D=R'^2-R^2+\|q\|_2^2,\quad
R'^2-R^2\ge\|q\|_2^2,\quad
R'-R\le\sqrt m\,D.\tag{A1}
\]

前两式用正部截断和 ⟨r,g⟩=0；末式由 R'−R≤⟨r'/R',q⟩=s'D/R'。又由

\[
s'(x'-x)=q-\langle\mathbf1,q\rangle x
\]

得到 ||x'−x||²≤4mD/R'。故若所有初始 Rᵢ⁰≥4mᵢL，利用 R 单调及 smoothness，有

\[
\Phi(x')-\Phi(x)\ge\tfrac12\sum_iD_i.
\]

记 ΔΦ=maxΦ−minΦ，则 Rᵢᵀ≤Rᵢ⁰+2√mᵢΔΦ=:Bᵢ，且

\[
\sum_{t<T}\sum_i \mathrm{BRGap}_i(x^t)^2
\le \sum_i(B_i^2-(R_i^0)^2).
\]

这是参数明确的 O(ε^-2) best-iterate 小核。**这是内部完整推导，未独立审查，未声称新颖。** 仅大初始化结果太容易从新记账导出，不能就此宣布论文目标完成。

**真正首个 proof obligation。** 在 r⁰=0、任意有理初始 x⁰ 下，控制低-state blocks 对 simultaneous cross term 的累计负贡献，界只允许多项式依赖 n,m,L,ΔΦ；不能隐藏 δ=min 首个正 regret norm。允许先反证：构造具有小有理系数、首激活 δ 极小且实际 hitting time 随 δ 增长的3×3势博弈。如果所有“坏常数”均为证明伪影，再争取 uniform ε^-2。

**玩具与可证伪测试。** `toy_checks.py` 对 m=2,3、r∈{0,1,2}ᵐ、u∈{−2,…,2}ᵐ，零态包含 uniform 与各顶点 fallback，共275+3750=4025个精确一步核查，A1 无反例。边界包含 clipping、零态及不截断。它不证明渐近速率；下一步应搜索两人3×3势、同时更新、任意非对称初始状态，测 hitting time 对首激活量的依赖。

**价值与反方。** 价值在于保留原 parameter-free、scale-invariant 更新，改善真实迭代复杂性；不是设计一个可被通用 gradient ascent 替代的算法。反方是结论可能只需一页证明，或者 S2 v2 / 未索引稿已覆盖；若两天内只得到大初始化推论，应停止把它列主课题。

## NASH-02 深挖：噪声下 RM+ 的势上升为什么失效

**精确模型。** 先限定 binary polymatrix exact potential game，最大度 Δ，局部 payoff ranges≤1，势可求值/梯度可采样。某玩家被激活时，给出全动作向量的无偏估计 \hat uᵢ，条件均值 uᵢ，条件次高斯噪声参数 σ²；不同动作可相关，但条件无偏。目标是在总样本数显式计费下，以概率≥1−δ输出一个实际 profile，其 max BRGap≤ε。先随机全信息；bandit 另立后续版本，不能混用。

**原文起点与类型。** S1 §5 明确列 stochastic/bandit 为下一步；这是“工具导向”的论文：把 regret-state norm 与 KKT gap 联系起来，而不是一个特殊博弈的算法。迁移价值要以保留 RM+ 优点和噪声记账的新机制评判。

**最小反例，已精确算。** 单玩家真效用 u=(1/2,0)，r=(1,0)、x=(1,0)，已精确最优。观测以各1/2概率为 (0,1/2) 或 (1,−1/2)，所以噪声逐坐标均值零、观测有界。第一分支使 r'=(1,1/2)、x'=(2/3,1/3)，真势变化−1/6；另一分支不动。故期望真势变化 **−1/12**，期望新 gap **1/12**。这不是不收敛反例，却严格否定“无偏观测 ⇒ 期望沿真势上升”这一常见错误推论。

**我们新 idea。** 不直接把随机项塞进确定性 A1。尝试显式分离 observed forward gain 与 true forward gain，用 confidence intervals 只在“可信正收益”时执行一次 RM+，否则增加 batch；或者保留 vanilla 轨迹，构建“势 + noise energy + state norm”的补偿 Lyapunov。前者可证性较好但可能过于常规；后者若成立更有方法价值。固定σ、固定batch、vanilla clipping 的长期行为必须独立处理。

**第一个 proof obligation。** 证明在条件估计误差 ||\hat u−u||∞≤η、且 current true gap≥ε 时，一次可信更新满足

\[
\Delta\Phi\ge c\,\mathrm{gap}^2/(\|r'\|_1+1)-\text{显式噪声罚项},
\]

并且噪声罚项可以按总样本预算加和。只证明 batch 越来越大从而渐近收敛不够；要和 stochastic gradient/Frank–Wolfe 的现成界比较。如果达到相同复杂度且无计算/调参优势，降为附录。

**可解性与危险障碍。** 确定性单步结构非常具体，二元一维可以手算，噪声反例能检验任何错误 Lyapunov。最危险的是 positive-part 与随机观测相关，不能直接用 martingale 抵消；另一个危险是最佳动作被误判时 regret-state 发生永久变化，之后的归一化学习率也被改变。

**第一批实验。** 一玩家严格线性、二元协调势 Φ=pq、带线性场的 Φ=apq+bp+cq、三节点链；比较 exact full information、固定 noisy batch、随gap调batch，记录真 gap、真势、regret norm和oracle调用数。随机实验需要保留 seed，现有文件只含无seed的exact双点反例，未报随机胜率。

## NASH-03：从新 Minty 算法转成可识别的结构类

**精确问题。** 有理局部收益图已给 tree decomposition，bag size≤w+1，每玩家≤m动作。对 Fᵢ=−uᵢ(·,x₋ᵢ)，判定是否存在 x*∈∏Δ(Aᵢ)，使 ⟨F(y),y−x*⟩≥0 对所有混合 y 成立，并输出 anchor 或 infeasibility certificate。

**Paper Fact / 机制。** S3 已解决 promised Minty 下找 ε-SVI，并证明一般识别 coNP-complete；显式 normal-form 的识别是 Prop1.14 的 LP。它利用的是 convex Minty feasible set 与易检验 SVI 的不同角色，不是“找到 Minty anchor”的通用算法。

**我们 idea。** 对有限混合博弈，qₓ*(y)=Σᵢ[uᵢ(xᵢ*,y₋ᵢ)−uᵢ(y)] 是 block-multiaffine，故最小值在 pure profile s 取得。所有 Minty 约束变成关于 x* 的线性约束

\[
\sum_i\sum_{a_i}x_i^*(a_i)u_i(a_i,s_{-i})\ge\sum_i u_i(s).
\]

bounded-treewidth 局部因子给动态规划 separation；通过 LP/ellipsoid 可识别 Minty。注意图宽必须按实际收益因子 primal graph 计算，不能只用 players 原始边图而忽视邻域因子。

**玩具/首义务。** 两人 A=I₂ 的 common-interest coordination 是树结构势博弈，却无 Minty anchor：在00与11的等概率分布下，任意 anchor 的 aggregate unilateral-deviation gain 平均恒为−1，exact文件核查25个有理anchor并给符号公式。先实现树宽2二元链 DP，与全枚举 pure-profile LP逐项对比，然后证明 separation 的bit complexity。

**价值判断。** 识别性比 promised算法多一层，但算法核心很可能是标准组合，不能因“没搜到相同标题”就称新颖。只有找到自然大于 harmonic/monotone 的可识别类、紧的宽度边界或更紧凑的certificates才值得主文；目前低优先级。

## NASH-04 深挖：pathwidth 恰3的局部三次势仍有重复平方精度障碍

**模型与量词。** binary graphical exact potential game，每玩家纯动作0/1，混合变量zᵥ∈[0,1]；有理多线性势Ψ由O(n)个至多三次单项式给出；局部 strategic interaction graph最大度≤6，n≥2时pathwidth恰3。扰动游戏将每个变量限制[ε,1−ε]。固定目标几何误差δ=1/4，问是否每个扰动NE均落在某个原游戏NE的闭ℓ∞半径δ球内，以及保证此性质需要多少perturbation bits。**这是几何精度问题，不能推成求任一NE困难。**

**Paper Fact。** S4 Thm4.10/C.10用4n+1玩家的重复平方构造给double-exponential障碍；同文polymatrix（二次势）PropC.8有poly-bit扰动上界。原共享t构造已经有constant pathwidth：在链式路径袋中始终保留这一个apex，只增加常数袋大小。作者还明确t的唯一任务是把变量固定为ε。因此此次新增本质是消除t的高degree并统一系数，不是首次建立bounded-treewidth障碍。核心机制是复制变量、强制无差异、链式实现平方。

**我们的局部化 idea。** 用局部tᵢ替代共享t。设x₀=x'₀=1/2，五组变量xᵢ,x'ᵢ,cᵢ,dᵢ,tᵢ（i=1,…,n），令

\[
\Psi=\sum_{i=1}^{n}\left[(t_i-c_i)(x_i-x_{i-1}x'_{i-1})
+(d_i-\tfrac12)(x_i-x'_i)-2t_i\right]-2x_n-2x'_n.\tag{A4}
\]

各玩家收益取Ψ中所有含自身变量的项，即删去non-strategic项；这样是**稀疏 graphical exact potential game**，与identical-interest势有相同最佳回应，但不谎称稀疏图下每个玩家的完整收益都等于全局Ψ。

**内审引理草案及证明。** 对任意n及 ε∈[2^(−2^n),1/2]，扰动游戏有一个NE，其到原NE集合的ℓ∞距离至少1/2，因而严格大于固定δ=1/4：

\[
t_i=c_i=\epsilon,\quad d_i=1/2,\quad
x_i=x'_i=\max\{\epsilon,2^{-2^i}\}.
\]

因为∂tᵢΨ=xᵢ−xᵢ₋₁x'ᵢ₋₁−2<0；∂cᵢΨ=xᵢ₋₁x'ᵢ₋₁−xᵢ≤0；∂dᵢΨ=0；非末端x,x'梯度为0；末端梯度严格负、其变量值为ε，所有扰动区间KKT/最佳回应条件成立。

再看任意原游戏NE。tᵢ梯度严格负，故tᵢ=0；此时末端xₙ、x'ₙ梯度均≤−3/2，故xₙ=x'ₙ=0。若所有dᵢ∈(0,1)、cᵢ<1，则dᵢ的无差异强制xᵢ=x'ᵢ。由x₀=1/2及xₙ=0，至少有i使xᵢ<xᵢ₋₁²；此时∂cᵢΨ>0强制cᵢ=1，矛盾。因此每个原NE要么某dᵢ在{0,1}，要么某cᵢ=1；与上列扰动profile相距至少1/2。这个非严格下界排除了闭半径1/4球，也排除了所有严格小于1/2的误差保证；**不声称排除闭半径1/2球**。

**图与编码证书（独立审查后加强）。** 每个单项式至多3变量。按A₁,C₁,D₁,A₂,C₂,D₂,…顺序使用路径袋

\[
\begin{aligned}
A_i&=\{x_{i-1},x'_{i-1},t_i,x_i\},\\
C_i&=\{x_{i-1},x'_{i-1},c_i,x_i\},\\
D_i&=\{x_i,d_i,x'_i\}.
\end{aligned}
\]

删去常量x₀,x'₀后覆盖所有项。xᵢ的出现袋为Aᵢ,Cᵢ,Dᵢ,Aᵢ₊₁,Cᵢ₊₁，x'ᵢ的出现袋为Dᵢ,Aᵢ₊₁,Cᵢ₊₁（末端删去不存在的袋），其余变量只出现一次，故running intersection成立，pathwidth≤3。n≥2时，对任一i≥2取四个branch sets
\(\{x_{i-1}\},\{x'_{i-1}\},\{c_i\},\{t_i,x_i\}\)。最后一组由tᵢ−xᵢ边连通；四组两两都有边，形成K₄ minor。因此treewidth≥3，连同上述路径分解，得到n≥2时**treewidth=pathwidth=3**。直接列邻接可见最大度≤6。所有系数为常数位数有理数；有O(n)张常数大小局部表。若邻接表用绝对玩家编号，完整编码长度L=O(n log n)，不能不注明编码就称O(n)bits；以玩家数N=5n陈述所需精度bits>2^(N/5)最稳妥。此加强来自fair_goods的独立内部审查建议并已重新核查；未做外部同行审查或新颖性确认。

**收益/图定义终检。** 此处图明确定义为Ψ非零单项式的primal graph，不是把全局Ψ当每个人完整收益后得到的payoff-dependency图，也不是把每张整utility table的scope全部clique化所得的另一张图。原始局部收益取
\(u_v^{\rm raw}(a_v,a_{-v})=a_v\partial_v\Psi(a_{-v})\)，故uᵥʳᵃʷ(0,·)=0，且其邻居正是相应单项式的共现变量（至多所给primal graph）。以下区分绝对值归一化与[0,1]归一化，不把二者混用。全cube上的梯度范围逐项为：

| 坐标 | ∂ᵥΨ | 全cube范围 |
|---|---|---|
| tᵢ | xᵢ−xᵢ₋₁x'ᵢ₋₁−2 | [−3,−1]；i=1实际更窄[−9/4,−5/4] |
| cᵢ | xᵢ₋₁x'ᵢ₋₁−xᵢ | [−1,1]；i=1实际[−3/4,1/4] |
| dᵢ | xᵢ−x'ᵢ | [−1,1] |
| xᵢ, i<n | tᵢ−cᵢ+dᵢ−1/2−(tᵢ₊₁−cᵢ₊₁)x'ᵢ | [−5/2,5/2] |
| x'ᵢ, i<n | −dᵢ+1/2−(tᵢ₊₁−cᵢ₊₁)xᵢ | [−3/2,3/2] |
| xₙ | tₙ−cₙ+dₙ−5/2 | [−7/2,−1/2] |
| x'ₙ | −dₙ−3/2 | [−5/2,−3/2] |

因此|uᵥʳᵃʷ|≤7/2。取uᵥᵃᵇˢ=uᵥʳᵃʷ/4只保证纯收益绝对值≤7/8、固定对手时动作差≤7/8，对应势Ψ/4；它不保证全部收益在[0,1]。若模型要求payoffs∈[0,1]，使用
\(\widetilde u_v=(u_v^{\rm raw}+7/2)/7\in[0,1]\)，对应势Ψ/7。加常数及乘正数不改变原游戏或扰动游戏的NE。现有代码验证的是uᵥᵃᵇˢ的绝对值版本，本候选没有强制[0,1]约定；需要时采用上式即可。在**原游戏任意NE**中已先得到tₙ=0，所以末端xₙ梯度实际上属于[−7/2,−3/2]，x'ₙ仍属于[−5/2,−3/2]，严格负，足以强制二者为0。没有将“全cube上界−1/2”和“原NE上界−3/2”混用。

**精确验证。** 新增的 `toy_checks_v2.py` 验证n=1,…,12，每个n的ε=2^(−2^n)、1/4、1/2，共36个扰动profile，逐坐标检查有理梯度的上下界符号，全部通过；同时验证图度、新袋覆盖和running intersection，以及K₄ minor的连通/相邻branch-set证书。n≥2实测最大度6、三次、新袋宽上界3且minor给下界3。输出为 `toy_results_v2.json`，保留旧代码与旧输出不覆盖。几何分离依赖上段全称证明，不能由这些点计算代替。

**独立审查后的价值降级。** 本引理只作为工具保存，退出本轮主押候选。最强反方成立：原共享t本就不破坏constant pathwidth，作者对t用途的明示也让副本局部化非常直接，同行可能只视为C.10的一段remark。下一轮只有研究真正正类才值得重新升格：**三次局部势的treewidth≤2（可再窄到pathwidth≤2）或Berge-acyclic三元势因子超图，是否排除超多项式扰动bits，还是仍存在重复平方障碍？** 必须固定收益归一化、δ=1/4和全部扰动NE的量词。当前K₄ minor和共享双变量三元因子使A4不属于这些类，这不是正定理的证据。首义务是反例搜索及结构重构；若只能做t副本或微调常数，不再作为独立论文题推进。完整独立内部review在 `../fair_goods/nash_sparse_potential_review.md`，不等于外部同行验证。

## NASH-05：rank-one 的枚举分类

**精确输入。** 非退化有理双矩阵(A,B)，A+B=abᵀ且rank=1，a只有k个不同取值。输出全部孤立NE，时间多项式依赖输入位数与输出总位数；或给一个NE后判定是否存在第二个。退化时解集可能连续，必须改成maximal equilibrium subsets的有限表示，不与非退化版本混用。

**Paper Fact。** S5 §10明确问output-efficient枚举及第二均衡复杂性；§6把rank-one均衡化成一参数LP路径与超平面交点，§8有指数多均衡。不能把“找到一个容易”误推“第二个也容易”。

**我们idea、玩具、首义务。** k=1可战略等价化成zero-sum，全部NE是primal/dual optimal faces；由此试k=2，看等值a-group是否减少与目标超平面相交的有效LP段数。先枚举3×3、4×4 small rational A和binary a，B=abᵀ−A，精确support enumeration检查NE数及path crossings；首义务不是写枚举器，而是证明“无输出段”的长度能被输出/输入控制，或给k=2反例。

**评价。** 若能刻画不同a-value数的阈值，是自然扩类；但rank-one中零和A完全任意，可能没有复杂性下降。总体比前两题大，不建议当前主押。近期检索未发现解决§10同问题的原论文，不等于不存在；同时rank-two相关问题不能依赖其旧稿开放状态。

## NASH-06：3×3 零和博弈的固定置信度实例复杂性

**精确输入/输出。** A∈[−1,1]^(3×3)，每次可选一个(i,j)，独立观察均值Aᵢⱼ、已知单位方差或有界噪声样本。先promise唯一、full-support、非退化NE。对于给定ε,δ，输出随机(x,y)，要求Pr[maxⱼxᵀAeⱼ−minᵢeᵢᵀAy≤ε]≥1−δ；最小化期望查询次数，显式反映support slack和basis conditioning。更一般非唯一类另立版本。

**Paper Fact。** S6的COLT题问一般矩阵实例复杂性；2023已研究n×2，故再做2×2不新。Jiang–Zhang2026用LP-resolving处理任意维/非唯一，但Thm5.1的表述是E[输出策略]近似最优，其ε^-1不能直接作为上述high-prob ε-NE上界。

**我们idea。** 结合full-support equilibrium的线性灵敏度与最优实验设计，先求固定3×3下局部characteristic time，然后设计support-certification+weighted confidence的allocation。下界需对“改变任一ε-correct answer集合”的替代矩阵取inf，不能只改一个payoff entry而忽略允许多种ε答案。

**玩具、可证伪与首义务。** 用RPS型A₀加一个有理δ扰动，计算augmented equilibrium basis的逆及condition number；构造有相同最小entry gap而不同灵敏度的两矩阵，检验只用entry gaps的复杂性猜想。首义务是写对change-of-measure下界和answer-set量词；若只得到uniform sampling或n×2旧式估计，淘汰。该题与优化/OR很契合，但需要bandit pure-exploration背景，当前没有足够证据列为20天首选。

## 下一轮执行建议与材料状态

1. A4已通过fair_goods独立内部数学审查并因价值原因降级为工具引理。仅当treewidth≤2/Berge-acyclic等真正结构正类出现实质进展时，才重新考虑主课题地位；不把小引理成立当选题成功。
2. 并行用一玩家噪声反例审计NASH-02所有候选Lyapunov；只保留能处理clipping相关性且报总样本复杂度的方案。
3. NASH-01若两天内仍只有large-init推论，则降级工具，不吞噬主研究资源。任何使用S2内容的稿件都需明确公开稿及撤回原因，不能把撤回当成可不引用。
4. NASH-03作为检验Minty工具本质的练习/子引理；NASH-05、06暂留map，不承诺20天可解。

交付文件：`REPORT.md`、`candidates.json`、`toy_checks.py`、`toy_results.json`，以及独立审查后新增的 `toy_checks_v2.py`、`toy_results_v2.json`。旧输出保留。代码只做exact有限核查；没有随机成功率、没有全局算法宣告、没有新颖性认证。


## 仓库复现入口

代码：`tests/audits/topic_selection/nash_equilibria/`；冻结输出：`evidence/runs/topic_selection/nash_equilibria/`。运行到新的临时目录，保持旧输出不变，见[本轮复现与核验](../VERIFICATION.md)。
