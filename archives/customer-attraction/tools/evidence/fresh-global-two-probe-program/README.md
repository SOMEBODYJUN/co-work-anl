# 合法单题背景的全比较主题对探针：证据身份

正式对象：[合法单题背景的全比较主题对探针](../../../state/程序/合法单题背景的全比较主题对探针--程序.md)。主源 `195c9fd7c0bf9575d1f8` 已全文 `clean show`，3601B 原件见 `original/probe_fresh_global_two.py`；没有改写原程序。

本目录保存三个不同层次：

1. 冻结的3601B源程序和源码合同。历史122B阴性报告由相邻 `fresh-global-two-probe-data` 保存，未重跑默认2000次尝试，未补写其缺失命令或逐LP状态。
2. 一次当前原main事件：`replay/run_observed.py` 用 `runpy` 加被动 `sys.setprofile`，显式 q6/cases4/seed71213/max-background4，84次HiGHS均返回success/status0。`replay/execution.json`、stdout、stderr及 `replay/runtime/bounded_probe.json` 是本次真实记录；执行发生在其中记录的scratch路径。原源前后SHA相同。没有另一轮无包装入口。
3. 一次独立 `Fraction` 接口核：`audit_probe_contract.py` 直接用均分分母重建4个IC矩阵与84个目标，将已有合法H四乘子证书接入这些原IC，再检查84个有理重构点。报告 `contract-audit.json` 记录8820矩阵系数、5292目标/恒等式、2940点上IC，全部通过；0原导入/helper/main/LP。没有重扫旧384证书。

`replay/lp-capture.json.gz` 为本次被动捕获的完整调用/返回记录，gzip mtime固定为0。解压后3108955B，SHA-256 `f8a4572d3d669f7eb9c2200ceb5bf21d90fd4dd1c5afd10a3ba6fabe35cc6e37`；压缩只是存储转换，没有删字段。84份数组包括每次约束、归一化、目标和全部返回权重/状态。重复约束也原样保留。

审计脚本是实际执行的原字节，期待在其自身目录读取 `lp-capture.json`。如需新的明确复核事件，应先将该脚本和解压JSON复制到新的scratch目录，再运行；不要在此冻结证据目录覆盖已有输出。被动运行包装器同样保留实际执行时的路径常量；新复放应选择新runtime且明确记录路径调整，不能把旧执行记录当作新事件。

本次浮点目标最小为约−5.55e−17，84个解的有理重构全部精确可行；10目标零、74正。已有H符号证书给全部目标下界0，故10个零点亦认证其相应锥问题最优0。74个正目标是精确可行值，本目录未提供其精确对偶或精确最优性证明。

`source-manifest.json` 为源、事件和核心文件指纹，`comparison-manifest.json` 为全仓实际阅读与区别，`self-check.json` 为最终静态自查。正文给模型、全离轨策略、全部平局、输出阈值、合法H证书及一般前缀反例的边界；这些不能由本目录的success字段替代。
