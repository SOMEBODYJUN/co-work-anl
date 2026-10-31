# Fractional rematching：rank独立Exact-first审查 v1

审查者：rank_deficiency_fee，2026-10-18。仅clone外scratch。此记录只认证指定v1；不改repo、Work/Git、原statement或既有记录。

## 1. 实际对象、路由和结论分层

实际全文读取的候选Exact：

`/workspace/scratch/038d9dcc4cac/fractional_rematching_extension_statement_only_v1.md`

whole SHA256：`33e8a8ec34d17ed605bf4b752ff4210d1bc9a68a46c8f673dd05f384754d7948`。

未读作者Proof（尚未解封）、general/rainbow其它新推导或root的A证明策略。先只据Exact独立闭合下文A的证明与匹配算法，随后按授权独立访问primary DLRV paper的Theorem 1、Theorem 10、§2.5列式与检索返回的相关片段，核文献归属。本次没有全文审完paper全部算法或其有限位实现。

本记录尚未冻结时，root通知作者另立v2，外部source-backend候选常数将从20000改为60000，并提示paper最后max-to-sum的保守因子；本记录不把该提示冒记为本agent独立发现。此时尚未读取v2，以下冻结v1真实范围，不倒填其新版数值或结论。

**结论：A为独立可完整证明的有限分数benchmark匹配引理，包括zero、正边perfect matching可行、填全及真正最大乘积匹配的确定性总位多项式算法。B–C作为明写E1–E3的条件蕴含成立；本记录不验证这些外部接口已由DLRV实现，不认证20000为其source-backend常数，也不认证1e12在任意未量化slack下都充分。C的单位证书、benchmark、两种log-CONFIG optimum、positive singleton matching前件和低utility比例推论均可独立证明。**

## 2. A：残余分数投影和平均budget

记b_i(S)=v_i(S∩B)，h_i(S)=|S∩H|。只考虑显式y的正entries。对每个active i（V_i>0），定义

    r_i(S)=b_i(S)/V_i；

对inactive i定义r_i(S)=0。Inactive的v_i(B)=0及monotonicity保证b_i(S)=0，因此未除以零。

把每个active i的y投影到B：

    z_{i,T}=Σ_{S:S∩B=T} y_{i,S}。

该z的agent行和为1，B每item容量不大于原y容量，所以是(A2)确实量化到的可行fractional family，而非一份假设已知的integral allocation。因而

    Σ_{i,S} y_{i,S} r_i(S) ≤ c n。

另由H的n枚item及(A1)，

    Σ_{i,S} y_{i,S} h_i(S)
      =Σ_{h∈H}Σ_{i,S:h∈S} y_{i,S} ≤ n。

令w_i(S)=r_i(S)+h_i(S)，可得加权总budget

    Σ_{i,S} y_{i,S} w_i(S) ≤ (c+1)n。          (R1)

此步真正需要对所有fractional residual families的(A2)；若只有integral welfare bound，不能无损代入这个投影z。A2本身的验证、V_i的寻找均非本引理算法提供。

## 3. A：局部最大值与正性

令

    m_i(S)=max(V_i, max_{h∈S∩H} v_i({h}))，

内层空最大值取0。Subadditivity对S∩B及H中的各singleton逐次使用，给

    v_i(S) ≤ b_i(S)+Σ_{h∈S∩H}v_i({h})
           ≤ w_i(S) m_i(S)。                 (R2)

对inactive i，b_i(S)=0；对active i，b_i(S)=V_i r_i(S)≤m_i(S)r_i(S)，所以两类均成立。

所有列出且y>0的configuration均v_i(S)>0。故(R2)强制w_i(S)>0和m_i(S)>0，所有后续log有定义。特别Vi=0时，S∩H至少有一个positive singleton；一般subadditive估计的反面正性足以保证这一点，不需XOS或submodular。

由weighted Jensen及Σ_{i,S}y_{i,S}=n，

    Σ y ln v_i(S)
      ≤ Σ y ln m_i(S)+Σ y ln w_i(S)
      ≤ Σ y ln m_i(S)
          +n ln(Σ y w_i(S)/n)
      ≤ Σ y ln m_i(S)+n ln(c+1)。             (R3)

此处benchmark是semantic正实数，不要求算法精确表示它。

## 4. A：partial matching到完整positive matching

对每个正entry(i,S)，若存在h∈S∩H使v_i({h})>V_i，按固定索引选其中最大singleton的h，并将该y质量指向原边(i,h)；否则把该质量暂记为agent i的outside质量。此时m_i(S)=V_i；由m_i(S)>0，发生outside的agent必V_i>0。等号tie选择outside也无妨。

