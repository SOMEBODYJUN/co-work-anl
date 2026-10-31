from pathlib import Path
import json
stage=Path(__file__).resolve().parents[4];base=stage/'archives/unrelated-machines/state/资源';base.mkdir(parents=True,exist_ok=True);objects=[]
def put(name,body):
 p=base/(name+'--资源.md');p.write_text(body.strip()+'\n');objects.append(str(p.relative_to(stage)))
put('单位多切片原矩阵的整数Bareiss独立入口',r'''
---
id: c2-unit-multislice-independent-bareiss-entry
kind: resource
type_tag: 资源
title: 单位多切片原矩阵的整数Bareiss独立入口
status: integrated
truth_status: exact-finite-PSD-and-nonPSD-audit; general-proof-separate
review_level: full-primary-read-and-frozen-output-identity
summary: 保存独立四阶矩阵的全部基、Boolean矩公式、整数消元及m2失败字段语义；m2的rank4仅是正pivot阶段数。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/c2_unit_multislice_independent.py
---

# 原入口及其有限数学输入

[原件](../../tools/evidence/um-cycle-leaf-and-cardinality-primary/original/c2_unit_multislice_independent.py) 2181字节，SHA `b12850596bb79361d58803866e5ba29c9366dcf57e98929d561d86fca005b262`。只用Fraction、combinations/product、lcm和json；不导规范代码，无CLI、外部数据、seed或浮点容差。main固定对m=2,3,4调用audit，不能把它当任意输入的SDP可行性程序。

令n=m+1、t=n/m，任务j选机器a的Boolean变量为x_(j,a)。基含常数、全部nm个一次项、每个不同任务对的m²个兼容二次项，维数1+nm+binom(n,2)m²。给两个基项合并literal：同任务不同机返回0；相同literal按Boolean合并。若相容并涉及k个不同任务，每机器出现数c_a，矩为

\[
y_S=\frac{\prod_{a=0}^{m-1}(t)_{c_a}}{(n)_k},\qquad (z)_h=z(z-1)\cdots(z-h+1).
\]

完整M2按每一对基项生成；实际k≤min(4,n)，所以m2/n3不调用分母(n)_4=0。代码不另检查one-hot/count/localizer等式，那些属于一般证明或聚合结果中的另一主程序；不能把其他字段的700/4105等检查计入本独立入口。

# 整数消元逐步义务

先取全部Fraction矩条目的分母LCM，得到正整数scale及整数对称矩阵A=scale·M2。prev初值1。每阶段先检查剩余对角有无负项，有则立即判非PSD并输出阶段/行/数值；否则选首个正对角pivot，同时交换该行和该列。对剩余r,c更新

\[
 A'_{rc}=\frac{pA_{rc}-A_{rk}A_{kc}}{\mathrm{prev}},
\]

并断言每项整除，再把pivot行列交叉项置零、prev=p。所有保留pivot正，故这是正缩放的Schur补/congruence，正性判断精确，无浮点特征值或容差。

若剩余对角全0，代码还扫描**整个尾矩阵**。尾全0才判PSD；若有非零非对角项，二维主块[[0,b],[b,0]]给一正一负方向，判非PSD。只看对角0不能通过。尾零时rank=k确为原完整矩阵rank；失败尾非零时输出键`rank:k`仅记已经取过的正pivot数，不能当整个失败矩阵的代数rank。`tail_nonzero`行列是消元/交换后的矩阵位置，也不直接等于原monomial标签。

# 真实旧结果和m2边界

[冻结结果](../../tools/evidence/um-cycle-leaf-and-cardinality-primary/historical-runs/c2_unit_multislice_gap_audit.json)的independent数组与本代码SHA精确绑定，历史命令为`python3 tests/audits/unrelated_machines/c2_unit_multislice_independent.py`，Python3.12.14。本批复用这次充分真实执行，新增原入口运行0；旧记录无单独数值退出码或耗时，不补造。

| m/n | dim | scale | 实际结果 |
|---|---:|---:|---|
|2/3|19|16|非PSD；4个正pivot后全零对角尾部仍有非零(11,15)，输出rank4不授作总代数rank|
|3/4|67|243|PSD，16正pivot、尾全零，完整rank16|
|4/5|181|6144|PSD，61正pivot、尾全零，完整rank61|

m2的另一显式负平方可从同矩公式直接核：p1=x_(1,1)x_(2,1)，p2=x_(1,1)x_(3,2)，p3=x_(2,2)x_(3,2)，其Gram为

\[
\begin{pmatrix}1/8&3/16&0\\3/16&3/8&3/16\\0&3/16&1/8\end{pmatrix},
\qquad L[(p1-p2+p3)^2]=-1/8.
\]

这给自足非PSD证据；三项最小性及m≥3的一般完整分解已在[多切片一般PSD审查](../审查/C2多切片的一般PSD与最小边界负平方--审查.md)保存。本代码本身没有寻找该负平方，也没有独立运行m5。

# 与一般C2合同及旧版本的关系

相同实例有n=m+1件单位作业、m台全可用机器，整数OPT2；四阶C2-load证书在t=n/m可行、比2m/(m+1)趋2。一般PSD来自完整常数/一次/对称harmonic/反对称harmonic张成和正交分解，不由三次有限消元外推。本合同没有三阶逐项非负、完整CONFIG或prefix localizer；同机三不同任务矩−1/m⁴，故不是概率分布。

旧聚合正文hash5fe91d…，最终规范hash96863e…仅修“C2不蕴含CONFIG”的范围句，两代码未改。本族CONFIG(t)不可行不能反过来证明CONFIG对所有输入可扩为共同M2，因此不称一般松弛全局支配。聚合中m5的dim406/rank171由原主线程另跑主程序，不能倒填本独立入口m2/3/4。当前资源补的是原矩阵与失败分支的真实实现；无新一般定理、通用SDP后端或一般UM困难性。
''')
put('强制负载与双域计数闭包的同步原实现',r'''
---
id: forced-load-two-domain-cardinality-original-closure
kind: resource
type_tag: 资源
title: 强制负载与双域计数闭包的同步原实现
status: integrated
truth_status: sound-monotone-filter-and-finite-implementation-boundary
review_level: full-primary-code-and-bearing-proof-read
summary: 保存残余容量计数保边、域单调证明、位多项式整数二分及原两树/细分全输入与有限枚举域；接受不是调度。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/cardinality_closure.py
---

# 真实接口和合法输入前提

[原件](../../tools/evidence/um-cycle-leaf-and-cardinality-primary/original/cardinality_closure.py) 9866B，SHA `ce176ca14d24e9f9b3ebda3eddba65dbbb851a23811729b1a6c9e7d9f9f7ee37`，仅标准库Fraction、product、defaultdict、hashlib/json/platform/Path/prod。`closure(m,jobs,T,trace=False)`的数学前提是m≥1、非负精确有理时间、任务字典的合法机器号及非空有限域、T≥0；它不实现通用格式/域验证，不能声称所有非法数据都会被拒。m在closure中不参与逐机展开，只用实际出现的active端点；`schedules`小oracle才创建长度m负载数组。空jobs直接接受。

先令D_j={i:p_ij≤T}，空域拒绝。每轮从同一旧D计算单域强制负载F_i及恰双域{i,v}的任务束。若F_i>T拒绝。固定j→i，对每v≠i去掉j后取B={h:D_h={i,v}}、残余R_v=T−F_v。对q=0,…,|B|令K_q={h∈B:p_vh>R_v/(q+1)}。严格大于承重：q+1项等号时可能恰装满。v最多接q个K任务，所以i至少接K中除去至多q个最大的p_ih之后的尾和b_q。代码降序排序后`sum(sizes[q:])`恰为此量，取max_q而非相加。

把p_ij、F_i（j若本就单域则扣回一次）及各v束的max尾和求和，若>T便标记删j→i；所有候选算完再同步删除。trace只保存正reserve的other/q/K/量以及总lower，不是另求的最优撤离匹配。稳定接受返回True、幸存域和历史rounds；不返回实际调度，不判OPT≤T。

# 健全性、单调性和数值下界

任一当前T调度若用j→i，单域任务先占F_v，K_q中最多q项可去v，其余必须去i；把这q项宽松地取为i上最大的，得到有效负载下界。不同v的双域束、j及其他单域任务互不交，因此可相加，不重复收费。每个删除均不属于任一T调度，同步删也保全部调度；空域/强制超载保证OPT>T。零时间、T0无除时间的异常。

[实际承重正文](../../tools/evidence/um-cycle-leaf-and-cardinality-primary/comparisons/bundle_coupling_subdivision_barrier.md)另证明域收缩/降T时保留候选的lower不减。双域h被迫到i时新增p_ih强制负载补足旧reserve最多p_ih的损失；被迫到v时若h∈旧K_q且q≥1，R′=R−p_vh给R′/q<R/(q+1)，旧K_q\{h}进入新K_(q−1)，剩余尾和不减；q0会强制超载，h不在旧K时同q保留。其他强制负载只降残余。由此同步穷尽覆盖任何合法删除序列，小T幸存域含于大T，接受向上单调。不能只以“每轮安全”替代这一步单调证明。

有限边E至多E+1轮，每候选的束/q/筛选/排序均多项式；只处理活跃机，二进制巨大m不致数值展开。F/b/r是输入有理时间有限求和，阈值除q+1只增O(log n)位，不逐轮增长新处理时间分母。

`lower_bound`取全部有限时间分母积D（位长≤输入分母总位数），缩放为整数。高端U=Σ_j min_i Dp_ij来自实际逐任务最短端调度的负载上界，低端−1；整数二分首个接受H，返回H/D≤OPT。空jobs返回0。调用次数O(log(U+1))按位长多项式，不逐格点扫D，更不能把该数值下界当近似调度。

# 两树输入和细分的实际生成

`vw(k)`令α=1/(k−1)，乘k/(k−1)至α≥1/2得到h；两棵树非底层各有k个私有孩子，边任务在父1/k、子1；底父与同一终端有k件不同平行任务；两根另有一件双端时间1的大任务。原版本k2/3为h1、4机5/7任务；k4为h3、74机169任务。

细分每件双端原任务(u:a,v:b)为两件(u:a,w:1)、(w:1,v:b)，私有w，各原任务身份保留，m′=m+n、n′=2n。生成器没有借其他项目API。若全部双域且简单无平行束、无单域，T≥1时每束≤1项、q0 K空、q≥1尾和0，因此没有首次删除。这个明确失败机制使细分下界变1，但真实OPT仍θ_k=2−1/k；后者由完整细分双向证明及原树调度证明承担。

原两树T<θ_k时，底束在q1迫(k−1)/k在父，incoming时间1遂被删，逐层传播至大任务空域；T≥θ_k保真实调度，闭包阈值等于该族OPT。一般输入没有此充分性。极小超载星消元或真正三机一致性是后来另一接口，不能因该过滤能切原树就认为一般近二完成。

# 历史执行范围和准确计数

[聚合旧run](../../tools/evidence/um-cycle-leaf-and-cardinality-primary/historical-runs/bundle_subdivision_audit.json)的`reports.cardinality_final.json`绑定同SHA；旧base_commit176ecd…，Python3.12.14、无随机数。原命令`python3 tests/audits/unrelated_machines/cardinality_closure.py`。本批复用充分真实旧run，新增原程序运行0，未补造历史退出码。

小矩阵枚举值{0,1,2,None}、每任务至少一端；(m,max_n)为(1,3),(2,3),(3,2)，包含n0。每种m的有效列数4^m−1，所以矩阵40+3616+4033=7689；每矩阵目标0,1/2,1,3/2,2,5/2,3，共53823 matrix-target。逐任务全有限端笛卡尔oracle核所有T可行调度保边，计115799次；跨目标会重复同一调度，不能称互异调度数。删边计7232也跨fixture/target累计。`accepted_infeasible=0`只在这个有限小宇宙，不证明一般完整判定。monotonic_target_checks53823是目标循环计数，不是53823次互异相邻目标的非平凡比较。

四边界为巨大m=2^100但空jobs、零时间T0、单端负载43/77、50位量级分母；均返回精确knownOPT。family固定k2/3/4、原/细分各一实例；k2目标{1,29/20,3/2}，k3{1,4/3,49/30,5/3}，k4{1,5/4,69/40,7/4}，共22记录。k2/3反复作有限全分配验证，k4从未枚举2^169/2^338；最后原/细分二分下界分别θ_k/1。k4的真实OPT7/4来自证明而非字段`known_opt`自证。

本资源新增完整同步原实现、残余单调性和输入/运行边界；已吸收的bundle等式与细分定理不重新命名。一般UM算法/困难性、配置oracle、外审和优先权未由有限通过得到。
''')
put('闭环单任务逃逸的原端点与全超立方体极小峰审计',r'''
---
id: closed-cycle-original-endpoint-minimax-hypercube-audit
kind: resource
type_tag: 资源
title: 闭环单任务逃逸的原端点与全超立方体极小峰审计
status: integrated
truth_status: finite-full-labelled-path-audit-with-separated-general-threshold
review_level: full-primary-read-and-real-old-run-binding
summary: 保存独立整数端点重构、全部状态负载与到任一最优状态的bottleneck Dijkstra，分开1024/16384/8192全状态和8/12/37结算状态。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/closed_cycle_escape_independent.py
---

# 原入口及整数实际输入

[原程序](../../tools/evidence/um-cycle-leaf-and-cardinality-primary/original/closed_cycle_escape_independent.py) 2342B，SHA `cf25765fb15827e3600c5715a3dd4b3f9b8983d175b666eebd44168a7b809c46`，只标准库，不导任何其他审计。main只跑(k,d)=(3,1),(3,2),(4,1)，无外部数据、seed或浮点。一般参数的数学域是k≥3,d≥1，但代码没有通用域校验，Dijkstra以10^20作未见距离哨兵，仅对所列小输入充分；不将run函数包装成任意无界参数的一般求解器。

每件任务恰两个端，按scale=4k²整数单位重建原矩阵。root为机0，环g=0,…,k；g<k有h=d个私有home，macro环g=k有h=d+k−1个home。置a=4k(k−1)、δ=4(k−1)、c=4。环根任务在root耗时：g0为δ+1、普通tiny为δ、macro为a，另一端为首home耗scale。每home一枚e任务在本home耗a，另一端为下一个home耗scale，尾任务另一端为root，g0尾耗2、其余尾耗c。总m=(k+1)d+k，n=(k+1)d+2k；所有任务都是不同带标签对象，d1仍有根和尾两件任务，不会压成一条边。

二进制mask第j位选该job两个端之一。坏sigma仅g0整环位为1，其余0。程序的cap逐job按该端真实时间累加每机负载，B/scale精确核为2−3/k+3/(2k²)。早期2/k²的版本不属于此原入口。

# 显式单任务路径与全部状态搜索

从bad出发，对普通tiny环g1,…,k−1依次先逆序翻所有e位（尾先回root），再翻该环根任务位；每步恰改变一个原job，总(k−1)(d+1)步。每个中间状态都实际求cap，最大恰B+c，最终cap=scale即OPT1的S0。路径不要求预先给一般最优终点或单调降低负载。

程序随后先计算**全部**2^n个带标签合法分配的真实峰值values。Dijkstra状态为整个mask，邻居为翻任意一个job位；标签是从bad到此状态的路径最大峰值，松弛new=max(旧路径标签,邻居真实峰)，堆按(标签,mask)破平局，丢弃过期项。首次结算任一`values[s]==scale`状态即停止，因此求的是“到最优调度集合的全部单任务路径中，最小可能最大峰值”，并非分别到每个预定最优终点都已证明同值。另核min(values)=scale，实际确认OPT1。

结算状态少不表示只读了这些赋值，完整values已先生成。Dijkstra统计不等于最短步数；显式路径的4/6/6步是另一个构造检查，不称所有最小峰值路径都最短。

# 与一般B+c阈值证明的准确关系

[既有冻结审查](../审查/闭环容量释放与单任务逃逸精确阈值冻结审查--审查.md)另有无界参数的下界：从bad离开时，未开环的非尾任务前移会使home负载≥1+a/scale；未开环尾任务回root恰B+c/scale；g0根回root加δ/scale+1/scale；g0其他e回home同样≥1+a/scale。后两种峰严格大于B+c/scale，故任意第一步的最低可能峰为B+c/scale。上面的逆序逐环路径达到它，所以到最优集合的minimax峰精确B_k+1/k²。

这是独立于有限Dijkstra的组合证明。代码不构造最优凸组合x、槽图或最小费用匹配，也不检验该族所有最小槽匹配或所有不增负载的批次；那些属于旧聚合的另外三个程序。不能把同一JSON中的slot/DP计数计成本源新检查。

# 真实旧运行

[完整冻结聚合](../../tools/evidence/um-cycle-leaf-and-cardinality-primary/historical-runs/optimal_hull_closed_cycle_audit.json)的`independent_minimax_path`为本代码实际输出，sha256表精确绑定本源与最终canonical ba5d9763…。历史命令`python3 tests/audits/unrelated_machines/closed_cycle_escape_independent.py`，Python3.12.14。本批复用充分同SHA执行，新增原入口run0，旧数值退出码与耗时未保存，不编造。

| k,d | m/n | 全部赋值 | Dijkstra结算 | B | 最小峰 | 增量 | 显式步数 |
|---|---|---:|---:|---:|---:|---:|---:|
|3,1|7/10|1024|8|7/6|23/18|1/9|4|
|3,2|11/14|16384|12|7/6|23/18|1/9|6|
|4,1|9/13|8192|37|43/32|45/32|1/16|6|

原程序完整枚举总25600份状态峰，实际堆结算共57次，两者不能替换。原审查的另一个subset-DP总91136调度属于另一审计器，不扩大到本三例。历史声明先行重构后读稿的范围、固定k参与机预算以及cactus兼容关系仍在旧页，本源只补独立端点重建和路径实现。

新资源保全部输入端点/显式path并绑定旧结果，不重授一般阈值定理，不声称通用路径算法、近似或hardness。固定有限case、原凸包身份、一般UM目标和外审分开。
''')
put('条件叶路径投影与一致边际的双原入口',r'''
---
id: conditional-leaf-path-and-consistent-marginals-primary-programs
kind: resource
type_tag: 资源
title: 条件叶路径投影与一致边际的双原入口
status: integrated
truth_status: finite-exact-input-flow-mixture-and-full-job-checks; general-proof-separate
review_level: full-both-primary-read-and-frozen-large-table-validation
summary: 保存v2单匹配路径投影和v3同边际运输/完整matching混合的两份独立程序、全部实际输入/零边界及真实root重放范围。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/conditional_leaf_hall_path_projection_independent.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/conditional_leaf_consistent_marginals_independent.py
---

# 两个原入口、输出文件和真实先验

[v2路径程序](../../tools/evidence/um-cycle-leaf-and-cardinality-primary/original/conditional_leaf_hall_path_projection_independent.py) 10072B，SHA `a27da8f52dc4fbe2bf719214c1d38ea2fbc75d3ef0a310fcb75b54bb0457fc38`；[v3 MC程序](../../tools/evidence/um-cycle-leaf-and-cardinality-primary/original/conditional_leaf_consistent_marginals_independent.py) 8976B，SHA `d4b8a93458e584057108414aa0d883a0ea16423f255beab627aa45abed8c5e71`。均只defaultdict/Fraction/Path/json，无作者/项目导入、随机数或外部输入。两者main会向**当前目录**写固定`sol_conditional_leaf_hall_independent_audit.json`或`sol_conditional_leaf_consistent_marginals_independent_audit.json`，并打印摘要；不是自动拒覆盖的新目录工具。

v2实现者先完整读Exact v2、未读作者Proof/checker后独立重构；v3是熟悉旧v2后只对新增MC条款作Exact-first，而非整个候选fresh盲审。旧[真实root重放范围](../../tools/evidence/um-cycle-leaf-and-cardinality-primary/historical-runs/conditional_leaf_hall_root_replay_scope.json)明确两脚本在全新空scratch目录实际执行；v2按解析JSON相等（不要求key顺序），MC按字节相等。两代码/完整输出hash精确吻合。本批复用这次充分执行，新增原入口run0、无新CWD写出；未记旧数值exit则保未知。

# 共同数学输入与指定分区

旧菜单每core c有非空显式states、系数p_csu≥0且每state总和1；λ每core和1，0≤z≤λ，Σp z≥ελ；每旧资源Σ_cs z≤1。两程序接收这些**已经给定**的有理点，不求LP。指定原groups全部为cores，新增相邻path groups为leaves。自动threshold分类只有在原groups非threshold-unit-demand前件满足时才等于该分区，不能静默换分区。

旧资源u有d个不同positive-neighbor cores，按core插入次序建其各自port。d≥1有d个port及d−1相邻双端叶；d0保一个unused资源。每原state的正系数转到该core的group port，同core所有states共享该port，不按state拆端。显式零系数也保留任务：若group非positive邻居，合法地路由该资源首port或unused端，不产生正z。

# v2的单匹配扩展与完整原任务检查

v2`lift`置β_i=Σ_s z_(c_i,s,u)，前缀B_i=Σ_(j≤i)β_j，叶i左/右流为1−B_i和B_i。资源首/中port叶占用1−β_i，末port≤1−β_d，与core合计≤1。对每core-state，拼接所有路径中“遗漏自己的group port、无邻居时遗漏首port”的整数匹配，再乘λ；每个条件行和λ、自有port无叶占用而z≤λ、其他port叶占用≤λ。λ0自然全0，d0/1无叶，不除λ。每原group的threshold residual b_g还按转移前后真实系数重新核相同。

`matrix_audit`构完整普通P：每资源一机、每indexed state一private root，每group一selector仅本组所有roots耗1；每个显式incidence（包括零）独立一job，private时间为原p、资源时间1。给定chosen state与不交bundles，仅把所选正incidence外送，其余所有原jobs包括未选states/zero jobs都留private；逐job核端与全部机负载，峰要求等于target，不优化。

主例t2/D4：主M有4个各在一行4个g上权1/4的states，16个H_(a,j)各有home unit g和两parking资源各权1/2；λ_M=1/4、λ_Hhome=3/4、λ_Hparking=1/4，正z=λ。旧资源共24（16g+8A），路径后17cores、40leaves、64resources、116总states、144incidences；180machines、201jobs、404finite资格。给M第一行两个g，两个被挤H各取互异parking，其余H取home，再逐旧资源留owner port/其余端匹配叶，完整实际峰3/2。所有group的positive-support FSLP(1)也按真实positive state占用核列≤1。此代码没有枚举最优bundles或全部调度。

# v3新增MC运输表与同一core的完整匹配混合

MC要求对每core c、每leaf-edge，Σ_s y^(c,s)=y0。v2每state只取自有孔的单匹配一般不满足它。v3对每路径β先选π≥β、Σπ=1，全部slack加到最后port。某core拥有port i时令θ_s=z_(c,s,u)、b=Σ_sθ_s；无port时θ=b=0。若b<1，代码明确计算

\[
q_{s,j}=\theta_s1_{j=i}
+\frac{\lambda_s-\theta_s}{1-b}(\pi_j-b1_{j=i}).
\]

非负、行和λ、列和π且q_(s,i)≥θ_s。b1时必须π_i=1、θ_s=λ_s，直接q_(s,i)=λ_s避免除0。条件叶左/右流分别Σ_(j>i)q_(s,j)、Σ_(j≤i)q_(s,j)；每port叶占λ_s−q_(s,j)，加自有z≤λ_s。对state求和得共同y0，故MC逐行成立，不强制所有cores共享联合状态律。

对每个core-state在[0,λ]上用每条path的q作孔区间，合并所有有理端点；每非空子区间取中点决定每条path的孔，拼接得到覆盖**全部**leaves的完整整数matching。每片真实资源不重复、每叶都出现，权为区间长；逐leaf-edge重构原条件流。片数≤1+所有path port总数，避免把路径概率作指数笛卡尔积。λ0只有一个端点，片family空且总权0。不同core-state各自混合，仍不提供all-core joint matching law。

作者后来给无除法的lower-fill greedy运输，这是另一证明实现；本原程序实际使用上面b<1有理公式及b1分支，不能因作者Proof更新而把旧代码重写成greedy。一般q-table/投影和Qt值证明已在[后续证明读后](../审查/条件叶Hall投影与一致边际四源证明读后--审查.md)吸收；早期[Exact-only候选页](../障碍/一致条件叶边际仍无福利下界--障碍.md)保历史待证明身份，新程序资源不覆盖它或以t2有限run重授全参数定理。

# 所有实际边界与计数

两程序另有同一ε2/5 toy：core A的a0/a1三项正系数均1/3，a1 λ0；B的b0也三项正系数1/3，保四显式零项；u2共享两core，u0无positive邻居，其余d1，z为2/3、1/3、1/2等部分量。v2全tail调度保4个zero jobs，12machines/18jobs、峰2；它只核执行/零保留，不计算toy最优值。MC不生成调度矩阵，只核流与matching混合。

MC还加b1 fixture：A home λ1、alt λ0，B park λ1、home λ0；共4个states、7个lifted resources、1leaf，global左右流0/1。`beta_one_state_cases=6`是**(core-state,旧resource路径块)**进入b1分支的次数，同一状态可在多资源重复计，绝非6个互异states。新资料中明确这个原计数语义，旧页建议不覆盖。

| MC fixture | states / resources / leaves | 条件行 / 列 | MC行 | 完整matching片 / 每state最大 |
|---|---|---|---:|---|
| family_t2 |36 / 64 / 40|1440 / 2304|1360|176 / 6|
| partial_z_zero_lambda_d0_d1_d2 |3 / 7 / 1|3 / 18|4|4 / 2|
| beta_one_with_d2_and_zero_states |4 / 7 / 1|4 / 24|4|2 / 1|

toy/边界的7资源含一个unused d0端，但conditional_columns只循环非空ports，所以分别3×6、4×6，不是states×7。MC主例states只计36个core states；v2的116包括80个新增leaf singleton states，两者数不同不矛盾。v2 conditional流存每叶一个确定端、含零λ值，共1440条；MC存两端每叶，共2880条，但“conditional_rows_checked”仍1440，不能把字典条目数当行数。

# 证据与范围

完整[MC输出](../../tools/evidence/um-cycle-leaf-and-cardinality-primary/historical-runs/conditional_leaf_consistent_marginals_independent.json)为943177B，[v2输出](../../tools/evidence/um-cycle-leaf-and-cardinality-primary/historical-runs/conditional_leaf_hall_path_projection_independent.json)为191593B；本批逐表核实际孔表、所有流、每片完整matching、完整P及两份实际赋值/负载。所有硬编码core/λ/z输入也独立物化保存，原脚本无其它数据依赖。

旧root记录的canonical SHA1dd80c…是当时读取身份，不能当作本批不存在整稿原字节已重核。v2/v3各自Exact-first原审查、作者Proof与后续规范读后已比较；同边际、完整单state matching与all-core joint law仍是三层不同合同。没有一般LP/完整优化后端、CONFIG/PSD等价、近二hardness或一般UM近似结论。
''')
(stage/'cleanup/workspaces/Boss4/r3-um-cycle-leaf-and-cardinality-primary/object-paths.json').write_text(json.dumps(objects,ensure_ascii=False,indent=2)+'\n');print({'objects':len(objects)})
