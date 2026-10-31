# 双轨阈值编码的三半上限与立方体真实前沿

读取目的：检验把一般 signed 阈值 PCSP 的近二源间隙搬到实际调度的具体编码，而不是把配置间隙当计算困难性。本页固定真实任务、资格和外部容量，给出整类编码的低负载算法、精确锐例及一个完整 NO 源族的真实最优值。UM-TARGET-v1 及其一般反面仍 OPEN。

**扣除经典工具后的地位。** 归一化双轨的三半界是标准有序槽在半质量证书上的直接推论；容量流与单例外选择也使用标准整数匹配。本页不把这些工具包装成原创近似算法。新增可复用内容是精确编码合同、全部机器实际输出、错误 NO 解码的具体失效范围、两种外部容量读出的锐例，以及立方体族的真实 OPT 精确前沿。新颖性、独立论文价值和外审均未认证。

## 1. 归一化双轨：即使源无解也总有实际三半调度

显式变量集 V，每变量两台私有机器 U(v,+),U(v,−)，一枚 selector job 仅可在这两轨上用时1。每 clause c 有一台不同于所有轨及其他 clause 的机器、整数 A_c≥1、m_c≤2A_c−1 枚真实 occurrence。重复字面仍算不同 occurrence/job。

令 K(v,s) 为对应轨的实际 occurrence 数，允许零。每 occurrence e=(v,s,c) 有一枚 port job，仅在 U(v,s) 用时1/K(v,s)，或在 clause c 用时1/A_c。K=0无port，绝不除零。没有其他任务、预载或背景容量。若连变量及 clause 都空，添一台空 dummy 以保持 m≥1。输入是显式变量/occurrence 与二进制整数 A_c；不靠二进制声明巨大变量数再隐式展开。

**UM-NORMALIZED-DUAL-RAIL-UNIVERSAL-THREE-HALVES-v1。** 对所有上述实例，不需要源真值赋值、未知 YES 或最优值，可确定性总位多项式输出每件 selector/port 的原合法目的地，全部机器共同 C_max≤3/2。若 V非空，selector给 OPT≥1，因此也是此类的3/2近似；V空时任务空，输出0=OPT。常数作为此类的绝对上界精确锐，见第2节。

### 半质量有序槽的自足证明

每件原任务在两个原端点各放一枚半片。每轨把 selector 半片放首，随后K个port半片两两成单位槽；每 clause 也把其port半片两两成槽。每job恰邻接两个槽，每槽最多有两枚半片。对任意job子集S，2|S|条半片入至N(S)，每槽至多2条，故|N(S)|≥|S|。确定性增广路匹配覆盖全部job；匹配槽所属机器就是实际σ。

若一轨收到selector，它占第一槽，其余port数至多ceil((K+1)/2)−1=floor(K/2)，故真实负载≤1+floor(K/2)/K≤3/2（K0仅selector）。未收selector的轨至多接自己的全部K枚port，负载≤1。每clause接收port数≤ceil(m_c/2)≤A_c，故负载≤1。所有机器在同一次matching共同满足界。

这正是ST有序槽的半质量特例：一般一行按时间w1≥w2≥…排序，半片两两成槽，匹配负载至多O=w1+w3+…；因O−w1≤w2+w4+…，有O≤(Σw+w1)/2。半质量分数行负载≤T、最大支持时间≤T即得3T/2。本模板轨的半负载≤1，clause半负载≤1，所有支持时间≤1。这里既未声称一般实例可求半质量见证，也未声称ST一般二倍界改进。

另有独立的共同整数流实现：K≥2的候选selector轨，每port可向该轨计数容量floor(K/2)或向clause计数容量floor(3A_c/2)；分数1/4留轨、3/4外送可行。两轨均K1的变量用一单位供给向两occurrence各分一半，整数读出后才选selector轨；空轨直接停selector。两类必须在**同一次流**中共用clause容量，不能独立拼接。此实现只承诺全局三半，独立半槽实现另给clause≤1。

### 严格阈值确可嵌入，弱端却不能据此解码

把selector所选轨的字面定义为真。源若每clause真字面数≤A_c，令真ports全外放、假ports全内放，得到C≤1。反过来C≤1时，selector所在轨不能再容纳任何正时间port，故所有真ports必须外放，各clause最多A_c枚，所以可解码严格源解。这个严格等价不推出弱端soundness：C>1时可以只外送同一真轨的一部分ports，其余留在selector旁。