所得矩阵x_{ih}行和≤1、列和≤1，因为每条所选边来自h∈S且原y满足item容量。每条被选原边的a_{ih}=V_i+v_i({h})≥m_i(S)>0。记行deficit r_i=1−Σ_h x_{ih}、列deficit c_h=1−Σ_i x_{ih}。恰有n个agents和n个H items保证两侧总deficit相同R。

若R>0，填

    x'_{ih}=x_{ih}+r_i c_h/R；

若R=0，直接x'=x。得到doubly stochastic n×n矩阵。只有outside质量为正的行参与补全，而这些行Vi>0，所以任意填边a_{ih}≥Vi>0。对一行的outside质量，总新增log-edge收益至少其outside质量乘ln Vi。故

    Σ_{i,h}x'_{ih} ln a_{ih} ≥ Σ_{i,S}y_{i,S}ln m_i(S)。   (R4)

由bipartite matching polytope整数性（或Birkhoff分解），x'为支持上的positive-factor perfect matchings的凸组合。于是至少一份matching的log-product不小于(R4)左边；真正最大乘积正边perfect matching更不会差。

结合(R3)，得

    Σ_i ln[V_i+v_i({π(i)})]
      ≥ Σ_{i,S} y_{i,S}ln v_i(S)−n ln(c+1)。

指数化并开n次方即(A4)。此为原H上的bijection，不是复制item或assembly新标签。所有factor严格positive也由上面的正边support证明直接给出。

H不必是某个先行最优singleton matching的像；A只需|H|=n。(A2)仍必须关于这个实际给定H的补集B成立。初始最大matching在B所述backend中是额外来源接口，不应回灌成A未写前件。

## 5. A：exact maximum-product matching的有限位算法

算法只需a_{ih}=V_i+v_i({h})，可求n²个singleton值；剔除a=0的边。上述证明保证正边存在perfect matching，可先作普通matching检查。给定前件不成立时，本引理没有额外保证；也不承诺从value oracle验证全域monotonicity、subadditivity或(A2)。

为避免把任意real-log assignment当exact-bit算法，取每个正a_{ih}=A_{ih}/B_{ih}的一种显式整数字表示，使分子分母均≤2^b，其中b由输入factor编码取公共上界。每个perfect matching乘积的分子、分母均≤2^{K_0}，K_0=n b。两份不同乘积P>P'的比值满足

    P/P'≥1+2^(−2K_0)，

所以

    ln P−ln P'≥2^(−2K_0−1)。

令每条边ln a的有理近似误差≤e，其中

    e=2^(−2K_0−ceil(log₂ n)−4)。

两份matching的总log近似差误差≤2ne，严格小于以上任意非零真实log-product gap。对这些有理近似权运行确定性maximum-weight perfect matching，所得matching因此也是**真正**最大乘积matching；原乘积相等的ties随意。近似精度只需输入总位长的多项式位数，不是按分母数值或1/min(a)展开。

所需log近似也可自足实现：对正有理a用binary幂缩放到[1,2)，再以t=(a−1)/(a+1)的缩放后值用

    ln a=2 Σ_{k≥0} t^(2k+1)/(2k+1)，|t|≤1/3，

及同样的ln2级数恢复幂次。达到指定二进制精度只需多项式项数，有理中间位长亦多项式。无需精确比较transcendental log sums或一般irrational benchmark。

因此(A4)的强exact算法成立，(A5)对任意显式epsilon>0可直接由同一更强算法满足，无需另引数值假设。H/B配置不需指数枚举；y仅是有限support和semantic guarantee，算法甚至无需读取其benchmark来优化matching。

## 6. A退化和编码

B空时上述projection为empty配置值0，不损证明。A空时所有Vi=0且所有v_i(B)=0；每条正y entry仍强制某个H positive singleton，partial matching实际上各行已满，不需以Vi0的行填全。重复configuration entries可聚合也可保留，budget、logs和matching质量均线性计入。

Singleton可以zero，只有factor a=0边被排除；Vi>0行仍可通过任意H item填全。n≥1及H恰n distinct items避免空H/空agents退化。有限rational假设排除infinite值和无限编码；value-query的实际返回位长按Exact明确计费。所有证明分母为0的潜在处均已单独分支，不暗用log0。

## 7. B：只认证明确conditional composition

E1得到同一原U上的H、B与Vi，并使active集合恰对应v_i(B)>0，于是inactive满足A的v_i(B)=0。E1必须提供**fractional**残余界，而不是只拿integral welfare近似或unknown optimum allocation作输入；寻找Vi、residual support及数值误差均属外部义务。

