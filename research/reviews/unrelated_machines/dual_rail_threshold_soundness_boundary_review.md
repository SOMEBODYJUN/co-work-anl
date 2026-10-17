# 双轨阈值编码：四个成本合同的实际审查

读取目的：区分数学盲重构、冻结全文读后攻击与实际实现核验；以下保留两位内部审查者各自的实读记录，不用一致意见代替证明。正文最终 SHA256 为 `069d7ac109263c410b0874e86840d5ad8fb0720b03b4acaae80825c7d11550ee`。四合同无尚成立 fatal；外审、新颖性与独立论文价值未认证。

根研究者亲读全部六份代码并重跑：scalar规范12565个完整小模板、2000个随机模板、748个小实例真实OPT；独立半槽250随机及完整32768份锐例原σ；split规范18479模板、2000随机及32768个内外模式（不是4251528份物理σ）；cube独立A1..5的6342个cuts、352个breakpoints与10份完整实际证书；单例外2000随机及597223份实际σ。有限运行只核实现，不承担一般证明。标准ST半质量推论及整数流已明确扣除。

root另从原资格重建12份具体证书：scalar10机15job、split14机15job、两份cube A3的42机165job、单例外arity越界A1..8。逐job原边合法并对所有机器重加负载；巨大binary A、空变量/rail、零权边分别在实现核验覆盖。所有数字由冻结stdout绑定，不将split模式枚举计作实际σ枚举。

代码独立性：独立半槽不import规范；cube独立oracle只将规范模块作为被测对象，其原矩阵重建、全cuts及breakpoints判断独立实现；单例外源于先陈述独立代码，root修正空轨变量不应要求另一轨exception的过强验证并新增该边界例，仅该域检查和错误source标签作修复，没有把它称为完整公共JSON solver。规范scalar的quarter-flow只保证全局三半，独立half-slot另保证clause≤1；不混称两个API的强结论。split公共API列出全部unit资格，A截真实arity，cube生成器按显式展开P/输出规模计复杂度。

[正文](../../current/unrelated_machines/dual_rail_threshold_soundness_boundary.md)及[冻结原输出](../../../evidence/runs/unrelated_machines/dual_rail_threshold_soundness_boundary_audit.json)是现行身份。接下来的两份审查原文说明各自先陈述/读后顺序；其中scratch文件名仅为审查过程定位，结论和必要内容已保存在本页及登记文件。

---

# 双轨阈值编码最终全文：数学读后攻击

审查者为 boss11 内部 `cover_consistency`。本次只审数学合同与证明，不冒称审计规范代码、独立程序或其运行直方图。此前 `dual_rail_one_exception_statement_first_review.md` 的单例外盲重构保持原字节；本次其余合同是读主文后的独立攻击，不倒写为 statement-first。

## 实际读取身份与结论

首次全文实读：`research/current/unrelated_machines/dual_rail_threshold_soundness_boundary.md`，SHA-256 `1a75b45978353ca15e0e078be1851bedec55d4c38fd384c940742f0f0f139e2c`。随后根研究者通知修复 §4 说明性阈值措辞，再次实际全文读取最终稿：

    069d7ac109263c410b0874e86840d5ad8fb0720b03b4acaae80825c7d11550ee

最终 §4 正确分别给出固定指定端口、自由选择最大端口及 W=1 的阈值化条件，避免原“只有 W=1 才等价”过强表述（例如 rho>=2 时其他参数上也可同时为真）。四正式合同没有因此改动。

在此最终哈希和各自明确模型内，完整读后攻击**没有尚成立的 fatal objection**。不认证全球新颖性、外审、独立论文价值或一般 `UM-TARGET-v1` 的任一结论。

## 四合同不混用

