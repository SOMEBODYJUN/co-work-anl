# 固定背景收益切片的有理秩与核基审计程序证据

本包整理主源 `6b6d01e6c77956272308` 的8089B标准库程序，正式对象为[固定背景收益切片的有理秩与核基审计程序](../../../state/程序/固定背景收益切片的有理秩与核基审计程序--程序.md)。

[原程序](original/audit_fixed_background.py)无输入JSON、CLI参数解析、本地依赖、优化器或SPE求解器。输入是源码中12个背景与固定M/r/s/k范围；Fraction矩阵含全零客户列。基础96例核秩及265个基，四槽165例核满秩，聚合77例核秩及546个基，单位背景14例仅核秩，六收益8个k各核8会员位型。完整核基不等于全部最小支撑回路枚举。

[源清单](source-manifest.json)绑定两个冻结提交、原blob、SHA和六件实际读过的相关原件；[比较清单](comparison-manifest.json)、[阅读记录](review-record.json)保数学理解与全仓相关纠错。相关原件包括[原数学稿](related/fixed_background_circuit_basis.md)、[原报告](related/fixed_background_audit.json)、[后续审查](related/fixed_background_rank_review.md)。后续4461B检查器及375B报告复用[数学证据包](../fixed-background-circuit-basis/README.md)，未运行。

唯一新原运行由[replay_main.py](replay_main.py)复制未改源码到全新仓外目录，以runpy执行原main，sys.setprofile只旁观返回，不替换函数或补调helper。[执行记录](replay/execution.json)与[进程记录](replay/process-capture.json)记录Python3.12.14、assert启用、exit0、总6.969239209秒及源前后SHA。[stdout](replay/stdout.txt)是384B汇总，[stderr](replay/stderr.txt)为空；[新完整报告](replay/fixed_background_audit.json)38584B与冻结原报告逐字一致。这是一次真实作者入口，不是第二次独立数学审计。

[原对象压缩账](replay/original-observations.json.gz)保存该次原返回处的矩阵、核基和参数，37648B解压842445B。合116096矩阵条目、811个选定基向量/14545系数；Fraction以分数字符串保真。[观察摘要](replay/observation-summary.json)逐族列出原返回记录和数量。六收益仅保8个参数与返回1，未额外打印64左右值。全调用计数见[运行范围](execution-scope.json)：原rank525，payoff135296；无新增秩/核扫描、LP或SPE。

[配套数据正文](../../../state/计算/固定背景收益切片的有限秩与核基审计--计算.md)复用同一事件；[完整有理回路定理](../../../state/定理/固定背景双主题收益切片的完整有理回路--定理.md)给解析证明。固定背景收益行是静态终局函数，不含完整历史策略、最佳回复或付款方向；共同有符号线性核不等于非负客户实现锥。有限通过与一般参数解析结论均不自动证明动态半覆盖。

若确需未来复现，可在新空目录执行以下命令；本次已执行一次，不需要为阅读封包再运行：

```sh
python3 -I -B replay_main.py --source original/audit_fixed_background.py --run-dir /absolute/new/empty/run-directory
```

包装器要求运行目录尚不存在，以免旧报告冒新结果；不要使用关闭assert的解释器选项。原作者脚本本身会直接覆盖同目录固定文件。

[check_package.py](check_package.py)只核字节、语法、已捕获数组形状/计数、链接和回执，不导入原程序、不消元、不计算收益。[成果指纹](artifact-manifest.json)排除自身与输出[self-check.json](self-check.json)以免循环。执行 `python3 -I -B check_package.py` 是静态封包自查，不能增加数学通过次数。
