# R79两匹配入口与原生势回归

本包完整清洗三主源，共12526B。父方报告本批claim已pushed/synced于`e107f5c37c97782fea9c09f61454be2f26d4f02f`；三件normal-show receipt逐件保存，原字节与inventory的size/SHA/blob定位一致。此处不把认领或本地staging当正文推送/done；交付事务由父方串行完成。

|源ID|原件|大小|独有内容的正式去向|
|---|---|---:|---|
|122b308e19e7b7f810a6|[attack_matching_cone.py](original/research/workspaces/customer-attraction/R-79a883d99127437ebe4f0423a181f01b/independent_audit/attack_matching_cone.py)|4625B|[有理匹配与固定锥程序](../../../state/程序/最优冻结匹配的有理指派检查与配对策略锥提案--程序.md)：43节点配对策略、258Γ、20弱最优支持、Σw归一/η非负、整数提议/全重复后检、接受控制流和序列化缺陷|
|0e4145bfdcb8baea4d5c|[attack_optimal_static_matching.py](original/research/workspaces/customer-attraction/R-79a883d99127437ebe4f0423a181f01b/independent_audit/attack_optimal_static_matching.py)|4623B|同页：全部SPE终局计数、所有OPT重复元组、Fraction标号列子集DP、canonical行置换不变性、CLI/输出合同|
|bd70f2bd09480a4928ab|[root_potential_regression.py](original/research/workspaces/customer-attraction/R-79a883d99127437ebe4f0423a181f01b/root_potential_regression.py)|3278B|[34客户原生回归](../../../state/程序/三十四客户联合势后悔与删位重置的原生回归--程序.md)：固定输入/策略/p、43/258真实IC、POT/RESET、import即执行及真实run|

## 实际阅读与运行

三程序从首字节到尾部完整读，包括每个函数、import/路径、全部main/顶层执行；四规范包依赖亦全文读。34客户输入13类全部读，并核原已有完整43节点数学证明；冻结匹配ID/八客户量词分离、52/1953全部最优反例、RA0/R51/R891实现合同、旧36客户删根预算及完整额外槽总账均比较，详[比较manifest](comparison-manifest.json)和[实读语义单元](source-reading.json)。

本次唯一数学执行是**原字节root回归一次**，代码和输入均未修改，exit0、stderr空，原输出保[native-regression/stdout.json](native-regression/stdout.json)、[事件](native-regression/execution.json)。两匹配入口的import/main/inspect/DP、规范BI及NumPy/SciPy/LP执行均0；原README的3800随机样本与20支持双实验只作历史MD报告，未冒当前重放。未重跑52/1953熟悉全树来触发序列化错误，错误由完整读数据类定义和直接json.dumps控制流确定。

五必要依赖从既有同SHA冻结资源复制到`original`的原路径；它们是可复用运行闭包，**不是本批新增主源、认领或done**。四规范模块来自`strategy-cones/original`，34客户输入来自`continuation-security`。来源、旧保存路径、size/SHA和用途见[依赖manifest](dependency-manifest.json)。外部NumPy/SciPy仅是两匹配脚本的显式依赖，未为本批运行它们。

`original`保原根相对深度：两个匹配入口依赖原共同目录包且互为同目录导入，root回归用parents[4]读固定examples；不可把脚本拷平后因路径错误断言原算法失败。root没有main守卫，import也会完整运行。

## 数学自查与关系

[自查](self-review.md)逐项核量词、真/冻收益、最优重复元组、归一/浮点证据、程序缺陷、C⁻/C⁺和已有反例范围。[关系说明](relations.md)给实现依赖、有限检查、后续纠错和与旧正文的接续，不制作第三阶段超图。该包无新half反例、无全域正面证明、无外审/新颖性认证。

[verify_delivery.py](verify_delivery.py)只核字节/receipt、AST可解析、链接和native事件绑定，不导入或再执行数学程序。其结果见[self-check.json](self-check.json)。阶段二逐源语义receipt由父方随正文推送后登记，不能把此结构自查代替数学判断。