| 合同 | 内端 | 外端及arity | 实际结论 |
| --- | --- | --- | --- |
| 归一化scalar | 每轨K端口各1/K，selector1 | clause标量时间1/A_c，arity<=2A_c−1 | 全机C<=3/2，clause<=1 |
| split unit | 同一归一化rail | 至多min(A_c,m_c)台unit机，每port外端时间1，arity<=2A_c | 全轨<=3/2，全部unit<=1 |
| 单例外 | 非负w、每轨W<=1、指定例外满足W−w_e<=rho−1 | 全局A，scalar时间1/A，arity<=2A | 全机<=rho，clause<=1 |
| 完整cube | 第一合同的特殊族，d=2A−1、k=2^(d−1) | 全2^d符号clauses，各scalar时间1/A | 精确OPT=min_B max(B/A,1+ceil(R_B/d)/k) |

每个模型都无其他任务或背景容量；空rail与全空dummy分别处理。不能把split unit的成本1当作scalar的1/A，不能把一般非均匀w替换归一化K，也不能把完整cube的对称性给任意源公式使用。

## §1：全类三半是半质量有序槽的直接推论

每job在两个真实不同端点各一半，对任何job子集的两份半片，槽容量至多两半片给Hall覆盖匹配。轨上selector半片必须位于第一槽；若selector被该轨接收，第一槽已被占，其他port数至多floor(K/2)，故负载<=1+floor(K/2)/K。K0单独是selector，不除零。未收selector的轨即使接全部ports也仅负载1；clause最多ceil(m/2)<=A_c枚ports，所以负载<=1。所有结论来自同一次匹配，不是逐机各自选不同任务。

一般半质量行权的奇序号和 O 满足 O<=(sum w+w1)/2，因而分数行负载<=T、最大支持时间<=T时给3T/2。这是经典有序槽工具的特殊输入，不是一般LP二倍界的新改进。主文已明确扣除。另一共同整数流说明中的1/4内留、3/4外送满足K/4<=floor(K/2)（K>=2）及3m_c/4<=floor(3A_c/2)；K1双轨变量的半分数供给只占更少clause流量，两类共用同一容量才成立。该段不替代自足半槽证明。

严格源等价也成立：C<=1时selector轨上的所有port处理时间均正（K>0），故必须全外送；反向把真ports外送、假ports全内留给合法C1。K0没有occurrence，不产生假除零约束。C>1后部分真ports留在selector旁正是弱解码失败点。

## §2：原锐例只证绝对阈值锐

四clause的严格源矛盾为：y真时前两clause要求x同时真假，因此y假；后两又要求z同时真假。每轨K2，实际处理时间只有1/2和1；无C<=1且负载半整数，故OPT>=3/2。给出的正selectors、正ports外送、负ports内留分配逐类负载为轨1、clauses(3/2,1/2,1,0)，达到该值。10机器15任务计数无误，重复occurrence必须保留为不同任务。

此例自身OPT=3/2；它证明全类绝对上界C<=3/2不能降低，并不证明“3/2近似比”不能改进。主文的近似保证来自存在selector时OPT>=1，两者层次不同。本文没有声称每clause变量互异也由此锐例得到锐性。

## §3：split unit实际整数流及全部机器

每变量删空轨分支后两轨K均正，D=K_++K_-，source供给b=floor(D/2)。给每occurrence半流再删一枚半单位可使每变量精确供给b，同时clause流<=m_c/2<=A_c。原整数网络可取整数满流，没有使用分数port作为实际任务。

若两符号都未达到ceil(K_s/2)，则z_++z_-<=ceil(K_+/2)+ceil(K_-/2)−2<=b−1，和满供给矛盾。选达到者放selector，只让此符号已被流选中的ports保留外送，另一符号全部内留。返回ports只会减少clause占用；选轨负载<=3/2，另一轨<=1。每clause真实外送数<=min(A_c,m_c)，给它们不同unit机器，每unit时间1且至多一job，负载<=1。

L_c=min(A_c,m_c)不会按二进制巨大A_c展开机器。四clause锐例在unit模型中C<=1仍强制真ports外送且每clause至多A_c枚，严格源矛盾仍适用；半整数负载网格再给下界3/2。机器数改为6轨+8unit=14，任务仍15，不能沿用scalar机器数或外端成本。

