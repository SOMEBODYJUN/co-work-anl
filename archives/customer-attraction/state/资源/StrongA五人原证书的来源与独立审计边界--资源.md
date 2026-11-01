---
id: customer-attraction/strongA-five-provider-raw-source-and-independent-audit-boundaries
kind: resource
type_tag: 资源
title: StrongA五人原证书的来源与独立审计边界
status: 五原全文与563651B完整4681处方已读；原5026标准库入口恰一次成功，新934与冻结全字节同
summary: 将五人59型原型与十客户compact反例分开，保存原seed负差/精确端点正差、完整原审计与tree旧review范围；本点弱最优指派通过，后继m≥7一般否定仍另属其族。
source_refs:
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round10/credible/audit_strong_adjacent_packet.py
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round10/credible/strong_adjacent_counterexample.md
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round10/credible/strong_adjacent_independent_audit.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round10/tree/strong_adjacent_raw_review.md
---

# 原五人raw证书的首次实际闭包

本五primary为5026B审计、6728B主稿、563651B raw、934B冻结独审输出及2954B tree旧review，共579293B，均正常show核size/SHA/blob后完整实读。raw的全部标量、原seed的40个frozen值、59客户行和4681个有序处方均按可逆全文视图读完，非以counts代读。[完整输入和全策略](../计算/五人原始相邻钱包证书的完整数据与一次核验--计算.md)使该有限对象自足；[证据目录](../../tools/evidence/strong-adjacent-raw-five-primary/README.md)保每个原字节。

当前[十客户紧凑反例](../反例/十客户重复实际行的相邻钱包失败--反例.md)早已独立否StrongA；那次三人21节点原审计不能替本五人4681节点背书。现未找到本5026/该raw SHA的既有实际执行载体，Root明确授权恰一次原标准库main以闭合这份完整raw。它已经成功，新934与冻结934逐字节相同；本次不称新反例、盲审、独立发现、外审或全m证明。

## 全模型与被否定的精确付款

采用[有限单位客户、共同有限非空集合目录、单位提供者与完整有序历史纯SPE](../定义/共同目录完整历史模型--定义.md)，保空主题、重复行动、零客户及离轨平局。固定实际叶Z、负载c_x、覆盖W，定义
\[
f_i(T)=\sum_{x\in T}\frac1{1+c_x-\mathbf1_{x\in Z_i}},\quad
Q_{max}=\sum_i\max_T f_i(T),
\]
\[
C_{adj}=\sum_{j<m}\sum_{x\in Z_j\setminus Z_{j+1}}\frac1{c_x(c_x+1)},\qquad
J=\sum_{c_x>0}\frac1{c_x+1}.
\]
冻结查询只变当前角色，**其余actual动作保持**；它不是沿改变历史走同σ的真实利润，不能对f直接套SPE IC。差集内c≥1，冻结分母至少1；零客户时均0。

StrongA要求每份完整SPE有Q_max−W≤C_adj。动机正确：任何合法m槽比较元组及指派的Q=Σ_i f_i(T_i)、并集O，逐客户给|O|≤Q+W−J；实际二进制会员串每次1→0退出对应一个不同覆盖位置，故退出数r_x≤c_x、C_adj≤J。若StrongA成立，最优比较Q≤Q_max≤W+C_adj便给OPT≤2W；前提已假，不由充分推导逆推为真。[全相邻静态消项](../引理/全相邻退出钱包的静态消项与冻结行价格--引理.md)保这些无条件代数和行价格，原末对及[直接吸收](../引理/静态覆盖松弛吸收末对钱包的直接缺额式--引理.md)没有因此被否。

# 五人原点的精确结论

m5/k8、59正整数型、共761588195074452900名不同单位客户，actual(5,5,0,0,1)。所有八个主题是不同客户集合；完整策略含1+8+64+512+4096=4681个历史，实际重复标签没有删掉离轨重复或合并同计数历史。标准库入口已实际逐32767个非自身偏离满足非负，最小差0；这是含真正平局的全树SPE而非仅末位/actual表。

