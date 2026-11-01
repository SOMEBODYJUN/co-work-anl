# 程序依赖与原输出布局

原code标准库product/Path/Fraction/json/sys，外部numpy与scipy.optimize.linprog；未锁原包版本，无本地helper/输入JSON或实例。原源码与三报告按原相邻目录保存；只AST静态解析，不import numpy/scipy或main，不重新生成矩阵。

三个sys.argv成员flag--weak/--terminal-only/--optimize-beta，无argparse或未知flag验证。suffix公式先terminal，再optimized优先于weak；main先print完整JSON再覆盖write_text邻文件，没有--output/openx。失败LP也写status且无显式抛错/非零exit。原报告没有argv/time/exit/env/codeSHA，不补造真实执行日志。

静态字段核明确前211/404少源码总写的terminal_only，457只形状相容。后续精确强弱代码不属于本程序runtime依赖，只作完整数学比较；不复制它们的run事件作本新运行，也不额外done related。
