# 小任务单侧稳定、全机联合舍入与选择复杂度的实际审查

读取目的：核对三个独立身份的审查顺序、证明覆盖与实现输入域。本文合并实际已完成的独立记录，不把模型自评、代码运行或多名审查者赞同当作数学证明。

- UM-TINY-WORK-STABILITY-JOINT-ROUND-v1：A先读Exact独立重构，后实际读作者证明、所调逐行基数引理和最终canonical；给定点构造器已实读并精确重跑。
- UM-TINY-WORK-STABILITY-SELECTION-NP-v1：B先读同一Exact独立重构，后实际读作者§3–6和最终canonical。固定源族的稳定证书选择NP完全；不是一般调度近似困难性。
- UM-SELECTOR-TINY-ROOT-THREE-VALUES-v1：hardness_decoder在B独立稿后另行推导，root收到证明梗概后重构，literature_mechanism后置证明知情审读；此项没有被倒记为纯陈述盲审。

最终正文SHA256为 `6f6d28e2c20290873ea77b6771f213534c92f4f3fec0fbce9f70192261384d83`。root实际阅读全文、以下独立重构及实际读后记录，核对全机同一匹配、所有原任务、绝对阈值、零值和总位复杂度；没有未闭合fatal objection。无外部同行评审与全球新颖性认证。UM-TARGET-v1仍OPEN。

有限证据仅覆盖所列实例：联合槽实现9个成功样例、15个拒绝及5个capped算术检查；parity ell2/3的全部1024/16384个实际分配；三值审计6个矩阵共816208个实际分配。大整数CLI和API修复关闭Python默认十进制解析上限导致的合法输入拒绝，不以它代替位复杂度证明。

原始草稿保留在当前工作目录，本文把其实际内容和精确hash一起存入长期审查；路径本身不是已入库的证据承诺。下面各节是冻结记录的原文，标题级别与原路径如实保留。


---

## A：只读精确陈述的独立重构

原记录SHA256：`286aaf6eee34615752f90bbebd491476b5b380d980db35b5b890c2088bd3eea7`。

# 小任务单侧工作量稳定接口A的陈述先行独立重构与攻击

冻结日期：2026-10-19。

唯一候选输入：`/workspace/scratch/6bd6916818c5/stability_candidate/exact_statements.md`，SHA256 `88443e0efff15113a07e54b93adf6e91fff8c964647417f32905d660de8523d7`，只研究其中A（UM-TINY-WORK-STABILITY-JOINT-ROUND-v1）。未读作者/root或rounding_new的证明草稿，也未取得其证明内容。本文件在作者稿开放前冻结，属于实际独立推导，不是只列攻击问题。

**结论：A按其明确合同成立，未发现反例。** 下文给出完整构造与独立承重证明。一般K的有限余量可通过整数计数多面体的顶点分母推出；该多面体和alpha_K都只用于分析，实际算法无需生成它们。未对外部新颖性作任何判断，亦不主张A关闭一般UM目标。

## 1. 全机实际构造

记总输入二进制长度为B。输入含合法处理时间矩阵P、T、显式列出的有理CONFIG点y、delta和二进制整数K。先依陈述把有任意零处理时间端点的job安排到某个零端，并从所有配置中删去这些job。其余job在每条有限端均严格为正，配置仍然合法且保持每个剩余job的覆盖等式。重复的删后配置无需合并；将其视为相同配置的多份概率质量即可。

对每条边取精确边际

\[
x_{ij}=\sum_{C\ni j}y_{iC}.
\]

只有x_ij>0的边进入算法。它们都可用且p_ij≤T，因为其job出现在某个正权可行配置中。每个剩余job满足Σ_i x_ij=1，各边x_ij≤1。

在每一机器i上，将支持边按tiny（p_ij≤delta T）与big分成两份；同一job可以在不同机器上属于不同份。每份内部按p_ij非增排序，并把对应质量x_ij依顺序放在一条线上，切成区间(0,1],(1,2],…，末槽可不足1。槽数等于总质量的上取整；零质量份不建槽。

为每个job和与其质量段正长相交的槽加边，相交长度记为w。全部机器的big槽、tiny槽放进**同一张**二部图。每个job的总w为1，每个槽的总w≤1。因此任意job集合S流向其邻槽的质量为|S|，而邻槽容量总数为|N(S)|，得Hall条件|S|≤|N(S)|。一个确定性二部匹配算法可同时覆盖全部job；把匹配job安排到其槽所属机器。

这里没有分别完成big匹配后才处理tiny的选择问题；一次匹配使用全部角色边，产生一张完整合法调度。单端job的唯一支持机器也在同一Hall论证中。

## 2. Tiny负载的无条件逐机界

固定机器i，tiny质量总工作正是s_i。记非空tiny槽数为h，槽内最大处理时间为t_1,…,t_h。非增排序使第l−1槽（l≥2）在单位质量上的全部处理时间均≥t_l。因此

\[
\sum_{l=2}^h t_l\le s_i.
\]

t_1≤b_i，而匹配每槽至多取一个job，故每个输出均满足

\[
L_i^{\rm tiny}\le s_i+b_i.
\]

若h=0，L_i^tiny=s_i=b_i=0；若h=1，上式仍成立。此结论不依赖其他机器最终把同一job当big还是tiny。

## 3. Big部分的容量与前缀严格计数

定义U_i=T−r_i≥0。每个正权配置C的big总工作满足

\[
\sum_{j\in C:\,big}p_{ij}
\le T-\tau_i(C)\le T-r_i=U_i,
\]

其big数≤K。故y投影到该机器big集合后仍是总概率1、容量U_i、基数≤K的配置分布。

若U_i=0，严格正big边不可能有正边际，big负载为0。以下取U_i>0并将big尺寸除以U_i归一化。

令big总质量q_i=Σ_{j big}x_ij≤K，非空槽数h=ceil(q_i)≤K，槽内最大归一化尺寸为a_1≥…≥a_h>0。若h=0或1，big总负载直接≤U_i。

对l=1,…,h，设N_l(C)为C中归一化尺寸≥a_l的big数。因为第l槽有某一最大尺寸job的质量段与其正长相交，所有尺寸≥a_l的边的总质量**严格大于l−1**，即

\[
\mathbb E_yN_l(C)>l-1. \tag{1}
\]

严格性不因q_i是整数、尺寸并列、质量段端点恰为整数而消失：被计入槽内最大值的job必须贡献正长交集，而不是只碰到端点。

N_l是整数，故(1)推出至少一个正权配置有N_l≥l。它的容量至多1，于是

\[
a_l\le1/l. \tag{2}
\]

这立即给K=1的1、K=2的1+1/2=3/2、K=3的1+1/2+1/3=11/6。若实际h<K，少取正项只改善此界。

## 4. 一般K的独立整数分母论证

现在K≥4，h≥2；d=h−1≤K−1。槽1的a_1≤1，只需证明

\[
\sum_{l=2}^h a_l\le1-K^{-(K-1)}. \tag{3}
\]

按阈值a_2,…,a_h把每个正权配置C的big jobs向下舍入成整数计数向量c(C)∈Z_{≥0}^d：

- c_2为尺寸≥a_2的job数；
- l≥3时，c_l为尺寸落在[a_l,a_{l-1})的job数；
- 尺寸<a_h的job丢弃。

阈值相等时相应半开区间为空，不影响恒等式

\[
\sum_{t=2}^l c_t(C)=N_l(C).
\]

并且Σ_l c_l(C)≤K，Σ_l a_l c_l(C)≤1。设F为实际出现的有限整数向量集合。考虑只用于证明的多面体