| 原独审完整字段 | 精确值/范围 |
|---|---|
|packet_sha256|96a9341a65e09f4423ce7dbcdfa4fd4cd6756939374d06f08cfdd6d5396a3b40|
|m/topics/client_count/customer_types|5/8/761588195074452900/59|
|decision_histories/nonself_IC/minimum_IC_margin|4681/32767/0|
|actual_path|(5,5,0,0,1)|
|W/OPT|722024386748740350 / 761588195074452900|
|Q/Csum/J|762488197001610750 / 37749121138612125 / 182175821951597100|
|Q−W−Csum|2714689114258275>0|
|最优有序元组检查数|840，全部8^5个候选中过滤覆盖最优者|
|minimum_optimal_assignment|(0,1,1,2,5)|
|minimum_optimal_Q|630010849990532175|
|min optimal Q−W−Csum|−129762657896820300|
|refutes_StrongA/refutes_HALF|true / false|
|refutes_some_optimal_assignment_weakening/universal_bound_proved|false / false|

所以StrongA全人数全SPE断言确被此m5点否定，half余量2W−OPT=682460578423027800>0。弱化为存在一个最优元组及指派时，此点有明确便宜的合法解；更不能把各行最大者(2,2,2,2,1)未经覆盖检查就当最优比较。packet的true_maximizers是每行**一个选取标签**，不是全部并列argmax集合；5026重新算全部8列最大值之和，并未单独assert该五标签字段列完所有平局。

主稿/tree旧review另给实际利润(142400688797178900,142400688797178900,142353183896993025,142353183896993025,152516641360396500)，前四frozen regret各10115952563217600、末位0。四边钱包为(0,17765105218601400,0,19984015920010725)。这些原细分值及“完整平局在tree输出”均如实保来源；本5026输出未单列完整frozen矩阵、利润向量、分边税或全tie集，不将934字段范围借给缺失tree输出。其完整全树IC/Q/Csum/J/OPT及最优minQ则已由本原main直接算出并与原值同。

## 5026原实现实际检查了什么

程序只用标准库，真实读取相邻strong_adjacent_gap_attack.json的endpoint和strategy。类型以(frozenset兴趣,正整数重数)保存，不逐个分配巨大客户列表；其精确重数求和等价这么多不同单位客户各给1/覆盖人数。没有规范solver/model/verifier、SciPy、cone或发现器导入，不把大整数合并计算称带权提供者。

1. 对全部actions收history→action，拒重复h；expected={0,…,7}^d、d0…4逐项核key集合及动作域。terminal(h)按完整h自己的处方继续；只有terminal所得终局计数被缓存作收益，不合并同计数的策略历史。
2. L=lcm(1,…,m+1)=60，以整数倍算终局各标签利润；每非规定b沿真孩子h+b再按σ完成，比较当前人真实收益，32767项均非负。重数为正int，所有所用分母正且整除L。
3. actual路径与packet.actual_path及terminal_counts逐项核。对path中每个角色分别删除原action/插查询，算完整5×8 frozen矩阵；重复5/0行分别保份数，Q取五行最大和。按同一actual顺序逐型算所有相邻退出次数、Csum和J。
4. OPT只枚C(8,5)=56个五个不同标签组合。覆盖单调，任何至多五个不同标签支持都可补成五个，故此足含重复的OPT5；并非遗漏重复比较。随后另枚product(range8,repeat5)全部32768个有序比较，缓存支持覆盖，只有840个最优者计数并逐角色算frozen和取最小；有序坐标已给全部角色指派，重复1保留，不另强制比较标签互异。
5. 先从定义算W/OPT/Q/Csum/gap，再assert与原字段同、gap>0及half；已知字段不是取代全IC计算。最后返回完整934字段。原代码依赖assert，main没有拒绝关闭断言的模式；本次用普通Python命令，不对关闭断言输出授核验合同。

原main先拒已有同名报告，运行后写相邻新934并打印完整单行836B JSON。路径依HERE，与cwd无关；本包只需原5026+原563651输入，runtime闭包自足。不取源文件指向的repeated_upgrade_attempt_m5、LP脚本或tree另一个审计来“凑依赖”。后者是来源谱系材料，不被此main读取。

# 发现过程字段与端点数学不互换

