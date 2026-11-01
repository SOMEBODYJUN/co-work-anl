# R70 七极大六人字面份额探针

主源5c0ef56d82f6b3351177，3546B，SHA256 bbff2b9a73fb15b000992d9ab14db9f5178f2de8ef8a249838415e2eb13a175a。完整数学合同、编码差异和21列精确诊断见[正式正文](../../../state/程序/七极大六人位掩码份额松弛的乘子与分离探针--程序.md)。

`original/seven_maxima_lp.py` 是 clean show 原字节，无修正。无项目运行时依赖或实例输入；科学依赖为 NumPy/SciPy。原 `share` 使用 mask 数值而非 bool，实际是 2^t 倍均分份额；所有数学行和目标按这一字面版本保存。

`run_observed.py` 是本次实际执行的包装器，原 main 默认参数仅一次，经 runpy 执行；被动 profile 计数 build1/mixed_coeffs1/linprog2。`original-event/` 保存原标准流、wrapper事件和完整 A/b/types/两结果 gzip，`invocation.json` 另保工具实际调用的解释器参数和观察耗时。原文件前后SHA相同。原入口不是直接CLI，第一LP状态2、第二状态0/目标约−0.3680110753802541；没有将其36个float支持称精确最优证书。

`audit_contract.py` 是单独的标准库 Fraction 实现，不导入原程序或求解器，只读已有 gzip。它首次一次成功核4064列308864系数及4064目标，逐项验证字面位值公式与正确均分行的非负差；另核新解析21列精确分离、全部76均值及90单位客户实际组合的末位严格偏离。它不把该组合称SPE，不重新求LP。`contract-audit.json`、`audit-stdout.txt`、`audit-stderr.txt`、`audit-event.json` 保存实际范围与事件；外层工具未暴露审计进程开始结束时间，记录仅保存实际argv、exit和工具观察墙时，不补造时间戳。

精确分离的21列不是原优化器36支持的有理化。六个I={0,j}/J全覆盖列各1/18、十五个I={j,k}/J空列各2/45，总权1、全部原行均值非负、目标−1/6。正确末位行却为−19/108，足以解释原弱化的不可实现边界。对旧41/83/3840或席位证书没有新扫描。

为了保留实际执行字节，包装器仍按当时scratch布局定位源：其所在目录的上一层名为 `round16-seven-maxima-source.py`。如需复现，先在新的独立目录复制该布局（源字节取original），再运行包装器；不要在当前证据目录重写已有事件。独立审计可在同样包含original-event/capture.json.gz的新副本中执行。以上是复现合同，不表示本次又执行了这些步骤。

`comparison.json` 绑定实际全文读过的相关数学对象和原六极大来源稿，记录相同/差异和不重复运行范围；`source-manifest.json` 绑定源版本和本包文件字节。`self_check.py` 只做AST、JSON/gzip解析、SHA、路径/链接、回执目标及已存结果字段检查，0数学入口/LP；其实际输出为 `self-check.json`。没有把静态自查叫另一独立数学审计，也未声称外审或一般六人half完成。
