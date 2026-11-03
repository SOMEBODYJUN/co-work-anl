# 两份早期包含原复算脚本

本包由[统一K三行程序](../../../state/程序/统一K三行系数障碍的固定有理复算--程序.md)与[1960型双包含程序](../../../state/程序/双包含半覆盖的去交集一千九百六十型复算--程序.md)拥有。两份原件沿实际冻结路径保存；`source-manifest.json`保完整提交、源ID、blob、size及SHA。

883B入口打印三行tuple与必要λ文字，只核三行障碍。1227B入口打印含Fraction/tuple的Python字典repr，核1960去交集系数域。两者无main guard，导入也执行；仅标准库，不读写文件。stdout均不是JSON。断言须启用。

本批以`python3 -I`各执行未改原件一次，`execution.json`与`rerun/<源ID>/stdout.txt`保新执行记录。两冻结源均未附独立stdout；新捕获不改写原历史。旧3118B审计的405B JSON、3360型独立重构与早先1960/三K重构仅被读取复用，未在本批重跑。

从仓库根复核两份原入口（只产生stdout）：

```sh
python3 -I archives/customer-attraction/tools/evidence/two-early-replay-source-contracts-primary/original/research/workspaces/customer-attraction/subagent-f/replay_m6_r2_uniform_K.py
python3 -I archives/customer-attraction/tools/evidence/two-early-replay-source-contracts-primary/original/research/workspaces/customer-attraction/subagent-f/replay_m6_two_early_A_half.py
```

`comparison.json`保存实际实读的相关对象和关系判断；`self-check.json`是字节、执行合同与引用结构检查，不是新数学认证。没有游戏/SPE搜索、LP、外审或一般六人half结论。
