---
id: customer-attraction/tail-profit-bellman-and-weak-gap-finite-diagnostic-programs
kind: program
type_tag: 程序
title: 剩余利润Bellman与弱缺口的有限诊断程序
status: seven-originals-completely-read-two-reports-retained-no-new-math-execution
truth_status: exact-finite-family-values-and-correct-diagnostic-objectives; weak-gap-universal-payment-unproved
review_level: 五源码全部分支、两JSON全部字段、规范依赖与成熟解析证明比较；0旧程序重跑
scope: 有限单位客户和非空共同目录；合法计数背景下完整有序历史纯SPE可实现终局；单个固定策略锥数值搜索
summary: 首次补齐交叠族尾利润有限审计、三种缺口诊断和34锥967LP原报告的真实合同；明确0.75优化的是归一O−m u，违例阈值1，既无精确对偶也未交完整策略清单。
source_ids: [da34be591dce00f9e47c, 38fb03cf0f5bbd051d5d, 80a6bb29f0afc92b5f50, 80c213d609b69da08b03, 6b88bf8a279be9be244f, b2c67f5ac6b0977c7fe1, aa7482f6d9c82cd45db7]
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/round5_induction/audit_profit_bellman_family.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/round5_induction/background_gap_diagnostic.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/round5_induction/bellman_diagnostic.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/round5_induction/profit_bellman_family_exact.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/round5_induction/weak_gap_cone_probe.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/round5_induction/weak_gap_cone_probe_exact.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/round5_induction/weak_gap_diagnostic.py
---

# 七源的新增身份

2125/1887/2476/2547/4045/503/1499B七原件共15082B，五PY全文与两JSON全部字段实读，双冻结提交同字节，逐size/SHA保全于[证据目录](../../tools/evidence/Boss7-resume-d22-induction/README.md)。既有[机制入口](../资源/一般机制入口的有限诊断与未付合同--资源.md)与[背景信用资源](../资源/背景信用的诊断范围与原稿证据合同--资源.md)当时明确“未读原码/报告”；本页补这一缺口，不把本批实读倒填成旧轮已经执行。

本批没有import或执行任何原数学程序，没有BI、LP、收益/IC重算、参数扫描或新数学checker。原保存报告的有限数值、实际代码能证明的合同和现成熟一般解析证明分别保留；代码存在和文件名含`exact`都不自动认证原运行或普遍命题。

## 模型及四个不同目标

采用[共同目录完整历史定义](../定义/共同目录完整历史模型--定义.md)，有限不同单位客户、非空共同目录、单位玩家，任意离轨平局、重复行动、空主题、同覆盖异标签和零客户都保留。以下软件的有效数学域取m≥1、k≥1；规范模型另允许零玩家边界，但这组诊断有min空集等分支，不能据导入包的边界健壮性假定其main也支持零玩家。

合法过去计数b∈Z_+^k、|b|≤m，余r=m−|b|。对一个客户x，b_x为过去负载；未来r槽计数q给c_x(q)。定义

\[
 F_r(b)=\max_{q\ge0,\,|q|=r}\sum_x\frac{c_x(q)}{b_x+c_x(q)},\quad F_0(b)=0,
\]

零分子项按0。真实SPE终局c≥b中未来负载q=c−b，未来总利润P=Σ_t q_t U_t(c)，最小未来玩家利润u_min=min_{q_t>0}U_t(c)。F是**剩余玩家利润最优**，不是含过去的覆盖补全或静态额外查询值。四类目标准确区分：

| 程序所检验对象 | 精确条件/余量 |
|---|---|
| 局部利润Bellman | 2u+F_(r−1)(b+e_a)−F_r(b)≥0 |
| 零根弱机会缺口 | m·min实际u+W−OPT_m≥0 |
| 完整终局插入保底 | min实际u−max_A Σ_(x∈A)1/(1+c_x)≥0，竞争中保全部m槽再加query |
| 合法背景弱机会缺口 | P+r·min未来u−F_r(b)≥0 |

插入式与含W的弱缺口不是同一命题。若背景式普遍成立，r u_min≤P给F_r≤2P，零根F_m(0)=OPT、P=W才推出half。有限无违不证明这个前提。局部Bellman已由[两个完整SPE族](../障碍/最优剩余利润的局部系数与共享负载信用--障碍.md)否定，即使任意人数无关有限系数也不够；这些失败没有否定背景式或half。

