# 对称终局见证作者源与定义级策略审计证据

本包实际primary仅三源；认领原回执[完整保留](claim-receipt.json)：Boss4、pushed/synced、tip `616781c7ec3000f5b043bfdf3ce9882886dcc29a`。没有占用其引用的其他程序/数据，没有共享Git写入或新领/done。正文待Root串行保存；本地成熟不等于已推送。

| ID | 原文件 | 字节 | SHA-256 |
|---|---|---:|---|
| bc20125e178455c0cc11 | [README](original/research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/credible_search/README.md) | 5914 | 4daf831443ddce0a26c0f0b608a29d65f2a25460e0abb005a5742af6a351f698 |
| 9c75087e540ebd1d488a | [正向群商稿](original/research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/credible_search/outcome_orbit_quotient.md) | 5410 | 8d10c5e87e9742f335c70f274be5c1845a18d36c416ab10bf66d7ad1645c842a |
| 3606a34fbf8e1c5980f5 | [原审计程序](original/research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/credible_search/audit_certificates.py) | 6146 | c0afb75176e136cb64d30963828f2f9bd4d0b945a93670a6d0bb1dc02e873188 |

[primary-inventory](primary-inventory.json)记录完整冻结commit/path、blob、SHA、行数与本地owner；[原本地导出清单](primary-local-export-manifest.json)核size/SHA256/Git blob SHA1。两冻结提交同内容只是一项源，不多算数学独立性。全部读取纯本地，缺blob没有网络fallback。

## 正式数学和去重

- [作者版本与有限候选](../../../state/资源/对称输入终局见证商的作者版本与有限候选--资源.md)：正向群商、输入类型组合重数/标记对齐、八候选全部原声明、两个精确点、30回归及审查时态。原群商完整双向证明已在[既有独审](../../../state/审查/固定输入同时轨道商的存在性与选择器边界--审查.md)，不重复授定理。
- [定义级审计算法](../../../state/算法/完整有序策略的定义级均分证书审计--算法.md)：从全有序后继归纳证明SPE检查正确性、精确覆盖/OPT、同计数冲突含义、glob真实输入合同与schema/零福利边界。

九份当前正式比较全文和其hash保存在[context inventory](formal-context/inventory.json)；这些是用于比较的冻结快照，旧相对链接按原正式路径解释，不替换共享正文。[comparison findings](comparison-findings.json)列已有证明去重、独审先验与未改共享页边界。

## 原glob域缺失，未执行原main

原main扫描脚本同目录全部 `*.json`，先以 `exact_candidate.certified` gate，再对两个candidate键各取其instance、共用第一键strategy，写同目录 `certificate_audit.json`。空目录也可exit0且records空，因此本次不作该调用。

[实际本地缺失清单](candidate-input-availability.json)有十一项：八个sym候选、warm_start_smoke、certificate_audit和同blob的audit_stdout。主导出清单另记录 `symmetric_dag.py` 与 `symmetric_dag_regression.json` 缺失。没有拿别的构造、不同schema或本文打印数值替代原输入。原八策略各2801/16806、两保对称门槛、30回归8/22、原搜索最优/时限均只保原文字声明。

`source-table-arithmetic.json`只核两个打印点的分数与收益加总，不认证策略。原代码main、原MIP、LP和30回归本次执行次数均为0。

## 旧同SHA函数调用的复用层级

[旧inventory](reused-acyclic-function-record/inventory.json)保全同SHA函数、旧独立调用程序、两固定输入、旧原报告及保存的replay报告。18432B报告两份逐字节同SHA `a8502a84fca9e7de11d9b5ae4b4720c26766d2f2c6fabfcdfc3149c3d5f1ea47`。调用域是52客户4/6的259历史1295非自身比较和86客户2/5的6历史24比较，不是八个sym策略。

完整历史重建驱动/源清单亦复制作为证据，但这里是**所用依赖的部分保全**；驱动还需要旧包的author相关文件，不能直接在这个裁剪目录执行。原完整包与[已完成计算页](../../../state/计算/无环真实替换的双实现精确核验--计算.md)仍是旧重建入口。该旧包未附单独进程event/stdout，本次不虚构；复用的是已保存报告及原重建记录，不称本次见证旧进程或新时长。旧audit函数被比较依赖使用不抵本次primary完整处置。

## 一次新控制程序，非旧候选复现

[新控制程序](probe_validator_contract.py)只用标准库，载入原字节的audit函数，**不调用main**。一次新空输出目录执行，exit0：

- [全部四正例输入](new-contract-check/new-control-inputs.json)：两互斥单例、3/1/1三主题已知5/3、同覆盖标签且同计数不同动作、一合法空主题。合计26历史/39非自身比较。
- [完整结果](new-contract-check/result.json)：四正例通过；删历史、重历史、错根计数、离轨不理性四项按预期断言拒绝；合法零福利例按预期触发原比例字段除零。两同时轨道索引枚举准确为2520/2446和6265/6134，无商42345/41888。
- [真实event](new-contract-check/event.json)、[stdout](new-contract-check/stdout.txt)、[stderr](new-contract-check/stderr.txt)：原main0、solver0，无新时限搜索或外部依赖。

输入/结果中所有新小例都标为EB构造，不冒充Root新输入或原历史证书。控制程序以清晰的新完整策略检验接口与维数；普遍正确性依赖正式算法的归纳证明，群商等价依赖已有解析证明。无本次新盲审、外审、新颖性、一般half或联合最优认证。总执行身份见[execution boundaries](execution-boundaries.json)。
