# 逐人DIRECT与安全扩充的五份探针来源

正式数学在[固定策略锥探针程序页](../../../state/程序/逐人最优覆盖门槛与安全扩充的固定策略锥探针--程序.md)及[三份浮点记录计算页](../../../state/计算/七主题逐人门槛与六主题扩充的三份浮点记录--计算.md)。前者重构完整历史种子BI、固定锥、u=1、两个目标与精确阳性出口；后者逐份保16/4/8的实际记录、原版本边界和后来DIRECT纠错。

## 原件和共同内核

`original/`保存两程序和三JSON，合计20486B，不改任何原字节。`source-manifest.json`保五个正式primary的ID、大小、SHA256、Git blob、两冻结来源commit及保存路径。

`dependencies/`是已审`strategy-cones`来源的同SHA共同内核及四份规范导入文件；`dependency-manifest.json`保来源路径/ID/hash，不新增primary、claim或done。实际使用内核的完整策略行、份额和精确核验；没有启动其main、Git查询或self-test。四个规范文件是导入依赖，这两个原探针没有调用规范ExactSPESolver求取种子策略。`related-context-manifest.json`保本轮比较的八份数学正文及原README身份。

## 唯一一轮原有限范围重放

`replay_frozen_probes.py`顺序建立三份clone外独立runtime，保原`research/workspaces/customer-attraction/R-5d61.../security/`、`tests/audits/`及`customer_attraction/`相对布局。两个探针源文件未修改；直接启动原CLI各一次：

|入口|topics|players|cases|seed|用时|输出字节|
|---|---:|---:|---:|---:|---:|---:|
|direct|7|4|16|231026|10.251秒|8251|
|direct|7|5|4|231027|13.941秒|2293|
|padding|6|3|8|231028|8.514秒|2300|

三报告逐字节相同，89个保存的float值全部差零。比较器虽预留1e-7绝对容差，最终不是仅靠该容差通过。原循环控制流给97+18+1680=1795次LP，均为这28个冻结样本的重放，没有增加case或换种子。没有candidate文件。

`replay-events.json`保当前完整命令、cwd、七个runtime输入文件各自SHA、返回码、时间、环境版本及输出SHA。每次原CLI的stdout/stderr和重放JSON分别保存，wrapper的stdout/stderr另存；所有stderr为空。三个原JSON不自带历史命令／运行event／动作表／客户点／精确对偶，本轮不倒填这些证据。direct原默认cases24，当前显式取16和4；padding原JSON没有根seed字段。

该wrapper要求固定外部runtime路径未存在才执行，防止覆盖既有运行；如需日后复现，应使用新的独立布局并调整运行路径，不覆盖本次证据。当前保存的是实际执行过的wrapper原字节，不为便携性事后改其逻辑。

## 数学边界

完整有序历史IC锥是精确数学对象，浮点`linprog`只做发现。两个探针均归一化实际收益u=1，padding只根且目标是扩充后的DIRECT，非half的2W。总并集上界9触发组合检查却没有四覆盖阳性；padding表中best都r2，源码仍遍历r3；r1由最大主题保证解析排除。

原代码只对超过阈值的阳性恢复精确重数，没有负结果的有理对偶证书。因此byteexact复现不将这28个锥升级成精确最优上界，更不能维护已被后来银行真族否定的普遍DIRECT。没有增做独立数值实现、全参数扫描、扩充策略审计或网络请求。

`self-check.json`仅做最后静态交付核对：原件／依赖指纹、receipt目标、Markdown链接和已有三重放文件，不调用任何数学入口。
