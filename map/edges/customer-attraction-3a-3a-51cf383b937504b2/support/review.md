# 同枝信用、固定归属、真实源与税包络的完整3A比较

本包为 `customer-attraction-3a-3a-51cf383b937504b2` 的22核心、5只读端点比较。按Root给出的pushed归属，owner为Boss6，request为 `3142d2fcd7884fc3b073a8578a8f0669`，definition pin为 `4c4e7f8a890018274250ba208dbd7d6ab38d1d1a77aa96b3596f04dea7704a08`，Root观察远端tip为 `d609d620f5c85950321cdc44ef642fc2f31dd0da`。worker仅实读clone、在本仓外写独立产物；没有Git、队列、凭据、网络、Library或科学程序重放。Root的round47预读仅作定位，本包逐核心的判断基于当前实读，不继承其为本包主覆盖。

交付四条新关系：两条整目标关系、两条局部贡献关系；并精确复用已canonical的旧27点两条独立延拓排除关系。9个核心linked，13个核心isolated-after-review。没有needs-decision，没有将上下文比较当逻辑边。原任务两条overlap均为in-packet：整数凸全O式与SG1、固定前缀租金式与幽灵预算边界，均在本包实际解决；没有声明follow-up对，不制造后续任务。

## 1. 同枝锐信用完整推出N和CK容量结果

固定同一实际叶的覆盖集C及负载c_x≥1。每次访问v来自实际前缀，使用同一完整策略的真实强制枝；只删该枝的未来者。旧前缀负载p≤c、当前查询位a∈{0,1}、删后/删前负载d0=p+a+h、d=d0+ell≤m。正确费用为

\[
 B=E+G=p(1/c-1/d_0)_++a(1/d_0-1/d),
\]

不是删除前旧损失的正部加退款。Q=p(1/c−1/d)、R=p(1/d0−1/d)满足E=(Q−R)+；p=c=a=1,d0=2,d5时，G+Q+=11/10而正确B=4/5。这只是代数双计见证，不冒完整SPE反例。

主引理逐情形证明0≤B≤1−1/d≤1−1/m。固定(c,p,a,d)的K由两个端点给出：

\[
K=\max\{0,a/(p+a)-a/d,p(1/c-1/d)\}.
\]

p=a=0按零；d0≤c部分单调减，d0>c部分单调增，若左端不可行，其候选不超过右端。故B≤K是真正锐终局标量包络；不把每个端点都说成同一完整SPE可实现。

对非负lambda_vx，逐客户跨**全部**访问求和即可得到完整目标：N要求Σ_v lambda_vx≤1，则Σ_xv lambda B≤(1−1/m)|C|；CK要求Σ_v lambda K≤q_x，则Σ_xv lambda B≤Σ_xq_x。无限可求和族由非负部分和极限得到。CK允许K很小或零时总访问质量超过1，所以不是N的改名。这里给的是已证完整限制域定理，relation_mode为unconditional；没有未证前提潜入这条聚合推导。仍open的是从遗漏需求构造满足共同容量的路由，以及为整行IC选择客户间一致的非负乘子。客户端可以比较任意lambda，不意味着原整主题IC能任意逐客户重权。

新边 `cag-same-branch-sharp-envelope-implies-n-ck-capacity` 以锐信用为唯一source，N/CK对象为target，whole_result覆盖其整条statement。

## 2. 固定全局owner：两个正确结果不互相冒作付款

owner两核心共享相同F/UNIT代数，但结论和承重步骤不同。对非owner覆盖者，e=1/(1+k_nonowner)，不依owner槽是否覆盖。强制比较前缀Z^i=finish_sigma(T1,…,Ti)的第s个非owner查询已有至少s个非owner覆盖，求和≤H_a−1。owner支持在该客户的比较覆盖槽；先为客户一次抽**全局**owner，sigma和T及全部真实叶固定，再取平均。无需SPE或T最优，不保证分数owner可还原为满足其它条件的整数owner，不能把actual前缀换成强制比较前缀，也不能逐leaf重抽owner。

