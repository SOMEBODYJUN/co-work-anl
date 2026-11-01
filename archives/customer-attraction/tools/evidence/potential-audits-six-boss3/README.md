# 弱强有限势与公共平移：六份原审计来源

本包保存三原Python、三原JSON，共20091B，以及两份相关原候选29755B。三个原入口均标准库、main guard，不需优化器。本文与当前事件的“原入口0运行”只指本批，不否认历史作者曾生成保存报告。

正式正文：

- [原审计合同](../../../state/程序/弱强有限势与公共平移的原审计合同--程序.md)：真实输入、210/252计数、原strong只210步sharp、平移信任元字段及固定候选限制。
- [双支持引理](../../../state/引理/三人删除势双支持恒等式与终局守恒的等价条件--引理.md)：Δ+3E=Rₐ−Rᵦ，以及纯调和时九条双支持记录与九个总支付差的等价。
- [既有完整原数组核验](../../../state/计算/有限势弱强两点的完整策略与同支持失败--计算.md)：此前一次定义级完整核验，非本批新运行。

## 实际执行事件

`compare_saved_audit_contracts.py`本次恰一次，assert开启，Python3.12.14，exit0/stderr空。只新增强表15个双支持代数式与弱表6个纯态支付；既有84点/43历史/2520sharp逐行输出以固定SHA读入，不再运行其产生器或重新枚举客户比率。三份派生报告的全部字段与原JSON相等。这是语义合同对照，不是三个原脚本的逐字节重放。

结果、event、真实argv/stdout/stderr在`comparison/`。原程序import/CLI、LP/MIP/BI/随机发现及前批完整检查器重运行均为0。新检查约0.046秒；准确时间以event为准，不把JSON解析/文件校验时间解释为算法性能结论。

已有证明依赖列于`prior-evidence-dependencies.json`，三个文件与pushed `77f896490649940761edb933e4c297fa5674d079`逐字节一致。它们已经在仓库中持久保存，未在本包重复放一份2.5MB输出。重跑这个最小对照时，需要仓库含这些精确文件：

```bash
python compare_saved_audit_contracts.py --repository /absolute/repository --output /absolute/new-comparison-output
```

此命令只适用于包内精确原件及固定旧证据，不充当任意势输入的通用验证工具。

## 以后若确需重放原入口

`restore_original_layout.py`本批只静态写成，未执行。它将六主源与两输入恢复为manifest记载的完整逻辑路径，必须指定新或空目录，不运行程序、不改冻结原件：

```bash
python restore_original_layout.py --destination /absolute/new-empty-source-root
```

在恢复根下的`research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/next_tree/`分别运行三个原Python，即会在该新目录写各自报告。保留Python的assert，不用`-O`。原weak和shift stdout是完整JSON；strong stdout删去两份九条数组，完整4433B载体只能从写出的JSON取得。任何未来实际运行应另记事件，不能借本批新对照的成功倒填原运行记录。

## 明确关系与未完成问题

弱/强原审计→两84表的固定精确约束；shift原审计→弱表的公共常数平移；强双支持公式→同一势中调和纯态下的总支付差。以上边有直接公式、输入SHA和输出字段证据。没有从有限势反例连到原共同客户半覆盖反例，也没有全人口延拓、固定查询最优性、随机搜索穷尽性或外部新颖性认证。
