# 全后继平稳运输：原程序和冻结报告

701B原程序与259B报告的完整原字节、双冻结路径及SHA在source-manifest.json。两份全文实读；报告source_sha256与代码字节一致。数学定义、一般余量因式分解、两状态局部锐性与SPE边界见[正文](../../../state/计算/全后继平稳运输的有限有理重放--计算.md)。

## 重现

```bash
python original/replay_stationary_successor_transfer.py
```

仅Python标准库，不要使用会移除assert的`-O`。脚本无参数、main守卫或输出文件；import也会运行。范围n1至12、b0至15、t0/1、z0至n共2880型；n2至12另验11个两状态比值。计数不是游戏/策略数。

## 当前事件

在clone外按原字节执行一次，约0.0306秒，exit0、stderr空，stdout三结果与冻结JSON三计数字段逐值一致。新stdout不是冻结JSON；原报告额外SHA/review两字段保留不改。runs/execution.json记录真实argv/UTC/版本/耗时/输入输出SHA，stdout/stderr各保原字节。本批没有第二套独立数值实现、完整SPE枚举、优化或新定理搜索；一般证明由正文及已有平稳引理承担。