\[
Q=\{z_2\ge\cdots\ge z_h\ge0:\ c\cdot z\le1\quad(c\in F)\}.
\]

原向量(a_2,…,a_h)属于Q。令z_{h+1}=0。对任意非零z∈Q，用Abel求和以及(1)，得到

\[
\begin{aligned}
1&\ge \mathbb E_y[c(C)\cdot z]\\
 &=\sum_{l=2}^h(z_l-z_{l+1})\mathbb E_yN_l(C)\\
 &>\sum_{l=2}^h(z_l-z_{l+1})(l-1)
 =\sum_{l=2}^h z_l. \tag{4}
\end{aligned}
\]

严格号合法：z非零且非增非负，所以至少一个差z_l−z_{l+1}>0，而所有对应计数期望都严格超过l−1。

Q有界。由E N_2>1，某个c∈F有c_2≥2，故每个z∈Q均满足z_2≤1/2，从而全部坐标在[0,1/2]。Q非空、闭且有界，线性目标Σz_l在某个顶点z*达到最大值v。由(4)及零点分支，v<1。

顶点处取d条线性独立的有效等式，写A z*=b。A是整数矩阵；每个配置约束行非负且L1范数≤K，每个次序约束行的L1范数≤2≤K，最后非负约束行范数1；b各项为0或1。Hadamard不等式给

\[
1\le D:=|\det A|\le K^d.
\]

Cramer法则使v=N/D，其中N为整数（取D为正后调整分子符号）。v<1推出N≤D−1，因此

\[
v\le1-1/D\le1-K^{-d}\le1-K^{-(K-1)}.
\]

这给(3)。所以每个匹配输出的big负载均满足

\[
L_i^{\rm big}\le\alpha_K U_i.
\]

此论证使用h−1个变量；h受实际输入job数控制。F、Q、顶点、D、K^(K−1)和alpha_K全部不进入构造，均不需算法计算或输出。

## 5. 合并界与稳定推论

同一匹配输出的同一机器上，big与tiny负载直接相加，得到

\[
L_i\le\alpha_K(T-r_i)+s_i+b_i
\]

同时对全部机器成立，没有概率事件或另选局部舍入结果的缺口。

由b_i≤delta T，alpha_K≥1，r_i≥0，若s_i−r_i≤omega T，则

\[
\begin{aligned}
L_i&\le\alpha_KT+(s_i-r_i)-(\alpha_K-1)r_i+b_i\\
&\le(\alpha_K+\omega+\delta)T.
\end{aligned}
\]

这一步没有把均值s_i误当成每个配置的tiny工作；每个配置的big容量只使用tiny下界r_i。

## 6. 统一总位复杂度

构造完全由显式有理边际、排序、槽碎片和无权匹配组成。

1. 显式输入的配置个数和全部job出现次数均≤B的多项式。处理零端、删除job、验证给定点合法性、计算每个x_ij均可用精确有理算术。求和分母若直接相乘，其位长最多为所加输入分母位长之和；重复工作仍仅使长度多项式增长。
2. 每机每类质量q至多实际job数n，其上取整可由有理数整除得到。**不能对K做循环。** 尽管K可能是编码短但数值极大的整数，槽数仅由q而非K决定。
3. 总质量为剩余job数n；每个非空机器/角色份最多多一个末槽，所以全部槽数≤n+2m。每个x_ij≤1的段与至多两个单位槽正长相交，故碎片边数≤2mn（或显式正边数的两倍）。
4. 比较尺寸、前缀和、碎片边界均为多项式长度整数的加乘比较；不涉及alpha_K。确定性增广路二部匹配在显式多项式大小图上运行，输出每个原job的一台机器。
5. r_i、s_i、b_i甚至不必用于算法；若用户要报告它们，也只是显式有理求和、比较及最小值，不引入大编码alpha。

因此存在一个统一多项式p，使运行时间≤p(B)，指数不随K、delta或配置数量参数改变。alpha_K在K为二进制输入时可有超多项式显式分母位长，这不影响算法，因为算法既不求它也不把它作为输出证书。

## 7. 退化与反例攻击记录

| 攻击点 | 实际结论 |
| --- | --- |
| T=0或OPT=0 | 合法CONFIG(0)等式点覆盖的每个job必有零端；预处理后无剩余job，完整调度负载0。无需除以T。 |
| U_i=T−r_i=0 | 该行正权配置没有正工作big jobs，故不对U_i除零；big槽为空，仍有L_i≤s_i+b_i。 |
| delta=0 | 去零后全部支持边为big，tiny参数r=s=b=0；证明给bounded-config-cardinality的alpha_K界。 |
| delta=1 | 每条支持边p≤T，故全部tiny，big槽为空；普通s_i+b_i界成立。 |
| 空job集合、空配置、无某类支持 | 空调度或该类零负载；每行概率和1保证min r_i有正权配置可取。 |
| 同job跨机器big/tiny换角色 | 一次共同匹配的job顶点只被匹配一次，合法性与完整性保持。 |
| 单端job、零概率配置、重配置 | 单端由Hall覆盖；y=0项不进入support/min；重配置不必合并。 |
| 极小正权、大分母、槽端点与并列尺寸 | 全部精确有理处理；正长碎片给严格前缀计数，数值规模不改变匹配次数。 |
| K二进制编码极大 | 不计算alpha，不枚举K或K次幂；输入显式配置cardinality可直接计数检验。 |
| 声称一般UM sub2 | 本定理依赖给定显式满足cardinality/stability的CONFIG点；没有生成器、可靠失败语义或一般OPT近似结论。 |

未找到fatal objection。最需要作者稿读后复核的地方是：其实际实现是否真的一次联合匹配；其一般K余量是否有与§4同等承重的严格计数与分母论证；是否避免按K数值循环或计算alpha的大分母。上述本轮独立证明本身已闭合A的数学及给定点算法合同。


---

## A：作者稿实读与依赖逐行引理核对

原记录SHA256：`cd335b4dc87ff03a84a441427acb6a7c765044b1e57e02b44f26e1bc132b8e71`。

# 小任务稳定联合槽接口的实际读后核查与三值负载范围攻击

日期：2026-10-19。此记录在陈述先行稿冻结并发hash之后形成。A的陈述先行独立稿不作回写；下面明确属于**实际读稿后、证明知情核查**。

## 1. 实际所读文件、版本与认证范围

| 文件 | 实际读取版本SHA256 | 本次范围 |
| --- | --- | --- |
| `stability_candidate/exact_statements.md` | `88443e0efff15113a07e54b93adf6e91fff8c964647417f32905d660de8523d7` | 前轮只认证A；本轮不补记为新blind review |
| 本审查者陈述先行冻结稿 `literature_mechanism_notes/tiny_work_stability_statement_first_attack.md` | `286aaf6eee34615752f90bbebd491476b5b380d980db35b5b890c2088bd3eea7` | 完整独立构造、前缀/整数分母界、给定点bit复杂度及退化分支 |
| 作者 `stability_candidate/author_proof_v1.md` | `9d817160e58e5428687ce66bf13eb670e8ff4eee7e189c0b6dd40af6b53571ab` | 本次A的实际认证范围仅§1–2（实际行5–27）；后续B的NP完全性不在本认证范围。矩阵定义仅用于后述scope对照 |
| 被作者借用的 `co-work-anl-boss4/research/current/unrelated_machines/bounded_configuration_cardinality_slot_margin.md` | `14c1b00b50a8b87f9aa30e5bbe77300516943a60e68073b123582e074ffe79f4` | 实际读到全文；借用核查针对§2–4的逐行包络证明，不调用§5的n^K承诺生成算法 |
| `hardness_decoder_notes/stability_selection_actual_value_scope.md` | `8155f786c0079ae5d9fce75af00ded57d9052402c0a14d35eaad94d49e86c7eb` | 实际全文读取后，对三值分类、两个任意调度decoder、全部job上界和CONFIG推论作证明知情攻击 |

