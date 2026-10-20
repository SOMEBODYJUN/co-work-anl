# 原子拥塞博弈重新选题：以资源边际代替策略计数的纯精炼均衡算法

本文件属于重新选题，不延续一般不相关调度低于2目标。检索截至2026-10-20。**推荐把 AP-01 与 AP-02 合为一条主候选继续48小时独立攻击；它们目前是有完整代数机制的候选证明草稿，不是已审定新定理。** 不承诺20天解决或发表。父代理及 `nash_structure` 已独立重构关键期望公式；文献排重仍未穷尽。

## 1. 去重候选池与淘汰理由

表中“文献题”指原文明确提出；“新切口”指本次从工具机制推导，不能冒充原作者原话。每项均按原子玩家、有限策略、单边偏离理解，除非另注。

| ID | 精确问题及输入域 | 母论文、位置、文章定性 | 核心机制、首个攻击、判断 |
|---|---|---|---|
| AP-01 | 非对称无权matroid拥塞博弈；任意非减有理延迟表；各基多面体有共同相对内部有理点p。多项式时间求normal-form纯trembling-hand perfect equilibrium。 | [R1] §6“without the symmetry assumption”；E.4/E.5计数输入。工具+复杂性分类；**新结构切口**。 | 用共同资源边际代替相同策略集，扰动后仍为普通拥塞博弈。下文给候选证明。反方：common-ri可能太窄；不能宣称解决全部非对称开放题。**主选**。 |
| AP-02 | 任意非对称matroid拥塞博弈；公共affine延迟a_e k+b_e，a_e,b_e≥0有理；不要求共同p或同rank。多项式求纯perfect equilibrium。 | [R1]同一公开问题；[R2] §3的player-specific matroid算法为备选导入。**工具迁移新切口**。 | 各自tremble边际不同，但affine期望仍是公共斜率+个人资源常数。用slot matroid intersection求势最小。**主选，与AP-01互补**。 |
| AP-03 | 全部非对称matroid、一般非减延迟，求纯perfect；进一步求proper。 | [R1] §6明确问题。问题突破型。 | AP-01排除“身份依赖”；一般情形资源期望依赖使用者集合。最小反例攻击取3玩家、两个不同可行基集、quadratic延迟。当前缺多项式势优化结构，**前沿上界，不定为20天任务**。 |
| AP-04 | weighted matroid set-functional costs及weakly monotone聚合g：收敛、算法、PoA/PoS。 | [R3] arXiv2024 §5结尾、2025 DAM版本。分类+工具统一；原文方向。 | 先审查strict局部交换工具。已发现v1 Lemma3.7的平台反例，见§5。不能直接把该lemma当算法引理。一般weighted best-response已有超多项式障碍[R2]；**保留第二梯队**。 |
| AP-05 | finite-delay priority-based player-specific singleton/matroid、资源优先级不一致；多项式求PNE。 | [R4] Thm4.5、6.4只保有限终止，§7要求有效算法。模型统一+工具。 | consistent priorities已有多项式次序；不一致优先级打破分层锁定。首48h取两个priority levels、singleton，追踪插入算法能否使计数单调。用户熟悉稳定匹配时有价值；尚无足够机制，**不压过AP-01/02**。 |
| AP-06 | k维需求、坐标非减资源成本、singleton策略；将需求全序条件放宽成小width偏序，求PNE或无PNE证书。 | [R5] §5、Thm8（AAMAS摘要编号）、UAI完整版结构需求部分。视角+CSP工具；**新参数切口**。 | 需求全序允许贪心插入；width=2未自动继承。首攻击2维两条链、3资源小整数成本搜无PNE。不能把一般k维线性一致性分类[R6]误当该特殊策略问题。风险：不自然参数或很小反例即摧毁。**第三梯队**。 |
| AP-07 | degree-d weighted polynomial congestion，缩小d-approx potential与近似PNE存在/复杂性界之间的差距。 | [R7] Thm1及[R8]主结果；工具+障碍。 | 近似势通过边际积分控制；要改善一般d依赖是长期问题。小d、限制weights等可试，但当前无新机制。**拒绝泛化为新“大目标”**。 |
| AP-08 | 无权polynomial latency games，最坏情况高质量近似PNE计算；超越d^{O(d)}。 | [R9] §3.3.2称为重要剩余开放题；2024 paper工具主导。 | 分阶段局部搜索/近似势。**不能**把2024平滑FPTAS当最坏情况结果；也不能许诺1+ε算法。范围过大，**不选**。 |
| AP-09 | 独立扰动resource数据下，不限制偏离涉及资源数B的一般拥塞博弈exact PNE平滑复杂性。 | [R10] §6、Thm4.2；通用局部搜索工具。 | B-restrained可分离性；一般B需跨多步rank分析。最小目标可取有界树宽但长策略；必须先排查直接套参数已覆盖。**大题，不选**。 |
| AP-10 | 对[R9]平滑FPTAS，把独立噪声放宽为相关/低维噪声。 | [R9] Lemma1与§3；**工具新切口**。 | 原证明核心实际只用min coefficient尾界；一些“相关推广”只需union bound，单个共同正toll就可使近似阈值变大。首攻击删掉独立性逐行重证。**很可能增量过小，主动淘汰**。 |

