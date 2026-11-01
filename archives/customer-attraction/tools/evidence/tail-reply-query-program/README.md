# 显式回复真尾利润投影程序证据

主源 `6da0dc66567a8ffba84d`，5035B，SHA-256 `5c474c910391fed3e3eecf801146aeb25c0f4dd1a2f88bd99ef313c8612b004c`；两冻结提交同字节。完整原件保于original/tail_reply_cuts.py，正式数学及实现合同见[程序正文](../../../state/程序/显式回复的真尾利润投影切面程序--程序.md)。本次使用的是原函数对冻结cut的精确回代，没有执行发现CLI。

## 文件和事件身份

| 文件 | 身份 |
| --- | --- |
| original/tail_reply_cuts.py | clean show导出的未改原码，全5035B实读。 |
| source-manifest.json | 原码、共享点/切表、比较程序/证明资源的ID、路径、字节及SHA；阅读范围分层。 |
| capture_original_functions.py | importlib载入完整原码，仅调用states和coefficient_rows各四次，保存原返回值；被动profile计数，不替换原函数。 |
| function-replay/function-execution.json | 本轮唯一原函数调用事件，Python/依赖版本、计数、输入/输出SHA及前后不变性。 |
| function-replay/original-function-rows.json | 四条全部1905列系数、精确状态质量、source收益、u6及负slack。 |
| self-check.json | 来源字节、原报告、脚本AST、正文链接及回执的自查；非新数学认证。 |

默认输入815400B的[early_reply_floors_exact.json](../tail-reply-query-cuts-data/original/early_reply_floors_exact.json)及1671B的[tail_reply_cuts.json](../tail-reply-query-cuts-data/original/tail_reply_cuts.json)由数据清洗统一导出和保存，本目录不再复制大点。源点完整1905列及全部元数据已实读；5287行/min0只是其原报告，本次未重建该旧图。194组全部四态和169正列也经数据方独立核。

## 本轮唯一调用了什么

原main没有verify分支，默认必做4×2×3×9=216个结构LP，因此本次不为已有四条有理负cut重求它。读取冻结cut后，通过未改原states生成质量分布、未改coefficient_rows生成四个向量，再用原psi算状态表达；逐项点乘全部1905权重，要求两种表达都等于保存的严格负slack。函数执行中的有理检查使用assert，运行未启用-O。

实际Python3.12.14、NumPy2.3.5、SciPy1.17.0，回代计时约0.095秒（不含导入依赖）。被动profile记states4、parse4、coefficient_rows4、psi588；原main0、discover0、外部linprog0。三个冻结文件SHA前后相同。结果SHA为 `9d48cc7ed48cde0c6dcad64e1009e6410518a46469066548d07c8f9f5e85f557`。这是当前函数回放，不能倒写成历史CLI、216结构重优化、独立第二矩阵或5287行全图验证。

数据方以独立强PAIR公式核全部256个actual六位/t/q端点，再独立生成四行7620个系数，与此已存结果逐项一致，见[数据核对](../tail-reply-query-cuts-data/four-cut-audit.json)。四个参数点都是i4/memberZ/r1/α1/γ1，分别等于mixed键(1,0,0,5)、(1,1,0,5)、(1,1,0,10)的1/30，及(1,1,1,5)的1/6。q=actual5指A6，不是A5；wj1指第二端B主题。各行在当前early点负，在另一个mixed5043点恰零，不能混点继承PASS。

## 可复核命令

若未来需要重做这项四行原函数回代，可在仓根使用新的仓外输出目录：

    python -I archives/customer-attraction/tools/evidence/tail-reply-query-program/capture_original_functions.py --source archives/customer-attraction/tools/evidence/tail-reply-query-program/original/tail_reply_cuts.py --point archives/customer-attraction/tools/evidence/tail-reply-query-cuts-data/original/early_reply_floors_exact.json --cuts archives/customer-attraction/tools/evidence/tail-reply-query-cuts-data/original/tail_reply_cuts.json --output-dir /tmp/new-tail-cut-function-check

本次实际argv保在function-execution.json，使用仓外冻结路径；正式文件复制后没有再调用原函数。程序模块没有本仓导入依赖，NumPy虽未实际用于这些公式仍在模块顶部导入；SciPy只在discover使用linprog。本包的完整原件及两个共享原JSON已足以核这四条行，不需要复制祖先5287图。

合法性依赖真实r人后继的背景利润界及三个非负行组合，r仅1至4；查询比较是r次重复Q，空题/重复合法。每客户独立最小化隐藏人数只放松必要行，不产生策略。浮点LP选乘子后，精确负值能认证该cut分离指定点；它不证明乘子最优或无更多cut，尤其原best_float未保存每结构状态、失败原因或精确对偶。正文完整保源点合同、系数公式、一般接口与四个既有强PAIR端点的区别。
