# 59条候选的实际比较：保留能形成完整成果的切口

**最新贡献尺度补充：** [完整问题、完成价值与旧NE关系](notes/main_problem_scope_and_value.md)回应用户准备投入几十个team的要求；来源强度之外，按完整定理能改变什么重新分层。全常数容量种类BMKP、一般非对称精炼等是主目标候选，现有两容量/affine草稿和短分类不自动足够承担全部投入。原有按短周期可推进性给出的排序保留为历史判断，当前不据此锁定唯一题目。

**本轮题源复核补充：** [作者原题、母工具与团队子题分别评价](notes/source_authority_audit.md)核对本分支及另一选题分支的前排来源。下面保留此前按可推进性给出的排序；加入用户强调的资深专家题源后，AP-02、FG01、FG02、两容量BMKP应重新进入共同前排比较。重边具体题源以青年作者为主，FA17/18为团队派生；不再把模型创始作者的名望转借为具体题的背书。本补充不升级数学结果或认证新颖性。

更新时间2026-10-20；主研究者boss37。**当前先推进近二值图的公平参数算法；并行保留资源轮廓的LP子模性分类、Nash克隆不变性分类。** 这是基于证明与反击的研究判断，不是成功率、发表保证或最终定题审批。

六名gpt-6.1-sol ultra子研究者已分两批实际完成，全部注入用户完整指导。环境只有三个子槽，没有声称六人同时在线。首轮45条、第二轮新增14条，当前[候选池](candidate_pool.json)共59条记录，[逐条索引](CANDIDATE_INDEX.md)给全部名称、来源和状态。该数包括被覆盖、合并及已闭合的子题，**不是59个已认证开放问题**。旧UM-TARGET-v1及其一般反面仍OPEN，退出默认主攻。

## 1. 不同类型采用不同价值标准

| 论文/idea类型 | 实际核查项 | 本轮判断变化 |
| --- | --- | --- |
| 作者明确问题A | 最新版本与后续是否仍开放；承重障碍；局部保底到整篇成果的差额 | NA02确为A，但Fisher–Lindahl已有对偶覆盖，淘汰；FA01的一般FPT仍未解，不冒充已解 |
| 作者建议方向B | 方向是否为精确猜想；派生限制是否自然；是否只是已知特例 | 非binary separable的共同函数子类已有直接log-gradient接口，表面标签不是差额 |
| 工具派生C | 可迁移结构、输入输出、非免费oracle；是否只是一次代入 | type scaling有更好势却使用HKS旧工具；coverage+pipage已有.316基线，普通常数改善降级 |
| 分类驱动C | iff、有效识别、禁形与自然对象；是否仅重述定义 | GA01有二维iff，NA03有active-cell量词消除/FPT/coNP；仍须排一般旧理论覆盖 |
| 结构扩类C | 限制保留的困难；差额是输入压缩、算法机制还是换图名 | forest阈值闭合；普通固定tw cactus已有XP，必须保留binary重数或任意heavy结构差额 |
| 定量/随机机制 | 最新基线、随机模型、保证的量词及有限观察范围 | 背包普通CRS基线更新为1/3；固定x均匀化和任意Poisson拆分都被反例击穿 |

不以作者名气、文件数、模型投票或算力预算替代这些判断。每个前排都有完整成果形态，以及一个会使它降级的具体异议。

## 2. 当前主线：近二值图的公平分配参数算法

