> 统一候选编号、当前状态和本轮最终判断以[候选比较](../BATTLE.md)为准；本文保留来源与推导过程。

# boss37 GAP/舍入第二轮：三强实攻、淘汰与新增候选

核查日期2026-10-20。本轮是重新选题，旧UM不是默认主目标。已全文读BOSS_START.md和VALUE_CRITERIA.md；只写`battle_gap_tools/`，未改共享git、凭据、公屏或提交。研究生方向契合：近似算法、组合/连续优化、随机舍入与随机运筹。下文区分A作者原题、B作者方向、C本轮派生；没有成功概率或发表保证。

## 1. 改变第一轮排名的实质结果

| 原ID | 第二轮结果 | 当前处置 |
|---|---|---|
| C01 向量LP值函数子模性 | 给出完整两资源 iff：全b,w子模，当且仅当非零列至多两条正比例射线。证明用对偶价格域的坐标min/max封闭；三不同方向构造严格反例。 | **本组最值得继续审查**，但先做一般price-lattice文献去重；不直接锁定论文主目标。 |
| C06 非均匀openingcost GBAP | 给定稀疏配置LP支持，旧配置coverage+两阶段pipage直接给always-feasible确定性(1−1/e)/2≈.31606乘LP值，比1/8强；无需隐式pricing。 | **泛常数改进淘汰**。只有超越明确baseline/运行参数才重开。 |
| C08 两尺寸knapsack gap | 找到2025后续general knapsack CRS1/3，首轮>.279目标过期；精确否定固定x类内weight uniformization；Bernoulli splitting也不总降低期望。 | **降为储备**。0.4323大猜想未查到解决，但原两步归约被真实障碍打断。 |

三个候选不再因为原排名而同等继续。C01有完整数学对象和可审查证明；C06主要回收去重/算法基线；C08需换核心工具后才值得主攻。

## 2. C01：完整分类的承重证明与价值边界

详见`C01_TWO_RESOURCE_CLASSIFICATION.md`。固定A∈R_+^{2×n}，要求对所有b,w≥0，φ(S)=max{wᵀx:Ax≤b,0≤x≤1_S}子模。零列剥离后，**当且仅当非零列至多两条正比例射线**。

这是genuinely fractional：两射线可有任意正有理数系数、任意实容量，原多面体不必integral。两射线的充分性在二维对偶价格空间成立：y≥0经两类型资源向量映成第一象限楔形锥K，K对坐标min/max封闭；对偶cost线性，物品项是单个价格的递减折线。把S,T最优价格的max给union、min给intersection即得子模不等式。

必要性取三方向的中间列d=λe+μf，b=αd，wd=1、we=max_r e_r/d_r、wf=max_r f_r/d_r。取α小保持x≤1，则φ(d)=φ(de)=φ(df)=α；仅取e,f可得>α利润。它给最小三列障碍和有理证书。

**最强objection。** 这可能是旧lattice/Topkis型parametric LP理论的特例；“完整iff”不等于新颖。还没有固定容量分类、assignment耦合、或实际新近似比。最低成果目前是可复用识别与反例定理，但是否足以独立成稿未知。下一步不是加随机测试，而是找到/排除价格格的一般定理覆盖；之后考虑新增C16的三资源两轮廓边界。

实验`two_ray_search.py`：seed20261020，300个6-item两射线随机实例，全部64个启用集LP与子模局部不等式无反例；只辅助检查，不承担证明。

## 3. C06：把常数改进的低价值解释做实

详见`C06_SUPPORT_PIPAGE_BASELINE.md`。输入有限K个配置的LP解x；每bin配置和≤1，每item总边际≤1，openingbudget≤B，并预先去除cost>B的bin。配置覆盖目标g(A)=∑_i max covered profit，先有G(x)≥(1−1/e)L。

同bin配置cost相同，沿(1,−1)方向pipage到每bin一非零；再按(1/c_l,−1/c_k)保持成本交换到至多一fractional配置。G在这类异号方向凸，每步挑不减G端点。最后整数集A和fractional singleton{e}都budget可行，G(z)≤g(A)+g({e})，取较好者保≥G(x)/2。下闭配置允许删除重复item，所以最终是实际指派。g和G能在稀疏支持上按利润阈值精确有理计算。

**范围。** 该证明针对原输入LP值，不只是support上整数OPT。它没有把通用.4323 matroid+knapsack算法错用成.4323 LP舍入；后者仍需额外integrality-gap论证。也不声称已解决所有交通额外约束，root应核对P03 Eq1.4是否正好是这个模型。

