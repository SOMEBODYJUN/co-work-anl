# 极大目录与严格有序压缩：原有限实现

正式对象：[极大目录与严格有序压缩原审计的有限重放](../../../state/计算/极大目录与严格有序压缩原审计的有限重放--计算.md)。四primary原件完整保在 `original/<id>/`；原件双冻结定位、blob、SHA在 `source-manifest.json`。四规范Python依赖全部按inventory SHA核同并实读，保在 `dependencies/customer_attraction/`，它们是复现依赖，不在本批另done。

## 两次实际事件

|入口|实际参数|结果|耗时|
|---|---|---|---|
|check_maximal_catalog_boundary.py|--max-k 4 --certificate-limit 3|8游戏的2766B报告逐字节同；6完整有序证书/1608决策历史|约0.413秒|
|check_strict_compression_boundary.py|--max-L 8|L3…8/246真子目录的4016B报告逐字节同|约0.065秒|

每原入口恰一次、exit0、stderr空。原源码前后SHA相同。`replay/<entry>/execution.json` 的可用Python清单不是加载跟踪；共享runtime中有两原入口和四规范依赖，严格压缩实际只用标准库。两个事件各有自己的进程、argv、UTC和日志，没有优化器、扩展参数扫描或第二套BI实现。

原maximal报告只记录完整证书通过flag与历史数，实际动作映射当场生成验证但未输出，不能冒有一份历史完整证书文件已存。k4只枚举全部终局计数并核指定计数，不生成有序证书。有限k1…4的full最差恰2k+2不外推一般k；全k的maximal分类与full指定路径存在性依靠已成解析对象。严格压缩的全L结论亦由数学证明承担。

## 复现依赖

从仓库根执行物化器，将8份原件/依赖复制到仓库外新空目录，物化本身不执行数学入口：

```sh
python3 archives/customer-attraction/tools/evidence/catalog-boundaries-original-boss3/materialize_runtime.py /absolute/new-empty-runtime
python3 -B /absolute/new-empty-runtime/research/workspaces/customer-attraction/R-5d61c5324e744dc0a66133207fcbd010/independent/check_maximal_catalog_boundary.py --max-k 4 --certificate-limit 3
python3 -B /absolute/new-empty-runtime/research/workspaces/customer-attraction/R-5d61c5324e744dc0a66133207fcbd010/independent/check_strict_compression_boundary.py --max-L 8
```

保持assert开启，仅需Python标准库。原maximal通过脚本parents[5]寻找规范包，所以保留上述相对树；输出默认stdout，不覆盖物化的报告。若另给--output，原代码用x独占创建，路径不能已有。物化器为本轮后加的复制工具，不计作第三个数学执行。

全部原报告字段、JSON比对及域计数保在 `report-structure-comparison.json`：maximal完整八记录、六份证书1608历史，严格压缩六长度246子目录。它只核已保存报告与整数公式，不跑新SPE。所有一般证明链接在正文；旧资源“当时缺原件”事实保留，当前恢复另立日期。

`report_comparison_recorded.py` 保存这次只读比较的实际脚本字节，其顶部base/stage是记录时的绝对路径；复用时须显式改成新的本地仓库/证据根。它不自动重放原入口，不把这个记录脚本冒成无配置便可运行的独立工具。
