# Q_D到有界状态叶重数私有树的单向低峰解码障碍

本页是1766批内反馈产生的新数学比较草稿，未申请对象ID、未登记、未改既有三条边或覆盖收据。所需输入已在本轮重新实读：Q_D的整数鸽巢上下界、完整flat UM双向值桥、逐原job的CONFIG(1)证书，以及v3有界完整state叶重数模型、全阈值存在界和全原任务回填。本页不重跑有限程序。全部引用绑定文末完整文件SHA与唯一章节。

## 精确加强结论

固定整数μ₀≥1。对每个整数D≥2，令Q_D为既有显式norm1菜单，P_D为它的**完整flat普通UM编译**，不是state-dummy SC实例，也不是仅保所选state的子实例。若

\[
D>\mu_0+2,
\]

则不存在一个有限普通UM实例P_D′同时满足以下三个条件：

1. P_D′完全属于v3的私有均匀满树结构，且每个完整state对每台真实外机的叶逆像重数至多μ₀。
2. P_D′的通常、全原job的CONFIG(1)可行。
3. \(\operatorname{OPT}(P_D)\le\operatorname{OPT}(P_D′)\)。

因此，连以下更贴近低峰迁移的弱合同也不可能：**只对每份峰值严格小于2的P_D′完整实际调度，要求存在一份峰不增的回源完整解码**。不要求解码任何高峰输出，也不要求正向实际映射、正向OPT保持、双向等价、计算性或复杂性假设，甚至无需存在一个可计算的实例变换。因为v3在T=1保证的见证有峰≤2−r₀/d<2，这个弱合同仍必然覆盖矛盾所需的见证。覆盖所有目标实际调度的合同当然也被排除。

更窄地说，矛盾只需条件3在**一份由v3保证存在的低峰目标调度**上成立；没有必要要求解码覆盖目标的所有实际调度。

## P_D的完整定义与整数实际值

资源为互异的g_(a,j)，a,j∈[D]，以及A_a，a∈[D]。main group有D个indexed states；第a态的支持是该行D个g_(a,j)，每项权1/D。每个(a,j)另有一个helper group，两个states分别是unit singleton g_(a,j)和unit singleton A_a。全部groups非空、全部states总权恰1。[Q1]

菜单实际值V_D定义为：每group选一个原state，在其正支撑中领取任意部分真实资源；跨group领取不交；最大化所有group所领权重的最小值。

**上界。** 考察任意最小group值严格为正的真实分配。main实际选某一行a，若领取r个该行g，则相应r个helper都失去自己的g。各helper仅有singleton可选，保持正值就必须各自取得同一个真实资源A_a。不可分资源只能给一个helper，故r≤1，main值≤1/D。若某group值为0，整体值已≤1/D，所以上界覆盖全部实际分配。

**达到。** main取第1态并只领g_(1,1)；该helper领A_1，其他全部helpers各领自己的g。全部资源领取不交，main值1/D、全部helper值1，故

\[
V_D=1/D.
\tag{1}
\]

P_D的机器是每state独立的private机及每真实资源独立的resource机。每group一枚unit selector，可去该group的任一private机。每个原state-resource incidence是一枚不同job，只能在自己的private机耗时该项权重，或在其真实资源机耗时1。所有未选态的incidence jobs也保留。[Q2a,Q2b]

从达到(1)的资源分配构造完整调度：selector置于所选state；仅所选bundle对应的incidence导出；其余incidences——包括全部未选态jobs——均留原private机。所选private负载2−group value，未选private负载1，资源机至多一枚unit。因此峰≤2−1/D。

反向，任取P_D的完整调度且峰C<2。每资源机至多一枚unit incidence。按每个selector的实际目的地读取其选中state的真实exports，各group的exports不交；该state的private总工作量原为1，所以导出价值恰为2−该private负载，至少2−C。由(1)，2−C≤1/D，故C≥2−1/D。C≥2的调度当然也满足同一下界。于是

\[
\boxed{\operatorname{OPT}(P_D)=2-1/D.}
\tag{2}
\]