# 规范依赖怎样保完整历史量词

三诊断导入的`customer_attraction`和弱锥导入的`customer_attraction_strategy_lp`已从现成准确冻结副本实际读其所需定义；[依赖指纹/范围](../../tools/evidence/Boss7-resume-d22-induction/dependency-closure.json)列文件和SHA。模型、ExactSPESolver、证书校验器全文核过；StrategyCone/顶点恢复/克隆/独立校验/序列化定义实读。未额外认领这些依赖或重复复制已有完整数学。

集合值求解器对计数前缀b缓存**所有**可实现终局R(b)，非终局满足

\[
 \theta(b)=\max_a\min_{c\in R(b+e_a)}U_a(c),\quad
 R(b)=\bigcup_a\{c\in R(b+e_a):U_a(c)\ge\theta(b)\}.
\tag{1}
\]

必要性来自真孩子的收益不小于其可实现最小值；充分性将所选孩子的目标与每个其它有序行动孩子的最差可信续局独立拼接。按有序历史可分别破平局，计数缓存没有强迫相同计数历史共用动作。全部收益和阈值用Fraction；它枚举终局集合而非所有完整动作图，也无多项式时界保证。

`certificate(target)`默认在每历史选首个admissible行动、其它孩子选按终局字典序的最低偏离利润目标，展开全部有序历史。StrategyCone再要求动作表恰含全部k^{<m}历史，对真实两枝终局建Γ，非负类型w使Γw≥0恰保该固定σ为SPE。导入的`verify_certificate`另从完整树逐枝检查，不调用终局求解器；这些实现职责不等于本批实际运行它们。

# 交叠族尾利润审计与完整五行报告

`audit_profit_bellman_family.py`只用标准库Fraction，无模型/BI导入，实例在函数中写死为n≥4、k=n+2标签A0、B1、叶2,…,n+1。x=n−2；每叶j有{L_j}:x及{B,L_j}:x；普通叶j<n另{A,L_j}:1，特殊叶另{A,B,L_n}:n−1。每个重数是不同单位客户，总N=2n²−2n−2。背景固定一份A，余n−1槽。

`profit`逐类型计算w·c/(1_{A∈type}+c)，只在c>0时取分数，故正是此背景的未来总利润。main以`combinations_with_replacement(range(k),n−1)`枚举全部计数，不扫描SPE策略。它断言最大值为

\[
 F_{n-1}(1_A)=2(n-1)(n-2)+(7n-13)/6,
\tag{2}
\]

并另断言指定计数“一个B、一个特殊叶和n−3个普通叶”取等。原代码把u=n−1/n、OPT=N代入报告，但**没有**验证完整SPE或其实际根利润；这部分由成熟[全历史交叠族及整数消元](../障碍/最优剩余利润的局部系数与共享负载信用--障碍.md)承担，不能从有限最大化推回一般完整策略。

报告根字段scope、rows共2项；每行恰n/customers/candidate_profiles/F_tail/expected/argmax/specified_argmax/root_utility/OPT/bellman_slack/required_coefficient共11字段。完整值如下，未省略任一字段的独有数学。

| n | N=OPT | 候选计数 | F_tail=expected | u | 2u+F_tail−OPT | (OPT−F_tail)/u |
|---:|---:|---:|---:|---:|---:|---:|
| 4 | 22 | 56 | 29/2 | 15/4 | 0 | 2 |
| 5 | 38 | 210 | 83/3 | 24/5 | −11/15 | 155/72 |
| 6 | 58 | 792 | 269/6 | 35/6 | −3/2 | 79/35 |
| 7 | 82 | 3003 | 66 | 48/7 | −16/7 | 7/3 |
| 8 | 110 | 11440 | 547/6 | 63/8 | −37/12 | 452/189 |

候选数总15501，分别是C(2n,n−1)。n4的argmax=(0,1,1,1,0,0)，specified_argmax=(0,1,1,0,0,1)，为不同的等号计数；n5…8两个计数均相同，依次(0,1,1,1,0,0,1)、(0,1,1,1,1,0,0,1)、(0,1,1,1,1,1,0,0,1)、(0,1,1,1,1,1,1,0,0,1)。原argmax在严格改善时才更新，是组合枚举中的首个最大点，不能改写为唯一最大点。

