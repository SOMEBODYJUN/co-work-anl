# Private clause / real ring 三半上界：独立 Exact-first 重构

主对象：`private_clause_query_return_universal_three_halves_exact_v1.md`。

主 Exact SHA-256：`21b334eec1ca8af9e368604552d93dd5b36eff9b75738e97db07f7097035fd2c`。

允许且实际读取的依赖只有：

- `general_weighted_query_return_three_halves_exchange_exact_v1.md`，SHA `bda34c6f0abcbbb3fafad8fbadbec8c2e89f940ddef8e3a8f6d9ab92b04cbd41`；这是新陈述，不被当作已证黑箱。
- 既存 current `two_witness_query_separation.md`，SHA `fa93beb7acbe8cbc96ce8da05c30e69584bd6c5828bb6e1ab164497150b45b1c`；下文只用/复证其 §1–2 的 v2 阈值染色机制，不认证同文件其它新计数身份。

读取次序为先主 Exact、再以上两份允许依赖。本次未读取任一新候选作者 Proof、root/其它 agent 推导；没有软件或有限枚举，仅 scratch 写记录，未改 repo、Work 或 Git。

**判定：主 Exact 通过，无 standing fatal。** 任意私有异权 H_c/A_c、全部给定 strict local certificates 与真实全局 ring 可以完整组合到 C≤3T/2。以下分别自证所需 local exchange，再独立给真实 ring matching，绝不把私有 outside 包装当原 ring。

## 1. 所需 local lemma：自行从旧染色机制证明

固定一个 clause，略去 c。取 i≠j 的 aligned λ_i、λ_j。为了精确记录缺席的 boundary jobs，**仅在分析中**给每枚 q/b 一个互不共享的 O_z，time T，把 λ_i/λ_j 省略的 boundary jobs放各自 O_z，得到同一辅助局部接口的完整 σ0/σ1。

这里的 O_z 不是主实例 P 的机器，也不会出现在最终 τ；其作用只是把内部两见证扩为可用旧染色机制的完整对象。内部 H、A、Q、R 的真实端与 processing times 都不改。

σ0=aligned_i：q_i 和所有 b≠b_i 内部。σ1=aligned_j：q_j 和所有 b≠b_j 内部。令两个 query 为

    z1=q_j，z2=b_i。

它们在 σ0 的旧端是不同私有 O_qj、O_bi，在 σ1 都进 H。其它 changed jobs 包括 q_i（内部→O_qi）、b_j（内部→O_bj）以及任意 A/其它 b 的内部重排。

### 1.1 不错误套用旧全局 δ 界

这两个 query 的旧 processing time 是 T，不是 tiny；旧 theorem 全局 δ 的直接上界会是 T，不能谎称 δ=0 然后由式子免费得到3T/2。这里需看实际染色 proof 的位置不变量。

按旧机制：query arcs 各染自身颜色；若某未触发 machine 接到某色新端总量>T/2，则将其全部非query出弧染该色。每个 nonquery由唯一旧机器赋色一次；每机所有新入量≤T，所以一机不能被两色触发。两色 nonquery supports A_z1、A_z2 不交，且全部内部新端仅取两个输入见证实际用过的端。

O_qj、O_bi 在 σ1 没有 job，且没有其它 job可用它们，因此没有新入流、永不触发。H 中也没有这两个 queries 的旧负荷。对任一颜色 z：

- H machine 未标该色时，旧总负荷≤T，所加该色流入≤T/2，故≤3T/2。
- H machine 标该色时，全部非query旧出弧已迁走；该机没有任何 query旧端残留，固定加选中流入是 σ1 负荷的子集，故≤T。
- 所有 O_z 每台只允许自身一 job，故无论该原 job在内还是外，实际 outside≤T。

于是两份单query调度**各自完整**≤3T/2，而非错误依赖全局 tiny 假设。零内部时间允许：严格触发>T/2及非负和不变量照常；未使用的 finite>T 端也不被调用。

### 1.2 从不交 supports 得到精确两种 boundary 模式

b_j 是 changed nonquery，因 supports 不交，至少一份单query调度不移动它。确定性选这样一份，再把 q_i 放其自身 O_qi（若本已外送则不变）。这只减少 H 负荷，且 O_qi 单 job≤T。

