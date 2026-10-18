# 稀释的共享终端实例：raw K2 的真实锐二倍间隙

Claim ID：`UM-DILUTED-SHARED-TERMINAL-RAW-K2-GAP-v1`。

本文给出普通 unrelated machines 的显式有理实例和共同四次矩证书。结论针对本文精确定义的 raw K2：逐机完整配置分布只共享 first/pair，加全局 M2 及全部仿射负载局部化。它把真实整数最优与这个强化下界的间隙推进到锐值2；不是计算困难性，也不包含 canonical native C2、joint-CONFIG-M2 或更强条件容量系统的间隙断言。

作者 Exact 与 Proof 分开冻结，独立审者先只读 Exact 重构，再在 root 实际全文读该记录后读作者 Proof。root 已实际全文读全部这些来源、本稿及有限审计代码，并在新目录精确重放局部输出。最终正文的实际复核和未检查范围另见[独立审查](../../reviews/unrelated_machines/diluted_shared_terminal_raw_k2_gap_review.md)。证明、审查、有限软件、外审和新颖性分别登记；一般主目标及反面仍 OPEN。

## 1. 对象、量词与结论

每个整数 k>=2 对应一个完整普通 UM 输入 P_k。定义

    L=2k^2,
    M=1+60Lk^4=1+120k^6,
    a=1/M,
    T0=1+1/k.

以下三项同时成立。

1. 真实最优值恰为 OPT(P_k)=2-floor(sqrt(k))/k。
2. 第3节的 raw K2 系统在目标 T0 有显式有理证书。它使用同一个全局四次矩泛函、M2 PSD、每台原机器的完整 CONFIG 分布及 first/pair 一致性、以及涉及全部原变量的每个全局 affine load localizer。
3. 证书的全部四次矩表、各机器配置列表与 localizer 矩阵均可在显式输入总位长的多项式时间和总输出位长内生成。这里是指定证书的生成结论，没有断言一般 SDP 精确可行性可在总位多项式时间求解。

将所有有限处理时间乘以 k/(k+1)，可得到目标一的同类证书，而真实最优为

    (2-floor(sqrt(k))/k)/(1+1/k) -> 2.

结合第10节的标准二倍舍入上界，这个 raw 系统相对真实最优的全类间隙上确界恰为2。本文不求出每个 P_k 的 raw 可行阈值，也不把证书当成实际目标一的 schedule。

## 2. 全部原机器、原 jobs 与处理矩阵

有 M 个组件。组件 i 有一台 U_i，L 台 B_i,b（b∈[L]），以及 k 台 Z_i,t（t∈[k]）。所有类型和所有不同下标均为物理不同的原机器。

全部原 jobs 如下；未列端点的处理时间为 infinity。

| 原 job | 全部有限端点与时间 |
|---|---|
| 单个 selector h | 每个 U_i，时间1 |
| 每个 i∈[M],j∈[k] 的 f_i,j | U_i 上时间1/k；每个 B_i,b 上时间1 |
| 每个 i∈[M],b∈[L],ell∈[k] 的 e_i,b,ell | B_i,b 上时间1/k；每个 Z_i,t 上时间1 |

所有 jobs 独立、不可分割，并须恰好执行一次。没有忽略未选中组件的 jobs，也没有把同一个原 job 拆成多个副本。输入不带源赋值、好配置或可行解 oracle。

机器数为 M(1+L+k)，job 数为 1+Mk(1+L)，有限端点数为

    E=M+Mk(1+L)+MLk(1+k).

这里完整描述全部有限端点与其二进制有理时间；按 UM-TARGET-v1 的完整矩阵输入时，另逐项写出全部 infinity 单元，m乘n亦为k的固定次多项式。有限端点记数只用于界定矩证书大小，不采用succinct输入。其大小可为 k 的较高次多项式；生成和位复杂度均相对这个显式展开输入，不相对 log k 承诺紧凑输出。

## 3. raw K2 的精确定义

对每个原有限端点设置 Boolean 变量 x_j,v。F 是全部次数至多4多项式上的共同线性泛函，F(1)=1。M2 以次数至多2的单项式为索引，条目为 F(pq)，要求 PSD。

施加原 job 的四次商关系：

- x^2-x=0，以及同一 job 两个不同端点的 xx'=0，各乘任意次数至多2的单项式；
- sum_v x_j,v-1=0，乘任意次数至多3的单项式。