**A结论：作者§1–2与陈述先行独立证明一致，无fatal objection。** 引用的是局部证明内核而非错误套用要求全局列覆盖的完整旧定理。给定点后的算法对二进制K统一位多项式。

**三值scope结论：所列原主构造范围内分类正确，无fatal objection。** 下文还给两个证明知情加强推论。没有认证B的NP完全性，也没有把scope推论包装为一般UM的算法/困难性结果。

## 2. 作者A逐行承重核查

| 作者实际行 | 断言/借用 | 实际核查与结论 |
| --- | --- | --- |
| 7 | 全局零端预处理、删配置、概率和与job覆盖等式 | 删除任一job不会破坏剩余job覆盖或行概率；每个被删job安排到实际零端即可完成其分配。配置不必合并。剩余有限端严格正，后面的U_i=0分支才可直接判big边际0。通过。 |
| 9–11 | 同job跨机混合角色；r为正支持tiny工作的最小值、s为均值 | 定义均在预处理后的配置上；r_i≤tau_i(C)≤T，故U_i=T−r_i非负。角色属于边而非job，必须在共同匹配中保留单一job顶点。通过。 |
| 13–17 | 完整输出、全部机器同时界、K输入时统一复杂度 | 构造不需搜索CONFIG，α_K只作分析；下面行21的匹配给实际全部job输出，非逐机择优或分数估值。通过。 |
| 21 | 分别排序big/tiny，全部槽一次联合Hall匹配 | 取每条x_ij的正长碎片w。每job的全部big/tiny碎片合计1，每槽≤1。Hall对所有job集合共同成立，任意覆盖匹配在每个槽至多取一件。没有复制跨机混合角色job。通过。 |
| 23首句 | 投影配置big容量统一为T−r_i | 对每个正权C，big工作≤T−tau(C)≤T−r_i，保留其原概率（包括空big投影）。无需给投影big集合补齐全局job覆盖。通过。 |
| 23引用句 | 借UM-BOUNDED-CONFIG-CARDINALITY-SLOT-v1 §2–4的逐行引理 | 已实际逐段核§2的严格前缀、整数类型，§3的Abel严格不等式/有界多面体/Hadamard-Cramer，§4的小K计数。全部只依赖本行配置概率分布和该行边际、共同容量、基数≤K；从未用到big列单独覆盖1。因而局部引理可合法迁移。通过。 |
| 23末句 | U_i=T−r_i=0 | 投影big配置容量0；去零后每big处理时间正，因此每个正权配置均无big job，其big边际和包络0。先分支再缩放，不除0。通过。 |
| 25前半 | Tiny ST收费与对同一匹配包络相加 | 第l槽最大tiny≤前一满槽的单位质量工作；和为≤s_i+b_i。此为对任意匹配的包络，故与big包络在同一全局输出相加。没有分布事件相交或选择不一致。通过。 |
| 25稳定推论 | 负号项与b界 | α(T−r)+s+b=αT+(s−r)−(α−1)r+b≤(α+omega+delta)T。r≥0、α≥1、b≤delta T均已满足。通过。 |
| 25复杂度句 | 槽数、巨大分母、alpha不求值 | 行21的图可以取槽总数≤n+2m；每条x_ij≤1的质量段至多跨两个正长单位槽，碎片≤2mn。有理累加、乘积、比较、整数ceil和无权匹配均按显式输入位长多项式。绝无按K或alpha分母数值循环。通过。 |
| 25实际最大big数句 | 用实际≤n的基数分析 | 令k_eff为显式正权配置的实际最大big数；k_eff=0时直接big负载0，不引入未定义α_0；否则k_eff≤min(K,n)，α_k单调非减，因此已有更强α_k_eff界推出α_K界。无需求任一alpha数值。通过。 |
| 25 T0/empty/single-end | 退化 | T=0时合法CONFIG等式点使每个job有零端，预处理后空；OPT=0即使给T>0也会将所有job送零端。空行有empty配置概率1；无tiny/big支持取0包络；单端由同一Hall匹配覆盖。通过。 |
| 27 | δ自动诱导K的参数相容性 | big定义为严格p>δT。δ=1/2使最多1个big；δ>1/3使最多2个big，且α_2+δ+omega<2正是omega<1/2−δ。边界δ=1/3也足以“最多2”，作者只用严格范围是保守陈述，无错误。通过。 |

旧正文开头提到固定K及§5的n^K搜索，**不应把该搜索移入新A构造**。作者已经明确引用§2–4局部包络，并非调用§5生成器；此处没有固定K与输入K之间的量词偷换。建议正式整合时继续把给定点构造与承诺点生成分开表述。

## 3. 三值scope的实际知情攻击

使用scope原文范围：ell≥2，q>0，每个x至少有tuple，直接使用完整root/selector/ell-leaf主矩阵；孤立源被替换的固定NO矩阵不套此公式。ν为最大3DM大小，H是X到互不相交Y∪Z的投影二部图，μ为H的最大matching大小。

### 3.1 任意实际调度的两个绝对阈值

每selector的唯一有限时间均1，故C≥1。若C<2，每台unit资源最多接一件leaf。

- C<1+1/ell时，每个被selector选中的root不能保留任何leaf。其B、C叶均实际外送；所有资源负载<2使这些B、C资源不重用。于是原selected tuples在X、Y、Z均不交，形成perfect3DM。该decoder不需要先规范其他jobs，亦不查询OPT。
- C<1+2/ell≤2时，每个selected root不能同时保留B、C两叶，因此每个x至少可选一枚实际外送的B/C叶。其目的资源全局不同，给出H中覆盖X的matching。D叶是否外送和其他jobs的位置均不影响该decoder。

第二条在ell=2时仍严格C<2，不会错误允许同unit资源两件leaf。阈值均为绝对数，不偷用源NO的未知OPT。

### 3.2 三份上界确实支付全部原jobs

- ν=q：selected roots全部ell叶外送；其B/C及按x标记的D资源互不冲突，unselected roots所有叶本地，总负载≤1。
- μ=q：对每条H matching边保留一个原tuple见证；其root接selector，外送对应一枚B/C叶及全部ell−2枚D叶，另一枚B/C叶留root。H保证所选unit资源不同，D按x互异，selected root负载1+1/ell。**所有unselected roots的全部leaf仍留home**，负载1。
- 无前提：每x任取一个tuple，selected root仅外送D叶，两个B/C叶都留下，负载1+2/ell；unselected roots全部叶本地，所有D资源至多一件。ell=2没有D时仍是完整C=2调度。

结合两条下界和C≥1，精确得到1、1+1/ell、1+2/ell三值。ν=q自动有μ=q，因此三个子句没有遗漏或交叉矛盾。重复tuple按root索引保留，两个不同x不能选同一root，见证选择也无此冲突。

## 4. 本次证明知情加强一：普通assignment LP(1)已足以推出匹配上界

scope原文以CONFIG(1)投影为fractional perfect3DM，再推出μ=q；其证明正确。此处可给更弱前提的自足论证，**不调用fractional hypermatching oracle**。

假设只有普通assignment LP在负载阈值1可行。记z_a为selector在root S_a上的分数，u_(a,t)为该root第t枚leaf实际分数外送其unit资源的量。每leaf覆盖1，故root容量给

