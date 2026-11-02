# 六十四原子跨族闭包四主源

正式数学为[1284行精确点](../../../state/计算/六十四原子跨族闭包的一千二百八十四行精确点--计算.md)，前阶段[入口资源](../../../state/资源/跨续局必要行的共同目录闭包与版本入口--资源.md)同步补明四底层证据已经取得。原437支持、规范行前缀、旧恢复helper及十行offdiagonal复用已有同SHA副本，不重复保存。完整来源、blob、双冻结commit及依赖指纹见[manifest.json](manifest.json)。

| 源ID | 原件 | 字节 | 完整读取及责任 |
|---|---|---:|---|
| 4030817f5bbc725a0033 | [cross_family_closure.json](original/cross_family_closure.json) | 4066 | 全部64有理重赋权和全部标量；39正质量，严格O>2，未有精确对偶 |
| 74cda81824ddc671daac | [cross_family_closure.py](original/cross_family_closure.py) | 9431 | 437/10调用、新637/200公式、浮点LP、Fraction恢复、上下界分别认证和输出控制流全文 |
| eb225d17ce9dbc98a288 | [verified_cross_family_closure.json](original/verified_cross_family_closure.json) | 135558 | 全18顶层字段及全部1284有理slack逐项消费；57零，0负，3输入SHA完整匹配 |
| ce2bfc40b0afa827a26f | [verify_cross_family_closure.py](original/verify_cross_family_closure.py) | 7589 | 新837行独立索引求和/可行会员枚举、旧437共享规范行、旧10直接式、完整点审计和写出规则全文 |

合计156644B，两冻结提交中各文件字节相同。新取得四原件的指纹绑定当前阅读对象，不回填原历史进程。

## 复用的成熟成功

原verified报告已完整保存成功所需1284个slack和支持/primal/generator三个SHA，均与当前确切原件相同。新637行由原审计显式源/目标索引求和逐原子比较；200行对共享t的会员位枚举极值，64原子共9525候选。旧437使用原规范函数，旧10行使用旧直接实现，不能称与所有上游隔离的第二矩阵实现。

原验证程序导入发现器及旧helper，故实际需要NumPy/SciPy导入，数学审计虽仅用Fraction且不调用LP。两个原文件均有main guard：导入不执行其main，但会运行这条依赖初始化；原main会覆盖同目录JSON。当前没有导入或执行任何原入口。

原报告没有audit自身SHA、argv、环境/库版本、原stdout/stderr。保留其真实成功身份，不凭现有源码或本轮读取伪造历史重放。

## 一次新读取与绑定检查

[inspect_saved.py](inspect_saved.py)只用标准库，**不重算64×1284矩阵**。它核所有64原子字段/共享d/旧菜单可行域、64新Fraction质量、W/O/正差，逐项读1284个Fraction slack并核完整行名集合、零数和非负性；核三个输入SHA。另以各t组二项系数乘积计数9525，不重新枚举原9525候选。

在本目录可运行：

~~~sh
python3 inspect_saved.py original ../fixed-sixty-four-support-five-sixteen-primal-primary/source-root/evidence/certificates/customer_attraction/five_player_indexed_bound.json inspection.json
~~~

[完整读取结果](inspection.json)保全部64原子的质量/域/计数核对及四行族汇总；其非负符号检查指**已保存slack**，没有伪称重新逐系数计算。该报告的参考行名排列与原验证字典在基础437的索引389起不全相同，但行名集合相同，按名解释slack；64质量和原原子次序没有改。

实际仅执行这一新小检查一次，exit0：

~~~json
{"atoms":64,"positive":39,"slacks_read":1284,"zero_slacks":57,"alignments_by_count":9525,"W":"1","O":"27561041386503802625436146549175021295/13418535024241695702985876902501004326","input_bindings":"all_match","original_entry_runs":0}
~~~

另单独核64个分母的LCM，保存[形式原子整数化算术](integerization.json)：共同分母26837070048483391405971753805002008652。它不是完整客户目录/SPE构造。代码/输出SHA和执行计数另见[run-metadata.json](run-metadata.json)。

因此本轮原发现LP/main、原verify入口、规范SPE solver和优化器调用均0；未为重复而重跑成熟成功。当前工作补的是四源完整理解、数据消费和确切绑定，不新增外审/盲审、全空间最优或原游戏反例。