另一核心的端点账是F_Q(Z0)+J_Q=|O|+ΣGamma_i。T任意合法时恒等式即成立；SPE只给Gamma≥0，T最优才给|O|=OPT及静态F≤OPT。对两固定owner，J_Q′−J_Q=−(F_Q′(Z0)−F_Q(Z0))；抬端点与signed债精确抵消。PREFIX误差上界不能当作负误差项的有利扣减，正部去槽债也不是J。上述信用不推出INV，INV也不推出H_a−1，所以两个核心均按实读比较记isolated-after-review。与本包ROLE钱包及同枝CK不同，均无已证明映射使其中一个自动支付另一个。

## 3. 真源、十三行及两个有限点

NEW-SOURCE-CUT-v1的整个一般定理已读：任意合法有序h恰余三人，源规定最终收益u，强制T后同一sigma真P/Q；全目录K须约束包括新增P/Q在内的每个标签。源IC权1、安全查Q权3/4、P容量权5/48及真末Q查X/Y/Z权1/24、1/24、1/6精确给7u/4+5K/48≥Σmin_pq L。安全价允许偏离后重选后继；四态放松没有共同P/Q实现逆命题。六人B-off代入T=R_Bij、X=Ti、Y=Ci、Z=Bj；此处Z是查询名，不是Z回复族。

十三行的全部F和13份非负slack逐项核过。节点为g=(A1,A2,A3)、R=sigma6(g,T,Y)，(g,R)真后继P/Q，S=sigma6(g,R,T)，Z=sigma6(g,A4,R)。S/Z来自不同有序历史，绝不能识别。D0=b+r+p+q与D1=b+r+t+s属于不同真终局。actual第三位安全价用前二位背景e+4，末价用实际前五位ell+1；不是强制枝的背景。十三个权依次为90783,19980,994,30434,23194,30434,3435,6480,13500,16545,16545,4860,19980，成本合90783u4+30668u3+60868u6，Q三查合37950。同一个s同时参加真第五位偏离、Q→S、旧Z→S和S自身IC，必须在同一(p,q,s)八态上极小。每条IC只有客户求和后非负。

双步BR运输另外成立：背景B=g+T下U=f−G，G对称，两条真实BR的slack之和恰U_B(R,S)−U_B(Y,S)≥0。但其独立权在十三行中为零，不能说它贡献该分离，更不能用它将真实三人源叶(R,P,Q)换成(R,T,S)。故M-8aa核心与投影只作精确比较，isolated-after-review。

旧27原生点b4c40bc9…与后28点480f7a96…分别读完整hist/组/原子结构；28的全部28份R/Z位和长有理权已显示阅读。两者16hist/194组相同，24共同签名全部改权、删旧3添新4；不能互换W/K、ZZ或负差。完整原py仅静态读，两个完整原报告的lhs/rhs/slack与输入SHA实读并作存储有理相减。保存的810/840负值按精确合同复用；本轮未调用phi、evaluate、旧verify、LP或全部旧行生成器。

旧27两canonical边保持当前端点pin，按文件SHA直接复用：

- `map/edges/customer-attraction-3a-3a-00330dfee5f33608/no-k-thirteen-projection.json`：保同hist、同有名B-off组的R/Z四态**绝对质量**y_Hg及actual利润；单位客户完成按同一正lambda将y和u同缩放。z项使Phi的交叉差13500/((a+1)(a+2))>0，只保一维边缘不够。无K、RR或跨组耦合消费，因此新增任意大小主题而保持此数据仍被排除。
- `map/edges/customer-attraction-3a-3a-00330dfee5f33608/whole-catalog-k-source-projection.json`：保所需旧会员/质量、源利润，并以lambda K0约束**整个完成目录含新标签**。K0约0.235是规范化坐标，不能当单位客户绝对容量；全部质量/利润/成本/负差同乘lambda。放宽到更大K会改变左端，该负差不能直接迁移。

两条为独立替代证明，不合成ALL，不凭负幅度声称行锥包含，也不refutes“旧指定1143行有低福利共同会员点”。旧3889保存表全结构消费，全部3889存储slack的符号统计与原报告相合；没有重建行或重验IC。原body与程序页/60ZZ审查提供成熟证据的不同owner和执行范围均保留。CA27只是本包只读端点；本包NEW与十三行核心各自全文阅读，不能用旧包覆盖代替它们的完整statement审查。

## 4. 税包络：完整条件贡献与未付存在性