\[
z_a+\frac1\ell\sum_{t=1}^\ell(1-u_{a,t})\le1,
\qquad\text{即}\qquad\sum_tu_{a,t}\ge\ell z_a.
\]

对任意S⊆X，合计其全部roots，selector覆盖使Σ_(a:x(a)∈S)z_a=|S|，所以这些roots至少外送ell|S|质量。它们的D资源只有(ell−2)|S|台、各容量1，故外送到B/C的质量至少2|S|。这些B/C目的地均在N_H(S)，每台容量1，因此

\[
|N_H(S)|\ge2|S|\ge|S|.
\]

Hall得μ=q，然后直接用§3.2的实际构造输出C≤1+1/ell。这个加强只处理该完整矩阵族与阈值1；没有一般UM LP的新gap结论，也没有稳定证书生成器。

## 5. 本次证明知情加强二：全原始矩阵族的(1+1/ell)逼近

三值分类直接给整族无需CONFIG前提的确定性算法：计算H的最大matching。

- 若μ=q，输出matching见证构造，C≤1+1/ell。因OPT≥1，比例≤1+1/ell。
- 若μ<q，输出任意tuple构造，C=1+2/ell；三值分类证明这个数恰为OPT，因此比例1。

于是该完整矩阵族存在确定性总位多项式的(1+1/ell)-approximation，仍保留全部jobs。ν=q判定并没有因此变容易：μ=q分支可能输出1+1/ell而OPT为1。

这与稳定证书选择的NP困难完全相容；稳定性是比实际低负载调度更强的分数证书合同。该族在ell增大时实际逼近更接近1，不能把其证书选择困难转成近二UM困难性。

## 6. 额外精确有限核验

实际编写并运行 `stability_scope_actual_assignment_audit.py`。处理时间乘ell后为整数，程序枚举每个原job的全部合法机器选择；没有删除unselected leaves，没有借用CONFIG点，也没有读取未知OPT当阈值。

| 源 | q | ell | ν | μ | 全部实际分配数 | 实际OPT |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 两个不交tuple | 2 | 2 | 2 | 2 | 16 | 1 |
| 两个不交tuple | 2 | 3 | 2 | 2 | 64 | 1 |
| 四tuple parity | 2 | 2 | 1 | 2 | 1024 | 3/2 |
| 四tuple parity | 2 | 3 | 1 | 2 | 16384 | 4/3 |
| 无孤立坐标H缺陷源 | 4 | 2 | 2 | 3 | 12288 | 2 |
| 无孤立坐标H缺陷源 | 4 | 3 | 2 | 3 | 786432 | 5/3 |

最后一源为`(0,0,0),(1,0,0),(2,0,0),(3,1,1),(3,2,2),(3,3,3)`，三类坐标均非孤立；其前三个X邻域只有B_0,C_0，确有μ<q。总计精确枚举816208份完整实际assignments，全部与分类相符。

有限枚举只核六个矩阵，不替代§3的一般证明。A的一般证明已由前轮独立稿和本轮逐行依赖核查闭合；本记录无外审或全球新颖性认证。


---

## B：只读精确陈述的独立重构

原记录SHA256：`28a2e5ff36a3bbcaf9e60984740673a684ee752da50554999388d74f770d83d9`。

# 单侧小任务工作稳定见证选择的独立重构

## 审查来源与范围

本稿只依据父任务提供的纯陈述 B（并读取 A 对 r、s 的定义）独立推导；未读取作者证明、root 或 rounding_new 的证明草稿。所读纯陈述为 `/workspace/scratch/6bd6916818c5/stability_candidate/exact_statements.md`，SHA-256 为 `88443e0efff15113a07e54b93adf6e91fff8c964647417f32905d660de8523d7`。

结论：在该明确矩阵族上，B(i)–(iii) 均可完整重构，未发现尚成立的实质反例。以下给出比 iff 更强的 CONFIG 可行点参数化，故不需要从作者构造猜测其局部见证。本文是已知 3DM NP 完全源上的新接口重构，不认证全球新颖性、外审或一般 R||Cmax 近二困难性。

## 1. 输入、合法性与完整配置列

固定整数 ell>=2，有理 omega∈[0,1/2)。源的显式三部集合 X,Y,Z 各大小 q，indexed tuples 集 A 大小 m。重复 indexed tuples 若允许，以下证明照常成立。

q>0 时，先检查任一坐标是否不在任何 tuple 中；若有，源无 perfect matching，输出一台机器、两件仅能在该机运行的 unit jobs。该矩阵合法且 CONFIG(1) 不可行：任一配置至多覆盖一件 job，概率总和一不能等式覆盖两件。这个固定 NO 也满足任一合法配置 big 数<=1。

其余 q>0 分支，每 x 的 selector 有至少一个合法 root 端。每叶 job 恰有两个不同有限端（其 root 及其资源），值分别 1/ell、1。因此整个 P 合法，无零时间。q=0 时 A 为空；增加一台 idle 机，无 jobs，其空配置权一给稳定证书，源的 empty perfect matching 与 OPT=0 同时成立。

下文处理 q>0、无孤立坐标的主分支。机器有 m 个 roots 与 ell*q 个资源，总数 m+ell*q。jobs 有 q 个 selectors 与 ell*m 个 leaf jobs；有限条目数为 (2ell+1)m。完整含 infinity 矩阵大小为 (m+ell*q)(q+ell*m)。固定 ell 时这些均是源显式编码的多项式，所有处理时间是固定长度有理数。

对 a=(x,y,z)，令其叶集 J_a 有 ell 件。该 root 仅有 A_x 一个 unit selector 和 J_a 的 ell 个 tiny 端。CONFIG(1) 的**全部**合法列恰为：selector singleton `{A_x}`，以及 J_a 的任意子集（包括空集）。不存在 selector 与任何 tiny job 共存的合法列。每个资源只见 unit jobs，故其全部合法列恰为空集与每件 eligible leaf 的 singleton。因 ell 固定，全部列数 O(m*2^ell+ell*m+ell*q)，可显式列出，不调用配置 LP 分离 oracle。

## 2. 任意 CONFIG 点都产生 fractional perfect matching

给任一等式覆盖 CONFIG(1) 点 y，不预设其 support。定义

- t_a：selector A_x 在 root S_a 被覆盖的边际；
- z_(a,h)：第 h 件叶在 S_a 被覆盖的边际；
- e_(a,h)：同一件叶在其唯一资源端被覆盖的边际。

逐 job 等式覆盖给 e_(a,h)=1−z_(a,h)。由 root 的完整配置列，selector 与每一叶都不共存，故

    t_a+z_(a,h)<=1，亦即 e_(a,h)>=t_a。                 (1)

逐 selector 等式覆盖给

    sum_(a:a.x=x) t_a=1；因此 sum_a t_a=q。             (2)

每 B_y 只含 unit jobs，资源配置概率总和一给

    sum_(a:a.y=y) e_(a,B)<=1。

对全部 q 个 B_y 求和，并用(1)–(2)：

    q=sum_a t_a <=sum_a e_(a,B)<=q。

所有非负差 e_(a,B)−t_a 的和为零，所以每一项都为零；而每个资源的总覆盖也都饱和。故 e_(a,B)=t_a，sum_(a:a.y=y)t_a=1。对 C_z 同理，得到 e_(a,C)=t_a 及 sum_(a:a.z=z)t_a=1。

ell>2 时，固定 x 与一条 D_(x,h) 资源，其 eligible leaf 正是所有 a.x=x 的第 h 附加叶。由(1)及(2)，

    1=sum_(a:a.x=x)t_a <=sum_(a:a.x=x)e_(a,h)<=1。