**明确排除过时题**：[R4] arXiv2024、WALCOM2025、TCS2026已经回答Ackermann等2008提出的“高优先级造成有限而非无限delay”模型问题；它本身不能再列OPEN。[R5] AAMAS2024只有摘要，必须用同作者UAI2024完整版排重，不能拿摘要未展开算法当新结果。

## 2. AP-01/AP-02共同模型与价值

设玩家i的策略为matroid M_i在共同有限地面E上的全部基B_i；允许不同matroid、不同rank、loops/coloops。输入是独立性oracle和非负有理延迟d_e(1),…,d_e(n)，按k非减。玩家成本为Σ_{e∈B_i}d_e(k_e)。目标是原始normal form的**纯perfect equilibrium**，不是SPE、mixed NE、仅PNE或某个特定均匀噪声的稳定点。

[R1]的工具本质是将ε扰动的成本作符号比较，并把可解组合优化算法搬进扰动问题；对称性用来隐藏玩家身份。其Appendix E.4还明确假设给定每资源包含于多少个基B_r，E.5有类似路径计数输入。我们不把删去这一附加输入单独包装成大突破：**核心价值是识别更弱的“边际兼容”结构，并给出任意非对称affine情形。** 文献检索未找到完全相同结论，不等于新颖性认证。

## 3. 候选证明草稿：资源边际足够，策略分布可以只存在

### AP-L1：小支持中心及全支持提升

对非空matroid基多面体P_i=conv{1_B:B∈B_i}，固定一个基B。列出B及全部可行单交换基B−e+f，取其指示向量均值p_i。个数至多1+r_i(m−r_i)，独立性oracle可多项式构造，坐标位长多项式。

候选引理：p_i∈ri(P_i)。证明：若p_i属于一个face，则该face必须包含均值中的每个顶点。matroid基多面体在B的全部邻顶点正是单交换基；一个proper face不能包含B的全部邻顶点，否则B处全tangent cone都落在该face方向空间中，与全多面体仿射维数矛盾。rank0或唯一基时结论退化为该单点的相对内部。

另一个标准凸几何事实：p_i∈ri(P_i)当且仅当存在对**每个基都赋正概率**的分布q_i，边际为p_i。向右可将p_i写为足够小的全顶点均值与P_i另一点的凸组合。算法不需要输出q_i；它只需有理p_i。勿把上述小支持均值本身误说成全支持q_i。

### AP-L2：自己的tremble项在偏离比较中消去

对纯核B_i，定义x_i^ε=(1−ε)δ_{B_i}+εq_i。所有q_i全支持，因此x_i^ε完全混合。固定对手后，对任意两个纯核S,T，

\[
C_i(x_i^ε(T),x_{-i}^ε)-C_i(x_i^ε(S),x_{-i}^ε)
=(1-ε)\sum_e(1_{e∈T}-1_{e∈S})\,
\mathbb E[d_e(1+K_{-i,e})].
\]

这里K_{-i,e}是对手使用e的人数。每位玩家内部资源间可以相关；对一个固定资源，**不同玩家的混合独立**足以计算该期望。本人q_i项是与纯核选择无关的常数，不能漏掉这一步而直接声称扰动是拥塞博弈。