**出处去重。** CGST2011 §4.2原文已给配置maxcoverage SAP和bin matroid扩展；Sarpatwar–Schieber–Shachnai arXiv1705.06319v3 Theorem1给显式地集matroid+knapsack的(1−e^{-2})/2，正文引言也提到已有1−1/e−ε算法但枚举指数差。2026 Ganz Rozenman–Kulik–Schwartz–Singh 2605.03071 Thm1.5又加速plain SAP，未自动包含任意openingbudget。基线是旧工具的可审核直接组合，**不是本轮可宣称的新贡献**。

## 4. C08：后续文献与两个精确归约障碍

### 4.1 2025后续使>.279目标过期

Sergeev thesis写作2020、arXiv2404.00041v1发布2024，§4.1 Conjecture4.2问自然knapsack LP的一般gap≥c=(1−e^{-2})/2；§4.3给monotone .279 scheme。

Ma–MacRury–Stein，**Forward-backward Contention Resolution Schemes for Fair Rationing**，EC2025，arXiv2502.09521v1。§1.2允许独立随机size S_i∈[0,1]∪{∞}且∑E[S_i1finite]≤1；Thm1.4给two-order 1/3-selectable knapsack CRS；Thm1.5 upper bound1/(2+e^{-1})。取S_i=s_i以概率x_i，否则∞，直接包含当前自然LP独立激活模型。因此普通CRS/correlation-gap下界至少1/3；其是否monotone不能从statement擅自假设。原C08若只要非monotone>.279已覆盖；若要monotone必须重新核查性质，不能自动比较。

本轮2020–2026交叉检索未发现一般c猜想的完整解决；这不等于证明仍公开。新论文随机size模型严格更广，不能把其1/3当成我们两尺寸sharp结果。

### 4.2 固定x的类内uniformization严格失败

容量1，大类两item尺寸a=7/10，小类三item尺寸b=2/5，a+b>1；可行集是一个大或至多两个小。

x=(3/5,13/50,17/100,17/50,23/50)，自然LP成本99/100。

取w=(2,2,1,1,2)，精确期望最优利润除wᵀx为117253/187500≈.6253493333。所有“每个尺寸类的正权重统一，允许任意item零权删除”的向量中，最小ratio为52726561/84062500≈.6272301673，由(2,2,1,1,1)达到。严格差237199/126093750>0。

验证不是浮点拟合：Fraction枚举全部32个激活集，再枚举全部support；对固定support，类间权比u/v的目标分段线性分式，breakpoints只有0,1,2,∞，故四种比值覆盖连续最小值。`exact_uniformization_counterexample.py`及json可直接复现。

**精确排除范围。** 排除“固定x时最坏权重可在每尺寸类统一”这条承重引理，即使允许零权subsupport。没有排除同时改变x的全局对称化，也没有反驳0.4323猜想。

### 4.3 Bernoulli拆分/Poisson化方向不固定

取a=.7,b=.4，A一件确定激活、B两件各概率.1，全部profit1。自然LP成本.78，分母1.2，Eopt=1+Pr[两B皆现]=1.01。把一件B拆成两件各概率.05、同尺寸同profit，期望资源和分母不变。B现在三个概率(.1,.05,.05)，Pr[至少两现]=.012，故Eopt=1.012上升。因此不能把“无限拆分到Poisson”当成自动降低ratio。

双Poisson均类权toy仍有用，但只是受限极限族。对于nomixing a+b>1，可行(X,Y)闭包边界不是错误的.5X+(1/3)Y≤1：最小cost在X≥Y时为(X+Y)/2，X≤Y时为(2X+Y)/3。脚本已用正确边界。1201个边界点×4种权比grid最小c在(X,Y)=(2,0)；数值不证明一般下界。

## 5. 至少四个实质不同的新增候选

### C16. 三资源、两轮廓的子模价格成本分类【C；分类驱动】

**精确对象。** A∈R_+^{3×n}仅有两种非比例资源轮廓u,v，列是s_i u或s_i v；要求全b,w启用集值子模。问哪些u,v具有此性质，或者对固定b给可检验必要充分条件。此处不再靠“第三方向禁形”，因为方向仍只有两种。

**机制差额。** C01二维充分性依赖可逆价格映射使bᵀy线性。三资源时相同(p,q)可有多个y，正确对偶价格cost变为c_b(p,q)=min{bᵀy:uᵀy=p,vᵀy=q,y≥0}，是分段线性凸函数。若证明其在二维价格锥上子模，上述格证明仍可用；若不子模，应构造启用集反例。把几何轮廓、容量b和cost折线放入同一分类，比直接说“低秩矩阵”精确。

**保底/主目标/伸展。** 保底：一个3资源2轮廓最小反例或证明一切都正（仅lemma不足独立稿）；主目标：iff+多项式识别/证书+非integral类别；伸展：任意资源数固定2轮廓及assignment耦合。**最强objection：** 可能所有两轮廓在任意维本来都由convex二维cost满足子模而直接推出；若是则不是新边界。第一动作枚举cost函数斜率及测试其lattice inequality，而非继续A随机扫。

