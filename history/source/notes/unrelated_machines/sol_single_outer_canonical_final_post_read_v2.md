# 单外层 canonical 最终全文 post-read：8c5fcf…版本

日期：2026-10-18。审查者：`/root/sol_general_repair`。本记录为内部 scratch 最终实读攻击，不替代外部同行评审、软件认证或 novelty 审查。

## 1. 冻结对象与审查身份

已实际完整读取标题、开头两段、全部身份表以及 §1–12，未以摘要或局部 diff 代替正文：

`single_outer_shared_selector_rounding_and_hardness_source_boundary_final_v2.md`

SHA256：`8c5fcf273f9cd99a7b31b6b082a0880fc7ce186a0771cf600241eb07cc86e221`。文件实际为374行；工具完整返回约6436 tokens，没有输出截断。本次不改动该正文或更早的916…原件，也未改 repo。

我此前已完成给定-point Exact 的独立重构与作者读后，又完成 typed-Q-alone 13/8 Exact 的独立重构与作者读后。故本轮是知情后的最终 canonical 复核，**不算新的独立盲票**。本轮前后核对了下列冻结记录的 hash 均未改变：

- `sol_one_outer_13_8_exact_first_reconstruction.md`：`399c6b29f54b1c0f49ee21e3ef64552edc1fec21fe09579a4dd91eecb5fe710f`。
- `sol_one_outer_13_8_author_read_after.md`：`2064056e2cbd657f45238b0249516558472a3567568074b4aedba3e5c3bf88d9`。

这些旧记录及此前读过的四份 Exact/Proof 是已知背景。本轮不重新代签它们的作者身份、不为未打开的其他 review/code 背书，也不把正文末尾的最终 review 链接当作已经读取该目标文件的证据。

## 2. 两个正式 claim 保持分离

`UM-SINGLE-OUTER-PRIMITIVE-SA1-EPS2-4-v1` 接收 typed Q、正有理 epsilon<=1 和同一完整共同 primitive-SA1 有理点；结论是实际最低质量>=epsilon^2/4、全部原 jobs 的 C<=2-epsilon^2/4。位复杂度对这三项的完整输入编码计。正文 §6 给的是 uniform-winner/count-DP 算法。

`UM-SINGLE-OUTER-TYPED-13-8-v1` 只接收显式 typed Q，由自身生成普通矩阵、LP、11次查询及至多一次 CDF 舍入；结论相对真实完整 OPT 为13/8。位复杂度对 Q 本身计。正文没有借旧 supplied-point claim 假设一个免费 feasible-point oracle。

两个结果均只在单 outer、所有 state 的正 homes 跨全部索引物理互异、每 home 一位 own-singleton helper、fallback B 与全部 homes 分离、无其他组的域。fallback 可以任意共享，也可以不存在；外层 state 非空且 normalize。结构呈现随输入给出，没有声称从任意矩阵识别它。相同 fallback 向量可保留不同 indexed states；outer 的索引重复不得绕过 homes 物理分离要求。给定零 incidences 和 unused resources 留在模型中，不作为免费辅助组。

## 3. 完整 ordinary P 与实际 OPT

§2 的每 group 一个 selector、每 listed incidence 一个不可拆 job、每 indexed state 一台 private machine 的对象定义一致。规模 S+U 台机器、G+I jobs、S+2I 有限单元正确，包含零 incidence 的 private 零端点。

§3 的 OPT=2-V 对所有真实完整 assignments 成立。正向只 export 选中 state 的正 allocated incidence，selector 去该 private，未选 state 全部原 payload 保留 private，完整负载为1。反向在 C<2 时单位 resource jobs 不可共机；selector 确定唯一原 state，该 private 的导出正质量至少2-C，得到不交 allocation。可将未选 state 的 exports 全部还原 private，峰值不会增加到超过原 C，因为 C>=1。OPT=2 时由正向及 V>=0 推 V=0，未漏边界。