因此该类每一叶也有 e_(a,h)=t_a，且 D 的行容量恰饱和。于是**全部 ell 件原叶**同时满足

    z_(a,h)=1−t_a，e_(a,h)=t_a。                     (3)

这些式子表明 t>=0 且 X、Y、Z 各坐标 incident t 总和一，恰是三维匹配的 fractional perfect matching；没有把不同局部点拼接起来。

## 3. 全部 root support 被迫只有两列

固定 a。root 事件 U 表示含 selector，Pr(U)=t_a。每一叶的出现事件 V_h 与 U 不交，且由(3)有 Pr(V_h)=1−t_a=Pr(not U)。所以

    Pr(not U 且 not V_h)=0。

对有限的 ell 件叶逐项使用非负概率，任何正权且不含 selector 的配置必须包含全部叶；任何含 selector 的合法配置则只能是 selector singleton。故 y 的该行概率 law 精确为

    t_a·{A_x} + (1−t_a)·J_a。                         (4)

每个资源的概率 law 也被其 singleton 覆盖边际唯一决定：对应 a 的 singleton 权为 t_a，空列权零（资源已饱和）。因此 CONFIG 可行域与 fractional perfect matching t 的多面体是上述显式仿射对应；反向给任一 fractional perfect matching，按(4)及资源 singleton laws 即得到 CONFIG 点。

尤其，不能只在作者选好的两列分布中检查稳定性；(1)–(4) 已覆盖所有原合法配置与每一个 CONFIG 可行点。

## 4. 稳定性等价与 perfect matching 解码

root 的全部 tiny 工作为一，selector singleton 的 tiny 工作为零。由(4)：

| t_a | r_a | s_a | s_a−r_a |
| --- | --- | --- | --- |
| 0 | 1 | 1 | 0 |
| 0<t_a<1 | 0 | 1−t_a | 1−t_a |
| 1 | 0 | 0 | 0 |

所有资源行的 r=s=0。由此全部机器满足稳定性，恰当且仅当

    对全部 a，t_a=0 或 t_a>=1−omega。                (5)

omega<1/2 使任何正 t_a 都严格大于 1/2。每个 x 的 incident t 和为一，因而恰有一个正项，而且该项等于一。Y、Z 的等式和随后使这些选中 tuples 各覆盖每个 y、z 恰一次，构成真实 perfect 3DM。

这个 decoder 只读任意输入证书的 selector marginals，并按正性选择 a；其正项其实全为一，不依赖数值近似，也不输入源最优值。s/r 在 t=0 的跳变已单列，不能误把该行的 r 仍写成零。

反向给 perfect matching M：每个 x 的 selector 放其 M 中的 tuple root；该 root 的所有叶外送原资源；其余 tuple 的全部叶留 root。资源 B、C 各接一件 unit，D_(x,h) 也只接 M 中唯一 tuple 的一件 unit；被 selector 占用的 roots 不留叶，其他 roots 的 ell 件小叶总负载一。全部原 jobs 恰执行一次，故 C<=1；其 Dirac CONFIG 证书逐行 s=r，因此适用于 omega=0 以及所有更大允许 omega。

反向任何实际 C<=1 分配的 Dirac 点也稳定（每行仅一正权配置，所以 r=s）。上述 decoder 因而也证明实际 OPT<=1 iff perfect 3DM。完整 source、CONFIG、actual 三个 iff 均成立。

## 5. NP 完全、证书位长和 YES 承诺搜索

NP-hardness 是普通显式 3DM 的多项式 many-one reduction，包含第1节的可靠孤立坐标 NO 分支与空源 YES 分支，固定任意 ell、omega 均成立。

NP membership 可直接使用上节的 integral schedule：若稳定证书存在，已证明源 perfect，故存在含每 job 一个机器索引的 C<=1 schedule；验证资格及精确负载为多项式。等价地，提供该 schedule 的逐机 Dirac CONFIG 列及权一即可，全部列与概率均有多项式位长，r/s 可直接算出。若要直接验证一般显式 y，则扫描正权列、核列合法性/概率和/逐 job 等式覆盖，并按正权 support 求 min 及均值，也都是总位多项式。没有假定任意实可行点本来具有一个免费短的概率展开。

固定 ell 另有完整配置列的多项式枚举，可对稳定 witness 形式直接给 NP 论证；但无需遍历 2^ell 来构造上述 Dirac YES 证书。不能据此声称“输入 binary ell 时按2^ell枚举”是位多项式。

假设存在 B(ii) 所说的**总**确定性 bit-poly 程序 F，在每个 actual OPT<=1 输入上输出可验证的稳定 CONFIG(1) 点。对任意 3DM 源先做本归约，运行 F，再验证其实际输出。YES 因 OPT<=1 必得到有效点；NO 根本不存在有效点，所以 F 的任意输出或拒绝都不能通过验证。总多项式运行保证该组合是普通 3DM 决定程序，从而 P=NP。因此 P!=NP 下不存在该承诺搜索程序。若只有 YES 分支终止而 NO 可无限运行，此论证不能直接使用；纯陈述已明确要求 total，故没有这一缺口。

这仅证明给定严格单侧稳定合同的见证搜索障碍，不是普通 UM 的一般近似困难性，也没有排除放宽 omega 或替代分数证书的算法。

## 6. omega=1/2 的全部 ell 反例

X=Y=Z={0,1}，四个 tuples 为

    (0,0,0), (0,1,1), (1,0,1), (1,1,0)。

不存在两条覆盖全部坐标的 matching：两条若 x 与 y 坐标分别不同，则其 xor z 坐标相同。每个坐标 incident 两条 tuples，令四个 t_a 都为1/2，是 fractional perfect matching。

对全部 ell>=2，按(4)令每个 root selector singleton 权1/2、全部 ell 叶配置权1/2；每个 B_y、C_z 及每个新增 D_(x,h) 都有两件 eligible unit 叶，各 singleton 权1/2。所有 jobs 精确覆盖一、每行概率一、配置容量一。roots 的 r=0、s=1/2，其余机器 r=s=0，故稳定于 omega=1/2。该完整证书没有 perfect 3DM，对端点排除正确。

还可核出端点稳定条件(5)为 t_a=0 或 t_a>=1/2，因坐标等式和一，各坐标只容一项1或两项1/2。本文不推导这个 half-integral existence 问题的复杂度；纯陈述也没有作此声称。

## 7. 核查状态

这是 statement-first 的一般数学重构，没有优化枚举或有限实验代替证明。完整 CONFIG 支撑刚性、所有原任务与 D 资源的共享方式、孤立源合法性、空任务、任意固定 ell 与半端点均已逐项处理。下一步应冻结此稿后，才阅读作者证明并核对是否有未付清的额外声称。


---

## B：作者稿§3–6实际读后攻击

原记录SHA256：`9fdd7fc736c855ff0b997c3c1cd56e0c2b820fa12db12c666f7d5cedb1c756dd`。

# 单侧稳定选择命题的作者全文实际读后攻击

## 版本、顺序和实际范围

先独立读取纯陈述 `stability_candidate/exact_statements.md`，SHA-256 `88443e0efff15113a07e54b93adf6e91fff8c964647417f32905d660de8523d7`；独立证明在 `stability_selection_independent.md` 冻结，SHA-256 `28a2e5ff36a3bbcaf9e60984740673a684ee752da50554999388d74f770d83d9`。冻结后获准实际读取作者 `/workspace/scratch/6bd6916818c5/stability_candidate/author_proof_v1.md`，核对 SHA-256 为 `9d817160e58e5428687ce66bf13eb670e8ff4eee7e189c0b6dd40af6b53571ab`。