默认`--max-n 8`，可选`--output`。不读外部实例；max-n<4会给空rows。指定output已存在时在全部计算后抛FileExistsError，不覆盖；不创建父目录，成功写JSON后向stdout打印同一data。JSON没有argv、代码SHA、耗时或完整运行事件，虽与默认n4…8相合，也不伪造历史调用。assert在优化模式会失效，本批未调用它；普遍(2)来自成熟解析而非15501有限外推。

# 三种精确诊断器的全部遍历与输出边界

三个脚本均用`Path(__file__).resolve().parents[5]`定位**旧源码布局**的根，插入sys.path，再遍历按文件名排序的`examples/customer_attraction/*.json`。归档副本不能仅靠文件名假定已经具备这些输入布局。原examples目录的完整当时清单/SHA不在这两JSON里，不能由源码过滤条件回填原实际输入数。

## bellman_diagnostic.py：一节点可实现性及F缓存

`counts(k,n)`枚举全部n槽计数。`check(ins)`先求solver.outcomes()，fp(b)将F_r(b)及一个argmax按b缓存，枚举全部余r槽，以Fraction求剩余利润。F0或全零最优时best初始化0且只接受严格改善，所以arg可保持None；它不表示最大值不存在。

随后遍历全部深度t=0,…,m−1、全部计数b、每合法行动a和c∈R(b+e_a)，仅保U_a(c)≥θ(b)。由(1)，这恰对应当前行动a和该孩子目标能接成一份可信父子SPE；它不是只查actual路径，也没有逐一枚举全部完整σ。计算slack=2U_a(c)+F_(r−1)(b+e_a)−F_r(b)，保最小值及prefix/action/terminal/r/u/F_r/F_tail/optimal/tail_optimal/slack共11字段的witness。

main只收k≤7,m≤5，不捕获格式/求解异常。每实例打印source、slack、checks；第一次负值打印COUNTEREXAMPLE后停止，再打印instances/checks/minimum/witness聚合。无CLI、无写文件；这九源中**没有**配套保存stdout或原诊断JSON。本源码本身不能认证某次实际找到了哪一个22客户终局。

## weak_gap_diagnostic.py：根缺口与完整m槽插入

对每个根可实现终局c，计算W、OPT、所有已占标签利润最小u，及

\[
 I(c)=\max_A\sum_{x\in A}\frac1{1+\sum_{t\ni x}c_t}.
\]

这是真实完整m槽后再加一个独立查询，分母有额外1，不能换成删当前m−1槽或自由分数背景。每终局记录六元组(m u+W−OPT,u−I(c),c,W,str(u),str(I))；函数返回字典序最小的缺口tuple、按第二分量最小的插入tuple、终局数。两种最小值可能来自不同终局。

main过滤m≤6,k≤10，每例仅打印source/gap_slack/insertion_slack/outcomes；只有弱缺口负时打印WEAK_GAP_FAILURE及完整gap tuple并停止，单独插入负不使它停。最后打印minimum_gap/source/累计outcomes。没有写文件/CLI/保存插入witness完整字段；本批不从入口一句“插入曾失败”补造缺失的具体值或全目录结论。

## background_gap_diagnostic.py：所有合法b下剩余玩家最小值

它复用同目录bellman的`counts`，逐深度i=0,…,m−1与每b计算F_r(b)，然后对每c∈R(b)置q=c−b，读取P=Σq_tU_t(c)、u=min_{q_t>0}U_t(c)，检查P+r u−F_r(b)。不是把过去玩家也放进min或P。witness恰prefix/terminal/r/minimum_payoff/profit/F_r/optimal/slack八字段。

main过滤m≤5,k≤7，逐例打印source/slack/checks，首个负值打印FAILURE再停止，最后聚合instances/checks和最坏minimum/witness。没有文件写出或CLI，依赖导入也不自动main。成熟入口报告19输入/2503个背景-终局计数是原Markdown自述；本批九源没有对应完整stdout，不将源码阅读全文升级为新的19/2503精确运行。

# 弱缺口固定完整策略锥LP与503B报告

`weak_gap_cone_probe.py`导入NumPy/SciPy/HiGHS和上述规范包，另用固定完整策略锥助手。它只对k≤6、m≤4的既有实例，按(welfare,min占用标签利润)对根终局排序取前至多2个；相同排序键没有追加终局字典序键，frozenset来源的平局次序未被另记录。每目标只取规范certificate的一份默认全历史策略，不穷尽同一终局的任意离轨平局选择。