这里的C<2仅用于反向资源独占，C≥2已单列；没有把部分资源领取当成完整调度，也没有删除未选态任务。[Q2a,Q2b]

## 源CONFIG(1)确实覆盖完整原任务

令main每态概率λ=1/D。每个helper在g-singleton态取概率1−1/D，在A-singleton态取概率1/D。每真实g资源的正支撑占用为

\[
1/D+(1-1/D)=1;
\]

每A_a资源的占用为D·(1/D)=1。故这是一份共同正支撑FSLP证书，不是按private权加权的容量松弛。[Q1,Q3]

将它直接展开为P_D的有限机器配置：

- 每个state private机，以λ取本group的selector，以1−λ取该state**全部**incidence jobs。
- 每枚incidence在对应unit资源机以λ取singleton配置；该资源全部singleton概率之和恰1。

每个private配置负载≤1，每台机器的配置概率和1；每个selector跨其所有state的覆盖和1。对每枚incidence，不论它在某个整数选择中会否属于未选state，private覆盖1−λ加resource覆盖λ恰为1。原Q_D没有零权incidence；一般桥允许零项时，还会把全部zero-private jobs加入selector配置，使它们仍覆盖1。[Q3]

所以CONFIG(1)可行是完整原P_D的真实配置证书；非空unit selector又使CONFIG(T<1)不可行，因此T_conf(P_D)=1。其完整显式规模为D²+1 groups、2D²+D states、3D² incidences、D²+D资源；不存在把D²个原helper或未选state藏掉的步骤。源CONFIG(1)本身并非下述数值矛盾所需的额外前提，但它保证本族确实检验“保CONFIG(1)的结构编译”这一接口。

## v3目标域与低峰见证

条件1中的v3域完整要求：[T1]

- 有整数d,h≥1、非空有限root集合和每root非空有限显式state菜单；d,h及menus均可随D任意变化。
- 每state是完全私有满d叉高h树，不同state、不同root的内部机器均互不共享。
- 每root恰一枚selector，全部可用端为本root各state树根，时间1。
- 每内部edge job只有父端1/d与唯一child端1；每leaf job只有父端1/d与由该state显式leafmap指定的唯一外机端1；其他端∞。
- 没有其他jobs、preloads、加工时间或额外有限资格。全部原state、枝和job均真实存在，必须执行。
- 对每完整state及真实外机z，|f_us^−1(z)|≤μ₀。该上界不限制跨state/root的总共享重数；外机仍可任意跨state/root共享。
- CONFIG(1)对每台机器取负载≤1配置、配置质量和1，每个原job恰覆盖1；向下封闭下“至少覆盖”可规范成该形式。

由v3 B取T=1，有s=0、a=d。令

\[
r_0=\left\lceil\frac d{\mu_0+2}\right\rceil.
\]

v3的rainbow blocker、同一共同λ容量及Haxell条件保证一份**完整原P_D′**实际调度σ′，使

\[
C_{\max}(\sigma′)\le2-r_0/d
\le2-1/(\mu_0+2)=:\alpha_{\mu_0}.
\tag{3}
\]

v3回填明确包含全部未选/零λ states及未选原d-branches；活跃内部机负载1+(d−r₀)/d，非活跃内部机全部d个small父置负载1，外机至多一枚unit。辅助a-tree或超边不是新增/删减的物理任务。[T2,T3]

Haxell在此只给有限存在性；辅助族可指数大，不影响存在性矛盾。既不要求多项式求出σ′，也不假设目标配置点本来就是整数联合调度law。

## 最小前提的矛盾证明

由条件3、(2)与(3)，

\[
2-1/D=\operatorname{OPT}(P_D)
\le\operatorname{OPT}(P_D′)
\le2-1/(\mu_0+2).
\tag{4}
\]

但D>μ₀+2等价于1/D<1/(μ₀+2)，与(4)矛盾。严格差为

\[
\Delta(D,\mu_0)=\frac1{\mu_0+2}-\frac1D>0.
\tag{5}
\]

