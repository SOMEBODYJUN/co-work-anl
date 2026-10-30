# 共享侧资源证据包

`source-manifest.json`逐件列冻结commit/path、SHA-256、字节及认领/比较角色；`original/`保全23份本批来源及16份已实读比较依赖。所有原件不改字节。

`replay.py`从original根运行15个规范Fraction程序，保存各stdout并递归比较全部JSON字段/实际输入；`replay/comparison.json`列完整差异。实测全部通过，14份报告字节相同；仅multi作者报告的顶层command绝对路径改变，所有数学、参数、输入、Python及源码hash均相同。

`check_freezes.py`核对倍率分离v1/v2/v3与异权v2的当前数学切片；`replay/freeze-comparison.json`也明确保留两个早期整稿hash无法匹配当前前缀的事实，不补造旧候选。

完整数学意义与真实范围在[计算对象](../../../state/计算/共享侧资源系列的精确复现--计算.md)，审查角色在[审查对象](../../../state/审查/共享侧资源系列的内部审查与版本范围--审查.md)。计算是有限实现检查，不替代一般证明。
