# 任意异权 query/return 三半交换：statement-first 独立审查

审查者：general_query_response_review。2026-10-18。

## 1. 实际读取、依赖与范围

本轮先仅读新Exact：
/workspace/scratch/038d9dcc4cac/general_weighted_query_return_three_halves_exchange_exact_v1.md

SHA-256：bda34c6f0abcbbb3fafad8fbadbec8c2e89f940ddef8e3a8f6d9ab92b04cbd41。

未读同名作者Proof、root其它推导或其它agent策略。另按Exact明确许可读取既有依赖全文：
/workspace/scratch/038d9dcc4cac/co-work-anl-boss11/research/current/unrelated_machines/two_witness_query_separation.md

该文件SHA-256：fa93beb7acbe8cbc96ce8da05c30e69584bd6c5828bb6e1ab164497150b45b1c。

实际调用仅其§1–2的UM-TWO-WITNESS-QUERY-SEPARATION-v2完整实际调度/不交nonquery支持/零时间域，以及§4确定性位多项式保证；不调用费用、sharpness或§5计数加强。此为现成定理的结构推论，不宣称新分离算法或新颖性。

**独立判断：新Exact的二选一完整actual输出、inactive弱禁止推论、全部有序索引推论及明确外部范围全部有效，无fatal。以下给出具体构造，不求未知strict见证。**

仅scratch新增，无repo/Work/Git修改。未作软件运行或有限枚举认证。

## 2. 在分析中将私有outside成本置零

记sigma0=sigma_i，sigma1=sigma_j，i≠j。构造分析用矩阵P0：保留全部原jobs、全部机器、全部有限资格与内部时间，仅把每个边界job在其自身O_z的时间T改为0。

这不是输出新物理实例或免费外部假设，只为调用允许零时间的既有定理；最后会恢复所有原时间。原两份完整assignment在P0中仍合法，负载只减不增，所以均≤T。

选择定理中的两个queries为

Z={b_i,q_j}。

它们在sigma0均在各自outside，而在sigma1均在H，因此确为不同owner的两枚changed原jobs。它们的初态时间在P0均为0，故对每个z∈Z，其他query初态每机聚合负荷delta_z=0。原H可空，但若真为空则该aligned输入前件不存在；算法只对已核合法输入给保证，不需额外假设H非空。

## 3. 调用两个single-query实际调度并保护b_j

既有v2定理给两两不交的nonquery改派支持A_(b_i)、A_(q_j)，及两份完整P0实际调度theta_(b_i)、theta_(q_j)：

- theta_z恰将query z及A_z取sigma1端，其余所有jobs取sigma0端；
- 另一枚query保持sigma0端；
- 全部原jobs各一次，峰≤max(3T/2,T+0)=3T/2。

原job b_j不是Z中的query。它在sigma0于H、在sigma1于自身outside。由于两个A支持不交，b_j至多属于一个支持。因此至少可选一枚z∈Z使b_j不在A_z；在对应theta_z中，b_j仍保sigma0实际内部端。

选择可完全确定化：若b_j不在A_(b_i)，优先取z=b_i，否则取z=q_j。只读支持成员关系，不判定任何未知模式是否可行。

随后将原q_i置于自己的O_(q_i)，若本已在那里则不变。q_i在sigma1原见证本来就在该outside，端合法；这一操作只会删除其当前内部负载，不增任何内部机器负载。没有删除、复制或拒绝q_i。

## 4. 模式身份逐job核实

若选z=b_i：

- b_i取sigma1内部端，另一query q_j保持sigma0 outside；
- b_j由保护条件留sigma0内部端；
- 每个其它b_l在两输入中均在H，因此不论取sigma0或sigma1端都在H；
- q_i被置outside，每个其它q_l（l不等于i,j）两输入中均在其唯一outside，故始终outside。

所以准确得到inactive，全部R内部、全部Q outside。

若选z=q_j：

- q_j取sigma1内部端，b_i作为另一query保持sigma0 outside；
- b_j仍在H，其它b_l也在H；
- q_i置outside，其它q_l保持outside。

