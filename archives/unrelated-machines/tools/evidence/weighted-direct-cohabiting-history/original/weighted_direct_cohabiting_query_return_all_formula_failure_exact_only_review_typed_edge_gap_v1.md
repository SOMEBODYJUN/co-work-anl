# 异权直接共居查询—返回接口：typed_edge_gap 独立 Exact-only 重构 v1

审查对象 ID：UM-WEIGHTED-DIRECT-COHABITING-QUERY-RETURN-ALL-FORMULA-FAILURE-v1。
实际只读对象：/workspace/scratch/038d9dcc4cac/weighted_direct_cohabiting_query_return_all_formula_failure_exact_v1.md。
实核 SHA256：076561e78796927d6792f6dfb3c581c11afd263752b9098abd9f35d58df2ddfb。
审查者：boss11 内部 typed_edge_gap，2026-10-18。

本记录在未读此ID作者Proof、未读其它人对此ID的推导前冻结。通用整数matching/双随机证书是既有方法，不主张新颖；以下按新Exact的真实P重新构图，没有把旧medium参数或旧private接口原结论免费搬来。本次没有软件枚举或审计运行声明。

结论：Exact的严格SAT双向身份合同、任意occurrence-dependent正权x_i+y_i≤1、全部公式actual≤3/2、baseline/active/dummy混合、空公式idle及总位复杂度均可自足闭合；无standing fatal。

## 1. 真实P与重要域条件

非空公式时每索引有不同M_i,C_i；q_i只有M_i:ρ、M_i+:1、C_i:x_i三个端；b_i只有pin(i):ρ、C_i:1两个端；u_c只有各真实i∈c的C_i:y_i。ρ>1/2，真实x_i,y_i正且和≤1，dummy x_i=1且不连任何u_c。

每索引只属于一个真实clause或是dummy；重复变量/文字是不同物理indices，不合并jobs。环长≥3使M_i、M_i+不同且每个有效edge对应环上的一条边。可选ρ>B/2不参与以下3/2构造，只影响另行希望的弱阈值保护。

## 2. strict≤1反向：先计数再得同编号，不能免费假定

任意M只允许q/b原jobs，且每个内部有限时间≥ρ>1/2，所以strict调度每M至多一件q/b。每C_i只有本编号q_i、b_i及其唯一clause的u有资格；x_i>0（dummy为1）使q_i与unit b_i不能strict共居，所以每C_i至多一件q/b。

q/b总计恰2N件，N台M与N台C合计至多2N个这样的槽。因此所有M与C都恰执行一件q/b。这一计数不把u算成独立单位槽，允许它真实与q共居。

由C_i恰一件q/b且二者仅有上述端，q_i@C_i iff b_i@pin(i)。每u_c实际所在C_i有y_i>0，不能同unit b_i共居；故此处必是同编号q_i@C_i、b_i@pin(i)。u不可能选dummy。

每索引于是有恰一件有效内部任务：未导出的q_i，或返回的b_i。该任务只用edge i的两个环端之一；若为b_i则端固定为pin(i)。所有M恰一件给出该cycle的perfect edge-to-vertex assignment，其方向只能全部左或全部右：若一edge用左端，则前edge不能用右端、递推全左；右端同理。

记变量环方向z0为edge i→M_i，z1为edge i→M_i+。每个返回b_i因此必须s_i=z；据z0取变量真、z1取变量假。每clause的实际u_c所在真实i都是返回索引，故该文字在同一变量赋值下满足。dummy返回可约束同一z，但不会作为clause见证；没有将返回身份额外加入模型。

## 3. SAT→strict完整调度

给满足赋值，各变量选对应z方向；每clause任取一个真实满足occurrence i。只对这些索引令q_i@C_i、b_i@pin(i)、u_c@C_i。其余全部q（含dummy）按变量z走内部环端，全部其余b（含dummy）留C_i。

选中的真实文字s_i=z，故返回b_i恰替代沿z方向原q_i所占环槽。每M仍恰一件、时间ρ或1；每选中C_i真实为q_i+u_c，负载x_i+y_i≤1；其它C_i为b_i负载1。全部q/b/u恰执行一次。一个clause只选一个occurrence，不同clauses的索引本来不同，重复文字不造成job复制。

## 4. 全公式3/2：共同辅助匹配的完整独立构造

精确按输入分C0={c:某y_i≤1/2}及C1=其余；令I1为active clauses的全部真实indices，m1=|C1|。每active i有y_i>1/2，故x_i<1/2。