### AP-01候选定理：共同相对内部边际

合同先以输入给出有理p∈∩_i ri(P_i)，不把交的识别混入最小结果。取各q_i边际同为p。令f_e=εp_e，h_e=1−ε+εp_e，则一个名义使用e的玩家所见有效延迟为

\[
\widetilde d_e^ε(k)=\mathbb E\left[d_e\left(1+
\operatorname{Bin}(k-1,h_e)+\operatorname{Bin}(n-k,f_e)\right)\right].
\]

两个二项变量独立；k包括该玩家。它是次数至多n−1的有理ε多项式，卷积可多项式计算；由h_e≥f_e可耦合证明按k非减。AP-L2说明纯核扰动博弈与普通非对称matroid拥塞博弈战略等价。

**真正非对称例子**：E={a,b,c,d}，rank2。M_1的基为所有二元集除ab；M_2的基为所有二元集除ac（各自一对parallel elements）。p=(1/5,11/20,11/20,7/10)属于两个基多面体的ri：p(E)=2，0<p_e<1，p_a+p_b=p_a+p_c=3/4<1。所以不是把“对称”换词。相反，若M_1排除ab、M_2排除cd，ri交为空：前者要求p_ab<1，后者p_cd<1，却p(E)=2。该障碍解释AP-01为何没有解决全部非对称问题。

### AP-02候选定理：任意非对称affine

现在允许任意p_i∈riP_i，取d_e(k)=a_e k+b_e。记P_e=Σ_j p_{j,e}。AP-L2中的期望直接线性化为

\[
\widetilde d_{i,e}^ε(k)
=a_e(1-ε)k+b_e+εa_e(1+P_e-p_{i,e}).
\]

因此身份依赖只在个人资源常数，公共斜率仍非负。这提供exact potential

\[
\Phi^ε(B)=\sum_e a_e(1-ε)\frac{k_e(k_e+1)}2
+\sum_i\sum_{e∈B_i}\{b_e+εa_e(1+P_e-p_{i,e})\}.
\]

该式同时证明AP-02不是强行假设共同边际；它覆盖上一个ri交为空的例子及rank不一致情形。迁移到degree2时，E[K²]含“哪些人是名义使用者”的项，不能继续用此式：这正是自然边界，非记号差异。

### AP-L3：两个候选均可由一个明确组合优化原语完成

对公共非减有效延迟g_e^ε(k)及个人线性项t_{i,e}^ε，目标是最小化

\[
\sum_e\sum_{k=1}^{k_e}g_e^ε(k)+\sum_i\sum_{e∈B_i}t_{i,e}^ε.
\]

用地面(i,e,k)，k=1,…,n。第一matroid是各玩家M_i将每元素e作n个parallel copies后的direct sum；第二matroid按(e,k)分组，每slot容量1。求大小R=Σ_i r_i的最小权公共独立集，权为g_e^ε(k)+t_{i,e}^ε。第一matroid保证同一玩家不会重复选e；第二保证slot不冲突。非减性允许把占用slot压到每资源前k_e个，所以最优权恰为所写势值。导入经典weighted matroid intersection，多项式oracle时间即可；这个slot技术本身不声称原创。

符号复杂度可直接落为整数权：清除所有有理系数的公共分母，设系数绝对值界U、公共基大小R、最大次数D≤n−1，取整数M>2RU+1，把多项式c_0+…+c_D ε^D编码成Σ_t c_t M^{D−t}。任意两个R元素解的权差按首个非零系数排序，后续项不会翻转；位长仍多项式。AP-02仅D=1。故不需要声称任意黑箱都能处理形式无穷小，也不需要执行指数精度数值极限。

势全局最小的固定纯核B*对所有充分小ε是扰动博弈PNE。因x_i^ε的主核必为对x_{-i}^ε的最佳回应，而q_i全支持，令ε↓0即给原normal-form纯perfect equilibrium。必须使用同一B*及一段充分小区间；单个有限ε的实验不够。

**当前余留义务**：严格核对weighted matroid intersection的编码与oracle成本；写出AP-L1的标准多面体引用或完全初等交换证明；全文查新，尤其2026正式版是否已含任意full-support perturbation/affine例子；检查所求是normal-form perfect而不是仅某种polytope perfect。共同ri交的LP+分离识别可作为后续增强，最小结果不依赖它。

