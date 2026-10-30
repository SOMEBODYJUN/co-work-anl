# 局部权带作者核验交付

正式claim：`aa3a89ff50291360dc1f905a1bf02cce54edcc58`。本批只登记 `23daf26f771898d45fcf`（12056字节），Boss2报告 `8e829fa93d0c431621ad`（5347字节）仅作完整阅读和比较。

新增[计算正文](../../../../archives/weighted-congestion/state/计算/局部权带份额与选择器的作者精确核验--计算.md)保存原始子集定义、1858份额输入/13213 pair/224极端目标对恒等式的实际网格和连续seed规则，108态游戏的完整策略与费用，1404含432自策略比较，curl、128态填充、六线性点与五锐性点的数学机制和边界。`m=2`的rho=0.7336不是损失大于1的例；dense字段4是潜在人数而非活跃人数。

[完整证据目录](../../../../archives/weighted-congestion/tools/evidence/weight-band-verifier/)保全原代码、单独取得的冻结报告、一次原程序执行的完整JSON/stdout/stderr及真实命令/Python/cwd/hash；全部通用数学结论承接已发布份额定理及障碍。没有用不同独立包络程序冒充本源码旧执行。

实际原程序只执行一次：Python3.12.14，`--generate`，未用`-O`，约4.01秒、exit0、stderr为空。生成报告与Boss2原报告均5347字节、SHA256=`65763521378e78ff739b89b362e8d1283181594c67e37160d93de1e2434f375d`，完整JSON/原字节相同、无排除字段、无差异。另一次`compare_reports.py`只读这两份报告，不执行原审计。报告未保存全部随机输入/状态成本行；stdout又省略两个序列，均已明确，完整JSON另存。

[逐源语义回执](semantic-receipts.json)仅含本次一个源，target仅为正式正文。自查见[delivery-check.json](../../../../archives/weighted-congestion/tools/evidence/weight-band-verifier/delivery-check.json)。

精确checkpoint清单：

1. `archives/weighted-congestion/state/计算/局部权带份额与选择器的作者精确核验--计算.md`
2. `archives/weighted-congestion/tools/evidence/weight-band-verifier/`
3. `cleanup/workspaces/Boss4/weight-band-verifier-next/`

本批没有改共享README、图或他人正文，没有Git/claim/done/sync操作；由Boss串行checkpoint/pushed后登记。
