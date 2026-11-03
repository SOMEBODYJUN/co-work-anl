# 实际十三行定价与导入最大根的原始证据

14主源共844889B，来自冻结 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 的同字节版本。[source-manifest.json](source-manifest.json)保逐源ID、完整路径、两提交、size/SHA256/Git blob和实际保存地址；`original/<完整原路径>`保原字节。此次重新逐件正常 `clean show`，14件与此前保留raw全部相同，实际回执在 `normal-show/`，不是根据文件名补造读取。父方确认14ID实际claim pushed `d5f86705390954d900948ac7b42d93038857eb44`；本包不把导出动作或该push当数学认证。

正式对象各自保不同真值和依赖：

- [两态全型定价](../../../state/程序/实际第三位十三行投影的两态全型定价--程序.md)：精确分解与原实现合同；当前仅6751行849列的浮点受限发现，没有target2全域报告。
- [二值四尾有限付款](../../../state/计算/二值四尾重权界在五人必要点的有限付款测试--计算.md)：唯一63点上的17546精确阴性，不能泛化银行外输入。
- [22行独立原收益重构](../../../state/审查/五人最大根二十二行证书的独立原收益重构--审查.md)：一份真实局部独立实现，准确复用成熟输入/结果，不称第二主程序；另保实际钱包与最大根合成接口。
- [7497旧点新行分离](../../../state/计算/五人七千四百九十七行旧点的新活跃行分离--计算.md)：便携字面求值器上的53行诊断、13严格负；不独立于该求值器。

## 逐源保留与成熟知识

下列文件均在原 `round8_five/maxroot/`。两态引理、64钱包、二值四尾和主五人证明已有完整数学，原成功不重复授予未绑定输入。

| ID | 原件 | 内容与去向 |
|---|---|---|
| a597d94390aeb4a5cc56 | README.md | 明确五人half已证/搜索冻结，192根、钱包、234/240障碍、hinge、6750→6751→7497及导入诊断的准确分界；程序正文与相邻成熟对象保存各单元。 |
| 229ddd23a41de996995d | actual13_decomposition_audit.json | 199B完整65664历史差值报告，程序正文；没有原运行SHA/环境则不补造。 |
| 7adcfd6b4ad8e8f5ca2b | actual13_payment_discovery.json | 完整795531B、6751行、849池、63正float/62dual、继承exact_mass、微负浮点slack。 |
| 2c041730362346cdefbf | actual13_payment_pricing.py | 6741B原发现器；max8 LP列、fixed-h max4 oracle、三族精确差值与浮点限制。 |
| 598d6bbd0dcb98249a8a | actual13_pricing_contract.md | 3303B原合同；零计数常数项保d、共同h外层、μ≥0及列/条件求值分离。 |
| 4e2de0ae1f4a6004bba0 | actual_payment.md | 任意C的AU、完整64态和最大根E/P合成；成熟钱包完整沿用，独有合成式在22行审查页。 |
| d5a65ef0b6a40aef6ca0 | check_imported_rows_on_old_point.py | 2718B，依赖LiteralDomain的53行应用诊断，同一K及/120。 |
| 2eb98f625a568a7ce307 | check_new_binary_four_tail_payment.py | 4133B，精确整数质量、60分母和三类完整有限银行，自身rho。 |
| 759fbb5fa86d602b0fa9 | imported_maxroot_independent_recheck.json | 两份22行、各1024会员/2048覆盖位、56零、两32前缀表与输入SHA。 |
| 932bf52512c084276444 | imported_proof_review.md | 完整3901B部分独审、共享实际末价、旧已含强PAIR、原发现归属、旧点13负；按数学单元拆至两页。 |
| 05a1e5889792efba897f | new_binary_four_tail_payment_check.json | 完整3181B，32自己的rho、两个8773、最紧行和长分数、negative空。 |
| 745224c204b2c30e2af0 | old_point_imported_row_separation.json | 完整10073B，输入/证书SHA、W/O/K、全部53长分数和13负。 |
| c6f4a50af01a355f86aa | price_actual13_payment.py | 317B续价wrapper，100/400/16/target2参数；不冒实际完成oracle。 |
| 9bc79cd6b0669d5eaad1 | recheck_imported_maxroot.py | 2890B标准库独立原收益实现，仅读取22权数据，真实三路径、消O与完整1024域。 |

