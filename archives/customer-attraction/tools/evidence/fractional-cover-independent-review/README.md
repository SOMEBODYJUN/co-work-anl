# 分数价格端点与六人条件证书的独立审查证据

正式对象：

- [全实权端点的直接余项证明](../../../state/证明/全实权末两人价格端点的直接余项--证明.md)：旧内部审查中无需总权重分段的弱端点短证。
- [六人证书的独立重构审查](../../../state/审查/六人分数覆盖证书的独立重构--审查.md)：真实行语义、独立性范围、两份完整原始残差表及运行对账。

`original/`保存本批五份冻结源原字节；`manifest.json`保存源ID、完整commit、路径、大小、SHA-256，两主要冻结提交内容相同。

|源ID|文件|
|---|---|
|`51dc4c98d2bfa9fb2721`|`audit_fractional_pair_half.py`|
|`9693ad684b4fedef975e`|`audit_fractional_endpoint_half.json`|
|`a656a730565f886ecee7`|`audit_fractional_pair_half.json`|
|`1a635414c42072ac4dfc`|`review_fractional_pair_half.md`|
|`fa6d2e5674c98371ca83`|`review_fractional_endpoint.md`|

从仓库根重跑：

```sh
python3 archives/customer-attraction/tools/evidence/fractional-cover-independent-review/replay_and_compare.py
```

包装器将冻结独立原码复制到临时目录，运行默认21/5和`--endpoint`两模式，核全JSON与历史报告相等，再核全部256个残差与旁边`fractional-cover-half/replay/independent-coefficients.json`一致；作者摘要报告的参数、极值和全部零型亦须一致。它只用标准库，不导入作者实现或求解器，不改`original/`。

两个模式均为完整128型系数检查，分别通过160个strongPAIR原IC恒等式和80个R投影角点；原始完整报告、回放及`replay/verification.json`保留实际执行结果。代码独立性指据已给有理乘子和数学行重构，不是独立发现乘子。没有完整SPE搜索、外审、新颖性、最优阈值或无条件六人half声称。
