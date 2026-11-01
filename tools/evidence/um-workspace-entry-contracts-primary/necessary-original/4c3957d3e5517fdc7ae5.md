# 七态原作业星：共同二次负载检验的局部核

ClaimVersion: UM-SEVEN-STATE-STAR-GLOBAL-QUADRATIC-LOCAL-v2

2026-10-18，boss11。对象是实际 OPT=1 的完整普通原矩。下述结论不声称递归接线或实际 near-two gap；证明使用对称化、有限点评估与 Cauchy 不等式。

## 0. 四个精确身份、假设及范围

主Claim **UM-SEVEN-STATE-STAR-GLOBAL-QUADRATIC-LOCAL-v2**：对§1全部偶d,s，显式完整原矩actual OPT=1，却有同一个有理degree-six原端点functional/M3、全部原Boolean与job onehot、每机所有global degree-two physical-load localizers及全行合法CONFIG first/pair；坏样本质量p=η³/1000与d无关。并可det-total-bit-poly生成全部矩和每行显式poly-support有理CONFIG证书。前身Exact和未发布LOCAL-v1只保原件；新增显式CONFIG支持依§7另付，没有回写旧审票。

辅助Claim **UM-UNIFORM-CARDINALITY-PAIR-SPARSE-SUPPORT-v1**：对每个显式d≥1、0≤h≤d，可确定性poly(d)生成至多D=1+d+binom(d,2)个实际h-subsets及有理权，精确保uniform-slice first/pair；不保更高矩，不能据此改共同L。§7自足给算法。

边界Claim **UM-SEVEN-STATE-STAR-AFFINE-BOOLEAN-BOUNDARY-v1**：固定§1正支持上的实仿射Boolean函数只有0/1/单bit及其补；在保base≤4矩、共同M3、原Boolean/onehot和各新端点X的Gram等式Lhat[(X−f)²]=0时也成立。同unit行pair零遂最多两个正covered owners，且只能同bit互补。逐背景量词和反例见§8，非无条件物理入度界。

边界Claim **UM-SEVEN-STATE-STAR-AND-GATE-LOCALIZER-OBSTRUCTION-v1**：保base≤5矩、共同M3、原Boolean/onehot，新增degree-one原端点Z忠实Gram等于CY_i且原v负载不变，则某global degree-two检验严格负。仅否定该给定点的忠实AND延拓，不否定所有非线性接线，见§9。

**Objects / Definitions / Domain / Quantifiers：** 主Claim和两边界对每个§1原矩及全部指定矩扩展逐个量化，q系数可为任意实数；辅助Claim对所有显式有限标签和cardinality量化。原矩域定义 UM-SEVEN-STATE-STAR-ORIGINAL-ENDPOINT-LAW-DOMAIN-v1；辅助特征域定义 UM-CARDINALITY-FIRST-PAIR-FEATURE-DOMAIN-v1。无额外UM侧约束、免费oracle或复杂度假设。

**Dependencies / Evidence / Status：** 自足有限代数、对称化/Cauchy、Gram-null、原Boolean identities及显式有理消列。核心、稀疏支持、仿射和AND各有单独先行Exact重构，root实际全文读后才释放对应Proof，再分别实际读后；最终规范稿实读以[实际审查](../../reviews/unrelated_machines/seven_state_star_global_quadratic_and_extension_boundary_review.md)为准。精确范围内证明完成、内部后置攻击，无外审或全球新颖性认证；标准工具不认领原创。

**Conclusion / Counterevidence / Objections / Scope：** 可复用内容是dim-free局部q2噪声控制及两种点延拓边界；原输入OPT=1，不是relaxation integrality gap、近二hardness、一般调度算法或递归证书。父/孩子/共享head新增负载仍必须逐行支付。有限129行audit只核12参数与3个small全矩，未构造growing-depth共同law；不把有限结果作为全称证明。Related Files与保真来源、软件实际范围见上述审查及§10。UM-TARGET-v1正反面均OPEN。

## 1. 精确原矩与结论

令 d,s 为正偶数，2<=s<=d/2；置 eta=s/d、h=s/2、T=1+eta。机器为 u,v,z_1,...,z_d。全部原 jobs 是 R,j_1,...,j_d，其有限时间恰为

    p_(u,R)=p_(v,R)=1,
    p_(v,j_l)=1/d, p_(z_l,j_l)=1，1<=l<=d.

