# 成对水库停止收费的原件与一次回归

[数学正文](../../../state/计算/成对水库停止收费的奇偶算术回归--计算.md)保存完整参数、真实尾地板的依赖、位置数及奇偶恒等式，并隔离9/5的条件身份。

- `original/audit_pair_source_arithmetic.py`：源e92c958804c538f9cc28，890字节，冻结原件。
- `original/pair_source_arithmetic.json`：源5d613b705fb300a005ea，813字节，六行输出及三个说明字段。
- `source-manifest.json`：两源完整冻结元数据，包含内容SHA-256、Git blob和两个来源提交；导出后已逐SHA核同。
- `replay/`：隔离复制的原程序和本轮一次执行输出，避免覆盖冻结原件。可用`python3 replay/audit_pair_source_arithmetic.py`复现，程序输出写在自身旁边。
- `replay-report.json`：真实一次执行的返回码、stdout、stderr、耗时和原JSON逐字节相等结果。

执行只含k=4至100的97个整数算术检查，0个LP、随机或SPE程序。全k结论由数学正文的解析恒等式和另有自足证明的完整历史地板共同承担。父方阶段二审查仅供历史语义比较，不在这两条done中重复登记。