每台原机器 v 有一个完整 CONFIG(T) 分布。其支持是该机器上原 eligible jobs 的子集，处理时间总和至多T，包括允许的空配置。这个分布的每个端点 first moment 及每对同机端点的 pair moment 分别等于 F(x)、F(xx')。全局不同机器之间的矩仍来自同一个 F；不要求不同机器的 CONFIG 分布共同来自一个合法全局 schedule law。

此外，对每台原机器 v，令 load_v=sum_j p_j,v x_j,v。对所有涉及整个输入全部有限端点的 affine 多项式 q，要求

    F[(T-load_v)q^2]>=0.

这等价于该机器的全局 affine load-localizer 矩阵 PSD；其条目用到至多三次矩，均在同一四次泛函中。

本定义没有 export<=activation、inactive-all-home 或精确 active-tail 数量等额外限制。本文证书确实含 inactive exports。那些限制可以定义更强的系统，但不能作为本 raw 系统的隐含条件。对固定目标，本文生成的是一个有限有理证书，没有使用 CONFIG 可行性 oracle。 本定义也没有把每个机器配置的选择另设为共同 Boolean 变量 Lambda_C，并对 x=sum_{C含x}Lambda_C 施加全四次 links；这样的 joint-CONFIG-M2 是另一更强合同，本文不声称满足。

## 4. 真实最优值：对每个完整实际 schedule 的上下界

令 s=floor(sqrt(k))。考虑任一 makespan T<2 的实际 schedule。h 必在某台 U_i 执行。该行至多保留 floor(k(T-1)) 个原 f jobs，因此至少

    r=k-floor(k(T-1))

个 f jobs 必须作为 unit 在该组件的 B 机器执行。它们占用不同 B，因为两个 unit 的负载是2。每个已被 unit 占用的 B 同理至少把 r 个原 e jobs 送到该组件的终端。k 台原终端各至多收一个 unit，所以

    r^2<=k.

于是 r<=s，进而 T>=2-s/k。T>=2 的 schedule 也满足这个下界。

上界是完整赋值：任选组件 i，在 U_i 执行 h；选 s 个 f jobs，送到 s 个不同 B；每个所选 B 送出 s 个 e jobs，使用跨这些 B 互异的 s^2 个终端。因为 s^2<=k，这可执行。所有其他原 f/e jobs，包括所有未选中组件的 jobs，都留在各自 tiny home。所选 U/B 的负载为 1+(k-s)/k，其他 home 行至多1，终端至多1。这证明真实最优恰为2-s/k。

近二下界来自每个实际完整赋值都必须满足的共享原终端容量 r^2<=k，而不是从某个矩法则恰好含有坏支持点推断出来。

## 5. 一个共同的有限全局矩法则

均匀选择 I∈[M]，将 h 放在 U_I。条件于 I，各组件独立；选中组件使用 H，其余组件使用 Q。每个样本都是全部原 jobs 的完整赋值。

H：均匀选择 injection sigma:[k]->[L]，把每个 f_i,j 放到 B_i,sigma(j)，全部 e jobs 留在 home。U_i 因而只有 h；恰有 k 台 B 同时有一个 unit f 与完整 tiny payload，负载2。

Q：以下三类互斥，概率总和为1。

- 概率1/2：全部 f/e jobs 留在 tiny home。
- 概率1/4：均匀选 (j,b)∈[k]×[L]，把 f_i,j 放到 B_i,b，其余 f 留 home；均匀选 [k] 的 bijection pi，把该 B 的全部 e_i,b,ell 放到 Z_i,pi(ell)；其余 e 留 home。
- 概率1/4：均匀选 (b,ell,t)∈[L]×[k]×[k]，仅把 e_i,b,ell 放到 Z_i,t，其余 f/e 全部留 home。

Q 的每个样本在每台机器上的实际负载至多1。H 的 U/终端负载至多1，B 负载为1或2。令 F(p)=E[p]。原 job 的 Boolean/one-hot 商关系在每个样本成立，故四次等式成立；M2 PSD 由 F(q^2)=E[q^2]>=0 直接成立。实际上这个共同有限赋值法则可延出任意阶 PSD 矩；这不等于声称更高阶 load localizers 或更高阶同机 CONFIG 一致性也成立。

## 6. 所有机器的完整 CONFIG first/pair 一致性

U_i 的实际行边际已经合法：h 单独执行的概率 a；每个恰缺 f_i,j 的 k-1-home 配置概率 (1-a)/(4k)；全部 k 个 f home 的配置概率 3(1-a)/4。所有这些配置负载至多1。

固定一台 B_i,b。记它的原 incoming-unit 指示变量为 R_j（j∈[k]），原 e-home 指示变量为 Y_ell。令

    p=ak/L, b0=c0=(1-a)/(4L).

全局矩法则在此行的边际是：unit 加全部 k 个 home 的总概率 p；unit 加0个 home 的概率 b0；无 unit 加恰 k-1 个 home 的概率 c0；无 unit 加全部 home 的其余概率。unit label 与 omitted-home label 各均匀。故 distinct-label first/pair 为

    F(R_j)=(p+b0)/k,
    F(Y_ell)=1-b0-c0/k,
    F(R_jR_j')=0                     (j!=j'),
    F(R_jY_ell)=p/k,
    F(Y_ell Y_ell')=1-b0-2c0/k       (ell!=ell').

diagonal 由 Boolean first 给出。

用以下五类合法配置代替这个行边际，仅要求 first/pair 相同。unit label 均匀；单个 home 的 label 独立均匀；恰遗漏一个 home 时 omitted label 均匀。

| 合法配置类型 | 总概率 |
|---|---:|
| 一个 unit 加一个 home e | kp |
| 一个 unit，无 home e | b0-(k-1)p |
| 无 unit，无 home e | p |
| 无 unit，恰 k-1 个 home e | c0-kp |
| 无 unit，全部 k 个 home e | 1-b0-c0+(k-2)p |

它们总和为1。第二、四行的非负性等价于 M-1>=4k(k-1) 及 M-1>=4k^2，由 M-1=60Lk^4 保证；最后一行至少为1-b0-c0>0。每个 unit 配置至多加一个时间1/k的 home，负载至多T0，其他配置至多1。直接代入给出上述全部 first/pair；例如第一类对每个 R_jY_ell 贡献 kp/k^2=p/k。这里没有要求 triples 一致。

每个终端的全局行边际是空或单个原 e-unit，已经合法。它的 Lk 个原 incoming endpoints 各有 singleton 概率

    (1-a)(k+1)/(4Lk^2),

其余概率为空；同机 distinct pair 全零。以上覆盖全部原机器。

## 7. 两个定量单组引理

固定某组件的一台 B。令 g=T0-load_B，tau=1/k。Q 下 g>=1/k；H 下

    g=tau-1{该B被injection选中},
    E_H g=tau-k/L=1/(2k)=mu>0,
    |g|<=1.

用所有 f/e 的 nonhome-head 变量分别记为 F_jb、G_b,ell,t。原 home 变量可由原 job one-hot 线性消去。因此任意单组 affine 表达式可写成

    q=beta+sum c_jb F_jb+sum d_b,ell,t G_b,ell,t.

记 ||c||^2=sum c_jb^2。以下界对任意 beta、d 一致成立：

    E_Q q^2 >= ||c||^2/(30Lk^3),
    E_H[gq^2] >= -2||c||^2.                                (7.1)

第二条中的 beta 可以与第一条不同。这允许稍后分别吸收任意全局条件均值。

证明第一条：令 q0=beta；qN_b,ell,t=beta+d_b,ell,t 是单 e-export 状态中的值；qF_jb,pi=beta+c_jb+sum_ell d_b,ell,pi(ell) 是单 f-export 状态中的值。逐状态恒等式为

    c_jb=qF_jb,pi-sum_ell qN_b,ell,pi(ell)+(k-1)q0.

用三项平方界及 (sum_ell qN)^2<=k sum_ell qN^2，平均 pi 并求和 j,b，得到

    ||c||^2 <=3 sum_(j,b) E_pi qF_jb,pi^2
               +3k sum_(b,ell,t) qN_b,ell,t^2
               +3kL(k-1)^2 q0^2.

Q 三类的权重分别控制：第一求和不超过4kL E_Qq^2，第二个噪声求和不超过4Lk^2 E_Qq^2，q0^2不超过2 E_Qq^2。故

    ||c||^2 <=(12kL+12Lk^3+6kL(k-1)^2)E_Qq^2
              <=30Lk^3 E_Qq^2.

证明第二条：H 下全部 G=0。令 S=sum_j c_j,sigma(j)，则不需 injection labels 独立便有

    E_H S^2 <=k E_H sum_j c_j,sigma(j)^2=(k/L)||c||^2.

对任意 beta 配方，并用 |g|<=1、Cauchy-Schwarz 及 mu>0，

    E_H[g(beta+S)^2]
      >=E_H[gS^2]-(E_H[gS])^2/mu
      >=-(1+1/mu)E_H S^2
      >=-(1+2k)(k/L)||c||^2
      >=-2||c||^2.

所有常数仅依 k,L，没有隐藏的 M 相关最小特征值或维数界。

## 8. 跨全部组件的 affine load localizers

令 q 为涉及全输入全部原端点的任意 affine 多项式。线性消去各 home 后，q 是常数、selector one-hot 变量 A_h=1{I=h} 的线性组合以及各组件表达式之和。

固定组件 i 的一台 B，并条件化 I=h。各组件独立。把每个 j!=i 的表达式减去其条件均值；这些 centered 项与组件 i 独立，彼此独立，条件均值零。把所有被减掉的条件均值连同 selector 系数吸收到数 beta_h。beta_h 可任意依赖 h；原 selector one-hot 正好允许这种条件 offset。于是精确等式为

    E[gq^2 | I=h]
      =E[g(beta_h+q_i)^2 | I=h]
         +E[g | I=h] sum_(j!=i) Var(q_j | I=h).             (8.1)

当 h=i，E[g|I=h]=mu>0；当 h!=i，该均值至少1/k。故方差项始终非负，丢去不影响下界。这一步没有按全局变量数或组件数收取误差。

h!=i 时用 Q 的逐点 slack 及(7.1)，对每个任意 beta_h 分别有

    E_Q[g(beta_h+q_i)^2]>=||c||^2/(30Lk^4).

h=i 时用 H 的第二个界，至少为 -2||c||^2。selector 平均后，

    F[gq^2]>=((1-a)/(30Lk^4)-2a)||c||^2=0,

因为 M-1=60Lk^4。这证明 B 的每个全局 affine localizer，包括 q 同时涉及任意多个其他组件和全部 selector endpoints 的情形。c=0 也由同式覆盖。

U 与终端在每个全局法则样本中的负载均至多1，故它们的 g>=1/k 逐点成立，全部全局 affine localizers 自动非负。至此所有原机器均已核对。

## 9. 有限证书与总位多项式生成

E 个 finite endpoints 的次数至多4单项式有 O(E^4) 个。home 指示可展开成 one-hot complement，每次最多四个因子，展开项数为 E 的固定次多项式。重复端点用 Boolean 化简，同 job 不同端点的乘积为零。

对 nonhome-head 单项式条件化 I；涉及的组件独立。H 下出现 e head 即零；r<=4 个不同 f jobs 的指定互异 B heads 的概率是 1/(L)_r，冲突则零。Q 下至多有一个不同 f head：若有，只有它所选 B 的 e heads 能出现，概率为1/(4kL)乘以至多四个 e heads 的 partial-permutation 概率1/(k)_s。没有 f head 时，Q 的 f-export 类对同一 B 的合法 partial-permutation e heads 贡献1/(4L)乘1/(k)_s；单 e-export 类只对一个不同 e head 贡献1/(4Lk^2)。空单项式为1；无法容纳的 r,s 情形为零。selector endpoint 要么指定唯一 I 并乘1/M，要么未出现而对 M 个 I 求和。

这些规则给出全部四次矩的确定性有理运算算法。相关 falling factorial 的阶至多4；分子分母及求和结果的位数均为显式输入长度的多项式。无需列举指数多个 injection、permutation 或全局独立样本。即使考虑完整有限法则，各单样本有理概率的位长也为输入长度的多项式。

每台 U 的 CONFIG 列表至多 k+2 项；每台 B 展开 uniform labels 后至多 k^2+2k+2 项；每个终端至多 Lk+1 项。全部概率公式显式，非负性和总和已证。M2 有 O(E^4) 个条目；各机器 affine localizer 有 O(E^2) 个条目，由已生成的同一矩表计算。整个证书输出和总位成本为输入长度的多项式。这个存在及生成证明不需要一般 CONFIG 或 SDP oracle。

## 10. 缩放与全类二倍上界

乘以 k/(k+1) 后，每个 large 时间为 k/(k+1)，每个 tiny 时间为1/(k+1)，目标变为1。配置列表和 F 不变，每个 load-localizer 多项式乘以同一个正因子，故证书仍成立。真实最优同时缩放，趋近2。

对任意普通 UM 实例的任一 raw K2 目标 T>0，CONFIG first marginals 已给出普通 fractional assignment：每个 job 总质量1，每行 fractional work 至多T，且支持上的每个处理时间至多T。标准二倍 assignment 舍入可直接证明如下。每行按处理时间降序把 fractional mass 连续填入容量1的 slots；job-slot 的分数二部匹配可由 matching integrality 取为覆盖全部 jobs 的整数匹配。第一 slot 的 job 时间至多T。第ell>=2 slot 所选 job 的时间至多前一个完整 slot 的 fractional work，因为该 slot 内所有处理时间都不小于它。求和后该机器总负载至多 T 加原 fractional work，因而至多2T。空行、零时间 jobs 和最后一个未满 slot 均按同一构造处理。对给定有理 first point，此舍入可在总位多项式时间执行。

对 OPT(P)>0 且存在 raw 可行目标的输入，定义 tau(P)=inf{T>0:raw K2 在 T 可行}。上界 OPT(P)<=2T 对每个可行 T 成立，故 tau(P)>0 且 OPT(P)/tau(P)<=2。本文 tau(P_k)<=T0，所以该比值至少为 (2-floor(sqrt(k))/k)/(1+1/k)，趋近2。因此全类间隙上确界恰为2。这里没有假定一般 raw K2 可行性 oracle 可高效求得，也没有从间隙推出近二 NP-hardness。

## 11. 更强条件可以切掉此点：准确边界

令 A_i 为 h 在 U_i 的原 selector endpoint，C_i,b 为该 B 的 unit incoming occupancy。全局法则在 A_i C_i,b=1 时，该 B 实际负载为2。因此

    F[A_i C_i,b(T0-load_B)]=a(k/L)(T0-2)<0.

这是真实有效的二事件条件容量不等式，但不属于第3节仅 affine-q PSD 的合同。这里的 C 是 incoming 原端点之和；逐原 incoming endpoint 分拆也产生负值。因此本文不声称通过额外的跨行二事件条件容量系统。

同机 triple 也能切掉此点。对不同 ell,ell'，全局 F(R_jY_ell Y_ell')=a/L>0；然而 T0 下含一个 unit 的合法配置至多含一个 home e，因此每个合法 CONFIG(T0) 都给这个 triple 为零。本文只匹配 first/pair，不匹配该 triple。任意更强同机一致性结论必须另证，不能回填为本 v1 已通过。