若仅从“每份峰<2的目标完整实际调度存在峰不增完整解码”出发，(3)的σ′由于r₀≥1、d≥1而确实有峰≤2−r₀/d<2，故已经处于该弱解码域。将弱条件只应用于这份σ′，就会在P_D产生峰≤α_(μ₀)的完整调度，直接违反(2)。无需解码峰≥2的任何输出。这是对存在性的否定，强于否定一个多项式实现。

对有限、非空合法UM实例，峰不增的非算法解码关系

\[
\forall\sigma′\in\mathcal S(P_D′)\ \exists\sigma\in\mathcal S(P_D):
C(\sigma)\le C(\sigma′)
\]

与OPT(P_D)≤OPT(P_D′)本来等价：正向取一份目标最优调度；反向对每σ′统一选择一份源最优调度即可。此等价不声称该固定源最优调度可计算或已给出。进一步，在本页目标域及CONFIG(1)前提下，目标最优值由(3)严格小于2，所以把左侧量词仅限制到C(σ′)<2仍与同一OPT不等式等价：取目标最优解即得正向，反向仍可统一选源最优解。因而本页没有隐藏要求高峰解码或比条件3更强的合同。

## 更精确的参数必要条件与边界

若允许每D的重数上界μ(D)变化，则任何满足目标结构、CONFIG(1)及单向OPT不增关系的候选至少必须满足

\[
\boxed{\mu(D)\ge D-2.}
\tag{6}
\]

可取μ(D)为目标完整state的实际最大叶资源重数，所以(6)不是说“声明一个很松的上界”就足够；实际最大重数也必须通过此必要条件。它仅是必要条件，不宣称μ=D−2可构造、更不宣称v3上界锐。

保留d的取整还能加强为

\[
\boxed{D\left\lceil\frac d{\mu+2}\right\rceil\le d.}
\tag{7}
\]

因此d≥D也是必要条件。特别地，若把目标分叉数固定为d₀，则D>d₀的Q_D不可能满足本页三条件，**即便允许实际叶重数μ随D任意增长**；这是r=1始终为v3合法参数所给的低峰界2−1/d₀，仍只在本页精确v3目标结构内成立。若D=μ+2，(7)进一步要求D整除d；若D不整除d，即使粗常数界恰取等号，默认r₀的取整仍给严格矛盾。D=μ+2且D|d时，本页的粗界没有产生矛盾；不能把“未排除”写成“存在”或“边界锐”。

还可使用v3的全部允许r而不局限默认r₀。设

\[
\mathcal R(d,h,\mu)=\{r\in\{1,\ldots,d\}:\quad
\mu(r-1)<d,\ [d-\mu(r-1)]^h\ge2r^h-1\}.
\]

集合至少含r=1。若R=max𝓡，则同样必要的是D·R≤d；只要存在一个允许r满足D·r>d，单向解码已矛盾。这是直接保留既有v3数值条件，没有求该条件的精确最优性。

若放宽解码为C(σ)≤C(σ′)+η，则必要η≥Δ(D,μ)；放宽为乘性ρ，则必要ρ≥(2−1/D)/(2−1/(μ+2))。这些是从现有上界导出的必要损失，不宣称达到。若目标仅有CONFIG(T_D)可行，只有在α_μT_D<2−1/D时本页同一数值论证仍矛盾；不能把CONFIG(1)免费换成任意较高阈值。

## 不被本结论排除的模型及准确用途

以下改变不由本页排除，也不因此被证明可行：

- 实际完整state叶重数随D增长并至少不被(6)、(7)等必要条件排除；无界μ本身不是充分构造。
- 共享内部机器、非均匀父端时间或不同树的异构分叉/高度、leaf多单位外端、selector资格或时间改变。
- 额外原jobs、preloads、额外有限端，或其他离开v3精确结构的改动。
- 不保持目标CONFIG(1)，或使用显式不同的负载尺度并支付相应峰值损失。
- 允许足够大的加性/乘性解码损失、只对不含(3)见证的受限目标输出集合解码、或完全改变原任务目标。

跨state/root共享**外机**、任意多个roots或state菜单、增大d/h、重新编号外资源、非算法/指数规模的实例变换，以及不要求正向OPT保持，都仍在本否定范围内，不能单独用作避开(4)的方法。空root若另允许则目标OPT0，同样不可能满足对P_D的条件3。

