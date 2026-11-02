# 统一可信价格与删位修复：五对父方原审计

这里保全R-ab4父方五份原Python、五份同名JSON、VALIDATION及workspace，共十二来源40653B；[source-manifest.json](source-manifest.json)保存每份来源ID、双冻结commit/path/blob、SHA与字节数。完整数学与适用域见[五审计程序正文](../../../state/程序/统一可信价格与删位修复的五份原始有理审计--程序.md)，旧核验门禁、审查稿SHA与历史身份见[版本登记](../../../state/资源/统一价格父方核验的版本与接续登记--资源.md)。

## 一次重放实际证明了什么

五原main于本次各执行一次，均exit0、stderr空，生成JSON与冻结报告逐字节相同。每项保存真实stdout/stderr、环境、起始时间、用时、原码与报告指纹；总账见[replay/summary.json](replay/summary.json)。没有执行新独立数学核、LP、随机搜索或完整策略验证器。代码不是新写的证明，重放也不为原作者历史进程补造旧环境记录。

| 原脚本 | 参数与输出的真实责任 | 原main本次次数 |
| --- | --- | ---: |
| audit_deletion_contract | n0…3的274目录、m2…5、29958最优无序元组、160085删二补锚检查；8960有符号纯账 | 1 |
| audit_uniform_bank_domain | m2…5非空marked共26真实可实现路径；2401价格网格；243纯代数输入 | 1 |
| audit_uniform_price_rows | m2…6的15条BAL末位BR目标；λ=(3,0,0,0)排旧上域 | 1 |
| audit_price_lower_cuts | m2…6的57条LOW目标；1296价格点；斜坡m2…50纯算术首次m7失败−2/7 | 1 |
| audit_signed_repair | 780向量中的133负成本；1560个以D>0为假设的强安全编译账 | 1 |

银行使用真实SPE结果集合求门槛，并以`ordered_outcomes(目标终局计数)`核指定顺序确可实现；这不是零长度终局恒真断言。LOW/BAL只需末位BR，早先正g说明其目标未必可信，不能作为半覆盖反例。signed的D>0是输入假设，没有新坏种子存在结论。

## 真正的导入依赖与副作用

三份游戏脚本在import时加载customer_attraction包；[dependency-manifest.json](dependency-manifest.json)精确绑定同冻结点的`__init__.py`、`model.py`、`exact.py`、`certificate.py`四文件。这四模块均全文实读。两个代数脚本只用标准库。所有五个文件有main guard，导入脚本本身不会调用run，但它们没有参数解析，执行`--help`仍会进入main并覆盖相邻JSON。

四模块保在`dependencies-original/customer_attraction/`；十二主源保在`original/`下的真实仓库相对路径。包初始化会导入certificate的定义；此次从未调用其证书扩展或完整IC验证函数。不要把模块被导入记成一次完整策略核验。

新入口[replay_parent_audits.py](replay_parent_audits.py)先核全部主源/依赖SHA，再在新临时根复制原路径布局；原三脚本的`__file__.parents[5]`因此仍正确。它按删位、银行、BAL、LOW、signed顺序各调用一次未改原main，保存标准流和JSON，并核字节相同，退出后删除隔离运行树。输出目录必须不存在：

```bash
python archives/customer-attraction/tools/evidence/uniform-price-parent-audits-primary/replay_parent_audits.py --output workspaces/replay-uniform-price-parent-audits-new
```

不关闭assert，不运行原件保存区中的main，不将当前仓库模块替换冻结模块。输出中的绝对运行目录只记录本次环境；复验用包内逻辑结构，不依赖旧scratch路径。

## 与一般数学的关系

五份报告全部保留scope字段：有限实现或系数代数，不是Q-CAG-HALF证明，也不证明坏种子存在。一般支撑函数、银行/LOW全参数构造、笛卡尔首次偏离后永久退出的完整历史策略、实价格分离和强安全条件编译在对应正式定理中分别证明。本组有限表只能核那些实现选择。

删位枚举的目录没有覆盖别名，但重复槽位保留；模型模块允许同覆盖不同标签。不能用有限目录枚举缩小当前模型。signed保负成本和零层，强安全保严格k阈值与t0分支；未把强安全B_sec换成半覆盖B。

[relation-review.json](relation-review.json)记实际实现、必要筛选、条件编译和版本关系，未修改共享图；[self-check.json](self-check.json)是来源、运行和链接的发布前自查，不代替正文中的数学判断。逐来源receipt由Boss3串行在checkpoint明确pushed之后提交。