对每个已占标签t和每个大小min(k,m)的不重复主题support，设置o为support覆盖行、p_t为该固定终局一名选t玩家的收益行，求

\[
 \max_{w\ge0}\ (o-mp_t)\cdot w,
 \qquad \Gamma_\sigma w\ge0,\quad c_\sigma\cdot w=1.
\tag{3}
\]

类型是全部2^k−1非空兴趣mask。覆盖单调，任意至多m主题支持可扩成大小min(k,m)，所以扫描这些support不遗漏该固定锥的最佳覆盖目标；重复槽不增覆盖。实际同标签玩家利润相同，遍历占用t足够表示每个实际玩家。归一的是**这份固定σ的W**，不是OPT或新权下全部SPE的最小福利。

目标值超过1，才可能反OPT−W≤m u_i；阈值不是0。每次LP后先更新maximum_float/argmax，若val≤1+10⁻⁸就继续；否则逐分量Fraction(float).limit_denominator(10⁷)，核w≥0、Γw≥0及W1，不通过时以活跃支持的有理消元`recover_vertex`恢复，仍不通过就跳过。恢复后还须精确(o−m p_t)w>1，清共同分母并约gcd成单位客户克隆，执行定义级全历史`independently_verify`以及规范完整树校验器两种检查，另精确算真实OPT、W、u并断言OPT−W>m u。

只有这一链通过才保存counterexample，字段为source/instance/strategy/player_topic/W/OPT/u/slack/portfolio/clones/normalized_objective；否则counterexample保持null。浮点失败直接抛RuntimeError，不自动当无违；未保存点也不证明不存在。输出固定覆写同目录`weak_gap_cone_probe_exact.json`，每target打印进度，找到精确反例即写并返回，正常结束最后写完整报告；无CLI、不拒覆、不建目录。导入助手的其它发现main未被本源调用。

503B冻结报告全部内容是：scope=`selected complete-policy cones, single weak gap objective, finite diagnostic only`；candidate=`OPT_m-W <= m u_i for every actual player`；cones34、lps967、maximum_float0.75、counterexample=null；argmax的source为prefix_balance_failure.json、terminal=(0,1,3,0,0,0)、player_topic1、portfolio=(0,1,3,4)；elapsed_seconds=5.082569599151611。

这些34是构造计数，不带动作表/哈希或跨输入去重，不能认证34份彼此不同σ。报告没有每LP primal/dual、精确残余、输入清单、求解器版本、全部Γ或完整34策略；**0.75不是已认证的精确3/4上界**，更非一般弱缺口定理。按本码与此报告相容的执行，最大值没过1，所以不会触发精确候选恢复；文件名`exact`不能补一份Farkas证书。最坏argmax只定位seed锥/目标，不存其优化后客户w，不能拿seed原重数冒这0.75的有理取等点。

该seed的准确[原fixture](../../tools/evidence/root-tail-probe-scope-and-report-check/source-root/examples/customer_attraction/prefix_balance_failure.json)为四人、六主题(L0,A,B,L1,L2,L3)、22单位客户，是交叠族n4的标签重排；它与前面硬编码A0/B1/叶2…的标签编号不同。程序原始输入与LP开放类型后的可变客户是不同对象。

# 当前状态、复用和接续

这批源码补的是正确有限查询和输出边界，不新授Bellman无限族证明或弱GAP普遍真值。一般[背景最小收益差额候选](../候选/真实尾部最优利润的最小收益差额候选--候选.md)的一/二人解析基底、伪孩子障碍与相同变量下的含符号债仍独立适用；这些脚本没有把局部充分式失败升级成half失败。

两JSON都是原有限报告，没捏造它们对应的历史stdout、argv或exit。三diagnostic无本批运行记录；weak锥既不重跑967LP，也不为0.75再做无必要恢复。若以后得到新的严格候选，应保原完整有序σ/客户/精确IC和实际OPT；若只求该有限锥的阴性认证，需补逐类型有理对偶，不能拿次数替证明。当前[六人目标](../../subarchives/six-providers/问题--问题.md)未由这里闭合，五人half他证也不倒证这些强辅助桥。关系是程序实现(1)、有限家族回归(2)、发现器(3)及有限状态报告，正式超图留第三阶段。
