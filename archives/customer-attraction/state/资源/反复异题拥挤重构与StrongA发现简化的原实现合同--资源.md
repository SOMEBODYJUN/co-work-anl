---
id: customer-attraction/repeated-distinct-punishment-strongA-discovery-simplification-contract
kind: resource
type_tag: 资源
title: 反复异题拥挤重构与StrongA发现简化的原实现合同
status: 三实现/42型主数据/510简化报告全文；真实bank消费字段闭合，0本次BI/LP/MILP运行
summary: 分清bank原seed、bank端点、新σ42型端点和同σ59型StrongA端点；129/16216在bank输入，W1有符号LP的原始/对偶恢复与整数最小化界各自保留，超时无primal不作最小性或不可行证据。
source_refs:
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round10/credible/repeated_upgrade_attempt.py
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round10/credible/strong_adjacent_gap_attack.py
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round10/credible/simplify_strong_adjacent_packet.py
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round10/credible/strong_adjacent_simplified_packet.json
---

# 五原及真正消费的输入

主5共578571B：5760/6744/4265三个代码、561292完整m5数据及510完整简化报告均正常show、核SHA/blob后全读；同σ已读上下文精确复用和42型/255克隆全部新字段见[完整原端点](../计算/同一完整策略下反复升级的四十二型原端点--计算.md)。本轮0原入口/导入、BI、LP、MILP、扫描或新数学checker，不将历史exact_primal/超时字段冒当前进程事件。

5760实际读bank_upgrade_attempt_m5.json中的endpoint/source_path/target_comparison。该561628B必要related已正常取得/SHA1080066754937f1f549210aa2775f1788b0f74def71baaedcb0c9e7d5d1abd72，完整读这三个消费字段（endpoint全部38型）及层级标量；**没有**完整读其未用source表、source_utilities、strategy、endpoint_clones或endpoint_utilities，不额外done。它们的原字节仍保全，不因运行闭包而冒全数学已清完。

20567B实际StrategyCone/helper已核a5b3cac7…并全文读，canonical四文件同SHA完整上下文复用。程序import链及输入按原source-root/customer_attraction、tests/audits/helper、R-cd/round10/credible布局保存，NumPy/SciPy为外部运行要求；当前未import或测试环境。helpermain、自测、扫描和其内部Git元数据命令均未执行。

## 四层数据不可混用

采用[完整单位客户共同目录模型](../定义/共同目录完整历史模型--定义.md)，这里均是五人/八标签的单点或单策略过程，非全模型上界。单位客户以非空兴趣型整数重数表示；实数质量只辅助优化，有理清共同分母再回单位客户。模型空主题、重复、零客户和平局保留；当前实际两个新端点覆盖集合互异，不把软件同覆盖标签扩展静默当一般集合目录。

对一般m人、p个共同主题，记n_I为接受标签集I的不同单位客户数。终局x的覆盖数c_I(x)=Σ_j1_(x_j∈I)，W(x)=Σ_(c_I(x)>0)n_I，OPT=max_(y∈{0,…,p−1}^m)W(y)；角色i利润u_i(x)=Σ_(I:x_i∈I)n_I/c_I(x)。零客户与不被任何主题覆盖的客户不作分母；可含空主题，所有有序历史、重复行动和全部平局都在策略域。

完整纯策略σ在每个|h|<m的有序h规定一个动作。令z_σ(h,a)为先在h选a再按σ走完的终局，则完整SPE要求每个h、每个a都有u_(|h|+1)(z_σ(h,σ(h)))≥u_(|h|+1)(z_σ(h,a))。各型的这一收益差行就是Γ_(h,a,I)，所以固定σ恰由r≥0、Γr≥0描述；它不是只核actual路径。后文w_I=1_(c_I(x)>0)是固定actual x的福利行，W1是w·r=1。