## §4：单例外与arity界

对两轨都非空的每变量，恰有两枚来自不同rails的真实指定exceptions。clause端点可以相同；此时半分数候选在同clause合为质量1。每clause的半分数质量不超过其真实exception incidence的一半，至多arity/2<=A。整数容量匹配选择每变量一个端点；同clause两exceptions最后只选一枚，而arity仍计两枚occurrences。

实际输出负载为选中rail的1+W−w_e<=rho，另一railW<=1，clause至多A枚各1/A。空rail变量放selector在空rail且无外送。rho>=1是承重前提。容量可截至变量数，单位source边使最多变量数次增广，无需展开数值A的slots。

最终阈值文字已正确：固定e用w_e>=W+1−rho；允许自由选择时用max w_e>=W+1−rho；W1才把阈值表达式化为2−rho，W<1的max>=2−rho是更强充分条件。不能用另一较大端口替代固定指定e。

2A+1锐界只在rho1作出：两clauses、2A+1变量，各rail唯一port内部时间1。C<1+1/A<=2强制每变量至少一port外送，同时各clause最多A枚，因为其外端1/A。因此至少2A+1枚供给超过两clause共2A容量。A与A+1分配达到1+1/A；A1仍成立，不能遗漏严格C<2才能强制外送的条件。没有推出一般NP困难性。

## §5—§6：cube精确min_B没有遗失物理解

全符号cube在任一赋值下都有全真d文字clause，所以A>=2时是弱阈值d−1也无解的实际NO源。A1时d=A=1，不能称NO。变量每符号出现k，机器2d+2^d、jobs d+d2^d均正确。

下界的关键归一化合法：逐变量交换rails并同步置换全部clause masks确是完整cube同构；之后所有selectors在负轨。正ports全移回无selector的正轨，最后负载恰1<=C，且其他机器只减负载。因此没丢失任何可能更优实际σ。

若C>=d/A，B=d已经给F_d=d/A<=C；不能直接把超范围的floor(AC)代入有限最小值。其余情况B=floor(AC)严格属于[A,d−1]。每负轨至多h=floor((C−1)k)枚内留port，每size-s clause至少(s−B)_+枚内留，故dh>=R_B，h>=ceil(R_B/d)，进而C>=F_B。所有floor/ceil在整数真实port数上使用，没有以平均分数内留替代实际负载。

上界固定B的删除网络中，每size-s clause均匀送(s−B)/s到其负变量，单边<=1。完整变量置换对称性使各变量恰R_B/d<=r_B，所以有理满流可整数化。实际输出中每clause外送恰min(s,B)；全负clause使最大外负载恰B/A。负轨内留整数总和R_B、各至多ceil(R_B/d)；R_B>0时至少一轨达到这个上整值，R_B0时selector本身为1。因此实际最大负载确为F_B，而非仅一个松弛上界。扫描所有B并取最小与下界吻合。

maxflow单位增广次数至多R_B<=d2^d，受**显式原port数量**控制；d-A+1个候选B也受显式输入控制。这是输入已经展开成2^d clauses、d2^d ports后的位多项式；不是poly(A)，更不是按二进制A的polylog(A)。用生成参数A表达族的简短公式，不会把指数输出成本消掉。

## §7—§8：趋一证书与A3精确值

固定某变量为负出现，可供选外送的负文字数<=A的clauses共有sum_{t<=A−1}binom(2A−2,t)>=k/2。各变量可各选k/2，不需协调：所有外送都只进s<=A的clauses，所以任何clause最多A枚外送。由此所有负轨恰3/2、正轨1、clause<=1，是完整而非投影证书。

R_A闭式可由尾和直接推出。令c=binom(2A−2,A−1)，则sum_{t=A}^{d−1}binom(d−1,t)=(k−c)/2，sum_{s=A+1}^dbinom(d,s)=k−binom(d,A)，以及A binom(d,A)=dc，合得R_A=(dc−k)/2。作为辅助精确算术检查，本审查者独立核过A1..100的定义与闭式一致；这不是程序审计或一般证明的替代。