- 若选中 z1=q_j：q_j 内部、b_i外部、b_j仍内部、q_i外部，得到指定 mismatch(j,i)。
- 若选中 z2=b_i：b_i内部、q_j仍外部、b_j仍内部、q_i外部，得到 inactive。

其它 q 均外部、其它 b 均内部，所有 A 一直在 H。只用原 local witness 的内部端；q_i被外送也只用分析 wrapper 的既有 outside。所有局部原 jobs各一次。此即所需新 weighted exchange 二选一核心合同的独立证明，不假定它的未读作者 Proof。

## 2. 不需要判定 inactive 可行性

对每 c，依固定顺序对全部 i≠j 运行上节算法。

- 若任一次输出 inactive，保存这份内部 assignment，把 c标为 inactive。
- 若没有一次输出 inactive，则所有有序对都已经给出了指定 mismatch(j,i)的3T/2证书；对 j=i 使用输入 aligned λ_i≤T。把 c标为 flexible。

因此每个 flexible clause 都有**每个** ordered query j / return r 的完整内部证书，inactive clauses 则有所有 b内部、所有 q外部的证书。这里没有求解“inactive在3T/2是否不可行”的未知判定问题。即使 inactive实际可行但算法没有找它，全部错配证书仍足以把该 c当 flexible。

计算版 λ全给，以上有限次构造均有效；存在版可数学上选定每份存在的 λ后得到相同存在性，不声称原 P 可免费求未知 strict witnesses。

## 3. 真正的全局 ring 边界匹配图

令 F 为 flexible clauses，h=|F|。构造**仅用于选择证书的抽象二部图**：

- 左侧：每个原 q_i（真实与dummy全部）及每 c∈F 一个符号 B_c。
- 右侧：每个原 ring machine M_i 及每 c∈F 一个符号 C_c。
- q_i 连它两个真实原 ring 端 M_i、M_i+；若 i属于 flexible c，还连 C_c。
- B_c 连该 clause 所有真实 return pins pin(i)。若多个 occurrences有同一 pin，合并为同一图边，但保留可选 occurrence 标签。

两侧各 N+h。B_c、C_c只是匹配标签，**不是新增执行 jobs/machines**。将来 C_c匹配到q_j表示读入该原 q_j；B_c匹配到pin(r)表示返回该原 b_r。所有 inactive clause 的 q只有ring边，dummy q也只有真实ring边。

## 4. 所有 ring 的共同容量：显式 fractional perfect matching

对 flexible clause c 的每个真实 occurrence i设 α_i=1/k_c≤1/2；其它真实/dummy indices设α_i=0。

若 i属于 flexible c，给：

    q_i→C_c: α_i；
    q_i→pin(i): 1/2−α_i；
    q_i→另一个真实ring端: 1/2；
    B_c→pin(i): α_i。

同一 B_c→machine若来自多个 occurrences，其流量相加。非flexible真实与dummy的 q_i 各向两个真实ring端送1/2，不给 dummy定义实际return pin。

所有数非负，这正是 k_c≥2 的使用点。每 q_i row=1；每 C_c column=Σ_{i∈c}1/k_c=1；每 B_c row=1。对每个 index i，将 q_i和对应B_c贡献相加，它给自身两个 ring端各恰1/2。每台 M_i收到 q_i 与其前驱 q 的各1/2，故每个 ring column也恰1。

padding保证真实环至少3个不同 indices，q的两个端及上述前驱均是原来不同机器/任务；不把资源复制造成两份。重复变量/文字仍是不同 physical occurrences，因此 α计数、q身份和clause membership均不合并；重复pin由汇总流自动处理。

于是图有 fractional perfect matching。对任意左子集 Y，其单位row流入N(Y)，而各右column总量1，所以 |N(Y)|≥|Y|；普通 Hall给整数 perfect matching，可用确定性 bipartite matching/flow 算出。无需 SAT assignment、统一变量环方向或分数执行原 jobs。

## 5. 将匹配选择真正落实成全部原 P

整数 perfect matching的每 C_c恰接一枚 q_j且j∈c；每 B_c恰接一台pin(r)，选固定最小合法 occurrence r作标签。取已存内部 mode(j,r)：j=r用strict aligned，j≠r用本节独立得到的mismatch。inactive clause使用其保存的inactive assignment。

