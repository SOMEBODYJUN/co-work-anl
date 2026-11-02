# R8e450实际分数负载六源的原件、依赖与固定核验

Boss2 / cleaner完整实读六主源22622B：2478B notes、2738B固定σ锥程序、11282B六组36点报告、3430B全终局程序，以及1977B/717B两份扫描报告。双冻结commit/path、SHA、Git blob和原件保存路径见source-manifest.json，实际clean show出口收据在export-metadata/。全部原件按source ID隔离，没有改源码或覆盖原输出。

## 数学落点

- [早期候选与后续反族](../../../state/资源/实际分数弱桥的早期候选与后续反族--资源.md)：保CA-FRACTIONAL-ACTUAL-LOAD-WEAK-v1、仍有效的覆盖充分性代数和当前一般桥已假；恰六人反例只反辅助桥。
- [两个原程序合同](../../../state/程序/实际分数查询的固定策略锥与整数终局扫描--程序.md)：分清浮点LP原始点、完整有序σ、整数集合值递推、浮点纪录筛选和缺失的全试验日志。
- [固定保存点核验](../../../state/计算/分数弱桥的三十六个保存点与两份起始终局--计算.md)：36点精确20700非自身IC，六名称仅三张σ；两个起始输入另给明确常值完整策略与1695计数类核验。

## 依赖与来源边界

dependency-manifest.json保18个只读相关来源：R8e450根README、原IntegerSetSolver后端、六对游戏/策略JSON和四个规范包模块。根README和11800B后端本批新存related-original/；其余16件直接复用已发表且逐字节核同的原件，不再复制或done。游戏和证书所有字段、完整有序动作映射均读过；原客户权重没有被混入重赋权点。规范包四模块与后端代码全文读过。

主probe列七个名称，冻结inventory和全部increments仅有六对输入，iid_empirical_kernel两路径未发现。read-boundary.json保这个检索结果；它不臆测未保存的历史环境。后端源码作为相关依赖保全，不代其独立来源清洗完成；其余搜索CLI分支也没有被冒作本次执行。

comparison-bindings.json保四份完整已读现有数学对象的字节绑定；relation-evidence.json只登记有解释的数学关系，没有导入旧图。通用反族及旧精确审计已充分处置且没有新疑点，本批旧四主题/13人审计均运行0。

## 唯一新数学执行

audit_preserved_points.py只用Python标准库，按source/dependency表核输入哈希，读36有理点和六份完整有序表，逐真实后继计算全部IC、W与六query。对两trial0输入另构造σ(h)=0，并遍历全部计数前缀核该明确策略。无LP、随机搜索、集合值求解器、银行控制器或旧反族运行。

run-metadata.json、audit.stdout.json及audit.stderr.txt分别保实际argv/解释器/时间/脚本SHA、完整37030B结果和空stderr。一次执行exit0。36点核4140记录×历史、20700非自身/24840含自身比较；两常值策略1695计数类、6075非自身/7770含自身比较。未显示枚举十二人所有5592405有序历史，而是利用已明确常值策略的计数不变性覆盖其义务。新见证不冒称原扫描导出的同一策略。

在包含所列已发表依赖的完整checkout中可运行：

```sh
python3 -I -B archives/customer-attraction/tools/evidence/r8e450-fractional-actual-load-primary/audit_preserved_points.py --evidence archives/customer-attraction/tools/evidence/r8e450-fractional-actual-load-primary --repository .
```

stdout是完整新JSON；程序本身不覆盖归档报告。此新入口只需标准库。原probe需NumPy/SciPy，原outcome_probe及后端需NumPy和规范包；旧报告未记录库版本，不能许诺跨版本逐浮点LP或自适应冠军路径字节一致。

materialize_original_layout.py可以把24个已核原始来源放进一个**不存在**的新目录，恢复原源码parents[5]和后端包发现所需路径；它只复制、不运行。若以后有明确新数学目的，原发现器应在这个副本运行；原probe会覆盖副本中的results.json，outcome_probe须另指定尚不存在的输出。该便捷复制器本批只做语法/路径合同检查，没有实际调用或补记为一次数学实验。

字段、SHA、链接和语法检查是发布完整性检查，不代替正文中的数学判断。六逐源回执分别说明实读、比较、独有去向与当前状态；只有父方显式checkpoint pushed并核远端文件/依赖后，才逐源done。
