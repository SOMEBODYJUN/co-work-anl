# 背景旧覆盖二倍付款模板的数据证据

对应主源dff8e1e5e5fd6e4b2731，正式正文为[背景旧覆盖二倍付款模板的不可行报告](../../../state/计算/背景旧覆盖二倍付款模板的不可行报告--计算.md)。[148B完整原表](original/fresh_cover_cost_2.json)实际clean show全文取得，三字段tau="2"、success=false及HiGHS失败文本全保；SHA-256为390eed8d1f1755881dc5afff4d20e3c275ec9313950897450a44c72e5766755b。

|文件|身份与职责|
|---|---|
|[audit_cost_template.py](audit_cost_template.py)|标准库独立单位份额重构，与全文读过原码的分子表达式逐项对照；不import或调用原程序，不跑LP|
|[coefficient-rows.json](coefficient-rows.json)|tau2的24列名称、全部192行/4608有理系数及192目标值，保原字典顺序和fresh/p1/slope区分|
|[exact-audit.json](exact-audit.json)|完整原三字段、52客户十类型到八支持的投影、24个配对、精确目标−6、tau范围及tau1全部192余项|
|[review-record.json](review-record.json)|读取/比较/执行责任和源版本；不把新精确证据记作原148B已有数据|
|[self-check.json](self-check.json)|最终SHA、JSON、代码AST、正文链接、原新报告绑定及回执目标核对|

本数据侧在仓外完整运行独立脚本一次，exit0；之后只复制并作静态自查，没有重跑该核。矩阵一条路径直接使用单位客户分数收益，另一条路径是原代码表达式的显式转写，用于核清清分母及旧负载差分；不宣称未经原码知情的盲审或第二套原LP。八支持证书满足y≥0、yᵀM₂≥0、yᵀf=−6，故给精确模板不可行性。

52客户完整根SPE及1554个有理比较复用[既有正式反例](../../../state/反例/实际前缀的剩余利润与新增覆盖--反例.md)，本次只新核六标签投影、24条件余量及额外付款。这个例子**满足**二倍付款条件：2uA−C_old=14/3≥0，而目标P+Δ−freshOPT₂=−1；它不满足较强tau1条件。Q、R两标签在投影中都是真回复原S，允许重复，不混成旧手写回复原R的版本。

原程序默认tau2的唯一执行由[程序证据包](../fresh-cover-cost-certificate-program/README.md)负责，见[执行记录](../fresh-cover-cost-certificate-program/replay/execution.json)及[当前重生报告](../fresh-cover-cost-certificate-program/replay/fresh_cover_cost_2.json)。本数据侧0原main/helper、0LP；不会另跑tau1、参数扫描或完整SPE审计。tau1四项可行证书来自精确代数和192余项，不依赖LP。

从仓库根仅重做数据核，可指定新的输出目录：

    python archives/customer-attraction/tools/evidence/fresh-cover-cost-certificate-data/audit_cost_template.py --primary archives/customer-attraction/tools/evidence/fresh-cover-cost-certificate-data/original/fresh_cover_cost_2.json --output-dir /tmp/fresh-cover-cost-audit

得到的Farkas见证同样覆盖tau≥17/12，但没有认证最佳临界tau；(1,17/12)的全模板状态未由本核验判断。有限模板无解、其条件命题的既有SPE反例、合法H或tau1条件证书，以及根half是不同层次，正文分别说明。
