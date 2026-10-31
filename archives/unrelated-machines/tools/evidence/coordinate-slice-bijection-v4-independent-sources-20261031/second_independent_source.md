# conditioned-bijection 坐标切片 v4：陈述先行独立重构

审查者：boss11 内部研究者 literal_gap_implementation。
唯一先读对象：`coordinate_slice_permutation_extension/coordinate_slice_permutation_v4_exact_statement.md`，SHA256 `dfe2def5608363c3615f1d2eb7085e6b30598196f746b112e9fc28f5e52ef7f5`。
本 Exact 自身已经完整定义原 P，因此无需读 v1；未读其他agent scratch、作者proof或询问其证明。
ID/version：`UM-Q-COORDINATE-SLICE-PARTIAL-MINREP-COUNTEREXAMPLE-v4`。

## 结论与认证范围

H、I、J、K 均可独立完整重构，无 standing fatal。H 是概率存在与 simultaneous 所有cheaplists保证；I 是每seed实际完整调度；J 是每seed的精确有理配置证书；K 只在good-H seed上给近1的精确整数gap。四层没有相互冒充。

没有构造或认证一个具体good seed，没有源NP-hardness、source-length多项式编译、UM主目标反面或全球新颖性认证。下列给自足证明，包括严格阈值方向，不依赖未读旧证明。

## H：conditioned随机双射仍存在部分覆盖NO

记每左列表 L_i、右列表 R_j，大小 l_i、r_j，成本约束为 sum_i l_i+sum_j r_j<=2gD。

### 1. 特殊标签0贡献很小

由 pi_ij(0)=p_i，因0导致覆盖的边数至多

    sum_j |R_j intersect {p_1,...,p_D}| <=sum_j r_j<=2gD
       <=rho D^2/8,

最后用 D>=16g/rho。这里即使某些左点没有0，或同一边也被非零标签覆盖，都是安全上界。

### 2. 每个非零覆盖事件的概率

对固定 i,j 和 alpha!=0，pi_ij(alpha) 均匀落在 Sigma minus {p_i}。故由非零alpha覆盖该边的概率至多

    l_i*r_j/(Q-1) <=(gD)^2/(Q-1).

最后一步仅用 l_i+r_j<=2gD。不同边的事件独立，因为各边的conditioned permutations独立；同一边内部不要求独立，union bound已足够。

D=ceil(16g/rho)<=20g/rho，sqrt Q>=(100g^2/rho)^2=10000g^4/rho^2，所以

    (gD)^2 <=sqrt Q/25,
    (gD)^2/(Q-1) <=2/(25sqrt Q)<Q^(-1/2).

此处 Q>=2，严格常数有余量。

### 3. 同时所有列表的union bound

总共有2DQ个“顶点-符号”，成本至多K=2gD。用 x=1/Q 的生成函数估计（K大于字母总数时也成立），列表总数 H_list 满足

    H_list<=sum_{k<=K} binom(2DQ,k)
          <=Q^(2gD)*(1+1/Q)^(2DQ)
          <=e^(2D)*Q^(2gD).

这只作数学计数，不枚举列表。

固定一份列表，令Y为由至少一个非零左标签覆盖的随机边数。它是独立Bernoulli之和，均值至多D^2 Q^(-1/2)。取 t=3rho D^2/4。由标准upper tail

    Pr[Y>=t]<=(e D^2 Q^(-1/2)/t)^t
       <=[4e/(3rho)*Q^(-1/2)]^t
       <=Q^(-t/4)=Q^(-3rho D^2/16),

因为 Q^(1/4)>=100g^2/rho>=400/rho>4e/(3rho)。阈值t远大于均值，所以该形式合法；阈值是实数时同样可由指数Markov得出。

若一份列表总覆盖>=rhoD^2，由特殊0部分<=rhoD^2/8，必有Y>=7rhoD^2/8，特别Y>=t。因此坏事件概率至多

    e^(2D) Q^(2gD-3rhoD^2/16)
       <=e^(2D) Q^(-gD)
       =(e^2/Q^g)^D <1/2.

最后 D>=16g/rho>=32，Q>=2D+1>=65，g>=2，故e^2/Q^g<8/65^2<1/2已经足够。得到概率至少1/2，对**全部**成本<=gN列表同时覆盖严格少于rhoM。列表允许看见整个seed后再选；uniform union bound覆盖这种自适应选择。

每seed的投影都是双射，且每条像为整个Sigma，因此每个b的像交确为整个Sigma。特殊条件只固定一对映射，不影响上述每条边在其余域上的均匀排列与边间独立性。

## I：每seed同一全局state0的真实近满树

所有玩家 i 都选 state0。对每个该state根，取固定的D-1个邻居，例如b_1,...,b_(D-1)。在每个选中b下，被省掉的坐标为pi_ij(0)=p_i。

对其余每个坐标：若是p_t且t!=i，则允许值为[D] minus {t}；若不是这些p_t，则允许任意固定D-1个值，例如[D] minus {D}。这在每一层都选恰D-1个孩子，与全局固定坐标次序兼容，因而给完整(D-1)叉深Q树。

同一b下玩家i的全部选叶满足

    x_(p_i)=i，且对每个t!=i，有x_(p_t)!=t。

因此玩家i与i'的叶集不相交：前者在坐标p_i'排除i'，后者固定为i'。不同b本来不同资源块。其余坐标和根舍掉哪个b不影响此证明，整个构造无中途换state。

### 所有机器、所有任务的实际sigma

