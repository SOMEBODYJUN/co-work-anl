# 单客户因果吸引包络的阅读与精确核验

正式对象：[因果吸引亏空的单客户锐包络](../../../state/引理/因果吸引亏空的单客户锐包络--引理.md)。

`source.md` 是本轮 Boss 串行导出的冻结来源原字节，不是重新生成的摘要。`read-manifest.json` 记录源ID `a2435072e35b12e57366`、两冻结提交、原路径、字节/SHA和本次全文实读的比较正文。比较源仅用于核对象身份及后续状态，不据此另标done。

新增 `audit_relaxed_envelope.py` 只用标准库 `Fraction`，独立从两个条件负载的原始份额定义计算D、C及协方差，检查有限域的精确身份、包络、端点最大值和有理顶点。它没有构造共同目录、求解或验证SPE、运行旧研究程序或搜索主目标反例；两条件负载的穷举不代表全部真实SPE。

复现命令：

```sh
python3 archives/customer-attraction/tools/evidence/r105-causal/audit_relaxed_envelope.py
```

本次真实执行一次，输出保于 `audit-result.json`；执行元数据及前后代码/主源SHA在 `execution.json`。普遍包络由正式正文中单调性、端点和配方证明，有限输出仅核实现与边界。全文比较的 hybrid 原稿与 credible9 原稿原件复用 manifest 中的已有证据路径，没有改动原件。

本源后半已有覆盖：调和混合展开未付去槽项，平稳边际不足以交换负载分母，既有恒等式不产生收入。真正版本增量为任意背景与剩余人数的单客户锐松弛包络。一般局部全p-u/Mfull的历史OPEN按后续银行完整SPE反例更新；FTA、Mpath及恰六人半覆盖不由这项局部失败判定。没有外审或新颖性认证。
