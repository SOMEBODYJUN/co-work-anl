---
id: "unrelated-machines/home-unit-token-paired-program-resource"
kind: "resource"
type_tag: "资源"
title: "单home正规化与需求桥双实现精确审计"
status: "exact-original-entries-reproduced-once-finite-domains-separated"
summary: "完整保留两个原程序、各一次隔离运行与不同输入域；独立home回放不导入核心，规范程序另验证真实token双向任务身份。"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/home_unit_cycle_and_directed_token.py", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:tests/audits/unrelated_machines/home_unit_cycle_and_directed_token.py", "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/home_unit_cycle_independent.py", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:tests/audits/unrelated_machines/home_unit_cycle_independent.py"]
source_ids: ["e8b6428338f9c956317c", "594190c19816e3b1e99a"]
---

## 原资源与实现身份

两程序均完整实际读取，原件逐字节保存在[证据目录](../../../../tools/evidence/um-home-unit-transit-and-envelope-primary/README.md)。规范源`e8b6428338f9c956317c`为435行/17130B，SHA `1cf7ebfc58e92dc7dac92a6d1753f8ae899be8be078b00b1da53e1ae7c6982bc`；独立源`594190c19816e3b1e99a`为122行/4918B，SHA `41d9dc92bee99dec3874bd23fe1e643c3327828e4754c432c66d79592593b330`。均只用stdlib和Fraction。规范入口支持`--audit normalizations|directed-token|all`与`--output`，本批只运行all一次；独立入口无核心导入。

[自足数学合同](../定理/单home正规化与一般有向需求树实际恒等--定理.md)分别证明逐简单环逐机不增、C<2的保U根精确profile，以及OPT=2−b*。程序不是一般范围证明的替代。

规范`HomeUnit`检查尺寸、合法home、a∈[0,1]、互异非home替代端与U非空合法端集；`loads`从原任务重算实际时间。`cancel_cycles`按原任务标签找简单环并回home；另一套拓扑删除核无环。`normalize_unit_roots`直接搜索原U根可达域，回home所有域外home任务，保全部U身份和位置。一般有向桥`build_token`只生成min(k,outdegree)枚child及可选filler、一枚根U；`_tree_data`检查单父、根可达、无环，`schedule_tree`在递归前裁掉多余孩子及整棵子树。全实际指派oracle和根树边子集oracle独立枚举；不会调用解码器来决定其最优值。

独立源先定义自己的actual-load、找环/取消、U可达profile及验证，再枚举其输入；没有导入规范模块。其枚举允许同home重复、a=1指定参考端、空J等，不实现一般需求桥。历史“独立”在这里可核为不同代码与不同oracle，不认证作者身份、盲审过程或外部新颖性。

## 本批一次原入口的精确范围

每入口在新建空cwd运行、原件以原basename复制、禁pyc、保argv/stdout/stderr/report及运行前后SHA。两入口均exit0，stderr空，输入未改；不覆写历史报告。

|入口|实际输入与检查|本次结果|
|---|---|---|
|规范正规化|三机、每机一J，a∈{0,1/2,1}，U数0/1/2，所有3机器指派；另四J重叠环及边界|9803完整调度、4034含环、992峰<2；3边界fixture|
|独立正规化|规模(m,n)=(1,0),(1,2),(2,3),(3,3)；每J独立选择home、a∈{0,1/2,1}、实际端；U根为空或一机|83936指派、18306含环且均消除、21212峰<2、18554次可执行root正规化、3边界检查|
|规范需求桥|三点64个无自环简单有向图、每个根、需求∈{0,1,2,2^80+7}且零需求仅原sink；全部任务指派及全部根树边子集|6591合法token实例、151959完整指派、1767次峰<2解码、17004树→实际调度|

规范正规化9803=9477主枚举+324重叠环枚举+不可达环/空例2；无预算额外例构成第三边界。独立83936=2+18+5184+78732，不能与规范9803合称同一测试集；其18554次root检查还过滤了全局max b_i≤原峰C，所以不等于全部21212个峰<2例。独立的三个边界分别表明：根正规化可以提高个别机器负载而保持峰；a>1破坏逐机去环；同时回home不等于单件迁移守峰。规范另外保存不受U到达的反馈环、U空和不预算时峰上升。

需求桥每个完整指派精确重算负载，逐个峰<2输出检查原边、原根、单父/可达/无环和评分；每个合法根树经裁枝分派**全部原任务**后检查峰≤2−b(H)。巨大需求只以二进制分母出现，验证构造不按k生成任务；它不说明所有输入被枚举。

## 独有边界与接续

本批另只导入规范定义、未调用原main，以两个精确小例核实旧v2反向说明的勘误：k=(1,0,0)、根两个终端时正确实际负载(1,1,0)；链k=(1,2,0)负载(1,3/2,1)。此新增诊断执行一次，报告位于`errata-diagnostic/report.json`；不增加源处置计数。

三个数学身份不能并成“去环便得到未知好森林”：输入已经是一份完整实际σ，根位置、共同资源搜索、好树寻找仍未被提供。需求桥允许一般有向环境，下一DAG FPT代码只覆盖其严格子域。程序覆盖的是列明有限族；一般定理依赖上述自足证明，未证明一般UM算法或复杂性下界。
