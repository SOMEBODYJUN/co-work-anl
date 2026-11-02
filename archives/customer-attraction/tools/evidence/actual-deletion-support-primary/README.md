# 实际删除支持障碍：primary原件与新事件

父来源冻结提交：`68fad804ec5946cb296f77dc5b336308a66abf12`；目录：`research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/security_aggregate/`。

- `deletion_obstruction.py`：源0c2ea8e325af864314f5，未改原件。
- `deletion_obstruction_audit.json`：源0927b908a1332c13d23d，未改历史输出。
- `replay.stdout`、`replay.stderr`、`replay-event.json`：本次隔离重放；原源码恰运行一次，stdout与历史JSON逐字节一致。
- `independent_check.py`、`independent.stdout`：本次独立bitmask/Fraction核验；不导入原代码，增加静态安全值双证、OPT和零/全兴趣/加倍边界。
- `manifest.json`：本包除manifest本身外各文件SHA-256及字节数。

复现：在本目录运行`python3 -I deletion_obstruction.py`及`python3 -I independent_check.py`。两个入口只打印stdout，不覆盖原报告。标准库即可。

数学正文：[单位客户原审计](../../../state/程序/实际终局删除支持障碍的单位客户原审计--程序.md)。仅有限固定实例和受限构造障碍，不是一般六人half反例或证明。