## 2. 十台机器十五件任务的三半锐例

三变量x,y,z，四clause的A_c均为2，occurrences依次为

- (x+,x+,y+)；
- (x−,x−,y+)；
- (y−,z+,z+)；
- (y−,z−,z−)。

每条轨K=2，故全部port两端均为1/2，selector为1。前两clause若y为真，会同时要求x假和x真，故y必须假；后两在y假时又同时要求z假和z真。因此没有严格源解，前述等价排除C≤1调度。全部实际负载在半整数网格上，故OPT≥3/2。

将所有selectors放正轨、所有正ports外放、所有负ports内放。六轨负载均为1，四clause负载为3/2,1/2,1,0，故OPT=3/2。实际原矩阵恰10机器15任务，重复occurrence是本锐例承重前提，不声称每clause变量互异时也由此例锐。两份独立程序均枚举全部2^15份原合法σ；其直方图为13824份C=3/2、18944份C=2。

## 3. 把clause拆成不可双占的unit slots也不能救近二soundness

另立模型以免偷换外部成本。每clause c给A_c≥1，arity现允许m_c≤2A_c；它的外端改为L_c=min(A_c,m_c)台私有unit机器。每port在自己的轨仍用1/K，但在本clause任一unit机器上都用1，其他边∞。其余selector/轨规则不变。截断L_c不改变任何有用容量，却避免按二进制巨大A_c展开空机器。无机器时仍添dummy。

**UM-SPLIT-CAPACITY-DUAL-RAIL-THREE-HALVES-v1。** 对每个上述实例，可确定性总位多项式输出完整实际σ，所有轨≤3/2，所有unit机器≤1。存在selector时亦给本类3/2近似。第2节同一四clause输入、改为每clause两台unit机后，14机器15任务的真实OPT恰3/2，因此绝对界锐；没有将外部scalar时间与unit时间混作同一对象。

证明：先把含空轨的变量停selector于空轨，其余ports全内收，不进流。对其余变量v设D_v=K(v,+)+K(v,−)，供给b_v=floor(D_v/2)。网络为source→变量（容量b_v）、变量→每真实occurrence（容量1）、occurrence→其clause（容量1）、clause→sink（容量A_c，实际可截至m_c）。每occurrence分1/2给出每变量D_v/2和每clausem_c/2≤A_c；每变量有多余半单位时删去一枚半流，得精确供给b_v的有理满流。整数容量保证整数满流。

令z_+,z_−为某变量被流选中的两符号port数。若两者都小于各自ceil(K/2)，其和≤ceil(K+/2)+ceil(K−/2)−2≤b_v−1，矛盾。因此可挑一个符号s，使z_s≥ceil(K_s/2)。selector放该轨，**只保留该符号被流选中的ports外送**；其他ports全收回自己的轨。选轨负载≤1+(K_s−z_s)/K_s≤3/2，另一轨≤1。舍去部分外送只减少clause占用；每clause外送≤A_c且≤m_c，给它们不同unit机即可。所有任务逐件原边合法。

锐例下界仍由严格源无解及所有有限处理时间为1/2或1推出。上界来自本构造，unit外端不能在<2负载下双占，所以此结果确实绕过了“近似倍数会放大scalar clause容量”的解释。两个source-based编码都失败，并不否定有更复杂内部状态/跨层一致性的归约。

## 4. 非均匀内端的单例外匹配合同（另一准确受限范围）

**UM-DUAL-RAIL-ONE-EXCEPTION-FLOOR-v1。** 此处每port内部时间可任意非负有理w_e，每轨总W≤1；selector仍为1。外端是单台clause机器、每port统一用时1/A，正整数A全局固定，arity≤2A。给有理ρ≥1；含空轨变量直接停selector。对其余变量的每条轨，给一枚指定真实exception e，使W−w_e≤ρ−1。则可总位多项式输出完整C≤ρ调度，每clause≤1。

每个未处理变量仅匹配其两exception的clause端点，clause整数容量A。两候选各分一半（同clause时合为质量1）可行，因为每clause的exception incidence至多arity≤2A。整数匹配给每变量选一例外：将该port外送、selector放其轨，其余全内收。所选轨≤1+W−w_e≤ρ，另一轨≤1，clause≤A/A。容量截变量数、至多变量数次单位增广，不展开数值A。