实际审读范围为作者稿 **§3–6**，即 B 的矩阵、CONFIG 投影、稳定选择 NP 完全、YES 承诺搜索、半端点及相关研究范围；没有审读 §1–2 的 A 舍入证明。读取仅在独立稿冻结之后发生。本文不把 B 的核查状态外推给 A 或未来正文版本。

## 逐项攻击结果

1. **新原矩阵的合法性。** 每 leaf 原任务有 root-small 与唯一 resource-unit 两个合法端；selector 的资格只依其 x。源孤立坐标可靠转固定合法 NO，空源另给 idle 空机。作者在非空分支也保留一台 idle，故机器数写成 |A|+ell*q+1；这是不改变配置与实际值的空行，不影响纯陈述允许的空任务处理。所有 D_(x,t) 按 x 共享，而非每个 tuple 私有，这一承重差别已实际核对。

2. **作者的全局容量等式。** 作者不用预设 root support，而先由 selectors 总期望 q、root 数 |A| 得 sum s_a<=|A|−q；再由全部 ell*|A| 叶的等式覆盖与 ell*q 台 unit 资源容量反向得 >=。两个界确实同时覆盖所有原叶、每个 D 资源、未选 roots 的输出和 idle 空行。总和取等迫每个 root 的期望负载恰一，非负且逐配置容量一，故每个正权配置的负载都一。根上只有 selector singleton 或全部 ell 叶能取得负载一。因此作者的完整 CONFIG 投影没有局部见证偷换。

3. **投影的两向与支持零点。** selector 概率 z_a 与每叶的 resource 边际相同；X/Y/Z 的 incident z 总和一，D 约束不增减该多面体。反向两列 root 分布和 unit-resource singleton 分布完整执行了每 job 覆盖。z_a=0 时 r=s=1，不能误套正 z 的 r=0；作者已分段处理。omega<1/2 给正 z>1/2，X 和式迫其唯一且为一，故完整 matching 解码正确。omega=0 也包含。

4. **NP membership。** 在纯陈述 B 的固定 ell 源族，roots 的完整合法列是 ell 叶的所有子集和 selector singleton，资源列仅为空或 singleton，故可显式多项式展开。作者猜 r∈{0,1/ell,...,1}、删 tau<r 的列、加 mean<=r+omega 的 LP 论证有效；无需强制某列真正取到所猜 r，因为真实 min 只会更大，仍有 mean−真实min<=omega。有界有理 LP 的基本解给多项式位长证书。我的独立稿另外通过 iff 对应的 Dirac actual schedule 给更短 NP 证书，二者相容。本次认证的是 Exact B 的受限选择问题；作者开头若泛写“合法 UM 输入的 NP 完全”宜在最终正文明确落回该域，不把本次固定列枚举审查扩展成任意 UM 全类的证明。

5. **YES 承诺搜索决定化。** total deterministic bit-poly 是必要的前提，作者明确保留。YES 时 actual OPT<=1，保证输出有效稳定点；NO 没有这样的点，任意输出都不能通过验证。域外输出任意只指总多项式界内的输出或拒绝，不许无限不终止。没有用未知 OPT 来判断输出是否达标。

6. **实际单位阈值。** 任意 C<=1 时 selector 占用的 root 不能留下任何一枚正 tiny 叶；所有选中叶都外送且资源 unit 不可重复，确实解码 perfect3DM。反向完整安排包含所有未选 tuple 的全部叶，实际 load<=1。q>0 时 selectors 又给 OPT>=1，合法性与 exact threshold 都闭合。

7. **半端点与作者实际证书。** parity 四 tuple 每对相交；四个 z=1/2 使每 X/Y/Z 坐标和一，新增每条 D 也恰接两件 eligible leaf，各 singleton 概率1/2。所有 ell>=2 的 root r=0、s=1/2，故 endpoint 证书正确。作者的 actual 上界留回共享 B_0 的一枚叶，其余原任务逐件合法，C=1+1/ell；整数1/ell网格及 no-unit-schedule 给下界。不能从这一个 NO 实例推断 omega=1/2 的选择问题可解，作者没有此扩张。

8. **研究范围。** NP 完全的是指定稳定见证选择；不是要求所有配置可行点稳定，也不是实际近二 gap。作者 §6 对半端点实际值趋一的限制正确。另有独立新 lemma 给整个新矩阵的实际三值分类，已在独立 scope 稿和纯 Exact 中单独冻结；它可加强此范围说明，但不改变 B 的证明。

## 独立 Fraction 有限审计

代码为 `/workspace/scratch/6bd6916818c5/hardness_decoder_notes/stability_parity_fraction_audit.py`，SHA-256 `f6516b385de4d32ba7313d47535846af5988fc12a0e949abddee213de182768d`；冻结输出为同目录 `stability_parity_fraction_audit.json`，SHA-256 `46ca58d85a916c9f1dfaec6dda666390c01e9f2f3513813a1c734fad0e3e75b9`。没有导入本题 canonical 或作者的构造/审计代码；仅从 parity source 生成原矩阵，非空分支也保留一台 idle。

| ell | 原机数（含idle） | 原jobs | finite端 | 全部实际 assignments | 完整合法 CONFIG 列 | 实际 OPT |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 9 | 10 | 20 | 1024 | 33 | 3/2 |
| 3 | 11 | 14 | 28 | 16384 | 55 | 4/3 |

全部实际 assignment 用 Fraction 逐机累加；ell2 有84份最优调度、其余940份峰值2。ell3 有132份峰4/3、1248份峰5/3、15004份峰2。半端点给定 CONFIG 证书完整核各概率、每 job 等式覆盖、全部列合法性、big数<=1、每行 r/s，最大振幅都恰1/2。该同一点不满足 omega=1/3；没有据有限检查断言所有 omega<1/2 点不存在，一般 NO 来自上面的证明。

另在所有 C<1+2/ell 的已枚举实际调度上执行独立的 X—(Y union Z) matching decoder，分别核84和132份。程序从二部 matching 独立生成一份完整 C=1+1/ell 上界，不沿用作者选定的两个 roots。源 nu=1、mu=2 由小源直接枚举/搜索核查。

这些运行没有优化全部 CONFIG 可行点、验证任意 3DM 源或检验一般 NP 完全性。完整数学命题来自独立证明及作者 §3–6 的实读攻击，有限运行仅检原矩阵、半端点证书及小例所有实际调度。

## 当前结论

对纯陈述 B 的精确输入族、全部固定 ell>=2、固定有理0<=omega<1/2、total YES-search 及半端点例，**未发现尚成立的数学 fatal objection**。独立重构、实际作者读后及有限软件范围已分开；未审 A、未外审、未认证全球新颖性。最终 canonical 若改变矩阵、tiny语义、证书输出形式或 promise 量词，需要再核对应变化，不能自动继承本记录。


---

## B及三值：最终canonical全文实读及独立审计重跑

原记录SHA256：`ed1b3e7ef4f8a8c3d9b1554c69bb674037de2e6d49f9f47fe9798ebd890a5503`。

# 单侧稳定与真实三值恒等式的最终 canonical 实读

## 最终版本与认证范围

实际全文读取 `/workspace/scratch/6bd6916818c5/co-work-anl-boss4/research/current/unrelated_machines/tiny_work_stability_joint_rounding_and_selection_barrier.md`，核对 SHA-256 为 `6f6d28e2c20290873ea77b6771f213534c92f4f3fec0fbce9f70192261384d83`。

