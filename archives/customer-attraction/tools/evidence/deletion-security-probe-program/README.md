# 实际终局删除支持随机探针证据

完整数学与程序合同见[正文](../../../state/程序/实际终局删除支持的随机策略锥探针--程序.md)。主源2353字节，ID `6186ac258e7f242f66a6`，双冻结版本SHA `12f34be25cc706f1151db51e264120f1d5440cc667de53bea53142679487d283`。

## 保全内容

- [original/deletion_probe.py](original/deletion_probe.py)：未修改原件。无主入口保护，import会开始顶层扫描。
- [dependencies/tax_probe.py](dependencies/tax_probe.py)及[customer_attraction包](dependencies/customer_attraction/__init__.py)：实际五个依赖全文已读、逐字冻结SHA绑定。tax只执行`if __name__`前缀；它的optimize/主入口未运行。
- [capture_first_iteration.py](capture_first_iteration.py)：一次真实首轮捕获器，只读原第33/34行局部状态，在第二次外层第13行停止；优化器与原函数未替换。
- [first-iteration/execution.json](first-iteration/execution.json)、[stdout.txt](first-iteration/stdout.txt)、[stderr.txt](first-iteration/stderr.txt)：受控原顶层事件1次、完整首轮1次、原makepolicy1次、LP22次；**不是100轮完整执行**。
- [first-iteration/first-iteration.json](first-iteration/first-iteration.json)：实际13类型seed表、259历史完整sig、1554×64有理IC、63覆盖系数、22查询和各自4删除行、全部22浮点返回。保存浮点解不等于已验证其有理可行/最优。
- [audit_first_iteration.py](audit_first_iteration.py)、[definition-audit.json](definition-audit.json)、[audit-execution.json](audit-execution.json)：一次独立Fraction定义核，原函数/solver/LP均不调用；全部seed松弛和22×4个seed删除期望保留。
- [source-manifest.json](source-manifest.json)：主源、五依赖、三个原文比较源及全文读过的正式对象身份。
- [self-check.json](self-check.json)：静态最终链接、SHA及回执检查。没有重跑算术或原扫描。

`related/`保存原工作区README、静态分数覆盖下界稿和相邻真正安全值筛查脚本。这些是全文比较来源，没有纳入本次执行或单独标记完成。相邻n3固定策略探针及其一次完整22LP事件由[另包](../deletion-branch-probe-program/README.md)保存，不和本n4首轮合并成一份搜索。

## 实际运行结果

Python3.12.14、NumPy2.3.5、SciPy1.17.0，首轮捕获耗时9.870893146秒。原输出：

```text
0 -0.0833333333333327 (1, 0, 3, 2) 7.8
```

22个LP报成功；没有候选文件；stderr空，主源和实际依赖保持冻结SHA。−0.08333…是浮点违反量，不是已证的−1/12最优值。首轮之外没有执行，既未恢复历史100轮，也未把无候选当普遍界。

独立核全部97902个IC客户系数及1554个t系数、63个覆盖系数、5544个删除客户系数及88个t系数，全部一致。seed为60名单位客户，W60、利润(18,29/2,14,27/2)；259历史全1554含自身比较成立，非自身1289正、6平局。此seed完整SPE认证不同于对22个浮点LP解或全部纯SPE终局的认证。

## 复现接口

`capture_first_iteration.py --runtime R --out O`需要一个新runtime R：把主原件和tax原件放在
`R/research/workspaces/customer-attraction/R-5e9dedd2606746ff8afbbb73bf816e7a/security/static/`，把四个包文件放在`R/customer_attraction/`。脚本切换cwd到R，保原相对import和文件名替换；O必须没有已有execution.json，以避免误把重复执行算唯一事件。运行需NumPy/SciPy。trace按冻结源的行号绑定，不适用于任意改版。

`audit_first_iteration.py --input first-iteration.json --out new-audit.json`仅需标准库，读取已保存矩阵并按单位客户定义重建。它不运行原脚本、原函数、原求解器或LP。当前证据已保存真实一次事件，无须为了阅读本包再次执行。

完整原扫描可在新的runtime直接运行原文件，但那将启动最多100轮并可能覆盖源码旁的deletion_candidate.json。本包没有执行该完整扫描。原候选分支只是打印精确minGamma，没有断言非负、没有精确重算目标；因此新candidate仍必须完整认证后才能引用。
