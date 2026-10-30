# 完整有序终局选择的原件与有限回归

数学对象：[整数投影](../../../state/等价/完整有序历史终局选择的整数投影--等价.md)。
实际证据：[有限回归与恢复边界](../../../state/计算/完整终局选择的有限回归与恢复边界--计算.md)。

本批完整处置四源：合同、12814字节全树实现、2616字节审计、6508字节冻结报告。PROVENANCE.json按来源ID、冻结提交、原路径、字节与SHA保存准确身份；六个运行依赖和六份全文比较来源不算额外done。

original/credible2/ 保存四份原件。dependencies/ 保存完整策略锥运行依赖；五份既有依赖按精确相对路径复用。comparisons/ 中同名实现的审读和上下文属于另一个数学编码，不能转作本文件的独立审查。

replay/ 保存本轮唯一一次原样有限回归的完整stdout、stderr、报告和元数据。8组20记录、680枚举固定锥LP、20联合求解，完整报告逐字节相同。三个数值正误差 \(10^{-6}\) 仍只是浮点回归差异，没有被记为精确反例。

从仓库根用不存在的目标目录运行：

~~~sh
python3 -E -B archives/customer-attraction/tools/evidence/full-history-selection/reproduce.py --output-dir NEW_FULL_TREE_AUDIT
~~~

需要NumPy、SciPy；本次版本和完整命令在replay-manifest.json。原文件不修改，不运行默认参数发现，不重新做旧时限搜索。主数学投影由一般证明承担，有限程序比较不认证跨全部策略或任意目录规模的统一上界。
