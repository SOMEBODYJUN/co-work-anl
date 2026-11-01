# 重复覆盖主题商：作者有限回归报告

正文：[重复覆盖主题商的有限回归报告](../../../state/计算/重复覆盖主题商的有限回归报告--计算.md)。本任务只处置源 `123d877633bcc8a2c79d` 的339B九字段作者报告，SHA256 `e9290b6074fb49286de774237f2ead2d4130adfe3bb784f587c572f87700b407`。原件共用 [已有保全文件](../action-quotient-parent-replay/related/duplicate_action_quotient_test_report.json)，不另复制；两冻结提交、源码、父报告和原数学稿定位见 [source-manifest.json](source-manifest.json)。

此前已有 [原作者测试执行事件](../action-quotient-parent-replay/replay/execution-event.json)及 [339B stdout](../action-quotient-parent-replay/replay/author-stdout.json)：两份源代码未改、assert开启、PYTHONOPTIMIZE移除，exit0、stderr空、约3.760秒，输出与本主源逐字节相同。本任务和本批关联核心/测试源共同复用这个事件，不新增作者入口运行，也不把同源重放计作另一独立完整测试实现。

- [inspect_report.py](inspect_report.py)只读取并核对已有字节、九字段、计数表和全部200病例诊断；没有编译器导入、原测试、BI或RNG调用。
- [report-interpretation.json](report-interpretation.json)保存九字段及其父报告/现存重放对应、67626=3840+7800+55986和43=16+27等真实范围。
- [case-domain.json](case-domain.json)列完整64个两人输入、16参数SPE计数格、200条已保存的诊断及六人固定输入。两人SPE数和三人诊断来自此前 [count-semantics.json](../action-quotient-parent-replay/replay/count-semantics.json)，本次逐项解释与整数核对，没有重新验证这些策略。
- [selfcheck.json](selfcheck.json)记录实际落地文件、源SHA、九字段/表格/病例列表、语法和相对链接核验。

原339B报告没有200例完整客户重数或policy。现有诊断也只保存游戏号、商类数和末位标签/覆盖差异的动作索引；本包明确不将其伪装成完整策略证书。43只检测历史(0,a)/(1,a)处原动作编号不同，其中16例覆盖类也变，27例仅别名变；它不检验同标签计数不同顺序下的Markov性。

仅重放本包的记录解释检查，可在结果仓库根目录运行：

```sh
python3 -B archives/customer-attraction/tools/evidence/duplicate-action-quotient-test-report/inspect_report.py --repository . --out ../duplicate-action-report-inspection
```

选新输出目录；脚本拒绝禁用assert的解释器。它不会运行旧测试或重采样。本报告穷尽的只是两人三标签64输入上的策略域；三人200例每例一份BI策略，六人只有一个全大主题完整策略（W6、OPT₆11）。任意人数、目录、完整SPE的双向商结论来自既有解析定理，而非这些有限计数。
