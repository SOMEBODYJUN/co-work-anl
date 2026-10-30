# 单行配置分解与开底双树五源原件

[正式审查](../../../state/审查/单位配置行分解与开底双树原矩阵--审查.md)给全部定义域、正部行证明、raw lift裁剪、闭树公式、六原矩阵及独立性/有限范围。原五源在 `original/`，四个比较源在 `comparisons/`；完整ID、两冻结40位commit、路径、大小和SHA见[provenance.json](provenance.json)。上一批已全读的配置canonical按同SHA复用，literal/core等成功入口没有重复执行。

- [单行原程序](original/unit_readout_configuration_row_decomposition.py)：给一机incoming1、k个small1/k的精确配置分布；optional lift先裁为合法共现质量。生产分解无SciPy，finite audit用SciPy找支持后逐项Fraction认证。
- [默认开底生成器](original/unit_readout_two_tree_certificates.py)：输出k4h3的三份含0/1 pins profile、unit/scaled-single两份源NO逃逸和一份平衡YES，共六完整证书；没有LP或OPT搜索。
- [独立原reader](original/unit_readout_two_tree_independent.py)：不import生成器，依仓库相对路径读大JSON并重建资格/全负载/源NO。
- [阈值小JSON](original/unit_readout_configuration_threshold_examples.json)：一份k3h1 literal见证和八组闭树参数。后者是参数清单，不是展开的巨大树实例。
- [完整六证书原JSON](original/unit_readout_two_tree_actual_certificates.json)：1762176字节，全部机器、原job资格/时间、sigma、全机loads、pins、clause统计及源NO赋值表，完整保留。

本批实际从仓库根只运行一次[replay.py](replay.py)：

```sh
python3 archives/unrelated-machines/tools/evidence/unit-configuration-tree-originals/replay.py --run-dir /workspace/scratch/37f0f9248cfc/boss4-next-cache/unit-configuration-tree-originals-run-001
```

Python3.12.14，NumPy2.3.5、SciPy1.17.0，外层exit0。脚本先按原布局复制字节到外部 `repository/tests/audits/unrelated_machines/` 与 `repository/examples/unrelated_machines/`，不改原reader硬编码的相对定位，也避免同期Git同步影响运行。未来复现须给一个尚不存在的新目录，脚本和行程序均拒绝覆盖。

四原入口各一次，全exit0，实际argv、cwd、stdout/stderr见[commands.json](replay/commands.json)。

- [row-audit.json](replay/row-audit.json)：1278点、894精确正支持、384精确分离、9边界，网格最大构造support2（不泛化为任意输入support2）。输入网格/边界由冻结源码完全指定，输出不含全1278份support日志。
- [row-input.json](replay/row-input.json) 与 [row-cli.json](replay/row-cli.json)：k4,s2,q1/3，t全1、raw lift为(2/3,0,0,0)，实际裁为全0并输出incoming/空配置；没有调用全局LP。
- [two-tree-generator.stdout](replay/two-tree-generator.stdout)：本次实际生成的完整JSON，和1762176字节原件逐字节相同，原stdout未截断或重编码。
- [two-tree-independent.stdout](replay/two-tree-independent.stdout)：原reader的全部结果，六证书/4440任务归属/2544全机负载/256源赋值检查。生成器及reader都没有 `--output` CLI，结果由原stdout捕获。

两个行入口stdout为空，四份stderr均为空，空日志也保留。所有运行文件hash与外层执行绑定见[execution.json](execution.json)，详细核验见[verification.json](replay/verification.json)。

新checker不import任何原程序，完整遍历所有JSON语义字段，另核13872有限资格项、4440归属、2544全机负载、384 pin和256源NO witness；与原reader覆盖相同六实例，不相加夸大域。八闭树参数只做整数幂和阈值公式算术，没有展开12^32树或调用全局CONFIG。小literal例只核源权重/容量与手写OPT1证明，没有重跑上一批已成功literal程序。

三个pin profile的pin时间不同，属于三个不同原P；unit/scaled-single的外部时间分别1和1/4；封闭树7/4字段又是另一原模型。源NO逃逸的3/2是已给sigma上界，未声称其真OPT3/2。单行配置分布不等于全局整数调度。这些区分与全部数学证明见正式审查，有限输出未升级一般UM、hardness、外审或新颖性。
