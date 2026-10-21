# 新表示分支：二次 fresh 博弈与频率二客户图

Q-CAG-HALF 仍 OPEN。本分支得到表示候选及高偏置安全边界，未给一般证明。

- [quadratic_graph_compiler.md](quadratic_graph_compiler.md)：全历史双向编译、θ等式、福利偏置及不能生成half坏点的原因；候选待独审。
- [quadratic_graph_compiler.py](quadratic_graph_compiler.py)：有理系数到整数单位客户编译及精确回归；仓库根运行。
- [quadratic_graph_audit.json](quadratic_graph_audit.json)：实际精确回归输出；不是一般福利证据。

继续时可攻击二次fresh个体θfloor，或降低输入特定私有偏置后重新核对old行动。
当前充分高偏置编译已证明安全，不能用它反复搜索half反例。
