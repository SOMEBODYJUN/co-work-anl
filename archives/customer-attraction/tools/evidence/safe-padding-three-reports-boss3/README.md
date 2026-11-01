# 安全不交目录扩充：原程序与三报告

正式对象：[安全不交扩充原程序与三份审计报告的逐案例对应](../../../state/计算/安全不交扩充原程序与三份审计报告的逐案例对应--计算.md)。四primary为4238B程序、8220B当前作者JSON、7033B旧带标签replay、8781B严格replay；所有原字节、双冻结版本、SHA和路径保在 `original/<id>/` 与 `source-manifest.json`。

原4238B程序在新外部目录只执行一次，约0.205秒、exit0、stderr空。生成报告8220B与当前作者报告逐字节同；该报告三根字段又等于严格replay投影，严格replay多五项版本/表示元数据。旧7033B没有旧代码SHA，未重跑旧版本，不称三份文件全字节同。

36输入的名义参数为m1…4、旧题1…3、各3个seed231029样本。先商等覆盖旧标签，再生成一份确定平局旧策略；同倍复制全部旧客户m份，新块各K单位客户，K0不添多个空集。全扩充历史与全部动作的Fraction核验共15849比较，包含自身；最小差0因此不必来自不同动作平局。一般任意旧σ保持由正文引用的全参数证明承担。

旧17106→新15849的1257差只在三个参数键出现：m1/k2/sample0去旧别名少1，m2/k1/sample2零K不添两个空标签少10，m4/k3/sample1旧三题商成两题少1246。所有36的K/OPT/卷积/minimum_gap不变。完整字段比较及每例Σq^d计数在 `three-report-comparison.json`，未另跑策略或SPE。

## 复现

只复制 `original/4aee24ec865e93986c02/audit_safe_catalog_padding.py` 到仓库外新空目录，保持assert，执行 `python3 -B /absolute/new-runtime/audit_safe_catalog_padding.py`。仅需Python标准库，没有输入文件、solver、网络或认证。它按__file__直接覆盖同stem JSON，故不能在原件目录执行；stdout只是36/15849/PASS摘要，完整数据在新生成JSON。

`replay/current-strict/` 保真实stdout/stderr、argv/UTC/源码前后SHA、生成完整报告和字节比较。生成报告SHA53c099db6eb0adb85e9d9e9017a78e9234b7a9da9775ed6f5de868229dff5357。

严格replay的程序SHA60ca4b…与本原码相同，statement SHA b622ac…也与既有安全扩充主稿原件相同；正文和 `three-report-comparison.json` 保准确路由。这些是当前实际文件对应，不补造旧带标签版本SHA或历史执行时间。原独审已经在既有数学对象完整保留，当前新增代码/报告事件不替换其先验。