在固定actual x删去**当前角色i**后同题查询t，
\[
f_i(t)=\sum_{I:t\in I}\frac{n_I}{1+c_I(x)-\mathbf1_{x_i\in I}},\qquad Q=\sum_{i=1}^m\max_t f_i(t).
\]
这一步把其余m−1个实际行动固定，和真策略偏离后的续局收益不同。令ℓ_I=Σ_(i=1)^(m−1)1_(x_i∈I,x_(i+1)∉I)，相邻预算为
\[
C_{\rm adj}=\sum_{I:c_I(x)>0}\frac{n_I\ell_I}{c_I(x)(c_I(x)+1)}.
\]
StrongA是所有真实完整SPE都满足Q−W≤C_adj的候选命题；实际固定query tuple a则用Q_a=Σ_if_i(a_i)及g=Q_a−w−C。它既不是“存在一个最优覆盖tuple及一次匹配”的量词，也不是half的OPT≤2W。这里的ℓ只按实际相邻**角色**边计退出，不补首尾虚拟边。

| 层 | W / OPT字段 | 准确身份与当前读取范围 |
|---|---|---|
|bank.source更早seed|source_W26/source_OPT32|bank程序更早输入的历史scalar；原source表本轮未全读，非5760实际消费输入|
|bank.endpoint|endpoint_W284593122/endpoint_OPT398900592|5760真实38型重构输入，source_path55001、J23467；这才是129/16216统计的客户权重|
|repeated.endpoint|W44924837031/OPT63464208590|新σ的42型精确原始声明，完整561292/255clones已读，3364 distinct IC行属于新σ|
|StrongA.endpoint|W722024386748740350/OPT761588195074452900|同新σ的59型正差点，原5026已恰一次实证，旧source40矩阵不属此endpoint|

bank没有顶层W/OPT，必须用endpoint_W/endpoint_OPT指其端点；source_W26不能错作其真重构输入福利。bank自身distinct_IC_rows3078是旧bank策略的原字段，未被5760读取；它不替新σ的3364，不能假称本批已对bank未用动作表作逐处方比较。5760实际上不读取bank.strategy，按bank客户及目标路径从所有R(k)重构整树，非就旧动作表逐项打补丁。

# 5760：完整可信菜单中的一次确定性重构

令ins=bank.endpoint，path=55001、target=其计数(2,1,0,0,0,2,0,0)。先用ExactSPESolver求全部子SPE终局菜单R(k)，若target不在R(0)则拒绝。实际已覆盖标签support={0,1,5}，missing_types取原bank客户兴趣与该support不交者；不是任意比较最优遗漏，也不是优化后42/59点遗漏重新定义。

对每个有序h、计数k、目标desired，候选规定动作a要求desired∈R(k+e_a)、u_a(desired)≥M(k)=max_b min_(q∈R(k+e_b))u_b(q)。若h是给定path前缀则强制下一path标签，否则在候选中按(u_a(desired),a)取最小。每节点还显式核规定a合法；不是贪心即时收益或随意固定不可信路径。

规定孩子继承desired。每个非规定b从
\[
\mathcal C_b=\{q\in R(k+e_b):u_b(q)\le u_a(desired)\}
\]
选一个，使下列score字典序最大，再按q字典序最大破平局：

1. upgrade=Σ_(I属bank实际遗漏型,b∈I)n_I Σ_(t∈I,t≠b)q_t。
2. distinct=非b标签中q_t>0的标签数。
3. 原bank输入覆盖welfare(q)。
4. −u_b(q)。

第一项计同一遗漏客户被**不同于查询标签b的行动**覆盖的角色数，若其它标签自身重复也按其人数q_t计；不是每客户只计一次，也不是只数不同标签。第二项才是全局不同标签数，不只客户I喜欢的标签。score是此算法的固定启发选择，不是新的收益效用或通用付款不等式。