其余时间无穷。共 d+2 台机器、d+1 枚独立不可拆原 job、2(d+1) 个有限条目；所有调度完整分配所有原 jobs。

记 C=1 当 R 在 v，Y_l=1 当 j_l 在 v，H=sum_l Y_l。全部原端点指示为 C,1-C,Y_l,1-Y_l。定义

    p=eta^3/1000,
    u0=4p(1-eta),
    e=4/5-p-u0.

下面的真实完整 assignment law P，在每个 H 类别中均匀选大小 H 的 home 集：

| C | H | 质量 |
|---|---|---|
| 1 | d | p |
| 1 | 0 | 1/20 |
| 1 | h | 1/20 |
| 0 | 0 | 1/20 |
| 0 | h | 1/20 |
| 0 | d/2 | u0 |
| 0 | d | e |

对全部原端点变量 X，令 L[f]=E_P[f(X)]。则：

1. L 的共同次数六矩给 M3(L) 正半定，并满足所有原 Boolean、原 job one-hot 等式；所有矩来自同一个真实完整 assignment law。
2. 每台机器 i 与任意全局实多项式 q(X)，只要 deg q<=2，均有 L[(T-load_i)q^2]>=0。q 可使用任意机器和原 job 的端点变量。
3. 每台机器均有支持在完整 CONFIG(T) 上的配置分布，与 L 的该行全部原端点 first/pair 矩精确一致，包括对角项。
4. 输入的实际 OPT=1。P 以正概率 p 产生峰值二样本；它不声称其自身逐点满足 makespan T。

## 2. 原 assignment、边界与共同 PSD

全部质量为正、总和为一；eta<=1/2 给 p<=1/8000，e>0.79。每次抽样把 R、每枚 j_l 各放在恰一个有限原端点，实际负载是

    load_u=1-C,
    load_v=C+H/d,
    load_(z_l)=1-Y_l.

所以非 v 行在每个样本负载均至多一。把 R 放 u、全部 j_l 留 v 给完整峰值一调度；R 在任何有限端点处理时间都是一，故实际 OPT=1。P 中只有类别 (C,H)=(1,d) 的 v 负载超过 T，该类别负载恰为二。

任意次数至多三的多项式 a 都满足 L[a^2]>=0，故共同 M3 PSD。Boolean 和每个原 job 的 one-hot 在每个样本精确成立，因而相应所有已定义矩等式也成立。

## 3. 合法完整行配置的精确 pair trade

对 v 使用以下另一配置分布 K_v，每类仍取均匀 H-subset：

| C | H | 质量 |
|---|---|---|
| 1 | s | p/eta |
| 1 | 0 | 1/20+p-p/eta |
| 1 | h | 1/20 |
| 0 | 0 | 1/20+u0/2 |
| 0 | h | 1/20 |
| 0 | d | e+u0/2 |

这些质量非负、总和一。active 配置 H<=s，inactive 配置 H<=d，故负载至多 T。由 exchangeability，一行全部 C、Y_l 的 first/pair 只需核 C,H,CH,H(H-1)。

将 P 的 active bad 质量 p 改到 active H=s、质量 p/eta，并用 active H=0 平衡质量，保持 C,H,CH；它使 H(H-1) 减少 p d(d-s)。将 inactive H=d/2 的质量 u0 平分到 inactive H=0,d，保持总质量和 H，且增加 H(H-1) 数量 u0 d^2/4。由 u0=4p(1-eta)，两个数量相等。其余类别不变，故全部 original first/pair 精确匹配。

u 行只有一枚可见原 job R；z_l 行只有一枚可见原 job j_l。其真实 Bernoulli 边际本身就是合法 CONFIG(T) 分布，并匹配该行 first/pair。以上逐行配置 law 不被冒称为另一个共同 assignment law。

## 4. 所有全局 q 的二次负载局部化

在本原矩中，全部原端点变量仿射于 C,Y_1,...,Y_d。因此任意全局 deg q<=2 的多项式仍是这些变量的次数至多二多项式。

对所有 home 标签置换作平均得到 bar q。每个类别的 slack g=T-load_v 是常数。在 g>=0 的类别，Jensen 给 E[q^2|C,H]>=bar q(C,H)^2；唯一负类别 Y 全一，不受置换影响。因此只需核对称化多项式。Boolean 化简后它恰可写为

    bar q(C,H)=P(H)+C(a+bH)，deg P<=2.