最终只分配原 jobs：

- flexible c 的 q_j在自身H_c，b_r在其原pin；其它q按匹配的真实ring端，其他b在H_c。
- inactive c 的所有b在H_c，所有q按真实ring匹配。
- 每 A_c始终在自身H_c。
- 每 dummy q按其真实ring边，dummy b在其独有D_i耗时T。

每原 ring machine在整数matching中恰接一件原q或所选真实b。外部端 time已在输入中给为[0,T]，所以其**实际**load≤T；即使time=0，cardinality“恰一件”仍成立。每dummy D_i仅自身b，load=T。各H_c mutually disjoint且与ring/D分离，其实际内部load≤3T/2。因此全机同时≤3T/2。

每个原 q、b、A恰执行一次，没有丢真实/未读queries、未返回b或dummy任务。分析 O_z全部丢弃；没有把其“私有、单job”的性质移植到真实共享pin。真实ring的共同容量由第4节全局matching另外证明。抽象B_c/C_c也全部消除为原job identities，不计作实际对象。

## 6. 边界与量词

- T>0是当前主域；零内部/外部processing times原生允许，构造只用非负有理比较及实际有限端，不对∞运算。
- H_c若空却要给q_i内部证书则前件不成立；非法λ可在计算版报告合同外。所有A有限资格及每模式恰一次由输入验证。
- k_c≥2不可免费移除：local要两索引，global fractional α≤1/2也用此条件。空/unit clauses均在域外。
- 所有occurrence的q拥有两个真实ring端，b仅其指定pin；不借用其它机器。不对某个源的strict SAT decoder作结论，尤其不能从external near-unit数值自动得身份。
- Φ为空时没有变量/clauses/indices/jobs，单独输出一台idle原机和零jobs，OPT0；不把非空公式计数0机器当合法UM。
- Φ非空、SAT或UNSAT、任意ordering与显式padding都不影响第4节守恒。dummy不需要clause证书或return pin。
- 存在版只是条件性OPT≤3T/2；计算版输入包含全部λ，不能偷放“求未知strict调度”oracle。

## 7. 原矩阵 counts 与总位多项式

实际机器 N+H+d，实际jobs 2N+a。real q外部2L、real b外部L，dummy q外部2d、dummy b外部d，故外部finite总3N；加内部E_int得3N+E_int。ring长≥3使q两个机器真正不同，不会重复计有限条目。dense大小(N+H+d)(2N+a)，空公式走独立分支。

局部certificate的每份指定job集是A_c+1个q+(k_c−1)个b，验证有限端/身份/有理load都为多项式。每c最多k_c(k_c−1)次local染色，每次只处理|H_c|+2k_c个分析machines、|A_c|+2k_c个原jobs；一次触发一machine、每nonquery着色一次。保存这些多项式份证书或事后按所需pair重算均可。

全局二部图两侧N+h，边数至多2N+2L≤4N；重复pins合并只减少边。显式fraction证书仅含1/2与1/k_c，整数matching不按分母值复制任何原job。最后逐原机串行输出2N+a个原jobs的时刻。

所有时间与T、λ负载、染色部分和以及开始时刻的分子分母位长为完整输入总位长的多项式。没有按T倒数、某个small time或分母数值展开。任意更长padding与aux网络按实际显式N、H、a、E_int及λ长度收费；仅当它们本来由源以多项式规模生成，才得到source bit-polynomial。

## 8. 排除的常见误用与最终结论

本证明没有：把旧全局δ误写成0；把新weighted Exchange Exact免费当已证；求解inactive不可行性；把local private outside当ring；将abstract C/B添成实际机器/jobs；假设SAT或同一source assignment；忽略unselected boundary/A/dummy jobs；将zero处理成正下界；或宣称任意global identity/compiler不可能。

**最终：主 Exact及其所需local二选一核心合同独立闭合，暂无standing fatal。** 在精确私有/单读入单返回/全索引strict可选/真实two-ring端及single-pin域内，任何公式都已有完整实际≤3T/2 schedule；故不能在此域制造NO>(2−δ)T、δ<1/2。越出这些假设的机制与一般UM目标仍开放。新作者Proof尚未读取，可在本记录冻结后解封做read-after。
