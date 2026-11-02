# 初始客户边回撤五源：原文、解析重构与精确复跑

五primary源共25583B，全部用`python3 work.py clean show ID`全文读，另以`--out`取回原字节并逐份核冻结size和SHA256；双冻结提交定位在[source-manifest.json](source-manifest.json)。其中数学稿10512B、return接续2471B、README1288B、程序9781B、冻结报告1531B。未只用文件名、旧摘要或检索命中作阅读声明。

## 数学去向及关键区别

- [初始客户边独立回撤定理](../../../state/定理/初始客户边独立回撤与共同价格分散返还--定理.md)：同一合法R流全部初始边分裂、逐角色全追踪、扩张INIT的独立回撤、所有非负price的精确可行性、同owner返还min(D,E)、抽象严格分离和常数price仍等原half。
- [真实return账本](../../../state/引理/真实历史返回动作的精确账本与共同资金缺口--引理.md)：旧history改回actual动作的真实return叶，P/N/e的符号、current正性、共同预算不可复制、Cauchy/Jensen只有收益下界。未把这次未闭合接续退休或写成新的half证明。
- [原程序合同](../../../state/程序/初始客户边回撤原审计的精确合同与有限覆盖--程序.md)：所有代码函数、输入字段、直接断言、原报告完整表、本次复跑及未激活项。它不是第二独立实现。

原README的工作区“不改共享、不git、不外发”是2026-10-24研究历史；本批不执行它作为新任务。其下一步“真实共同不等式、停止机械commodity细化”保在数学边界。两原稿当时的五人OPEN不继承为现状：当前五人half已有独立正式证明；此固定流修复族的普遍成功、六人和一般人数仍未由本批给出。

## 全仓相关比较

[comparison-manifest.json](comparison-manifest.json)保7份已读正式对象的精确快照及唯一相关原JSON：联合INIT/I-PAY/R-FLOW/ROLE、加强初始化和来源密度、owner比例回撤与首失败price、三实现不同maxfuture/commonfuture角点、原owner程序的已有复跑、52客户完整冻结匹配对象、五人half完整证明。没有将这些旁读源重复done。

数学区别已逐项保在新正文：atom比owner更细但不新增钱包；回撤可使d′>u而仍需最后2u；不能合不同路由或T的有利金额；全额逐角色追踪不能替成总额相等；固定cut充要不等于原SPE成功；真实return不同于actual-prefix reset；Jensen方向不能倒转。没有找到后续全称不等式证明上述缺口已解决。

52客户fixture已全文读，包括全部259有序动作及24冻结匹配字段；其原32574B保在[related/static_matching_counterexample.json](related/static_matching_counterexample.json)。本程序实际只消费instance和certificate.actions，不将其附带唯一最优/匹配结论扩大成本程序运行认证。

## 一次未改字节精确运行

原源码和fixture按原相对路径复制到`replay/tree`，执行原main一次；[execution.json](replay/execution.json)记录真实命令、cwd、UTC、耗时、exit及代码/输入/输出指纹。[stdout](replay/stdout.txt)、[stderr](replay/stderr.txt)、[新报告](replay/atom_retraction_audit.json)与[冻结原报告](original/research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/common_capacity/atom_retraction_audit.json)分开。

exit0；报告1531B，与冻结逐字节同，SHA256为`074495dc0c46f57c2bb93327dc4ec9d96df3bcc469eccfb8ed0886a3fbcfe43c`。代码没有修改；没有新随机扫描/优化器。若从仓库根再现，命令为：

```sh
python3 archives/customer-attraction/tools/evidence/initial-edge-atom-retraction-primary/replay/tree/research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/common_capacity/audit_atom_retraction.py
```

原main会覆写重放树内部同名报告，冻结原件在original/不变。

直接有限范围：1554项含自身完整IC、固定T的126覆盖组合、maxfuture和I补余、2条各1/8且均末位终结的atom、逐角色终端全追踪、θ=(0,1/3)终端缩放、81真实价格分散恒等式；另64价格检查属于未认证为博弈的抽象三角合同。真实例owner不同，未激活同owner跨价分散或真实严格细化；程序只用mandatory/raw边，未测非零common。一般解析结论由证明承担，不由有限检查替代。

## 关系判断与限制

[relation-review.json](relation-review.json)记录实际比较后的精确关系及保留条件。它是第二阶段入库关系核查，不生成第三阶段正式超图。无外审、新颖性或一般SPE修复认证；当前已证五人及开放六人边界保持。
