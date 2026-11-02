# 静态占用与完整零遗憾族的程序闭包

六份冻结原件均完整读取；原字节31,340B及两冻结提交定位见source-manifest.json。数学范围、实际LP和时态说明见[正式资源对象](../../../state/资源/静态最坏占用反例与零遗憾紧族的精确程序闭包--资源.md)。

两原标准库精确审计各运行一次，新报告与冻结报告逐字节相同。replay-verification.json给本次命令语义、范围、比较与环境；current-*.json及两个stdout是本次输出。它们复核实现，全部参数结论仍由正式数学证明承担。

verify_saved_boundary.py只核原随机报告中最佳点的显式有理重构，不调用优化器、不重跑发现。saved-boundary-exact.json完整保存70背景核验及重构后的25活跃计数。原JSON的active_backgrounds=2来自重权前种子；二者不能直接相等。

所有原代码都有main保护。audit_occupied_static_minimizer.py的--output必须指定新路径；audit_safe_zero_regret_family.py在脚本同目录独占创建报告。复用后者时只拷脚本到空目录。occupied_saddle_face_probe.py使用NumPy/SciPy并覆盖自己的同名报告，本批没有运行它；不要在original目录直接运行。原探针无锁定依赖版本，80次阴性不承担候选正确性。

本证据包不包含新SPE搜索、LP/MIP运行或随机扩样，也不认证原随机历史的逐次环境。已有相关数学的真实审查/新颖性范围均不因代码重放而改变。
