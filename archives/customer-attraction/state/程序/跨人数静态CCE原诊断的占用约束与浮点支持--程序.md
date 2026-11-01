---
id: customer-attraction/population-cce-original-occupancy-lp-and-floating-support-scope
kind: program
type_tag: 程序
title: 跨人数静态CCE原诊断的占用约束与浮点支持
status: full-original-code-and-report-read; prior-inputs-exactly-reused; no-replay
truth_status: floating-proposals-only; general-PC-and-exact-CCE-feasibility-not-certified
review_level: informed-source-contract-and-all-field-report-analysis
scope: nine-given-m-player-paths-vs-m-plus-one-static-count-CCE-LPs
summary: 2312原HiGHS入口无SPE IC核，14227报告九组全部标量与51浮点支持保；n位置静态删插R/W占用LP定义正确，正gap不授精确CCE/最小值或half，0新run。
source_ids: [b8caf94b4052b9634e85, 607a9fe90134e4fc281b]
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/security_aggregate/population_cce_check.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/security_aggregate/population_cce_check.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/security_aggregate/population_cce_check.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/security_aggregate/population_cce_check.json
---

# 跨人数静态CCE原诊断的占用约束与浮点支持

2312B源码和14227B完整报告共16539B，均actual normal取得并全文主读。本次接续[跨人数CCE候选](../候选/跨人数静态粗相关均值与顺序福利比较--候选.md)此前仅据MD记录的有限诊断：补真实程序、九例全部字段与51个原浮点支持点，不重授占用LP或PC候选。原CLI/import、顺序IC/路径/H重放、profile枚举、LP和新数学实现运行均0；刚在pair包完整读过的九模型/九策略按同SHA精确复用。

## 当前代码只恢复旧路径，不重新认证SPE

源码导json/pathlib/Fraction/numpy/scipy.optimize.linprog，无main guard。import即扫描、恢复路径、列举占用、求LP、打印并覆盖同目录population_cce_check.json，不能当只读模块加载。ROOT=Path(__file__).resolve().parents[5]按原工作区层级取仓库根，OUT源码目录；无argv、输入/输出路径选项。