本点还在未选中组件中执行 unit exports，故不满足 native canonical export<=activation。当前真实实例的 raw gap 不构成 canonical 系统、强条件 Hall 系统或计算困难性的结论；近二 hardness 仍 OPEN。

## 12. 来源与有限软件状态

作者冻结 Exact 为 `sol_diluted_shared_terminal_raw_k2_exact_only.md`，SHA256 `25888ec48d8000769bcf5d8d2c4ab9cf29825e9084d1f5bb888de6be7c44210b`。单独冻结的作者 Proof 为 `sol_diluted_shared_terminal_raw_k2_author_proof.md`，SHA256 `2e926c6471c68843602f78c101874198e0ad2808b8db12d737cc8a04f27ad948`。本稿完整重述最终数学对象与证明，没有把旧 actual-OPT-one 支持法则例子升级为真实 gap，也未声称对标准 matching、slot rounding 或有限矩构造工具的新颖性。

作者 finite audit 仅针对 k=2 的局部 frame：直接枚举121个有理 H/Q states，逐项核对 B-row 全部 first/pair，再对 constant、selector-regime A、全部16个 f heads、全部32个 e heads 共50维的 weighted affine Gram 做精确 Fraction LDL，并逐项重放。50个 pivots 全正。它没有展开 M=7681 的全输入 M2 或所有跨组件 contexts；一般 k 和任意全局 contexts 由第7–8节理论证明覆盖。

该局部 audit 代码为 `sol_diluted_shared_terminal_raw_k2_finite_audit.py`，SHA256 `4da7af092c02ff53ff41b041d78099f23f23fea28f6021222f140e48911f362c`；输出 JSON SHA256 `0b2b750dbce6a49f2b027731b868eb2f709f93b1e573d3948edf07bf0eb392e6`。代码通过 --output 指定唯一输出文件，可以在新的目录重放；它是有限作者核，不是一般证书生成器或新算法软件的实现。本文不以 hash 替代实际全文审读，也不代签尚未读过的历史来源。

root 的实际重放命令为 `python3 tests/audits/unrelated_machines/diluted_shared_terminal_raw_k2_finite_audit.py --output <全新scratch文件>`；运行结果与作者原 JSON 逐字相同。具体 argv、目录、代码及输出 hash 保留在 root replay scope。此 k=2 例本身的 OPT/T0=1，不能把它包装成有限实例已经数值显示近二；任意大 k 的锐界由前文解析证明。
