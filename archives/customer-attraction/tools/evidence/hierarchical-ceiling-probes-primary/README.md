# 公共核对称DP与层级浮点探针原件

本批八主源10315B，全部原size/SHA-256/Git blob核同。`original/`按冻结路径保存三个.py及五个JSON；相邻interval_hierarchy_probe会导入hierarchical_ceiling_probe的rows_for，另外需要外部NumPy。common_core_ceiling_probe只用标准库。原码/报告不修改，没有额外依赖源码需要下载。

数学正文分为[公共核对称占用算法](../../../state/算法/公共核等私客放松的对称占用递推--算法.md)与[层级浮点筛查资源](../../../state/资源/层级目录的浮点剪枝探针与冻结候选--资源.md)。前者有完整最大占用/对称轨道等价证明，后者完整保生成域、三候选全部客户行、浮点容差及40/80/仅best三种不同历史记录范围。

本批新增原main0、自写数学checker0、旧成功重跑0，无当前PASS。五JSON是冻结历史数值，未记命令/退出码/代码SHA/NumPy版本；m16仅best不代表批完成。精确OPT可由其整数行及m>=q证明，G_float未有理重放，不把小数理性化为精确值。

实际20源claim原完整回执为`actual-claim-original20.json`，pushed/synced commit c526dcd14714c47beab04912f6746d7b35a734e3；本8真实子集核在claim-scope-verification。normal-show八原捕获及其原完整manifest保在acquisition，语义与SHA逐项列primary-source-manifest。冻结报告全部字段另有frozen-report-full-readback，当前全仓比较保current-comparison-manifest。

若后续新问题需要重放，应复制整个original树到独立目录；两个浮点run会覆盖脚本相邻best/summary，不提供输出目录，stdout带BEST/DONE前缀。当前并未执行这些建议。Phase2仅解释实现/有限筛查/结构类边界，Phase3超图未在此生成。