升序glob examples/customer_attraction/*.json，同名匹配evidence/certificates/customer_attraction；缺cert、strategy非dict或无actions则跳过。acts由history→action字典构建、重复history后项覆盖，仅以len(acts)==Σk^i筛选，未检查精确history域/动作范围/客户schema。与前包pair程序不同，**这里没有任何给定策略SPE IC断言**。只从h=()按acts追加至长度m，按输入客户重数求实际覆盖W；证书expected/security/CCE旁字段不参与。

原字段SPE_W/SPE_average是作者给已存在策略的命名，不是本程序重新证得SPE。当前九例输入/证书与刚全文读取的1469006B/12222动作全字节相同，精确复用原件和可逆depth/lex视图，不重复大表或旧IC；其余runtime文件仍仅目录过滤/字节保全，均不额外done。

## n=m+1是另一个同时行动游戏

同客户、同全部目录，但静态人数n=m+1；所有玩家同时行动。q为k维非负整数计数，Σq=n，允许重复主题。counts(k,n)按首坐标0,…,n递归后面的计数，k1时yield(n,)；这是所有占用向量的词典序枚举，不是顺序SPE集合或iid分布。

代码先完整qs=list(counts(k,n))，再在len(qs)>15000时直接continue，无记录该例；上限不是在枚举途中停止。已保存九例的profiles分别35…5005，均小于该cap；当前不重新列举6510个计数或运行LP。five行old players=5/new_players=6仅表示六人**静态**LP，不是六人顺序SPE实验或六人half认证。

每q客户负载v_x=Σ_(a∈B_x)q_a，W(q)=Σ_(v_x>0)w_x。固定主题a，原代码用Fraction算

\[
 R_a(q)=\sum_{x\in a,v_x>0}\frac{w_x(n+1)}{v_x+1}
       +\sum_{x\in a,v_x=0}w_x n.
\]

零负载项必须是n，不能把正负载公式延到0而得n+1。其意义是n个位置分别删去自己的原行动、改为固定a的收益总和：v>0时，v名原覆盖者每人得w/v，其余n−v人每人w/(v+1)，和w(n+1)/(v+1)；v0时所有人各得w。它与静态额外query“保全部n原槽再加一槽”的分母不同，也不涉及SPE真实后继响应。

## 玩家对称化与LP的正确含义

给定q后，均匀打乱n个玩家位置；玩家可以相关，主题没有被强制对称，每个q也不是iid product。此分布每人原收益W(q)/n，对事前固定a的偏离收益R_a(q)/n。因此q分布x满足全部

\[
 \sum_qx_q[R_a(q)-W(q)]\le0\quad(a=0,\ldots,k-1)
\]

就逐人满足CCE。反之任意CCE在玩家置换下对称化保福利和全部固定偏离约束，故最低福利可由这些占用变量精确表示。只有先作玩家对称化，k条聚合约束才能替代每人约束；这不是一般不对称分布只验总和，也不是条件于推荐行动的CE。

令C_n为全部静态CCE最低**总**福利。精确数学LP最小化Σx_qW(q)/n，值C_n/n，变量x≥0、Σx=1及上面k行。代码将reg=R−W转float，A_ub=reg.T、b_ub=0，A_eq一行1，bounds=(0,None)，HiGHS最小化float(wc)/n。没有把query与当前推荐行动绑定，没有从原顺序策略限制静态支持，也不要求每个支持q自己是均衡。

## 本报告的浮点性质及正负gap各需什么证明

res.success时记录res.fun与W/m−res.fun，仅把res.x中v>1e−8的项写入support；没有重归一、Fraction重构、精确CCE残差、完整res.x、对偶或匹配下界。被阈值删掉的非零小权重未知，已存support的概率和/重算目标不应被强行当精确1或res.fun。浮点里的两个近似相等概率也照原小数分别保留，不合并为猜测有理数。

失败分支两个数值为None且不写support；九条实际都有数值和support，符合该版本success分支结构，但原JSON没单存HiGHS status/message/迭代或运行绑定。源根status只是finite floating LP diagnostic only，不断言PC或逐例CCE认证。

若要证明某给定例的PC，一个精确可行CCE且平均福利≤旧W/m就足够，不必证明它最低；本51个浮点点没有这种精确可行性证书。反向若出现负float gap，要反PC还须认证全部CCE的最小值确高于旧W/m，不能仅用一个高成本可行点或近似res.fun。本报告九个gap正，也不自动证明九例的精确PC，更不外推全实例/全SPE。

## 原三个外层字段与九行所有标量

status="finite floating LP diagnostic only"，claim="min CCE_(m+1) W/(m+1) <= SPE_m W/m"，rows九项，每项恰instance/players/new_players/SPE_W/SPE_average/profiles/CCE_min_average_float/claim_gap_float/support九字段。下表全部八个标量并保支持数；小数按原JSON可回读表示，不作有理化。

|instance|players|new_players|SPE_W|SPE_average|profiles|CCE_min_average_float|claim_gap_float|stored_support|
|---|---|---|---|---|---|---|---|---|
|aggregate_theta_failure.json|3|4|34|11.333333333333334|126|8.303571428571427|3.029761904761907|6|
|empirical_iid_kernel.json|3|4|7|2.3333333333333335|35|1.6590909090909087|0.6742424242424248|3|
|five_individual_security.json|5|6|85|17.0|5005|13.997139826241089|3.0028601737589113|6|
|global_decorrelation_failure.json|4|5|85|21.25|252|16.50866274594872|4.741337254051281|5|
|individual_security_failure.json|3|4|32|10.666666666666666|126|7.963153384747217|2.7035132819194487|5|
|local_security_increment.json|3|4|105|35.0|126|26.362380626235982|8.637619373764018|7|
|optimal_last_query_failure.json|4|5|1559|389.75|462|301.7693210343216|87.98067896567841|8|
|root_stationary_kernel.json|3|4|17|5.666666666666667|126|4.1368421052631525|1.5298245614035144|6|
|root_tax_failure.json|4|5|38|9.5|252|8.323201139871767|1.1767988601282333|5|


profiles是静态n人数的全部计数列数，九项原计数合6510，不是6510份完整SPE或本次LP运行；51个已写support atoms与51个runtime JSON只是两个恰好相同的数量。旧SPE福利是总W，SPE_average=W/m，LP目标是新人数的平均C_n/n；不能把res.fun直接当总CCE福利或以支持点W≤旧W作候选定义。

## 全部51个原支持点

每项三字段counts/probability_float/W全部保留；counts索引按该原模型主题顺序，位置均匀化是LP的数学解释，不是这些数组本身保存了n!个排列。原完整模型/证书闭包另存。

### aggregate_theta_failure.json

|原序|counts|probability_float|W|
|---|---|---|---|
|1|`[0,0,0,0,2,2]`|0.05288461538461537|33|
|2|`[0,0,0,2,2,0]`|0.05288461538461537|33|
|3|`[0,2,2,0,0,0]`|0.2799908424908425|33|
|4|`[1,1,0,1,0,1]`|0.10714285714285714|35|
|5|`[2,0,2,0,0,0]`|0.2799908424908425|33|
|6|`[2,2,0,0,0,0]`|0.22710622710622708|33|

### empirical_iid_kernel.json

|原序|counts|probability_float|W|
|---|---|---|---|
|1|`[0,0,0,4]`|0.09090909090909091|5|
|2|`[0,2,0,2]`|0.8181818181818181|7|
|3|`[0,4,0,0]`|0.0909090909090909|5|

### five_individual_security.json

|原序|counts|probability_float|W|
|---|---|---|---|
|1|`[0,0,0,0,0,0,0,0,0,6]`|0.0017833718507195267|65|
|2|`[0,0,0,0,0,1,1,1,1,2]`|0.19364983346492476|85|
|3|`[0,0,0,0,6,0,0,0,0,0]`|0.01596179069577507|65|
|4|`[1,1,1,1,0,0,0,1,1,0]`|0.33112889581178384|84|
|5|`[1,1,1,1,0,1,1,0,0,0]`|0.3311288958118003|84|
|6|`[1,1,1,1,2,0,0,0,0,0]`|0.12634721236499213|85|

### global_decorrelation_failure.json

|原序|counts|probability_float|W|
|---|---|---|---|
|1|`[0,0,3,2,0,0]`|0.26328442219637793|83|
|2|`[2,0,1,0,0,2]`|0.22272161335631266|85|
|3|`[2,0,1,1,0,1]`|0.024103559341196974|89|
|4|`[2,1,2,0,0,0]`|0.48151914975562726|81|
|5|`[3,0,0,2,0,0]`|0.00837125535048387|73|

### individual_security_failure.json

|原序|counts|probability_float|W|
|---|---|---|---|
|1|`[0,0,0,0,0,4]`|0.024850042844901814|21|
|2|`[0,0,0,1,1,2]`|0.1996572407883468|33|
|3|`[0,0,4,0,0,0]`|0.024850042844901468|21|
|4|`[1,1,0,1,1,0]`|0.5509854327335076|32|
|5|`[1,1,2,0,0,0]`|0.19965724078834898|33|

### local_security_increment.json

|原序|counts|probability_float|W|
|---|---|---|---|
|1|`[0,0,0,0,0,4]`|0.036985044779464064|68|
|2|`[0,0,4,0,0,0]`|0.03422109299808721|67|
|3|`[0,1,0,1,1,1]`|0.14088221852789296|110|
|4|`[1,0,1,1,1,0]`|0.24389866677565983|108|
|5|`[1,1,0,1,0,1]`|0.22790085155301978|108|
|6|`[1,1,0,1,1,0]`|0.19399985958115895|107|
|7|`[1,1,1,0,1,0]`|0.12211226578471718|110|

### optimal_last_query_failure.json

|原序|counts|probability_float|W|
|---|---|---|---|
|1|`[0,0,2,0,0,3,0]`|0.011449433973292351|1248|
|2|`[0,0,2,3,0,0,0]`|0.14284351118043276|1248|
|3|`[0,0,3,2,0,0,0]`|0.09960390438481517|1248|
|4|`[0,2,0,0,3,0,0]`|0.01339212159801408|1248|
|5|`[0,3,2,0,0,0,0]`|0.0010333393972039875|1248|
|6|`[1,1,0,0,1,1,1]`|0.7166115526685237|1612|
|7|`[2,0,0,0,0,0,3]`|0.007533068398348871|1248|
|8|`[3,0,0,0,0,0,2]`|0.007533068399581717|1248|

### root_stationary_kernel.json

|原序|counts|probability_float|W|
|---|---|---|---|
|1|`[0,0,2,0,0,2]`|0.3879699248120281|14|
|2|`[0,1,0,2,1,0]`|0.22406015037593943|19|
|3|`[2,0,0,1,1,0]`|0.12631578947368247|17|
|4|`[2,0,0,2,0,0]`|0.0015037593984968832|14|
|5|`[2,1,0,0,1,0]`|0.13383458646616705|19|
|6|`[2,1,0,1,0,0]`|0.12631578947368255|17|

### root_tax_failure.json

|原序|counts|probability_float|W|
|---|---|---|---|
|1|`[2,0,1,0,1,1]`|0.14604606981714455|45|
|2|`[3,0,0,0,1,1]`|0.5776537639515567|41|
|3|`[3,0,0,2,0,0]`|0.1278793635715978|40|
|4|`[3,1,0,0,1,0]`|0.0513535977202583|46|
|5|`[3,2,0,0,0,0]`|0.09706720493944282|40|



## PC与其它已知比较的范围

[原3197B尝试](../../tools/evidence/population-cce-original-diagnostic-two-primary/related-original/research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/security_aggregate/population_cce_attempt.md)已全文读；其未证PC是C_(m+1)/(m+1)≤W_m/m。现[静态安全引理](../引理/静态粗相关均衡的安全下界与三单例严格间隙--引理.md)证明C_n≥n v_n：每位CCE固定行动约束按独立最优安全query混合。配静态OPT_m≤2m v_(m+1)，PC若成立便有W_m≥m v_(m+1)≥OPT_m/2。只是条件蕴含，LP表示或有限正gap没有完成PC。

[同人数强CCE替换](../反例/三人顺序SPE低于全部静态CCE福利--反例.md)已由八/十三客户三人例反驳，分别W6<C₃544/87、W9<C₃2785/297；那是m人总福利比较，不是本跨人数平均PC。另[较弱同人数CCE桥](../候选/较弱CCE福利桥的占用LP表示与边界--候选.md)要求W≥(1−1/(2m))C_m，目标亦不同。真正安全值与CCE最低值还有严格间隙，不把C_n/n直接改名v_n。一般half或五人half成立均不反推这些更强前提。

源码的静态偏离冻结其它玩家终局行动；顺序SPE控制改动作后别人的真实响应。原尝试以菜单叶加一人再对称化，仍欠静态可行性与平均成本控制两项。多一槽稀释交集不自动消除响应差，也不能把各高福利菜单叶共同记在原actual预算。

## 精确复用、标签与原执行身份

必要51runtime JSON和九全字段/全策略view从刚冻结pair包同SHA复用，来源manifest/原字节/原字段顺序照存。九模型/九证书此前已全文读，其余33仍只作selector结构保全，不能变成本包新的数学阅读或done。code没有新消费项目solver，旧12222动作/IC/H/LP均不重放；给定策略只用于恢复旧实际W。

输入允许同覆盖labels（empirical的2/3）。静态CCE可投影到覆盖类，任意固定类偏离可由原代表检验；反向把类分布lift到固定代表，其余同覆盖标签偏离收入相同，故静态CCE最低福利不因别名改变。但报告q维度/支持概率点和给定顺序动作表不随商原样保留；[完整策略商](../等价/覆盖等价标签的完整策略商--等价.md)需重构σ，本程序没执行商或给商后证书。

旧4969B security README与[分段资源页](../资源/安全聚合探索与银行任务的分段证据身份--资源.md)此前仅报告有限浮点任务、未读此code/JSON。本次补真正LP/全部字段，不倒填旧审查或新blind。每例print(row)是Python对象表示，counts在内存为tuple、写JSON变list；最终JSON indent2加LF，stdout不是同一JSON报告，原无code/inputhash、argv/cwd/exit/耗时或完整solver日志，不虚构历史绑定。

两primary均retained到本程序对象与[来源闭包](../../tools/evidence/population-cce-original-diagnostic-two-primary/README.md)。16XR原完整16ID claim pushed，raw needs-attention与独立2untracked/2tracked全same、零missing/different/unmerged且stash保留并列；不改raw为synced，不裁成两ID回执。Boss4未Git/claim/done，数学执行0，交Root审后串行保存。