所有q来自真正R(k+e_b)、并满足当前IC门槛；递归基例核终局目标一致。由[完整可信菜单算法](../算法/可信续局菜单与完整策略重构--算法.md)，每个孩子是子SPE且规定收益不低于每个偏离孩子，故整树可信。该菜单包含非极小偏离收益续局，比默认canonical极小孩子广；本启发每节点仍只选一个，不遍历所有完整SPE、也不声称对每份策略有正采样支持。

nonminimal_children129统计所选q的当前偏离收益严格大于该孩子全部R中的最小值；children_with_omitted_upgrade_crowding16216统计score第一项>0的非规定孩子个数。两者均在**bank.endpoint**输入/构造时取得，分母是全部有序节点非规定孩子集合，既不是客户数、也不是actual路径次数或优化后重数下的同一统计。

## 新σ的重数LP和原42型接受合同

重构后先在bank输入canonical verify_certificate，再造StrategyCone。helper对全部有序历史真后继作Fraction收益差Γ，去全零/完全重复行；非自身IC原有32767项，去重后原报3364行。只按终局计数缓存收益，σ仍保完整h。客户型空间是全部255非空型，Γ只依σ，不依用于生成它的bank/42/59重数。

optimize(J)最大化固定J覆盖v_J·r，约束r≥0、Γr≥0、w_actual·r=1。J=(2,3,4,6,7)是不同标签的支持，满足helper.coverage_row的集合支持调用合同；不能把其按bit求mask的函数未经处理用于重复索引。一般模型的比较重复仍合法，OPT由单调补齐不同支持求得，StrongA后续固定queries的重复则另按行保份数。

helper先将float坐标各限分母10^7，精确核Γ、非负和W1；失败则在浮点正支持>10⁻⁸上取近紧行（误差<10⁻⁷），用Fraction独立消元恢复，仍须精确复查。成功点清分母、除公共gcd得整数克隆；程序再直接Fraction各历史复核、canonical全证书核验，算真实W/OPT后才写42型输出。直接复核不调用canonical，但共享helper按原σ构造的terminal缓存，非外审或另一个盲实现。

每坐标精确对偶要求βw−Γᵀμ≥v_J、μ≥0；报告dual_bound=null/dual_optimal=false/dual_support空，故只有有限可行原始声明，没有交付该锥上界，更无全部σ/全部目录证明。原42型的固定J恰是唯一最优支持由其五个私有型证明，但此点objective=OPT/W不能代全锥最优或OPT≤2W的一般证明。当前五人half另有别证，旧HALF发现目的保为历史，不为清洗重跑该攻击。

# 6744：同一σ的固定查询StrongA线性攻击

程序读完整repeated.endpoint及其actions/path，不重选σ。在42型旧点精确算每行八个frozen值，按(值,−标签)选最小编号最大者(2,2,2,2,1)。用全部255型定义行F_(i,t)、相邻C行，Q_a=Σ_i F_(i,a_i)，g=Q_a−w−C。实际frozen分母1+c_I−1_(path_i∈I)，query不属I时系数0；C只在c>0用退出数/[c(c+1)]，空/零/重复情形不作0/0。

只为当前固定a解float LP：max g·r，r≥0、Γr≥0、w·r=1；既非Σr=1，也非枚举新策略/全部queries。W1保证正福利归一化；固定queries的差不总是重权后true rowmax差，所以恢复后**重新算全部八列最大值**，不能只沿旧a宣布StrongA。

精确恢复同样先各坐标分母≤10^7、失败再recover_vertex，必须Γ精确可行且W恰1。清整数克隆后canonical证书/直接全history复核；再算true_Q、W/OPT、fixed_gap、Csum、strong_gap。输出refutes_StrongA取strong_gap>0，refutes_HALF另取OPT>2W，二者不混。原59型正点已经由另5026原stdlib入口一次实际核完，本次不重复该入口，更不重跑LP。

对g的对偶还原要求μ≥0及βw−Γᵀμ≥g全部255坐标，β为W等式乘子不需预设正；只有核过才写fixed_query_dual_bound和非零乘子。原raw实际null/空，不能由HiGHS Optimal字符串或exact_primal=true补一个精确上界。source40矩阵/负source gap属于旧42型点，endpoint59/正true_gap属于另一输入；同σ、同actual路径并不等同客户表或原目标。

