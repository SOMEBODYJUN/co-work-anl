# UM 90a2 round40 数学比较

本轮按当前任务 owner Boss6、read-add request `80475a88751840bb96e97f3515130347` 工作。12 个核心、STAR 与 uniform affine theorem 两只读依赖和任务指定的 40 个去重正文文件均完整实读；另完整读取 STAR 的 f0d0 证据页与 affine theorem 的 bb7f 证据页，共 42 个去重正文。所有范围按当前 registry/input_pins 核对。未运行任何旧审计程序、LP、大证书或全树。下列历史计数只按原 SHA 与成熟合同复用，不是本轮新实验。

## 1. 占位面至固定 K 三半调度

新 accepted whole 边 `um-90a2-occupation-face-to-fixed-sink-three-halves` 将一般 2K 引理实际接到给 T 的完整三半算法。模式的宏信息只能是 occupied/empty；occupation 向量必须是覆盖全部宏的 transversal base。两个最优宏匹配沿同一路径双向交换，两个最优性方向推出等权，交换森林给 `dim G≥|F|/2`。模式纤维维数为 `Σ(a_h−1)−|F|`，故原模式面维数至少 R/2，K 侧行的投影顶点使 R≤2K。

该引理单独不保预算。完整目标另外执行：全私有任务共同尺度 `T/(4N)` 的 sink 向上取整 DP，保真实 home 时间和实际原任务回溯；参考模式每 sink 总量≤5T/4；枚举≤10K² heavy homes 的具体模式，余者只留总出口≤T/(8K) 的模式；用全部 y 坐标 lex 精确 LP 取得投影顶点；带下界宏匹配覆盖全部宏与强制 occupied homes，再按支持模式回填唯一 home 私有组。仅≤2K个home改变，故每sink≤`5T/4+2K·T/(8K)=3T/2`。empty home≤T；occupied私有≤T/2加实际宏≤T，同样≤3T/2。所有原任务恰一次。

T=0先零端检查，p>T剪枝、空库、无宏与无私有任务分支均保留。固定 K 才是总位多项式，次数依 K；lex 位长由同一原扩展多面体顶点坐标控制。OPT≤T保参考分支，所以 FAIL⇒OPT>T；成功不判定OPT≤T。未知 OPT 的宏边>OPT/2 promise 是另一身份，不加进本目标。历史12次回填是检查事件、去重6份调度，有限枚举不是通用 LP/scheduler 实现。

## 2. 稀疏、STAR 与收缩族

精确复用 canonical ALL 边 `um-ea0e151c-sparse-and-star-transfer-to-contracted-gap`，文件 SHA `72a953143d0016d847a8b44bede5ef8a39f60860aa6ac532ecac483f262bf4b5`；不重建同一关系。

原族参数 k≥3，r=(k−1)/k，s0最小使kr^s0≤1，M=(k−1)k^(s0−2)，H≥s0且2^(H−2)≥M，γ=2^(2−H)，T=1+1/k<θ=2−1/k<2。M按外送有身份block任务数计，不再乘k−1。原OPTθ的下界来自每活跃核心至少下传两条边，≥2^(H−1)活跃底簇迫z负载≥2；上界为单路径调度。逐有限原边分别存在完整CONFIG(T)条件点，不是共同base或多query law。

指定左右端点序列每步F恰两枚unit，2>T且每删一余1≤T。F外域互斥使每外列至多一F，故命中列质量Q_F=q_F≥1。通用转移充分条件是Q≥1，外部任务期望q≥1本身不够。每query独立沿argmin追原祖先，正向所在星抽质量时目标机器优先，才保最终强制边质量1。每实际步全局至多一次split，重复配置质量须相加。

超T的θ上界需要额外论证：每被删端点两unit总2>θ，所以原θ调度至少一F任务在外；选其真实外端压成替代任务，峰不增。仅T可行性iff不足。反向argmin/补集恢复峰≤max(B,T)，因T<θ给终态下界θ。终态按核心、三unit终端及z逐类无星；不推任意收缩次序。逆向不保所有原probe。有限k3/H5的729/1051→405/727、324次收缩、1778终态边、1480支持等均为原冻结展开证据。

四机器bag/三机器separator若有完整交集联合一致可胶合为真实调度；只单机器边际不够。这是更强合同的逃生口，不是通用CONFIG oracle或任意SA/SDP层级下界。

## 3. 固定槽与最小工作量面

核心入口把两个不同矩阵族分开。真OPT凸包族：一个unit big、m²−1枚1/(m+1) tiny，均匀真实最优分解给x=1/m；每机恰m槽，任一覆盖匹配均使big机有m−1 tiny，峰2−2/(m+1)。选同图最佳matching不能修；槽外移m−1 tiny即达OPT1。额外one-destination约束下最小Hamming三角数是另一合同，且不能断言所有合法修复均最短。

最小工作量面族另用big时间m、home small时间1、外端1+1/m，真实OPT=m+1/m；阈值LP最小工作量面全部small固定home，全部big端正。仅其支撑整数输出峰2m−1。整数迁移s的成本恰m²+s/m，预算q/m才对应≤q件；一般Δ对应floor(mΔ)。允许任意固定正乘法成本松弛时相对增加趋0，不得声称排除。该资源不提供occupation有限模式、共享固定sink或原T见证，故本包没有从相同“舍入”名词造边。

## 4. 收费、统一停车与仿射合同

