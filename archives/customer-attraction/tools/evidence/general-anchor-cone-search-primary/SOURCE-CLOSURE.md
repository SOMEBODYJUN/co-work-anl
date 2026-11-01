# 动态加载闭包与输出

primary parents[5]定位original root，再importlib执行R-ffea…/credible_counterexample/cone_search.py。两原路径都原样保存；helper只有标准库/numpy/scipy，无更多本地import，main guard只在其作为脚本时旧扫描才执行。primary只用comp，不用helper.Search/opt/main。

原import会动态exec helper顶层定义/科学包，故当前仅AST parse，不import主源/helper或构建AnchorSearch。外部numpy/scipy版本未锁，不说当前复现旧环境。四报告不是主code输入，只有固定构造参数/seed与科学运行时。

--output必填并直接覆盖，中途每5step与末尾写相同7字段，父目录不创建、无openx。seed/k/r/steps有默认但只有k/r/steps入报告；无completion/argv/源码SHA或stdout进度日志绑定，不补造。原数据数组逐token读取不是pay/BI/LP执行。