这不是一般UM hardness或不可近似性：Q_D是已显式求出值的易描述族，结论只否定一类结构编译及其单向低峰解码。它也不否定既有norm1菜单的tree/menu-port/SC路径正规化N。binary-selector-tree的**图上分支数2，不等于v3统一父端时间1/d中的d=2**。N在每个菜单顶点建立自己的group/unit selector，带有own/child-own等unit singleton态和原payload态，随后还接menu-port资源路径；其处理时间、selector数量和共享port资源的任务角色均未满足“每root一枚unit selector、全部树edge父端恰同一1/d、内部child端1、内部机完全私有、无其它任务”的整体v3合同。不能只从树形图外观把N(Q_D)判成d=2的v3实例；N未声称将所有Q_D映入本页固定μ₀或固定d₀的目标类。[Q4,Q2a]

**建议：具有独立复用价值。** 它把“必须同时保实际值”的较强笼统障碍，收紧为一个可审计的单向OPT/低峰解码不可能性，并给出实际重数必须至少线性增长的必要条件。适合作为单独的精确obstruction目标：其前提应同时引用Q_D的完整整数实际值和v3有界重数CONFIG存在界，保ALL；source CONFIG完整证书可作适用接口的承重证据，但不冒作数值矛盾不可缺的逻辑前提。本页未申请或假造稳定ID，也未新增图边/登记。

## 精确证据引用

| 标记 | path | 完整文件SHA256 | 唯一section |
|---|---|---|---|
| Q1 | archives/unrelated-machines/state/定理/规范化平菜单的CONFIG与正支撑LP双向保持--定理.md | 8bfbaa80b98546b6d1320e9760bb9491165e26a6cef1b6cd35eb86116c822f66 | 5. 自足的 (Q_D) 障碍与规模 |
| Q2a | archives/unrelated-machines/state/资料/加权菜单Santa值桥与不相关机转换--资料.md | d01ac63a4da47c8cfaed8ed296efa00ea4b375ef8b567c0338c938d6d175aa8c | 精确模型 |
| Q2b | archives/unrelated-machines/state/资料/加权菜单Santa值桥与不相关机转换--资料.md | d01ac63a4da47c8cfaed8ed296efa00ea4b375ef8b567c0338c938d6d175aa8c | 双向转换与公式 |
| Q3 | archives/unrelated-machines/state/定理/规范化平菜单的CONFIG与正支撑LP双向保持--定理.md | 8bfbaa80b98546b6d1320e9760bb9491165e26a6cef1b6cd35eb86116c822f66 | 1. 平坦不相关机与 FSLP 的双向证书 |
| Q4 | archives/unrelated-machines/state/审查/归一化CONFIG有限证书三向桥的v3审读范围--审查.md | 2ee2f04fa427e1889073c25daaab373a8d4042f633aa78ca0fd76df80d9e996b | FSLP、完整machine CONFIG(1)与normalform |
| T1 | archives/unrelated-machines/state/定理/私有菜单树有界叶重数配置界--定理.md | 5b810c65140f9581fb362f8ff739b09f019a7c435a1bc2eb3d7a34d42c3041d3 | Objects / Domain / Quantifiers / Assumptions |
| T2 | archives/unrelated-machines/state/定理/私有菜单树有界叶重数配置界--定理.md | 5b810c65140f9581fb362f8ff739b09f019a7c435a1bc2eb3d7a34d42c3041d3 | B. 全部 CONFIG(T) 阈值与配置整数间隙 |
| T3 | archives/unrelated-machines/state/定理/私有菜单树有界叶重数配置界--定理.md | 5b810c65140f9581fb362f8ff739b09f019a7c435a1bc2eb3d7a34d42c3041d3 | 5. 完整原 P 的实际调度 |
| T4 | archives/unrelated-machines/state/定理/私有菜单树有界叶重数配置界--定理.md | 5b810c65140f9581fb362f8ff739b09f019a7c435a1bc2eb3d7a34d42c3041d3 | 6. 默认 r 与全配置整数间隙 |