所以准确得到指定mismatch(j,i)，不是任意某一错配。

所有A jobs在两份见证均在H，输出也只在两个已用内部端之间选。各其它内部原job同样只取其实际sigma0/sigma1内部端。手动置outside的只有q_i，因此没有引入任何未用内部资格、假定两见证其余owners相同，或忽略不同job在同机的真实cost。

## 5. 恢复真实outside时间，得到同一原P完整actual

将P0的outside成本恢复成原P的T。每个O_z只有原z一件job具资格，且O_z互异，A没有outside资格；因此任何完整assignment在所有真实outside机器上同时负载≤T。q_i的手动outside移动也只使其私有O_(q_i)承一件T，不影响其它outside。

内部时间从未改变，手动外移q_i又只减内部负载，所以全部H仍≤3T/2。因为T>0，outside上界T≤3T/2。故上述assignment在原P中合法、完整，并有C_max≤3T/2。

矩阵P0仅是分析工具；最终输出只含原机器编号、每件原job恰一次，资格全为原P真实资格，成本全按原P恢复。内部目的地只来自输入实际用过的内部端，符合Exact的更强端点合同。

任意零内部时间、无内部资格的其它边界jobs、同机异权、任意arity、未用机器、内部有限端>T和A为空均不影响论证。输入见证实际使用的端必有限，其它∞从未参与算术；两份aligned所需入内部的b_i/q_j若无内部资格，输入本身就不合法。

## 6. inactive弱禁止与所有索引

如果inactive在峰≤3T/2不可行，算法输出不可能为inactive，所以必为指定mismatch(j,i)≤3T/2。算法不需要决定该不可行性；它先输出完整assignment及准确模式，弱禁止只在推论中排除一个标签。

交换i,j及输入两见证同理给mismatch(i,j)。若全部k份aligned strict见证实际给出，对所有有序不同对逐次运行，输出k(k−1)份完整原P调度，输出大小及总运行均多项式。若只知各见证存在，只得对应存在性，不声称可计算未知strict见证。

任意B≥3T/2时，inactive在≤B被禁止蕴含它在≤3T/2被禁止，于是每个指定错配已在≤3T/2≤B存在。这与“全部aligned strict可行且每个≤B的query/return必须同编号”合同矛盾。这里必须先有同一P的两份aligned strict实际见证；不是从任意源NO自动生成它们。

T=0不在新ID域内，本证明不对其作额外推广；既有分离定理允许零端时间，足够支撑P0，不需正内部端假设。

## 7. 总位多项式

验证原输入可逐原job查合法端、模式、完整性及全机有理负载，不合法时报告合同外。随后只把2k个已有outside finite数改为二进制0，调用已存确定性位多项式分离算法，选择一个支持、外移一个原job、恢复真实时间与输出assignment。

没有增加机器/jobs、分裂任务、按T倒数或分母展开。0、T、3T/2和所有部分和的位长在原总编码长度内多项式；原内部非均匀时间完整保留。Dense输入成本按(|H|+2k)(|A|+2k)计，不能只报稀疏边成本。每份输出给全部N=|A|+2k件原job的原机器编号，所有配对输出N k(k−1)亦为显式多项式。

## 8. 真正使用的外部假设与未覆盖范围

恢复outside成本时关键使用私有O_z、只有z可去、timeT，以及全部A固定内部。若真实source compiler把边界接到共享变量环、共享clause机或共同外部锁，这些机器可能同时承多jobs，恢复后的外部负载不由本证明控制，不能免费替换成O_z。

若A可跨局部网络外送、每次读入/返回不止一个边界job、或源依赖额外共同不可分负载，也没有自动适用结论。此Claim不排全部global identity/block-coherence编译器、不给一般UM或source-gap算法，不升级near2主目标，不提供新外部文献或新匹配定理。

**最终statement-first冻结：新Exact有效，无fatal；它是既存双见证查询分离v2在上述完整私有outside接口上的直接结构推论，未读同名作者Proof。**
