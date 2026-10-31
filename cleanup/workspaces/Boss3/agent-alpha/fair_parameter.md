> 统一候选编号、当前状态和本轮最终判断以[候选比较](../BATTLE.md)为准；本文保留来源与推导过程。

# boss37 第二轮：公平参数化选题 battle 与实质试攻

核查日2026-10-20。范围是重新选题，非旧UM主目标。仅写本目录；未改共享git、未提交、未推公屏，由根部统一。已全文读`BOSS_START.md`与`VALUE_CRITERIA.md`。A=作者原文明确问题；B=作者明确建议；C=本轮派生。没有估计“20天成功概率”。

## 已产生的数学增量

1. **FP-COUNTER-BALANCE-v1**：一个k=1、5顶点、底层path的严格反例，证明不能把所有非special内部平行包先平分。路径上可以传递大于奇偶量级的容量。
2. **FP-FOREST-THRESHOLD-v1**：固定heavy后，若单位边简单支持为森林，则存在一维向上区间消息，得到任意二进制multiplicity与s/h偏置下的多项式精确算法。由此得该受限类`2^k poly`，并非一般多重图F01。
3. **FP-CHARITY-SIMPLE-v1**：推导simple graph Min-Charity EF的`3^k poly`精确算法，甚至支持任意非负donation costs。关键“anchored单位组件的部分解可以全补回”lemma、二分流与完整最优性证明都在[PROOFS.md](../notes/heavy_edge_residual_and_charity.md)。这是本轮最值得外部独立审查的实质资产；新颖性尚未确认，可能过短。

实际程序：`probe.py`4200个森林实例与全整数枚举比较，差异0；`charity_probe.py`1200个小simple实例与全部`3^m`partial orientations真最优比较，差异0。均Python任意精度整数，两个固定seed和输入范围见结果json。计算只核程序，普遍命题依据书面证明。

## 候选比较：共六个，暂不机械相加评分

