# 五人结构化相对私有块证据

[正式计算对象](../../../state/计算/五人结构化相对私有块最优点--计算.md)自足说明固定策略、目标、全部浮点字段、严格负IC、新有理重构和精确对偶，不能只用此目录的PASS代替数学条件。

* `original.json`：源 `9d2fb6b26cc4ae9f2ce7` 的955字节冻结原件；两冻结提交完全相同，SHA与路径见 `source-manifest.json`。
* `verify_exact.py`：本轮新标准库核验器。重建固定种子及其精确优先策略，不导入原代码、规范solver或数值优化库。它不会解LP。`policy-exact.json` 是该策略的330条完整计数动作，不是从原JSON读取出的历史策略文件。
* `exact-report.json`：本轮精确报告；包含十进制/二进制解释的全部负IC、重构点、完整9+5乘子及127项残差。不得把新有理点与旧float混为同一输入。
* `exact-stdout.txt`、`exact-execution.json`：本轮最终核验的stdout、进程状态、Python版本、真实命令及运行时间。没有用浮点容差判号。

重跑命令从仓库根执行：

```sh
python3 archives/customer-attraction/tools/evidence/structured-packing-n5/verify_exact.py --captured-policy archives/customer-attraction/tools/evidence/structured-packing-scanner/rerun/observed_5.json
```

不加 `--captured-policy` 仍可独立执行全部数学审计；加此参数会额外验证本轮原入口捕获动作与独立精确种子策略逐项相同。对原策略的平局判断必须保留这个区分：原程序确用NumPy浮点，观察当前动作匹配不制造缺失的历史运行日志。

固定策略的计数域共330节点、2310条含self IC；独立核验又逐条遍历2801个有序决策历史及19607真实比较。根最优支持检查枚举21个五标签支持，首步补全检查枚举35个四标签支持。新有理质量乘5为45个单位客户，全部IC、归一化、packing及对偶补足关系精确通过；9条IC和5条pack非负乘子给所有127类型余项非负，16零111正。该固定锥最优8/5已认证，任意其他策略/人数不在此结论内。

原十进制解释32条负IC、二进制解释37条负IC；二者都违反根改B比较，不是精确SPE。所有原字段仍原样保留。本例新精确福利比OPT/W恰等于8/5，但优化目标是最小相对私有块/根收益；实际外部A客户使首步损失/u只有3/5。

原程序[冻结字节](../structured-packing-scanner/original/structured_packing_scan.py)、[原入口运行元数据](../structured-packing-scanner/rerun/run-metadata.json)、[捕获动作](../structured-packing-scanner/rerun/observed_5.json)由同批扫描器任务交付。本页实际读取这些n5捕获动作及原输出并比较：新原入口n5输出与本原件全955字节相同。原程序复跑不计为本独立核验器的一部分；源码/报告的语义与数值认证责任分别保留。