记 q_a(x)=bar q(1,x)、q_i(x)=bar q(0,x)，lambda=d/h=2/eta。active-minus-inactive 为仿射函数，故精确有

    q_a(d)=lambda q_a(h)+(1-lambda)q_a(0)
             +q_i(d)-lambda q_i(h)-(1-lambda)q_i(0).

五个系数平方和为 4lambda^2-4lambda+3<=16/eta^2。五个右侧类别的质量乘 slack 各至少 eta/40；其中 inactive H=d 类别使用 e>0.79。Cauchy 因而给

    p(1-eta) q_a(d)^2
      <= (16p(1-eta)/eta^2) sum_(five classes) q_class^2
      <= (16eta/1000) sum_(five classes) q_class^2
      <= (eta/40) sum_(five classes) q_class^2.

其余 inactive H=d/2 类别的贡献非负，故 L[g q^2]>=0。非 v 行的 slack 在 P 每个样本非负，直接得到它们的全部全局 q 局部化。所有机器在这一步使用同一个 L。

## 5. 可用的背景接口及其准确限制

固定一个外部背景 b，设同一完整普通原矩的全部原 assignment 指示可写为 Phi_b(C,Y)，每个坐标均仿射于 C,Y。要求 P 支持上的每个 Phi_b(C,Y) 都是真实完整 assignment，且指定行 v 的可见原 jobs 恰为某枚 R 与 d 枚指定 payload jobs，端点指示仍恰为 C,Y_l；在 v 没有新增 payload。因此 v 的实际负载仍是 C+H/d。

在该合同下，任意全局 deg q<=2 的 q(Phi_b(C,Y)) 仍为局部 deg<=2，故第 4 节逐背景给 v 的全部负载局部化。第 3 节的配置 trade 也逐背景给 v 的 original first/pair 匹配。若 b 随机，须对每个 b 使用同一参数的 P，才能直接积分这项结论。

这项背景接口只自动证明指定行 v。新背景中 u、各导出头及其他机器的负载、原 job 覆盖和配置矩都须由完整 Phi_b 及单独论证核实；第 4 节不替它们承担新增负载。只有当其他行逐点 load<=T，或已另证其共同负载局部化与配置匹配时，才能宣称扩展输入满足全部行条件。

例如在某 z_l 上加入固定 payload b0>eta 而其余公式不变，取 q=1-Y_l 即有

    L[(T-load_(z_l))q^2]=(eta-b0)P(Y_l=0)<0.

所以将 z_l 改为有自有 payload 的内部孩子不能免费接线。直接将不同 z_l,z_j 合并也会出现正概率的两个 unit jobs 同头，而 T<2 的完整 CONFIG pair 不允许它。这里没有递归 shared-head 定理。

## 6. 总位复杂度与实际审计范围

所有参数和概率均为显式二进制有理数。给定 H 类别，t 个不同 home 指示乘积的期望是 (H)_t/(d)_t；补端点用有限展开，冲突 one-hot 单项式为零。因此任意固定次数 D 的全部共同矩可在显式原输入总位长的确定性多项式时间与位长内精确生成。D=6 足以列出本合同全部 M3 与二次负载矩阵；行配置 first/pair 同理。这里没有枚举所有子集，也没有优化或精确 SDP oracle。

实际 Fraction 审计代码为 sol_seven_state_star_quadratic_audit.py，129 行，SHA256 86d05b9013dda128a753f610eaeb9eec4146212c34fa9afcd2bbea3ccab382bd。它检查 12 组参数，及其中 3 组完整 small M3、全部 global q2 负载矩阵（最大分别 130、46 维）。实际输出 sol_seven_state_star_quadratic_audit.json 的 SHA256 为 9be19dec14e2abdb97377175372f63cbe47c08414e52516de5cc65cd74599335；root 已独立 fresh-output 重放得到同字节。有限审计没有代替上面的任意 d,s 证明，也没有检查 growing-depth 接线。

原作者稿 sol_seven_state_star_global_quadratic_coercivity_learning.md（SHA256 d560f9cf9a263d75cb1fa518a118078bcd013de91af4a8c771ced9257f3ef072）保留原字节。本文为其局部定理的自足重整，未纳入高 D 插值猜想或未完成的跨行 law；最终规范正文的实际阅读与软件身份单独记于审查，未把原件或未读文件自动认证。