raw保source_file=repeated_upgrade_attempt_m5.json，以及原seed五行八列source_frozen_payoffs；那些40个值对应source_W44924837031、source_Csum2140620747、source_Q46065063663、source_signed_gap−1000394115。它们是**压力前的旧seed**，不是本巨大endpoint的矩阵。负source_gap与正端点gap并不冲突；固定查询(2,2,2,2,1)后重加权造成分离。

source的40个字符串与全部元数据已无损保/全文读；当前5026没有读取source_file或复算这些旧seed值。主稿称在已有完整策略锥内、允许全部255非空型、固定查询/W1做float LP，再有理恢复/整数化/全历史接受。本raw只交59正型端点与全策略，floating_status=HiGHS Optimal仅历史数值状态；exact_primal=true按精确可行证据保，不等全策略/所有输入最优。

fixed_query_dual_bound为null、dual_support为空，所以没有原精确dual最优证书。seconds20.714152067000214是旧发现字段，不是本次审计耗时。原ratio440874/417971及normalized_fixed_gap3143/835942按原精确字段保存；5026主要assert清单不单独检查这两个字符串或source矩阵。本次成功不借给原发现LP最优性/求解器环境/最小客户数。主稿的简化尝试超时且无可用点也只保其历史，不取未运行的simplified packet冒新证据。

# 两个独立审计和三个后续量词

5026及934是credible侧原标准库实现，当前恰一次重放它。2954B tree稿日期2026-10-24，自述仅先读raw整数客户及完整策略、未读/导入作者发现/核验/规范oracle，另写Fraction审计；它声称4681/32767、全部792五槽多重集OPT、全利润与各行ties。这个原内部先验比当前知情清洗不同；本五源没有tree所指audit_strong_adjacent_raw_packet.py或它的JSON，**没有为tree另跑一次或授原代码已读**。

tree稿说未测弱最优指派，credible5026却枚840个最优有序指派；两者是不同实现范围，不是矛盾。56个不同支持算OPT（credible）、792多重集算OPT（tree原说）、32768有序比较中840最优逐指派（credible）也有不同用途，不能混作同一个循环数。

| 对象与当前状态 | 确切作用 |
|---|---|
|本五人raw|StrongA失败；840最优指派中minQ低于W+C_adj，故本点不反存在版|
|既有十客户三人compact|rowmax、每个最优指派和每个共同query加强失败；真正minQ6仍通过存在版；21节点原成功仍只属它|
|后继唯一最优支持全m族|[正式反族](../反例/唯一最优支持下相邻钱包的固定倍数反族--反例.md)给W=m²、C_adj1、minQ−W=(m−4)/2；m≥7才严格反存在版/任意固定倍数，m6恰等号|
|末对钱包/静态直接吸收/净ROW/half|没有被上述机制反例连带否定；直接EARLY仍需独立金额，五人half当前另证|

主稿顶部已将存在版一般状态追补为“另由root全人数族否定”，而§4早OPEN及冻结934的false只描述早期/此输入。保全部原字节及读序，不把此点成功改成一般仍OPEN，也不把后继m7失败塞进本m5报告。更宽有利最优Q≤(1+1/m)W与真实净差付款量词另保，本批不关闭。

# 当前唯一执行及保存

Python3.12.14普通命令在新隔离原布局恰一次，exit0、elapsed0.1605624270014232秒、stderr0、原生stdout836B；新934 SHA55709c51b7a83e2fa86dd1a7736f919bb7c6b4ecdd6e27a8f5cb61367ccfad2a，与冻结报告全字节同、全部字段无差。code和raw原件/隔离副本前后SHA均同。完整实际argv/cwd/退出/耗时/stdout/stderr、前后指纹及全部新文件另附execution.json，非只一句PASS。

没有重跑solver、compact、tree、额外scanner或自写数学checker；全历史可逆视图只改排版、JSON值还原逐字符同。原11WQ实际pushed/synced和五normalshow如实保，Root串行白名单checkpoint/done，子线程不Git/start/claim/done。当前知识只对这份明确raw证书新闭合实际复现，不认证全m上界、外审或新颖性。