静态Q须在查询前固定，且同一个Q服务所有T。逐客户1_(a>0)≤(a+b)/(1+b)给OPT≤E_mix≤E_*；在BR最小背景处tau≤(m−1)BR再给E_*≤(2m−1)theta。有限minimax没有把背景改成观察查询后选择。静态CCE的独立均匀删位构造给E_mix≤(2−1/m)E_muW，但没有E_muW≤给定顺序sigma的W，不能搬CCE预算。

在同一sigma任何长m−2有序P及其真实beta循环C，两个真实slack平均加对称交叠消去得到所有T同时E_C f_(P+a)(T)≤u(P)。税增量D_C来自**同一**循环，且D_C≤u(P)。所以E_mix≤m u(P)+tau(P)+D_C。它不推出E_*≤该循环预算。

新ALL边把完整静态定理与完整循环定理共同用于充分方向：若该原sigma内确有P,C满足m u(P)+tau(P)+D_C≤2W，则OPT≤E_mix≤2W。推导完整，accepted+conditional；contribution只写这一固定策略的条件结论，remaining明确对每份原SPE找到这样的P,C尚未证明，较强E_*预算亦未支付。没有将候选整条标whole_result。m≥2为循环域；m1可直接处理，但不是这条循环源定理的量词。

## 5. 完整图整数凸式对SG1的实质局部收紧

原声明overlap为M-790与SG1。任一真实O行客户系数为独立上包络减w delta，整行加权后非负。取完整O图、每无序族对一条边、固定客户间一致lambda≥0；每客户各族背景同b_x、重数同k_x，故有效权同w_x=lambda/((b_x+1)(b_x+2))。令Lk_x=q t_x+rho_x、ell_x=max(0,2k_x−q)。M-790给真实总缺额至少

\[
D_x=w_x[q\binom{t_x}2+\rho_xt_x-\binom L2\ell_x].
\]

因此Σ_x[Σ_e lambda E^O_e,x−D_x]≥0，是SG1在此子域的更紧必要式。组合等号在族内自由重排放松由连续k位置模q平衡列实现，保完整本地直方图；不保证同一真实目录/历史约束允许该重排。q3,L4,k1时，SG1通用Xi=0，D=w>0，显示实际增量，绝非单纯引用。新边以M-790为source、SG1为target，accepted+unconditional contribution；整条任意D/O图SG1不由此子域单独证明。所有离轨A_r还须共同付到根W。

R-373d原标准库脚本与286B报告全文静态读：1200随机定义、150半密度、135clique，第三段真范围q1…6/L2…6/k0…q；其lambda2、b0使w1。它们核定义代数和取等构造，不核完整SPE。本轮不重跑。

## 6. 固定前缀租金式完整专化为幽灵预算障碍

另一个声明overlap是M-2c95与幽灵预算边界。取两单位客户、A={x,z},B={x}；每位行动者无论未来如何，x份额总为1/m，B不覆盖z，而A有严格正z份额。因此全有序历史恒选A确为完整严格SPE，W2。用M-2c95的r2/s1固定队列公式，在H=A^h上x被A/B两次命中、z只被A一次命中，得到

\[
E_h=2h/((h+1)(h+3))+h/((h+1)(h+2)).
\]

分式拆为−2/(h+1)+2/(h+2)+3/(h+3)，求h0…c−1即3H_c+5/(c+1)+3/(c+2)−13/2。取m9,c7时所有辅助配置h+3≤9，求和1879/840、超W的199/840，且随c对数发散。这完整支付目标的存在实例、全历史激励、Eh、闭式、数值和精确反驳范围。新specializes边为whole_result，relation_mode unconditional。

它没有refutes正确局部租金恒等式。固定H的望远镜分子必须不变；跨h加入新人后不能再以原队列望远镜。Omega只作分析，不是合法偏离。此完整例否的是无权重复累加储备，不否有共同权重/一次收费的运输，也不否half。原1022比较/100闭式核验和11984回归按各自保存合同复用，未重跑。

## 7. 其余核心逐项边界

