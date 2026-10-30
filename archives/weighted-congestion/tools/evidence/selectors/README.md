# 局部矩与选择器限制：可复现资源

正式入口为[计算对象](../../../state/计算/局部矩与平稳择证的精确复现--计算.md)与[审查对象](../../../state/审查/局部矩与选择器限制的审查范围--审查.md)。`source-manifest.json`逐份记10个领取源的完整双冻结定位和SHA256，`original/`原字节不改。`comparison-manifest.json`及`comparison/`只保两份额外实读审查依赖，不计本批done。

三份代码仅依赖Python标准库，完整数学参数内嵌。原样从`original/`运行：

```sh
python3 tests/audits/weighted_congestion/template_certificates/verify_selector_local_moments.py
python3 tests/audits/weighted_congestion/template_certificates/independent_selector_local_moments.py
python3 tests/audits/weighted_congestion/template_certificates/verify_stationary_selector_obstruction.py
```

本轮完整stdout为三个`replay-*.json`，stderr为对应`replay-*.stderr.txt`（均0字节），exit均0。`replay-comparison.json`保实际命令、环境、比较目标和全部差异；三个差异数组均空。前两个历史报告有外层执行包装，精确比较其中`result`；第三个比较全JSON。未改写冻结结果。

两个local程序的f454 proof hash是历史固定版字面元数据，非当前725行整合稿hash。三程序不承担后来刚性、近似支持、完整proper植入与mover程序的复现；其一般证明和历史审查范围见正式对象。有限通过不构成任意实参数证明、全类均衡保证、外审或新颖性认证。