本次数学认证限于 **B 对应§3–5、真实三值§6及§7相关范围说明**。全文读取包括§1–2，但没有为 A 的联合槽舍入重新独立重构或攻击，故 A 不继承本次 B 的核查状态。

先前 B 的 statement-first 独立稿 hash 为 `28a2e5ff36a3bbcaf9e60984740673a684ee752da50554999388d74f770d83d9`，作者§3–6读后稿 hash 为 `9fdd7fc736c855ff0b997c3c1cd56e0c2b820fa12db12c666f7d5cedb1c756dd`；本次均不改其原字节。三值 lemma 是我在 B 独立稿后额外推导；root 已事先收到证明梗概，最终 canonical 如实将其后续重构记为知情，未冒记其为只读三值 Exact 的盲审。

## B 最终正文核查

- §3 已明确限定 selector/root/ell-leaf 实际矩阵族，关闭作者稿首句可能泛指任意 UM 输入的范围歧义。固定 ell>=2、固定有理0<=omega<1/2 的量词不变。
- 所有源处理与原资格都保留：空源、孤立坐标的固定合法 NO、重复 tuple 索引、每 x 共享的 ell−2 台 D 资源及 idle 空行。完整规模与固定参数的位多项式范围一致。
- §4 的全局容量两侧取等覆盖每一枚 leaf；强迫每个正权 root 配置负载一，故只含 selector 或全部 ell 叶。不是预设两列后检查；fractional perfect3DM 的两向 CONFIG 对应完备。
- min-support 在z=0、z=1和0<z<1三个分支均正确；omega<1/2迫每个 x 只有一项正 z=1，Y/Z 等式给真实 perfect3DM。固定 omega=0 不漏。
- 固定 ell 下全部合法 CONFIG 列可多项式列出。猜 r、只保 tau>=r、加 mean<=r+omega 的 LP 不必另迫“真实 min=猜值”，真实 min 更大仍满足稳定性。短有理证书及 total YES-search 决定化正确。
- §5 的 parity NO、所有 ell 的半端点证书和全部原任务的精确 actual OPT=1+1/ell 证明均保持。没有将 omega=1/2 的反例泛写成该端点问题可解。

## §6 真实三值核查

主分支 q>0、每 x 有 tuple，固定 NO 和空源单列，范围与独立纯 Exact 一致。nu=q、nu<q且mu=q、mu<q 三行互斥并覆盖；nu=q必有mu=q。

两个下界使用严格绝对阈值 C<1+1/ell 及 C<1+2/ell<=2。前者迫 selected root 全叶外送，后者迫至少一件 B/C 叶外送。所有资源 unit 容量在这些严格阈值下都确为至多一件，故两个真实 decoder 对任意完整实际调度有效；没有规范未选状态任务。

两个上界同样付清完整原 jobs：mu=q 时全局匹配选 tuple，送全部 D 和一枚所匹配 B/C；一般分支任选 tuple，只送全部 D。ell=2 的空 D 分支正确。mu<q 时第二个构造精确达界；mu=q 时第一个构造至多1+1/ell，而原 OPT>=1，因此按mu选择就有整个已呈现类的(1+1/ell)实际近似，不需要求nu。

CONFIG1 可行的 fractional3DM 在 H 两类边各送z_a/2，左行和一、右列和1/2，确给覆盖X的二部分数匹配，从整数匹配得到mu=q。因此该前提下无需稳定见证便能输出<=1+1/ell，范围说明成立。canonical 明确源呈现为算法输入，不偷含未标记 raw 矩阵识别。

## 完整 canonical audit 实读与重跑

实际全文读取 `tests/audits/unrelated_machines/tiny_work_stability_selection_audit.py`，核对 SHA-256 `295bed9f20a22e6e3638d4687884a5fd384cec3c42ebd5e682ce682dc2757494`。与原独立代码完整 diff 只增加 hashlib/platform/Path imports 和输出元数据；构造、Fraction负载、全部 CONFIG 列、证书及完整 assignment 枚举逻辑没有改动。

从仓库目录实际执行：

    python3 tests/audits/unrelated_machines/tiny_work_stability_selection_audit.py

输出到独立 scratch 文件 `stability_canonical_replay.json`，不覆盖仓库 frozen evidence。与 `evidence/runs/unrelated_machines/tiny_work_stability_selection_audit.json` 比较，JSON对象和文件字节都完全相同；两者 SHA-256 都为 `dff07141158d51756b20ca5ddf7cd60d514a12d3701fd680231434413912efbf`。cases数组也与原独立输出一致。

范围仍严格限 parity 四 tuple 的 ell2/3：完整调度1024/16384份、完整合法 CONFIG 列33/55、actual OPT3/2与4/3，给定半端点点的最大稳定振幅1/2，第二阈值 decoder 分别核84/132份。没有优化全部 CONFIG 可行点、实现稳定见证 finder 或把有限 audit 当普遍 NP 完全性证明。

## 最终结论

对该 hash 版本的 **B§3–5与三值§6，未发现尚成立的数学 fatal objection**。最终范围、证据归属和位复杂度与原独立重构一致。本文不认证 A、不认证未读的其他 canonical 或 audit、不认证外审及全球新颖性；一般UM-TARGET-v1和近二困难性仍开放。


---

## A及三值：最终canonical全文实读与实现输入域修复

原记录SHA256：`7c6af64cf1dfde1fec56a93ab114ad6bc2beaa12835da1b4147fe499c109a31d`。

# 小任务稳定接口canonical最终实读、构造器重跑与精确编码修复记录

日期：2026-10-19。此为最终实际阅读及运行记录，不修改任何前轮冻结稿，也不把证明知情阶段倒记为blind review。

**最终结论：A§1–2与§6的三值恒等式/已呈现源上的实际算法通过本次核查；给定点构造器在修复精确数字解析上限后通过重跑。未发现未闭合fatal objection。B的稳定证书选择NP完全性不在本审查者认证范围。**

## 1. 本次实际读取的最终版本

| 文件 | SHA256 | 实际读取/认证范围 |
| --- | --- | --- |
| canonical `research/current/unrelated_machines/tiny_work_stability_joint_rounding_and_selection_barrier.md` | `6f6d28e2c20290873ea77b6771f213534c92f4f3fec0fbce9f70192261384d83` | 实际全文读到；认证A§1–2，以及§6。B可见不等于自动认证B |
| 最终构造器 `tests/audits/unrelated_machines/tiny_work_stability_joint_rounding.py` | `f1ebc2dc1946d0b207ae36c7be56b95df639d468a07032077726ba7602f68d61` | 实际完整读到，包括decode与main的数字cap修复、虚拟行转换、一次共同槽匹配、capped幂比较和全部audit分支 |
| 所调baseline `tests/audits/unrelated_machines/rounding_and_gap.py` | `5ba0dc52ddbb90ffece75e5accd2e801957c1172e337b9bdf033e22a64cbd75a` | 实际读取本次调用的rational、matrix、loads、round_slots实现与迭代BFS增广；未追加认证其无关gap生成器 |
| 最终冻结 `evidence/runs/unrelated_machines/tiny_work_stability_joint_rounding_exact_encoding_audit.json` | `17714bfbe3814a8359dff92e6ca85d2f24efdeba1c3a912703ca12c6f8b00c6f` | 实际读取；与本审查者最终code独立fresh replay逐字节完全相同 |
| 最终冻结 `evidence/runs/unrelated_machines/tiny_work_stability_exact_encoding_cli.json` | `c33e0a40952498cf08f650f736c98f73ad1c6a1969b74452d91420f9052881b1` | 实际全文读取；按其输入recipe独立重建，输入hash也相同，默认子进程环境得到精确相同负载 |