## 7. 显式有限CONFIG证书：定基数first/pair稀疏支持

这里单独证明辅助Claim，不把原L改成下面的稀疏law。对显式d≥1、0≤h≤d，令φ(A)为h-subset A的(1,全部singleton、全部异pair)的0/1列，维数D。标签置换τ只置换φ坐标，故φ(τA)=A_τφ(A)为线性作用。

从A0={1,…,h}的单点law起，依次i=d,d−1,…,2均匀选j∈[i]并交换标签(i,j)。完整Fisher–Yates序列得到uniform permutation，故最终subset均匀。实际算法每阶段只保至多D个有权实际subsets：先展开至多iD个交换后候选，再在其φ特征上显式消列，保first/pair。因为后续每个阶段的期望是线性算子，阶段压缩不影响最终特征均值。

消列全在已列出的候选上作。将正权写a_l/Q，若候选数>D，在至多D+1列中求一个非零整数线性依赖u，φ列0/1给其系数O(D log(D+1))bits（用基本依赖minors）；常数坐标使Σu=0，故正负都有。取u_k>0中使a_k/u_k最小者，更新

    Q'=Q u_k， a'_l=a_l u_k−a_k u_l。

所有a'_l非负、和为Q'、至少一个为零，φ均值不变。重复至支持≤D。全程仅普通精确有理/整数消元，不调用定基数quadratic pricing或所有h-subsets枚举。每阶段至多dD候选、总O(d²D)次消列；每次共同分母只乘一个上述poly-bit整数，分支只乘i，故总分母bits≤log(d!)+O(d²D² log(D+1))=poly(d)。分子0≤a_l≤Q亦同。d=1无pair；h0/hd可唯一集合输出。

最终每singleton边际h/d、异pair h(h−1)/(d(d−1))。将§3每个固定(C,H)类别分别替为该算法输出，C固定使CY first/pair也保持，H固定使每配置实际负载不变，得到K_v至多6D个合法原CONFIG(T)及有理权。u,z是两点Bernoulli支持。全部矩/配置证书可按显式原d-job输入的总位多项式生成。共同L及全globalq证明仍用原uniform H-subsets，绝不声称新稀疏row law保三阶以上矩或是另一共同L。

root另有左右递归/超几何混合/显式O(d5)候选LP的不同构造；独立重构者先得到本Fisher–Yates方案，root实际读后才释放递归Proof，读后也另冻。二者是标准凸压缩工具的不同具体后端，不作全球新颖性认定。

## 8. 仿射Boolean原端点及unit owner边界

本P正支持包含Ω0={0,1}×({0^d,1^d}并全部h-subsets)，1≤h≤d/4。实仿射f=a+bC+Σc_iY_i若在Ω0上Boolean，则由Y0处a,a+b∈{0,1}知b为−1/0/1。b=±1时每个Y的两个C值都Boolean且差一，h-subset交换迫全部c_i相同、再h≥1迫c_i0，得C或1−C。

b0时取补可令a0。h1则每c_i0/1，全一处Σc_i0/1迫至多一个1。h≥2时比较共享h−1索引的两subsets，c_i−c_j∈{−1,0,1}：要么全同、由hc和dc都0/1迫全零；要么恰为c,c+1两层。h-subset高层计数覆盖整数区间[max(0,h−d+m),min(h,m)]，所有hc+计数要在0/1，宽度≤1。由d≥4h，两层若均至少2宽度≥2，故只剩唯一高层或唯一低层。唯一高层给c0及Y_i；唯一低层给H/h−Y_i，在全一处值d/h−1≥3不Boolean。恢复取补，完整清单为0,1,C,1−C,Y_i,1−Y_i；含h1、d4及h=d/4。

共同矩版本不要求新增原端点先有真joint law。令Lhat定义至次数6，M3 PSD，base(C,Y)≤4矩同P，原Boolean/onehot所有总次数≤6 identities，且选定每端点X有仿射f与Lhat[(X−f)²]=0。线性G=X−f为M3零向量，与deg≤3多项式正交。对r1..4，X^r−f^r=GΣ_(j=0)^(r−1)X^(r−1−j)f^j，故Lhat f^r=Lhat X^r=Lhat X。于是E_P[(f²−f)²]=0，正支持迫f逐点Boolean，落上列清单。一阶/pair通过同一零向量分别替换，得Lhat X=E_P f、Lhat XX'=E_P ff'。

