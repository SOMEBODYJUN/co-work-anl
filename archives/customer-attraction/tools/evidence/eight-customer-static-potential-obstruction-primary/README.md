# 八客户静态PNE逐客户负载势比较障碍

本包保全五主来源共7463字节：旧independent_bottleneck/README及四份potential原稿、脚本、报告。`source-manifest.json`列出两个冻结位置、源ID、大小、SHA-256、blob及保全路径。四势原件已由旧保存恢复，本次与父方正常导出的五份冻结源逐字核同；新增README原件与另九源CCE包同字节。旧清单缺失的相关count-policy路径已改为实际存在的相邻证据包，不复制冒造缺失文件。

完整数学见[八客户静态势障碍](../../../state/障碍/静态均衡逐客户负载势支配的八客户障碍--障碍.md)，程序及来源合同见[五源资源](../../../state/资源/逐客户势静态桥的五源合同与精确核验--资源.md)。本例在三人原单位客户模型里有完整σC终局011；静态PNE仅112、113、123。对f0=0、f1>0、f2<2f1、f3任意，PNE与011的差分别f1、f1、4f1−2f2，均正。调和势8对9，覆盖6对7或8；不是六人half反例。

`original/`中五原件从未修改。`potential_bottleneck_audit.py`只核静态分类与逐人调和势边际，不核SPE。已有完整σC程序、输入和成功21节点84比较保存于相邻`independent-cce-ordered-count-versions-primary`包；本批全文读取并核其成功事件与冻结报告字节，新增σC运行0次。两证据的数学作用不能互换。

四势恢复包原来没有成功静态重放记录。本次在clone外新目录对1305B静态原码仅执行一次，`python -I`、assert启用，exit0、stderr空。`runs/static-original/`保完整stdout、stderr、原生成1600B JSON、执行事件和核对；生成报告/冻结报告/stdout逐字节相同。没有新实例扫描。原脚本输出的768是64×3×4名义候选空间；`all(...)`遇首个盈利偏离会短路，不是实际求值计数。192条调和删除边际断言则确实逐项执行。正式正文另给不用枚举器的静态PNE解析穷尽。

如需复验，从仓库根运行，指定尚不存在的输出目录：

```sh
python3 archives/customer-attraction/tools/evidence/eight-customer-static-potential-obstruction-primary/replay_static_original.py --output-dir /tmp/cag-static-potential-replay
```

包装器先核五原件hash，并只读取已有σC运行证据，再复制原静态程序到指定新目录执行，避免它覆盖冻结JSON。不要在冻结原码旁直接运行或import原码；原顶层没有main guard，会写同目录同名JSON。

`relationships.json`是本批人工关系判断，保同实例顺序可信性与静态分类的联合前提、与既有PNE/Φ<OPT/删除漂移/客户编译障碍的区别；不代替第三阶段图。未认证外审、新颖性或规模最小性。