母论文：Kanellopoulos等，*EF(X) Orientations: A Parameterized Complexity Perspective*，[arXiv:2512.25033v5](https://arxiv.org/html/2512.25033v5)，2026-10-07。§5明确问多重图EF定向按heavy边数的FPT及treewidth参数去除shared weight的问题。heavy指至少一端整数价值≥2，不能随意换阈值而沿用Claim。

| 对象 | 身份与已完成进展 | 真正未决义务 |
| --- | --- | --- |
| FA01 一般multigraph、k-heavy EF | A；原Thm13只simple。普通内部包平分有k=1反例；unit支持forest的阈值算法已完成 | 一般f(k)poly或自然复杂性边界；≤2k特殊端点本身不是压缩证明 |
| FA17 simple最小charity、任意非负删除cost | C；3^k poly完整算法已完成，root复核未见缺口 | 全球查重、紧指数/核化或实质多重图扩张；短推论是否足够成稿 |
| FA18 unit-support cactus、binary重数与任意fixed-heavy偏置 | C；forest单接口闭合，单环变为系数{1,2}整数TVPI | binary-bit算法或边界；不能调用只给伪多项式的integer TVPI当答案 |
| FA02 tw+单边最大权重 | A；旧算法依赖同pair总shared weight | 实际证明计数ILP结构参数；原图tw不等于ILP primal/dual treedepth |

### 完整算法的承重机制

simple charity枚举每条heavy的左/右/删，共3^k。固定后，二端正值非heavy边均为(1,1)。单位边组件有正收益锚点时，任意EF partial解可逐边激活并补回所有单位边；无锚点时，含环组件全保留可行，树组件必须全删。剩余转成最低入度的二分流。可补回/必须删给出最小删除成本，而非仅找到某个partial orientation。

[完整证明](notes/heavy_edge_residual_and_charity.md)处理simple假设、全顶点公平比较、巨大二进制权重与实际输出。1200个simple小例与全部3^m部分方向真最优一致；4200个任意偏置森林残差与完整整数oracle一致。计算核程序，普遍命题依据书面证明。

**暂列第一的理由**：已有精确算法、失败机制、自然母问题和可继续接口，能组织成接近二值时的公平可计算性研究。**最强异议**：已完成两项都可能过短，而一般多重图扩张仍可能难。如果查重显示只是短推论，又没有新的复杂性或压缩机制，应降级，不能把若干小lemma硬凑成论文。

## 3. 优化备选：资源轮廓决定启用LP的子模性

源工具：Kulik–Sarpatwar–Schieber–Shachnai，*Generalized Assignment via Submodular Optimization with Reserved Capacity*，ESA2019，[arXiv:1907.01745v2](https://arxiv.org/html/1907.01745v2)，Theorem1的scalar assignment LP子模性。下面的矩阵分类是C，不是作者原题。

固定A≥0，定义φ(S)=max{w·x:Ax≤b,0≤x≤1_S}。

- **二维完整分类**：A有两行时，对所有b,w≥0均子模，当且仅当非零列至多在两条正比例射线上。
- **全维充分性**：任意资源数d，至多两条列射线仍保证全部b,w子模。
- 高维不主张必要性：I3虽有三射线，值函数仍为模函数。

两个类型价格的逐坐标min/max可以用互补非负系数分裂原对偶向量，保持成本和；每个hinge只依赖所属类型价格。二维三射线的中间列可被两端正组合替代，形成严格三列反例。[二维iff](notes/two_resource_lp_submodularity.md)与[全维充分性](notes/two_profile_lp_in_arbitrary_dimension.md)均经root重构，未发现缺口。

**价值要求**：符合工具本质→自然类→禁形→识别的路径。下一步应排查Topkis、连续子模和资源替代性文献，再找真实assignment接口或高维结构。**最强异议**：充分方向可能为经典格理论短推论，目前没有GAP新近似因子；不能因有完整iff就认证独立文章。

## 4. Nash备选：多面体凹偏好的克隆不变性

Becker等[2509.08767v3](https://arxiv.org/html/2509.08767v3) §8末的一般cloning分类为A。我们的u(δ)=min_{r≤R}a_r·δ、非负有理矩阵识别为C。

本轮完成：点wise共享超梯度判据；2^R poly(m,R,bits)识别；一般R的多项式有理/Farkas失败证书，从而语言在coNP；两项目全保持、三项目两分支反例。没有coNP-hardness、complete或一般R多项式结论。

有效识别并非只改写KKT：先枚举active rows；每个可正坐标分别求LP见证，平均后仍在同一精确active cell并同时使全部可正坐标为正；再做逐坐标与共同超梯度LP，消去连续分配和任意clones量词。

[几何正文](notes/budget_cloning_and_concave_geometry.md)、[coNP证书](notes/budget_cloning_complexity_certificate.md)、[版本/旧理论审计](notes/budget_cloning_source_audit.md)分别记录算法、位长和来源。v1曾有一般凹性断言，v3已收窄；不能说本反例反驳现行定理。

**价值要求**：一般R的tight complexity、可读禁形或新的均衡算法后果，才能补成更完整项目。**最强异议**：Tseng/Dlask的coordinate minimization和active-face理论可能直接覆盖；KKT、光滑共享gradient和普通多面体枚举不是新工具。R=2识别已经完成，不再当待攻题。

## 5. 决定性去重：论文仍写open，不等于可以立题

NA02要求weighted Leontief、binary有理预算的精确多项式NE。root先形成weighted-log高精优化与有理恢复框架，独立攻击发现更短的linear Fisher接口，再查到已有覆盖链：

**Brandt等2305.10286v4 §4.4 Proposition1（NE=Lindahl）→ Tao–Zheng2511.04572v2 §3 Theorem2及dual utility公式（public Leontief↔private linear Fisher）→ Orlin2010精确算法。**

同一v、b，Fisher prices p和quantity allocationλ给公共总分配δ=p及实际个人支出X_ix=p_xλ_ix。MBB最大v/p恰为Leontief临界最小p/v；预算行和、分配列和与零价都已核实。

AAMAS2026正式版§8仍列open，但直接数学覆盖链已经足够。**NA02作为新算法主目标淘汰**，保存[自足归约与来源](notes/leontief_fisher_known_interface.md)。不是宣布新解决作者问题，也不推测作者未同步的原因。它体现了先内化工具、再比较真实差额的必要性。

## 6. 其他候选怎样前移

| 候选族 | 保留理由 | 前移条件 |
| --- | --- | --- |
| FA03/04/05 冲突图极大EF1和均衡部分着色 | 树定理和块接口具体；complete multipartite构造已核 | 后续查重通过，环块/模块有实质机制 |
| FA11/12 两大小/两预算chores EF1 | 伪多项式EFX、多项式EF2与EF1特例之间有差额 | 保留housekeeper与预算可行子包定义，闭合交换/密度证明 |
| NA01/06 随机BR仙人掌、两类pair策略PNE | 随机token或matching接口具体 | 核原hard gadget是否已在该类；区分全局势最小和任意NE |
| NA05 l1均衡上的社会成本选择 | 任意NE已解，优化输出不同且集合非凸 | 阈值cell产生算法/困难性核心；固定m枚举不是独立成果 |
| AT01/02/03 有限权重势、分类、平滑动态 | 64/59全人数证书已完成 | 排HKS/CF/HKM覆盖，补统一最优性或非平凡算法步数 |
| GA17/18 AW非线性下尾、两alternative OCRS | 期望接口、pair-blocker是明确义务 | 核benchmark或q=2仍含hardcore，不能无目标改常数 |
| GA19 低支持循环order配给 | 随机OR/服务路线，目标精确 | 查低支持permutation旧文，得严格新界或匹配障碍 |

FA07三值chores网格主要是已知反例邻域观察，列储备。AT04/06、GA03/05/16、NA02等保留淘汰原因；不删除失败来提高命中率。FA19/20等仍有全文义务，明确needs_verification；摘要不当全文定理。

## 7. 数学进展与有限证据分开

| 记录 | 实际依据 | 不支持的扩大结论 |
| --- | --- | --- |
| 全人数64/59势 | 初等不等式完整证明；61206条Fraction边际检查 | 最好NE阈值、新颖性、poly改善步数 |
| forest阈值/charity3^k | 归纳/补全+flow证明；4200/1200独立oracle对比 | 一般multigraph FPT、weighted deletion实验全覆盖 |
| LP二维iff/全维充分 | 对偶构造与三列反例；300小例浮点仅探索 | 高维iff、GAP改进因子 |
| cloning FPT/coNP | 有理LP、KKT、Farkas及位长；6个浮点原型手例 | coNP-hard/最优复杂性或免费数值oracle |
| 已知四人13chores | 62720类型矩阵、142真删除子实例、473参数点 | 全局最小反例或全参数区域定理 |
| 背包均匀化障碍 | 32激活集Fraction、分段比值完整断点证明 | 允许改x的全局归约失败或一般猜想否定 |

[root独立复核](notes/round2_independent_root_review.md)记录推理、边界和未查新义务。[实验manifest](probes/round2_manifest.json)保留代码/冻结输出hash。研究脚本重跑先复制，避免改写冻结JSON。

## 8. 本阶段完成与接续

已完成广搜、两轮实际推导、交叉攻击、决定性覆盖核查、候选去重、证明与证据落盘。探索无审批/路线登记门槛。当前不再重复已闭合的小例，而围绕前三个成果包的真实差额推进；新覆盖或反例可随时改变排序。

沿用原work.py、token和已有研究分支/公屏，没有新建分支。远端保存只按checkpoint回执报告；结构检查不认证数学和新颖性。