单位 selector 保证此域始终1<=OPT<=2。因此通用 UM 的空任务/零 OPT 情形没有被隐含纳入这个结构域；正文也没有将本结论宣称为一般输入算法。

## 4. LP、必要性、FAIL 与一次共同条件

§4 明确包含所有原 A/Z、全部 boxes/nonnegative/gates、resource caps、state partitions 和 perspective qualities，以及每个原 primitive 和补的所有线性 lift。所有量共用一个对称二阶数组，二进制对角合并；变量及约束数多项式。无 PSD、额外 unit-FSLP、未知 joint law 或高阶 oracle。

实际 quality>=epsilon 的 allocation 产生 rank-one 0/1 点；故精确 LP 不可行才有 V<epsilon。正文的 FAIL 明确排除 timeout、数值未找到解等含义。标准确定性有理 LP 可以返回编码长度多项式的精确点或精确 infeasible。epsilon monotonicity 用到的 mu_A、Y_AF、mu_A-Y_AF 均由相同 box lifts 非负，论证正确；搜索实际上只依赖必要性方向，不依赖 feasible 下端点<=V。

§5 own singleton 即便附带零 incidences，唯一正 claim 仍满足 Z-epsilon A>=0。乘1-Z后得 mu_A<=Y_AZ，再由 boxes/gate 得 Y_AZ<=mu_Z<=mu_A；(6) 从同一 gate 的 F/补 lift 导出，未调用 triple。选正 marginal outer state 仅条件化一次。fallback packing 所有资源列来自同一 conditioned row；删去其他 helper claims 只会放松。零 marginal 无除法。由 conditional own/resource 冲突，f_j>=b_j，故 Wf>=epsilon^2。

若某 helper 无 fallback，其 f_j=0，条件量自动令对应 b_j=0；算法不会构造不存在的 fallback state。剩余 positive weighted claims 足以满足(7)时仍可运行，否则此处不存在给定可行点。正文没有漏这个分支。

## 5. 两个福利后端及精确位成本

§6 uniform winner：在给定 j 的 state/request 后，其余 helpers 的请求独立于 j，期望数<=1。整数1/(1+T)>=1-T/2 给赢率>=1/2，因此 W>=epsilon^2/2。公式(10a)分别保留 r 的请求概率和 m 的 weighted value-request mass，即使未固定 state 的价值与自身请求相关也正确，因为赢率只依赖其他 helpers。Bernoulli count-DP 可逐资源、逐 excluded helper 计算；固定 states 后的最大 chosen-clause 分配逐项支配剩余均匀赢家实验。阈值 tau=epsilon^2/4 的推导 z>=(epsilon^2)/(4-epsilon^2)>=tau 正确。所有 helpers，包括其他 outer rows 的 helper 均回填，未丢辅助组。

§7 CDF-max：beta 总量<=1只用于初始福利下界。有限层积分等于最大分数期望；helper 之间独立足够，不要求不同资源请求独立。1-exp(-t)>=(1-1/e)t，e>8/3，且 Wf>0，给严格 W>(5/8)epsilon^2。精确去随机化在 partial state choices 下使用(15)，不错误地继续假设条件后的请求总量<=1。最终取每资源最大原 chosen-clause 系数，支配剩余请求实验。

这两套算法的数学步骤分别成立。§6 的旧 count-DP 不获得§7的新常数；§7 的 CDF 小审计也不能认证旧 count-DP。正文 Software=None、无11-LP端到端实现的说明准确。我的旧独立 Exact-first CDF 算法与 canonical 的 uniform-winner 算法也不是同一个 backend 实现。

标准 rational LP、一次正 marginal 除法、正概率 state 枚举、有限 score levels、CDF products 和 count-DP 均具有多项式位成本。正分母可能数值很大，但仅用其编码长度；不以 reciprocal 作循环界。DP 引入的1/(1+t)可统一到H!倍数，位长O(H log H)，而 CDF 每项只含多项式个原输入/point 因子；因此不是把一般 arithmetic circuit 的多项式操作数误当自动多项式位长。Q_j<=1 来自一个原 normalized chosen state，而不是将不同 states 的价值相加。

