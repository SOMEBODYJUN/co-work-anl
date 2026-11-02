# 对称不交卫星块的程序、报告与核验

四份主源的原字节在 `original/`，由 `python work.py clean show ID` 实际导出并SHA核对；[source-manifest.json](source-manifest.json)保完整冻结路径、两个来源提交、字节数和SHA。主源共48463字节，分别为11286/11127/19290/6760字节。相关8389B README在 `related-original/counterexample-search-README.md`，仅供数学证明比较，不将其他代理认领再计本批完成。

- [精确算法正文](../../../state/算法/对称不交卫星块的完整SPE结果轨道递推--算法.md)
- [完整资源合同](../../../state/资源/对称卫星商程序与八九人有限报告的证据合同--资源.md)

源码SHA `37783fd478eae16f71aae62fcb93634e81cfc2919858e8edcacefd7185a2180f`；八人SHA `38a6535edf56be8c2b5eb0dfe5de6a5c0192e042d6a8905da8589be0aa28c626`；九人SHA `2d53063ad4dbf1f1d288d0b8851116d814a1a72d8120cc4da70a054b11902180`；旧独审SHA `a3b7b53a03b0f5ad827e29a06c24803e950543d505faa42eda220f0cbc27e8b0`。

`customer_attraction/` 是相同冻结提交的四个规范包导入依赖，来源/大小/SHA见 [canonical-dependency-manifest.json](canonical-dependency-manifest.json)。原源码会向祖先查找该包，故此布局保留原字节即可导入，未改原程序路径搜索。

本次只一次新函数级执行，命令从仓库根为：

```bash
python archives/customer-attraction/tools/evidence/symmetric-core-satellite-orbit-primary/verify_saved_inputs.py
```

[verification-event.json](verification-event.json)绑定实际命令、UTC开始、耗时与退出码；[stdout](verification.stdout)/[stderr](verification.stderr)原样保留。exit0，原288比较、新seed2026110207的36混负载比较、零客户并类控制1例、两报告52个具体输入全部通过，价格LP/main执行0。完整输入、轨道、核算值与旧36不可重放说明见 [verification.json](verification.json)。重新运行该命令只更新本目录新verification.json，不会更新四主源，但不应把重复执行次数混入这份已存事件。

八人报告12个根均1轨道/1128状态，九人40个根中step7两轨道、其他各1/762状态；最大OPT/W分别401/341和157/97。八人12个保存组合均有理精算匹配，最大2431/3220仍只是可行价格下界。大输入未另外展开有名完整历史证书；完整结果集正确性由正文受限对称模型的精确归纳承担。

旧独审36项缺实际重数、生成器与两边结果集，保留原声称，不把新36误报为重放旧36。两原报告schema不完全等于现源码main schema，未追认原生产argv/代码SHA。可选concentrated程序分支没有本批冻结报告，通用SPE/半覆盖/价格普遍上界均未由随机有限阴性完成。
