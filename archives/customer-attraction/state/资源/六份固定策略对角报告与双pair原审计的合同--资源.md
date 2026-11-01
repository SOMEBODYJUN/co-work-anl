---
id: "customer-attraction/six-fixed-policy-diagonal-and-two-pair-original-audit-contracts"
kind: "resource"
type_tag: "资源"
title: "六份固定策略对角报告与双pair原审计的合同"
status: "five-primary-sources-fully-read;historical-reports-retained;zero-current-mathematical-execution"
summary: "完整保3355/10478六例与4190/1985双pair代码报告和6175论证；12真实六例输入同SHA全读，区分CWD/stdout入口与顶层覆盖输出、全历史IC与标量PB、历史OPEN与当前反例。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round7/coupling/audit_diagonal_full_menu.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round7/coupling/diagonal_full_menu_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round7/security/audit_pair_scope.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round7/security/pair_scope_exact.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round7/security/cross_pair_scope.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round7/security/cross_pair_scope.md"
---

# 六份固定策略对角报告与双pair原审计的合同

## 五份主源与证据身份

主源5904857c603ef0ca7c13（3355B程序）、4fe55e53f846fb6a36b1（10478B报告）、52bd5a241f2419c725b9（4190B程序）、289e9373a8667f96e765（1985B报告）、1a9d3978667435956e55（6175B稿），共26183B，均全文实读。前三件先前作为比较原件已读，实际正常show取得后逐项同SHA核复用；后两件本次正常取得后完整读。两个冻结提交均记录于[指纹清单](../../tools/evidence/full-menu-diagonal-and-pair-scope-five-primary/source-manifest.json)。[原件、正常show、全13项实际claim及本批收据](../../tools/evidence/full-menu-diagonal-and-pair-scope-five-primary/README.md)保全，claim推送6b8634ca657ac4736263ce61511bb036e6b6dce8、raw local_sync=synced不改写。

本批原程序main/import、旧348/34+empty重演、收益/IC重算、Fraction数学checker、优化器、扫描均0。指纹、JSON解析、AST和策略键域结构检查不计算效用，也不叫数学PASS。两个原JSON没有执行环境、退出码、时间或自身代码/输入哈希绑定，属于完整历史计算记录，不能将“原报告存在+当前读码”合成当前实际成功运行。

新增数学分别在[矩阵与单向链引理](../引理/完整根矩阵的交叉系数与自耦合蕴含--引理.md)和[PB指定两枝反例](../反例/PB背景两条指定根枝的交叉查询--反例.md)。既成348游戏及银行反族不重授新发现。

## 3355B入口：真实输入、全历史与有限分布

程序只用stdlib Fraction、itertools、Path、json，有main guard；导入只定义常量/函数，main调用六个run并将**完整JSON打印stdout**。它没有报告文件写入语句，10478B邻接JSON不能被描述为其直接写出的文件。输入路径为相对于**进程CWD**的examples/customer_attraction/{name}.json及evidence/certificates/customer_attraction/{name}.json，不是相对__file__定位。

从example读取players/topics/customers，每类multiplicity（默认1）展开为不同单位客户；策略从cert.get('strategy',cert)['actions']读取。字典化后断言键集合恰等所有0,…,m−1深度有序历史；该断言本身不检查字典化前重复、也无单独action标签合法性断言。本次对12真实JSON另做无重复、标签范围及完整键域结构检查，均满足；没有借结构检查重算SPE。

每个历史h计算原σ规定动作及所有强制当前动作后的真实完整叶，每主题核当前效用不高于规定效用；计数包括规定动作自身。重复/离轨历史在全笛卡尔树中逐个保留。K的分母1+完整全局叶负载，过去玩家和强制当前都保留。计算全部H_AB及所有不同A,B的负交叉计数，再查每个非空支持的均匀p和每对两点严格内部二次极小p；未求全单纯形极值。t不在(0,1)、二次项非正时不另添候选，因为单点端点已在均匀列表。

报告顶层完整保candidate/scope/arithmetic/cases；每例保name/players/topics/complete_ic_checks/exact_distributions_tested/negative_cross_coefficients/min_gap及witness。witness含history、p、名为diagonal的**d向量**、full_query_matrix、全部forced_leaves；diagonal不是K的对角线。原完整JSON保留六张见证K和所有强制叶，不用下表代替原始矩阵。