给定E1在这份实例/这组H,Vi上成立，A产生comparison matching π*。E2若确如v1(B1)在一个概率≥p0的同一成功事件上对全部comparison matchings成立，便可取π*；或直接有对这份最佳comparison matching的同概率保证也足够。不能把“每固定π各有概率p0”弱化版本在依赖随机H,Vi之后未经条件化直接套用；Exact要求的共同comparison保证避免该量词问题。没有指数union bound。

代入A4即(B2)，同一p0不损，外部E3的固定安全slack只乘最终常数。v1写20000(c+1)d²，给定c2,d5/2时算术确为375000；这是**假设(B1)真时**的条件常数，不证明paper backend满足20000，也不拿paper main integral ratio充当log-CONFIG gap。任意固定外部slack下存在某个绝对integer rho，但其具体值依赖被验证的常数与slack；不从“slack为某个常数”自动认证1e12数值。

## 8. C：unit-FSLP形成benchmark1与singleton匹配前件

每indexed normalized clause非负且总和1，所以其positive support P_{i,s}非空、v_i(P_{i,s})=1；任意S的v_i(S)∈[0,1]。将lambda的每条正entry作为y_{i,P_{i,s}}，重复support可相加或保留，agent行和1，item容量由unit-FSLP保证。全部正entry value恰1，故B(y)=1。

还可不输入未知allocation而认证backend所需positive singleton matching存在：每个lambda正entry选P_{i,s}中一枚positive clause item，将lambda质量分配至(i,j)。得到agent行和1、item列和≤1的positive singleton fractional matching；因为v_i({j})≥p_{i,s,j}>0，整数性给原U上的全agent positive injection。此处只保证positive，不保证每agent constant utility或unit integral allocation。

每个可行log-CONFIG的positive entry值≤1，故目标≤0；刚得y使目标0。因此item≤1版optimum0。Item equality版也为0：从y依次给每个item j补缺口1−load_j，当前不含j的跨全部配置质量为n−load_j≥1−load_j。按固定顺序给整条configuration加j，最后至多拆一条entry消耗精确缺口。处理其它item时保留已有items，所以原item等式不再破坏。每item至多增加一条support，至多初始support+|U|条，行质量不变。Monotonicity与normalized上界1使原value1一直为1。此填全不需要指数配置枚举或unknown integral allocation；binary有理拆分也只涉及输入质量的和差。

Explicit XOS的value/XOS-maximizing-clause查询由表直接求最大值。对有理价格p_j，demand可对每条clause计算Σ_j max(p_{i,s,j}−p_j,0)，取最佳clause并返回该clause的positive差item集合；max_S max_s可交换。因此这些查询本身是总位多项式。但它们并不自动验证外部convex relaxation/support/rounding全部E3。

## 9. C：robust低utility比例和原indexed state

在E1–E3成立后，取最终factor与slack上方的固定integer rho>1，成功时NSW≥1/rho。全部utility≤1，且成功的positive product使每agent utility>0。对任意正integer K，设m个agent有utility<rho^(−K)。若m>0，则其严格低于threshold且其它≤1给

    product_i v_i(S_i) < rho^(−K m)。

但成功又给product≥rho^(−n)，于是K m<n。若m=0，同样有0<n/K。故m<n/K，证(C1)严格不等号。

固定eta∈(0,1)，K=ceil(1/eta)满足1/K≤eta，所以m<eta n。Threshold rho^(−K)为固定rational；对实际S_i扫描原clause表取达到max的一条**原indexed state**即可，duplicate clauses仍保留索引，未拼装坐标。该论证不保证所有agents都有某个constant utility，不能据此下界ordinary min V。

## 10. Primary attribution的实际读取与最终边界

独立访问primary：Shahar Dobzinski, Wenzheng Li, Aviad Rubinstein, Jan Vondrák, *A constant factor approximation for Nash social welfare with subadditive valuations*, arXiv:2309.04656v1，PDF https://arxiv.org/pdf/2309.04656 （本次返回23页v1）。实际检索读取Theorem 1、§2.5 Lemmas 8–9与末尾列式、Theorem 10及§3所列c2、d=2/(1−2epsilon)和375000参数，外加检索返回片段；未全文认证paper全部证明/有限位实现。

Theorem 10的对象是demand-query model的subadditive NSW近似，paper引言定义approximation相对integral optimal allocation。未把它记作原文已述log-CONFIG integrality-gap theorem。A是本记录独立证明的fractional-benchmark extension，不由paper的integral guarantee一句话推出。Paper的外部E1–E3依赖及source常数仍须单独审。

General XOS不是默认submodular；本证明只用其monotone subadditive性质和explicit表。没有software/finite audit、source hardness、NP-versus-RP或global novelty结论。v1原件不改；任何v2/v3对象都应在另行实际读取后新冻，不能冒记本v1已经认证。
