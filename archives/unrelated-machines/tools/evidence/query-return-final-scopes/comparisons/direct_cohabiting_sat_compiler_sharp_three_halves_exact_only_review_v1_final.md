# 直接共居 SAT compiler 的精确三半阈值：statement-first 独立审查

审查者：general_query_response_review。2026-10-18。

## 1. 输入、实际读取与正式范围

本轮仅读：
/workspace/scratch/038d9dcc4cac/weighted_direct_cohabiting_query_return_all_formula_failure_exact_v1.md

SHA-256：076561e78796927d6792f6dfb3c581c11afd263752b9098abd9f35d58df2ddfb。

另据root消息中的新精确陈述，正式审查UM-DIRECT-COHABITING-SAT-COMPILER-SHARP-THREE-HALVES-v1：同一原P，全部真实occurrences的x_i=y_i=1/2，dummy x_i=1，3/4<rho<1；非空UNSAT实例actual OPT=3/2，非空SAT实例actual OPT=1；任意完整C<3/2实际调度可det-bit-poly解码SAT。

所见source是完整矩阵定义及既有strict/全公式上界、算法分支合同的陈述，其中已陈述baseline上界物理分支；本次不宣称未见这些已给结论。未读取作者Proof、其它agent输出或root策略，新fixed-half阈值的下界/解码由以下原矩阵计数独立推出。全部所需结论在本记录重证，不把source中尚无证明的身份合同当成引理。

正式认证仅这个fixed-half新Claim，不认证任意异权active-branch共同matching的全公式定理。仅scratch新增，无repo/Work/Git修改。

**明确结论：新Claim有效，无fatal。全部原jobs、任意合法额外query exports/returns、dummy及重复文字/变量均被覆盖。**

## 2. 核心低于三半的实际容量计数

设非空实例有N个索引、N台M及N台C、N件q与N件b，另外m件u。取任意完整实际调度，峰C_max<3/2。

每件在M上的q或b，其时间至少rho；两件总时≥2rho>3/2。因此每台M至多一件q/b。u没有M资格。

C_i上可执行的q/b只有同编号q_i、b_i。真实q_i耗时1/2，dummy q_i耗时1，b_i耗时1，所以两者同居至少3/2。当前严格阈值下，每台C也至多一件q/b。

全部2N件q/b只能在这2N台M/C执行，每台至多一件。因此每台M、每台C都恰执行一件q/b。这是对实际调度的强迫结论，不是预设同编号返回；u可能共居但不改变q/b的计数。

尤其对每个索引i恰有：

- q_i在C_i，当且仅当b_i不在C_i，即b_i在pin(i)；
- b_i在C_i，当且仅当q_i在其两个环内M端之一。

因此每对(q_i,b_i)恰有一件留C_i、一件在所属变量的M环。此处允许dummy q导出、额外真实q导出、任何合法未规范化返回，均没有先行禁止。

## 3. 一致环方向与SAT解码

对每索引i，令e_i为(q_i,b_i)中实际位于M的那一件。它的端必为M_i或M_(i+)。定义h_i=0表示e_i在M_i，h_i=1表示e_i在M_(i+)。若e_i=b_i，则由pin定义必有h_i=s_i。

固定一个变量的环。M_i上的e-job数量恰为

(1−h_i)+h_(i−)。

上节已强迫它等于1，故h_(i−)=h_i。沿环所有h_i同一常数z_v∈{0,1}。Padding保证环长至少3，所有端标识明确；不同变量M环隔离。

任意clause原job u_c只能在某真实occurrence i∈c的C_i上耗时1/2。该C_i不能同时执行b_i，因为1+1/2=3/2超过当前严格峰；而每C_i已恰有一件q/b，所以它必执行q_i，进而b_i在pin(i)，故s_i=h_i=z_v。

令Boolean变量v在z_v=0时取True，在z_v=1时取False。按源polarity正文字0、负文字1，s_i=z_v恰说明所选occurrence的literal被满足。每clause自己的实际u目的地都给出这样一个满足literal，因此解码出全Φ的满足赋值。

重复文字、同clause重复变量和重复clauses都无碍：每枚实际occurrence有独立索引，u只用其自身clause的真实occurrences，不能去dummy。Dummy返回若发生，只给同一z_v附加一致方向，不会充当clause证据。

解码只扫描原assignment、按job身份和实际端读e_i/h_i并沿显式环检查，再输出每变量一位；按显式N、L、输入有理位长deterministic polynomial。不需要匹配oracle、搜索SAT赋值或规范化调度。峰承诺下，任何额外合法exports/returns均已被同一计数覆盖。