不同primitive bits的四种jointpattern在Ω0全正；两个非零清单函数product均值0只可能同bit互补。故若一物理unit行的一组**不同原jobs**端点都受上述Gram-affine关系覆盖，且同行pair为0，则其中最多两个正一阶owners，恰两个时必须同bit互补；常数一只可独占。CONFIG(B<2)一致first/pair强制该pair0。未covered端点及任意多个零一阶资格不受此界。

逐固定背景β应用须在该背景重新有Ω0全支持与相应共同矩/Gram/pair条件；未条件化M3不自动免费给条件点。不能将这个fiber结论升为总物理入度≤2：独立均匀β∈[N]，新增N枚原unitjobs J_a仅在w、各自不同u_a可执行，令X_(J_a,w)=1_(β=a) C、另端为补。固定β只有一个正owner且所有端点仿射；积分后w有N个正first (1/10+p)/N、不同job pairs仍点态0，所有新增行逐样本≤1。完整原jobs和实际OPT1都保留。

## 9. 忠实AND原端点使globalq2检验失败

本Claim的矩前提是**base≤5**，不混§8的base≤4。固定任意i，新增degree-one原endpoint/显式Boolean坐标Z（不能只将CY_i改名算degree one）。共同degree6 Lhat/M3、原Boolean/onehot identities，base≤5矩同P，原v负载仍C+H/d，并假设忠实二次Gram等式Lhat[(Z−CY_i)²]=0。

取g=T−C−H/d、q=Z(H−h)。q在新原变量上真为degree2。G=Z−CY_i为M3的degree2零向量，可与degree≤3多项式正交。先用Boolean Z²=Z乘degree3的Q=g(H−h)²（总degree5），再以G乘Q，最后用base≤5：

    Lhat[gq²]=Lhat[QZ]=Lhat[QCY_i]
              =E_P[gCY_i(H−h)²]
              =−p(1−eta)(d−h)²<0。

C0四类被C消去；C1,H0有Yi0，C1,Hh有H−h0，仅坏C1,Hd剩负值。所有参数含最小d4都严格负；不需要额外CONFIG假设，加入它们亦无帮助。

物理读法可在原星外新增一unit job K，仅在两个不同新private machines时间一，以CY_i/其补分配。每样本所有原jobs完整，新增行≤1，真实law/M3/Gram皆有，但原v行新增可见q严格负。UM资格本身没有强制此AND，这只是给定点忠实依赖延拓的反例；改base、改v load、非忠实/别的非线性依赖均须另证。本页不据此否定所有非仿射gluing。

## 10. 实际来源与仍未解决的全局义务

kernel原Exact939a→identity先行224行7d61→root实际读后释放86行d560 Proof→identity实际全文读后100行7549；其中root曾参与插值，非另一blind。稀疏支持新Exact bf45→global先行65行a1e5的Fisher–Yates→root实际读后释放15行f3d7递归Proof→29行b5d6实际读后。仿射新Exact a38d→literal先行94行d320→138行作者Proof b887实际读后17行24f1；AND新Exact8ca3→literal先行57行a492→77行6869作者Proof实际读后15行8fbf。各先行背景如实披露，不倒改字节。root实际完整读这些Proof、重构、读后与129行audit，一次fresh CLI输出与作者JSON逐字同9be19dec；最终规范稿actualread另冻，来源/准确hash见审查。

核心控制坏态质量Θ(η³)且不随d/全局q维数丢失；新增显式rowCFG证书支付了输入到完整有限支持的可构造性。两类边界说明仿射复制和忠实AND分别怎样触发原unit pair/原二次负载检验，而非只画抽象logical gate。

局部输入本来OPT1。growing-depth shared owner仍缺同一原job law、全部机器共同负载与任何低载实际σ→源NO解码；各entry firstflow或逐row noise表不等于同一point。本页不声称rawSH3 gap、NP/UGC/GapETH lower bound或统一小于2算法。软件没有实现显式稀疏支持/接线/SDP finder；12有限参数不替代任意d,s证明。一般UM-TARGET-v1及其反面仍OPEN。