| ID/来源 | 精确研究对象与目标 | 文献差额、类型、真正机制 | 第一判别动作及本轮结果 | 最强反对意见/研究价值要求 |
|---|---|---|---|---|
| **FP01 = F01 / A** | 任意非负整数additive multigraph，k条heavy，EF orientation求`2^k poly`，先任意FPT(k) | P1 §5原题；P1 Thm13仅simple，固定heavy后用degree lower bounds，multigraph必须保留pair可见量。分类+接口工具 | 已固定残差精确式；全平分被严格击穿；light-support forest阈值DP已闭合。下一步用环块/双接口最小例测frontier，或找固定heavy残差poly/困难性 | 原题的承重障碍尚未消除，不能因作者新近提出就把一般FPT锁作20天主目标；forest lemma单独不够文章 |
| **FP02 = F02 / A** | 任意multigraph EF/EFX及min-charity，参数`tw+Wmax`，Wmax为单条边端点最大值，目标FPT | P1 §5原题；既有Thm14/23用Wshared（同pair价值总和），不是Wmax。计数压缩/结构ILP工具 | 已核通用ILP不能直接盖掉：bounded coefficient+incidence treedepth甚至常数5仍可能NP-hard（P2），旧FPT需要primal/dual treedepth；图tw不是ILP图tw。先做binary types pair-count编码与矩阵结构检查 | P2只是排除错误黑盒，不能证明本题难；既有XP`(n+m)^O(tw)`已覆盖固定tw，故仅做tw=2,Wmax=2算法没有差额。此题暂比FP03更难判别 |
| **FP03 / C** | simple graph Min-Charity EF，k heavy；任意非负边删除cost；求最优FPT算法并探紧指数/核 | P1 Table1明确Thm13是唯一未声称扩展min-charity的算法；本题是我们派生，不冒充§5开放题。组合：branch heavy状态+binary组件激活+quota flow | 本轮已给`3^k poly`自足证明及算法，1200例真最优核对无差异；下一步独立审稿+最新后续查重，尝试`2^k poly`或一般multigraph salvage | 可能只是短推论，单一3^k定理不保证独立成稿；需 tightness、weighted charity/核化或multigraph实质扩张。是**最可立即核实的新成果包**，不是已确认论文选题 |
| **FP04 / C** | 固定heavy残差，单位支持为cactus，允许arbitrary binary m,s,h；求poly位复杂度，随后`2^k poly`EF | 从FP01母题选择自然block扩类；FP-FOREST新一维阈值接口是地基。类型：接口工具+自然扩类 | 下一动作只看单cycle块与一个父接口，问“可扩展输入是否仍由一个阈值与可实现root-pair收入区间描述”；cycle上所有pair数量可枚举给伪多项式/显式m多项式，但需二进制m压缩 | 固定tw=2且**显式**单位边输入已有P1 XP覆盖，本题必须明确差额是巨大binary multiplicity压缩+arbitrary heavy结构不计入light tw，或推广到多接口。不能把普通cactus算法本身包装过高 |
| **FP05 / C** | minimum total subsidy orientation按heavy数k参数化，先simple，严格用共同补贴比较`v_i(X_i)+p_i >= v_i(X_j)+p_j` | P3 §3.2 binary多项式、§3.1 {1,2} NP-hard；自然near-binary优化扩张，工具是envy graph正环/最长路+heavy branch | 先核P4 IJCAI26最新补贴文；再检查固定heavy后，最优补贴的vertex potentials能否与lower-degree flow共同建模。此轮仅精确构造候选，未证FPT | **不能**把补贴当独立为每人填自身deficit；p_j也在右边，方向可能不envy-freeable。branch fixed后仍是混合离散/势函数问题，比FP03明显未闭合。可作为OR对偶工具储备 |
| **FP06 / C，Nash/公平桥梁** | 战略E-C-E机制中，在原文已固定的某一机制版本下，限制true valuations为binary graphical（每件至多2人相关），求best response的poly算法与全部/存在PNE的公平界；先n=3 | P5 v2于2026-10-19更新：若干E-C-E版本有PNE；摘要将某些best-response近似公平正面限于n<=3，n>=4有负面。我们加sparse interest不是作者原题。视角：envy-cycle tie rules可能成为战略操纵的结构接口 | 首先从P5全文固定report domain、picking order、tie-breaking和cycle rule，列举n=3,m<=6报告博弈；若直接继承原文结论则淘汰。此轮只完成一手来源发现，不以摘要当完整定理 | 分配结果为图支持不等于机制中每步都保留支持，且graphical true valuation不限制任意misreport；不写清机制就没有数学问题。当前证据弱于FP01/03，只储备 |

### 比较结论

目前不建议继续把“所有普通组件平分后仅留下2k个端点”当F01主算法。这一压缩方式确切错误。保留普通组件的数值边界接口仍有希望，但必须处理实质容量传播。

FP03应立即给另一研究者独立核：它已从选题变为一个精确算法命题，价值风险也很清楚——可能太短或已被覆盖。若它只需简短proof即可成立，这可以作为文章的一节或反向帮助定位multigraph的真正障碍；不应为追求“保底”刻意把小扩展包装成整篇成果。

FP02没有被“套ILP即可”淘汰，但当前没有新结构lemma；它是自然原题，未成为本轮最可立即推进的选择。

## 对FP02：为何通用ILP并不直接解决

自然pair-count变量为每一端点权类型(a,b)的定向数量，种类数至多`(Wmax+1)^2`。系数有界本身不是FPT保证。

即使只写固定heavy残差的EF行`sum_l x_il+x_ij >= ...`，中心i在高degree星图上也会令所有incident变量同时出现在一个约束中；原图tw=1，但自然ILP primal图有任意大clique。用utility变量和prefix sums拆约束可以改变矩阵图，但必须实际证明primal/dual treedepth、block depth或其他可用参数被`tw+Wmax`控制。原图tw不能直接代入ILP的tw。更不能把`n^{O(tw)}`叫FPT。

P2给的负面结论是“bounded incidence treedepth+coefficient”的一般IP仍NP-hard；因此不存在所设想的这一个通用正面黑盒。它不排除这个fair-orientation专用矩阵有特殊可解性，也不能用来声称FP02已hard。

## 一手来源与读取程度