## 4. 首48小时与20天最小交付

0–12小时：把AP-L1/L2及两个有效延迟公式写成独立证明；重读[R1] E.4/E.5，核实计数oracle与定义。12–24小时：由独立研究者攻击own-tremble消去、same-p必要性、degree2失效；枚举不相同matroid的所有纯核检查。24–48小时：写出slot matroid intersection完整变换及位长界，搜索最近邻；若该桥梁有洞则立即降级，不以模型算力当可行性证据。

20天最小可交付是**一篇围绕同一机制的自足理论短稿**：先保住“任意非对称affine matroid的纯perfect算法”，再加“共同ri边际、任意非减延迟”结构推广及对称情形去计数附加输入。若发现结果已含于[R1]或无实质新颖性，停止包装；转向degree2中身份依赖的可解结构，而不是自动升级一般非对称难题。该范围有明确证明链、原文公开问题、自然边界，比泛攻近似Nash常数更符合20天资源。

## 5. 独立玩具发现与有限计算

**AP-X1（已证反例，针对指定预印本lemma而非主定理）**：[R3] arXiv:2401.03861v1 Lemma3.7称非PNE必有严格改善的单交换。取单玩家U_{2,4}、常数资源成本(2,2,1,1)、g=max、当前基{a,b}。所有单交换成本仍2，而{c,d}成本1。故该strict local-to-global表述不成立；可能由平台上的弱改善交换修复。2025期刊全文本次403，**未确认正式版本是否已经修正**，不能对外宣称期刊错误，更不能据此否定存在性定理。

精确审计代码：[atomic_tremble_audit.py](../../../tests/audits/topic_selection/atomic_tremble_audit.py)；输出：[atomic_tremble_audit.json](../../../evidence/runs/topic_selection/atomic_tremble_audit.json)。使用Fraction、无随机seed；3玩家、4资源、两个非对称rank2 matroid、125纯核profile；ε∈{1/10,1/100}。分别按完整对手基分布枚举与资源Bernoulli公式比对AP-01偏离差；另取不相同边际检查AP-02 affine式。**这是有限算术核查，不是普遍定理、perfect证明或新颖性证明。**

## 6. 原始来源、位置与本轮web refs

