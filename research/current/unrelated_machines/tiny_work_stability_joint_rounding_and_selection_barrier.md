# 小任务工作量的单侧稳定：联合槽舍入与证书选择的精确障碍

读取目的：检验“把无限多小任务的影响压缩成稳定工作量，再重用有限大任务槽余量”的算法路线。本文关闭给定稳定证书到真实调度的接口，同时证明从输入寻找这种过强证书不能当作免费步骤。两项限定身份均不解决一般UM-TARGET-v1；全局新颖性与外审未认证。

## 1. 对象与联合槽结论

采用UM-MODEL-v1。输入为合法非负有理/∞矩阵P、有理T≥0、显式有理等式覆盖CONFIG(T)点y。每机器的配置概率和1，每原任务覆盖和1。先把具有某条零边的任务分到该零边，并从所有源配置删除；合并重复配置可选，后续所有任务的有限端均为正。

固定有理δ∈[0,1]与整数K≥1；机器i上p_ij≤δT的边为tiny，其余为big。任务在不同机器上的角色可以不同。每个正权源配置至多K个big任务，tiny数量不限制。定义
τ_i(C)=Σ_(j∈C,tiny) p_ij，r_i=min_(y_iC>0)τ_i(C)，s_i=Σ_C y_iC τ_i(C)，b_i=max_(tiny,x_ij>0)p_ij，空最大值0。
令α_1=1，α_2=3/2，α_3=11/6；K≥4时α_K=2−K^{−(K−1)}。

**UM-TINY-WORK-STABILITY-JOINT-ROUND-v1。** 在给定显式证书的总二进制编码长度的确定性多项式时间内，可以输出一个完整合法调度，所有机器同时满足
L_i≤α_K(T−r_i)+s_i+b_i。                         (1)
若还满足s_i−r_i≤ωT，则
L_i≤(α_K+ω+δ)T。                               (2)
K作为输入时构造次数仍为统一多项式；没有枚举n^K子集或求一般配置LP。

## 2. 全机共同构造与证明

取边际x。每行分别把big边际和tiny边际按实际p非增排序，各自建立标准单位槽，只有区间交长严格正才连边。最后把**全部**槽放入同一二部图，每原任务是一个左顶点，并只运行一次覆盖全部任务的整数匹配。原x给这个图一份任务行和1、槽容量≤1的分数匹配，故Hall保证整数匹配存在。同一任务在不同机器的big/tiny角色没有复制或分别作两个独立决定。

每正权配置删除tiny后，big数≤K、big工作≤T−τ_i(C)≤T−r_i。这些配置的源概率仍和1；因此有限配置基数槽界的逐行证明给big槽完整包络≤α_K(T−r_i)。引用[UM-BOUNDED-CONFIG-CARDINALITY-SLOT-v1正文§2–4](bounded_configuration_cardinality_slot_margin.md)的**逐行**引理；其证明只用本行配置与严格前缀，并不需要删除tiny之后big列本身覆盖1。真正全任务列覆盖由前一段统一匹配负责。若T−r_i=0，则所有big边际为0，包络0。

tiny槽用标准ST前一满槽收费，负载≤s_i+b_i。两个包络对同一匹配逐行相加即(1)。由于α_K≥1、r_i≥0、b_i≤δT，(1)≤α_KT+(s_i−r_i)+δT即(2)。边际求和、源配置投影、排序、严格交长和一次确定性增广匹配全部位多项式。槽总数≤原正边数+2m；极小正质量及大分母不引起按数值循环。无需实际计算巨大K的α_K分母；可按实际正权配置最大big数≤n分析，α_K只出现在保证公式。T0分支由配置可行性只含零负载，被预处理为零调度；空任务、单可用机器和空行都覆盖。

参数必须相容：只按δ阈值自动计数会给K约1/δ，不能把K独立固定再让δ任意小。K1与δ=1/2给(3/2+ω)T；K2用锐α2可在δ>1/3且ω<1/2−δ时给严格次二。下面证明即使tiny可固定得任意小，一侧稳定证书的输入生成仍可能含精确NP选择。

## 3. 单侧稳定证书的选择障碍

**UM-TINY-WORK-STABILITY-SELECTION-NP-v1。** 对每个固定整数ℓ≥2及固定有理0≤ω<1/2，在下面的selector/root/leaf合法实际矩阵族上，判定是否存在等式覆盖CONFIG(1)点y、使各行s_i−r_i≤ω，是NP完全的。此族时间只含{1/ℓ,1}且每配置至多一个big任务。tiny恰为1/ℓ端。