前轮陈述先行独立稿SHA `286aaf6eee34615752f90bbebd491476b5b380d980db35b5b890c2088bd3eea7`，作者稿实际读后记录SHA `cd335b4dc87ff03a84a441427acb6a7c765044b1e57e02b44f26e1bc132b8e71`，均保持原字节。本次不把新增canonical §6视作新的陈述先行审查。

## 2. 数学A最终核查

canonical A§1–2保留了前轮已独立重构的全部承重步骤：

1. 全局零端预处理并从全部配置删去相应job；T=0时因此得到零调度。
2. 同一原job仍是唯一列；每机器big/tiny两个虚拟行只是角色边的分离。全部虚拟槽放在一张图中，一次Hall匹配覆盖全部剩余jobs。不会为混合角色做两个不同决定。
3. 每个正权源配置的big投影容量≤T−tau(C)≤T−r_i。引用的是已实际读到的bounded-cardinality正文§2–4逐行包络证明，而非要求big列单独覆盖1的完整旧定理，也非其n^K配置生成器。
4. T−r_i=0分支的big边际为0，不作缩放除0；无tiny支持的b_i、s_i均为0。
5. Big与tiny包络都是对任意同一槽匹配的逐行上界，直接相加得α_K(T−r_i)+s_i+b_i。稳定性推论的负号项−(α_K−1)r_i方向正确。
6. 算法只从实际x生成槽并匹配。总槽数≤n+2m，正长碎片数≤2mn；有理位长均为显式输入位长多项式。K即使二进制表示很大也不进入次数循环，alpha_K不需要实际构造。实际big基数为0时直接零包络，不使用未定义alpha_0。

因此数学A仍通过。此前观察到的Python解析上限是实现输入域问题，**不是数学A的反例或定理错误**。

## 3. 第三ClaimID、源呈现与§6算法

canonical第三身份准确写为 **UM-SELECTOR-TINY-ROOT-THREE-VALUES-v1**。它与A给定点舍入及B稳定证书选择分开，输入明确包含源构造呈现，q>0且每个x至少有tuple；固定NO映射与空源按其原分支处理。没有声称从未标记raw矩阵识别模板。

其两条任意调度decoder仍正确：

- C<1+1/ell时，selected root的全部leaf必须外送，unit资源在C<2下不重用，得到perfect3DM。
- C<1+2/ell≤2时，selected root至少外送B/C之一，给H=X—(Y∪Z)中覆盖X的matching。

三份完整实际上界保留全部unselected roots的全部leaf；D资源按x标记，H的全局匹配保证所选B/C目的地互斥。ell=2时D为空的两个上界仍成立。故真实OPT的1、1+1/ell、1+2/ell三值分类成立。

已呈现源上的(1+1/ell)实际算法不求ν：若μ=q，输出matching见证的1+1/ell构造；若μ<q，1+2/ell构造恰达到第三分支OPT。普通二部匹配与全jobs回填的总位多项式界成立。

canonical的CONFIG1可行⇒μ=q只使用其已写明的fractional3DM z沿x→y、x→z各送z_a/2的分数matching，再应用二部matching整数性。**本次认证不依赖本审查者前轮提出、但未纳入canonical的普通assignment-LP加强。** 未在canonical依赖链中暗加该加强。

本构造器文件实现的是A的给定点输出接口；它的audit不因此自动变成§6全域算法或B选择复杂度证明。§6数学算法的正确性由上述任意调度decoder及完整构造承担。

## 4. 构造器实际逻辑审阅

构造器先验证原点合法性，再删除零端jobs；因此非法job覆盖不会被预处理遮盖。重复job索引、禁用端、负概率、行概率非1、配置超载均在匹配前拒绝。Big基数只约束去零后正权配置；零概率合法大列不会错误触发K限制。

为每个原机器建立两个虚拟行，但每个剩余job仅保留一个原列。实际只调用一次baseline.round_slots。返回的虚拟行号除以2映回原机器，再用原矩阵计算全部实际负载，零端job负载0。

对k≥4，校验A≤(2−k^{−(k−1)})U等价于slack=2U−A>0且k^{k−1}≥ceil(U/slack)。代码以有理整数交叉乘法算比较阈值，并用二进制平方及饱和截断判断幂，不构造alpha分母；中间乘积位长受阈值位长及输入log k控制，次数O(log k)。零容量及k=1/2/3另行处理正确。

Baseline槽循环按正长碎片推进，每个x_ij≤1；它不是按分母或质量的数值大小推进。匹配采用显式BFS增广，不依赖Python递归深度。代码与给定点数学构造一致。

## 5. 独立fresh replay与逐字节比较

本审查者实际运行最终SHA为f1eb…的程序：

`python3 tests/audits/unrelated_machines/tiny_work_stability_joint_rounding.py --audit`

stdout保存为
`literature_mechanism_notes/canonical_tiny_work_constructor_arbitrary_precision_replay.json`，SHA
`17714bfbe3814a8359dff92e6ca85d2f24efdeba1c3a912703ca12c6f8b00c6f`。

与最终canonical exact_encoding audit **JSON对象相等且完整字节相等**，差异字段为空。实际结果：7个主成功fixture、2个额外成功fixture、15个匹配前拒绝、9次总槽调用、5个capped界算术检查。覆盖混合角色、tiny数量超过K、T−r=0、原零job删减、空job/T0、8193-bit K、大分母、K3正r及零权列。

该有限运行验证实现和所列参数，不替代一般数学证明。

## 6. 实质实现异议的观察、修复与关闭

原代码SHA `508592f655923b8601abf3c606af7c2c643529b95c889798b517aa093f47f676`在默认Python3.12数字解析cap下，确会拒绝两份合法输入：K=10^5000的一unit job点，以及p00=1/10^5000、K1的一job点。前者json整数解析失败，后者Fraction字符串解析失败。旧stdout audit与这两份观察JSON均保留在scratch，没有覆盖。

最终code在**main、decode入口都**调用set_int_max_str_digits(0)（功能存在时）。main在json.load之前解除限制；decode在处理任意长rational strings之前解除限制；后续Fraction输出也不再受cap阻挡。该修改闭合了本次观察到的输入域缺口。

本审查者在未设置PYTHONINTMAXSTRDIGITS覆盖的默认子进程中重跑：

- 原K=10^5000样例成功，K_bits=16610，负载1；
- 原p00=1/10^5000样例成功，输出精确负载字符串长度5003且等于原值；
- 新默认导入API进程从cap4300开始，调用decode后cap0；同时输入K=10^5000与p00=1/10^5000，返回完整assignment[0]和精确原负载。

记录在 `canonical_arbitrary_precision_independent_rechecks.json`。

并实际按canonical CLI evidence的同一recipe重建组合输入：p00=1/(10^5000+1)、K=10^5000、T1、delta0、singleton权1。独立生成的输入SHA恰为
`4d1a9e90b6dc935721522039bd3ccd45c5ae5cffa78f6e10e5b835fa8a7f896c`，与root证据相同。

默认子进程成功，assignment[0]，精确输出负载等于输入p00，K_bits=16610，分母十进制长度5001，alpha检查为capped comparison且0次幂推进。独立完整stdout SHA为
`f567a454a135dee23c64f88f0de89afa0950206e8c4b6c8125db5b07aafcd2dd`；记录在 `canonical_final_combined_exact_encoding_record.json`，输入和完整stdout另各保存。

**此实现异议已关闭。** 本记录不追加任何数学真值、外审或全球新颖性升级；一般UM-TARGET-v1仍未关闭。