- **R1** Ioannis Anagnostides, Maria-Florina Balcan, Kiriaki Fragkia, Tuomas Sandholm, Emanuel Tewolde, Brian Hu Zhang. *The Complexity of Equilibrium Refinements in Potential Games*. [arXiv v2 PDF](https://arxiv.org/pdf/2511.03968), 2026-02-10；§6无对称与proper开放问题；Thm4.4/4.5；Appendix E.4/E.5的B_r/B_e计数输入。作者[Fragkia publication page](https://kiriakifragkia.github.io/publications/)确认EC2026。web `turn65view0`, `turn71view0`, `turn71view1`, `turn65search15`。v1有关normal-form proper部分已经移出，不混用。
- **R2** Heiner Ackermann, Heiko Röglin, Berthold Vöcking. *Pure Nash Equilibria in Player-Specific and Weighted Congestion Games*. TCS410(17),1552–1563 (2009). [作者全文](https://www.roeglin.org/publications/WINE06.pdf)，§3 player-specific构造，§4 weighted及收敛障碍；作者2008预印本为正式论文前身。web `turn103view0`, `turn102search0`。
- **R3** Kenjiro Takazawa. *Pure Nash Equilibria in Weighted Congestion Games with Complementarities and Beyond*. [2024 arXiv](https://arxiv.org/pdf/2401.03861)，Definitions3.1/3.2、Thm3.3、Lemma3.7、§5结尾；正式题名 *Pure Nash equilibria in weighted matroid congestion games with non-additive aggregation and beyond*, DAM361(2025),226–235, [DOI](https://doi.org/10.1016/j.dam.2024.10.017)。web `turn4view0`, `turn11view0`, `turn6view0`, `turn11search14`。期刊全文本次不可读。
- **R4** Kenjiro Takazawa. *A Unified Model of Congestion Games with Priorities: Two-Sided Markets with Ties, Finite and Non-Affine Delay Functions, and Pure Nash Equilibria*. [2024预印本](https://arxiv.org/pdf/2407.12300)，§4.5/§6.4/§7；WALCOM2025；TCS1082(2026),116144，[DOI](https://doi.org/10.1016/j.tcs.2026.116144)。web `turn32view0`, `turn37view2`, `turn28search0`。
- **R5** Mohammad T. Irfan, Hau Chan, Jared Soundy. *Equilibrium Computation in Multidimensional Congestion Games: CSP and Learning Dynamics Approaches*. [UAI2024正式页](https://proceedings.mlr.press/v244/irfan24a.html)、[作者全文](https://tildesites.bowdoin.edu/~mirfan/papers/congestion-games-uai-2024.pdf)，§4 CSP、§5结构及dynamics；[AAMAS2024摘要](https://www.ifaamas.org/Proceedings/aamas2024/pdfs/p2309.pdf) Thm8是ordered demand singleton。web `turn32search0`, `turn37view0`, `turn3view3`。
- **R6** Max Klimm, Andreas Schütz. *Equilibria in Multiclass and Multidimensional Atomic Congestion Games*. MOR47(4),2743–2764 (2022). [DOI](https://doi.org/10.1287/moor.2021.1223)，consistent cost sets的affine/exponential分类。web `turn28search2`, `turn28search49`；本次作者PDF fetch失败，故不从未读证明提出新定理。
- **R7** Ioannis Caragiannis, Angelo Fanelli. *On Approximate Pure Nash Equilibria in Weighted Congestion Games with Polynomial Latencies*. [ICALP2019正式页](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2019.133)，Thm1、近似势；[arXiv](https://arxiv.org/abs/1902.07173)，JCSS117(2021)。会议与journal改进后的PoS公式不同，不混报。web `turn109search0`, `turn0academia30`。
- **R8** George Christodoulou, Martin Gairing, Yiannis Giannakopoulos, Diogo Poças, Clara Waldmann. *Existence and Complexity of Approximate Equilibria in Weighted Congestion Games*. [ICALP2020](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2020.32)，后MOR48(1),583–602 (2023), [DOI](https://doi.org/10.1287/moor.2022.1272)。web `turn65view2`, `turn0search13`。
- **R9** Yiannis Giannakopoulos. *A Smoothed FPTAS for Equilibria in Congestion Games*. EC2024，[全文](https://arxiv.org/pdf/2306.10600)，Thm1、Lemma1、§3.3.2 polynomial、§3.3.3 cost-sharing。web `turn19view0`, `turn19view1`, `turn19view2`。
- **R10** Yiannis Giannakopoulos, Themistoklis Melissourgos, Alexander Grosz. *On the Smoothed Complexity of Combinatorial Local Search*. MOR2025, [DOI](https://doi.org/10.1287/moor.2024.0610)、[全文](https://arxiv.org/pdf/2211.07547)，Thm4.2、4.6、§6。web `turn4view2`, `turn89view3`, `turn19view3`。
- **R11** Heiner Ackermann, Heiko Röglin, Berthold Vöcking. *On the Impact of Combinatorial Structure on Congestion Games*. JACM55(6),2008，[原始ECCC](https://eccc.weizmann.ac.il/eccc-reports/2006/TR06-067/index.html)，matroid best-response多项式收敛分类。web `turn80search4`。本稿算法也可走此导入，但slot全局优化更直接。
- **R12** András Frank. *A Weighted Matroid Intersection Algorithm*. J.Algorithms2(4),328–336 (1981), [DOI](https://doi.org/10.1016/0196-6774(81)90032-8)、[作者文献页](https://andrasfrank.web.elte.hu/pub/pub.html)。web `turn109search4`, `turn109search9`。本稿只导入经典精确多项式优化原语，不声称该原语新颖。

## 7. 当前battle结论

AP-01/02胜在**从2026原始文章的明确问题出发，找到可验证的结构与代数原因**；不是一般调度或一般PNE难题换名。它们的风险主要是论文价值与最近邻遗漏，而不再是完全没有证明机制。AP-04/05有新近原文方向但缺关键算法结构，暂不投入20天主资源；AP-07/08/09是大开放题，AP-10容易沦为一行推论，均主动降级。
