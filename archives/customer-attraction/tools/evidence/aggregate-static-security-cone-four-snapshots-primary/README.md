# 聚合静态安全交替程序与四份保存点

五份原件从实际`work.py clean show ID`取得，按`source-manifest.json`冻结大小和SHA-256核对。原件不修改；两冻结来源位置同字节。`reuse-scan.json`记录补录前对当前checkout其余路径的同哈希复用检查，没有命中。正式自足合同、全部参数和数学边界见[程序正文](../../../state/程序/完整策略锥聚合静态安全交替搜索与四个零间隙保存点--程序.md)。

`verify_snapshots.py`只用标准库。先核五原件指纹，再对四个显式有理恢复及原十进制输入独立从定义检查全部有序历史；对恢复点逐静态背景检查原始下界、固定纯背景检查对偶上界，生成`rerun/exact-report.json`及`rerun/summary.json`。报告含每个历史的指定行动、终局、全部行动收益和slack，以及全部276个静态背景的纯查询值和查询期望。JSON重复键会被拒绝。程序不导入发现器、LP或SPE求解器。

总计3021节点、20729行动比较。恢复点都完整SPE且W=m v；原7_5精确十进制却在根有负slack−1/50000000000000000，故有理恢复与原浮点状态分开。所有恢复质量乘20或7可成为有限不同单位客户。原mask、target、sigma与query_p均保全；target在6_3和7_5是计数代表，实际有序路径不同。

`replay_smoke.py`绑定相邻[search_cce原件](../security-cce-search-program-primary/original/search_cce.py)的SHA-256，运行原安全脚本的新`k2,m2,trials1,seed1`试验。`rerun/smoke-execution.json`、stdout、stderr和best保存真实执行，未重建四份缺运行参数的旧搜索。导入依赖4806B、SHA-256 bf868944a4c4400b408db663626b3cb9223fb4acd9a5cbe99bc83590a888cc26、源ID60bd06f1f9dcdc4e5347。

仓库根运行：

```sh
python archives/customer-attraction/tools/evidence/aggregate-static-security-cone-four-snapshots-primary/verify_snapshots.py
python archives/customer-attraction/tools/evidence/aggregate-static-security-cone-four-snapshots-primary/replay_smoke.py
```

没有新全称聚合安全定理、全锥证书、六人half结论、外部审查、新颖性或最小性认证。本包五源逐项语义回执位于`cleanup/workspaces/Boss7/resume-current/security-snapshots/receipts.json`；回执本身不代替上述数学核验。
