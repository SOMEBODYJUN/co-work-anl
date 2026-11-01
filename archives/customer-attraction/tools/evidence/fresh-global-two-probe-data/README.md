# 单背景主题两人全比较探针的阴性报告

主源 `7fc957114a5ab7ea917a` 的[122B原报告](original/fresh_global_two_probe.json)完整保留六字段，SHA256 `ac507559105f4ffd6151124b859dcb20337694c48f69582540bc04d88f8160b7`。两冻结提交同字节。[自足数据正文](../../../state/计算/单背景主题两人全比较探针的阴性报告--计算.md)解释全部控制流、35行策略锥、21比较、模型量词、证书与反例边界。

历史值是cases2000、policies643、solved13503、best0.0、seconds24.15056276321411、foundnull。在所读生成器合同下，完整结束且643×21=13503可推出q6；报告没有seed、max-background、命令、政策表、环境、求解成功数或精确客户。不能把源码默认seed71213/maxbg4补写为历史事实；best0是负改善哨兵，solved计所有返回而非success。

## 本包文件

|文件|内容|
|---|---|
|[original/fresh_global_two_probe.json](original/fresh_global_two_probe.json)|唯一主原件，无改写字段或添加参数。|
|[audit_saved_reports.py](audit_saved_reports.py)|只读源AST和保存JSON/gzip的结构、算术与证据身份；不导入原代码，不调用LP或重算原IC。|
|[report-audit.json](report-audit.json)|全部六字段、条件计数推断、缺失信息清单、新84记录的计数和证书目标分解。|
|[manifest.json](manifest.json)|原来源及所有实际比较材料、共享证据与交付指纹。|
|[self-check.json](self-check.json)|本包最终静态检查；不重复数学入口。|

## 当前证据责任

[程序原件](../fresh-global-two-probe-program/original/probe_fresh_global_two.py)及[程序正文](../../../state/程序/合法单题背景的全比较主题对探针--程序.md)由程序任务保存。本次只做一份明确小输入：q6/cases4/seed71213/max-background4。其[事件](../fresh-global-two-probe-program/replay/execution.json)、[压缩逐LP捕获](../fresh-global-two-probe-program/replay/lp-capture.json.gz)和[新六字段输出](../fresh-global-two-probe-program/replay/runtime/bounded_probe.json)是84LP新运行，不是历史13503LP的复现。

[共享独立Fraction审计](../fresh-global-two-probe-program/contract-audit.json)核8820不同矩阵系数、5292目标/证书坐标和2940真实IC，84份精确可行重构：10个零、74个正。历史报告没有这些状态，不能倒填。两个微负浮点返回均为数值误差范围，未跨best更新阈值。10个精确零与既有H解析下界相合，可认证对应固定问题最优0；74个正值未给精确最优性证明。

[背景菜单证书](../../../state/计算/背景菜单的有限证书--计算.md)通过合法H地板及实际末位两次查询证明该子域P+Δ≥freshOPT₂；正文保完整四IC与余项，不靠本有限阴性报告作一般证明。[一般GLOBAL反例](../../../state/反例/实际前缀的剩余利润与新增覆盖--反例.md)的旧覆盖不是目录中合法H，因此它与该子域定理相容。未重复旧384行证书审计、52客户全树核验、历史2000轮或新84LP入口。

本数据任务仅新增保存记录的读取与静态核对。报告六字段完整处置；生成器和其它数学来源由各自对象承担，不代其它源完成登记。后续若要恢复643个政策或历史命令，须有额外原始日志；122B不能提供它们。