## 原点与新点的全部量词分流

42型原点Q46065063663−W44924837031−C2140620747=−1000394115，没有击穿StrongA；重权后59型点正差2714689114258275。后者仍满足half且有840最优有序比较中便宜指派；后续[tree全矩阵解析](五人相邻钱包原证书的tree全矩阵独审与最优选择界--资源.md)更证明其全部最优指派都满足相邻界，而共同query2仍反每query加强。不能把改变目标后的成功说成原OPT/W提高或HALF失败。

已有[十客户compact](../反例/十客户重复实际行的相邻钱包失败--反例.md)独立更小地否StrongA/每最优指派加强；后继全人数族在m≥7连存在版也否。它们与本代码链都是不同输入/量词，不再认一个新StrongA反例、一般方法不可能或六人半覆盖失败。

# 4265/510：整数客户数简化的准确失败范围

simplify读59型StrongAraw的m/p/path/fixed_queries/actions；import6744的行函数有main guard，不执行该LPmain。仍固定同σ、同旧a，定义同g。把Γ和g所有Fraction分母取LCM=s，原报告s60，形成整数行sΓ、sg后转float稀疏矩阵。

MILP变量v为255维非负整数克隆数，目标minΣv_I；约束(sΓ)v≥0、(sg)v≥1。后者精确意图是g·v≥1/60>0，**没有**保W=1，也没有上界每个客户数。若以后真有被接受最小点，首先只是同σ/同固定查询约束内，不是所有策略/所有StrongA反例客户数全局最小。

若res.x存在，逐坐标round成整数并要求误差≤10⁻⁵，再精确检查Γ、g·v>0；其后canonical全证书/直接全history复核，重新算true rowmax、真实OPT、正差/half和客户数，再保存endpoint/strategy等。float可行或solver状态不代这些接受检查；同覆盖标签扩展也须对具体接受点论证，当前没有这样的简化点。

510B原输出的全部字段为：scope一份同策略整数简化、source_file StrongAraw、m5/k8、actual55001、fixed_queries22221、floating_status=`Time limit reached. (HiGHS Status 13: model_status is Time limit reached; primal_status is None)`、solver_status1、universal_bound_proved=false、scale60、seconds94.47556687799988。它没有endpoint、strategy、W、OPT或customer_count；结合代码只在res.x存在且验收后追加这些字段，原记录没有交付可接受的简化见证。

time_limit选项30秒而seconds约94.48是整函数从读源/建cone/矩阵到solver结束的原耗时，不能把不同口径当造假或一个数学结果。超时/无primal既不证明整数不可行，也不证明原59型点最小或不可压缩；原大点的精确StrongA反例不受这次失败尝试影响。没有为补一个点再跑MILP或额外扫描。

# 程序、来源与当前0执行

三main都有guard并拒已有同名输出，未来若需重演须全原布局和新输出副本；当前只AST/文义阅读，无import及环境测试。helper虽保self_test/main/历史扫描/Git命令，调用这三个main不会跑helper.main，当前更未调用任何主入口。保全代码不等于当前执行其外部依赖。

同σ身份、source_W和255clone编码的核对只是文件值比较，不是新SPE/LP checker。旧bank只消费字段阅读/完整字节保留、新42点完整字段阅读、既有59点充分实际复现三种证据范围分开；不把129/16216移给重权点或bank3078移给新σ3364。

26WV原claim是pushed，raw sync needs-attention原样保；38untracked/2tracked同字节、无missing/different/unmerged、stash保留的独立记录并列而非伪改synced。五receipt仅本5，必要bank/helper/canonical/StrongAraw不额外done，旧冻结包不改。全部Git、claim、checkpoint和done由Root串行，0外审/新颖性认证。