|case|单位客户／类型数|m/k／决策节点|含self IC|p项数|负交叉|所测min gap|
|---|---:|---:|---:|---:|---:|---:|
|portfolio_matching_failure|86/10|2/5／6|30|245|0|299/150|
|root_tax_failure|61/12|4/6／259|1554|20169|0|5/11|
|individual_security_failure|34/13|3/6／43|258|3326|0|23/14|
|eight_cce_welfare_gap|8/4|3/4／21|84|393|0|2/13|
|coverage_opportunity_failure|11/7|3/5／31|155|1260|0|3/14|
|prefix_balance_failure|22/12|4/6／259|1554|20172|0|5/22|

合计619决策节点、3635含self比较、45565次分布求值；分布列表允许重复，不能称45565个不同p。六例都不是恰六人输入，individual_security只是原六主题34例，没有添加空主题，也不是348例。

|case|原min witness有序h|p非零坐标|原d向量（主题顺序）|
|---|---|---|---|
|portfolio|(2)|所有5主题各1/5|(37/2,19,13,19,18)|
|root_tax|(1,1,1)|p₁=10/11,p₃=1/11|(30,5/2,11,10,37/2,37/2)|
|individual_security|(2,2)|p₂=6/7,p₅=1/7|(47/3,47/3,7,41/3,41/3,13)|
|eight_cce|(0,0)|p₀=12/13,p₁=1/13|(2/3,4,5/3,5/3)|
|coverage|(1,1)|p₁=6/7,p₂=1/7|(5,1,3,13/3,13/3)|
|prefix|(0,0,0)|p₀=10/11,p₃=1/11|(5/4,21/4,19/2,5,5,7)|

所有见证深度m−1，forced_leaves恰按主题下标将当前主题逐一接到h后；这是完整报告实际字段，并不暗示搜索只查末位。negative_cross_coefficients是在全部619历史逐对求的。若其历史计算正确，各H_AB≥0再结合自身税，解析地给这六份固定σ的**全部h、全部p**非负；不需要把有限p列表冒作密集采样证明，也不把min_gap视为全单纯形极小值。该固定范围的正面结论与普遍候选已有反例同时成立。

## 六例12件真实输入已完整阅读

[输入定位/指纹清单](../../tools/evidence/full-menu-diagonal-and-pair-scope-five-primary/six-related-inputs-manifest.json)给12件共65846B在当前仓库的精确路径和SHA/blob，均在本次本地可用，未网络补取、未追加其primary done。[无损阅读视图](../../tools/evidence/full-menu-diagonal-and-pair-scope-five-primary/six-inputs-lossless-reading-view.md)保全部58客户兴趣类型、619条策略行动（按深度/有序前缀无损分组）和每件其余JSON字段；本次完整读该视图及原JSON内容，不以文件名或摘要认读。

六件certificate结构并不统一：root_tax与individual_security有嵌套strategy及额外security/expected等字段，其余直接给actions/terminal_counts；root_tax的嵌套strategy不含terminal_counts。程序只消费actions；不会认证终局计数、安全值、查询概率、dual rivals、expected福利/OPT或原claim标签。相关字段原样保留在现有原证据中，本页不把它们并入3355B测试义务。按类型重数展开不同单位客户，不改博弈模型；完整策略仍按有序历史索引，不压缩成负载策略。

## 4190B入口：旧348完整策略与PB标量两部分

该程序**没有main guard，顶层即执行**；导入也会读输入、计算、覆盖输出并打印JSON。HERE=__file__所在目录，WORKSPACES=HERE.parents[2]，唯一真实文件输入是同级工作室R-d22…/representation/high_insertion_2cycle_348_exact.json。其原7417B输入已在[既成依赖清单](../../tools/evidence/minimal-support-and-uniform-time-primary/dependency-manifest.json)保全，SHA d60b843f01893bf24f11141342918760a9c3f25b44e43e1ddf8e4aefe09303d9；本次复核同SHA，未重新运行。当前原1985报告中的prior_root_certificate为另一历史绝对路径，只是原定位字符串，不是当前可读路径或字节绑定。