固定指定e的真实条件是w_e≥W+1−ρ。允许自由选择例外时，精确条件为max w_e≥W+1−ρ；在W=1时阈值化为2−ρ。在W<1时，max w_e≥2−ρ仍是可用的更强充分条件，不能据某枚较大端口就替代原先固定指定的e。

arity界对ρ=1锐：两clause、2A+1变量，每变量两轨各有唯一内部时间1的port，正/负分别接两clause、外端1/A。此例除arity=2A+1外满足合同。每个C<1+1/A≤2调度必须每变量至少外送一port，却总clause容量不足2A+1，故OPT≥1+1/A；将变量按A与A+1分给两clause达到。没有把此度数锐例当近二NP困难性。

## 5. 完整符号立方体源与实际实例

取整数 A>=1，d=2A-1，变量数 d。源包含全部 2^d 个符号模式的 d 元约束。每变量每符号恰出现

    k=2^(d-1)

次。对任何赋值 x，总存在一个符号模式使全部 d 个文字都真。因此 A>=2 时，该源即便将每约束阈值放宽至 d-1=2A-2，也没有解。这是可直接验证的 NO 源输入，不声称该单个源族本身 NP-hard。A=1 时严格阈值等于 d，不能称为这个 NO 族。

实际调度实例有 2d+2^d 台机器和 d+d*2^d 枚 jobs。全部边、任务和共同 clause capacities 都显式列出。

## 6. 精确最优值公式

对整数 B 属于 [A,d]，定义

    R_B = sum_{s=0}^d (s-B)_+ * binom(d,s),
    r_B = ceil(R_B/d),
    F_B = max{B/A, 1+r_B/k}.

**UM-DUAL-RAIL-FULLCUBE-EXACT-FAILURE-v1。** 第1节归一化模板取该完整立方体得到的实际调度实例的整数最优 makespan 精确为

    OPT_A = min_{B=A,...,d} F_B.

所有量词为每个整数 A>=1；目标是这个显式族的最优值，非一般算法或困难性。给定显式 cube，可确定性按其总编码长度多项式构造达到所选 F_B 的实际完整分配。

### 下界

每个 selector 时间 1，所以任何实际 makespan C>=1。若 C>=d/A，选 B=d 已有 F_d=d/A<=C。否则令 B=floor(AC)，它属于 [A,d-1]。

由于源含全部符号模式，可以逐变量交换正负轨，同时相应置换 clause masks 和 ports。这是实例的同构，故不失一般性所有 selectors 均在负轨。

所有正 ports 可移回正轨，合计负载恰 1<=C；这样不会增加任何其他机器的负载。故可设正 ports 全部内放。每个负轨最多容纳 h=floor((C-1)k) 枚负 ports。一个有 s 个负文字的 clause 至多容纳 B 枚负 ports，至少 s-B 枚（正时）须移回各自负轨。全 cube 至少需 R_B 枚内放，故 d*h>=R_B，从而 h>=r_B、C>=1+r_B/k。又 C>=B/A，所以 C>=F_B>=min F。

### 上界和实际可构造性

固定 B。对每个负文字集合 S、s=|S|>B 的 clause，需从它的 s 枚负 ports 中选择 s-B 枚内放；其他 clauses 无需内放。建立二部网络：source->clause 容量 s-B；clause->v 对每个 v 属于 S 容量 1；v->sink 容量 r_B。

存在显式有理满流：clause 将其 s-B 均匀分给 S 中 s 个变量。由于全部 2^d 个 S 都存在，变量置换保持该流规则；每个变量总流量相同，合计 R_B，故每个恰为 R_B/d<=r_B。各 incidence 流量 (s-B)/s<=1。整数容量最大流因此有整数满流。也可直接以整数增广路求取：最多 R_B<=d*2^d 次单位增广，是显式原 port 数的多项式，不是按隐藏数值作伪多项式推断。

将满流选择的负 ports 内放，其他负 ports 放 clause，所有正 ports 内放，selectors 在负轨。各 clause 外放负 port 数恰为 min(s,B)，故最大 clause 负载恰 B/A；每负轨内放 ports 至多 r_B。若 R_B>0，平均数迫使至少一轨恰达到 r_B；R_B=0 时 selector 本身负载 1。实际 makespan 恰 F_B。取所有 d-A+1 个 B 中最好者即可。

输入规模含显式 2^d clauses 和 d*2^d ports。上述是按展开后的输入编码长度多项式，不声称 poly(A)。所有时间分母为 A 或 k，位长 O(A)；网络容量和全部计数不超过显式任务数。

