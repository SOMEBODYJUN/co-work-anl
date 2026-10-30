# 反馈环、资源干预、稳健校准与稀疏门证据

本批16原件85551字节全部完整读取，另5份比较依赖完整取源/阅读；source-manifest.json明确claimed与comparison-only，后者不扩done分母。original/从未就地执行或改写。相关数学按证明、算法、反例、构造及审查分别建正式对象。

四原程序在各自replay/子目录的同字节副本实际各运行一次；四退出0、stderr空，所生成报告分别与冻结audit.json、sparse_gate_audit.json、feedback_cycle_audit.json、audit_result_v2.json逐字节相同。robust当前代码写audit_result.json，但数学结果对应v2；旧v1唯一少global_threshold_report_regression，version-comparison.json明确范围。旧报告无代码hash，不由JSON猜旧完整源码。

replay.py隔离程序同目录写文件副作用，保存stdout/stderr/实际报告/源和副本SHA/比较。若需重新复现，使用新的输出目录，例如：

```sh
python3 archives/weighted-congestion/tools/evidence/scale-robust-intervention/replay.py --output-dir /workspace/scratch/37f0f9248cfc/boss4-next-cache/scale-robust-fresh-run
```

该目录必须没有先前生成报告；脚本拒绝替换已有运行。此说明的命令未再次执行；本次四份已通过审计没有例行重跑。

稳健审计通过只读call profiler保存全部2180个真实threshold_extrema参数（num/den/lower/upper有理字符串），没有替换原函数。其余输入全部确定性地在原代码中，随机部分另固定seed20261021。有限盒/图/位串/小游戏不证明一般量词，不是完整并发协议实现或部署测试；MaxCut稿没有专门程序运行，外部无权简单Max-Cut一手前提仍未核得。

related-search/保存5个全冻结精确字面检索及完整读段；0命中不证明无相关，另按攻击归属取齐repair_design三文件。candidate反馈稿与root_feedback原稿SHA550ccb…逐字相同，实际逐字比较可核；入口自报快审不替代缺失底层审查文本。bounded_degree_gate_design.md仅被README引用、未在冻结inventory见原件，未假装恢复。
