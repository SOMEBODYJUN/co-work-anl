---
id: "unrelated-machines/dag-transit-paired-audit-resource"
kind: "resource"
type_tag: "资源"
title: "根DAG守恒支撑双实现与不同枚举域"
status: "five-original-fixture-families-and-independent-oracles-finite"
summary: "保全新旧程序真实运行依赖与两个9496例的不同输入；精确流、全树oracle、随机重标与巨大需求均按实际范围登记。"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/rooted_dag_transit_branch_search.py", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:tests/audits/unrelated_machines/rooted_dag_transit_branch_search.py", "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/rooted_dag_transit_independent.py", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:tests/audits/unrelated_machines/rooted_dag_transit_independent.py"]
source_ids: ["e8706876e0c1b5dcebd9", "3c16720b6c276a5997e1"]
---

## 程序身份和实际依赖

规范源`e8706876e0c1b5dcebd9`（286行/12068B，SHA `b61709532d1abfd0bf9c7d99364ea0b693ec13232657385235c4ba7312cc1191`）完整实现高点k≥2K、守恒低点1≤k≤2K−1的证书验证、拆点流、提取、最小K、枚举高点支撑和阈值精确优化。[算法正文](../算法/根DAG守恒证书与非单位需求参数精确算法--算法.md)给一般证明、2^h总复杂度及单边锐界。

独立源`3c16720b6c276a5997e1`（240行/10673B，SHA `e00600477410af8bec19ea2d7064c23fd19849495ec72346400bf79d88fcf0be`）先定义自己的输入/证书检查、整数流、原边流穷举、所有边子集根树oracle、旧流裁剪、最小K和支撑搜索；之后显式加载被审规范模块交叉比较。运行可用`--implementation`指定模块。本批传入byte-exact规范副本。它不调用规范main/fixtures，但不是整个运行不导入被审实现；历史先盲重构的交流身份不等于可执行过程的依赖独立。

规范fixtures另动态加载同目录旧`rooted_dag_congestion_flow.py`（源`cd5e59034198845a9ec2`，565行/24748B，SHA `64895990f782290aab59bedd7600422bc046cfd818d2f648c8142c5e06a056bd`），调用旧min_certificate/validate。该依赖已全文实读，单独main执行数0；其余均stdlib、无外部数据/网络。独立检查器的部分辅助函数以合法生成输入为前提，并非针对任意未知字典键/非法图的完整恶意输入验证器。

## 本批新隔离运行

两个原入口各在新空cwd执行**一次**，所有别名源SHA前后相同，exit0、stderr空；准确argv及report保存在[证据目录](../../../../tools/evidence/um-home-unit-transit-and-envelope-primary/README.md)。报告记录的b617…是被审**代码**SHA，不是输出文件SHA；execution.json另给实际stdout SHA。

|规范项目|真实范围/结果|
|---|---|
|自然拓扑标号精确枚举|n=1..4；全部前向简单DAG、合法需求{0,1,2,4}；9496例，对照63736个父点选择树|
|固定全支撑W/K|28488例，4179个可行证书实际提取；不是全部子支撑都被穷举|
|随机与根重标|seed7102026、500个5–8点图，13938个父点选择；全部500次重标任意根|
|边界fixture|10条报告：5个单边需求、根终端远处巨大死端、旧流须裁、任意根巨大非根需求、1502点单位走廊等|

单边根需求1,3,5,9,10^100+1，新最小K分别1,2,3,5,(10^100+2)//2，实际树值为1/k；旧最小K=k。unit merge新K1、旧K2。1502点走廊非单位数h=0仍取得值1。远处需求q的正死端使固定全支撑K=floor(q/2)+1，即使根终端可直接提单点。任意根样例含非根需求10^100+39，值2/(10^100+39)、h1。

|独立项目|真实范围/结果|
|---|---|
|全根树边子集oracle|n≤4、自然拓扑DAG、合法需求**{0,1,2,3}**；9496例，不是规范的同一9496输入|
|固定支撑原边流oracle|n≤3，边流整数0..K；5350例，其中695可行|
|免费补低点/终端|695次，补入后逐点核共同合同|
|旧→新拓扑裁流|504例，实际修改流后验证|
|与规范接口对照|1516次固定W最小K、1390次支撑搜索，3个新增边界fixture|
|单边锐界|K=1..100及10^100+39、10^300+27，共102行，每行精确值1/(2K−1)|

两枚举总例数相同不说明需求域相同；原边流oracle与规范拆点流也不是同一个搜索过程。原件和report完整保留所有字段，包括巨大整数、流和实际H，正文不把随机例数量当普遍证明。

## 比较、状态与接续

旧原始canonical§1–6的高点阈值是K；本规范/独立实现测试§7–9阈值2K及FPT增量。已清洗的“守恒扩区与路线拼接”两页还含另外程序/路线数据；本次只比较其相关段落，不额外勾选其被链来源。新旧同W/K可行性为严格包含，旧f可能须裁剪，不能直接改阈值标签后复用原f。

固定支撑位多项式、只高点指数枚举与2^h精确算法是不同合同；所有验证使用同一共同流和实际树。不能把单点逐个可满足、激活LP边际或一般UM原实例当作已经提供该共同支撑。软件的有限回放为实现证据，一般证明在算法页，h无界和一般矩阵桥仍是清楚的剩余义务。