## 7. 与 rho 无关的三半逃逸及更强近一族

一个无需最大流的 C<=3/2 证书适用于每个 A>=2：每变量只将其 k/2 个负 ports 外放，选在负文字总数不超过 A 的 clauses 中；其他负 ports 内放，正 ports 全内放。固定负出现后，可选 clauses 数是

    sum_{t=0}^{A-1} binom(2A-2,t) >= k/2.

因此可确定性选择。各负轨为 1+1/2，正轨为 1；被外放的 clauses 只可能有至多 A 个负文字，故 clause 负载至多 1。所有原 jobs 均已完整分配。

更强地，取第6节 B=A，得

    OPT_A <= 1+ceil(R_A/d)/k,
    R_A = (d*binom(2A-2,A-1)-k)/2.

闭式由 s*binom(d,s)=d*binom(d-1,s-1) 和二项对称求和得到，也可直接使用定义，不依赖闭式。

令 S 为公平二项随机变量 Bin(d,1/2)，仅作有限和估计而非随机算法。因 A=d/2+1/2，

    E(S-A)_+ <= (1/2) E|S-d/2| <= sqrt(d)/4.

最后一步是 Cauchy-Schwarz，方差为 d/4。R_A=2^d E(S-A)_+，故

    OPT_A <= 1+1/(2*sqrt(d))+1/k -> 1.

任意固定 1<rho<2，选足够大的 A，可同时满足这个上界小于 rho，以及 rho*A<d。此时源连弱阈值 floor(rho*A) 都无解，而实际调度有 C<rho。近二所需的 soundness 因而在这个具体平衡双轨模板中失败。没有将该失败升级为所有多任务码不可能。

## 8. A=3 的完全实际锐证书及下界

A=3,d=5,k=16：42 台机器、165 枚 jobs。所有 selectors 放负轨。每个大小 4 的负文字集合缺一个变量 i，从该 clause 内收变量 (i+1 mod 5) 的 port；在全 5 负的 clause 内收变量 0,1 的两个 ports。除此以外，负 ports 全外放；正 ports 全内放。

总共内收七枚负 ports，每负轨内收数为 [2,2,1,1,1]。负轨负载为 [9/8,9/8,17/16,17/16,17/16]；正轨均为 1。所有 clause 至多三枚负 ports，负载至多 1。因此实际 makespan=9/8。

若有 C<9/8 的任何实际调度，按第6节同构和正轨归一化后，每负轨最多一枚负 port，总共最多五枚；每 clause 外放数不超过 floor(3C)<=3。五个大小4的 clauses 各须至少内收一枚，全5负 clause 须至少内收两枚，总共至少七枚，矛盾。故该完整实际实例 OPT=9/8。源对每个赋值仍有全5真 clause，弱阈值4也无解。


## 9. 实际审计、来源扣除和剩余义务

规范程序与独立构造分别输出原jobs、资格、完整σ和全机负载；具体模型/实现不能互换。完整立方体程序以A生成显式指数规模实例，复杂度按展开后P的总编码长度/输出规模计，**不是按log A多项式**。独立cut oracle只枚举删除网络全部变量侧cuts和所有物理负载breakpoints，不冒称枚举2^(原任务数)份σ。

相同模型的旧provisional 8/5、共同k、异质k_v版本没有重复建账。正式身份只使用本页四个不同合同：归一化scalar、split unit、加权单例外、完整cube精确前沿；后者是前者的特殊族，真实OPT求值另立身份。每个精确Claim、所有前提、实现和有限核验分别登记。

针对性源码祖先为ST1993有序槽；本页的半质量因子和匹配不主张原创。BG2016源近二PCSP并不为具体码提供自动可靠解码，全文/适用范围沿已有manifest和[single-job投影](signed_one_job_port_downset.md)读取。独立审查、冻结全文哈希、实际证书与各程序有限范围见[本次审查](../../reviews/unrelated_machines/dual_rail_threshold_soundness_boundary_review.md)。外审与全球新颖性未认证。

要重新尝试近二归约，必须改变本页仍可全局构造弱调度的明确结构，而不是仅改变源NO阈值、端口数、内部均匀度或scalar/unit容量写法。非归一化跨层负载、相关核心选择或另一外部读出仍须完整YES保持、实际NO源解码与总位多项式证明；本页不排除它们，也未否定一般UM-TARGET-v1。
