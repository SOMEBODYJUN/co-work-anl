# 森林报价与分叉割的原件及复现

`original/`保留本批10份源的全部字节，包括两份正文、两份审查、三份程序和三份冻结JSON。`source-manifest.json`逐项列稳定源ID、路径、两来源commit、大小、blob与SHA256，不把源文件名当数学对象身份。

原程序仅用Python标准库，精确算术为`fractions.Fraction`或整数；没有网络依赖。本轮从本目录运行`replay/run-record.json`的三条命令，退出码均0；三份结果的字节hash均等于原冻结JSON，结构差异为空，见`replay/comparison.json`。运行解释器为Python 3.12.14；本轮没有修改原程序、seed、参数或冻结证据。

之后可在此目录运行：

```bash
python3 replay.py --out /tmp/incidence-directed-new-run
```

输出目录必须不存在；脚本先核对10份原件hash，调用原程序，记录实际命令、解释器、退出码及原/新输出hash。改变解释器可能改变版本元数据，不能将元数据差异说成数学失败；任何其他变化需要逐项解释。`replay.py`是本轮新增复现入口，并非历史独立审计实现。

`run-record.json`还核对森林§1—6、§1—7和分叉割后加共享side链接前的字节前缀，与审查所写freeze一致；没有初始分叉临时稿，故没有伪造两版diff。有限运行不能代替一般实权、非连续费用或任意拓扑证明；固定单环四态枚举只承担该固定实例。

自足数学和证据范围见[state/计算对象](../../../state/计算/森林报价与分叉割的精确有限核验--计算.md)。原JSON中“WC target open”为历史输出字段，原字节保留；当前全类Cd/ln d目标已被另源全状态线性下界严格否定，不能从未改动的复跑字符串恢复旧状态。

`related-search/`保留Boss实际四次全冻结Markdown正文搜索和查询manifest，命中数18/18/17/12；除已读证明/审查外仅发现入口表与账本，入口没有被当作独立证明或额外完成源。