对S~Bin(d,1/2)，中心正部期望为一半绝对偏差，Cauchy给E(S−A)_+<=sqrt(d)/4。配上R_A=2^dE(S−A)_+、k=2^(d−1)和ceil余项1/k，确得OPT_A<=1+1/(2sqrt(d))+1/k趋1。固定1<rho<2时，可同时取此上界<rho及rho A<d，所以弱阈值floor(rho A)仍NO而实际C<rho，否定的是该具体码的soundness。

A3证书中五个size4 clauses分别内留(i+1 mod5)，各变量各一次；size5再给变量0、1一次，所以负轨计数(2,2,1,1,1)、总内留7、最大1+2/16=9/8。每clause至多三枚外送。C<9/8归一化后每负轨最多一枚，总至多5；五个size4及一个size5 clause合需至少7，矛盾。42机器165任务及真正OPT9/8均核对，无需假定算法输出某源赋值。

## 边界及最终standing状态

所有四正式合同在其自身量词/资格/外部成本下成立；未发现standing fatal。本文没有为主文链接的程序、有限直方图或cut oracle实现作代码审计；那些事实由根研究者及实际实现审查记录承担。半质量有序槽、整数匹配、流整数性都按基本经典工具使用，没有在本页认证文献全球新颖性。

低负载构造和cube counter-soundness只排除具体双轨编码合同；状态相关资格、非归一化跨层负载、其他背景容量或更复杂一致性机制仍需自己的分析。最终稿保持一般UM-TARGET-v1及其反面OPEN，是正确范围。


---

# 双轨四合同 canonical 最终冻结全文审查

## 审查顺序、范围及版本

本轮先实际全文读取

    research/current/unrelated_machines/dual_rail_threshold_soundness_boundary.md
    1a75b45978353ca15e0e078be1851bedec55d4c38fd384c940742f0f0f139e2c

对四个正式合同作攻击后，只提出§4固定指定例外与自由挑选max条件的说明性措辞问题，未发现定理的致命反例。root接受并修改该段，随后实际读取变更段、核对最终hash

    069d7ac109263c410b0874e86840d5ad8fb0720b03b4acaae80825c7d11550ee.

不仅依据root“其余不变”的报告：我把最终稿中这一段换回先读时的原段，所得完整字节SHA256恰为原1a75b459...139e2c，因此独立核实此次版本间只有该段变化。两版本均另存scratch snapshot；旧盲稿未改，仓库未改。

审查来源分层：normalized半槽证明与完整锐例原P枚举在读root/shared新稿前独立完成；fullcube精确式也先按statement独立重构、随后读scratch冻结稿；split及one-exception则属于本次canonical读后攻击。未把这些来源伪称全是盲审。根研究者执行的规范/独立代码运行和软件计数，不冒称我亲跑。

## 1. Normalized scalar合同及ST扣除

正式输入仍精确保留arity m_c≤2A_c−1，A_c独立整数，K(v,s)为真实出现数、可零；重复occurrences为不同真实任务；机器组互异，无背景任务。没有把split的2A_c范围悄悄并入normalized身份。

先selector半片再port半片的rail slots数ceil((K+1)/2)，clause slots数ceil(m/2)。每job两不同原端slots，每slot至多两job半片，任意job子集S的2|S|关联逼|N(S)|≥|S|，同一matching覆盖全部任务。收selector的rail第一slot必被它占用，port数≤floor(K/2)，负载≤3/2；其余rail≤1、clause≤ceil(m/2)/A_c≤1。K0只selector、K1首槽冲突、空变量/clauses的dummy分支均正确。

一般半行引理也成立：排序w1≥w2≥...，每两枚半片一slot，匹配负载≤O=w1+w3+...；O−w1≤w2+w4+...，故O≤(Σw+w1)/2。半质量行负载≤T、支持最大≤T给3T/2。本文明确将其作为ST有序槽直接推论，不冒充一般二倍界改进或原创算法。normalized中selector排首也是有序槽（K1时平局先selector）；不同A巨位长不需展开A个slot。