- **P1** Kanellopoulos, Nemery, Pergaminelis, Sotiriou, Vasilakis, *EF(X) Orientations: A Parameterized Complexity Perspective*, arXiv:2512.25033v5, 2026-10-07：[HTML](https://arxiv.org/html/2512.25033v5)、[PDF](https://arxiv.org/pdf/2512.25033v5)。已读§§3.1,3.3,3.4,4.2,5；PDF Appendix B Thm13 proof/Claims29–30逐行读；其余相关DP附录已按Source Audit审计（页码以节/定理定位为准）。本文用到的既有事实限于上述定理范围与开放题位置。
- **P2** Eiben–Ganian–Knop–Ordyniak–Pilipczuk–Wrochna, *Integer Programming and Incidence Treedepth*, arXiv:2012.00079v1：[作者摘要](https://arxiv.org/abs/2012.00079)。已核constant5 incidence treedepth、coefficient1时NP-hard以及primal/dual treedepth正向区别。另核Ganian–Ordyniak, *The Complexity Landscape of Decompositional Parameters for ILP*, [1809.00585](https://arxiv.org/abs/1809.00585)。尚未重建其困难性归约，本轮只用它排除错误黑盒。
- **P3** Li–Sun–Suzuki–Xing, *On the Subsidy of Envy-Free Orientations in Graphs*, [arXiv:2502.13671v1](https://arxiv.org/html/2502.13671v1), 2025-02-19。已读§§1.1,3.2,7；它也有binary multigraph四种种子结构，故读P1时应把该工具链一并纳入排重，不能误认为所有binary机制只出现于P1。
- **P4** Li–Sun–Xing, *Eliminating Envy in Multigraphs Through Subsidy*, [IJCAI26 Proceedings 0387](https://www.ijcai.org/proceedings/2026/0387.pdf)。仅检到正式primary proceedings/摘要，PDF正文工具读取失败；FP05不得在核清此文前升主目标。
- **P5** *Envy Cycle Elimination with Strategic Agents: Best Responses and Fairness Guarantees*, [arXiv:2605.31253](https://arxiv.org/abs/2605.31253), v1 2026-05-29、最新版v2 2026-10-19。已打开primary摘要核v2新边界，未全文，FP06明确为待原文固定机制的C候选；后续务必读v2而不是沿用v1。

最新覆盖检索：system1与system2分别搜索`"2512.25033" multigraph heavy`、`"Min-Charity" "heavy" orientation`、`"charity" "EF Orientation" parameterized edges`、`"Min-Charity EF" "heavy"`等，没有检到独立后续覆盖FP03；这仅是检索记录，不证明新颖性。

## 恢复顺序与边界

1. 外部独立核`PROOFS.md`第3节，尤其active扩展是否依赖simple且忽略了p_j式外部支付（本命题根本无补贴）。
2. 执行两个脚本重现冻结json；不要扩大随机样本来替代审稿。
3. 精读P4/P5只在保留FP05/06时做；本轮不以弱储备题稀释FP03的核验。
4. F01下一可证义务：双接口组件响应集合能否压缩，或给不可压缩/NP-hard阻碍；当前仅森林单接口闭合。

没有推送commit；本目录是待根部挑选汇入的具体资产。

## FP04 的 ring 接口：具体下一可运行证明义务

根部独立提出以下精确单环化。循环编号i；e_i={i,i+1}有m_i条单位边；x_i为分给i+1条数。先把挂树用森林阈值接口吸收进常量/需求。无挂树时i收益为`R_i=s_i+x_{i-1}+m_i-x_i`，故三类比较为

    2*x_{i-1}-x_i >= h_i,left + m_{i-1}-s_i-m_i,
    x_{i-1}-2*x_i >= h_i,right-s_i-m_i,
    x_{i-1}-x_i >= max_{j非左右邻居} h_ij-s_i-m_i,
    0 <= x_i <= m_i, x_i整数.

所有变量依赖沿同一方向闭成一个环，系数只出现1,2。它属于monotone two-variable-per-inequality，但不应由此直接称二进制多项式：

Hochbaum–Naor, *Simple and Fast Algorithms for Linear and Integer Programs with Two Variables Per Inequality*, SICOMP23(6), 1994，[primary publisher](https://epubs.siam.org/doi/10.1137/S0097539793251876)、[作者PDF](https://hochbaum.ieor.berkeley.edu/html/pub/HNaorSICOMP94.pdf)，摘要对monotone **integer**问题给的是pseudo-polynomial；real LP版本才是强poly的另一条结果。

可判别题应写成：上述单向循环、系数{1,2}、任意二进制m与offset的特殊整数系统是否有poly(bit-length)算法/简洁区间frontier？若使用已有TVPI结论，必须逐项核它允许的coefficient、objective、domain和bit-length。当前没有声称该系统的困难性或新算法。

## Source Audit appendix：FP-CHARITY-SIMPLE-v1 的直接覆盖排查（2026-10-20）

**结论边界**：在[arXiv:2512.25033v5 完整41页PDF](https://arxiv.org/pdf/2512.25033v5)的正文、主表、相关完整附录证明中，**未发现作者已经陈述或证明 simple graph Min-Charity EF 按heavy数k的FPT、3^k算法，或任意非负edge donation cost版本**。这仅完成“该版本是否直接包含同一结论”的审计；不是全球新颖性证明，更不是独立成稿价值证明。

定位及核对依据（优先按节/定理定位，避免不同reader页码偏移）：

| 检查位置 | 原文实际范围 | 与我们命题的关系 |
|---|---|---|
| §1.2 Table1及caption | 第二行为simple EF的k-heavy算法；caption明确把第二行排除在minimum-charity扩展声明之外 | 主表没有声称所查结论，但“没声称”本身不排除附录藏有直接证明，因此继续往下核 |
| §2.1 Min-Charity正式定义 | 目标是最大保留条数/最少删除条数；没有单独cost c(e)输入 | valuation的weights不等于donation costs，不能据“weighted graph”误判已覆盖weighted charity |
| §3.1 Thm7、完整附录Thm7证明 | 仅binary valuations；坏binary组件用删一条平行边产生偶数种子，或者把simple树全部删除 | 已覆盖我们proof中的无anchor纯单位组件基础；没有固定heavy方向后的anchored补全lemma |
| §3.3 Thm13、附录Claims29–30及Thm13结尾 | 固定每条heavy的两个方向；所有剩余单位边必须全部定向；下界indegree转换UDCGO | 它是完整EF的2^k算法；附录没有“删heavy”第三状态或最小化partial edge loss步骤 |
| §3.4 Thm14完整DP附录；§4.2 Thm23完整DP附录 | minimum charity由signature的k计数删除边，复杂度Wshared^O(tw)poly；k在此是charity数量，不是heavy数 | 此处的k记号不能误读成heavy参数。原图可有任意大tw，故不能直接推出我们按heavy数的算法 |
| §5全文及全PDF关键词检索 | heavy的未来问题是multigraph EF；本文未写simple charity的heavy FPT题目；全文`cost`无匹配，`weighted`出现于估值/归约语境 | FP03仍应记C（我们派生），不能冒称作者公开问题。未检到weighted donation cost定理 |

读取方法：打开完整PDF的全域文本索引，对`charity`、`heavy`、`cost`、`weighted`和相关定理做跨正文/附录检索，再重读Thm7证明、Thm13及Claims29–30、Thm14/23中signature和删除计数转移及复杂度。没有把HTML缺失的附录当成不存在。审计不宣称重新核实全部无关SAT困难性证明。

定向后续检索用两套引擎，重点primary arXiv、Dagstuhl及作者/会议页面：`"Min-Charity EF Orientation"`、`"orientation" "charity" "heavy edges"`、`"envy-free orientation" "deletion" "parameter"`、`"envy-free" "orientation" "heavy" "charity" site:arxiv.org`、`"fair orientations" "weighted charity"`、`"envy-free" "orientation" "3^k"`。返回的一手相关结果仍为P1不同版本及作者ACAC26摘要，未检到独立后续对同一heavy-charity算法的覆盖；普通EFX with charity、minimum subsidy、图连通orientation均不构成同问题覆盖。搜索结果不全，未检到不等于不存在。

**据此的研究处置**：保留为自足、可审核、尚未确认新颖性的短算法扩展。关键新写明的接口是“固定heavy状态下anchored单位组件可全补回”，它与Thm13的quota流及Thm7的binary坏组件组合较短；因此即使所有证明正确且原文未写，最强低价值解释依然是“作者工具的短推论”。不把它单独宣传为已选中的完整论文。
