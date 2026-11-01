# R51路径与末尾删行障碍的560记录报告

正式对象：[R51路径末尾障碍有限审计](../../../state/计算/R51路径末尾障碍有限审计--计算.md)。主源 `5fbb919968e92b8c7ad2` 为277934字节JSON，固定 \(2\le m\le15\) 的560个参数组，不是560份完整SPE证书。

- `original/path_tail_obstruction_audit.json`：完整冻结报告，未修改。
- `related/`、`manifest.json`：配套4937字节生成器、父审MD、发现稿及四源冻结定位、字节数、SHA-256。
- `verify_report_fields.py`：不导入原生成器或规范求解器。重建全部字段，定义级执行134400个actual行动比较、455条远轨见证和12694个小树比较；尾count245478仅独立计数。
- `field-check-result.json`、`field-check-event.json`、`field-check-stderr.txt`：真实独立结果、命令、退出码、耗时、输出哈希和空stderr。
- `complete-field-ledger.tsv`：全部560条记录所有字段与嵌套值，没有抽样省略。
- `independent-full-negative-rows.json`：独立重放415条小树负IC，含参数、历史、动作及有理收益。

从仓库根目录运行：

```sh
python3 archives/customer-attraction/tools/evidence/R51-path-tail-obstruction-report/verify_report_fields.py
```

本任务不重跑原生成器。同批程序任务已执行一次隔离重放，见[事件](../R51-path-tail-obstruction-auditor/run/event.json)与[新报告](../R51-path-tail-obstruction-auditor/run/path_tail_obstruction_audit.json)；本任务已核其与原JSON逐字节相同，stdout仅两行摘要。

105项 \(d=1\) 是全效率边界，455项 \(d\ge2\) 均有指定早期负行，41个形式根低于half全部来自后者。\(m>4\) 的full/负行计数0表示没有扫描全树，尾计数也仅五个明确 \(r=0\) 实例。一般量词由解析证明承担，没有六人或一般half反例。