共同整数流替代实现虽不是本证明所需，其1/4留候选轨与3/4送clause的局部容量也成立：K≥2时K/4≤floor(K/2)，m≤2A_c−1时3m/4≤floor(3A_c/2)；K1/K1变量的单位供给及空轨分支须共享同一次clause流。正文明确了这个承重条件，没有先独立分流再非法相加。

## 2. Scalar锐例与近似比边界

四个重复literal clauses确使源严格无解：y真迫x同时假真；y假迫z同时假真。C≤1实际调度解码真ports均外放，排除该值；所有实际负载半整数，故OPT≥3/2。正文给的all-positive-selector实际上界逐机正确：六轨一，四clause分别3/2,1/2,1,0。

我此前独立代码已重建原10机15job两端矩阵并枚举32768份合法σ：13824份C3/2、18944份C2。该枚举只适用于scalar原P，不可用作split物理枚举。

正文正确只称absolute T1上界锐。虽然selectors时间一逼OPT≥1，C≤3/2因此推出此类3/2近似，但OPT=3/2的该锐例本身输出也是最优，不证明算法approximation ratio的3/2锐性。未发现正文混称。

## 3. 新split-unit合同的完整证明攻击

### 模型及位规模

每clause L_c=min(A_c,m_c)台私有unit机，port在其中任一台时间一、内部仍1/K。与scalar不同，这是每port可有多条外部边的新真实P；不能把它当旧矩阵的同对象。L_c≤m_c控制显式规模；空clause无unit机，若最终无机器添dummy合法。

### 全局flow

有空轨的变量可把selector停空轨，另一轨全部port内收负载≤1，无需占任何clause。剩余两轨均非空的变量D_v=K_++K_-，供给b_v=floor(D_v/2)。先每occurrence半流，变量总D_v/2，clause入流≤m_c/2≤A_c；D_v奇时删掉该变量任一枚occurrence的半流即可准确降为b_v，只会降低clause入流。于是有总供给sum b_v的有理满流，整数容量流给整数满流。所有clause在同一网络共享容量，不存在逐clause选择相互冲突。

设整数选中数z_+,z_-，和恰b_v。若两者均少于ceil(K_s/2)，则

    z_++z_-≤ceil(K_+/2)+ceil(K_-/2)−2≤b_v−1.

最后一步逐奇偶均正确：两偶给b−2，一奇给b−1，两奇给b−1。因此至少一轨有z_s≥ceil(K_s/2)。只保留该符号的selected ports外送，另一符号selected ports收回，只减clause使用。selector在合格轨，其内留port数K_s−z_s≤floor(K_s/2)，负载≤3/2；另一轨全port合计一。每clause最终外送≤A_c且≤m_c，能逐一给不同的L_c台unit机，各负载一。实际任务唯一分配、全部原合法边均有保证。

### 14机15job的真OPT

不能直接搬用§2那份scalar上界σ，因为其首clause外送三件会超出两台unit机。正文没有这样做，而由本节构造给上界；这点是实质需要的区分。

我另用此前独立半槽scalar输出（它每clause≤一，即最多两port）将外送port注入各clause两个不同unit机，独立生成完整14机15job真实矩阵、每job所有原端和实际sigma。逐job累加与逐machine重加得到

    rails: 3/2,1,3/2,1,3/2,1;
    eight units: 1,1,0,0,1,0,0,0.

因此实际upper为3/2、所有unit≤1。新script及输出在scratch `independent_split_sharp_assignment.py/.json`；script SHA256

    83e318ce9965f7cba0b48d4ae5c0ec1f441ae554c6cb59a91ac82f620aab522c.

下界也完整：C≤1时selector rail无正port，每clause两unit机最多收两件，故仍解码那四clause的严格源解，不可能。所有有限时间是1或1/2，C<3/2必C≤1，所以OPT≥3/2。该论证不依赖端点数仍二；事实上split ports有三个可用端。独立程序列八种selector真值的违反clause；**没有枚举全部4,251,528份split物理σ**，该下界是一般计费推导加八种真值核对。

