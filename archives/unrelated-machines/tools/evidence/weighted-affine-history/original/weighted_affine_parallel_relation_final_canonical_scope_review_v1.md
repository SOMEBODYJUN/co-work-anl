# Weighted affine并行关系：最终canonical完整范围实读审查 v1

审查者：rank_deficiency_fee，2026-10-18。实际全文读取最终canonical的header及§1–4，另冻本记录；未改repo/Work/Git或任何原冻结文件。

## 1. 实际读取对象、SHA与原路由

正式ID：`UM-WEIGHTED-AFFINE-LINE-PARALLEL-RELATIONS-HALF-ESCAPE-v1`。

本次实际全文读取：

`/workspace/scratch/038d9dcc4cac/co-work-anl-boss11/research/current/unrelated_machines/weighted_affine_parallel_relation_reweighting_obstruction.md`

wholeSHA256：

`1b0b9519c0e04d340278edd54d4f9eff8c20c824cb962a114dbcf22023e2f293`。

认证此准确字节版本的header、§1–4全部数学、actual合同及scope。Root所称早期scratch初稿未由本审查者实际读取，本记录不伪造对它的先行审查，也不认证未做的初稿差分。对最终sum明确限S\B的公式已按本次实际字节核对。

冻结链重新核hash均未变：

* Exact：`weighted_affine_line_parallel_relations_half_escape_exact_v1.md`，`780454f7a404d2fd17edf2adbf2e8e2fdd8318f98686478547a3be58d4433c7e`。
* 作者Proof：`weighted_affine_line_parallel_relations_half_escape_proof_v1.md`，`17bfce4c624b6c72566940329328f9765541e65db6a5156a4b6a2912761da6de`。
* 独立Exact-first：`weighted_affine_line_parallel_relations_rank_exact_first_review_v1.md`，`865ed89990239c36dabefe8250d72c7cfb2a4ea5f4f10ee4b609b2beea368be4`。
* 作者Proof实际读后：`weighted_affine_line_parallel_relations_rank_author_read_after_v1.md`，`6ac1283ca20717db3bdf89fcf933eee27f5b9fe95df0875572a7484691cc138e`。

顺序如实：本审查者仅据指定Exact独立重构先冻，root实际读后才交作者Proof；本审查者随后实际读作者Proof并另冻读后。Root先前已听作者口头策略，不记作该候选盲审。Bulk等其它候选不纳入本次认证。

## 2. Header和§1：对象/量词完整性

PrimeR≥2、k≥2均可变，R个groups j共享k个不同tag变量；A_j完整列出Σa_i=j的全部R^(k−1) tuples。每state每tag一条slope a_i/intercept j的长R线，支持D=kR个distinct真实资源。

权逐(j,a,u)显式非负有理、每state和恰1，可任意依赖整tuple/组/tag/cell，允许0；无共同item值、对称或小最大项前提。Partial B_j完全自由且全局不交，不要求一致source赋值或product结构。

完整UM每state独立private、每真实resource一机、每group一selector1；每incidence独立原job，private时间w或资源时间1，其余∞。所有unselected states和w0 jobs保留；原task都有finite端，R≥2及非空menus保证合法普通UM对象。没有隐藏guard、预载或拒绝。

Header没有引入外部LST困难性为证明前提；value1/R易判族与hard image严格区分，无复杂度假设或未知witness/oracle输入。

## 3. §2–3：任意state权的半保留及det-bit-poly finder

**合法候选与条件分布。** C={Σc=1}、D₀={Σd=0}，每个大小R^(k−1)。a(j)=cj+d必在A_j。固定j，(c,d)↔(c,a)的双射使条件于整个a后c仍均匀；k≥2保证各c_i均匀1/R。没有误假定不同坐标或不同组独立，也未将state-dependent权当独立输入。

**真实交集。** Tagi的selected lines满足y=d_i z+j(c_i z+1)；c_i0时两两平行不交，非零时恰共同P_i=(x_i,−1/c_i,−d_i/c_i)。不同tag点不同，所有P_i属于每组selected state，其外资源各组独占。

**损失与exception。** 固定state条件下，非零z成为共点的概率1/R、零z不成为共点，故E[L_j|a]≤1/R、总期望≤1。枚举中存在总loss≤1候选，至多一组loss>1/2。无exception就全删共点；有唯一exception则把全部共点连同其余自身资源给该组，其余删共点。所有B_j整数且不交，exception质量1、其它≥1/2。等号1/2、R2、零权都有效；R2/零权不需要额外排除域或算法分支。

**算法与位长。** 候选R^(2k−2)≤(R^k)²，而完整输入已列R^k states及每state kR权，所以对显式编码多项式，k不必固定。逐候选算R组至多k共点权，精确找首个总loss≤1者；概率平均只证存在，输出算法确定性。场运算/逆元按logR位长，有理和的分母积位长受输入条目位长之和控制，候选间不累计分母。未按1/w或分母数值展开，不称succinct poly(k,logR)算法。

**全部原actual。** Selector选态，只外送B_j对应原incidences，其余全部原jobs留各自private。Selected private明确为

    1+Σ_(u∈S_(j,a(j))\B_j)w_(j,a(j),u)
      =2−Σ_(u∈B_j)w_(j,a(j),u)≤3/2。

Unselected private总权1，真实resources至多一unit。全任务一次、原端合法，在一个共同assignment同时回算全机。B内w0 job可导出或留private不改private质量，仍执行一次。故actualOPT≤3/2，selector给≥1。

**规模。** GroupsR、privateR^k、resourcekR²、incidenceskR^(k+1)、selectorsR；finite2kR^(k+1)+R^k，dense(R^k+kR²)(kR^(k+1)+R)。计数与raw一致，输出全部jobs位长显式多项式，不借有限实验或隐藏后端。

## 4. §4与整体否定范围

主族每个全局赋值的坐标和只等于唯一j，恰满足一个constraint，value=1/R；这不意味着它属于某个未分析的hard reduction输出像。

Singleton A'_j={(j,0,…,0)}在(x₁,−1,0)共点置权1、其它0，R≥2时V0。所有private执行给峰2；任意C<2迫每group唯一正incidence导出到共同resource而负载≥R≥2，矛盾，所以actualOPT2，含所有零私时jobs。k1主关系正退化为此，不能删k≥2条件。

因此旧uniform任意关系半保留不能延伸成任意关系任意权半保留。反过来，本页只对**完整并行sum关系**的所有权保证半值，反驳只改这些原incidence权、保groups/states/resources/eligibilities、还想在包含本族的整个NO域强制V<1/2的接口。

若hard image避开本族、增加额外结构或预处理、改关系/资源/资格/gadget，本页没有排除。若原full supports已不交，任意归一化非负权保full质量1只是YES机械保留，不提供一般NO partial decoder。没有normalized tiny-NO困难性源、一般UM算法或near2主反面。

## 5. 最终认证

在准确wholeSHA `1b0b9519c0e04d340278edd54d4f9eff8c20c824cb962a114dbcf22023e2f293`下，canonical header与§1–4完整自足，与冻结Exact/Proof、先行独立重构和作者读后一致。未发现standing fatal objection。

正式认证限定域的constructive半保留、全部原UM≤3/2、边界反例与显式位复杂度；无软件/有限实验/外审/全球新颖性认证。原raw及独立记录不变，UM-TARGET-v1仍OPEN。