**最终有限义务已闭合，候选淘汰。** 根部要求直接证明或反驳后，本组在`C01_ARBITRARY_DIMENSION_TWO_RAYS.md`建立新Claim C01-v3.1：任意d、至多两列射线时，对所有b,w启用集LP值都子模。证明用二维价格向量的显式min/max分裂系数，在原d维对偶变量上直接保持和，不依赖crosspartial或价格实现唯一性；有效价格成本的边界也已独立证明。故这个三资源切口不是开放题，回收为C01充分方向扩展，不列主攻。高维两射线不必要：I_3有三射线而值函数模。

### C17. AW舍入对非线性coverage效用的下尾界【C；工具迁移驱动】

**源头。** Arndt–Moseley–Pruhs–Zlatin，arXiv2607.09268v1，Thm17：strongly λ-bounded sequential selection process对线性a∈[0,1]^n，Pr[aᵀX≤(1/5−δ)aᵀx/(λ+1)]≤4exp(−δ²aᵀx/[3(λ+1)^3])；Lemmas15–16证明AW在k matroids上stronglyk-bounded。

**精确派生题。** AW输出S，f是归一单调coverage function、单item边际≤1，F(x)=E[f(R(x))]。能否给维度无关下尾Pr[f(S)≤cF(x)/(k+1)]≤Cexp(−c'F(x)/(k+1)^3)，先固定明确c,c'，再扩到monotone submodular。源文给线性covering constraints，不应把其“submodular maximization应用”错说已给nonlinear objective本身的下尾。

**toy/承重义务。** Coverage atoms高度重叠时，不能固定一个modular lower bound且让其在x上达到F(x)：由f(S)≥∑_{i∈S}m_i只能得到某条chain的modular值，可能远小于F(x)。需引入exposure时的随机边际，证明总conditional drift与quadratic variation被F控制。线性Thm17不能直接plug-in。

**成果层级。** 保底：对disjoint bounded-overlap coverage得到真实variance lemma（可能只是地基）；主目标：一般coverage的dimension-free theorem及一个原线性定理不能覆盖的多目标服务例；伸展：all monotone submodular。**最强objection：** 可能由self-bounding/Talagrand+AW已有proof一行推广，或AW非monotone使一般f期望本身都达不到所需benchmark。必须先核查AW期望保证对f的适用条件；没有这个条件不锁主目标。

### C18. 有界batch alternatives的random-element OCRS【C；结构扩类/定量机制】

**源头。** Ma–MacRury–Zhang，arXiv2403.05378v3（2026-08-11），Thm3.4用affineplane证明L资源random-element OCRS的1/(L+1) barrier，标准单element OCRS和L-partite另有严格改善。§3.3与AppendixD用修正unionbound、两个blocker同时出现的正概率突破barrier。

**精确新切口。** 固定L≥3，每batch最多q=2个互斥alternatives，batch独立、产品占≤L个unitcapacity资源，使用原自然exante LP。问是否存在ε_L>0的(1/(L+1)+ε_L)-selectable OCRS，或者给q=2已tight的具体构造。不要泛提“负相关更弱”：用q限制和原文pair-blocker项明确。

**为何不是现成特例。** q=2不蕴含L-partite。L=2的paper硬例本来每batch两个alternatives，故不能把命题写成所有L≥2。L≥3时affineplane每batch有L条平行线，q=2剥去那个具体完整hardcore，但不证明所有hardcore消失。

**成果层级。** 保底：对L=3,q=2写最小hardLP或正的pair-blockerlemma；主目标：全L≥3的explicit improvement和matching obstruction/参数边界；伸展：batchsize q与resourceL的插值。**最强objection：** affineplane可能通过padding/gadget在q=2重现，或者改进仅是原AppendixD代数的直接替换。首动作：把q=2约束代入原Lemma3.7/ D.2的交叉batch nonconflicting pairs下界，看是零还是严格正，不做无目标算法搜索。

### C19. 路径/环路低支持arrival permutations的sharp rationing CRS【C；新视角与精确优化】

**源头。** Ma–MacRury–Stein2502.09521v1 Thm1.2–1.3给forward/reverse两个orders的rank1 exact保证exp(ρ/2)/(1+ρexp(ρ/2))；ρ=1为.622459，介于单order.5和uniformrandomorder1−1/e。两方向源于mobilepantry同一路线反走不增加距离。

**精确新切口。** 固定循环路线，允许r个切点的cyclic rotations及其reverse，共≤2r个order，分布可依已知x选择但不依activation。rank1 ∑x≤1，求最佳通用selectability α_r及如何构造orderdistribution和在线policy；先r=2（4个orders），并给sharp small-LP dual obstruction。和knapsack C08不同：这里重点是受限arrival entropy/route结构与公平服务，不是offline weightedrankgap。

**真实价值标准。** 只有得到严格α_2>.622459、或证明任意固定有限r仍卡在同常数并揭示机制，再给α_r的定量规律，才比任意加几种order有内容。若r≤n且rotations本来能由旧singleunitLP直接出1−1/e，便作为baseline淘汰。

**成果层级。** 保底：r=2的最小对抗实例及精确政策LP（地基）；主目标：sharp α_2与算法，或循环routes完整1−1/e theorem且多资源扩展有真实新义务；伸展：knapsack两尺寸及routingcost约束。**最强objection：** 低支持order/secretary已有dense literature，可能以random-order distributions或pairwise independence形式全覆盖。本轮只读到源文，没有完成该分支新颖性审查，当前是储备。

补充去重：MacRury–Nuti–Vondrák **Prophet Inequalities and Online Contention Resolution for Matchoids**, arXiv2609.20939v1，Thm1.3/Cor1.4已给一般k-matchoid randomorder (1−e^{-k})/k，adversarialorder1/(k+1)。不能再把“把这两个常数推广到一般matchoid”作新题。该文§1.1明确仍问randomorder界对k-matchoids/ k-matroid intersections是否tight；原问题A巨大，只建议用C18类结构切口，不直接主攻一般tightness。

## 6. 与另两线前排的battle意见

| 比较对象 | 本组相对优势 | 本组最强劣势 | 判断 |
|---|---|---|---|
| 有限权重原子势函数/分类 | C01已有完整且很短的双向证明与最小禁形；C06可快速证伪伪差额。 | C01可能被一般格定理直接覆盖，尚无实际GAP算法提升；势函数若有新等价刻画+动态后果，贡献链更完整。 | 不凭完整proof就压过博弈线；先比较“已知定理覆盖”和“最小独立成果”。 |
| 公平分配heavy-item FPT | C01输入更干净、量词明确且无隐藏parameter指数；C17/C18与随机运筹训练契合。 | heavy FPT若精确参数化自然重物品、现有算法不能直接调用，20天完成包更像完整论文；本组C08核心归约已失败。 | 当前不能说GAP整体优于heavyFPT；保留C01/C17继续判别，其余不占默认主攻。 |

根部应按对方确切定理而非路线名比较；本文件没有看到其他agent最终exactcards，故不虚构其已证明/未证明的细节。

## 7. Primary链接与核查位置

- Sergeev2020/2024: https://arxiv.org/html/2404.00041v1 ，§4.1 Conj4.2、§4.3、§6；已读对应正文。
- Ma–MacRury–Stein2025: https://arxiv.org/html/2502.09521v1 ，§1.2、Thm1.2–1.5、§4；已读定义与theorem，不宣称审完全部technicalproof。
- Sarpatwar–Schieber–Shachnai2018: https://arxiv.org/pdf/1705.06319 ，pp1–3、Theorem1；已读matroid+knapsackstatement与通用算法比较。
- Ma–MacRury–Zhang2026v3: https://arxiv.org/html/2403.05378v3 ，§3.2Thm3.4、§3.3、AppendixD；已读affineplane结构与pair-blocker接口。
- Arndt–Moseley–Pruhs–Zlatin2026: https://arxiv.org/html/2607.09268v1 ，Definitions11–12、Lemmas13/15/16、Thm17；已读关键过程假设。
- MacRury–Nuti–Vondrák2026: https://arxiv.org/html/2609.20939v1 ，§1.1 Thm1.1–1.3/Cor1.4、明确tightness问题；只用于已知覆盖。
- Jiang–Samaranayake: https://arxiv.org/html/2208.11832v4 ，§7明确改进Algorithm1理论界/新算法建议；注意HTML首页文本日期2026-08-24而arXiv版本标签2024-10-10，引用时保留确切v4，不凭页眉认作新版本。

## 8. 可运行入口与未决义务

- `python battle_gap_tools/experiments/exact_uniformization_counterexample.py`：无依赖exactFraction证书。
- `python battle_gap_tools/experiments/two_class_attack.py`：scipy/ numpy，seed20261020，60 fixed-x worstweightsLP；3个uniformizationviolations；双Poisson只是grid。
- `python battle_gap_tools/experiments/two_ray_search.py`：scipy，300随机实例完整启用集检查，不当作定理。

下一首要动作：独立审查C01 iff与C06 pipage，随后price-lattice文献去重；C08停止沿已反驳uniformization推进。第二优先：C17先核AW对nonlinear f的期望接口，C18先检查q=2能否阻止原hardcore。没有满足新颖性与最小完整结果前，不建议把任何一个包装成已选定20天必成主目标。
