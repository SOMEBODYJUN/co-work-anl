# 三人分数推送快照的证据与当前重建

主源 `35e31246cf15d1179101`，原路径 `research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/security/pushforward_fractional_candidate_individual_security_failure_0.json`，1636B，SHA256 `05bc79520b37efa566dc34d332de481cc194d038e8f2ac2d1cf41cb761d40e0e`。`original/`原样保留六字段；`related/`是已全文读取的原输入、完整策略及相关代码/说明的字节副本，不属于本次认领范围。两冻结提交为 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`。逐文件原来源和内容指纹见 `manifest.json`。

正文为 [三人个体安全推送分数候选快照](../../../state/计算/三人个体安全推送分数候选快照--计算.md)。重要身份差异：name指向的旧输入是34客户，本快照权重却在舍去10^-15级漂移后等于已知36客户输入/10；两份输入有同一张43动作完整策略。原十进制权重若视为精确数，产生61项微小负IC，不能用它们冒精确SPE证书。

`verify_snapshot.py`是本轮新写的标准库定义级重建器，不导入原审计器、规范模型、SPE求解器或浮点优化器。执行：

```sh
python3 archives/customer-attraction/tools/evidence/pushforward-fractional-individual-snapshot/verify_snapshot.py
```

2026-11-01当前执行exit0，输出 `PASS-current-reconstruction-not-original-CLI`。其输出 `replay/reconstruction.json`记录全部六字段语义核查、字节SHA、原十进制诊断、恢复36客户后258项完整IC、216终局收益守恒、保存gap的浮点公式重建及显式归一化p的精确有理差；`replay/rationalized-ic-table.json`保258行真实后继比较。当前恢复权重与归一化p的正gap约0.019283932400532812；完整保根三槽则为负；全六标签自由两槽cap333/350<根1。

此重建证明指定公式与保存gap吻合，不能重建历史优化过程。冻结Python内容搜索 `pushforward_fractional` 无命中；相邻 `full_terminal_push_probe.py`保存不同schema并测试保根r槽，不能冒称就是该JSON生成器。`extra=0`的删根解释由配套质量约定与当前公式匹配支持，缺失原schema之处在正文明确保留。

已有解析引理承担整个四标签/两列连续最优值161/15及自由六标签333/35；本程序只核明确点，不再搜索连续最小值。不重跑随机LP/SLSQP扫描、不把本轮重建改称原CLI重放、独立发现或新的反例。receipt只处理主源，相关源不由本目录代办done。