- selector_i 放state0根，时间1。
- 所选pruned树内的port jobs都送孩子端，时间1；其他ports全部留父端，时间1/D。
- 一台所选内部机有一件incoming unit（根为selector，其他为父port）及恰一件未下送small，因此负载1+1/D。
- 其他内部机没有incoming unit，自己D个ports全部留父，总负载1；包括所有未选states和state0中剪掉的全部分支。
- 共享资源机只承载选中叶的incoming unit，由上面的全局叶不交至多一件，负载0或1。

每个selector及每条port恰放一次合法端，没有遗漏非active分支或原P之外的预载。故完整原P的实际C<=1+1/D。这个上界对所有good/bad seeds成立。

## J：CONFIG阈值恰1的精确证书

为每台内部机器写两种配置：

    active：只含它的incoming unit job，权1/Q；
    inactive：含全部D枚outgoing parent-small jobs，权1-1/Q。

根的incoming是本玩家selector；其他内部节点是唯一父port。两种配置都负载恰1；机器权重和恰1。

对共享资源机器(b_j,x)，可用terminal port jobs的数量恰Q。具体地，玩家i的state alpha有一个叶port在此机器，恰当且仅当

    x_(pi_ij(alpha))=i。

因pi_ij是双射，此玩家的这种alpha数量是 |{beta in Sigma:x_beta=i}|。对i=1,...,D求和为Q。每个符合条件的(i,alpha)对应唯一叶port（坐标编译的leafmap injective），因此恰有Q枚不同incoming unit jobs。

为这Q枚jobs各写singleton配置，权1/Q；资源机器配置和恰1，负载都1。

逐任务覆盖：每selector在自己的Q个state根active配置中各占1/Q，总覆盖1。每内部arc或terminal port在父机inactive配置中覆盖1-1/Q、在其child内部机active或资源singleton配置中覆盖1/Q，总覆盖恰1。所有machine和job条件精确满足，没有把机器间相关性冒称一份真实调度。

所有权分母为Q。证书非空配置数<=2*(内部机数)+Q*(资源机数)，列出inactive D-job集合的总长度正好按outgoing port数计；资源singleton数按terminal port数计。因此证书大小/构造时间相对**显式完整P**为多项式（事实上按finite-incidence编码线性级，外加机器/任务编号位数）。

因为每个selector所有有限处理时间均1，在T<1时没有任何配置能覆盖它，所以T_CONFIG>=1。上述证书给<=1，故恰1；玩家数D>0，不能用空任务例外躲掉下界。

## K：strict iff 自足重构和网格

### strict<=1等价于原源全满足

给实际C<=1。每玩家selector选定一个全局state alpha_i并在根占unit1。根的全部D个small ports都不能留父，因此全下送；递归每个子内部机也是incoming1，整棵所选state的D叉Q树必须全部下送。于是在每个b_j，玩家i必须占其全部切片

    {x:x_(beta_i)=i}， beta_i=pi_ij(alpha_i)。

玩家i与i'的这两个切片：若beta_i=beta_i'，同一坐标要求两个不同值i、i'，故不交；若beta_i!=beta_i'，两个坐标可分别指定为i、i'，其他任取，必有共同x，资源机需两件unit而超1。因此各玩家切片两两不交，当且仅当同一b_j的全部beta_i相等（D>=2）。取该共同beta_j即得到原projection game的完整单标签满足赋值。

反向若原源有alpha_i,beta_j满足所有边，则选各alpha_i状态全D叉树，所有ports下送，其他state ports留父；同一b_j下各玩家切片按同一坐标beta_j的不同值i分开。所有内部机与使用资源机负载<=1，得到完整实际strict解。

### good-H排除strict并给精确值

若good-H seed存在满满足单标签，其总cost为N<=gN，覆盖全部M>=rhoM，违背H的严格上界。故源不满满足，strict iff给原P不存在C<=1。

所有处理时间为1或1/D，任意实际机器负载、makespan都在(1/D)整数网格。显式P有限，每job有限端非空，完整分配有限且OPT取得，所以OPT>1强迫OPT>=1+1/D。结合I的完整实际上界，恰有

    OPT=1+1/D， T_CONFIG=1， ratio=1+1/D。

这是近1的精确gap，不是近2困难性；没有把source weak lists的NO和UM近二NO混同。

## 位复杂度、存在性和scope

D,Q、所有permutation tables是有限显式对象。对给定seed，I/J的标签、坐标和配置均可在完整P显式长度内构造/回算。私有树每state D^Q 叶，整体P可能指数于源编码；本v4明确不承诺binary D,Q的统一多项式source compiler，审查未引入这种承诺。

H给有限概率空间上好seed存在，不给确定性polytime验证NO的算法。精确uniform permutation sampling的具体随机运行时间约定也不是本项hardness前提；即使只把H看作有限存在命题，反例逻辑足够。若后续要一个实际被验证good seed，必须另外提供检测/生成证据，不能由本稿冒领。

source图确为simple balanced D-regular K_(D,D)。H不需要PCP像、common-source hardness或UGC；每seed完美公共像来自bijective而不是全局YES。不可自动对good seed做任意多互不相交copy并沿用同成本soundness，原Exact已正确保留这一量词边界。

本稿只否定该具体坐标切片编译的充分解码合同：双射/均匀纤维/公共投影像及CONFIG1同时存在，仍可在good-NO源上有真实1+1/D调度。没有一般UM反面或近似求解器，全球新颖性、实现和外部审查均未认证。
