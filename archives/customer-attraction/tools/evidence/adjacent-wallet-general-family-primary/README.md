# 最优指派相邻钱包一般族的完整原件与精确QA

两份自足正文为[固定倍数反族](../../../state/反例/唯一最优支持下相邻钱包的固定倍数反族--反例.md)与[计数前缀原审计](../../../state/计算/相邻钱包一般族的计数前缀精确审计--计算.md)。数学反证、有限实现与两份内部审查的先验分别保存。

## 正式五主源

新的65源认领已由Boss4明确确认pushed/synced `e8bb5a61692cd2aa542bbb4e710bc00c3bdf6ada`，其中本批5源。确认前仅只读已发表相关正文、未创建本stage或写未认领源；确认后才全文读原件、核SHA、写正文与执行。五源31943B，两个冻结位置逐字节相同，原件保原仓库相对路径。

|ID|路径尾部|字节|
|---|---|---:|
|81bc4b8504d7a37b9805|round10/parent/optimal_assignment_adjacent_wallet_counterfamily.md|7350|
|3a4479719e981f9bc43d|round10/parent/audit_optimal_adjacent_family.py|3287|
|2e83f00a05168c0aa558|round10/parent/optimal_adjacent_family_exact_audit.json|2638|
|d6ada5ea6dd4defa20fe|round10/tree/existential_adjacent_family_review.md|7724|
|662bb9acaf7487aaf7e7|round10/netglobal/weak_adjacent_root_family_independent_review.md|10944|

原公共前缀为 `research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/`。完整commit/path/blob/SHA和阅读角色见[source-manifest.json](source-manifest.json)。

## 一次真实原入口

原程序全内置同一客户族、完整计数策略及m2/3/5/7，无外部输入或第三方包。只用标准库和精确整数LCM/Fraction。原报告以`open('x')`写出，故新隔离 `replay-tree/` 只先放原码，输出确不存在；冻结JSON另在 `original/`。

原main唯一一次：Python3.12.14，exit0，0.10331559181213379秒，stderr空，源码前后SHA不变。新2638B报告全字节等冻结，SHA `3c4342975a202b73757663671290821a35094fd68e46a06d9e5f7ca68c9cc670`。完整[execution](replay/execution.json)、[stdout](replay/stdout.txt)、[stderr](replay/stderr.txt)、[新JSON](replay/optimal_adjacent_family_exact_audit.json)及[运行输入清单](runtime-input-manifest.json)分别保存。stdout紧凑格式不与缩进报告冒称字节相同。没有另跑其他原程序或增补扫描。

真实循环核5361个计数前缀、47480项含自身IC，它们对这份明确计数策略代表600708个有序历史，后者没有被字面逐条遍历。最优指派循环每例只检查m个D位置；唯一最优支持和所有A列同值使之穷尽全部成本类型。原程序不通过全目录m元组暴力枚举求OPT；OPT普遍性由私有客户强制论证承担。

## 两份审查及全仓比较

tree先按精确构造/政策/候选合同重构，明确未读主稿或作者代码；随后全文读主稿和旧13人算术，后段是对稿不再称盲审。netglobal先按root精确合同、在主证明前重构，后完整对照主稿；其文本没有被本批扩写成“已运行作者代码”。两份review都不独立认证有限QA，也不做外审/新颖性评判。未用PASS代替完整证明：所有触发历史、A耗尽只在末位、b新鲜、D单独分母、唯一最优多重集、D两类成本、固定α量词及J_base范围均进反族正文。

三份comparison-only原件13403B：旧十客户紧凑反例、直接静态吸收/早期缺额、旧13人基本税算术。全文对读并保存，不额外done。现行共同目录模型、完整历史终局集合算法、计数策略净化问题、同负载不同续局反例、十客户反例、直接吸收及真实净差付款候选均全文比较；五人定理/六人问题仅核模型状态。

全仓冻结Markdown按一般族/程序完整名查后续，确认旧相邻存在性OPEN只属历史并已加修订。未作额外非Markdown远端扫描；全部必要本地blob可读，提取禁lazy-fetch，未尝试任何认证或备用凭据。

## 真实失败层级

每m≥2有合法完整SPE；存在性相邻钱包桥仅从m≥7严格失败，任意固定α在m>2α+4失败，α不能随m变化。m6等号仅解析代入、原程序未跑；m5单族负差不当五人通用正面结果。该策略满足half，更宽Q≤(1+1/m)W和J_base付款未被反驳。对最优主题的真实V_ij=m也不击破净差匹配候选；此为从策略推导的接口比较，非新增原程序输出。

计数核验不是模型净化定理；给定完整策略可能同计数使用不同平局，只有本明确policy(q)才允许此压缩。解析全m证明、有限四例、代表历史数与实际检查数、内部合同重构/后对稿和本次读后复现全部分开。一般六人目标、全ROLE/共同容量不因该精确辅助桥反例升级。

工作区含5receipt、数学自查、关系及下一实际候选。结构[verification](verification.json)只核字节/链接/报告和已有执行，不再次运行数学原程序。
