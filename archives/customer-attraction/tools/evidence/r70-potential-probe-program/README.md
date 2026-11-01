# 有序自复制税势预算探针的证据

主源 b3e90092c8c176acf8e7，原潜势探针2951B，原字节 SHA `b902078f2d0486182e904be371956c1bd82bd6b9f1261d50621b56666412e8f1`。来源和全读比较指纹见 `source-manifest.json`，数学/输入/输出自足说明见[程序正文](../../../state/程序/有序自复制税势预算的全SPE终局探针--程序.md)。

`original/potential_probe.py` 原样保留。只有stdlib，无外部模型依赖；`audit_interface.py` 是本次新检查器。它恰一次执行原main（runpy，同一Python进程，显式m3/k2/trials1/seed670305）并被动捕获已有返回表，另调原one三个新输入。原main1/one4/LP0/成熟旧点重算0。包装器实际exit0；main正常返回，无单独原进程exit码。原main约0.01199秒，stdout91B/stderr0。原码前后SHA同。

`new-interface-event/` 保全部原stdout/stderr、execution和完整interface-audit。定义核穷举418份完整纯策略并沿各自真实后继核5528比较，211份SPE；四个输入56前缀集合、84收益、34势单元及预算/返回值全部一致。报告保所有34终局值和全部前缀集合。这是四个固定新小实例的实现核，非默认千次扫描、旧stdout复现、一般P0证明或六人half认证。

`check_package.py` 只做源字节、AST/JSON、真实事件字段/既存审计摘要、相对链接及receipt检查，不执行原程序或数学枚举；产物 `self-check.json`。已读的SIX_BRIEF由同批root唯一保在相邻 `r70-six-provider-entry/original/`，不重复存。原入口和新接口如确需再次运行，必须使用全新输出目录并另计事件，不能覆盖本事件。