于是UNSAT实例不可能存在C_max<3/2的完整actual。

## 4. 所有公式的完整三半上界

固定半权后可直接给出共同原端assignment，无须general异权active分支：

- 每个q_i放M_i，耗时rho；
- 每个b_i放C_i，耗时1；
- 每clause任取一枚真实occurrence i∈c，把u_c放C_i，耗时1/2。

M_i上恰q_i、负载rho<1。每occurrence只属于一个clause，所以不同clauses所选索引互异，每C_i至多额外一件u_c；其load为1或3/2。Dummy没有clause资格，只承载b_i。全部2N+m件原jobs各一次，没有virtual执行端或删除的未选任务。

非空时至少一个u存在，因此这份调度峰恰3/2。结合上节，所有域内非空UNSAT Φ的actual OPT精确3/2。由于这些UNSAT的完整等号witness存在，解码阈值严格小于3/2是sharp，不能扩成≤3/2。

## 5. SAT时完整unit调度与非空下界1

给任意满足赋值，按前节规则设每变量方向z_v：True→0、False→1。每clause选一枚满足occurrence i；令E为这些选中的真实索引。各clause的occurrences独立，E中的索引不跨clause复用，且每i∈E满足s_i=z_v。

- i∈E：q_i放C_i；b_i放pin(i)，与方向z_v一致；该clause的u_c也放C_i。
- i不在E，含所有dummy：b_i放C_i；q_i沿方向z_v放M_i（z_v=0）或M_(i+)（z_v=1）。

每变量环沿同一方向，因此每台M恰一件原q或b，耗时rho或1。选中C_i的两件q_i+u_c耗时1/2+1/2=1；其它C_i只有b_i，耗时1。所有原jobs完整执行，峰≤1。

任何非空实例均不可能峰<1：若有这种调度，它也低于3/2，故§2强迫每C_i恰有一件q/b。任取一clause，其u_c在真实C_i上。若该C有b_i，负载至少3/2；若有q_i，真实q耗时1/2，与u共居load1。两种都不可能低于1。因而非空SAT实例OPT恰1。

空公式依原定义输出idle机器及零jobs，OPT0；不被误纳“非空SAT OPT1”的结论。

## 6. 独立完整小矩阵穷举check

另按指定rho=4/5、Φ=(x∨x)∧(¬x∨¬x)从原资格独立生成矩阵。唯一变量四枚实际occurrences按正、正、负、负排序成4环，无dummy。原机8台、原jobs为4 q+4 b+2 u共10件、有限条目24。用整数10单位记录rho8、half5、unit10。

每q有3端、每b有2端、每u有2端，完整assignment数3^4·2^4·2^2=5184。实际枚举全部原有限端组合，最小峰15/10；低于15单位者0份，最优15单位者247份。一般解析lower已在§2–3给出，未以此有限检查替代。

检查文件：
/workspace/scratch/038d9dcc4cac/direct_cohabiting_sat_sharp_three_halves_independent_enum_v1.json

SHA-256：d7fb60f5c1857174868efe7366c3506ca6cacb2cf2710bfe37586113a3d2cad4。

文件含全部稀疏finite原矩阵、infinity语义、枚举总数/峰histogram、一份最优assignment及baseline完整assignment/load。未读取作者软件、未增加原资格；所用instance确实UNSAT，因为两clauses分别要求x与¬x。

## 7. 复杂度与范围

最少padding N≤L+2v；也允许更长显式dummy输入，所有算法按实际N。完整P的2N机器、2N+m jobs、5N+L finite entries及dense 2N(2N+m)计量保持原定义。参数rho按输入二进制有理，half与dummy unit固定；映射、解码和原机回算按显式总位长多项式，不按分母或接近阈值的倒数复制。

本Claim只给明示direct-cohabiting SAT矩阵固定半权下的精确YES1／NO3/2实际间隔；没有将fixed3/2作为near2 NO源、新颖hardness、一般medium接口不可能性或一般UM算法。任意异权的全公式active匹配合同不在本正式认证内。无其它Proof或agent推导读取，未改repo/Work/Git。

**最终statement-first冻结：新fixed-half sharp-three-halves Claim通过，无fatal；SAT非空OPT1、UNSAT OPT3/2及任意完整C<3/2的det-bit-poly SAT解码全部闭合。**

排版冻结说明：首写v1（SHA 7f9caf5f91d72a512f983c9b887e10e5adf64d5eaefd88ac7d53096489bacf5f）保原字节。本final只将§7一处非正式间隔写法精确为YES1／NO3/2，不改任何公式、证明或结论。
