# 三段回复身份投影的原件与核验

数学正文见[三段回复身份闭包](../../../state/计算/三段回复身份闭包的精确局部投影--计算.md)。三份冻结源完整原字节在 `original/`，两冻结提交、来源ID和SHA见 [source-manifest.json](source-manifest.json)。

`original/check_chain_L3.py` 只用Python标准库，无参数；向当前工作目录写 `chain_L3_exact.json`。本轮原入口实际执行一次，生成文件保在 [author-replay/chain_L3_exact.json](author-replay/chain_L3_exact.json)，与冻结报告逐字节相同；[事件记录](author-replay/event.json)不冒称游戏或策略树运行。

在本目录运行 `python3 audit_chain_projection.py`，从十一条必要行的逐客户系数独立重建（不导入作者实现），输出 [audit-output.json](audit-output.json)。它检查18组各512态，共9,216项行分解，并核全部极小值、见证与权重。原数据保14组严格身份增益；同一实际参考路径的12组中只有8组严格增益、4组负极小值。

这些都是局部必要关系。未运行LP、客户实例构造、完整SPE逆归纳或六人半覆盖证明。关系比较和使用边界见 [relationship-review.json](relationship-review.json) 及正文。临时清洗回执不属于数学证明。
