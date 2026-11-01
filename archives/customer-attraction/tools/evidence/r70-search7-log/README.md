# 七极大六人搜索日志的证据

主源 `cdcebe2079bef8ffb20b` 是 [scan_36155.txt](original/scan_36155.txt) 的全部 2509 字节、24 行、12 次改善。正文为[七极大六人搜索的十二次改善记录](../../../state/计算/七极大六人搜索的十二次改善记录--计算.md)。原文件没有历史命令、seed、预算、stderr 完成行或退出状态；文件名 36155 不补作这些字段。所有保存的 half 余量为正。

## 本包的一次实际核验

[audit_log.py](audit_log.py) 从十二组不同单位客户直接构造七主题集合，核 12×924＝11088 个静态覆盖、84 个遗漏一主题的覆盖、12 个声明叶的精确份额、全表参数、严格改善与原六位有效数字 token。结果为 [log-audit.json](log-audit.json)，完整多重集覆盖表为 [static-coverages.json.gz](static-coverages.json.gz)，[execution.json](execution.json)记录这唯一事件。

它不导入原程序，不调用 ELF、LP、随机搜索、SPE 集合递推或完整策略重构。静态审计不单独认证任何点的根可实现性或根最低 SPE 福利。它首次执行时读取仓外冻结导出 `/workspace/scratch/c0ab78c47566/round17-r70-scan_36155.txt`，输出到脚本所在目录；这里保留原脚本与事件字节，没有事后改成一个并未执行过的命令。若将来重现，先把 SOURCE 改到本包原件，并在新的空输出目录运行，须记作新事件；当前代码以 `open('x')` 防止覆盖既有结果。此说明不要求再次执行。

## 共享程序包的不同事件

已全文读原 [search7.cpp](../r70-search7-program/original/search7.cpp)，并对照当前 ELF 原始结构输出及[短事件](../r70-search7-program/binary-event/execution.json)：旧 ELF 和一次新编译件各以 `1 192711` 执行一次，两者 stdout/stderr 相同，预算 1 实际 2 次评估。新编译件与旧 ELF 字节不同；短事件不证明历史长日志的命令或二进制版本，亦不证明所有输入等价。本包没有再次编译或运行。

共享[末点独立事件](../r70-search7-program/last-point-execution.json)仅对 eval47752 的 159 客户点重新构造单位客户收益，作一次整数集合 DP 和一次完整有序历史策略核验。其覆盖值直接复用本包末点 924 表并绑定 SHA，而非第二次独立覆盖扫描。[结果](../r70-search7-program/last-point/point-audit.json)为 1716 个 R 集合均单元素，根计数 (0,2,0,0,0,0,4)、W131、OPT158；[完整策略](../r70-search7-program/last-point/complete-strategy.json)有 19608 节点、137256 个比较，自身比较零 19608 项，所有非自身 117648 项严格正，最小正余量 1/10。新实际路径为 (6,6,6,6,1,1)。[明细](../r70-search7-program/last-point/exact-details.json.gz)保集合与全部比较，正文给出由全历史严格性推出唯一纯 SPE 的归纳。

前 11 点新增的是输入、静态最优覆盖、指定叶收益及输出算术检查；没有借末点认证替代它们的完整 SPE 审查。三个计算事件分别是本包静态核、共享短 ELF 检查、共享末点 DP/完整策略核，绝不合称原长扫描复现。

## 身份与静态自查

[source-manifest.json](source-manifest.json)绑定主源、全部本包交付及共享依赖；[shared-evidence-review.json](shared-evidence-review.json)记录实际解析共享结果的作用域与输入 SHA；[self-check.json](self-check.json)只作结构、链接、源字节和共享输入绑定检查，不重复任何数学入口。

日志 SHA-256 为 `ebe12aedf423068a7db88401b75113d69f43ae0ed2626d2efc264aa490581afb`；独立报告 SHA 为 `ce61c3d8f22b1cf352dbb45befd7accbfbe006877ff12f069d2c06f3077f9274`；gzip SHA 为 `9debdd77f04c61f65f3dd62fd6d55b134799df7c80016e435aab5f0709d59366`，解压 SHA 为 `eec0169b49c903d6bac1374634899fcda0340f3a7517deaef8bad7507b885a9b`。关联及比较已写正文，本阶段不另建关系图。
