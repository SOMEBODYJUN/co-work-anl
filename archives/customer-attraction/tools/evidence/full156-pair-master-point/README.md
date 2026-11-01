# 完整156主题的配对必要点证据

主源86dc0b448e2d53c20f0b；正式对象为[完整156主题构造所用的配对必要点](../../../state/计算/完整156主题构造所用的配对必要点--计算.md)。本包保完整原字节、全部364变量的无损读表和本轮独立新增子行审计，三者不混成原10344行全图的新重放。

## 原件和读取链

以下均通过 `WCG_ACTOR=Boss7 python3 work.py --save repository-cleanup clean show ID --out PATH` 取得，没有修改原内容；research_5位于冻结工作区 `research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/`。主源在68fad804ec5946cb296f77dc5b336308a66abf12及aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c两个提交相同。

| 本包路径 | 源ID | 字节数 | SHA-256 |
| --- | --- | ---: | --- |
| original/pair_master_exact.json |86dc0b448e2d53c20f0b|158498|090586fb86af4e80b33eb24893d72fa2d240d156d639bcb97a9f8b413eddb2d2|
| related/pair_closure.py |01723987ead5f058e8ed|6572|bf72caf986685f6db6ae22106cf531d2314f19cf636621136804d685ed524f91|
| related/zz_threshold_closure.py |9c82a1b1090372077fec|8353|959d52f297152b1f2ae5e07834c56ed94f87a5cef0cf252acf2a2d0071a0b7eb|
| related/combined_branch_master.md |aa17048f7637dc3e22aa|5032|23a09a40692a1539655d96723b8d81a5974f6ab96d7cd8d9af2d3b7019c2179d|

配对点的九顶层字段和364条六字段记录已全部阅读。lossless-variable-reading.json保存原metadata键序、53个有理数字符串字典及全部364行；组编码八位为family、diagonal、wi三位、wj三位。重建原JSON的全部键值、键序和格式后158498B逐字节相等，数据中的0、重复组、零权重都没有删去。

核验共享combined依赖，不持久复制第二份：[combined_branch_master_exact.json](../full156-tail-parent-report/original/research_5/combined_branch_master_exact.json)，源5e6ada29cce2eeda7f9e，816453B，SHA-256 d1aeba67e20c8d8fc7ff38cd6566ac05c3771731f586584e5c6f1dfe233472a8。本任务实读16个hist及相随joint-reply以查R边缘、隐含00、全部层坐标；全1905列的其他语义由伴随任务负责，不记成本任务全文认证。

另全文读研究5的README(d76e7dd2c583592141a0)、HANDOFF(424d7d80cc41bfb5ae5c)、7510B生成器30ffd5d8405d7bc16953，以及正式共同阈值、强PAIR、旧回复报价/最优单换、阶段点、固定前缀停界、父方尾报告及审计器。生成器原件保在[共享程序证据](../full156-kernel-generator/original/full156_tail2_kernel.py)，其SHA-256为f84aa1a54ffba718b2f77ad65fb0f79c9ba2690fde75a5d84c53d5eb913cdc0c。

## 本轮独立运行

在仓库根运行 `python3 archives/customer-attraction/tools/evidence/full156-pair-master-point/audit_pair_point.py`。本轮实际执行成功，Python3.12.14、未开优化、退出0、stdout和stderr空；输出current-added-row-audit.json及lossless-variable-reading.json。程序拒绝禁用assert，并先核两份冻结输入SHA；仅标准库，不导入旧图模块、不调用优化器、不改原件。

代码SHA-256为d13bde57451672155e9c0844d9ffe72a203b51579980d862707924d7ac0999b1。结果55702B，SHA-256为9283105cea8fc411c1b861e261a5ffa631ca7d4811d78d09ae0a2b0ece20061f；无损表34137B，SHA-256为8b1a6af393682abda943b03f167c0e082ca888d5d991538dafd7794487ae444b。

实际检查：全部364行metadata与combined当前列绑定及R共同阈值完全匹配；10正hist、29层；所有Z质量界成立。60个Z→Z、60个PAIR(R,Z)、60个PAIR(Z,Z)的完整180个有理余量均保输出，三族最小0、零行31/18/18。2528个min交叠及5056边缘上界全部通过，其中4574个上界紧。全部新增行5236。另重建16hist总质量1、每hist的T会员数1、实际W、OPT6=1和正half差；183零、101上界、80内点、181正Z。

没有重新生成旧5108行并在新Z处求值，没有执行原pair_closure.py --master --verify，没有恢复原LP基或证明80自由变量的秩/唯一性。原10344行minimum_slack=0保作者报告身份；本轮新增子行核验不扩成原图全量新认证。即使旧combined原点通过5108行，也不能替代新Z的旧行验证。

## 共用生成和后续范围

共享生成器任务各运行一次原default和--with-welfare入口；本任务已实读其[执行记录](../full156-kernel-generator/rerun/execution.json)及[比较结果](../full156-kernel-generator/rerun/comparison.json)，没有重复执行。收益和福利数学字段全相同；计时变化使新kernel字节SHA及引用它的福利kernel_sha256变化，不能说逐字节复现旧矩。kernel的pair_source_sha256已实际匹配本包原件。

阈值实现给合法共同会员；所选必要行不推出完整SPE。旧低福利实际尾(A5,A6)末位理性、倒二有缺陷；固定前四题的真尾恰六个(Ci,Bi)，均严格高于half。后续新terminal-query cut、别的前缀或更新点不可与本原件哈希混用。完整数学定义、失败机制、旧证据与当前证据的量词边界均在正式对象中保留。