- 自由分数定义：t_r(b)的r−1是确定静态竞争质量。Jensen给t≤v，嵌入t_(r−1)(b+1_A)≥t_r(b)；r1直接成立。原自由q不能限制到actual支持，log势KKT也不等同t的minmax。其逐人FF已有银行反族，定义不携带该顺序付款。与本包36客户的特定均值负载失败不同，未获完整逻辑边。
- 门槛跳变M-d81：两人alpha/beta/z在beta=alpha/2的tie允许末位复制A，L(A)与Theta右跳alpha/2；固定sigma选择另一个tie后继可在两侧同为SPE，根收益连续。它反的是跨面单线性表示，不否Farkas或本税包络固定策略条件式，亦不推出ROLE可行性。
- 五索引核心：固定同一sigma，25真实安全比较求和给CFM；七节点×十菜单70行仅用各族边缘，未假设跨族同索引dot。1759的27+70+1386+276计数合同已实读。707浮点点、未执行230类原型和当前已证五人half各自独立；它没有本包六人真源的同域映射。
- 任意人数条件平方：同一个signed Möbius表保全部≤m模式、formal pattern次数+2deg f≤m平方及all-a全树形式IC；齐次化次数和完整谐和空间分解已读。二阶整数L(L−1)期望−1/4否非负共同客户表示。另一个真单位客户同图源不保矩值，不能混成合法负客户游戏。signed W=OPT1，不是half分离。
- 删除regret M-4e3：任意非负整数辅助b,d，删除后保持同一尾history策略映射；K_j是合法当前T的前缀分母上界最大，不是所有真实叶Delta的最大。R_j=max_T(Delta−A−Gamma)，K−A−R是非负最小残差。65例实现证据不升级删后SPE或跨叶CK；与同枝B在对象、删除位置和费用上不同，不能直接合账。
- 辅助锚点M-be54：原12条m2…7的AB/DE输出全部读；其辅助收益模型、原CAG五人七主题有限证书、未认证float发现分开。W=4m+1或4m均高于半值，既无普遍m定理，也无模型迁移。
- 纯交换M-3e15：只需正支持包含比较O，回复新增覆盖在O外为零，纯基数交换自动成立；11正hist/d1是指定1269点的支撑证据，未重验其全部行。九项带价必要式仍可排那个点，因此纯覆盖交换无区分力不等同所有真实IC无力。
- 实际删除支持核心：三人36单位客户、完整43历史sigma、查询5在实际三删位背景恒12，故支持内任何混合不能cap到34/3；特定均值负载最大397/35只超1/105。自由Q2给v3=10，m3强聚合本例反而成立。全K不交目录并人数变3K，有静态上界15/2+5/(2K)；不与固定三人Cartesian混同，不从六人路径猜全树。它不反本包自由t或E_mix候选。
- 七极大核心：130放宽列和四个乘子精确最优−3080653/133198702；五列非负对偶消去四系数，原始有理解给全130下界。漏扣(6c+15e)f/j已被旧源撤回。此模板负最优不提供共同目录/真实后继实现，不能接成六人half反例，也不能借其它不同细化预算补成原四族成功。
- 固定比较ROLE：INIT/I补余/R流均共用同sigma/B/T；去ROLE紧凸非空、MASS总量|O|、节点密度和PRICE-DP都已读。每context≤u_k不能合成同角色所有context≤2u_k。常数价格PRICE-CUT已经是half，目标未被消元证明。来源反链只给严格future每层来源库存，actual-prefix目标不在GENERAL-DENSITY域；与固定owner平均或同枝CK没有免费资金桥。

这些13个isolated核心均有实际比较、准确已证范围和未付义务。没有根据主题相近造hub、没有提出论证缺步的proposed边，也没有要求为每个open候选另立任务。

## 8. 阅读、证据与新旧运行

`reading-ledger.json`列本任务全部声明refs及实际完整/section读取范围、27对象pin、必要证据SHA。只要求section而实际按段阅读的资料按精确标题记录；其余实际全文读取的文件不冒作只核字节。超出声明范围的原真源md/py/报告、两个点、旧3889存储表及旧canonical review另外记录。原native JSON的全部字段/数组作结构消费；长数据的逐字段摘要和内容digest在`structured-consumption.json`，不将模型未逐屏显示的百万表说成逐字人工核对。

本轮有理操作仅解析保存数据、比较存储分数和报告lhs−rhs、统计既有slack符号、核原生结构/版本与SHA；没有生成或求值新的IC行、重算810/840、旧ZZ117612、旧3889、LP、全树、系数扫描或任何科学main。解析证明为当前已读推导，不将历史PASS归成本轮运行。最终SHA清单不hash自身或receipt，receipt不列自身为asset。Root安装后按原生bind/check发布，再以真实远端owner/request/pins完成done。