## 6. 数值质量线与11次查询

§8 系数、分支与常数均正确：

    (5/8)e^2-(2q0-q0^2)=(209e^2-468e+260)/64,
    a=13/8, b=10/8, d=1/256, q0=ae-b, q=q0+d.

这里 e 仅作为本段 epsilon 的短变量，不是自然常数。二次式分子在[0,1]递减，值最小1。q>0给q0>-d，平移消耗严格小于2d+d^2=513/65536，而1/64=1024/65536，剩余严格大于511/65536。q<=97/256<1。Good weight z<=q 会给 W<=2q-q^2，与严格福利矛盾，所以 z>q。epsilon=1 给定点的实际 q=97/256，完整 C<=415/256；这不是 Q-alone 算法自动在1查询的保证。

§9 恰好11次正 dyadic midpoint 查询，无第12次epsilon=1查询，无epsilon=0点。唯一需要的真实不变量 V<=h 由 FAIL=>V<midpoint 保持；feasible l 可以超过 V。结束 h-l=1/2048，l>=V-1/2048。

q<=0 时，aV-b<=-d+a eta=-51/16384<0，故 V<10/13，完整 baseline C<=2 已满足13/8相对保证。q>0 时 l>0且确有保存点；q>=aV-b+51/16384，从(19)、2+b=2a、OPT=2-V得到严格 C<(13/8)OPT。非严格报告当然成立。真OPT=1、所有查询可行、某些查询虚假可行、一次点也未保存，都由同样两分支覆盖。

## 7. 全部 jobs、NP源与审查措辞

§10 逐一恢复 selector 和全部 original incidences，selected private、unselected private、unit-resource loads 均已在§3计入。zero jobs 留private零端，duplicate indexed states不合并，unused machines保留。未见未付费 guard、被丢弃 helper 或 logical capacity 被塞回原调度定义。

§11 的 hardness-source corollary 明确固定0<delta<3/8，此时2-delta>13/8。YES为真实完整OPT=1；NO为真实完整OPT>=2-delta。给定 typed presentation 的总位多项式归约若产生这类真实承诺，13/8算法及 exact makespan比较确可多项式区分，推出相应NP-hard语言在P。结论是在P!=NP下该特定结构不能承担此类真实源，并未排除数值YES/NO实例本身或一般UM困难性。没有把固定selector的局部坏负载当真实NO。

若另给R_1完整点，旧绝对7/4、新绝对415/256是不同输入合同下的直接上界，正文没有拿它们代替Q-alone算法。正文只声明delta严格在范围内，未靠边界相等时的比较规则扩张。

§12 清楚标知情作者重构、四个来源用途、非新盲审、无外审及无novelty认证。我对最终正文中的数学链条承担本记录的实际读后结论，不代签作者实际读取的其他文件范围。本文末尾相对 review 链接及未来登记状态也不在本次软件/内容认证范围；root可在完成登记时引用本冻结记录。

## 8. 最终结论与未解范围

未发现最终8c5fcf…正文的数学或量词fatal；两个限定算法的证明、完整原任务输出、总位复杂度、FAIL含义及上述NP-source直接推论均闭合。它们仍是两个不同claim。未请求更改正文，未升级任何旧审查、旧backend小样本、未打开代码、外部同行评审或全局新颖性状态。

多人共享结构尚未解决：单 outer 条件 packing 不能直接合成多 outer 目标。我的三outer真实分布例仅切 plain primitive-SA1/resource-empty floor外推；已明确被CONFIG及degree-one负载localizer切，不能当当前强K2反例。后续主线应继续使用共同selector、CFG及affine/localizer信息攻击真实多 outer/deep问题。一般UM-TARGET-v1仍OPEN，本次最终读后不作其完成声明。