原README的192态和234/240模板已在[最大根与铰链原独审](../../../state/审查/最大根与加权铰链原独审的输入和结论边界--审查.md)、[有理模板障碍](../../../state/障碍/最大根局部模板的有理可行障碍--障碍.md)完整整理；索引/hinge在[冻结发现合同](../../../state/程序/最大根铰链定价的索引域与冻结发现记录--程序.md)，6750及先前查询补全在[第三位菜单补全](../../../state/程序/真实第三位投影的菜单补全与续价合同--程序.md)。这些原稿的历史旧作者归属和受限中间值不改写成新机制。原稿未闭合的E预算不改变当前普遍五人定理状态。

## 16项复用依赖与复现布局

[reused-dependencies.json](reused-dependencies.json)逐件绑定当前路径、字节数、SHA和压缩输入的解压后SHA，不重复保存大点。该清单明示复用范围，不能将已取得目录说成全部继承代码逐行重新认证。

| 入口 | 必要数据/模块与已归档路由 |
|---|---|
| actual13发现/续价 | 本包两程序；先前trueH_own_index_pricing/discovery、公共price_indexed_hinges、certificate/actual13_projection.py/json；其下继承fixed-closure→source-last→payment→indexed hinge等，完整路由由上述成熟证据包README/manifest保留。 |
| 二值付款测试 | fixed-closure类及其cm/counts；source_exact_point SHA5930；省校正版证书SHAc0fd；MENUS从已保存menu_ap_pricing.py读取为七菜单。 |
| 最大根重构 | 只需标准库和已保存half5-exact/components/maxroot_four_copy.json SHAa52c；成熟局部local.json和正式32表供记录比较，不是该原脚本运行依赖。 |
| 旧点诊断 | 旧布局half5_exact_v1整个规范包，verify_certificate/source_tables/53权；压缩保存的完整旧点，解压后1688965B、SHA8b28。规范包与主/局部证明已有独立所属目录。 |

程序都带旧目录路径、动态导入和旁写报告。未来运行应在隔离副本恢复原研究相对路径与规范 `customer_attraction/proofs/half5_exact_v1/` 包布局，并恢复已归档继承模块搜索路径；不要直接在original中执行覆盖原报告。本包不宣称为所有旧入口新建了自足可执行环境，也不补原日志未记的argv/数值库版本或全部传递依赖运行SHA。当前保存原程序而非以包装器替换发现器。

## 本次实际检查与没有重跑的域

新增标准库 [check_saved_data.py](check_saved_data.py) 不导入原模块或科学包，输出 [saved-data-check.json](saved-data-check.json)。它实际消费5JSON每个键/数组/长分数、5Python AST、4Markdown完整文本；核14主源及16依赖指纹、正常show身份；849原子全部直方图/共d/菜单边缘和primal/dual、6750→6751完整行名/原子继承、63有理后继坐标、32自身rho与成熟省校正版表、两32根表与成熟1024/56记录、旧点85→64质量投影及全部7497保存slack、53新slack和13负。另按不同表布局比较实际钱包64个保存值相同。所有质量、分数和零字段均保留。

检查只做保存数据和记录一致性：没有计算旧行系数、65664差值、6552对照、144/126核心、256四尾、1024根、17546付款、53新行、7497旧行，也没有执行LP/oracle/SPE。原件说明的这些历史成功各按自己的输入和依赖保留。

从仓库根可运行：

```sh
python3 archives/customer-attraction/tools/evidence/actual13-pricing-and-imported-root-primary/check_saved_data.py
```

暂存合并前加 `--repo <现有结果仓库>` 读取复用依赖。开发中为补入64保存表比较，保存数据检查共运行两次，均通过；每份输出的saved_data_check=1是单次运行计数，批次记录见 [execution-scope.json](execution-scope.json)。没有将这两次数据检查称为新数学PASS。

## 对象关系与接续

[relationship-review.json](relationship-review.json)解释本四对象与现有P13引理、二值四尾、MAXROOT、实际钱包、旧输入和普遍五人定理之间的实现/应用/排除关系。它是这次入库的关系判断，不导入旧图，不宣称完成第三阶段建边。所有对象坚持五人域，绝不把actual13当十三人；必要点、条件oracle、有限精确实验和真实SPE反例保持不同身份。