### 位复杂度

总供给≤真实occurrence总数，capacity可截m_c或变量数；单位增广次数因此对显式输入多项式。给unit不同目的地只用实际外送数≤m_c，不按巨大A_c数值循环。K0在预处理消去、K1/K1被整数ceil反证覆盖，不需额外不存在性假设。

## 4. 单例外rho合同及已消除措辞问题

每条轨总内部W≤1、selector仍一；对每未预处理变量的两条非空rail，各给一个实际指定exception e，要求W−w_e≤rho−1。每变量给两exception的clause候选各质量1/2；同clause时合为一。每clause收到的exception incidence至多原arity≤2A，故分数使用≤A。同一物理occurrence只能属于一个变量、一个rail的exception，不会跨变量重复计数。整数容量匹配给每变量一个具体exception；同clause的双候选任选一条满足指定合同的真实port即可。

外送这个exception、selector放其rail，所选rail负载≤1+W−w_e≤rho；另一轨≤1，clause≤A/A=1。rho≥1确保所有机器共同≤rho。非负零w、W0但rail有ports、全局A大位长、同clause两候选皆无漏洞。容量截变量数防止按A展开。

我对旧版本的唯一异议是：固定指定e的条件不能被“存在某个大port/max”替代；而rho≥2时即使W<1，两个阈值条件也可能同时恒真，所以“只有W1才等价”字面过强。最终版本精确区分

    指定e：w_e≥W+1−rho；
    自由挑选：max w_e≥W+1−rho；
    W1：阈值化为2−rho；
    W<1：max w_e≥2−rho为较强充分条件，不能换掉指定e。

新段消除了这个说明性问题。正式定理及原证明本来就按指定e假设，未因此反驳。

arity例外边界也正确：2A+1变量、两clause、每rail唯一内部时间一port。C<1+1/A≤2迫每变量至少一port外送，但每clause最多A件，总2A不足；按A和A+1分给两clause给上界1+1/A。故该越界例说明rho1、arity2A条件不能随意升至2A+1，没有NP-hardness结论。

## 5. Fullcube正式迁移及引用核对

已对scratch原全文a4f7f663...cea33作过单独冻结攻击且无fatal。本次额外机械比较原§2–5与canonical§5–8，除了标题编号、Claim ID、准确加上“第1节归一化模板取完整cube”的定位句、把第3节引用改为第6节、尾部空行，数学正文完全相同。比较脚本按这些精确字符串替换后对两段strip字节相等。

因此原先已核的selector独立翻符号同构、正轨规范化、B=min(d,floor AC)分支、ceil R_B/d、对称分数流与整数输出、clause恰min(s,B)、全部原rail/selector负载、R_A闭式和Cauchy近一估计均保留。A1边界及A≥2 fullcube无严格YES、也无弱B≤d−1解，仍写清；条件YES映射不冒充本族有YES。

引用正确：§7取第6节B=A，§8下界取第6节同构。第1节scalar合同、split新合同、单例外合同不混成一个P。§9将已知ST/flow扣除，不把近一NO见证当一般困难性。另独立已核A20时最优B21，故保留min_B而不是偷改成总取B=A是必要的；当前公式保留正确。

仅核markdown链接存在性时，single-job投影目标已存在；本轮canonical review链接在审查时尚未创建，root正在汇总，属于交付前导航待生成，不是数学异议。

## 6. 最终状态

最终hash069d7ac109263c410b0874e86840d5ad8fb0720b03b4acaae80825c7d11550ee范围内，四正式定理均无standing fatal objection。§4说明性异议已实际修正并复查。精确锐界只评absolute T1合同，未把它升为算法approximation ratio锐性。保留源与调度真值、一般证明与有限实现、独立先陈述与读后攻击的层次。

尚未认证新颖性、独立论文价值、外审或root/shared规范软件的全部运行计数；本审查不涉及一般UM-TARGET-v1正反结论的升级。
