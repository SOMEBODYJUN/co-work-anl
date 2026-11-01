# 单背景主题随机回复图报告的数据合同

[自足计算对象](../../../state/计算/单背景主题两人回复图的随机探针报告--计算.md)解释主源 `369a02858830364f3155` 的全部130B与六字段。本报告是q=7、L=1、12000次有放回随机回复图的历史汇总；best=0是从未更新的阈值哨兵，不是LP最优值。seed、图清单、不同图数、每图目标及客户权重均未保存。

| 文件 | 内容 |
| --- | --- |
| [original/fresh_arbitrary_probe.json](original/fresh_arbitrary_probe.json) | 两冻结提交同字节的130B历史报告 |
| [inspect_report.py](inspect_report.py) | 原报告和原程序AST的静态解释器，不运行随机数、原函数、原算术块或LP |
| [data-contract.json](data-contract.json) | 本轮首次静态运行输出；六字段全值、best唯一赋值、末尾返回键、默认值与历史值区别、127型/48行/117649图的结构解释 |
| [source-manifest.json](source-manifest.json) | 原源、比较材料及共享合成接口核的正式指纹和路径 |
| [check_package.py](check_package.py) | 收尾静态核：文件绑定、保存记录结构、链接、回执；不重做系数或LP |
| [self-check.json](self-check.json) | 实际静态收尾结果及正式文件清单 |

原2412B生成器只在[程序包](../fresh-arbitrary-reply-probe-program/original/probe_fresh_arbitrary_reply.py)保存。完整合同见[程序对象](../../../state/程序/合法单题背景的任意末回复策略锥探针--程序.md)。程序包另有一次[共享合成接口核](../fresh-arbitrary-reply-probe-program/cone-contract-audit.json)与[真实执行记录](../fresh-arbitrary-reply-probe-program/audit-execution.json)：人工q7/L1/seed0、回复[6,2,6,3,0,2,4]，原AST算术片段执行1次，原run/main和LP均0；6223收益项、6096 IC系数及127目标项与独立有理式核，浮点误差另存。它不是历史12000轮的复放。本数据任务未重复这次算术核。

报告中的127是非零主题会员位掩码，质量w≥0且Σw=1。固定r(1)=2的回复图有7⁶=117649个；每图有42末位IC、6首位真后继IC。所有质量放mask127便使所有IC为0、目标2/3，所以任意图的归一锥非空；满额feasible计数并不是稀有或非退化策略实现的证据。

目标是P+Δ−指定T/S的新覆盖。合法H四乘子证书可以转换为两条首位真偏离、两条实际末位查询和逐型非负余项，故对全部精确可行图有目标≥0；全L的结论来自[解析证书](../../../state/计算/背景菜单的有限证书--计算.md)，不是12000次浮点抽样外推。一般合法前缀的相同预算已被[52客户完整SPE](../../../state/反例/实际前缀的剩余利润与新增覆盖--反例.md)否定，旧覆盖并集是否为一道合法题H是明确分界。

静态解释器已首次通过，无需为记录再次运行。未来确有输入变化时可从本目录使用以下接口；它不会调用原发现器：

```sh
python -B inspect_report.py --source ../fresh-arbitrary-reply-probe-program/original/probe_fresh_arbitrary_reply.py --output /absolute/scratch/new-data-contract.json
```

原表seconds=32.25970125198364属于历史内部计时，本轮没有复现或认证这个速度。本轮也没有补造seed、历史stdout、精确LP最优值、完整根策略或根实际可达性证书。
