# R891完整菜单、前缀预算与ROW客户锥程序

五主原件共15660B，四份Python与一份821B JSON均完整实读。[source-manifest](source-manifest.json)绑定完整冻结commit/path/blob/size/SHA256及未改原件；另两根入口2850B只作相关合同，见[related-source-manifest](related-source-manifest.json)，不代其primary done。

## 正式数学程序对象

1. [逐人完整菜单的集合续局与计数策略客户锥探针](../../../state/程序/逐人完整菜单的集合续局与计数策略客户锥探针--程序.md)：两种保当前槽M_i攻击，集合BI可实现菜单与固定Markov客户锥不同；后者纯float、前者只精确复算有理查询下界且未导完整树。
2. [全前缀残余覆盖与尾部利润的精确有限探针](../../../state/程序/全前缀残余覆盖与尾部利润的精确有限探针--程序.md)：所有缓存合法前缀/子SPE，OPT_missing≤新增覆盖+余者利润；只有p0直接等价根half，不能把任意背景反例冒根actual反例。
3. [真实查询行固定客户锥的比较极点与有限阴性账](../../../state/程序/真实查询行固定客户锥的比较极点与有限阴性账--程序.md)：全原有序策略固定、比较m槽极点缩减、四float阴性锥/一个dense guard及正点精确化/整数缩放合同。

|主源ID|未改原件|字节|独有内容|
|---|---|---:|---|
|f7c3f43a7e26e0bcc3fb|[menu_attack.py](original/research/workspaces/customer-attraction/R-8918a9ea76c74f88a9de75e2c4a948e9/independent_general/menu_attack.py)|3585|精确R/θ兼容孩子、3目标/3起点×5轮、查询LP和Fraction lower、400随机域及输出|
|b35a0a5ab08c84d8d29b|[menu_cone_attack.py](original/research/workspaces/customer-attraction/R-8918a9ea76c74f88a9de75e2c4a948e9/independent_general/menu_cone_attack.py)|3226|一份Markov策略全部count-state IC、固定π客户锥float margin、300随机域和计数policy输出|
|24829198bbf004acb2d5|[prefix_candidate.py](original/research/workspaces/customer-attraction/R-8918a9ea76c74f88a9de75e2c4a948e9/independent_general/prefix_candidate.py)|1847|精确全缓存p/q、余k遗漏最优/Δ/U、全部非空类型正重数的3000随机域、仅stdout|
|4a0117aafc16525bb945|[row_cone_attack.json](original/research/workspaces/customer-attraction/R-8918a9ea76c74f88a9de75e2c4a948e9/parent/row_cone_attack.json)|821|全部五记录：56/222/222/20 float负值，五人资源跳过，无阳性或原进程|
|77685decd6a85cfc001d|[row_cone_attack.py](original/research/workspaces/customer-attraction/R-8918a9ea76c74f88a9de75e2c4a948e9/parent/row_cone_attack.py)|6181|五输入原cert先验、全有序Γ、比较支撑/集中重复极点、float提案到有理/整数/全树分支与累计输出|

[semantic-units.json](semantic-units.json)逐函数、分支、报告记录和输出合同给去向，不以文件名/头部摘要代全文。[comparison-bindings.json](comparison-bindings.json)记录十份实际全文比较对象的SHA、用途及未改声明，其中银行对象为本会话已全读、同SHA复用。

## 必要输入、旧成功证据与本次零执行

`menu_attack`、`prefix_candidate`导入规范model/exact；`row_cone`导入model/certificate并读五对examples/完整策略。包初始化也导入exact，所以完整依赖共四模块和十JSON，共14件1417104B。它们已经在正式结果树保存，本批按冻结inventory逐件核SHA，代码全文读，JSON全部字段/动作结构遍历；不重复复制1.3MB旧五人表，也不额外done。

[dependency-reuse-manifest.json](dependency-reuse-manifest.json)给全部14件的**真实既有repo路径**、完整原来源和指纹；未来需按原相对路径复制到临时source-root，再恢复research/workspaces深度。不是把旧原件所在地随意当原ROOT。[fixture-input-reading.json](fixture-input-reading.json)逐件保全部客户输入、其它metadata及完整动作记录的结构阅读结果：

|fixture|m/k|单位客户|全部有序动作记录|actual|
|---|---|---:|---:|---|
|individual_security_failure|3/6|34|43|(0,3,4)|
|global_decorrelation_failure|4/6|89|259|(2,5,0,0)|
|root_tax_failure|4/6|61|259|(0,0,0,5)|
|five_individual_security|5/10|86|11111|(4,5,6,7,8)|
|eight_cce_welfare_gap|3/4|8|21|(0,1,1)|

五人巨表的完整SPE/成功定义级核验复用已发表正文，本次不是新11111节点激励审计。源ROW程序先验证原cert再k>6跳dense锥；五人报告未列actual，不能将另读输入的actual倒填成报告字段。其它四锥的520个float负LP不证明精确全锥上界。

[execution-and-output-scope.json](execution-and-output-scope.json)明确本批原入口执行/import、LP、BI、随机、SPE重放均0。四源码有main守卫；本批没有其它三探针候选文件/原stdout，也没有ROW原stdout/进程回执。原五记录保历史有限结果，不补造它们来自哪个解释器或观测事件。

## 数学与关系边界

逐人完整m槽、全位置自由/均匀菜单、删槽聚合预算、全合法背景前缀预算和ROW净差分别定义。`menu_attack`变量名dual并非对偶乘子；float `menu_cone`正margin也不是精确证书。ROW比较次数的极点缩减是确定的线性解释，但有限负float不升级普遍数学；正分支保存的是整数化前有理D，实际整数游戏缺口为D·den/gcd。

[relation-review.json](relation-review.json)区分实现、后来反证状态、不同菜单域、根特化、末两已证边界、有限报告与旧SPE证据复用，逐条给前提及拒绝误推。没有新正式三级图或一般六人half结论。两根related的六分支和未付款义务保历史，不强制当前研究路线。

[publication-check.py](publication-check.py)只验字节/JSON/AST、14依赖、表和链接、五收据及原记录转录；[结果](publication-check.json)不运行原数学程序，也不代替阅读、证明或远端门槛。父方串行发布正文并核复用路径后再done，本stage不自称已经推送。