程序实际消费packet.instance及certificate.actions；以(frozenset兴趣标签,整数重数)聚合Fraction(w,cover_count)，与每位客户单位展开数学等价，却**没有实际生成348元素单位列表**。6175B稿“逐单位重算”按实现应理解为单位模型的重数求和。代码无单独键域/重复/标签验证；循环遍历三层43历史、每层全6主题，共258含self比较及215 proper deviations。生成六个强制根叶和d、内部完整6×6 K，但输出不保K全矩阵；只保pair及选定指标。K全36项已由别的原实现充分复现，当前不重跑。

它断言A2/B5 pair left147/right159、半半C=737/12<d₀、第0列cap69<d₀；从实际根叶(0,3,4)按重数算W230。原输出全部root_empty字段为customers348、players3、histories43、comparisons_including_self258、proper_deviations215、actual_leaf、W、六forced_leaves（034/134/234/301/401/501）、六root_payoffs均147/2、pair[2,5]、pair_left/right/deficit−12、iid_diagonal_C_on_pair及pure_column_0_cap。原small策略的已充分成功与本4190入口是不同代码身份；本次不伪造后者当前run成功。

PB部分没有导入PB控制器或构造48,495,120客户/巨大策略树。它只设置八个整数参数，计算f/g，assert处罚180、旧非热点171、空1891、贪心2294，assert2294>1891、r−t<2(Q−1)，并以Fraction核交叉下界减收益>0及7HM²>2(M+11)²。其输出existing_arbitrary_background完整字段为parameters、two_queries文字、each_root_profit、each_cross_query_lower、pair_right_minus_left_lower、greedy_count、empty_after_punish、scope；三个巨大有理数在[指定枝正文](../反例/PB背景两条指定根枝的交叉查询--反例.md)逐一保留。其普遍SPE合法性来自既有PB解析证明，不来自此标量脚本。

最后将完整JSON写到HERE/pair_scope_exact.json（会覆盖同名文件），并打印同一完整JSON；无命令行参数、优化器、随机搜索、策略改动、参数扫描或外部验证器。当前不导入/执行，亦没有因代码assert字面存在而宣称其已运行。

## 6175B稿的全部数学与状态去向

§1及§4的对象、PAIR→SELF→WP→Mfull→extra-one充分链已自足写入新引理，保独立查询、保根r槽、非对称K和min/max方向。§2旧348不是新游戏；实际pair只否强候选，不能把D<C或pair负传给C>u；现正文已有完整输入和当前银行比较，故去重。§3此前仅作为related摘要的PB两枝现完整保存计数和严格f/g证明。§5准确保4190/1985只做两个指定攻击、不搜索或推进half的实现范围。

原稿和原1985 status写“一般half、root security/extra-one等OPEN”，是冻结时态。当前[银行完整根例](../反例/笛卡尔银行完整根菜单的低值自洽分布失败--反例.md)给m≥4（含6）的真空根Mfull及全p-WP失败，四人u=4/3、Mfull=59/36；[整数extra-one状态](../问题/自由extra-one与iid安全值边界--问题.md)还明确v₅≥B₄=19/14>4/3，不再将它们称当前开放。六例有限正面与这些普遍反例并无冲突，且银行福利仍过half。原34加空主题D<C<u只是另一强桥停界，不能混入六例individual_security的原输入。

任意合法PB背景已有完整子SPE，但[最后单例偏离](../障碍/PB大背景的最后单例偏离--障碍.md)排同参数直接实际前缀；本页不从“可合法形成”跳成“实际在轨”。五人half为他证；当前恰六人每份完整SPE的half没有被本五源解决或否定。

## 关系与接续

本次三页分别承担矩阵身份/充分条件、既成PB策略的两枝反例、实现和历史证据。六份报告只实现固定输入检查；全p结论由H逐项非负的解析推导承担，其数值前提保历史报告证据层次。PAIR反例反驳的是同一矩阵加强，不否定合法局部SD/COLUMN/PROJ，也没有共同实际钱包。与[此前静态列审查](../../subarchives/six-providers/state/审查/静态列与查询投影的历史审查及强菜单停界--审查.md)不重复授予数学；本批补完整五主源身份、两件新pair原件及此前未展开的PB指定枝。

关系在[独立审查清单](../../tools/evidence/full-menu-diagonal-and-pair-scope-five-primary/relations.json)逐项说明，Root串行保存正式正文后才可逐源done；本worker未改共享图/目录、未Git/claim/done。接续应研究真正共同支付或更弱正确命题；本批无需追加旧六例或旧348阴性/成功重演。