同一受限源族上，稳定证书存在 iff原实例OPT≤1 iff源perfect3DM为YES。因此若P≠NP，没有总确定性位多项式程序能在每个OPT≤1输入上保证给出这种可验证稳定证书；域外允许任意行为。ω=1/2不能纳入上述等价，但本页不判定该端点的复杂度。

**外部依赖。** perfect3DM的NP完全性作为Paper Fact，沿已归档[Karp1972原文](../../../history/source/literature/unrelated_machines/karp_1972_reprinted_2010_reducibility.pdf)及[既有准确定位](joint_matching_completion_and_block_cuts.md#3-um-joint-choice-np-v1即使没有必选大任务也有精确困难)使用；本页不认领新的源复杂度定理。下面的实际矩阵与配置稳定性投影自足重构，不援用旧匹配见证的困难性来替代新对象证明。

**完整矩阵。** 源X,Y,Z等势q，显式triples列表A，a=(x,y,z)。机器为每a的root S_a；每y的B_y、每z的C_z；ℓ>2时每x另有ℓ−2台D_(x,t)。每x一枚selector A_x，在所有含x的S_a上时间1。每a有ℓ枚leaf jobs，均在S_a时间1/ℓ，各自另在B_y、C_z、D_(x,1),…,D_(x,ℓ−2)之一时间1。无其他有限端。加一台idle保证空源合法。源q0直接空YES；存在孤立坐标时直接输出一机两unit任务的固定合法NO，其CONFIG1不可行。否则每selector至少一个合法端，所有leaf总有两个端。
机器数|A|+ℓq+1，任务数q+ℓ|A|，有限边数(2ℓ+1)|A|。ℓ固定，输出为源位长多项式；重复tuple保索引，不影响论证。机器D不存在于ℓ2分支。

## 4. 配置空间的精确投影与稳定性强迫

对任意CONFIG1证书，令z_a是selector A_x分给S_a的边际，s_a为该root的tiny工作。selector覆盖给Σ_(a∋x)z_a=1，因此Σ_a z_a=q。每root期望负载≤1，故Σ_a s_a≤|A|−q。

每a的ℓ个leaf中，root上的总边际质量为ℓs_a，故送unit资源的总质量为ℓ−ℓs_a。全部unit资源只有ℓq台、每台配置期望负载≤1，所以Σ_a s_a≥|A|−q。两侧都紧，因而每root期望负载z_a+s_a=1。非负配置负载≤1，平均等于1迫每个正权root配置负载恰为1。它只能是selector singleton或**全部ℓ枚leaf**，没有其它负载1配置。由此每leaf在root边际精确1−z_a，在自己的unit资源边际精确z_a。

B、C资源容量给Σ_(a∋y)z_a≤1、Σ_(a∋z)z_a≤1；各坐标总和为q，故逐行均等于1。D的每x复制约束与X覆盖相同。于是源z恰为fractional perfect3DM polytope；反向任一此z，都以root两配置概率z_a与1−z_a、unit资源singleton概率z_a构造完整CONFIG1点。这是完整双向投影，不是只检查一份给定证书。

每root的单侧振幅因此恰为
s_a−r_a=0（z_a=0或z_a=1），而z_a∈(0,1)时为1−z_a。
资源行tiny工作恒0。稳定性ω<1/2使任何正z_a都≥1−ω>1/2。每x的z和1，故只可能有一个正项且它等于1。Y、Z和式给全局不交，得到perfect3DM。反向perfect3DM给0/1 z、实际负载1及每行Dirac配置，振幅0。

**实际调度的同源解码。** 负载≤1时每selector选一个不同root，被占root的全部leaf都必须出去，B/C各资源最多一job；得到perfect3DM。反向把所选root的leaf全部外送、未选root全留home，安排全部原任务，负载≤1。q>0时selector保证YES的OPT恰1。没有用未知NO-OPT做decoder阈值。

**NP和promise搜索。** 固定ℓ时root配置为至多ℓ个leaf的子集或一个selector，总列数O(|A|2^ℓ+ℓ|A|+m)；unit资源只需singleton/empty。猜每行r_i∈{0,1/ℓ,…,1}，保留τ≥r_i的列并加s_i≤r_i+ω，形成显式有理LP。若非空有多项式位长基本解；其真实min≥猜r，故确满足所需单侧界。反之原证书可猜其真实min。验证显式y只需有理运算，故在NP。对保证YES输出证书的总多项式B，在归约输入运行并验证：YES必接受、NO根本无稳定证书；即可判3DM。只说“承诺实例最终停机”不够，须有总多项式界。

## 5. 半端点的完整实际NO见证

q2的parity triples：X=Y=Z={0,1}，A={(x,y,z):z=x xor y}。任意两tuple都相交，故无perfect匹配。取四个z_a=1/2：每坐标有两个incident triples，其和1；root以1/2选selector、1/2选全leaf，所有unit资源以1/2 singleton填满。完整CONFIG1成立且root振幅精确1/2，资源振幅0。

实际OPT精确1+1/ℓ：源无perfect匹配说明OPT>1，而全部负载为1/ℓ格点，所以OPT≥1+1/ℓ。将两个selectors放到(x,y,z)=(0,0,0),(1,0,1)的roots；其它root全leaf留home。两个selected roots各外送全部leaf，但共享B_0的两枚leaf只外送一枚、另一枚留其root。C端不同，D端按x不同，故全部其它外送job各自unit机无冲突；最大负载1+1/ℓ。这付清全部原jobs而非仅选中一层。该端点反例不证明omega>=1/2时容易，也不产生近二困难性。

## 6. 同一矩阵的真实峰值只有三个等级

**UM-SELECTOR-TINY-ROOT-THREE-VALUES-v1。** 这是不同于稳定证书搜索的新范围恒等式。限上面的主构造q>0且每x至少有一tuple；固定NO映射与空源另按其原分支处理。给定源构造呈现，令ν为最大3DM大小，令μ为二部图H=X—(Y∪Z)的最大匹配数；x与资源u相邻当且仅当某原tuple同时含x和u，边保留tuple见证。则完整原矩阵满足

| 源状态 | 真实OPT |
| --- | --- |
| ν=q | 1 |
| ν<q且μ=q | 1+1/ℓ |
| μ<q | 1+2/ℓ |

第1行已证。任意实际C<1+1/ℓ使每个selector占用root的全部leaf都外送，得到perfect3DM，给第2行的下界。任意C<1+2/ℓ≤2则每资源至多一unit；每个selector所占root至少有一枚B/C leaf外送（否则这两枚留home就已超阈值）。各x取一条这样的实际外送端，得到覆盖X的H匹配。因此μ<q时有第三行下界。两个decoder都扫描任意完整实际assignment，使用可计算的绝对阈值，不输入未知OPT，也不规范其它原job。

若μ=q，对每个匹配x→u取其原tuple a(x)，把selector放到S_a(x)，外送该root全部D叶与所匹配的一枚B/C叶，另一枚B/C叶留下；未选roots全部leaf留home。D按x tag不同，Y/Z目的资源由同一全局匹配互斥，全部原job负载≤1+1/ℓ。若无该匹配，仍可每x任选一个tuple，仅外送其全部D叶，两个B/C叶留root，全部负载≤1+2/ℓ。这给两个对应上界；ℓ2时D为空也成立。

构造H并普通匹配及映回全jobs为确定性位多项式；源呈现是上述算法输入的一部分，不另声称从未标记raw矩阵识别该模板。若CONFIG1可行，其fractional3DM z在H上沿x→y和x→z各送z_a/2，x行和1、Y/Z列和1/2，故μ=q。于是**同一证书选择很难的族，在CONFIG1可行时无需稳定证书便能输出≤1+1/ℓ**；按μ选择上述两个构造，整个已呈现族还有(1+1/ℓ)实际近似。没有判定ν=q的多项式算法，这仍保留精确NP困难性。

此三值结论由hardness_decoder在其B独立稿冻结后单独推导；root随后逐阈值重构并实际读稿。两个阶段不能倒记为root只看该三值Exact的盲审。独立的后置证明知情攻击单独记录。

## 7. 准确状态与可回收义务

(1)给完整显式稳定点到实际全机输出的条件桥，支持无限tiny与混合角色；选择障碍说明把此点的生成当LP/匹配是错误。它不否定改变证书、允许更宽松tiny结构、联合利用实际槽损失、重开边或一般(2−eps)算法。特别是本源的半端点NO最优为1+1/ℓ，会随tiny缩小接近1而非2。

所有一般性结论由以上证明承担，有限Fraction审计只核声明参数与对象。A与B的声明先行独立重构、实际作者读后及最终全文读稿分别记录；三值恒等式的作者及证明知情审查另分清。给定点构造已实现，稳定证书生成器未实现；相关范围见[实际审查](../../reviews/unrelated_machines/tiny_work_stability_and_selection_review.md)。[构造器](../../../tests/audits/unrelated_machines/tiny_work_stability_joint_rounding.py)复用既有ST匹配；[独立原矩阵审计](../../../tests/audits/unrelated_machines/tiny_work_stability_selection_audit.py)不导入构造器。没有一般近二算法或困难性结论，UM-TARGET-v1仍OPEN。