两层标签收费针对显式投影多重图与原 A/B/C 资格：每顶点至多一重标签，任意状态选择可完整调度到1+floor(D/2)/D≤3/2，精确值1+μ/D不提供μ优化器。奇数q平行边强列表NO可仍有OPT1+1/q。出现异权文字池的另一完整调度依赖每变量每极性所有eligible occurrence总预算≤1、子句至少二occurrence；首项共享槽和两两配槽给共同覆盖，未选首项侧偶数项和≤1/2。两模型无任务/机器映射，不互换锐性或升一般hardness。

统一D停车的非空主点与B≤1分支有OPT=2−β*，vacancy为显式transversal对偶，用Rado/整数matching保全部aux和原ports；published two-value resource-matroid后端只按其精确合同使用，未在仓库实现。B≥2全部ports留轨精确达B；U空时另unit b-matching。该域既非MaxMin Theorem15的已知最优玩家类型，也非固定K/唯一home三半域。

仿射review区分三域：任意非空显式关系+均匀权对每任意local选择的Hall；宽Cartesian rectangle、marks和任意state权只构造某个indexed-state共同选择；完整并行sum关系任意state权亦只构造某个选择。固定intercept注入、变量tags和同一allocation都承重，不能由共同三半数字互移菜单自由度。该review本身只记证明/内部读序及字节范围，不为所有affine hard images提供新命题。

经正式 read-add 真实 uniform theorem 后，新 accepted contribution 边 `um-90a2-affine-hall-to-free-vacancy-parking-three-halves` 将其完整矩阵恒等嵌入停车的无 aux 子类：主点=constraint、标签=indexed allowed state、parent=state private、port=原 incidence、D=kR，所有未选任务保留。aux空的 transversal 拟阵秩零，vacancy对偶为自由拟阵；共同不交保留即可满足全部资源约束。对每个任意local选择、每个group子族F，用注入截距的至多一交和tags分离得 `|N(F)|≥k(R+1)|F|/2≥ceil(kR/2)|F|`；普通quota整数matching给每group b=ceil(kR/2)个真实资源。于是β*≥b/D，实际所选parent峰2−b/D≤3/2，其余parent与资源≤1；unit selector使OPT≥1，亦给相同实际相对比。这个子类无需4+η后端，真正全满足赋值才另有β*=1、OPT1。该边只作为parking的子类贡献，未支付一般aux、任意束或未实现后端，也不以review本身作逻辑源。

## 5. 匿名token的共同四阶与原身份边界

一个共同degree4 functional同时覆盖所有组与未动contexts，满足Boolean/one-hot/计数理想至四次和共同M2。下降阶乘核在显式k标签域内定义；k1线性替换、r0/k均保留。类别计数n0=k−rA,nw=Xw的平均/contrast分解给M1 PSD；跨组与未动context交叉相消，head-head非负用共同四阶平方。这没有推出M2或所有原行CONFIG。

给定k=r4点取210个四集uniform ν及signed β，10个纯半四集各1/8、100个2+2各−1/400，δ1/100。aggregate M2 PSD的210函数空间与55pair/head空间两个Schur扣项谱不同，余谱均正；不能混成同一个谱。形式核的二次Q平方−1/150是kernel失败；任意保aggregate≤4矩的原身份扩展必须满足整体head×affine-context K PSD，其半符号方向−1/25另外证明given-point无扩展。不同context的单独交叉块不能称PSD。必要K不充分；13机6任务实例有实际OPT1，不能由坏点拒绝原输入或得近二gap。

## 6. 七态原星

正偶d,s，2≤s≤d/2，η=s/d，h=s/2，T1+η。真实七态law按(C,H)给同一个L、共同M3及原one-hot。唯一负slack类(1,d)质量η³/1000产生负载2；实际OPT1由另完整调度给出。任意全局二次q代端点后，对称平均为P2(H)+C(a+bH)，两支共享二次项。五点评估系数平方和≤16/η²、五正类mass×slack≥η/40，支付唯一负项；零平方和使用≤，主archive已修正旧原件严格号，非新错误。

逐行CONFIG是另行pair trade，保持C,H,CH,H(H−1)，不与真实law混成同一T支持。仿射背景只自动支付指定v行且v无新增payload；孩子、父行及shared heads须另证。加入b>η payload或合并unit heads会分别破localizer/CONFIG pair。12参数、前三组完整M3/global-q2是有限审计，未重跑且不改一般解析证明。这与匿名点非扩展、稀疏逐query存在的量词不同，未建立逻辑边。

## 7. 两个外部算法范围

M-04dd…是ST1993线性变速、整数快慢端、非负运行费用、正μ的cost+μCmax二近似。f(t)与μt决定保留区间，实际值≤f(t)+μt；最小makespan最优解为整数的引理才给整数搜索与O(log(n max u)) LP调用。普通有理固定速矩阵、非线性/离散速度或不同目标不能直接继承此搜索。固定槽的坏输出不否定该二近似。

M-1faa…是MaxMin一般加性估值的Theorem15正式声明：big阈值OPT/2且最优分配玩家类型信息除O(log n)项外给定。当前13页源和资源页缺技术报告[23]的完整算法证明，因此仍unassessed；不能靠条件推导隐藏缺证、不能借二度MaxMin Theorem12或two-value resource-matroid算法补证。本轮按当前冻结输入记录精确缺口，不替缺失证明补造算法。

## 处置

本任务没有声明overlap_comparisons，故不造closed_overlaps。其余核心的isolation是上述实际比较范围中的结论，并非不存在任何未来关系。新必要read依赖仅通过Boss串行read-add；没有修改clone、队列、规范正文、源证据或Git。