先固定所有baseline与dummy的b_i在自身C_i；它们不会返回。baseline/dummy q仍必须在共同环匹配中，不能删掉。建立只用于计算的二部图：

- 左侧：所有N件真实q_i；所有active索引的真实b_i；所有active clauses的真实u_c。
- 右侧：全部N台真实M；所有active索引的真实C_i；另每active clause一枚virtual R_c。
- q_i连自己的两个环端M_i,M_i+；仅active q_i额外连其clause的virtual R_c。
- active b_i连pin(i)、C_i；active u_c连该clause全部C_i。

左右同为N+|I1|+m1个vertices。virtual R只分析q将来哪一件导出，不是原P的执行机器。

给active i∈c置w_i=1/k_c≤1/2；其余indices置w_i=0。如下单位行列和fractional perfect matching全部非负：

- q_i到pin(i)权1/2−w_i，到edge另一个环端权1/2；active q_i到R_c再给w_i。
- active b_i到pin(i)权w_i，到C_i权1−w_i。
- active u_c到每C_i权w_i。

q行和1，b行和1，u行和Σ_i∈c w_i=1。每M原有相邻q两份1/2，按pin扣除的每个w_i恰由同编号b_i的w_i补回，故列和严格1；active C_i列和(1−w_i)+w_i=1；virtual R_c列和Σ_i∈c w_i=1。这里的weights只是matching质量，既没有把实际ρ/x/y改成unit，也没有实际生成virtual jobs。

普通二部matching整数性给共同perfect matching。于是每active c的R_c恰选一件真实q_j，定义j(c)；其真实u_c匹配某C_r，定义r(c)。该C_r不再能给b_r，所以b_r匹配pin(r)。其它active C_i必须由自己的b_i占据，因为只有一件u_c填一个C；因此每active clause恰一return。q只有每个R_c接收的那一件导出，其余q都在环端。所有M恰一件匹配q/b，所有return pins全局互异。没有预设j(c)=r(c)，也没有按clause分别找互不兼容的内部调度。

## 5. 从辅助匹配恢复唯一完整actual，并逐C核真实异权

所有M上匹配到的q/b仍在对应真实有限端执行，恰一件、时间≤1。active b/u按匹配在真实pin/C执行；将每件匹配virtual R_c的真实q_j实际改放自己的C_j，耗时输入原x_j。baseline与dummy b按第4节固定；baseline/dummy q已在共同matching里走真实环端。最后每baseline c选一个y_i≤1/2的真实i，放其真实u_c@C_i。

逐机无遗漏：

- baseline C_i仍有unit b_i，无q导出到此；选中u所在机额外加y_i≤1/2，负载≤3/2。baseline其它C为1。
- active若j(c)=r(c)，该C真实是q_j+u_c，负载x_j+y_j≤1，b_j已返回。
- active若j(c)≠r(c)，C_j是q_j+unit b_j，负载1+x_j<3/2；C_r只有u_c，负载y_r≤1。其余active C为unit b。
- dummy q没有virtual资格，始终内部；dummy b留C，负载1。

每occ只属一个clause，故上述不同clause的C核对不会互相叠加u。全部原q/b/u恰一次且都用Exact原有限端；virtual R在恢复时完全消失。所得同一actual调度峰≤3/2，无论公式真假。

## 6. 退化域与总位复杂度

若active集合空，辅助图只剩全部q到全部M的环图，fractional half/half及perfect matching仍成立；所有b固定C，全部u由baseline步骤加入。无需存在active clause的额外前提。

空公式按Exact只有一台idle原机器、零jobs，OPT0，满足赋值和全部调度为空；不输出0台机器。只保实际出现变量，使此域L=N=0。对非空公式按最少padding有N≤L+2v；若额外dummy表显式给出，则按实际N计输入/输出，不把隐式指数padding当多项式。

非空P有限条目恰3N+2N+L=5N+L，dense条目2N(2N+m)；原q/b/u数2N+m。辅助图O(N+L1+m1) vertices/edges，fractionalw_i只需1/k_c（位长O(log k_c)），实际算法用整数matching并不按w_i倒数或任何处理时间倒数循环。按符号构造即可验证fractional证书，匹配整数性及确定性增广输出完整assignment。ρ/x/y的正性、和与1/2比较可精确有理运算；实际逐机至多本页列出的常数项相加，位长多项式。

结论仅排这套具体direct cohabitation矩阵的near2 soundness。它保严格SAT身份却全公式≤3/2，不排一般medium/多尺度/identity读取，也不提供一般UM近似算法。作者Proof尚未读取，本独立记录先冻；无代码/有限运行承担一般证明。
